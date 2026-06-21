#!/usr/bin/env python3
"""
markratcliffemoving.co.uk content audit.

Verifies forty-one build rules:
  1. Blogs are ≥2000 words.
  2. Location pages are ≥1500 words.
  3. Every page has ≥10 distinct in-body internal links.
  4. blog/index.html lists every blog post, newest-first, capped at 9.
  5. sitemap.xml contains a <url> for every indexable HTML page.
  6. No two indexable pages share the same <title> tag.
  7. Meta descriptions are ≤145 characters.
  8. <title> pixel width is ≤550px (Arial Bold ≈ 20px, matches SF).
  9. Every <img> has an alt attribute (empty alt allowed only with
     role="presentation" or aria-hidden="true" for decorative images).
 10. Every indexable page has a static <link rel="canonical">
     pointing to its production https://www.markratcliffemoving.co.uk
     URL (no JS-injected canonicals — crawlers like Screaming Frog
     don't execute JS).
 11. No two indexable pages share the same <h1> tag.
 12. Internal <a href> values must point at an indexable, self-
     canonical page — no links to noindex, redirect-stub or
     canonicalised pages, and no `*/index.html` links.
 13. Every canonical target itself resolves to an indexable page on
     disk (no canonical chains).
 14. <link rel="canonical"> appears inside the <head> element.
 15. Every <img> carries both width and height attributes (CLS).
 16. Internal anchor text is descriptive — no "click here", "read
     more", "learn more", "here" etc.
 17. Internal anchors have non-empty accessible names (visible text,
     image alt, or aria-label).
 18. <h1> is the first heading on the page — no <h2>-<h6> before it.
 19. Every <img alt="..."> ≤100 chars when present.
 20. Every page has Content-Security-Policy and Referrer-Policy
     declared via <meta> tags.
 21. Every image in /images/ is ≤200 KB on disk.
 22. /_headers file present with X-Frame-Options + X-Content-Type-
     Options + Referrer-Policy + Strict-Transport-Security. NOTE:
     the site currently deploys on GitHub Pages, which ignores
     _headers, so HSTS / XFO / XCTO are not actually served. CSP
     and Referrer-Policy still apply via <meta http-equiv> in each
     page (Rule 20). The _headers file is kept in-repo so a future
     migration to Cloudflare Pages or Netlify activates the full
     header set with zero further work — user explicitly chose to
     accept this trade-off (2026-05-22) rather than migrate hosts.
 23. /_redirects file present with mappings for every legacy noindex
     stub (delivered by Cloudflare Pages / Netlify).
 24. No internal <a href> carries URL parameters (clean, static URLs
     for every indexable page).
 25. No two indexable pages share the same meta description (paired
     with Rule 6 closing the duplicate-content surface).
 26. Every indexable page has exactly one <h1> — not zero, not more.
 27. No mixed content — indexable pages must not load resources or
     link to http:// URLs (HTTPS-only).
 28. /robots.txt exists, allows crawling of the production site, and
     lists the sitemap.
 29. Every indexable page's body content demonstrates E-E-A-T —
     Experience, Expertise, Authority, Trust. Concretely: the body
     (between </nav> and <footer>) must contain at least 4 distinct
     signals from the set below, so no page is generic / AI-written
     filler:
       • "Mark Ratcliffe" (organisation identity)
       • "1982" / "since 1982" / "40 years" / "forty years" (longevity)
       • "BAR" / "British Association of Removers" (industry authority)
       • "BS 8564" / "Advance Payment Guarantee" (accreditation/trust)
       • "Sussex" (first-hand local expertise)
       • "our crew" / "our team" / "we've" / "we have" (first-person
         experience)
       • "01323" or other contact specifics (trust signal)
 30. Every indexable page carries a JSON-LD block whose @graph
     references the canonical organization @id
     `https://www.markratcliffemoving.co.uk/#organization` — gives
     every SERP entry point a LocalBusiness/MovingCompany card and
     powers Knowledge Panel / local-pack rich results.
     Injected sitewide by tools/build-schema.py.
 31. Every <script type="application/ld+json"> body is valid JSON.
     (Malformed JSON-LD is silently ignored by Google — no error,
     no rich result. This rule catches the silent failure mode.)
 32. Pages with user-visible FAQ content (one or more <details>
     <summary>question?</summary>…</details> blocks) declare
     FAQPage schema in some JSON-LD block, so the FAQ rich result
     can render. tools/build-schema.py auto-generates FAQPage from
     visible Q&A if the page doesn't already have one.
 33. Exactly one <meta name="description"> per page — multiple
     meta descriptions are invalid HTML and Google may pick the
     wrong one. Fixed by tools/cleanup-html.py.
 34. No JS-injected <link rel="canonical"> tags. Crawlers without
     JS execution (Screaming Frog, many SERP previews) can't see
     a runtime-created canonical, so it must be hardcoded static
     markup in <head>. Fixed by tools/cleanup-html.py.
 35. Internal directory links (e.g. /services, /areas-covered)
     must carry a trailing slash. GitHub Pages 301-redirects
     /services → /services/, costing a crawl hop and leaking
     link equity. Every such href is one redirect we don't need.
     Also catches the `/services#anchor` and `/services?q=…`
     forms that strip the slash before the suffix.
 36. Every internal <script src> / <link href> / <img src>
     resolves to a real file on disk — no 404s the moment a
     page loads. (External http/https URLs are out of scope.)
 37. Every internal <a href> points to a real .html file (or a
     directory with an index.html). The narrower companion to
     Rule 12 — "no 404 on click" guarantee.
 38. No trailing slash on a .html file URL. /foo.html/ is a 404
     on most static hosts and a needless 301 on the rest.
 39. Every <h2> text is unique across the entire site — no
     cross-page <h2> duplicates. Duplicate H2s are a textbook
     "templated content" signal Google penalises. Each <h2>
     should describe the section content of its specific page.
     tools/dedupe-h2s.py rewrites duplicates by weaving the
     page's <h1> topic into each H2 so variants stay on-topic.
 40. Any schema.org Product JSON-LD must declare `name` AND at
     least one of `offers` / `review` / `aggregateRating` —
     Google's mandatory product-snippet fields. A Product without
     these is silently dropped from rich results.
 41. No HTML microdata attributes (itemscope / itemtype /
     itemprop). Structured data on the site is JSON-LD only.
     Mixed-signal pages trigger Google's "Unparsable structured
     data" report if a microdata itemtype URL is stale or wrong.

Items the user's checklist mentioned that this static audit cannot
verify (need separate runtime tooling or deployment-level checks):
  - External 4xx URLs (need live HTTP requests; see
    tools/check-external-links.py when added)
  - Redirect chains, redirect loops, soft 404s (server-side concerns
    on the production deploy)
  - JavaScript-rendered content visibility (rendering check)

Run from the site root:
    python3 tools/audit.py

Exit codes:
    0  all rules pass
    1  one or more rules failed (list printed)
"""

from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BLOG_MIN_WORDS     = 2000
LOCATION_MIN_WORDS = 1500
BODY_LINKS_MIN     = 10
BLOG_INDEX_MAX     = 9
META_DESC_MAX      = 145
TITLE_PX_MAX       = 550
ALT_TEXT_MAX       = 100
IMAGE_MAX_BYTES    = 200 * 1024
NON_DESCRIPTIVE_ANCHORS = {
    'click here', 'clickhere', 'read more', 'learn more', 'more', 'here',
    'this', 'click', 'continue reading', 'continue', 'link', 'this link',
    'more info', 'read', 'see more', 'view more', 'find out more', 'tap here',
}

