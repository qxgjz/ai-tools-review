# -*- coding: utf-8 -*-
import os
from PIL import Image
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
src = os.path.join(base, 'content_drafts', 'screenshots', 'batch16', 'gemini-pricing.png')
dst = os.path.join(base, 'public', 'screenshots', 'real', 'webp', 'gemini-pricing.webp')
img = Image.open(src).convert('RGB')
img.save(dst, 'WEBP', quality=82)
print('saved', dst, os.path.getsize(dst), 'bytes')
