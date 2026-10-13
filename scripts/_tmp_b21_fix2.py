# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

p = base + r'\content_drafts\2026-10-12-devin-ai-review_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "## Conclusion\n\nDevin remains the reference autonomous software engineer in 2026 for teams with a steady flow of well-scoped tasks: it explores the codebase, implements, tests in its own browser, and opens the PR ready to merge, with Free at $0, Pro at $20/month, and Max at $200/month on the SWE-2 generation."
new = "## Conclusion\n\nThe buying decision comes down to one question: does your team have a steady stream of well-scoped engineering tasks? If yes, Devin — Free at $0, Pro at $20/month, and Max at $200/month on the SWE-2 generation — is the strongest autonomous engineer in 2026: it explores the codebase, implements, tests in its own browser, and opens the PR ready to merge."
assert old in s; s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('devin conclusion fixed')

p2 = base + r'\content_drafts\2026-10-12-perplexity-vs-chatgpt-2026_REWRITE.md'
s2 = io.open(p2, encoding='utf-8').read()
old2 = "**Free** guarantees unlimited text chats on GPT-6 while rationing uploads, image creation, voice chats, deep research, memory, Codex, and ChatGPT Work."
new2 = "The ChatGPT free rung keeps unlimited conversation on GPT-6, while uploads, image creation, voice chats, deep research, memory, Codex, and ChatGPT Work stay rationed."
assert old2 in s2; s2 = s2.replace(old2, new2, 1)
io.open(p2, 'w', encoding='utf-8').write(s2)
print('perplexity free sentence fixed')
