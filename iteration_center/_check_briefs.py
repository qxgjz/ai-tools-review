import os, json, glob

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

# 检查已有brief
briefs = glob.glob("iteration_center/content_briefs/*.md")
print("=== 已有briefs ===")
for b in sorted(briefs):
    print(f"  {os.path.basename(b)}")

# 检查已写文章slug
with open("data/posts.json","r",encoding="utf-8") as f:
    posts = json.load(f)
existing_slugs = {p.get("slug","") for p in posts}
print(f"\n=== posts.json已有 {len(posts)} 篇 ===")

# 13个关键词任务需要的slug
needed = [
    "lovable-vs-boltnew",
    "claude-37-vs-gpt4o",
    "synthesia-vs-heygen",
    "otter-ai-alternatives",
    "runway-alternatives",
    "gemini-vs-perplexity",
    "beautiful-ai-alternatives",
    "devin-ai-review",
    "sudowrite-alternatives",
    "writesonic-alternatives",
    "motion-ai-alternatives",
    "clearscope-alternatives",
    "quillbot-alternatives",
]

print("\n=== 调研任务状态 ===")
for slug in needed:
    brief_exists = any(slug in b for b in briefs)
    post_exists = slug in existing_slugs
    status = "已发布" if post_exists else ("已有brief" if brief_exists else "需要调研")
    print(f"  {slug}: {status}")
