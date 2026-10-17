import io, os, re

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
D = os.path.join(BASE, 'content_drafts')

def rd(fn):
    return io.open(os.path.join(D, fn), encoding='utf-8').read()

def wr(fn, s):
    io.open(os.path.join(D, fn), 'w', encoding='utf-8', newline='').write(s)

# ── 1. 3D generators ──────────────────────────────────────────────
f1 = '2026-10-17-best-ai-3d-generators-2026_NEW.md'
s = rd(f1)
s = s.replace('title: "Best AI 3D Generators 2026: 7 Tools Tested for Game, Print & Product"',
              'title: "Best AI 3D Generators 2026: 7 Tools Compared"')
# outbound markdown links (insert after pricing mentions)
s = s.replace('**Pricing (official meshy.ai/pricing, checked October 2026):**',
              '**Pricing (official [meshy.ai/pricing](https://www.meshy.ai/pricing), checked October 2026):**')
s = s.replace('**Pricing (official tripo3d.ai/pricing):**',
              '**Pricing (official [tripo3d.ai/pricing](https://www.tripo3d.ai/pricing)):**')
s = s.replace('**Pricing:** Creator $30/mo', '**Pricing:** Creator $30/mo (per [hyper3d.ai](https://hyper3d.ai/))')
s = s.replace('## FAQ\n', '## Frequently Asked Questions\n')
wr(f1, s)
print('f1 patched')

# ── 2. is-chatgpt-getting-worse ───────────────────────────────────
f2 = '2026-10-17-is-chatgpt-getting-worse-2026_NEW.md'
s = rd(f2)
s = s.replace('## FAQ\n', '## Frequently Asked Questions\n')
# outbound links
s = s.replace('tracked by chatgptdisaster.com) describes', 'tracked by [chatgptdisaster.com](https://chatgptdisaster.com/why-chatgpt-is-getting-worse.html)) describes')
s = s.replace('The tryorbye.com analysis', 'The [tryorbye.com](https://www.tryorbye.com/products/chatgpt) analysis')
s = s.replace('documented across Reddit threads. And the signalreads.com coverage',
              'documented across Reddit threads. And the [signalreads.com](https://signalreads.com/articles/mass-cancellation-party/) coverage')
# expand: add two H2 sections before "## FAQ"
addition2 = '''
## What the Data Says: Reviews, Threads, and Cancellation Movements

It helps to separate the three kinds of evidence before you conclude anything, because they answer different questions.

**Review aggregation.** G2's Learn Hub analysis of user reviews found that up to 1 in 4 ChatGPT reviews (23%) and 1 in 5 Gemini reviews (20%) mention accuracy friction. That's a measured, review-level signal — not a single viral thread — and it tracks the "hedging instead of answering" complaint that dominates community discussions. When a quarter of reviews mention accuracy problems, the perception of decline has real mass, even if benchmark scores stayed flat.

**Community threads.** The r/ChatGPT thread tracked by chatgptdisaster.com describes the model as one that "no longer feels like the one users paid for, and it hedges instead of answering." The tryorbye.com product analysis aggregates complaints from 5,000+ users who said GPT-5 "feels like a downgrade, creatively and emotionally flat." These are self-selected voices — unhappy users post more than satisfied ones — but the consistency of the language (hedging, flat, downgrade) across independent sources is telling.

**Cancellation movements.** signalreads.com documented thousands of ChatGPT Plus subscribers publicly declaring they're done paying $20/month for degraded service. A mass-cancellation movement is a signal about *value*, not just quality: enough people believe the experience no longer matches the price that organized pushback forms. That's rare in any software category, and it should be taken seriously even if the underlying model improved.

The honest synthesis: the evidence proves a real, measurable decline in *user experience* for a meaningful minority — through evasive answers, creative flattening, and service friction — but it does not prove a benchmark-level regression of the flagship model. Both can be true, and both matter.

## How to Fix the "Worse" Experience Without Switching

Before you cancel, run through the fixes that solve most perceived-degradation problems — they cost nothing and often restore the old feel:

1. **Reset the conversation and restate requirements.** Context saturation is the single biggest cause of "the model got dumber mid-session." Start a fresh thread and re-state your exact task, audience, and constraints.
2. **Add a directness instruction.** If the model hedges, tell it: "Answer directly. No disclaimers, no hedging, no 'it depends.' Give your best answer first." For many users this alone eliminates the evasive-output pattern.
3. **Pin your voice with a custom GPT or project.** "Thin voice training reads generic, producing polished copy with no personality" is a fixable problem: load style guides, sample posts, and a persona description so every output inherits your voice rather than the default corporate tone.
4. **Break long tasks into focused prompts.** "Long drafts get repetitive, reusing sentence patterns across a run of posts" is usually a context-window artifact. Generate each section as its own prompt, then assemble.
5. **Check your plan limits.** If you're on a free or capped plan, throttling changes output behavior. Upgrade for a month and compare — sometimes the "dumber model" is just the throttled one.
6. **A/B test against another model.** Run the same prompt on Gemini's free tier. If Gemini's output is clearly better, the problem is real and the fix is switching — not more prompt engineering.

None of these fix genuine regression, but together they resolve the majority of complaints that look like regression. If you've done all six and ChatGPT still loses your blind test, switch with confidence.

'''
s = s.replace('## Frequently Asked Questions\n', addition2 + '\n## Frequently Asked Questions\n')
wr(f2, s)
print('f2 patched')

