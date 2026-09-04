# -*- coding: utf-8 -*-
"""Restore homepage-only styles into pages.css (they lived in index.html's old
inline <style> block that was removed this morning). Bump cache to v9."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
px = os.path.join(HERE, 'pages.css')
css = open(px, encoding='utf-8').read()

BLOCK = '''
/* --- Homepage-specific classes (index.html) --- */
.headline { margin: 0; font-size: clamp(39.4px, 3.66vw, 53.4px); font-weight: 700; line-height: 1.15; letter-spacing: -.02em; text-wrap: balance; }
.headline .grad, .lede .hl { background: var(--gradient); -webkit-background-clip: text; background-clip: text; color: transparent; }
.lede { max-width: 44ch; margin: 0; color: var(--ink); font-size: 16px; line-height: 1.6; }
.lede .hl { color: #b9a6ff; font-weight: 600; }
.brand-mark img { width: 100%; height: 100%; object-fit: cover; border-radius: 15.3px; display: block; }
'''

if '.headline' not in css:
    marker = '/* Side bullet list'
    css = css.replace(marker, BLOCK + marker, 1)
    open(px, 'w', encoding='utf-8', newline='').write(css)
    print('pages.css: homepage styles added')
else:
    print('pages.css: homepage styles already present')

# bump css version on all deployed pages v8 -> v9
PAGES = ['index','agents','avatar-app','company-brain','distribution','future','marketing','mcp-server','smart','virtual-mascot','workflows']
for fn in PAGES:
    p = os.path.join(HERE, fn + '.html')
    t = open(p, encoding='utf-8').read()
    n = t.replace('pages.css?v=8', 'pages.css?v=9')
    if n != t:
        open(p, 'w', encoding='utf-8', newline='').write(n)
print('pages.css bumped to v9 everywhere')

assert '.headline' in open(px, encoding='utf-8').read()
print('OK')