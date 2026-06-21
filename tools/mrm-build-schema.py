#!/usr/bin/env python3
"""
Inject a canonical schema.org Organization block (LocalBusiness +
MovingCompany dual-type) into every indexable HTML page's <head>.

Why this script exists:
  - "LocalBusiness on every page" is enforced by audit Rule 30.
  - One source of truth for the organization's name, address, phone,
    geo, opening hours, aggregateRating etc. so a fact change is a
    one-file edit, not 230+ files.

The script is idempotent — it wraps the injected block in sentinel
comments and rewrites the contents on every run.

It also fixes the well-known address-bug pages (BN23 6PH "Birch
Industrial Estate") by replacing the stale address with the current
Lower Dicker BN27 4EL address wherever it appears in JSON-LD.

For pages that legitimately display the aggregate rating to users
(home page hero trust strip + the reviews page), the org block carries
aggregateRating. For all other pages, the rating is omitted (Google
guidance: aggregateRating must reflect content visible on the page).

Run from the site root:
    python3 tools/build-schema.py
"""

from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ORG_ID = 'https://www.markratcliffemoving.co.uk/#organization'

CANONICAL_ORG: dict = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "MovingCompany"],
    "@id": ORG_ID,
    "name": "Mark Ratcliffe Moving & Storage",
    "alternateName": "Mark Ratcliffe Moving",
    "legalName": "EMV London Ltd",
    "url": "https://www.markratcliffemoving.co.uk/",
    "logo": {
        "@type": "ImageObject",
        "url": "https://www.markratcliffemoving.co.uk/images/mark-ratcliffe-moving-and-storage-logo.webp",
        "width": 180,
        "height": 60
    },
    "image": "https://www.markratcliffemoving.co.uk/images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp",
    "telephone": "+441323848008",
    "email": "office@markratcliffemoving.co.uk",
    "foundingDate": "2017",
    "priceRange": "££",
    "currenciesAccepted": "GBP",
    "paymentAccepted": "Cash, Credit Card, Bank Transfer",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Unit J12 Swallow Business Park, Diamond Drive",
        "addressLocality": "Lower Dicker",
        "addressRegion": "East Sussex",
        "postalCode": "BN27 4EL",
        "addressCountry": "GB"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 50.77465207,
        "longitude": 0.29392332
    },
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"}
    ],
    "areaServed": [
        {"@type": "AdministrativeArea", "name": "East Sussex"},
        {"@type": "AdministrativeArea", "name": "West Sussex"},
        {"@type": "AdministrativeArea", "name": "Surrey"},
        {"@type": "AdministrativeArea", "name": "Kent"}
    ],
    "sameAs": ["https://www.facebook.com/mark.ratcliffe.10441"],
    "knowsAbout": [
        "House removals", "Office removals", "Packing services",
        "Self storage", "International removals", "European removals",
        "Piano moving", "Antique furniture moving", "House clearance"
    ]
}

AGGREGATE_RATING: dict = {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "120",
    "ratingCount": "120",  # Google requires either ratingCount OR reviewCount;
                            # we include both to satisfy strict Search Console
                            # validation across all snippet rich-result types.
    "bestRating": "5",
    "worstRating": "1"
}

# Pages that legitimately display the rating in user-visible content
# (so the markup matches what the page actually shows).
PAGES_WITH_VISIBLE_RATING = {
    'index.html',
    'reviews.html',
}

