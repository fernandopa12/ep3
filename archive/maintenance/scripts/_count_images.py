from pathlib import Path
import re
html = Path(r"c:\Users\user\Downloads\ep3\17989742_v3 - Copia.html").read_text(encoding="utf-8")
for i, m in enumerate(re.finditer(r'<img src="data:image/png;base64,([A-Za-z0-9+/=]+)"', html), 1):
    pos = m.start()
    snippet = html[max(0, pos-180):pos]
    slide = 'unknown'
    for n in range(1, 10):
        marker = f'data-slide="{n}"'
        idx = html.rfind(marker, 0, pos)
        if idx != -1:
            slide = str(n)
    print(f'image {i}: slide {slide}, pos {pos}, b64len {len(m.group(1))}')
