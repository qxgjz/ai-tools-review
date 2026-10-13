# -*- coding: utf-8 -*-
import os
from PIL import Image
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
src_dir = base + r'\content_drafts\screenshots\batch17'
dst_dir = base + r'\public\screenshots\real\webp'
for name in ['midjourney-plans', 'midjourney-home', 'suno-pricing']:
    src = os.path.join(src_dir, name + '.png')
    im = Image.open(src).convert('RGB')
    dst = os.path.join(dst_dir, name + '.webp')
    im.save(dst, 'WEBP', quality=80, method=6)
    print(name + '.webp', os.path.getsize(dst), 'bytes')
