# GA4 AI 引流渠道 Regex 配置 · 2026-10-28（r37）

> 来源：r36 学习（GA4 原生 AI Assistant 行会漏计；Editorialge/NeuralAdX 方法论）。待 GA4 UI 可访问时应用（当前代理故障）。

## 自定义渠道组（GA4 Admin → Data settings → Channel groups）
### 渠道名：AI Assistants（置于 Organic Search 之前匹配）

**默认渠道组匹配规则（regex）**：
```
source matches regex (perplexity\.ai|chatgpt\.com|chat\.openai\.com|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|notion\.so|you\.com)
```

### 兜底：AI 内容工具来源（第二优先级）
```
source contains ai | medium matches regex (assistant|chatbot|llm|answer-engine)
```

## 与 GSC Generative AI 报告交叉分析口径
- GA4 AI 渠道 = **点击后到站** 的 AI 引流（转化层）
- GSC Generative AI 报告 = **AI Overviews/AI Mode 印象**（曝光层，无点击也有价值）
- 对比项：AI 访客 engagement rate vs 自然搜索访客（r36 知识点：ChatGPT 渠道 28 sessions/68% engagement = 最高质量渠道）

## 注意事项
- GA4 默认渠道组规则需复制后编辑，避免影响原生分组
- regex 匹配大小写不敏感，源名统一小写
- 应用后观察 7 天，对照 Ahrefs Web Analytics 的 ai-assistant 行验证覆盖
