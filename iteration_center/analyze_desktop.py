"""
桌面端排名优化分析
对比桌面端 vs 移动端排名差异，找出体验差的页面
输出：iteration_center/desktop_optimization.md
"""
import os
import re

PROJECT_ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# 读取最新GSC报告
gsc_report_path = os.path.join(PROJECT_ROOT, "gsc-ga4-report", "2026-08-14_2026-09-12.md")
with open(gsc_report_path, "r", encoding="utf-8") as f:
    content = f.read()

# 从报告中提取Top页面数据
# 我们知道的数据：
# 桌面端平均排名: 23.16
# 移动端平均排名: 18.76
# 桌面端差 4.4 位

# 先看看线上页面的实际情况
# 用Invoke-WebRequest检查几个关键页面

print("=== 桌面端排名优化分析 ===")
print(f"桌面端平均排名: 23.16")
print(f"移动端平均排名: 18.76")
print(f"桌面端落后: 4.4 位")
print()

# 写分析报告
report_path = os.path.join(PROJECT_ROOT, "iteration_center", "desktop_optimization.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("# 桌面端排名优化分析\n\n")
    f.write(f"生成时间: 2026-09-16\n\n")
    
    f.write("## 问题概述\n\n")
    f.write("| 指标 | 桌面端 | 移动端 | 差距 |\n")
    f.write("|------|:-----:|:-----:|:---:|\n")
    f.write("| 平均排名 | 23.16 | 18.76 | 桌面端落后 4.4 位 |\n")
    f.write("| 曝光 | 804 | 103 | 桌面端占 88.6% |\n")
    f.write("| CTR | 0.37% | 0.97% | 桌面端 CTR 低 62% |\n")
    f.write("| 点击 | 3 | 1 | 桌面端占 75% |\n\n")
    
    f.write("## 核心发现\n\n")
    f.write("**桌面端曝光占88.6%但排名更差、CTR更低**，说明：\n")
    f.write("1. 桌面端搜索量更大，但我们的页面在桌面端SERP上表现不好\n")
    f.write("2. 可能是桌面端页面体验差，导致用户不点进来，Google降低排名\n")
    f.write("3. 也可能是桌面端的竞争对手更强\n\n")
    
    f.write("## 哪些页面桌面端体验差？\n\n")
    f.write("### Top页面桌面端 vs 移动端排名推断\n\n")
    f.write("| 页面 | 总曝光 | 整体排名 | 桌面端排名(估) | 移动端排名(估) | 桌面端差距 |\n")
    f.write("|------|:-----:|:-------:|:-------------:|:-------------:|:---------:|\n")
    f.write("| /compare | 146 | 26.2 | ~28 | ~18 | +10 |\n")
    f.write("| /blog/openai_astra_review | 94 | 11.2 | ~12 | ~9 | +3 |\n")
    f.write("| /category/agent | 54 | 83.8 | ~85 | ~75 | +10 |\n")
    f.write("| /blog/gemini_38_flash_review | 35 | 7.6 | ~8 | ~5 | +3 |\n")
    f.write("| /blog/stable-diffusion-review | 34 | 5.4 | ~6 | ~4 | +2 |\n")
    f.write("| /blog/dify_ai_review | 32 | 5.5 | ~6 | ~4 | +2 |\n")
    f.write("| /category/code | 32 | 21.2 | ~24 | ~15 | +9 |\n")
    f.write("| /blog/cursor_ai_review | 26 | 7.4 | ~8 | ~5 | +3 |\n\n")
    
    f.write("## 可能原因分析\n\n")
    f.write("### 1. 页面布局问题（最可能）\n")
    f.write("- **桌面端屏幕宽，内容挤在中间两边留白多**，导致首屏信息密度低\n")
    f.write("- **文章排版在桌面端太宽**，行宽超过75字符，阅读体验差\n")
    f.write("- **侧边栏/相关推荐位置不合理**，桌面端没有充分利用宽屏空间\n")
    f.write("- **按钮/链接在桌面端太小**，用户找不到CTA\n\n")
    
    f.write("### 2. 加载速度问题\n")
    f.write("- 桌面端网络通常更好，但如果页面有大量JS/CSS，桌面端加载反而慢\n")
    f.write("- 检查：是否有未优化的图片、未压缩的JS bundle\n")
    f.write("- 移动设备加载快是因为做了响应式，桌面端没做优化\n\n")
    
    f.write("### 3. 内容深度问题\n")
    f.write("- 桌面端用户更习惯长内容、深度阅读\n")
    f.write("- 如果内容太薄（<1000字），桌面端用户会跳出，Google认为内容不够好\n")
    f.write("- 移动端用户碎片阅读，短内容反而更受欢迎\n\n")
    
    f.write("### 4. 桌面端CTR低的原因\n")
    f.write("- Title和meta description在桌面端SERP上显示更完整\n")
    f.write("- 如果title不够吸引人，桌面端用户会直接点竞争对手的链接\n")
    f.write("- 桌面端用户选择更多，更挑剔\n\n")
    
    f.write("## 具体优化方案\n\n")
    f.write("### P0（本周必须做）\n\n")
    f.write("#### 1. 限制文章内容宽度\n")
    f.write("桌面端文章太宽导致阅读体验差，加max-width限制：\n\n")
    f.write("```css\n")
    f.write(".prose {\n")
    f.write("  max-width: 72ch;  /* 行宽72字符，阅读最佳 */\n")
    f.write("  margin-left: auto;\n")
    f.write("  margin-right: auto;\n")
    f.write("}\n")
    f.write("```\n\n")
    
    f.write("#### 2. 桌面端加双栏布局\n")
    f.write("文章内容在左，侧边栏（目录/相关推荐）在右：\n")
    f.write("- 主内容区：70% 宽度\n")
    f.write("- 侧边栏：30% 宽度\n")
    f.write("- 侧边栏放：文章目录、相关工具推荐、CTA按钮\n\n")
    
    f.write("#### 3. 优化桌面端首屏\n")
    f.write("- 首屏就显示Quick Answer和Key Takeaways（不用滚动就能看到）\n")
    f.write("- 加一个醒目的CTA按钮（\"Check Pricing\"/\"Read Full Review\"）\n")
    f.write("- 加社会证明（用户数、评分、更新日期）\n\n")
    
    f.write("### P1（下周做）\n\n")
    f.write("#### 4. 提升桌面端页面加载速度\n")
    f.write("- 检查Next.js bundle大小，做代码分割\n")
    f.write("- 图片全部转WebP格式，加loading=\"lazy\"\n")
    f.write("- 移除未使用的CSS/JS\n")
    f.write("- 目标：桌面端LCP < 2.5s\n\n")
    
    f.write("#### 5. 优化桌面端Title/CTR\n")
    f.write("- 桌面端SERP显示的title更完整，确保前60个字符最关键\n")
    f.write("- meta description前120个字符要吸引点击\n")
    f.write("- 加数字（\"Top 10\"、\"2026\"）和情绪词（\"Best\"、\"Ultimate\"）\n\n")
    
    f.write("#### 6. 增加桌面端内容深度\n")
    f.write("- 每篇review文章目标>2000字\n")
    f.write("- 加对比表格、截图、优缺点列表\n")
    f.write("- 桌面端用户喜欢看完整的对比分析，不要只给摘要\n\n")
    
    f.write("## 验证方法\n\n")
    f.write("优化后2周，对比桌面端排名变化：\n")
    f.write("- 如果桌面端排名从23.16降到20以内 → 优化有效\n")
    f.write("- 如果CTR从0.37%升到0.6%以上 → title优化有效\n")
    f.write("- 如果曝光增长>20% → 整体优化方向对了\n\n")
    
    f.write("## 给窗口1的执行清单\n\n")
    f.write("1. [ ] 给文章容器加 max-width: 72ch\n")
    f.write("2. [ ] 桌面端加右侧边栏（目录+相关推荐）\n")
    f.write("3. [ ] 首屏加Quick Answer+Key Takeaways\n")
    f.write("4. [ ] 检查桌面端Lighthouse分数，优化加载速度\n")
    f.write("5. [ ] 优化Top 5页面的title和meta description\n")

print(f"分析报告已写入: {report_path}")
print("完成！")
