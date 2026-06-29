# -*- coding: utf-8 -*-
"""Build the core pages: about, pricing, FAQ, contact, get-a-quote, reviews,
leave-a-review, gallery, job-vacancies, privacy, terms, 404.
Content preserved from the live site + expanded per the SEO bible. Real facts only
(liability up to £10m, CRB-checked staff, since 2016). No fabricated reviews.
Forms POST to a Cloudflare Worker endpoint (TODO: deploy + Resend key)."""
import os, sys, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, card_grid, cta_band, faq_block

HERO = "images/photos/professional-wolves-removals-team-sussex.webp"
FORM_ENDPOINT = "/api/contact"   # Cloudflare Pages Function -> Resend (functions/api/contact.js); needs RESEND_API_KEY, CONTACT_FROM, CONTACT_TO

def page_hero(h1, lead_html, img_src=None, bullets=None):
    inc = ""
    if bullets:
        inc = '<ul class="space-y-2 list-none p-0">' + "".join(
            f'<li class="flex items-start gap-2"><span class="text-green mt-1 shrink-0">{icon("check-bold","w-5 h-5")}</span><span>{b}</span></li>'
            for b in bullets) + "</ul>"
    # distinct, on-topic hero per page (seeded by its H1) when not given an explicit image
    photo = E.page_photos(h1, 1)[0]
    src = img_src or ("images/photos/" + photo[0] + ".webp")
    hero_img = img(src, photo[1] if not img_src else "Wolves Removals Sussex", cls="w-full h-full object-cover", eager=True)
    return (
        '<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
        f'<div class="absolute inset-0">{hero_img}</div>'
        '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
        f'<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{h1}</h1>'
        f'<div class="mt-4 text-lg xl:text-xl max-w-3xl">{lead_html}</div>{E.hero_review_row(inc)}'
        '</div></div></div></section>')

# ---------------------------------------------------------------- forms
def _field(label, name, typ="text", required=False, placeholder="", half=False):
    req = ' required aria-required="true"' if required else ""
    star = ' <span class="text-darkgrey">*</span>' if required else ""
    col = "md:col-span-6" if half else "md:col-span-12"
    return (f'<div class="col-span-12 {col}"><label class="block font-semibold mb-1" for="f-{name}">{esc(label)}{star}</label>'
            f'<input class="w-full" type="{typ}" id="f-{name}" name="{name}" placeholder="{esc(placeholder)}"{req}></div>')

def _quote_form_card(heading="Request Your Free Quote"):
    chips = "".join(
        f'<label class="enq-chip"><input type="checkbox" name="enquiry" value="{esc(v)}"><span>{esc(v)}</span></label>'
        for v in ["Home removal", "Commercial", "Packing", "Storage", "International / EU", "Man &amp; van", "Other"])
    return (
        '<div class="bg-white rounded-2xl shadow-custom px-8 py-12 text-black">'
        f'<h2 class="leading-tight text-black">{esc(heading)}</h2>'
        '<p class="text-darkgrey text-sm mt-1 mb-0">Tell us about your move and we&rsquo;ll send a clear, fixed price &mdash; no obligation. Fields marked <span class="font-semibold">*</span> are required.</p>'
        f'<form class="enquiry-form mt-5" method="post" action="{FORM_ENDPOINT}" novalidate>'
        '<div class="grid grid-cols-12 gap-4">'
        + _field("First name", "first_name", required=True, half=True)
        + _field("Last name", "last_name", required=True, half=True)
        + _field("Email", "email", typ="email", required=True, half=True)
        + _field("Phone", "phone", typ="tel", half=True)
        + _field("Moving from (town & postcode)", "from", half=True)
        + _field("Moving to (town & postcode)", "to", half=True)
        + _field("Preferred move date", "date", typ="date", half=True)
        + _field("Property size (e.g. 3-bed house)", "size", half=True)
        + '<div class="col-span-12"><span class="block font-semibold mb-2">What can we help with?</span>'
          f'<div class="flex flex-wrap gap-2">{chips}</div></div>'
        + '<div class="col-span-12"><label class="block font-semibold mb-1" for="q-message">Tell us about your move</label>'
          '<textarea class="w-full" id="q-message" name="message" rows="4" placeholder="Access, parking, special items, anything we should know..."></textarea></div>'
        + '<div class="col-span-12 hidden" aria-hidden="true"><label>Leave blank<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>'
        + '<div class="col-span-12"><label class="flex items-start gap-2 text-sm text-darkgrey"><input type="checkbox" name="consent" required aria-required="true"> '
          '<span>I agree to Wolves Removals contacting me about my enquiry and accept the <a href="/privacy-policy/">privacy policy</a>. <span class="font-semibold">*</span></span></label></div>'
        + '<div class="col-span-12"><button type="submit" class="button-orange w-full justify-center">Send My Enquiry</button>'
          f'<p class="mt-3 text-sm text-darkgrey text-center mb-0">Prefer to talk? Call <a class="font-semibold" href="{E.S.BUSINESS["phone_link"]}">{E.S.BUSINESS["phone"]}</a> or email <a class="font-semibold" href="mailto:{E.S.BUSINESS["email"]}">{E.S.BUSINESS["email"]}</a>.</p></div>'
        '</div></form></div>')

def quote_form(heading="Request Your Free Quote"):
    return section(
        '<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2">'
        + _quote_form_card(heading) + '</div></div>', bg="bg-lightgrey")

def _contact_form_card():
    chips = "".join(
        f'<label class="enq-chip"><input type="checkbox" name="enquiry" value="{esc(v)}"><span>{esc(v)}</span></label>'
        for v in ["Home removal", "Commercial", "Packing", "Storage", "International / EU", "Man &amp; van", "Other"])
    return (
        '<div class="bg-white rounded-2xl shadow-custom px-8 py-12 text-black">'
        '<h2 class="leading-tight text-black">Send Us a Message</h2>'
        '<p class="text-darkgrey text-sm mt-1 mb-0">We usually reply within a few hours. Fields marked <span class="font-semibold">*</span> are required.</p>'
        f'<form class="enquiry-form mt-5" method="post" action="{FORM_ENDPOINT}" novalidate>'
        '<div class="grid grid-cols-12 gap-4">'
        + _field("First name", "first_name", required=True, half=True)
        + _field("Last name", "last_name", required=True, half=True)
        + _field("Email", "email", typ="email", required=True, half=True)
        + _field("Phone", "phone", typ="tel", half=True)
        + '<div class="col-span-12"><span class="block font-semibold mb-2">What can we help with?</span>'
          f'<div class="flex flex-wrap gap-2">{chips}</div></div>'
        + '<div class="col-span-12"><label class="block font-semibold mb-1" for="c-message">Your message</label>'
          '<textarea class="w-full" id="c-message" name="message" rows="4" placeholder="Tell us about your move &mdash; dates, where from &amp; to, anything we should know..."></textarea></div>'
        + '<div class="col-span-12 hidden" aria-hidden="true"><label>Leave blank<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>'
        + '<div class="col-span-12"><label class="flex items-start gap-2 text-sm text-darkgrey"><input type="checkbox" name="consent" required aria-required="true"> '
          '<span>I agree to Wolves Removals contacting me about my enquiry and accept the <a href="/privacy-policy/">privacy policy</a>. <span class="font-semibold">*</span></span></label></div>'
        + '<div class="col-span-12"><button type="submit" class="button-orange w-full justify-center">Send My Message</button>'
          f'<p class="mt-3 text-sm text-darkgrey text-center mb-0">Prefer to talk? Call <a class="font-semibold" href="{E.S.BUSINESS["phone_link"]}">{E.S.BUSINESS["phone"]}</a> or email <a class="font-semibold" href="mailto:{E.S.BUSINESS["email"]}">{E.S.BUSINESS["email"]}</a>.</p></div>'
        '</div></form></div>')

TRUST_RATING = "5.0"
TRUST_REVIEWS = "610"

