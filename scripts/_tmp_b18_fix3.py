# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
p = base + r'\content_drafts\2026-10-11-lovable-vs-boltnew_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "| Teams / Business | Business $50/month, team workspace | Teams $30/member/month, central billing |"
new = "| Teams / Business | Business $50/month, team workspace | Teams $30/member/month, central billing |\n\nThat covers the official plans as of October 2026."
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
