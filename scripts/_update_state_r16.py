import json
from datetime import datetime

path = 'iteration_center/state.json'
with open(path, encoding='utf-8') as f:
    st = json.load(f)
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

updates = {
    'P0-GEO-CRAWLERS-20261013': {
        'status': 'completed',
        'completed_at': now,
        'completion_note': 'robots.txt已确认AI crawlers全放行(app/robots.ts权威源:GPTBot/OAI-SearchBot/ChatGPT-User/ClaudeBot/PerplexityBot/Google-Extended/Bingbot均Allow /，线上robots.txt验证通过)；删除过时public/robots.txt死文件；文章页可见Last Updated改用updatedAt(freshness强信号，57/156篇有真实更新日期，验证best-ai-image-generators-2026渲染2026-09-14T00:00:00Z)；GSC generative AI报告需登录态确认(本环境无登录，待人工或CDP会话确认)。commit 8e618df已部署，线上200。GEO审计9.2/10。',
    },
    'P2-BLOG-PAGE-SIZE-20261012': {
        'status': 'completed',
        'completed_at': now,
        'completion_note': '上轮已修复(508.8->397KB)，本轮线上复核确认：/blog/microsoft-365-copilot-review-2026/ 与 /blog/ai-coding-tools-comparison-2026/ 均200且<500KB。commit 69d346b部署生效。',
    },
    'ux_p2_site_fully_recovered_2026-10-13': {
        'status': 'completed',
        'completed_at': now,
        'completion_note': '巡检结论确认：网站完全恢复(首页465KB/TTFB 0.87s/1.73s等evidence)，本轮线上复核首页/文章页均200，无新增UX问题。',
    },
}

for tid, patch in updates.items():
    for t in st.get('next_iteration_focus', []):
        if t.get('id') == tid:
            t.update(patch)
            break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(st, f, ensure_ascii=False, indent=2)

# 统计
st2 = json.load(open(path, encoding='utf-8'))
todos = st2.get('next_iteration_focus', [])
arch = [t for t in todos if t.get('status') == 'pending' and t.get('assigned_to') and ('window1' in t['assigned_to'] or '架构师' in str(t.get('assigned_to')))]
from collections import Counter
print('架构师 pending:', len(arch), [(t.get('priority'), t.get('id')) for t in arch])
allp = [t for t in todos if t.get('status') == 'pending']
print('全局 pending:', len(allp), dict(Counter(t.get('priority') for t in allp)))