# The reviews displayed on /reviews.html as user-facing testimonial cards.
# These need to also exist as schema.org Review objects on that page so
# Google's Review snippet rich result can render. They live here (rather
# than being parsed off the page) so build-schema.py is the single source
# of truth — re-runs always reinstate them, even if the surrounding HTML
# changes. Update this list when new customer reviews are added to the
# /reviews.html cards.
REVIEWS_PAGE = 'reviews.html'
# Each Review carries itemReviewed pointing at the canonical org @id so
# Google's review-snippet validator knows what the review is about.
# Without itemReviewed, Search Console reports the review as invalid
# ("Missing field itemReviewed") and the rich result doesn't render.
_REVIEWED = {"@id": ORG_ID}
EMBEDDED_REVIEWS: list[dict] = [
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "S. Patel"}, "datePublished": "2025-09-14", "reviewBody": "From the survey to the final box being unpacked, the Mark Ratcliffe team handled our Eastbourne-to-Lewes move with absolute care. Every piece of furniture was pad-wrapped and labelled — nothing arrived with a scratch. Our previous remover damaged our dining table in transit; the difference in approach is night and day."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "J. Williams"}, "datePublished": "2025-08-22", "reviewBody": "Used Mark Ratcliffe for our move from Newhaven to Brighton and then six months of storage at their Lower Dicker depot. Uniformed crew, immaculate vans, secure steel storage room — worth every penny. We collected six months later and everything came out exactly as it went in."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Margaret K."}, "datePublished": "2025-07-09", "reviewBody": "After my mother passed away we needed her house in Hailsham cleared sensitively. The team treated her possessions with such respect, set aside everything we wanted to keep, donated what could be reused and recycled the rest. They handled the paperwork for the executor and were genuinely kind throughout. Would recommend to anyone in similar circumstances."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Andrew & Liz Turner"}, "datePublished": "2025-06-18", "reviewBody": "We moved from Sovereign Harbour to the Costa Blanca and Mark Ratcliffe handled everything — the packing, the ToR1 customs paperwork, the shipping and the destination delivery. We had heard horror stories of post-Brexit moves to Spain, but ours was textbook. Furniture arrived in three weeks, intact, and the Spanish destination crew was excellent."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Dr. Pongsak C."}, "datePublished": "2025-05-30", "reviewBody": "Returning to Bangkok after twenty years in the UK was emotional. The Mark Ratcliffe Thai removals team understood the practicalities — Thai customs, the address format, the timing around our Bangkok delivery slot. Container arrived on schedule and the destination unpack was professional. Highly recommended for any UK-Thailand move."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Stephen R."}, "datePublished": "2025-04-12", "reviewBody": "We downsized from a 4-bedroom house in Polegate to a 2-bedroom bungalow. The team helped us identify what was going to the bungalow, what was going to family, and what was going to storage for later. The whole transition was completed in two days with zero stress."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Caroline M."}, "datePublished": "2025-03-04", "reviewBody": "Just needed a single-day move from my flat in Bexhill to the new place in Eastbourne. Man-and-van service was perfectly suited, two crew arrived on time, were polite, careful and efficient. Hourly billing was honest — they did not pad the hours. Less than half the price of the full-service quotes I had received elsewhere."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "The Harrison Family"}, "datePublished": "2025-02-21", "reviewBody": "We had used a national firm for our previous move ten years ago and ended up with a broken dining chair and a chipped antique cabinet. This time we used Mark Ratcliffe on the recommendation of a neighbour. Everything pad-wrapped before it left the room. Zero damage. The 'do not unwrap until placed' approach genuinely makes the difference."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Peter & Susan B."}, "datePublished": "2025-01-15", "reviewBody": "Our 5-bedroom country house in Heathfield was a complex move with antique furniture, a piano and a large wine collection. Mark Ratcliffe sent a four-person crew and two lorries over two days. Everything was handled with care. The wine collection was packed in dedicated temperature-tolerant boxes. Professional service from quote to completion."},
    {"@type": "Review", "itemReviewed": _REVIEWED, "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"}, "author": {"@type": "Person", "name": "Office Manager"}, "datePublished": "2024-11-26", "reviewBody": "We moved our 30-person office from Eastbourne town centre to a new building near Sovereign Harbour over a single weekend. Mark Ratcliffe planned the move, labelled every workstation, coordinated with our IT contractor, and we were open for business on Monday morning with no delays. The cleanest office move I have ever managed."},
]