# ── 3. chatgpt-pro-200-worth-it ───────────────────────────────────
f3 = '2026-10-17-chatgpt-pro-200-worth-it-2026_NEW.md'
s = rd(f3)
s = s.replace('## FAQ\n', '## Frequently Asked Questions\n')
# outbound links
s = s.replace('tracked by scand.ai) challenges', 'tracked by [scand.ai](https://scand.ai/scandal/chatgpt-users-challenge-200-agi-pricing-after-output-failures)) challenges')
s = s.replace('multiple.chat\'s plan comparison notes', "[multiple.chat](https://multiple.chat/chatgpt-alternatives-2026)'s plan comparison notes")
s = s.replace('per buyersprint.com\'s 2026 pricing survey', 'per [buyersprint.com](https://buyersprint.com/2026/04/20/chatgpt-alternatives-2026/) pricing survey')
# expand: add two H2 sections before "## Frequently Asked Questions"
addition3 = '''
## ChatGPT Pro Features Deep Dive: What $200 Buys in Practice

To decide if Pro is worth it, you need the feature list in concrete terms, not marketing language. In 2026 the practical differences between Plus and Pro are:

**The frontier reasoning model.** Pro unlocks the most capable reasoning model available to consumer ChatGPT users. For code architecture reviews, dense legal or financial analysis, research synthesis, and multi-step problem solving, the quality gap between the standard and frontier models is real — but it only matters if your tasks are hard enough to cross that gap. Answer honestly: do your weekly tasks ever actually fail at the Plus tier, or do you just assume a better model would help?

**Higher usage caps.** Pro dramatically raises limits compared to Plus. The catch, documented in OpenAI Developer Community posts, is that "$200 Pro 20x hard usage limits appeared without advance notice" — the plan that exists to remove limits can still impose them, and the surprise is worse at this price point. If your workflow is high-volume, verify the current cap policy on the official page before relying on unlimited use.

**Advanced research and reasoning tooling.** Pro includes the deeper research capabilities and the reasoning tools that Plus users get only with limited daily allocations. If your work is research-heavy — due diligence, market analysis, literature review — this is the most defensible reason to pay. If your work is short-form writing or everyday Q&A, it is the most wasteful.

**The ecosystem premium.** Pro sits inside the OpenAI product line with the same interface, memory, and integrations you already use. If you've built workflows around ChatGPT, the switching cost to another frontier plan is real, and staying is worth something. But "staying because it's convenient" is not the same as "the $200 is justified" — price the convenience and be honest about it.

The bottom line on features: Pro buys the frontier model, higher caps, and deeper research — three things that only pay for themselves if your workload is heavy and your tasks are hard. Otherwise you're paying $180/month for capability you use twice a week.

## How to Test ChatGPT Pro for Yourself Without Paying First

You don't have to hand over $200 to find out if you need it. Run this protocol on the $20 plan (or free tier) first:

1. **Log your limit hits for two weeks.** Every time you hit a cap, record what you were doing. If you hit limits fewer than five times in two weeks, Pro's higher caps are wasted money.
2. **Build your 10 hardest real tasks.** Architecture reviews, analysis, long synthesis — the work that would plausibly justify a frontier model. Save the exact prompts.
3. **Run them on the standard model first.** If the standard model already handles them, the frontier upgrade is speculative. If it fails, you have a candidate reason to pay.
4. **Run the failures on Claude Max and Gemini.** Access both for two weeks (Claude Pro $20 and Gemini free/Plus cover the test). Score outputs blind on correctness, directness, and completeness.
5. **Name the work that only Pro completes.** If you can't name a task — not a category, a specific recurring task — that only Pro finishes well, the $200 plan is not for you. This single question settles the debate faster than any review.

If the test shows Pro wins on tasks that pay your bills, the subscription pays for itself and the price stops mattering. If it ties or loses, buy Plus or Claude Pro, keep the $180/month, and revisit when your workload actually grows into the plan.

'''
s = s.replace('## Frequently Asked Questions\n', addition3 + '\n## Frequently Asked Questions\n', 1)
wr(f3, s)
print('f3 patched')
