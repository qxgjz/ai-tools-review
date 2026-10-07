# OpenSEO 部署指南

> OpenSEO (20.5K stars) - 开源自托管SEO套件，对标Semrush（$200/月）

## 功能清单
- 关键词研究（搜索量、竞争度、CPC）
- 排名追踪（每日/每周）
- 外链分析（外链数量、质量、锚文本）
- 技术SEO审计（爬取、错误检测）
- 内容优化建议
- 竞品分析
- 多项目管理

## 部署方式

### 方式1：Docker Compose（推荐）
```bash
# 克隆仓库
git clone https://github.com/staniel0912/OpenSEO.git
cd OpenSEO

# 复制环境变量
cp .env.example .env

# 启动
docker-compose up -d

# 访问
# http://localhost:3000
```

### 方式2：本地开发
```bash
# 前端
cd frontend
npm install
npm run dev

# 后端
cd backend
pip install -r requirements.txt
python main.py
```

## 环境变量配置
```env
# 数据库
DATABASE_URL=postgresql://openseo:openseo@localhost:5432/openseo

# Redis
REDIS_URL=redis://localhost:6379

# 搜索API（二选一）
SERPAPI_KEY=your_serpapi_key
# 或
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_cse_id

# 爬虫
CRAWLER_MAX_CONCURRENT=10
CRAWLER_DELAY=1
```

## 与现有工具对比

| 功能 | OpenSEO | zens-ink | 我们现有 |
|------|---------|----------|----------|
| 关键词研究 | ✅ 完整 | ✅ 6个模块 | ✅ Serper API |
| 排名追踪 | ✅ 自动 | ✅ rank_tracker | ⚠️ 手动 |
| 外链分析 | ✅ 完整 | ❌ 不可用 | ❌ 无 |
| 技术审计 | ✅ 爬取 | ✅ site_audit | ✅ 自建脚本 |
| 内容优化 | ✅ AI建议 | ✅ content_qc | ✅ QC流水线 |
| 竞品分析 | ✅ 完整 | ✅ competitor_gap | ⚠️ 手动 |
| 部署难度 | 高（Docker） | 低（pip） | 低 |
| 资源占用 | 高（DB+Redis） | 低 | 低 |

## 建议

**当前阶段不部署OpenSEO**，原因：
1. 需要Docker + PostgreSQL + Redis，资源占用高
2. zens-ink已覆盖80%功能（关键词、审计、内容QC、竞品）
3. 我们的核心瓶颈是内容质量，不是工具数量
4. 等网站流量到1000+/天再考虑部署

**如果未来要部署**：
1. 先在本地Docker测试
2. 迁移现有关键词数据到OpenSEO
3. 用OpenSEO的外链分析功能（这是我们缺失的）
4. 保留zens-ink作为轻量补充

## 相关链接
- GitHub: https://github.com/staniel0912/OpenSEO
- 文档: https://openseo.dev/docs
- Demo: https://demo.openseo.dev
