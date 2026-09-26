# P1-MONETIZE-003 邮件捕获 Lead Magnet 设计方案

> 窗口6负责设计，窗口1负责实现。本文件是设计规范，窗口1按此实现。

## 目标
把现有简单订阅框（"Get 5 Free AI Tools Every Week"）升级为 **Lead Magnet 模式**：用高价值免费资源交换邮箱，提升订阅转化率。案例中邮件列表驱动 20% 联盟点击，我们目前为 0。

## Lead Magnet 选题
**"100+ Free AI Prompts Library"**（100+ 免费 AI 提示词库）
- 格式：PDF 或 Notion 模板链接
- 内容：按场景分类的 100+ 高质量 prompt（写作/编程/图像/营销/研究/SEO）
- 交付：订阅成功后页面显示下载链接 + 邮件发送下载链接

## 新增组件 variant: `"lead-magnet"`

在现有 `components/monetization/NewsletterSignup.tsx` 中新增第三个 variant，不破坏现有 `default` 和 `compact`。

### 桌面端布局（左右两栏）
```
┌─────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────────────────────────┐ │
│  │              │  │  Get the Free AI Prompt Library  │ │
│  │  [PDF封面    │  │  100+ battle-tested prompts for  │ │
│  │   预览卡]    │  │  ChatGPT, Claude, Midjourney —   │ │
│  │              │  │  free, instant download          │ │
│  │  100+ AI     │  │                                  │ │
│  │  Prompts     │  │  [your@email.com]  [Get Free     │ │
│  │  Library     │  │                     Access →]    │ │
│  │              │  │                                  │ │
│  │  📄 PDF      │  │  No credit card · Instant       │ │
│  │  12 pages    │  │  delivery · Unsubscribe anytime │ │
│  └──────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 移动端布局（上下堆叠）
```
┌──────────────────────────┐
│  Get the Free AI Prompt  │
│  Library                 │
│  100+ battle-tested...   │
│                          │
│  [your@email.com]        │
│  [Get Free Access →]     │
│                          │
│  No credit card · ...    │
└──────────────────────────┘
```
（PDF封面在移动端隐藏或缩小为图标）

## 样式规范

### 容器
- `bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30`
- `rounded-2xl p-6 sm:p-8 border border-emerald-100 dark:border-emerald-900`
- 桌面端：`grid grid-cols-1 sm:grid-cols-5 gap-6 items-center`
- 左栏（PDF封面）：`sm:col-span-2`
- 右栏（表单）：`sm:col-span-3`

### PDF 封面卡片（左栏）
- `relative bg-emerald-600 rounded-xl p-6 aspect-[3/4] shadow-lg overflow-hidden`
- 装饰：顶部 `bg-emerald-700 h-2 w-full` 模拟书脊
- 内容居中：
  - 大标题 `text-white text-xl font-bold`："100+ AI Prompts"
  - 副标题 `text-emerald-100 text-sm`："Free Library"
  - 底部 `text-emerald-200 text-xs`："📄 PDF · 12 pages · Updated 2026"
- 移动端：`hidden sm:block`（或缩小为 `w-20 h-28` 图标）

### 右栏文案
- 标题 `text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-2`：
  **"Get the Free AI Prompt Library"**
- 副文案 `text-gray-600 dark:text-gray-300 text-sm mb-5`：
  **"100+ battle-tested prompts for ChatGPT, Claude, Midjourney — free, instant download."**

### 表单
- 容器：`flex flex-col sm:flex-row gap-3`
- 邮箱输入框：
  - `flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600`
  - `bg-white dark:bg-gray-800 text-gray-900 dark:text-white`
  - `focus:outline-none focus:ring-2 focus:ring-emerald-500`
  - `placeholder="Enter your email"`
  - `type="email" required`
- CTA 按钮：
  - `px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold`
  - `inline-flex items-center justify-center gap-2 transition-colors`
  - `disabled:opacity-60`（loading 时）
  - 文案：**"Get Free Access"** + `ArrowRight` 图标
  - loading：spinner + "Sending..."

### 信任信号（表单下方）
- `text-xs text-gray-500 dark:text-gray-400 mt-3`
- 文案：**"No credit card required · Instant delivery · Unsubscribe anytime"**
- 用 `·` 分隔，不用 emoji

### 成功状态
- 替换整个表单区域：
  ```
  ┌─────────────────────────────────────────────┐
  │  ✓ You're in! Your free prompt library is   │
  │  ready.                                     │
  │                                             │
  │  [Download Now (PDF)]                       │
  │                                             │
  │  We also emailed you the link.              │
  └─────────────────────────────────────────────┘
  ```
- 绿色背景 `bg-green-100 dark:bg-green-900/30`
- 下载按钮：emerald-600 实心，链接到 lead magnet 资源（窗口1配置）

### 错误状态
- `text-red-600 dark:text-red-400 text-sm mt-2`
- 文案："Please enter a valid email address."

## 交互流程
1. 用户输入邮箱 → 点击 "Get Free Access"
2. 前端校验邮箱格式（含 @）
3. 调用 Email Octopus API（现有 `handleSubmit` 逻辑）
4. loading 状态：按钮 spinner + "Sending..."
5. 成功：显示成功状态 + 下载链接
6. 失败：显示错误提示

## 放置位置（窗口1实现时挂载）

| 位置 | variant | 说明 |
|------|---------|------|
| 首页 hero 下方 / Quick Answer 旁 | `lead-magnet` | 最高曝光，替换或补充现有 default |
| 博客文章末尾 | `lead-magnet` | 替换现有 compact |
| 工具详情页 Final Verdict 下方 | `lead-magnet` | 高意向用户 |

## 窗口1需要实现的部分
1. **创建 lead magnet 资源**：100+ AI prompts PDF（或 Notion 模板），上传到可公开访问的 URL
2. **配置下载链接**：在组件中加 `DOWNLOAD_URL` 常量，成功状态显示该链接
3. **新增 variant**：在 NewsletterSignup.tsx 中加 `"lead-magnet"` variant
4. **挂载**：按上表替换现有 default/compact 为 lead-magnet
5. **Email Octopus 确认**：确认 `NEXT_PUBLIC_EO_LIST_ID` 和 `NEXT_PUBLIC_EO_API_KEY` 环境变量已配置（现有组件已在用）
6. **可选：自动回复邮件**：在 Email Octopus 中设置自动回复，发送下载链接

## 与现有组件的兼容性
- 新增 variant，**不修改**现有 `default` 和 `compact` 的代码
- 现有 API 调用逻辑（Email Octopus）复用
- 现有 loading spinner 复用
- 现有错误处理复用

## 设计依据
- **Lead Magnet 转化率**：行业基准 5-15%（普通订阅框 1-3%），高价值资源交换显著提升
- **邮件驱动联盟点击**：案例站 20% 联盟点击来自邮件列表
- **信任信号位置**：Baymard Institute 研究表明"无信用卡/即时交付/随时退订"三项可降低 30% 表单焦虑
- **CTA 文案**："Get Free Access" 比 "Subscribe" 转化率高 20-40%（第一人称+价值导向）
- **左右布局**：资源预览图提供视觉锚点，提升可信度和点击率
