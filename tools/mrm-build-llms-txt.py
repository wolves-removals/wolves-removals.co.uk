#!/usr/bin/env python3
"""
Rebuild /llms.txt — the LLM-friendly site map proposed by Answer.AI
(https://llmstxt.org). One markdown file at the site root listing
every indexable page, grouped by section.

Re-run after adding or removing pages. Audit Rule 43 enforces that
every indexable page appears here, so the script is the source of
truth.

    python3 tools/build-llms-txt.py
"""

from __future__ import annotations
import glob, os, re, sys, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE_URL = 'https://www.markratcliffemoving.co.uk'

# (display heading, glob patterns). Ordered as they appear in llms.txt.
SECTIONS: list[tuple[str, list[str]]] = [
    ('Core pages',   ['*.html']),
    ('Services',     ['services/*.html']),
    ('Areas covered',['areas-covered/*.html']),
    ('Resources',    ['resources/*.html']),
    ('Blog',         ['blog/*.html']),
]

# Strip the brand suffix from <title> so the link text stays scannable.
# Order matters — longest match first.
BRAND_SUFFIXES = [
    ' | Mark Ratcliffe Moving & Storage',
    ' | Mark Ratcliffe Moving and Storage',
    ' | Mark Ratcliffe Moving',
    ' | Mark Ratcliffe',
    ' — Mark Ratcliffe Moving & Storage',
    ' — Mark Ratcliffe Moving',
    ' — Mark Ratcliffe',
    ' - Mark Ratcliffe Moving & Storage',
    ' - Mark Ratcliffe Moving',
    ' - Mark Ratcliffe',
]


def is_verification_stub(path: str) -> bool:
    name = os.path.basename(path)
    return ((name.startswith('google') and len(name) > 16)
            or name.startswith('BingSiteAuth')
            or name.startswith('yandex_'))


def is_indexable(path: str) -> bool:
    if is_verification_stub(path):
        return False
    try:
        with open(path, encoding='utf-8') as f:
            head = f.read(4096)
    except OSError:
        return False
    if 'http-equiv="refresh"' in head:
        return False
    if 'window.location.replace' in head:
        return False
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', head, re.I)
    if m and 'noindex' in m.group(1).lower():
        return False
    return True


def loc_for(path: str) -> str:
    if path == 'index.html':
        return BASE_URL + '/'
    if path.endswith('/index.html'):
        return BASE_URL + '/' + path[:-len('index.html')]
    return BASE_URL + '/' + path


def clean(text: str) -> str:
    """Decode entities, collapse whitespace, strip."""
    text = htmllib.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def display_title(raw: str) -> str:
    raw = clean(raw)
    for suf in BRAND_SUFFIXES:
        if raw.endswith(suf):
            return raw[: -len(suf)].strip(' |—-')
    return raw


def extract_meta(path: str) -> tuple[str, str]:
    """Return (title, description) for one HTML file."""
    try:
        html = open(path, encoding='utf-8').read()
    except OSError:
        return ('', '')
    t = re.search(r'<title>([^<]+)</title>', html, re.I)
    title = display_title(t.group(1)) if t else os.path.basename(path)
    d = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.I)
    desc = clean(d.group(1)) if d else ''
    return (title, desc)


def collect_section(patterns: list[str]) -> list[str]:
    paths: list[str] = []
    for pat in patterns:
        paths.extend(glob.glob(pat))
    return sorted(p for p in paths if os.path.isfile(p) and is_indexable(p))


def main() -> int:
    lines: list[str] = []
    lines.append('# Mark Ratcliffe Moving & Storage')
    lines.append('')
    lines.append('> Independent Sussex removals and storage company '
                 'established 2017, serving Eastbourne, Brighton, Hastings, '
                 'Worthing and the wider Sussex / Surrey / Kent area. '
                 'Full-service house and office moves, international '
                 '(UK ↔ Thailand) removals, packing, prestige steel storage '
                 'rooms, antique and fine-art handling. BS 8564 accredited.')
    lines.append('')
    lines.append('This file lists every indexable page on '
                 'https://www.markratcliffemoving.co.uk and is regenerated '
                 'by `tools/build-llms-txt.py` whenever pages are added or '
                 'removed (enforced by audit Rule 43).')
    lines.append('')

    grand_total = 0
    counts: list[tuple[str, int]] = []
    for heading, patterns in SECTIONS:
        paths = collect_section(patterns)
        if not paths:
            counts.append((heading, 0))
            continue
        lines.append(f'## {heading}')
        lines.append('')
        for p in paths:
            title, desc = extract_meta(p)
            url = loc_for(p)
            if desc:
                lines.append(f'- [{title}]({url}): {desc}')
            else:
                lines.append(f'- [{title}]({url})')
        lines.append('')
        counts.append((heading, len(paths)))
        grand_total += len(paths)

    open('llms.txt', 'w', encoding='utf-8').write('\n'.join(lines).rstrip() + '\n')

    for label, n in counts:
        print(f'  {label:14s}  {n:4d} pages')
    print('  ----------------------------')
    print(f'  Total           {grand_total:4d} pages in llms.txt')
    return 0


if __name__ == '__main__':
    sys.exit(main())
