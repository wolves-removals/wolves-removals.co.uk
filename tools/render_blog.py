# -*- coding: utf-8 -*-
"""Build the blog: reads data/blog/*.json (one per post) -> renders /blog/<slug>/
pages + the /blog/ index (newest first). Adds BlogPosting + FAQPage + Breadcrumb schema.
Each post JSON schema:
{
  "slug","title","meta","h1","date" (YYYY-MM-DD),"category",
  "lead": "<p>..</p>",              # intro / excerpt
  "body": "<h2>..</h2><p>..</p>",   # >=2000 words
  "faqs": [["Q","<p>A</p>"], ...],
  "related": ["slug", ...]
}"""
import os, sys, json, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, card_grid, cta_band, faq_block

HERO = "images/photos/wolves-crew-busy-sussex-moving-day.webp"
BLOG_DIR = os.path.join(E.S.ROOT, "data", "blog")

def load_posts():
    posts = []
    for f in glob.glob(os.path.join(BLOG_DIR, "*.json")):
        try:
            p = json.load(open(f, encoding="utf-8"))
            if p.get("slug") and p.get("body"):
                posts.append(p)
        except Exception as e:
            print(f"  ! skip {os.path.basename(f)}: {e}")
    posts.sort(key=lambda p: p.get("date", "2024-01-01"), reverse=True)
    return posts

def _hero(p, photo=None):
    src = ("images/photos/" + photo[0] + ".webp") if photo else HERO
    hero_img = img(src, f"Wolves Removals blog — {esc(p['h1'])[:60]}", cls="w-full h-full object-cover", eager=True)
    cat = f'<span class="inline-block bg-orange text-white text-sm font-semibold uppercase px-3 py-1 rounded-full mb-3">{esc(p.get("category","Moving Advice"))}</span>'
    return ('<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
            f'<div class="absolute inset-0">{hero_img}</div>'
            '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
            f'{cat}<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{p["h1"]}</h1>'
            f'<div class="mt-4 text-lg xl:text-xl max-w-3xl">{p.get("lead","")}</div>'
            f'<p class="mt-4 text-beige text-sm">Published {esc(p.get("date",""))} &middot; Wolves Removals</p>'
            f'{E.hero_review_row()}'
            '</div></div></div></section>')

def _blogposting_schema(p, photo=None):
    image = E.abs_url("images/photos/" + photo[0] + ".webp") if photo else E.abs_url(HERO)
    return {"@context": "https://schema.org", "@type": "BlogPosting",
            "headline": p["h1"], "datePublished": p.get("date", ""), "dateModified": p.get("date", ""),
            "author": {"@type": "Organization", "name": "Wolves Removals", "url": E.S.SITE_URL},
            "publisher": {"@type": "Organization", "name": "Wolves Removals",
                          "logo": {"@type": "ImageObject", "url": E.abs_url("images/brand/wolves-removals-logo.png")}},
            "mainEntityOfPage": E.abs_url(f"/{p['slug']}/"),
            "image": image, "description": p.get("meta", "")}

