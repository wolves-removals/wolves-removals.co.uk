# -*- coding: utf-8 -*-
"""Wolves Removals static render engine.

Reproduces the original wolvesremovals theme chrome (header / footer / sections)
using the SAME compiled stylesheet (css/site.min.css) + Barlow fonts + brand
classes, while emitting markup that satisfies the MRM SEO bible
(canonical, OG/Twitter, JSON-LD LocalBusiness + Breadcrumb + FAQPage,
clickable tel/mailto, descriptive anchors, alt text, etc.).

Pure stdlib. Render scripts import from here.
"""
import json, os, sys, re, subprocess, functools, zlib, hashlib, html as _html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))
import siteconfig as S  # data/siteconfig.py
try:
    from hero_map import OLD_HEROES   # data/hero_map.py — curated hero per canonical path
except ImportError:
    OLD_HEROES = {}

def _asset_ver():
    """Cache-buster derived from the COMPILED stylesheet so `?v=` changes whenever the
    output CSS changes — including when new Tailwind utility classes are added in markup
    (a source-only hash missed those). Build CSS before HTML so this reads the fresh file."""
    for rel in ("css/site.min.css", "tools/css/site.input.css"):
        try:
            return hashlib.md5(open(os.path.join(S.ROOT, rel), "rb").read()).hexdigest()[:8]
        except Exception:
            continue
    return "23"

ASSET_VER = _asset_ver()

# ---------------------------------------------------------------- helpers
def esc(t):
    # Idempotent: unescape first so pre-existing entities (&, &mdash;, &rsquo;) aren't
    # double-encoded into visible "&amp;" / "&mdash;" text, then escape exactly once.
    return _html.escape(_html.unescape(str(t)), quote=True)

def abs_url(path):
    path = path or "/"
    if path.startswith("http"):
        return path
    return S.SITE_URL.rstrip("/") + "/" + path.lstrip("/")

def _clip(t, n):
    t = " ".join(str(t).split())
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"

# Inline SVG icons (no external sprite dependency)
ICONS = {
    "phone": '<svg viewBox="0 0 512 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M493 384l-91-91c-12-12-31-12-43 0l-45 45c-58-30-104-77-134-134l45-45c12-12 12-31 0-43l-91-91c-12-12-31-12-43 0L46 30C32 44 25 64 28 84c19 122 76 232 163 319s197 144 319 163c20 3 40-4 54-18l39-39c12-12 12-31 0-43z"/></svg>',
    "mobile": '<svg viewBox="0 0 24 24" class="{c}" fill="currentColor" aria-hidden="true"><path d="M8 2h8a3 3 0 0 1 3 3v14a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V5a3 3 0 0 1 3-3zm0 2a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1H8zm4 14.5a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/></svg>',
    "mail": '<svg viewBox="0 0 512 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M48 96c-18 0-32 14-32 32v10l240 156 240-156v-10c0-18-14-32-32-32H48zm448 79L262 332c-4 3-9 4-6 4-3 0-7-1-10-3L16 175v209c0 18 14 32 32 32h416c18 0 32-14 32-32V175z"/></svg>',
    "facebook": '<svg viewBox="0 0 320 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M279 288l14-93h-89v-60c0-26 12-50 52-50h41V6S250 0 215 0c-73 0-121 44-121 124v71H12v93h82v224h102V288z"/></svg>',
    "twitter": '<svg viewBox="0 0 512 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M389 48h70L305 224l181 240H345L235 320 108 464H38l164-188L28 48h145l99 131zm-25 374h39L156 88h-42z"/></svg>',
    "instagram": '<svg viewBox="0 0 448 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M224 141c-63 0-114 51-114 114s51 114 114 114 114-51 114-114-51-114-114-114zm0 188c-41 0-74-33-74-74s33-74 74-74 74 33 74 74-33 74-74 74zm145-194c0 15-12 27-27 27s-27-12-27-27 12-27 27-27 27 12 27 27zM224 48c66 0 74 0 100 1 24 1 37 5 46 9 12 4 20 10 28 18s14 16 18 28c4 9 8 22 9 46 1 26 1 34 1 100s0 74-1 100c-1 24-5 37-9 46-4 12-10 20-18 28s-16 14-28 18c-9 4-22 8-46 9-26 1-34 1-100 1s-74 0-100-1c-24-1-37-5-46-9-12-4-20-10-28-18s-14-16-18-28c-4-9-8-22-9-46-1-26-1-34-1-100s0-74 1-100c1-24 5-37 9-46 4-12 10-20 18-28s16-14 28-18c9-4 22-8 46-9 26-1 34-1 100-1z"/></svg>',
    "linkedin": '<svg viewBox="0 0 448 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M100 448H7V148h93v300zM53 107a54 54 0 1 1 0-108 54 54 0 0 1 0 108zm395 341h-92V302c0-35-1-79-49-79-48 0-55 38-55 77v148h-93V148h89v41h1c12-23 43-48 88-48 94 0 111 62 111 142v165z"/></svg>',
    "pinterest": '<svg viewBox="0 0 496 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M248 8C111 8 0 119 0 256c0 105 65 195 158 231-2-20-4-50 1-72 4-19 29-122 29-122s-7-15-7-37c0-35 20-61 45-61 21 0 32 16 32 35 0 21-14 53-21 83-6 25 13 45 37 45 44 0 78-47 78-114 0-60-43-101-104-101-71 0-112 53-112 108 0 21 8 44 18 57 2 2 2 4 2 6-2 8-6 24-7 28-1 4-4 5-9 3-32-15-52-62-52-100 0-80 59-155 170-155 89 0 159 64 159 149 0 89-56 161-134 161-26 0-51-14-59-30l-16 62c-6 22-21 50-32 67 24 7 49 11 76 11 137 0 248-111 248-248C496 119 385 8 248 8z"/></svg>',
    "tumblr": '<svg viewBox="0 0 320 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M309 480c-14 14-49 26-91 26-110 0-130-81-130-138V236H40v-72c66-17 93-74 97-124h62v112h81v84h-81v122c0 35 18 47 46 47 13 0 31-5 39-10l29 49z"/></svg>',
    "youtube": '<svg viewBox="0 0 576 512" class="{c}" fill="currentColor" aria-hidden="true"><path d="M549.7 124.1c-6.3-23.7-24.8-42.3-48.3-48.6C458.8 64 288 64 288 64S117.2 64 74.6 75.5c-23.5 6.3-42 24.9-48.3 48.6-11.4 42.9-11.4 132.3-11.4 132.3s0 89.4 11.4 132.3c6.3 23.7 24.8 41.5 48.3 47.8C117.2 448 288 448 288 448s170.8 0 213.4-11.5c23.5-6.3 42-24.1 48.3-47.8 11.4-42.9 11.4-132.3 11.4-132.3s0-89.4-11.4-132.3zm-317.5 213.5V175.2l142.7 81.2-142.7 81.2z"/></svg>',
    "instagram-color": '<svg viewBox="0 0 448 512" class="{c}" aria-hidden="true"><defs><linearGradient id="igg" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#FEDA77"/><stop offset="25%" stop-color="#F58529"/><stop offset="50%" stop-color="#DD2A7B"/><stop offset="75%" stop-color="#8134AF"/><stop offset="100%" stop-color="#515BD4"/></linearGradient></defs><path fill="url(#igg)" d="M224 141c-63 0-114 51-114 114s51 114 114 114 114-51 114-114-51-114-114-114zm0 188c-41 0-74-33-74-74s33-74 74-74 74 33 74 74-33 74-74 74zm145-194c0 15-12 27-27 27s-27-12-27-27 12-27 27-27 27 12 27 27zM224 48c66 0 74 0 100 1 24 1 37 5 46 9 12 4 20 10 28 18s14 16 18 28c4 9 8 22 9 46 1 26 1 34 1 100s0 74-1 100c-1 24-5 37-9 46-4 12-10 20-18 28s-16 14-28 18c-9 4-22 8-46 9-26 1-34 1-100 1s-74 0-100-1c-24-1-37-5-46-9-12-4-20-10-28-18s-14-16-18-28c-4-9-8-22-9-46-1-26-1-34-1-100s0-74 1-100c1-24 5-37 9-46 4-12 10-20 18-28s16-14 28-18c9-4 22-8 46-9 26-1 34-1 100-1z"/></svg>',
    "chevron": '<svg viewBox="0 0 20 20" class="{c}" fill="currentColor" aria-hidden="true"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>',
    "check": '<svg viewBox="0 0 20 20" class="{c}" fill="currentColor" aria-hidden="true"><path d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.7a1 1 0 011.4 0z"/></svg>',
    # 50% thicker stroke-style tick (use without fill-current — stroke takes currentColor)
    "check-bold": '<svg viewBox="0 0 24 24" class="{c}" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.4 4.5L19.5 7"/></svg>',
    "download": '<svg viewBox="0 0 20 20" class="{c}" fill="currentColor" aria-hidden="true"><path d="M10 2a1 1 0 011 1v7.59l2.3-2.3a1 1 0 011.4 1.42l-4 4a1 1 0 01-1.4 0l-4-4a1 1 0 011.4-1.42l2.3 2.3V3a1 1 0 011-1zM4 15a1 1 0 011 1v1h10v-1a1 1 0 112 0v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2a1 1 0 011-1z"/></svg>',
}
def icon(name, cls=""):
    return ICONS.get(name, "").format(c=cls)

# --- Per-page content expansions (authored by helper agents, kept in data/expansions/<kind>/<slug>.json)
_EXP_DIR = os.path.join(S.ROOT, "data", "expansions")
def load_expansion(kind, slug):
    """Return {'sections': [[h2,html],...], 'body': str, 'faqs': [[q,a],...]} or empties."""
    p = os.path.join(_EXP_DIR, kind, slug + ".json")
    if not os.path.exists(p):
        return {"sections": [], "body": "", "faqs": []}
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        return {"sections": [], "body": "", "faqs": []}
    return {"sections": d.get("sections", []), "body": d.get("body", ""), "faqs": d.get("faqs", [])}

@functools.lru_cache(maxsize=None)
def _dims(abspath):
    """Real pixel dimensions via macOS sips (cached). Returns (w,h) or (None,None)."""
    try:
        out = subprocess.check_output(["/usr/bin/sips", "-g", "pixelWidth", "-g", "pixelHeight", abspath],
                                      text=True, stderr=subprocess.DEVNULL)
        w = re.search(r"pixelWidth:\s*(\d+)", out)
        h = re.search(r"pixelHeight:\s*(\d+)", out)
        return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)
    except Exception:
        return (None, None)

def img(src, alt, cls="", eager=False, extra=""):
    """<img> with auto width/height (no CLS), lazy by default, alt<=100 chars (bible)."""
    src = src.lstrip("/")
    w, h = _dims(os.path.join(S.ROOT, src))
    wh = (f' width="{w}" height="{h}"' if w else "")
    loading = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    a = esc(_clip(alt, 100))
    # Responsive hero: serve an 800w variant to mobile (LCP) when one exists for this eager image.
    srcset = ""
    if eager and w and src.endswith(".webp"):
        s800 = src[:-5] + "-800.webp"
        if os.path.exists(os.path.join(S.ROOT, s800)):
            srcset = f' srcset="/{s800} 800w, /{src} {w}w" sizes="100vw"'
    return f'<img src="/{src}" alt="{a}"{wh}{srcset}{loading} decoding="async" class="{cls}"{(" " + extra) if extra else ""}>'

# ---- contextual photo pool (real, optimised webp moving photos) ----
PHOTOS = [
    ("wolves-team-loading-van-sussex", "Wolves Removals team loading a removal van in Sussex"),
    ("professional-movers-carrying-furniture-sussex", "Professional movers carrying furniture during a Sussex house move"),
    ("wolves-crew-preparing-moving-day", "Wolves Removals crew preparing a home for moving day"),
    ("careful-furniture-handling-house-removal", "Careful handling of furniture during a house removal"),
    ("wolves-van-ready-sussex-removal", "Wolves Removals van ready for a Sussex house move"),
    ("movers-wrapping-protecting-furniture", "Movers wrapping and protecting furniture for transport"),
    ("professionally-packed-moving-boxes-ready", "Professionally packed moving boxes ready for a house move"),
    ("loading-removal-lorry-furniture-sussex", "Loading a removal lorry with household furniture in Sussex"),
    ("wolves-team-sussex-house-move", "Wolves Removals team at work on a Sussex house move"),
    ("protecting-customer-belongings-house-move", "Protecting customer belongings for a safe house move"),
    ("removal-team-carrying-moving-boxes", "Removal team carrying moving boxes into a Sussex property"),
    ("furniture-loaded-sussex-removal-service", "Furniture being loaded for a Sussex removal service"),
    ("wolves-movers-handling-wardrobe", "Wolves Removals movers carefully handling a wardrobe"),
    ("removal-van-loaded-sussex-move", "A removal van loaded and ready for a Sussex house move"),
    ("wolves-crew-busy-sussex-moving-day", "Wolves Removals crew on a busy Sussex moving day"),
    ("professional-wolves-removals-team-sussex", "The professional Wolves Removals team based in Sussex"),
    ("careful-packing-sussex-home-removal", "Careful packing during a Sussex home removal service"),
    ("wolves-loading-furniture-removal-van", "Wolves Removals loading furniture into a removal van"),
    ("movers-transporting-household-items-sussex", "Movers transporting household items safely in Sussex"),
    ("removal-van-team-sussex-move", "A removal van and team ready for a Sussex house move"),
    ("wolves-handling-sussex-house-relocation", "Wolves Removals handling a Sussex house relocation"),
    ("loading-boxes-furniture-removal-van", "Loading boxes and furniture into a removal van in Sussex"),
    ("professional-removals-movers-sussex-property", "Professional removals movers at a Sussex property"),
    ("wolves-team-carrying-furniture-carefully", "Wolves Removals team carrying furniture with great care"),
    ("careful-removal-household-belongings-sussex", "Careful removal of household belongings in Sussex"),
    ("wolves-crew-completing-sussex-move", "Wolves Removals crew completing a Sussex house move"),
    # --- Jack's photos (real moves), optimised + upright, added to the rotation ---
    ("wolves-removals-team-fleet-vans", "The Wolves Removals team with their fleet of removal vans"),
    ("wolves-vans-sussex-country-house", "Wolves Removals vans at a grand Sussex country house"),
    ("two-wolves-vans-sussex-manor", "Two Wolves Removals vans outside a Sussex manor house"),
    ("wolves-van-outside-customer-home", "A Wolves Removals van parked outside a customer's home"),
    ("wolves-luton-storage-packing-van", "A branded Wolves Removals Luton van for removals, storage and packing"),
    ("wolves-lorry-arriving-sussex-property", "A Wolves Removals lorry arriving at a Sussex property"),
    ("wolves-team-loading-townhouse-move", "Wolves Removals team loading the van outside a townhouse"),
    ("wolves-movers-carrying-framed-mirror", "Wolves Removals movers carrying a large framed mirror during a move"),
    ("wolves-mover-holding-framed-painting", "A Wolves Removals mover carefully holding a framed oil painting"),
    ("wolves-mover-hanging-framed-picture", "A Wolves Removals mover hanging a framed picture on the wall"),
    ("loading-round-mirror-wolves-van", "Loading a large round mirror into a Wolves Removals van"),
    ("two-movers-positioning-timber-crate", "Two movers positioning a bespoke timber moving crate"),
    ("bespoke-timber-crate-protected-items", "A bespoke timber crate packed with protected items"),
    ("wolves-team-wrapping-furniture-move", "The Wolves Removals team wrapping furniture during a move"),
    ("furniture-wrapped-protected-removal", "Furniture wrapped and protected ready for a removal"),
    ("containerised-storage-units-wolves-store", "Containerised storage units at the Wolves Removals store"),
    ("a-forklift-handling-containerised-removals-storage", "A forklift handling containerised removals storage"),
]
from library_photos import LIBRARY_PHOTOS  # Mark's optimised photos added to the rotation
try:
    from library_photos import EXTRA_PHOTO_NAMES   # merged 'extra variety' photos