def custom_cert_card(open_about=False):
    """Inline replica of the Trustindex certificate (renders on any domain).
    open_about=True expands the 'About Trustindex certificate' item by default."""
    ic = {
        "reviews": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="8" r="3"/><path d="M4 20a6 6 0 0 1 11-3.4"/><path d="M18 13l1 2 2.2.3-1.6 1.6.4 2.2-2-1-2 1 .4-2.2L15.8 15l2.2-.3z" fill="currentColor" stroke="none"/></svg>',
        "issue": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M19.5 7.7a4 4 0 0 0-7-2.6 4 4 0 0 0-7 2.6C5.5 12.2 12 16 12 16s6.5-3.8 6.5-8.3z"/><path d="M8.6 10.6l2 2 3.4-3.4"/></svg>',
        "verified": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.4-3 7.4-7 8.9-4-1.5-7-4.5-7-8.9V6z"/><path d="M9 12l2.2 2.2L15.5 10"/></svg>',
        "data": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>',
        "about": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 11.2v4.8"/><circle cx="12" cy="7.8" r="0.5" fill="currentColor" stroke="none"/></svg>',
    }
    chev = icon("chevron", "w-4 h-4 fill-current")
    b = E.S.BUSINESS
    def item(key, label, body, certified=True, open=False):
        cert = '<span class="tcc-cert">Certified</span>' if certified else ''
        return (
            f'<div class="tcc-item" x-data="{{open:{str(open).lower()}}}">'
            '<button type="button" class="tcc-row" @click="open=!open" :aria-expanded="open">'
            f'<span class="tcc-ic">{ic[key]}</span><span class="tcc-t">{label}</span>{cert}'
            f'<span class="tcc-chev" :class="open && \'rot\'">{chev}</span></button>'
            f'<div class="tcc-body" x-show="open" x-cloak x-transition.duration.200ms>{body}</div>'
            '</div>')
    body_reviews = ('<p>Customer reviews showcase the level and quality of service a website provides.</p>'
        '<p>Trustindex collaborates with 137 review platforms to provide website visitors easy access to all real and verified reviews in one place.</p>'
        '<p>Reviews from other platforms are displayed and added to the ratings only if they are proven spam-free and meet Trustindex&rsquo;s guidelines.</p>')
    body_issue = ('<p>Trustindex continuously measures the satisfaction of your customers based on evaluations. '
        'Less than 1% of the customers surveyed indicated a problem.</p>')
    def kv(k, v, ver=False):
        vt = ' <span class="tcc-ver">Verified</span>' if ver else ''
        return f'<div class="tcc-kv"><div class="k">{k}</div><div class="v">{v}{vt}</div></div>'
    body_verified = ('<p>The website&rsquo;s contact information and business information has been independently verified by Trustindex.</p>'
        '<p class="tcc-h">Contact details</p>'
        + kv("Phone:", b["phone"], True)
        + kv("E-mail:", b["email"], True)
        + '<p class="tcc-h">Business data</p>'
        + kv("Company name:", esc(b["name"]))
        + kv("Domain:", "wolves-removals.co.uk")
        + kv("Company founded:", "2017")
        + kv("Number of employees:", "1-10")
        + kv("Start of Trustindex verification:", "2026-06-07"))
    checks = [("Google", "Safe Browsing: no problems detected"), ("Blacklist", "Not a Blacklisted Site"),
              ("SSL", "Valid SSL certificate"), ("Spam", "E-mail is spam-free")]
    checks_html = "".join(f'<li><span class="lbl">{esc(l)}</span><span class="txt">{esc(t)}</span><span class="ok">&#10003;</span></li>' for l, t in checks)
    body_data = ('<p>The website is constantly checked for security issues by Trustindex.</p>'
        f'<ul class="tcc-checks">{checks_html}</ul>')
    more = ('<a href="https://www.trustindex.io/features-list/review-certificate/for-visitors/" '
            'target="_blank" rel="nofollow noopener" aria-label="More details about Trustindex certificates for visitors">More details &raquo;</a>')
    body_about = ('<p>Websites that continuously maintain a high level of customer satisfaction and comply with a high level of '
        'security protocol can obtain a Trustindex certificate. When shopping, look for Trustindex certificates and buy with confidence.</p>'
        f'<p>{more}</p>')
    return (
        '<div class="tcc">'
        '<div class="tcc-head"><span>wolves-removals.co.uk</span><a class="tcc-rev" href="/reviews/" aria-label="Read our latest customer reviews">Latest reviews &rsaquo;</a></div>'
        '<div class="tcc-sub">This site has obtained the following certificates:</div>'
        '<div class="tcc-rating"><div><div class="tcc-lab">Excellent rating</div>'
        f'<div class="tcc-stars">&#9733;&#9733;&#9733;&#9733;&#9733;<span class="num">{TRUST_RATING}</span></div>'
        f'<div class="tcc-reviews">{TRUST_REVIEWS} customer reviews</div></div>'
        '<div class="tcc-badge"><div class="top"><span class="chk">&#10003;</span> Excellent Service</div>'
        '<div class="bot">Verified by <strong>Trustindex</strong></div></div></div>'
        '<div class="tcc-list">'
        + item("reviews", "Reviews credibility", body_reviews)
        + item("issue", "100% issue-free services", body_issue)
        + item("verified", "Verified business", body_verified)
        + item("data", "Data protection", body_data)
        + item("about", "About Trustindex certificate", body_about, certified=False, open=open_about)
        + '</div>'
        '<div class="tcc-foot">&copy; 2026 trustindex.io</div>'
        '</div>')

def _trust_cards(open_about=False):
    """Certificate card + inline Trustindex reviews widget, stacked (natural flow so an
    expanded certificate item pushes the reviews card down rather than overlapping it)."""
    return (f'{custom_cert_card(open_about=open_about)}'
            '<div class="ti-reviews-widget mt-5">'
            "<script defer async src='https://cdn.trustindex.io/loader.js?7617bac361e11404f15684e7385'></script>"
            '</div>')

def trust_hero(heading, intro_html, form_card, reverse=False, equal=False, open_about=False,
               img_src="images/photos/wolves-removals-team-fleet-vans.webp",
               img_alt="The Wolves Removals team with their fleet of vans in Sussex"):
    """Dark hero pairing a form card with the trust cards (certificate + reviews).
    Form is always first in the DOM (mobile shows it first). reverse=True puts the trust
    cards on the LEFT on desktop (form right) via flex order; equal makes the columns 6/6.
    open_about=True expands the certificate's About item by default."""
    hero_img = img(img_src, img_alt, cls="w-full h-full object-cover", eager=True)
    fspan, cspan = ("lg:col-span-6", "lg:col-span-6") if equal else ("lg:col-span-7", "lg:col-span-5")
    align = "items-start"
    cards = _trust_cards(open_about=open_about)
    if reverse:
        form_col = f'<div class="col-span-12 {fspan} lg:order-2">{form_card}</div>'
        cards_col = f'<div class="col-span-12 {cspan} lg:order-1">{cards}</div>'
    else:
        form_col = f'<div class="col-span-12 {fspan}">{form_card}</div>'
        cards_col = f'<div class="col-span-12 {cspan}">{cards}</div>'
    return (
        '<section class="relative w-full bg-darkgrey text-white overflow-hidden">'
        f'<div class="absolute inset-0">{hero_img}</div>'
        '<div class="absolute inset-0 contact-hero-overlay"></div>'
        '<div class="container relative z-10 py-12 lg:py-16">'
        '<div class="text-center max-w-2xl mx-auto mb-8 lg:mb-10">'
        f'<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{heading}</h1>'
        f'<p class="mt-4 text-lg xl:text-xl">{intro_html}</p></div>'
        f'<div class="grid grid-cols-12 gap-6 lg:gap-8 {align}">'
        f'{form_col}{cards_col}'
        '</div>'
        '</div></section>')

def contact_hero():
    return trust_hero("Contact Wolves Removals",
        "Call, email or send us a message &mdash; a friendly, family-run Sussex team, ready to help plan your move.",
        _contact_form_card(), reverse=False)

def video_survey_block(bg="bg-white"):
    items = ["Extremely convenient &mdash; no need to be home for a surveyor",
             "Works on smartphones and tablets (FaceTime on iPhone/iPad, WhatsApp on Android)",
             "Our surveyor guides you step by step",
             "Just point your device at the items you want to move",
             "Get your quote within 24 hours of the video survey"]
    lis = "".join(f'<li>{i}</li>' for i in items)
    html = ('<h2 class="relative leading-tight text-black">Schedule a Video Survey</h2>'
            '<p>Short on time? Book a quick video survey instead of an in-home visit. It&rsquo;s a simple way to get an '
            'accurate, no-obligation quote from the comfort of your home.</p>'
            f'<ul class="tick-list">{lis}</ul>')
    return E.media_rows(html, "pricing-video-survey", bg, used=set())

# ---------------------------------------------------------------- pages
def _why_choose(bg):
    rows = [
        ("Family-run since 2016", "A modern, family-run team built on traditional values &mdash; reliability and keeping our promises."),
        ("Fully insured &amp; accredited", "Liability cover up to £10 million, LAPADA member and Checkatrade-verified."),
        ("Trained, uniformed team", "Experienced, CRB/DBS-checked movers who treat your belongings with real care."),
        ("Transparent fixed pricing", "Clear written quotes with no hidden fees, plus video or in-home surveys."),
    ]
    cells = "".join(
        f'<div class="col-span-12 md:col-span-6"><div class="group flex gap-3 h-full bg-white rounded-xl border border-border shadow-custom p-6 transition-colors duration-200 hover:bg-darkgrey hover:border-darkgrey">'
        f'<span class="text-green shrink-0">{icon("check-bold","w-6 h-6")}</span>'
        f'<div><h3 class="text-lg font-semibold text-black group-hover:text-white">{t}</h3><p class="mt-1 text-darkgrey group-hover:text-beige mb-0">{d}</p></div></div></div>'
        for t, d in rows)
    return section('<div class="text-center mb-8"><h2 class="relative leading-tight text-black">Why Choose Wolves Removals?</h2></div>'
                   f'<div class="grid grid-cols-12 gap-6">{cells}</div>', bg=bg)

def _process(bg):
    # Unified chevron step-process design (shared with the home page).
    return E.step_process(bg=bg)

