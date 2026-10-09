# -*- coding: utf-8 -*-
"""将 batch11 选用的 png 转 webp 存入 public/screenshots/real/webp/"""
import os
from PIL import Image

SRC = 'content_drafts/screenshots/batch11'
DST = 'public/screenshots/real/webp'
os.makedirs(DST, exist_ok=True)

MAPPING = {
    'synthesia-pricing.png': 'synthesia-pricing.webp',
    'heygen-templates.png': 'heygen-templates.webp',
    'heygen-pricing.png': 'heygen-pricing.webp',
    'motion-pricing.png': 'motion-pricing.webp',
    'reclaim-product.png': 'reclaim-product.webp',
    'paraphraser-io.png': 'paraphraser-io.webp',
    'undetectable-ai.png': 'undetectable-ai.webp',
}

for src, dst in MAPPING.items():
    sp = os.path.join(SRC, src)
    dp = os.path.join(DST, dst)
    if not os.path.exists(sp):
        print('MISSING', sp)
        continue
    img = Image.open(sp).convert('RGB')
    img.save(dp, 'WEBP', quality=82, method=6)
    sz = os.path.getsize(dp)
    print('OK', dst, f'{sz/1024:.1f}KB', img.size)
