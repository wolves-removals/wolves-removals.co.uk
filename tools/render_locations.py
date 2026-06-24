# -*- coding: utf-8 -*-
"""Build all /locations/ pages (towns + county hubs).
Mirrors the live location-page structure (town woven throughout) and expands every
page past 1500 words with county context, nearby cross-links, services, storage,
process, town-specific FAQs (+FAQPage schema), LocalBusiness + Breadcrumb schema.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, card_grid, cta_band, faq_block
sys.path.insert(0, os.path.join(E.S.ROOT, "data"))
import locations as L
import zlib

def zlib_idx(s):
    return zlib.crc32(str(s).encode())

COUNTY_BLURB = {
    "West Sussex": ("West Sussex combines coastal towns, busy market centres and rural villages, so no two moves are "
                    "the same. From seafront flats to large countryside homes, our team knows the access, parking and "
                    "route challenges across the county and plans every {town} move accordingly."),
    "East Sussex": ("East Sussex stretches from the South Downs to the coast, with narrow lanes, conservation areas and "
                    "period properties that demand careful handling. Our crews move regularly throughout the county and "
                    "plan each {town} removal around its access and parking."),
    "Surrey": ("Surrey blends commuter towns, leafy villages and larger family homes, often with tight driveways and "
               "restricted parking. We plan each {town} move around access, permits and timing so your day runs to "
               "schedule."),
    "Hampshire": ("Hampshire ranges from the South Downs to historic market towns. We cover {town} and the surrounding "
                  "area regularly, planning each move around local access, routes and timing."),
    "Kent": ("Kent's mix of historic towns and rural villages brings its own access and parking considerations. We plan "
             "each {town} move carefully so collection and delivery run smoothly."),
}

INTROS = [
    ("Planning a {town} removal is easier with a dependable, fully insured team by your side. At Wolves Removals we "
     "deliver professional removals in {town} for both local moves and long-distance relocations, managing every stage "
     "with care from the first box to the last."),
    ("Looking for a reliable {town} removals company? Wolves Removals provides careful, fully insured home and business "
     "moves in {town} and across {county}, handling packing, transport, storage and unpacking so your move feels "
     "effortless."),
    ("Moving in or out of {town}? Wolves Removals is a trusted, family-run removals company offering professional {town} "
     "removals, secure storage and expert packing &mdash; with the local knowledge to keep your move on schedule."),
]

def usp(town):
    items = [
        f"Professional, fully insured removals in {town}",
        "Trained, experienced movers &mdash; 100+ years' combined experience",
        "Upfront, transparent pricing with no hidden surprises",
        "Local knowledge for a smooth, personalised move",
        "Containerised storage, long and short-term",
    ]
    return "".join(
        f'<li class="flex items-start gap-2"><span class="text-green mt-1 shrink-0">{icon("check-bold","w-5 h-5")}</span><span>{esc(t)}</span></li>'
        for t in items)

def hero(town, county, photo):
    intro = INTROS[zlib_idx(town) % len(INTROS)].format(town=town, county=county)
    hero_img = img("images/photos/" + photo[0] + ".webp", f"Wolves Removals team carrying out a removal in {town}",
                   cls="w-full h-full object-cover", eager=True)
    bullets = f'<ul class="space-y-2 list-none p-0">{usp(town)}</ul>'
    return (
        '<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
        f'<div class="absolute inset-0">{hero_img}</div>'
        '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
        f'<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{esc(town)} Removals Company</h1>'
        f'<p class="mt-4 text-lg xl:text-xl max-w-2xl">{intro}</p>'
        f'{E.hero_review_row(bullets)}'
        '</div></div></div></section>')

def about(town, county, styler=None):
    blurb = COUNTY_BLURB.get(county, COUNTY_BLURB["West Sussex"]).format(town=town)
    hub = next((h for h in L.HUBS if county in h[2]), None)
    hublink = f'<a href="/locations/{hub[0]}/">{esc(county)}</a>' if hub else esc(county)
    html = (
        f'<h2 class="relative leading-tight text-black">Professional Removals in {esc(town)}</h2>'
        f'<p>Moving home can be exciting, but it can also feel stressful. With Wolves Removals, your {esc(town)} move '
        'becomes a seamless, worry-free journey. As a trusted, family-run removals company based near '
        '<a href="/locations/pulborough-removals/">Pulborough</a> in West Sussex, we have been keeping our promises '
        f'since 2016 &mdash; and we cover {esc(town)} and the wider {hublink} area for both home and business moves.</p>'
        f'<p>Our dedicated team of professional {esc(town)} removal experts handles every aspect of your move with the '
        'utmost care and efficiency, making sure your belongings arrive safely, on time and exactly as they left. We are '
        'a <strong>LAPADA member</strong>, <strong>Checkatrade-verified</strong> and <strong>fully insured</strong>, so '
        f'your possessions are in safe hands throughout your {esc(town)} removal.</p>'
        f'<p>{blurb}</p>'
        '<p>Our comprehensive range of services includes:</p>'
        '<ul class="tick-list">'
        f'<li>Local, long-distance and <a href="/services/international-removals/">international moving</a> within the UK &amp; EU</li>'
        '<li>Expert <a href="/services/full-packing-service/">packing</a> and <a href="/services/full-unpacking-service/">unpacking</a> services</li>'
        '<li><a href="/services/specialised-antiques-moving/">Antique and valuable item</a> transportation</li>'
        '<li><a href="/services/piano-moving/">Heavy and speciality item</a> removal and transportation</li>'
        '<li>Convenient local <a href="/services/man-and-van/">man and van hire</a></li>'
        '<li>Short and long-term <a href="/services/storage/">secure storage</a> facilities</li>'
        '</ul>')
    return styler(html, "bg-white") if styler else section(prose(html, span="lg:col-span-10 lg:col-start-2"), bg="bg-white")

def services_in(town, bg="bg-lightgrey"):
    cards = [
        ("House Removals", "/services/house-removals/",
         f"<p>We pack and load your belongings with great care, then unload and unpack them at your new {esc(town)} home exactly where you want them.</p>"),
        ("Commercial Removals", "/services/commercial-removals/",
         "<p>We streamline your office relocation &mdash; including unpacking &mdash; so your business is back up and running fast.</p>"),
        ("International Removals", "/services/international-removals/",
         "<p>Door-to-door European and worldwide moves with expert export packing and customs guidance.</p>"),
        ("Man and Van", "/services/man-and-van/",
         f"<p>A flexible, cost-effective option for smaller {esc(town)} moves, with the same care as a full removal.</p>"),
        ("Packing Services", "/services/full-packing-service/",
         "<p>Full or fragile-only packing using quality materials, protecting your most delicate items.</p>"),
        ("Secure Storage", "/services/storage/",
         "<p>Clean, dry, containerised storage for short or long-term needs, fully managed by our team.</p>"),
    ]
    return card_grid(cards, cols=3, heading=f"Our {town} Removal &amp; Storage Services",
                     intro=f"Every {esc(town)} job is handled by our trained, fully insured team &mdash; from a single item to a full home or office move.",
                     bg=bg)

def why_choose(town, bg="bg-white"):
    rows = [
        ("Fully insured &amp; trusted", f"Every {esc(town)} move is fully insured, and we are LAPADA and Checkatrade verified."),
        ("Trained, experienced team", "Our movers bring over 100 years' combined experience and treat every home with respect."),
        ("Transparent pricing", "Clear, fixed written quotes with no hidden extras &mdash; you know the cost up front."),
        ("Local knowledge", f"We know the roads, parking and access around {esc(town)}, so your move runs to schedule."),
    ]
    cells = "".join(
        f'<div class="col-span-12 md:col-span-6"><div class="group flex gap-3 h-full bg-white rounded-xl border border-border shadow-custom p-6 transition-colors duration-200 hover:bg-darkgrey hover:border-darkgrey">'
        f'<span class="ico-badge shrink-0 w-10 h-10">{icon("check-bold","w-5 h-5")}</span>'
        f'<div><h3 class="text-lg font-semibold text-black group-hover:text-white">{t}</h3><p class="mt-1 text-darkgrey group-hover:text-beige mb-0">{d}</p></div></div></div>'
        for t, d in rows)
    return section(
        f'<div class="text-center mb-8"><h2 class="relative leading-tight text-black">Why {esc(town)} Chooses Wolves Removals</h2></div>'
        f'<div class="grid grid-cols-12 gap-6">{cells}</div>', bg=bg)

def process_section(town, bg="bg-lightgrey"):
    # Unified chevron step-process design (shared with the home page); town-specific heading.
    return E.step_process(bg=bg, heading=f"Our Step-by-Step {esc(town)} Move")

def local_section(town, county, photo):
    heading = f'<h2 class="relative leading-tight text-black">Local Moving in {esc(town)}</h2>'
    body = (
        f'<p>Every {esc(town)} move is different, and the details matter. Before moving day we check access at both '
        'properties &mdash; parking restrictions, narrow lanes, stairs, lifts and any permits that might be needed &mdash; '
        f'so there are no surprises on the day. That local planning is what keeps a {esc(town)} removal running on time.</p>'
        f'<p>Whether you are moving from a flat, a terraced house or a large family home in or around {esc(town)}, our '
        'team scales to suit, bringing the right vehicle, equipment and crew. We protect floors, doorways and furniture as '
        'standard, and handle fragile or high-value items &mdash; from glassware to '
        '<a href="/services/specialised-antiques-moving/">antiques</a> and '
        '<a href="/services/piano-moving/">pianos</a> &mdash; with specialist care.</p>'
        f'<p>If your {esc(town)} move involves a gap between completion dates, our '
        '<a href="/services/storage/">containerised storage</a> keeps your belongings clean, dry and secure for as long '
        'as you need. And if you would rather not lift a finger, our '
        '<a href="/services/full-packing-service/">full packing service</a> takes care of everything, room by room. '
        'For a clear idea of cost, see our <a href="/pricing/">pricing guide</a> or '
        '<a href="/get-a-quote/">request a free, no-obligation quote</a>.</p>'
        f'<p>To get started, we recommend a free survey &mdash; either a quick video walkthrough or an in-home visit '
        f'&mdash; so we can understand your {esc(town)} move in detail and give you an accurate, fixed price. There is no '
        'obligation, and it lets us plan vehicles, crew, packing materials and any specialist handling well in advance. '
        'From that first conversation to the moment you settle into your new home, you will have a dedicated move '
        'coordinator on hand to answer questions and keep everything on track.</p>')
    return E.feature_panel(heading, body, photo, reverse=False, bg="bg-beige", with_cta=True)

def prep_section(town, county, styler=None):
    t = esc(town); c = esc(county)
    html = (
        f'<h2 class="relative leading-tight text-black">Preparing for Your {t} Move</h2>'
        f'<p>A little preparation makes a big difference to how smoothly your {t} removal runs. We recommend starting '
        'six to eight weeks ahead where you can: confirm your dates, book your survey and begin a room-by-room '
        f'declutter so you only pay to move what you actually want in your new {c} home. Anything you are unsure about, '
        'our team is happy to advise on &mdash; from what can be stored to what is best left behind.</p>'
        f'<p>Packing is usually the biggest job of any {t} move. You can pack yourself using our boxes and materials, '
        'or hand it over entirely to our <a href="/services/full-packing-service/">full packing service</a>. Either way, '
        'we strongly recommend professional <a href="/services/fragile-packing/">fragile packing</a> for glassware, '
        'mirrors, artwork and anything sentimental. Label every box clearly by room, and keep a separate &ldquo;first '
        f'night&rdquo; box of essentials so you are not hunting through cartons on your first evening in {t}.</p>'
        f'<p>In the final week before your {t} move, let your utility providers, bank and the {c} council know you are '
        'moving, arrange mail redirection, and run down your fridge and freezer ready for defrosting. It also pays to '
        f'plan access at both properties &mdash; parking, narrow lanes, stairs or lifts &mdash; which we will already '
        f'have noted at your survey so your {t} crew arrives ready to work. If your completion dates do not quite line '
        'up, our <a href="/services/storage/">secure containerised storage</a> bridges the gap for as long as you need.</p>'
        f'<p>On moving day itself, our trained, fully insured {t} team handles the heavy lifting, protects your floors '
        'and furniture as standard, and places everything in the right room at the other end &mdash; unpacking as much '
        'as you would like. To make your move easier still, you can download our free '
        '<a href="/">essential moving guide</a> and work through it at your own pace.</p>'
        f'<p>What sets a {t} move with Wolves Removals apart is the personal, local service behind it. As a family-run '
        f'company that has been keeping its promises since 2016, we treat every {t} home as if it were our own, and you '
        'will deal with the same friendly, accountable team from your first enquiry to the final box. Because we are '
        f'based locally and know {c} well, we plan realistic timings around traffic, access and parking rather than '
        'rushing the day. As a LAPADA member and Checkatrade-verified, fully insured company, you have genuine '
        f'reassurance that your {t} removal is handled to a professional standard &mdash; and if anything changes in the '
        'run-up to your move, your dedicated coordinator is only ever a phone call or email away.</p>'
        '<ul class="tick-list">'
        f'<li>Free, no-obligation survey and fixed written quote for your {t} move</li>'
        '<li><a href="/services/full-packing-service/">Packing</a>, <a href="/services/full-unpacking-service/">unpacking</a> and furniture dismantling and reassembly</li>'
        '<li>Specialist care for <a href="/services/specialised-antiques-moving/">antiques</a>, <a href="/services/piano-moving/">pianos</a> and high-value items</li>'
        f'<li>Short and long-term <a href="/services/storage/">storage</a> close to {t} when you need it</li>'
        '</ul>')
    return styler(html, "bg-white") if styler else section(prose(html, span="lg:col-span-10 lg:col-start-2"), bg="bg-white")

def nearby_section(slug, town, county):
    near = L.nearby(slug)
    hub = next((h for h in L.HUBS if county in h[2]), None)
    pills = "".join(
        f'<a href="/locations/{s}/" class="px-5 py-2 rounded-full border border-border bg-white hover:border-orange hover:text-orange font-semibold">{esc(n)}</a>'
        for s, n, _ in near)
    hub_pill = (f'<a href="/locations/{hub[0]}/" class="px-5 py-2 rounded-full border border-border bg-white hover:border-orange hover:text-orange font-semibold">All {esc(county)}</a>' if hub else "")
    map_html = E.map_embed(f"{town}, {county}, UK", f"{town}, {county}")
    return section(
        '<div class="grid grid-cols-12 gap-8 lg:gap-12 items-stretch">'
        '<div class="col-span-12 lg:col-span-6 self-center">'
        f'<h2 class="relative leading-tight text-black">Areas Near {esc(town)} We Also Cover</h2>'
        f'<p class="text-lg xl:text-xl font-medium mt-2">We move households and businesses throughout {esc(county)} and the '
        'wider South East. A few of the nearby towns we serve:</p>'
        f'<div class="flex flex-wrap gap-3 mt-6">{pills}{hub_pill}</div>'
        f'<p class="mt-6"><a class="font-bold uppercase text-orange inline-flex items-center gap-1" href="/locations/">See every area we cover {icon("chevron","h-4 w-4 -rotate-90 fill-current")}</a></p>'
        '</div>'
        f'<div class="col-span-12 lg:col-span-6">{map_html}</div>'
        '</div>', bg="bg-lightgrey")

def town_faqs(town, county):
    return [
        (f"How much do removals cost in {town}?",
         f"<p>The cost of a {esc(town)} removal depends on the size of your property, the distance, access and any "
         'packing or storage you need. The best way to get an accurate figure is a free, no-obligation quote &mdash; '
         '<a href="/get-a-quote/">request yours here</a> or see our <a href="/pricing/">pricing guide</a>.</p>'),
        (f"Do you offer same-day or short-notice moves in {town}?",
         f"<p>Where our schedule allows, we can accommodate short-notice and urgent {esc(town)} moves, including our "
         '<a href="/services/man-and-van/">man and van</a> service. Contact us as early as you can and we&rsquo;ll do '
         "our best to fit you in.</p>"),
        (f"Can you store my belongings in or near {town}?",
         '<p>Yes &mdash; we offer clean, dry, ultra-secure containerised <a href="/services/storage/">storage</a> for '
         '<a href="/services/storage/short-term-storage/">short</a> and '
         f'<a href="/services/storage/long-term-storage/">long-term</a> needs, ideal when completion dates for your '
         f'{esc(town)} move don&rsquo;t line up.</p>'),
        (f"Are you insured for removals in {town}?",
         f"<p>Absolutely. Every {esc(town)} move is fully insured and carried out by our trained team. We are also a "
         "LAPADA member for antiques and fine art and Checkatrade-verified for added peace of mind.</p>"),
        (f"Which areas around {town} do you cover?",
         f"<p>As well as {esc(town)}, we cover the whole of {esc(county)} and the wider South East, plus nationwide and "
         'European moves. See our <a href="/locations/">areas we cover</a> for your town.</p>'),
        (f"Do you supply packing materials for a {town} move?",
         f"<p>Yes. You can buy sturdy boxes, tape, bubble wrap and specialist cartons for your {esc(town)} move, or let "
         'our team take care of it all with our <a href="/services/full-packing-service/">full packing</a> and '
         '<a href="/services/fragile-packing/">fragile packing</a> services. We can also collect used boxes afterwards '
         'when one of our vans is next in the area.</p>'),
        (f"Will you dismantle and reassemble furniture in {town}?",
         f"<p>We can. Just let us know at the quote stage which items need taking apart and rebuilding for your "
         f"{esc(town)} move &mdash; beds, wardrobes and flat-pack units are all part of the service &mdash; and our team "
         "will handle it safely at both ends so you don&rsquo;t have to.</p>"),
    ]

def build_town(slug, town, county):
    pics = E.page_photos(slug, 5)
    styler = E.make_prose_styler(slug, E.page_photos(slug, 12))
    faqs = town_faqs(town, county)
    faq_html, faq_schema = faq_block(faqs, heading=f"{town} Removals &mdash; Your Questions Answered", bg="bg-white")
    body = "\n".join([
        hero(town, county, pics[0]),
        E.quote_bar(lead=f"Moving in {town}?", rest="Get a Free Quote",
                    subtext=f"Find out how much your {town} move will cost."),
        about(town, county, styler), services_in(town), E.trust_reviews_row(), why_choose(town),
        process_section(town), local_section(town, county, pics[1]), prep_section(town, county, styler),
        nearby_section(slug, town, county),
        E.storage_cta(seed=slug),
        E.photo_strip(pics[2:5], heading=f"Wolves Removals in {town}",
                      intro=f"Our trained, fully insured team on recent moves around {esc(town)} and the wider area.",
                      bg="bg-white"),
        cta_band(f"Get In Touch for a Free {town} Removals Quote",
                 f"Fill in our quick form, call us or email us and a friendly member of our {esc(town)} removals team will be in touch.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
        faq_html,
    ])
    doc = E.render_page(
        title=f"{town} Removals | Wolves Removals — {county}",
        description=f"Professional, fully insured removals in {town}, {county}. Family-run Wolves Removals: home & commercial moves, packing and secure storage. Free quote.",
        canonical_path=f"/locations/{slug}/",
        body=body, og_image="images/photos/" + pics[0][0] + ".webp",
        breadcrumb=[("Home", "/"), ("Areas We Cover", "/locations/"), (town, f"/locations/{slug}/")],
        extra_schema=[faq_schema], active="locations", show_trust_reviews=False,
        local_area=town)
    return E.write(f"locations/{slug}/index.html", doc)

def _town_pills(towns):
    return "".join(
        f'<a href="/locations/{s}/" class="px-5 py-2 rounded-full border border-border bg-white hover:border-orange hover:text-orange font-semibold">{esc(n)}</a>'
        for s, n, _ in sorted(towns, key=lambda t: t[1]))

_PIN_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" class="county-pin" aria-hidden="true">'
            '<path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>')

def _county_card(name, towns, hslug=None):
    """A polished county card for the locations index: slate header with map-pin,
    county name and town-count badge, then the town links as pills inside."""
    title = f'<a href="/locations/{hslug}/">{esc(name)} Removals</a>' if hslug else f'{esc(name)} Removals'
    pills = "".join(f'<a href="/locations/{s}/">{esc(n)}</a>'
                    for s, n, _ in sorted(towns, key=lambda t: t[1]))
    cnt = len(towns)
    return ('<div class="county-card">'
            f'<div class="county-head">{_PIN_SVG}<h3 class="county-title">{title}</h3>'
            f'<span class="county-count">{cnt} town{"" if cnt == 1 else "s"}</span></div>'
            f'<div class="county-body">{pills}</div></div>')

def hub_prose(name, bg="bg-white", styler=None):
    html = (
        f'<h2 class="relative leading-tight text-black">Your Complete {esc(name)} Removals Partner</h2>'
        f'<p>Whatever your {esc(name)} move involves, we handle it under one roof. Most of our work is residential '
        f'<a href="/services/house-removals/">house removals</a> &mdash; from compact flats to large family homes &mdash; '
        'but we also carry out <a href="/services/commercial-removals/">office and commercial relocations</a>, '
        '<a href="/services/student-removals/">student moves</a> and quick '
        f'<a href="/services/man-and-van/">man and van</a> jobs throughout {esc(name)}. Every move is fully insured and '
        'led by a dedicated coordinator, so you always have one point of contact.</p>'
        '<p>If your timings don&rsquo;t line up, our clean, dry, containerised '
        '<a href="/services/storage/">storage</a> keeps your belongings safe for as long as you need &mdash; whether '
        'that&rsquo;s a few days of <a href="/services/storage/short-term-storage/">short-term storage</a> or months of '
        '<a href="/services/storage/long-term-storage/">long-term storage</a>. We also offer full and fragile-only '
        '<a href="/services/full-packing-service/">packing</a>, plus specialist handling for '
        '<a href="/services/specialised-antiques-moving/">antiques</a>, '
        '<a href="/services/piano-moving/">pianos</a> and other high-value items.</p>'
        f'<p>Moving beyond {esc(name)}? We handle long-distance moves nationwide and '
        '<a href="/services/international-removals/">European and international relocations</a>, with expert '
        '<a href="/services/export-packing-service/">export packing</a> and customs guidance. Wherever you&rsquo;re '
        'headed, you&rsquo;ll get the same careful, transparent service &mdash; backed by our LAPADA and Checkatrade '
        'accreditation. <a href="/get-a-quote/">Request a free quote</a> or call us to talk through your move.</p>')
    if styler:   # split into topic-matched media rows so the prose has images beside it
        return styler(html, bg)
    return section(prose(html, span="lg:col-span-10 lg:col-start-2"), bg=bg, extra="logo-row overflow-hidden")

def build_hub(slug, name, counties):
    towns = [t for t in L.TOWNS if t[2] in counties]
    intro_html = (
        f'<h2 class="relative leading-tight text-black">Removals Across {esc(name)}</h2>'
        f'<p>Wolves Removals provides professional, fully insured home and business removals throughout {esc(name)}. '
        'Family-run and based near <a href="/locations/pulborough-removals/">Pulborough</a>, we have been keeping our '
        'promises since 2016, backed by <strong>LAPADA</strong> and <strong>Checkatrade</strong> accreditation and full '
        f'insurance. From packing and <a href="/services/house-removals/">house removals</a> to '
        f'<a href="/services/commercial-removals/">commercial moves</a> and secure '
        f'<a href="/services/storage/">storage</a>, we handle every {esc(name)} move with care. Choose your town below, '
        'or <a href="/get-a-quote/">request a free quote</a>.</p>'
        f'<p>Our movers know {esc(name)} well &mdash; the roads, the parking, the access quirks of period homes, seafront '
        'flats and rural lanes alike. That local knowledge means each move is planned around real conditions, so your day '
        'runs on time and without surprises.</p>')
    pics = E.page_photos(slug, 5)
    styler = E.make_prose_styler(slug, E.page_photos(slug, 12))
    faqs = town_faqs(name, name)
    faq_html, faq_schema = faq_block(faqs, heading=f"{name} Removals &mdash; Your Questions Answered", bg="bg-lightgrey")
    body = "\n".join([
        hero(f"{name} Removals", name, pics[0]),
        E.quote_bar(lead=f"Moving across {name}?", rest="Get a Free Quote",
                    subtext=f"Trusted removals throughout {name} — get a fast, no-obligation price."),
        styler(intro_html, "bg-white"),
        services_in(name),                                  # lightgrey
        E.trust_reviews_row(),
        why_choose(name, bg="bg-white"),
        hub_prose(name, bg="bg-lightgrey", styler=styler),
        prep_section(name, name, styler),
        section(
            '<div class="grid grid-cols-12 gap-8 lg:gap-12 items-stretch">'
            '<div class="col-span-12 lg:col-span-6 self-center">'
            f'<h2 class="relative leading-tight text-black">Towns We Cover in {esc(name)}</h2>'
            f'<p class="text-lg xl:text-xl font-medium mt-2">Select your town for local {esc(name)} removal details:</p>'
            f'<div class="flex flex-wrap gap-3 mt-6">{_town_pills(towns)}</div></div>'
            f'<div class="col-span-12 lg:col-span-6">{E.map_embed(f"{name}, UK", name, zoom=9)}</div>'
            '</div>', bg="bg-white"),
        process_section(name, bg="bg-lightgrey"),
        local_section(name, counties[0], pics[1]),          # white
        E.storage_cta(seed=slug),
        E.photo_strip(pics[2:5], heading=f"Wolves Removals Across {name}", bg="bg-lightgrey"),
        cta_band(f"Moving in {name}? Get a Free Quote",
                 "Tell us where and when you&rsquo;re moving and we&rsquo;ll send a clear, fixed written quote.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-white"),
        faq_html,
    ])
    doc = E.render_page(
        title=f"{name} Removals | Wolves Removals",
        description=f"Professional, fully insured removals across {name}. Family-run Wolves Removals: home & commercial moves, packing and secure storage. Get a free quote today.",
        canonical_path=f"/locations/{slug}/",
        body=body, og_image="images/photos/" + pics[0][0] + ".webp",
        breadcrumb=[("Home", "/"), ("Areas We Cover", "/locations/"), (name, f"/locations/{slug}/")],
        extra_schema=[faq_schema], active="locations", show_trust_reviews=False,
        local_area=name, local_area_type="AdministrativeArea")
    return E.write(f"locations/{slug}/index.html", doc)

def build_index():
    # Each county is a full-width heading + wrapping town pills, so a long county
    # (West Sussex) flows into a few tidy rows instead of one tall, unbalanced column.
    blocks = []
    for hslug, hname, counties in L.HUBS:
        if hname == "Sussex":
            continue  # Sussex overlaps W/E; skip to avoid duplicate town lists
        towns = [t for t in L.TOWNS if t[2] in counties]
        blocks.append(_county_card(hname, towns, hslug))
    kent = [t for t in L.TOWNS if t[2] == "Kent"]
    if kent:
        blocks.append(_county_card("Kent", kent))
    intro = (
        '<h2 class="relative leading-tight text-black">Areas We Cover</h2>'
        '<p>Wolves Removals provides professional, fully insured removals and storage across Sussex, Surrey, Hampshire '
        'and Kent &mdash; plus nationwide and European moves. Family-run and based near '
        '<a href="/locations/pulborough-removals/">Pulborough</a> since 2016, we know the South East&rsquo;s roads, '
        'access and parking. Choose your county or town below, or <a href="/get-a-quote/">request a free quote</a>.</p>'
        '<p>Wherever you are in the region, you get the same service: a dedicated move coordinator, trained and fully '
        'insured movers, transparent fixed pricing and careful handling of everything from everyday furniture to '
        '<a href="/services/specialised-antiques-moving/">antiques</a> and <a href="/services/piano-moving/">pianos</a>. '
        'We also offer clean, dry <a href="/services/storage/">containerised storage</a> if your dates don&rsquo;t quite '
        'line up, plus full and fragile <a href="/services/full-packing-service/">packing services</a> to take the '
        'pressure off moving day.</p>')
    pics = E.page_photos("locations-index", 5)
    styler = E.make_prose_styler("locations-index", E.page_photos("locations-index", 12))
    faqs = town_faqs("the South East", "the South East")
    faq_html, faq_schema = faq_block(faqs, heading="Areas We Cover &mdash; Your Questions Answered", bg="bg-lightgrey")
    # Ordered for a natural flow: title → CTA → context → the core area list (what visitors
    # came for) → services → why us → proof → storage → process → deeper prose → final CTA → FAQs.
    # Backgrounds alternate white / lightgrey with the dark hero + CTA bands as accents.
    towns = section(
        '<div class="grid grid-cols-12 gap-8 lg:gap-12 items-stretch mb-10">'
        '<div class="col-span-12 lg:col-span-6 self-center">'
        '<h2 class="relative leading-tight text-black">Towns &amp; Counties We Cover</h2>'
        '<p class="text-lg xl:text-xl font-medium mt-2">From Sussex and Surrey to Hampshire and Kent &mdash; choose your '
        'county or town below, and see the wider area we cover across the South East.</p></div>'
        f'<div class="col-span-12 lg:col-span-6">{E.map_embed("Sussex, England, UK", "the South East", zoom=8)}</div>'
        '</div>'
        f'<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2 space-y-6">{"".join(blocks)}</div></div>',
        bg="bg-lightgrey")
    body = "\n".join([
        hero("Areas We Cover", "Sussex", pics[0]),                                   # dark
        E.quote_bar(lead="Get a Free", rest="Removals Quote",
                    subtext="Wherever you're moving in the South East, we'll give you a clear price."),  # dark band
        styler(intro, "bg-white"),                                                   # white
        towns,                                                                       # lightgrey
        services_in("Sussex", bg="bg-white"),                                        # white
        why_choose("the South East", bg="bg-lightgrey"),                             # lightgrey
        E.photo_strip(pics[2:5], heading="Wolves Removals Across the South East", bg="bg-white"),  # white
        E.storage_cta(seed="locations-index"),                                       # dark band
        process_section("Sussex", bg="bg-white"),                                    # white
        hub_prose("South East", bg="bg-lightgrey", styler=styler),                                  # lightgrey
        cta_band("Don&rsquo;t See Your Town? We Still Cover You",
                 "We move throughout the South East and beyond. Tell us where you&rsquo;re moving and we&rsquo;ll send a free quote.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-white"),               # white
        faq_html,                                                                    # lightgrey
    ])
    doc = E.render_page(
        title="Areas We Cover | Wolves Removals — Sussex & Surrey",
        description="Wolves Removals covers Sussex, Surrey, Hampshire and Kent plus nationwide and European moves. Find professional, fully insured removals in your town.",
        canonical_path="/locations/", body=body, og_image="images/photos/" + pics[0][0] + ".webp",
        breadcrumb=[("Home", "/"), ("Areas We Cover", "/locations/")],
        extra_schema=[faq_schema], active="locations")
    return E.write("locations/index.html", doc)

def build():
    n = 0
    build_index(); n += 1
    for slug, name, counties in L.HUBS:
        build_hub(slug, name, counties); n += 1
    for slug, town, county in L.TOWNS:
        build_town(slug, town, county); n += 1
    print(f"built {n} location pages (index + {len(L.HUBS)} hubs + {len(L.TOWNS)} towns)")

if __name__ == "__main__":
    build()
