# -*- coding: utf-8 -*-
import json, subprocess, io, re
files = [r'content_drafts\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md',
         r'content_drafts\2026-10-10-agenta-ai-review-2026_DRAFT.md',
         r'content_drafts\2026-10-10-cursor-vs-windsurf-2026_REWRITE.md']
for f in files:
    out = subprocess.run(['python','-m','zens_ink.content_qc',f,'--format','json'], capture_output=True, text=True)
    data = json.loads(out.stdout)[0]
    print('===', f.split('\\')[-1], '| score:', data.get('score'), '| word_count:', data.get('word_count'))
    checks = data.get('checks') or {}
    for name, c in checks.items():
        if isinstance(c, dict):
            passed = c.get('passed')
            if passed is False or (isinstance(passed, str) and passed.lower() == 'false'):
                print('  FAIL:', name, '|', str(c.get('reason') or c.get('message') or '')[:150])
    print()
