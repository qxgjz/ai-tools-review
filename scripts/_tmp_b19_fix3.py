# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-gemini_38_flash_review_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
old = "The r/SaaS founders' keep-vs-cut rule"
new = """| Workload | Best model | Why |
|---|---|---|
| Code autocomplete and quick edits | Flash | Low latency, flat cost per token |
| RAG pipelines | Flash | Retrieval does the heavy lifting |
| Agent tool calls | Flash | Each call is a generation; cost stays sane |
| Multi-step math and deep review | Pro | Extended reasoning wins |
| Long-horizon planning | Pro | Reasoning depth beats speed |

The r/SaaS founders' keep-vs-cut rule"""
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
