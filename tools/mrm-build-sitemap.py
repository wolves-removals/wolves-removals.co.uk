#!/usr/bin/env python3
"""
Rebuild /sitemap.xml as a single flat <urlset> containing every
indexable HTML page on the site.

Each URL is tagged with a priority + changefreq derived from which
section it lives in (root / services / areas / resources / blog).

Run from the site root:
    python3 tools/build-sitemap.py
"""

from __future__ import annotations
import glob, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE_URL = 'https://www.markratcliffemoving.co.uk'

# (label, glob patterns, priority, changefreq). Order controls the
# section blocks in the output file (root first, then services, etc.).
SECTIONS = [
    ('root',      ['*.html'],                 '1.0', 'weekly'),
    ('services',  ['services/*.html'],        '0.8', 'monthly'),
    ('areas',     ['areas-covered/*.html'],   '0.8', 'monthly'),
    ('resources', ['resources/*.html'],       '0.7', 'monthly'),
    ('blog',      ['blog/*.html'],            '0.6', 'monthly'),
]

# Legacy sub-sitemap files left over from the previous index-based
# layout — removed if present so we don't confuse crawlers.
LEGACY_SUB_SITEMAPS = [
    'page-sitemap.xml',
    'services-sitemap.xml',
    'areas-sitemap.xml',
    'resources-sitemap.xml',
    'blog-sitemap.xml',
]


def is_indexable(path: str) -> bool:
    # Skip search-console verification stubs (one-line files whose content
    # must stay byte-exact for the provider — see audit.py for the same rule).
    name = os.path.basename(path)
    if (name.startswith('google') and len(name) > 16
            or name.startswith('BingSiteAuth')
            or name.startswith('yandex_')):
        return False
    try:
        with open(path, encoding='utf-8') as f:
            html = f.read(4096)
    except OSError:
        return False
    if 'http-equiv="refresh"' in html: return False
    if 'window.location.replace' in html: return False
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
    if m and 'noindex' in m.group(1).lower():
        return False
    return True


def loc_for(path: str) -> str:
    if path == 'index.html':
        return BASE_URL + '/'
    if path.endswith('/index.html'):
        return BASE_URL + '/' + path[:-len('index.html')]
    return BASE_URL + '/' + path


def lastmod_for(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()


def main() -> int:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    total = 0
    counts: list[tuple[str, int]] = []
    for label, patterns, priority, freq in SECTIONS:
        paths: list[str] = []
        for pat in patterns:
            paths.extend(glob.glob(pat))
        paths = sorted(p for p in paths if os.path.isfile(p) and is_indexable(p))
        counts.append((label, len(paths)))
        if paths:
            lines.append(f'  <!-- {label} ({len(paths)} URLs) -->')
        for p in paths:
            lines.append('  <url>')
            lines.append(f'    <loc>{loc_for(p)}</loc>')
            lines.append(f'    <lastmod>{lastmod_for(p)}</lastmod>')
            lines.append(f'    <changefreq>{freq}</changefreq>')
            lines.append(f'    <priority>{priority}</priority>')
            lines.append('  </url>')
            total += 1
    lines.append('</urlset>')
    lines.append('')
    open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines))

    # Tidy up the previous index + per-section sub-sitemaps so the
    # file tree mirrors the new single-file layout.
    removed = []
    for legacy in LEGACY_SUB_SITEMAPS:
        if os.path.exists(legacy):
            os.remove(legacy)
            removed.append(legacy)

    for label, n in counts:
        print(f'  {label:10s}  {n:3d} URLs')
    print(f'  ---------------------')
    print(f'  Total      {total:3d} URLs in sitemap.xml')
    if removed:
        print(f'\nRemoved legacy sub-sitemaps: {", ".join(removed)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