except ImportError:
    EXTRA_PHOTO_NAMES = frozenset()
PHOTOS = PHOTOS + LIBRARY_PHOTOS

# Home & About are "left alone": when building them we freeze out the EXTRA variety photos
# so their image picks stay exactly as before the pool was expanded.
_FREEZE_EXTRAS = {"on": False}
def freeze_extras(on):
    _FREEZE_EXTRAS["on"] = bool(on)

# Box-shop product/kit SKU shots must NEVER appear on any other page — they're only
# valid on the shop itself (rendered there by explicit product cards, not the pool).
# Sourced live from the shop renderer so it can never drift; hardcoded fallback below.
_BOXSHOP_FALLBACK = frozenset({
    "small-moving-box", "large-moving-box", "extra-large-moving-box", "wardrobe-moving-box",
    "packing-tape-roll", "bubble-wrap-roll", "packing-paper-pack", "mattress-protector-cover",
    "marker-pen", "one-bedroom-moving-kit", "two-bedroom-moving-kit",
    "three-bedroom-moving-kit", "four-bedroom-moving-kit",
})
_BOXSHOP_CACHE = {"set": None}
def boxshop_photos():
    if _BOXSHOP_CACHE["set"] is None:
        try:
            import render_boxshop as BS
            _BOXSHOP_CACHE["set"] = ({p[5] for p in BS.PRODUCTS} | {k[6] for k in BS.KITS}) | _BOXSHOP_FALLBACK
        except Exception:
            _BOXSHOP_CACHE["set"] = _BOXSHOP_FALLBACK
    return _BOXSHOP_CACHE["set"]

def _pool():
    if _FREEZE_EXTRAS["on"] and EXTRA_PHOTO_NAMES:
        # Home/About: preserve their exact verified picks (already box-shop-free, so
        # no exclusion needed — and removing entries here would shift their windows).
        return [p for p in PHOTOS if p[0] not in EXTRA_PHOTO_NAMES]
    return [p for p in PHOTOS if p[0] not in boxshop_photos()]

def page_photos(seed, n=5):
    """Deterministic, distinct photos for a page (variety across pages, no dupes within).
    Excludes the photo reserved for the site-wide quote band so no page repeats it."""
    pool = [p for p in _pool() if p[0] != QUOTE_BAND_PHOTO]
    L = len(pool)
    start = zlib.crc32(str(seed).encode()) % L
    if _FREEZE_EXTRAS["on"]:   # Home/About: keep the original contiguous window (left alone)
        return [pool[(start + i) % L] for i in range(min(n, L))]
    # Bespoke pages: walk the pool with a seed-varied stride coprime to L, so different
    # pages get INTERLEAVED (non-overlapping) selections instead of overlapping windows.
    stride = _coprime_stride(seed, L)
    return [pool[(start + i * stride) % L] for i in range(min(n, L))]

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def _coprime_stride(seed, L):
    if L <= 3:
        return 1
    s = 5 + (zlib.crc32(("stride-" + str(seed)).encode()) % (L - 4))
    for _ in range(L):
        if _gcd(s, L) == 1:
            return s
        s = s + 1 if s + 1 < L else 1
    return 1

# ---- topic matching: pick the photo whose alt text best fits a paragraph ----
_MATCH_STOP = {  # brand / location / generic filler — NOT topical subjects, so they must not drive matching
    "wolves", "removals", "removal", "sussex", "surrey", "kent", "hampshire", "across", "into",
    "with", "your", "that", "this", "from", "team", "crew", "movers", "mover", "professional",
    "professionally", "moving", "move", "house", "home", "homes", "family", "large", "whole",
    "simply", "keeping", "grand", "room", "rooms", "classical", "view", "busy", "recent", "based",
    "leading", "modern", "trained", "fully", "insured", "great", "care", "careful", "carefully",
    "work", "working", "completing", "preparing", "transport", "ready", "during", "full", "every",
    "single", "smaller", "handy", "online", "flexible", "choose", "settled", "sooner", "bridge",
    "complete", "options", "optional", "extras", "help", "kind", "take", "takes", "more",
    "daunting", "manageable", "mountain", "days"}
def _stem(w):
    return w[:-1] if len(w) > 4 and w.endswith("s") else w
def _kwset(text):
    return set(_stem(w) for w in re.findall(r'[a-z]+', text.lower())
               if len(w) > 3 and w not in _MATCH_STOP)
def _wc(text):
    d = {}
    for w in re.findall(r'[a-z]+', text.lower()):
        if len(w) > 3 and w not in _MATCH_STOP:
            sw = _stem(w); d[sw] = d.get(sw, 0) + 1
    return d
_PHOTO_DF = {}                                  # how many photos' alts contain each word
for _p in PHOTOS:
    for _w in _kwset(_p[1]):
        _PHOTO_DF[_w] = _PHOTO_DF.get(_w, 0) + 1
def match_photo(text, used=(), seed=None):
    """SITE RULE: the photo beside a paragraph must be about what the paragraph says.
    Score each pool photo by alt-vs-text word overlap, weighting rare/distinctive words
    (wardrobe, painting, storage, forklift...) most. Returns None if nothing overlaps.
    With `seed` (a page key), vary the choice among the NEAR-BEST topical matches so
    templated text (e.g. every town's 'about' section) gets a DIFFERENT but still on-topic
    photo on each page instead of always the single best — so pages aren't templated."""
    tc = _wc(text)
    if not tc:
        return None
    scored = []
    for p in _pool():
        if p[0] in used or p[0] == QUOTE_BAND_PHOTO:
            continue
        s = sum(tc.get(w, 0) / _PHOTO_DF.get(w, 1) for w in _kwset(p[1]))
        if s > 0:
            scored.append((s, p))
    if not scored:
        return None
    scored.sort(key=lambda x: -x[0])
    if seed is None:
        return scored[0][1]
    best = scored[0][0]
    top = [p for s, p in scored if s >= best * 0.45][:8]   # near-best topical matches
    return top[zlib.crc32(str(seed).encode()) % len(top)]

def _row_photo(seed, text, used, i=0):
    """A topic-matched, not-yet-used photo to sit BESIDE a prose row's text. Falls back to
    the deterministic page pool, then any unused pool photo; updates `used`. Lets every
    content row carry its own image without repeating one on the page (R9-safe)."""
    p = match_photo(text, used, seed=f"{seed}-{i}")   # page-seeded so pages aren't templated
    if p is None:
        p = next((x for x in page_photos(f"{seed}-{i}", 60) if x[0] not in used), None)
    if p is None:
        p = next((x for x in _pool() if x[0] not in used and x[0] != QUOTE_BAND_PHOTO), None)
    if p is None:
        p = page_photos(seed, 1)[0]
    used.add(p[0])
    return p

def photo_block(photo, cls="w-full h-full object-cover", eager=False):
    fn, alt = photo
    return img("images/photos/" + fn + ".webp", alt, cls=cls, eager=eager)

def text_with_image(inner_html, photo, reverse=False, bg="bg-white"):
    """Two-column section: prose beside a contextual photo. The text + image sit
    inside the same cols-2..11 envelope as prose() so left/right edges line up
    with the rest of the page's content (no misaligned blocks)."""
    media = (f'<div class="h-64 sm:h-80 lg:h-full lg:min-h-[22rem] overflow-hidden rounded-xl shadow-custom">'
             f'{photo_block(photo)}</div>')
    # text occupies 5 of 12 cols, image 5 of 12; col-start positions them within cols 2..11
    if reverse:
        text_cls = "col-span-12 lg:col-span-5 lg:col-start-7"
        pic_cls = "col-span-12 lg:col-span-5 lg:col-start-2 lg:row-start-1"
    else:
        text_cls = "col-span-12 lg:col-span-5 lg:col-start-2"
        pic_cls = "col-span-12 lg:col-span-5 lg:col-start-7"
    text = f'<div class="{text_cls}">{inner_html}</div>'
    pic = f'<div class="{pic_cls}">{media}</div>'
    return section(f'<div class="grid grid-cols-12 gap-8 lg:gap-12 items-center">{text}{pic}</div>', bg=bg)

def text_with_video(inner_html, slug, reverse=False, bg="bg-white"):
    """Two-column row: prose beside an ambient, muted, auto-playing looped video
    (no sound, no controls). Files: /videos/<slug>.mp4 + .webp poster. Portrait clips
    are width-capped and centred so they don't dominate the row."""
    vw, vh = _dims(os.path.join(S.ROOT, "videos", f"{slug}.webp"))
    vw, vh = (vw or 1280), (vh or 720)
    style = ' style="max-width:300px"' if vh > vw else ""
    media = (f'<figure class="mx-auto rounded-xl overflow-hidden shadow-custom bg-black"{style}>'
             f'<video class="w-full block" autoplay muted loop playsinline preload="metadata" '
             f'poster="/videos/{slug}.webp" width="{vw}" height="{vh}">'
             f'<source src="/videos/{slug}.mp4" type="video/mp4"></video></figure>')
    if reverse:
        text_cls = "col-span-12 lg:col-span-5 lg:col-start-7"
        pic_cls = "col-span-12 lg:col-span-5 lg:col-start-2 lg:row-start-1"
    else:
        text_cls = "col-span-12 lg:col-span-5 lg:col-start-2"
        pic_cls = "col-span-12 lg:col-span-5 lg:col-start-7"
    return section(f'<div class="grid grid-cols-12 gap-8 lg:gap-12 items-center">'
                   f'<div class="{text_cls}">{inner_html}</div><div class="{pic_cls}">{media}</div></div>', bg=bg)

def _para_blocks(html):
    """(heading_html, [(tag, html),...]) — preserves EVERY top-level content element in
    order (paragraphs, lists, sub-headings, tables, blockquotes); nothing is dropped.
    head = a leading <h1>/<h2> (the section heading carried onto the first row)."""
    head = ""
    m = re.match(r'\s*(<h[12]\b[^>]*>.*?</h[12]>)\s*', html, re.S)
    if m:
        head, html = m.group(1), html[m.end():]
    return head, [(t.lower(), full) for full, t in re.findall(r'(<(\w+)\b[^>]*>.*?</\2>)', html, re.S)]

def _split_row(inner_html, photo, reverse=False, bg="bg-white", contain=False, obj_pos="center", min_h=None):
    """Tight text+image row. The image is ABSOLUTELY positioned inside a relative box,
    so it never pushes the row taller than the text — the text sets the height and the
    photo crops to fit (no whitespace, ever). Sides alternate (reverse=image-left). The
    faded Wolves logo watermark sits behind the text side (logo-row), like the home page.
    `min_h` sets a desktop minimum row height (e.g. "22rem") so short sections still get a
    proper-sized image while the image still stretches to match longer text."""
    src = "images/photos/" + photo[0] + ".webp"
    if contain:   # diagrams/infographics: whole image on white, TOP-aligned so a tall
                  # portrait lines up with the heading beside it. Absolutely positioned
                  # (like the cover branch) so it never pushes the row taller than the text.
        media = ('<div class="relative h-72 sm:h-96 lg:h-full overflow-hidden rounded-xl shadow-custom bg-white">'
                 + img(src, photo[1], cls="absolute inset-0 w-full h-full object-contain object-top p-3") + '</div>')
    else:
        _ex = f'style="object-position:{obj_pos}"' if obj_pos != "center" else ""
        _mh_media = f' lg:min-h-[{min_h}]' if min_h else ""   # floor on the image box itself
        media = (f'<div class="relative h-56 sm:h-72 lg:h-full{_mh_media} overflow-hidden rounded-xl shadow-custom">'
                 + img(src, photo[1], cls="absolute inset-0 w-full h-full object-cover", extra=_ex) + '</div>')
    _tx = " lg:self-center" if min_h else ""   # short text centres beside the min-height image
    if contain:   # diagrams/infographics get a wider image column (~50% larger than a photo row)
        if reverse:   # image left, text right
            pic_d  = f'<div class="col-span-12 lg:col-span-5 lg:col-start-1 lg:row-start-1">{media}</div>'
            text_d = f'<div class="col-span-12 lg:col-span-6 lg:col-start-7{_tx}">{inner_html}</div>'
        else:         # image right, text left
            text_d = f'<div class="col-span-12 lg:col-span-6 lg:col-start-1{_tx}">{inner_html}</div>'
            pic_d  = f'<div class="col-span-12 lg:col-span-5 lg:col-start-8">{media}</div>'
    elif reverse:   # image left, text right
        text_d = f'<div class="col-span-12 lg:col-span-6 lg:col-start-6{_tx}">{inner_html}</div>'
        pic_d = f'<div class="col-span-12 lg:col-span-4 lg:col-start-2 lg:row-start-1">{media}</div>'
    else:         # image right, text left
        text_d = f'<div class="col-span-12 lg:col-span-6 lg:col-start-2{_tx}">{inner_html}</div>'
        pic_d = f'<div class="col-span-12 lg:col-span-4 lg:col-start-8">{media}</div>'
    return section(f'<div class="grid grid-cols-12 gap-6 lg:gap-10 items-stretch">{text_d}{pic_d}</div>',
                   bg=bg, pad="pt-6 lg:pt-10 pb-6 lg:pb-10", extra="logo-row overflow-hidden")

def media_rows(inner_html, seed, bg="bg-white", used=None, group=2, force=None, force_contain=False, force_pos=None, pins=None, min_h=None, vary=True):
    """Site rule: a 2+ paragraph block is broken into tight text+image rows (`group`
    paragraphs each); each image is TOPIC-MATCHED to its paragraph (match_photo), crops
    to the text height (no whitespace), and sides alternate. Pass a shared `used` set to
    stop a page repeating photos. `bg` may be a callable or a string."""
    if used is None:
        used = set()
    head, blocks = _para_blocks(inner_html)
    if callable(bg):
        nextbg = bg
    else:
        _c = {"n": 0 if bg != "bg-beige" else 1}
        def nextbg():
            v = "bg-white" if _c["n"] % 2 == 0 else "bg-beige"
            _c["n"] += 1
            return v
    if not blocks:
        return section(prose(inner_html), bg=nextbg())
    # Group blocks into rows: a sub-heading (<h3>/<h4>) starts a new row; otherwise pack up
    # to `group` paragraphs. Every non-paragraph element rides along, so nothing is dropped.
    groups, cur, pc = [], [], 0
    for tag, full in blocks:
        if cur and (tag in ("h3", "h4") or (tag == "p" and pc >= group)):
            groups.append(cur); cur, pc = [], 0
        cur.append(full)
        if tag == "p":
            pc += 1
    if cur:
        groups.append(cur)
    if len(groups) >= 2 and len(groups[-1]) == 1:      # don't strand a lone trailing block
        last = groups.pop(); groups[-1] += last
    rows = []
    for gi, g in enumerate(groups):
        body = (head if gi == 0 else "") + "".join(g)
        if gi == 0 and force:                          # pinned image for the first row
            photo = force
        elif pins and gi in pins:                      # pinned image for a specific row: (file, alt[, obj_pos])
            photo = pins[gi]
        else:
            photo = match_photo(body, used, seed=(f"{seed}-{gi}" if vary else None))   # page-seeded (bespoke per page)
            if photo is None:
                photo = next((p for p in page_photos(f"{seed}-{gi}", 16) if p[0] not in used),
                             page_photos(seed, 1)[0])
        used.add(photo[0])
        rbg = nextbg()   # side tracks the (already-alternating) bg, so consecutive rows flip sides
        _pos = "center"
        if gi == 0 and force and force_pos:
            _pos = force_pos
        elif pins and gi in pins and len(pins[gi]) > 2:
            _pos = pins[gi][2]
        rows.append(_split_row(body, photo, reverse=(rbg == "bg-beige"), bg=rbg,
                               contain=(gi == 0 and bool(force) and force_contain), obj_pos=_pos, min_h=min_h))
    return "\n".join(rows)

