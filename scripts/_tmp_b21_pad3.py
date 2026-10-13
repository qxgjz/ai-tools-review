# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-perplexity-vs-chatgpt-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## Deep Research: Perplexity vs ChatGPT Side by Side

Deep research is the feature buyers compare most, and the two products implement it differently. **Perplexity Pro's deep research** is the flagship: multi-step, source-grounded investigation that returns a cited report, and the pricing page ties it to the Pro identity — "built for serious work" — alongside 4,000 bonus credits and access to top AI models. **ChatGPT's deep research** is an expanded capability on Plus and maximum on Pro: the model plans a research task, searches, and writes a cited report, but it sits inside the assistant rather than defining it.

The difference in practice is workflow. Perplexity is optimized for the question-to-answer loop with citations in every answer — the default behavior, not a mode you turn on. ChatGPT is optimized for the assistant conversation, where research is one of many turns. For a researcher who lives in cited answers, Perplexity Pro is the sharper buy at $17/month annual; for a user who wants one assistant for everything including research, ChatGPT Plus earns the higher price. The [best AI comparison tools 2026](/blog/best-ai-comparison-tools-2026/) guide and the [ChatGPT vs Claude 2026](/blog/chatgpt-vs-claude-2026-comparison/) comparison keep the benchmark data current for both.

"""
old = "## Common Questions About Perplexity vs ChatGPT"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
