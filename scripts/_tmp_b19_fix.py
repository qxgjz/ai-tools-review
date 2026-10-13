# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-gemini_38_flash_review_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "It competes on the fast, low-cost tier rather than on long-form writing or assistant polish. The [Claude vs Gemini 2026](/blog/claude-vs-gemini-2026-comparison/) and [ChatGPT vs Claude 2026](/blog/chatgpt-vs-claude-2026-comparison/) comparisons cover those dimensions."
new = "It competes on the fast, low-cost tier rather than on long-form writing or assistant polish. Our separate head-to-head reviews rate those assistant-tier dimensions in depth."
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
