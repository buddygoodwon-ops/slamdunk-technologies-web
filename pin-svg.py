from pathlib import Path
p = Path(__file__).parent / 'build-pages.py'
s = p.read_text(encoding='utf-8')
s = s.replace('<svg viewBox=', '<svg width="21.25" height="21.25" viewBox=')
p.write_text(s, encoding='utf-8')
print('svgs pinned:', s.count('width="21.25"'))