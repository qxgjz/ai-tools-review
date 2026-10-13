# -*- coding: utf-8 -*-
import io, json, subprocess, time
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = None
for k, v in keys.items():
    if k.lower().startswith('github_pat'):
        pat = v
        break
assert pat, 'no github pat'
def gh(path):
    r = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + pat,
                        'https://api.github.com/repos/qxgjz/ai-tools-review' + path],
                       capture_output=True, text=True)
    return json.loads(r.stdout)
for i in range(20):
    runs = gh('/actions/runs?per_page=5')
    items = runs.get('workflow_runs', [])
    for it in items[:3]:
        print(it['head_sha'][:7], it['status'], it['conclusion'], it['name'])
    head = items[0] if items else {}
    if head.get('head_sha', '').startswith('b0e8927') or head.get('head_sha', '').startswith('8b687e9'):
        if head.get('status') == 'completed':
            print('FINAL:', head['head_sha'][:7], head['conclusion'])
            break
    time.sleep(25)
