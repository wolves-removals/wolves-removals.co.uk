#!/usr/bin/env python3
"""
Rebuild the blog/index.html main content area.

Generates a two-column layout: main column with the latest 9 cards
(Rule 4 cap) plus category-grouped lists giving access to every post,
and a sticky sidebar with recent posts and CTA blocks.

The script overwrites everything between
    <!-- BLOG_INDEX_AUTO_START -->
and
    <!-- BLOG_INDEX_AUTO_END -->
in blog/index.html. The hero, footer and surrounding chrome stay manual.

Run from the site root:    python3 tools/build-blog-index.py
"""

from __future__ import annotations
import glob, json, os, re, sys
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, 'blog')
INDEX = os.path.join(BLOG_DIR, 'index.html')
MAX_CARDS = 9
SIDEBAR_RECENT = 8

# Explicit slug → category mapping. Each post belongs to exactly one
# category. Order of CATEGORIES below determines display order on the
# page (and the category nav pills).
CATEGORIES = [
    ('planning',     'Planning your move'),
    ('cleaning',     'Move-out cleaning'),
    ('packing',      'Packing & materials'),
    ('storage',      'Storage'),
    ('cost',         'Cost & budget'),
    ('remover',      'Choosing a remover'),
    ('local',        'Local area guides'),
    ('family',       'Family & lifestyle'),
    ('seasonal',     'Seasonal moves'),
    ('specialist',   'Specialist moves'),
    ('business',     'Business & office'),
    ('international','International'),
    ('sustainable',  'Sustainable moves'),
    ('stories',      'Customer stories'),
]

