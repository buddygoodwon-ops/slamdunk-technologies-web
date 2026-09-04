# -*- coding: utf-8 -*-
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --- 1) workflows.html: give the h2 a dedicated class (idempotent) ----------
p = os.path.join(HERE, 'workflows.html')
t = open(p, encoding='utf-8').read()
if 'flow-heading' not in t:
    old = '<h2 class="page-heading ">Your apps. Our new apps.<br><span class="grad">One epic flow.</span></h2>'
    new = '<h2 class="page-heading flow-heading">Your apps. Our new apps.<br><span class="grad">One epic flow.</span></h2>'
    assert old in t, 'workflows heading not found'
    t = t.replace(old, new, 1)
    open(p, 'w', encoding='utf-8', newline='').write(t)
    print('workflows.html: h2 now has flow-heading class')
else:
    print('workflows.html: flow-heading class already present')

# --- 2) pages.css: lock two lines ---
p = os.path.join(HERE, 'pages.css')
css = open(p, encoding='utf-8').read()
if '.flow-heading' not in css:
    css = css.replace(
        '.cta-button { display: inline-flex;',
        '''.page-heading.flow-heading { white-space: nowrap; letter-spacing: -.025em; }
@media (max-width: 980px) {
  .page-heading.flow-heading { font-size: clamp(27px, 6vw, 42px); white-space: nowrap; }
}
@media (max-width: 560px) {
  .page-heading.flow-heading { font-size: clamp(23px, 6vw, 30px); white-space: nowrap; }
}
.cta-button { display: inline-flex;''',
        1)
    open(p, 'w', encoding='utf-8', newline='').write(css)
    print('pages.css: flow-heading two-line styles added')
else:
    print('pages.css: flow-heading styles already present')

# --- 3) index.html: add missing pages.css link ---
idx = os.path.join(HERE, 'index.html')
t = open(idx, encoding='utf-8').read()
if 'pages.css' not in t:
    t = t.replace('<link rel="stylesheet" href="floating-bar.css?v=4">',
                  '<link rel="stylesheet" href="pages.css?v=7">\n  <link rel="stylesheet" href="floating-bar.css?v=4">', 1)
    open(idx, 'w', encoding='utf-8', newline='').write(t)
    print('index.html: pages.css?v=7 link added')
else:
    print('index.html: pages.css already linked')

# --- 4) bump every deployed page + index to v7 ---
pages = ['index', 'agents', 'avatar-app', 'company-brain', 'distribution', 'future', 'marketing', 'mcp-server', 'smart', 'virtual-mascot', 'workflows']
for fn in pages:
    p = os.path.join(HERE, fn + '.html')
    s = open(p, encoding='utf-8').read()
    n = s.replace('pages.css?v=6', 'pages.css?v=7')
    if n != s:
        open(p, 'w', encoding='utf-8', newline='').write(n)
print('pages.css bumped to v7 on all deployed pages')

# --- verify ---
checks = {
    'workflows.html': 'flow-heading' in open(os.path.join(HERE, 'workflows.html'), encoding='utf-8').read(),
    'pages.css': '.flow-heading' in open(os.path.join(HERE, 'pages.css'), encoding='utf-8').read(),
    'index.html': 'pages.css?v=7' in open(os.path.join(HERE, 'index.html'), encoding='utf-8').read(),
}
for k, v in checks.items():
    print(k, 'OK' if v else 'FAIL')
if not all(checks.values()):
    raise SystemExit('verification failed')
print('ALL CHECKS PASSED')