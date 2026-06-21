from pathlib import Path
import re
html = Path(r"c:\Users\user\Downloads\ep3\17989742_v3 - Copia.html").read_text(encoding="utf-8")
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, flags=re.S)
script = re.search(r'<script>(.*?)</script>', html, flags=re.S)
print('style blocks:', len(styles))
for i, s in enumerate(styles, 1):
    print(f'-- style {i} chars={len(s)}')
    print(s[:400].replace('\n','\\n'))
    print('...')
if script:
    print('-- script chars=', len(script.group(1)))
    print(script.group(1)[:1200].replace('\n','\\n'))
