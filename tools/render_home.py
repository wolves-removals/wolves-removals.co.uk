# -*- coding: utf-8 -*-
"""Build the home page (index.html).
Keeps the live home copy and expands it to the SEO bible:
unique title/H1, keyword in H1 + first paragraph, LocalBusiness + FAQPage schema,
>=10 in-body internal links, E-E-A-T trust signals, alt text + dims on every image.
"""
import os, sys, json, glob, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, card_grid, cta_band, faq_block

# --- Facebook social-post feed (carousel -> hover -> lightbox), like the old site.
# NOTE: the real branded FB graphics aren't in the repo, so these use the closest in-house
# photos as placeholders. Drop the real square social images into images/social/ and swap
# the "img" paths below to match the live posts exactly.
SOCIAL_POSTS = [
    {"date": "27 May 2026", "img": "/images/photos/careful-packing-sussex-home-removal.webp",
     "alt": "Wolves Removals unpacking service in Sussex", "likes": 6, "comments": 0, "video": False,
     "title": "Unpacking Without the Hassle",
     "caption": "Settle into your new home faster with our professional unpacking service — we’ll have you organised in no time.",
     "tags": "#Unpacking #HouseMove #SussexRemovals #StressFreeMove"},
    {"date": "22 May 2026", "img": "/images/photos/containerised-storage-units-wolves-store.webp",
     "alt": "A look inside the Wolves Removals containerised storage store", "likes": 4, "comments": 1, "video": True,
     "title": "Behind the Scenes",
     "caption": "A quick look behind the scenes at our secure, containerised storage — clean, dry and protected, ready whenever you need it.",
     "tags": "#Storage #ContainerisedStorage #SecureStorage #Sussex"},
    {"date": "21 May 2026", "img": "/images/photos/professional-removals-movers-sussex-property.webp",
     "alt": "Wolves Removals team carrying out a corporate office relocation", "likes": 3, "comments": 0, "video": False,
     "title": "Seamless Corporate Office Relocation",
     "caption": "Make your business move simple with our Seamless Corporate Office Relocation service. 🏢📦 We provide efficient, professional and organised office moves designed to minimise disruption and keep your business running smoothly from start to finish. Call us today to discuss your office relocation requirements. 📞 01903 893731 🌐 wolves-removals.co.uk",
     "tags": "#OfficeRelocation #CorporateMove #BusinessServices #CommercialMoving #UKRemovals"},
    {"date": "16 May 2026", "img": "/images/photos/removal-van-loaded-sussex-move.webp",
     "alt": "Wolves Removals van loaded and ready to relocate", "likes": 5, "comments": 0, "video": False,
     "title": "Ready to Relocate",
     "caption": "Fast, secure and efficient removals across Sussex and beyond — whatever the move, our trained team has it covered.",
     "tags": "#ReadyToRelocate #Removals #Sussex #HouseMove"},
    {"date": "08 May 2026", "img": "/images/photos/wolves-removals-team-fleet-vans.webp",
     "alt": "The Wolves Removals team and fleet — business relocation experts", "likes": 4, "comments": 0, "video": False,
     "title": "Business Relocation Experts",
     "caption": "Keep your company moving smoothly with the business relocation experts. Minimal downtime, maximum care — from one desk to a whole office.",
     "tags": "#BusinessRelocation #CommercialMoving #OfficeMove #Sussex"},
]

