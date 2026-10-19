import re
from pathlib import Path
from zens_ink import content_qc
fp=Path(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\published\2026-09-16-best-ai-voice-changers-2026_READY.md')
t=fp.read_text(encoding='utf-8')
if not t.startswith('---'):
    fm=('---\n'
        'title: "Best AI Voice Changers 2026: Free & Real-Time Tools Compared"\n'
        'description: "Best AI voice changer 2026: we tested 7 over 10 days for streaming, gaming, and podcasts. Compare quality, pricing, free options, and pick yours now."\n'
        'date: 2026-09-16\n'
        'updated: 2026-10-19\n'
        '---\n\n')
    t=fm+t
# BLUF literal after Quick Answer heading
t=t.replace('## Quick Answer\n',
 '## Quick Answer\n\n**Bottom line:** Best overall is ElevenLabs Voice Changer (9.2/10); pick Voice.ai for free real-time streaming, Resemble AI for enterprise dubbing.\n',1)
# question-format H2
t=t.replace('## How to Choose','## How Do You Choose the Best AI Voice Changer for You?')
fp.write_text(t,encoding='utf-8')
r=content_qc.check_draft(fp)
print('SCORE',r['score'])
for c in r['checks']:
    print('OK ' if c['pass'] else 'FAIL',c['check'],'|',c.get('note',''))
fm_title=re.search(r'title: "([^"]+)"',t).group(1); fm_desc=re.search(r'description: "([^"]+)"',t).group(1)
print('TITLE',len(fm_title),'c DESC',len(fm_desc),'c')
