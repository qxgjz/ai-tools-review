# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'

# ---------- beginners ----------
p1 = base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
s1 = io.open(p1, encoding='utf-8').read()
r1 = [
 ("# Best AI Tools for Beginners 2026 (No Tech Background)",
  "# Best AI Tools for Beginners 2026 (Without a Tech Background)"),
 ("## The Best AI Tools for Beginners by Use Case",
  "## Best AI Tools by Use Case in 2026"),
 ("| General questions and research | ChatGPT (free) | Unlimited GPT-6 chats, deep research, no setup |",
  "| General questions and research | ChatGPT (free) | Unlimited GPT-6 chats, deep research, zero setup |"),
 ("Using all three costs nothing.",
  "All three apps run free, so you can keep them all."),
 ("One beginner-specific point: **you do not need to pick just one.**",
  "One beginner-specific point: **you can keep all three in your rotation.**"),
]
for a, b in r1:
    assert a in s1, a[:60]
    s1 = s1.replace(a, b, 1)
io.open(p1, 'w', encoding='utf-8').write(s1)
print('beginners patched')

# ---------- agenta ----------
p2 = base + r'\2026-10-10-agenta-ai-review-2026_DRAFT.md'
s2 = io.open(p2, encoding='utf-8').read()
r2 = [
 ("## How Does Agenta Compare to Building Agents on ChatGPT or n8n?",
  "## Agenta vs ChatGPT Agents vs n8n"),
 ("| Open source | Yes (MIT) | No | Yes (fair-code) |",
  "| Open source | Yes (MIT) | Closed | Yes (fair-code) |"),
 ("| Self-host | Yes (Docker Compose / Helm) | No | Yes |",
  "| Self-host | Yes (Docker Compose / Helm) | Cloud-only | Yes |"),
]
for a, b in r2:
    assert a in s2, a[:60]
    s2 = s2.replace(a, b, 1)
io.open(p2, 'w', encoding='utf-8').write(s2)
print('agenta patched')
