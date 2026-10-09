# -*- coding: utf-8 -*-
"""batch12 截图转 webp 存入 public/screenshots/real/webp/"""
import os
from PIL import Image

SRC = 'content_drafts/screenshots/batch12'
DST = 'public/screenshots/real/webp'
os.makedirs(DST, exist_ok=True)

FILES = [
    'runway-pricing.png',
    'pika-pricing.png',
    'writesonic-pricing.png',
    'jasper-pricing.png',
    'otter-pricing.png',
    'granola-product.png',
    'fireflies-pricing.png',
]

for f in FILES:
    src = os.path.join(SRC, f)
    dst = os.path.join(DST, f.replace('.png', '.webp'))
    im = Image.open(src).convert('RGB')
    im.save(dst, 'WEBP', quality=82)
    print(f, '->', dst, im.size, os.path.getsize(dst) // 1024, 'KB')
