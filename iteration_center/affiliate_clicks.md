# Affiliate 点击追踪报告

> 创建：2026-09-18
> Commit: 18dd2fe

## UTM追踪方案

所有affiliate链接已加UTM参数：
```
?utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={tool_slug}
```

## 已处理链接

| 位置 | 数量 | 说明 |
|------|------|------|
| tools.json affiliateUrl | 1 | elevenlabs |
| posts.json 文章内容 | 60 | 13篇文章中的affiliate链接 |

## GA4查询方式

在GA4中查看：
1. 进入 **报告 → 流量获取 → 流量来源概览**
2. 筛选 `utm_medium = affiliate`
3. 主维度选 `utm_content`（对应tool_slug）
4. 看事件：**click** 或 **session_start**

每周五从GA4拉取以下数据：
- 每个utm_content的点击数
- Top10最被点击的工具
- 转化率（点击 → 注册/购买）

## 当前数据

| 指标 | 数值 |
|------|------|
| 已追踪链接 | 61 |
| 开始追踪日期 | 2026-09-18 |
| 首次数据拉取 | 2026-09-25（一周后） |

## 说明

- UTM参数只加在query string，不改affiliate链接本身
- 不影响PartnerStack的cookie归因（cookie是独立的）
- GA4数据有24-48小时延迟
- 新联盟接入后自动加UTM（窗口1改代码逻辑）

---

*窗口5变现运营*
