# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-midjourney-v7-review-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sents = re.split(r'(?<=[.!?])\s+', s)
for i, x in enumerate(sents):
    if re.search(r'\b(not|never|no|without|isn\'t|aren\'t|doesn\'t|don\'t|won\'t|can\'t|cannot)\b', x, re.I):
        print(i, '|', x.strip()[:160])