def build_post(p, by_slug):
    pics = E.page_photos(p["slug"], 14)
    _used = {pics[0][0]}   # topic-matched body photos avoid the hero + each other
    schema = [_blogposting_schema(p, pics[0])]
    faqs = [(q, a) for q, a in p.get("faqs", [])]
    # Split the article at its <h2> headings so each section becomes a rich,
    # alternating block (same treatment as the service pages) rather than one wall of text.
    chunks = [c.strip() for c in re.split(r'(?=<h2)', p["body"]) if c.strip()]
    pi = [1]
    def npic():
        x = pics[pi[0] % len(pics)]; pi[0] += 1; return x
    nbn = [0]
    def nbg():
        b = "bg-white" if nbn[0] % 2 == 0 else "bg-beige"; nbn[0] += 1; return b
    cvn = [0]; wrn = [0]
    # Cap how many photos the article body uses so long posts stay within the photo
    # pool (hero + feature + 7-image gallery + related + sitewide feed already use ~22).
    def can_pic():
        return pi[0] <= 12
    def rich_row(chunk):
        bg = nbg()
        side = "left" if wrn[0] % 2 == 1 else "right"; wrn[0] += 1
        photo = E._row_photo(p["slug"], chunk, _used, wrn[0])   # topic-matched, unused, R9-safe
        if bg == "bg-beige":  # cream rows become a photo+text card
            v = (cvn[0] % 3) + 1; cvn[0] += 1
            return E.content_card(chunk, variant=v, bg=bg, photo=photo, img_side=side)
        # white rows: image stretches to the text height (so they match) with a min size,
        # so short sections still get a proper image instead of a thin crop.
        return E._split_row(chunk, photo, reverse=(side == "left"), bg=bg, min_h="22rem")
    parts = [_hero(p, pics[0]),
             E.quote_bar(lead="Moving House Soon?", rest="Get a Free Quote",
                         subtext="Get a fast, fixed price from your local Sussex removals team.")]
    if len(chunks) <= 1:  # no headings to split on
        if p["body"].count("<p") >= 2:
            parts.append(E.media_rows(p["body"], f"{p['slug']}-body", nbg, used=_used, group=3, min_h="22rem"))
        else:
            ph = E._row_photo(p["slug"], p["body"], _used)
            parts.append(E._split_row(p["body"], ph, bg="bg-white", min_h="22rem"))
        parts.append(E.wolves_feature_panel(npic(), reverse=False, bg="bg-beige"))
    else:
        panel_at = max(1, len(chunks) // 2)
        for i, chunk in enumerate(chunks):
            if chunk.count("<p") >= 2:   # site rule: 2+ paragraphs -> topic-matched split rows
                parts.append(E.media_rows(chunk, f"{p['slug']}-c{i}", nbg, used=_used, group=3, min_h="22rem"))
            elif i == 0:
                ph = E.match_photo(chunk, _used) or npic(); _used.add(ph[0])
                parts.append(E.text_with_image(chunk, ph, reverse=False, bg=nbg()))
            else:
                parts.append(rich_row(chunk))
            if i == panel_at:  # a brand/trust feature panel partway through
                parts.append(E.wolves_feature_panel(npic(), reverse=True, bg=nbg()))
    parts.append(E.photo_strip([npic(), npic(), npic()], heading="", bg=nbg(), seed=p["slug"]))
    if faqs:
        fhtml, fschema = faq_block(faqs, heading=f"{esc(p['h1'])} &mdash; FAQs", bg=nbg())
        parts.append(fhtml); schema.append(fschema)
    rel = [by_slug[s] for s in p.get("related", []) if s in by_slug][:3]
    if len(rel) >= 3:  # image-led related cards (matches the blog index)
        cards = [(r["h1"][:60], f"/{r['slug']}/",
                  f'<p><span class="text-orange font-semibold text-sm uppercase">{esc(r.get("category","Advice"))}</span><br>'
                  f'{esc((r.get("lead","") and re.sub("<[^>]+>","",r["lead"]))[:120])}</p>',
                  E.page_photos(r["slug"], 1)[0]) for r in rel]
        parts.append(card_grid(cards, cols=3, heading=f"More Guides Like &ldquo;{esc(p['h1'][:34])}&rdquo;", bg="bg-lightgrey"))
    parts.append(cta_band("Planning a Move in Sussex?", "Get a free, no-obligation quote from our friendly, fully insured team.",
                          "Get a Free Quote", "/get-a-quote/", bg="bg-white"))
    doc = E.render_page(title=p["title"], description=p["meta"], canonical_path=f"/{p['slug']}/",
        body="\n".join(parts), og_image="images/photos/" + pics[0][0] + ".webp",
        breadcrumb=[("Home", "/"), ("Blog", "/blog/"), (p["h1"][:50], f"/{p['slug']}/")],
        extra_schema=schema, active="blog")
    return E.write(f"{p['slug']}/index.html", doc)

def build_index(posts):
    import json
    from datetime import datetime as _dt
    # Synonym map so the search matches what people actually type (e.g. "moving" -> removals).
    SYN = {"removal": "moving move relocation relocate", "storage": "store self storage units",
           "packing": "pack boxes wrapping materials", "man and van": "small move van",
           "antique": "antiques fine art valuables heirloom", "office": "commercial business workplace",
           "commercial": "office business", "international": "european overseas abroad",
           "clearance": "house clearance rubbish waste", "student": "uni university",
           "fragile": "delicate glassware china", "piano": "instrument"}
    def _syn(text):
        t = text.lower()
        return " ".join(v for k, v in SYN.items() if k in t)
    def _lead(p):
        return re.sub("<[^>]+>", "", p.get("lead", "") or "").strip()
    def _blob(p):
        base = p["h1"] + " " + p.get("category", "") + " " + _lead(p)
        return (base + " " + _syn(base)).lower()
    def _fmt(d):
        try: return _dt.strptime(d, "%Y-%m-%d").strftime("%-d %B %Y")
        except Exception: return ""
    _used_thumbs = set(); _post_thumb = {}
    for _p in posts:   # distinct thumbnail per post so no image repeats across the grid
        _pick = next((c for c in E.page_photos(_p["slug"], 40) if c[0] not in _used_thumbs),
                     E.page_photos(_p["slug"], 1)[0])
        _used_thumbs.add(_pick[0]); _post_thumb[_p["slug"]] = _pick
    def _card(p):
        pic = _post_thumb[p["slug"]]
        q = esc(_blob(p))
        return (f'<a href="/{p["slug"]}/" data-blog-card data-q="{q}" class="group flex flex-col h-full bg-white border border-border rounded-xl shadow-custom overflow-hidden transition hover:shadow-lg">'
                f'<div class="overflow-hidden" style="aspect-ratio:16/10;">'
                f'{img("images/photos/" + pic[0] + ".webp", pic[1], cls="w-full h-full object-cover")}</div>'
                f'<div class="flex flex-col flex-1 p-6">'
                f'<h3 class="text-lg xl:text-xl font-bold text-black group-hover:text-orange leading-snug">{esc(p["h1"])}</h3>'
                f'<p class="mt-3 text-darkgrey leading-relaxed line-clamp-6 flex-1">{esc(_lead(p)[:280])}</p>'
                f'<div class="mt-5 pt-4 border-t border-border text-sm font-semibold text-darkgrey">Wolves Removals &middot; {_fmt(p.get("date",""))}</div>'
                f'</div></a>')
    grid = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">' + "".join(_card(p) for p in posts) + '</div>'
    # Smart-search index (embedded JSON) + topic suggestions.
    search_posts = [{"t": p["h1"], "u": f'/{p["slug"]}/', "c": p.get("category", "Advice"),
                     "i": "/images/photos/" + _post_thumb[p["slug"]][0] + ".webp", "s": _blob(p)}
                    for p in posts]
    _topics = sorted(set(p.get("category", "Advice") for p in posts) |
                     {"Removals", "Packing", "Storage", "Man and Van", "Antiques", "Commercial", "International", "Local Guides"})
    index_json = json.dumps({"posts": search_posts, "topics": _topics}, ensure_ascii=False).replace("<", "\\u003c")
    main_col = ('<div class="mb-8"><h2 class="relative leading-tight text-black">Recent Articles</h2>'
                '<p class="text-lg xl:text-xl font-medium mt-3 text-darkgrey">Moving advice, packing tips, storage ideas and local '
                'guides from our experienced Sussex removals team &mdash; newest first.</p></div>' + grid +
                '<p id="blog-search-empty" style="display:none" class="text-center text-darkgrey text-lg mt-10">'
                'No articles match your search &mdash; try a different word.</p>')
    b = E.S.BUSINESS
    recent = "".join(
        f'<li><a href="/{p["slug"]}/" class="block py-3 border-b border-border text-black hover:text-orange font-medium leading-snug">{esc(p["h1"])}</a></li>'
        for p in posts[:10])
    _ipt = "w-full rounded-lg border-0 px-4 py-3 text-black"
    sidebar = (
        '<div class="mb-10"><h2 class="text-2xl font-bold text-black leading-tight">Search</h2>'
        '<div class="w-16 h-1 bg-orange rounded mt-2 mb-3"></div>'
        '<div class="relative">'
        '<input type="search" id="blog-search" placeholder="Search articles&hellip;" aria-label="Search articles" autocomplete="off" '
        'role="combobox" aria-expanded="false" aria-controls="blog-search-results" aria-autocomplete="list" '
        'class="w-full rounded-lg border border-border bg-white pl-11 pr-4 py-3 text-black focus:border-orange focus:outline-none">'
        '<svg class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-darkgrey pointer-events-none" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle>'
        '<path d="M21 21l-4.3-4.3" stroke-linecap="round"></path></svg>'
        '<div id="blog-search-results" role="listbox" aria-label="Search results" '
        'class="hidden absolute left-0 right-0 top-full mt-2 z-50 bg-white border border-border rounded-xl shadow-lg max-h-[26rem] overflow-y-auto"></div>'
        '</div>'
        f'<script type="application/json" id="blog-search-index">{index_json}</script></div>'
        '<div class="mb-10"><h2 class="text-2xl font-bold text-black leading-tight">Recent News</h2>'
        '<div class="w-16 h-1 bg-orange rounded mt-2 mb-3"></div>'
        f'<ul class="list-none p-0 m-0">{recent}</ul></div>'
        '<div class="mb-10"><h2 class="text-2xl font-bold text-black leading-tight">Quote Or Question?</h2>'
        '<div class="w-16 h-1 bg-orange rounded mt-2 mb-5"></div>'
        '<div class="bg-darkgrey text-white rounded-2xl p-6 lg:p-8 shadow-custom">'
        f'<p class="text-center font-bold text-lg">Call us <a class="text-white underline hover:no-underline" href="{b["phone_link"]}">{b["phone"]}</a></p>'
        '<p class="text-center font-bold my-2">Or</p>'
        '<p class="text-center font-bold text-lg mb-5">Message Us</p>'
        '<form class="space-y-3" method="post" action="/api/contact" novalidate>'
        f'<input type="text" name="first_name" placeholder="Your Name" class="{_ipt}" required>'
        f'<input type="email" name="email" placeholder="Your Email" class="{_ipt}" required>'
        f'<input type="tel" name="phone" placeholder="Your Phone" class="{_ipt}">'
        f'<input type="text" name="enquiry" placeholder="Best time to call back" class="{_ipt}">'
        '<button type="submit" class="w-full bg-white text-darkgrey font-bold uppercase tracking-wide rounded-lg px-4 py-3 hover:bg-black hover:text-white transition">Submit</button>'
        '</form></div></div>'
        '<div class="bg-darkgrey text-white rounded-2xl p-6 lg:p-8 text-center shadow-custom">'
        '<h3 class="text-xl font-bold leading-tight mb-3">Get Our Moving Services at Competitive Prices</h3>'
        '<p class="mb-5">Fast, fixed, no-obligation quotes from your local Sussex team.</p>'
        '<a href="/get-a-quote/" class="inline-block bg-white text-darkgrey font-bold uppercase tracking-wide rounded-full px-7 py-3 hover:bg-black hover:text-white transition">Get a Free Quote</a>'
        '</div>')
    two_col = section(
        '<div class="grid grid-cols-12 gap-8 lg:gap-12 items-start">'
        f'<div class="col-span-12 lg:col-span-8">{main_col}</div>'
        f'<aside class="col-span-12 lg:col-span-4">{sidebar}</aside>'
        '</div>', bg="bg-lightgrey", extra="logo-row overflow-hidden")
    faqs = [
        ("What does the Wolves Removals blog cover?",
         "<p>Our blog shares moving advice, packing and storage tips, and local area guides from our experienced Sussex removals team &mdash; practical, first-hand guidance to help your move go smoothly.</p>"),
        ("How often do you publish new articles?",
         "<p>We add new guides regularly, covering everything from packing fragile items to choosing a removals company and moving to towns across Sussex. Check back often, or <a href=\"/contact-us/\">get in touch</a> with a question.</p>"),
        ("Can Wolves Removals help with my move, not just offer advice?",
         "<p>Of course &mdash; alongside our guides we offer full home and commercial removals, expert packing and secure storage across Sussex and beyond. <a href=\"/get-a-quote/\">Request a free quote</a> to get started.</p>"),
        ("Where can I read reviews of Wolves Removals?",
         "<p>You can read genuine, verified customer reviews on our <a href=\"/reviews/\">reviews page</a>, as well as on Google, Checkatrade and Facebook.</p>"),
    ]
    body = "\n".join([
        _hero({"h1": "Removals & Moving Blog", "lead": "<p>Tips, guides and advice from Sussex&rsquo;s family-run removals team.</p>",
               "category": "Blog", "date": ""}),
        E.quote_bar(lead="Planning Your Move?", rest="Get a Free Quote",
                    subtext="Tell us about your move for a clear, no-obligation price."),
        two_col if posts else section('<p class="text-center">Articles coming soon.</p>', bg="bg-lightgrey"),
        faq_block(faqs, heading="The Blog &mdash; Your Questions Answered", bg="bg-white")[0],
        cta_band("Ready to Move?", "Let our experienced, fully insured team take the strain.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
        f'<script defer src="/js/blog-search.js?v={E.ASSET_VER}"></script>',
    ])
    doc = E.render_page(title="Removals & Moving Blog | Wolves Removals Sussex",
        description="Moving advice, packing tips, storage ideas and local guides from Wolves Removals — Sussex's family-run removals and storage experts.",
        canonical_path="/blog/", body=body, og_image=HERO,
        extra_schema=[faq_block(faqs, heading="x")[1]], dedupe=False,
        breadcrumb=[("Home", "/"), ("Blog", "/blog/")], active="blog")
    return E.write("blog/index.html", doc)

def build():
    posts = load_posts()
    by_slug = {p["slug"]: p for p in posts}
    for p in posts:
        build_post(p, by_slug)
    build_index(posts)
    print(f"built {len(posts)} blog posts + index")

if __name__ == "__main__":
    build()
