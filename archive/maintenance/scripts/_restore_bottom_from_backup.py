import base64, re
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw

base = Path(r"c:\Users\user\Downloads\ep3")
current_html_path = base / "17989742_v3 - Copia.html"
backup_html_path = base / "17989742_v3 - Copia_BACKUP.html"

current_html = current_html_path.read_text(encoding="utf-8")
backup_html = backup_html_path.read_text(encoding="utf-8")

rects = {
    4: (1185, 55, 1520, 160),
    5: (860, 70, 1160, 160),
}

pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'

for slide, rect in rects.items():
    cur_start = current_html.find(f'<!-- SLIDE {slide}')
    cur_end = current_html.find(f'<!-- SLIDE {slide+1}') if slide < 9 else len(current_html)
    cur_block = current_html[cur_start:cur_end]
    cur_match = re.search(pattern, cur_block)
    if not cur_match:
        raise SystemExit(f'current slide {slide}: image not found')
    current_b64 = cur_match.group(1)

    bak_start = backup_html.find(f'<!-- SLIDE {slide}')
    bak_end = backup_html.find(f'<!-- SLIDE {slide+1}') if slide < 9 else len(backup_html)
    bak_block = backup_html[bak_start:bak_end]
    bak_match = re.search(pattern, bak_block)
    if not bak_match:
        raise SystemExit(f'backup slide {slide}: image not found')
    backup_b64 = bak_match.group(1)

    img = Image.open(BytesIO(base64.b64decode(backup_b64))).convert('RGBA')
    ImageDraw.Draw(img).rectangle(rect, fill=(255,255,255,255))

    out = BytesIO()
    img.save(out, format='PNG', optimize=True)
    new_b64 = base64.b64encode(out.getvalue()).decode('ascii')

    current_html = current_html.replace(current_b64, new_b64, 1)
    img.save(base / f'slide{slide}_current.png')
    print(f'slide {slide}: rebuilt from backup and cleaned rect={rect}')

current_html_path.write_text(current_html, encoding='utf-8')
print('html updated from backup-based rebuild')