def media_body(html, seed, bg="bg-white", used=None, group=2, span="lg:col-span-10 lg:col-start-2"):
    """Render a full body (one or more <h2> sections), applying the split rule per
    section: 2+ paragraphs -> topic-matched media rows; otherwise a single prose section
    with the logo watermark. bg + image-side alternation stays continuous across sections."""
    if used is None:
        used = set()
    if callable(bg):
        nextbg = bg
    else:
        _c = {"n": 0 if bg != "bg-beige" else 1}
        def nextbg():
            v = "bg-white" if _c["n"] % 2 == 0 else "bg-beige"
            _c["n"] += 1
            return v
    chunks = [c.strip() for c in re.split(r'(?=<h2)', html) if c.strip()] or [html]
    out = []
    _side = {"n": 0}
    for ci, chunk in enumerate(chunks):
        if chunk.count("<p") >= 2:
            out.append(media_rows(chunk, f"{seed}-{ci}", nextbg, used=used, group=group))
        else:   # single-paragraph section: give it a real image beside the text too
            side = "left" if _side["n"] % 2 == 1 else "right"; _side["n"] += 1
            photo = _row_photo(seed, chunk, used, ci)
            out.append(_split_row(chunk, photo, reverse=(side == "left"), bg=nextbg()))
    return "\n".join(out)

def map_embed(query, title, cls="", zoom=10):
    """No-key Google Maps area embed (frame-src www.google.com is allow-listed in _headers).
    items-stretch + h-full lets it match the height of the text beside it. `query` like
    'Petersfield, Hampshire, UK'; lower `zoom` for wider county views."""
    from urllib.parse import quote as _q
    src = f"https://www.google.com/maps?q={_q(query)}&z={zoom}&output=embed"
    return (f'<div class="rounded-xl overflow-hidden shadow-custom border border-border '
            f'h-72 sm:h-80 lg:h-full lg:min-h-[20rem] {cls}">'
            f'<iframe title="Map of {esc(title)} — area Wolves Removals covers" src="{src}" '
            'width="100%" height="100%" style="border:0;display:block" loading="lazy" '
            'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>')

def feature_panel(heading_html, body_html, photo, reverse=False, bg="bg-white", with_cta=True):
    """Slate feature panel (old-site style): a rounded dark-grey card holding a
    white-framed photo on one side and white heading/body + CTA on the other."""
    b = S.BUSINESS
    media = (f'<div class="relative h-72 sm:h-96 lg:h-full overflow-hidden rounded-xl border-[5px] border-white shadow-lg">'
             f'{img("images/photos/" + photo[0] + ".webp", photo[1], cls="absolute inset-0 w-full h-full object-cover")}</div>')
    cta_html = ""
    if with_cta:
        cta_html = (
            '<div class="mt-7 flex flex-wrap items-center gap-x-6 gap-y-3">'
            '<a href="/get-a-quote/" class="button-orange">Get a Free Quote</a>'
            f'<a href="{b["phone_link"]}" class="inline-flex items-center gap-2 text-white font-bold text-lg lg:text-xl hover:text-orange" '
            f'aria-label="Call {b["phone"]}">{icon("phone","w-5 h-5")}{b["phone"]}</a>'
            '</div>')
    txt = (f'<div class="feature-panel col-span-12 lg:col-span-6{" lg:col-start-7" if not reverse else ""} lg:row-start-1">'
           f'{heading_html}{body_html}{cta_html}</div>')
    pic = (f'<div class="col-span-12 lg:col-span-6{" lg:col-start-7" if reverse else ""} lg:row-start-1">{media}</div>')
    return section(
        '<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2">'
        '<div class="bg-darkgrey rounded-2xl lg:rounded-[2rem] p-5 sm:p-7 lg:p-10 xl:p-12 shadow-custom">'
        # text first in the DOM so mobile stacks text-above-image; lg:col-start keeps desktop positions
        f'<div class="grid grid-cols-12 gap-7 lg:gap-10 items-stretch">{txt}{pic}</div>'
        '</div></div></div>', bg=bg)

def wolves_feature_panel(photo, reverse=False, bg="bg-white", name=None):
    """Standard slate feature panel for pages without their own feature section.
    `name` makes the heading a UNIQUE, page-specific <h2> (e.g. on service pages); without
    it the heading is a styled non-heading (recurring trust block) so it doesn't create a
    duplicate <h2> across the many generic pages that use this panel."""
    if name:
        heading = f'<h2 class="relative leading-tight">Why Move With Wolves Removals for {esc(name)}?</h2>'
    else:
        heading = ('<div class="relative leading-tight font-bold uppercase text-3xl 2xl:text-4xl mb-4">'
                   'Why Move With Wolves Removals?</div>')
    body = (
        '<p>We&rsquo;re a friendly, family-run Sussex removals and storage company that has been keeping its promises '
        'since 2016. From a single item to a full home or office move, every job is fully insured and led by a dedicated '
        'coordinator, so you always have one point of contact.</p>'
        '<p>As a <strong>LAPADA member</strong> and a <strong>Checkatrade-verified</strong> team, we handle it all with '
        'real care &mdash; expert <a href="/services/full-packing-service/">packing</a>, '
        '<a href="/services/house-removals/">home</a> and <a href="/services/commercial-removals/">business removals</a>, '
        'clean, secure <a href="/services/storage/">storage</a> and specialist '
        '<a href="/services/specialised-antiques-moving/">antiques</a> handling across Sussex, Surrey, Hampshire and Kent.</p>')
    return feature_panel(heading, body, photo, reverse=reverse, bg=bg, with_cta=True)

# Shared "We're Trusted By" strip — LAPADA accreditation centred above a 6-up row of
# estate-agent logos. ONE source of truth so it's identical on every page it appears
# (home, about, reviews). Add new agent logos to TRUSTED_ESTATE_LOGOS.
TRUSTED_ESTATE_LOGOS = [
    ("images/photos/fine-and-country-recommend-wolves.png", "Fine & Country estate agents recommend Wolves Removals"),
    ("images/photos/justin-lloyd-estate-agents-recommend.webp", "Justin Lloyd estate agents recommend Wolves Removals"),
    ("images/photos/mansell-mctaggart-estate-agents-partner.webp", "Mansell McTaggart estate agents partner with Wolves Removals"),
    ("images/photos/leaders-estate-agents-recommend.webp", "Leaders estate agents recommend Wolves Removals"),
    ("images/photos/alex-harvey-estate-agents-recommend.webp", "Alex Harvey estate agents recommend Wolves Removals"),
    ("images/photos/at-home-estate-lettings-recommend.webp", "At Home estate and lettings agency recommend Wolves Removals"),
]
TRUSTED_LAPADA_LOGO = ("images/photos/lapada-approved-service-provider.webp",
                       "LAPADA Approved Service Provider, Association of Art & Antiques Dealers")

def trusted_by(bg="bg-lightgrey"):
    """The shared 'We're Trusted By' strip — identical wherever it appears."""
    cells = "".join(
        f'<div class="flex items-center justify-center py-3 px-3">'
        f'{img(s, a, cls="h-10 sm:h-12 lg:h-14 w-auto max-w-full")}</div>'
        for s, a in TRUSTED_ESTATE_LOGOS)
    agents = f'<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 items-center gap-2">{cells}</div>'
    lapada = ('<div class="flex justify-center mb-10 lg:mb-12">'
              '<a href="https://lapada.org/dealers/wolves-removals/" target="_blank" rel="noopener" '
              'aria-label="Wolves Removals on LAPADA, The Association of Art &amp; Antiques Dealers" '
              'class="inline-block hover:opacity-80 transition-opacity">'
              f'{img(TRUSTED_LAPADA_LOGO[0], TRUSTED_LAPADA_LOGO[1], cls="h-32 sm:h-40 lg:h-44 w-auto")}</a></div>')
    return section(
        '<div class="text-center mb-10"><h2 class="relative leading-tight text-black">We&rsquo;re Trusted By</h2></div>'
        + lapada + agents, bg=bg)

def photo_strip(photos, heading="See Our Sussex Movers in Action", intro=None, bg="bg-lightgrey", seed=None):
    # Build a richer, de-duplicated set so the carousel has images to scroll through.
    # Top up to 7, seeded per page (`seed`) so headingless strips (e.g. blogs) don't all
    # pull the SAME top-up photos.
    pics, seen = [], set()
    for p in list(photos) + page_photos(seed or heading or "gallery", len(PHOTOS)):
        if p[0] in seen or p[0] == QUOTE_BAND_PHOTO:
            continue
        pics.append(p); seen.add(p[0])
        if len(pics) >= 7:
            break
    slides = "".join(
        f'<figure class="pstrip-slide"><div class="pstrip-frame">{photo_block(p)}</div></figure>'
        for p in pics)
    arrow = lambda d, lbl, path: (
        f'<button type="button" class="pstrip-arrow pstrip-{d}" aria-label="{lbl}">'
        f'<svg viewBox="0 0 24 24" class="w-6 h-6" aria-hidden="true">'
        f'<path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
        f'stroke-linejoin="round" d="{path}"/></svg></button>')
    arrows = (arrow("prev", "Show previous photos", "M15 5l-7 7 7 7")
              + arrow("next", "Show more photos", "M9 5l7 7-7 7"))
    head = ""
    if heading:
        head = f'<div class="text-center mb-8"><h2 class="relative leading-tight text-black">{esc(heading)}</h2>'
        head += (f'<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{intro}</p>' if intro else "") + "</div>"
    carousel = (f'<div class="pstrip" data-carousel>'
                f'<div class="pstrip-track" role="group" aria-label="{esc(heading or "Photo gallery")}">{slides}</div>'
                f'{arrows}</div>')
    return section(head + carousel, bg=bg)

def photo_gallery(photos, heading=None, intro=None, bg="bg-white"):
    """Centre-focused scrolling carousel (reuses the pstrip styling + photo-carousel.js):
    a horizontal scroll-snap gallery where the middle slide sits 50% larger than its
    neighbours. Shows EVERY photo passed (no 7-image cap) — used for the full antique set."""
    seen, pics = set(), []
    for p in photos:
        if not p or p[0] in seen or p[0] == QUOTE_BAND_PHOTO:
            continue
        seen.add(p[0]); pics.append(p)
    if not pics:
        return ""
    slides = "".join(
        f'<figure class="pstrip-slide"><div class="pstrip-frame">{photo_block(p)}</div></figure>'
        for p in pics)
    arrow = lambda d, lbl, path: (
        f'<button type="button" class="pstrip-arrow pstrip-{d}" aria-label="{lbl}">'
        f'<svg viewBox="0 0 24 24" class="w-6 h-6" aria-hidden="true">'
        f'<path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
        f'stroke-linejoin="round" d="{path}"/></svg></button>')
    arrows = (arrow("prev", "Show previous photos", "M15 5l-7 7 7 7")
              + arrow("next", "Show more photos", "M9 5l7 7-7 7"))
    head = ""
    if heading:
        head = (f'<div class="text-center mb-8"><h2 class="relative leading-tight text-black">{esc(heading)}</h2>'
                + (f'<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{intro}</p>' if intro else "")
                + "</div>")
    carousel = (f'<div class="pstrip" data-carousel>'
                f'<div class="pstrip-track" role="group" aria-label="{esc(heading or "Antiques gallery")}">{slides}</div>'
                f'{arrows}</div>')
    return section(head + carousel, bg=bg)

# ---- site-wide quote band (photo background + inline enquiry form) ----
FORM_ENDPOINT = "/api/quote"   # TODO: Cloudflare Worker -> Resend (needs key + verified sender)
QUOTE_BAND_PHOTO = "wolves-team-sussex-house-move"

def _qfield(name, placeholder, typ="text", required=False, half=True):
    req = ' required aria-required="true"' if required else ""
    col = "md:col-span-6" if half else "md:col-span-12"
    return (f'<div class="col-span-12 {col}">'
            f'<input class="w-full" type="{typ}" name="{name}" placeholder="{esc(placeholder)}" '
            f'aria-label="{esc(placeholder.rstrip("*"))}"{req}></div>')

def quote_band():
    b = S.BUSINESS
    bg = img("images/photos/" + QUOTE_BAND_PHOTO + ".webp",
             "Wolves Removals team on a Sussex house move", cls="w-full h-full object-cover")
    checks = "".join(
        f'<label class="flex items-center gap-2 font-normal normal-case"><input type="checkbox" name="enquiry" value="{esc(v)}"> {esc(v)}</label>'
        for v in ["Sales / New quotation", "General Enquiry"])
    form = (
        f'<form class="enquiry-form" method="post" action="{FORM_ENDPOINT}" novalidate><div class="grid grid-cols-12 gap-4">'
        + _qfield("first_name", "First Name*", required=True)
        + _qfield("last_name", "Last Name*", required=True)
        + _qfield("email", "Email*", typ="email", required=True)
        + _qfield("phone", "Phone", typ="tel")
        + '<div class="col-span-12"><span class="block font-semibold mb-2 text-black">Nature of Enquiry <span class="text-darkgrey">*</span></span>'
          f'<div class="flex flex-wrap gap-x-6 gap-y-2 text-black">{checks}</div></div>'
        + '<div class="col-span-12"><textarea class="w-full" name="message" rows="4" placeholder="Message" aria-label="Message"></textarea></div>'
        + '<div class="col-span-12 hidden" aria-hidden="true"><label>Leave blank<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>'
        + '<div class="col-span-12"><button type="submit" class="button-orange w-full justify-center">Submit</button>'
          '<p class="mt-3 text-xs text-darkgrey mb-0">By submitting this form you agree to our <a href="/privacy-policy/">privacy policy</a>. '
          'We&rsquo;ll only use your details to respond to your enquiry.</p></div>'
        '</div></form>')
    return (
        '<section id="quote" class="relative w-full overflow-hidden bg-darkgrey text-white">'
        f'<div class="absolute inset-0">{bg}</div>'
        '<div class="absolute inset-0 bg-darkgrey/90"></div>'
        '<div class="container relative z-10 py-12 lg:py-20"><div class="grid grid-cols-12 gap-8 lg:gap-12 items-center">'
        '<div class="col-span-12 lg:col-span-5">'
        '<h2 class="text-white leading-tight"><span class="bg-[#dad6c2] text-black px-2 box-decoration-clone">Interested</span> in Our Services? Get In Touch for a Free Quote</h2>'
        '<p class="mt-4 text-lg xl:text-xl">Simply fill in the contact form, call us or email us and a friendly member of our team will be in touch.</p>'
        f'<p class="mt-6 flex items-center gap-3 text-lg font-semibold"><span class="text-[#dad6c2]">{icon("phone","w-5")}</span>'
        f'<a class="text-white hover:text-orange" href="{b["phone_link"]}">{b["phone"]}</a> / '
        f'<a class="text-white hover:text-orange" href="{b["mobile_link"]}">{b["mobile"]}</a></p>'
        f'<p class="mt-2 flex items-center gap-3 text-lg font-semibold"><span class="text-[#dad6c2]">{icon("mail","w-5")}</span>'
        f'<a class="text-white hover:text-orange break-all" href="mailto:{b["email"]}">{b["email"]}</a></p>'
        '</div>'
        '<div class="col-span-12 lg:col-span-7"><div class="enquiry-card bg-white rounded-2xl shadow-custom p-6 lg:p-10 text-black">'
        f'{form}</div></div>'
        '</div></div></section>')

# ---- sticky floating action buttons (quote / call), like Mark Ratcliffe ----
def fabs():
    # Bottom-right is reserved for the site-wide Trustindex floating badge (set in the
    # Trustindex dashboard), so only the WhatsApp FAB renders here, bottom-left.
    b = S.BUSINESS
    wa_icon = ('<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.04 4C9.4 4 4 9.4 4 '
               '16.04c0 2.12.55 4.18 1.6 6L4 28l6.13-1.6a12 12 0 0 0 5.9 1.5h.01C22.68 27.9 28 22.5 28 15.96 28 9.4 '
               '22.68 4 16.04 4zm0 21.8h-.01a9.9 9.9 0 0 1-5.05-1.38l-.36-.21-3.64.95.97-3.55-.24-.37a9.86 9.86 0 0 '
               '1-1.51-5.24c0-5.46 4.45-9.9 9.9-9.9 2.64 0 5.13 1.03 7 2.9a9.86 9.86 0 0 1 2.9 7c0 5.46-4.45 9.9-9.9 '
               '9.9zm5.43-7.41c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.49 0 1.47 1.07 2.89 1.22 3.09.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35z"/></svg>')
    return (
        f'<a href="{b["whatsapp_link"]}" target="_blank" rel="noopener" class="fab fab-whatsapp fab-icon" aria-label="Message Wolves Removals on WhatsApp">{icon("phone","")}</a>')

