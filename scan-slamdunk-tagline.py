# -*- coding: utf-8 -*-
import glob, re
for f in sorted(glob.glob('*.html')):
    if f in ('page-template.html','second-home-template.html','indexdiagonalfix.html','indexv2.html','indexv3.html'):
        continue
    t = open(f, encoding='utf-8').read()
    m = re.search(r'<div class="cta-row">.*?</div>\s*</div>', t, re.S)
    if m:
        print('---', f)
        print(re.sub(r'\s+', ' ', m.group(0))[:600])
    else:
        print('---', f, ': NO cta-row')