# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-claude-opus-4-vs-gpt-5-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## Memory, Context, and the Everyday Assistant

For everyday assistant work, the two products differ in where they put their limits. **ChatGPT Free gives you unlimited text chats with GPT-6** and rations everything else — uploads, image creation, voice, deep research, memory, Codex, and Work are all "limited" on the pricing page — which makes it the most usable free assistant in the category. **Claude Free** gives full chat, web search, file creation, code execution, memory, apps, and Artifacts at $0, with usage limits applying at the plan level. Both free tiers are genuinely useful; the difference is ChatGPT's unlimited-text guarantee versus Claude's broad tool set.

On paid tiers, **Pro (Claude) adds more usage, scheduled tasks, and dashboards**, while **Plus (ChatGPT) adds advanced reasoning, Projects, custom GPTs, and expanded everything** — the packaging reflects the same split: Claude optimizes for depth per session, ChatGPT for breadth across sessions. The [Claude alternatives 2026](/blog/claude-alternatives-2026/) and [ChatGPT alternatives 2026](/blog/chatgpt-alternatives-2026/) guides list the cheaper and specialized options around both, and the [Gemini vs ChatGPT 2026](/blog/gemini-vs-chatgpt-2026/) page adds the third option for the same buying decision.

"""
old = "## Common Questions About Claude Opus 4 vs GPT-5"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
