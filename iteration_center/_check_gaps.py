"""Round 7: Check coverage gaps and mine new keywords"""
import os, json, glob

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

# List existing briefs
briefs = sorted(glob.glob("iteration_center/content_briefs/*_input.md"))
print(f"=== Existing briefs ({len(briefs)}) ===")
for b in briefs:
    print(f"  {os.path.basename(b)}")

# List existing posts slugs
with open("data/posts.json","r",encoding="utf-8") as f:
    posts = json.load(f)
slugs = [p.get("slug","") for p in posts]
print(f"\n=== Existing posts ({len(slugs)}) ===")
for s in sorted(slugs):
    print(f"  {s}")
