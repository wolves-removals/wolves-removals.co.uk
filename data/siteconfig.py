# -*- coding: utf-8 -*-
"""Site-wide configuration for Wolves Removals static build.
Single source of truth for contact details, navigation, footer, services and locations.
Read by tools/engine.py and the render scripts.
"""
import os, re

SITE_URL = "https://wolves-removals.co.uk"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUSINESS = {
    "name": "Wolves Removals",
    "legal_name": "Wolves Removals Limited",
    "tagline": "Professional Home & Office Removals in Sussex",
    "phone": "01903 893731",
    "phone_link": "tel:+441903893731",
    "mobile": "07789 390421",
    "mobile_link": "tel:+447789390421",
    "whatsapp": "07789 390421",
    "whatsapp_link": "https://wa.me/447789390421",
    "email": "contact@wolves-removals.co.uk",
    "street": "Doryln House, London Road, Ashington",
    "locality": "Pulborough",
    "region": "West Sussex",
    "postcode": "RH20 3JT",
    "area_served": ["West Sussex", "East Sussex", "Surrey", "Hampshire", "Kent"],
    "geo": {"lat": "50.9462", "lng": "-0.3870"},  # Ashington, West Sussex (approx)
    "founded": "2016",  # "Keeping promises since 2016" — real founding year (live site)
    "hours": "Mo-Fr 08:00-18:00, Sa 09:00-13:00",
}

SOCIAL = {
    "facebook": "https://www.facebook.com/wolvesremovals/",
    "twitter": "https://twitter.com/WolvesRemovals",
    "instagram": "https://www.instagram.com/wolvesremovals/",
}

# Real, verifiable trust signals only — never invent (E-E-A-T + GDPR).
ACCREDITATIONS = ["LAPADA member", "Checkatrade verified", "Fully insured"]
TRUSTED_BY = ["Fine & Country", "Justin Lloyd", "Mansell McTaggart"]

# ---- Services (slug, label) — order/labels mirror the live mega-menu ----
SERVICES = [
    ("services/house-removals/", "House Removals"),
    ("services/commercial-removals/", "Commercial Removals"),
    ("services/european-removals/", "European Removals"),
    ("services/international-removals/", "International Removals"),
    ("services/student-removals/", "Student Removals"),
    ("services/man-and-van/", "Man and Van"),
    ("services/specialised-antiques-moving/", "Specialist Antique Moving"),
    ("services/antiques-in-west-sussex/", "Antiques in West Sussex"),
    ("services/white-glove-service/", "White Glove Service"),
    ("services/piano-moving/", "Piano Moving"),
    ("services/custom-crate-service/", "Custom Crate Service"),
    ("services/contract-delivery-services/", "Contract Delivery Services"),
    ("services/house-clearance/", "House Clearance"),
    ("services/removal-services/", "Removal Services"),
    ("services/full-packing-service/", "Full Packing Service"),
    ("services/full-unpacking-service/", "Full Unpacking Service"),
    ("services/fragile-packing/", "Fragile Packing"),
    ("services/non-fragile-packing-service/", "Non-Fragile Packing Service"),
    ("services/export-packing-service/", "Export Packing Service"),
    ("services/packing-materials/", "Packing Materials (Box Shop)"),
]
STORAGE = [
    ("services/storage/", "Storage"),
    ("services/storage/long-term-storage/", "Long-Term Storage"),
    ("services/storage/short-term-storage/", "Short-Term Storage"),
    ("services/storage/business-and-commercial-storage/", "Business & Commercial Storage"),
    ("services/student-storage/", "Student Storage"),
    ("storage-calculator/", "Storage Calculator"),
]
COUNTY_HUBS = [
    ("locations/sussex-removals/", "Sussex"),
    ("locations/west-sussex-removals/", "West Sussex"),
    ("locations/east-sussex-removals/", "East Sussex"),
    ("locations/surrey-removals/", "Surrey"),
    ("locations/hampshire-removals/", "Hampshire"),
]

def _name_from_loc_slug(slug):
    s = slug.strip("/").split("/")[-1]
    s = s.replace("removals-", "").replace("-removals", "")
    return s.replace("-", " ").title()

def load_locations():
    """All /locations/ URLs from the canonical map → [(path, name)]."""
    out = []
    f = os.path.join(ROOT, "data", "urls-pages.txt")
    if os.path.exists(f):
        for line in open(f, encoding="utf-8"):
            u = line.strip()
            m = re.search(r"/locations/([^/]+)/?$", u)
            if m and u.rstrip("/") != SITE_URL + "/locations":
                path = "locations/" + m.group(1) + "/"
                out.append((path, _name_from_loc_slug(path)))
    # de-dup, keep order
    seen, uniq = set(), []
    for p, n in out:
        if p not in seen:
            seen.add(p); uniq.append((p, n))
    return uniq

# ---- Footer columns (label, [(text, href)]) — content from live footer ----
def footer_columns():
    return [
        ("Our Services", [
            ("House Removals", "/services/house-removals/"),
            ("Commercial Removals", "/services/commercial-removals/"),
            ("International Removals", "/services/international-removals/"),
            ("Student Removals", "/services/student-removals/"),
            ("Specialist Antique Moving", "/services/specialised-antiques-moving/"),
            ("Man and Van", "/services/man-and-van/"),
            ("Contract Delivery Service", "/services/contract-delivery-services/"),
            ("White Glove Service", "/services/white-glove-service/"),
        ]),
        ("Packing & Storage", [
            ("Full Packing Service", "/services/full-packing-service/"),
            ("Fragile Packing", "/services/fragile-packing/"),
            ("Export Packing Service", "/services/export-packing-service/"),
            ("Storage", "/services/storage/"),
            ("Long-Term Storage", "/services/storage/long-term-storage/"),
            ("Short-Term Storage", "/services/storage/short-term-storage/"),
            ("Business & Commercial Storage", "/services/storage/business-and-commercial-storage/"),
        ]),
        ("Useful Links", [
            ("Packing Materials", "/services/packing-materials/"),
            ("Pricing", "/pricing/"),
            ("Blog", "/blog/"),
            ("FAQs", "/frequently-asked-questions/"),
            ("Gallery", "/gallery/"),
            ("Reviews", "/reviews/"),
            ("About Us", "/about-us/"),
        ]),
        ("Areas We Cover", [
            ("Sussex", "/locations/sussex-removals/"),
            ("West Sussex", "/locations/west-sussex-removals/"),
            ("East Sussex", "/locations/east-sussex-removals/"),
            ("Hampshire", "/locations/hampshire-removals/"),
            ("Surrey", "/locations/surrey-removals/"),
        ]),
    ]