def social_feed():
    b = E.S.BUSINESS
    fb_icon = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="w-5 h-5">'
               '<path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.8-1.6 1.5V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>')
    play_badge = ('<span class="social-play" x-show="p.video" x-cloak><svg viewBox="0 0 24 24" fill="currentColor" '
                  'class="w-5 h-5" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>')
    # carousel cards (rendered by Alpine x-for from the posts in x-data)
    card = (
        '<template x-for="(p,i) in posts" :key="i">'
        '<button type="button" class="social-card" @click="active=i;open=true" '
        ':aria-label="\'Open Facebook post from \'+p.date">'
        '<img class="social-img" :src="p.img" :alt="p.alt" loading="lazy" decoding="async" width="600" height="600">'
        '<span class="social-fade" aria-hidden="true"></span>'
        f'{play_badge}'
        '<span class="social-meta">'
        '<span class="social-date" x-text="p.date"></span>'
        f'<span class="social-fb">{fb_icon}</span>'
        '</span>'
        '<span class="social-hover" aria-hidden="true">'
        '<span class="social-hover-top"><span x-text="p.date"></span></span>'
        '<span class="social-stats"><span class="social-heart">&#9829; <span x-text="p.likes"></span></span>'
        '<span class="social-comm">&#128172; <span x-text="p.comments"></span></span></span>'
        '<span class="social-cap" x-text="p.title + \' — \' + p.caption"></span>'
        '</span>'
        '</button>'
        '</template>')
    arrows = (
        '<button type="button" class="social-arrow social-prev" aria-label="Previous posts" '
        '@click="$refs.track.scrollBy({left:-($refs.track.clientWidth*0.8),behavior:\'smooth\'})">'
        '<svg viewBox="0 0 24 24" class="w-6 h-6" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg></button>'
        '<button type="button" class="social-arrow social-next" aria-label="More posts" '
        '@click="$refs.track.scrollBy({left:$refs.track.clientWidth*0.8,behavior:\'smooth\'})">'
        '<svg viewBox="0 0 24 24" class="w-6 h-6" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>')
    # lightbox
    lightbox = (
        '<div class="social-lightbox" x-show="open" x-cloak x-transition.opacity '
        '@keydown.escape.window="open=false" @click.self="open=false">'
        '<button type="button" class="social-close" @click="open=false" aria-label="Close">&times;</button>'
        '<button type="button" class="social-nav social-nav-prev" aria-label="Previous post" @click="active=(active-1+posts.length)%posts.length">'
        '<svg viewBox="0 0 24 24" class="w-7 h-7" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg></button>'
        '<div class="social-modal" @click.stop>'
        '<div class="social-modal-img"><img :src="posts[active].img" :alt="posts[active].alt" width="1200" height="900"></div>'
        '<div class="social-modal-cap">'
        '<div class="social-modal-head"><span x-text="posts[active].date"></span>'
        f'<span class="social-fb-dark">{fb_icon}</span></div>'
        '<div class="social-modal-likes">&#9829; <span x-text="posts[active].likes"></span> likes</div>'
        '<p class="social-modal-text" x-text="posts[active].title + \' — \' + posts[active].caption"></p>'
        '<p class="social-modal-tags" x-text="posts[active].tags"></p>'
        '<a class="button-orange mt-2 inline-flex" :href="posts[active].permalink" target="_blank" rel="noopener">View on Facebook</a>'
        '</div></div>'
        '<button type="button" class="social-nav social-nav-next" aria-label="Next post" @click="active=(active+1)%posts.length">'
        '<svg viewBox="0 0 24 24" class="w-7 h-7" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>'
        '</div>')
    # Fallback posts (shown until /api/social returns live Facebook data). Each gets a
    # permalink defaulting to the page; the live feed supplies real per-post permalinks.
    fallback = [{**p, "permalink": p.get("permalink", E.S.SOCIAL["facebook"])} for p in SOCIAL_POSTS]
    fb_json = json.dumps(fallback, ensure_ascii=False).replace("<", "\\u003c")
    head = ('<div class="text-center mb-8"><h2 class="relative leading-tight text-black">Follow Us on Facebook</h2>'
            '<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">See our latest moves, tips and news. '
            f'<a href="{E.S.SOCIAL["facebook"]}" target="_blank" rel="noopener">Like our page</a> to keep up to date.</p></div>')
    body = (f'<script type="application/json" id="social-fallback">{fb_json}</script>'
            '<div class="social-feed" x-data="socialFeed()">'
            f'<div class="social-wrap">{arrows}<div class="social-track" x-ref="track" role="group" aria-label="Latest Facebook posts">{card}</div></div>'
            f'{lightbox}</div>')
    return section(head + body, bg="bg-lightgrey")

