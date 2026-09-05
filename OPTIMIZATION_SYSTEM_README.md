# 网站优化自动化提示词体系

一套完整的网站优化自动化系统，包含13个专业模块的提示词、JSON输出规范、GitHub Actions每周自动诊断工作流和AI自动执行优化功能。

## 📋 目录结构

```
website-optimization-prompts/
├── prompts/                          # 提示词文件
│   ├── output-schema.json           # JSON输出格式规范
│   ├── 00-orchestrator.json         # 总控提示词
│   ├── 01-crawlability.json         # 可抓取性优化
│   ├── 02-renderability.json        # 可渲染性优化
│   ├── 03-indexability.json         # 可索引性优化
│   ├── 04-core_web_vitals.json      # Core Web Vitals优化
│   ├── 05-tool_page_content.json    # 工具页内容优化
│   ├── 06-article_page_content.json # 文章页内容优化
│   ├── 07-category_page_content.json # 分类页内容优化
│   ├── 08-eeat.json                 # E-E-A-T强化
│   ├── 09-structured_data.json      # 结构化数据优化
│   ├── 10-internal_linking.json     # 内链优化
│   ├── 11-link_building.json        # 外链建设
│   └── 12-conversion_rate.json      # 转化率优化
├── .github/
│   ├── workflows/
│   │   ├── weekly-diagnosis.yml     # 每周自动诊断工作流
│   │   └── auto-optimize.yml        # 自动执行优化工作流
│   └── scripts/
│       ├── run_diagnosis.py          # 运行诊断脚本（调用豆包API）
│       ├── generate_summary.py       # 生成摘要报告脚本
│       ├── create_p0_issues.py       # 创建P0 Issue脚本
│       └── execute_optimizations.py  # 执行优化脚本
├── reports/                          # 诊断报告输出目录
├── optimizations/                    # 优化执行日志目录
└── README.md                         # 说明文档
```

## 🎯 提示词模块说明

### 总控模块
- **orchestrator**: 网站优化总监，全面诊断网站，调度12个子模块，输出整体优化方案

### 技术模块（4个）
1. **crawlability**: 可抓取性优化（robots.txt、sitemap、服务器响应、抓取预算）
2. **renderability**: 可渲染性优化（SSR/SSG/ISR、JavaScript渲染、hydration）
3. **indexability**: 可索引性优化（meta robots、canonical、重复内容、404处理）
4. **core_web_vitals**: Core Web Vitals优化（LCP、CLS、INP、资源加载）

### 内容模块（3个）
5. **tool_page_content**: 工具页内容优化（533个工具评测页）
6. **article_page_content**: 文章页内容优化（47篇文章）
7. **category_page_content**: 分类页内容优化（18个分类页）

### 其他模块（5个）
8. **eeat**: E-E-A-T强化（经验、专业、权威、可信）
9. **structured_data**: 结构化数据优化（Schema.org、富摘要）
10. **internal_linking**: 内链优化（网站架构、主题聚类、权重传递）
11. **link_building**: 外链建设（白帽外链策略、目录提交、客座文章）
12. **conversion_rate**: 转化率优化（联盟链接、CTA、信任信号、A/B测试）

## 📊 JSON输出格式

所有提示词的输出必须严格遵循 `prompts/output-schema.json` 定义的JSON格式，包含：

- `report_id`: 报告唯一ID
- `generated_at`: 生成时间
- `website_url`: 网站URL
- `module`: 诊断模块
- `summary`: 摘要（健康度评分、最致命问题、最值钱机会、合规状态）
- `issues`: 问题清单（每个问题包含id、标题、严重程度、优先级、证据、修复方案、代码修改）
- `action_plan`: 执行计划（P0/P1/P2任务）
- `expected_results`: 预期效果（短期/中期KPI）
- `verification`: 验证方法
- `pending_verification`: 待核实清单
- `compliance_check`: 合规检查结果

## 🚀 GitHub Actions工作流

### 1. 每周自动诊断（weekly-diagnosis.yml）

**触发方式**:
- 每周一早上8点（UTC）自动运行
- 支持手动触发

**执行流程**:
1. 并行运行13个模块的诊断（最多4个并行）
2. 每个模块调用豆包API进行诊断
3. 输出JSON格式的诊断报告
4. 汇总所有报告，生成Markdown摘要
5. 提交报告到仓库
6. 为P0问题自动创建GitHub Issue

### 2. 自动执行优化（auto-optimize.yml）

**触发方式**:
- 每周诊断工作流完成后自动触发
- 支持手动触发（可指定模块和优先级）

**执行流程**:
1. 获取最新的诊断报告
2. 提取P0优先级的优化项
3. 根据报告中的代码修改建议自动执行
4. 创建优化分支
5. 自动创建Pull Request
6. 等待人工审核和合并
7. Vercel自动部署

## 🔧 配置说明

### GitHub Secrets配置

在GitHub仓库的Settings → Secrets and variables → Actions中添加以下Secrets：

| Secret名称 | 说明 | 示例 |
|-----------|------|------|
| `DOUBAO_API_KEY` | 豆包API Key | `ark-xxxxxxxxxx` |
| `DOUBAO_ENDPOINT_ID` | 豆包Endpoint ID | `ep-xxxxxxxxxx` |

### 本地测试

```bash
# 安装依赖
pip install requests httpx python-dotenv

# 设置环境变量
export DOUBAO_API_KEY="your-api-key"
export DOUBAO_ENDPOINT_ID="your-endpoint-id"

# 运行单个模块诊断
python .github/scripts/run_diagnosis.py \
  --module crawlability \
  --prompt-file prompts/01-crawlability.json \
  --output-dir reports/2026-09-05 \
  --website-url https://www.aitoolcrux.com

# 生成摘要报告
python .github/scripts/generate_summary.py \
  --reports-dir reports/2026-09-05 \
  --output reports/2026-09-05/SUMMARY.md
```

## 📈 工作原理

### 诊断流程

```
GitHub Actions触发
    ↓
加载提示词文件
    ↓
调用豆包API（云端运行，可访问Google）
    ↓
AI根据提示词对网站进行全面诊断
    ↓
输出严格JSON格式的诊断报告
    ↓
验证报告格式
    ↓
保存报告到reports/目录
```

### 优化执行流程

```
诊断完成
    ↓
提取P0问题
    ↓
分析代码修改建议
    ↓
备份原文件
    ↓
自动应用代码修改
    ↓
创建优化分支
    ↓
创建Pull Request
    ↓
人工审核
    ↓
合并到main分支
    ↓
Vercel自动部署
```

## ⚠️ 注意事项

1. **AI输出验证**: AI生成的代码修改建议需要人工审核后再合并
2. **回滚机制**: 所有文件修改前都会自动备份，可随时回滚
3. **API限流**: 豆包API有调用频率限制，工作流中已设置最多4个并行
4. **数据隐私**: 不要在提示词中包含敏感信息（密码、密钥等）
5. **合规性**: 所有优化建议必须符合Google搜索中心官方规范，禁止黑帽技术

## 📝 自定义扩展

### 添加新的提示词模块

1. 在 `prompts/` 目录创建新的JSON文件，格式参考现有模块
2. 在 `weekly-diagnosis.yml` 的 `strategy.matrix.module` 中添加新模块
3. 在 `generate_summary.py` 的 `module_names` 字典中添加模块名称

### 修改诊断频率

编辑 `weekly-diagnosis.yml` 中的 `schedule.cron` 表达式：
- 每周一: `0 8 * * 1`
- 每天: `0 8 * * *`
- 每小时: `0 * * * *`

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。
