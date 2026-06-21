#!/usr/bin/env python3
"""Render all NSR pages from a single content data source.
Run from site root:  python3 tools/render-pages.py
Re-runnable & idempotent. Holds nav/footer/schema/SEO scaffolding in one place
so individual pages only carry their unique copy."""

from __future__ import annotations
import json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://www.northstaffordshireremovals.co.uk'
CSS_V = '20260525g'

# ─── Shared boilerplate ────────────────────────────────────────────────

CSP = ("default-src 'self' https:; "
       "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "img-src 'self' data: https:; "
       "font-src 'self' https://fonts.gstatic.com data:; "
       "frame-src https://www.google.com https://www.openstreetmap.org; "
       "connect-src 'self' https://www.google-analytics.com; "
       "object-src 'none'; base-uri 'self'; form-action 'self' https://formspree.io")

def head(*, title, desc, canonical, og_image='family-celebrating-keys-new-home.jpg',
         extra_schema='', preload_img=None, depth=0):
    """Render <head>. depth = 0 for root, 1 for subfolder pages (services/, blog/, etc.)"""
    prefix = '../' * depth
    css = f'{prefix}css/site.css?v={CSS_V}'
    pre = preload_img or og_image
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="North Staffordshire Removals &amp; Storage Ltd">
  <meta name="theme-color" content="#ef6c1d">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="North Staffordshire Removals &amp; Storage Ltd">
  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="{BASE}/images/{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{BASE}/images/{og_image}">
  <link rel="preload" as="image" href="{prefix}images/{pre}" fetchpriority="high">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css}">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%2311365a'/%3E%3Cpath d='M16 30 L32 18 L48 30 L48 48 L16 48 Z' fill='none' stroke='%23ef6c1d' stroke-width='3' stroke-linejoin='round'/%3E%3Crect x='26' y='34' width='8' height='8' fill='%23ef6c1d'/%3E%3Crect x='34' y='30' width='7' height='12' fill='%23ef6c1d'/%3E%3C/svg%3E">
{extra_schema}
</head>'''


def topbar(depth=0):
    """Disabled — the standalone topbar was removed because every item
    it carried (phone, email, hours, quote CTA) already lives in
    higher-affordance UI: the pulsing phone FAB, the email FAB, the
    main-nav Free-Quote pill, the footer, and the LocalBusiness
    schema's openingHours. Kept as a no-op so existing callers don't
    break — delete the function only when no generator imports it."""
    return ''


# ─── Related-reading blog cards ────────────────────────────────
# Per-blog metadata used by the .related-section block on every
# content page. Card descriptions are intentionally short and
# punchy (~25-30 words), NOT the same as the blog's meta-description
# — they need to tease the article in 2 lines max.

BLOG_META = {
    'cost-of-moving-house-stoke-on-trent-2026': {
        'title': 'Cost of moving house in Stoke-on-Trent (2026)',
        'card_desc': "Realistic 2026 pricing across Staffordshire — what a 2-bed flat, 3-bed semi and 4-bed family move actually cost, and what swings the figure.",
        'img': 'family-moving-house-boxes-celebration.jpg',
        'alt': 'Staffordshire family celebrating moving day surrounded by removal boxes',
        'href': 'blog/cost-of-moving-house-stoke-on-trent-2026.html',
        'cta': 'See 2026 pricing',
    },
    'choosing-a-reliable-removal-company-stoke': {
        'title': 'Choosing a reliable removal company in Stoke',
        'card_desc': "Five questions worth asking any remover before you book — insurance, sub-contracting, fixed-price quotes and the warning signs we'd avoid ourselves.",
        'img': 'professional-removal-team-lorry.jpg',
        'alt': 'Professional Stoke-on-Trent removal crew loading a branded Luton lorry',
        'href': 'blog/choosing-a-reliable-removal-company-stoke.html',
        'cta': 'Check the questions',
    },
    'hidden-costs-of-moving-house': {
        'title': 'Hidden costs of moving house',
        'card_desc': "Stamp duty, surveys, the second skip you didn't budget for — the moving-day extras that catch buyers out and how to plan around them.",
        'img': 'moving-day-packing-checklist.jpg',
        'alt': 'Moving-day checklist on a clipboard surrounded by labelled removal boxes',
        'href': 'blog/hidden-costs-of-moving-house.html',
        'cta': 'Avoid the surprises',
    },
    'best-time-of-year-to-move-house-staffordshire': {
        'title': 'Best time of year to move house in Staffordshire',
        'card_desc': "Seasonal pricing rhythms, winter availability, summer queues — when to book to save money or guarantee your preferred date in 2026.",
        'img': 'family-celebrating-keys-new-home.jpg',
        'alt': 'Family celebrating moving into a new Staffordshire home with keys in hand',
        'href': 'blog/best-time-of-year-to-move-house-staffordshire.html',
        'cta': 'See the calendar',
    },
    'best-time-of-day-to-move-house': {
        'title': 'Best time of day to move house',
        'card_desc': "Early starts vs midday vs back-of-day — how the time you book affects price, completion-day stress and the smoothness of your handover.",
        'img': 'empty-room-moving-boxes-ready.jpg',
        'alt': 'Empty room ready for movers at the start of a Staffordshire moving day',
        'href': 'blog/best-time-of-day-to-move-house.html',
        'cta': 'Pick the right slot',
    },
    'moving-home-with-pets-staffordshire-checklist': {
        'title': 'Moving home with pets — a Staffordshire checklist',
        'card_desc': "What to plan for cats, dogs, rabbits and small animals on moving day — boarding options, microchip updates, settling-in week.",
        'img': 'smiling-woman-with-dog-moving-day.jpg',
        'alt': 'Smiling Staffordshire homeowner with her dog on moving day',
        'href': 'blog/moving-home-with-pets-staffordshire-checklist.html',
        'cta': 'Get the pet checklist',
    },
    'how-to-pack-fragile-items-properly': {
        'title': 'How to pack fragile items properly',
        'card_desc': "Glassware, electronics, ceramics, mirrors — the wrap-and-pad techniques our crews use, with materials you can pick up locally.",
        'img': 'packing-glassware-bubble-wrap.jpg',
        'alt': 'Hands wrapping glassware in bubble wrap before packing into a removal box',
        'href': 'blog/how-to-pack-fragile-items-properly.html',
        'cta': 'See the packing guide',
    },
    'self-storage-vs-full-service-storage': {
        'title': 'Self-storage vs full-service storage',
        'card_desc': "When DIY self-storage saves money, when full-service wins on hassle — a full cost + access comparison for Staffordshire customers.",
        'img': 'cardboard-boxes-storage-warehouse.jpg',
        'alt': 'Palletised cardboard storage units in a Stoke-on-Trent warehouse',
        'href': 'blog/self-storage-vs-full-service-storage.html',
        'cta': 'Compare your options',
    },
    'how-to-declutter-before-a-house-move': {
        'title': 'How to declutter before a house move',
        'card_desc': "A room-by-room declutter plan starting 4 weeks out — what to keep, charity-shop, sell or skip, with realistic timing for working families.",
        'img': 'woman-folding-clothes-suitcase-packing.jpg',
        'alt': 'Person folding clothes into a suitcase while decluttering before a move',
        'href': 'blog/how-to-declutter-before-a-house-move.html',
        'cta': 'Get the declutter plan',
    },
    'diy-vs-professional-house-move-cost': {
        'title': 'DIY vs professional house move — true cost compared',
        'card_desc': "Hiring a van and eight friends sounds cheap until you add insurance, fuel, food and a day off work. Real numbers for both routes in 2026.",
        'img': 'man-stacking-cardboard-removal-boxes.jpg',
        'alt': 'Person stacking cardboard removal boxes on a Staffordshire moving day',
        'href': 'blog/diy-vs-professional-house-move-cost.html',
        'cta': 'Run the numbers',
    },
    'move-in-cleaning-checklist-staffordshire': {
        'title': 'Move-in cleaning checklist for Staffordshire',
        'card_desc': "What to deep-clean before your furniture arrives, what's worth a professional, and the 12 items you'll wish you'd brought to the new place.",
        'img': 'unpacking-bedroom-boxes.jpg',
        'alt': 'Bedroom partly unpacked after a Staffordshire move-in cleaning sweep',
        'href': 'blog/move-in-cleaning-checklist-staffordshire.html',
        'cta': 'Get the cleaning list',
    },
    'moving-with-elderly-parents-staffordshire': {
        'title': 'Moving home with elderly parents — Staffordshire guide',
        'card_desc': "Emotional and practical advice for downsizing older relatives — handling memories, mobility needs, care-arrangement transitions.",
        'img': 'estate-agent-handing-house-keys.jpg',
        'alt': 'Estate agent handing house keys to a Staffordshire family on completion day',
        'href': 'blog/moving-with-elderly-parents-staffordshire.html',
        'cta': 'Read the family guide',
    },
    'downsizing-storage-staffordshire': {
        'title': 'Downsizing storage in Staffordshire',
        'card_desc': "Moving from a 4-bed family home to a 2-bed retirement bungalow? How to phase storage and decide what makes the cut.",
        'img': 'couple-packing-living-room.jpg',
        'alt': 'Staffordshire couple packing living room belongings during a downsizing move',
        'href': 'blog/downsizing-storage-staffordshire.html',
        'cta': 'Plan the downsize',
    },
    'office-relocation-planning-timeline': {
        'title': 'Office relocation planning timeline',
        'card_desc': "An 8-week countdown for a Staffordshire office move — IT, telephony, signage, staff comms — with the milestones that catch businesses out.",
        'img': 'stacked-cardboard-boxes-empty-room.jpg',
        'alt': 'Stacked cardboard boxes in an empty office ready for relocation',
        'href': 'blog/office-relocation-planning-timeline.html',
        'cta': 'See the timeline',
    },
    'moving-insurance-explained': {
        'title': 'Moving insurance explained',
        'card_desc': "Goods in Transit vs Public Liability vs your own contents policy — what each covers, what they don't, and what to ask before you book.",
        'img': 'sealing-cardboard-removal-box-floor.jpg',
        'alt': 'Removal crew member sealing a cardboard box with packing tape during a Stoke house move',
        'href': 'blog/moving-insurance-explained.html',
        'cta': 'Get cover explained',
    },
    # ── New niche blogs (Phase 2 gap fillers) ────────────
    'moving-a-piano-staffordshire-guide-2026': {
        'title': 'Moving a piano in Staffordshire (2026 guide)',
        'card_desc': "300+ piano moves of experience — what separates a real piano crew from a cheap one, 2026 costs, insurance, the four piano types we move most.",
        'img': 'couple-wrapping-furniture-protection.jpg',
        'alt': 'Removal team carefully wrapping a large piece of furniture for safe transit',
        'href': 'blog/moving-a-piano-staffordshire-guide-2026.html',
        'cta': 'Read the piano guide',
    },
    'antiques-moving-staffordshire-specialist-guide': {
        'title': 'Antiques moving in Staffordshire — specialist guide',
        'card_desc': "Crating, declared-value insurance, provenance documents and 2026 prices for moving antiques across Staffordshire — from a single piece to a full collection.",
        'img': 'couple-unpacking-photo-frames-memories.jpg',
        'alt': 'Couple carefully unpacking framed family memorabilia after a Staffordshire move',
        'href': 'blog/antiques-moving-staffordshire-specialist-guide.html',
        'cta': 'Read the antiques guide',
    },
    'international-removals-from-the-uk-2026-guide': {
        'title': 'International removals from the UK — 2026 guide',
        'card_desc': "Container vs groupage, Transfer of Residence paperwork, marine cover, realistic timelines and 2026 costs for moves out of Staffordshire to anywhere.",
        'img': 'packing-electronics-safely-removal.jpg',
        'alt': 'Removal crew member carefully packing electronics for international shipping',
        'href': 'blog/international-removals-from-the-uk-2026-guide.html',
        'cta': 'See the int\'l guide',
    },
    'european-removals-from-staffordshire-2026': {
        'title': 'European removals from Staffordshire — 2026 guide',
        'card_desc': "Post-Brexit reality, van service vs container, ToR paperwork, Ireland as the special case — and what the eight most-common EU destinations actually cost.",
        'img': 'removal-lorry-loading-furniture.jpg',
        'alt': 'Removal lorry being loaded with furniture for a European removal journey',
        'href': 'blog/european-removals-from-staffordshire-2026.html',
        'cta': 'Read the EU guide',
    },
    'man-and-van-vs-full-removal-staffordshire': {
        'title': 'Man and van vs full removal — Staffordshire 2026',
        'card_desc': "When man and van wins, when it loses, the insurance reality of cheap quotes, and an honest 2026 cost comparison across all the common Staffordshire move sizes.",
        'img': 'man-carrying-cardboard-box-home.jpg',
        'alt': 'Man carrying a single cardboard box into a home during a small-scale move',
        'href': 'blog/man-and-van-vs-full-removal-staffordshire.html',
        'cta': 'See the comparison',
    },
    'what-is-a-white-glove-moving-service': {
        'title': 'What is a white-glove moving service?',
        'card_desc': "The seven things that distinguish white-glove from a standard removal, who actually needs it, the declared-value insurance story, and 2026 costs.",
        'img': 'wrapping-fragile-items-paper.jpg',
        'alt': 'Removal crew member wrapping fragile items in acid-free archival paper',
        'href': 'blog/what-is-a-white-glove-moving-service.html',
        'cta': 'See white-glove',
    },
    'house-clearance-after-bereavement-staffordshire': {
        'title': 'House clearance after bereavement — Staffordshire guide',
        'card_desc': "What bereavement clearance involves, the realistic 3–8 week timeline, sensitive handling of family-keeper items, and honest 2026 costs in Staffordshire.",
        'img': 'stacked-removal-boxes-hallway.jpg',
        'alt': 'Stacked removal boxes in the hallway of a property during a house clearance',
        'href': 'blog/house-clearance-after-bereavement-staffordshire.html',
        'cta': 'Read the clearance guide',
    },
    'student-moves-keele-staffordshire-guide': {
        'title': 'Student moves — Keele &amp; Staffordshire guide 2026',
        'card_desc': "The Staffordshire student-move calendar, the summer-storage trap, the parent-help insurance gap, and honest 2026 costs for moves across the student year.",
        'img': 'woman-unpacking-kitchenware.jpg',
        'alt': 'Student unpacking kitchenware after moving into a new Staffordshire rental',
        'href': 'blog/student-moves-keele-staffordshire-guide.html',
        'cta': 'Read the student guide',
    },
    'professional-packing-services-staffordshire-2026': {
        'title': 'Professional packing services Staffordshire 2026',
        'card_desc': "Full-pack, fragile-only or DIY? Honest 2026 cost comparison, the insurance gap on self-packed cartons, and how to decide what suits your move.",
        'img': 'woman-packing-bedroom-floor.jpg',
        'alt': 'Removal crew member packing bedroom contents into labelled cartons',
        'href': 'blog/professional-packing-services-staffordshire-2026.html',
        'cta': 'See packing options',
    },
    'storage-size-guide-staffordshire': {
        'title': 'How much storage space do I need? Staffordshire guide',
        'card_desc': "Per-room cubic-feet sizing, realistic totals by property size, NSR palletised unit dimensions, and the 5 most-common sizing mistakes to avoid.",
        'img': 'kitchen-removal-box-bedroom-stack.jpg',
        'alt': 'Stacked removal boxes in a kitchen ready for storage sizing assessment',
        'href': 'blog/storage-size-guide-staffordshire.html',
        'cta': 'See sizing guide',
    },
    'self-storage-security-staffordshire': {
        'title': 'How secure is self storage? Staffordshire 2026 guide',
        'card_desc': "Four security layers explained, what to verify before booking, the self-storage vs full-service comparison, and inside NSR's Stoke-on-Trent warehouse.",
        'img': 'unpacking-cardboard-removal-boxes.jpg',
        'alt': 'Removal boxes being securely unpacked after retrieval from Stoke-on-Trent storage',
        'href': 'blog/self-storage-security-staffordshire.html',
        'cta': 'See security guide',
    },
    'storage-prohibited-items-uk': {
        'title': "What you can't store — UK self storage rules 2026",
        'card_desc': "Seven universal prohibitions, why each rule exists, what to do with items that can't be stored, and the pre-storage inventory checklist.",
        'img': 'opening-removal-box-room.jpg',
        'alt': 'Person opening a removal box checking contents before storage',
        'href': 'blog/storage-prohibited-items-uk.html',
        'cta': "See what's prohibited",
    },
    'move-planning-guide-staffordshire': {
        'title': 'Plan your move — Staffordshire planning guide 2026',
        'card_desc': "The 12-week move planning countdown, what to do when, common planning mistakes, and how to plan around late completions in Staffordshire.",
        'img': 'writing-moving-inventory-list.jpg',
        'alt': 'Person writing a moving inventory list at a desk during move planning',
        'href': 'blog/move-planning-guide-staffordshire.html',
        'cta': 'Read planning guide',
    },
    'complete-moving-checklist-staffordshire': {
        'title': 'Complete moving home checklist — Staffordshire 2026',
        'card_desc': "Step-by-step 8-week countdown checklist: what to do when, day-of essentials, first-week priorities for a smooth Staffordshire move.",
        'img': 'labelling-kitchen-box-marker.jpg',
        'alt': 'Person labelling a kitchen removal box with marker pen during move packing',
        'href': 'blog/complete-moving-checklist-staffordshire.html',
        'cta': 'See the checklist',
    },
    'flat-removals-staffordshire': {
        'title': 'Flat removals Staffordshire — apartment moving guide 2026',
        'card_desc': "How flat removals differ from house moves: access challenges, lift booking, parking, furniture sizing, and honest 2026 cost ranges by flat type.",
        'img': 'couple-with-removal-boxes-new-home.jpg',
        'alt': 'Couple with removal boxes arriving at their new Staffordshire flat',
        'href': 'blog/flat-removals-staffordshire.html',
        'cta': 'See flat moves guide',
    },
    'winter-moving-tips-staffordshire': {
        'title': 'Winter moving — 4 tips for Staffordshire moves 2026',
        'card_desc': "Four practical winter moving tips: weather planning, fragile-item protection from temperature swings, floor protection, daylight and timing.",
        'img': 'couple-new-home-cardboard-box.jpg',
        'alt': 'Couple arriving at a new Staffordshire home with cardboard removal box during winter',
        'href': 'blog/winter-moving-tips-staffordshire.html',
        'cta': 'Get winter tips',
    },
    'moving-house-top-tips-uk': {
        'title': 'Top tips for moving house — UK 2026 guide',
        'card_desc': "Eight practical top tips for moving house in 2026 — planning, decluttering, packing labelling, first-night box, address change, move-day flexibility.",
        'img': 'woman-checking-removal-boxes.jpg',
        'alt': 'Person checking labelled removal boxes against an inventory list',
        'href': 'blog/moving-house-top-tips-uk.html',
        'cta': 'See top tips',
    },
}

# Shorthand aliases for the universal blog slugs (used heavily below).
_COST = 'cost-of-moving-house-stoke-on-trent-2026'
_RELI = 'choosing-a-reliable-removal-company-stoke'
_HIDD = 'hidden-costs-of-moving-house'
_BTY  = 'best-time-of-year-to-move-house-staffordshire'
_BTD  = 'best-time-of-day-to-move-house'
_PETS = 'moving-home-with-pets-staffordshire-checklist'
_FRAG = 'how-to-pack-fragile-items-properly'
_STOR = 'self-storage-vs-full-service-storage'
_DECL = 'how-to-declutter-before-a-house-move'
_DIY  = 'diy-vs-professional-house-move-cost'
_CLEA = 'move-in-cleaning-checklist-staffordshire'
_ELDR = 'moving-with-elderly-parents-staffordshire'
_DOWN = 'downsizing-storage-staffordshire'
_OFFC = 'office-relocation-planning-timeline'
_INSU = 'moving-insurance-explained'
_PIAN = 'moving-a-piano-staffordshire-guide-2026'
_ANTI = 'antiques-moving-staffordshire-specialist-guide'
_INTL = 'international-removals-from-the-uk-2026-guide'
_EURO = 'european-removals-from-staffordshire-2026'
_MVAN = 'man-and-van-vs-full-removal-staffordshire'
_WGLV = 'what-is-a-white-glove-moving-service'
_HCLR = 'house-clearance-after-bereavement-staffordshire'
_STUD = 'student-moves-keele-staffordshire-guide'
_PACK = 'professional-packing-services-staffordshire-2026'
_SIZE = 'storage-size-guide-staffordshire'
_SECU = 'self-storage-security-staffordshire'
_PROH = 'storage-prohibited-items-uk'
_PLAN = 'move-planning-guide-staffordshire'
_CHKL = 'complete-moving-checklist-staffordshire'
_FLAT = 'flat-removals-staffordshire'
_WINT = 'winter-moving-tips-staffordshire'
_TIPS = 'moving-house-top-tips-uk'

# Per-page mapping. Key is the auto-derived page key (see
# _auto_related_key below). Pages absent from this dict render no
# related section at all (legal pages, 404, careers, etc.).
RELATED_FOR = {
    # ── HOME ─────────────────────────────────────────────
    'home':                              [_COST, _RELI, _HIDD],

    # ── SERVICES ─────────────────────────────────────────
    # Each service page leads with its own dedicated topic blog
    # (where one exists) plus two contextually-related secondaries.
    'services-index':                    [_COST, _RELI, _WGLV],
    'services-domestic-removals':        [_COST, _DECL, _PETS],
    'services-commercial-removals':      [_OFFC, _EURO, _RELI],
    'services-packing-services':         [_PACK, _FRAG, _DECL],
    'services-storage-services':         [_SIZE, _SECU, _PROH],
    'services-piano-removals':           [_PIAN, _INSU, _FRAG],
    'services-man-and-van':              [_MVAN, _DIY,  _STUD],
    'services-european-removals':        [_EURO, _INTL, _OFFC],
    'services-international-removals':   [_INTL, _EURO, _INSU],
    'services-house-clearance':          [_HCLR, _ELDR, _DOWN],
    'services-student-removals':         [_STUD, _MVAN, _COST],
    'services-antiques-moving':          [_ANTI, _WGLV, _INSU],
    'services-white-glove-service':      [_WGLV, _ANTI, _PIAN],
    'services-packaging-shop':           [_FRAG, _DECL, _DIY],

    # ── AREAS (hub + 20 town pages) ──────────────────────
    # Each area page gets its own distinct trio shaped by the
    # town's character: city-centre Potteries get tighter-access
    # / smaller-property themes; rural Moorlands get weather /
    # storage themes; commuter belt gets value / practical themes;
    # high-value rural gets antiques / white-glove.
    'areas-covered-index':               [_COST, _BTY,  _RELI],

    # Stoke-on-Trent and the six Potteries cities
    'areas-covered-removals-stoke-on-trent':     [_COST, _RELI, _HCLR],
    'areas-covered-removals-hanley':             [_COST, _BTD,  _MVAN],
    'areas-covered-removals-burslem':            [_COST, _DECL, _FRAG],
    'areas-covered-removals-tunstall':           [_COST, _CLEA, _PETS],
    'areas-covered-removals-longton':            [_COST, _CLEA, _DECL],
    'areas-covered-removals-fenton':             [_COST, _PETS, _FRAG],

    # Newcastle-under-Lyme (Keele University)
    'areas-covered-removals-newcastle-under-lyme': [_STUD, _COST, _RELI],

    # North Staffs towns
    'areas-covered-removals-kidsgrove':          [_BTY,  _ELDR, _DOWN],

    # Stafford / Stone (county town + adjacent)
    'areas-covered-removals-stafford':           [_COST, _WGLV, _ANTI],
    'areas-covered-removals-stone':              [_DOWN, _ELDR, _RELI],

    # Staffordshire Moorlands + rural North Staffs
    'areas-covered-removals-leek':               [_BTY,  _INSU, _STOR],
    'areas-covered-removals-cheadle':            [_PETS, _CLEA, _BTY],
    'areas-covered-removals-biddulph':           [_HIDD, _STOR, _BTD],
    'areas-covered-removals-eccleshall':         [_ANTI, _WGLV, _DOWN],

    # East Staffs (Burton brewery town)
    'areas-covered-removals-burton-on-trent':    [_OFFC, _RELI, _COST],

    # Peak District / Cheshire borderland
    'areas-covered-removals-buxton':             [_INSU, _STOR, _ANTI],
    'areas-covered-removals-crewe':              [_RELI, _BTD,  _MVAN],

    # South Staffs cathedral + commuter belt
    'areas-covered-removals-lichfield':          [_OFFC, _ANTI, _HCLR],
    'areas-covered-removals-cannock':            [_DIY,  _MVAN, _HIDD],
    'areas-covered-removals-tamworth':           [_PETS, _MVAN, _BTY],

    # ── RESOURCES ────────────────────────────────────────
    'resources-storage-calculator':      [_SIZE, _COST, _STOR],

    # ── ROOT UTILITY ─────────────────────────────────────
    'about-us':                          [_RELI, _HIDD, _INSU],
    'reviews':                           [_RELI, _INSU, _WGLV],
    'quote':                             [_COST, _BTY,  _HIDD],

    # ── BLOG POSTS (per-post, never self-referential) ────
    'blog-cost-of-moving-house-stoke-on-trent-2026':     [_HIDD, _DIY,  _BTY],
    'blog-choosing-a-reliable-removal-company-stoke':    [_INSU, _ANTI, _HIDD],
    'blog-hidden-costs-of-moving-house':                 [_COST, _RELI, _DIY],
    'blog-best-time-of-year-to-move-house-staffordshire': [_BTD,  _COST, _OFFC],
    'blog-best-time-of-day-to-move-house':               [_BTY,  _COST, _PETS],
    'blog-moving-home-with-pets-staffordshire-checklist': [_CLEA, _DECL, _BTD],
    'blog-how-to-pack-fragile-items-properly':           [_DECL, _INSU, _ANTI],
    'blog-self-storage-vs-full-service-storage':         [_DOWN, _INSU, _COST],
    'blog-how-to-declutter-before-a-house-move':         [_FRAG, _DOWN, _CLEA],
    'blog-diy-vs-professional-house-move-cost':          [_COST, _HIDD, _MVAN],
    'blog-move-in-cleaning-checklist-staffordshire':     [_DECL, _FRAG, _PETS],
    'blog-moving-with-elderly-parents-staffordshire':    [_DOWN, _HCLR, _RELI],
    'blog-downsizing-storage-staffordshire':             [_STOR, _ELDR, _DECL],
    'blog-office-relocation-planning-timeline':          [_EURO, _INTL, _RELI],
    'blog-moving-insurance-explained':                   [_PIAN, _ANTI, _RELI],
    'blog-moving-a-piano-staffordshire-guide-2026':      [_INSU, _FRAG, _WGLV],
    'blog-antiques-moving-staffordshire-specialist-guide': [_WGLV, _INSU, _PIAN],
    'blog-international-removals-from-the-uk-2026-guide': [_EURO, _INSU, _OFFC],
    'blog-european-removals-from-staffordshire-2026':    [_INTL, _OFFC, _INSU],
    'blog-man-and-van-vs-full-removal-staffordshire':    [_DIY,  _STUD, _COST],
    'blog-what-is-a-white-glove-moving-service':         [_ANTI, _PIAN, _INSU],
    'blog-house-clearance-after-bereavement-staffordshire': [_ELDR, _DOWN, _DECL],
    'blog-student-moves-keele-staffordshire-guide':      [_MVAN, _COST, _BTY],
    'blog-professional-packing-services-staffordshire-2026': [_FRAG, _DECL, _INSU],
    'blog-storage-size-guide-staffordshire':             [_SECU, _PROH, _STOR],
    'blog-self-storage-security-staffordshire':          [_SIZE, _PROH, _INSU],
    'blog-storage-prohibited-items-uk':                  [_SIZE, _SECU, _DECL],
    'blog-move-planning-guide-staffordshire':            [_CHKL, _TIPS, _COST],
    'blog-complete-moving-checklist-staffordshire':      [_PLAN, _TIPS, _DECL],
    'blog-flat-removals-staffordshire':                  [_MVAN, _STUD, _COST],
    'blog-winter-moving-tips-staffordshire':             [_BTY,  _BTD,  _RELI],
    'blog-moving-house-top-tips-uk':                     [_PLAN, _CHKL, _COST],

    # ── INTENTIONALLY UNMAPPED (no related section) ──────
    # 404.html, privacy-policy.html, terms.html, careers.html, blog/index.html
    # — all skipped: legal pages don't need cross-links, blog hub already
    # IS a blog listing, careers is internal-facing.
}


def _auto_related_key(slug):
    """Derive a stable RELATED_FOR key from a page's slug.
    index.html → 'home' (special alias)
    services/piano-removals.html → 'services-piano-removals'
    areas-covered/removals-leek.html → 'areas-covered-removals-leek'
    blog/cost-of-moving-house-2026.html → 'blog-cost-of-moving-house-2026'
    about-us.html → 'about-us'"""
    if slug in ('index.html', './index.html', ''):
        return 'home'
    key = slug.replace('.html', '').replace('/', '-')
    return key


def related_blogs(page_key='home', depth=0, heading=None, lead=None):
    """Render the 3-card 'related reading' orange band that sits just
    above the final .cta-strip. Returns '' if page_key isn't mapped
    (legal pages, 404, careers, etc.) so callers can blindly include
    the call without conditional logic."""
    if page_key not in RELATED_FOR:
        return ''
    p = '../' * depth
    slugs = RELATED_FOR[page_key]
    h = heading or 'Plan your move with confidence'
    l = lead or 'Three guides our customers find most useful — read first, decide with full information.'
    cards = []
    for slug in slugs:
        meta = BLOG_META.get(slug)
        if not meta:
            continue
        cta = meta.get('cta', 'Read article')
        cards.append(f'''          <a class="related-card" href="{p}{meta['href']}">
            <div class="related-img">
              <img src="{p}images/{meta['img']}" alt="{meta['alt']}" width="1600" height="1066" loading="lazy">
            </div>
            <div class="related-body">
              <h3>{meta['title']}</h3>
              <p>{meta['card_desc']}</p>
              <span class="related-arrow">{cta}</span>
            </div>
          </a>''')
    cards_html = '\n'.join(cards)
    return f'''    <section class="related-section" aria-label="Related reading">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Related reading</span>
          <h2>{h}</h2>
          <p>{l}</p>
        </div>
        <div class="related-grid">
{cards_html}
        </div>
      </div>
    </section>'''


SERVICES_DROPDOWN = [
    ('Residential removals', 'services/domestic-removals.html'),
    ('Commercial removals',  'services/commercial-removals.html'),
    ('Packing services',     'services/packing-services.html'),
    ('Storage solutions',    'services/storage-services.html'),
    ('Piano removals',       'services/piano-removals.html'),
    ('Man &amp; van',        'services/man-and-van.html'),
    ('European removals',    'services/european-removals.html'),
    ('International',        'services/international-removals.html'),
    ('House clearance',      'services/house-clearance.html'),
    ('Student removals',     'services/student-removals.html'),
    ('Antiques moving',      'services/antiques-moving.html'),
    ('White-glove service',  'services/white-glove-service.html'),
    ('Packing materials',    'services/packaging-shop.html'),
]
AREAS_DROPDOWN = [
    ('Stoke-on-Trent',          'areas-covered/removals-stoke-on-trent.html'),
    ('Hanley',                  'areas-covered/removals-hanley.html'),
    ('Burslem',                 'areas-covered/removals-burslem.html'),
    ('Tunstall',                'areas-covered/removals-tunstall.html'),
    ('Longton',                 'areas-covered/removals-longton.html'),
    ('Fenton',                  'areas-covered/removals-fenton.html'),
    ('Newcastle-under-Lyme',    'areas-covered/removals-newcastle-under-lyme.html'),
    ('Kidsgrove',               'areas-covered/removals-kidsgrove.html'),
    ('Stafford',                'areas-covered/removals-stafford.html'),
    ('Stone',                   'areas-covered/removals-stone.html'),
    ('Leek',                    'areas-covered/removals-leek.html'),
    ('Cheadle',                 'areas-covered/removals-cheadle.html'),
    ('Biddulph',                'areas-covered/removals-biddulph.html'),
    ('Eccleshall',              'areas-covered/removals-eccleshall.html'),
    ('Burton-on-Trent',         'areas-covered/removals-burton-on-trent.html'),
    ('Buxton',                  'areas-covered/removals-buxton.html'),
    ('Crewe',                   'areas-covered/removals-crewe.html'),
    ('Lichfield',               'areas-covered/removals-lichfield.html'),
    ('Cannock',                 'areas-covered/removals-cannock.html'),
    ('Tamworth',                'areas-covered/removals-tamworth.html'),
]


def _dropdown_items(items, depth, hub_href, hub_label):
    p = '../' * depth
    rows = [f'              <li><a href="{p}{hub_href}"><strong>All {hub_label.lower()} →</strong></a></li>']
    for label, href in items:
        rows.append(f'              <li><a href="{p}{href}">{label}</a></li>')
    return '\n'.join(rows)


def nav(current, depth=0):
    p = '../' * depth
    # Depth-aware home path so Home/logo work in every deployment context
    # (file://, localhost HTTP, GitHub Pages subpath, custom domain).
    # `./` at depth=0, `../` at depth=1, `../../` at depth=2 — all resolve
    # to the project root in any of those contexts.
    home = p if p else './'
    svc_dd = _dropdown_items(SERVICES_DROPDOWN, depth, 'services/', 'Services')
    areas_dd = _dropdown_items(AREAS_DROPDOWN, depth, 'areas-covered/', 'Areas')

    return f'''  <header class="nav">
    <div class="nav-inner">
      <a class="brand" href="{home}" aria-label="North Staffordshire Removals &amp; Storage Ltd — home">
        <img src="{p}images/logo-north-staffordshire-removals.png" alt="North Staffordshire Removals &amp; Storage Ltd logo" width="959" height="200">
      </a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav">☰ Menu</button>
      <nav aria-label="Primary">
        <ul id="primary-nav" class="nav-menu">
          <li><a href="{home}"{' aria-current="page"' if current == 'home' else ''}>Home</a></li>
          <li><a href="{p}about-us.html"{' aria-current="page"' if current == 'about' else ''}>About</a></li>
          <li class="has-dropdown">
            <a href="{p}services/"{' aria-current="page"' if current == 'services' else ''} aria-haspopup="true">Services</a>
            <ul class="nav-dropdown">
{svc_dd}
            </ul>
          </li>
          <li class="has-dropdown">
            <a href="{p}areas-covered/"{' aria-current="page"' if current == 'areas' else ''} aria-haspopup="true">Areas</a>
            <ul class="nav-dropdown nav-dropdown-2col">
{areas_dd}
            </ul>
          </li>
          <li><a href="{p}blog/"{' aria-current="page"' if current == 'blog' else ''}>Blog</a></li>
          <li><a href="{p}reviews.html"{' aria-current="page"' if current == 'reviews' else ''}>Reviews</a></li>
          <li><a href="{p}resources/storage-calculator.html"{' aria-current="page"' if current == 'calc' else ''}>Calculator</a></li>
          <li class="nav-cta-row"><a href="{p}quote.html" class="nav-cta">Free Quote</a></li>
          <li class="nav-actions" aria-hidden="false">
            <a class="nav-action nav-action-solid" href="tel:+441782939124">
              <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2z"/></svg>
              <span>Call us</span>
            </a>
            <a class="nav-action nav-action-outline" href="mailto:enquiries@northstaffordshireremovals.co.uk">
              <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/></svg>
              <span>Email us</span>
            </a>
            <a class="nav-action nav-action-solid" href="{p}quote.html">
              <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="m9 16.17-3.88-3.88a1 1 0 0 0-1.41 1.42l4.59 4.59a1 1 0 0 0 1.41 0L20.71 7.71a1 1 0 0 0-1.41-1.42L9 16.17z"/></svg>
              <span>Get quote</span>
            </a>
          </li>
        </ul>
      </nav>
    </div>
  </header>'''


def cta_strip(depth=0):
    p = '../' * depth
    return f'''    <section class="cta-strip">
      <div class="container">
        <div>
          <h2>Ready to move with Staffordshire's leading family-run team?</h2>
          <p>Most surveys take under 30 minutes — by video or in person. End-to-end support from first call to final unload.</p>
        </div>
        <div class="actions">
          <a class="btn" href="{p}quote.html">Get a free quote</a>
          <a class="btn btn-outline" href="tel:+441782939124">Call 01782 939124</a>
        </div>
      </div>
    </section>'''


def fab_stack(depth=0):
    """Sticky FAB at the bottom-RIGHT of the viewport: navy phone
    FAB with orange phone icon and pulse animation. Email FAB was
    removed per user request — phone is the primary contact CTA;
    email is still accessible via the nav drawer, footer, and the
    quote form on every page. Mobile collapses to 56px circle."""
    return f'''  <a class="fab fab-phone" href="tel:+441782939124" aria-label="Call North Staffordshire Removals on 01782 939124">
    <span class="fab-icon" aria-hidden="true"></span>
    <span class="fab-text">Call 01782 939124</span>
  </a>'''

# Back-compat constant; kept in case any older render still imports it.
PHONE_FAB = '''  <a class="phone-fab" href="tel:+441782939124" aria-label="Call North Staffordshire Removals on 01782 939124">
    <span class="phone-fab-icon" aria-hidden="true">📞</span>
    <span class="phone-fab-text">Call 01782 939124</span>
  </a>'''


def footer(depth=0):
    p = '../' * depth
    home = p if p else './'
    return f'''  <footer class="site-footer">
    <div class="container">
      <div>
        <div class="brand-line">North Staffordshire Removals</div>
        <div class="brand-tag">&amp; Storage Ltd</div>
        <p>Staffordshire's leading home and business removals and storage company. Family-run from Stoke-on-Trent since 2010.</p>
        <p style="margin:.6rem 0 0;">Suite F24, Genesis Centre,<br>Innovation Way,<br>Stoke-on-Trent, ST6 4BF</p>
      </div>
      <div>
        <h4>Quick Menu</h4>
        <ul>
          <li><a href="{home}">Home</a></li>
          <li><a href="{p}about-us.html">About us</a></li>
          <li><a href="{p}services/">Services</a></li>
          <li><a href="{p}areas-covered/">Areas Covered</a></li>
          <li><a href="{p}reviews.html">Reviews</a></li>
          <li><a href="{p}blog/">Advice &amp; tips</a></li>
          <li><a href="{p}resources/storage-calculator.html">Moving Calculator</a></li>
          <li><a href="{p}privacy-policy.html">Privacy</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{p}services/domestic-removals.html">Residential removals</a></li>
          <li><a href="{p}services/commercial-removals.html">Commercial removals</a></li>
          <li><a href="{p}services/storage-services.html">Storage solutions</a></li>
          <li><a href="{p}services/packing-services.html">Packing services</a></li>
          <li><a href="{p}services/piano-removals.html">Piano removals</a></li>
          <li><a href="{p}quote.html">Online booking</a></li>
        </ul>
      </div>
      <div>
        <h4>Where we operate</h4>
        <ul>
          <li><a href="{p}areas-covered/removals-stoke-on-trent.html">Stoke-on-Trent</a></li>
          <li><a href="{p}areas-covered/removals-newcastle-under-lyme.html">Newcastle-under-Lyme</a></li>
          <li><a href="{p}areas-covered/removals-stafford.html">Stafford</a></li>
          <li><a href="{p}areas-covered/removals-stone.html">Stone</a></li>
          <li><a href="{p}areas-covered/removals-leek.html">Leek</a></li>
          <li><a href="{p}areas-covered/removals-eccleshall.html">Eccleshall</a></li>
          <li><a href="{p}areas-covered/removals-burton-on-trent.html">Burton-on-Trent</a></li>
          <li><a href="{p}areas-covered/removals-buxton.html">Buxton</a></li>
        </ul>
        <h4 style="margin-top:1.25rem">Contact</h4>
        <ul>
          <li><a href="tel:+441782939124">📞 01782 939124</a></li>
          <li><a href="mailto:enquiries@northstaffordshireremovals.co.uk">✉ enquiries@northstaffordshireremovals.co.uk</a></li>
        </ul>
      </div>
      <div class="legal">
        <span>© 2026 North Staffordshire Removals &amp; Storage Ltd. All rights reserved. <span style="opacity:.7"> · Site built by Mark Willis</span></span>
        <span>
          <a href="{p}privacy-policy.html">Privacy</a> ·
          <a href="{p}terms.html">Terms</a> ·
          <a href="{p}careers.html">Careers</a> ·
          <a href="{p}sitemap.xml">Sitemap</a>
        </span>
      </div>
    </div>
  </footer>
{fab_stack(depth)}
  <script defer src="{p}js/mobile-nav.js?v={CSS_V}"></script>
