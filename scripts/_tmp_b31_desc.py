# -*- coding: utf-8 -*-
import io, re, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
files = ['2026-10-17-ai-tools-hallucinate-least-2026_NEW.md',
         '2026-10-17-ai-writing-tools-match-your-voice-2026_NEW.md',
         '2026-10-17-ai-tools-generous-rate-limits-2026_NEW.md']
for fn in files:
    p = os.path.join(base, 'content_drafts', fn)
    s = io.open(p, encoding='utf-8').read()
    m = re.search(r'^description:\s*"(.*?)"$', s, flags=re.M)
    d = m.group(1) if m else 'NONE'
    print(fn.split('-')[3], '| len:', len(d), '|', d[:70])
