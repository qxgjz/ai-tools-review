import json
proj = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
posts = json.load(open(proj + r"\data\posts.json", "r", encoding="utf-8-sig"))
slugs = {p["slug"] for p in posts}
for s in ["best-ai-voice-generators-2026", "best-ai-resume-builders-2026", "best-ai-pr-tools-2026"]:
    status = "EXISTS" if s in slugs else "MISSING"
    print(f"{s}: {status}")
print(f"Total posts: {len(posts)}")
# Show last 5 slugs
print("Last 5 slugs:")
for p in posts[:5]:
    print(f"  {p['slug']}")
