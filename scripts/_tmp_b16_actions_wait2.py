# -*- coding: utf-8 -*-
import io, json, subprocess, time
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = ''
for k, v in keys.items():
    if isinstance(v, str) and ('ghp_' in v or 'github_pat' in k):
        pat = v
        break
def runs():
    out = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + pat,
                          'https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=3&event=push'],
                         capture_output=True, text=True).stdout
    return json.loads(out)
for i in range(20):
    try:
        d = runs()
        deploy = None
        for run in d.get('workflow_runs', []):
            if run['name'] == 'Deploy to Cloudflare Pages' and run['head_sha'][:7] == '684c6de':
                deploy = run
                break
        if not deploy:
            print(i, 'deploy run not found')
        else:
            print(i, 'status:', deploy['status'], '| conclusion:', deploy['conclusion'])
            if deploy['status'] == 'completed':
                print('FINAL:', deploy['conclusion'])
                break
    except Exception as e:
        print(i, 'ERR', str(e)[:80])
    time.sleep(30)