SLUG_TO_CATEGORY = {
    # planning
    'how-to-prepare-for-your-house-move.html':                'planning',
    'moving-house-checklist-eastbourne.html':                 'planning',
    'what-to-pack-first-when-moving-house.html':              'planning',
    'moving-day-survival-kit.html':                           'planning',
    'essential-moving-day-survival-kit.html':                 'planning',
    'what-happens-on-moving-day.html':                        'planning',
    'moving-day-step-by-step-guide.html':                     'planning',
    'how-to-organise-move-when-busy.html':                    'planning',
    'best-day-of-week-to-move-house.html':                    'planning',
    '10-most-commonly-forgotten-moving-items.html':           'planning',
    # cleaning
    'how-to-clean-old-house-before-moving.html':              'cleaning',
    'cleaning-checklist-moving-out.html':                     'cleaning',
    # packing
    'how-to-pack-fragile-items.html':                         'packing',
    'packing-tips-fragile-items-pictures.html':               'packing',
    'how-to-pack-kitchen-items-safely.html':                  'packing',
    'how-to-pack-clothes-without-wrinkling.html':             'packing',
    'how-to-pack-electronics-safely.html':                    'packing',
    'benefits-of-professional-packing-service.html':          'packing',
    'cardboard-boxes-vs-plastic-crates.html':                 'packing',
    'full-pad-wrap-protection-explained.html':                'packing',
    'how-our-pad-wrap-service-protects-furniture.html':       'packing',
    # storage
    'how-to-choose-right-self-storage.html':                  'storage',
    'short-term-vs-long-term-storage.html':                   'storage',
    'what-you-can-and-cannot-store.html':                     'storage',
    'how-to-prepare-furniture-for-storage.html':              'storage',
    'prestige-steel-storage-rooms.html':                      'storage',
    # cost
    'cost-of-moving-house-sussex-2026.html':                  'cost',
    'how-to-save-money-on-house-move-2026.html':              'cost',
    'ways-to-save-on-house-move.html':                        'cost',
    'should-you-move-yourself-or-hire-professionals.html':    'cost',
    'diy-move-vs-professional.html':                          'cost',
    # remover
    'choosing-a-removal-company-eastbourne.html':             'remover',
    'questions-to-ask-removals-company.html':                 'remover',
    'how-to-spot-rogue-removal-traders.html':                 'remover',
    'common-moving-scams-2026.html':                          'remover',
    'how-to-avoid-moving-scams.html':                         'remover',
    # local
    'moving-to-eastbourne-area-guide.html':                   'local',
    'moving-to-brighton-area-guide.html':                     'local',
    'moving-to-chichester-area-guide.html':                   'local',
    'moving-to-hastings-area-guide.html':                     'local',
    'moving-to-worthing-area-guide.html':                     'local',
    'moving-to-lewes-area-guide.html':                        'local',
    'newhaven-or-seaford-which-is-better.html':               'local',
    'best-areas-to-live-east-sussex-2026.html':               'local',
    'moving-to-countryside-east-sussex.html':                 'local',
    'moving-to-tunbridge-wells-area-guide.html':              'local',
    'eastbourne-parking-permits-when-moving.html':            'local',
    'best-schools-eastbourne-families.html':                  'local',
    'moving-to-listed-building-sussex.html':                  'local',
    'cost-of-living-eastbourne-vs-brighton.html':             'local',
    'moving-from-london-to-sussex.html':                      'local',
    # family
    'moving-house-with-children.html':                        'family',
    'moving-house-with-pets.html':                            'family',
    'moving-house-alone-practical-tips.html':                 'family',
    'moving-student-belongings-parents-guide.html':           'family',
    'student-move-tips-for-parents.html':                     'family',
    'how-to-downsize-before-moving.html':                     'family',
    'moving-from-flat-vs-house.html':                         'family',
    # seasonal
    'moving-house-in-winter.html':                            'seasonal',
    'moving-house-in-summer.html':                            'seasonal',
    'moving-during-school-holidays.html':                     'seasonal',
    'moving-during-school-holidays-pros-cons.html':           'seasonal',
    'moving-over-christmas-and-new-year.html':                'seasonal',
    'moving-house-at-christmas-worth-it.html':                'seasonal',
    'christmas-new-year-house-move.html':                     'seasonal',
    'spring-cleaning-before-moving-house.html':               'seasonal',
    'spring-clean-while-moving.html':                         'seasonal',
    'school-holiday-moves.html':                              'seasonal',
    # specialist
    'moving-heavy-awkward-items.html':                        'specialist',
    'heavy-item-moves-pianos-safes.html':                     'specialist',
    'moving-antiques-valuable-furniture.html':                'specialist',
    'antique-furniture-moving-specialist.html':               'specialist',
    'moving-fine-art-collectibles.html':                      'specialist',
    'fine-art-moving-guide.html':                             'specialist',
    'moving-care-home-nursing-home.html':                     'specialist',
    'care-home-relocation-guide.html':                        'specialist',
    'moving-pub-or-restaurant.html':                          'specialist',
    'licensed-premises-relocation.html':                      'specialist',
    # business
    'office-relocation-minimise-disruption.html':             'business',
    'business-office-relocation.html':                        'business',
    # international
    'international-moves-from-sussex.html':                   'international',
    'overseas-removals-from-sussex.html':                     'international',
    # sustainable
    'eco-friendly-moving-sustainable-removals.html':          'sustainable',
    'ten-ways-eco-friendly-house-move.html':                  'sustainable',
    'sustainable-removals-guide.html':                        'sustainable',
    'how-to-make-move-carbon-neutral.html':                   'sustainable',
    'how-to-offset-carbon-emissions-moving.html':             'sustainable',
    'carbon-neutral-moves-explained.html':                    'sustainable',
    # stories
    'real-customer-moving-stories.html':                      'stories',
    'customer-moving-stories.html':                           'stories',
}

# Fallback keyword hints for any post that isn't explicitly mapped above
# (e.g. when new posts are added). Order matters — first match wins.
FALLBACK_HINTS = [
    ('cleaning',   'cleaning'),
    ('moving-to-', 'local'),
    ('removals-',  'local'),
    ('storage',    'storage'),
    ('packing',    'packing'),
    ('pad-wrap',   'packing'),
    ('fragile',    'packing'),
    ('cost',       'cost'),
    ('save',       'cost'),
    ('international', 'international'),
    ('overseas',   'international'),
    ('eco',        'sustainable'),
    ('carbon',     'sustainable'),
    ('children',   'family'),
    ('pets',       'family'),
    ('student',    'family'),
    ('office',     'business'),
    ('care-home',  'specialist'),
    ('antique',    'specialist'),
    ('art',        'specialist'),
    ('piano',      'specialist'),
    ('checklist',  'planning'),
    ('day',        'planning'),
]


def category_for(slug: str) -> str:
    if slug in SLUG_TO_CATEGORY:
        return SLUG_TO_CATEGORY[slug]
    for needle, key in FALLBACK_HINTS:
        if needle in slug:
            return key
    return 'planning'


