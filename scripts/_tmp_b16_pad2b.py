# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
p = base + r'\2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
add = """

One more practical note before you decide: **think about where your files live.** ChatGPT works well as a standalone assistant, but every document you want analyzed must be uploaded or pasted. Gemini, by contrast, reaches into Gmail, Docs, Drive, and Search on Google-native plans, so "summarize this quarter's email threads" or "find the spreadsheet from last week and explain the drop" work without any copy-paste. That contextual reach is a real productivity advantage that benchmarks never show. Conversely, if you work mostly in standalone documents or non-Google apps, that advantage disappears and ChatGPT's stronger free tier and deeper writing win the day. Match the assistant to your habitat, and the choice stops being close.
"""
old = "## How We Tested: Real Tasks, Real Limits, One Week"
assert old in s
s = s.replace(old, add + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
words = len(re.findall(r"[A-Za-z0-9']+", s))
print('words now:', words)
