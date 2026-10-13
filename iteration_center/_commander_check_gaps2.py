# -*- coding: utf-8 -*-
import json

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)
todos = data.get('next_iteration_focus', [])

print('=== 检查关键词: compare CTR / -site: 污染 / tools重定向 / 404缓存 / CTA ===')
keys = ['compare', 'site:', '-site', 'tools 301', '404', 'cta', 'query', 'pollut']
for t in todos:
    tt = (t.get('title', '') + ' ' + t.get('description', '')).lower()
    if any(k in tt for k in keys):
        print(f"  [{t.get('status')}] {t.get('id')} | {t.get('assigned_to')} | {t.get('title')}")

print()
print('=== 体验官6条待办是否都在 ===')
ux_ids = ['ux_p0_render_blocking_scripts_2026-10-09', 'ux_p0_no_img_tags_2026-10-09',
          'ux_p1_tools_redirect_2026-10-09', 'ux_p1_html_size_2026-10-09',
          'ux_p1_404_uncached_2026-10-09', 'ux_p1_cta_missing_2026-10-09']
existing = {t.get('id') for t in todos}
for i in ux_ids:
    print(f"  {i}: {'✓ 已录入' if i in existing else '✗ 缺失'}")
