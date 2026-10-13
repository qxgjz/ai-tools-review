# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "ChatGPT's free tier handled all five tasks with unlimited text chats and only limited uploads — we never felt blocked."
new = "ChatGPT's free tier handled all five tasks on unlimited text chats, with uploads as the only limit."
assert old in s, 'still missing'
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", s))
print('OK replaced | zens-ink words:', words)
