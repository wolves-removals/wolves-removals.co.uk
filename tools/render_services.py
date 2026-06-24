# -*- coding: utf-8 -*-
"""Build all /services/ pages from data/services_data.py.
Per-service authored content (lead, what's included, body sections, FAQs) +
shared templated sections (why choose, process, related services, CTA) +
LocalBusiness + Breadcrumb + FAQPage schema. Service URLs match live exactly.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, card_grid, cta_band, faq_block
sys.path.insert(0, os.path.join(E.S.ROOT, "data"))
import services_data as D

HERO_IMG = "images/photos/wolves-van-ready-sussex-removal.webp"

def _name(slug):
    s = next((x for x in D.SERVICES if x["slug"] == slug), None)
    return s["name"] if s else slug.replace("-", " ").title()

def hero(s, photo=None):
    inc = "".join(
        f'<li class="flex items-start gap-2"><span class="text-green mt-1 shrink-0">{icon("check-bold","w-5 h-5")}</span><span>{x}</span></li>'
        for x in s.get("included", []))
    alt = "Wolves Removals " + esc(s["name"]).lower() + " in Sussex"
    src = ("images/photos/" + photo[0] + ".webp") if photo else HERO_IMG
    hero_img = img(src, alt, cls="w-full h-full object-cover", eager=True)
    phone_link = E.S.BUSINESS["phone_link"]
    phone = E.S.BUSINESS["phone"]
    # Google review widget fixed in the bottom corner of the dark hero panel (all services)
    inc_html = f'<ul class="space-y-2 list-none p-0">{inc}</ul>' if inc else ""
    bottom = E.hero_review_row(inc_html)
    return (
        '<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
        f'<div class="absolute inset-0">{hero_img}</div>'
        '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
        f'<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{s["h1"]}</h1>'
        f'<div class="mt-4 text-lg xl:text-xl max-w-2xl">{s["lead"]}</div>'
        f'{bottom}'
        '</div></div></div></section>')

def eeat_block(name, bg, flank=None):
    html = (
        f'<h2 class="relative leading-tight text-black">Trusted {esc(name)} Since 2016</h2>'
        '<p>Wolves Removals is a modern, family-run removals company built on traditional values &mdash; reliability, '
        'responsiveness and keeping our promises. We&rsquo;ve been moving homes and businesses across Sussex, Surrey, '
        'Hampshire and Kent since 2016, and we&rsquo;re proud to be recommended by leading estate agents including '
        'Fine &amp; Country, Justin Lloyd and Mansell McTaggart.</p>'
        '<p>Our accreditations reflect how we work: we are a <strong>LAPADA member</strong> for antiques and fine-art '
        'handling, <strong>Checkatrade-verified</strong>, and <strong>fully insured</strong> on every job. To deliver '
        'consistently high standards we run a modern, fully maintained fleet and a trained, experienced team who treat '
        'your belongings as their own. We also welcome feedback &mdash; listening to our customers is how we keep '
        f'improving. Read our <a href="/reviews/">customer reviews</a> or learn more <a href="/about-us/">about us</a>.</p>')
    if flank:
        return E.photo_flanked_row(html, flank, bg=bg)
    return section(prose(html, span="lg:col-span-10 lg:col-start-2"), bg=bg, extra="logo-row overflow-hidden")

def process_block(name, bg):
    # Unified chevron step-process design; heading + step labels tailored to the page topic.
    return E.step_process(bg=bg, topic=E.process_topic(name))

def storage_size_guide(bg):
    """Size-guide card (contain image + text) for storage pages so visitors can see what
    fits in a standard pod — topic-relevant imagery, shown once per page."""
    text = ('<h2 class="relative leading-tight text-black">How Much Fits In A Storage Pod?</h2>'
            '<p>Our most popular containerised pod measures roughly <strong>5ft &times; 7ft &times; 8.6ft '
            '(1.5m &times; 2.1m &times; 2.6m)</strong> &mdash; room for the contents of a one-bedroom flat: a '
            'sofa or armchair, a fridge-freezer, a wardrobe, a coffee table and a good stack of boxes, as shown '
            'here. Need more space? We simply add another pod, so you only ever pay for what you use.</p>'
            '<p>Not sure how much you&rsquo;ll need? Try our free <a href="/storage-calculator/">storage '
            'calculator</a> to size your space in minutes.</p>')
    return E.content_card(text, variant=1, bg=bg,
                          photo=("storage-pod-size-guide", "Wolves Removals storage pod size guide showing what fits in a 5ft by 7ft by 8.6ft pod"),
                          img_side="right", img_fit="contain")

def why_choose(name, bg):
    rows = [
        ("Fully insured &amp; accredited", "LAPADA member and Checkatrade-verified, with full insurance on every move."),
        ("Trained, experienced team", "Over 100 years' combined experience, handling your belongings with real care."),
        ("Transparent fixed pricing", "Clear written quotes with no hidden extras &mdash; you know the cost up front."),
        ("One point of contact", "A dedicated move coordinator looks after your job from first call to settling in."),
    ]
    cells = "".join(
        f'<div class="col-span-12 md:col-span-6"><div class="group flex gap-3 h-full bg-white rounded-xl border border-border shadow-custom p-6 transition-colors duration-200 hover:bg-darkgrey hover:border-darkgrey">'
        f'<span class="ico-badge shrink-0 w-10 h-10">{icon("check-bold","w-5 h-5")}</span>'
        f'<div><h3 class="text-lg font-semibold text-black group-hover:text-white">{t}</h3><p class="mt-1 text-darkgrey group-hover:text-beige mb-0">{d}</p></div></div></div>'
        for t, d in rows)
    return section(
        f'<div class="text-center mb-8"><h2 class="relative leading-tight text-black">Why Choose Wolves Removals for {esc(name)}?</h2></div>'
        f'<div class="grid grid-cols-12 gap-6">{cells}</div>', bg=bg)

def related(s, bg):
    rel = s.get("related", [])[:6]
    if len(rel) < 3:
        return ""
    cards = []
    for slug in rel:
        rs = next((x for x in D.SERVICES if x["slug"] == slug), None)
        if rs:
            cards.append((rs["name"], f"/services/{slug}/", f"<p>{rs.get('teaser', 'Find out more about this service.')}</p>"))
    return card_grid(cards, cols=3, heading=f"Services Related to {esc(s['name'])}", bg=bg)

# Curated storage imagery so the storage page's photos match its title (relevance rule).
STORAGE_IMAGERY = {
    "intro": ("wolves-van-outside-storage-warehouse-doorway",
              "A Wolves Removals van outside the secure storage warehouse doorway"),
    "panel": ("wolves-operator-forklift-storage-containers",
              "A Wolves Removals operator driving a forklift to load wooden storage containers"),
    "gallery": [
        ("forklift-loading-storage-container-store", "A forklift loading a wooden storage container at the Wolves Removals store"),
        ("loading-storage-container-onto-removal-lorry", "Loading a wooden storage container onto a Wolves Removals lorry"),
        ("forklift-loading-container-into-lorry", "A forklift loading a wooden storage container into a lorry"),
    ],
    # keyed by cream-card index -> (photo, image side)
    "cards": {
        0: (("wolves-van-loading-at-storage-facility",
             "A Wolves Removals van loading at a secure self-storage facility"), "right"),
        1: (("storage-pod-size-guide",
             "Wolves Removals storage pod size guide — what fits in a 5ft x 7ft x 8.6ft pod"), "right", "contain"),
        2: (("wolves-self-storage-containers-field",
             "Wolves Removals self-storage containers for short and long-term storage"), "left"),
    },
    # faded photos for the left+right of an alternating white prose row
    "flank": [
        ("storage-warehouse-aisle-wooden-containers", "An aisle of wooden storage containers inside the Wolves Removals store"),
        ("row-of-mobile-storage-containers", "A row of Wolves Removals mobile storage containers"),
    ],
    # faded fleet/team photos flanking the "Trusted Sussex Removals Since 2016" section
    "eeat_flank": [
        ("wolves-removals-team-fleet-vans", "The Wolves Removals team with their fleet of removal vans"),
        ("wolves-vans-sussex-country-house", "Wolves Removals vans at a grand Sussex country house"),
    ],
}

# Topical photo pools so each topic-specific service shows imagery that matches its title.
_ANTIQUES = [
    ("antiques-room-statues-sea-view", "A grand room of antiques and classical statues with a sea view"),
    ("antique-drawing-room-interior", "An elegant antique-furnished drawing room interior"),
    ("furniture-wrapped-blue-moving-blankets", "Furniture wrapped in blue quilted moving blankets ready for transport"),
    ("period-room-marble-fireplace-antiques", "A period room with a marble fireplace and fine antiques"),
    ("movers-with-fragile-mirror-crate", "Wolves movers positioning a bespoke crate for a large mirror"),
    ("crew-dining-room-antiques", "Wolves crew handling antiques in a grand dining room"),
    ("carrying-gilt-framed-landscape-painting", "A Wolves Removals crew member with a gilt-framed antique landscape painting"),
    ("classical-sculpture-fine-art-removals", "Classical sculptures handled during a fine-art removal"),
    ("antique-relief-sculptures-fine-art", "Antique relief sculptures prepared for careful transport"),
    ("craning-bronze-statue-in-garden", "Craning a bronze statue in a garden for a specialist move"),
    ("crane-lifting-statue-garden", "Craning a garden statue during a specialist antiques removal"),
    ("garden-classical-statues", "Classical garden statues handled by our specialist team"),
    ("formal-garden-statue", "A formal garden statue prepared for a specialist move"),
    ("wrapping-bronze-bust", "Wrapping a bronze bust for protection in transit"),
    ("handling-gilt-framed-antique-painting", "Wolves Removals carefully handling a gilt-framed antique painting"),
    ("carrying-gilt-framed-antique-painting", "A mover carrying a large gilt-framed antique painting"),
    ("handling-framed-old-master", "Carefully handling a framed old-master painting"),
    ("handling-framed-portrait", "Handling a large framed antique portrait"),
    ("hanging-antique-portrait-fine-art", "Hanging an antique portrait during a fine-art move"),
    ("wolves-mover-holding-framed-painting", "A Wolves Removals mover holding a framed antique painting"),
    ("wolves-movers-carrying-framed-mirror", "Wolves Removals movers carrying a large framed mirror through a hallway"),
    ("wrapping-ornate-gilt-framed-mirror", "Wrapping an ornate gilt-framed mirror for protection"),
    ("carrying-wrapped-round-antique-table", "Carrying a wrapped round antique table with care"),
    ("moving-antique-chest", "Moving an antique chest with specialist care"),
    ("wooden-crate-packed-wrapped-antiques", "A wooden crate packed with wrapped antiques"),
    ("large-antique-crate-room", "A large bespoke antique crate in a period room"),
    ("foam-lined-fine-art-crate", "A foam-lined crate built for fine-art transport"),
    ("building-wooden-crate-for-fine-art", "Building a bespoke wooden crate for a fine-art piece"),
    ("building-wooden-export-crate-fine-art", "Building a wooden export crate for fine art"),
    ("carrying-antique-piano-specialist-removals", "Wolves specialists carrying an antique piano with care"),
    ("crane-loading-statue-trailer", "Craning a statue onto a trailer for specialist transport"),
    ("crane-loading-statue-trailer-2", "Loading a large statue with a crane for a specialist move"),
]
_PACKING = [
    ("wrapping-furniture-with-protective-packing", "Wrapping furniture with protective packing materials"),
    ("packing-cardboard-box-home-removals", "Packing a cardboard box during a home removal"),
    ("packing-books-into-moving-boxes", "Packing books neatly into moving boxes"),
    ("movers-taping-cardboard-box-packing", "Movers taping a cardboard box during packing"),
    ("wrapping-armchair-in-living-room", "Wrapping an armchair in protective cover in the living room"),
    ("wrapped-furniture-protective-covers-packing", "Furniture wrapped in protective covers ready to move"),
    ("packing-furniture-boxes-home-removals", "Packing furniture and boxes for a home removal"),
    ("packing-small-item-into-box", "Carefully packing a small item into a box"),
]
_CRATE = [
    ("building-wooden-export-crate-fine-art", "Building a bespoke wooden export crate for fine art"),
    ("large-flat-wooden-export-crate", "A large flat wooden export crate for artwork"),
    ("two-movers-with-front-export-crate", "Two movers with a large export crate"),
    ("wooden-crate-packed-wrapped-antiques", "A wooden crate packed with wrapped antiques"),
    ("loading-wooden-crates-into-van", "Loading wooden crates into the removal van"),
    ("carrying-export-crate-outside-townhouse", "Carrying an export crate outside a townhouse"),
    ("framed-mirror-in-wooden-crate", "A framed mirror secured in a wooden crate"),
    ("building-wooden-crate-for-fine-art", "Building a wooden crate for a fine-art item"),
]
_PIANO = [
    ("carrying-antique-piano-specialist-removals", "Wolves Removals specialists carrying an antique piano"),
    ("two-movers-with-front-export-crate", "Two movers with a large protective crate"),
    ("wrapping-furniture-with-protective-packing", "Wrapping a heavy item with protective packing"),
    ("carrying-wrapped-round-antique-table", "Carrying a wrapped antique table with care"),
    ("large-flat-wooden-export-crate", "A large flat wooden crate for a valuable item"),
    ("building-wooden-export-crate-fine-art", "Building a bespoke crate for a valuable item"),
]
# Storage sub-pages (short/long/business/student) — topical pool led by the new
# containerised-storage + forklift photos, then the existing store/warehouse imagery.
_STORAGE = [
    ("wolves-van-outside-storage-warehouse-doorway", "A Wolves Removals van outside the secure storage warehouse doorway"),
    ("forklift-loading-storage-container-store", "A forklift loading a wooden storage container at the Wolves Removals store"),
    ("wolves-operator-forklift-storage-containers", "A Wolves Removals operator driving a forklift to load wooden storage containers"),
    ("loading-storage-container-onto-removal-lorry", "Loading a wooden storage container onto a Wolves Removals lorry"),
    ("forklift-loading-container-into-lorry", "A forklift loading a wooden storage container into a lorry"),
    ("wolves-van-loading-at-storage-facility", "A Wolves Removals van loading at a secure self-storage facility"),
    ("secure-container-storage-warehouse-interior", "Inside the clean, secure containerised storage warehouse at Wolves Removals"),
    ("wolves-self-storage-containers-field", "Wolves Removals self-storage containers for short and long-term storage"),
    ("storage-warehouse-aisle-wooden-containers", "An aisle of wooden storage containers inside the Wolves Removals store"),
    ("row-of-mobile-storage-containers", "A row of Wolves Removals mobile storage containers"),
    ("forklift-moving-storage-crate-warehouse", "A forklift moving a storage crate in the Wolves Removals store"),
    ("loading-crates-into-storage-container", "Loading wooden crates into a secure Wolves Removals storage container"),
]
SERVICE_PHOTOS = {
    "storage/short-term-storage": _STORAGE,
    "storage/long-term-storage": _STORAGE,
    "storage/business-and-commercial-storage": _STORAGE,
    "student-storage": _STORAGE,
    "piano-moving": _PIANO,
    "specialised-antiques-moving": _ANTIQUES,
    "antiques-in-west-sussex": _ANTIQUES,
    "white-glove-service": _ANTIQUES,
    "custom-crate-service": _CRATE,
    "export-packing-service": _CRATE,
    "full-packing-service": _PACKING,
    "fragile-packing": _PACKING,
    "non-fragile-packing-service": _PACKING,
    "full-unpacking-service": _PACKING,
    "packing-materials": _PACKING,
}

# The fixed antiques gallery — the SAME 20 images shown on every antiques page's carousel.
# Reserved in _used so they never duplicate a hero/intro/panel/body image (R9-dup-img safe).
_ANTIQUES_ALT = dict(_ANTIQUES)
ANTIQUES_GALLERY = [(_fn, _ANTIQUES_ALT[_fn]) for _fn in [
    "antiques-room-statues-sea-view", "furniture-wrapped-blue-moving-blankets", "period-room-marble-fireplace-antiques",
    "movers-with-fragile-mirror-crate", "crew-dining-room-antiques", "wolves-movers-carrying-framed-mirror",
    "carrying-gilt-framed-landscape-painting", "craning-bronze-statue-in-garden", "garden-classical-statues",
    "formal-garden-statue", "wrapping-bronze-bust", "handling-framed-portrait",
    "hanging-antique-portrait-fine-art", "wolves-mover-holding-framed-painting", "carrying-wrapped-round-antique-table",
    "moving-antique-chest", "wooden-crate-packed-wrapped-antiques", "large-antique-crate-room",
    "building-wooden-export-crate-fine-art", "crane-loading-statue-trailer",
]]

# Hand-pinned images for specific spots on specific pages (overrides the auto/themed pick).
# "sections": heading-substring -> (filename, alt, contain) pins a section's media-row image.
# "exclude": antique images kept OFF this page entirely (gallery + auto-picked body rows).
# Both antiques pages pin hero/intro/panel to the same three so none of the gallery 20 collide.
_ANTIQUES_HIP = {
    "hero":  ("antique-drawing-room-interior", "An elegant antique-furnished drawing room interior"),
    "intro": ("classical-sculpture-fine-art-removals", "Classical sculptures handled during a fine-art removal"),
    "panel": ("antique-relief-sculptures-fine-art", "Antique relief sculptures prepared for careful transport"),
}
PAGE_IMG_PINS = {
    # House removals: pin the "Smooth Moving Day" row to a careful-handling photo instead of
    # the off-topic empty-period-room shot.
    "house-removals": {
        "panel": ("wolves-vans-residential-street",
                  "Wolves Removals vans on a residential street during a Sussex house removal"),
        # keep the replaced storage shot from being auto-picked into a body row
        "exclude": ["wolves-self-storage-containers-field"],
        "sections": {
            "From First Phone Call": ("wolves-survey-inventory-clipboard",
                "A Wolves Removals inventory clipboard and pen used during a free home survey and written quote", False),
            "A Smooth Moving Day": ("careful-furniture-handling-house-removal",
                "A Wolves Removals crew member carefully loading boxes on moving day", False),
            "Protecting Your Floors": ("furniture-wrapped-protected-removal",
                "Furniture wrapped in protective covering during a Wolves Removals house move", False),
            "Dismantling, Reassembly": ("handling-large-framed-art",
                "A Wolves Removals mover carefully handling a large framed artwork during a house move", False),
            "Moving With Children Or Pets": ("wolves-removals-office-puppy-desk",
                "The Wolves Removals office puppy sitting on a desk beside the computer", False),
            "Moving Day Hour By Hour": ("wolves-removals-mover-moving-day",
                "A Wolves Removals team member preparing a dining table for protection on moving day", False),
        },
    },
    # Removal services hub: pin the "Survey & Quote" row to the clipboard/survey photo.
    "removal-services": {
        "sections": {
            "The Survey": ("wolves-clipboard-in-storage-warehouse",
                "A Wolves Removals surveyor with a clipboard assessing items for a move quote", False),
            "One Family": ("wolves-removals-team-fleet-vans",
                "The Wolves Removals family team beside their fleet of removal vans", False),
            "Beyond the Standard Move": ("loading-wooden-crate-into-container",
                "A Wolves Removals crew loading a wooden crate into a storage container", False),
        },
    },
    # Commercial: feature panel uses a real team photo (not the Wolves Storage logo).
    "commercial-removals": {
        "panel": ("wolves-van-loading-at-storage-facility",
                  "A Wolves Removals van loading at a secure storage facility during a commercial move"),
        "sections": {
            "A Single Coordinator": ("wolves-move-coordinator-portrait",
                "A Wolves Removals move coordinator who owns your whole commercial relocation", False),
            "Who Our Commercial": ("wolves-crew-setting-up-office",
                "The Wolves Removals crew setting up desks and equipment in a commercial office", False),
            "Out-of-Hours": ("wolves-removals-team-fleet-vans",
                "The Wolves Removals team ready beside their van for an out-of-hours commercial move", False),
            "Desk Crate Systems": ("building-wooden-crate-for-fine-art",
                "A Wolves Removals crew building a bespoke wooden crate around a long item", False),
            "Specialist Crating": ("craning-bronze-horse-statue-garden",
                "A Wolves Removals crane lifting a bronze horse statue in a garden", False),
            "IT, Server": ("specialist-equipment-chamber-office-move",
                "Wolves Removals moving a wrapped specialist pressure chamber out of an office", False),
        },
    },
    # Man and van: feature panel uses the fleet-in-a-field photo (replacing the depot
    # shot), and keep that depot shot off the page so it can't be auto-picked elsewhere.
    "man-and-van": {
        "panel": ("wolves-removals-fleet-vans-field",
                  "The Wolves Removals fleet of vans and Luton lorries lined up in a Sussex field"),
        "exclude": ["removals-van-storage-depot-3"],
        "sections": {
            "Access, Parking": ("removal-lorry-on-residential-street",
                "A Wolves Removals lorry parked on a residential street for a move", False),
            "Single Items": ("wolves-team-loading-van-sussex",
                "The Wolves Removals team loading a van for a man-and-van job in Sussex", False),
            "Clearing a Few Rooms": ("furniture-wrapped-blue-moving-blankets",
                "Furniture wrapped in blue quilted moving blankets ready for a man-and-van move", False),
        },
    },
    "international-removals": {
        "exclude": ["wrapped-furniture-empty-room"],   # freed when the destination row became a timeline
        "sections": {
            "Inventories, Documentation": ("wolves-clipboard-in-storage-warehouse",
                "A Wolves Removals clipboard and inventory in the storage warehouse", False),
        },
    },
    # Export packing: the "Why Move With Wolves Removals?" feature panel uses the new
    # furniture-wrapping photo instead of the default crate-outside-townhouse shot.
    "export-packing-service": {
        "panel": ("wolves-mover-wrapping-dining-furniture",
                  "A Wolves Removals mover wrapping a dining table and chairs in protective padding"),
        "sections": {
            "Export Packing Actually Involves": ("taping-furni-soft-around-furniture",
                "A Wolves Removals packer taping Furni-Soft padding around a furniture item for export", False),
        },
    },
    # Force the new storage warehouse photo into the storage hub's intro media row
    # (the "intro" slot is otherwise bypassed when the intro has 2+ paragraphs).
    "storage": {
        "intro": ("wolves-van-outside-storage-warehouse-doorway",
                  "A Wolves Removals van outside the secure storage warehouse doorway"),
    },
    "antiques-in-west-sussex": {
        **_ANTIQUES_HIP,
        "sections": {
            "LAPADA Membership": ("lapada-approved-service-provider", "LAPADA approved service provider, Association of Art & Antiques Dealers", True),
            "Handling Clocks":   ("wrapping-ornate-gilt-framed-mirror", "Wrapping an ornate gilt-framed mirror for protection", False),
        },
        "exclude": [
            "crane-lifting-statue-garden", "handling-gilt-framed-antique-painting",
            "carrying-gilt-framed-antique-painting", "building-wooden-crate-for-fine-art",
            "handling-framed-old-master", "crane-loading-statue-trailer-2",
            "carrying-antique-piano-specialist-removals",
        ],
    },
    "piano-moving": {
        "panel": ("carrying-antique-piano-specialist-removals",
                  "Wolves Removals specialists carrying an antique piano during a careful move"),
    },
    "custom-crate-service": {
        "panel": ("wheeling-export-crate-on-trolley",
                  "A Wolves Removals export crate being wheeled out on a trolley"),
        "sections": {
            "Pieces a Crate Is Built For": ("loading-wooden-crate-into-container",
                "A Wolves Removals crew loading a wooden crate into a storage container", False),
        },
    },
    "contract-delivery-services": {
        "sections": {
            "White-Goods Delivery": ("wrapped-furniture-and-labelled-boxes",
                "A room of wrapped furniture and labelled boxes packed ready for delivery", False),
            "How a Contract Delivery": ("wolves-removals-vans-at-depot",
                "Two Wolves Removals vans parked outside the depot at Kings House", False),
        },
    },
    "white-glove-service": {
        "panel": ("wolves-crew-handling-large-framed-art",
                  "Wolves Removals crew in white gloves handling a large framed artwork"),
        "exclude": ["careful-packing-sussex-home-removal"],   # freed when the concierge row became a timeline
        "sections": {
            "What a White-Glove Move": ("lapada-approved-service-provider",
                "LAPADA approved service provider, Association of Art &amp; Antiques Dealers", True),
            "Handling, Crating": ("wolves-crew-carrying-wrapped-furniture",
                "Wolves Removals crew in white gloves carrying an item wrapped in protective padding", False),
        },
    },
    "specialised-antiques-moving": {
        **_ANTIQUES_HIP,
        "exclude": ["careful-packing-sussex-home-removal", "carrying-antique-piano-specialist-removals"],
        "sections": {
            "Trusted by Collectors": ("antique-marble-top-gilt-commode",
                "An antique Louis XVI marble-topped gilt-mounted commode in a gallery", False),
            "Handling Each Type of Antique": ("antique-marble-draped-statue",
                "An antique marble statue of a draped female figure on a marble pedestal", False),
        },
    },
}

def _ri(inner):   # line-art icon for a risk-methodology step (tan disc supplies the dark colour)
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" class="w-7 h-7 lg:w-8 lg:h-8">' + inner + '</svg>')

# The 5-stage risk-assessment methodology shown as a vertical icon timeline on the
# commercial page (replaces the old flat infographic image).
RISK_STEPS = [
    (_ri('<circle cx="10.5" cy="10.5" r="6.5"/><path d="M20.5 20.5l-5-5"/>'),
     "Risk Identification", "Survey properties for access hazards"),
    (_ri('<path d="M12 3.5v16M5.5 19.5h13"/><path d="M12 6l6.5 1.8M12 6 5.5 7.8"/><path d="M5.5 7.8 3 13a2.7 2.7 0 0 0 5 0L5.5 7.8zM18.5 7.8 16 13a2.7 2.7 0 0 0 5 0l-2.5-5.2z"/>'),
     "Risk Analysis", "Evaluate lifting weights and transit times"),
    (_ri('<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9.5 4a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v1h-5V4z"/><path d="M8.7 12.3l1.8 1.8 3.8-3.8"/>'),
     "Risk Evaluation", "Compare against manual handling guidelines"),
    (_ri('<path d="M4 20h16"/><rect x="5" y="12" width="3.4" height="6" rx="0.6"/><rect x="10.3" y="8.5" width="3.4" height="9.5" rx="0.6"/><rect x="15.6" y="5" width="3.4" height="13" rx="0.6"/>'),
     "Risk Prioritisation", "Rank risks by potential damage to goods"),
    (_ri('<path d="M12 3l7 2.4v5.4c0 4.4-3 7.3-7 8.4-4-1.1-7-4-7-8.4V5.4L12 3z"/><path d="M9 12l2 2 4-4"/>'),
     "Risk Treatment", "Avoid, minimise, transfer or accept"),
]

# Destination-end journey for the international page (same vertical timeline component,
# wording tuned to the "Destination Delivery, Unpacking & Storage" paragraph).
INTL_STEPS = [
    (_ri('<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.4 3.9 5.4 3.9 8.5s-1.5 6.1-3.9 8.5c-2.4-2.4-3.9-5.4-3.9-8.5s1.5-6.1 3.9-8.5z"/>'),
     "Customs Clearance", "Cleared through customs at destination"),
    (_ri('<rect x="2.5" y="6.5" width="11" height="9" rx="1"/><path d="M13.5 9.5h4l3 3v3h-7z"/><circle cx="6.5" cy="17.3" r="1.7"/><circle cx="17.3" cy="17.3" r="1.7"/>'),
     "Delivery To Your Door", "Destination agents deliver to your address"),
    (_ri('<path d="M4 10.5V8.5A2.5 2.5 0 0 1 6.5 6h11A2.5 2.5 0 0 1 20 8.5v2"/><path d="M3.5 10.5h17a1 1 0 0 1 1 1V16H2.5v-4.5a1 1 0 0 1 1-1z"/><path d="M5 16v2M19 16v2"/>'),
     "Unloading &amp; Placement", "Furniture set in the rooms you choose"),
    (_ri('<path d="M3.5 8.5l3-4.5h11l3 4.5"/><path d="M3.5 8.5v9.5a1 1 0 0 0 1 1h15a1 1 0 0 0 1-1V8.5"/><path d="M3.5 8.5h17M12 4v4.5"/>'),
     "Unpacking &amp; Cartons", "Boxes unpacked and packaging removed"),
]

# The white-glove "concierge process" shown as the same vertical timeline, worded for the
# premium fully-managed service (mirrors the five stages listed in that section).
WHITEGLOVE_STEPS = [
    (_ri('<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9.5 4a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v1h-5V4z"/><path d="M8.7 10.5l1.3 1.3 2.3-2.3M8.7 15l1.3 1.3 2.3-2.3"/>'),
     "Survey &amp; Plan", "Pre-move survey, inventory and room-by-room plan"),
    (_ri('<path d="M3 7.5l9-4.5 9 4.5v9l-9 4.5-9-4.5v-9z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>'),
     "Full Packing", "Every room packed in premium materials"),
    (_ri('<path d="M12 3l7 2.4v5.4c0 4.4-3 7.3-7 8.4-4-1.1-7-4-7-8.4V5.4L12 3z"/><path d="M9 12l2 2 4-4"/>'),
     "Bespoke Protection", "Custom crates for the most delicate valuables"),
    (_ri('<rect x="2.5" y="6.5" width="11" height="9" rx="1"/><path d="M13.5 9.5h4l3 3v3h-7z"/><circle cx="6.5" cy="17.3" r="1.7"/><circle cx="17.3" cy="17.3" r="1.7"/>'),
     "Secure Transport", "Careful loading, transit and unloading"),
    (_ri('<path d="M3.5 8.5l3-4.5h11l3 4.5"/><path d="M3.5 8.5v9.5a1 1 0 0 0 1 1h15a1 1 0 0 0 1-1V8.5"/><path d="M3.5 8.5h17M12 4v4.5"/>'),
     "Unpack &amp; Place", "Unpacked, positioned and packaging removed"),
]

def build_service(s):
    faqs = s["faqs"]
    _i = {"n": 0}
    def nb():
        b = "bg-white" if _i["n"] % 2 == 0 else "bg-beige"
        _i["n"] += 1
        return b
    # Blueprint applied to every service: cream prose rows become rotating cards (some
    # with a topical photo), white prose rows alternate faded logo / faded side-photos.
    # Storage keeps its hand-curated imagery; other services use their page_photos pool.
    is_storage = (s["slug"] == "storage")
    _cv = {"n": 0}
    _wr = {"n": 0}
    themed = SERVICE_PHOTOS.get(s["slug"])
    pool = themed if themed else E.page_photos(s["slug"], 12)
    def card_media(i):
        if is_storage:
            return STORAGE_IMAGERY["cards"].get(i)
        if i % 2 == 0 and pool:
            return (pool[i % len(pool)], "left" if (i // 2) % 2 == 1 else "right")
        return None
    def flank_pair(w):
        if is_storage:
            return STORAGE_IMAGERY["flank"]
        j = (2 * w) % len(pool)
        return [pool[j], pool[(j + 1) % len(pool)]]
    def prose_row(inner):
        bg = nb()
        if is_storage:   # storage keeps its hand-curated card/flank imagery (bespoke page)
            if bg == "bg-beige":
                n = _cv["n"]; v = (n % 3) + 1; _cv["n"] += 1
                media = card_media(n)
                if media:
                    return E.content_card(inner, variant=v, bg=bg, photo=media[0], img_side=media[1],
                                          img_fit=(media[2] if len(media) > 2 else "cover"))
                return E.content_card(inner, variant=v, bg=bg)
            if bg == "bg-white":
                w = _wr["n"]; _wr["n"] += 1
                if w % 2 == 1:
                    return E.photo_flanked_row(inner, flank_pair(w), bg=bg)
                return section(prose(inner, span="lg:col-span-10 lg:col-start-2"), bg=bg,
                               extra="logo-row overflow-hidden")
            return section(prose(inner, span="lg:col-span-10 lg:col-start-2"), bg=bg, extra="logo-row overflow-hidden")
        # Every other service: a real, topic-matched image beside every prose row.
        side = "left" if _wr["n"] % 2 == 1 else "right"; _wr["n"] += 1
        _rp = next((v for k, v in _sections.items() if k in inner), None)  # heading-substring pin
        photo = (_rp[0], _rp[1]) if _rp else E._row_photo(s["slug"], inner, _used, _wr["n"])
        _contain = bool(_rp and len(_rp) > 2 and _rp[2])   # pinned diagrams/infographics: don't crop
        if bg == "bg-beige":
            v = (_cv["n"] % 3) + 1; _cv["n"] += 1
            return E.content_card(inner, variant=v, bg=bg, photo=photo, img_side=side,
                                  img_fit=("contain" if _contain else "cover"))
        return E._split_row(inner, photo, reverse=(side == "left"), bg=bg, contain=_contain)
    pics = list(themed) if themed else E.page_photos(s["slug"], 6)
    if len(pics) < 6:
        pics = (pics + E.page_photos(s["slug"], 6))[:6]
    intro_pic = STORAGE_IMAGERY["intro"] if is_storage else pics[1]
    panel_pic = STORAGE_IMAGERY["panel"] if is_storage else pics[5]
    gallery_pics = STORAGE_IMAGERY["gallery"] if is_storage else pics[2:5]
    hero_photo = next((p for p in E.PHOTOS if p[0] == s["hero"]), pics[0]) if s.get("hero") else pics[0]
    _pins = PAGE_IMG_PINS.get(s["slug"], {})
    if "hero" in _pins: hero_photo = _pins["hero"]
    if "intro" in _pins: intro_pic = _pins["intro"]
    if "panel" in _pins: panel_pic = _pins["panel"]
    _intro_force = _pins.get("intro")
    _sections = _pins.get("sections", {})
    _exclude = set(_pins.get("exclude", []))
    _used = {p[0] for p in [hero_photo, intro_pic, panel_pic] + list(gallery_pics)}  # split rows avoid these + each other
    if _intro_force: _used.add(_intro_force[0])
    _used |= {v[0] for v in _sections.values()}   # reserve pinned section images
    _used |= _exclude                              # keep excluded images out of auto-picks
    if "antique" in s["slug"]:                     # reserve the fixed gallery so body rows never reuse it
        _used |= {g[0] for g in ANTIQUES_GALLERY}
    parts = [hero(s, hero_photo),
             E.quote_bar(lead=f"Need {s['name']}?", rest="Get a Free Quote",
                         subtext="Tell us about your move for a fast, fixed price — no obligation.")]
    for idx, (h2, html) in enumerate(s.get("sections", [])):
        inner = f'<h2 class="relative leading-tight text-black">{h2}</h2>{html}'
        if idx == 0:  # row 1: light intro (image/video + text); row 2: slate feature panel
            if s.get("intro_video"):    # ambient muted video beside the intro text
                parts.append(E.text_with_video(inner, s["intro_video"], reverse=False, bg=nb()))
            elif html.count("<p") >= 2:   # site rule: 2+ paragraphs -> split into media rows
                parts.append(E.media_rows(inner, f"{s['slug']}-intro", nb, used=_used, force=_intro_force))
            else:
                parts.append(E.text_with_image(inner, intro_pic, reverse=False, bg=nb()))
            parts.append(E.wolves_feature_panel(panel_pic, reverse=False, bg=nb(), name=s["name"]))
            if s.get("video"):
                _vids = [s["video"]] if isinstance(s["video"], str) else s["video"]
                for _vi, _vid in enumerate(_vids):
                    parts.append(E.video_embed(_vid, bg=nb(), aside=(s.get("video_writeup") if _vi == 0 else None)))
        elif html.count("<p") >= 2:     # site rule: 2+ paragraphs -> split into media rows
            _sp = next((v for k, v in _sections.items() if k in h2), None)   # heading-substring pin
            _f = (_sp[0], _sp[1]) if _sp else None
            _fc = bool(_sp and len(_sp) > 2 and _sp[2])
            parts.append(E.media_rows(inner, f"{s['slug']}-sec{idx}", nb, used=_used, force=_f, force_contain=_fc))
        else:
            parts.append(prose_row(inner))
    _exp = E.load_expansion("services", s["slug"])
    for _ei, (_h2, _html) in enumerate(_exp["sections"]):
        _inner = f'<h2 class="relative leading-tight text-black">{esc(_h2)}</h2>{_html}'
        if s["slug"] == "commercial-removals" and "Health, Safety" in _h2:   # vertical risk-method timeline
            parts.append(E.methodology_timeline(RISK_STEPS,
                "Wolves Removals Risk Assessment Methodology", "Sussex UK Professional Removals",
                _inner, bg=nb(), reverse=True))
            continue
        if s["slug"] == "international-removals" and "Destination Delivery" in _h2:   # destination-journey timeline
            parts.append(E.methodology_timeline(INTL_STEPS,
                "Wolves Removals Destination Handover", "Door-to-Door Worldwide Moves",
                _inner, bg=nb(), reverse=True))
            continue
        if s["slug"] == "white-glove-service" and "Concierge Process" in _h2:   # white-glove concierge timeline
            parts.append(E.methodology_timeline(WHITEGLOVE_STEPS,
                "Wolves Removals White-Glove Service", "Concierge-Level Care, Sussex",
                _inner, bg=nb(), reverse=True))
            continue
        _sp = next((v for k, v in _sections.items() if k in _h2), None)   # heading-substring pin
        _f = (_sp[0], _sp[1]) if _sp else None
        _fc = bool(_sp and len(_sp) > 2 and _sp[2])
        if _html.count("<p") >= 2:
            parts.append(E.media_rows(_inner, f"{s['slug']}-exp{_ei}", nb, used=_used, force=_f, force_contain=_fc))
        else:
            parts.append(prose_row(_inner))
    if _exp["faqs"]:
        faqs = list(faqs) + [tuple(x) for x in _exp["faqs"]]
    parts.append(eeat_block(s["name"], nb(), flank=E.eeat_flank(s["slug"], _used)))
    if "antique" in s["slug"]:
        # Both antiques pages show the SAME fixed gallery of 20 (reserved in _used above so
        # they never duplicate a hero/intro/panel/body image on either page).
        parts.append(E.photo_gallery(ANTIQUES_GALLERY, heading="Antiques &amp; Fine Art We Move Across Sussex",
            intro="A closer look at the paintings, sculptures, statues, mirrors and period pieces our specialist team crates, wraps and transports with care.", bg=nb()))
    else:
        parts.append(E.photo_strip(gallery_pics, heading=f"{s['name']} with Wolves Removals",
                                   intro="Our trained, fully insured team handling moves across Sussex and beyond.", bg=nb()))
    # Storage sub-pages get the pod size-guide (the main /services/storage/ already has it via its card).
    if s["slug"] != "storage" and (s["slug"].startswith("storage") or s["slug"] == "student-storage"):
        parts.append(storage_size_guide(nb()))
    parts.append(process_block(s["name"], nb()))
    if s["slug"].startswith("storage"):
        parts.append(E.storage_cta(seed=s["slug"]))
    parts.append(why_choose(s["name"], bg=nb()))
    rel = related(s, bg=nb()) if len([x for x in s.get("related", []) if any(y["slug"] == x for y in D.SERVICES)]) >= 3 else ""
    if rel:
        parts.append(rel)
    parts.append(cta_band(f"Get a Free {s['name']} Quote",
                          "Fill in our quick form, call us or email us and a friendly member of the team will be in touch.",
                          "Get a Free Quote", "/get-a-quote/", bg=nb()))
    parts.append(faq_block(faqs, heading=f"{s['name']} &mdash; Your Questions Answered", bg=nb())[0])
    faq_schema = faq_block(faqs, heading="x")[1]
    body = "\n".join(p for p in parts if p)
    slug = s["slug"]
    doc = E.render_page(
        title=s["title"], description=s["meta"], canonical_path=f"/services/{slug}/",
        body=body, og_image="images/photos/" + hero_photo[0] + ".webp",
        breadcrumb=[("Home", "/"), ("Services", "/services/"), (s["name"], f"/services/{slug}/")],
        extra_schema=[faq_schema], active="services", show_quote=False)
    return E.write(f"services/{slug}/index.html", doc)

def _svc(slug):
    return next((x for x in D.SERVICES if x["slug"] == slug), None)

# Themed groups → (heading, intro, photo filename, photo alt, [service slugs])
HUB_CATEGORIES = [
    ("Home &amp; Business Removals",
     "Fully managed moves for homes and businesses of every size, planned and led by a dedicated coordinator from your first call to settling in.",
     "professional-movers-carrying-furniture-sussex",
     "Wolves Removals movers carrying furniture on a Sussex house move",
     ["house-removals", "commercial-removals", "man-and-van", "removal-services", "house-clearance", "contract-delivery-services"]),
    ("Long-Distance, European &amp; International",
     "Moving further afield? We handle UK-wide, European and worldwide relocations door to door, with expert export packing and customs guidance.",
     "removal-van-loaded-sussex-move",
     "A Wolves Removals van loaded and ready for a long-distance move",
     ["european-removals", "international-removals", "export-packing-service", "student-removals"]),
    ("Specialist &amp; Antique Moving",
     "As a LAPADA member we move antiques, fine art, pianos and other high-value pieces with bespoke handling, crating and white-glove care.",
     "wolves-movers-handling-wardrobe",
     "Wolves Removals movers carefully handling a valuable item with care",
     ["specialised-antiques-moving", "antiques-in-west-sussex", "white-glove-service", "piano-moving", "custom-crate-service"]),
    ("Packing &amp; Materials",
     "Let our trained packers take the strain, or pick up quality materials to pack yourself &mdash; with fragile items always handled with extra care.",
     "professionally-packed-moving-boxes-ready",
     "Professionally packed moving boxes ready for a Sussex house move",
     ["full-packing-service", "full-unpacking-service", "fragile-packing", "non-fragile-packing-service", "packing-materials"]),
    ("Secure Storage",
     "Clean, dry, containerised storage for whenever your dates don&rsquo;t line up &mdash; from a few days to long term, for households and businesses alike.",
     "removal-team-carrying-moving-boxes",
     "Wolves Removals team carrying boxes into secure containerised storage",
     ["storage", "storage/short-term-storage", "storage/long-term-storage", "storage/business-and-commercial-storage", "student-storage"]),
]

def _category_block(cat, reverse, bg):
    heading, intro, fn, alt, slugs = cat
    lis = ""
    for sl in slugs:
        s = _svc(sl)
        if not s:
            continue
        lis += (f'<li><a href="/services/{sl}/" class="font-semibold">{esc(s["name"])}</a> '
                f'<span class="text-darkgrey">&mdash; {esc(s.get("teaser", ""))}</span></li>')
    inner = (
        f'<h2 class="relative leading-tight text-black">{heading}</h2>'
        f'<p class="text-lg">{intro}</p>'
        f'<ul class="tick-list mt-2">{lis}</ul>')
    return E.text_with_image(inner, (fn, alt), reverse=reverse, bg=bg)

def build_hub():
    intro = (
        '<h2 class="relative leading-tight text-black">Our Removal &amp; Storage Services</h2>'
        '<p>Wolves Removals offers a complete range of professional, fully insured moving services across Sussex, '
        'Surrey, Hampshire and Kent &mdash; from <a href="/services/house-removals/">house removals</a> and '
        '<a href="/services/commercial-removals/">office moves</a> to '
        '<a href="/services/international-removals/">international relocations</a>, specialist '
        '<a href="/services/piano-moving/">piano</a> and <a href="/services/specialised-antiques-moving/">antique</a> '
        'handling, expert <a href="/services/full-packing-service/">packing</a> and secure '
        '<a href="/services/storage/">storage</a>. Family-run since 2016 and accredited by LAPADA and Checkatrade, we '
        'tailor every move to you. Explore each service below, or <a href="/get-a-quote/">request a free quote</a> to get started.</p>')
    cat_blocks = [
        _category_block(c, reverse=(i % 2 == 1), bg=("bg-lightgrey" if i % 2 == 0 else "bg-white"))
        for i, c in enumerate(HUB_CATEGORIES)
    ]
    strip = E.photo_strip(E.page_photos("services-hub-gallery", 5)[:3],
                          heading="Your Move, in Safe Hands",
                          intro="Our trained, fully insured Sussex team handling recent home, business and specialist moves.",
                          bg="bg-white")
    faqs = [
        ("What removal and storage services do Wolves Removals offer?",
         "<p>We handle home and commercial removals, international and European moves, full and part packing, specialist piano and antiques handling, and secure containerised storage &mdash; everything you need for your move under one roof.</p>"),
        ("Do you offer a free quote for your services?",
         "<p>Yes &mdash; every service comes with a free, no-obligation quote. We offer free in-home and video surveys so we can give you a clear, fixed written price with no hidden extras. <a href=\"/get-a-quote/\">Request your free quote</a> to get started.</p>"),
        ("Are Wolves Removals fully insured and accredited?",
         "<p>We&rsquo;re fully covered for goods in transit and public liability, and we&rsquo;re accredited by LAPADA and verified on Checkatrade, so your belongings are protected at every stage of the move.</p>"),
        ("Which areas do your services cover?",
         "<p>We&rsquo;re based in Pulborough, West Sussex and cover the whole of Sussex, Surrey, Hampshire and Kent, plus UK-wide and European moves. See the <a href=\"/locations/\">areas we cover</a>.</p>"),
        ("Can I combine several services in one move?",
         "<p>Absolutely &mdash; most moves combine packing, removals and storage. Tell us what you need and we&rsquo;ll tailor a single, joined-up plan and one clear quote. <a href=\"/contact-us/\">Get in touch</a> to discuss your move.</p>"),
    ]
    body = "\n".join([
        hero({"name": "Our Services", "h1": "Removal & Storage Services in Sussex",
              "lead": "<p>Everything you need for a smooth move &mdash; packing, removals, storage, delivery and specialist handling, all under one roof.</p>",
              "included": ["Fully insured, accredited and family-run since 2016",
                           "Home, commercial, international and specialist moves",
                           "Expert packing and secure containerised storage"]}),
        E.quote_bar(lead="Get a Free", rest="Removals Quote",
                    subtext="Compare our full range of Sussex removal and storage services."),
        E.media_rows(intro, "services-hub-intro", "bg-white", used=set()),
        *cat_blocks,
        strip,
        eeat_block("Sussex Removals &amp; Storage", "bg-lightgrey", flank=E.eeat_flank("services-hub")),
        process_block("Our Services", "bg-white"),
        faq_block(faqs, heading="Removal &amp; Storage Services &mdash; Your Questions Answered", bg="bg-lightgrey")[0],
        cta_band("Not Sure Which Service You Need?",
                 "Tell us about your move and we&rsquo;ll recommend the right option and send a free quote.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-white"),
    ])
    doc = E.render_page(
        title="Removal & Storage Services | Wolves Removals — Sussex",
        description="Professional removal & storage services from Wolves Removals: house & commercial moves, international, packing, antiques, piano moving and secure storage across Sussex.",
        canonical_path="/services/", body=body, og_image=HERO_IMG,
        extra_schema=[faq_block(faqs, heading="x")[1]],
        breadcrumb=[("Home", "/"), ("Services", "/services/")], active="services")
    return E.write("services/index.html", doc)

def build():
    build_hub()
    for s in D.SERVICES:
        build_service(s)
    print(f"built {len(D.SERVICES)} service pages + hub")

if __name__ == "__main__":
    build()
