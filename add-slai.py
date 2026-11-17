# -*- coding: utf-8 -*-
"""Ensure EVERY page loads the "See Like an AI MCP" toggle (see-like-ai.css + see-like-ai.js).

Idempotent and safe to re-run. Bumps the cache-busting ?v= to 2 so browsers/CDN
pick up the updated script. Works on pages with or without <head>/<body> tags.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
CSS_TAG = '<link rel="stylesheet" href="see-like-ai.css?v=3">'
JS_TAG = '<script src="see-like-ai.js?v=2"></script>'


def insert_before(raw, close_tag, tag, nl):
    m = re.search(close_tag, raw, flags=re.I)
    if m:
        return raw[: m.start()] + tag + nl + raw[m.start():]
    return None


def ensure(path):
    raw = path.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    before = raw

    # CSS
    if "see-like-ai.css" in raw:
        raw = re.sub(r"see-like-ai\.css\?v=\d+", "see-like-ai.css?v=3", raw)
    else:
        out = insert_before(raw, r"</head>", CSS_TAG, nl)
        if out is None:
            out = insert_before(raw, r"</title>", CSS_TAG, nl)  # no <head>: place after <title>
        raw = out if out is not None else (raw + nl + CSS_TAG)

    # JS
    if "see-like-ai.js" in raw:
        raw = re.sub(r"see-like-ai\.js\?v=\d+", "see-like-ai.js?v=2", raw)
    else:
        out = insert_before(raw, r"</body>", JS_TAG, nl)
        raw = out if out is not None else (raw + nl + JS_TAG)

    if raw != before:
        path.write_text(raw, encoding="utf-8", newline="")
        return "updated"
    return "ok"


changed = 0
for p in sorted(ROOT.glob("*.html")):
    st = ensure(p)
    print(f"{p.name:<28} {st}")
    if st == "updated":
        changed += 1
print(f"\n{changed} page(s) updated")
