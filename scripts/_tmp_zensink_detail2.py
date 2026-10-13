# -*- coding: utf-8 -*-
import json, subprocess
files = [r'content_drafts\2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md',
         r'content_drafts\2026-10-10-agenta-ai-review-2026_DRAFT.md',
         r'content_drafts\2026-10-10-cursor-vs-windsurf-2026_REWRITE.md']
for f in files:
    out = subprocess.run(['python','-m','zens_ink.content_qc',f,'--format','json'], capture_output=True, text=True)
    data = json.loads(out.stdout)[0]
    print('===', f.split('\\')[-1], '| score:', data.get('score'), '| wc:', data.get('word_count'))
    checks = data.get('checks')
    if isinstance(checks, list):
        for c in checks:
            if isinstance(c, dict):
                ok = c.get('passed')
                if ok is False or (isinstance(ok, str) and ok.lower() == 'false'):
                    print('  FAIL:', c.get('check') or c.get('name'), '|', str(c.get('reason') or c.get('message') or '')[:180])
    print()
