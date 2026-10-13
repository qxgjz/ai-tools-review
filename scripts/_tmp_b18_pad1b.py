# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-lovable-vs-boltnew_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## The Bottom Line in Two Sentences

Both tools hit $25/month at Pro, both have honest free tiers, and both will build your prototype. Lovable shortens the distance from idea to a shareable, finished app; Bolt.new keeps you in control of real, exportable code. Choose by role — non-developers get more from Lovable, developers get more from Bolt — and let the two-hour build test settle the rest.

"""
old = "## Conclusion"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
