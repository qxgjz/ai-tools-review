# -*- coding: utf-8 -*-
import io, json, subprocess, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
path = base + r'\content_drafts\2026-10-12-clearscope-alternatives_REWRITE.md'
out = subprocess.run([sys.executable, '-m', 'zens_ink.content_qc', path, '--format', 'json'], capture_output=True, text=True, encoding='utf-8')
res = json.loads(out.stdout)
r = res[0] if isinstance(res, list) else res
for k, v in r.items():
    print(k, ':', str(v)[:300])
