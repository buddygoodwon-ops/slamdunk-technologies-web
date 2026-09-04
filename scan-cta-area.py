# -*- coding: utf-8 -*-
import glob, re
for f in sorted(glob.glob('*.html')):
    if f in ('page-template.html','second-home-template.html','indexdiagonalfix.html','indexv2.html','indexv3.html'):
        continue
    t = open(f, encoding='utf-8').read()
    m = re.search(r'<div class="cta-row">.*?</div>\s*</div>\s*(?:<div class="hero-photo-frame">|</section>|<section)', t, re.S)
    if not m:
        # try looser: from cta-row to closing of hero-copy
        i = t.find('<div class="cta-row">')
        if i != -1:
            m = re.search(r'<div class="cta-row">.*?</div>\s*</div>', t[i:i+1500], re.S)
    print('---', f)
    print(re.sub(r'\s+', ' ', m.group(0))[:500] if m else 'NO cta-row')