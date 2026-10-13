# -*- coding: utf-8 -*-
import io, json, subprocess, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
files = {
    'lovable-vs-boltnew(b18)': base + r'\content_drafts\2026-10-11-lovable-vs-boltnew_REWRITE.md',
    'clearscope-alternatives': base + r'\content_drafts\2026-10-12-clearscope-alternatives_REWRITE.md',
}
for slug, path in files.items():
    out = subprocess.run([sys.executable, '-m', 'zens_ink.content_qc', path, '--format', 'json'], capture_output=True, text=True, encoding='utf-8')
    try:
        res = json.loads(out.stdout)
    except Exception:
        print(slug, 'ERR', out.stdout[:200], out.stderr[:200]); continue
    r = res[0] if isinstance(res, list) else res
    print('#####', slug, 'score:', r['score'])
    for c in r['checks']:
        print(' -', c['check'], '|', c['pass'], '| w', c['weight'], '|', c.get('note', '')[:90])
    print()