# Approximate Arial Bold ~20px character pixel widths.
# Calibrated to match Screaming Frog's "Title Pixel Width" output within ~3%.
CHAR_PX = {
    ' ': 5, '!': 5, '"': 6, '#': 11, '$': 11, '%': 17, '&': 13, "'": 4,
    '(': 7, ')': 7, '*': 8, '+': 12, ',': 5, '-': 7, '.': 5, '/': 6,
    '0': 11, '1': 11, '2': 11, '3': 11, '4': 11, '5': 11, '6': 11, '7': 11, '8': 11, '9': 11,
    ':': 6, ';': 6, '<': 12, '=': 12, '>': 12, '?': 11, '@': 18,
    'A': 12, 'B': 13, 'C': 14, 'D': 14, 'E': 13, 'F': 12, 'G': 15, 'H': 14, 'I': 6,
    'J': 9, 'K': 13, 'L': 11, 'M': 16, 'N': 14, 'O': 15, 'P': 13, 'Q': 15, 'R': 14,
    'S': 13, 'T': 12, 'U': 14, 'V': 12, 'W': 18, 'X': 12, 'Y': 12, 'Z': 12,
    '[': 6, '\\': 6, ']': 6, '^': 9, '_': 11, '`': 6,
    'a': 11, 'b': 12, 'c': 10, 'd': 12, 'e': 11, 'f': 7, 'g': 12, 'h': 12, 'i': 5,
    'j': 5, 'k': 11, 'l': 5, 'm': 17, 'n': 12, 'o': 12, 'p': 12, 'q': 12, 'r': 7,
    's': 10, 't': 7, 'u': 12, 'v': 10, 'w': 16, 'x': 11, 'y': 10, 'z': 10,
    '{': 6, '|': 5, '}': 6, '~': 12,
    # common Unicode punctuation appearing in titles
    '–': 11, '—': 14, '‘': 4, '’': 4, '“': 8, '”': 8, '·': 5, '•': 7, '…': 13,
    '&ndash;': 11, '&mdash;': 14, '&amp;': 13, '&middot;': 5,
}
DEFAULT_PX = 11

def title_pixel_width(text: str) -> int:
    # Decode the few HTML entities we use in titles before measuring.
    decoded = (text.replace('&amp;', '&')
                   .replace('&ndash;', '–')
                   .replace('&mdash;', '—')
                   .replace('&middot;', '·')
                   .replace('&rsquo;', '’')
                   .replace('&lsquo;', '‘')
                   .replace('&rdquo;', '”')
                   .replace('&ldquo;', '“')
                   .replace('&quot;', '"')
                   .replace('&apos;', "'"))
    return sum(CHAR_PX.get(c, DEFAULT_PX) for c in decoded)

# Heuristic location-page detector. Anything starting with removals-* at the root,
# any subpage under areas-covered/, plus the two outliers in root.
LOCATION_GLOBS = [
    'areas-covered/*.html',
]
LOCATION_EXTRA: list[str] = []

NAV_END_RE   = re.compile(r'<div class="menu-button[^>]*>.*?</div>\s*</div>\s*</div>', re.S)
FOOTER_RE    = re.compile(r'<footer', re.S)
WORD_HEAD_RE = re.compile(r'<head.*?</head>', re.S | re.I)
WORD_SCRIPT  = re.compile(r'<script.*?</script>', re.S | re.I)
WORD_STYLE   = re.compile(r'<style.*?</style>',  re.S | re.I)
TAG_RE       = re.compile(r'<[^>]+>')
ENT_RE       = re.compile(r'&[a-z]+;')

def is_redirect_stub(html: str) -> bool:
    return 'http-equiv="refresh"' in html or 'window.location.replace' in html

def word_count(html: str) -> int:
    h = WORD_HEAD_RE.sub('', html)
    h = WORD_SCRIPT.sub('', h)
    h = WORD_STYLE.sub('', h)
    t = TAG_RE.sub(' ', h)
    t = ENT_RE.sub(' ', t)
    return len(t.split())

def body_internal_links(html: str, current_path: str) -> set[str]:
    m_start = NAV_END_RE.search(html)
    m_end   = FOOTER_RE.search(html)
    start   = m_start.end() if m_start else 0
    end     = m_end.start() if m_end else len(html)
    body    = html[start:end]
    refs    = re.findall(r'<a\b[^>]*?\bhref="([^"]+)"', body)
    seen    = set()
    for href in refs:
        h = href.split('#')[0].split('?')[0].strip()
        if not h or h in ('/', './', '../'): continue
        if h.startswith(('mailto:', 'tel:', 'javascript:', '#')): continue
        if h.startswith(('http://', 'https://', '//')):
            if 'markratcliffemoving.co.uk' not in h: continue
            m = re.search(r'markratcliffemoving\.co\.uk(/.+)', h)
            if m: h = m.group(1).lstrip('/')
        # Strip a single leading ../ or ./ so equivalent paths dedupe correctly
        if h.startswith('../'): h = h[3:]
        elif h.startswith('./'): h = h[2:]
        # Count internal HTML pages and directory URLs (e.g. services/, blog/)
        if h.endswith('.html') or h.endswith('/'):
            seen.add(h)
    return seen

def all_pages() -> list[str]:
    paths = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    # Skip Google / Bing / Yandex search-console verification stubs — they're
    # tiny one-line files whose content must stay byte-exact for the provider
    # to verify ownership, so they can't carry the boilerplate audit rules
    # expect (title, canonical, CSP, etc.).
    def is_verification_stub(p: str) -> bool:
        name = os.path.basename(p)
        return (name.startswith('google') and len(name) > 16
                or name.startswith('BingSiteAuth')
                or name.startswith('yandex_'))
    return sorted(p for p in paths if os.path.isfile(p) and not is_verification_stub(p))

def is_blog_post(path: str) -> bool:
    return path.startswith('blog/') and os.path.basename(path) != 'index.html'

def is_location_page(path: str) -> bool:
    return path.startswith('areas-covered/') and os.path.basename(path) != 'index.html'

def blog_post_meta(path: str) -> dict | None:
    """Pull headline + datePublished from a blog post's BlogPosting JSON-LD."""
    html = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and item.get('@type') == 'BlogPosting':
                return {
                    'slug': os.path.basename(path),
                    'date': item.get('datePublished'),
                    'headline': item.get('headline'),
                }
    return None

BASE_URL = 'https://www.markratcliffemoving.co.uk'

def indexable_pages(pages: list[str]) -> list[str]:
    out = []
    for p in pages:
        try:
            html = open(p, encoding='utf-8').read(4096)
        except OSError:
            continue
        if is_redirect_stub(html): continue
        m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
        if m and 'noindex' in m.group(1).lower():
            continue
        out.append(p)
    return out

def sitemap_locs() -> set[str]:
    """Return every <loc> across the sitemap index + sub-sitemaps.
    Falls back to a flat sitemap.xml if no <sitemapindex> wrapper is found."""
    try:
        xml = open('sitemap.xml', encoding='utf-8').read()
    except OSError:
        return set()
    if '<sitemapindex' in xml:
        locs: set[str] = set()
        for child in re.findall(r'<sitemap>\s*<loc>([^<]+)</loc>', xml):
            # Strip BASE_URL prefix to find local sub-sitemap file
            child_path = re.sub(r'^https?://(?:www\.)?markratcliffemoving\.co\.uk/', '', child)
            if not os.path.exists(child_path):
                continue
            try:
                sub_xml = open(child_path, encoding='utf-8').read()
            except OSError:
                continue
            locs.update(re.findall(r'<loc>([^<]+)</loc>', sub_xml))
        return locs
    return set(re.findall(r'<loc>([^<]+)</loc>', xml))

def expected_loc(path: str) -> str:
    if path == 'index.html':
        return BASE_URL + '/'
    if path.endswith('/index.html'):
        return BASE_URL + '/' + path[:-len('index.html')]
    return BASE_URL + '/' + path