def extract_meta(path: str) -> dict | None:
    html = open(path, encoding='utf-8').read()
    if 'http-equiv="refresh"' in html or 'window.location.replace' in html:
        return None

    headline = date = image = description = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict): continue
            if item.get('@type') == 'BlogPosting':
                headline    = item.get('headline')    or headline
                date        = item.get('datePublished') or date
                description = item.get('description') or description
                img = item.get('image')
                if isinstance(img, dict): img = img.get('url')
                image = img or image

    if not headline:
        m = re.search(r'<title>([^<]+)</title>', html)
        if m:
            headline = m.group(1).strip()
            headline = re.sub(r'\s*[|·—]\s*Mark Ratcliffe.*$', '', headline)
    if not description:
        m = re.search(r'<meta name="description" content="([^"]+)"', html)
        if m: description = m.group(1)
    if not image:
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if m: image = m.group(1)

    if not headline: return None

    if image:
        image = image.split('?')[0]
        m = re.search(r'/images/([^/]+\.\w+)$', image)
        if m:
            image = '../images/' + m.group(1)
        elif image.startswith('../images/'):
            pass
        else:
            image = '../images/mark-ratcliffe-modern-removal-lorry-eastbourne.webp'

    sort_date = date or '1970-01-01'
    slug = os.path.basename(path)

    return {
        'slug':        slug,
        'title':       unescape(headline.strip()),
        'date':        sort_date,
        'description': unescape((description or '').strip()),
        'image':       image,
        'category':    category_for(slug),
    }


def render_card(post: dict) -> str:
    cat_label = next((label for key, label in CATEGORIES if key == post['category']), 'Moving Tips')
    return (
        '          <article class="np-blog-card">\n'
        f'            <img src="{post["image"]}" alt="{post["title"]}" loading="lazy" decoding="async" width="600" height="360">\n'
        '            <div class="np-blog-card-body">\n'
        f'              <div class="np-blog-card-meta">{cat_label} &middot; {post["date"]}</div>\n'
        f'              <h3><a href="{post["slug"]}">{post["title"]}</a></h3>\n'
        f'              <p>{post["description"]}</p>\n'
        f'              <a href="{post["slug"]}" class="np-blog-card-cta"><strong>Read: {post["title"]} &rarr;</strong></a>\n'
        '            </div>\n'
        '          </article>'
    )


def render_category_pill(key: str, label: str, count: int) -> str:
    return f'          <a class="np-cat-pill" href="#cat-{key}">{label} <span>({count})</span></a>'


def render_category_section(key: str, label: str, posts: list[dict]) -> str:
    items = '\n'.join(
        f'              <li><a href="{p["slug"]}">{p["title"]}</a></li>' for p in posts
    )
    return (
        f'        <section class="np-blog-category" id="cat-{key}">\n'
        f'          <h3>{label} <span class="np-cat-count">({len(posts)} article{"s" if len(posts)!=1 else ""})</span></h3>\n'
         '          <ul class="np-blog-list">\n'
        f'{items}\n'
         '          </ul>\n'
         '        </section>'
    )


def render_sidebar_recent(posts: list[dict]) -> str:
    items = '\n'.join(
        f'            <li><a href="{p["slug"]}">{p["title"]}</a></li>' for p in posts
    )
    return (
        '        <div class="np-sidebar-block">\n'
        '          <h3>Recent posts</h3>\n'
        '          <ul class="np-sidebar-list">\n'
        f'{items}\n'
        '          </ul>\n'
        '        </div>'
    )


SIDEBAR_CTA = """        <div class="np-sidebar-block np-sidebar-cta">
          <h3>Quote or question?</h3>
          <p>Call us on <a href="tel:01323848008">01323 848 008</a> &mdash; or send a free quote request and we&rsquo;ll come back within 48 hours.</p>
          <a class="np-btn np-btn-primary np-sidebar-btn" href="../mark-ratcliffe-moving-online-removals-quote.html">Get a Free Quote</a>
        </div>"""

SIDEBAR_SERVICES = """        <div class="np-sidebar-block np-sidebar-services">
          <h3>Our services</h3>
          <p>Family-run Sussex removals since 1982. Local moves, international, packing, storage, piano, antiques.</p>
          <a class="np-btn np-btn-secondary np-sidebar-btn" href="../services/">View all services</a>
        </div>"""


