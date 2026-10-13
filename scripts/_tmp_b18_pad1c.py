# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-lovable-vs-boltnew_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
One warning before you build: every prompt-to-app tool hallucinates features. Lovable will occasionally produce a settings screen that looks complete and silently omits the save action; Bolt will sometimes wire a button to a handler that exists nowhere in the code. The fix is the same discipline that applies to all AI output — verify the critical path manually. Log in, create a record, edit it, delete it, and refresh — if the generated app survives that loop, it is ready to show; if it fails, regenerate that screen rather than shipping the gap.

"""
old = "## The Bottom Line in Two Sentences"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
