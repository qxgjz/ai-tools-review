# -*- coding: utf-8 -*-
import io, json, subprocess, time
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = None
for k, v in keys.items():
    if k.lower().startswith('github_pat'):
        pat = v
        break
def gh(path):
    r = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + pat,
                        'https://api.github.com/repos/qxgjz/ai-tools-review' + path],
                       capture_output=True, text=True)
    return json.loads(r.stdout)
for i in range(24):
    runs = gh('/actions/runs?per_page=5')
    deploys = [it for it in runs.get('workflow_runs', []) if it.get('name') == 'Deploy to Cloudflare Pages']
    for it in deploys[:2]:
        print(it['head_sha'][:7], it['status'], it['conclusion'])
    done = [it for it in deploys if it.get('status') == 'completed']
    if done:
        d = done[0]
        print('FINAL:', d['head_sha'][:7], d['conclusion'])
        break
    time.sleep(30)
