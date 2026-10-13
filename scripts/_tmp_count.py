# -*- coding: utf-8 -*-
import re, io, json, os, sys
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts')
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
f = os.path.join(base, 'content_drafts', '2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md')
s = io.open(f, encoding='utf-8').read()
words = len(re.findall(r"[A-Za-z0-9']+", s))
print('file exists, chars:', len(s), '| words:', words)
