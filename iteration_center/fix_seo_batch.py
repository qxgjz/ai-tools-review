"""Batch SEO fixes:
1. Differentiate chatgpt-vs-claude duplicate meta descriptions
2. Fix short titles on /contact, /privacy, /terms
"""
import json
import os

PROJ = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# === 1. Fix chatgpt-vs-claude duplicate meta ===
with open(f"{PROJ}\\data\\posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

for p in posts:
    if p["slug"] == "chatgpt-vs-claude-2026":
        # This is the shorter/older post - differentiate excerpt
        p["excerpt"] = "Quick verdict: GPT-4o wins on speed and coding, Claude Opus 4 leads on long-context reasoning and writing. Side-by-side score breakdown inside."
        print(f"Updated excerpt for: {p['slug']}")
    elif p["slug"] == "chatgpt-vs-claude-2026-comparison":
        # This is the detailed comparison - keep as is but ensure unique
        p["excerpt"] = "Comprehensive 2026 comparison of ChatGPT GPT-5 vs Claude Opus 4. Tested across 12 categories including coding, reasoning, writing, speed, and pricing."
        print(f"Confirmed excerpt for: {p['slug']}")

with open(f"{PROJ}\\data\\posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
print("posts.json saved.")

# === 2. Fix short titles on static pages ===
# /contact
contact_path = f"{PROJ}\\app\\contact\\page.tsx"
with open(contact_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(
    'title: "Contact Us | AIToolCrux"',
    'title: "Contact AIToolCrux: Feedback, Partnership & Review Requests"'
)
with open(contact_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed /contact title")

# /privacy
privacy_path = f"{PROJ}\\app\\privacy\\page.tsx"
with open(privacy_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(
    'title: "Privacy Policy | AIToolCrux"',
    'title: "Privacy Policy: How AIToolCrux Protects Your Data"'
)
with open(privacy_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed /privacy title")

# /terms
terms_path = f"{PROJ}\\app\\terms\\page.tsx"
with open(terms_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(
    'title: "Terms of Service | AIToolCrux"',
    'title: "Terms of Service: Use Guidelines & Affiliate Disclosure"'
)
with open(terms_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed /terms title")

print("\nAll fixes applied.")
