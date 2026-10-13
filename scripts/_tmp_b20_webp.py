# -*- coding: utf-8 -*-
import os
from PIL import Image
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
src = base + r'\content_drafts\screenshots\batch20\dify-pricing.png'
dst = base + r'\public\screenshots\real\webp\dify-pricing.webp'
im = Image.open(src).convert('RGB')
im.save(dst, 'WEBP', quality=80, method=6)
print('dify-pricing.webp', os.path.getsize(dst), 'bytes')
