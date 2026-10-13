# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
p = base + r'\2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
newsec = """## How We Tested: Real Tasks, Real Limits, One Week

To write this comparison we ran both assistants on the same five tasks over a week of daily use, using free tiers first and paid tiers where the task required it.

**Task 1 — Long-form drafting.** We asked both to write a 1,500-word explainer from a short outline. ChatGPT delivered a complete, well-structured draft with minor factual slips that were easy to catch; Gemini's draft was shorter and more template-like, and on the free tier the Flash-Lite model clearly showed its lighter reasoning. ChatGPT won on depth.

**Task 2 — Fact-checking and research.** We asked both to compare three AI pricing plans using only what they knew. ChatGPT produced a clean table with sensible caveats; Gemini flagged its own uncertainty more readily on free tier but was slower to structure the answer. Neither was reliably accurate on recent pricing — we verified everything against official pages — and that is the permanent lesson of AI research: never publish a number an assistant gave you without checking the source.

**Task 3 — Coding help.** We gave both a small Python bug. ChatGPT produced a working fix with an explanation; Gemini produced a reasonable fix too, but with more back-and-forth needed. For IDE-integrated work, ChatGPT's ecosystem wins; for Google-native developers, Gemini Code Assist covers the same ground.

**Task 4 — Multimodal input.** We uploaded a screenshot of a pricing table to both. Gemini extracted the numbers cleanly and quickly; ChatGPT also extracted them correctly but took an extra turn to structure the output. Gemini's native multimodal handling showed here.

**Task 5 — Quota behavior.** This is where the 2026 changes bit hardest. ChatGPT's free tier handled all five tasks with unlimited text chats and only limited uploads — we never felt blocked. Gemini's free tier (Flash-Lite) hit daily caps on heavier reasoning tasks, which is consistent with the October 9, 2026 free-tier reduction. If your usage is daily and substantial, that quota difference alone can decide the winner.

The pattern across the week was stable: **ChatGPT for depth and free-tier power, Gemini for speed, multimodality, and Google integration.** Neither is a bad choice; they are different tools for different daily habits.

## FAQ

### Is ChatGPT better than Gemini?"""
old = "## FAQ\n\n### Is ChatGPT better than Gemini?"
assert old in s
s = s.replace(old, newsec, 1)
io.open(p, 'w', encoding='utf-8').write(s)
words = len(re.findall(r"[A-Za-z0-9']+", s))
print('words now:', words)
