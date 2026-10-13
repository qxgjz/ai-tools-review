# -*- coding: utf-8 -*-
import io, json, subprocess
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
for slug in ['lovable-vs-boltnew', 'beautiful-ai-alternatives', 'sudowrite-alternatives']:
    md = base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md'
    r = subprocess.run(['python', '-m', 'zens_ink.content_qc', md, '--format', 'json'], capture_output=True, text=True, cwd=base)
    d = json.loads(r.stdout)[0]
    fails = [(c['check'], c.get('note','')[:60]) for c in d['checks'] if not c['pass']]
    print(slug, '| score:', d['score'], '| words:', d['word_count'], '| vague:', d.get('vague_density'))
    for f in fails:
        print('   FAIL:', f)