def render_auto_block(posts: list[dict]) -> str:
    """Assemble the full auto-generated content block."""
    # Latest 9 — newest first, cap-9 (Rule 4)
    posts_sorted = sorted(posts, key=lambda p: (p['date'] or '', p['slug'] or ''), reverse=True)
    latest = posts_sorted[:MAX_CARDS]

    # Sidebar recent: 8 newest by date
    recent_sidebar = posts_sorted[:SIDEBAR_RECENT]

    # Category groups
    by_cat: dict[str, list[dict]] = {key: [] for key, _ in CATEGORIES}
    for p in posts_sorted:
        if p['category'] in by_cat:
            by_cat[p['category']].append(p)

    grid_html = '<div class="np-blog-grid">\n' + '\n'.join(render_card(p) for p in latest) + '\n          </div>'

    pills_html = '\n'.join(
        render_category_pill(key, label, len(by_cat[key]))
        for key, label in CATEGORIES if by_cat[key]
    )

    sections_html = '\n'.join(
        render_category_section(key, label, by_cat[key])
        for key, label in CATEGORIES if by_cat[key]
    )

    sidebar_recent_html = render_sidebar_recent(recent_sidebar)

    return f"""<!-- BLOG_INDEX_AUTO_START -->
  <section class="np-section np-section-soft np-blog-layout-section">
    <div class="np-inner np-blog-layout">
      <div class="np-blog-main">

        <h2>Latest articles</h2>
        {grid_html}

        <h2 class="np-blog-all-heading">Browse all {len(posts_sorted)} articles by topic</h2>
        <nav class="np-blog-categories-nav" aria-label="Blog categories">
{pills_html}
        </nav>

{sections_html}

      </div>
      <aside class="np-blog-sidebar" aria-label="Sidebar">
{sidebar_recent_html}

{SIDEBAR_CTA}

{SIDEBAR_SERVICES}
      </aside>
    </div>
  </section>
  <!-- BLOG_INDEX_AUTO_END -->"""


# Markers must already be present in blog/index.html
MARKER_START = '<!-- BLOG_INDEX_AUTO_START -->'
MARKER_END   = '<!-- BLOG_INDEX_AUTO_END -->'

# Markers in resources/blog.html (the magazine-style featured page)
RES_MARKER_START = '<!-- RESOURCES_BLOG_AUTO_START -->'
RES_MARKER_END   = '<!-- RESOURCES_BLOG_AUTO_END -->'
RES_PATH         = 'resources/blog.html'
RES_FEATURED     = 6      # newest N cards
RES_SIDEBAR_RECENT = 6    # next N in sidebar list


def render_res_card(post: dict) -> str:
    """Featured card for /resources/blog.html — same per-card descriptive
    anchor pattern as /blog/index.html (Rule 16 compliant). Card image path
    needs to be one directory up (/resources/ is one level deep just like
    /blog/, so the existing ../images/ prefix works as-is)."""
    cat_label = next((label for key, label in CATEGORIES if key == post['category']), 'Moving Tips')
    return (
        '          <article class="np-blog-card">\n'
        f'            <img src="{post["image"]}" alt="{post["title"]}" loading="lazy" decoding="async" width="600" height="360">\n'
        '            <div class="np-blog-card-body">\n'
        f'              <div class="np-blog-card-meta">{cat_label} &middot; {post["date"]}</div>\n'
        f'              <h3><a href="../blog/{post["slug"]}">{post["title"]}</a></h3>\n'
        f'              <p>{post["description"]}</p>\n'
        f'              <a href="../blog/{post["slug"]}" class="np-blog-card-cta"><strong>Read: {post["title"]} &rarr;</strong></a>\n'
        '            </div>\n'
        '          </article>'
    )


def render_res_sidebar_recent(posts: list[dict]) -> str:
    items = '\n'.join(
        f'            <li><a href="../blog/{p["slug"]}">{p["title"]}</a></li>' for p in posts
    )
    return (
        '        <div class="np-sidebar-block">\n'
        '          <h3>Recent posts</h3>\n'
        '          <ul class="np-sidebar-list">\n'
        f'{items}\n'
        '          </ul>\n'
        '        </div>'
    )


def render_res_sidebar_categories(by_cat: dict[str, list[dict]]) -> str:
    items = '\n'.join(
        f'            <li><a href="../blog/#cat-{key}">{label} <span class="np-sidebar-list-count">({len(by_cat[key])})</span></a></li>'
        for key, label in CATEGORIES if by_cat.get(key)
    )
    return (
        '        <div class="np-sidebar-block np-sidebar-categories">\n'
        '          <h3>Browse by category</h3>\n'
        '          <ul class="np-sidebar-list">\n'
        f'{items}\n'
        '          </ul>\n'
        '        </div>'
    )


