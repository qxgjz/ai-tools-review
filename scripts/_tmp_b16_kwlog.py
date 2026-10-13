# -*- coding: utf-8 -*-
import io
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\batch_written_keywords.md'
rows = """
| 2026-10-11 | claude vs gemini 2026 (REWRITE, 38->73) | N/A (rewrite) | claude-vs-gemini-2026-comparison | 2120 | Commodity Rewrite (P1) |
| 2026-10-11 | gemini vs chatgpt 2026 (REWRITE, 38->73) | N/A (rewrite) | gemini-vs-chatgpt-2026 | 2135 | Commodity Rewrite (P1) |
| 2026-10-11 | elevenlabs v2 review 2026 (REWRITE, 38->73) | N/A (rewrite) | elevenlabs-v2-review-2026 | 2110 | Commodity Rewrite (P1) |
"""
s = io.open(p, encoding='utf-8').read()
if 'claude-vs-gemini-2026-comparison | 2120' not in s:
    s = s.rstrip() + '\n' + rows
    io.open(p, 'w', encoding='utf-8').write(s)
    print('appended')
else:
    print('already present')