# ---------------------------------------------------------------- HEAD
def head_html(title, description, canonical_path, og_image=None, robots="index, follow",
              extra_head="", schema=None):
    canonical = abs_url(canonical_path)
    desc = _clip(description, 145)              # bible: meta description <=145 chars
    og_img = abs_url(og_image) if og_image else abs_url("images/brand/wolves-removals-logo.png")
    parts = [
        "<!doctype html>",
        '<html lang="en-GB" class="scroll-smooth">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        # Security headers as meta (mirrors /_headers; covers hosts like GitHub Pages that
        # ignore /_headers). frame-ancestors is header-only (ignored in meta) so it's omitted here.
        ('<meta http-equiv="Content-Security-Policy" content="'
         "default-src 'self'; img-src 'self' data: https:; "
         "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.trustindex.io https://*.trustindex.io; "
         "style-src 'self' 'unsafe-inline' https://cdn.trustindex.io https://*.trustindex.io; "
         "font-src 'self' data: https://cdn.trustindex.io https://*.trustindex.io; "
         "connect-src 'self' https://cdn.trustindex.io https://*.trustindex.io https://api.postcodes.io; "
         "frame-src https://*.trustindex.io https://www.youtube-nocookie.com https://www.google.com; "
         "form-action 'self'; base-uri 'self'"
         '">'),
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        f'<meta name="robots" content="{robots}">',
        f'<link rel="canonical" href="{canonical}">',
        # Open Graph
        '<meta property="og:type" content="website">',
        '<meta property="og:locale" content="en_GB">',
        f'<meta property="og:site_name" content="{esc(S.BUSINESS["name"])}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{canonical}">',
        f'<meta property="og:image" content="{og_img}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{og_img}">',
        '<meta name="theme-color" content="#E8E6DA">',
        # icons
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
        '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">',
        '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">',
        '<link rel="manifest" href="/site.webmanifest">',
        # fonts (preload Barlow)
    ]
    for w in ("Regular", "Medium", "Semibold", "Bold"):
        parts.append(f'<link rel="preload" href="/fonts/Barlow-{w}.woff2" as="font" type="font/woff2" crossorigin>')
    if og_image:
        _ogrel = og_image.lstrip("/")
        _o800 = (_ogrel[:-5] + "-800.webp") if _ogrel.endswith(".webp") else ""
        if _o800 and os.path.exists(os.path.join(S.ROOT, _o800)):
            _ow, _ = _dims(os.path.join(S.ROOT, _ogrel))
            parts.append(f'<link rel="preload" as="image" imagesrcset="/{_o800} 800w, /{_ogrel} {_ow}w" '
                         'imagesizes="100vw" fetchpriority="high">')
        else:
            parts.append(f'<link rel="preload" as="image" href="{og_img}">')
    parts.append(f'<link rel="stylesheet" href="/css/site.min.css?v={ASSET_VER}">')
    if schema:
        for block in (schema if isinstance(schema, list) else [schema]):
            parts.append('<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False) + "</script>")
    if extra_head:
        parts.append(extra_head)
    parts.append("</head>")
    return "\n".join(parts)

def _font_face_css():
    faces = []
    for w, weight in (("Regular", 400), ("Medium", 500), ("Semibold", 600), ("Bold", 700)):
        faces.append(
            f"@font-face{{font-family:'Barlow';font-style:normal;font-weight:{weight};"
            f"font-display:swap;src:url('/fonts/Barlow-{w}.woff2') format('woff2');}}")
    return "<style>" + "".join(faces) + "</style>"

# ---------------------------------------------------------------- HEADER
# Nav model. type: "link" | "dropdown" (compact) | "mega" (full-width multi-column).
NAV = [
    {"label": "Removals", "href": "/services/", "type": "mega", "cols": [
        ("Home & Business", "/services/", [
            ("House Removals", "/services/house-removals/"),
            ("Commercial Removals", "/services/commercial-removals/"),
            ("Man and Van", "/services/man-and-van/"),
            ("Removal Services", "/services/removal-services/"),
            ("House Clearance", "/services/house-clearance/"),
            ("Contract Delivery", "/services/contract-delivery-services/")]),
        ("Long-Distance & Student", None, [
            ("European Removals", "/services/european-removals/"),
            ("International Removals", "/services/international-removals/"),
            ("Student Removals", "/services/student-removals/"),
            ("Export Packing Service", "/services/export-packing-service/")]),
        ("Specialist Moving", None, [
            ("Specialist Antique Moving", "/services/specialised-antiques-moving/"),
            ("Antiques in West Sussex", "/services/antiques-in-west-sussex/"),
            ("White Glove Service", "/services/white-glove-service/"),
            ("Piano Moving", "/services/piano-moving/"),
            ("Custom Crate Service", "/services/custom-crate-service/")]),
        ("Packing & Materials", None, [
            ("Full Packing Service", "/services/full-packing-service/"),
            ("Full Unpacking Service", "/services/full-unpacking-service/"),
            ("Fragile Packing", "/services/fragile-packing/"),
            ("Non-Fragile Packing", "/services/non-fragile-packing-service/"),
            ("Packing Materials", "/services/packing-materials/"),
            ("Box Shop (Order Online)", "/box-shop/")]),
    ]},
    {"label": "Storage", "href": "/services/storage/", "type": "dropdown", "links": [
        ("Storage Overview", "/services/storage/"),
        ("Long-Term Storage", "/services/storage/long-term-storage/"),
        ("Short-Term Storage", "/services/storage/short-term-storage/"),
        ("Business & Commercial Storage", "/services/storage/business-and-commercial-storage/"),
        ("Student Storage", "/services/student-storage/"),
        ("Storage Calculator", "/storage-calculator/"),
        ("Removals & Storage Calculator", "/removals-calculator/")]},
    {"label": "Box Shop", "href": "/box-shop/", "type": "link"},
    {"label": "Locations", "href": "/locations/", "type": "mega",
     "grid": "grid-cols-2 sm:grid-cols-3 lg:grid-cols-6", "cols": [
        ("Sussex", "/locations/sussex-removals/", [
            ("Arundel", "/locations/arundel-removals/"),
            ("Bognor Regis", "/locations/bognor-regis-removals/"),
            ("Burgess Hill", "/locations/burgess-hill-removals/"),
            ("Chichester", "/locations/chichester-removals/"),
            ("Crawley", "/locations/crawley-removals/"),
            ("East Preston", "/locations/east-preston-removals/"),
            ("Henfield", "/locations/henfield-removals/"),
            ("Horley", "/locations/horley-removals/"),
            ("Horsham", "/locations/horsham-removals/")]),
        ("West Sussex", "/locations/west-sussex-removals/", [
            ("Lancing", "/locations/lancing-removals/"),
            ("Littlehampton", "/locations/littlehampton-removals/"),
            ("Midhurst", "/locations/midhurst-removals/"),
            ("Petworth", "/locations/petworth-removals/"),
            ("Shoreham", "/locations/shoreham-removals/"),
            ("Steyning", "/locations/steyning-removals/"),
            ("Storrington", "/locations/storrington-removals/"),
            ("Billingshurst", "/locations/billingshurst-removals/"),
            ("Haywards Heath", "/locations/haywards-heath-removals/"),
            ("Worthing", "/locations/worthing-removals/")]),
        ("East Sussex", "/locations/east-sussex-removals/", [
            ("Brighton", "/locations/brighton-removals/"),
            ("Eastbourne", "/locations/eastbourne-removals/"),
            ("Lewes", "/locations/lewes-removals/"),
            ("Saltdean", "/locations/saltdean-removals/"),
            ("Tunbridge Wells", "/locations/tunbridge-wells-removals/"),
            ("Uckfield", "/locations/uckfield-removals/"),
            ("Hove", "/locations/hove-removals/")]),
        ("Hampshire", "/locations/hampshire-removals/", [
            ("Petersfield", "/locations/petersfield-removals/")]),
        ("Surrey", "/locations/surrey-removals/", [
            ("Cranleigh", "/locations/removals-cranleigh/"),
            ("Guildford", "/locations/guildford-removals/"),
            ("Reigate", "/locations/reigate-removals/")]),
        ("Kent", None, [
            ("Tunbridge Wells", "/locations/tunbridge-wells-removals/")]),
    ]},
    {"label": "About", "href": "/about-us/", "type": "dropdown", "links": [
        ("About Us", "/about-us/"), ("Pricing", "/pricing/"), ("Reviews", "/reviews/"),
        ("Gallery", "/gallery/"),
        ("Helpful Tips", "/helpful-tips/"),
        ("Blog", "/blog/"), ("FAQs", "/frequently-asked-questions/"),
        ("Careers", "/job-vacancies/")]},
    {"label": "Contact Us", "href": "/contact-us/", "type": "link"},
]

LINK_CLS = "text-black font-semibold uppercase lg:hover:text-orange text-base lg:text-sm xl:text-base"

def _toplink(label, href):
    return f'<a href="{href}" class="nav-top shrink-0 {LINK_CLS}">{esc(label)}</a>'

def _mega_col(title, churl, links):
    t_esc = esc(title)
    if churl:
        title_html = f'<a href="{churl}" class="font-semibold text-base lg:text-lg text-black hover:text-orange">{t_esc}</a>'
    else:
        title_html = f'<span class="font-semibold text-base lg:text-lg text-black">{t_esc}</span>'
    lis = "".join(f'<li><a href="{h}" class="block py-1 text-black hover:text-orange font-normal normal-case">{esc(t)}</a></li>'
                  for t, h in links)
    chev = icon("chevron", "h-4 w-4 fill-current")
    # On mobile each county/group is a collapsible accordion (.mega-sublist is forced
    # open on desktop via CSS). On desktop the toggle button is hidden.
    return (
        '<div x-data="{c:false}" class="border-b border-black/10 pb-2 mb-1 lg:border-0 lg:pb-0 lg:mb-0">'
        '<div class="flex items-center justify-between gap-2 lg:mb-2 lg:pb-2 lg:border-b lg:border-border">'
        f'{title_html}'
        f'<button type="button" @click="c=!c" :class="c?\'rotate-180\':\'\'" '
        f'class="lg:hidden p-2 -mr-2 bg-transparent transition-transform duration-200" aria-label="Toggle {t_esc}">{chev}</button>'
        '</div>'
        f'<ul class="mega-sublist list-none p-0 m-0 space-y-1 pt-1 pb-2 lg:pt-0 lg:pb-0" x-show="c" x-cloak>{lis}</ul>'
        '</div>')

def _nav_items():
    li_base = "lg:h-full w-full lg:w-auto flex items-center lg:pr-4 xl:pr-5 2xl:pr-7 border-b border-black/10 lg:border-b-0"
    out = []
    for it in NAV:
        t, label, href = it["type"], it["label"], it["href"]
        if t == "link":
            out.append(f'<li class="{li_base} px-4 py-3 lg:p-0 lg:py-10">{_toplink(label, href)}</li>')
            continue
        trigger = (f'<div class="flex items-center w-full lg:w-auto justify-between px-4 lg:p-0 py-3 lg:py-0">'
                   f'{_toplink(label, href)}'
                   f'<button type="button" aria-label="Open {esc(label)} menu" @click="o=!o" '
                   f'class="nav-top lg:ml-1 p-1 bg-transparent transition-transform duration-200" :class="o?\'rotate-180\':\'\'">'
                   f'{icon("chevron","h-5 w-5 fill-current")}</button></div>')
        if t == "dropdown":
            links = "".join(f'<li><a href="{h}" class="block py-1 lg:py-2 lg:px-5 text-black hover:text-orange font-normal normal-case">{esc(lt)}</a></li>'
                            for lt, h in it["links"])
            panel = (f'<ul x-cloak class="bg-white w-full px-4 py-2 lg:absolute lg:top-full lg:left-0 lg:w-72 lg:z-30 '
                     f'lg:shadow-lg lg:border-t-4 lg:border-lightgrey list-none my-0 lg:p-2" '
                     f':class="o ? \'block\' : \'hidden\'">{links}</ul>')
        else:  # mega
            cols = "".join(_mega_col(ct, cu, cl) for ct, cu, cl in it["cols"])
            grid = it.get("grid", "grid-cols-1 md:grid-cols-2 lg:grid-cols-4")
            _m = re.search(r"lg:grid-cols-\d+", grid)
            grid_m = "grid-cols-1 " + (_m.group(0) if _m else "lg:grid-cols-4")  # single column on mobile
            panel = (f'<div x-cloak class="bg-white w-full lg:absolute lg:left-0 lg:right-0 lg:top-full lg:z-30 '
                     f'lg:shadow-lg lg:border-t-4 lg:border-lightgrey" :class="o ? \'block\' : \'hidden\'">'
                     f'<div class="px-5 py-3 lg:px-0 lg:py-8 lg:container"><div class="grid {grid_m} gap-x-8 gap-y-5">{cols}</div></div></div>')
        pos = "lg:relative " if t == "dropdown" else ""   # mega panels span full header width
        # Desktop hover with a short close-delay: crossing the gap between the
        # trigger and the panel (or moving diagonally to a far column) starts a
        # 250ms timer; re-entering the <li> subtree (which includes the panel,
        # a DOM child) cancels it, so the menu no longer vanishes mid-select.
        out.append(
            f'<li class="{pos}{li_base} flex-col lg:flex-row lg:py-10" x-data="{{o:false,t:0}}" '
            f'@mouseenter="if(window.innerWidth>=1024){{clearTimeout(t);o=true}}" '
            f'@mouseleave="if(window.innerWidth>=1024){{t=setTimeout(()=>o=false,250)}}">{trigger}{panel}</li>')
    return "\n".join(out)

def header_html(active=""):
    b = S.BUSINESS
    nav = _nav_items()
    return f'''<header id="header" class="h-[100px] sm:h-[108px] md:h-[108px] lg:h-[164px] xl:h-[171px] 2xl:h-[174px]">
  <div id="inner-header" class="bg-[#dad6c2] z-50 w-full fixed shadow-custom-header">
    <div class="contact-bar bg-darkgrey py-4 md:py-5">
      <div class="container">
        <div class="flex items-center justify-end gap-2 sm:gap-6 font-medium">
          <div class="hidden xl:flex items-center gap-6">
            <a class="text-white hover:text-orange" href="/contact-us/">Write to Jack Wolfe</a>
            <a class="flex items-center gap-2 text-white hover:text-orange" aria-label="Email {b['email']}" href="mailto:{b['email']}">{icon('mail','w-4 text-beige')}<span>{b['email']}</span></a>
            <a class="text-white hover:text-orange" href="/gallery/">Gallery</a>
          </div>
          <div class="flex items-center gap-2 sm:gap-6">
            <a class="flex items-center gap-2 text-white hover:text-orange" aria-label="Call us on {b['phone']}" href="{b['phone_link']}">{icon('phone','w-4 text-beige')}<span>Call us on {b['phone']}</span></a>
            <a class="hidden md:flex items-center gap-2 text-white hover:text-orange" aria-label="Call our mobile {b['mobile']}" href="{b['mobile_link']}">{icon('mobile','w-4 text-beige')}<span>{b['mobile']}</span></a>
            <a class="hidden sm:flex xl:hidden items-center gap-2 text-white hover:text-orange" aria-label="Email {b['email']}" href="mailto:{b['email']}">{icon('mail','w-4 text-beige')}<span>{b['email']}</span></a>
            <a class="flex sm:hidden items-center gap-2 text-white hover:text-orange" aria-label="Email {b['email']}" href="mailto:{b['email']}">{icon('mail','w-4 text-beige')}<span>Email Us</span></a>
          </div>
        </div>
      </div>
    </div>
    <div class="container mx-auto h-full">
      <div id="top-header" class="flex flex-wrap sm:flex-nowrap items-stretch h-full justify-between lg:gap-4 xl:gap-8">
        <div id="logo" class="order-1 relative shrink-0 w-[112px] sm:w-[140px] lg:w-[180px] xl:w-[200px] z-50">
          <a id="site-logo" class="absolute left-0 top-1/2 -translate-y-1/2 flex z-50" href="/" title="{b['name']}">
            <img class="h-[64px] sm:h-[88px] lg:h-[164px] xl:h-[180px] w-auto drop-shadow-lg" src="/images/brand/wolves-removals-logo.png" width="440" height="438" alt="{b['name']} logo" />
          </a>
        </div>
        <div class="order-2 hidden lg:flex lg:flex-1 items-center justify-end gap-4 xl:gap-6">
          <nav id="site-navigation" aria-label="Primary" class="font-medium">
            <ul class="flex lg:flex-row lg:items-center lg:justify-end p-0 mb-0 list-none">{nav}</ul>
          </nav>
          <a class="button-orange btn-white btn-sweep pulse shrink-0 whitespace-nowrap lg:px-10 xl:px-14" href="/get-a-quote/"><span class="relative z-10">Get a Free Quote</span><span class="btn-sweep-shine" aria-hidden="true"></span></a>
        </div>
        <div class="order-3 w-fit flex lg:hidden items-center justify-end gap-4">
          <a class="button-orange btn-white btn-sweep pulse rounded-xl whitespace-nowrap text-xs px-4 sm:text-sm sm:px-6" href="/get-a-quote/"><span class="relative z-10">Get a Free Quote</span><span class="btn-sweep-shine" aria-hidden="true"></span></a>
          <button type="button" aria-label="Open menu" @click="menuOpen=!menuOpen" class="text-black bg-transparent p-2">
            <svg viewBox="0 0 24 24" class="w-7 h-7" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
          </button>
        </div>
      </div>
    </div>
    <div x-cloak class="lg:hidden absolute top-full left-0 w-full bg-[#dad6c2] max-h-[80vh] overflow-y-auto" :class="menuOpen ? 'block' : 'hidden'">
      <nav aria-label="Mobile" class="font-medium">
        <ul class="flex flex-col p-0 mb-0 list-none">{nav}</ul>
      </nav>
    </div>
  </div>
</header>'''

# ---------------------------------------------------------------- FOOTER
def footer_html():
    b = S.BUSINESS
    cols = []
    # contact column first
    cols.append(f'''<div class="w-1/2 md:w-1/3 lg:w-auto lg:flex-1">
      <p class="text-lg font-semibold mb-3 text-white">Contact Us</p>
      <address class="not-italic leading-relaxed">
        <strong>{esc(b['name'])}</strong><br>{esc(b['street'])}<br>{esc(b['locality'])} ({esc('Horsham District')})<br>{esc(b['region'])} {esc(b['postcode'])}
      </address>
      <p class="mt-3 flex items-center gap-2"><a class="flex items-center gap-2 text-white hover:text-orange" href="{b['phone_link']}" aria-label="Call {b['phone']}">{icon('phone','w-4 text-beige')}{b['phone']}</a></p>
      <p class="flex items-center gap-2"><a class="flex items-center gap-2 text-white hover:text-orange" href="{b['mobile_link']}" aria-label="Call {b['mobile']}">{icon('phone','w-4 text-beige')}{b['mobile']}</a></p>
      <p class="flex items-center gap-2"><a class="flex items-center gap-2 text-white hover:text-orange" href="mailto:{b['email']}" aria-label="Email {b['email']}">{icon('mail','w-4 text-beige')}{b['email']}</a></p>
    </div>''')
    # map column — sits beside Contact Us
    cols.append(
        '<div class="w-full sm:w-1/2 lg:w-auto">'
        '<p class="text-lg font-semibold mb-3 text-white">Find Us</p>'
        '<iframe title="Wolves Removals on Google Maps" '
        'src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2514.3453870554604!2d-0.39006729999999995!3d50.93582529999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4875be0cfeaa65a1%3A0xb3edb5f864a3b9f4!2sSussex%20Removals%20Company%20%7C%20Wolves%20Removals!5e0!3m2!1sen!2suk!4v1780856560287!5m2!1sen!2suk" '
        'class="block" style="border:0;width:215px;max-width:100%;height:200px;border-radius:10px;" '
        'allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>')
    for label, links in S.footer_columns():
        lis = "".join(f'<li><a class="text-white hover:text-orange" href="{h}">{esc(t)}</a></li>' for t, h in links)
        cols.append(f'''<div class="w-1/2 md:w-1/3 lg:w-auto lg:flex-1">
      <p class="text-lg font-semibold mb-3 text-white">{esc(label)}</p>
      <ul class="list-none p-0 m-0 space-y-1">{lis}</ul></div>''')
    # (url, label, icon, brand colour). Instagram uses its signature gradient icon.
    _socials = [
        ("https://www.instagram.com/wolvesremovals/", "Instagram", "instagram-color", ""),
        ("https://www.facebook.com/wolvesremovals/", "Facebook", "facebook", "#1877F2"),
        ("https://www.linkedin.com/company/wolves-removals", "LinkedIn", "linkedin", "#0A66C2"),
        ("https://www.pinterest.co.uk/wolvesremovals/", "Pinterest", "pinterest", "#E60023"),
        ("https://x.com/WolvesRemovals", "X (Twitter)", "twitter", "#000000"),
        ("https://www.tumblr.com/wolvesremovalsltd", "Tumblr", "tumblr", "#36465D"),
        ("https://www.youtube.com/@wolvesremovals", "YouTube", "youtube", "#FF0000"),
    ]
    def _sa(u, label, ic, color):
        st = f'style="color:{color}" ' if color else ''
        return (f'<a href="{u}" aria-label="Wolves Removals on {label}" rel="noopener nofollow" target="_blank" '
                f'{st}class="hover:opacity-80 transition-opacity">{icon(ic, "w-5 h-5")}</a>')
    social = "".join(_sa(*s) for s in _socials)
    return f'''<footer id="colophon" class="bg-darkgrey relative text-white">
  <div class="w-full py-10 lg:py-20">
    <div class="container">
      <div class="flex flex-wrap gap-y-6 lg:gap-8 text-base lg:text-sm xl:text-base">{''.join(cols)}</div>
    </div>
  </div>
  <div class="py-4 xl:py-6 bg-white text-black">
    <div class="container">
      <div class="flex flex-col lg:flex-row gap-4 justify-between items-center font-semibold">
        <p class="m-0">&copy; 2026 {esc(b['name'])} | {esc(b['tagline'])} UK. <a class="text-black hover:text-orange" href="/privacy-policy/">Privacy Policy</a> &middot; <a class="text-black hover:text-orange" href="/terms-conditions/">Terms</a></p>
        <div class="flex items-center gap-4 text-darkgrey">{social}</div>
      </div>
    </div>
  </div>
</footer>'''

# ---------------------------------------------------------------- SECTIONS
def section(inner, bg="bg-white", pad="pt-8 lg:pt-16 pb-8 lg:pb-16", extra=""):
    return (f'<section class="relative {bg} w-full {pad} border-border {extra}">'
            f'<div class="container">{inner}</div></section>')

def prose(html_content, center=False, span="lg:col-span-8 lg:col-start-3"):
    al = "text-center" if center else "text-left"
    return (f'<div class="grid grid-cols-12 gap-y-4 lg:gap-8">'
            f'<div class="col-span-12 {span} text-black">'
            f'<div class="{al}">{html_content}</div></div></div>')

# Self-hosted promo videos (in /videos/). name/description are PLAIN text (escaped for HTML, raw for schema).
VIDEO_META = {
    "wolves-removals-promo-b": ("Wolves Removals — Sussex Removals & Storage",
        "Meet the Wolves Removals team — the people, vehicles and care behind our Sussex moves.", "PT1M13S"),
    "wolves-removals-promo-a": ("Wolves Removals — Sussex Removals & Storage",
        "A look at Wolves Removals across Sussex, Surrey, Kent and Hampshire.", "PT1M"),
    "storage-container-promo-b": ("Secure Storage with Wolves Removals",
        "Our team loading and storing mobile storage containers securely at our Sussex depot.", "PT29S"),
    "storage-container-promo-a": ("Secure Storage with Wolves Removals",
        "Mobile storage containers loaded and stored securely by the Wolves Removals team.", "PT33S"),
    "packing-paintings-promo": ("Packing & Crating Fine Art and Paintings",
        "How our specialists wrap, pack and custom-crate paintings and antiques for safe transport.", "PT2M48S"),
    "packing-mirror-promo": ("Packing & Protecting Mirrors",
        "Wrapping and crating a large mirror for a safe, damage-free move.", "PT1M48S"),
    "packing-plates-promo": ("Expert Packing of Fragile Crockery",
        "Our team carefully wrapping and boxing fragile plates and china ready for moving.", "PT1M10S"),
    "packing-books-promo": ("Packing Books & Heavy Items",
        "Packing books safely and efficiently into the right boxes for a move.", "PT1M59S"),
    "packing-sofa-promo": ("Protecting & Moving Sofas",
        "Wrapping and moving a sofa with full furniture protection.", "PT45S"),
    "packing-wine-glasses-promo": ("Wrapping & Protecting Furniture for Transport",
        "Our team wrapping furniture in protective Furni-Soft padding ready for a safe move.", "PT25S"),
}

def video_embed(slug, bg="bg-white", heading=True, aside=None):
    """Self-hosted promo video player + VideoObject JSON-LD. Files: /videos/<slug>.mp4 + .webp.
    aside: optional write-up HTML placed BESIDE the video (vertically centred so the
    text stays within the video's height; stacks above the video on mobile). When set,
    it replaces the centred heading/description (the description still feeds the JSON-LD)."""
    name, desc, dur = VIDEO_META[slug]
    base, poster, mp4 = "https://wolves-removals.co.uk", f"/videos/{slug}.webp", f"/videos/{slug}.mp4"
    schema = {"@context": "https://schema.org", "@type": "VideoObject", "name": name, "description": desc,
              "thumbnailUrl": [base + poster], "contentUrl": base + mp4, "uploadDate": "2026-06-01", "duration": dur}
    # Real poster dimensions set the player's width/height (no CLS) and let portrait
    # clips render in a sensibly capped frame instead of a huge 16:9 letterbox.
    vw, vh = _dims(os.path.join(S.ROOT, "videos", f"{slug}.webp"))
    vw, vh = (vw or 1280), (vh or 720)
    # Portrait clips: cap width via inline style (a Tailwind arbitrary class like
    # max-w-[210px] would need a separate build:css recompile, so it silently no-ops).
    portrait = vh > vw
    fig_cls = "rounded-xl overflow-hidden shadow-lg bg-black" + ("" if portrait else " max-w-4xl")
    fig_style = ' style="max-width:210px"' if portrait else ""
    video_tag = (f'<video class="w-full block" controls preload="none" playsinline poster="{poster}" width="{vw}" height="{vh}">'
                 f'<source src="{mp4}" type="video/mp4">Your browser doesn&rsquo;t support embedded video.</video>')
    schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
    if aside:
        # Video + write-up side by side. items-center keeps the (shorter) text within
        # the video's vertical bounds — neither above nor below it; stacks on mobile.
        fig = f'<figure class="{fig_cls} mx-auto lg:mx-0 shrink-0"{fig_style}>{video_tag}</figure>'
        row = (f'<div class="flex flex-col lg:flex-row lg:items-center gap-6 lg:gap-12">'
               f'{fig}<div class="flex-1 text-left">{aside}</div></div>{schema_tag}')
        return section('<div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-10 lg:col-start-2 text-black">'
                       + row + '</div></div>', bg=bg)
    head = (f'<div class="text-center mb-5"><h2 class="relative leading-tight text-black">{esc(name)}</h2></div>'
            if heading else "")
    inner = (head +
        f'<figure class="{fig_cls} mx-auto"{fig_style}>{video_tag}</figure>'
        f'<p class="text-center text-base mt-4 max-w-2xl mx-auto">{esc(desc)}</p>'
        f'{schema_tag}')
    return section(prose(inner, span="lg:col-span-10 lg:col-start-2"), bg=bg)

CCARD_VARIANTS = {1: "ccard--accent", 2: "ccard--slate", 3: "ccard--outline"}

def content_card(inner_html, variant=1, bg="bg-beige", span="lg:col-span-10 lg:col-start-2",
                 photo=None, img_side="right", img_fit="cover"):
    """A prose row lifted into a styled card panel on its (cream) background.
    `variant` 1/2/3 rotates the card treatment so cream rows are never identical.
    Pass `photo=(filename, alt)` to make a two-column photo+text card (image on
    `img_side`). `img_fit="contain"` shows the whole image on a white panel (use for
    diagrams/size guides whose edges/labels must not be cropped)."""
    vcls = CCARD_VARIANTS.get(variant, "ccard--accent")
    if photo:
        fit = "object-contain" if img_fit == "contain" else "object-cover"
        mcls = "ccard-media ccard-media--contain" if img_fit == "contain" else "ccard-media"
        # size-guide/diagram images (contain mode) load eagerly so they always show
        media = (f'<div class="{mcls}">'
                 f'{img("images/photos/" + photo[0] + ".webp", photo[1], cls="w-full h-full " + fit, eager=(img_fit == "contain"))}</div>')
        text = f'<div class="ccard-text">{inner_html}</div>'
        # text always first in DOM (mobile stacks text-above-image); desktop side set via CSS order
        body = f'<div class="ccard-split ccard-split--{esc(img_side)}">{text}{media}</div>'
        extra = " ccard--has-media"
    else:
        body, extra = inner_html, ""
    return section(
        '<div class="grid grid-cols-12">'
        f'<div class="col-span-12 {span} text-black">'
        f'<div class="ccard {vcls}{extra}">{body}</div>'
        '</div></div>', bg=bg)

def photo_flanked_row(inner_html, photos, bg="bg-white", span="lg:col-span-8 lg:col-start-3"):
    """A flat prose row with two faded, topically-relevant photos bleeding in from
    the left and right edges (fading into white). Alternates with the logo-watermark
    rows so the page isn't a repeated logo. Side photos hide on mobile."""
    lp, rp = photos[0], photos[1]
    left = f'<div class="flank-side flank-side-l" aria-hidden="true">{photo_block(lp)}</div>'
    right = f'<div class="flank-side flank-side-r" aria-hidden="true">{photo_block(rp)}</div>'
    content = (f'<div class="container">'
               f'<div class="grid grid-cols-12"><div class="col-span-12 {span} text-black">'
               f'<div class="text-left">{inner_html}</div></div></div></div>')
    tone = " flank-cream" if bg == "bg-beige" else ""
    return (f'<section class="relative {bg} w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden flank-row{tone}">'
            f'{left}{right}{content}</section>')

def _deflank_section(sec):
    """Turn a faded-flank row (two faded edge photos) into a tight text+image row that
    keeps ONE of the photos as a solid image beside the text — so the row is no longer a
    flank (splits an adjacent pair) yet still has an image beside it."""
    bgm = re.search(r'<section class="relative (bg-\S+)', sec)
    bg = bgm.group(1) if bgm else "bg-white"
    imgs = re.findall(r'<img\b[^>]*>', sec)
    tm = re.search(r'<div class="text-left">(.*?)</div></div></div></div></section>', sec, re.S)
    if not imgs or not tm:   # fallback: strip flanks to a plain logo-watermark row
        s2 = re.sub(r'<div class="flank-side\b[^"]*"[^>]*>.*?</div>', "", sec, count=2, flags=re.S)
        return s2.replace(" flank-cream", "").replace(" flank-row", " logo-row")
    inner = tm.group(1)
    img_tag = re.sub(r'\sclass="[^"]*"', ' class="absolute inset-0 w-full h-full object-cover"', imgs[0], count=1)
    media = ('<div class="relative h-56 sm:h-72 lg:h-full overflow-hidden rounded-xl shadow-custom">'
             + img_tag + '</div>')
    return (f'<section class="relative {bg} w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
            '<div class="container"><div class="grid grid-cols-12 gap-6 lg:gap-10 items-stretch">'
            f'<div class="col-span-12 lg:col-span-6 lg:col-start-2">{inner}</div>'
            f'<div class="col-span-12 lg:col-span-6 lg:col-start-8">{media}</div></div></div></section>')

def split_adjacent_flanks(body):
    """Site-wide rhythm rule: two faded-flank rows must never sit directly adjacent.
    Walk the top-level sections in order and convert the SECOND of each consecutive
    flank pair into a logo-watermark row, so flank rows always alternate with plain ones."""
    segs = re.split(r'(<section\b.*?</section>)', body, flags=re.S)
    prev_flank = False
    for i, seg in enumerate(segs):
        if not seg.startswith("<section"):
            continue
        m = re.match(r'<section\b[^>]*>', seg)
        is_flank = bool(m and "flank-row" in m.group(0))
        if is_flank and prev_flank:
            segs[i] = _deflank_section(seg)
            prev_flank = False          # the converted row is now plain
        else:
            prev_flank = is_flank
    return "".join(segs)

def rich_prose(body_html, seed, photo_budget=12):
    """Split a long prose body at its <h2> headings into the site-standard, topic-matched
    media rows (tight text+image, alternating sides, logo watermark). Delegates to
    media_body so about/pricing match the service, blog & location pages."""
    return media_body(body_html, seed, used=set(), group=2)

# Dedicated Trustindex widget for the hero review card (separate ID from the floating
# corner badge, so both render on the same page without conflict).
TI_HERO_WIDGET = "f62b22e344ef413cc336104943f"

def review_card(cls=""):
    """Live Trustindex Google-reviews widget for the hero (renders its own card UI)."""
    c = ("ti-hero " + cls).strip()
    return (f'<div class="{c}" aria-label="Customer reviews">'
            f"<script defer async src='https://cdn.trustindex.io/loader.js?{TI_HERO_WIDGET}'></script>"
            '</div>')

def hero_review_row(bullets_html=""):
    """Hero panel: optional bullets, then the Trustindex review widget with the
    'top rated' badge beside it (side-by-side on desktop, wrapping on mobile)."""
    bullets = f'<div class="mt-6">{bullets_html}</div>' if bullets_html else ""
    badge = ('<div class="ti-hero pt-[15px]" aria-label="Top rated service rating">'
             "<script defer async src='https://cdn.trustindex.io/loader.js?cd741d573fcc673344062ffdcd3'></script>"
             '</div>')
    return f'{bullets}<div class="mt-6 flex flex-wrap items-center gap-4">{review_card()}{badge}</div>'

def make_prose_styler(seed, photos=None, span="lg:col-span-10 lg:col-start-2"):
    """Returns styled(inner_html, bg) applying the storage blueprint to prose sections:
      - cream rows -> rotating cards (variants 1/2/3); every other card carries a
        topical photo, alternating left/right;
      - white prose rows -> alternating faded logo watermark / faded side photos.
    `photos`: list of (filename, alt) relevant to the page; defaults to page_photos(seed).
    Pass photos=[] to suppress imagery (text cards + logo watermarks only) — use this on
    off-topic pages (e.g. blog) where a removals photo wouldn't match the subject."""
    pool = photos if photos is not None else page_photos(seed, 12)
    st = {"card": 0, "side": 0, "mr": 0}
    used = {pool[0][0]} if pool else set()
    def styled(inner, bg):
        if pool and inner.count("<p") >= 2:   # site rule: 2+ paragraphs -> topic-matched split media rows
            st["mr"] += 1
            return media_rows(inner, f"{seed}-mr{st['mr']}", bg, used=used, group=2)
        if not pool:   # deliberately image-less pages (calculators / off-topic): keep text-only
            if bg == "bg-beige":
                i = st["card"]; st["card"] += 1
                return content_card(inner, variant=(i % 3) + 1, bg=bg)
            return section(prose(inner, span=span), bg=bg, extra="logo-row overflow-hidden")
        # every content row carries a real, topic-matched image beside the text
        side = "left" if st["side"] % 2 == 1 else "right"; st["side"] += 1
        photo = _row_photo(seed, inner, used, st["side"])
        if bg == "bg-beige":
            i = st["card"]; st["card"] += 1
            return content_card(inner, variant=(i % 3) + 1, bg=bg, photo=photo, img_side=side)
        return _split_row(inner, photo, reverse=(side == "left"), bg=bg)
    return styled

# Step-process sets — same 8-card design + same icon set, relabelled per topic.
PROC_STEPS_REMOVAL = [
    ("Home Survey", "On site, online or by phone", "home-survey-clipboard", "Home survey clipboard checklist icon"),
    ("Quotation", "", "quotation-price-clipboard", "Removals quotation price clipboard icon"),
    ("Quotation Acceptance", "", "quotation-acceptance-handshake", "Quotation acceptance handshake icon"),
    ("Packing Day", "24 hrs before", "packing-day-24-hours-clock", "Packing day 24 hours clock icon"),
    ("Move Day", "", "move-day-van-calendar", "Move day removal van and calendar icon"),
    ("Unloading at New Address", "", "unloading-at-new-address-box", "Unloading boxes at the new address icon"),
    ("Placing Furniture &amp; Flatpack", "(Optional extra)", "placing-furniture-flatpack-hand", "Placing furniture and flatpack assembly icon"),
    ("Happy Customers in New Home", "", "happy-customers-new-home-family", "Happy customers in their new home icon"),
]
PROC_STEPS_PACKING = [
    ("Home Survey", "On site, online or by phone", "home-survey-clipboard", "Home survey clipboard checklist icon"),
    ("Your Packing Quote", "", "quotation-price-clipboard", "Packing quotation price clipboard icon"),
    ("Booking Confirmed", "", "quotation-acceptance-handshake", "Packing booking confirmed handshake icon"),
    ("Materials Delivered", "Boxes, wrap &amp; tape", "unloading-at-new-address-box", "Packing materials and boxes delivered icon"),
    ("Packing Day", "", "packing-day-24-hours-clock", "Professional packing day icon"),
    ("Wrapped &amp; Labelled", "", "placing-furniture-flatpack-hand", "Belongings wrapped and labelled with care icon"),
    ("Loaded &amp; Transported", "", "move-day-van-calendar", "Loaded and transported in our van icon"),
    ("Unpacked &amp; Settled", "(Optional extra)", "happy-customers-new-home-family", "Unpacked and settled into the new home icon"),
]
PROC_STEPS_STORAGE = [
    ("Home Survey", "On site, online or by phone", "home-survey-clipboard", "Home survey clipboard checklist icon"),
    ("Your Storage Quote", "", "quotation-price-clipboard", "Storage quotation price clipboard icon"),
    ("Booking Confirmed", "", "quotation-acceptance-handshake", "Storage booking confirmed handshake icon"),
    ("We Pack &amp; Collect", "", "unloading-at-new-address-box", "We pack and collect your belongings icon"),
    ("Transport to Our Store", "", "move-day-van-calendar", "Transport to our secure store icon"),
    ("Secure Containerised Storage", "", "placing-furniture-flatpack-hand", "Securely stored in containerised units icon"),
    ("Access or Long-Term", "Short or long term", "packing-day-24-hours-clock", "Access or long-term storage duration icon"),
    ("Returned When Ready", "", "happy-customers-new-home-family", "Belongings returned to you when ready icon"),
]
_PROC_INTRO = {
    "removal": ("Whether you&rsquo;re moving locally or internationally, downsizing or expanding, trust the "
                "removal experts committed to making your move simple and stress-free."),
    "packing": ("From the first box to the last, our trained team protects everything you own &mdash; "
                "here&rsquo;s how our professional packing service works, step by step."),
    "storage": ("Clean, dry, secure containerised storage for as long as you need it &mdash; here&rsquo;s how "
                "storing your belongings with Wolves Removals works, step by step."),
}

def process_topic(name):
    """Map a service/page name to the topic word used in the step-process heading."""
    n = (name or "").lower()
    if "packing" in n: return "Packing"
    if "storage" in n: return "Storage"
    if "commercial" in n or "office" in n: return "Commercial Removal"
    if "international" in n: return "International Removal"
    if "european" in n: return "European Removal"
    if "man" in n and "van" in n: return "Man &amp; Van"
    return "Removal"

def step_process(bg="bg-beige", topic="Removal", heading=None, intro=None):
    """Shared chevron step-process section. `topic` tailors the heading + the 8 step
    labels to the page (Removal / Packing / Storage); the design is identical site-wide."""
    t = topic.lower()
    if "packing" in t:
        steps, ptype = PROC_STEPS_PACKING, "packing"
    elif "storage" in t:
        steps, ptype = PROC_STEPS_STORAGE, "storage"
    else:
        steps, ptype = PROC_STEPS_REMOVAL, "removal"
    heading = heading or f"Our Step-by-Step {topic} Process"
    intro = intro or _PROC_INTRO[ptype]
    cells = ""
    for i, (title, sub, slug, alt) in enumerate(steps):
        ico = img(f"images/process/wolves-removals-process-{slug}-icon.webp", alt,
                  cls="w-14 h-14 xl:w-16 xl:h-16 object-contain")
        sub_html = f'<div class="uppercase text-darkgrey group-hover:text-beige leading-snug text-sm xl:text-base">{sub}</div>' if sub else ""
        cells += (
            '<div class="proc-step group transition-colors duration-100 hover:bg-darkgrey shrink-0 w-[85%] sm:w-[60%] md:w-auto snap-center relative flex items-center gap-3 bg-lightgrey pl-7 pr-12 py-7 min-h-full">'
            f'<span class="absolute top-3 left-6 font-bold text-darkgrey group-hover:text-white text-lg">{i+1}.</span>'
            '<div class="flex-1 min-w-0">'
            f'<div class="uppercase font-bold text-black group-hover:text-white leading-snug text-base xl:text-lg">{title}</div>'
            f'{sub_html}</div>'
            '<div class="ico-badge shrink-0 w-[5.25rem] h-[5.25rem] xl:w-24 xl:h-24 '
            f'shadow-[0_8px_18px_-6px_rgba(0,0,0,0.16)]">{ico}</div>'
            '</div>')
    dots = "".join(
        f'<button type="button" class="proc-dot{" is-active" if i == 0 else ""}" data-i="{i}" aria-label="Go to step {i+1}"></button>'
        for i in range(len(steps)))
    return section(
        f'<div class="text-center mb-8 lg:mb-10"><h2 class="relative leading-tight text-black">{heading}</h2>'
        f'<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{intro}</p></div>'
        '<div data-proc>'
        '<div class="flex md:grid md:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6 auto-rows-fr '
        'overflow-x-auto md:overflow-visible snap-x snap-mandatory proc-scroll -mx-4 px-4 md:mx-0 md:px-0 pb-2 md:pb-0">'
        f'{cells}</div>'
        f'<div class="proc-dots md:hidden" role="tablist" aria-label="Step navigation">{dots}</div>'
        '</div>'
        f'<script defer src="/js/process-carousel.js?v={ASSET_VER}"></script>',
        bg=bg)

def cta_band(heading, text_html, button_label, button_href, bg="bg-lightgrey", photos=None):
    """Centred heading + text + button, flanked by two contextual photos that
    fade into the section background on both sides (like the original site)."""
    if photos is None:
        photos = page_photos(heading, 2)
    end = "white" if "white" in bg else "lightgrey"   # fade colour = section background
    lp, rp = photos[0], photos[1]
    left = (f'<div class="hidden md:block absolute inset-y-0 left-0 w-[15%] lg:w-1/6" aria-hidden="true">'
            f'{photo_block(lp)}'
            f'<div class="absolute inset-0 bg-gradient-to-r from-{end}/10 via-{end}/75 to-{end}"></div></div>')
    right = (f'<div class="hidden md:block absolute inset-y-0 right-0 w-[15%] lg:w-1/6" aria-hidden="true">'
             f'{photo_block(rp)}'
             f'<div class="absolute inset-0 bg-gradient-to-l from-{end}/10 via-{end}/75 to-{end}"></div></div>')
    content = (
        '<div class="container relative z-10">'
        '<div class="max-w-4xl mx-auto text-center">'
        f'<h2 class="relative leading-tight text-black">{esc(heading)}</h2>'
        f'<div class="text-lg xl:text-xl font-medium mt-2">{text_html}</div>'
        f'<a href="{button_href}" class="button-orange mt-6 xl:mt-8 mx-auto inline-flex items-center gap-3">{esc(button_label)}</a>'
        '</div></div>')
    return (f'<section class="relative {bg} w-full overflow-hidden pt-10 lg:pt-20 pb-10 lg:pb-20 border-border">'
            f'{left}{right}{content}</section>')

def quote_bar(lead="Get a Free", rest="Home Removal Quote",
              subtext="Find out how much your home move will cost.",
              button_label="Get a Free Quote", button_href="/get-a-quote/"):
    """Slim slate CTA bar: split heading + subtext on the left, click-to-call
    number and orange quote button on the right (stacks centred on mobile)."""
    b = S.BUSINESS
    head = ('<div class="text-center lg:text-left">'
            f'<h2 class="text-white text-2xl lg:text-3xl mb-1"><span class="text-beige">{esc(lead)}</span> {esc(rest)}</h2>'
            f'<p class="text-white/90 font-medium mb-0 normal-case">{esc(subtext)}</p></div>')
    phone = (f'<a href="{b["phone_link"]}" class="inline-flex items-center gap-2 text-white font-bold text-lg xl:text-xl '
             f'hover:text-orange whitespace-nowrap" aria-label="Call Wolves Removals on {b["phone"]}">'
             f'{icon("phone","w-5 h-5 text-beige")}<span>{b["phone"]}</span></a>')
    btn = f'<a href="{button_href}" class="button-orange whitespace-nowrap">{esc(button_label)}</a>'
    actions = f'<div class="flex flex-wrap items-center justify-center gap-x-7 gap-y-4 shrink-0">{phone}{btn}</div>'
    return ('<section class="bg-darkgrey w-full py-7 lg:py-9 border-border">'
            '<div class="container"><div class="flex flex-col lg:flex-row items-center lg:justify-between gap-6">'
            f'{head}{actions}</div></div></section>')

# Card rollover alternates creme (light → keep dark text) and grey (dark → white text). No orange/green.
CARD_HOVER = [
    ("card-hov-creme hover:bg-[#dad6c2] hover:border-black", ""),              # creme hover, dark text
    ("hover:bg-darkgrey hover:border-darkgrey", " group-hover:text-white"),    # grey hover, white text
]

# Simple line-art pictograms (currentColor) used beside card headings, like the old site.
PICTOGRAMS = {
    "house": '<path d="M12 3 2 11h3v9h6v-6h2v6h6v-9h3z"/>',
    "office": '<path d="M3 21V3h11v6h7v12H3zm2-2h4V5H5v14zm6 0h8v-8h-5v2h-3v6zM7 7h2V5H7zm0 4h2V9H7zm0 4h2v-2H7z"/>',
    "globe": '<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm6.9 6h-2.9a15 15 0 00-1.3-3.6A8 8 0 0118.9 8zM12 4c.8 0 2 1.5 2.6 4H9.4C10 5.5 11.2 4 12 4zM4.3 14a8 8 0 010-4h3.1a18 18 0 000 4zm.8 2h2.9a15 15 0 001.3 3.6A8 8 0 015.1 16zM12 20c-.8 0-2-1.5-2.6-4h5.2C14 18.5 12.8 20 12 20zm.6-6H9.4a16 16 0 010-4h5.2a16 16 0 010 4zm2 2h2.9a8 8 0 01-4.2 3.6A15 15 0 0014.6 16zm.5-2a18 18 0 000-4h3.1a8 8 0 010 4z"/>',
    "van": '<path d="M2 6h12v9H2zm13 3h3.2l2.8 3v3h-6zM6 16a2 2 0 100 4 2 2 0 000-4zm10 0a2 2 0 100 4 2 2 0 000-4z"/>',
    "box": '<path d="M12 2l9 4v12l-9 4-9-4V6zm0 2.2L5.5 7 12 9.8 18.5 7zM5 8.6V17l6 2.7v-8.4zm14 0-6 2.7v8.4l6-2.7z"/>',
    "boxes": '<path d="M3 3h8v8H3zm10 5h8v13h-8zM3 13h8v8H3z"/>',
    "student": '<path d="M12 3 1 8l11 5 9-4.1V15h2V8zM5 12.7V16c0 1.7 3.1 3 7 3s7-1.3 7-3v-3.3l-7 3.2z"/>',
    "piano": '<path d="M3 4h18v16H3zm3 1v9h2V5zm4 0v9h2V5zm4 0v9h2V5z"/>',
    "antique": '<path d="M8 2h8v2a4 4 0 01-1.5 3.1A5 5 0 0118 12v6a3 3 0 01-3 3H9a3 3 0 01-3-3v-6a5 5 0 013.5-4.9A4 4 0 018 4z"/>',
    "glove": '<path d="M7 22a6 6 0 01-2-4.5V11a1.5 1.5 0 013 0V8a1.5 1.5 0 013 0V7a1.5 1.5 0 013 0v2a1.5 1.5 0 013 0v6a7 7 0 01-2 5z"/>',
    "pin": '<path d="M12 2a7 7 0 00-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/>',
    "doc": '<path d="M6 2h8l4 4v16H6zm8 1.5V7h3.5zM8 11h8v1.5H8zm0 3h8v1.5H8zm0 3h5v1.5H8z"/>',
    "spark": '<path d="M12 2l2.4 6.2L21 10l-6.6 1.8L12 18l-2.4-6.2L3 10l6.6-1.8z"/>',
    "pound": '<path d="M6 20v-1.8c1.2-.3 2-1.3 2-2.7V13H6.2v-1.6H8V9.4A4 4 0 0 1 15.8 8l-1.7.9A2 2 0 0 0 10 9.4v2h3.4V13H10v2.5c0 .9-.3 1.7-.9 2.3H18V20z"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.4 9.3-8 11-4.6-1.7-8-6-8-11V5z"/>',
    "help": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 16.2a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6zm1.7-6.3c-.7.5-.9.8-.9 1.4v.3h-1.7v-.4c0-1 .4-1.6 1.2-2.1.7-.5.9-.7.9-1.2 0-.6-.5-1-1.2-1-.7 0-1.2.4-1.5 1.1l-1.5-.7A3.1 3.1 0 0 1 11.9 7c1.8 0 3 1 3 2.5 0 1-.4 1.6-1.2 2.1z"/>',
    "clock": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 5h-2v6l5 3 1-1.7-4-2.3z"/>',
}

def _faq_icon(question):
    """Pick a topic pictogram for a FAQ from keywords in its question."""
    q = str(question).lower()
    table = [
        ("how much", "pound"), ("cost", "pound"), ("price", "pound"), ("pricing", "pound"),
        ("quote", "pound"), ("deposit", "pound"), ("£", "pound"), ("pay", "pound"),
        ("insur", "shield"), ("protect", "shield"), ("damage", "shield"), ("safe", "shield"),
        ("lapada", "shield"), ("checkatrade", "shield"), ("guarantee", "shield"),
        ("area", "pin"), ("where", "pin"), ("town", "pin"), ("postcode", "pin"),
        ("location", "pin"), ("travel", "pin"), ("distance", "pin"), ("nationwide", "pin"),
        ("pack", "box"), ("material", "box"), ("wrap", "box"), ("fragile", "box"), ("box", "box"),
        ("storage", "boxes"), ("store", "boxes"),
        ("advance", "clock"), ("how long", "clock"), ("when", "clock"), ("notice", "clock"),
        ("book", "clock"), ("same-day", "clock"), ("short-notice", "clock"), ("date", "clock"),
        ("time", "clock"), ("day", "clock"), ("timing", "clock"),
        ("piano", "piano"), ("antique", "antique"), ("valuable", "antique"), ("fine art", "antique"),
        ("student", "student"), ("man and van", "van"), ("clearance", "boxes"),
    ]
    for kw, name in table:
        if kw in q:
            return name
    return "help"

def _pictogram(title, href):
    key = (str(href) + " " + str(title)).lower()
    table = [("commercial", "office"), ("office", "office"), ("international", "globe"),
             ("european", "globe"), ("student", "student"), ("piano", "piano"),
             ("antique", "antique"), ("white-glove", "glove"), ("white glove", "glove"),
             ("man-and-van", "van"), ("man and van", "van"), ("contract-delivery", "van"),
             ("delivery", "van"), ("removal-services", "van"), ("storage", "boxes"),
             ("packing", "box"), ("materials", "box"), ("box shop", "box"),
             ("house-clearance", "boxes"), ("clearance", "boxes"), ("house", "house"),
             ("/locations/", "pin"), ("removals", "van")]
    name = "spark"
    for kw, ic in table:
        if kw in key:
            name = ic
            break
    if "/blog/" in key or (href and href.strip("/") and "/" not in href.strip("/") and "removal" not in key):
        # root-level slugs are blog posts
        pass
    return f'<svg viewBox="0 0 24 24" class="w-10 h-10" fill="currentColor" aria-hidden="true">{PICTOGRAMS.get(name, PICTOGRAMS["spark"])}</svg>'

def _seed_from_href(href):
    """Map a card's link to the seed its destination page uses for page_photos(),
    so the card image == the linked page's hero (i.e. matches what the card references)."""
    h = (href or "").strip("/")
    for pref in ("services/", "locations/", "helpful-tips/"):
        if h.startswith(pref):
            return h[len(pref):]
    return h  # blog posts live at root

def card_grid(cards, cols=3, heading=None, intro=None, bg="bg-white", bg_image=None):
    """cards: list of (title, href, body_html). Each card carries a full-bleed image =
    the hero of the page it links to. Padded to full rows (no orphans)."""
    colcls = {2: "md:col-span-6", 3: "md:col-span-6 lg:col-span-4", 4: "md:col-span-6 lg:col-span-3"}[cols]
    cells = []
    for i, card in enumerate(cards):
        # Cards accept (title, href, body) or (title, href, body, photo). With a photo,
        # a 16:10 hero image tops the card (e.g. blog articles); without one, a brand
        # pictogram sits beside the heading. White card, brand border, hover fills a
        # rotating brand colour. Visible CTA is descriptive (never bare "Read more").
        title, href, body = card[0], card[1], card[2]
        photo = card[3] if len(card) > 3 else None
        hov_bg, hov_text = CARD_HOVER[i % len(CARD_HOVER)]
        snippet = re.sub(r"</?p[^>]*>", "", body, flags=re.I).strip()  # un-wrap a single <p>
        cta = f'Read more about {esc(title)}'
        if photo:
            media = ('<div class="overflow-hidden" style="aspect-ratio:16/10;">'
                     + img("images/photos/" + photo[0] + ".webp", photo[1], cls="w-full h-full object-cover")
                     + '</div>')
            cells.append(
                f'<div class="col-span-12 {colcls}"><a href="{href}" class="card-rollover group flex flex-col h-full bg-white border-2 border-darkgrey rounded-xl shadow-custom overflow-hidden transition {hov_bg}">'
                f'{media}'
                f'<div class="flex flex-col flex-1 p-6">'
                f'<h3 class="text-xl font-semibold text-black{hov_text}">{esc(title)}</h3>'
                f'<p class="mt-3 flex-1 text-darkgrey{hov_text} line-clamp-3 mb-0">{snippet}</p>'
                f'<span class="mt-4 font-bold uppercase text-blue{hov_text} inline-flex items-center gap-1">{cta} {icon("chevron","h-4 w-4 -rotate-90 fill-current")}</span>'
                f'</div></a></div>')
        else:
            pic = _pictogram(title, href)
            cells.append(
                f'<div class="col-span-12 {colcls}"><a href="{href}" class="card-rollover group flex flex-col h-full bg-white border-2 border-darkgrey rounded-xl shadow-custom p-6 transition {hov_bg}">'
                f'<div class="flex items-start gap-4"><span class="ico-badge shrink-0 w-14 h-14">{pic}</span>'
                f'<h3 class="text-xl font-semibold text-black{hov_text}">{esc(title)}</h3></div>'
                f'<p class="mt-3 flex-1 text-darkgrey{hov_text} line-clamp-3 mb-0">{snippet}</p>'
                f'<span class="mt-4 font-bold uppercase text-blue{hov_text} inline-flex items-center gap-1">{cta} {icon("chevron","h-4 w-4 -rotate-90 fill-current")}</span>'
                f'</a></div>')
    head = ""
    if heading:
        head = f'<div class="text-center mb-8"><h2 class="relative leading-tight text-black">{esc(heading)}</h2>'
        head += (f'<div class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">{intro}</div>' if intro else "") + "</div>"
    grid = f'<div class="grid grid-cols-12 gap-6 lg:gap-8">{"".join(cells)}</div>'
    if bg_image:
        bgimg = img("images/photos/" + bg_image[0] + ".webp", bg_image[1], cls="w-full h-full object-cover")
        return (
            '<section class="relative bg-white w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
            f'<div class="absolute inset-0">{bgimg}</div>'
            '<div class="absolute inset-0 cardbg-fade"></div>'
            f'<div class="container relative z-10">{head}{grid}</div></section>')
    return section(head + grid, bg=bg)

# Fleet/team photos for the "Trusted ... Since 2016" trust block's faded flanks — picked
# per page so the trust band isn't an identical template on every page.
EEAT_FLANK_POOL = [
    ("wolves-removals-team-fleet-vans", "The Wolves Removals team with their fleet of removal vans"),
    ("wolves-vans-sussex-country-house", "Wolves Removals vans at a grand Sussex country house"),
    ("two-wolves-vans-sussex-manor", "Two Wolves Removals vans outside a Sussex manor house"),
    ("three-wolves-vans-sussex-house", "Three Wolves Removals vans outside a large Sussex house"),
    ("fleet-of-removal-vans-sussex", "The fleet of Wolves Removals vans in Sussex"),
    ("wolves-vans-residential-street", "Two branded Wolves Removals vans on a residential street"),
    ("wolves-van-outside-customer-home", "A Wolves Removals van outside a customer's home"),
    ("removals-van-fleet-field-3", "The Wolves Removals van fleet parked in a field"),
]

def eeat_flank(seed, used=()):
    """Two page-seeded fleet/team photos for the trust block's faded flanks — varied per
    page and avoiding photos already used on the page (R9-safe)."""
    avail = [p for p in EEAT_FLANK_POOL if p[0] not in used] or EEAT_FLANK_POOL
    o = zlib.crc32(str(seed).encode()) % len(avail)
    return [avail[o], avail[(o + 1) % len(avail)]]

STORAGE_CTA_COLS = [
    ("Long-Term Storage", "/services/storage/long-term-storage/",
     "Ideal for extended storage between moves, downsizing or freeing up space. Flexible, affordable terms from three months or more."),
    ("Short-Term Storage", "/services/storage/short-term-storage/",
     "Perfect for moving delays, renovations or temporary storage during transitions &mdash; from a couple of days to a few months."),
    ("Business Storage", "/services/storage/business-and-commercial-storage/",
     "Secure storage for stock, equipment, office furniture and business moves. Fully managed, including packing and unpacking."),
]

STORAGE_CTA_BGS = [
    ("containerised-storage-units-wolves-store", "Containerised storage units at the Wolves Removals store"),
    ("forklift-lifting-storage-crate", "A forklift lifting a storage crate at the Wolves Removals store"),
    ("stacked-storage-containers-warehouse", "Stacked wooden storage containers in the storage warehouse"),
    ("removal-van-outside-storage-warehouse", "A Wolves Removals van outside the secure storage warehouse"),
    ("secure-container-storage-warehouse-interior", "Inside the clean, secure containerised storage warehouse"),
    ("row-of-mobile-storage-containers", "A row of Wolves Removals mobile storage containers"),
    ("a-forklift-handling-containerised-removals-storage", "A forklift handling containerised removals storage"),
    ("wolves-van-secure-storage-facility", "A Wolves Removals van at the secure storage facility"),
]

def storage_cta(bg_photo=None, bg="bg-darkgrey", seed=None):
    """Storage promo CTA — three storage types over a faded slate photo, to drive
    visitors into storage. With `seed` (a page key) the faded background photo is chosen
    per page from STORAGE_CTA_BGS, so the band isn't an identical template on every page."""
    if bg_photo is None:
        bg_photo = (STORAGE_CTA_BGS[zlib.crc32(str(seed).encode()) % len(STORAGE_CTA_BGS)]
                    if seed is not None else STORAGE_CTA_BGS[0])
    cells = ""
    for title, href, desc in STORAGE_CTA_COLS:
        cells += (
            '<div class="col-span-12 md:col-span-4 flex flex-col items-center text-center">'
            f'<h3 class="text-xl xl:text-2xl font-bold uppercase text-white leading-tight">{esc(title)}</h3>'
            f'<p class="mt-3 text-white/95 text-base xl:text-lg flex-1">{desc}</p>'
            f'<a href="{href}" class="button-orange btn-white mt-6 w-full sm:w-auto justify-center text-center">Explore {esc(title)}</a>'
            '</div>')
    bgimg = img("images/photos/" + bg_photo[0] + ".webp", bg_photo[1], cls="w-full h-full object-cover")
    heading = ('Need <span class="text-[#dad6c2]">Long or Short-Term Storage</span> for '
               '<span class="text-[#dad6c2]">Your Home or Business</span>?')
    return (
        f'<section class="relative {bg} w-full overflow-hidden pt-12 lg:pt-20 pb-12 lg:pb-20 border-border">'
        f'<div class="absolute inset-0">{bgimg}</div>'
        '<div class="absolute inset-0 storage-cta-overlay"></div>'
        '<div class="container relative z-10">'
        f'<div class="text-center mb-9 lg:mb-12"><h2 class="storage-cta-head text-white leading-tight">{heading}</h2></div>'
        f'<div class="grid grid-cols-12 gap-8 lg:gap-12">{cells}</div>'
        '</div></section>')

def faq_block(faqs, heading="Frequently Asked Questions", bg="bg-lightgrey", fancy=True, extra=""):
    """faqs: list of (question, answer_html_or_text). Returns (html, schema_dict).
    fancy=True uses the bespoke card layout: a topic icon per FAQ + rollover effect."""
    items = []
    for q, a in faqs:
        if fancy:
            picto = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="w-6 h-6">'
                     f'{PICTOGRAMS.get(_faq_icon(q), PICTOGRAMS["help"])}</svg>')
            items.append(
                '<div class="faq-card" x-data="{open:false}" :class="open && \'is-open\'">'
                '<button type="button" class="faq-head" @click="open=!open" :aria-expanded="open">'
                f'<span class="faq-ico">{picto}</span>'
                f'<span class="faq-q">{esc(q)}</span>'
                f'<span class="faq-toggle" :class="open && \'is-open\'">{icon("chevron","w-5 h-5 fill-current")}</span>'
                '</button>'
                f'<div class="faq-body" x-show="open" x-cloak x-transition.duration.200ms>{a}</div>'
                '</div>')
        else:
            items.append(
                f'<div class="border-b border-border py-4" x-data="{{open:false}}">'
                f'<button type="button" class="w-full flex items-center justify-between text-left bg-transparent" @click="open=!open" :aria-expanded="open">'
                f'<span class="text-lg xl:text-xl font-semibold text-black">{esc(q)}</span>'
                f'<span :class="open?\'rotate-180\':\'\'" class="transition-transform">{icon("chevron","h-6 w-6 fill-current text-orange")}</span></button>'
                f'<div class="mt-3 text-darkgrey" x-show="open" x-cloak x-transition.duration.200ms>{a}</div></div>')
    span = "lg:col-span-10 lg:col-start-2" if fancy else "lg:col-span-8 lg:col-start-3"
    body = f'<div class="faq-list">{"".join(items)}</div>' if fancy else "".join(items)
    html_out = section(
        f'<div class="grid grid-cols-12"><div class="col-span-12 {span}">'
        f'<div class="text-center mb-6 lg:mb-8"><h2 class="relative leading-tight text-black">{esc(heading)}</h2></div>'
        f'{body}</div></div>', bg=bg, extra=extra)
    schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": _html.unescape(_strip_tags(a))}}
            for q, a in faqs]
    }
    return html_out, schema

