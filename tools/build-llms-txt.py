#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate /llms.txt — a structured map of the site for LLMs/AI search."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
import siteconfig as S
import services_data as SD
import locations as L

SITE = S.SITE_URL

def main():
    lines = []
    lines.append("# Wolves Removals")
    lines.append("")
    lines.append("> Family-run Sussex removals company based near Pulborough, West Sussex (since 2016). "
                 "Home, commercial, antiques and international removals, packing and secure storage across "
                 "Sussex, Surrey, Hampshire and Kent. LAPADA member, Checkatrade-verified, fully insured. "
                 f"Tel {S.BUSINESS['phone']} / {S.BUSINESS['email']}.")
    lines.append("")
    lines.append("## Key pages")
    for label, path in [("Home", "/"), ("About Us", "/about-us/"), ("Services", "/services/"),
                        ("Pricing", "/pricing/"), ("Areas We Cover", "/locations/"),
                        ("Storage Calculator", "/storage-calculator/"), ("FAQs", "/frequently-asked-questions/"),
                        ("Helpful Tips", "/helpful-tips/"), ("Reviews", "/reviews/"),
                        ("Get a Quote", "/get-a-quote/"), ("Contact", "/contact-us/")]:
        lines.append(f"- [{label}]({SITE}{path})")
    lines.append("")
    lines.append("## Services")
    for s in SD.SERVICES:
        lines.append(f"- [{s['name']}]({SITE}/services/{s['slug']}/): {s.get('teaser','').rstrip('.')}.")
    lines.append("")
    lines.append("## Areas we cover")
    for slug, name, counties in L.HUBS:
        lines.append(f"- [{name}]({SITE}/locations/{slug}/)")
    for slug, town, county in L.TOWNS:
        lines.append(f"- [{town} removals]({SITE}/locations/{slug}/)")
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"llms.txt: {len(lines)} lines")

if __name__ == "__main__":
    main()