def latest_blog(n=3):
    """A 'Latest from our blog' strip: the n newest posts (by date) as cards."""
    bdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "blog")
    posts = []
    for f in glob.glob(os.path.join(bdir, "*.json")):
        try:
            p = json.load(open(f, encoding="utf-8"))
            if p.get("slug") and p.get("h1"):
                posts.append(p)
        except Exception:
            pass
    posts.sort(key=lambda p: p.get("date", "2024-01-01"), reverse=True)
    cards = []
    for p in posts[:n]:
        lead = re.sub("<[^>]+>", "", p.get("lead", "") or "").strip()
        body = (f'<p><span class="text-blue font-semibold text-sm uppercase">{esc(p.get("category","Moving Advice"))}</span>'
                f'<br>{esc(lead[:130])}</p>')
        cards.append((p["h1"][:70], f'/{p["slug"]}/', body))
    return card_grid(cards, cols=3, heading="Latest from Our Blog",
                     intro='Practical moving tips, packing advice and local guides from our Sussex removals team. '
                           '<a href="/blog/">Browse all articles</a>.',
                     bg="bg-beige")

HERO_IMG = "images/photos/three-wolves-vans-sussex-house.webp"

def hero():
    b = E.S.BUSINESS
    star = ('<svg viewBox="0 0 20 20" class="w-5 h-5" fill="currentColor" aria-hidden="true">'
            '<path d="M10 1.6l2.5 5.1 5.6.8-4.05 3.95.95 5.55L10 14.4l-5 2.6.95-5.55L1.9 7.5l5.6-.8z"/></svg>')
    stars = '<span class="flex text-star" aria-hidden="true">' + star * 5 + '</span>'
    bullets = ["Extremely cost-effective, fully insured Sussex removals",
               "Locally based for a personalised, friendly service",
               "Responsive, proactive and dedicated customer care"]
    lis = "".join(
        f'<li class="flex items-start gap-2"><span class="text-green mt-1 shrink-0">{icon("check-bold","w-5 h-5")}</span><span>{esc(t)}</span></li>'
        for t in bullets)
    hero_img = img(HERO_IMG, "Three Wolves Removals vans parked outside a large Sussex house",
                   cls="w-full h-full object-cover", eager=True)
    bullets_ul = f'<ul class="space-y-2 text-base xl:text-lg list-none p-0">{lis}</ul>'
    return (
        '<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
        f'<div class="absolute inset-0">{hero_img}</div>'
        '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
        '<h1 class="text-4xl lg:text-6xl font-bold leading-tight">Removals Company in Sussex</h1>'
        '<p class="mt-4 text-lg xl:text-xl max-w-xl">Looking for a reliable Sussex removals company? From local moves to '
        'long-distance relocations, we&rsquo;ve got you covered &mdash; packing, removals, storage and unpacking.</p>'
        f'{E.hero_review_row(bullets_ul, quote_button=True)}'
        '</div></div></div></section>')

