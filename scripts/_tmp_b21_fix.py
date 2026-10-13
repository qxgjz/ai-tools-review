# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# ---- devin-ai-review ----
p = base + r'\content_drafts\2026-10-12-devin-ai-review_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
fixes = [
    ("## Conclusion\n\nDevin is the most capable autonomous software engineer in 2026 for teams with a steady flow of well-scoped tasks:",
     "## Conclusion\n\nDevin remains the reference autonomous software engineer in 2026 for teams with a steady flow of well-scoped tasks:"),
    ("and reporting \"I tested setup, sign-in, and account linking in the browser. Existing email login still works, all checks pass.\"",
     "and reporting that setup, sign-in, and account linking were tested in the browser, with existing email login still working and all checks passing."),
    ("\"I tested setup, sign-in, and account linking in the browser. Existing email login still works, all checks pass.\" That is the core promise",
     "it reports evidence such as setup, sign-in, and account linking tested in the browser with all checks passing. That is the core promise"),
]
for old, new in fixes:
    if old in s:
        s = s.replace(old, new, 1)
        print('devin fix OK:', old[:50])
    else:
        print('devin MISS:', old[:50])
io.open(p, 'w', encoding='utf-8').write(s)

# ---- perplexity-vs-chatgpt-2026 ----
p2 = base + r'\content_drafts\2026-10-12-perplexity-vs-chatgpt-2026_REWRITE.md'
s2 = io.open(p2, encoding='utf-8').read()
fixes2 = [
    ("## Perplexity vs ChatGPT: Pricing Compared\n\n| Plan | Perplexity | ChatGPT |",
     "## Plan-by-Plan Pricing Comparison\n\n| Plan | Perplexity | ChatGPT |"),
    ("**Free** — unlimited text chats with GPT-6, with limited messages for uploads, image creation, voice chats, deep research, memory, Codex, and ChatGPT Work.",
     "**Free** guarantees unlimited text chats on GPT-6 while rationing uploads, image creation, voice chats, deep research, memory, Codex, and ChatGPT Work."),
    ("For cited research answers and deep research, yes — Perplexity Pro at $17/month annual is purpose-built for source-grounded answers.",
     "For cited research answers and deep research, yes — Perplexity Pro at its $17 annual rate is the sharper research subscription, because citations and deep research sit at the center of the product design."),
    ("Free is $0 with unlimited GPT-6 text chats; Go and Plus sit between; Pro adds your choice of 3 usage tiers, GPT-6 Astra, and the Dot agent, per the official pricing page.",
     "Free costs nothing and keeps unlimited GPT-6 conversation; the middle rungs expand access stepwise; Pro adds usage tiers, GPT-6 Astra, and the Dot agent, per the official pricing page."),
]
for old, new in fixes2:
    if old in s2:
        s2 = s2.replace(old, new, 1)
        print('perplexity fix OK:', old[:50])
    else:
        print('perplexity MISS:', old[:50])
io.open(p2, 'w', encoding='utf-8').write(s2)
print('done')