def _strip_tags(t):
    import re
    return re.sub(r"<[^>]+>", "", str(t)).strip()

# ---------------------------------------------------------------- SCHEMA
def schema_localbusiness():
    b = S.BUSINESS
    return {
        "@context": "https://schema.org", "@type": "MovingCompany",
        "@id": S.SITE_URL + "/#business",
        "name": b["name"], "legalName": b["legal_name"], "url": S.SITE_URL,
        "telephone": b["phone"], "email": b["email"],
        "image": abs_url("images/brand/wolves-removals-logo.png"),
        "logo": abs_url("images/brand/wolves-removals-logo.png"),
        "address": {"@type": "PostalAddress", "streetAddress": b["street"],
                    "addressLocality": b["locality"], "addressRegion": b["region"],
                    "postalCode": b["postcode"], "addressCountry": "GB"},
        "geo": {"@type": "GeoCoordinates", "latitude": b["geo"]["lat"], "longitude": b["geo"]["lng"]},
        "areaServed": [{"@type": "AdministrativeArea", "name": a} for a in b["area_served"]],
        "openingHours": b["hours"],
        "sameAs": list(S.SOCIAL.values()),
    }

def schema_breadcrumb(trail):
    """trail: list of (name, path)."""
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(p)}
            for i, (n, p) in enumerate(trail)]
    }

