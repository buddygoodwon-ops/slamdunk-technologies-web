# -*- coding: utf-8 -*-
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(HERE, "index.html")

txt = open(index_path, encoding="utf-8").read()

# 1. Remove the entire <style> block.
# Assuming it starts after a stylesheet link and ends before </head>
# Need to be careful here to match the exact block
style_block_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
txt = style_block_pattern.sub('', txt)

# 2. Replace the <h1> tag with <h1 class="brand-title"> and change brand-suffix to suffix.
# Also ensure the class is "brand-title" and not just "h1"
txt = re.sub(r'<h1>SLAM<span class=\"accent\">DUNK</span> <span class=\"brand-suffix\">TECHNOLOGIES</span></h1>',
             r'<h1 class=\"brand-title\">SLAM<span class=\"accent\">DUNK</span> <span class=\"suffix\">TECHNOLOGIES</span></h1>',
             txt)

# 3. Ensure the correct CSS versions are linked in the head (pages.css?v=6, floating-bar.css?v=4)
txt = re.sub(r'pages\.css\\?v=\\d+', 'pages.css?v=6', txt)
txt = re.sub(r'floating-bar\.css\\?v=\\d+', 'floating-bar.css?v=4', txt)

# 4. Ensure floating-bar.js version is v4 (it seems to have been v1 before)
txt = txt.replace("floating-bar.js?v=1", "floating-bar.js?v=4")


open(index_path, "w", encoding="utf-8", newline="").write(txt)
print("index.html updated for consistent brand title sizing.")

# Verify the changes locally before committing
# Check for remaining style tags
if re.search(r'<style>.*?</style>', txt, re.DOTALL):
    print("WARNING: <style> block still found after removal attempt.")
if '<h1>SLAM<span class="accent">DUNK</span> <span class="brand-suffix">TECHNOLOGIES</span></h1>' in txt:
    print("WARNING: Old h1 structure still found.")
if 'floating-bar.js?v=1' in txt:
    print("WARNING: floating-bar.js?v=1 still found.")
