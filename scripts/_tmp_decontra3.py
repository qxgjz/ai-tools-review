# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
p1 = base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
s1 = io.open(p1, encoding='utf-8').read()
old = "## Which AI Tool Is Best for Beginners in 2026?"
new = "## Which AI Tool Is Best for Beginners in 2026 — and Which Is Not Worth It?"
assert old in s1
s1 = s1.replace(old, new, 1)
io.open(p1, 'w', encoding='utf-8').write(s1)
print('beginners patched round3')
