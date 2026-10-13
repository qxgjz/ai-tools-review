# -*- coding: utf-8 -*-
# 战略学习：2026 SEO/GEO/AI搜索前沿趋势 —— 写入经验表格 + 3条state.json待办
import json, os, datetime

path = r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

today = '2026-10-11'

# 1) 追加战略学习记录到核心原则下方（在 "## 📊 数据说话铁律" 之前）
entry = '''
### {date} 指挥官战略学习：2026年SEO/GEO/AI搜索前沿趋势（来源：RightBlogger/RankingStudios/AIThinkerLab/nAIvigate/ToolStack/Ahrefs 6家权威）
**核心认知（10-15个知识点）**：
1. **GEO=被AI引用，不是排名**：传统SEO抢排名，GEO抢"AI答案里的引用"。2026年Google AI Overviews出现在40-47%搜索（Ahrefs：品牌词83%），出现AI摘要时有机CTR从28%→17%
2. **排名第1≠AI可见**：Google top10与AI引用重叠率从75%→17-38%。第6名页结构更清晰也能被AI引用在#1前面
3. **AI流量转化率是搜索的4-23倍**：ChatGPT转化14.2-15.9%、Perplexity 10.5%、Claude 16.8% vs Google有机1.76%；Ahrefs：AI流量占0.5%访客却贡献12.1%注册（24:1）
4. **前30%内容占44.2%引用**：答案必须出现在文章前30%（导语+第一段），开头1-2句直接给答案（字典式定义），别埋在第四段
5. **事实密度是关键**：每100词至少1个可验证统计/命名实体/具体日期，加统计(+40%可见性)、加引用(+115%排名5的可见性)、加引语是普林斯顿研究三大最有效手段
6. **H2改成真问题**：'Meta Description Tips' → 'What makes a good meta description?'。用People Also Ask提取用户真实问法
7. **FAQ+FAQPage schema是最高转化GEO改动**：6-8个PAA问题，每个<80词答案，加FAQPage JSON-LD
8. **3类schema必须**：Article、FAQPage、BreadcrumbList；3个以上schema类型使LLM引用概率+13%
9. **内容集群（Topical Cluster）**：1主指南+3-5支撑帖+内链互连，AI给覆盖主题多页的站点更高权重
10. **E-E-A-T强化**：实名作者（姓名/照片/背景）、可验证引用、自有数据（"我们测了X个月"）、真实案例。匿名站永远不被AI引用
11. **Google官方立场**：优化生成式AI搜索=还是SEO；不需要llms.txt、不需要特殊AI markup（Google忽略llms.txt）；警惕第三方GEO hacks承诺
12. **新鲜度>传统SEO**：AI引擎重读新内容（Ahrefs：被AI引用的URL平均比Google有机结果新25.7%）；旧文章要定期刷新数据+日期戳
13. **测量GEO**：GSC 2026年6月上线生成式AI性能报告（AI Overviews/AI Mode曝光）；Bing 2026年2月上线AI Performance dashboard；ChatGPT/Perplexity需手动prompt测试（每平台5个品牌prompt）
14. **AI agent搜索来临**：ChatGPT Work模式/Gemini auto browse代用户浏览网页；Google A2A协议（2025年4月）让agent跨厂商协调——内容要被agent解析引用
15. **robots.txt放行AI爬虫**：GPTBot、Google-Extended、PerplexityBot必须允许；很多站无意中屏蔽了它们
16. **红海警示**：Gartner预测2028年前有机搜索流量降50%+；HubSpot已报告70-80%下降。信息类流量在收缩，AI引用流量在增长——**从"排名游戏"转向"被引用竞赛"**

**对我们的直接含义**：aitoolcrux收录/流量上不来的根因=①页面性能故障（AI爬虫也不等慢站）②内容无前30%直接答案/无问题式H2/无FAQ schema ③E-E-A-T弱（无作者页/无自有数据）④GEO测量缺失（没跑过AI引用prompt测试）

---

## 📊 数据说话铁律（必须严格遵守）
'''.format(date=today)

marker = '## 📊 数据说话铁律（必须严格遵守）'
if marker in content:
    content = content.replace(marker, entry, 1)
else:
    content = content + entry

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ 经验已写入 commander_learning.md')

# 2) 写3条state.json待办
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sp = os.path.join(base, 'iteration_center', 'state.json')
with open(sp, encoding='utf-8') as f:
    data = json.load(f)
focus = data.get('next_iteration_focus', [])

new_todos = [
    {
        'id': 'P0-GEO-001',
        'status': 'pending',
        'priority': 'P0',
        'assigned_to': ['window2', '创作家'],
        'task': 'P0-GEO-001: 全站文章GEO结构整改（最高曝光20篇优先）：①每篇开头第1段直接给答案（字典式定义，40-55词自包含）②H2全部改成People Also Ask真实问法（How/What/Best/Is开头）③加FAQ区（6-8问，每问<80词答案）④正文每100词至少1个可验证统计/日期/实体 ⑤加FAQPage+Article+BreadcrumbList schema。用toolstack 5步框架执行，写完用zens-ink复查>70',
        'source': 'commander_learning_geo_2026',
        'created': today
    },
    {
        'id': 'P0-GEO-002',
        'status': 'pending',
        'priority': 'P0',
        'assigned_to': ['window1', '架构师'],
        'task': 'P0-GEO-002: 技术GEO整改：①检查robots.txt放行GPTBot/Google-Extended/PerplexityBot（当前可能屏蔽）②全站文章加FAQPage JSON-LD schema（批量生成脚本）③Article+BreadcrumbList schema补齐 ④确认Cloudflare Pages不拦截AI爬虫（User-Agent检查）',
        'source': 'commander_learning_geo_2026',
        'created': today
    },
    {
        'id': 'P1-GEO-003',
        'status': 'pending',
        'priority': 'P1',
        'assigned_to': ['window4', 'analyst'],
        'task': 'P1-GEO-003: GEO基线测量（本月必做）：①用Perplexity/ChatGPT/Claude各跑5个品牌prompt（"best AI tools directory"、"AI tool comparison"、"futurepedia vs aitoolcrux"等），记录是否被提及/引用/推荐，输出到iteration_center/ai_citation_audit.md ②下月同prompt复测对比，量化GEO提升 ③检查GSC生成式AI性能报告（2026年6月已上线）是否可用',
        'source': 'commander_learning_geo_2026',
        'created': today
    },
]

# 去重
for nt in new_todos:
    exists = any(str(t.get('task', '')).startswith(nt['task'][:30]) for t in focus)
    if not exists:
        focus.append(nt)
        print('✅ 已写入待办: {}'.format(nt['id']))
    else:
        print('已存在跳过: {}'.format(nt['id']))

data['next_iteration_focus'] = focus
with open(sp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('✅ state.json 已更新，active={}'.format(len(focus)))