# ---------------------------------------------------------------- PAGE
def _dedupe_images(html, seen=None):
    """RULE: no /images/photos/ image may appear twice on a page. Each repeat is
    swapped for an unused pool photo (correct alt + dimensions, same classes).
    Pass a shared `seen` set to chain de-dup across several HTML fragments."""
    if seen is None:
        seen = set()
    alt_by = {p[0]: p[1] for p in PHOTOS}
    pool = [p[0] for p in PHOTOS if p[0] != QUOTE_BAND_PHOTO]
    def repl(m):
        tag = m.group(0)
        stem = m.group(1).rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if stem not in seen:
            seen.add(stem)
            return tag
        for cand in pool:
            if cand not in seen:
                seen.add(cand)
                cm = re.search(r'class="([^"]*)"', tag)
                cls = cm.group(1) if cm else ""
                eager = ('fetchpriority="high"' in tag) or ('loading="eager"' in tag)
                return img("images/photos/" + cand + ".webp", alt_by.get(cand, "Wolves Removals Sussex move"), cls=cls, eager=eager)
        return tag
    return re.sub(r'<img\b[^>]*?\bsrc="(/images/photos/[^"]+)"[^>]*?>', repl, html)

def trust_reviews_row():
    """Two Trustindex review widgets side-by-side in one row. Added sitewide
    (except the /reviews/ page) just above the footer so the content flows into it.
    58be6f… sits on the left, 7530e3… on the right."""
    return (
        '<section class="relative bg-lightgrey w-full pt-8 lg:pt-16 pb-8 lg:pb-16 border-border overflow-hidden">'
        '<div class="container"><div class="flex justify-center mb-8 lg:mb-10">'
        '<div class="ti-reviews-widget max-w-full">'
        "<script defer async src='https://cdn.trustindex.io/loader.js?cd741d573fcc673344062ffdcd3'></script>"
        '</div></div></div>'
        '<div style="max-width:1720px;margin-left:auto;margin-right:auto;padding-left:1rem;padding-right:1rem;">'
        '<div class="ti-reviews-widget w-full">'
        "<script defer async src='https://cdn.trustindex.io/loader.js?c457a627393e67277d368b8df3b'></script>"
        '</div></div></section>')

