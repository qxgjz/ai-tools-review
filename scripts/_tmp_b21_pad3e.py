# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-perplexity-vs-chatgpt-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## The Credits and Quota Reality Check

The fine print decides the real cost. **Perplexity's model** — Free has limited daily usage, and Pro's "4,000 bonus credits" plus expanded Computer access shows the platform meters by credits and sessions; heavy research days burn through daily limits faster than casual days, and the annual price ($17/month billed annually) is the way the platform locks in the committed user. **ChatGPT's model** — Free guarantees unlimited text chats and rations the rest, and the paid rungs expand those limits stepwise; the pricing page's "Limits apply" footnote is the honest statement that every tier has a ceiling.

The planning rule from the r/ChatGPT quote — *"running into the quota wall fairly quickly"* — is to measure your actual weekly usage before choosing: a research-heavy week favors Perplexity's credits-and-citations design; a conversation-and-creation week favors ChatGPT's unlimited-text floor. The [ChatGPT alternatives 2026](/blog/chatgpt-alternatives-2026/) and [best AI tools for beginners 2026](/blog/best-ai-tools-for-beginners-2026/) guides include the cheaper options if either quota model feels like a wall.

"""
old = "## Common Questions About Perplexity vs ChatGPT"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
