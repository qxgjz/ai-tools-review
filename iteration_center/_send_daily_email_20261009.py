# -*- coding: utf-8 -*-
"""指挥官日报邮件 2026-10-09（HTML版）"""
import smtplib
from email.message import EmailMessage

html = """<html><body style="font-family:Segoe UI,Arial,sans-serif;background:#f4f4f5;padding:20px">
<div style="max-width:720px;margin:0 auto;background:#fff;border-radius:12px;padding:28px;border:1px solid rgba(0,0,0,0.08)">
<h1 style="color:#5E6AD2;margin:0 0 4px">🤖 指挥官日报</h1>
<p style="color:rgba(0,0,0,0.60);margin:0 0 16px">2026-10-09 星期五 · 完成率0%/A目标21%/B目标0%/C目标0%</p>

<span style="display:inline-block;background:#EF4444;color:#fff;border-radius:20px;padding:4px 14px;font-size:13px">🔴 今日预警</span>
<p style="margin:12px 0 20px">今天必须避免的错误：<b>只开单不验收、窗口干活不更新state.json、completed待办堆积不清理、各窗口一次只修2-3篇偷懒</b></p>

<h2 style="color:#111;font-size:18px">📋 待办完成率</h2>
<table style="width:100%;border-collapse:collapse;margin:8px 0 20px">
<tr style="background:#f4f4f5"><th style="padding:8px;text-align:left">指标</th><th style="padding:8px;text-align:left">数值</th></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">总待办</td><td style="padding:8px;border-bottom:1px solid #eee"><b>42条</b>（P0:18, P1:23；清理2条空待办，补录3条P0催办）</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">状态分布</td><td style="padding:8px;border-bottom:1px solid #eee">pending 35 + open 6（创作家6篇关键词文章认领中）+ completed 0</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">完成率</td><td style="padding:8px;border-bottom:1px solid #eee"><b style="color:#EF4444">0%</b>（窗口干活但只写日志不更新state.json=核心问题）</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">各窗口pending</td><td style="padding:8px;border-bottom:1px solid #eee">window2/创作家=14, window1=5, window3=5, window5=5, window7设计师=4, 打磨师=2, 拓荒者=2, analyst=1, ux=1, polisher=1</td></tr>
</table>

<h2 style="color:#111;font-size:18px">📊 今日各窗口进展（9个日志，全部真实）</h2>
<table style="width:100%;border-collapse:collapse;margin:8px 0 20px">
<tr style="background:#f4f4f5"><th style="padding:8px;text-align:left">窗口</th><th style="padding:8px;text-align:left">产出</th><th style="padding:8px;text-align:left">阻塞</th></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">拓荒者-增长</td><td style="padding:8px;border-bottom:1px solid #eee">HN 3篇评论草稿（DeepSeek/Whistle/Jevman）+外链机会报告</td><td style="padding:8px;border-bottom:1px solid #eee">⚠️ HN/Reddit登录阻塞</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">分析师</td><td style="padding:8px;border-bottom:1px solid #eee">关键词机会20词+15页（6个P0：best ai agents/ai agent vs chatbot等）</td><td style="padding:8px;border-bottom:1px solid #eee">—</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">拓荒者-痛点</td><td style="padding:8px;border-bottom:1px solid #eee">72条真实评论/5来源，4个痛点聚类（订阅太贵P0、视频credits烧太快P0）</td><td style="padding:8px;border-bottom:1px solid #eee">—</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">分析师-竞品</td><td style="padding:8px;border-bottom:1px solid #eee">竞品内容缺口：AI Agents分类页（竞品567-620 vs 我们0）等4个缺口</td><td style="padding:8px;border-bottom:1px solid #eee">—</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">打磨师</td><td style="padding:8px;border-bottom:1px solid #eee">3轮质检：幻觉审计报告+全站审计+关键词密度检查</td><td style="padding:8px;border-bottom:1px solid #eee">—</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">体验官</td><td style="padding:8px;border-bottom:1px solid #eee">UX审计（render-blocking、无img标签等6条已录入）</td><td style="padding:8px;border-bottom:1px solid #eee">—</td></tr>
</table>

<h2 style="color:#111;font-size:18px">🎯 30天目标进度</h2>
<table style="width:100%;border-collapse:collapse;margin:8px 0 20px">
<tr style="background:#f4f4f5"><th style="padding:8px;text-align:left">目标</th><th style="padding:8px;text-align:left">当前</th><th style="padding:8px;text-align:left">进度</th></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">A. GSC曝光2095→10000+</td><td style="padding:8px;border-bottom:1px solid #eee">曝光58（当前）/2095（30天）</td><td style="padding:8px;border-bottom:1px solid #eee">21%</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">B. 日均UV5→50+</td><td style="padding:8px;border-bottom:1px solid #eee">GA4无数据</td><td style="padding:8px;border-bottom:1px solid #eee">0%</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">C. 联盟$0→$100/月</td><td style="padding:8px;border-bottom:1px solid #eee">无数据</td><td style="padding:8px;border-bottom:1px solid #eee">0%</td></tr>
</table>

<h2 style="color:#111;font-size:18px">🏗 网站关键数据</h2>
<table style="width:100%;border-collapse:collapse;margin:8px 0 20px">
<tr style="background:#f4f4f5"><th style="padding:8px;text-align:left">指标</th><th style="padding:8px;text-align:left">数值</th></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">文章数</td><td style="padding:8px;border-bottom:1px solid #eee">146</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">工具数</td><td style="padding:8px;border-bottom:1px solid #eee">533</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">截图数</td><td style="padding:8px;border-bottom:1px solid #eee">119</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">迭代轮次</td><td style="padding:8px;border-bottom:1px solid #eee">62</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">设计窗口</td><td style="padding:8px;border-bottom:1px solid #eee">✅ 已开（window7，4条待办：shadcn完整接入/hero重做/视觉审计/排版统一）</td></tr>
</table>

<h2 style="color:#111;font-size:18px">📝 本次补录的待办（3条P0）</h2>
<table style="width:100%;border-collapse:collapse;margin:8px 0 20px">
<tr style="background:#f4f4f5"><th style="padding:8px;text-align:left">#</th><th style="padding:8px;text-align:left">待办</th><th style="padding:8px;text-align:left">负责人</th></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">1</td><td style="padding:8px;border-bottom:1px solid #eee">🔴状态更新铁律：所有窗口完成任务必须立即同步state.json状态，禁止只写日志不更新</td><td style="padding:8px;border-bottom:1px solid #eee">all_windows</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">2</td><td style="padding:8px;border-bottom:1px solid #eee">6篇关键词P0文章3天内完成并标记completed，zens-ink验证≥70分</td><td style="padding:8px;border-bottom:1px solid #eee">创作家</td></tr>
<tr><td style="padding:8px;border-bottom:1px solid #eee">3</td><td style="padding:8px;border-bottom:1px solid #eee">收录P0-2 IndexNow批量提交Top50无曝光工具页（397页未索引最大瓶颈）本周执行</td><td style="padding:8px;border-bottom:1px solid #eee">架构师</td></tr>
</table>

<h2 style="color:#111;font-size:18px">🧠 今日经验</h2>
<p style="margin:8px 0">窗口有日志产出≠任务完成，state.json状态才是唯一验收标准；报告校验闭环已生效（痛点/关键词/竞品P0/P1 100%已录入）；设计工作已独立窗口7并强制"先预览再部署"。</p>

<p style="color:rgba(0,0,0,0.45);font-size:12px;margin-top:24px">AIToolCrux 指挥官自动日报 · 2026-10-09 21:39</p>
</div></body></html>"""

msg = EmailMessage()
msg.set_content(html, subtype='html')
msg['From'] = 'AIToolCrux Commander <840754587@qq.com>'
msg['To'] = '840754587@qq.com'
msg['Subject'] = '【指挥官日报】2026-10-09（完成率0%/A目标21%/B目标0%/C目标0%）'

try:
    s = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30, local_hostname='localhost')
    s.login('840754587@qq.com', 'rkphxyrugwvabdbf')
    s.sendmail('840754587@qq.com', ['840754587@qq.com'], msg.as_string())
    s.quit()
    print('✅ 邮件发送成功')
except Exception as e:
    print('❌ 邮件发送失败:', str(e)[:200])
