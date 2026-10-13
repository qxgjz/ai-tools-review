# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'

# beginners: remove the CTA self-link (it links to its own slug)
p1 = base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
s1 = io.open(p1, encoding='utf-8').read()
s1 = s1.replace(" and use our [best AI tools for beginners 2026](/blog/best-ai-tools-for-beginners-2026/) checklist to map each tool to a specific task this week.",
                " and use this article's checklist to map each tool to a specific task this week.", 1)
io.open(p1, 'w', encoding='utf-8').write(s1)

# agenta: remove duplicate internal links, keep 5 unique targets
p2 = base + r'\2026-10-10-agenta-ai-review-2026_DRAFT.md'
s2 = io.open(p2, encoding='utf-8').read()
# second occurrence of best-ai-agents-2026 in Conclusion/CTA -> plain text
s2 = s2.replace("our [best AI agents 2026](/blog/best-ai-agents-2026/) ranking puts Agenta in context",
                "our best AI agents 2026 ranking puts Agenta in context", 1)
s2 = s2.replace("check back with AIToolCrux for the latest [AI agents 2026](/blog/best-ai-agents-2026/) comparison",
                "check back with AIToolCrux for the latest AI agents 2026 comparison", 1)
# second occurrence of how-to-build in the new section -> keep first only
s2 = s2.replace("our [how to build an AI agent](/blog/how-to-build-an-ai-agent/) guide recommends",
                "our how to build an AI agent guide recommends", 1)
io.open(p2, 'w', encoding='utf-8').write(s2)
print('internal links trimmed')

# verify
for fn, p in [('2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md', p1), ('2026-10-10-agenta-ai-review-2026_DRAFT.md', p2)]:
    s = io.open(p, encoding='utf-8').read()
    ints = re.findall(r'\[[^\]]*\]\((/blog/[^)]+)\)', s)
    exts = re.findall(r'\[[^\]]*\]\((https?://[^)]+)\)', s)
    words = len(re.findall(r"[A-Za-z0-9']+", s))
    print(fn, '| words:', words, '| int:', len(ints), '| ext:', len(exts))
