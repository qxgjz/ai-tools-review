import json
from datetime import datetime

path = 'iteration_center/state.json'
with open(path, encoding='utf-8') as f:
    st = json.load(f)
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# 本轮：P1 ux_p1_still_unstable → completed（线上复核稳定）；P0-301-REDIRECT → completed（3条301已验证）
updates = {
    'ux_p1_still_unstable_2026-10-13_17h': {
        'status': 'completed',
        'completed_at': now,
        'completion_note': '第17轮复核：站点已恢复稳定。服务器端web_fetch验证首页/博客/ranking/tools全200完整渲染；404产物out/404.html存在(98.6KB,web_fetch link dead为404无内容可提取的正常行为)；/tools→/ranking 301为public/_redirects刻意配置(注释"/tools list -> /ranking")非bug保留；巡检所指"Vercel日志"系误判——本站实际部署Cloudflare Pages无Vercel，17:00波动为Cloudflare边缘瞬时抖动已恢复。重复Title已线上确认修复(chat="Chat AI Tools Reviews" vs ai-chatbots="AI Chatbots AI Tools Reviews")。',
    },
    'P0-301-REDIRECT-20261013': {
        'status': 'completed',
        'completed_at': now,
        'completion_note': '3条旧article-api长URL已在public/_redirects配置301到新短URL(commit fcf2dce,Deploy success)。线上服务器端web_fetch验证：1)article-api-...creatium-coach-review-2025-is-this-...-md→/blog/creatium-coach-review-2025/渲染Creatium Coach Review 2026页✅ 2)article-api-...creatium-coach-review-2025-a-handy-way-...-md→同目标✅ 3)article-api-...elevenlabs-review-2026-...-md→/blog/elevenlabs-review-2026/渲染ElevenLabs Review 2026页✅。目标页均存在(creatium 408KB/elevenlabs 215KB产物)。GSC 27曝光404将随301生效转为redirect，新URL收录待GSC下次抓取。',
    },
}

for tid, patch in updates.items():
    for t in st.get('next_iteration_focus', []):
        if t.get('id') == tid:
            t.update(patch)
            break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(st, f, ensure_ascii=False, indent=2)

st2 = json.load(open(path, encoding='utf-8'))
todos = st2.get('next_iteration_focus', [])
arch = [t for t in todos if t.get('status') == 'pending' and t.get('assigned_to') and ('window1' in str(t.get('assigned_to')) or '架构师' in str(t.get('assigned_to')))]
from collections import Counter
print('架构师 pending:', len(arch), [(t.get('priority'), t.get('id')) for t in arch])
allp = [t for t in todos if t.get('status') == 'pending']
print('全局 pending:', len(allp), dict(Counter(t.get('priority') for t in allp)))
