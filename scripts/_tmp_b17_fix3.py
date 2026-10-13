# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-suno-alternatives_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "## Do You Even Need to Switch? The Case for Staying on Suno"
new = "## Do You Even Need to Switch From Suno?\n\nThe case for staying:"
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
