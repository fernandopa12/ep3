import base64, re
from pathlib import Path
html = Path(r"c:\Users\user\Downloads\ep3\17989742_v3 - Copia.html").read_text(encoding="utf-8")
for slide in [4,5]:
    start = html.find(f'<!-- SLIDE {slide}')
    end = html.find(f'<!-- SLIDE {slide+1}') if slide < 9 else len(html)
    block = html[start:end]
    m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', block)
    if not m:
        print(f'slide{slide}: no image')
        continue
    data = base64.b64decode(m.group(1))
    out = Path(r"c:\Users\user\Downloads\ep3") / f"slide{slide}_current.png"
    out.write_bytes(data)
    print(f'{out} {len(data)}')