def about_us():
    E.freeze_extras(True)   # leave the About page alone — exclude the merged 'extra variety' photos
    # Shared used-images set so no photo repeats across the page (audit §6).
    U = set()
    hero_photo  = ("wolves-removals-team-fleet-vans", "The Wolves Removals team with their fleet of removal vans")
    growth_photo = ("wolves-vans-sussex-country-house", "Wolves Removals vans at a grand Sussex country house")
    ahead_photo  = ("removal-van-outside-storage-warehouse", "A Wolves Removals van outside the secure storage warehouse")
    jack_photo  = ("jack-wolfe-founder-wolves-removals", "Jack Wolfe, founder and director of Wolves Removals")
    # Jack's photo replaces this one in the founder story — keep it off the page entirely.
    U |= {hero_photo[0], growth_photo[0], ahead_photo[0], jack_photo[0],
          "movers-transporting-household-items-sussex", "foam-lined-fine-art-crate",
          "wolves-handling-sussex-house-relocation"}

    # ---- Founder's story (alternating topic-matched media rows) ----
    founder_html = (
        '<h2 class="relative leading-tight text-black">Meet Jack Wolfe, Our Founder</h2>'
        '<p>At Wolves Removals, moving isn&rsquo;t just our business &mdash; it&rsquo;s something we&rsquo;ve spent a '
        'lifetime perfecting. I&rsquo;m Jack Wolfe, Director of Wolves Removals, and my journey into the removals industry '
        'began long before the company was founded.</p>'
        '<p>For many years I worked as an antique dealer, supplying some of London&rsquo;s most respected high-street '
        'antique shops, particularly in Chelsea and across the capital. My work took me all over Europe &mdash; spending '
        'much of my time in France, Germany, Holland, Belgium and Spain &mdash; sourcing antiques and fine furnishings '
        'from major fairs, markets and exhibitions before transporting them back to England for sale to the trade.</p>'
        '<p>Handling valuable, fragile and often irreplaceable pieces taught me the importance of care, planning and '
        'attention to detail. Every item had a story, and every journey required real expertise to make sure it arrived '
        'safely.</p>'
        '<p>As my reputation grew, fellow antique dealers began asking if I could help transport their purchases back to '
        'the UK. What started as helping colleagues soon developed into a specialist transport service for '
        '<a href="/services/specialised-antiques-moving/">antiques and fine art</a>. From there we expanded into '
        'collecting items from auction houses across the UK and Europe, providing secure transport for buyers and dealers '
        'alike.</p>'
        '<h3>From Antiques to a Full-Service Company</h3>'
        '<p>Recognising the growing demand for a reliable, professional service, I founded Wolves Removals in 2016. What '
        'began as specialist transport for antiques and fine art naturally evolved into a full-service removals, '
        '<a href="/services/storage/">storage</a> and transport company. Over the years we have expanded to include '
        '<a href="/services/house-removals/">domestic removals</a>, '
        '<a href="/services/commercial-removals/">commercial relocations</a>, secure storage solutions and specialist '
        'handling services.</p>'
        '<p>Today, Wolves Removals is proudly based in West Sussex, serving customers across the South East, London and '
        'throughout the UK. Thanks to our extensive experience working across the continent, we also provide '
        '<a href="/services/european-removals/">European</a> and '
        '<a href="/services/international-removals/">international</a> removals, storage and transport &mdash; helping '
        'clients move safely and efficiently between the UK and Europe.</p>'
        '<p>Despite our growth, the principles on which the business was built have never changed. The same care, '
        'precision and attention to detail that were essential when transporting valuable antiques now form the '
        'foundation of every removal, storage and transport job we undertake &mdash; from a single heirloom to an entire '
        'household or business relocation.</p>'
        '<p>Whether we&rsquo;re moving a family home, relocating a business, transporting fine art or placing treasured '
        'belongings into secure storage, we approach every job with the same respect and professionalism. Moving and '
        'storing isn&rsquo;t simply about transporting possessions from one place to another &mdash; it&rsquo;s about '
        'handling the things that matter most to you.</p>'
        '<p>That&rsquo;s why we take the time to plan carefully, communicate clearly and deliver a service that gives our '
        'customers complete peace of mind. From a single antique to an entire household or business relocation, our '
        'commitment remains the same: professional service, meticulous care and a personal touch that comes from decades '
        'of hands-on experience.</p>'
        '<div class="wr-signature"><span class="wr-sig-name">&mdash; Jack Wolfe</span>'
        '<span class="wr-sig-role">Founder &amp; Director, Wolves Removals</span></div>')
    # First row (the "Meet Jack Wolfe" intro) shows Jack's own photo.
    # Row 1 (the "Handling valuable…" paragraph) shows the office-dog photo instead of a crate.
    office_dog = ("wolves-removals-office-puppy",
                  "The Wolves Removals office dog beside the team&rsquo;s LAPADA and Checkatrade certificates",
                  "50% 60%")
    antiques_gallery = ("classical-statues-fine-art-collection",
                        "Classical statues, busts and antiques in a grand fine-art collection")
    dog_van = ("wolves-removals-dog-removal-van",
               "The Wolves Removals dog looking out of a branded removal van window")
    founder = E.media_rows(founder_html, "about-founder", bg="bg-white", used=U, vary=False,
                           force=jack_photo, force_pos="top", pins={1: office_dog, 2: antiques_gallery, 3: dog_van})

    # ---- Key numbers band ----
    stats = [("2016", "Founded in West Sussex"), ("HGV", "Licensed operator"),
             ("UK &amp; EU", "Removals, storage &amp; transport"), ("£10m", "Liability cover")]
    stats_band = section(
        '<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2">'
        '<div class="wr-stats">' + "".join(
            f'<div class="wr-stat"><div class="wr-stat-num">{n}</div><div class="wr-stat-label">{l}</div></div>'
            for n, l in stats) + '</div></div></div>', bg="bg-beige")

    # ---- Our Growth ----
    growth_inner = (
        '<h2 class="relative leading-tight text-black">Our Growth</h2>'
        '<p>What started as a one-van operation in 2016 has grown into a fully equipped removals, '
        '<a href="/services/storage/">storage</a> and transport company, with a modern fleet and facilities built to '
        'handle projects of every size.</p>'
        '<p>Our fleet now includes multiple removal vans, specialist transport vehicles, trailers and an HGV lorry. '
        'Combined with our secure warehouse storage, we take on everything from local house moves to large-scale '
        '<a href="/services/commercial-removals/">commercial relocations</a>, long-term storage and complex European '
        'transport. As a licensed HGV operator, we work to the highest industry standards &mdash; giving you complete '
        'confidence in both the transport and secure storage of your belongings.</p>')
    growth = E.text_with_image(growth_inner, growth_photo, reverse=False, bg="bg-white")

    # ---- Our Journey (timeline) ----
    journey = [
        ("2016", ["Wolves Removals founded by Jack Wolfe",
                  "Started with a single van and a small warehouse unit",
                  "Specialised in antiques, fine art and auction-house purchases",
                  "Built a reputation on reliability, care and word-of-mouth"]),
        ("2017", ["Expanded transport services throughout the UK",
                  "Grew work with antique dealers, interior designers and private collectors",
                  "Began larger domestic removals alongside specialist transport"]),
        ("2018", ["Added further vehicles to support growing demand",
                  "Expanded into secure storage services",
                  "Established regular transport routes across the UK and Europe"]),
        ("2019&ndash;2024", ["Steady year-on-year growth across domestic, commercial and storage work",
                  "Broadened our secure storage capacity and service range",
                  "Deepened our UK and European transport network"]),
        ("2025", ["Moved into a larger warehouse facility to support continued growth",
                  "Significantly expanded storage capacity and operational capabilities",
                  "Completed a growing number of domestic, commercial and European relocations"]),
        ("2026", ["Acquired our first HGV lorry and specialist transport trailer",
                  "Obtained our HGV Operator&rsquo;s Licence",
                  "Expanded capabilities for large-scale removals, secure storage and logistics",
                  "Strengthened our UK and European transport and storage solutions"]),
    ]
    tl_items = "".join(
        f'<div class="wr-tl-item"><div class="wr-tl-card"><span class="wr-tl-year">{yr}</span><ul>'
        + "".join(f'<li>{m}</li>' for m in ms) + '</ul></div></div>'
        for yr, ms in journey)
    journey_section = section(
        '<div class="text-center mb-8 lg:mb-10"><h2 class="relative leading-tight text-black">Our Journey</h2>'
        '<p class="text-lg xl:text-xl max-w-2xl mx-auto mt-2">From a single van in 2016 to a licensed HGV operation '
        'serving the UK and Europe today.</p></div>'
        '<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-8 lg:col-start-3">'
        f'<div class="wr-timeline">{tl_items}</div></div></div>', bg="bg-lightgrey")

    # ---- Looking Ahead (slate feature panel) ----
    ahead_body = (
        '<p>We remain committed to investing in our fleet, our storage facilities and our team. We&rsquo;ll keep '
        'expanding our secure <a href="/services/storage/">storage</a> and transport capabilities while holding on to the '
        'personal service, professionalism and attention to detail that have defined Wolves Removals since day one.</p>'
        '<p>From a single van and a small warehouse in 2016 to a growing fleet, larger secure storage and a full HGV '
        'operation today, Wolves Removals continues to grow while staying true to the values the company was built on. '
        'Read our <a href="/reviews/">customer reviews</a>, or see our transparent <a href="/pricing/">removal pricing</a>.</p>')
    looking_ahead = E.feature_panel('<h2 class="relative leading-tight text-black">Looking Ahead</h2>',
                                    ahead_body, ahead_photo, reverse=True, bg="bg-beige")

    about_faqs = [
        ("How long has Wolves Removals been trading?", "<p>We&rsquo;ve been helping people move across Sussex and the UK since 2016, growing from specialist antiques removals into a full-service, family-run removals and storage company.</p>"),
        ("Is Wolves Removals insured?", "<p>Yes &mdash; we are fully insured with liability cover up to £10 million, and optional full damage insurance is available for your goods.</p>"),
        ("Do you specialise in antiques?", "<p>We do. As a <a href=\"/services/specialised-antiques-moving/\">LAPADA member</a> we handle antiques, fine art and valuables with bespoke crating and white-glove care.</p>"),
        ("Which areas do you cover?", "<p>The whole of Sussex, much of Surrey, the Petersfield area of Hampshire, plus Kent, nationwide and EU moves. See our <a href=\"/locations/\">areas we cover</a>.</p>"),
        ("Are you accredited?", "<p>Yes &mdash; we&rsquo;re a LAPADA member and Checkatrade-verified, and we&rsquo;re recommended by leading estate agents including Fine &amp; Country, Justin Lloyd and Mansell McTaggart.</p>"),
    ]
    about_faq_html, about_faq_schema = faq_block(about_faqs, heading="About Wolves Removals — FAQs", bg="bg-white")
    body = "\n".join([
        page_hero("About Wolves Removals",
                  "<p>A family-run Sussex removals, storage and transport company &mdash; built on decades of hands-on "
                  "experience moving antiques, fine art and the things that matter most.</p>",
                  img_src="images/photos/" + hero_photo[0] + ".webp",
                  bullets=["Founded in 2016 &mdash; rooted in antiques &amp; fine art",
                           "Family-run &amp; fully insured (liability up to £10m)",
                           "Licensed HGV operator with secure warehouse storage",
                           "Trusted across Sussex, the UK &amp; Europe"]),
        E.quote_bar(lead="Thinking of Moving?", rest="Get a Free Quote",
                    subtext="Experience the Wolves Removals difference — request your free quote."),
        founder,
        stats_band,
        E.trust_reviews_row(),
        growth,
        journey_section,
        looking_ahead,
        _why_choose("bg-white"),
        _trust_logos("bg-lightgrey"),
        about_faq_html,
        cta_band("Ready to Plan Your Move?", "Get a free, no-obligation quote from our friendly Sussex team.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
    ])
    E.freeze_extras(False)   # restore full pool for all other pages
    return E.render_page(title="About Wolves Removals | Family-Run Sussex Removals",
        description="Wolves Removals is a family-run Sussex removals company, specialists in home, commercial and antiques moves since 2016. LAPADA & Checkatrade accredited, fully insured.",
        canonical_path="/about-us/", body=body, og_image="images/photos/" + hero_photo[0] + ".webp", extra_schema=[about_faq_schema],
        breadcrumb=[("Home", "/"), ("About Us", "/about-us/")], active="about", show_trust_reviews=False), "about-us/index.html"

def _trust_logos(bg):
    # Shared "We're Trusted By" strip — identical to the home page (single source of truth).
    return E.trusted_by(bg)

def pricing():
    html = (
        '<h2 class="relative leading-tight text-black">Transparent, Competitive Removal Pricing</h2>'
        '<p>The cost of a house move varies depending on the size of your home, the distance to your new location and '
        'the services you need &mdash; packing, storage, dismantling or specialist handling. We keep our pricing '
        'competitive and transparent, with <strong>no hidden fees</strong>, and we&rsquo;re based in the heart of Sussex '
        'so we know the local area inside out.</p>'
        '<p>Because every move is different, the most accurate way to understand your cost is a free, no-obligation '
        'quote tailored to you. We serve customers moving within <a href="/locations/west-sussex-removals/">Sussex</a>, '
        '<a href="/locations/surrey-removals/">Surrey</a>, <a href="/locations/hampshire-removals/">Hampshire</a> and '
        'Kent, as well as nationwide and European destinations.</p>'
        '<p class="text-sm text-darkgrey">Prices last reviewed: 2026 &middot; all moves are fully insured.</p>'
        '<h2 class="relative leading-tight text-black">What Affects the Price of a Move?</h2>'
        '<p>Understanding what drives cost helps you plan. The main factors are:</p>'
        '<ul class="tick-list">'
        '<li><strong>Property size &amp; volume</strong> &mdash; more belongings means more time, crew and vehicle space.</li>'
        '<li><strong>Distance</strong> &mdash; local moves cost less than long-distance, European or international ones.</li>'
        '<li><strong>Access &amp; parking</strong> &mdash; stairs, lifts, narrow lanes and parking restrictions add time.</li>'
        '<li><strong>Packing</strong> &mdash; <a href="/services/full-packing-service/">full</a> or '
        '<a href="/services/fragile-packing/">fragile-only</a> packing, or buy '
        '<a href="/services/packing-materials/">materials</a> and pack yourself.</li>'
        '<li><strong>Storage</strong> &mdash; <a href="/services/storage/short-term-storage/">short</a> or '
        '<a href="/services/storage/long-term-storage/">long-term</a> if your dates don&rsquo;t align.</li>'
        '<li><strong>Special items</strong> &mdash; <a href="/services/piano-moving/">pianos</a>, '
        '<a href="/services/specialised-antiques-moving/">antiques</a> and fragile valuables need extra care.</li>'
        '</ul>'
        '<p>For complete peace of mind we are fully insured with liability cover up to £10 million, and we offer '
        'optional full damage insurance for your goods for an extra 10% of your invoice total.</p>'
        '<h2 class="relative leading-tight text-black">What&rsquo;s Included in Your Quote</h2>'
        '<p>Our quotes are clear and itemised, so you know exactly what you&rsquo;re paying for. Depending on your move, '
        'that typically includes a trained, uniformed crew, a suitable vehicle, protective materials (blankets, straps '
        'and floor protection), loading, transport, unloading and placement in the right rooms. Optional extras such as '
        '<a href="/services/full-packing-service/">packing</a>, furniture dismantling and reassembly, '
        '<a href="/services/storage/">storage</a> and specialist handling are quoted separately so you can pick exactly '
        'what you need &mdash; with no pressure and no hidden fees.</p>'
        '<h2 class="relative leading-tight text-black">Ways to Keep Your Move Affordable</h2>'
        '<p>There are simple ways to manage the cost of a move. Doing some of your own '
        '<a href="/services/packing-materials/">packing</a> with our materials can reduce labour time; being flexible '
        'on dates and avoiding peak periods (Fridays and month-ends) can help; and decluttering before you move means '
        'less to transport. Booking early secures your preferred date and gives us time to plan the most efficient move. '
        'Whatever your budget, we&rsquo;ll talk through the options honestly and recommend what genuinely suits you.</p>'
        '<h2 class="relative leading-tight text-black">What Goes Into a Typical Move</h2>'
        '<p>To give a sense of how pricing works, consider a typical local three-bedroom house move within Sussex. '
        'We&rsquo;d usually assign a crew of two to four trained movers and an appropriately sized vehicle, allow time '
        'for careful loading and protection of furniture, transport to your new home, and unloading with placement in '
        'the right rooms. If you add <a href="/services/full-packing-service/">full packing</a> the day before, that '
        'extends the time and materials; a longer-distance move adds travel and fuel.</p>'
        '<p>A smaller move &mdash; a one-bedroom flat, a student move or a few items &mdash; is often best suited to our '
        'cost-effective <a href="/services/man-and-van/">man and van</a> service, which starts from £80. Larger family '
        'homes, listed buildings or difficult access naturally take longer. Because these variables differ for every '
        'household, we always recommend a free survey (video or in person) so your quote reflects your actual move &mdash; '
        'not a one-size-fits-all estimate.</p>'
        '<h2 class="relative leading-tight text-black">Storage &amp; Packing Options</h2>'
        '<p>If your completion dates don&rsquo;t align, our containerised <a href="/services/storage/short-term-storage/">'
        'short-term</a> and <a href="/services/storage/long-term-storage/">long-term storage</a> keeps your belongings '
        'safe at a sensible cost. And if you&rsquo;d rather not pack at all, our '
        '<a href="/services/full-packing-service/">full packing service</a> handles everything room by room. '
        '<a href="/get-a-quote/">Request your free quote</a> and we&rsquo;ll give you a clear, fixed price with no '
        'surprises.</p>')
    pricing_faqs = [
        ("How much does a house move cost?", "<p>It depends on your property size, distance, access and the services you choose. A local move starts lower than a long-distance or international one. <a href=\"/get-a-quote/\">Request a free quote</a> for an accurate, fixed price.</p>"),
        ("Are there any hidden fees?", "<p>No &mdash; our quotes are clear and itemised with no hidden fees. Optional extras like packing and storage are quoted separately so you only pay for what you need.</p>"),
        ("How do I get a quote?", "<p>Book a free video or in-home survey and we&rsquo;ll send a fixed written quote. Use our <a href=\"/get-a-quote/\">online form</a> or call us to arrange it.</p>"),
        ("Do you require a deposit?", "<p>Bookings are confirmed on receipt of any agreed deposit for the minimum charge. We&rsquo;ll explain everything clearly with your quote.</p>"),
        ("How can I keep the cost down?", "<p>Doing some of your own <a href=\"/services/packing-materials/\">packing</a>, being flexible on dates, decluttering and booking early all help. We&rsquo;ll advise honestly on what suits your budget.</p>"),
    ]
    pricing_faq_html, pricing_faq_schema = faq_block(pricing_faqs, heading="Removal Pricing — FAQs", bg="bg-white")
    body = "\n".join([
        page_hero("Removal Pricing", "<p>Clear, competitive removal prices with no hidden fees &mdash; and a free, no-obligation quote tailored to your move.</p>",
                  bullets=["Competitive prices with no hidden fees", "Free, no-obligation quotes (video or in person)", "Fully insured &mdash; liability up to £10m"]),
        E.quote_bar(lead="Want an Exact Price?", rest="Get a Free Quote",
                    subtext="Every move is unique — get a tailored, no-obligation quote."),
        E.rich_prose(html, "pricing"),
        E.wolves_feature_panel(E.page_photos("pricing-feature", 1)[0], reverse=False, bg="bg-beige"),
        _process("bg-white"),
        _why_choose("bg-beige"),
        video_survey_block(bg="bg-lightgrey"),
        pricing_faq_html,
        cta_band("Get Your Free, No-Obligation Quote", "Tell us about your move and we&rsquo;ll send a clear, fixed price.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
    ])
    return E.render_page(title="Removal Pricing | Wolves Removals — No Hidden Fees",
        description="Competitive, transparent removal pricing from Wolves Removals with no hidden fees. See what affects the cost of a move and get a free, no-obligation quote.",
        canonical_path="/pricing/", body=body, og_image=HERO, extra_schema=[pricing_faq_schema],
        breadcrumb=[("Home", "/"), ("Pricing", "/pricing/")], active="pricing"), "pricing/index.html"

FAQS = [
    ("Are my goods insured during the move?", "<p>We are fully insured with liability cover up to £10 million. At our standard rates we hold no liability for goods in transit, but we offer full damage insurance for your goods for an extra 10% of your invoice total &mdash; just ask at the quotation stage.</p>"),
    ("Are there items you cannot transport?", "<p>For safety we don&rsquo;t generally transport flammable liquids or gases, and we ask that no paint or oil is transported due to the risk of leaks and damage. If in doubt, mention items at the quote stage and we&rsquo;ll advise.</p>"),
    ("Are your staff trained and vetted?", "<p>Yes. All Wolves staff are experienced movers who have completed our personal training programme and health &amp; safety training, and have passed police CRB/DBS checks. Our team is fully trained and uniformed.</p>"),
    ("What days and hours do you work?", "<p>Our team works 7 days a week and we tailor our service to the exact date and timescale you need. We aim to start promptly, with staff generally leaving base between 6:00am and 8:00am depending on your property&rsquo;s location.</p>"),
    ("Do I need to arrange parking?", "<p>Yes &mdash; arranging parking on the day is down to you. Please organise any necessary permits, passes or paperwork so we can park close to the property and keep your move efficient.</p>"),
    ("Do you dismantle and reassemble furniture?", "<p>Yes. Our vans carry the tools needed to dismantle and reassemble furniture. Please mention you need this at the quotation stage so we can plan time for it.</p>"),
    ("Do you carry out international and EU moves?", "<p>Absolutely &mdash; our motto is &ldquo;No Job Too Big, No Journey Too Far&rdquo;. We have experience moving around the EU and are happy to quote for any <a href=\"/services/international-removals/\">international</a> or <a href=\"/services/european-removals/\">European removal</a>.</p>"),
    ("How can I pay?", "<p>We accept credit/debit cards, cash on completion and BACS payment. Unfortunately we can no longer accept cheques.</p>"),
    ("What affects how long my move takes?", "<p>Several factors, mainly the volume of goods and the distance involved &mdash; but it&rsquo;s often the little things (access, stairs, parking and last-minute packing) that take the most time. Good preparation keeps things moving.</p>"),
    ("How big will the moving crew be?", "<p>Crew size depends on the information we gather beforehand and our site inspection. Generally a crew of 2&ndash;4 movers is sufficient for most home moves.</p>"),
    ("Will you move single items?", "<p>We carry out full removals over any distance. For one-off or small jobs, our <a href=\"/services/man-and-van/\">man and van</a> service is ideal. We&rsquo;re unable to transport certain loose individual items on their own &mdash; just ask and we&rsquo;ll advise.</p>"),
    ("Do you provide packing and boxes?", "<p>Yes &mdash; we can supply boxes, bubble wrap and tape before your move for you to pack yourself, or our team can carefully pack your home piece by piece with our <a href=\"/services/full-packing-service/\">full packing service</a>.</p>"),
    ("Do you help me plan and remember everything?", "<p>Yes &mdash; moving is stressful and it&rsquo;s easy to forget things, so we&rsquo;ve put together a moving plan and checklist to help you stay organised in the run-up to the big day.</p>"),
    ("Which areas do you cover?", "<p>We cover the whole of <a href=\"/locations/west-sussex-removals/\">West Sussex</a> and <a href=\"/locations/east-sussex-removals/\">East Sussex</a>, much of <a href=\"/locations/surrey-removals/\">Surrey</a>, and the <a href=\"/locations/petersfield-removals/\">Petersfield</a> area of <a href=\"/locations/hampshire-removals/\">Hampshire</a> &mdash; plus nationwide and EU moves. See our <a href=\"/locations/\">areas we cover</a>.</p>"),
    ("What kind of service can I expect?", "<p>A friendly, family-based service from a fully trained, uniformed team. We work hard to make your move as stress-free and simple as possible, and our office staff are always on hand to answer questions.</p>"),
    ("What time will you arrive on moving day?", "<p>We aim to start promptly so your move begins smoothly. Our crews generally leave base between 6:00am and 8:00am depending on where your property is, and we&rsquo;ll confirm an expected arrival window with you beforehand.</p>"),
    ("Do you offer storage as well as removals?", "<p>Yes &mdash; we provide clean, dry, ultra-secure containerised <a href=\"/services/storage/\">storage</a> for both <a href=\"/services/storage/short-term-storage/\">short</a> and <a href=\"/services/storage/long-term-storage/\">long-term</a> needs, ideal when your moving dates don&rsquo;t quite line up.</p>"),
    ("Can you move me at the weekend?", "<p>Yes. Our team works 7 days a week and we tailor dates and times to suit you, including weekends, subject to availability &mdash; so book early to secure your preferred slot.</p>"),
]

def faq_page():
    fhtml, fschema = faq_block(FAQS, heading="Frequently Asked Questions", bg="bg-white")
    intro = ('<h2 class="relative leading-tight text-black">Removals Questions, Answered</h2>'
             '<p>Our frequently asked questions offer plenty of advice and hopefully answer your queries before you get '
             'in touch. If you can&rsquo;t find what you&rsquo;re looking for, please <a href="/contact-us/">contact '
             'us</a> &mdash; we&rsquo;re always happy to help.</p>')
    body = "\n".join([
        page_hero("Frequently Asked Questions", "<p>Helpful answers about our removals, packing, storage and insurance &mdash; and how we make your move stress-free.</p>",
                  bullets=["Extremely cost-effective", "Locally based for a personal service", "Responsive, dedicated customer care"]),
        E.quote_bar(lead="Ready When You Are", rest="Get a Free Quote",
                    subtext="Got the answers you need? Request a fast, no-obligation quote."),
        section(prose(intro, span="lg:col-span-10 lg:col-start-2"), bg="bg-lightgrey", extra="logo-row overflow-hidden"),
        fhtml,
        cta_band("Still Have a Question?", "Get in touch and a friendly member of our team will be glad to help.",
                 "Contact Us", "/contact-us/", bg="bg-lightgrey"),
    ])
    return E.render_page(title="Frequently Asked Questions | Wolves Removals Sussex",
        description="Answers to common questions about Wolves Removals: insurance, packing, payment, crew, areas covered and more. Family-run Sussex removals since 2016.",
        canonical_path="/frequently-asked-questions/", body=body, og_image=HERO,
        breadcrumb=[("Home", "/"), ("FAQs", "/frequently-asked-questions/")], extra_schema=[fschema], active="faq"), "frequently-asked-questions/index.html"

def contact_us():
    b = E.S.BUSINESS
    details = (
        '<h2 class="relative leading-tight text-black">Get in Touch With Wolves Removals</h2>'
        '<p>We&rsquo;re always happy to help with any questions. Call us, email us or fill in the form and a friendly '
        'member of our team will be in touch. We aim to respond quickly and can arrange an in-home visit or a video '
        'survey at your convenience.</p>'
        f'<p><strong>Address:</strong> {esc(b["name"])}, {esc(b["street"])}, {esc(b["locality"])}, {esc(b["region"])} {esc(b["postcode"])}<br>'
        f'<strong>Phone:</strong> <a href="{b["phone_link"]}">{b["phone"]}</a> &middot; <a href="{b["mobile_link"]}">{b["mobile"]}</a><br>'
        f'<strong>Email:</strong> <a href="mailto:{b["email"]}">{b["email"]}</a></p>'
        '<p>You can also read our <a href="/frequently-asked-questions/">FAQs</a>, browse our '
        '<a href="/gallery/">gallery</a> or see the <a href="/locations/">areas we cover</a>.</p>')
    body = "\n".join([
        contact_hero(),
        section(prose(details, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        video_survey_block(bg="bg-lightgrey"),
    ])
    return E.render_page(title="Contact Us | Wolves Removals — Sussex Removals Company",
        description="Contact Wolves Removals in Pulborough, West Sussex. Call 01903 893731, email us or request a free quote online. Friendly, family-run Sussex removals team.",
        canonical_path="/contact-us/", body=body, og_image=HERO, show_quote=False,
        breadcrumb=[("Home", "/"), ("Contact Us", "/contact-us/")], active="contact"), "contact-us/index.html"

def get_a_quote():
    intro = ('<h2 class="relative leading-tight text-black">Why Choose Wolves Removals</h2>'
             '<p>To request a free quote without any obligation, complete the form above. One of our moving consultants '
             'will be in touch to arrange a convenient visit or a video survey. You&rsquo;re in safe hands:</p>'
             '<ul class="tick-list"><li>Video or in-person, no-obligation quotes</li>'
             '<li>Competitive home removal prices with no hidden fees</li>'
             '<li>Fully insured with liability cover up to £10 million</li>'
             '<li>LAPADA member, Checkatrade-verified and family-run since 2016</li></ul>')
    body = "\n".join([
        trust_hero("Get a Free Quote",
                   "Tell us about your move and we&rsquo;ll send a clear, fixed price with no obligation.",
                   _quote_form_card("Request Your Free Quote"), reverse=False, equal=True, open_about=True),
        section(prose(intro, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        video_survey_block(bg="bg-white"),
    ])
    return E.render_page(title="Get a Free Quote | Wolves Removals Sussex",
        description="Request a free, no-obligation removals quote from Wolves Removals. Video or in-person surveys, competitive prices, fully insured. Sussex, Surrey, Hampshire & Kent.",
        canonical_path="/get-a-quote/", body=body, og_image=HERO, show_quote=False,
        breadcrumb=[("Home", "/"), ("Get a Quote", "/get-a-quote/")], active="quote"), "get-a-quote/index.html"

def reviews():
    intro = (
        '<h2 class="relative leading-tight text-black">What Our Customers Say</h2>'
        '<p>Reviews are key to our business, so don&rsquo;t just take our word for the level of care our team '
        'provides &mdash; read our customers&rsquo; reviews to see what they have to say about moving with Wolves '
        'Removals. Our dedication to the job is second to none, which is why so many people across Sussex choose us when '
        'moving home.</p>'
        '<p>We&rsquo;re proud of our reputation on independent review platforms. You can read genuine, verified reviews '
        'from our customers here:</p>'
        '<ul class="tick-list">'
        f'<li><a href="{E.S.SOCIAL["facebook"]}" rel="noopener" target="_blank">Read our reviews on Facebook</a></li>'
        '<li><a href="https://www.checkatrade.com/" rel="noopener" target="_blank">Find us on Checkatrade</a> &mdash; verified customer feedback</li>'
        '<li><a href="https://www.google.com/search?q=Wolves+Removals+reviews" rel="noopener" target="_blank">See our Google reviews</a></li>'
        '</ul>'
        '<p>We love hearing from our clients. If you&rsquo;ve moved with us and would like to share your experience, '
        'we&rsquo;d be delighted &mdash; please <a href="/leave-a-review/">leave a review</a>. Your feedback helps us '
        'keep improving and helps others choose the right removals team.</p>')
    _wids = ["9bf688f7376165888b96b8af525", "f62b22e344ef413cc336104943f",
             "4da8f0f7337865876b76fb1246e", "3009af24977d2779b55bb4ba13", "a90600949eb4279f7c5a27ac8a"]
    review_widgets = "".join(
        '<div class="ti-reviews-widget mb-10 last:mb-0">'
        f"<script defer async src='https://cdn.trustindex.io/loader.js?{w}'></script></div>"
        for w in _wids)
    widgets_section = section(
        '<div class="text-center mb-8"><h2 class="relative leading-tight text-black">Read Our Verified Reviews</h2></div>'
        f'<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2">{review_widgets}</div></div>',
        bg="bg-lightgrey")
    body = "\n".join([
        page_hero("Customer Reviews", "<p>Read genuine reviews from people who&rsquo;ve moved with Wolves Removals across Sussex and beyond.</p>",
                  bullets=["Verified reviews on Checkatrade, Google &amp; Facebook", "Family-run, dedicated customer care", "Recommended by leading estate agents"]),
        E.quote_bar(lead="Join Our Happy Customers", rest="Get a Free Quote",
                    subtext="See why Sussex trusts Wolves Removals — get your free quote."),
        section(prose(intro, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        widgets_section,
        _trust_logos("bg-white"),
        cta_band("Moved With Us? Leave a Review", "We&rsquo;d love to hear about your experience.",
                 "Leave a Review", "/leave-a-review/", bg="bg-lightgrey"),
    ])
    return E.render_page(title="Customer Reviews | Wolves Removals Sussex",
        description="Read genuine customer reviews of Wolves Removals on Checkatrade, Google and Facebook. Family-run Sussex removals trusted for home, commercial and antiques moves.",
        canonical_path="/reviews/", body=body, og_image=HERO,
        breadcrumb=[("Home", "/"), ("Reviews", "/reviews/")], active="reviews"), "reviews/index.html"

def leave_a_review():
    intro = ('<h2 class="relative leading-tight text-black">Leave Us a Review</h2>'
             '<p>Thank you for moving with Wolves Removals! We&rsquo;d be grateful if you could take a moment to share '
             'your experience &mdash; it helps us keep improving and helps others choose the right removals team. Leave '
             'a review on your preferred platform, or send us your feedback directly using the form below.</p>'
             '<ul class="tick-list">'
             f'<li><a href="{E.S.SOCIAL["facebook"]}" rel="noopener" target="_blank">Review us on Facebook</a></li>'
             '<li><a href="https://www.google.com/search?q=Wolves+Removals+reviews" rel="noopener" target="_blank">Review us on Google</a></li>'
             '<li><a href="https://www.checkatrade.com/" rel="noopener" target="_blank">Review us on Checkatrade</a></li>'
             '</ul>')
    review_form = section(
        '<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-8 lg:col-start-3">'
        '<div class="bg-white rounded-xl border border-border shadow-custom p-6 lg:p-10">'
        '<h2 class="relative leading-tight text-black text-center">Send Us Your Feedback</h2>'
        f'<form class="mt-6" method="post" action="{FORM_ENDPOINT}" novalidate><div class="grid grid-cols-12 gap-4">'
        + _field("Your name", "name", required=True, half=True) + _field("Email", "email", typ="email", half=True)
        + '<div class="col-span-12"><label class="block font-semibold mb-1" for="f-review">Your review</label>'
          '<textarea class="w-full" id="f-review" name="review" rows="5" required aria-required="true"></textarea></div>'
        + '<div class="col-span-12"><label class="flex items-start gap-2 text-sm"><input type="checkbox" name="consent" required> '
          'I&rsquo;m happy for Wolves Removals to use my feedback and I accept the <a href="/privacy-policy/">privacy policy</a>.</label></div>'
        + '<div class="col-span-12 text-center"><button type="submit" class="button-orange mx-auto">Submit Review</button></div>'
        '</div></form></div></div></div>', bg="bg-lightgrey")
    body = "\n".join([
        page_hero("Leave a Review", "<p>Moved with us? We&rsquo;d love to hear how it went.</p>"),
        section(prose(intro, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        review_form,
    ])
    return E.render_page(title="Leave a Review | Wolves Removals Sussex",
        description="Moved with Wolves Removals? Share your experience on Google, Facebook or Checkatrade, or send your feedback directly. Thank you for choosing our Sussex team.",
        canonical_path="/leave-a-review/", body=body, og_image=HERO, show_quote=False,
        breadcrumb=[("Home", "/"), ("Leave a Review", "/leave-a-review/")], active="reviews"), "leave-a-review/index.html"

def gallery():
    import zlib, render_boxshop as BS
    # Box-shop product/kit shots are e-commerce SKU photos, not "team in action"
    # imagery — keep them out of the gallery. Pulled live from the shop renderer.
    BOXSHOP = {p[5] for p in BS.PRODUCTS} | {k[6] for k in BS.KITS}
    # Near-identical shots already represented by another photo in the grid.
    GALLERY_DUPES = {
        "wrapped-furniture-protective-covers-removals",
        "team-preparing-dining-table-move",
        "wrapping-table-packed-room",
        "wolves-removals-crew-team",
        "wolves-removals-wolf-head-emblem",
        "loading-crates-into-street-van",
        "wolves-luton-van-sussex-home",
        "furniture-loaded-sussex-removal-service",
        "two-removal-vans-at-country-house",
        "two-vans-at-country-house",
        "wolves-removals-storage-certificate-recognition",
        "packing-furniture-in-attic-bedroom",
    }
    EXCLUDE = BOXSHOP | GALLERY_DUPES
    # Show EVERY remaining content photo in the library. Dedupe the pool, then order
    # by a stable hash so near-identical shots aren't adjacent.
    pool = [p for p in dict.fromkeys(E.PHOTOS) if p[0] not in EXCLUDE]  # (name, alt) tuples
    photos = sorted(pool, key=lambda p: zlib.crc32(p[0].encode()))
    # Pad the tail to a multiple of 6 so the grid has no lonely orphan row at any
    # breakpoint (1 / 2 / 3 cols). Reserve = genuine on-disk photos not in the pool.
    RESERVE = [
        ("wolves-storage-units-countryside-field", "Wolves Removals storage units in the Sussex countryside"),
        ("games-room-snooker-table-interior", "A games room with snooker table ahead of a Sussex removal"),
        ("elegant-lounge-before-house-removals", "An elegant lounge prepared for a Sussex house removal"),
        ("empty-period-drawing-room-sea-view", "A period drawing room with sea view cleared for a move"),
        ("empty-period-dining-room-chandelier", "A period dining room with chandelier cleared for a move"),
    ]
    photos += RESERVE[:(-len(photos)) % 6]
    cells = "".join(
        f'<div class="col-span-12 sm:col-span-6 lg:col-span-4"><div class="rounded-xl overflow-hidden border border-border shadow-custom">{img("images/photos/"+n+".webp", a, cls="w-full h-64 object-cover")}</div></div>'
        for n, a in photos)
    intro = ('<h2 class="relative leading-tight text-black">See Our Home Movers in Action</h2>'
             f'<p>Browse our full gallery of {len(photos)} photos &mdash; the Wolves Removals team at work across Sussex, '
             'from careful packing and antique handling to loading, storage and delivery. '
             'It&rsquo;s the care and professionalism in these everyday moments that our customers value most.</p>')
    body = "\n".join([
        page_hero("Gallery", "<p>See the Wolves Removals team in action on moves across Sussex.</p>"),
        E.quote_bar(lead="Picture Your Move Sorted", rest="Get a Free Quote",
                    subtext="Let us handle your move with the same care — get a free quote."),
        section(prose(intro, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        section(f'<div class="grid grid-cols-12 gap-6">{cells}</div>', bg="bg-lightgrey"),
        cta_band("Like What You See?", "Get a free, no-obligation quote for your move.", "Get a Free Quote", "/get-a-quote/", bg="bg-white"),
    ])
    return E.render_page(title="Gallery | Wolves Removals Sussex — Our Team in Action",
        description="See the Wolves Removals team in action across Sussex — packing, loading and delivering home and commercial moves with care. Family-run, fully insured removals.",
        canonical_path="/gallery/", body=body, og_image="images/photos/wolves-team-loading-van-sussex.webp",
        breadcrumb=[("Home", "/"), ("Gallery", "/gallery/")], active="gallery"), "gallery/index.html"

# --- Careers application form (modelled on Mark Ratcliffe, minus the bus/minibus licences) ---
_CAREERS_LIC = [("B", "B (car)"), ("BE", "BE (car + trailer)"), ("C1", "C1 (3.5t&ndash;7.5t)"),
                ("C1E", "C1E (C1 + trailer)"), ("C", "C (rigid LGV)"), ("CE", "CE (artic LGV)"),
                ("CPC", "Driver CPC"), ("ADR", "ADR (hazardous)")]
_CAREERS_RTW = ["Yes &mdash; UK / Irish citizen", "Yes &mdash; settled / pre-settled status",
                "Yes &mdash; visa with right to work", "No / unsure"]
_CAREERS_POS = ["Removals Porter / Mover", "Driver &mdash; LGV (7.5t+)", "Driver &mdash; 3.5t / Van", "Packer",
                "Antiques / Specialist Handler", "Office / Administration", "Self-employed mover", "Other"]
_CAREERS_LICHELD = ["Yes &mdash; full UK", "Yes &mdash; full EU / EEA", "Yes &mdash; provisional", "No"]
_CAREERS_AVAIL = ["Full-time", "Part-time", "Flexible / either", "Seasonal only"]

def _csel(label, name, options, required=False, half=False):
    req = ' required aria-required="true"' if required else ""
    star = ' <span class="text-darkgrey">*</span>' if required else ""
    col = "md:col-span-6" if half else "md:col-span-12"
    opts = '<option value="">&mdash; select &mdash;</option>' + "".join(f'<option>{o}</option>' for o in options)
    return (f'<div class="col-span-12 {col}"><label class="block font-semibold mb-1" for="f-{name}">{label}{star}</label>'
            f'<select class="w-full" id="f-{name}" name="{name}"{req}>{opts}</select></div>')

def _ctext(label, name, placeholder=""):
    return (f'<div class="col-span-12"><label class="block font-semibold mb-1" for="f-{name}">{label}</label>'
            f'<textarea class="w-full" id="f-{name}" name="{name}" rows="4" placeholder="{esc(placeholder)}"></textarea></div>')

def _careers_form():
    lic = "".join(f'<label class="flex items-center gap-2 text-sm"><input type="checkbox" name="licenceCats" value="{v}"> {l}</label>'
                  for v, l in _CAREERS_LIC)
    def grp(title, inner):
        return f'<h3 class="text-lg font-bold text-black mt-7 mb-3 leading-tight">{title}</h3><div class="grid grid-cols-12 gap-4">{inner}</div>'
    return (
        '<div class="bg-white rounded-2xl shadow-custom px-6 lg:px-8 py-10 text-black">'
        '<h2 class="leading-tight text-black">Job Application Form</h2>'
        '<p class="text-darkgrey text-sm mt-1 mb-0">Fields marked <span class="font-semibold">*</span> are required &mdash; it takes about five minutes.</p>'
        '<form id="careers-form" class="enquiry-form mt-2" method="post" action="/api/careers" novalidate>'
        + grp("Your details",
              _field("First name", "firstName", required=True, half=True)
              + _field("Last name", "lastName", required=True, half=True)
              + _field("Email", "email", typ="email", required=True, half=True)
              + _field("Phone", "phone", typ="tel", required=True, half=True)
              + _field("Town / city", "town", half=True)
              + _field("Postcode", "postcode", required=True, half=True)
              + _csel("Right to work in the UK", "rightToWork", _CAREERS_RTW, required=True))
        + grp("The role",
              _csel("Position applied for", "position", _CAREERS_POS, required=True)
              + _csel("Availability", "availability", _CAREERS_AVAIL, half=True)
              + _field("Earliest start date", "startDate", typ="date", half=True))
        + grp("Driving",
              _csel("Do you hold a driving licence?", "licence", _CAREERS_LICHELD, half=True)
              + _field("Years driving", "yearsDriving", typ="number", half=True)
              + f'<div class="col-span-12"><span class="block font-semibold mb-2">Licence categories (tick all that apply)</span>'
                f'<div class="grid grid-cols-2 sm:grid-cols-3 gap-2">{lic}</div></div>')
        + grp("Experience",
              _field("Years in removals / moving", "yearsRemovals", typ="number", half=True)
              + _ctext("Previous experience &mdash; companies, roles, dates", "experience", "Most recent employer first. Include dates if you can.")
              + _ctext("Why this role &mdash; what attracts you to working with us?", "whyRole", "Optional &mdash; but it really helps."))
        + '<div class="grid grid-cols-12 gap-4 mt-7">'
        + '<div class="col-span-12 hidden" aria-hidden="true"><label>Leave blank<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>'
        + '<div class="col-span-12"><label class="flex items-start gap-2 text-sm text-darkgrey"><input type="checkbox" name="consent" required aria-required="true"> '
          '<span>I consent to Wolves Removals storing the information in this application to process my enquiry, under the '
          '<a href="/privacy-policy/">privacy policy</a>. I can request deletion at any time. <span class="font-semibold">*</span></span></label></div>'
        + '<div class="col-span-12"><button type="submit" class="button w-full justify-center">Submit Application</button>'
          '<p data-careers-status class="mt-3 text-sm text-darkgrey text-center mb-0" role="status" aria-live="polite"></p></div>'
        + '</div></form></div>')

def job_vacancies():
    intro = ('<h2 class="relative leading-tight text-black">Careers at Wolves Removals</h2>'
             '<p>We&rsquo;re a friendly, family-run Sussex removals and storage company that has been keeping its promises '
             'since 2016. Our crews are in customers&rsquo; homes every day, so we hire for character first &mdash; '
             'trustworthy, polite, careful people &mdash; then train the skills in-house. As a <strong>LAPADA member</strong> '
             'and <strong>Checkatrade-verified</strong> team, we take real pride in doing things properly.</p>'
             '<p>We take on experienced movers, drivers and packers, but removals experience isn&rsquo;t essential &mdash; '
             'many of our team arrived from completely different backgrounds. Every role includes full in-house training and '
             'health &amp; safety training, and is subject to a DBS check. If that sounds like you, fill in the application '
             'form below and we&rsquo;ll be in touch.</p>')
    look = ('<h2 class="relative leading-tight text-black">What We Look For</h2>'
            '<p>Three things, in this order. <strong>Character</strong> &mdash; you&rsquo;ll be in customers&rsquo; homes, so '
            'trustworthiness, politeness and care matter most. <strong>Reliability</strong> &mdash; the team needs you on '
            'time, in the right uniform, with the right kit. <strong>Physical capability</strong> &mdash; the work is heavy, '
            'and stairs and awkward access are routine.</p>'
            '<h3 class="text-black leading-tight mt-6">How our application process works</h3>'
            '<p>The form above takes around five minutes. You&rsquo;ll receive a confirmation email, and our team reviews '
            'every application within five working days. If your experience is a fit, we&rsquo;ll arrange a phone call or an '
            'in-person chat. Permanent and self-employed roles both follow the same process.</p>'
            '<h3 class="text-black leading-tight mt-6">Training is on us</h3>'
            '<p>Removals experience is welcome but not required. New starters train in-house across pad-wrap method, fragile '
            'handling, antique and fine-art care, inventory paperwork and customer service. As LAPADA specialists in '
            '<a href="/services/specialised-antiques-moving/">antiques and fine art</a>, we&rsquo;ll teach you to handle '
            'valuable, delicate items with real confidence.</p>')
    cfaqs = [
        ("Do I need removals experience?", "<p>No &mdash; experience is welcome but not essential. We provide full in-house training, so what matters most is the right attitude: reliable, careful and good with customers.</p>"),
        ("What roles do you hire for?", "<p>Removals porters/movers, drivers (van and LGV), packers, antiques/specialist handlers and office staff &mdash; plus self-employed movers. Tell us what you&rsquo;re after on the form.</p>"),
        ("Do you carry out background checks?", "<p>Yes &mdash; roles are subject to a DBS check, as our teams work in customers&rsquo; homes.</p>"),
        ("How will I hear back?", "<p>You&rsquo;ll receive a confirmation email, and we review every application within five working days. If it&rsquo;s a fit, we&rsquo;ll be in touch to arrange a chat.</p>"),
        ("Can I apply if I&rsquo;m self-employed?", "<p>Absolutely &mdash; we work with self-employed movers too. Just select &ldquo;Self-employed mover&rdquo; on the form.</p>"),
    ]
    cfaq_html, cfaq_schema = faq_block(cfaqs, heading="Careers &mdash; Your Questions Answered", bg="bg-white")
    body = "\n".join([
        page_hero("Careers at Wolves Removals",
                  "<p>Join a friendly, family-run Sussex removals team. We hire for character and train the skills &mdash; apply below.</p>",
                  bullets=["Family-run &amp; trusted since 2016", "Full in-house training &mdash; no experience needed",
                           "LAPADA member &amp; Checkatrade-verified", "Movers, drivers, packers &amp; office roles"]),
        E.quote_bar(lead="Ready to Apply?", rest="Fill in the form below",
                    subtext="It takes about five minutes — we review every application within five working days."),
        section(prose(intro, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        section('<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2">' + _careers_form() + '</div></div>', bg="bg-lightgrey"),
        section(prose(look, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        cfaq_html,
        cta_band("Not Sure Which Role Fits?", "Get in touch and tell us a bit about yourself &mdash; we&rsquo;d love to hear from you.",
                 "Contact Us", "/contact-us/", bg="bg-lightgrey"),
        f'<script defer src="/js/careers-form.js?v={E.ASSET_VER}"></script>',
    ])
    return E.render_page(title="Careers | Jobs at Wolves Removals Sussex",
        description="Careers at Wolves Removals — join our friendly, family-run Sussex removals team. Movers, drivers, packers & office roles, full training, no experience needed. Apply online.",
        canonical_path="/job-vacancies/", body=body, og_image=HERO, extra_schema=[cfaq_schema],
        breadcrumb=[("Home", "/"), ("Careers", "/job-vacancies/")], active="about"), "job-vacancies/index.html"

def _legal(title, slug, h1, intro, sections):
    secs = "".join(f'<h2 class="relative leading-tight text-black">{h}</h2>{b}' for h, b in sections)
    html = f'<p>{intro}</p>{secs}'
    body = "\n".join([
        page_hero(h1, "<p>How we handle your information and the terms of our service.</p>"),
        section(prose(html, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
    ])
    return E.render_page(title=title, description=intro[:140],
        canonical_path=f"/{slug}/", body=body, og_image=HERO, robots="index, follow",
        breadcrumb=[("Home", "/"), (h1, f"/{slug}/")]), f"{slug}/index.html"

def privacy_policy():
    return _legal("Privacy Policy | Wolves Removals", "privacy-policy", "Privacy Policy",
        "Wolves Removals is committed to protecting your privacy and handling your personal data in line with UK GDPR and the Data Protection Act 2018.",
        [("What We Collect", "<p>We collect only the information needed to respond to your enquiry and provide your removal &mdash; such as your name, contact details, addresses and move details, submitted via our forms, by phone or by email.</p>"),
         ("How We Use It", "<p>We use your information to provide quotes, arrange and carry out your move, and respond to your queries. We do not sell your data, and we only share it with third parties where necessary to deliver your move or where required by law.</p>"),
         ("How Long We Keep It", "<p>We keep personal data only as long as necessary for the purposes above and to meet our legal obligations, after which it is securely deleted.</p>"),
         ("Your Rights", "<p>Under UK GDPR you have the right to access, correct, or request deletion of your personal data, and to object to or restrict its processing. To exercise these rights, contact us at "
          f'<a href="mailto:{E.S.BUSINESS["email"]}">{E.S.BUSINESS["email"]}</a>.</p>'),
         ("Cookies", "<p>This website uses minimal cookies necessary for it to function. We do not use intrusive tracking. You can control cookies through your browser settings.</p>"),
         ("Contact", f'<p>For any privacy questions, contact Wolves Removals at <a href="mailto:{E.S.BUSINESS["email"]}">{E.S.BUSINESS["email"]}</a> or {E.S.BUSINESS["phone"]}.</p>')])

def terms_conditions():
    return _legal("Terms & Conditions | Wolves Removals", "terms-conditions", "Terms & Conditions",
        "These terms set out the basis on which Wolves Removals provides its removal, packing and storage services. Full written terms are provided with your quotation.",
        [("Quotes & Bookings", "<p>Quotes are based on the information you provide and any survey carried out. Bookings are confirmed on receipt of any agreed deposit. Please tell us about access, parking and special items at the quotation stage.</p>"),
         ("Insurance & Liability", "<p>We are fully insured with liability cover up to £10 million. At standard rates we hold no liability for goods in transit; full damage insurance for your goods is available for an additional 10% of your invoice total. Please ask for details.</p>"),
         ("Items We Cannot Carry", "<p>For safety we do not transport flammable liquids or gases, paint or oil. Please remove such items before your move.</p>"),
         ("Payment", "<p>We accept credit/debit cards, cash on completion and BACS. We are unable to accept cheques.</p>"),
         ("Your Responsibilities", "<p>Please arrange any necessary parking permits or passes, and ensure access is available at both properties. Full terms and conditions are supplied with your written quotation.</p>"),
         ("Contact", f'<p>Questions about these terms? Contact us at <a href="mailto:{E.S.BUSINESS["email"]}">{E.S.BUSINESS["email"]}</a> or {E.S.BUSINESS["phone"]}.</p>')])

def not_found():
    html = ('<div class="text-center"><h1 class="text-5xl lg:text-7xl font-bold text-orange">404</h1>'
            '<h2 class="relative leading-tight text-black mt-4">Page Not Found</h2>'
            '<p class="text-lg xl:text-xl">Sorry, we couldn&rsquo;t find that page. It may have moved. Try one of these:</p>'
            '<div class="flex flex-wrap gap-3 justify-center mt-6">'
            '<a href="/" class="button-orange">Home</a>'
            '<a href="/services/" class="px-6 py-3 rounded-full border-2 border-orange text-orange font-semibold uppercase hover:bg-orange hover:text-white">Services</a>'
            '<a href="/locations/" class="px-6 py-3 rounded-full border-2 border-orange text-orange font-semibold uppercase hover:bg-orange hover:text-white">Areas We Cover</a>'
            '<a href="/get-a-quote/" class="px-6 py-3 rounded-full border-2 border-orange text-orange font-semibold uppercase hover:bg-orange hover:text-white">Get a Quote</a>'
            '<a href="/contact-us/" class="px-6 py-3 rounded-full border-2 border-orange text-orange font-semibold uppercase hover:bg-orange hover:text-white">Contact</a>'
            '</div></div>')
    body = section(f'<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-8 lg:col-start-3 py-12">{html}</div></div>', bg="bg-white", extra="logo-row overflow-hidden")
    doc = E.render_page(title="Page Not Found (404) | Wolves Removals",
        description="Sorry, that page could not be found. Browse Wolves Removals services, areas covered, or get a free quote.",
        canonical_path="/404.html", body=body, og_image=HERO, robots="noindex, follow", show_quote=False)
    return doc, "404.html"

def _legacy_page(slug, title, desc, h1, lead, body_html, cta_h, cta_text, cta_label, cta_url):
    """Real (200) self-canonical noindex landing page kept at a legacy URL, so the old URL
    resolves to useful content with a clear path to the live page &mdash; no redirect, no 404."""
    body = "\n".join([
        page_hero(h1, lead),
        section(prose(body_html, span="lg:col-span-10 lg:col-start-2"), bg="bg-white", extra="logo-row overflow-hidden"),
        cta_band(cta_h, cta_text, cta_label, cta_url, bg="bg-lightgrey"),
    ])
    return E.render_page(title=title, description=desc, canonical_path=f"/{slug}/", body=body, og_image=HERO,
        robots="noindex, follow", breadcrumb=[("Home", "/"), (h1, f"/{slug}/")], active="", show_quote=False), f"{slug}/index.html"

def legacy_pages():
    b = E.S.BUSINESS
    home = _legacy_page("home", "Welcome — Wolves Removals Sussex",
        "Wolves Removals: friendly, family-run Sussex removals, storage and packing. Home, commercial, antiques and European moves.",
        "Welcome to Wolves Removals",
        "<p>A friendly, family-run Sussex removals &amp; storage team &mdash; here&rsquo;s everything we do.</p>",
        '<h2 class="relative leading-tight text-black">Your Local Sussex Removals &amp; Storage Team</h2>'
        '<p>Since 2016, Wolves Removals has helped households and businesses move across West Sussex, East Sussex, Surrey and '
        'Hampshire &mdash; and further afield across the UK and into Europe. We handle home and commercial removals, full packing, '
        'secure containerised storage and specialist antiques moves, all with genuine, family-run care.</p>'
        '<p>You&rsquo;ve followed an older link &mdash; head to our <a href="/">homepage</a> to explore our services, read genuine '
        '<a href="/reviews/">customer reviews</a> and get a free quote.</p>',
        "Explore Wolves Removals", "Browse our removals, storage and packing services and get a free, no-obligation quote.",
        "Visit Our Homepage", "/")
    contact = _legacy_page("contact", "Contact Our Team — Wolves Removals",
        "Contact Wolves Removals, Pulborough, West Sussex. Call 01903 893731, email us, or send a message for a free removals quote.",
        "Contact Our Sussex Removals Team",
        "<p>Call, email or send us a message &mdash; a friendly, family-run Sussex team, ready to help with your move.</p>",
        '<h2 class="relative leading-tight text-black">Get in Touch</h2>'
        '<p>We&rsquo;re always happy to help with any questions about your move. Call us, email us, or send a message and a '
        'friendly member of the team will be in touch.</p>'
        f'<p><strong>Phone:</strong> <a href="{b["phone_link"]}">{b["phone"]}</a> &middot; <a href="{b["mobile_link"]}">{b["mobile"]}</a><br>'
        f'<strong>Email:</strong> <a href="mailto:{b["email"]}">{b["email"]}</a><br>'
        f'<strong>Address:</strong> {esc(b["name"])}, {esc(b["street"])}, {esc(b["locality"])}, {esc(b["region"])} {esc(b["postcode"])}</p>'
        '<p>To send us a message or request a quote, head to our <a href="/contact-us/">contact page</a>.</p>',
        "Ready to Talk?", "Send us a message or request a free, no-obligation quote.",
        "Go to Our Contact Page", "/contact-us/")
    quote = _legacy_page("quote", "Get Your Free Quote — Wolves Removals",
        "Get a free, no-obligation removals quote from Wolves Removals. Clear, fixed written prices for home, commercial, packing and storage in Sussex.",
        "Get Your Free Moving Quote",
        "<p>A fast, fixed, no-obligation price from your local Sussex removals team.</p>",
        '<h2 class="relative leading-tight text-black">Free, No-Obligation Quotes</h2>'
        '<p>Tell us about your move and we&rsquo;ll send a clear, fixed written quote &mdash; no hidden extras. We offer free '
        'in-home and video surveys at a time that suits you, covering home and commercial removals, packing, storage and '
        'specialist moves.</p>'
        '<p>Ready when you are &mdash; head to our <a href="/get-a-quote/">quote page</a> to fill in our quick form.</p>',
        "Ready for Your Quote?", "Fill in our quick form for a fast, fixed, no-obligation price.",
        "Get a Free Quote", "/get-a-quote/")
    return [home, contact, quote]

def build():
    pages = [about_us(), pricing(), faq_page(), contact_us(), get_a_quote(), reviews(),
             leave_a_review(), gallery(), job_vacancies(), privacy_policy(), terms_conditions(), not_found()] + legacy_pages()
    for doc, path in pages:
        E.write(path, doc)
    print(f"built {len(pages)} core pages")

if __name__ == "__main__":
    build()