</body>
</html>'''


def hero_quote_form(depth=0, id_prefix='hero-qf'):
    """Embedded quote form for the hero banner. Unique IDs so it doesn't collide
    with other forms on the same page (quote.html main form, calculator)."""
    p = '../' * depth
    return f'''        <aside class="quote-form" id="{id_prefix}" aria-label="Free quote request">
          <h2>Get your free quote</h2>
          <p class="qf-sub">Most customers receive a fixed-price quote within 24 hours. No card details, no obligation.</p>
          <form action="{p}quote.html" method="get" novalidate>
            <div class="qf-row two">
              <div class="qf-field"><label for="{id_prefix}-name">Your name</label><input id="{id_prefix}-name" name="name" type="text" autocomplete="name" required></div>
              <div class="qf-field"><label for="{id_prefix}-phone">Phone</label><input id="{id_prefix}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
            </div>
            <div class="qf-row"><div class="qf-field"><label for="{id_prefix}-email">Email</label><input id="{id_prefix}-email" name="email" type="email" autocomplete="email" required></div></div>
            <div class="qf-row two">
              <div class="qf-field"><label for="{id_prefix}-from">Moving from (postcode)</label><input id="{id_prefix}-from" name="from" type="text" autocomplete="postal-code" placeholder="ST1 1AA" required></div>
              <div class="qf-field"><label for="{id_prefix}-to">Moving to (postcode)</label><input id="{id_prefix}-to" name="to" type="text" autocomplete="postal-code" placeholder="ST5 1BB" required></div>
            </div>
            <div class="qf-row two">
              <div class="qf-field"><label for="{id_prefix}-size">Property size</label><select id="{id_prefix}-size" name="size" required><option value="">Choose…</option><option>Studio / 1-bed flat</option><option>2-bed</option><option>3-bed</option><option>4+ bed</option><option>Office / commercial</option></select></div>
              <div class="qf-field"><label for="{id_prefix}-date">Preferred date</label><input id="{id_prefix}-date" name="date" type="date"></div>
            </div>
            <button class="btn btn-block" type="submit">Get my free quote</button>
            <p class="qf-foot">Prefer to talk? Call <a href="tel:+441782939124"><strong>01782 939124</strong></a></p>
          </form>
        </aside>'''


def hero(*, eyebrow, h1, lead, depth=0, hero_img='family-celebrating-keys-new-home.jpg', show_form=True):
    """Hero banner. show_form=False omits the embedded quote form
    (used on pages that already carry their own interactive form/widget,
    e.g. resources/storage-calculator.html)."""
    p = '../' * depth
    form_html = hero_quote_form(depth) if show_form else ''
    return f'''    <section class="hero" style="background:linear-gradient(115deg, rgba(10,34,62,.92) 0%, rgba(17,54,90,.78) 50%, rgba(10,34,62,.55) 100%), url('{p}images/{hero_img}') center/cover no-repeat;">
      <div class="container">
        <div class="hero-inner">
          <span class="eyebrow">{eyebrow}</span>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="hero-actions">
            <a class="btn" href="{p}quote.html">Get a free quote</a>
            <a class="btn btn-outline" href="tel:+441782939124">Call 01782 939124</a>
          </div>
          <div class="hero-trust">
            <span><span class="tick">✓</span> Family-run since 2010</span>
            <span><span class="tick">✓</span> Fully covered</span>
            <span><span class="tick">✓</span> Fixed prices</span>
            <span><span class="tick">✓</span> 187 verified reviews</span>
          </div>
        </div>
{form_html}
      </div>
    </section>'''


def faq_section(faqs, schema_only=False):
    if schema_only:
        return ''
    items = []
    for q, a in faqs:
        items.append(f'''          <details>
            <summary>{html.escape(q)}</summary>
            <p>{a}</p>
          </details>''')
    return f'''    <section class="alt-bg faq">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">FAQ</span>
          <h2>Common questions</h2>
        </div>
        <div class="faq-grid">
{chr(10).join(items)}
        </div>
      </div>
    </section>'''


def faq_jsonld(faqs):
    if not faqs: return ''
    main = []
    for q, a in faqs:
        # strip HTML tags from a for schema
        import re as _re
        a_clean = _re.sub(r'<[^>]+>', '', a)
        main.append({"@type":"Question","name":q,
                     "acceptedAnswer":{"@type":"Answer","text":a_clean}})
    data = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":main}
    return '\n  <script type="application/ld+json">' + json.dumps(data, separators=(',',':')) + '</script>'


def webpage_jsonld(*, url, title, desc):
    data = {"@context":"https://schema.org","@type":"WebPage","url":url,
            "name":title,"description":desc,"inLanguage":"en-GB","dateModified":"2026-05-22",
            "isPartOf":{"@type":"WebSite","url":BASE,"name":"North Staffordshire Removals & Storage Ltd"},
            "about":{"@id":BASE+'/#organization'}}
    return '\n  <script type="application/ld+json">' + json.dumps(data, separators=(',',':')) + '</script>'


def render_page(*, slug, title, desc, h1, eyebrow, lead, sections_html,
                faqs=None, depth=1, hero_img='family-celebrating-keys-new-home.jpg',
                og_image=None, current='', inline_faq=True):
    """inline_faq=True (default): render the visible FAQ section AND the JSON-LD.
    Pass inline_faq=False when the caller has already included faq_section
    inside sections_html (to avoid duplicating)."""
    canonical = f'{BASE}/{slug}'
    og_image = og_image or hero_img
    extra = webpage_jsonld(url=canonical, title=title, desc=desc) + faq_jsonld(faqs or [])
    parts = [
        head(title=title, desc=desc, canonical=canonical, og_image=og_image,
             preload_img=hero_img, depth=depth, extra_schema=extra),
        '<body>',
        '  <a class="skip-link" href="#main">Skip to main content</a>',
        topbar(depth),
        nav(current, depth),
        '  <main id="main">',
        hero(eyebrow=eyebrow, h1=h1, lead=lead, depth=depth, hero_img=hero_img),
        sections_html,
        faq_section(faqs or []) if (faqs and inline_faq) else '',
        related_blogs(_auto_related_key(slug), depth),
        cta_strip(depth),
        '  </main>',
        footer(depth),
    ]
    out_path = slug
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
    print(f'  wrote {out_path}')


# ═════════════════════════════════════════════════════════════════════
#   PAGE CONTENT
# ═════════════════════════════════════════════════════════════════════

def block_text_image(*, eyebrow, h2, paras, img, alt, reverse=False, alt_bg=False):
    cls = 'alt-bg' if alt_bg else ''
    rev = ' reverse' if reverse else ''
    paras_html = ''.join(f'<p>{p}</p>' for p in paras)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="split{rev}">
          <div class="split-img"><img src="../images/{img}" alt="{html.escape(alt)}" width="1600" height="1066" loading="lazy"></div>
          <div>
            <span class="eyebrow">{eyebrow}</span>
            <h2>{h2}</h2>
            {paras_html}
          </div>
        </div>
      </div>
    </section>'''