SENTINEL_START = '<!-- mrm-schema:org:start -->'
SENTINEL_END = '<!-- mrm-schema:org:end -->'
FAQ_SENTINEL_START = '<!-- mrm-schema:faq:start -->'
FAQ_SENTINEL_END = '<!-- mrm-schema:faq:end -->'
# Match the full sentinel block (including the embedded <script>).
SENTINEL_RE = re.compile(
    re.escape(SENTINEL_START) + r'.*?' + re.escape(SENTINEL_END) + r'\s*\n?',
    re.S,
)
FAQ_SENTINEL_RE = re.compile(
    re.escape(FAQ_SENTINEL_START) + r'.*?' + re.escape(FAQ_SENTINEL_END) + r'\s*\n?',
    re.S,
)
HEAD_CLOSE_RE = re.compile(r'</head>', re.I)
# Capture <details>…<summary>question?</summary>…</details> blocks for
# FAQPage auto-generation. The summary must end with a question mark to
# qualify (decorative <details> with non-question summaries are skipped).
DETAILS_RE = re.compile(
    r'<details[^>]*>\s*<summary[^>]*>(.*?\?)</summary>(.+?)</details>',
    re.S | re.I,
)
TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')

# Pages excluded from the rule entirely.
def is_excluded(path: str) -> bool:
    name = os.path.basename(path)
    if name == '404.html':
        return True
    if (name.startswith('google') and len(name) > 16
            or name.startswith('BingSiteAuth')
            or name.startswith('yandex_')):
        return True
    return False


def strip_html(s: str) -> str:
    return WS_RE.sub(' ', TAG_RE.sub(' ', s)).strip()


def extract_faqs(html: str) -> list[tuple[str, str]]:
    """Find visible <details>…<summary>?</summary>…</details> Q&A pairs."""
    pairs: list[tuple[str, str]] = []
    seen_q: set[str] = set()
    for m in DETAILS_RE.finditer(html):
        question = strip_html(m.group(1))
        answer = strip_html(m.group(2))
        if not question or not answer:
            continue
        if question in seen_q:
            continue
        seen_q.add(question)
        pairs.append((question, answer))
    return pairs


def has_existing_faqpage(html: str) -> bool:
    """True iff some non-sentinel JSON-LD on the page declares FAQPage."""
    # Skip our own sentinel block so re-runs don't see themselves and bail.
    scan = FAQ_SENTINEL_RE.sub('', html)
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', scan, re.S):
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
                    return True
                if '@graph' in node:
                    stack.append(node['@graph'])
    return False


def faq_block_for(pairs: list[tuple[str, str]]) -> str:
    """Builds the sentinel-wrapped FAQPage <script> for the given Q&A pairs."""
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }
    body = json.dumps(faq, ensure_ascii=False, separators=(',', ':'))
    return (
        f'  {FAQ_SENTINEL_START}\n'
        f'  <script type="application/ld+json">{body}</script>\n'
        f'  {FAQ_SENTINEL_END}\n'
    )


JSONLD_RE = re.compile(
    r'(\s*<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>\s*\n?)',
    re.S,
)


def strip_duplicate_org_blocks(html: str) -> tuple[str, list]:
    """Remove pre-existing JSON-LD blocks whose top-level object has
    @id=#organization. If the block carries a `review` array, absorb
    those Review objects so we can re-attach them to the canonical
    block we're about to inject. Handles both single-object blocks
    and @graph wrappers (in @graph form, only the org entry is
    excised; the rest of the graph is preserved).
    """
    absorbed: list = []
    out: list[str] = []
    pos = 0
    for m in JSONLD_RE.finditer(html):
        out.append(html[pos:m.start()])
        pos = m.end()
        opener, body, closer = m.group(1), m.group(2).strip(), m.group(3)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            out.append(m.group(0))
            continue
        # Case 1: top-level dict with the canonical @id
        if isinstance(data, dict) and data.get('@id') == ORG_ID:
            if isinstance(data.get('review'), list):
                absorbed.extend(data['review'])
            # Drop the whole block.
            continue
        # Case 2: @graph wrapper containing the org entry
        if isinstance(data, dict) and isinstance(data.get('@graph'), list):
            new_graph = []
            removed_any = False
            for item in data['@graph']:
                if isinstance(item, dict) and item.get('@id') == ORG_ID:
                    removed_any = True
                    if isinstance(item.get('review'), list):
                        absorbed.extend(item['review'])
                    continue
                new_graph.append(item)
            if removed_any:
                if new_graph:
                    data['@graph'] = new_graph
                    new_body = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
                    out.append(opener + new_body + closer)
                # else: graph is empty, drop the whole block
                continue
        # Block is unrelated to the org — keep it as-is.
        out.append(m.group(0))
    out.append(html[pos:])
    return ''.join(out), absorbed


