# -*- coding: utf-8 -*-
import io, json, subprocess, sys, time
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = None
for k, v in keys.items():
    if 'github' in k.lower() and 'pat' in k.lower():
        pat = v; break
if not pat:
    for k, v in keys.items():
        if isinstance(v, str) and v.startswith('ghp_'):
            pat = v; break
print('PAT found:', bool(pat))
deadline = time.time() + 600
while time.time() < deadline:
    out = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + pat,
                          'https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=3'],
                         capture_output=True, text=True, encoding='utf-8')
    try:
        runs = json.loads(out.stdout).get('workflow_runs', [])
    except Exception:
        print('parse err', out.stdout[:200]); time.sleep(20); continue
    for r in runs[:3]:
        print(r['head_sha'][:7], r['status'], r.get('conclusion'), r['name'])
    run = runs[0]
    if run['status'] == 'completed':
        print('DONE conclusion=', run.get('conclusion'))
        break
    time.sleep(30)
