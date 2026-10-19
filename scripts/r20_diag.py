from zens_ink import content_qc
from pathlib import Path
p=Path(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\published\2026-09-16-best-ai-voice-changers-2026_READY.md')
r=content_qc.check_draft(p)
print('SCORE',r['score'],'words',r.get('word_count'),'fact',r.get('fact_density'),'vague',r.get('vague_density'))
for c in r['checks']:
    print('OK ' if c['pass'] else 'FAIL', c['check'],'|',c.get('note',''))
