# -*- coding: utf-8 -*-
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(HERE, "index.html")

txt = open(index_path, encoding="utf-8").read()

# 1. Remove the entire <style> block.
style_block_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
txt = style_block_pattern.sub('', txt)

# 2. Update the brand text section to ensure correct h1 and span classes
# Find the current brand-text block
brand_text_match = re.search(r'(<div class="brand-text">.*?</div>)', txt, re.DOTALL)
if brand_text_match:
    old_brand_text_block = brand_text_match.group(1)
    
    # Construct the new h1 structure with correct classes
    new_h1 = '<h1 class="brand-title">SLAM<span class="accent">DUNK</span> <span class="suffix">TECHNOLOGIES</span></h1>'
    new_brand_text_block = re.sub(r'<h1>.*?</h1>', new_h1, old_brand_text_block, flags=re.DOTALL)
    
    # Replace brand-suffix with suffix in the new_brand_text_block if it somehow remained
    new_brand_text_block = new_brand_text_block.replace('class="brand-suffix"', 'class="suffix"')

    txt = txt.replace(old_brand_text_block, new_brand_text_block)
    print("Updated brand text H1 structure.")
else:
    print("WARNING: Could not find brand-text block in index.html")

# 3. Ensure the correct CSS versions are linked in the head (pages.css?v=9, floating-bar.css?v=4)
txt = re.sub(r'pages\.css\?v=\d+', 'pages.css?v=9', txt)
txt = re.sub(r'floating-bar\.css\?v=\d+', 'floating-bar.css?v=4', txt)

# 4. Ensure floating-bar.js version is v4
txt = re.sub(r'floating-bar\.js\?v=\d+', 'floating-bar.js?v=4', txt)


open(index_path, "w", encoding="utf-8", newline="").write(txt)
print("index.html updated for consistent brand title sizing.")

# Verify the changes locally
if re.search(r'<style>.*?</style>', txt, re.DOTALL):
    print("WARNING: <style> block still found after removal attempt.")
if '<h1>SLAM<span class="accent">DUNK</span> <span class="brand-suffix">TECHNOLOGIES</span></h1>' in txt:
    print("WARNING: Old h1 structure still found.")
if 'floating-bar.js?v=1' in txt:
    print("WARNING: floating-bar.js?v=1 still found.")
if 'pages.css?v=9' not in txt:
    print("WARNING: pages.css?v=9 not found.")
