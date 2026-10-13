# -*- coding: utf-8 -*-
"""用外部权威数据作为 context 重跑幻觉检测（真正有效的检测）"""
import os, sys, json
from pathlib import Path

ROOT = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(ROOT); sys.path.insert(0, '.')

from llmevalkit.hallucination import (
    EntityHallucination, NumericHallucination, ContradictionDetector, FabricatedInfo,
)

# 权威 context（从官网抓的真实数据）
AUTHORITATIVE = {
    'midjourney-v7-vs-flux': """
Midjourney pricing (official docs.midjourney.com 2026):
- Basic plan: $10/month (billed monthly), $96/year ($8/mo)
- Standard plan: $30/month, $288/year ($24/mo), 15 fast GPU hours, unlimited relax
- Pro plan: $60/month, $576/year ($48/mo), 30 fast GPU hours, stealth mode
- Mega plan: $120/month, $1152/year ($96/mo), 60 fast GPU hours
- No free tier. Fast GPU overage $4/hour.

Flux 1.1 Pro pricing (official docs.bfl.ai / blackforestlabs.ai):
- FLUX1.1 [pro]: $0.04 per image (API, pay-as-you-go)
- FLUX.1 Kontext [pro]: $0.04/image (4 credits)
- FLUX.1 Kontext [max]: $0.08/image (8 credits)
- No subscription; billed per image generated.
- Max resolution 4 megapixels (2048x2048) on ultra.

Flux is developed by Black Forest Labs, a German company spun out of Stability AI.
Flux 1.1 Pro is known for strong prompt adherence and text rendering.
Midjourney v7 is known for aesthetic quality and character consistency.
""",
    'chatgpt-vs-claude': """
OpenAI ChatGPT pricing (official openai.com/api/pricing 2026):
- ChatGPT Free: GPT-4o mini access with daily message limits
- ChatGPT Plus: $20/month, GPT-4o access, advanced data analysis
- ChatGPT Team: $25/user/month
- GPT-4o API: $2.50/M input tokens, $10/M output tokens
- GPT-4o context window: 128K tokens

Anthropic Claude pricing (official anthropic.com/pricing 2026):
- Claude Free: limited usage
- Claude Pro: $20/month, extended Claude usage
- Claude Team: $25/user/month
- Claude 3.7 Sonnet API: $3/M input, $15/M output
- Claude Sonnet 4.5: $3/M input, $15/M output
- Claude Sonnet 5: $2/M input, $10/M output
- Claude 3.7 context window: 200K tokens

OpenAI founded 2015, San Francisco. Anthropic founded 2021, San Francisco.
""",
    'claude-37-vs-gpt4o': """
Claude 3.7 Sonnet (official anthropic.com/news/claude-3-7-sonnet):
- Released February 2025
- Pricing: $3 per million input tokens, $15 per million output tokens
- Extended thinking mode: enabled via "thinking" parameter, budget up to 128K output tokens
- Context window: 200K tokens
- Same price in both standard and extended thinking modes (thinking tokens included in output price)
- Benchmarks: strong on SWE-bench coding, long-context reasoning

GPT-4o (official openai.com):
- Released May 2024
- Pricing: $2.50 per million input tokens, $10 per million output tokens
- Context window: 128K tokens
- Multimodal: native image, audio, video input
- Real-time voice mode available
- Faster inference than GPT-4 Turbo

Cost comparison: Claude 3.7 output ($15/M) is 50% more expensive than GPT-4o output ($10/M).
Claude 3.7 input ($3/M) is 20% more expensive than GPT-4o input ($2.50/M).
""",
    'n8n-review': """
n8n pricing (official n8n.io/pricing 2026):
- Community Edition: free, self-hosted, unlimited workflows/users
- Starter Cloud: €20/month (billed annually, €24 monthly), 2,500 workflow executions/month, 5 concurrent executions, 1 shared project
- Pro Cloud: €50/month (billed annually, €60 monthly), 10,000 executions, 20-50 concurrent executions, 3 shared projects, 7 days insights
- Business: €667/month (billed annually, €800 monthly), 40,000 executions, SSO/LDAP, Git version control, 30 days insights
- Enterprise: custom pricing

n8n charges per workflow execution (one complete run = one execution).
Unlike Zapier which bills per task/step, n8n's execution = full workflow run regardless of steps.
n8n is open-source (fair-code), founded 2019 by Jan Oberhauser, based in Berlin, Germany.
n8n supports 400+ integrations and has built-in AI agent nodes.
""",
}

drafts = {
    'midjourney-v7-vs-flux': 'content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md',
    'chatgpt-vs-claude': 'content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md',
    'claude-37-vs-gpt4o': 'content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md',
    'n8n-review': 'content_drafts/2026-10-09-n8n-review-2026_DRAFT.md',
}

detectors = [
    ('entity', EntityHallucination(use_llm=False)),
    ('numeric', NumericHallucination(use_llm=False)),
    ('fabricated', FabricatedInfo(use_llm=False)),
    ('contradiction', ContradictionDetector(use_llm=False)),
]

results = {}
for slug, path in drafts.items():
    text = Path(path).read_text(encoding='utf-8')
    ctx = AUTHORITATIVE[slug]
    print(f'\n=== {slug} (article {len(text)} chars, authoritative ctx {len(ctx)} chars) ===')
    results[slug] = {}
    for name, d in detectors:
        try:
            r = d.evaluate(answer=text, context=ctx)
            results[slug][name] = {'score': r.score, 'reason': r.reason, 'details': r.details}
            print(f'  [{name}] score={r.score:.3f} | {r.reason[:120]}')
        except Exception as e:
            results[slug][name] = {'error': str(e)}
            print(f'  [{name}] ERROR: {e}')

# Print numeric mismatches in detail
print('\n' + '='*70)
print('NUMERIC MISMATCHES (article says X, authoritative context says Y):')
print('='*70)
for slug, res in results.items():
    n = res.get('numeric', {}).get('details', {})
    if isinstance(n, dict) and n.get('checks'):
        bad = [c for c in n['checks'] if not c.get('match', True)]
        if bad:
            print(f'\n--- {slug}: {len(bad)} mismatches ---')
            for c in bad[:15]:
                print(f"  article={c.get('output')!r}  official={c.get('context')!r}")

# Print fabricated statements
print('\n' + '='*70)
print('FABRICATED STATEMENTS (unsupported by authoritative context):')
print('='*70)
for slug, res in results.items():
    f = res.get('fabricated', {}).get('details', {})
    if isinstance(f, dict) and f.get('statements'):
        bad = [s for s in f['statements'] if not s.get('supported', True)]
        if bad:
            print(f'\n--- {slug}: {len(bad)} unsupported ---')
            for s in bad[:10]:
                print(f"  [{s.get('coverage',0):.2f}] {s.get('text','')[:200]}")

# Save
out = Path('iteration_center/_hallucination_with_official_ctx.json')
out.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(f'\nSaved: {out}')
