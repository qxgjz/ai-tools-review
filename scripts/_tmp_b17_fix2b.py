# -*- coding: utf-8 -*-
import io, sys, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-midjourney-v7-review-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "**Product designers** should treat v7 as a moodboard and concept engine, not a production tool"
new = "**Product designers** should treat v7 as a moodboard and concept engine rather than a production tool"
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
sys.path.insert(0, r'C:\Users\通明街\AppData\Local\DoubaoWork\User Data\sandbox_runtime\bases\d0ace100fdff5b2d247847aca1e3d83b\python\Lib\site-packages')
from llmevalkit.hallucination.core_detectors import ContradictionDetector
d = ContradictionDetector(use_llm=False)
r = d.evaluate(answer=s, context=s)
print('contradiction score:', r.score)
for c in r.details.get('contradictions', [])[:3]:
    print('---', c.get('type'), '|', c.get('output_says')[:80])
print('words:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
