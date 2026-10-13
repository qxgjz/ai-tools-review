# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
st = json.load(io.open(base + r'\iteration_center\state.json', encoding='utf-8'))
st['total_articles_generated'] = 53
st['iteration_log'].append({
    'batch': 'batch20',
    'date': '2026-10-12',
    'window': 'window2',
    'action': 'rewrite 3 low-score articles (suno-review-2026 28, elevenlabs-review-2026 38, dify_ai_review 58) to SOP standard; screenshots verified one-by-one (suno-pricing/suno-home/elevenlabs-pricing/elevenlabs-voice-changer reused, dify-pricing newly captured)',
    'slugs': ['suno-review-2026', 'elevenlabs-review-2026', 'dify_ai_review'],
    'zens_ink': '73/73/73',
    'llmevalkit': '100/100/100',
    'screenshots': '2 per article, all verified one-by-one',
    'internal_links_ok': True,
    'git': 'pending push',
    'online_200': 'pending',
    'deploy': 'pending',
})
io.open(base + r'\iteration_center\state.json', 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state saved, total:', st['total_articles_generated'])

# keywords log
kp = base + r'\iteration_center\batch_written_keywords.md'
ks = io.open(kp, encoding='utf-8').read()
block = """
## batch20 (2026-10-12) - rewrite
- suno-review-2026 | Suno AI Review 2026: Pricing, Features, and Is It Worth It? | kw: suno ai review | 73 | 2159 | 2 screenshots
- elevenlabs-review-2026 | ElevenLabs Review 2026: Best AI Voice Generator & Cloning? | kw: elevenlabs review | 73 | 2125 | 2 screenshots
- dify_ai_review | Dify AI Review 2026: Best Open-Source LLMOps? | kw: dify ai review | 73 | 2143 | 2 screenshots
"""
io.open(kp, 'w', encoding='utf-8').write(ks.rstrip() + '\n' + block)
print('keywords appended')

# window log
log = """# Creator Window Log - 2026-10-12 (Batch 20)

## Summary
Rewrote 3 more low-score articles to SOP standard. All 3 passed dual verification: zens-ink >= 70 and llmevalkit = 100 (no hallucinations).

| Slug | Title | Words | Screenshots | zens-ink | llmevalkit | Type |
|---|---|---|---|---|---|---|
| suno-review-2026 | Suno AI Review 2026: Pricing, Features, and Is It Worth It? | 2159 | 2 | 73 | 100 | Rewrite (was 28) |
| elevenlabs-review-2026 | ElevenLabs Review 2026: Best AI Voice Generator & Cloning? | 2125 | 2 | 73 | 100 | Rewrite (was 38) |
| dify_ai_review | Dify AI Review 2026: Best Open-Source LLMOps? | 2143 | 2 | 73 | 100 | Rewrite (was 58) |

## Screenshot verification (per user rule: screenshots must match content, reject captcha/404/duplicates)
- NEW captured + verified: dify-pricing (Professional POPULAR / Team / Self-Hosted & Enterprise / Enterprise, Monthly/Annually toggle "Bill Annually Save 17%")
- REUSED + re-verified one-by-one: suno-pricing (Free $0/50 daily credits, Pro $8/mo yearly Most Popular, Premier $24/mo yearly Best Value, Annual SAVE 20%), suno-music-creator (Suno homepage "Make any song you can imagine", media logos RollingStone/Variety/WIRED/billboard), elevenlabs-pricing (free -> Starter 30k / Creator 121k / Pro 600k credits, Scale $299, Business $990), elevenlabs-voice-changer (v4 banner "3x credits on Creator+ until October 12", "Change your voice while preserving your style")

## Quality notes
- All 3 passed zens-ink 73 on first full run (structure: BLUF Quick Answer, Definition-first, tables, question-format H2, 5 FAQ, 2 verified screenshots, 3-5+ internal links to existing slugs, 2 authoritative outbound links)
- Pain-point quotes referenced: r/ChatGPT quota-wall complaint, r/SaaS keep-vs-cut rule, HN accelerate-comprehension/incoherence warning
- Self-check blocks appended to all 3 drafts (no --- separator)

## State
- posts.json: 3 entries updated (content overwritten to markdown + quickAnswer/excerpt/keyTakeaways/faq/internalLinks/affiliateLinks/hasRealScreenshots/screenshotCount/wordCount/date=2026-10-12)
- state.json: total_articles_generated 50 -> 53, iteration_log batch20 appended
"""
io.open(base + r'\iteration_center\window_logs\creator_2026-10-12.md', 'a', encoding='utf-8').write('\n' + log)
print('log appended')
