# SEO Toolkit 自动化工具链使用手册

> **核心原则：能用脚本/API自动化的，AI绝不手动操作。AI只做需要判断和创作的部分。**

## 工具链总览

| 脚本 | 功能 | 调用方式 | 输出 |
|------|------|---------|------|
| `keyword_pipeline.py` | 关键词挖掘（SERP+竞争度+意图+PAA） | `python scripts/seo_toolkit/keyword_pipeline.py --seed "ChatGPT" --count 15` | keyword_pipeline.md + state.json待办 |
| `competitor_pipeline.py` | 竞品分析（批量抓取页面结构） | `python scripts/seo_toolkit/competitor_pipeline.py --keyword "best AI tools"` | competitor_templates.md + competitor_analysis/ |
| `painpoint_pipeline.py` | 用户痛点挖掘（Reddit+G2+PAA） | `python scripts/seo_toolkit/painpoint_pipeline.py --keyword "ChatGPT"` | user_painpoints/{keyword}_summary.md |
| `quality_gate.py` | 15项质量门检查 | `python scripts/seo_toolkit/quality_gate.py --slug {文章slug}` | 通过/不通过+具体问题 |
| `screenshot_bot.py` | Playwright批量截图 | `python scripts/seo_toolkit/screenshot_bot.py --url https://... --tool chatgpt` | public/screenshots/{tool}/3张WebP |
| `gsc_pipeline.py` | GSC分析+待办自动写入 | `python scripts/seo_toolkit/gsc_pipeline.py` | gsc_analysis_{日期}.md + state.json待办 |
| `publisher.py` | 自动写入+git+线上验证 | `python scripts/seo_toolkit/publisher.py --slug {文章slug}` | commit hash + 线上验证结果 |

## 各窗口调用脚本的标准流程

### 窗口4（数据/SEO分析）每次触发：

```bash
# 1. GSC分析（自动识别3类问题页面+写待办）
python scripts/seo_toolkit/gsc_pipeline.py

# 2. 关键词挖掘（从state.json选一个P0大品牌词作为seed）
python scripts/seo_toolkit/keyword_pipeline.py --seed "Claude" --count 15

# 3. 竞品分析（针对Top P0词）
python scripts/seo_toolkit/competitor_pipeline.py --keyword "Claude vs ChatGPT"
```

AI只需要：从输出中判断哪些词最值得写、哪些竞品结构最值得借鉴。

### 窗口3（内容生产）每次触发：

**调研阶段（3:00）：**
```bash
# 调用窗口4产出的keyword_pipeline.md，选1个P0词
# 调用painpoint_pipeline挖掘用户痛点
python scripts/seo_toolkit/painpoint_pipeline.py --keyword "Claude"
```

**写作阶段（7:00）：**
- AI读 keyword_pipeline.md + competitor_templates.md + user_painpoints/
- AI生成Brief（用模板）+ 写文章正文（创作部分AI做）
- 用Python写入posts.json

**发布阶段（11:00）：**
```bash
# 1. 截图（如果文章需要新工具截图）
python scripts/seo_toolkit/screenshot_bot.py --url https://claude.ai --tool claude

# 2. 质量门检查（15项逐项检查）
python scripts/seo_toolkit/quality_gate.py --slug {文章slug}
# 不通过→AI修复→重新检查，直到15/15通过

# 3. 发布（tsc+git+Vercel+线上验证）
python scripts/seo_toolkit/publisher.py --slug {文章slug} --message "feat: add article"
```

### 窗口1（技术/SEO）每次触发：
- 读state.json的P0待办
- 用Python扫描+修复
- tsc验证+git提交+线上验证

### 窗口2（外链）每次触发：
- 用Serper API批量搜索外链目标（Python脚本）
- AI判断哪些目标值得提交
- 浏览器提交表单（需要人工交互的部分）

### 窗口5（变现）每次触发：
- Python扫描posts.json的联盟链接
- AI判断哪些链接需要更新
- 新联盟申请（AI写申请邮件）

### 窗口6（UI/UX）每次触发：
- Playwright截图对比页
- AI分析设计问题
- 修改代码+tsc+git+线上验证

## 脚本输出格式标准

所有脚本输出统一格式，AI读取后直接可用：

### keyword_pipeline.md 格式：
```
| 优先级 | 关键词 | KD | 低DR站数 | 意图 | 内容类型 | PAA数量 |
| P0 | Claude review 2026 | 27 | 10 | commercial | 评测页 | 4 |
```

### quality_gate.py 输出：
```
✅ [1] 字数2500-4000: 2850
❌ [4] 有对比表: 无 → 修复: 添加对比表格
检查结果: 14/15 通过
```

## 错误处理

- 脚本失败时，AI查看错误信息，修复后重试
- Serper API限流（429）时，等待10秒重试
- Playwright超时（30s）时，改用requests+BS4 fallback
- 所有脚本都有try/except，不会因为一个词失败而中断整个流水线

## 扩展新脚本

需要新功能时，在scripts/seo_toolkit/下添加新脚本，遵循：
1. 命令行参数用argparse
2. 输出到iteration_center/或public/
3. 能写state.json的自动写
4. 有明确的成功/失败退出码