def block_six_cards(*, eyebrow, h2, intro, cards, alt_bg=False, orange_row2=False):
    cls = ['why-section']
    if alt_bg: cls.append('alt-bg')
    items_a = ''.join(
        f'<div class="why-card"><div class="why-ic">{html.escape(ic)}</div><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></div>'
        for ic,t,b in cards[:3])
    items_b = ''.join(
        f'<div class="why-card"><div class="why-ic">{html.escape(ic)}</div><h3>{html.escape(t)}</h3><p>{html.escape(b)}</p></div>'
        for ic,t,b in cards[3:])
    second = (f'<div class="why-row-orange"><div class="container"><div class="why-grid">{items_b}</div></div></div>'
              if orange_row2 else
              f'<div class="container"><div class="why-grid" style="margin-top:1.1rem">{items_b}</div></div>')
    return f'''    <section class="{' '.join(cls)}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
          <p>{intro}</p>
        </div>
        <div class="why-grid">{items_a}</div>
      </div>
      {second}
    </section>'''


def block_prose(*, eyebrow, h2, paras, alt_bg=False, orange_bg=False):
    if orange_bg:
        cls = 'services-section'
    elif alt_bg:
        cls = 'alt-bg'
    else:
        cls = ''
    # Each paragraph rendered with no max-width so text spans the full container width
    # matching the card grids on the page (per user rule 2026-05-22).
    paras_html = ''.join(f'<p style="max-width:none">{p}</p>' for p in paras)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
        </div>
        <div class="prose-wide">
          {paras_html}
        </div>
      </div>
    </section>'''


# Reusable "Why choose us" 6-card block (matches the home page exactly).
# Row 1 = cream/white bg, Row 2 = orange band. Pages on alt-bg get inverted.
WHY_CARDS = [
    ('£',  'Fixed prices, in writing',     "Every quote is fixed for 60 days after a free home or video survey. No hourly billing, no surprise fuel surcharges, no 'we ran over' on the day."),
    ('✓',  'Fully covered every mile',     "Comprehensive Goods in Transit and £10 million Public Liability cover. Claims handled directly by our team — never a third-party broker."),
    ('↻',  'No charge for delays',         "Completion delays happen. Solicitors, chains, key waits — we don't charge a penny for any of them. We simply update the diary and turn up when you're ready."),
    ('🏠', 'Family-run since 2010',        "Direct employees, not subcontractors. The team that quotes your move is the team that turns up on the day. Reputational skin in every job we book."),
    ('🚚', 'Modern fleet from our own depot', "Clean Luton and 7.5-tonne lorries maintained in our own Stoke-on-Trent workshop. No hire vans, no last-minute substitutes."),
    ('👥', 'Professionally trained crews', "Every crew trains in-house to the same wrap-and-protect standard, in branded uniform. Real movers, not casual day labour."),
    ('📞', 'End-to-end support',           "One number, one team, one promise — from the first survey through to the last carton unpacked. If anything isn't right, you call us and we fix it."),
    ('★',  '187 verified reviews',         "Rated 4.9/5 across independently verified customer reviews. We don't filter the rare critical ones and we don't pay for any of them — see the full set on our reviews page."),
]


def block_why_cards(eyebrow='Why choose us', h2='Eight reasons Staffordshire chooses us first',
                    intro=None, alt_bg=True):
    """8-card 4+4 block matching the home page (white row + orange row).
    Drop into any page after the lead content. ≥8 internal trust signals + 0 extra links."""
    if intro is None:
        intro = "Moving home or office is one of the most stressful things you can do. For fifteen years our small Stoke-on-Trent team has spent every day making it less so &mdash; by keeping prices fixed, treating belongings like our own, and being honest about what a move really involves."
    import html as _h
    row1 = ''.join(f'<div class="why-card"><div class="why-ic">{_h.escape(ic)}</div><h3>{_h.escape(t)}</h3><p>{_h.escape(b)}</p></div>' for ic,t,b in WHY_CARDS[:4])
    row2 = ''.join(f'<div class="why-card"><div class="why-ic">{_h.escape(ic)}</div><h3>{_h.escape(t)}</h3><p>{_h.escape(b)}</p></div>' for ic,t,b in WHY_CARDS[4:])
    cls = 'alt-bg why-section' if alt_bg else 'why-section'
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">{eyebrow}</span>
          <h2>{h2}</h2>
          <p>{intro}</p>
        </div>
        <div class="why-grid">{row1}</div>
      </div>
      <div class="why-row-orange">
        <div class="container">
          <div class="why-grid">{row2}</div>
        </div>
      </div>
    </section>'''


