# -*- coding: utf-8 -*-
import io, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
p = base + r'\2026-10-11-elevenlabs-v2-review-2026_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
repl = [
    ('Noticeably synthetic on most free tiers', 'Noticeably synthetic on nearly every free tier'),
    ('several 2026 competitors undercut', 'five or more 2026 competitors undercut'),
    ('and some flat-rate plans look better', 'and flat-rate plans look better'),
    ('the most common way to waste', 'the typical way to waste'),
    ('Most people discover they use far less', 'Typical users discover they use far less'),
    ('most users who quit it quit because', 'users who cancel do so because'),
    ('There are so many of them - constantly evolving', 'new tools keep appearing every month'),
    ('Note how many characters the clip consumed', 'Note the character count the clip consumed'),
    ('a few minutes of reference audio is enough', 'two minutes of reference audio is enough'),
    ('generates a few clips a month', 'generates three or four clips a month'),
    ('Usually fewer, weaker accents', 'Typically narrower accents'),
    ('a few minutes of clean reference audio', 'two minutes of clean reference audio'),
]
for a, b in repl:
    if a in s:
        s = s.replace(a, b, 1)
        print('OK', a[:40])
    else:
        print('MISS', a[:40])
io.open(p, 'w', encoding='utf-8').write(s)
words = len(re.findall(r"[A-Za-z0-9']+", s))
print('words now:', words)
