# -*- coding: utf-8 -*-
"""Build the interactive /storage-calculator/ page.
Self-contained vanilla-JS calculator: pick item quantities -> total volume (cu ft)
-> recommended storage size. No external libs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, cta_band, faq_block

HERO = "images/photos/wolves-van-secure-storage-facility.webp"

import json as _json, re as _re, html as _h
_ITEMS = _json.load(open(os.path.join(E.S.ROOT, "data", "storage_items.json"), encoding="utf-8"))

def _slug(s):
    return _re.sub(r"[^a-z0-9]+", "-", _h.unescape(str(s)).lower()).strip("-")

DURATIONS = [
    ("1-2", "1&ndash;2 months", "Short-term"),
    ("3-5", "3&ndash;5 months", "Flexible term"),
    ("6-11", "6&ndash;11 months", "Longer stay"),
    ("12+", "12+ months", "Best value"),
]

def _step_head(n, title, sub=""):
    return ('<div class="scalc-step-head">'
            f'<span class="scalc-step-badge">{n}</span>'
            f'<div class="scalc-step-text"><h3 class="scalc-step-title">{title}</h3>'
            + (f'<p class="scalc-step-sub">{sub}</p>' if sub else '')
            + '</div></div>')

def _block(head, content, show=""):
    attr = f' data-show-modes="{show}"' if show else ""
    return f'<div class="scalc-block"{attr}>{head}{content}</div>'

# Non-stackable items: max units that fit in one pod (floor space, can't be stacked).
# The storage calculator sizes these to their pod footprint (250 / N) rather than raw cube.
PERPOD = {"Motorbike": 2, "Sofa, 3-seater": 3}

def _item_picker():
    """Shared room-by-room item picker (search + tabs + panels) used by both the
    storage calculator and the removals & storage calculator."""
    tabs, panels = [], []
    for ci, (room, items) in enumerate(_ITEMS):
        rslug = _slug(room)
        pid = "scalc-panel-" + rslug
        sel = "true" if ci == 0 else "false"
        act = " is-active" if ci == 0 else ""
        hid = "" if ci == 0 else " hidden"
        tabs.append(
            f'<button type="button" role="tab" class="scalc-tab{act}" data-target="{pid}" aria-selected="{sel}">{room}</button>')
        rows = []
        for name, cuft, cum in items:
            nm = esc(name)
            plain = _h.unescape(str(name))
            dname = esc(plain.lower())
            iid = "scalc-" + rslug + "-" + _slug(name)
            pp = PERPOD.get(plain)
            vol = f'{cuft} cu ft' + (f' &middot; {pp}/pod max' if pp else '')
            pp_attr = f'data-perpod="{pp}" ' if pp else ''
            rows.append(
                f'<div class="scalc-item" data-name="{dname}">'
                f'<div class="scalc-item-info"><span class="scalc-item-name">{nm}</span>'
                f'<span class="scalc-item-vol">{vol}</span></div>'
                '<div class="scalc-stepper">'
                f'<button type="button" class="scalc-step" data-action="dec" aria-label="Remove one {nm}">&minus;</button>'
                f'<input id="{iid}" type="number" min="0" value="0" inputmode="numeric" '
                f'data-cuft="{cuft}" data-cum="{cum}" {pp_attr}data-room="{room}" data-label="{nm}" '
                f'aria-label="Quantity of {nm}">'
                f'<button type="button" class="scalc-step" data-action="inc" aria-label="Add one {nm}">+</button>'
                '</div></div>')
        panels.append(
            f'<div id="{pid}" class="scalc-panel" role="tabpanel"{hid}>'
            f'<div class="scalc-items">{"".join(rows)}</div></div>')
    return (
        '<div class="scalc-search"><input id="scalc-search" type="search" placeholder="Search all items&hellip;" aria-label="Search items"></div>'
        f'<div class="scalc-tabs" role="tablist" aria-label="Rooms">{"".join(tabs)}</div>'
        f'<div class="scalc-panels">{"".join(panels)}</div>')

# Typical removal volumes (cu ft) by home size — Mark Ratcliffe pricing-tier figures.
PROPERTY_SIZES = [("tiny", "Tiny", 300), ("1bed", "1-bed", 500), ("2bed", "2-bed", 800),
                  ("3bed", "3-bed", 1000), ("4bed", "4-bed", 1800), ("5bed", "5+ bed", 2800)]

# --- Auto-inventory (like Mark Ratcliffe): picking a home size fills the item picker
# with a typical inventory the customer can then adjust. Presets reference (room, name)
# pairs from storage_items.json and resolve to the live input IDs. ---
_ITEM_ID = {}
for _r, _its in _ITEMS:
    for _n, _cf, _cm in _its:
        _ITEM_ID[(_r, _h.unescape(str(_n)))] = "scalc-" + _slug(_r) + "-" + _slug(_n)

_TV = 'TV, large (50"+)'
PRESETS = {
  "tiny": [
    ("Bedroom (master)", "Bed, double (mattress only)", 1), ("Bedroom (master)", "Bed, double (base only)", 1),
    ("Bedroom (master)", "Wardrobe, single", 1), ("Bedroom (master)", "Bedside table", 1),
    ("Living room", "Sofa, 2-seater", 1), ("Living room", "Armchair", 1), ("Living room", "Coffee table", 1),
    ("Living room", _TV, 1),
    ("Kitchen / utility", "Fridge-freezer, tall", 1), ("Kitchen / utility", "Washing machine", 1),
    ("Boxes & cartons", "Standard removals box (medium)", 10), ("Boxes & cartons", "Book box (1.5 cu ft)", 4),
  ],
  "1bed": [
    ("Bedroom (master)", "Bed, double (mattress only)", 1), ("Bedroom (master)", "Bed, double (base only)", 1),
    ("Bedroom (master)", "Wardrobe, double", 1), ("Bedroom (master)", "Chest of drawers, large", 1),
    ("Bedroom (master)", "Bedside table", 1),
    ("Living room", "Sofa, 2-seater", 1), ("Living room", "Armchair", 1), ("Living room", "Coffee table", 1),
    ("Living room", _TV, 1), ("Living room", "TV unit / stand", 1), ("Living room", "Bookcase, small", 1),
    ("Dining room", "Dining table, 4-seater", 1), ("Dining room", "Dining chair", 2),
    ("Kitchen / utility", "Fridge-freezer, tall", 1), ("Kitchen / utility", "Washing machine", 1),
    ("Kitchen / utility", "Microwave", 1),
    ("Boxes & cartons", "Standard removals box (medium)", 15), ("Boxes & cartons", "Book box (1.5 cu ft)", 6),
  ],
  "2bed": [
    ("Bedroom (master)", "Bed, double (mattress only)", 1), ("Bedroom (master)", "Bed, double (base only)", 1),
    ("Bedroom (master)", "Wardrobe, double", 1), ("Bedroom (master)", "Chest of drawers, large", 1),
    ("Bedroom (master)", "Bedside table", 2),
    ("Kids bedroom", "Bed, single (mattress only)", 1), ("Kids bedroom", "Bed, single (base only)", 1),
    ("Kids bedroom", "Junior wardrobe", 1), ("Kids bedroom", "Chest of drawers, kids", 1),
    ("Living room", "Sofa, 3-seater", 1), ("Living room", "Armchair", 1), ("Living room", "Coffee table", 1),
    ("Living room", _TV, 1), ("Living room", "TV unit / stand", 1), ("Living room", "Bookcase, large", 1),
    ("Living room", "Sideboard", 1),
    ("Dining room", "Dining table, 6-seater", 1), ("Dining room", "Dining chair", 4),
    ("Kitchen / utility", "Fridge-freezer, tall", 1), ("Kitchen / utility", "Washing machine", 1),
    ("Kitchen / utility", "Cooker, freestanding", 1), ("Kitchen / utility", "Dishwasher", 1),
    ("Kitchen / utility", "Microwave", 1),
    ("Boxes & cartons", "Standard removals box (medium)", 32), ("Boxes & cartons", "Book box (1.5 cu ft)", 8),
    ("Boxes & cartons", "Wardrobe carton (tall)", 2),
  ],
  "3bed": [
    ("Bedroom (master)", "Bed, king (mattress only)", 1), ("Bedroom (master)", "Bed, king (base only)", 1),
    ("Bedroom (master)", "Bed, double (mattress only)", 1), ("Bedroom (master)", "Bed, double (base only)", 1),
    ("Kids bedroom", "Bed, single (mattress only)", 1), ("Kids bedroom", "Bed, single (base only)", 1),
    ("Bedroom (master)", "Wardrobe, double", 2), ("Kids bedroom", "Junior wardrobe", 1),
    ("Bedroom (master)", "Chest of drawers, large", 2), ("Kids bedroom", "Chest of drawers, kids", 1),
    ("Bedroom (master)", "Bedside table", 3), ("Bedroom (master)", "Dressing table", 1),
    ("Living room", "Sofa, 3-seater", 1), ("Living room", "Sofa, 2-seater", 1), ("Living room", "Armchair", 1),
    ("Living room", "Coffee table", 1), ("Living room", _TV, 1), ("Living room", "TV unit / stand", 1),
    ("Living room", "Bookcase, large", 1), ("Living room", "Sideboard", 1),
    ("Dining room", "Dining table, 6-seater", 1), ("Dining room", "Dining chair", 6),
    ("Kitchen / utility", "Fridge-freezer, American", 1), ("Kitchen / utility", "Washing machine", 1),
    ("Kitchen / utility", "Tumble dryer", 1), ("Kitchen / utility", "Cooker, freestanding", 1),
    ("Kitchen / utility", "Dishwasher", 1), ("Kitchen / utility", "Microwave", 1),
    ("Office / study", "Desk", 1), ("Office / study", "Office chair", 1),
    ("Boxes & cartons", "Standard removals box (medium)", 45), ("Boxes & cartons", "Book box (1.5 cu ft)", 12),
    ("Boxes & cartons", "Wardrobe carton (tall)", 3), ("Boxes & cartons", "Linen box (large)", 2),
  ],
  "4bed": [
    ("Bedroom (master)", "Bed, king (mattress only)", 1), ("Bedroom (master)", "Bed, king (base only)", 1),
    ("Bedroom (master)", "Bed, double (mattress only)", 2), ("Bedroom (master)", "Bed, double (base only)", 2),
    ("Kids bedroom", "Bed, single (mattress only)", 1), ("Kids bedroom", "Bed, single (base only)", 1),
    ("Bedroom (master)", "Wardrobe, double", 3), ("Kids bedroom", "Junior wardrobe", 1),
    ("Bedroom (master)", "Chest of drawers, large", 3), ("Kids bedroom", "Chest of drawers, kids", 1),
    ("Bedroom (master)", "Bedside table", 4), ("Bedroom (master)", "Dressing table", 1),
    ("Living room", "Sofa, 3-seater", 1), ("Living room", "Sofa, 2-seater", 1), ("Living room", "Armchair", 2),
    ("Living room", "Coffee table", 1), ("Living room", _TV, 1), ("Living room", "TV unit / stand", 1),
    ("Living room", "Bookcase, large", 2), ("Living room", "Sideboard", 1),
    ("Dining room", "Dining table, 6-seater", 1), ("Dining room", "Dining chair", 6),
    ("Kitchen / utility", "Fridge-freezer, American", 1), ("Kitchen / utility", "Washing machine", 1),
    ("Kitchen / utility", "Tumble dryer", 1), ("Kitchen / utility", "Cooker, freestanding", 1),
    ("Kitchen / utility", "Dishwasher", 1), ("Kitchen / utility", "Microwave", 1),
    ("Office / study", "Desk", 1), ("Office / study", "Office chair", 1), ("Office / study", "Bookcase, office", 1),
    ("Garage / shed", "Lawnmower, push", 1), ("Garage / shed", "Bicycle", 2),
    ("Boxes & cartons", "Standard removals box (medium)", 60), ("Boxes & cartons", "Book box (1.5 cu ft)", 16),
    ("Boxes & cartons", "Wardrobe carton (tall)", 4), ("Boxes & cartons", "Linen box (large)", 3),
  ],
  "5bed": [
    ("Bedroom (master)", "Bed, king (mattress only)", 2), ("Bedroom (master)", "Bed, king (base only)", 2),
    ("Bedroom (master)", "Bed, double (mattress only)", 2), ("Bedroom (master)", "Bed, double (base only)", 2),
    ("Kids bedroom", "Bed, single (mattress only)", 2), ("Kids bedroom", "Bed, single (base only)", 2),
    ("Bedroom (master)", "Wardrobe, double", 4), ("Kids bedroom", "Junior wardrobe", 2),
    ("Bedroom (master)", "Chest of drawers, large", 4), ("Kids bedroom", "Chest of drawers, kids", 1),
    ("Bedroom (master)", "Bedside table", 6), ("Bedroom (master)", "Dressing table", 2),
    ("Living room", "Sofa, 3-seater", 2), ("Living room", "Sofa, 2-seater", 1), ("Living room", "Armchair", 2),
    ("Living room", "Coffee table", 2), ("Living room", _TV, 2), ("Living room", "TV unit / stand", 1),
    ("Living room", "Bookcase, large", 2), ("Living room", "Sideboard", 1),
    ("Dining room", "Dining table, 8-seater", 1), ("Dining room", "Dining chair", 8),
    ("Kitchen / utility", "Fridge-freezer, American", 1), ("Kitchen / utility", "Washing machine", 1),
    ("Kitchen / utility", "Tumble dryer", 1), ("Kitchen / utility", "Cooker, freestanding", 1),
    ("Kitchen / utility", "Dishwasher", 1), ("Kitchen / utility", "Microwave", 1),
    ("Office / study", "Desk", 2), ("Office / study", "Office chair", 2), ("Office / study", "Bookcase, office", 2),
    ("Garage / shed", "Lawnmower, push", 1), ("Garage / shed", "Bicycle", 3), ("Garage / shed", "Workbench", 1),
    ("Boxes & cartons", "Standard removals box (medium)", 80), ("Boxes & cartons", "Book box (1.5 cu ft)", 20),
    ("Boxes & cartons", "Wardrobe carton (tall)", 6), ("Boxes & cartons", "Linen box (large)", 4),
  ],
}

def _preset_attr(key):
    d = {}
    for room, name, qty in PRESETS.get(key, []):
        kk = (room, name)
        if kk in _ITEM_ID:
            d[_ITEM_ID[kk]] = qty
        else:
            print("WARN: preset item not found:", room, "/", name, file=sys.stderr)
    return _json.dumps(d, separators=(",", ":")).replace('"', "&quot;")

def calculator_widget():
    # --- Step 1: what are you storing? (the item inventory, feeds the pod count) ---
    step1 = _block(
        _step_head(1, "What are you storing?",
                   "Add the items you plan to store and we&rsquo;ll work out the volume and how many pods you need &mdash; or skip this and just set the number of pods below."),
        '<div class="scalc-pickerwrap">' + _item_picker() + '</div>'
        '<p id="scalc-pods-from-items"></p>')

    # --- Step 2: how many storage pods? (auto-filled from your items, adjustable) ---
    step2 = _block(
        _step_head(2, "How many storage pods do you need?",
                   "Set above by your items, or choose directly &mdash; each pod holds about 250 cu ft (7 cu m), roughly a van load."),
        '<div class="scalc-pods-pick">'
        '<button type="button" class="scalc-pods-btn" data-pods-dec aria-label="Fewer pods">&minus;</button>'
        '<div class="scalc-pods-val"><span class="scalc-pods-num" id="scalc-pods-num">1</span>'
        '<span class="scalc-pods-lab">storage pods</span></div>'
        '<button type="button" class="scalc-pods-btn" data-pods-inc aria-label="More pods">+</button>'
        '</div>'
        '<p class="scalc-pods-rate" id="scalc-pods-rate"></p>')

    # --- Step 3: how long — a rough term (for those without a move-out date) or exact dates ---
    _terms = [("1 week", 7), ("2 weeks", 14), ("1 month", 30), ("3 months", 91), ("6 months", 182), ("1 year", 365)]
    term_btns = "".join(
        f'<button type="button" class="scalc-dur" data-days="{d}" aria-pressed="false">{lbl}</button>'
        for lbl, d in _terms)
    step3 = _block(
        _step_head(3, "How long do you need storage?",
                   "Storage is flexible, with no long tie-ins. Pick a rough length and we&rsquo;ll fill the dates from today &mdash; tweak them, set your own, or choose ongoing if you&rsquo;re not sure."),
        '<div class="scalc-sub-lab">Roughly how long?</div>'
        f'<div class="scalc-dur-grid">{term_btns}</div>'
        '<button type="button" class="scalc-dur scalc-dur--ongoing" data-ongoing aria-pressed="false">I&rsquo;m not sure yet &mdash; flexible, ongoing storage</button>'
        '<div id="scalc-dates-wrap" class="scalc-durexact">'
        '<div class="scalc-field-row">'
        '<div class="scalc-field"><label for="scalc-from-date" class="scalc-lab">Storage start date</label>'
        '<input id="scalc-from-date" type="date" class="scalc-input"></div>'
        '<div class="scalc-field"><label for="scalc-to-date" class="scalc-lab">Storage end date</label>'
        '<input id="scalc-to-date" type="date" class="scalc-input"></div>'
        '</div></div>'
        '<p class="scalc-note" id="scalc-dates-note">Pick a rough length above, or enter your own dates.</p>')

    # --- Step 4: contents cover ---
    step4 = _block(
        _step_head(4, "Contents cover",
                   "Your belongings are kept in clean, dry, secure storage pods and covered to a standard level."),
        '<label class="scalc-check"><input type="checkbox" id="scalc-cover">'
        '<span class="scalc-check-text"><strong>Ask about optional extended cover</strong>'
        'Tick this and we&rsquo;ll include extended cover options with your free, no-obligation quote.</span></label>')

    left = ('<div class="col-span-12 lg:col-span-8 scalc-steps">'
            + step1 + step2 + step3 + step4 + '</div>')

    # --- Sticky summary ---
    summary = (
        '<div class="scalc-results-card">'
        '<h3 class="scalc-results-h">Your storage summary</h3>'
        '<div class="scalc-totals">'
        '<div class="scalc-total"><span class="scalc-total-num" id="scalc-tile-pods">1</span><span class="scalc-total-unit">pods</span></div>'
        '<div class="scalc-total"><span class="scalc-total-num" id="scalc-tile-days">0</span><span class="scalc-total-unit">days</span></div>'
        '<div class="scalc-total"><span class="scalc-total-num" id="scalc-tile-cuft">0</span><span class="scalc-total-unit">cu ft</span></div>'
        '</div>'
        '<div class="scalc-rec" id="scalc-rec"><strong>1 storage pod</strong><span class="scalc-rec-sub">each holds ~250 cu ft / 7 cu m</span></div>'
        '<div class="mt-4 mb-1 text-center">'
        '<div class="text-xs font-semibold text-darkgrey uppercase tracking-wide">Estimated storage cost</div>'
        '<div class="text-4xl font-bold text-[#dad6c2] leading-tight" id="scalc-storage-price">&mdash;</div>'
        '<div class="text-xs text-darkgrey"><span id="scalc-cost-lead">for the period</span> &middot; inc VAT &middot; <span id="scalc-storage-daily">&mdash;</span> per pod/day</div></div>'
        '<div class="scalc-sum">'
        '<div class="scalc-sum-row"><span>From</span><span id="scalc-sum-from" class="scalc-sum-val">&mdash;</span></div>'
        '<div class="scalc-sum-row"><span>To</span><span id="scalc-sum-to" class="scalc-sum-val">&mdash;</span></div>'
        '<div class="scalc-sum-row"><span>Duration</span><span id="scalc-sum-days" class="scalc-sum-val">&mdash;</span></div>'
        '<div class="scalc-sum-row"><span>Contents cover</span><span id="scalc-sum-cover" class="scalc-sum-val">Standard</span></div>'
        '</div>'
        '<div class="scalc-pricetable">'
        '<div class="scalc-pt-head">Storage prices by term</div>'
        '<div class="scalc-pt-row"><span>Weekly</span><span class="scalc-pt-val" data-pt-days="7" data-pt-unit="/wk">&mdash;</span></div>'
        '<div class="scalc-pt-row"><span>Paid monthly</span><span class="scalc-pt-val" data-pt-days="30.44" data-pt-unit="/mo">&mdash;</span></div>'
        '<div class="scalc-pt-row"><span>3 months pre-payment</span><span class="scalc-pt-val" data-pt-days="91">&mdash;</span></div>'
        '<div class="scalc-pt-row"><span>6 months pre-payment</span><span class="scalc-pt-val" data-pt-days="182">&mdash;</span></div>'
        '<div class="scalc-pt-row"><span>12 months pre-payment</span><span class="scalc-pt-val" data-pt-days="365">&mdash;</span></div>'
        '</div>'
        '<div class="scalc-sum" id="scalc-vol-wrap" hidden>'
        '<div class="scalc-sum-row"><span>Estimated volume</span><span id="scalc-sum-vol" class="scalc-sum-val">&mdash;</span></div>'
        '</div>'
        '<div class="scalc-inv-wrap" id="scalc-inv-wrap" hidden><div class="scalc-inv-head">Your list</div>'
        '<div id="scalc-inventory" class="scalc-inv"></div></div>'
        '<a href="/get-a-quote/" id="scalc-quote" class="button-orange w-full text-center">Get a free storage quote</a>'
        '<button type="button" id="scalc-reset" class="scalc-reset">Reset calculator</button>'
        '</div>')
    right = f'<div class="col-span-12 lg:col-span-4 lg:self-stretch">{summary}</div>'

    return section(
        '<div id="storage-calc" data-scalc data-calc data-mode="storage" class="scalc-shell">'
        '<div class="scalc grid grid-cols-12 gap-6 lg:gap-8 items-start">'
        + left + right +
        '</div></div>'
        f'<script defer src="/js/storage-calculator.js?v={E.ASSET_VER}"></script>',
        bg="bg-white")

def calc_widget_moving():
    """Removals & Storage calculator modelled on Mark Ratcliffe: a 3-way mode selector
    (Removals / Storage / Removals & Storage) drives an itemised cost breakdown. Removals
    uses MRM's volume + mileage figures (VAT shown, added at booking); storage is pods at
    a tiered £2.50 to £2.071/pod/day. Self-contained — served by /js/calc.js."""
    _tk = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6.5h10.5v9H3z"/><path d="M13.5 9.5H18l3 3v3h-7.5z"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17.5" cy="17.5" r="1.6"/></svg>'
    _stsvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10l9-5 9 5"/><path d="M5 10v9h14v-9"/><path d="M9.5 19v-4.5h5V19"/></svg>'
    _bxsvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5l8 4v9l-8 4-8-4v-9z"/><path d="M4 7.5l8 4 8-4"/><path d="M12 11.5V20"/></svg>'
    _modes = [("removals", "Removals only", "Move your items to a new home.", _tk),
              ("storage", "Storage only", "Store your items securely with us.", _stsvg),
              ("both", "Removals &amp; storage", "A move plus secure storage.", _bxsvg)]
    modebar = _block(
        _step_head(1, "What are you calculating?", "Choose what you&rsquo;d like us to price up."),
        '<div class="scalc-modebar" role="radiogroup" aria-label="What are you calculating?">' + "".join(
            f'<label class="scalc-mode"><input type="radio" name="calc-mode" value="{v}"{" checked" if v == "both" else ""}>'
            f'<span class="scalc-mode-card"><span class="scalc-mode-ico">{ico}</span>'
            f'<span class="scalc-mode-txt"><strong>{t}</strong><small>{d}</small></span></span></label>'
            for v, t, d, ico in _modes) + '</div>')
    _bed = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a2 2 0 012-2h14a2 2 0 012 2v6"/><path d="M3 14h18"/><path d="M3 18v1.5M21 18v1.5"/><rect x="6" y="7.6" width="5" height="3.4" rx="1"/></svg>'
    _ranges = {"tiny": "150&ndash;300", "1bed": "300&ndash;500", "2bed": "800&ndash;1,400",
               "3bed": "1,000&ndash;1,500", "4bed": "1,800&ndash;2,400", "5bed": "2,800&ndash;4,000+"}
    prop_cards = "".join(
        f'<button type="button" class="scalc-opt scalc-opt--home" data-prop="{k}" data-vol="{vol}" data-preset="{_preset_attr(k)}" data-range="{_ranges.get(k, "")}" data-label="{lbl}" aria-pressed="false">'
        f'<span class="scalc-opt-ico">{_bed}</span><span class="scalc-opt-main">{lbl}</span></button>'
        for k, lbl, vol in PROPERTY_SIZES)
    step2 = _block(
        _step_head(2, "How big is the home?",
                   "Pick the closest match &mdash; it sets a typical cubic-ft figure you can fine-tune."),
        f'<div class="scalc-opt-grid scalc-opt-grid--6">{prop_cards}</div>')
    cuft_sub = (
        '<div class="scalc-sub"><div class="scalc-sub-lab">Adjust cubic ft</div>'
        '<input id="scalc-cuft-input" type="number" min="0" inputmode="numeric" aria-label="Adjust cubic ft" class="scalc-cuft-input" value="0">'
        '<p class="scalc-hint" id="scalc-cuft-hint">Set by your home size or the inventory above &mdash; this is the volume your estimate uses, and you can edit it here.</p>'
        '</div>')
    dist_sub = (
        '<div class="scalc-sub"><div class="scalc-sub-lab">Round-trip distance</div>'
        '<div class="scalc-addr"><span class="scalc-addr-head">Moving from</span>'
        '<div class="scalc-field-row">'
        '<div class="scalc-field"><label for="scalc-from-num" class="scalc-lab">House number or name</label>'
        '<input id="scalc-from-num" type="text" class="scalc-input" placeholder="e.g. 47 or Rose Cottage"></div>'
        '<div class="scalc-field"><label for="scalc-from-pc" class="scalc-lab">Postcode or full address</label>'
        '<input id="scalc-from-pc" type="text" class="scalc-input" placeholder="e.g. BN21 3AB" autocomplete="postal-code"></div></div></div>'
        '<div class="scalc-addr"><span class="scalc-addr-head">Moving to</span>'
        '<div class="scalc-field-row">'
        '<div class="scalc-field"><label for="scalc-to-num" class="scalc-lab">House number or name</label>'
        '<input id="scalc-to-num" type="text" class="scalc-input" placeholder="e.g. 12 or The Old Vicarage"></div>'
        '<div class="scalc-field"><label for="scalc-to-pc" class="scalc-lab">Postcode or full address</label>'
        '<input id="scalc-to-pc" type="text" class="scalc-input" placeholder="e.g. TN22 5JD"></div></div></div>'
        '<div class="scalc-dist-actions">'
        '<button type="button" id="scalc-calc-dist" class="scalc-btn-primary">Calculate distance &rarr;</button>'
        '<span id="scalc-dist-status" class="scalc-dist-status"></span></div>'
        '<button type="button" id="scalc-adjust-manual" class="scalc-adjust" aria-expanded="false">Adjust manually <span aria-hidden="true">+</span></button>'
        '<div id="scalc-manual-wrap" class="scalc-manual-wrap" hidden>'
        '<div class="scalc-field"><label for="scalc-miles" class="scalc-lab">Round-trip distance (miles)</label>'
        '<input id="scalc-miles" type="number" min="0" inputmode="numeric" class="scalc-input" placeholder="e.g. 30"></div></div>'
        '</div>')
    step3 = _block(
        _step_head(3, "Move distance", "Add your move distance for the mileage estimate."),
        dist_sub, show="removals both")
    _durs = [("1 week", 7), ("2 weeks", 14), ("1 month", 30), ("3 months", 91), ("6 months", 182), ("1 year", 365)]
    dur_btns = "".join(
        f'<button type="button" class="scalc-dur" data-days="{d}" aria-pressed="false">{lbl}</button>'
        for lbl, d in _durs)
    days_panel = _block(
        _step_head(4, "How long do you need storage?",
                   "Pick a rough term or type the exact days &mdash; storage runs from &pound;2.50 down to &pound;2.071 per pod per day as you add pods."),
        f'<div class="scalc-dur-grid">{dur_btns}</div>'
        '<div class="scalc-sub"><div class="scalc-sub-lab">Days of storage</div>'
        '<input id="scalc-days" type="number" min="0" inputmode="numeric" aria-label="Days of storage" class="scalc-cuft-input" value="28">'
        '<p class="scalc-hint">7 days = 1 week &middot; 30 = a month &middot; 365 = a year. Each pod holds ~250 cu ft (7 cu m).</p></div>',
        show="storage both")
    inv_panel = _block(
        _step_head(5, "Inventory (optional)",
                   "Auto-fill a typical loadout for your home size, or tick items yourself for a precise volume."),
        '<div class="scalc-invbar">'
        '<label class="scalc-switch"><input type="checkbox" id="scalc-inv-toggle"><span class="scalc-switch-track"></span></label>'
        '<div class="scalc-invbar-txt"><strong id="scalc-inv-toggle-label">Use our typical inventory list?</strong>'
        '<small>Auto-fills a standard loadout for your home size &mdash; adjust quantities after.</small></div>'
        '<button type="button" id="scalc-tick-manual" class="scalc-btn-ghost">Or tick items manually &rarr;</button>'
        '</div>'
        '<div id="scalc-picker" class="scalc-pickerwrap" hidden>' + _item_picker() + '</div>')
    cuft_block = _block(
        _step_head(6, "Adjust the volume",
                   "This is the figure your estimate uses &mdash; set above by your home size or items, and editable here."),
        cuft_sub)
    est = (
        '<div class="scalc-estimate">'
        '<div class="scalc-est-head">Your estimate (+ VAT at booking)</div>'
        '<div class="scalc-estbox">'
        '<div class="scalc-estrow" data-show-modes="removals both"><span>Removals</span><strong id="scalc-split-rem">&pound;0.00</strong></div>'
        '<div class="scalc-estrow" data-show-modes="storage both"><span id="scalc-split-sto-label">Storage</span><strong id="scalc-split-sto">&pound;0.00</strong></div>'
        '</div>'
        '<p class="scalc-est-vol">Total volume: <strong id="scalc-cuft">0</strong> cu ft &middot; <strong id="scalc-cum">0.00</strong> cu m &middot; <strong id="scalc-count">0</strong> items</p>'
        '<div class="scalc-sum">'
        '<div class="scalc-sum-row" data-show-modes="removals both"><span>Vehicle</span><span id="scalc-c-vehicle" class="scalc-sum-val">&mdash;</span></div>'
        '<div class="scalc-sum-row" data-show-modes="removals both"><span>Volume cost</span><span id="scalc-c-volume" class="scalc-sum-val">&pound;0.00</span></div>'
        '<div class="scalc-sum-row" data-show-modes="removals both"><span>Mileage</span><span id="scalc-c-mileage" class="scalc-sum-val">&pound;0.00</span></div>'
        '<div class="scalc-sum-row" data-show-modes="removals both"><span>Removals nett</span><span id="scalc-c-nett" class="scalc-sum-val">&pound;0.00</span></div>'
        '<div class="scalc-sum-row" data-show-modes="removals both"><span>VAT (20%)</span><span id="scalc-c-vat" class="scalc-sum-val">&pound;0.00</span></div>'
        '<div class="scalc-sum-row scalc-sum-row--total" data-show-modes="removals both"><span>Removals subtotal</span><span id="scalc-c-total" class="scalc-sum-val">&pound;0.00</span></div>'
        '<div class="scalc-sum-row" data-show-modes="storage both"><span>Storage pods</span><span id="scalc-s-pods" class="scalc-sum-val">&mdash;</span></div>'
        '<div class="scalc-sum-row" data-show-modes="storage both"><span>Daily rate</span><span id="scalc-s-daily" class="scalc-sum-val">&pound;0.00</span></div>'
        '<div class="scalc-sum-row scalc-sum-row--total" data-show-modes="storage both"><span>Storage subtotal</span><span id="scalc-s-total" class="scalc-sum-val">&pound;0.00</span></div>'
        '</div>'
        '<div class="scalc-roomreq" data-show-modes="storage both">Storage required: <strong id="scalc-s-podsreq">&mdash;</strong></div>'
        '<div class="scalc-inv-wrap"><div class="scalc-inv-head">Your list</div>'
        '<div id="scalc-inventory" class="scalc-inv"><p class="scalc-inv-empty">No items selected yet.</p></div></div>'
        '<form id="scalc-quote-form" class="scalc-quoteform" novalidate>'
        '<div class="scalc-sub-lab">Get this estimate by email</div>'
        '<div class="scalc-field-row">'
        '<div class="scalc-field"><label for="scalc-q-name" class="scalc-lab">Your name</label>'
        '<input id="scalc-q-name" name="name" type="text" class="scalc-input" required aria-required="true"></div>'
        '<div class="scalc-field"><label for="scalc-q-email" class="scalc-lab">Email</label>'
        '<input id="scalc-q-email" name="email" type="email" class="scalc-input" required aria-required="true"></div></div>'
        '<div class="scalc-field-row">'
        '<div class="scalc-field"><label for="scalc-q-phone" class="scalc-lab">Phone</label>'
        '<input id="scalc-q-phone" name="phone" type="tel" class="scalc-input"></div>'
        '<div class="scalc-field"><label for="scalc-q-date" class="scalc-lab">Preferred date (optional)</label>'
        '<input id="scalc-q-date" name="date" type="date" class="scalc-input"></div></div>'
        '<div hidden aria-hidden="true"><label>Leave blank<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>'
        '<button type="submit" id="scalc-quote" class="scalc-quote-btn">Send these figures for a quote &rarr;</button>'
        '<p id="scalc-quote-msg" class="scalc-quote-msg" role="status" aria-live="polite"></p>'
        '</form>'
        '<button type="button" id="scalc-reset" class="scalc-reset">Reset calculator</button>'
        '<p class="scalc-note">Estimate only &mdash; the exact quote depends on access, stairs, packing materials, antiques handling and timing. We&rsquo;ll confirm with a free, no-obligation survey.</p>'
        '</div>')
    body = modebar + step2 + step3 + days_panel + inv_panel + cuft_block + est
    return section(
        '<div id="calc" data-calc data-calc-mode="both" class="scalc-shell">' + body + '</div>'
        f'<script defer src="/js/calc.js?v={E.ASSET_VER}"></script>',
        bg="bg-white")

def build_removals():
    intro = ('<h2 class="relative leading-tight text-black">Estimate Your Move in Minutes</h2>'
             '<p>Use our free <a href="/services/house-removals/">removals</a> and storage calculator to size your move. '
             'Pick your home size for an instant estimate, or add your items room by room for accuracy &mdash; we&rsquo;ll '
             'recommend the right <strong>van and crew</strong>, and how many secure <a href="/services/storage/">storage '
             'pods</a> you&rsquo;d need if you&rsquo;re storing too. It&rsquo;s a guide &mdash; we confirm your exact '
             'vehicle, crew and price with a quick free survey.</p>')
    how = ('<h2 class="relative leading-tight text-black">From a Quick Estimate to a Fixed Price</h2>'
           '<p>The calculator gives you a realistic starting point &mdash; total volume, the recommended vehicle and crew, '
           'plus storage if you need it. For a guaranteed price we offer a free, no-obligation '
           '<a href="/get-a-quote/">video or in-home survey</a>, where we confirm access, parking and any '
           '<a href="/services/specialised-antiques-moving/">specialist items</a> like pianos or antiques. Just storing? '
           'Use our dedicated <a href="/storage-calculator/">storage calculator</a> instead.</p>')
    faqs = [("How accurate is the calculator?", "<p>It&rsquo;s a solid guide based on typical item volumes. For a guaranteed price we recommend a free video or in-home survey.</p>"),
            ("What does the van &amp; crew recommendation mean?", "<p>From your total volume we suggest the right vehicle (from a Luton van up to a lorry) and crew size. We&rsquo;ll confirm the exact setup on your survey.</p>"),
            ("Can I add storage?", "<p>Yes &mdash; choose &lsquo;Need storage too?&rsquo; and we&rsquo;ll show how many secure <a href=\"/services/storage/\">storage pods</a> you&rsquo;d need.</p>"),
            ("Do you move pianos and antiques?", "<p>Yes &mdash; we&rsquo;re LAPADA antiques specialists. Add them to your list and mention them on your quote so we bring the right kit.</p>")]
    faq_html, faq_schema = faq_block(faqs, heading="Removals & Storage Calculator — FAQs", bg="bg-white")
    HERO2 = "images/photos/wolves-crew-busy-sussex-moving-day.webp"
    hero_img = img(HERO2, "Wolves Removals crew on a Sussex moving day", cls="w-full h-full object-cover", eager=True)
    hero = ('<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
            f'<div class="absolute inset-0">{hero_img}</div>'
            '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
            '<h1 class="text-3xl lg:text-5xl font-bold leading-tight">Removals &amp; Storage Calculator</h1>'
            '<div class="mt-4 text-lg xl:text-xl max-w-3xl"><p>Get an instant estimate of your move &mdash; volume, the right van and crew, and storage if you need it.</p></div>'
            f'{E.hero_review_row()}'
            '</div></div></div></section>')
    styler = E.make_prose_styler("removals-calculator", photos=[])
    body = "\n".join([
        hero,
        E.quote_bar(lead="Worked Out Your Move?", rest="Get a Free Quote",
                    subtext="Get a free, no-obligation removals or storage quote from our Sussex team."),
        styler(intro, "bg-white"),
        calc_widget_moving(),
        styler(how, "bg-beige"),
        faq_html,
        cta_band("Ready for a Fixed Price?", "Get a free, no-obligation quote from our friendly, fully covered Sussex team.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
    ])
    doc = E.render_page(title="Removals & Storage Calculator | Wolves Removals Sussex",
        description="Free removals & storage calculator from Wolves Removals — estimate your move volume, the right van and crew, and storage pods across Sussex. Get a free quote.",
        canonical_path="/removals-calculator/", body=body, og_image=HERO2,
        breadcrumb=[("Home", "/"), ("Removals & Storage Calculator", "/removals-calculator/")], extra_schema=[faq_schema], active="")
    E.write("removals-calculator/index.html", doc)
    print("built removals-calculator")

def build():
    intro = ('<h2 class="relative leading-tight text-black">Estimate the Storage You Need</h2>'
             '<p>Not sure how much <a href="/services/storage/">storage</a> you need? Use our free calculator to size it '
             'up in a few clicks. Tell us how many secure storage pods you want &mdash; or build a quick inventory and '
             'we&rsquo;ll work it out for you, as each pod holds roughly 250 cubic feet (7 cubic metres). Then pick your '
             'storage start and end dates and we&rsquo;ll calculate the length of storage and your total cost. It&rsquo;s '
             'a guide only &mdash; we&rsquo;ll confirm your exact price with a quick free survey.</p>')
    how = ('<h2 class="relative leading-tight text-black">How Our Storage Works</h2>'
           '<p>At Wolves Removals your belongings are professionally packed and sealed into clean, dry, ultra-secure '
           'storage pods &mdash; each holding roughly 250 cubic feet (7 cubic metres) and not left loose on open shelving. Choose '
           '<a href="/services/storage/short-term-storage/">short-term storage</a> for moving delays and renovations, '
           '<a href="/services/storage/long-term-storage/">long-term storage</a> for extended needs, or '
           '<a href="/services/storage/business-and-commercial-storage/">business storage</a> for stock and equipment. '
           'We can collect, store and redeliver as part of your <a href="/services/house-removals/">move</a>.</p>')
    faqs = [("How accurate is the storage calculator?", "<p>It gives a helpful guide based on typical item volumes. For an exact figure we recommend a free video or in-home survey.</p>"),
            ("How is my furniture stored?", "<p>Professionally packed and sealed into clean, dry, secure storage pods &mdash; each holding around 250 cu ft (7 cu m) and protected from damp and damage throughout.</p>"),
            ("Can I store for just a short time?", "<p>Yes &mdash; our <a href=\"/services/storage/short-term-storage/\">short-term storage</a> starts from just a couple of days.</p>"),
            ("Do you collect and deliver?", "<p>Yes &mdash; we can collect, store and redeliver your belongings as part of your move.</p>")]
    faq_html, faq_schema = faq_block(faqs, heading="Storage Calculator — FAQs", bg="bg-white")
    hero_img = img(HERO, "A Wolves Removals van outside the secure storage facility in Sussex", cls="w-full h-full object-cover", eager=True)

    van_inner = (
        '<h2 class="relative leading-tight text-black">Collected, Stored and Returned</h2>'
        '<p>Our liveried Wolves Removals Luton van handles the heavy lifting for you. We collect your belongings, '
        'transport them to our secure Sussex storage facility and load them into clean, dry <strong>storage pods</strong> '
        '&mdash; each holding roughly 250 cubic feet (7 cubic metres). When you&rsquo;re ready, we redeliver everything as '
        'part of your <a href="/services/house-removals/">house move</a>.</p>'
        '<p>It&rsquo;s the same trusted team for <a href="/services/full-packing-service/">packing</a>, '
        '<a href="/services/storage/short-term-storage/">short-term storage</a>, '
        '<a href="/services/storage/long-term-storage/">long-term storage</a> and '
        '<a href="/services/storage/business-and-commercial-storage/">business storage</a> &mdash; '
        'fully covered from your door to our store and back again.</p>')
    van_section = E.text_with_image(
        van_inner,
        ("wolves-luton-storage-packing-van",
         "The Wolves Removals Luton van for removals, storage and packing in Sussex"),
        reverse=True, bg="bg-white")
    hero = ('<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
            f'<div class="absolute inset-0">{hero_img}</div>'
            '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
            '<h1 class="text-3xl lg:text-5xl font-bold leading-tight">Storage Calculator</h1>'
            '<div class="mt-4 text-lg xl:text-xl max-w-3xl"><p>Estimate how much secure storage you need in just a few clicks.</p></div>'
            f'{E.hero_review_row()}'
            '</div></div></div></section>')
    styler = E.make_prose_styler("storage-calculator", photos=[])
    body = "\n".join([
        hero,
        E.quote_bar(lead="Need Storage or Removals?", rest="Get a Free Quote",
                    subtext="Worked out your space? Get a free, no-obligation quote."),
        styler(intro, "bg-white"),
        calculator_widget(),
        van_section,
        styler(how, "bg-beige"),
        faq_html,
        cta_band("Need Secure Storage?", "Get a free, no-obligation storage quote from our Sussex team.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
    ])
    doc = E.render_page(title="Storage Calculator | Wolves Removals — Estimate Your Storage",
        description="Free Wolves Removals storage calculator — size your storage in secure pods, set your dates and get an instant cost across Sussex.",
        canonical_path="/storage-calculator/", body=body, og_image=HERO,
        breadcrumb=[("Home", "/"), ("Storage Calculator", "/storage-calculator/")], extra_schema=[faq_schema], active="")
    E.write("storage-calculator/index.html", doc)
    print("built storage-calculator")
    build_removals()

if __name__ == "__main__":
    build()
