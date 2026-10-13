# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-perplexity-vs-chatgpt-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## Who Should Choose a Different Tool

The honest comparison includes the cases where neither is the right buy. **Teams that need an API for product search** should evaluate Perplexity's API or a search-focused service rather than a consumer plan — the credits economics differ from the chat plans. **Users who need document-level work** — long-form writing, spreadsheets, presentations — get more from ChatGPT's expanded Work and Projects than from Perplexity's answer engine. **Privacy-first users** should check each platform's data-handling policies before choosing, since answer engines and assistants both train on usage by default on some tiers. **And users with a hard budget** should compare the [ChatGPT alternatives 2026](/blog/chatgpt-alternatives-2026/) and the broader [best AI tools for beginners 2026](/blog/best-ai-tools-for-beginners-2026/) lists before committing to either ladder.

The decision rule: Perplexity for cited answers and research, ChatGPT for a general assistant, and a specialized tool when the workload is narrower than either — the match-the-tool-to-the-task discipline this site applies across the whole category.

"""
old = "## Common Questions About Perplexity vs ChatGPT"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
