import base64, re
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw

base = Path(r"c:\Users\user\Downloads\ep3")
html_path = base / "17989742_v3 - Copia.html"
html = html_path.read_text(encoding="utf-8")

for slide in [4,5]:
    start = html.find(f'<!-- SLIDE {slide}')
    end = html.find(f'<!-- SLIDE {slide+1}') if slide < 9 else len(html)
    block = html[start:end]
    m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', block)
    if not m:
        raise SystemExit(f'slide {slide}: image not found')
    old_b64 = m.group(1)
    img = Image.open(BytesIO(base64.b64decode(old_b64))).convert('RGBA')
    draw = ImageDraw.Draw(img)
    w, h = img.size

    if slide == 4:
        rect = (1210, 75, 1518, 145)
    else:
        rect = (875, 85, 1158, 150)

    draw.rectangle(rect, fill=(255,255,255,255))

    out = BytesIO()
    img.save(out, format='PNG', optimize=True)
    new_b64 = base64.b64encode(out.getvalue()).decode('ascii')
    html = html.replace(old_b64, new_b64, 1)
    img.save(base / f'slide{slide}_current.png')
    print(f'slide {slide} fixed {img.size} rect={rect}')

html_path.write_text(html, encoding='utf-8')
print('html updated')
