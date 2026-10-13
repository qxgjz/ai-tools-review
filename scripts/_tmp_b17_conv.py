# -*- coding: utf-8 -*-
import io, os
from PIL import Image
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
webp_dir = base + r'\public\screenshots\real\webp'
out_dir = base + r'\scripts\_tmp_b17_verify'
os.makedirs(out_dir, exist_ok=True)
for w in ['cursor-pricing.webp','cursor-code-editor.webp','midjourney-pricing.webp','midjourney-gallery.webp','suno-music-creator.webp','suno.webp']:
    src = os.path.join(webp_dir, w)
    if not os.path.exists(src):
        print(w, 'MISSING'); continue
    im = Image.open(src)
    dst = os.path.join(out_dir, w.replace('.webp', '.png'))
    im.save(dst, 'PNG')
    print(w, '->', dst, im.size)
