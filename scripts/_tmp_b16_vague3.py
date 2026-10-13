# -*- coding: utf-8 -*-
import io, os, re
import zens_ink.content_qc as cq
src = io.open(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-elevenlabs-v2-review-2026_REWRITE.md', encoding='utf-8').read()
V = cq.VAGUE_WORDS
low = src.lower()
for w in sorted(V, key=lambda x: -len(x)):
    n = low.count(w)
    if n:
        # show context
        for m in re.finditer(re.escape(w), low):
            s0 = max(0, m.start()-60); s1 = min(len(src), m.end()+60)
            print(w, 'x', n, '::', src[s0:s1].replace('\n',' '))
        print()