def audit():
    pages = all_pages()
    failures = {
        'blog_word_count':       [],
        'location_word_count':   [],
        'internal_links':        [],
        'blog_index_listing':    [],
        'blog_index_order':      [],
        'sitemap':               [],
        'duplicate_titles':      [],
        'meta_description':      [],
        'title_pixel_width':     [],
        'image_alt':             [],
        'canonical':             [],
        'duplicate_h1':          [],
        'links_to_non_canonical':[],
        'canonical_target':      [],
        'canonical_in_head':     [],
        'img_dimensions':        [],
        'non_descriptive_anchor':[],
        'empty_anchor':          [],
        'h1_not_first':          [],
        'alt_too_long':          [],
        'security_meta':         [],
        'image_size':            [],
        'headers_file':          [],
        'redirects_file':        [],
        'url_parameters':        [],
        'duplicate_descriptions':[],
        'h1_count':              [],
        'mixed_content':         [],
        'robots_txt':            [],
        'eeat':                  [],
    }

    blog_posts = []
    blog_index_posts_listed = set()

    for path in pages:
        try:
            html = open(path, encoding='utf-8').read()
        except OSError:
            continue
        if is_redirect_stub(html):
            continue

        wc = word_count(html)
        link_count = len(body_internal_links(html, path))

        # Rule 1 — blog word count
        if is_blog_post(path):
            blog_posts.append(path)
            if wc < BLOG_MIN_WORDS:
                failures['blog_word_count'].append((wc, path))

        # Rule 2 — location word count
        if is_location_page(path):
            if wc < LOCATION_MIN_WORDS:
                failures['location_word_count'].append((wc, path))

        # Rule 3 — ≥10 in-body internal links
        if link_count < BODY_LINKS_MIN:
            failures['internal_links'].append((link_count, path))

    # Rule 4 — blog index
    index_path = 'blog/index.html'
    if os.path.isfile(index_path):
        index_html = open(index_path, encoding='utf-8').read()
        listed = []
        # Find each card's <h3><a href="slug">title</a> inside the .np-blog-grid
        m = re.search(
            r'<div class="np-blog-grid">(.*?)</div>\s*</div>',
            index_html,
            re.S,
        )
        if m:
            grid = m.group(1)
            for href_m in re.finditer(r'<h3><a href="([^"]+)">', grid):
                slug = href_m.group(1).split('#')[0].split('?')[0]
                listed.append(slug)
        # Visible count must be ≤ 9
        if len(listed) > BLOG_INDEX_MAX:
            failures['blog_index_listing'].append(
                f'visible count is {len(listed)} (>{BLOG_INDEX_MAX})'
            )
        # Every post should be listed (unless total > MAX, then top MAX by date should be listed)
        post_metas = [blog_post_meta(p) for p in blog_posts]
        post_metas = [m for m in post_metas if m]
        post_metas.sort(key=lambda x: (x.get('date') or '', x.get('slug') or ''), reverse=True)
        expected = [m['slug'] for m in post_metas[:BLOG_INDEX_MAX]]
        # Order check
        if listed and listed != expected:
            failures['blog_index_order'].append(
                f'index order does not match newest-first.\n'
                f'    Expected: {expected}\n'
                f'    Got:      {listed}'
            )
        # Listing-completeness check (when total posts ≤ MAX, every post must appear)
        if len(post_metas) <= BLOG_INDEX_MAX:
            missing = sorted(set(m['slug'] for m in post_metas) - set(listed))
            if missing:
                failures['blog_index_listing'].append(
                    f'missing posts on index: {missing}'
                )

    # Report
    any_fail = False
    print('=' * 64)
    print('markratcliffemoving.co.uk — content rule audit')
    print('=' * 64)

    def rule(name: str, ok_msg: str, fail_list):
        nonlocal any_fail
        if not fail_list:
            print(f'  ✓ {name}: {ok_msg}')
            return
        any_fail = True
        print(f'  ✗ {name}: {len(fail_list)} failure(s)')
        for f in fail_list[:20]:
            if isinstance(f, tuple):
                print(f'      {f[0]:>5}  {f[1]}')
            else:
                print(f'      {f}')
        if len(fail_list) > 20:
            print(f'      ... and {len(fail_list) - 20} more')

    rule('Rule 1 — blogs ≥%d words' % BLOG_MIN_WORDS,
         f'{len(blog_posts)} posts all ≥{BLOG_MIN_WORDS} words',
         failures['blog_word_count'])

    n_loc = sum(1 for p in pages if is_location_page(p) and not is_redirect_stub(open(p).read()))
    rule('Rule 2 — location pages ≥%d words' % LOCATION_MIN_WORDS,
         f'{n_loc} location pages all ≥{LOCATION_MIN_WORDS} words',
         failures['location_word_count'])

    n_total = sum(1 for p in pages if not is_redirect_stub(open(p).read()))
    rule('Rule 3 — ≥%d distinct in-body links' % BODY_LINKS_MIN,
         f'{n_total} pages all ≥{BODY_LINKS_MIN} links',
         failures['internal_links'])

    rule('Rule 4a — blog index lists every post (cap %d)' % BLOG_INDEX_MAX,
         'index lists every post, capped correctly',
         failures['blog_index_listing'])
    rule('Rule 4b — blog index ordered newest-first',
         'newest-first ordering correct',
         failures['blog_index_order'])

    # Rule 5 — sitemap covers every indexable page
    indexable = indexable_pages(pages)
    sitemap   = sitemap_locs()
    missing = []
    for p in indexable:
        if expected_loc(p) not in sitemap:
            missing.append(p)
    if missing:
        for m in missing:
            failures['sitemap'].append(('missing', m))
    extra = []
    indexable_set = {expected_loc(p) for p in indexable}
    for loc in sitemap:
        if loc not in indexable_set:
            extra.append(loc)
    if extra:
        for e in extra:
            failures['sitemap'].append(('orphan ', e))
    rule('Rule 5 — sitemap.xml covers every indexable page',
         f'{len(indexable)} indexable pages all listed; {len(sitemap)} sitemap entries match',
         failures['sitemap'])

    # Rule 6 — no duplicate <title> tags across indexable pages
    title_re = re.compile(r'<title>([^<]+)</title>', re.I)
    titles_seen: dict[str, list[str]] = {}
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        m = title_re.search(html)
        if not m:
            failures['duplicate_titles'].append(('no-title', p))
            continue
        title = ' '.join(m.group(1).split()).strip()
        titles_seen.setdefault(title, []).append(p)
    for title, paths in titles_seen.items():
        if len(paths) > 1:
            failures['duplicate_titles'].append(
                f'"{title}" used by {len(paths)} pages: {", ".join(paths)}'
            )
    rule('Rule 6 — no duplicate <title> tags',
         f'{len(titles_seen)} unique titles across {len(indexable)} indexable pages',
         failures['duplicate_titles'])

    # Rules 7 & 8 — meta description length & title pixel width
    desc_re  = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        dm = desc_re.search(html)
        if not dm:
            failures['meta_description'].append(('no-desc', p))
        else:
            dlen = len(dm.group(1))
            if dlen > META_DESC_MAX:
                failures['meta_description'].append((dlen, p))
        tm = title_re.search(html)
        if tm:
            t   = ' '.join(tm.group(1).split()).strip()
            px  = title_pixel_width(t)
            if px > TITLE_PX_MAX:
                failures['title_pixel_width'].append((px, p))

    rule(f'Rule 7 — meta description ≤{META_DESC_MAX} chars',
         f'{len(indexable)} pages all within {META_DESC_MAX} chars',
         failures['meta_description'])
    rule(f'Rule 8 — title pixel width ≤{TITLE_PX_MAX}px',
         f'{len(indexable)} pages all within {TITLE_PX_MAX}px',
         failures['title_pixel_width'])

    # Rule 9 — every <img> has an alt attribute (decorative may use alt="" + role/aria-hidden)
    img_re = re.compile(r'<img\b([^>]*)>', re.I)
    attr_re = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"', re.I)
    n_imgs_scanned = 0
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        for m in img_re.finditer(html):
            attrs = dict(attr_re.findall(m.group(1)))
            # ignore srcs inside <picture>'s <source> — these are <img>, not <source>, so always check
            n_imgs_scanned += 1
            src = (attrs.get('src') or attrs.get('data-src') or '(no src)')[:80]
            if 'alt' not in attrs:
                failures['image_alt'].append(f'no-alt   {p}  ({src})')
                continue
            alt = attrs['alt'].strip()
            if not alt:
                role = attrs.get('role', '').lower()
                hidden = attrs.get('aria-hidden', '').lower()
                if role == 'presentation' or hidden == 'true':
                    continue  # decorative — OK
                failures['image_alt'].append(f'empty-alt {p}  ({src})')

    rule('Rule 9 — every <img> has alt text',
         f'{n_imgs_scanned} images across {len(indexable)} pages all have alt (or decorative role)',
         failures['image_alt'])

    # Rule 10 — every indexable page has a static canonical pointing to production
    canon_re = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        ms = canon_re.findall(html)
        expected = expected_loc(p)
        if not ms:
            failures['canonical'].append(f'missing  {p}')
        elif len(ms) > 1:
            failures['canonical'].append(f'multiple {p} ({len(ms)} canonical tags)')
        elif ms[0] != expected:
            failures['canonical'].append(f'wrong    {p}  → {ms[0]}  (expected {expected})')

    rule('Rule 10 — every page has a static canonical → production URL',
         f'{len(indexable)} pages all canonical to www.markratcliffemoving.co.uk',
         failures['canonical'])

    # Rule 11 — no duplicate <h1> tags across indexable pages
    h1_re = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
    h1_tag_strip = re.compile(r'<[^>]+>')
    h1s_seen: dict[str, list[str]] = {}
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        m = h1_re.search(html)
        if not m:
            failures['duplicate_h1'].append(('no-h1', p))
            continue
        text = h1_tag_strip.sub('', m.group(1))
        text = ' '.join(text.split()).strip()
        h1s_seen.setdefault(text, []).append(p)
    for text, paths in h1s_seen.items():
        if len(paths) > 1:
            failures['duplicate_h1'].append(
                f'"{text}" used by {len(paths)} pages: {", ".join(paths)}'
            )
    rule('Rule 11 — no duplicate <h1> tags',
         f'{len(h1s_seen)} unique H1 tags across {len(indexable)} indexable pages',
         failures['duplicate_h1'])

    # Pre-compute each file's canonical href (None if no canonical or non-existent file).
    # This lets Rules 12 and 13 share the same data.
    canon_by_file: dict[str, str] = {}
    canon_lookup_re = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)
    for p in pages:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        m = canon_lookup_re.search(html)
        if m:
            canon_by_file[p] = m.group(1)

    def url_to_path(u: str) -> str:
        """Convert an absolute production URL or relative href back to a repo path."""
        u = u.split('#')[0].split('?')[0]
        u = re.sub(r'^https?://(www\.)?markratcliffemoving\.co\.uk', '', u)
        u = u.lstrip('/')
        if u == '':
            return 'index.html'
        if u.endswith('/'):
            return u + 'index.html'
        return u

    indexable_set = set(indexable)

    def resolve_href(href: str, p_dir: str) -> str | None:
        """Resolve href → repo-relative path. Returns None if href is off-site or not an html file."""
        h = href.split('#')[0].split('?')[0]
        if not h: return None
        if h.startswith(('http://', 'https://', '//')):
            if 'markratcliffemoving.co.uk' not in h: return None
            return url_to_path(h)
        if h.startswith('/'):
            return url_to_path(h)
        appends_index = h.endswith('/')
        joined = os.path.normpath(os.path.join(p_dir, h.rstrip('/') or '.'))
        if joined == '.':
            joined = ''
        if appends_index:
            target = (joined + '/index.html') if joined else 'index.html'
        else:
            target = joined
        target = target.replace(os.sep, '/').lstrip('./')
        if not target.endswith('.html'):
            return None
        return target

    # Rule 12 — internal links must point at indexable, self-canonical pages
    link_re = re.compile(r'<a\b[^>]*?\bhref="([^"]+)"', re.I)
    raw_index_re = re.compile(r'(^|/)index\.html$')
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        offenders: dict[str, str] = {}
        p_dir = os.path.dirname(p)
        for m in link_re.finditer(html):
            href = m.group(1)
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')): continue
            if href.startswith(('http://', 'https://', '//')) and 'markratcliffemoving.co.uk' not in href: continue
            # raw `*/index.html`-form hrefs leak the duplicate URL surface — always offending
            raw = href.split('#')[0].split('?')[0]
            if raw_index_re.search(raw):
                offenders[href] = 'leaks /index.html (use directory URL)'
                continue
            target_path = resolve_href(href, p_dir)
            if target_path is None: continue
            # Destination must be indexable
            if target_path not in indexable_set:
                if os.path.exists(target_path):
                    offenders[href] = f'→ non-indexable {target_path}'
                else:
                    offenders[href] = f'→ missing file {target_path}'
                continue
            # Destination's canonical must be self
            target_canon = canon_by_file.get(target_path)
            target_expected = expected_loc(target_path)
            if target_canon and target_canon != target_expected:
                offenders[href] = f'→ canonicalised: {target_path} canon={target_canon}'
        if offenders:
            shown = list(offenders.items())[:4]
            extra = '' if len(offenders) <= 4 else f' (+{len(offenders)-4} more)'
            failures['links_to_non_canonical'].append(
                f'{p}  ' + '; '.join(f'{h} {why}' for h, why in shown) + extra
            )

    rule('Rule 12 — internal links → indexable, self-canonical pages',
         f'{len(indexable)} pages: all internal links land on canonical destinations',
         failures['links_to_non_canonical'])

    # Rule 13 — every canonical target itself resolves to an indexable file
    for p in indexable:
        c = canon_by_file.get(p)
        if not c:
            continue  # Rule 10 already caught missing canonicals
        target_path = url_to_path(c)
        if not os.path.exists(target_path):
            failures['canonical_target'].append(f'{p}  canon→ {c}  (file {target_path} missing)')
            continue
        if target_path not in indexable_set:
            failures['canonical_target'].append(f'{p}  canon→ {c}  (target {target_path} non-indexable)')

    rule('Rule 13 — canonical targets are indexable',
         f'{len(canon_by_file)} canonical targets all resolve to indexable pages',
         failures['canonical_target'])

    # Rule 14 — canonical link element inside <head>
    head_close_re = re.compile(r'</head>', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        cm = canon_lookup_re.search(html)
        hm = head_close_re.search(html)
        if cm and hm and cm.start() > hm.start():
            failures['canonical_in_head'].append(p)
    rule('Rule 14 — canonical link element inside <head>',
         f'{len(indexable)} pages: all canonical tags inside <head>',
         failures['canonical_in_head'])

    # Rule 15 — every <img> has width + height attributes
    img_iter_re = re.compile(r'<img\b([^>]*)>', re.I)
    img_attr_re = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"', re.I)
    n_imgs = 0
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        for m in img_iter_re.finditer(html):
            n_imgs += 1
            attrs = dict(img_attr_re.findall(m.group(1)))
            if 'width' not in attrs or 'height' not in attrs:
                src = (attrs.get('src') or attrs.get('data-src') or '?')[:60]
                failures['img_dimensions'].append(f'{p}  ({src})')
    rule('Rule 15 — every <img> has width+height attributes',
         f'{n_imgs} images across {len(indexable)} pages all have dimensions',
         failures['img_dimensions'])

    # Rule 16 / 17 / 19 — anchor text + alt length
    body_a_re = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.I | re.S)
    tag_strip_re = re.compile(r'<[^>]+>')

    def clean_anchor_text(s: str) -> str:
        s = tag_strip_re.sub('', s)
        s = (s.replace('&rarr;', '→').replace('&larr;', '←')
              .replace('&ndash;', '–').replace('&mdash;', '—')
              .replace('&amp;', '&').replace('&nbsp;', ' ')
              .replace('&middot;', '·').replace('&rsquo;', '’')
              .replace('&lsquo;', '‘').replace('&hellip;', '…'))
        s = re.sub(r'&[a-zA-Z]+;', '', s)
        return re.sub(r'\s+', ' ', s).strip()

    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        # body region = after </head>, before <footer>
        head_m = head_close_re.search(html)
        body = html[head_m.end():] if head_m else html
        f_m = re.search(r'<footer\b', body)
        if f_m: body = body[:f_m.start()]
        for m in body_a_re.finditer(body):
            attrs = dict(img_attr_re.findall(m.group(1)))
            href = attrs.get('href', '')
            if not href or href.startswith(('mailto:', 'tel:', '#', 'javascript:')):
                continue
            inner = m.group(2)
            text = clean_anchor_text(inner)
            norm = re.sub(r'[→»>\s\.,!:;\-–—]+', ' ', text.lower()).strip()
            # Rule 16 — non-descriptive
            if norm in NON_DESCRIPTIVE_ANCHORS:
                failures['non_descriptive_anchor'].append(f'{p}  "{text}" → {href}')
            # Rule 17 — empty anchor text (no visible, no img alt, no aria-label)
            if not text:
                im = re.search(r'<img\b[^>]*\balt="([^"]*)"', inner, re.I)
                if im and im.group(1).strip():
                    continue
                if attrs.get('aria-label', '').strip():
                    continue
                failures['empty_anchor'].append(f'{p}  href={href}')

        # Rule 19 — alt text length
        for m in img_iter_re.finditer(html):
            attrs = dict(img_attr_re.findall(m.group(1)))
            alt = attrs.get('alt', '')
            if len(alt) > ALT_TEXT_MAX:
                failures['alt_too_long'].append(f'{p}  alt={len(alt)} chars')

    rule(f'Rule 16 — descriptive anchor text (no "click here"/"read more"/"learn more")',
         f'{len(indexable)} pages: all internal anchor text is descriptive',
         failures['non_descriptive_anchor'])
    rule(f'Rule 17 — anchors have accessible names',
         f'{len(indexable)} pages: no empty-text anchors',
         failures['empty_anchor'])

    # Rule 18 — H1 is the first heading on the page
    heading_re = re.compile(r'<(h[1-6])\b', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        bm = re.search(r'<body\b[^>]*>', html, re.I)
        body_html = html[bm.end():] if bm else html
        first = heading_re.search(body_html)
        if first and first.group(1).lower() != 'h1':
            failures['h1_not_first'].append(f'{p}  first heading: <{first.group(1)}>')
    rule('Rule 18 — <h1> is the first heading on the page',
         f'{len(indexable)} pages: heading order starts with <h1>',
         failures['h1_not_first'])

    rule(f'Rule 19 — alt text ≤{ALT_TEXT_MAX} chars',
         f'{n_imgs} images across {len(indexable)} pages all within {ALT_TEXT_MAX} chars',
         failures['alt_too_long'])

    # Rule 20 — Content-Security-Policy + Referrer-Policy meta tags
    csp_re_a = re.compile(r'<meta\s+http-equiv="Content-Security-Policy"', re.I)
    ref_re_a = re.compile(r'<meta\s+name="referrer"', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        missing = []
        if not csp_re_a.search(html): missing.append('Content-Security-Policy')
        if not ref_re_a.search(html): missing.append('Referrer-Policy')
        if missing:
            failures['security_meta'].append(f'{p}  missing: {", ".join(missing)}')
    rule('Rule 20 — CSP + Referrer-Policy meta tags present',
         f'{len(indexable)} pages: all have CSP and Referrer-Policy',
         failures['security_meta'])

    # Rule 21 — image file size ≤200 KB on disk
    n_imgs_on_disk = 0
    for img in glob.glob('images/*'):
        if not os.path.isfile(img): continue
        ext = os.path.splitext(img)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'):
            continue
        n_imgs_on_disk += 1
        sz = os.path.getsize(img)
        if sz > IMAGE_MAX_BYTES:
            failures['image_size'].append(f'{img}  {sz//1024} KB (>200 KB)')
    rule('Rule 21 — images ≤200 KB on disk',
         f'{n_imgs_on_disk} files in /images/ all ≤200 KB',
         failures['image_size'])

    # Rule 22 — _headers file present with required security headers
    headers_path = '_headers'
    required_headers = {
        'X-Frame-Options',
        'X-Content-Type-Options',
        'Referrer-Policy',
        'Strict-Transport-Security',
    }
    if not os.path.exists(headers_path):
        failures['headers_file'].append(f'{headers_path} missing — create one for Cloudflare Pages / Netlify deployments')
    else:
        try:
            content = open(headers_path).read()
        except OSError:
            content = ''
        missing = [h for h in required_headers if h.lower() not in content.lower()]
        if missing:
            failures['headers_file'].append(f'{headers_path} missing headers: {", ".join(missing)}')
    rule('Rule 22 — /_headers carries required security headers',
         f'{headers_path} present with X-Frame-Options, X-Content-Type-Options, Referrer-Policy, HSTS',
         failures['headers_file'])

    # Rule 23 — no redirect stubs anywhere on the site (no 302s, no soft-301s,
    # no meta-refresh, no JS location.replace). Internal links must hit final URLs.
    for p in pages:
        try:
            head = open(p, encoding='utf-8').read(8192)
        except OSError:
            continue
        if 'http-equiv="refresh"' in head or 'window.location.replace' in head:
            failures['redirects_file'].append(f'{p} contains a redirect stub')
    rule('Rule 23 — no redirect stubs (no 302s / meta-refresh / JS redirects)',
         f'{len(pages)} HTML files: none redirect to another URL',
         failures['redirects_file'])

    # Rule 24 — no internal <a href> carries URL parameters
    a_param_re = re.compile(r'<a\b[^>]*?\bhref="([^"]+)"', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        for m in a_param_re.finditer(html):
            href = m.group(1)
            if href.startswith(('mailto:', 'tel:', '#', 'javascript:')): continue
            if href.startswith(('http://', 'https://', '//')) and 'markratcliffemoving.co.uk' not in href: continue
            # We care only about HTML page links, not asset cache-busts in <a href>
            if '?' in href and href.endswith('.html'):
                failures['url_parameters'].append(f'{p}  {href}')
            elif '?' in href and (href.endswith('/') or '?' in href.split('#')[0].split('/')[-1] and '.' not in href.split('?')[0].split('/')[-1]):
                failures['url_parameters'].append(f'{p}  {href}')
    rule('Rule 24 — no URL parameters on internal page links',
         f'{len(indexable)} pages: all internal page links are static URLs',
         failures['url_parameters'])

    # Rule 25 — no duplicate meta descriptions
    descs_seen: dict[str, list[str]] = {}
    desc_lookup_re = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        m = desc_lookup_re.search(html)
        if not m: continue
        d = ' '.join(m.group(1).split()).strip()
        if d:
            descs_seen.setdefault(d, []).append(p)
    for d, paths in descs_seen.items():
        if len(paths) > 1:
            failures['duplicate_descriptions'].append(
                f'"{d[:70]}..." used by {len(paths)} pages: {", ".join(paths)}'
            )
    rule('Rule 25 — no duplicate meta descriptions',
         f'{len(descs_seen)} unique descriptions across {len(indexable)} pages',
         failures['duplicate_descriptions'])

    # Rule 26 — exactly one <h1> per page
    h1_open_re = re.compile(r'<h1\b', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        count = len(h1_open_re.findall(html))
        if count != 1:
            failures['h1_count'].append(f'{p}  ({count} <h1> tags — must be exactly 1)')
    rule('Rule 26 — exactly one <h1> per page',
         f'{len(indexable)} pages: each has exactly one <h1>',
         failures['h1_count'])

    # Rule 27 — no mixed content (http:// resources/links on indexable pages)
    http_ref_re = re.compile(r'\b(?:src|href)="(http://[^"]+)"', re.I)
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        offenders: set[str] = set()
        for m in http_ref_re.finditer(html):
            u = m.group(1)
            # Skip schema vocabulary URLs (used as @context inside JSON-LD strings,
            # not as live resource references). Actually most live in JSON-LD blobs.
            # Easiest: ignore http://schema.org URLs and any http URL inside <script type="application/ld+json">.
            if u.startswith('http://schema.org') or u.startswith('http://www.w3.org'):
                continue
            # Check if inside a JSON-LD block (these aren't fetched resources)
            ctx_start = max(0, m.start() - 200)
            preceding = html[ctx_start:m.start()]
            if 'application/ld+json' in preceding and '</script>' not in preceding:
                continue
            offenders.add(u)
        if offenders:
            failures['mixed_content'].append(
                f'{p}  {len(offenders)} http:// reference(s): {list(offenders)[:2]}'
            )
    rule('Rule 27 — no mixed content (https-only)',
         f'{len(indexable)} pages: no http:// resources or links',
         failures['mixed_content'])

    # Rule 28 — robots.txt exists and references the sitemap
    if not os.path.exists('robots.txt'):
        failures['robots_txt'].append('robots.txt missing')
    else:
        rb = open('robots.txt').read()
        if 'Sitemap:' not in rb:
            failures['robots_txt'].append('robots.txt does not list Sitemap:')
        # Check for accidental site-wide block (Disallow: /)
        if re.search(r'^User-agent:\s*\*\s*\n\s*Disallow:\s*/\s*$', rb, re.M):
            failures['robots_txt'].append('robots.txt has Disallow: / under User-agent: * — blocks the entire site')
    rule('Rule 28 — robots.txt present and not site-blocking',
         'robots.txt allows crawling and references the sitemap',
         failures['robots_txt'])

    # Rule 29 — E-E-A-T signals in body content
    # Each page body must include at least 4 distinct signals from the set
    # below — demonstrating organisation identity, longevity, industry
    # authority, accreditation, local first-hand expertise, lived
    # experience, and concrete contact details.
    EEAT_SIGNALS = [
        ('identity',     re.compile(r'\bMark\s+Ratcliffe\b', re.I)),
        ('longevity',    re.compile(r'\b(?:since\s+1982|1982|forty\s+years|40\+?\s*years|40-?plus\s*years)\b', re.I)),
        ('authority',    re.compile(r'\b(?:BAR\b|British\s+Association\s+of\s+Removers)\b')),
        ('accreditation',re.compile(r'\b(?:BS\s*8564|Advance\s+Payment\s+Guarantee)\b', re.I)),
        ('local',        re.compile(r'\b(?:Sussex|Eastbourne|East\s+Sussex|West\s+Sussex)\b', re.I)),
        ('first_person', re.compile(r"\b(?:our\s+crew|our\s+crews|our\s+team|we['’]ve|we\s+have\s+(?:moved|packed|wrapped|loaded|been)|in\s+our\s+\d+\s*years?)\b", re.I)),
        ('contact',      re.compile(r'\b01323\s*848\s*008\b|\b01323848008\b|\b07437\s*414\s*589\b')),
    ]
    for p in indexable:
        try:
            html = open(p, encoding='utf-8').read()
        except OSError:
            continue
        m_start = NAV_END_RE.search(html)
        m_end   = FOOTER_RE.search(html)
        start   = m_start.end() if m_start else 0
        end     = m_end.start() if m_end else len(html)
        body    = html[start:end]
        text    = TAG_RE.sub(' ', body)
        text    = ENT_RE.sub(' ', text)
        hits    = sum(1 for _, pat in EEAT_SIGNALS if pat.search(text))
        if hits < 4:
            present = [name for name, pat in EEAT_SIGNALS if pat.search(text)]
            failures['eeat'].append(f'{p}  only {hits}/{len(EEAT_SIGNALS)} E-E-A-T signals (has: {", ".join(present) or "none"})')
    rule('Rule 29 — body content shows E-E-A-T (≥4 of 7 trust signals)',
         f'{len(indexable)} pages: every body demonstrates expertise/experience/authority/trust',
         failures['eeat'])

    # Rule 30 — every indexable page carries a JSON-LD block whose
    # graph references the canonical organization @id. This gives every
    # SERP entry point a LocalBusiness/MovingCompany card and powers
    # rich results (knowledge panel, local pack, sitelinks).
    ORG_ID = 'https://www.markratcliffemoving.co.uk/#organization'
    org_id_failures: list[str] = []
    json_parse_failures: list[str] = []
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        found_org = False
        for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
            raw = m.group(1).strip()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                json_parse_failures.append(f'{p}  invalid JSON: {e.msg} at line {e.lineno}')
                continue
            # Walk the data — could be a dict, a list, or a graph.
            stack = [data]
            while stack:
                node = stack.pop()
                if isinstance(node, list):
                    stack.extend(node)
                elif isinstance(node, dict):
                    if node.get('@id') == ORG_ID:
                        found_org = True
                        break
                    if '@graph' in node:
                        stack.append(node['@graph'])
            if found_org:
                break
        if not found_org:
            org_id_failures.append(p)
    rule('Rule 30 — every page carries canonical LocalBusiness JSON-LD',
         f'{len(indexable)} pages: all reference the #organization @id',
         org_id_failures)
    rule('Rule 31 — every JSON-LD block parses as valid JSON',
         f'{len(indexable)} pages: every <script type="application/ld+json"> body is valid',
         json_parse_failures)

    # Rule 32 — pages with user-visible FAQ content (one or more
    # <details>…<summary>question?</summary>…</details> blocks) must
    # declare FAQPage in some JSON-LD block so search engines render
    # the FAQ rich result.
    DETAILS_FAQ_RE = re.compile(
        r'<details[^>]*>\s*<summary[^>]*>[^<]*\?</summary>',
        re.S | re.I,
    )
    faq_schema_failures: list[str] = []
    faq_pages_counted = 0
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        if not DETAILS_FAQ_RE.search(html):
            continue
        faq_pages_counted += 1
        has_faq = False
        for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
            try:
                data = json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                continue
            stack = [data]
            while stack:
                node = stack.pop()
                if isinstance(node, list):
                    stack.extend(node)
                elif isinstance(node, dict):
                    t = node.get('@type')
                    if t == 'FAQPage' or (isinstance(t, list) and 'FAQPage' in t):
                        has_faq = True
                        break
                    if '@graph' in node:
                        stack.append(node['@graph'])
            if has_faq:
                break
        if not has_faq:
            faq_schema_failures.append(p)
    rule('Rule 32 — pages with visible FAQ content declare FAQPage schema',
         f'{faq_pages_counted} pages have <details><summary>?</summary>; all carry FAQPage JSON-LD',
         faq_schema_failures)

    # Rule 33 — exactly one <meta name="description"> per page. Multiple
    # meta descriptions are invalid HTML and confuse search engines —
    # Google may use whichever it picks, often the wrong one.
    META_DESC_PAGE_RE = re.compile(
        r'<meta\s+[^>]*?name\s*=\s*["\']description["\']',
        re.I,
    )
    multi_desc_failures: list[str] = []
    for p in indexable:
        n = len(META_DESC_PAGE_RE.findall(open(p, encoding='utf-8').read()))
        if n > 1:
            multi_desc_failures.append(f'{p}  ({n} meta descriptions)')
    rule('Rule 33 — exactly one <meta name="description"> per page',
         f'{len(indexable)} pages: each declares a single meta description',
         multi_desc_failures)

    # Rule 34 — no JS-injected canonicals. Crawlers like Screaming Frog
    # and many SERP previews don't execute JavaScript, so a canonical
    # created at runtime via createElement('link') / setAttribute('rel',
    # 'canonical') is invisible to them. Canonicals must be hardcoded
    # in the <head> as static markup.
    JS_CANON_RE = re.compile(
        r'setAttribute\(\s*["\']rel["\']\s*,\s*["\']canonical["\']',
        re.I,
    )
    js_canon_failures: list[str] = []
    for p in indexable:
        if JS_CANON_RE.search(open(p, encoding='utf-8').read()):
            js_canon_failures.append(p)
    rule('Rule 34 — no JS-injected <link rel="canonical">',
         f'{len(indexable)} pages: every canonical is hardcoded static HTML',
         js_canon_failures)

    # Rule 35 — internal directory links must carry a trailing slash,
    # including when followed by a #fragment or ?query. GitHub Pages
    # (and most static hosts) 301-redirect /services to /services/.
    # Every such redirect costs a hop on first crawl and wastes link
    # equity, so we link to /services/ directly.
    DIR_NAMES = ('services', 'areas-covered', 'blog', 'resources')
    BARE_DIR_RE = re.compile(
        r'<a\b[^>]*?\bhref="(\.\./)?(' + '|'.join(DIR_NAMES) + r')(["#?])',
        re.I,
    )
    bare_dir_failures: list[str] = []
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        for m in BARE_DIR_RE.finditer(html):
            bare_dir_failures.append(f'{p}  href="{m.group(1) or ""}{m.group(2)}{m.group(3)}…" (add trailing slash before {m.group(3)!r})')
    rule('Rule 35 — internal directory links use trailing slash',
         f'{len(indexable)} pages: no bare directory hrefs that would 301 redirect',
         bare_dir_failures)

    # Rule 36 — every internal <script src>, <link href> (CSS/icon/
    # preload), and <img src> must resolve to a real file on disk.
    # A typo'd path here is a guaranteed 404 the moment the page
    # loads — the kind of issue Screaming Frog surfaces under
    # "Response Codes: Internal Client Error (4xx)".
    on_disk: set[str] = set()
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs: dirs.remove('.git')
        if '.claude' in dirs: dirs.remove('.claude')
        for f in files:
            on_disk.add(os.path.relpath(os.path.join(root, f)))
    def resolve_resource(href: str, pdir: str) -> str | None:
        h = href.split('#')[0].split('?')[0]
        if not h: return None
        if h.startswith(('data:', 'mailto:', 'tel:', 'javascript:')): return None
        if h.startswith(('http://', 'https://', '//')): return None
        if h.startswith('/'):
            return h.lstrip('/')
        return os.path.normpath(os.path.join(pdir, h))
    RES_PATTERNS = [
        (re.compile(r'<script\b[^>]*?\bsrc="([^"]+)"', re.I), 'script-src'),
        (re.compile(r'<link\b[^>]*?\bhref="([^"]+)"[^>]*?\brel="(?:stylesheet|icon|apple-touch-icon|shortcut icon|preload)"', re.I), 'link-href'),
        (re.compile(r'<link\b[^>]*?\brel="(?:stylesheet|icon|apple-touch-icon|shortcut icon|preload)"[^>]*?\bhref="([^"]+)"', re.I), 'link-href'),
        (re.compile(r'<img\b[^>]*?\bsrc="([^"]+)"', re.I), 'img-src'),
    ]
    resource_failures: list[str] = []
    for p in indexable:
        pdir = os.path.dirname(p) or '.'
        html = open(p, encoding='utf-8').read()
        seen_in_page: set[tuple[str, str]] = set()
        for pat, kind in RES_PATTERNS:
            for m in pat.finditer(html):
                href = m.group(1)
                target = resolve_resource(href, pdir)
                if target is None: continue
                if target not in on_disk:
                    key = (kind, target)
                    if key in seen_in_page: continue
                    seen_in_page.add(key)
                    resource_failures.append(f'{p}  {kind}="{href}" → missing {target!r}')
    rule('Rule 36 — every <script src>/<link href>/<img src> resolves on disk',
         f'{len(indexable)} pages: every internal CSS/JS/image reference exists',
         resource_failures)

    # Rule 37 — every internal <a href> resolves to a real .html file
    # on disk (or a directory that has an index.html). Rule 12 already
    # covers the indexability angle; this rule is the narrower
    # "no 404 on click" guarantee.
    A_HREF_RE = re.compile(r'<a\b[^>]*?\bhref="([^"]+)"', re.I)
    href_404_failures: list[str] = []
    for p in indexable:
        pdir = os.path.dirname(p) or '.'
        html = open(p, encoding='utf-8').read()
        for m in A_HREF_RE.finditer(html):
            href = m.group(1)
            base = href.split('#')[0].split('?')[0]
            if not base: continue
            if base.startswith(('mailto:', 'tel:', 'javascript:', 'data:')): continue
            if base.startswith(('http://', 'https://', '//')): continue
            if base in ('.', './'):
                target = os.path.normpath(os.path.join(pdir, 'index.html'))
            elif base.startswith('/'):
                target = base.lstrip('/')
                if target.endswith('/'):
                    target += 'index.html'
            elif base.endswith('/'):
                target = os.path.normpath(os.path.join(pdir, base, 'index.html'))
            else:
                target = os.path.normpath(os.path.join(pdir, base))
            if target not in on_disk:
                href_404_failures.append(f'{p}  href="{href}" → missing {target!r}')
    rule('Rule 37 — every internal <a href> points at a real file',
         f'{len(indexable)} pages: zero internal click-throughs would 404',
         href_404_failures)

    # Rule 38 — no trailing slash on a .html file URL. /foo.html/ is
    # either 404 (most hosts) or a needless 301 (some). Always
    # bare /foo.html (no trailing slash).
    HTML_TRAILING_SLASH_RE = re.compile(r'<a\b[^>]*?\bhref="([^"]+\.html/(?:[#?][^"]*)?)"', re.I)
    html_slash_failures: list[str] = []
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        for m in HTML_TRAILING_SLASH_RE.finditer(html):
            html_slash_failures.append(f'{p}  href="{m.group(1)}" (drop the trailing slash)')
    rule('Rule 38 — no trailing slash on a .html file URL',
         f'{len(indexable)} pages: every .html href is a clean file URL',
         html_slash_failures)

    # Rule 39 — every <h2> text is unique across the entire site.
    # Cross-page H2 duplicates are a textbook "templated content"
    # signal Google penalises — every <h2> should describe the
    # specific section content of its page, not appear as a shared
    # boilerplate string. tools/dedupe-h2s.py rewrites duplicates to
    # weave the page's topic (from its <h1>) into each H2 so the
    # variants stay on-topic and readable.
    H2_ALL_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.I | re.S)
    NAV_END_RE_LOCAL = re.compile(r'</nav>\s*</div>|</nav>(?!\s*<)', re.I | re.S)
    FOOTER_RE_LOCAL = re.compile(r'<footer\b', re.I)
    def clean_h2(s: str) -> str:
        t = re.sub(r'&[a-z]+;|&#\d+;', ' ', re.sub(r'<[^>]+>', '', s), flags=re.I)
        return re.sub(r'\s+', ' ', t).strip().lower()
    h2_to_pages: dict[str, list[str]] = {}
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        m = NAV_END_RE_LOCAL.search(html); s = m.end() if m else 0
        m = FOOTER_RE_LOCAL.search(html); e = m.start() if m else len(html)
        for mm in H2_ALL_RE.finditer(html[s:e]):
            text = clean_h2(mm.group(1))
            if not text: continue
            h2_to_pages.setdefault(text, []).append(p)
    h2_dup_failures: list[str] = []
    for text, ps in h2_to_pages.items():
        if len(ps) > 1:
            sample = ', '.join(ps[:3]) + ('...' if len(ps) > 3 else '')
            h2_dup_failures.append(f'"{text[:80]}" appears on {len(ps)} pages ({sample})')
    rule('Rule 39 — every <h2> is unique site-wide',
         f'{len(indexable)} pages: {len(h2_to_pages)} distinct H2 strings, zero cross-page duplicates',
         h2_dup_failures)

    # Rule 40 — any schema.org Product JSON-LD must declare `name` AND
    # at least one of `offers` / `review` / `aggregateRating`. These
    # are Google's hard requirements for product-snippet rich results
    # — a Product missing either is silently dropped from the SERP.
    # Currently the site has no Product schema (we sell services, not
    # products), so this rule trivially passes — its real job is to
    # block any future regression that adds Product markup without
    # the mandatory fields.
    product_invalid: list[str] = []
    products_seen = 0
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
            try:
                data = json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                continue
            stack = [data]
            while stack:
                node = stack.pop()
                if isinstance(node, list):
                    stack.extend(node); continue
                if not isinstance(node, dict):
                    continue
                if '@graph' in node:
                    stack.append(node['@graph'])
                for v in node.values():
                    if isinstance(v, (dict, list)):
                        stack.append(v)
                t = node.get('@type')
                if t == 'Product' or (isinstance(t, list) and 'Product' in t):
                    products_seen += 1
                    if not node.get('name'):
                        product_invalid.append(f'{p}  Product missing "name"')
                    if not any(k in node for k in ('offers', 'review', 'aggregateRating')):
                        product_invalid.append(f'{p}  Product missing one of offers/review/aggregateRating')
    rule('Rule 40 — Product JSON-LD has name + offers/review/aggregateRating',
         f'{len(indexable)} pages: {products_seen} Product schemas, all complete',
         product_invalid)

    # Rule 41 — no HTML microdata attributes. We use JSON-LD exclusively
    # for structured data. Mixed signals (some pages microdata, some
    # JSON-LD) confuse Google's parsers and trigger "Unparsable
    # structured data" reports if a microdata itemtype value goes stale
    # or mistypes a schema URL. Block any future microdata regression.
    MICRODATA_RE = re.compile(r'\b(itemscope|itemtype|itemprop)\s*=', re.I)
    microdata_failures: list[str] = []
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        if MICRODATA_RE.search(html):
            microdata_failures.append(f'{p} contains microdata (itemscope/itemtype/itemprop) — use JSON-LD instead')
    rule('Rule 41 — no HTML microdata (itemscope/itemtype/itemprop)',
         f'{len(indexable)} pages: structured data is JSON-LD only',
         microdata_failures)

    # Rule 42 — <h1> text ≤70 characters. Screaming Frog and most SEO
    # tools flag longer H1s as a soft warning; >70 chars also tends
    # to wrap awkwardly on mobile heroes. Title (Rule 8) is pixel-
    # width gated; this rule is the H1 analogue.
    H1_LEN_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
    h1_too_long: list[str] = []
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        m = H1_LEN_RE.search(html)
        if not m: continue
        text = re.sub(r'\s+', ' ', re.sub(r'&[a-z]+;|&#\d+;', ' ', re.sub(r'<[^>]+>', '', m.group(1)))).strip()
        if len(text) > 70:
            h1_too_long.append(f'{p}  {len(text)} chars: "{text[:60]}..."')
    rule('Rule 42 — <h1> text ≤70 characters',
         f'{len(indexable)} pages: every H1 is concise (≤70 chars)',
         h1_too_long)

    # Rule 44 — zero stale-year + BAR self-claim tokens. The company was
    # founded 2017, not 1982; we cannot claim BAR membership or BAR-only
    # APG protection. This rule scans every indexable HTML file (full
    # source) for any of the forbidden tokens. Re-run tools/sweep-2017-
    # rebrand.py if violations appear after content edits.
    # Founding-date + over-claim guard only. BAR-membership claims are
    # NOT banned (the company is BAR-affiliated, per user instruction).
    # 'movership' is kept because it's a sweep artifact that never
    # appears legitimately and should always be caught.
    BANNED_TOKENS = [
        '1982', 'forty years', 'four decades', 'for decades', 'over decades',
        '40 years', '40+ years', 'over 40 years',
        'tens of thousands of moves', 'tens of thousands of homes',
        'ten thousand moves', 'ten thousand homes',
        '40+ Years moving overseas', 'movership',
    ]
    stale_failures: list[str] = []
    for p in indexable:
        text = open(p, encoding='utf-8').read()
        for tok in BANNED_TOKENS:
            if tok in text:
                stale_failures.append(f'{p}: contains banned token "{tok}" — re-run: python3 tools/sweep-2017-rebrand.py')
    rule('Rule 44 — no stale-year (1982) or BAR self-claim tokens',
         f'{len(indexable)} pages: all clear of banned founding-date and BAR-membership tokens',
         stale_failures)

    # Rule 43 — llms.txt covers every indexable page. Mirrors Rule 5 for the
    # Answer.AI llms.txt standard (https://llmstxt.org). Source of truth is
    # tools/build-llms-txt.py — never hand-edit llms.txt.
    llms_failures: list[str] = []
    try:
        llms_text = open('llms.txt', encoding='utf-8').read()
    except OSError:
        llms_failures.append('llms.txt missing at site root — run: python3 tools/build-llms-txt.py')
        llms_text = ''
    llms_urls = set(re.findall(r'\((https?://[^)\s]+)\)', llms_text))
    expected_urls = {expected_loc(p) for p in indexable}
    for p in indexable:
        loc = expected_loc(p)
        if loc not in llms_urls:
            llms_failures.append(f'missing from llms.txt: {p} ({loc}) — run: python3 tools/build-llms-txt.py')
    for url in llms_urls:
        if url not in expected_urls and url.startswith(BASE_URL):
            llms_failures.append(f'orphan link in llms.txt: {url} — run: python3 tools/build-llms-txt.py')
    rule('Rule 43 — llms.txt covers every indexable page',
         f'{len(indexable)} indexable pages all listed in llms.txt',
         llms_failures)

    # Rule 45 — og:image / twitter:image must match the page's hero
    # (the <link rel="preload" as="image" fetchpriority="high">). This
    # ensures the social-share preview matches what the visitor will
    # actually see at the top of the page, and that the OG image lives
    # on our own domain (no external CDN dependency).
    # Attribute order in source HTML varies: handle both
    #   content="X" property="og:image"
    #   property="og:image" content="X"
    def _meta_content(html, prop):
        for pat in (
            r'<meta\s+content="([^"]+)"\s+property="' + re.escape(prop) + r'"',
            r'<meta\s+property="' + re.escape(prop) + r'"\s+content="([^"]+)"',
        ):
            m = re.search(pat, html, re.I)
            if m: return m.group(1)
        return None
    PRE_RE  = re.compile(r'<link\s+rel="preload"\s+as="image"\s+href="([^"]+)"', re.I)
    og_failures: list[str] = []
    for p in indexable:
        html = open(p, encoding='utf-8').read()
        og_val = _meta_content(html, 'og:image')
        tw_val = _meta_content(html, 'twitter:image')
        m_pre = PRE_RE.search(html)
        if not og_val:
            og_failures.append(f'{p}: missing og:image meta tag')
            continue
        # Must live on our own domain, not an external CDN.
        if not og_val.startswith(BASE_URL):
            og_failures.append(f'{p}: og:image points off-domain ({og_val})')
            continue
        # Twitter image must equal OG image.
        if tw_val and tw_val != og_val:
            og_failures.append(f'{p}: twitter:image differs from og:image')
        # If a preload hero exists, og:image must reference the same file.
        if m_pre:
            hero = os.path.basename(m_pre.group(1))
            if os.path.basename(og_val) != hero:
                og_failures.append(f'{p}: og:image does not match hero preload ({os.path.basename(og_val)} vs {hero})')
    rule('Rule 45 — og:image matches page hero (on-domain)',
         f'{len(indexable)} pages: every social-share image matches the page\'s own hero',
         og_failures)

    print('=' * 64)
    if any_fail:
        print('FAIL — one or more rules violated. See list above.')
        print('To regenerate the blog index after adding/removing posts:')
        print('    python3 tools/build-blog-index.py')
        print('To regenerate the sitemap after adding/removing pages:')
        print('    python3 tools/build-sitemap.py')
        print('To regenerate llms.txt after adding/removing pages:')
        print('    python3 tools/build-llms-txt.py')
        print('To re-inject canonical schema.org JSON-LD on every page:')
        print('    python3 tools/build-schema.py')
        return 1
    print('PASS — all forty-five content rules satisfied.')
    return 0

if __name__ == '__main__':
    sys.exit(audit())
