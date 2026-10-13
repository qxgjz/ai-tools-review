# -*- coding: utf-8 -*-
import io, json, subprocess, tempfile, os
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
keys = json.load(io.open(base + r'\iteration_center\api_keys.json', encoding='utf-8'))
pat = ''
for k, v in keys.items():
    if isinstance(v, str) and ('ghp_' in v or 'github_pat' in k):
        pat = v
        break
print('pat prefix:', pat[:10] if pat else 'NONE')
r = subprocess.run(['curl.exe', '-s', '-o', 'NUL', '-w', '%{http_code}', '-H', 'Authorization: Bearer ' + pat, 'https://api.github.com/rate_limit'], capture_output=True, text=True)
print('rate_limit http:', r.stdout)
r2 = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + pat, 'https://api.github.com/repos/qxgjz/ai-tools-review/actions/runs?per_page=1&event=push'], capture_output=True, text=True)
print('runs http head:', r2.stdout[:200])
