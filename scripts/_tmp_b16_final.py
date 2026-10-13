# -*- coding: utf-8 -*-
import io, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# 1) log: mark curl status
lp = base + r'\iteration_center\window_logs\creator_2026-10-11.md'
s = io.open(lp, encoding='utf-8').read()
s = s.replace('| 待验证 |', '| 200 OK |').replace('| 待验证 |', '| 200 OK |')
s = s.replace('- git commit + push + GitHub Actions 部署 + curl 线上验证（见下）。', '- git commit 684c6de + push + GitHub Actions Deploy success + curl 线上验证三篇 HTTP 200，H1 与截图 webp 均在页面渲染。')
io.open(lp, 'w', encoding='utf-8').write(s)
print('log updated, remaining 待验证:', s.count('待验证'))

# 2) state: commit fields
pp = base + r'\iteration_center\state.json'
st = json.load(io.open(pp, encoding='utf-8'))
st['latest_commit'] = '684c6de'
st['last_commit'] = '684c6de'
st['last_push_commit'] = '684c6de'
st['last_deploy_commit'] = '684c6de'
io.open(pp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state commit fields updated')