_BLOG_FEED_CACHE = None
def blog_feed(n=10):
    """Sitewide 'Latest from our blog' strip — identical carousel design to the old
    Facebook feed, but server-rendered from the newest blog posts as links (no JS
    feed/lightbox; arrows scroll the track via Alpine). Computed once and cached."""
    global _BLOG_FEED_CACHE
    if _BLOG_FEED_CACHE is not None:
        return _BLOG_FEED_CACHE
    import glob as _glob, json as _json
    from datetime import datetime as _dt
    bdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "blog")
    posts = []
    for f in _glob.glob(os.path.join(bdir, "*.json")):
        try:
            p = _json.load(open(f, encoding="utf-8"))
            if p.get("slug") and (p.get("h1") or p.get("title")):
                posts.append(p)
        except Exception:
            pass
    posts.sort(key=lambda p: p.get("date", "2024-01-01"), reverse=True)
    art_icon = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" class="w-5 h-5">'
                '<path d="M5 3h11l4 4v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm10 1.5V8h3.5L15 4.5zM7 10h10v1.6H7zm0 3.6h10v1.6H7zm0 3.6h7v1.6H7z"/></svg>')
    import urllib.parse as _ul
    cards = []; data = []
    for i, p in enumerate(posts[:n]):
        slug = p["slug"]; title = (p.get("h1") or p.get("title"))
        cat = p.get("category", "Moving Advice")
        pic = page_photos(slug, 1)[0]; img_src = "/images/photos/" + pic[0] + ".webp"
        try:
            d = _dt.strptime(p.get("date", "2024-01-01"), "%Y-%m-%d").strftime("%-d %b %Y")
        except Exception:
            d = ""
        absu = abs_url(slug + "/"); eu = _ul.quote(absu, safe=""); et = _ul.quote(title, safe="")
        data.append({"img": img_src, "alt": pic[1], "title": title, "cat": cat, "date": d,
                     "url": "/%s/" % slug, "abs": absu,
                     "fb": "https://www.facebook.com/sharer/sharer.php?u=" + eu,
                     "x": "https://twitter.com/intent/tweet?text=" + et + "&url=" + eu,
                     "wa": "https://wa.me/?text=" + _ul.quote(title + " " + absu, safe=""),
                     "em": "mailto:?subject=" + et + "&body=" + eu})
        cards.append(
            f'<a class="social-card" href="/{slug}/" aria-label="Open article: {esc(title)}" @click.prevent="active={i};open=true">'
            f'<img class="social-img" src="{img_src}" alt="{esc(pic[1])}" loading="lazy" decoding="async" width="600" height="600">'
            '<span class="social-fade" aria-hidden="true"></span>'
            f'<span class="social-meta"><span class="social-date">{esc(d)}</span><span class="social-fb">{art_icon}</span></span>'
            '<span class="social-hover" aria-hidden="true">'
            f'<span class="social-hover-top">{esc(cat)}</span>'
            f'<span class="social-cap">{esc(title)}</span>'
            '<span class="social-readmore">Enlarge &amp; read &rarr;</span>'
            '</span></a>')
    arrows = (
        '<button type="button" class="social-arrow social-prev" aria-label="Previous articles" '
        '@click="$refs.track.scrollBy({left:-($refs.track.clientWidth*0.8),behavior:\'smooth\'})">'
        '<svg viewBox="0 0 24 24" class="w-6 h-6" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg></button>'
        '<button type="button" class="social-arrow social-next" aria-label="More articles" '
        '@click="$refs.track.scrollBy({left:$refs.track.clientWidth*0.8,behavior:\'smooth\'})">'
        '<svg viewBox="0 0 24 24" class="w-6 h-6" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>')
    head = ('<div class="text-center mb-8"><div class="relative leading-tight text-black font-bold uppercase text-3xl 2xl:text-4xl mb-4">Latest From Our Blog</div>'
            '<p class="text-lg xl:text-xl font-medium mt-2 max-w-3xl mx-auto">Practical moving tips, packing advice and local guides from our Sussex removals team. '
            '<a href="/blog/">Browse all articles</a> to keep up to date.</p></div>')
    posts_json = _json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    _fb='<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.8-1.6 1.5V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>'
    _x='<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5" aria-hidden="true"><path d="M18.9 2H22l-7.3 8.3L23 22h-6.6l-5-6.7L5.6 22H2.5l7.8-8.9L2 2h6.8l4.6 6.2L18.9 2zm-2.3 18h1.8L7.5 3.9H5.6L16.6 20z"/></svg>'
    _wa='<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.5A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.8.9.9-2.7-.2-.3A8 8 0 1 1 12 20zm4.4-5.6c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.6-1.2.1-.2 0-.3 0-.4l-.8-1.9c-.2-.4-.4-.4-.5-.4h-.5c-.2 0-.4.1-.6.3-.8.8-.9 1.9-.4 3 .9 2.1 2.5 3.7 4.6 4.6 1.4.6 2 .6 2.7.5.5-.1 1.4-.6 1.6-1.1.2-.5.2-1 .1-1.1-.1-.1-.2-.1-.4-.2z"/></svg>'
    _em='<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5" aria-hidden="true"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm8 7L4 6.2V18h16V6.2L12 11z"/></svg>'
    _cp='<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5" aria-hidden="true"><path d="M16 1H4a2 2 0 0 0-2 2v12h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/></svg>'
    def _sh(field, lbl, svg, blank=True):
        t = ' target="_blank" rel="noopener nofollow"' if blank else ''
        return f'<a class="blog-share-btn" :href="posts[active].{field}"{t} aria-label="{lbl}">{svg}</a>'
    share = (
        '<div class="blog-share"><span class="blog-share-label">Share this article</span><div class="blog-share-row">'
        + _sh("fb", "Share on Facebook", _fb) + _sh("x", "Share on X", _x)
        + _sh("wa", "Share on WhatsApp", _wa) + _sh("em", "Share by email", _em, blank=False)
        + '<button type="button" class="blog-share-btn" @click="navigator.clipboard&amp;&amp;navigator.clipboard.writeText(posts[active].abs);$el.classList.add(\'is-copied\')" aria-label="Copy link">'
        + _cp + '</button></div></div>')
    modal = (
        '<div class="social-lightbox" x-show="open" x-cloak x-transition.opacity '
        '@keydown.escape.window="open=false" @click.self="open=false">'
        '<button type="button" class="social-close" @click="open=false" aria-label="Close">&times;</button>'
        '<button type="button" class="social-nav social-nav-prev" aria-label="Previous article" @click="active=(active-1+posts.length)%posts.length">'
        '<svg viewBox="0 0 24 24" class="w-7 h-7" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg></button>'
        '<div class="social-modal" @click.stop>'
        '<div class="social-modal-img"><img :src="posts[active].img" :alt="posts[active].alt" width="1200" height="900"></div>'
        '<div class="social-modal-cap">'
        '<div class="social-modal-head"><span x-text="posts[active].cat"></span><span x-text="posts[active].date"></span></div>'
        '<p class="social-modal-text" x-text="posts[active].title"></p>'
        '<a class="button-orange inline-flex mt-1 mb-3" :href="posts[active].url">View blog</a>'
        + share +
        '</div></div>'
        '<button type="button" class="social-nav social-nav-next" aria-label="Next article" @click="active=(active+1)%posts.length">'
        '<svg viewBox="0 0 24 24" class="w-7 h-7" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>'
        '</div>')
    body = (f'<script type="application/json" id="blog-feed-data">{posts_json}</script>'
            '<div class="social-feed" x-data="{open:false,active:0,posts:JSON.parse(document.getElementById(\'blog-feed-data\').textContent)}">'
            f'<div class="social-wrap">{arrows}<div class="social-track" x-ref="track" role="list">{"".join(cards)}</div></div>'
            f'{modal}</div>')
    _BLOG_FEED_CACHE = section(head + body, bg="bg-lightgrey")
    return _BLOG_FEED_CACHE

