# -*- coding: utf-8 -*-
# 更新 commander_learning.md：关键数据表 + 追加今日调度记录
import os, datetime, re

path = r'C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

today = '2026-10-11'

# 1) 更新关键数据表
replacements = {
    '| GSC曝光 | 2,095（旧30天）/ 58（新资源28天，9/30起有数据） | 2026-10-10 |':
    '| GSC曝光 | 2,095（旧30天）/ 46（新资源10-01~10-06周期） | 2026-10-11 |',
    '| GSC点击 | 9（旧30天）/ 0（新资源） | 2026-10-10 |':
    '| GSC点击 | 9（旧30天）/ 0（新资源） | 2026-10-11 |',
    '| 文章总数 | 146 | 2026-10-10 |':
    '| 文章总数 | 154 | 2026-10-11 |',
    '| 工具总数 | 533 | 2026-10-10 |':
    '| 工具总数 | 533 | 2026-10-11 |',
    '| 真实截图数 | 119（public/screenshots递归统计） | 2026-10-10 |':
    '| 真实截图数 | 127（public/screenshots递归统计） | 2026-10-11 |',
    '| 待办总数 | 58→清理9completed+6open修复+4去重→45，补录假完成整改+3条报告P0=49（P0:25,P1:30,P2:6→清理后） | 2026-10-10 14:37 |':
    '| 待办总数 | 60 active（P0:24,P1:31,P2:5），清理13 completed到archived（累计510），补录P0-PERF-001性能故障 | 2026-10-11 |',
    '| 待办完成率 | 17.3%（9 completed / 52，<50%需催办；假完成3篇已重开整改；已清理至archived累计497） | 2026-10-10 14:37 |':
    '| 待办完成率 | 18.1%（13 completed / 72，<50%需催办；本轮清理13条到archived累计510，补录性能P0） | 2026-10-11 |',
    '| 迭代轮次 | 488（archived累计，含本轮清理9条） | 2026-10-10 |':
    '| 迭代轮次 | 510（archived累计，含本轮清理13条） | 2026-10-11 |',
}
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
    else:
        print('⚠️ 未找到: {}'.format(old[:50]))

# 2) 追加今日调度记录（插到 "## 📊 数据说话铁律" 之前）
entry = '''
### {date} 指挥官每日调度（SOP版）
- **完成率18.1%**：60 active待办中0 completed（13条completed已清理到archived累计510）；P0:24/P1:31/P2:5
- **窗口负载（pending）**：创作家28条（最重）、分析师6、设计师5、拓荒者5、架构师1、增长黑客1、打磨师2
- **完成真实性验证✅**：打磨师整改3篇文章复查真实分——claude-opus-4-vs-gpt-5-2026=88分、perplexity-vs-chatgpt-2026=88分、midjourney-v7-vs-dall-e-3-2026=88分，全部≥70真实完成（非假完成）
- **新错误发现**：UX日志10-10报告**网站性能故障持续36小时+**（首页TTFB 4.29s、加载15s超时、404 code=000）但state.json无对应待办——报告P0未录入！已补录P0-PERF-001给架构师
- **GA4结论**：异常流量P0（10-03单日893 sessions是8倍中位数）已录入✅；(not set)落地页276 sessions仅1 engaged已录入✅；但4个拉取脚本仍指向旧property 556518278（96%Bot污染）
- **30天目标A进度**：新GSC资源46曝光/0点击（10-01~10-06），距10000+差距巨大
- **新经验**：打磨师R5真修复逻辑有效——HTML包装骗分（95假分）→转标准markdown（<h2>→##、<a>→[text](url)）后真实100分；指挥官必须用zens-ink content_qc.check_draft(path)复查真实分，不能信日志
- **下一步**：性能P0-PERF-001架构师立即处理；GA4脚本切新property；创作家28条pending批量消化（每次≥5条）

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
print('✅ commander_learning.md 已更新 ({})'.format(today))
