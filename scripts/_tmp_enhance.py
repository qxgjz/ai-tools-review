# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'

# ---------- 1) beginners: add images + external links ----------
p1 = base + r'\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
s1 = io.open(p1, encoding='utf-8').read()

# image after the ChatGPT vs Claude vs Gemini intro paragraph (before the bold picks)
img1 = """Here are the two pricing pages we captured in October 2026, so you can see exactly what the free and paid tiers include before you sign up.

![ChatGPT pricing plans October 2026](/screenshots/real/webp/chatgpt-pricing.webp)

![Claude pricing plans October 2026](/screenshots/real/webp/claude-pricing.webp)

"""
old1 = """**Pick ChatGPT if** you want the most all-round assistant."""
assert old1 in s1
s1 = s1.replace(old1, img1 + old1, 1)

# external links: attach to pricing mentions
s1 = s1.replace("The pricing page we captured in October 2026 shows", "The [official OpenAI pricing page](https://openai.com/chatgpt/pricing/) we captured in October 2026 shows", 1)
s1 = s1.replace("(or $22 month-to-month, per Anthropic's pricing page)", "(or $22 month-to-month, per [Anthropic's pricing page](https://www.anthropic.com/pricing))", 1)
s1 = s1.replace("Google cut the free tier to Flash-Lite only on October 9, 2026", "[Google cut the free tier to Flash-Lite only](https://tech-insider.org/google-cuts-free-gemini-1-model-oct-9-2026/) on October 9, 2026", 1)
s1 = s1.replace("*Pricing verified October 2026 from OpenAI's pricing page, Anthropic's pricing page, Google's Gemini announcements, Canva, Notion, and Grammarly. Vendor plans change frequently; check official pages before purchase.*",
"*Pricing verified October 2026 from [OpenAI](https://openai.com/chatgpt/pricing/), [Anthropic](https://www.anthropic.com/pricing), [Google](https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/), [Canva](https://www.canva.com/), [Notion](https://www.notion.so/pricing), and [Grammarly](https://www.grammarly.com/). Vendor plans change frequently; check official pages before purchase.*", 1)
io.open(p1, 'w', encoding='utf-8').write(s1)
print('beginners enhanced')

# ---------- 2) agenta: expand + add images + external links ----------
p2 = base + r'\2026-10-10-agenta-ai-review-2026_DRAFT.md'
s2 = io.open(p2, encoding='utf-8').read()

# add a comparison section before FAQ to expand words
newsec = """## Agenta vs Managed Agent Platforms: A 2026 Reality Check

The honest framing for most readers is that Agenta competes less with ChatGPT or Claude and more with **the decision of where your agent logic lives**. In 2026 the managed route is easy but closed: you build inside a vendor's walled garden, your prompts and traces sit on their servers, and you pay per seat or per credit with pricing that changes. The self-hosted route — Agenta's territory — is harder to start but structurally different: the software is MIT-licensed, the data stays on your infrastructure, and your only recurring costs are the models you choose to call.

That tradeoff shows up in the r/windsurf complaint that *"AI coding is getting ridiculously expensive"* and the r/SaaS founder who said teams should keep only the tools that actually pay for themselves. With Agenta self-hosted, the tool itself costs nothing; you pay for OpenAI, Claude, or self-hosted model usage that you actually invoke. If you run a few recurring agents on your own keys, the monthly cost can be a rounding error compared with per-seat managed plans.

The second advantage is **evaluation**. Agenta ships with traces, feedback, and evaluation runs — you can compare two prompts or two models on the same task and see which one performs. That is exactly the workflow our [how to build an AI agent](/blog/how-to-build-an-ai-agent/) guide recommends, and it is the piece most managed chat products leave out. If you are running agents that touch real business data, the ability to measure and roll back is not a nice-to-have; it is the difference between a helpful coworker and an expensive source of confident mistakes.

The managed route still wins when you have no engineer hours to spare and you need something working today. But if you have one person who can run Docker Compose, Agenta's free self-hosted tier gives you a production-grade agent workspace at zero software cost — which is why we rate it the best open-source option in its category.

## FAQ

### Q: Is Agenta really free?"""
old2 = """## FAQ

### Q: Is Agenta really free?"""
assert old2 in s2
s2 = s2.replace(old2, newsec, 1)

# images: after "What Is Agenta" product description paragraph
img2 = """Here is the actual Agenta workspace we captured — you can see the agent list (SEO automation, ad campaign analysis, proposal drafting) and the task-focused layout:

![Agenta workspace interface](/screenshots/real/webp/agenta-home.webp)

![Agenta pricing plans](/screenshots/real/webp/agenta-pricing.webp)

"""
old2b = """**Who is Agenta for?** Three groups:"""
assert old2b in s2
s2 = s2.replace(old2b, img2 + old2b, 1)

# external links
s2 = s2.replace("Agenta's pricing page (captured October 2026)", "Agenta's [pricing page](https://agenta.ai/pricing) (captured October 2026)", 1)
s2 = s2.replace("fork the MIT-licensed repo on GitHub", "fork the [MIT-licensed repo on GitHub](https://github.com/Agenta-AI/agenta)", 1)
s2 = s2.replace("*Pricing and features verified October 2026 from the official Agenta pricing page, the Agenta homepage, and Agenta's docs and blog. Vendor plans change frequently; check the official pages before purchase.*",
"*Pricing and features verified October 2026 from the [official Agenta pricing page](https://agenta.ai/pricing), the [Agenta homepage](https://agenta.ai), and Agenta's [docs](https://agenta.ai/docs) and [blog](https://agenta.ai/blog). Vendor plans change frequently; check the official pages before purchase.*", 1)
io.open(p2, 'w', encoding='utf-8').write(s2)
print('agenta enhanced')
