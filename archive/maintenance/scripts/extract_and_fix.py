#!/usr/bin/env python3
import base64
import re
from PIL import Image, ImageDraw
from io import BytesIO
import os

# Ler HTML
with open('17989742_v3 - Copia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Encontrar positions dos slides
slide4_idx = html.find('<!-- SLIDE 4')
slide5_idx = html.find('<!-- SLIDE 5')
slide6_idx = html.find('<!-- SLIDE 6')

# Extrair ranges de slides
slide4_content = html[slide4_idx:slide5_idx]
slide5_content = html[slide5_idx:slide6_idx]

# Regex para encontrar base64 data
pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'

# Extrair imagens
def extract_images_from_content(content, slide_name):
    matches = re.finditer(pattern, content)
    images = []
    for match in matches:
        b64_data = match.group(1)
        images.append(b64_data)
    print(f"{slide_name}: {len(images)} imagem(ns) encontrada(s)")
    return images

slide4_images = extract_images_from_content(slide4_content, "Slide 4")
slide5_images = extract_images_from_content(slide5_content, "Slide 5")

# Processar imagens para remover watermark
def remove_watermark_and_save(b64_data, filename):
    try:
        # Decodificar imagem
        img_data = base64.b64decode(b64_data)
        img = Image.open(BytesIO(img_data))
        
        print(f"\n  - Imagem carregada: {img.size} ({img.format})")
        
        # Remover área do watermark (geralmente no canto inferior direito)
        # "powered by perplexity" geralmente fica em um retângulo pequeno
        width, height = img.size
        
        # Estratégia: encontrar e remover texto da região inferior direita
        # Vamos usar ImageDraw para pintar branco sobre o watermark
        draw = ImageDraw.Draw(img)
        
        # Remover ~10% da parte inferior direita onde fica o watermark
        removal_height = int(height * 0.15)
        removal_width = int(width * 0.3)
        
        # Coordenadas: remover a área inferior direita
        x1 = width - removal_width
        y1 = height - removal_height
        x2 = width
        y2 = height
        
        # Preencher com branco (ou cor similar ao fundo)
        bg_color = img.getpixel((width-5, height-5))  # Pegar cor do canto
        draw.rectangle([x1, y1, x2, y2], fill=bg_color)
        
        print(f"  - Watermark removido da área: ({x1}, {y1}) até ({x2}, {y2})")
        
        # Converter de volta para base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        new_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Salvar original também para comparação
        with open(f"{filename}_original.png", 'wb') as f:
            f.write(img_data)
        
        # Salvar versão sem watermark
        buffered.seek(0)
        with open(f"{filename}_fixed.png", 'wb') as f:
            img.save(f, format="PNG")
        
        print(f"  ✓ Salvo: {filename}_fixed.png")
        
        return new_b64
        
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return None

# Processar slide 4
print("\nProcessando Slide 4...")
new_slide4_b64 = None
if slide4_images:
    new_slide4_b64 = remove_watermark_and_save(slide4_images[0], "slide4_img0")

# Processar slide 5
print("\nProcessando Slide 5...")
new_slide5_b64 = None
if slide5_images:
    new_slide5_b64 = remove_watermark_and_save(slide5_images[0], "slide5_img0")

# Substituir no HTML
if new_slide4_b64 and slide4_images:
    print("\nSubstituindo imagem do Slide 4 no HTML...")
    old_tag = f"data:image/png;base64,{slide4_images[0]}"
    new_tag = f"data:image/png;base64,{new_slide4_b64}"
    html = html.replace(old_tag, new_tag)
    print("✓ Substituição feita")

if new_slide5_b64 and slide5_images:
    print("\nSubstituindo imagem do Slide 5 no HTML...")
    old_tag = f"data:image/png;base64,{slide5_images[0]}"
    new_tag = f"data:image/png;base64,{new_slide5_b64}"
    html = html.replace(old_tag, new_tag)
    print("✓ Substituição feita")

# Salvar HTML atualizado
output_file = '17989742_v3 - Copia_FIXED.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✓ HTML salvo em: {output_file}")
