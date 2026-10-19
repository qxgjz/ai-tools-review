"""从 data/tools.json 生成 data/tools-compact.json（generator 页专用精简数据）。
保留 generator 推荐算法 + 结果卡片渲染所需字段：id/slug/name/vendor/category/scores/hasFreeTier。
用途：避免 generator 页（'use client'）把全量 tools.json（~9.6MB）打包进客户端 JS。
用法：python scripts/build_tools_compact.py  （tools.json 更新后需重跑）
"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'data', 'tools.json')
dst = os.path.join(root, 'data', 'tools-compact.json')
tools = json.load(open(src, encoding='utf-8'))
KEEP = ('id', 'slug', 'name', 'vendor', 'category', 'scores', 'hasFreeTier')
compact = []
missing_scores = 0
for t in tools:
    if not t.get('scores'):
        missing_scores += 1
        continue
    compact.append({k: t.get(k) for k in KEEP})
json.dump(compact, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
sz = os.path.getsize(dst)
print('SRC_TOOLS=', len(tools), 'COMPACT=', len(compact), 'SKIPPED_NO_SCORES=', missing_scores)
print('COMPACT_SIZE_KB=', round(sz / 1024, 1), 'vs FULL_KB=', round(os.path.getsize(src) / 1024, 1), '(-%d%%)' % round((1 - sz / os.path.getsize(src)) * 100))
