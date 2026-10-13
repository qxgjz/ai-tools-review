# -*- coding: utf-8 -*-
import io, json, subprocess
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
for slug in ['cursor_ai_review', 'midjourney-v7-review-2026', 'suno-alternatives']:
    md = base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md'
    r = subprocess.run(['python', '-m', 'zens_ink.content_qc', md, '--format', 'json'], capture_output=True, text=True, cwd=base)
    try:
        d = json.loads(r.stdout)
        print('===', slug, '| score:', d.get('score') or d.get('overall_score') or d.get('total_score'), '| keys:', list(d.keys())[:12])
        if d.get('vague_words'):
            print('  vague:', d['vague_words'])
        checks = d.get('checks') or d.get('details') or {}
        if isinstance(checks, dict):
            fails = [k for k, v in checks.items() if isinstance(v, dict) and v.get('passed') is False]
            print('  failed checks:', fails[:10])
    except Exception as e:
        print('===', slug, 'PARSE ERR', str(e)[:100])
        print(r.stdout[:800])
