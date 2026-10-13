# -*- coding: utf-8 -*-
"""2026-10-12 战略学习：冷启动增长黑客/零预算流量（方向3）——写经验+3条待办"""
import json, os

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")
STATE = os.path.join(IC, "state.json")
LEARN = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"

# ========== Step 2: 追加经验到学习笔记开头经验表格 ==========
new_row = "| 2026-10-12 | 战略学习 | 冷启动增长黑客/零预算流量方法 | 知识点：1.Reddit零预算真实案例:0观众0预算创始人靠'暖号+先发原生价值再丢链接'做到$17K/月(usegavel,10-08更新)；2.script7案例:89用户/1个月内/零广告=Reddit发故事型非销售内容+X上第一个回复且从不推销+Discord主动帮忙(vynixal)；3.BIP(Building in Public)是近十年独立开发者最有效营销:展示过程/挣扎/代码→信任+反馈闭环(blogburst)；4.10封研究过的邮件>1000封模板邮件,定向冷启动outreach(Greg Isenberg)；5.单渠道深耕>铺5渠道:选一个渠道做到极致(usegavel)；6.新站90天真实外链目标:5-15个相关真实域名,1条有流量的编辑链接>20条目录链接(meeeters)——我们已4条存活差1-11；7.前14天唯一目标是'被索引':GSC验证+sitemap+Bing Webmaster同步,没被索引一切白费(profiletree)——我们10个手动URL验证未启动需补；8.第1个月聚焦地基不是内容:移动3秒加载+干净URL+架构一次做对(firstsearch)；9.新站排名现实周期:3-6个月才有明显流量,低竞争词+技术卓越可8-12周见首个稳定访客(truescho)；10.90天0→50K案例=技术SEO+关键词+内容+内链+结构化内容组合拳(hnkmedia)；11.1篇优质内容多格式分发:博客→YouTube→SlideShare→infographic→推文系列(vebnox)；12.写'用户打进Google的具体问题'而不是关键词(textsight)；13.高DA目录提交→24小时内被索引,跳过6个月sandbox(tapjoin)——我们目录提交策略已验证正确；14.我们现状映射:已过索引期(533工具页收录),外链4/15目标差11个,HN/Reddit社区渠道刚起步被登录态阻塞——社区驱动增长=零预算流量最大机会；15.优先级:社区渠道(Reddit/HN/X)是未来2周最高ROI动作,目录站批量提交保持节奏即可 | 来源tapjoin+callumknox+usegavel+vynixal+blogburst+meeeters+semrush+profiletree+hnkmedia+firstsearch+truescho+textsight+vebnox |\n"

with open(LEARN, encoding="utf-8") as f:
    content = f.read()
# 插入到第2行（表格头之后）：在第3行引用行之前插入
lines = content.split("\n")
# 在第2行后插入新行（index 2 处，即第3行位置）
lines.insert(2, new_row.rstrip("\n"))
with open(LEARN, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("学习笔记经验表格已更新（插入1行）")

# ========== Step 3: 写3条state.json待办 ==========
with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])
existing_ids = {t.get("id") for t in nf}
today = "2026-10-12"

new_todos = [
    {
        "id": "P0-COMMUNITY-REDDIT-20261012",
        "task": "Reddit社区增长(零预算最高ROI动作)：用户登录Beautiful_Smoke_2425后，先在r/SaaS/r/Entrepreneur/r/microsaas暖号——发2-3条故事型非销售内容/真诚回答（不是链接），积累账号可信度后再自然提到aitoolcrux；本周已收集3个待回复帖(r/SaaS 3条)优先真诚回答；禁止纯推销（参考：0观众0预算Reddit暖号→$17K/月案例）",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window2", "增长黑客", "拓荒者"],
        "source": "commander_learning_cold_start_growth_20261012",
        "created_at": today,
    },
    {
        "id": "P1-BACKLINK-15-20261012",
        "task": "外链补足90天目标缺口：当前4条存活dofollow backlink，距目标5-15个相关真实域名差1-11个；优先获取1条'有流量的编辑链接'（客座博客/资源页，质量>数量），而非继续批量目录盲扫；持续使用Serper调研的资源页/客座博客线索（backlink_opportunities.md）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window2", "增长黑客"],
        "source": "commander_learning_cold_start_growth_20261012",
        "created_at": today,
    },
    {
        "id": "P1-GSC-URL-VERIFY-20261012",
        "task": "GSC收录补齐（冷启动第7知识点落地）：10个手动提交URL的验证仍未启动（用户侧GSC后台操作），需在GSC「网址检查」中对这10个URL执行验证/请求收录，确保533工具页+博客页覆盖收录（前14天唯一目标=被索引，我们已过此期但仍未验证10个URL）；指挥官每日调度时跟踪该用户侧待办",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["指挥官"],
        "source": "commander_learning_cold_start_growth_20261012",
        "created_at": today,
    },
]

added = 0
for t in new_todos:
    if t["id"] in existing_ids:
        print(f"跳过已存在: {t['id']}")
        continue
    nf.append(t)
    added += 1

state["next_iteration_focus"] = nf
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"新增待办: {added} 条，active总数: {len(nf)}")
for t in new_todos:
    print(f"  - {t['id']} | {t['priority']} | {t['assigned_to']}")
