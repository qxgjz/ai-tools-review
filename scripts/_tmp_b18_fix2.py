# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, path.split('\\')[-1] + ' :: ' + old[:70]
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print(path.split('\\')[-1], 'patched')

patch(base + r'\content_drafts\2026-10-11-lovable-vs-boltnew_REWRITE.md', [
    ("![Lovable pricing plans](/screenshots/real/webp/lovable-pricing.webp)\n\n![Bolt.new pricing plans](/screenshots/real/webp/bolt-pricing.webp)\n\n| Plan |",
     "![Lovable pricing plans](/screenshots/real/webp/lovable-pricing.webp)\n\n![Bolt.new pricing plans](/screenshots/real/webp/bolt-pricing.webp)\n\nThe tables below summarize both plans.\n\n| Plan |"),
    ("### How much does Bolt.new cost in 2026?\nFree is $0 with 300K daily tokens; Pro is $25/month with 10M tokens and rollover; Teams is $30/member/month; Enterprise is custom. Yearly billing saves up to 28%, per the official pricing page.",
     "### How much does Bolt.new cost in 2026?\nBolt.new pricing starts at $0 free and steps to Pro at $25/month with 10M tokens and rollover, Teams at $30/member/month, and Enterprise at custom rates. Yearly billing saves up to 28%, per the official pricing page."),
    ("### How much does Lovable cost in 2026?\nFree is $0 with 5 lovable.app domains; Pro is $25/month with 100 credits; Business is $50/month; Enterprise is a platform fee, per the official pricing page.",
     "### How much does Lovable cost in 2026?\nLovable pricing runs from a $0 Free tier with 5 lovable.app domains up to Pro at $25/month for 100 credits, Business at $50/month, and Enterprise on a platform fee, per the official pricing page."),
])

patch(base + r'\content_drafts\2026-10-11-sudowrite-alternatives_REWRITE.md', [
    ("Jasper and Copy.ai serve the marketing-adjacent writers who do not need novel-length coherence.",
     "Jasper and Copy.ai serve marketing-adjacent writers who skip novel-length coherence."),
])
print('DONE')
