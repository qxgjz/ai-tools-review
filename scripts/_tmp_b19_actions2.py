# -*- coding: utf-8 -*-
import io, json, subprocess, time
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
deadline = time.time() + 900
while time.time() < deadline:
    out = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + pat,
                          'https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=10'],
                         capture_output=True, text=True, encoding='utf-8')
    try:
        runs = json.loads(out.stdout).get('workflow_runs', [])
    except Exception:
        print('parse err'); time.sleep(30); continue
    dep = next((r for r in runs if 'cloudflare' in r['name'].lower()), None)
    if dep is None:
        print('no deploy run yet'); time.sleep(30); continue
    print(dep['head_sha'][:7], dep['name'], dep['status'], dep.get('conclusion'))
    if dep['status'] == 'completed':
        print('DEPLOY DONE conclusion=', dep.get('conclusion'))
        break
    time.sleep(30)
