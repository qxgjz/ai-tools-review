# -*- coding: utf-8 -*-
"""batch31 fix1: descriptions 70-160 chars + source refs -> markdown outbound links"""
import io, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
D = os.path.join(base, 'content_drafts')

JOBS = [
    ('2026-10-17-ai-tools-hallucinate-least-2026_NEW.md',
     "AI hallucination in 2026: benchmark rates for GPT-5, Claude, Gemini and Perplexity, plus a verification workflow to catch wrong answers.",
     [
        ('(Whizi)', '([Whizi\'s 108-model meta-analysis](https://whizi.io/de/resources/ai-hallucination-statistics/))'),
        ('(Hackceleration Claude review, 2026)', '([Hackceleration Claude review](https://www.hackceleration.com/labs/review/claude))'),
        ('(RFP.wiki Perplexity review)', '([RFP.wiki Perplexity review](https://learn.g2.com/perplexity-ai-review))'),
        ('(r/ChatGPT, via chatgptdisaster.com)', '([chatgptdisaster.com](https://chatgptdisaster.com/why-chatgpt-is-getting-worse.html))'),
        ('(Presenc AI, Suprmind 2026)', '([Presenc AI](https://presenc.ai/research/ai-hallucination-rate-benchmarks-2026), [Suprmind](https://suprmind.ai/hub/ai-hallucination-rates-benchmarks-in-2026/))'),
        ('(G2 Learn Hub)', '([G2 Learn Hub](https://learn.g2.com/ai-code-generation))'),
     ]),
    ('2026-10-17-ai-writing-tools-match-your-voice-2026_NEW.md',
     "Why AI writing sounds generic in 2026, which tools have real voice training (Writesonic, Jasper, Copy.ai, Sudowrite, Rytr), and how to make output match your voice.",
     [
        ('(Blaze AI review via writenexa.com)', '([Blaze AI review, writenexa.com](https://www.writenexa.com/blog/blaze-ai-explained-i-put-its-writing-engine-to-work-for-a-month/))'),
        ('(writenexa.com)', '([writenexa.com](https://www.writenexa.com/blog/blaze-ai-explained-i-put-its-writing-engine-to-work-for-a-month/))'),
        ('(Velocity)', '([Velocity](https://www.velocity.li/blog/ai-writing-brand-voice-social-media-2026))'),
        ('(Dupple)', '([Dupple](https://dupple.com/learn/best-ai-for-writing))'),
        ('(Humbot, 2026)', '([Humbot](https://humbot.ai/hub/humanize-ai/how-to-humanize-ai-writing))'),
        ('(DailyAIWire, 2026)', '([DailyAIWire](https://dailyaiwire.com/ai-blog/how-to-humanize-ai-content/))'),
        ('(G2 Perplexity review)', '([G2 Perplexity review](https://learn.g2.com/perplexity-ai-review))'),
        ('(redeepseek.io)', '([redeepseek.io](https://www.redeepseek.io/blog/best-ai-writing-tools-that-sound-human))'),
        ('(AIToolKit Pro)', '([AIToolKit Pro](https://aitoolkitpro.blog/best-ai-writing-tools-2026/))'),
        ('(CompareBestAI)', '([CompareBestAI](https://comparebestai.com/articles/which-ai-writing-tool-produces-the-least-ai-sounding-output))'),
        ('(UmanWrite\'s 2026 research)', '([UmanWrite\'s 2026 research](https://www.umanwrite.com/articles/humanize-ai-text-step-by-step))'),
     ]),
    ('2026-10-17-ai-tools-generous-rate-limits-2026_NEW.md',
     "Claude, ChatGPT, Gemini and Copilot rate limits in 2026: official message caps, weekly walls, and a mixing strategy to avoid hitting them mid-task.",
     [
        ('(support.claude.com, updated October 2026)', '([Anthropic Help Center](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work))'),
        ('(support.anthropic.com)', '([Anthropic Claude Code docs](https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan))'),
        ('(help.openai.com, GPT-5.5 in ChatGPT)', '([OpenAI Help Center](https://help.openai.com/zh-hant/articles/11909943-gpt-52-in-chatgpt))'),
        ('(help.openai.com)', '([OpenAI Help Center](https://help.openai.com/pt-br/articles/20001354))'),
        ('(openai.com, ChatGPT Go announcement)', '([OpenAI announcement](https://openai.com/index/introducing-chatgpt-go/))'),
        ('(toolchase.com, 2026)', '([toolchase.com](https://toolchase.com/blog/best-chatgpt-alternatives-2026/))'),
        ('(buyersprint.com)', '([buyersprint.com](https://buyersprint.com/2026/04/20/chatgpt-alternatives-2026/))'),
        ('(aitoolreviews.co, 2026)', '([AI Tool Reviews](https://aitoolreviews.co/articles/why-ai-writing-sounds-robotic-fix-2026/))'),
        ('(Hackceleration 2026)', '([Hackceleration](https://www.hackceleration.com/labs/review/claude))'),
        ('(Hackceleration review of Claude)', '([Hackceleration review of Claude](https://www.hackceleration.com/labs/review/claude))'),
        ('(OpenAI Developer Community, via pain-point research)', '([OpenAI Developer Community](https://community.openai.com/))'),
     ]),
]

for fn, desc, pairs in JOBS:
    p = os.path.join(D, fn)
    s = io.open(p, encoding='utf-8').read()
    # fix description
    s2 = re.sub(r'(?<=^description: ").*?(?=")', desc, s, count=1, flags=re.M | re.S)
    if s2 == s:
        print(fn, 'DESC NOT REPLACED'); continue
    n = 0
    for old, new in pairs:
        if old in s2:
            s2 = s2.replace(old, new); n += 1
    io.open(p, 'w', encoding='utf-8', newline='').write(s2)
    print(fn, '| desc replaced | links replaced:', n)
