# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-sudowrite-alternatives_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## The Budget Rule for Fiction AI

The practical budget rule for fiction writers is the same one the r/SaaS founders apply to every AI subscription: measure the output before you pay. Draft a full chapter in each candidate's free tier — ChatGPT for outlines, Claude for prose, Sudowrite's no-credit-card trial for style control — and count the time from blank page to a readable draft. Writers who finish a chapter in one free session have their answer; writers who hit the free limits mid-chapter know exactly which paid tier the project needs. A novel drafted this way costs $18 to $22 a month for three to six months, which is cheaper than any writing software that preceded AI, and the draft belongs to you under every paid plan's commercial terms.

"""
old = "## Common Questions About Sudowrite Alternatives"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
