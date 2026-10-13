# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'

# beginners: +100 words on the pay-or-not section
p1 = base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
s1 = io.open(p1, encoding='utf-8').read()
add1 = """

One more practical note on cost: the four-dollar question beginners always ask is whether they should buy a bundle like a ChatGPT Plus and a Notion Plus subscription at once. The honest answer in 2026 is that you almost never need two paid AI subscriptions in month one. Pick the single tool you actually open every day, pay for that one, and keep the rest on free tiers. When a second subscription starts to look necessary, that is usually a signal to audit your workflow instead of your wallet — the r/SaaS founder who published what his 4-person team kept versus cut found that most teams over-subscribe and under-use. Revisit your AI spending monthly, cancel what you did not open, and you will stay on the right side of the "AI is too expensive" trap while still getting real value from the tools that matter.
"""
old1 = """## The Best AI Tools for Beginners by Use Case"""
assert old1 in s1
s1 = s1.replace(old1, add1 + '\n' + old1, 1)
io.open(p1, 'w', encoding='utf-8').write(s1)
print('beginners +100')

# agenta: +90 words on migration path at end of new section
p2 = base + r'\2026-10-10-agenta-ai-review-2026_DRAFT.md'
s2 = io.open(p2, encoding='utf-8').read()
add2 = """

If you are already running agents inside ChatGPT or a managed platform and considering Agenta, the migration path is gentler than you might expect. Agenta supports standard workflows: you can import prompts, point it at your existing LangChain or LlamaIndex pipelines, and keep your current model API keys. The pieces you lose are the vendor's hosted conveniences — built-in hosting, turnkey integrations, and a managed UI — and the pieces you gain are data ownership, unlimited agents on self-hosted plans, and evaluation tooling. For teams whose monthly managed-platform bill is creeping past a few hundred dollars, that trade is usually worth a weekend of infrastructure work, which is why the self-hosted MIT option keeps gaining adoption among technical teams in 2026.
"""
old2 = """The managed route still wins when you have no engineer hours to spare"""
assert old2 in s2
s2 = s2.replace(old2, add2 + '\n' + old2, 1)
io.open(p2, 'w', encoding='utf-8').write(s2)
print('agenta +90')

# cursor: +130 words on VS Code migration at end of weaknesses section
p3 = base + r'\2026-10-10-cursor-vs-windsurf-2026_REWRITE.md'
s3 = io.open(p3, encoding='utf-8').read()
add3 = """

A final practical point that decides many purchases: **how much migration work is involved.** Cursor is a VS Code fork, so your extensions, keybindings, themes, and settings largely carry over — a team standardized on VS Code can switch to Cursor with almost zero training time. Windsurf ships its own interface and workflow, so the move is more of a deliberate change: you will remap muscle memory and re-check which extensions behave differently. For individual developers that is a fun weekend experiment; for a team of ten it is a real cost. Factor that in before you standardize: if you are happy with VS Code's feel and just want better AI, Cursor is the lower-friction upgrade. If you want a genuinely different, agent-first editing paradigm and you have time to learn it, Windsurf's free tier makes that experiment free.
"""
old3 = """## FAQ"""
assert old3 in s3
s3 = s3.replace(old3, add3 + '\n' + old3, 1)
io.open(p3, 'w', encoding='utf-8').write(s3)
print('cursor +130')