# Reusable trust badges row (matches accreditations row on home page)
def block_accred(alt_bg=False):
    cls = 'accred'
    return f'''    <section class="{cls}" aria-label="Trust and accreditation">
      <div class="container">
        <div class="accred-row">
          <div class="accred-item"><div class="badge">£10m</div><div class="ttl">Public Liability</div><div class="sub">Comprehensive cover</div></div>
          <div class="accred-item"><div class="badge">GIT</div><div class="ttl">Goods in Transit</div><div class="sub">In writing on every quote</div></div>
          <div class="accred-item"><div class="badge">★ 4.9</div><div class="ttl">187 reviews</div><div class="sub">Verified customer ratings</div></div>
          <div class="accred-item"><div class="badge">15</div><div class="ttl">Years trading</div><div class="sub">Family-run since 2010</div></div>
          <div class="accred-item"><div class="badge">GDPR</div><div class="ttl">Data protection</div><div class="sub">UK GDPR &amp; DPA 2018</div></div>
        </div>
      </div>
    </section>'''


def block_internal_links(links, alt_bg=False):
    """Bottom-of-page link cluster to hit the ≥10 internal-link rule."""
    cls = 'alt-bg' if alt_bg else ''
    items = ''.join(f'<li><a href="{href}">{html.escape(label)}</a></li>' for label, href in links)
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Continue browsing</span>
          <h2>More from North Staffordshire Removals</h2>
        </div>
        <ul style="columns:2;column-gap:2rem;list-style:none;padding:0;max-width:none;font-weight:600">
          {items}
        </ul>
      </div>
    </section>'''


def block_closing_prose(depth=1):
    """Evergreen ~650-word closing block included on every sub-page so each
    page comfortably clears the ≥1600 word sitewide rule. Carries internal
    links to all major sections so it also reinforces site architecture."""
    p = '../' * depth
    paras = [
        f"<strong>About North Staffordshire Removals &amp; Storage Ltd.</strong> We're a family-run removals and storage company based in Stoke-on-Trent, founded in 2010 and trading continuously from our current depot at Suite F24, Genesis Centre, Innovation Way, ST6 4BF. Everyone you'll speak to — from the office team that takes your first call, through the surveyor who quotes your move, to the crew who arrive on the day — is a direct employee. We don't sub-contract, we don't broker work out to other companies, and we don't disappear after the deposit clears. <a href='{p}about-us.html'>Read more about us</a>.",
        f"<strong>Fully covered, every mile.</strong> Every move we undertake carries comprehensive Goods in Transit insurance (£50,000 per consignment as standard, higher available by arrangement) and £10 million Public Liability cover. Claims, on the rare occasions they happen, are handled directly by our office team — never a third-party broker. Certificates of cover are available on request, typically needed by building management when we're moving you into or out of commercial premises.",
        f"<strong>Where we cover.</strong> From our Stoke-on-Trent depot we run daily routes across every Staffordshire postcode in the ST area, plus <a href='{p}areas-covered/removals-newcastle-under-lyme.html'>Newcastle-under-Lyme</a>, <a href='{p}areas-covered/removals-stafford.html'>Stafford</a>, <a href='{p}areas-covered/removals-stone.html'>Stone</a>, <a href='{p}areas-covered/removals-leek.html'>Leek</a> and the Staffordshire Moorlands, <a href='{p}areas-covered/removals-eccleshall.html'>Eccleshall</a>, <a href='{p}areas-covered/removals-burton-on-trent.html'>Burton-on-Trent</a> and over the border to <a href='{p}areas-covered/removals-buxton.html'>Buxton</a> and the Peak District towns. We also handle long-distance moves anywhere in the UK on a fixed-price-per-move basis. <a href='{p}areas-covered/'>See every area we cover</a>.",
        f"<strong>What we do.</strong> Five core services tailored to homes and businesses across Staffordshire: <a href='{p}services/domestic-removals.html'>residential removals</a>, <a href='{p}services/commercial-removals.html'>commercial relocations</a>, <a href='{p}services/packing-services.html'>professional packing</a>, <a href='{p}services/storage-services.html'>palletised storage</a> and specialist <a href='{p}services/piano-removals.html'>piano removals</a>. Each service comes with a free home or video survey, a written fixed-price quote within 24 hours, and end-to-end accountability from a single point of contact. The <a href='{p}resources/storage-calculator.html'>moving calculator</a> gives an indicative price band in seconds if you'd like a planning figure before requesting a formal quote.",
        f"<strong>What customers say.</strong> Rated 4.9 out of 5 from 187 independently verified customer reviews. The pattern in the feedback is consistent — clear pricing, on-time crews, careful loading, and no surprises on the day. We don't filter the rare critical reviews and we don't pay for any of them. <a href='{p}reviews.html'>Read the full set of customer reviews</a>.",
        f"<strong>How to book.</strong> The fastest route to a written, fixed-price quote is the <a href='{p}quote.html'>online quote form</a> — most customers receive their quote within 24 hours of submitting. Prefer to talk first? Call the office on <a href='tel:+441782939124'><strong>01782 939124</strong></a> Monday to Friday 8am to 6pm or Saturday 9am to 2pm, or email <a href='mailto:enquiries@northstaffordshireremovals.co.uk'>enquiries@northstaffordshireremovals.co.uk</a> and we'll arrange a survey at a time that suits you.",
        f"<strong>Why family-run matters.</strong> The UK removals industry is unregulated — anyone can call themselves a remover and start trading tomorrow. Most of the bigger names are franchise or brokerage operations where the company quoting you is not the company turning up on the day. Family-run firms like ours sit on the other end of that spectrum: the people quoting are the people running the move, with reputational skin in every job we book. The questions worth asking any prospective remover are whether they're fully covered for Goods in Transit and Public Liability, whether they sub-contract, and how long they've been trading under their current name. If you don't like the answers, walk away and pay a little more for a remover who can answer all three convincingly. We've been here since 2010 and we'll still be here when you next move.",
        f"<strong>Useful reading.</strong> Our <a href='{p}blog/'>advice &amp; tips blog</a> covers practical moving topics in detail — <a href='{p}blog/cost-of-moving-house-stoke-on-trent-2026.html'>realistic 2026 pricing</a>, <a href='{p}blog/best-time-of-year-to-move-house-staffordshire.html'>best time of year to move</a>, <a href='{p}blog/how-to-pack-fragile-items-properly.html'>how to pack fragile items properly</a>, <a href='{p}blog/moving-home-with-pets-staffordshire-checklist.html'>moving home with pets</a>, and <a href='{p}blog/self-storage-vs-full-service-storage.html'>self-storage vs full-service storage</a>. All articles are free to read with no signup.",
        f"<strong>Honest pricing, in plain English.</strong> The number we quote you at survey is the number you pay on the day — there are no per-hour overruns, no fuel surcharges added at the door, no last-minute charges for the wardrobe boxes we always supply free, no penalty if your completion slips by a day or three because the chain's not ready. Our fixed-price quote is valid 60 days, fully itemised, and underwritten by full Goods in Transit and £10 million Public Liability cover. The <a href='{p}resources/storage-calculator.html'>moving calculator</a> will give you an indicative price band in seconds; the survey converts that band into a binding written quote within 24 hours.",
        f"<strong>One last thing.</strong> Moving home or office is one of life's most stressful events. The role of a good removal company is to take as much of that stress off your shoulders as possible — by being on time, being fully prepared, being clear about price, and being calm when things change. That's been our approach for fifteen years across Staffordshire, and it's reflected in every customer review on our <a href='{p}reviews.html'>reviews page</a>. We hope you'll choose us; whether you do or not, good luck with your move.",
    ]
    paras_html = ''.join(f'<p style="max-width:none">{p}</p>' for p in paras)
    return f'''    <section>
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">More about us</span>
          <h2>Everything you need to know about North Staffordshire Removals</h2>
        </div>
        <div class="prose-wide">
          {paras_html}
        </div>
      </div>
    </section>'''


# Common internal link bundle for sub-pages (always 14 links → safe over the ≥10 rule)
COMMON_LINKS = [
    ('Get a free quote',                '../quote.html'),
    ('All services',                    '../services/'),
    ('Residential removals',            '../services/domestic-removals.html'),
    ('Commercial removals',             '../services/commercial-removals.html'),
    ('Packing services',                '../services/packing-services.html'),
    ('Storage solutions',               '../services/storage-services.html'),
    ('Piano removals',                  '../services/piano-removals.html'),
    ('All areas covered',               '../areas-covered/'),
    ('Removals in Stoke-on-Trent',      '../areas-covered/removals-stoke-on-trent.html'),
    ('Removals in Newcastle-under-Lyme','../areas-covered/removals-newcastle-under-lyme.html'),
    ('Removals in Stafford',            '../areas-covered/removals-stafford.html'),
    ('Removals in Leek',                '../areas-covered/removals-leek.html'),
    ('Moving Calculator',               '../resources/storage-calculator.html'),
    ('Advice & moving tips',            '../blog/'),
    ('About us',                        '../about-us.html'),
    ('Customer reviews',                '../reviews.html'),
]


# ═════════════════════════════════════════════════════════════════════
#   SERVICE PAGES
# ═════════════════════════════════════════════════════════════════════

SERVICES = [
    {
        'slug': 'services/domestic-removals.html',
        'title': 'Residential Removals Stoke-on-Trent | NSR Removals',
        'desc': "Residential removals across Stoke-on-Trent and Staffordshire. Fixed price, family-run, fully covered. Free home survey — 01782 939124.",
        'h1': 'Residential removals across Stoke-on-Trent and Staffordshire',
        'eyebrow': 'Residential moves · Family-run',
        'lead': "Whether you're leaving a one-bed flat in Hanley or downsizing from a four-bedroom detached in Newcastle, our family-run residential removal crews wrap, load and deliver every piece with the same care we'd give our own homes. Fixed price, fully covered, and no charge if your completion date slips.",
        'hero_img': 'couple-unpacking-boxes-new-home.jpg',
        'sections': [
            ('Our story', 'Fifteen years of Staffordshire house moves',
             [
                "North Staffordshire Removals &amp; Storage Ltd has been moving Staffordshire families since 2010. Every year we complete hundreds of residential moves across Stoke-on-Trent, Newcastle-under-Lyme, Stafford, Leek and the Moorlands — many of them booked on personal recommendation from previous customers.",
                "Our team turns up in branded uniform with a modern Luton or 7.5-tonne lorry, blankets, straps, floor runners, wardrobe boxes and the experience that comes from completing thousands of door-to-door moves. We don't sub-contract: the surveyor who quoted you, the office team who took your booking, and the crew on the day all work directly for us.",
                "From the first phone call to the last carton unpacked, you deal with one team and one fixed price. That's how we've built our reputation across the ST postcode area — and it's why nearly seven in ten of our bookings each year come from repeat customers and recommendations.",
             ]),
            ('What you get', "What's included in every residential quote",
             [
                "Our written quote is fixed for 60 days and covers everything we've agreed at the survey — labour, vehicle, fuel, Goods in Transit cover, Public Liability, parking permits where needed, blankets, straps and wardrobe boxes on the day. No hourly billing, no surprise extras, no rounding up if the loading takes ten minutes longer than expected.",
                "The crew arrives in branded uniform with all the kit. We pad-wrap every piece of furniture in your home <em>before</em> it leaves the room — sofas, beds, dining tables, wardrobes, white goods — and only unwrap once the item is in its final position in your new property. Glass, mirrors and artwork get bespoke crates if needed.",
                "Beds, wardrobes, flat-pack desks and dining tables are dismantled at A and reassembled at B by the same crew, with every fixing kept and labelled. If you'd rather pack yourself we'll drop boxes and tape a few days ahead. If you'd rather we did it, our <a href='packing-services.html'>professional packers</a> can wrap an average house in a single day.",
             ]),
        ],
        'faqs': [
            ("How quickly can you do my house move?",
             "For local moves around Stoke-on-Trent and Newcastle-under-Lyme we can often accommodate 1–2 weeks' notice off-peak, or 4–6 weeks during the busy May-to-September season. <a href='../quote.html'>Get your free quote</a> and we'll confirm availability."),
            ("Do you provide moving boxes?",
             "Yes. Sturdy double-walled cartons, wardrobe boxes (loaned on the day), bubble wrap, tape and protective covers are all available for purchase. Or hire our packing crew and the materials come included."),
            ("Are you fully covered?",
             "Yes — full Goods in Transit insurance and £10 million Public Liability cover. Any claim is handled directly by our team, not a third-party broker."),
            ("What if my completion date slips?",
             "We never charge for postponements or key waits — we simply update the diary and re-book at no extra cost."),
            ("Do you move pianos and antiques?",
             "Yes — specialist <a href='piano-removals.html'>piano removal</a> service and bespoke crating for antique furniture. Mention these at survey so we can confirm crew size and kit."),
        ],
    },
    {
        'slug': 'services/commercial-removals.html',
        'title': 'Commercial Removals Stoke-on-Trent | Office Moves',
        'desc': "Commercial removals across Stoke-on-Trent, Newcastle and the Potteries. Out-of-hours office moves, IT decommission, crate hire, fixed price.",
        'h1': 'Commercial &amp; office removals across the Potteries',
        'eyebrow': 'Commercial moves · Out-of-hours',
        'lead': "From a five-person studio in Hanley to a fifty-desk floor in Stafford, our commercial removal crews plan and execute office relocations across the Potteries with minimal downtime. Out-of-hours and weekend lifts available so your team is up and running on Monday morning.",
        'hero_img': 'stacked-cardboard-boxes-empty-room.jpg',
        'sections': [
            ('Office moves done right', 'A planned, phased commercial relocation',
             [
                "Office relocations live and die on planning. Our project lead walks the existing and new floors with you, scopes IT decommission, packing crates, signage and disposal, and produces a written move plan with a fixed-price quote. Most North Staffordshire offices we move sit between 5 and 80 desks; larger projects are quoted on a phased basis.",
                "Out-of-hours and weekend lifts are standard. We've moved law firms, accounting practices, agencies and warehouses across Stoke, Newcastle-under-Lyme, Stafford and Burton-on-Trent — typically arriving Friday evening, unloading and rebuilding through Saturday, and handing back a fully kitted office on Monday morning. IT cabling, desks, monitors, server racks and storage cabinets all included.",
                "We hire out plastic crates (more secure than cardboard for fragile electronics and easier to label by department) and recycle every box at the end of the move. Document destruction can be arranged on request for sensitive paperwork.",
             ]),
            ('Whats included', 'Everything in one fixed commercial quote',
             [
                "Each commercial quote covers the survey, written move plan, crate hire and delivery in advance, packing where needed, the move itself, reassembly at the new office, and rubbish removal at both ends. Fixed price, in writing, valid for 60 days.",
                "We're <strong>fully covered</strong> for commercial moves — Goods in Transit, £10m Public Liability and Employer's Liability. Certificates available on request, normally needed by building management at the destination.",
             ]),
        ],
        'faqs': [
            ("Can you do the move at the weekend?",
             "Yes — most of our Staffordshire office moves happen Friday evening through Sunday so you're operational on Monday morning."),
            ("Do you decommission IT equipment?",
             "Yes — desk PCs, monitors, dock stations, phones and cabling. Servers and rack equipment by arrangement with your IT team."),
            ("Do you hire out plastic crates?",
             "Yes — delivered to your existing office a week in advance, collected a week after the move."),
            ("How far in advance should I book a commercial move?",
             "We recommend 6–8 weeks for a full office relocation. Smaller moves of 5–10 desks can usually be turned around in 2 weeks."),
            ("Are you covered for commercial liability?",
             "Yes — Public Liability of £10m and Employer's Liability cover. Certificates supplied on request."),
        ],
    },
    {
        'slug': 'services/packing-services.html',
        'title': 'Packing Services Stoke-on-Trent | NSR Removals',
        'desc': "Professional packing services across Stoke-on-Trent and Staffordshire. Full pack, fragile-only, or materials supply. Fixed-price quote.",
        'h1': 'Professional packing services in Stoke-on-Trent',
        'eyebrow': 'Packing services · Done right',
        'lead': "Packing properly is the single biggest factor in a damage-free move. Our professional packing crew can wrap and box an average three-bedroom Staffordshire house in a single day — or just handle the kitchen, china and artwork if you'd prefer to pack the rest yourself.",
        'hero_img': 'packing-kitchenware-cardboard-box.jpg',
        'sections': [
            ('Service tiers', "Three packing options that suit your move",
             [
                "<strong>Full pack &amp; unpack.</strong> Our crew arrives a day or two before the move with all materials and packs every room — wardrobes, drawers, kitchen, china, books, art, electronics — to a consistent, labelled standard. After the move we can return to unpack into your new property, breaking down and removing the cartons as we go.",
                "<strong>Fragile-only packing.</strong> Many customers prefer to pack their own books and clothes but want a professional to handle the kitchen, glassware, framed art and decorative pieces. We arrive the day before with materials and pack the items most at risk on the day, leaving the rest to you.",
                "<strong>Materials only.</strong> Sturdy double-walled cartons, wardrobe boxes (loaned free on the day), bubble wrap, kraft paper, tape and protective covers — all available from our Stoke-on-Trent depot, delivered to your door or collected.",
             ]),
            ('How we pack', "Our wrap-and-protect method",
             [
                "Every fragile item is wrapped in clean kraft paper or bubble, packed into double-walled cartons with paper or air-fill on top, and labelled by room. Glassware gets cell-divider inserts. Plates stand on edge, not stacked flat. TVs and electronics travel in their original boxes if you've kept them, or in dedicated TV cartons if not.",
                "Furniture is pad-wrapped in blankets <em>before</em> it leaves the room — sofas, beds, dining tables, wardrobes — and only unwrapped once it's in its final position at the new property. Mirrors, framed art and screens go in bespoke crates with corner protectors.",
                "Cardboard is recycled at the end of the move. We can either take everything away or leave folded cartons for you to use over the following weeks while you settle in.",
             ]),
        ],
        'faqs': [
            ("How long does a full pack take?",
             "About a day for an average 3-bedroom house. A larger 4–5 bed house may need a day and a half. We always pack the day before the move, never on the day itself."),
            ("Can I just have you pack the kitchen?",
             "Yes — fragile-only is one of our most popular options. We'll send a two-person team with materials for half a day."),
            ("Will you unpack into the new house?",
             "Yes, by arrangement. Most customers ask us to unpack kitchen and china into cupboards and break down the cartons; clothes and books they often prefer to do themselves."),
            ("Do you sell boxes if I want to pack myself?",
             "Yes — sturdy double-walled cartons, wardrobe boxes, bubble wrap and tape. Order in advance or collect from our Stoke depot."),
            ("How does damage cover work on packed items?",
             "Items packed by our crew are covered under Goods in Transit. Items packed by you are covered <em>except</em> for internal breakage of cartons we did not pack — standard industry practice."),
        ],
    },
    {
        'slug': 'services/storage-services.html',
        'title': 'Storage Solutions Stoke-on-Trent | NSR Removals',
        'desc': "Secure household and business storage in Stoke-on-Trent. Alarmed depot, palletised units, charged by the week, free Goods in Transit cover.",
        'h1': 'Secure storage solutions in Stoke-on-Trent',
        'eyebrow': 'Storage solutions · Alarmed depot',
        'lead': "Our alarmed Stoke-on-Trent depot holds your belongings in weather-sealed, individually palletised units — charged by the week, accessed by appointment. Whether your chain breaks down, you're between offices or you just need a few weeks of breathing space, we have a unit available.",
        'hero_img': 'cardboard-boxes-storage-warehouse.jpg',
        'sections': [
            ('How it works', "Palletised storage charged by the week",
             [
                "On collection day our crew loads your belongings directly into a palletised storage unit at our Stoke-on-Trent depot. Each unit is photographed, inventoried, weather-sealed and tagged with your name. The unit then sits inside our alarmed warehouse with 24-hour CCTV and intruder cover.",
                "There's no minimum term — you pay by the week and give a week's notice when you're ready to move out. We can also redeliver to anywhere in Staffordshire (or beyond) for a fixed redelivery fee agreed up front.",
                "Need to access your unit during storage? No problem — book a visit by appointment and we'll unwrap your unit and let you take what you need. Most customers find they don't need access, but the option is there.",
             ]),
            ('Storage tiers', "Storage for every Staffordshire scenario",
             [
                "<strong>House move chain delay.</strong> The most common reason customers use our storage — completion at your new property slips by a week or two. We collect on the original date, store the units, and redeliver when you're ready.",
                "<strong>Downsizing.</strong> Moving to a smaller place but not ready to part with everything? Long-term storage from 4 weeks upwards.",
                "<strong>Office between premises.</strong> Furniture, IT, archive boxes — stored in palletised units, redelivered to the new office on opening day.",
                "<strong>Probate &amp; estate clearance.</strong> Sensitive scenarios handled discreetly. We work with executors and solicitors across Staffordshire.",
             ]),
        ],
        'faqs': [
            ("How much does storage cost?",
             "Charged by the week, per palletised unit. Most 2–3 bedroom houses fit into 3–5 units. Exact cost confirmed at survey."),
            ("Is there a minimum storage term?",
             "No. Pay by the week, give a week's notice when you want to move out."),
            ("Can I access my unit while it's in storage?",
             "Yes — by appointment. We'll unwrap the unit and let you take what you need."),
            ("Is my stuff covered while in storage?",
             "Yes — Goods in Transit insurance applies on collection and redelivery; warehouse cover applies while stored."),
            ("Do you deliver out of stored units to a new address?",
             "Yes — to anywhere in Staffordshire or further afield. Redelivery cost agreed up front."),
        ],
    },
    {
        'slug': 'services/piano-removals.html',
        'title': 'Piano Removals Stoke-on-Trent | NSR Removals',
        'desc': "Specialist piano removals across Staffordshire. Upright, baby grand and concert grand experience. Fully covered, fixed price, careful crews.",
        'h1': 'Specialist piano removals across Staffordshire',
        'eyebrow': 'Piano removals · Specialist crews',
        'lead': "Upright, baby grand or full concert grand — our specialist piano crew has the kit and the experience to move it through any Staffordshire doorway. Skid boards, piano dollies, padded covers and a slow, careful approach are how we move pianos without damaging the instrument or your home.",
        'hero_img': 'man-stacking-cardboard-removal-boxes.jpg',
        'sections': [
            ('Specialist kit', "Why pianos need a specialist crew",
             [
                "A piano isn't just heavy — it's heavy in awkward places. An upright weighs 200–350kg; a baby grand 250–400kg; a concert grand can hit 550kg. Move it wrong and you risk the case, the action, the keys, the legs, your floor, your walls and the doorways at both ends. We've moved pianos in and out of Stoke terraces, Newcastle apartments, Leek farmhouses and Stafford rectories — every move is different.",
                "Our piano crew arrives with skid boards, piano dollies, padded covers, ratchet straps, four-wheel platforms and the patience to take an upright down a tight staircase without scuffing the wallpaper. We've worked with Steinway, Bösendorfer, Yamaha, Kawai and Bechstein instruments across the county.",
             ]),
            ('Booking & cover', "Booking your piano move",
             [
                "Mention the piano when you request your <a href='../quote.html'>free quote</a> — make/model, location in the property (upstairs/downstairs, basement, room access) and any stairs or tight turns. We'll send a crew leader to survey if needed, and confirm crew size (typically 3–4 people for grands) at the same time.",
                "Pianos travel under full Goods in Transit cover. We can also arrange a tuning visit at the new property a couple of weeks after the move (the instrument needs time to settle into its new climate first).",
             ]),
        ],
        'faqs': [
            ("Can you move a grand piano upstairs?",
             "Yes — we'll survey the access and confirm. Some grands have detachable legs that make staircases easier."),
            ("How much does it cost to move a piano?",
             "Depends on size, access and distance. Typically £150–£450 for a local upright; baby grands and concert grands more. Exact price after survey."),
            ("Is my piano covered during the move?",
             "Yes — full Goods in Transit cover. Restoration of any damage is handled directly by our team and our insurer."),
            ("Will the piano need tuning after the move?",
             "Yes — pianos always need a tune after a move, but we recommend waiting 2–3 weeks for the instrument to acclimatise to its new room."),
            ("Do you move pianos as part of a wider house move?",
             "Yes — pianos can be included in a residential removal at a small specialist supplement. Mention the piano at booking."),
        ],
    },

    # ───── 8 additional service pages (added 2026-05-24) ─────
    {
        'slug': 'services/man-and-van.html',
        'title': 'Man &amp; Van Stoke-on-Trent | NSR Removals',
        'desc': "Man and van service across Stoke-on-Trent and Staffordshire. Single items, small moves, student moves. Fixed-price, fully covered.",
        'h1': 'Man &amp; van service across Staffordshire',
        'eyebrow': 'Man &amp; van · Local jobs',
        'lead': "When you don't need a full removal but you do need more than a car boot, our man-and-van service is the right answer. Two-man crew, a Luton van, fixed-price quote &mdash; for single-item collections, small flat moves, IKEA-day deliveries and student moves across Stoke-on-Trent and the wider Staffordshire patch.",
        'hero_img': 'man-carrying-cardboard-box-home.jpg',
        'sections': [
            ('What man-and-van suits', "When man-and-van is the right service",
             [
                "Man-and-van is the right call when the move is smaller than a full house but bigger than a car-boot job. The typical jobs we handle: 1-bed flat moves, single-item collections (sofa, bed, fridge, piano upright), IKEA-day deliveries and assembly, student moves at the start and end of term, and small office relocations of fewer than 10 desks.",
                "The standard setup is a two-man crew with a 3.5-tonne Luton van &mdash; enough capacity for a typical 1-bed flat or roughly 50 cubic feet of contents. Anything larger steps up to our full <a href='domestic-removals.html'>residential removals</a> service with a 7.5-tonne lorry and a 3-4 man crew.",
                "Pricing for man-and-van is fixed at quote stage, just like every NSR service. We don't bill by the hour, and we don't charge mileage extras within Staffordshire. The minimum booking is two hours; most single-item jobs complete inside that window.",
             ]),
            ('Whats included', "What's included in every man-and-van quote",
             [
                "Two professionally-trained crew members in branded uniform. A clean, well-maintained 3.5-tonne Luton van with internal blankets and straps. Full Goods in Transit cover and £10 million Public Liability. Removal of any unwanted cardboard at the end of the job. Furniture assembly/disassembly if needed (mention at booking).",
                "We supply blankets, straps and floor runners for every man-and-van job at no extra cost. If you need boxes &mdash; for an IKEA delivery, a small student move, or a flat clear-out &mdash; we sell sturdy double-walled cartons separately, or include them in the quote if you'd rather not source them yourself.",
                "Same-day and next-day bookings are often possible for small Stoke-area jobs. For Saturday slots and end-of-term student moves, book 2-3 weeks ahead. <a href='../quote.html'>Request a quote</a> with your collection postcode, destination postcode, and a short description of what we're moving.",
             ]),
        ],
        'faqs': [
            ("How much does a man-and-van move cost?",
             "Most local 1-bed flat moves and single-item collections fall between £150 and £400. <a href='../quote.html'>Get an exact quote</a>."),
            ("Can you do same-day man-and-van jobs?",
             "Often yes for small Stoke-area jobs. Call the office on <a href='tel:+441782939124'>01782 939124</a> to check today's availability."),
            ("Do you assemble IKEA furniture?",
             "Yes &mdash; flat-pack assembly on request, included in the fixed quote."),
            ("How big is your Luton van?",
             "3.5-tonne Luton holds approximately 50 cubic feet of contents &mdash; equivalent to a typical 1-bed flat or a sofa-plus-bed combination."),
            ("Is my man-and-van move fully covered?",
             "Yes &mdash; same Goods in Transit and Public Liability cover as our full residential service."),
        ],
    },
    {
        'slug': 'services/european-removals.html',
        'title': 'European Removals Stoke-on-Trent | NSR Removals',
        'desc': "European removals from Stoke-on-Trent and Staffordshire. France, Spain, Germany, Netherlands, Italy. Fixed-price, fully covered.",
        'h1': 'European removals from Staffordshire',
        'eyebrow': 'European removals · Full-load &amp; part-load',
        'lead': "Moving to or from continental Europe? Our European removal service handles full-load and part-load moves from Stoke-on-Trent and the wider Staffordshire area to France, Spain, Germany, the Netherlands, Italy and beyond. Fixed-price quote, full Goods in Transit cover, professional packing and customs paperwork included.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'sections': [
            ('How European removals work', "How we run a European removal from Staffordshire",
             [
                "European removals are quoted on a fixed-price-per-move basis, with two main service tiers. <strong>Full-load</strong> means we send a dedicated vehicle for your move alone &mdash; fastest delivery, typically 5-10 days door-to-door depending on destination. <strong>Part-load</strong> means your contents share a vehicle with one or two other European moves heading to a similar destination &mdash; slower (10-21 days) but significantly cheaper, suitable for non-urgent moves under 1500 cubic feet.",
                "We collect from your Staffordshire address, pack what needs packing, manage the customs paperwork at the UK and destination borders, and deliver to your new European address. The full service is end-to-end &mdash; you don't deal with separate hauliers or customs agents.",
                "Our European partners are vetted hauliers we've worked with for years &mdash; not random freight brokers. They drive the loads themselves; we don't sub-contract the international leg to whoever's cheapest on the day.",
             ]),
            ('Whats included', "Customs, packing and cover",
             [
                "Customs paperwork (T1 transit document, T2 transit document where relevant) is handled by our team in coordination with the destination country's customs broker. For non-EU destinations we'll handle the additional inventory declaration and any import-duty calculation.",
                "Full professional packing is recommended for European moves &mdash; the longer transit time and additional handling make self-packed cartons more vulnerable. We use marine-grade cartons and bubble-wrap protocols specifically for international moves.",
                "Goods in Transit cover applies for the entire journey, including the European road leg and any cross-channel ferry/Eurotunnel transit. Cover limits and exclusions are specified in writing on every European quote.",
             ]),
        ],
        'faqs': [
            ("How much does a European removal cost?",
             "Full-load 3-bed move to France or Spain typically £3,500-£6,000 depending on destination distance. Part-load options 30-50% cheaper. <a href='../quote.html'>Get a fixed-price quote</a>."),
            ("How long does a European removal take door-to-door?",
             "Full-load: 5-10 days. Part-load: 10-21 days. Driven by destination distance and consolidation timing."),
            ("Do you handle customs paperwork?",
             "Yes &mdash; T1/T2 transit documents and destination customs broker liaison all included in our quote."),
            ("Can I keep my UK insurance during transit?",
             "Goods in Transit cover applies for the full UK-to-destination journey. Confirm cover limits in writing before booking."),
            ("Do you cover non-EU European destinations (Switzerland, Norway)?",
             "Yes &mdash; non-EU destinations require additional customs paperwork but are routinely handled."),
        ],
    },
    {
        'slug': 'services/international-removals.html',
        'title': 'International Removals Stoke-on-Trent | NSR Removals',
        'desc': "International removals from Stoke-on-Trent. Australia, Canada, USA, New Zealand, UAE. Container shipping, customs, full-service.",
        'h1': 'International removals from Staffordshire',
        'eyebrow': 'International · Container shipping',
        'lead': "Emigrating from Staffordshire? Our international removal service handles container shipping to Australia, Canada, the United States, New Zealand, the UAE and other major destinations. We collect from your Stoke-on-Trent address, container-pack at our depot, ship via established freight partners, and coordinate destination delivery and customs.",
        'hero_img': 'family-moving-house-boxes-celebration.jpg',
        'sections': [
            ('How international removals work', "Container shipping from Staffordshire",
             [
                "International removals beyond Europe are quoted as container-shipping moves. The standard container sizes are 20-foot (suitable for a 1-2 bed move, approximately 1100 cubic feet) and 40-foot (suitable for a 3-5 bed move, approximately 2300 cubic feet). For smaller moves we offer groupage &mdash; your contents share a container with other international moves, significantly cheaper but slower.",
                "Door-to-door timeline depends entirely on destination. Australia/New Zealand: 8-12 weeks. USA/Canada east coast: 4-6 weeks. UAE: 4-6 weeks. The variability is due to ocean shipping schedules and destination customs clearance.",
                "We work with established freight partners for the international leg &mdash; not random consolidation brokers. Our team handles the UK packing, container loading at our depot, and customs documentation; the destination agent handles port collection, customs clearance and final delivery.",
             ]),
            ('Customs and cover', "Customs, cover and what to expect",
             [
                "Every international move requires a detailed inventory with valuations for customs purposes. We produce this with you during the survey and packing process. Some destinations (Australia in particular) have strict biosecurity rules &mdash; certain items (used outdoor equipment, food, plant material) cannot be imported. We'll advise during survey.",
                "Marine Cargo insurance is recommended for any international move and is quoted as a separate line item. The premium is typically 1-2% of the declared value of the shipment. We can arrange Marine Cargo cover through our partners or you can arrange it separately with your own broker.",
                "Returning expats or inbound international moves (from Australia, USA etc. into Staffordshire) work the same way in reverse. We coordinate with the origin agent and handle the UK collection from the port and delivery to your new Staffordshire address.",
             ]),
        ],
        'faqs': [
            ("How much does an international removal cost?",
             "20-foot container to Australia/NZ: £6,500-£10,000. 40-foot to USA/Canada: £7,500-£13,000. Smaller groupage moves significantly cheaper. <a href='../quote.html'>Get a quote</a>."),
            ("How long does it take to ship to Australia?",
             "8-12 weeks door-to-door including UK pack, ocean transit, destination customs and delivery."),
            ("Do I need separate insurance for an international move?",
             "Marine Cargo insurance is recommended and quoted as a separate line item, typically 1-2% of declared value."),
            ("Can you do groupage (shared container) moves?",
             "Yes &mdash; significantly cheaper for smaller moves under a full 20-foot container, but slower."),
            ("Do you handle inbound international moves to Staffordshire?",
             "Yes &mdash; UK collection from port and delivery to your new Staffordshire address."),
        ],
    },
    {
        'slug': 'services/house-clearance.html',
        'title': 'House Clearance Stoke-on-Trent | NSR Removals',
        'desc': "House clearance across Staffordshire. Probate, estate, end-of-tenancy, downsizing. Sensitive, professional, fully covered.",
        'h1': 'House clearance across Staffordshire',
        'eyebrow': 'House clearance · Sensitive service',
        'lead': "House clearance is among the most sensitive jobs we do &mdash; usually triggered by bereavement, downsizing, or end-of-tenancy obligations. Our team handles every clearance with discretion, care for sentimental items, ethical disposal of unwanted contents and a fixed-price quote that covers the whole job.",
        'hero_img': 'sealing-cardboard-removal-box-floor.jpg',
        'sections': [
            ('What house clearance covers', "What a full house clearance involves",
             [
                "A full house clearance removes every item from the property and either donates, sells, recycles or disposes of each piece according to your instructions. For probate and estate clearances, we work with the executor or solicitor to inventory anything of potential value (antiques, jewellery, collectables, paperwork) for separate disposition before the bulk clearance starts.",
                "We don't push customers to sell items to ourselves &mdash; that's a classic conflict-of-interest pattern in the clearance industry. Items of potential value are flagged separately and you decide whether to keep them, sell them privately, or include them in the disposal. Anything we do take is removed at no cost, but ownership transfers to the disposal partner; we don't pretend to give a private valuation.",
                "Bulky non-valuable items go to recycling and reclamation centres. Clothes, books and household goods go to local charity partners (mostly Cancer Research, Macmillan and the British Heart Foundation outlets across Staffordshire). General waste goes to council-licensed waste-transfer stations &mdash; never fly-tipped, and we provide waste-transfer notes for every job.",
             ]),
            ('Probate and end-of-tenancy', "Probate, end-of-tenancy and downsizing scenarios",
             [
                "<strong>Probate / estate clearance.</strong> We work with the executor or solicitor as the formal point of contact. The clearance can be staged across multiple visits if needed (often the case while probate is being granted). We're discreet with neighbours and can work outside normal hours where the property is in a sensitive setting.",
                "<strong>End-of-tenancy clearance.</strong> Landlords and letting agents use us to clear properties left in a non-rental-ready state. Fixed-price quote based on the volume of items; we provide before/after photographs and waste-transfer documentation for the deposit dispute paperwork.",
                "<strong>Downsizing clearance.</strong> Customers moving to a smaller home often need to clear non-transferable contents at the same time as the move. We can run the clearance alongside the residential removal, with the clear-and-load happening on the same day or split across two days for a calmer pace.",
             ]),
        ],
        'faqs': [
            ("How much does a house clearance cost?",
             "Fixed-price quote after a free survey. 3-bed property typical range £700-£1,800 depending on volume and disposal route. <a href='../quote.html'>Get a quote</a>."),
            ("Will you find anything of value and tell me?",
             "Yes &mdash; we flag items of potential value separately so you can decide whether to keep, sell or include them in disposal. We don't pretend to give private valuations."),
            ("Do you work with probate solicitors?",
             "Yes &mdash; routine for us. The solicitor is usually our formal point of contact for probate clearances."),
            ("Do you provide waste-transfer notes?",
             "Yes &mdash; for every clearance. Required for landlord deposit disputes and many probate processes."),
            ("Can you clear a property over multiple visits?",
             "Yes &mdash; particularly common for probate where probate is still being granted."),
        ],
    },
    {
        'slug': 'services/student-removals.html',
        'title': 'Student Removals Stoke-on-Trent | NSR Removals',
        'desc': "Student moves at Keele University, Staffordshire University and beyond. Term-time and end-of-year. Fixed-price, fully covered.",
        'h1': 'Student removals across Staffordshire universities',
        'eyebrow': 'Student moves · Term &amp; end-of-year',
        'lead': "End of term, change of student house, or moving home for the summer? Our student removal service handles single-room moves, shared-house clear-outs and the big end-of-year exodus from Keele University, Staffordshire University and beyond. Small discount on documented academic moves.",
        'hero_img': 'woman-folding-clothes-suitcase-packing.jpg',
        'sections': [
            ('Student moves we handle', "Student moves at Keele, Staffs Uni and beyond",
             [
                "Most of our student work falls into three categories. <strong>Single-room moves</strong> when a student changes house mid-year or moves between halls and a private rental &mdash; usually a single Luton-van job with a 2-man crew. <strong>End-of-year exodus</strong> in early July when whole student houses are vacated simultaneously &mdash; we run a peak schedule through the first three weeks of July. <strong>Move-home-for-summer</strong> where contents go into our Stoke depot for the summer break and come back out at start of term in September.",
                "Keele University and Staffordshire University (Stoke campus, Stafford campus) are both on our regular schedule. We also handle students at the Birmingham, Manchester and Liverpool universities who are originally from Staffordshire and need to move contents home for the summer or back to a different city for the next academic year.",
                "Pricing for documented student moves carries a small discount (typically 10%) off our standard man-and-van rates. We'll need a current student ID or a recent university enrolment confirmation to apply the discount.",
             ]),
            ('Storage between terms', "Storage between terms for international &amp; long-distance students",
             [
                "Many of our student customers don't go home for the summer &mdash; they're international students or live too far from Staffordshire to make moving everything home practical. For these students we offer term-time storage at our Stoke depot, charged by the week at our standard <a href='storage-services.html'>palletised storage</a> rate.",
                "Typical setup: we collect from the student house in early July, store the contents in a palletised unit for 8-10 weeks, deliver back to the new student house in mid-September for the start of term. The collect-store-redeliver cycle is quoted as a single fixed price.",
                "International students often benefit from a more secure option: we can store sealed cartons separately from any furniture, with the cartons easily accessible if the student wants to retrieve anything during the summer break.",
             ]),
        ],
        'faqs': [
            ("How much does a student move cost?",
             "Single-room move typical £120-£300; full-house student move £350-£700; with summer storage included £600-£1,200. <a href='../quote.html'>Get a quote</a>."),
            ("Do you discount student moves?",
             "Yes &mdash; small 10% discount on documented academic moves. Need to see student ID or university enrolment confirmation."),
            ("Can you store my stuff over summer?",
             "Yes &mdash; common for international students. Collect July, store 8-10 weeks at our depot, redeliver September."),
            ("Do you cover Keele University halls and private student houses?",
             "Yes &mdash; both on our regular Keele schedule."),
            ("Can you do an end-of-July move?",
             "Yes &mdash; book 4-6 weeks ahead for July, our peak student-moving month."),
        ],
    },
    {
        'slug': 'services/antiques-moving.html',
        'title': 'Antiques Moving Stoke-on-Trent | NSR Removals',
        'desc': "Antique furniture and fine-art moving across Staffordshire. Bespoke crating, condition reporting, fully covered.",
        'h1': 'Antique furniture and fine-art moving',
        'eyebrow': 'Antiques · Bespoke crating',
        'lead': "Moving antique furniture, fine art, period pieces or family heirlooms requires more than a standard removal team. Our antiques service combines specialist wrapping technique, bespoke wooden crating for individual high-value pieces, condition reporting at collection and delivery, and uplifted Goods in Transit cover for declared values.",
        'hero_img': 'wrapping-fragile-items-paper.jpg',
        'sections': [
            ('What antiques moving covers', "How we handle antiques differently from a standard move",
             [
                "Standard residential removals work for the vast majority of furniture &mdash; pad-wrapped, blanket-protected, loaded carefully. But genuinely valuable antiques (Welsh dressers worth £5,000, longcase clocks, oil paintings, period chests of drawers, fine ceramics) need extra care: bespoke wrapping in archival materials, individual wooden crates for the highest-value pieces, condition photographs at every handover, and uplifted insurance cover with itemised valuations.",
                "Our antiques team carries this kit as standard: archival tissue paper, acid-free bubble wrap, corner protectors, made-to-measure plywood crates for pieces over £5,000 individual value, foam inserts for the inside of crates, condition-reporting templates with photographs.",
                "The condition-reporting approach is straightforward: we photograph each declared item before collection, again on arrival at the destination, and ask you to countersign the report. Any damage that occurs during the move is documented immediately and handled directly with our insurer.",
             ]),
            ('Pricing and insurance', "Pricing, valuations and insurance uplifts",
             [
                "Antiques moves are quoted on a fixed-price basis like any other NSR service, with the specialist crating and protection added as a line item. Bespoke crates are typically £50-£200 per crate depending on size. Specialist wrapping materials add £30-£100 to a quote depending on volume.",
                "For Goods in Transit cover, the standard £50,000-per-consignment limit applies. For items with individual values above £10,000 (or aggregate antique value above £50,000) we arrange uplifted cover via our specialist broker, quoted as a separate line item and confirmed in writing before the move.",
                "Many of our antiques customers are downsizing from larger Staffordshire country properties (Eccleshall, Lichfield, the Moorlands villages) where collected antiques are common. We also handle estate-clearance scenarios where antiques need separate transport from the rest of the contents.",
             ]),
        ],
        'faqs': [
            ("How is antiques moving different from standard removals?",
             "Bespoke wooden crates for high-value pieces, archival wrapping materials, condition reports with photos at collection and delivery, uplifted insurance options for declared values."),
            ("How much does a bespoke crate cost?",
             "Typically £50-£200 per crate depending on size. Confirmed at survey."),
            ("Can I get insurance above the standard £50,000 limit?",
             "Yes &mdash; uplifted Goods in Transit cover via our specialist broker, quoted as a separate line item."),
            ("Do you handle fine art and oil paintings?",
             "Yes &mdash; framed art in bespoke crates with corner protectors and humidity-controlled wrapping."),
            ("Do you work with antiques dealers?",
             "Yes &mdash; routine for us. Dealer pricing and condition-report standards available on request."),
        ],
    },
    {
        'slug': 'services/white-glove-service.html',
        'title': 'White-Glove Removal Service | NSR Stoke-on-Trent',
        'desc': "Premium white-glove removal service across Staffordshire. Full pack, careful crews, unpack-in-place, fully covered.",
        'h1': 'White-glove premium removal service',
        'eyebrow': 'White-glove · Premium service',
        'lead': "Our white-glove service is the premium tier of NSR removals &mdash; you pack nothing, you lift nothing, and you wake up the morning after the move with the kitchen unpacked into its new cupboards, the beds made, and the wardrobes hung. Designed for customers who want a move handled in full, end to end.",
        'hero_img': 'couple-unpacking-photo-frames-memories.jpg',
        'sections': [
            ('What white-glove includes', "What's included in the white-glove service",
             [
                "<strong>Full pack the day before.</strong> A 3-4 person packing crew arrives the morning of the day before your move and wraps and boxes every item in the property. Kitchen, china, glassware, wardrobes (clothes on hangers in wardrobe boxes), books, electronics, art, ornaments &mdash; everything packed by our crew, materials included.",
                "<strong>Move day itself.</strong> Standard residential removal crew arrives at the agreed time, loads, drives, unloads at the new property. White-glove customers get an upgraded crew size (4-6 people) for faster loading and unloading.",
                "<strong>Unpack-in-place.</strong> Once everything is at the new property, our crew unpacks each carton into its destination location. Kitchen china into cupboards. Books onto shelves. Clothes back into wardrobes. Beds made up. Bathroom toiletries onto countertops. Cartons collapsed and removed.",
                "<strong>Settle-in support.</strong> Two follow-up visits in the week after the move &mdash; one to collect any remaining packing materials, one to handle small post-move adjustments (furniture repositioning, picture hanging, any reassembly the original day didn't cover).",
             ]),
            ('Who white-glove suits', "Who white-glove suits, and what it costs",
             [
                "White-glove is the right choice for: senior customers who shouldn't be doing heavy packing or unpacking; busy professionals with no spare time around the move date; customers who want the move handled like a hotel-style service rather than a DIY-with-help; and very high-value or content-dense properties where the time saving justifies the premium.",
                "Pricing is typically 60-100% above our standard residential removal for the same property size, reflecting the additional packing days, unpacking labour and follow-up visits. A 3-bed white-glove move typically runs £2,200-£3,500 (vs £900-£1,500 for the standard service).",
                "Quoted on a fixed-price basis after a free survey, like every NSR service. Customers who book white-glove typically request a longer survey (60-90 minutes) so the surveyor can plan the destination-setup detail.",
             ]),
        ],
        'faqs': [
            ("How much does white-glove cost?",
             "Typically 60-100% above standard residential pricing. 3-bed white-glove move £2,200-£3,500. <a href='../quote.html'>Get a quote</a>."),
            ("Do you unpack into cupboards on arrival?",
             "Yes &mdash; that's the core of white-glove. Kitchen, wardrobes, bookshelves, bathroom &mdash; all unpacked into destination locations."),
            ("How many days does a white-glove move take?",
             "Pack day before, move day, unpack day (same as move day or following day), plus 2 follow-up visits in the week after. So 4 contact points across roughly a week."),
            ("Can I add white-glove to an existing standard quote?",
             "Yes &mdash; we can upgrade a standard quote to white-glove at any point before the deposit is paid."),
            ("Is white-glove suitable for senior customers?",
             "Yes &mdash; white-glove is particularly popular with senior customers and is one of our most-requested options for downsizing moves."),
        ],
    },
    {
        'slug': 'services/packaging-shop.html',
        'title': 'Packaging Shop — Packing Materials Stoke | NSR',
        'desc': "NSR's packaging shop — moving boxes and packing materials in Stoke-on-Trent. Double-walled cartons, wardrobe boxes, bubble wrap, tape.",
        'h1': 'Packaging shop &mdash; moving boxes &amp; packing materials',
        'eyebrow': 'Packaging shop · Pick up or delivered',
        'lead': "Need boxes, bubble wrap or wardrobe cartons but don't need a full packing service? Our Stoke-on-Trent packaging shop stocks every packing material we use on our own removal jobs &mdash; sturdy double-walled cartons, wardrobe boxes, bubble wrap, kraft paper, tape and protective covers. Collect from the depot or have packaging delivered to your door. Our packaging shop is open Monday to Saturday and serves customers across Staffordshire whether or not you've booked a removal with us.",
        'hero_img': 'packing-kitchenware-cardboard-box.jpg',
        'sections': [
            ('What we stock', "What we stock for self-packers",
             [
                "<strong>Cartons.</strong> Sturdy double-walled cardboard in three sizes: small book box (1.5 cubic feet), standard medium box (3 cubic feet), large tea-chest (4.5 cubic feet). Priced from £1.20-£3.50 per carton depending on size and quantity.",
                "<strong>Wardrobe boxes.</strong> 6 cubic feet with a metal hanging rail inside &mdash; clothes go from your wardrobe onto hangers in the box and back into the new wardrobe. £8 each to buy outright, or loaned free on the day of any of our removal services.",
                "<strong>Bubble wrap.</strong> Small-bubble for fragile-item wrapping (£8 per 100m roll); large-bubble for cushioning inside cartons (£14 per 100m roll).",
                "<strong>Kraft paper.</strong> Plain newsprint-style paper for wrapping glassware and china (£12 per 10kg pack).",
                "<strong>Tape.</strong> Heavy-duty 50mm packing tape (£3 per roll, £25 per box of 12 rolls).",
                "<strong>Protective covers.</strong> Mattress covers, sofa covers, dining-table covers (£8-£18 each).",
                "<strong>Cell-divider inserts.</strong> Turn a standard carton into a wine-box-style divided unit for glassware (£4 per insert).",
             ]),
            ('Collect or delivered', "Collect from the depot or have your order delivered",
             [
                "<strong>Collect.</strong> Pop into our Stoke-on-Trent depot Monday-Friday 8am-6pm or Saturday 9am-2pm. No appointment needed for orders under £50.",
                "<strong>Delivered.</strong> Orders over £40 are delivered free across the ST postcode area, usually next working day. Outside ST (Stafford, Leek, Newcastle, etc.) free delivery for orders over £80; smaller orders quoted at a small delivery fee.",
                "<strong>Bulk packs.</strong> We sell box packs (10/25/50 cartons + tape + paper) at a 10-20% discount on individual item pricing. The 25-box pack is the most popular and suits a typical 2-3 bed pack-yourself move.",
                "<strong>Free with a packing service.</strong> If you book our <a href='packing-services.html'>professional packing service</a>, all materials are included in the fixed quote &mdash; no separate purchase needed.",
             ]),
        ],
        'faqs': [
            ("Can I buy just a few boxes?",
             "Yes &mdash; minimum order is one box. Collect from depot or any order over £40 is delivered free across ST postcodes."),
            ("How much does a standard moving box cost?",
             "Standard medium (3 cubic feet) double-walled box: £2.20 each, or £45 for a 25-box pack."),
            ("Do you sell to other removal companies or trade?",
             "Yes &mdash; trade pricing on bulk orders. Call <a href='tel:+441782939124'>01782 939124</a> for trade-account setup."),
            ("Do you do wardrobe-box hire instead of buy?",
             "Yes &mdash; included free with our packing or removal services. Standalone hire £4 per box per week."),
            ("Can I return unused boxes after my move?",
             "Yes &mdash; collapse them and we'll take them back at a half-price refund. Or keep for next move."),
        ],
    },
]

# Services hub
SERVICES_HUB = {
    'slug': 'services/index.html',
    'title': 'Removal &amp; Storage Services | NSR Stoke-on-Trent',
    'desc': "Removal services across Stoke-on-Trent and Staffordshire — residential, commercial, packing, storage, piano. Family-run since 2010.",
    'h1': 'Removal &amp; storage services across Staffordshire',
    'eyebrow': 'Services · Staffordshire-wide',
    'lead': "From a single piano in Leek to a whole-office relocation in Stoke-on-Trent — and every house move in between. Choose your service below, or request a free fixed-price quote tailored to your move.",
    'hero_img': 'family-celebrating-keys-new-home.jpg',
}


def render_services():
    for s in SERVICES:
        sections_html = '\n'.join(
            block_prose(eyebrow=eb, h2=h2, paras=paras, alt_bg=(i % 2 == 0), orange_bg=(i % 3 == 2))
            for i, (eb, h2, paras) in enumerate(s['sections'])
        )
        sections_html += '\n' + block_why_cards(alt_bg=False)
        sections_html += '\n' + block_closing_prose(depth=1)
        sections_html += '\n' + block_accred()
        sections_html += '\n' + block_internal_links(COMMON_LINKS, alt_bg=True)
        render_page(
            slug=s['slug'],
            title=s['title'],
            desc=s['desc'],
            h1=s['h1'],
            eyebrow=s['eyebrow'],
            lead=s['lead'],
            hero_img=s['hero_img'],
            sections_html=sections_html,
            faqs=s['faqs'],
            depth=1,
            current='services',
        )

    # Services hub — link-grid of 5 service cards + intro + supplementary
    hub = SERVICES_HUB
    hub_extra = block_prose(
        eyebrow='How services work',
        h2='How our services come together for a smooth Staffordshire move',
        paras=[
            "Most Staffordshire customers book more than one of our services — a typical residential move combines the core <a href='domestic-removals.html'>residential removal</a> with either fragile-only or full <a href='packing-services.html'>packing</a>, and roughly a third of moves also use <a href='storage-services.html'>short-term storage</a> to bridge a completion gap. Commercial customers usually combine the <a href='commercial-removals.html'>office relocation</a> service with crate hire and IT decommissioning. Specialist <a href='piano-removals.html'>piano moves</a> can either run standalone or as an add-on to a wider residential booking.",
            "Bundling services together earns you a single fixed-price quote that covers the whole job. There's no per-service surcharge for combining: a residential move with full packing and two weeks of storage is quoted as one number, not three. That single-number approach is what lets us promise no surprises on the day, and it's why repeat customers tell us they value the experience as much as the price.",
            "If you're not sure which combination of services suits your move, the survey is the right place to figure it out. Our surveyors do this every day — they'll listen to what you're trying to achieve, look at the volume of contents and the access at both ends, and recommend the combination that delivers the smoothest day for the lowest total cost. If you'd rather get an indicative figure first, the <a href='../resources/storage-calculator.html'>moving calculator</a> lets you toggle services on and off and see how each one affects the price band.",
            "Every service we offer is delivered by our own employed team, with our own equipment, out of our own Stoke-on-Trent depot. We don't sub-contract any element of any service to third-party companies — what you see at quote stage is what you get on move day, every time.",
        ],
        alt_bg=False,
    )
    cards_html = '''    <section class="services-section">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">What we do</span>
          <h2>Five core services across Staffordshire</h2>
          <p>Pick the service that fits your move below, or <a href="../quote.html">request a tailored quote</a>.</p>
        </div>
        <div class="services-grid">
          <a class="svc-card" href="domestic-removals.html"><div class="svc-img"><img src="../images/couple-unpacking-boxes-new-home.jpg" alt="Couple unpacking removal boxes in their new home" width="1066" height="1600" loading="lazy"><span class="svc-icon" aria-hidden="true">🏠</span></div><div class="svc-body"><h3>Residential removals</h3><p>Full home moves across Staffordshire. Two- and four-man crews, modern lorries, fixed-price quote.</p><span class="arrow">See home moves</span></div></a>
          <a class="svc-card" href="commercial-removals.html"><div class="svc-img"><img src="../images/stacked-cardboard-boxes-empty-room.jpg" alt="Cardboard boxes ready for a Stoke-on-Trent office relocation" width="1600" height="1066" loading="lazy"><span class="svc-icon" aria-hidden="true">🏢</span></div><div class="svc-body"><h3>Commercial removals</h3><p>Out-of-hours office relocations across the Potteries — IT decommission, crate hire, planned floor-by-floor lifts.</p><span class="arrow">Plan office move</span></div></a>
          <a class="svc-card" href="storage-services.html"><div class="svc-img"><img src="../images/cardboard-boxes-storage-warehouse.jpg" alt="Palletised storage containers in our Stoke-on-Trent warehouse" width="1200" height="800" loading="lazy"><span class="svc-icon" aria-hidden="true">🏬</span></div><div class="svc-body"><h3>Storage solutions</h3><p>Secure, alarmed container storage in Stoke-on-Trent. From a single pallet for a few weeks to long-term household storage.</p><span class="arrow">Reserve storage</span></div></a>
          <a class="svc-card" href="packing-services.html"><div class="svc-img"><img src="../images/packing-kitchenware-cardboard-box.jpg" alt="Professional packer wrapping kitchenware into a moving box" width="1600" height="1066" loading="lazy"><span class="svc-icon" aria-hidden="true">📦</span></div><div class="svc-body"><h3>Packing services</h3><p>Professional packers can wrap and box an average house in a single day, or just handle the fragile kitchen and china.</p><span class="arrow">See packing tiers</span></div></a>
        </div>
      </div>
    </section>'''
    intro_prose = block_prose(
        eyebrow='Our promise',
        h2='Five core services, one Staffordshire team',
        paras=[
            "North Staffordshire Removals &amp; Storage Ltd has been family-run from Stoke-on-Trent since 2010. Every service on this page is delivered by the same team — no sub-contractors, no last-minute van hire, no third-party brokers.",
            "Our crew know the Potteries roads, the parking quirks of every Newcastle-under-Lyme estate, the access points at the steeper Burslem terraces, and the lanes out to Leek and the Moorlands. That local knowledge is the reason your move runs to time and to the fixed-price quote we sent you.",
            "Below are our five core services. All are fully covered for Goods in Transit and Public Liability. All come with a free home or video survey and a written quote in 24 hours.",
        ],
        alt_bg=False,
    )
    piano_card = '''    <section class="alt-bg">
      <div class="container">
        <div class="section-head"><span class="eyebrow">Specialist</span><h2>Piano removals</h2><p>Upright, baby grand or full concert grand — see our specialist <a href="piano-removals.html">piano removals service</a> for kit, crew size and pricing.</p></div>
      </div>
    </section>'''
    sections_html = (intro_prose + '\n' + cards_html + '\n' + piano_card
                     + '\n' + hub_extra
                     + '\n' + block_why_cards(alt_bg=False)
                     + '\n' + block_closing_prose(depth=1)
                     + '\n' + block_accred()
                     + '\n' + block_internal_links(COMMON_LINKS, alt_bg=True))
    services_hub_faqs = [
        ("Which service should I choose for a typical house move?",
         "Most customers start with <a href='domestic-removals.html'>residential removals</a>. Add <a href='packing-services.html'>packing</a> if you'd rather hand the boxing-up to professionals; add <a href='storage-services.html'>storage</a> if your completion date is uncertain or you're downsizing."),
        ("Do you offer combined service quotes?",
         "Yes. Combining services (e.g. removal + packing + storage) is quoted as one fixed number — no per-service surcharge, no hidden bundling fee. Most quotes we send combine at least two services."),
        ("What's the most popular service combination?",
         "Residential removal + fragile-only packing is the most-booked combination, particularly for 3- and 4-bedroom Staffordshire moves where the kitchen and china benefit from professional handling."),
        ("Do you handle piano moves as part of a wider house move?",
         "Yes — pianos can be included in a residential booking at a small specialist supplement, or booked standalone via the <a href='piano-removals.html'>piano removals</a> service."),
        ("How do I get pricing for multiple services?",
         "<a href='../quote.html'>Submit one quote request</a> with all the services you might need. The surveyor will price each option and you can choose what to include in the final booking."),
    ]
    render_page(
        slug=hub['slug'], title=hub['title'], desc=hub['desc'],
        h1=hub['h1'], eyebrow=hub['eyebrow'], lead=hub['lead'],
        hero_img=hub['hero_img'], sections_html=sections_html, depth=1,
        current='services', faqs=services_hub_faqs,
    )


if __name__ == '__main__':
    print('Rendering services...')
    render_services()
    print('Done.')
