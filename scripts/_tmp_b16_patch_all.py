# -*- coding: utf-8 -*-
import io, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'

def patch(fn, repls, anchor, newsec):
    p = os.path.join(base, fn)
    s = io.open(p, encoding='utf-8').read()
    for a, b in repls:
        if a in s:
            s = s.replace(a, b, 1)
            print(fn, 'OK', a[:50])
        else:
            print(fn, 'MISS', a[:50])
    assert anchor in s, 'anchor missing: ' + anchor
    s = s.replace(anchor, newsec + '\n' + anchor, 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", s))
    print(fn, '-> zens-ink words now:', words)
    print()

# ---- Article 1: claude-vs-gemini ----
patch(
    '2026-10-11-claude-vs-gemini-2026-comparison_REWRITE.md',
    [],
    '## Conclusion',
    """## Who Should Pick Each in 2026

The choice narrows to three profiles. **Pick Claude if you write or code daily** — long documents, marketing copy, scripts, contract review, or serious IDE work. Anthropic's models stay coherent where rivals drift, and Claude Code is the most mature terminal agent in 2026. **Pick Gemini if your workday runs in Google Workspace** — Gmail, Docs, Drive, and Search become extensions of the assistant, and AI Plus at $4.99/month is the cheapest capable upgrade on the market. **Pick neither and stay free if your usage is occasional** — both free tiers cover light questions, and the r/SaaS pattern of over-subscribing and under-using is the most expensive mistake in the AI market this year.

One final check before you buy: verify the current prices on the official pages we linked, because both vendors adjust plans quarterly. The October 2026 numbers in this guide — Claude Pro at $18 annual or $22 monthly, Gemini AI Plus at $4.99, AI Pro at $19.99 with 5 TB, and the Flash-Lite-only free tier — were correct as of this writing, but a plan change can shift the math overnight."""
)

# ---- Article 2: gemini-vs-chatgpt ----
patch(
    '2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md',
    [('with only limited uploads — we never felt blocked.',
      'with uploads as the only limit.')],
    '## Conclusion',
    """## Who Should Pick Each in 2026

Three profiles decide the winner. **Pick ChatGPT if you write, research, or code regularly** — GPT-6's free tier is powerful enough for daily text work, and Plus at $20/month unlocks deep research and image generation without a second thought. **Pick Gemini if your data lives in Google** — Workspace integration, native multimodal input, and the AI Pro storage bundle make it the practical choice for Google-native teams. **Pick by free tier first if you are on a tight budget** — ChatGPT's unlimited text chats beat Gemini's Flash-Lite-only free tier since October 9, 2026, so start there and upgrade only when a real limit bites.

As with any assistant, recheck the official pricing pages before you commit. Both OpenAI and Google adjust plans frequently, and the October 2026 figures in this guide — free unlimited GPT-6 text, Plus at $20, Gemini AI Plus at $4.99, AI Pro at $19.99 with 5 TB — were accurate at publication but can change without notice."""
)

# ---- Article 3: elevenlabs ----
patch(
    '2026-10-11-elevenlabs-v2-review-2026_REWRITE.md',
    [('you pay for characters generated, not for time or features.',
      'you pay for characters generated rather than for time or features.')],
    '## Conclusion',
    """## Who Should Pick Which Plan in 2026

Match the plan to your publishing cadence, not to the marketing page. **Stay on Free at 10,000 characters if you test or prototype** — short clips, voice experiments, and one-off projects are fully covered. **Take Starter at $5/month if you publish occasionally for commercial use** — 30,000 characters and basic cloning handle a monthly video or a podcast intro. **Take Creator at $22/month if you publish weekly** — 100,000 characters, full cloning, and dubbing cover a standard YouTube schedule without quota math every weekend. **Step to Pro at $99/month only if you hit Creator's cap** — 500,000 characters and priority generation are for daily publishers and agencies, and most solo creators never need that tier.

Before upgrading, verify the current numbers on the official pricing page — vendors revise plans every few months, and the October 2026 prices in this review were correct at publication but should be rechecked when you buy."""
)
