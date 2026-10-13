# -*- coding: utf-8 -*-
import io, os
from PIL import Image
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
src = base + r'\content_drafts\screenshots\batch21'
dst = base + r'\public\screenshots\real\webp'
for name in ['devin-home', 'devin-pricing', 'perplexity-pricing']:
    p = os.path.join(src, name + '.png')
    im = Image.open(p).convert('RGB')
    out = os.path.join(dst, name + '.webp')
    im.save(out, 'WEBP', quality=80, method=6)
    print(name, im.size, os.path.getsize(out))
