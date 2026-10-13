# -*- coding: utf-8 -*-
import json, subprocess
f = r'content_drafts\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md'
out = subprocess.run(['python','-m','zens_ink.content_qc',f,'--format','json'], capture_output=True, text=True)
data = json.loads(out.stdout)[0]
print('keys:', list(data.keys()))
print('score:', data.get('score'))
print('word_count:', data.get('word_count'))
print('checks type:', type(data.get('checks')))
print(json.dumps(data.get('checks'), ensure_ascii=False, indent=1)[:2500])