RES_SIDEBAR_CTA = """        <div class="np-sidebar-block np-sidebar-cta">
          <h3>Quote or question?</h3>
          <p>Call us on <a href="tel:01323848008">01323 848 008</a> &mdash; or send a free quote request and we&rsquo;ll come back within 48 hours.</p>
          <a class="np-btn np-btn-primary np-sidebar-btn" href="../mark-ratcliffe-moving-online-removals-quote.html">Get a Free Quote</a>
        </div>"""


def render_resources_blog_block(posts: list[dict]) -> str:
    posts_sorted = sorted(posts, key=lambda p: (p['date'] or '', p['slug'] or ''), reverse=True)
    featured = posts_sorted[:RES_FEATURED]
    sidebar_recent = posts_sorted[RES_FEATURED:RES_FEATURED + RES_SIDEBAR_RECENT]

    by_cat: dict[str, list[dict]] = {key: [] for key, _ in CATEGORIES}
    for p in posts_sorted:
        if p['category'] in by_cat:
            by_cat[p['category']].append(p)

    featured_html = '<div class="np-blog-grid">\n' + '\n'.join(render_res_card(p) for p in featured) + '\n          </div>'
    sidebar_recent_html = render_res_sidebar_recent(sidebar_recent)
    sidebar_categories_html = render_res_sidebar_categories(by_cat)

    return f"""<!-- RESOURCES_BLOG_AUTO_START -->
  <section class="np-section">
    <div class="np-inner">
      <p style="font-size:1.15rem;">Our blog is where we share what we&rsquo;ve learned in forty-plus years of moving Sussex households &mdash; the practical stuff that doesn&rsquo;t fit on a service page, the longer reads about how the removals industry actually works, the customer stories that explain why we do things the way we do. Below are the latest articles; for the full categorised library of all {len(posts_sorted)} posts, jump to the <a href="../blog/">blog archive</a>.</p>
    </div>
  </section>

  <section class="np-section np-section-soft np-blog-layout-section">
    <div class="np-inner np-blog-layout">
      <div class="np-blog-main">
        <h2>News and updates</h2>
        {featured_html}
        <div class="np-blog-archive-link">
          <a class="np-btn np-btn-primary" href="../blog/">Browse all {len(posts_sorted)} articles in the blog archive &rarr;</a>
        </div>
      </div>
      <aside class="np-blog-sidebar" aria-label="Sidebar">
{sidebar_recent_html}

{RES_SIDEBAR_CTA}

{sidebar_categories_html}
      </aside>
    </div>
  </section>
  <!-- RESOURCES_BLOG_AUTO_END -->"""



def main() -> int:
    posts = []
    for path in glob.glob(os.path.join(BLOG_DIR, '*.html')):
        if os.path.basename(path) == 'index.html': continue
        meta = extract_meta(path)
        if meta: posts.append(meta)

    if not posts:
        print('No blog posts found', file=sys.stderr)
        return 1

    auto_block = render_auto_block(posts)

    index_html = open(INDEX, encoding='utf-8').read()
    s = index_html.find(MARKER_START)
    e = index_html.find(MARKER_END)
    if s < 0 or e < 0 or e < s:
        print('Markers not found in blog/index.html. Add:', file=sys.stderr)
        print(f'  {MARKER_START}  ...  {MARKER_END}', file=sys.stderr)
        return 1

    new_index = index_html[:s] + auto_block + index_html[e + len(MARKER_END):]
    open(INDEX, 'w', encoding='utf-8').write(new_index)

    n_total = len(posts)
    n_visible = min(MAX_CARDS, n_total)
    print(f'Rebuilt {INDEX}: latest {n_visible} cards + {n_total} categorised links.')

    # Also rebuild /resources/blog.html — featured 6 + sidebar (Yoast-style)
    res_path = os.path.join(ROOT, RES_PATH)
    if os.path.isfile(res_path):
        res_html = open(res_path, encoding='utf-8').read()
        rs = res_html.find(RES_MARKER_START)
        re_ = res_html.find(RES_MARKER_END)
        if rs >= 0 and re_ > rs:
            res_block = render_resources_blog_block(posts)
            new_res = res_html[:rs] + res_block + res_html[re_ + len(RES_MARKER_END):]
            open(res_path, 'w', encoding='utf-8').write(new_res)
            print(f'Rebuilt {RES_PATH}: featured {RES_FEATURED} + sidebar with {RES_SIDEBAR_RECENT} recent + categories.')
        else:
            print(f'WARN — markers missing in {RES_PATH}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
