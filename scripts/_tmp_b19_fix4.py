# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-gemini_38_flash_review_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old1 = "For speed and cost per token, yes; for deep reasoning and complex problem solving, no — Pro is the reasoning flagship. Teams route routine work to Flash and hard problems to Pro."
new1 = "Flash wins on speed and cost per token; Pro wins on deep reasoning and complex problem solving. Teams route routine work to Flash and hard problems to Pro."
assert old1 in s
s = s.replace(old1, new1, 1)
old2 = "| Code autocomplete and quick edits | Flash | Low latency, flat cost per token |"
new2 = "| Code autocomplete and quick edits | Flash | Low latency and predictable pricing |"
assert old2 in s
s = s.replace(old2, new2, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
