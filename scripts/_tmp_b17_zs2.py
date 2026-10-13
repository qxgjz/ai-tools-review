# -*- coding: utf-8 -*-
import io, json, subprocess
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
md = base + r'\content_drafts\2026-10-11-suno-alternatives_REWRITE.md'
r = subprocess.run(['python', '-m', 'zens_ink.content_qc', md, '--format', 'json'], capture_output=True, text=True, cwd=base)
d = json.loads(r.stdout)[0]
print('score:', d['score'], 'word_count:', d['word_count'])
for c in d['checks']:
    print(c['check'], '| pass:', c['pass'], '| weight:', c['weight'], '| note:', (c.get('note') or '')[:120])
