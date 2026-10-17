# -*- coding: utf-8 -*-
import io, os, re, subprocess

py = r'C:\Users\通明街\AppData\Local\DoubaoWork\User Data\sandbox_runtime\bases\d0ace100fdff5b2d247847aca1e3d83b\python\python.exe'
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
files = [
    'content_drafts/2026-10-17-ai-tools-hallucinate-least-2026_NEW.md',
    'content_drafts/2026-10-17-ai-writing-tools-match-your-voice-2026_NEW.md',
    'content_drafts/2026-10-17-ai-tools-generous-rate-limits-2026_NEW.md',
]
for fn in files:
    p = os.path.join(base, fn)
    r = subprocess.run([py, '-m', 'zens_ink.content_qc', p, '--format', 'json'],
                       capture_output=True, text=True, encoding='utf-8')
    out = (r.stdout or '') + (r.stderr or '')
    scores = re.findall(r'"score"\s*:\s*(\d+)', out)
    fails = re.findall(r'"check"\s*:\s*"([^"]+)",\s*"pass"\s*:\s*false', out)
    print(fn.split('/')[-1], '| scores:', scores, '| fails:', fails)
    wc = re.search(r'"word_count"\s*:\s*(\d+)', out)
    if wc: print('   word_count:', wc.group(1))
