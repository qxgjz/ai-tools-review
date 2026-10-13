# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-midjourney-v7-review-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
pairs = [
    ("the difference between tiers is GPU fast time plus concurrency, not image quality — the same model renders on every plan.",
     "the tiers differ in GPU fast time and concurrency while rendering the same image quality on every plan."),
    ("an upgrade buys throughput, not better output.",
     "an upgrade buys throughput alone, with the output quality staying identical."),
    ("the tool is not cheap, but it is drastically cheaper than the manual workflow it replaces.",
     "the tool carries a real price tag, yet it is drastically cheaper than the manual workflow it replaces."),
    ("The cheapest way to try it is Basic at $10/month; there is no meaningful free plan.",
     "The cheapest way to try it is Basic at $10/month, and the free allowance is negligible."),
]
for old, new in pairs:
    assert old in s, old[:60]
    s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
import re
print('patched, words:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
