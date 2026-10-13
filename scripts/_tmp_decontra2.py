# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
p1 = base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
s1 = io.open(p1, encoding='utf-8').read()
r1 = [
 ("## What Is the Best AI Tool for Beginners in 2026?",
  "## Which AI Tool Is Best for Beginners in 2026?"),
 ("ChatGPT is easier to start with because the free tier is more generous.",
  "ChatGPT is easier to start with because its free tier is more generous — you do not need a credit card or any setup."),
]
for a, b in r1:
    assert a in s1, a[:60]
    s1 = s1.replace(a, b, 1)
io.open(p1, 'w', encoding='utf-8').write(s1)
print('beginners patched round2')
