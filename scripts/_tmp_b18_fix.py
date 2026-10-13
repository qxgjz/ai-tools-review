# -*- coding: utf-8 -*-
import io
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, path.split('\\')[-1] + ' :: ' + old[:70]
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8').write(s)
    print(path.split('\\')[-1], 'patched')

# beautiful-ai: add outbound links + question H2
patch(base + r'\content_drafts\2026-10-11-beautiful-ai-alternatives_REWRITE.md', [
    ("## Gamma vs Beautiful.ai: The Direct Head-to-Head",
     "## Is Gamma Better Than Beautiful.ai?"),
    ("The honest verdict: if you present to clients and need guaranteed brand alignment, Beautiful.ai's $14.50 Pro is a fair price. If you need volume, variety, or a zero-cost start, Gamma wins the value equation, and Canva covers the template-heavy middle ground.",
     "The honest verdict: if you present to clients and need guaranteed brand alignment, Beautiful.ai's $14.50 Pro is a fair price. If you need volume, variety, or a zero-cost start, [Gamma](https://gamma.app) wins the value equation, and [Canva](https://www.canva.com) covers the template-heavy middle ground. Both official sites are linked for direct verification of their free tiers."),
])

# sudowrite: add outbound links + question H2
patch(base + r'\content_drafts\2026-10-11-sudowrite-alternatives_REWRITE.md', [
    ("## Claude vs Sudowrite: The Fiction Test",
     "## Is Claude Better Than Sudowrite?"),
    ("**Claude** is the strongest prose writer in 2026",
     "**[Claude](https://www.anthropic.com/claude) is the strongest prose writer in 2026"),
    ("**NovelAI** runs its own models tuned for genre fiction",
     "**[NovelAI](https://novelai.net) runs its own models tuned for genre fiction"),
])
print('DONE')