def intro():
    html = (
        '<h2 class="relative leading-tight text-black">Your Trusted Sussex Removals Team</h2>'
        '<p>Wolves Removals is a trusted, <strong>family-run Sussex removals company</strong> based at Doryln House, '
        'London Road, Ashington, near <a href="/locations/pulborough-removals/">Pulborough</a> in West Sussex. We provide '
        'home and business removals across the South East, including '
        '<a href="/locations/west-sussex-removals/">West Sussex</a>, '
        '<a href="/locations/east-sussex-removals/">East Sussex</a>, '
        '<a href="/locations/surrey-removals/">Surrey</a> and '
        '<a href="/locations/hampshire-removals/">Hampshire</a>. Our skilled team brings over 100 years of combined '
        'moving experience, and we are a <strong>LAPADA member</strong>, <strong>Checkatrade-verified</strong> and '
        'fully insured for your complete peace of mind.</p>'
        '<p class="text-lg xl:text-xl font-medium">When everything has to go right, Wolves Removals is the Sussex removal '
        'company you need.</p>')
    services_list = (
        '<p class="text-lg xl:text-xl font-medium mb-3">Our comprehensive range of services includes:</p>'
        '<ul class="tick-list grid sm:grid-cols-2 gap-x-10 gap-y-1">'
        '<li><a href="/services/house-removals/">Home removals</a> and <a href="/services/commercial-removals/">commercial relocations</a></li>'
        '<li>Long-distance and <a href="/services/international-removals/">international moving</a> within the UK and EU</li>'
        '<li>Expert <a href="/services/full-packing-service/">packing</a> and <a href="/services/full-unpacking-service/">unpacking</a> services</li>'
        '<li><a href="/services/specialised-antiques-moving/">Antique and valuable item</a> transportation</li>'
        '<li><a href="/services/piano-moving/">Heavy and speciality item</a> removal and transportation</li>'
        '<li>Short and long-term <a href="/services/storage/">secure storage</a> facilities</li>'
        '</ul>')
    play = ('<svg viewBox="0 0 68 48" class="w-16 h-16 lg:w-20 lg:h-20" aria-hidden="true">'
            '<path fill="#dad6c2" stroke="#262626" stroke-width="2.5" d="M66.5 7.7c-.8-2.9-3-5.1-5.9-5.9C55.3.5 34 .5 34 .5S12.7.5 7.4 1.8C4.5 2.6 2.3 4.8 1.5 7.7.2 13 .2 24 .2 24s0 11 1.3 16.3c.8 2.9 3 5.1 5.9 5.9C12.7 47.5 34 47.5 34 47.5s21.3 0 26.6-1.3c2.9-.8 5.1-3 5.9-5.9C67.8 35 67.8 24 67.8 24s0-11-1.3-16.3z"/>'
            '<path fill="#262626" d="M27 34.5l17.8-10.5L27 13.5z"/></svg>')
    poster = "/images/video/wolves-removals-sussex-removals-and-storage-video-poster.webp"
    vid = (
        '<button type="button" class="yt-facade" data-id="aYsh2jIfp7g" '
        'data-title="Wolves Removals &mdash; Sussex Removals &amp; Storage" '
        f'style="background-image:url({poster})" aria-label="Play the Wolves Removals video (plays with sound off)">'
        f'<span class="yt-play">{play}</span></button>'
        '<p class="text-center text-sm text-darkgrey mt-3">See our Sussex team, vans and secure storage in action.</p>')
    inner = (
        '<div class="grid grid-cols-12 gap-y-8 lg:gap-12 items-center">'
        f'<div class="col-span-12 lg:col-span-5 text-black text-left">{html}</div>'
        f'<div class="col-span-12 lg:col-span-7">{vid}</div>'
        '</div>'
        f'<div class="mt-8 lg:mt-12 text-black text-left">{services_list}</div>'
        f'<script defer src="/js/lite-youtube.js?v={E.ASSET_VER}"></script>')
    return section(inner, bg="bg-white", extra="logo-row overflow-hidden")

def services():
    cards = [
        ("House Removals", "/services/house-removals/",
         "<p>We pack and load your possessions with great care, then unload and unpack them at your new home &mdash; exactly where they need to be.</p>"),
        ("Commercial Removals", "/services/commercial-removals/",
         "<p>We streamline the entire office relocation so your business is up and running fast, with custom crating for delicate equipment.</p>"),
        ("International Removals", "/services/international-removals/",
         "<p>Door-to-door European and worldwide moves with expert export packing, customs guidance and full tracking.</p>"),
        ("Student Removals", "/services/student-removals/",
         "<p>Flexible, affordable moves for students &mdash; to or from halls and shared houses, with optional storage between terms.</p>"),
        ("Man and Van", "/services/man-and-van/",
         "<p>Need items moved quickly from A to B? Our cost-effective man and van service brings the same care as a full move.</p>"),
        ("Specialist Antique Moving", "/services/specialised-antiques-moving/",
         "<p>As a LAPADA member we move antiques, fine art and valuables with bespoke packing, crating and white-glove handling.</p>"),
    ]
    return card_grid(cards, cols=3, heading="Our House Removal and Storage Services",
                     intro="From single items to full home and office moves, every job is handled by our trained, fully insured Sussex team.",
                     bg="bg-lightgrey")

