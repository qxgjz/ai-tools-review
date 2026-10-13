# -*- coding: utf-8 -*-
import json, subprocess
f = r'content_drafts\2026-10-10-what-is-an-ai-agent_DRAFT.md'
out = subprocess.run(['python','-m','zens_ink.content_qc',f,'--format','json'], capture_output=True, text=True)
data = json.loads(out.stdout)[0]
print('score:', data.get('score'), '| wc:', data.get('word_count'))
for c in data.get('checks', []):
    print(' ', c.get('check'), '|', c.get('pass'), '|', c.get('note', '')[:90])