def render_page(*, title, description, canonical_path, body, og_image=None,
                robots="index, follow", breadcrumb=None, extra_schema=None, active="", show_quote=True, dedupe=True, show_fabs=True,
                show_trust_reviews=True):
    # Hero pinning: if this page had a curated hero in the 'Old wolves site' snapshot,
    # restore it — swap the eager hero <img> and point og/twitter/preload at it — so the
    # hero never drifts when the photo-rotation pool changes.
    _ov = OLD_HEROES.get(canonical_path)
    if _ov:
        _hsrc = "images/photos/" + _ov[0] + ".webp"
        if os.path.exists(os.path.join(S.ROOT, _hsrc)):
            _hero_img = img(_hsrc, _ov[1], cls="w-full h-full object-cover", eager=True)
            body, _hn = re.subn(r'<img\b[^>]*\bfetchpriority="high"[^>]*>', lambda m: _hero_img, body, count=1)
            if _hn:
                og_image = _hsrc
    _seen = set()
    body = _dedupe_images(body, _seen) if dedupe else body
    body = split_adjacent_flanks(body)   # no two faded-flank rows back-to-back (site-wide)
    # Reviews row sits in-flow as ~row 5 (after the 4th top-level section) on every page
    # type. Location & About pages insert it manually at their own logical row 5 and pass
    # show_trust_reviews=False, so they skip this. The /reviews/ page never gets it.
    if show_trust_reviews and canonical_path != "/reviews/":
        _secs = [m.start() for m in re.finditer(r'<section\b', body)]
        _rv = trust_reviews_row()
        if len(_secs) >= 5:
            body = body[:_secs[4]] + _rv + "\n" + body[_secs[4]:]
        else:
            body = body + "\n" + _rv
    question = ""
    if show_quote:
        question = _dedupe_images(cta_band(
            "Have a Removals Question?",
            'Feel free to <a href="/contact-us/">contact us</a>, browse our '
            '<a href="/gallery/">gallery</a> or read our '
            '<a href="/frequently-asked-questions/">FAQs page</a> which is full of useful information.',
            "Get a Free Quote", "/get-a-quote/", bg="bg-white"), _seen)
    feed = _dedupe_images(blog_feed(), _seen) if dedupe else blog_feed()
    schema = [schema_localbusiness()]
    if breadcrumb:
        schema.append(schema_breadcrumb(breadcrumb))
    if extra_schema:
        schema += extra_schema if isinstance(extra_schema, list) else [extra_schema]
    doc = [
        head_html(title, description, canonical_path, og_image=og_image, robots=robots, schema=schema),
        f'<body class="font-body bg-white text-black overflow-x-clip text-base xl:text-lg{(" page-" + active) if active else ""}">',
        '<div id="page" class="relative min-h-screen block" x-data="{menuOpen:false}">',
        header_html(active=active),
        '<div id="content" class="site-content font-normal text-black">',
        '<main id="main" class="site-main" role="main">',
        body,
        "</main></div>",
        feed,
        (quote_band() if show_quote else ""),
        question,
        footer_html(),
        "</div>",
        (fabs() if show_fabs else ""),
        # (Sticky floating reviews badge removed — the live review widget now sits in the hero.)
        # Social-feed Alpine component (registers before Alpine inits) — fetches /api/social, falls back to embedded posts.
        f'<script defer src="/js/social-feed.js?v={ASSET_VER}"></script>',
        # Alpine.js powers the menu, dropdowns, FAQ accordions and mobile toggle.
        f'<script defer src="/js/alpine.min.js?v={ASSET_VER}"></script>',
        # Photo-strip carousel (arrows + centre-emphasis); no-ops on pages without [data-carousel].
        f'<script defer src="/js/photo-carousel.js?v={ASSET_VER}"></script>',
        "</body></html>",
    ]
    return "\n".join(doc)

def write(path_rel, html_doc):
    out = os.path.join(S.ROOT, path_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return out
