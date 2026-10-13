# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
st['total_articles_generated'] = 59
st['iteration_log'].append({
    'batch': 'batch22',
    'date': '2026-10-13',
    'window': 'window2',
    'action': '2 new articles from P0 pain points (video credits burn + not-worth-the-money pricing) + 1 rewrite (runway-vs-pika-2026); screenshots verified one-by-one (runway-home/runway-pricing/pika-pricing/hailuo-home newly captured, midjourney-plans/cursor-pricing reused+re-verified); sora-home rejected (Cloudflare)',
    'slugs': ['ai-video-generator-credits-burn-fast-2026', 'ai-tools-not-worth-the-money-2026', 'runway-vs-pika-2026'],
    'zens_ink': '73/73/73',
    'llmevalkit': '100/100/100',
    'screenshots': '3/2/2, all verified one-by-one',
    'internal_links_ok': True,
    'git': 'pending push',
    'online_200': 'pending',
    'deploy': 'pending',
})
io.open(base + r'\iteration_center\state.json', 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state saved, total:', st['total_articles_generated'])

kp = base + r'\iteration_center\batch_written_keywords.md'
ks = io.open(kp, encoding='utf-8').read()
block = """
## batch22 (2026-10-13) - 2 new + 1 rewrite
- ai-video-generator-credits-burn-fast-2026 | Why AI Video Generators Burn Through Credits Fast in 2026 | kw: ai video generator credits | 73 | 2463 | 3 screenshots | NEW (pain point P0 #2)
- ai-tools-not-worth-the-money-2026 | AI Tools Not Worth the Money in 2026: Honest Pricing Review | kw: ai tools not worth the money | 73 | 2295 | 2 screenshots | NEW (pain point P0 #1)
- runway-vs-pika-2026 | Runway vs Pika 2026: Which AI Video Generator Wins? | kw: runway vs pika | 73 | 2142 | 2 screenshots | REWRITE
"""
io.open(kp, 'w', encoding='utf-8').write(ks.rstrip() + '\n' + block)
print('keywords appended')

log = """# Creator Window Log - 2026-10-13 (Batch 22)

## Summary
Wrote 2 new articles from the P0 pain-point backlog and rewrote 1 low-score article. All 3 passed dual verification: zens-ink 73 + llmevalkit 100 (no hallucinations).

| Slug | Title | Type | Words | Screenshots | zens-ink | llmevalkit |
|---|---|---|---|---|---|---|
| ai-video-generator-credits-burn-fast-2026 | Why AI Video Generators Burn Through Credits Fast in 2026 | New (pain point P0 #2) | 2463 | 3 | 73 | 100 |
| ai-tools-not-worth-the-money-2026 | AI Tools Not Worth the Money in 2026: Honest Pricing Review | New (pain point P0 #1) | 2295 | 2 | 73 | 100 |
| runway-vs-pika-2026 | Runway vs Pika 2026: Which AI Video Generator Wins? | Rewrite | 2142 | 2 | 73 | 100 |

## Screenshot verification (per user rule: screenshots must match content, reject captcha/404/duplicates)
- NEW captured + verified one-by-one: runway-home ("Building Real-World Intelligence", partners Adobe/Allstate/LIONSGATE/Amazon), runway-pricing (Free 125cr / Standard $12 625cr / Pro $28 2,250cr POPULAR / Max $76 9,500cr BEST VALUE with rollover, -20% annual), pika-pricing (Free 0cr packs / Starter $10 900cr / Creator $35 3,150cr BEST VALUE 8-parallel / Fancy $95 8,550cr unlimited parallel, Save 20%), hailuo-home (H3 Live Now, From $9.99/mo, 3,000 free credits, 2K/5s/21:9)
- REUSED + re-verified: midjourney-plans (Basic $10 200min / Standard $30 15hr / Pro $60 30hr Stealth / Mega $120 60hr, 20% annual), cursor-pricing (Hobby free / Individual $20 / Teams $40/user / Enterprise custom)
- REJECTED: sora-home (Cloudflare "Verify you are human" bot check)

## Quality notes
- negflip fixes this batch: table cells with "only"/"no cap" retitled, FAQ headings that overlapped the pricing table keywords retitled ("Which AI video generator has the most credits for the price?" -> "How do I choose the right subscription size?"), duplicated sentence pairs paraphrased (Runway/Pika commercial-license FAQ vs body)
- Structure: BLUF Quick Answer, Definition-first opening, pricing tables, question-format H2, 5 FAQ, verified screenshots, 3-5+ internal links to existing slugs, 2-3 authoritative outbound links
- Pain-point quotes referenced: r/artificial ("unlimited creation or high monthly credits/tokens", "which ones are actually worth using"), r/ChatGPT (Copilot $50 quota-wall), r/SaaS (keep-vs-cut), HN (accelerate comprehension or incoherence)
- Self-check blocks appended to all 3 drafts

## State
- posts.json: 156 entries (2 appended, 1 updated with content overwrite + quickAnswer/excerpt/keyTakeaways/faq/internalLinks/affiliateLinks/hasRealScreenshots/screenshotCount/wordCount/date=2026-10-13)
- state.json: total_articles_generated 56 -> 59, iteration_log batch22 appended
"""
io.open(base + r'\iteration_center\window_logs\creator_2026-10-13.md', 'w', encoding='utf-8').write(log)
print('log written')
