# -*- coding: utf-8 -*-
"""Idempotently add Organization + Offer JSON-LD structured data to every site page.

Fixes the "See Like AI Sees" warning: "No JSON-LD found - add Organization/Offer schema."
Safe to re-run: a page that already has application/ld+json is skipped.
Also writes structured-data.json (the machine-readable copy served by the MCP server).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://slamdunktechnologies.com/#organization",
    "name": "SlamDunk Technologies",
    "alternateName": "SlamDunk",
    "url": "https://slamdunktechnologies.com",
    "logo": "https://slamdunktechnologies.com/assets/dogicon.jpg",
    "description": (
        "SlamDunk Technologies deploys intelligent BuddyFetch.AI agents for small and medium "
        "businesses - an agentic AI operating layer that mines prospects, runs workflows, "
        "handles marketing, and adapts to scale, all managed by phone, text, and email."
    ),
    "slogan": "The Agentic AI Team Working! for You.",
    "parentOrganization": {
        "@type": "Organization",
        "name": "BuddyFetch.AI",
        "url": "https://www.buddyfetch.ai",
    },
    "founder": {"@type": "Person", "name": "Glenn Wilbor", "jobTitle": "Founder & CEO"},
    "foundingLocation": "San Diego, CA",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "5234 Cushman Place #300",
        "addressLocality": "San Diego",
        "addressRegion": "CA",
        "postalCode": "92110",
        "addressCountry": "US",
    },
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "name": "Buddy Goodwon",
            "telephone": "+1-619-642-2585",
            "email": "buddy@buddyfetch.ai",
            "areaServed": "US",
            "availableLanguage": "English",
        }
    ],
    "sameAs": ["https://www.buddyfetch.ai/slamdunk"],
}

OFFER = {
    "@context": "https://schema.org",
    "@type": "Offer",
    "name": "MCP Server Conversion of Website",
    "description": (
        "Convert your existing website with an MCP server so AI agents can interact with it "
        "directly - book an appointment, get a quote, or even make a purchase."
    ),
    "url": "https://slamdunktechnologies.com/mcp-server.html",
    "availability": "https://schema.org/InStock",
    "category": "AI SEO / MCP Server Conversion",
    "seller": {"@id": "https://slamdunktechnologies.com/#organization"},
    "itemOffered": {
        "@type": "Service",
        "name": "MCP Server Conversion of Website",
        "serviceType": "Agentic AI & MCP Server Conversion",
        "provider": {"@id": "https://slamdunktechnologies.com/#organization"},
    },
    "potentialAction": {
        "@type": "ReserveAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://calendly.com/glenn-wilbor-birdrockfunding/30min",
        },
        "result": {"@type": "Reservation", "name": "30-minute demo with Glenn Wilbor"},
    },
}

MARKER = "application/ld+json"


def json_ld_block(obj, nl):
    body = json.dumps(obj, indent=2, ensure_ascii=True)
    body = nl.join("  " + line for line in body.split("\n"))
    return (
        '<script type="application/ld+json">' + nl
        + body + nl
        + "</script>"
    )


def inject(path):
    raw = path.read_text(encoding="utf-8")
    if MARKER in raw:
        return "skip (already has JSON-LD)"
    nl = "\r\n" if "\r\n" in raw else "\n"
    snippet = json_ld_block(ORG, nl) + nl + json_ld_block(OFFER, nl)

    m = re.search(r"</title>", raw, flags=re.I)
    if m:
        out = raw[: m.end()] + nl + snippet + raw[m.end():]
    elif re.search(r"<head[^>]*>", raw, flags=re.I):
        m2 = re.search(r"<head[^>]*>", raw, flags=re.I)
        out = raw[: m2.end()] + nl + snippet + raw[m2.end():]
    else:
        out = snippet + nl + raw
    path.write_text(out, encoding="utf-8", newline="")
    return "injected"


def main():
    changed = 0
    for p in sorted(ROOT.glob("*.html")):
        status = inject(p)
        print(f"{p.name:<28} {status}")
        if status == "injected":
            changed += 1
    # machine-readable copy for the MCP server / crawlers
    (ROOT / "structured-data.json").write_text(
        json.dumps([ORG, OFFER], indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(f"\n{changed} page(s) updated; wrote structured-data.json")


if __name__ == "__main__":
    main()
