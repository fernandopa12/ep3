from pathlib import Path
from io import BytesIO
import base64, re
from PIL import Image

base = Path(r"c:\Users\user\Downloads\ep3")
source = base / "17989742_v3 - Copia.html"
html = source.read_text(encoding="utf-8")

assets_css = base / "assets" / "css"
assets_js = base / "assets" / "js"
assets_images = base / "assets" / "images"
archive_backups = base / "archive" / "backups"
archive_maintenance = base / "archive" / "maintenance"
archive_scripts = archive_maintenance / "scripts"
archive_images = archive_maintenance / "images"
for path in [assets_css, assets_js, assets_images, archive_backups, archive_scripts, archive_images]:
    path.mkdir(parents=True, exist_ok=True)

style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, flags=re.S)
script_match = re.search(r'<script>(.*?)</script>', html, flags=re.S)
if len(style_blocks) != 2 or not script_match:
    raise SystemExit('failed to locate style/script blocks')

styles_css = """\
:root {
  --color-bg:#faf8f4;
  --color-bg-deep:#f3f0ea;
  --color-surface:#ede9e1;
  --color-text:#1a1714;
  --color-text-secondary:#3d3a35;
  --color-text-muted:#7a7570;
  --color-accent-1:#1d3557;
  --color-accent-2:#457b9d;
  --color-accent-3:#e63946;
  --color-glass-bg:rgba(255,255,255,0.84);
  --color-glass-border:rgba(0,0,0,0.08);
  --font-display:'Cormorant Garamond', Georgia, serif;
  --font-body:'Source Sans 3', system-ui, sans-serif;
}

.font-display{font-family:var(--font-display)}
""" + style_blocks[1].strip() + "\n"
(assets_css / "styles.css").write_text(styles_css, encoding="utf-8")
(assets_js / "slides.js").write_text(script_match.group(1).strip() + "\n", encoding="utf-8")

img_matches = list(re.finditer(r'<img src="data:image/png;base64,([A-Za-z0-9+/=]+)"', html))
image_names = ["slide-4-chart.png", "slide-5-chart.png", "slide-6-chart.png"]
if len(img_matches) != len(image_names):
    raise SystemExit(f'expected {len(image_names)} embedded images, found {len(img_matches)}')

for match, name in zip(img_matches, image_names):
    b64 = match.group(1)
    image_bytes = base64.b64decode(b64)
    Image.open(BytesIO(image_bytes)).save(assets_images / name)
    html = html.replace(f'data:image/png;base64,{b64}', f'assets/images/{name}', 1)

html = re.sub(r'\s*<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>\s*', '\n', html, count=1)
html = re.sub(r'<style[^>]*>.*?</style>\s*<style>.*?</style>', '<link rel="stylesheet" href="assets/css/styles.css">', html, count=1, flags=re.S)
html = re.sub(r'<script>.*?</script>', '<script src="assets/js/slides.js"></script>', html, count=1, flags=re.S)
(base / "index.html").write_text(html, encoding="utf-8")

for name in ["17989742_v3 - Copia.html", "17989742_v3 - Copia_BACKUP.html", "17989742_v3 - Copia_FIXED.html"]:
    src = base / name
    if src.exists():
        dst = archive_backups / name
        if dst.exists():
            dst.unlink()
        src.replace(dst)

for src in list(base.glob("*.py")):
    dst = archive_scripts / src.name
    if dst.exists():
        dst.unlink()
    src.replace(dst)

for src in list(base.glob("slide*_*.png")):
    dst = archive_images / src.name
    if dst.exists():
        dst.unlink()
    src.replace(dst)

print('Project reorganized successfully')