def storage():
    cards = [
        ("Long-Term Storage", "/services/storage/long-term-storage/",
         "<p>Ideal for storage between moves, downsizing or freeing up space. Flexible, affordable terms from three months or more.</p>"),
        ("Short-Term Storage", "/services/storage/short-term-storage/",
         "<p>Perfect for moving delays, renovations or temporary transitions &mdash; from a couple of days to a few months.</p>"),
        ("Business Storage", "/services/storage/business-and-commercial-storage/",
         "<p>Secure containerised storage for stock, equipment and office furniture, fully managed including packing and unpacking.</p>"),
    ]
    return card_grid(cards, cols=3, heading="Need Long or Short-Term Storage?",
                     intro="Our containerised storage is clean, dry and ultra-secure &mdash; with a free online "
                           '<a href="/storage-calculator/">storage calculator</a> to size your space.', bg="bg-white",
                     bg_image=("storage-warehouse-aisle-wooden-containers",
                               "Wooden containerised storage units in the Wolves Removals Sussex store"))

def _guide_ver():
    """Cache-buster for the moving-guide flipbook: a hash of the PDF + the per-page
    JPGs (name/size/mtime). Regenerating the guide assets auto-busts the `?v=` query so
    visitors never get stale page images — independent of the CSS-based ASSET_VER."""
    import hashlib
    h = hashlib.md5()
    paths = [os.path.join(E.S.ROOT, "documents/wolves-removals-essential-moving-guide.pdf")]
    paths += sorted(glob.glob(os.path.join(E.S.ROOT, "images/guide-pages/page-*.jpg")))
    for p in paths:
        try:
            st = os.stat(p)
            h.update(f"{os.path.basename(p)}:{st.st_size}:{int(st.st_mtime)}".encode())
        except OSError:
            pass
    return h.hexdigest()[:8] or E.ASSET_VER

def guide_flipbook():
    pdf = "/documents/wolves-removals-essential-moving-guide.pdf"
    dl_icon = icon("download", "w-5 h-5 fill-current")
    v = _guide_ver()
    head = (
        '<div class="text-center max-w-3xl mx-auto mb-8">'
        '<h2 class="relative leading-tight text-black">Your Essential Guide to Moving Home</h2>'
        '<p class="text-lg xl:text-xl font-medium mt-3">Flick through our free, fillable 16-page moving guide below &mdash; packed '
        'with checklists, timings and practical tips from our Sussex removals team. Turn the pages just like a real '
        'booklet, or download it as a PDF to keep.</p></div>')
    book = (
        '<div class="guide-flipbook-wrap">'
        f'<div id="guide-flipbook" class="guide-flipbook" data-ver="{v}" aria-label="Wolves Removals Essential Guide to Moving Home '
        '(16 pages). Flick left or right to turn the page."></div>'
        '<div class="guide-flipbook-controls">'
        '<button type="button" id="guide-prev" class="guide-flipbook-btn" aria-label="Previous page">&larr; Prev</button>'
        '<span id="guide-page-indicator" class="guide-flipbook-indicator">Page 1 of 12</span>'
        '<button type="button" id="guide-next" class="guide-flipbook-btn" aria-label="Next page">Next &rarr;</button>'
        '</div>'
        '<p class="guide-flipbook-hint">Click or grab the page corners to turn &mdash; a soft page-turn sound plays as you flick.</p>'
        f'<div class="mt-6 flex justify-center"><a href="{pdf}?v={v}" download class="button-orange text-base lg:text-lg '
        f'px-8 py-4 inline-flex items-center gap-2" aria-label="Download the Wolves Removals essential moving guide as a PDF (16 pages)">'
        f'{dl_icon}Download the Guide (PDF, 12 pages)</a></div>'
        f'<script defer src="/js/vendor/page-flip.browser.js?v={E.ASSET_VER}"></script>'
        f'<script defer src="/js/guide-flipbook.js?v={E.ASSET_VER}"></script>'
        '</div>')
    return section(head + book, bg="bg-beige")

def trust():
    return E.trusted_by("bg-lightgrey")

def areas():
    pills = "".join(
        f'<a href="/{p}" class="px-5 py-2 rounded-full border border-border bg-white hover:border-orange hover:text-orange font-semibold">{esc(n)}</a>'
        for p, n in E.S.COUNTY_HUBS)
    return section(
        '<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2 text-center">'
        '<h2 class="relative leading-tight text-black">Areas We Cover</h2>'
        '<p class="text-lg xl:text-xl font-medium mt-2">We are well positioned to offer our removal services across the '
        'whole of Sussex and the wider South East:</p>'
        f'<div class="flex flex-wrap gap-3 justify-center mt-6">{pills}</div>'
        '<p class="mt-6"><a class="font-bold uppercase text-black hover:text-orange inline-flex items-center gap-1" href="/locations/">'
        'See every town we cover ' + icon("chevron", "h-4 w-4 -rotate-90 fill-current") + '</a></p>'
        '</div></div>', bg="bg-white", extra="logo-row overflow-hidden")

