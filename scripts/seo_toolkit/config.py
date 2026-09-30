"""
SEO Toolkit 配置文件
所有脚本共用的路径、API key、常量
"""
import os

# 项目根目录
PROJECT_ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# 数据文件路径
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
POSTS_JSON = os.path.join(DATA_DIR, "posts.json")
TOOLS_JSON = os.path.join(DATA_DIR, "tools.json")

# 迭代中心路径
ITERATION_DIR = os.path.join(PROJECT_ROOT, "iteration_center")
STATE_JSON = os.path.join(ITERATION_DIR, "state.json")
KEYWORD_PIPELINE = os.path.join(ITERATION_DIR, "keyword_pipeline.md")
COMPETITOR_TEMPLATES = os.path.join(ITERATION_DIR, "competitor_templates.md")
CONTENT_BRIEFS_DIR = os.path.join(ITERATION_DIR, "content_briefs")
USER_PAINPOINTS_DIR = os.path.join(ITERATION_DIR, "user_painpoints")
OUTREACH_TARGETS = os.path.join(ITERATION_DIR, "outreach_targets.md")
OUTREACH_TRACKER = os.path.join(ITERATION_DIR, "outreach_tracker.md")

# 截图路径
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "public", "screenshots")

# GSC报告路径
GSC_REPORT_DIR = os.path.join(PROJECT_ROOT, "gsc-ga4-report")

# API Keys
SERPER_API_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
SERPER_API_URL = "https://google.serper.dev/search"

# Git配置
GIT_PROXY = "http://127.0.0.1:7890"

# 大品牌词列表（种子词）
SEED_KEYWORDS = [
    "ChatGPT", "Claude", "Gemini", "Midjourney", "Grammarly",
    "Cursor", "Dify", "DeepSeek", "Perplexity", "Jasper",
    "Canva AI", "Notion AI", "Copilot", "Suno", "Runway",
    "ElevenLabs", "Descript", "Otter AI", "Fireflies", "Tldraw"
]

# 文章质量标准
QUALITY_STANDARDS = {
    "min_words": 2500,
    "max_words": 4000,
    "quick_answer_min": 280,
    "quick_answer_max": 320,
    "min_key_takeaways": 3,
    "min_faq": 5,
    "min_internal_links": 3,
    "min_affiliate_links": 2,
    "min_screenshots": 3,
}
