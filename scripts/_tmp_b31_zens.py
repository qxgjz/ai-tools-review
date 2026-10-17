# -*- coding: utf-8 -*-
import io, json, os, subprocess, sys

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
    # find last JSON object
    try:
        j = json.loads(out[out.rfind('{'):out.rfind('}') + 1])
        score = j.get('score') or j.get('overall_score') or j.get('total_score')
        print(fn.split('/')[-1], '| score:', score)
        # print failed checks
        checks = j.get('checks') or j.get('results') or {}
        if isinstance(checks, dict):
            for k, v in checks.items():
                if isinstance(v, dict) and not v.get('passed', True):
                    print('   FAIL:', k, v.get('message', v.get('detail', ''))[:120])
    except Exception as e:
        print(fn.split('/')[-1], '| parse err:', e)
        print('  raw tail:', out[-300:])
