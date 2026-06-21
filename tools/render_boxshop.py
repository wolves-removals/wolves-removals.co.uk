# -*- coding: utf-8 -*-
"""Box Shop — a Shopify-style packing-materials shop. Customers add items with quantity
steppers; a live sticky basket shows the running order; on submit, Wolves and the
customer both receive an order email (front-end posts to /api/boxshop -> Resend)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, img, section, faq_block, cta_band, icon as _eicon

HERO = "images/photos/movers-taping-cardboard-box-packing.webp"

# (id, name, price £, description, icon-key). Prices/dimensions from the old box shop.
# (id, name, price £, description, icon-key, image). `image` (a /images/photos webp stem)
# overrides the icon with a real product photo when supplied.
PRODUCTS = [
    ("small-box", "Small Box", 2.80, "18in &times; 13in &times; 13in", "box", "small-moving-box"),
    ("large-box", "Large Box", 4.20, "18in &times; 18in &times; 20in", "box", "large-moving-box"),
    ("extra-large-box", "Extra Large Box", 4.50, "18in &times; 18in &times; 30in", "box", "extra-large-moving-box"),
    ("wardrobe-box", "Wardrobe Box", 12.50, "20in &times; 18in &times; 48in &mdash; holds 20&ndash;30 garments", "wardrobe", "wardrobe-moving-box"),
    ("packing-tape", "Packing Tape", 2.50, "50m &times; 5cm high-quality vinyl", "tape", "packing-tape-roll"),
    ("bubble-wrap", "Bubble Wrap", 20.00, "25m roll of 75cm width", "bubble", "bubble-wrap-roll"),
    ("packing-paper", "Packing Paper", 19.80, "10kg of paper", "paper", "packing-paper-pack"),
    ("mattress-protector", "Mattress Protector", 13.00, "Plastic mattress cover", "mattress", "mattress-protector-cover"),
    ("marker-pen", "Marker Pen", 2.00, "Permanent marker for labelling boxes", "pen", "marker-pen"),
]

ICONS = {
    "box": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M12 2.5l8.5 4.2v10.6L12 21.5l-8.5-4.2V6.7L12 2.5z"/><path d="M3.5 6.7L12 11l8.5-4.3M12 11v10.5"/></svg>',
    "wardrobe": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><rect x="5.5" y="3.5" width="13" height="17" rx="1"/><path d="M9 3.5v4M15 3.5v4M9 7.5h6" stroke-linecap="round"/><path d="M12 11.5v2" stroke-linecap="round"/></svg>',
    "tape": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><circle cx="11" cy="12" r="7.5"/><circle cx="11" cy="12" r="2.6"/><path d="M18.4 12H22l-1.6 3"/></svg>',
    "bubble": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="8" cy="10" r="1.1"/><circle cx="12" cy="10" r="1.1"/><circle cx="16" cy="10" r="1.1"/><circle cx="10" cy="14" r="1.1"/><circle cx="14" cy="14" r="1.1"/></svg>',
    "paper": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3.5" width="14" height="17" rx="1"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
    "mattress": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="8.5" width="19" height="7" rx="2.5"/><path d="M6.5 8.5v7M10.5 8.5v7M14.5 8.5v7M18.5 8.5v7"/></svg>',
    "kit": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M2.5 9.3l5.5-2.7 5.5 2.7-5.5 2.7-5.5-2.7z"/><path d="M2.5 9.3v6l5.5 2.7 5.5-2.7v-6"/><path d="M8 12v6.7"/><path d="M15 6.2l3-1.5 3 1.5-3 1.5-3-1.5z"/><path d="M15 6.2v4.2l3 1.5 3-1.5V6.2"/></svg>',
    "pen": '<svg class="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1.5-4.5L15.5 5.5l3 3L8.5 18.5 4 20z"/><path d="M13.5 7.5l3 3"/></svg>',
}

# House moving kits — each kit is a real bundle; its price is the exact sum of its
# contents (no markup), and those contents are listed on the card. Adjust the quantities
# in KIT_CONTENTS to taste — the price and the on-card list update automatically.
_PRICE = {p[0]: p[2] for p in PRODUCTS}
_PNAME = {p[0]: p[1] for p in PRODUCTS}
KIT_CONTENTS = {
    "kit-1-bed": [("small-box", 10), ("large-box", 5), ("packing-tape", 2), ("bubble-wrap", 1)],
    "kit-2-bed": [("small-box", 15), ("large-box", 10), ("packing-tape", 3), ("bubble-wrap", 1), ("packing-paper", 1)],
    "kit-3-bed": [("small-box", 20), ("large-box", 15), ("extra-large-box", 2), ("wardrobe-box", 1),
                  ("packing-tape", 4), ("bubble-wrap", 2), ("packing-paper", 1)],
    "kit-4-bed": [("small-box", 25), ("large-box", 20), ("extra-large-box", 4), ("wardrobe-box", 2),
                  ("packing-tape", 5), ("bubble-wrap", 2), ("packing-paper", 2)],
}
def _kit_price(kid):
    return round(sum(_PRICE[i] * q for i, q in KIT_CONTENTS[kid]), 2)
def _kit_desc(kid):
    return ", ".join(f"{q} &times; {_PNAME[i]}" for i, q in KIT_CONTENTS[kid])
KITS = [
    ("kit-1-bed", "1 Bedroom Moving Kit", _kit_price("kit-1-bed"), _kit_desc("kit-1-bed"), "kit", None, "one-bedroom-moving-kit"),
    ("kit-2-bed", "2 Bedroom Moving Kit", _kit_price("kit-2-bed"), _kit_desc("kit-2-bed"), "kit", None, "two-bedroom-moving-kit"),
    ("kit-3-bed", "3 Bedroom Moving Kit", _kit_price("kit-3-bed"), _kit_desc("kit-3-bed"), "kit", "Most popular", "three-bedroom-moving-kit"),
    ("kit-4-bed", "4 Bedroom Moving Kit", _kit_price("kit-4-bed"), _kit_desc("kit-4-bed"), "kit", None, "four-bedroom-moving-kit"),
]

CART_SVG = ('<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/>'
            '<path d="M2 3h2.2l2.1 11.4a1.5 1.5 0 001.5 1.2h8.7a1.5 1.5 0 001.5-1.2L20 7H5.2"/></svg>')

def _hero():
    hero_img = img(HERO, "Wolves Removals box shop — moving boxes and packing materials", cls="w-full h-full object-cover", eager=True)
    # Hidden on mobile (straight to the shop); shown on desktop.
    return ('<section class="relative w-full bg-darkgrey text-white overflow-hidden hidden lg:flex items-center min-h-[24rem] lg:min-h-[30rem]">'
            f'<div class="absolute inset-0">{hero_img}</div>'
            '<div class="container relative z-10 w-full py-[3.4rem] lg:py-[5.5rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-8 hero-panel">'
            '<span class="inline-block bg-[#dad6c2] text-black text-sm font-semibold uppercase px-3 py-1 rounded-full mb-3">Box Shop</span>'
            '<h1 class="text-3xl lg:text-5xl font-bold leading-tight">Moving Boxes &amp; Packing Materials</h1>'
            '<div class="mt-4 text-lg xl:text-xl max-w-3xl">Strong, double-walled boxes, tape, bubble wrap and more &mdash; '
            'add what you need to your basket and we&rsquo;ll confirm your order and arrange collection or delivery across Sussex. '
            '<strong>Free delivery on orders over &pound;75 within Sussex.</strong></div>'
            f'{E.hero_review_row()}'
            '</div></div></div></section>')

def _trust_bar():
    pts = [("Strong, double-walled boxes", "box-icon"),
           ("Free collection from us", "tick"),
           ("Free delivery over &pound;75 in Sussex", "van"),
           ("Family-run &amp; trusted since 2016", "tick")]
    cells = "".join(
        f'<div class="flex items-center justify-center gap-2 text-center"><span class="ico-badge w-9 h-9 shrink-0">{_eicon("check","w-4 h-4")}</span>'
        f'<span class="text-sm lg:text-base font-semibold text-black">{label}</span></div>'
        for label, _ in pts)
    return section(f'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">{cells}</div>',
                   bg="bg-lightgrey", extra="hidden lg:block")

def _prod_cat(icon):
    return "boxes" if icon in ("box", "wardrobe") else "materials"

def _product_card(pid, name, price, desc, icon, badge=None, image=None, cat=""):
    badge_html = (f'<span class="absolute top-3 left-3 z-10 bg-[#dad6c2] text-black text-xs font-bold uppercase tracking-wide px-2.5 py-1 rounded-full shadow">{badge}</span>'
                  if badge else "")
    if image:  # real product photo (sits on a white tile so white-background shots blend)
        media = f'<span class="bs-icon block w-4/5 h-4/5">{img("images/photos/" + image + ".webp", esc(name), cls="w-full h-full object-contain")}</span>'
        tile = "bg-white"
    else:      # fall back to the line-art icon on a soft tile
        media = f'<span class="bs-icon block w-2/5 h-2/5 text-darkgrey">{ICONS[icon]}</span>'
        tile = "bg-beige"
    _d = desc.replace("&times;", " ").replace("&mdash;", " ").replace("&ndash;", " ").replace("&amp;", " ")
    search = esc((name + " " + _d).lower())
    return (f'<article data-bs-card="{pid}" data-bs-cat="{cat}" data-bs-search="{search}" class="bs-card relative flex flex-col bg-white border border-border rounded-2xl overflow-hidden '
            f'transition duration-200 hover:shadow-xl hover:-translate-y-1">'
            f'<div class="relative aspect-square {tile} flex items-center justify-center overflow-hidden">'
            f'{badge_html}{media}'
            f'<span class="bs-in absolute top-3 right-3 z-10 items-center gap-1 bg-[#dad6c2] text-black text-xs font-bold px-2.5 py-1 rounded-full shadow">In basket</span>'
            f'</div>'
            f'<div class="flex flex-col flex-1 p-4">'
            f'<h3 class="font-bold text-black text-base leading-snug">{name}</h3>'
            f'<p class="text-sm text-darkgrey mt-1 flex-1">{desc}</p>'
            f'<div class="mt-3 flex items-center justify-between gap-2">'
            f'<span class="text-lg font-bold text-black">&pound;{price:.2f}</span>'
            f'<div class="inline-flex items-center rounded-full border border-border bg-white overflow-hidden shrink-0">'
            f'<button type="button" data-bs-step="-1" aria-label="Remove one {esc(name)}" class="w-8 h-8 flex items-center justify-center text-lg font-bold text-darkgrey hover:bg-[#dad6c2] hover:text-black transition">&minus;</button>'
            f'<input data-bs-product="{pid}" data-bs-name="{esc(name)}" data-bs-price="{price:.2f}" value="0" inputmode="numeric" '
            f'aria-label="Quantity of {esc(name)}" class="w-9 h-8 text-center font-semibold text-black border-0 focus:outline-none bg-white p-0">'
            f'<button type="button" data-bs-step="1" aria-label="Add one {esc(name)}" class="w-8 h-8 flex items-center justify-center text-lg font-bold text-darkgrey hover:bg-[#dad6c2] hover:text-black transition">+</button>'
            f'</div></div></div></article>')

def _basket():
    ipt = "w-full rounded-lg border border-border px-4 py-2.5 text-black bg-white"
    return (
        '<div class="bg-white overflow-hidden min-h-full lg:min-h-0 lg:rounded-2xl lg:border lg:border-border lg:shadow-custom lg:max-h-[calc(100vh_-_13rem)] lg:overflow-y-auto">'
        f'<div class="flex items-center gap-3 p-5 bg-darkgrey text-white">{CART_SVG}'
        '<h2 class="text-lg font-bold leading-none">Your Basket</h2>'
        '<span data-bs-count class="ml-auto bg-[#dad6c2] text-black text-sm font-bold min-w-[1.75rem] h-7 px-2 inline-flex items-center justify-center rounded-full">0</span>'
        '<button type="button" data-bs-close class="lg:hidden -mr-1 p-1 text-white/80 hover:text-white" aria-label="Close basket">'
        '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'
        '<div data-bs-items class="px-5 max-h-[22rem] overflow-y-auto"></div>'
        '<div class="p-5 border-t border-border bg-lightgrey">'
        '<div class="flex justify-between items-center font-bold text-lg"><span>Subtotal</span><span data-bs-total>&pound;0.00</span></div>'
        '<p class="text-xs text-darkgrey mt-1">Free collection &middot; free delivery over &pound;75 in Sussex &middot; nothing charged online.</p></div>'
        '<form id="bs-form" class="p-5 space-y-3 border-t border-border" novalidate>'
        '<h3 class="font-bold text-black">Your details</h3>'
        f'<input type="text" name="name" placeholder="Your Name" required class="{ipt}">'
        f'<input type="email" name="email" placeholder="Your Email" required class="{ipt}">'
        f'<input type="tel" name="phone" placeholder="Your Phone" class="{ipt}">'
        f'<select name="fulfilment" class="{ipt}"><option value="Collection">Collection from us (free)</option>'
        '<option value="Delivery">Delivery (free over &pound;75 in Sussex)</option></select>'
        f'<textarea name="address" rows="2" placeholder="Delivery address (if delivering)" class="{ipt}"></textarea>'
        f'<textarea name="notes" rows="2" placeholder="Anything else? (move date, etc.)" class="{ipt}"></textarea>'
        '<button type="submit" class="button-orange w-full justify-center">Place Order</button>'
        '<p data-bs-msg class="text-sm font-semibold text-darkgrey" role="status" aria-live="polite"></p>'
        '<p class="text-xs text-darkgrey">We&rsquo;ll email you a copy and confirm availability, payment and delivery. '
        '<noscript>Online ordering needs JavaScript &mdash; please call us to order.</noscript></p>'
        '</form></div>')

def build():
    # One filterable grid: kits first, then boxes, then other materials.
    items = [(_product_card(*k, cat="kits"), "kits") for k in KITS]
    items += [(_product_card(p[0], p[1], p[2], p[3], p[4], image=p[5], cat=_prod_cat(p[4])), _prod_cat(p[4]))
              for p in PRODUCTS]
    cards_html = "".join(c for c, _ in items)
    counts = {"all": len(items)}
    for _, cat in items:
        counts[cat] = counts.get(cat, 0) + 1
    PILLS = [("all", "All"), ("kits", "Moving Kits"), ("boxes", "Boxes"), ("materials", "Packing Materials")]
    pill_html = "".join(
        f'<button type="button" data-bs-filter="{key}" '
        f'class="bs-pill{" bs-pill-on" if key == "all" else ""} whitespace-nowrap rounded-full border border-border '
        f'px-4 py-2 text-sm font-semibold text-darkgrey bg-white hover:border-darkgrey transition">'
        f'{label} <span class="opacity-60">{counts.get(key, 0)}</span></button>'
        for key, label in PILLS)
    search_input = (
        '<div class="relative mb-3">'
        '<input type="search" id="bs-search" placeholder="Search products&hellip;" aria-label="Search products" autocomplete="off" '
        'class="w-full rounded-lg border border-border bg-white pl-11 pr-4 py-2.5 text-black focus:border-[#262626] focus:outline-none">'
        '<svg class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-darkgrey pointer-events-none" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle>'
        '<path d="M21 21l-4.3-4.3" stroke-linecap="round"></path></svg></div>')
    left = (
        '<div class="-mx-4 px-4 lg:mx-0 lg:px-0 mb-6 lg:mb-8 sticky top-[100px] sm:top-[108px] lg:static z-30 bg-[#6a7682] lg:bg-transparent py-2">'
        + search_input
        + f'<div class="bs-pills flex gap-2 overflow-x-auto pb-1" role="tablist" aria-label="Filter products">{pill_html}</div></div>'
        f'<div class="grid grid-cols-2 xl:grid-cols-4 gap-4 xl:gap-5">{cards_html}</div>'
        '<p data-bs-noresults class="hidden text-center text-darkgrey py-10">No products match &mdash; '
        '<button type="button" data-bs-clear class="text-[#262626] underline">clear filters</button>.</p>')
    # Mobile: the basket is a slide-in drawer (.bs-drawer) opened by a sticky bottom bar,
    # so it's reachable however long the product list is. Desktop: the sticky sidebar.
    overlay = '<div data-bs-overlay class="hidden lg:hidden fixed inset-0 bg-black/50 z-[60]"></div>'
    bar = ('<button type="button" data-bs-open aria-label="View your basket" '
           'class="lg:hidden fixed bottom-0 inset-x-0 z-50 bg-darkgrey text-white px-4 py-3.5 flex items-center gap-3 text-left shadow-[0_-6px_24px_rgba(0,0,0,.28)]">'
           f'<span class="relative inline-flex shrink-0">{CART_SVG}'
           '<span data-bs-count class="absolute -top-2 -right-2 bg-[#dad6c2] text-black text-[11px] font-bold min-w-[1.15rem] h-[1.15rem] px-1 inline-flex items-center justify-center rounded-full">0</span></span>'
           '<span class="font-bold text-lg" data-bs-total>&pound;0.00</span>'
           '<span class="ml-auto font-bold uppercase text-sm tracking-wide inline-flex items-center gap-1">View Basket'
           '<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></span></button>')
    content = (
        '<div class="bs-shop-shell">'
        '<div class="text-center mb-8 lg:mb-12"><h2 class="relative leading-tight text-white">Choose Your Packing Materials</h2>'
        '<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto text-[#eceef0]">Pick a ready-made moving kit, or add individual items with the '
        '&minus; / + buttons. Your basket updates as you go &mdash; then send us your order in one click.</p></div>'
        '<div class="grid grid-cols-12 gap-8 lg:gap-10 items-start">'
        f'<div class="col-span-12 lg:col-span-8">{left}</div>'
        f'<aside class="bs-drawer lg:col-span-4 lg:sticky lg:top-[180px]">{_basket()}</aside>'
        '</div>'
        '</div>'
        + overlay + bar)
    shop = section(content, bg="bg-white", extra="lg:!overflow-visible")
    faqs = [
        ("How do I order packing materials?",
         "<p>Add what you need to your basket with the &minus; / + buttons, fill in your details and hit <strong>Place Order</strong>. "
         "We&rsquo;ll email you a copy and get back to you to confirm availability, payment and collection or delivery.</p>"),
        ("Can I collect, or do you deliver?",
         "<p>Both &mdash; collection from us is free, and <strong>delivery within Sussex is free on orders over &pound;75</strong>. "
         "Under that we deliver across Sussex for a small charge we&rsquo;ll confirm with you. "
         "Choose your preference in the basket, or <a href=\"/contact-us/\">get in touch</a> if you&rsquo;re not sure.</p>"),
        ("How do I pay?",
         "<p>You don&rsquo;t pay online. Once we&rsquo;ve confirmed your order and stock we&rsquo;ll arrange payment with you directly &mdash; "
         "simple and secure.</p>"),
        ("Do you offer materials as part of a removal?",
         "<p>Yes. If we&rsquo;re handling your move you can add materials to your quote, or use our full "
         "<a href=\"/services/full-packing-service/\">packing service</a> and let our team do it all. "
         "<a href=\"/get-a-quote/\">Request a free quote</a>.</p>"),
    ]
    faq_html, faq_schema = faq_block(faqs, heading="Box Shop &mdash; Your Questions Answered", bg="bg-beige", extra="logo-row overflow-hidden")
    body = "\n".join([
        _hero(),
        _trust_bar(),
        shop,
        faq_html,
        cta_band("Prefer Us to Pack For You?", "Our trained, fully covered team can pack your whole home with our own materials.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-white"),
        f'<script defer src="/js/box-shop.js?v={E.ASSET_VER}"></script>',
    ])
    doc = E.render_page(
        title="Moving Boxes & Packing Materials | Wolves Removals",
        description="Order strong moving boxes, packing tape, bubble wrap and more from the Wolves Removals box shop. Add to your basket and we'll confirm collection or delivery across Sussex.",
        canonical_path="/box-shop/", body=body, og_image="images/photos/" + HERO.split("/")[-1],
        extra_schema=[faq_schema], breadcrumb=[("Home", "/"), ("Box Shop", "/box-shop/")], active="box-shop")
    E.write("box-shop/index.html", doc)
    print("built box shop")
