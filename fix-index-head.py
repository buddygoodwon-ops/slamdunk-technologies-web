# -*- coding: utf-8 -*-
"""Fix index.html head for consistent brand title sizing."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))

HEAD_SNIPPET = '''<title>SlamDunk Technologies</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="pages.css?v=6">
  <link rel="stylesheet" href="floating-bar.css?v=4">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/appicon-180.png">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#000000">'''

index_path = os.path.join(HERE, "index.html")
txt = open(index_path, encoding="utf-8").read()

# 1. Replace the entire <head> section content
head_start_tag = txt.find("<head>")
head_end_tag = txt.find("</head>")

if head_start_tag != -1 and head_end_tag != -1:
    # Capture everything from <head> to </head> inclusive
    old_head_block = txt[head_start_tag : head_end_tag + len("</head>")]
    
    # Construct the new head block with correct spacing
    new_head_block = f"<head>\n  {HEAD_SNIPPET}\n  </head>"
    
    txt = txt.replace(old_head_block, new_head_block)
    print("Replaced head section.")
else:
    print("Error: Could not find <head> tags in index.html")

# 2. Ensure floating-bar.js version is v4 (was v1 in initial index.html, not fixed by first global script)
txt = txt.replace("floating-bar.js?v=1", "floating-bar.js?v=4")

open(index_path, "w", encoding="utf-8", newline="").write(txt)
print("index.html updated.")