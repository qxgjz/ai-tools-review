# -*- coding: utf-8 -*-
import io, json, subprocess
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
files = ['2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md',
         '2026-10-10-agenta-ai-review-2026_DRAFT.md',
         '2026-10-10-cursor-vs-windsurf-2026_REWRITE.md']
for f in files:
    out = subprocess.run(['python','-m','zens_ink.content_qc',base+'\\'+f,'--format','json'], capture_output=True, text=True)
    d = json.loads(out.stdout)[0]
    print(f, '| zens:', d.get('score'), '| wc:', d.get('word_count'))
