# -*- coding: utf-8 -*-
import io, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
files = ['2026-10-11-claude-vs-gemini-2026-comparison_REWRITE.md',
         '2026-10-11-gemini-vs-chatgpt-2026_REWRITE.md',
         '2026-10-11-elevenlabs-v2-review-2026_REWRITE.md']
for fn in files:
    p = os.path.join(base, fn)
    s = io.open(p, encoding='utf-8').read()
    n = s.count('## FAQ\n')
    s = s.replace('## FAQ\n', '## Frequently Asked Questions\n')
    io.open(p, 'w', encoding='utf-8').write(s)
    print(fn, '| replaced FAQ headings:', n, '| now has FAQHQ:', s.count('## Frequently Asked Questions'))
