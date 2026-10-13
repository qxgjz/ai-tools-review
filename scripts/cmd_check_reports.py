# -*- coding: utf-8 -*-
# 检查：1) 性能故障是否已录入待办 2) 3篇假完成整改文章当前分数记录 3) 报告文件中的P0/P1问题提取
import json, os, re, glob

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)
focus = data.get('next_iteration_focus', [])

print('=== 1. 性能/故障相关待办检查 ===')
kw = ['性能', '故障', 'TTFB', '超时', '504', '慢', '不可达', '404', '加载']
hits = [t for t in focus if any(k in str(t.get('task', '')) for k in kw)]
for t in hits:
    print('[{}|{}|{}] {}'.format(t.get('status'), t.get('priority'), t.get('assigned_to'), str(t.get('task'))[:120]))
if not hits:
    print('❌ 未找到性能故障相关待办！UX报告P0未录入')

print()
print('=== 2. 3篇整改文章在state.json中的记录 ===')
slugs = ['claude-opus-4-vs-gpt-5-2026', 'perplexity-vs-chatgpt-2026', 'midjourney-v7-vs-dall-e-3-2026']
for s in slugs:
    hits = [t for t in focus if s in str(t.get('task', ''))]
    for t in hits:
        print('[{}|{}] {}'.format(t.get('status'), t.get('priority'), str(t.get('task'))[:150]))

print()
print('=== 3. 报告文件P0/P1问题提取 ===')
# audit_findings.md 提取 P0
af = os.path.join(base, 'iteration_center', 'audit_findings.md')
if os.path.exists(af):
    with open(af, encoding='utf-8') as f:
        content = f.read()
    # 找最近的P0行
    lines = content.split('\n')
    print('audit_findings.md 总行数:', len(lines))
    # 打印最后40行看最新问题
    for l in lines[-40:]:
        if l.strip():
            print(l[:130])