def upgrade_html(path: str, rel_path: str) -> tuple[bool, bool]:
    """Reads, rewrites, writes the HTML for one page.

    Returns (changed, injected_faq) so the caller can report counts.
    """
    try:
        html = open(path, encoding='utf-8').read()
    except OSError:
        return False, False
    original = html

    # Strip any previously-injected sentinel blocks before we add fresh ones.
    html = SENTINEL_RE.sub('', html)
    html = FAQ_SENTINEL_RE.sub('', html)

    # Strip any pre-existing JSON-LD blocks that re-declare the canonical
    # organization @id (duplicates would conflict with our injected one).
    # Any review[] they carry is absorbed and re-attached below.
    html, absorbed_reviews = strip_duplicate_org_blocks(html)

    # Fix the well-known stale Eastbourne / BN23 6PH address that lives in
    # some pages' hand-crafted JSON-LD. Only touches the exact string
    # patterns; doesn't disturb anything else.
    html = html.replace('"streetAddress": "Birch Industrial Estate"',
                        '"streetAddress": "Unit J12 Swallow Business Park, Diamond Drive"')
    html = html.replace('"addressLocality": "Eastbourne"',
                        '"addressLocality": "Lower Dicker"')
    html = html.replace('"postalCode": "BN23 6PH"', '"postalCode": "BN27 4EL"')

    # Build the canonical Organization block (always).
    org = dict(CANONICAL_ORG)
    if rel_path in PAGES_WITH_VISIBLE_RATING:
        org['aggregateRating'] = AGGREGATE_RATING
    # Reviews are sourced from EMBEDDED_REVIEWS (the canonical list) on
    # the reviews page; any reviews absorbed from existing JSON-LD blocks
    # on other pages are kept too.
    if rel_path == REVIEWS_PAGE:
        org['review'] = EMBEDDED_REVIEWS
    elif absorbed_reviews:
        org['review'] = absorbed_reviews
    body = json.dumps(org, ensure_ascii=False, separators=(',', ':'))
    block = (
        f'  {SENTINEL_START}\n'
        f'  <script type="application/ld+json">{body}</script>\n'
        f'  {SENTINEL_END}\n'
    )

    # If the page has visible <details>?</summary> Q&A blocks and no
    # existing FAQPage in its JSON-LD, auto-generate one. Existing
    # hand-crafted FAQPage schemas are respected (we don't overwrite).
    injected_faq = False
    faqs = extract_faqs(html)
    if faqs and not has_existing_faqpage(html):
        block += faq_block_for(faqs)
        injected_faq = True

    # Inject right before </head>.
    m = HEAD_CLOSE_RE.search(html)
    if not m:
        print(f'  ! no </head> in {path}; skipped', file=sys.stderr)
        return False, False
    html = html[:m.start()] + block + html[m.start():]

    if html != original:
        open(path, 'w', encoding='utf-8').write(html)
        return True, injected_faq
    return False, injected_faq


def main() -> int:
    pages = (
        glob.glob('*.html')
        + glob.glob('areas-covered/*.html')
        + glob.glob('blog/*.html')
        + glob.glob('services/*.html')
        + glob.glob('resources/*.html')
    )
    changed = 0
    skipped = 0
    rating_pages = 0
    faq_pages = 0
    for p in sorted(pages):
        if is_excluded(p):
            skipped += 1
            continue
        ok, faq = upgrade_html(p, p)
        if ok:
            changed += 1
        if faq:
            faq_pages += 1
        if p in PAGES_WITH_VISIBLE_RATING:
            rating_pages += 1
    print(f'  upgraded {changed} pages; {skipped} excluded')
    print(f'  aggregateRating embedded on {rating_pages} pages with visible ratings')
    print(f'  FAQPage auto-generated on {faq_pages} pages with visible Q&A')
    return 0


if __name__ == '__main__':
    sys.exit(main())
