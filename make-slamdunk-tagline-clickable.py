# -*- coding: utf-8 -*-
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index','agents','avatar-app','company-brain','distribution','future','marketing','mcp-server','smart','virtual-mascot','workflows']

PAT = re.compile(r'<strong[^>]*>\s*That(?:&#39;|\\\x27|\x27)s a SlamDunk!\s*</strong>', re.S)
NEW = '<a class="slamdunk-link" href="index.html" aria-label="Back to the home page">That\'s a SlamDunk!</a>'

# --- 1) HTML: swap the tagline for a big home link --------------------------
for fn in PAGES:
    p = os.path.join(HERE, fn + '.html')
    t = open(p, encoding='utf-8').read()
    if 'slamdunk-link' in t:
        print(fn + '.html: already done')
        continue
    n = PAT.sub(lambda m: NEW, t, count=1)
    if n == t:
        raise SystemExit(fn + '.html: tagline not found!')
    open(p, 'w', encoding='utf-8', newline='').write(n)
    print(fn + '.html: tagline is now a big home link')

# --- 2) CSS: big font + pointer ---------------------------------------------
cssp = os.path.join(HERE, 'pages.css')
css = open(cssp, encoding='utf-8').read()
if '.slamdunk-link' not in css:
    css = css.replace(
        '.cta-text strong { font-size: 14px; font-weight: 600; }',
        '''.cta-text strong { font-size: 14px; font-weight: 600; }
.slamdunk-link { display: inline-block; margin-top: 4px; font-size: clamp(20px, 3vw, 28px); font-weight: 800; line-height: 1.25; letter-spacing: -.01em; background: var(--gradient); -webkit-background-clip: text; background-clip: text; color: transparent; transition: opacity .15s, transform .15s; }
.slamdunk-link:hover { opacity: .88; transform: translateY(-1px); }''', 1)
    open(cssp, 'w', encoding='utf-8', newline='').write(css)
    print('pages.css: big slamdunk-link styles added')
else:
    print('pages.css: slamdunk-link styles already present')

# --- 3) bump cache-buster to v8 --------------------------------------------
for fn in PAGES:
    p = os.path.join(HERE, fn + '.html')
    t = open(p, encoding='utf-8').read()
    n = t.replace('pages.css?v=7', 'pages.css?v=8')
    if n != t:
        open(p, 'w', encoding='utf-8', newline='').write(n)
print('pages.css bumped to v8 everywhere')

# verify
for fn in PAGES:
    t = open(os.path.join(HERE, fn + '.html'), encoding='utf-8').read()
    assert 'class="slamdunk-link" href="index.html"' in t, fn
    assert 'pages.css?v=8' in t, fn
css = open(cssp, encoding='utf-8').read()
assert '.slamdunk-link' in css
print('ALL CHECKS PASSED')