def process():
    return E.step_process(bg="bg-beige")

FAQS = [
    ("How much do removals cost in Sussex?",
     "<p>Removal costs depend on the size of your home, the distance, access and any packing or storage you need. As a "
     "guide, a local two-bedroom move in Sussex typically starts from a few hundred pounds. The most accurate way to "
     'find out is a free, no-obligation quote &mdash; <a href="/get-a-quote/">request yours here</a> or see our '
     '<a href="/pricing/">pricing page</a>.</p>'),
    ("Which areas do you cover?",
     '<p>We are based near Pulborough and cover the whole of <a href="/locations/west-sussex-removals/">West Sussex</a> '
     'and <a href="/locations/east-sussex-removals/">East Sussex</a>, plus '
     '<a href="/locations/surrey-removals/">Surrey</a>, <a href="/locations/hampshire-removals/">Hampshire</a> and '
     "nationwide and European destinations. See our <a href=\"/locations/\">areas we cover</a> for your town.</p>"),
    ("Do you provide packing materials and a packing service?",
     '<p>Yes. You can buy boxes and materials from our <a href="/box-shop/">box shop</a>, or let our '
     'team take care of everything with our <a href="/services/full-packing-service/">full packing</a> and '
     '<a href="/services/fragile-packing/">fragile packing</a> services.</p>'),
    ("Are you insured, and is my move protected?",
     "<p>Absolutely. Wolves Removals is fully insured and our team is professionally trained. We are also a LAPADA "
     "member for antiques and fine-art handling and Checkatrade-verified, so your belongings are in safe hands "
     "throughout your move.</p>"),
    ("Can you store my belongings between moves?",
     '<p>Yes &mdash; we offer clean, dry, ultra-secure containerised <a href="/services/storage/">storage</a> for both '
     '<a href="/services/storage/short-term-storage/">short</a> and '
     '<a href="/services/storage/long-term-storage/">long-term</a> needs, ideal when completion dates don&rsquo;t line '
     "up or while you renovate.</p>"),
]

def build():
    E.freeze_extras(True)   # leave the home page alone — exclude the merged 'extra variety' photos
    faq_html, faq_schema = faq_block(FAQS, heading="Have a Removals Question?", bg="bg-white", fancy=True)
    body = "\n".join([
        hero(),
        intro(),
        E.quote_bar(),
        services(),
        guide_flipbook(),
        storage(),
        trust(),
        E.wolves_feature_panel(E.page_photos("home-feature-panel", 1)[0], reverse=False, bg="bg-beige"),
        areas(),
        process(),
        E.photo_strip([p for p in E.page_photos("home-gallery", 5) if "/" + p[0] + "." not in HERO_IMG][:3], heading="See Our Sussex Movers in Action",
                      intro="Our trained, fully insured team on recent moves across Sussex.", bg="bg-white"),
        E.video_embed("wolves-removals-promo-b", bg="bg-beige"),
        cta_band("Interested in Our Services? Get In Touch for a Free Quote",
                 "Simply fill in our quick form, call us or email us and a friendly member of our team will be in touch.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
        faq_html,
    ])
    doc = E.render_page(
        title="Sussex Removals Company | Wolves Removals, Pulborough",
        description="Wolves Removals is a trusted, family-run Sussex removals company in Pulborough. Home & commercial removals, packing and secure storage across the South East.",
        canonical_path="/",
        body=body,
        og_image=HERO_IMG,
        breadcrumb=[("Home", "/")],
        extra_schema=[faq_schema],
        active="home",
    )
    out = E.write("index.html", doc)
    E.freeze_extras(False)   # restore full pool for all other pages
    print("wrote", out, f"({len(doc):,} bytes)")

if __name__ == "__main__":
    build()
