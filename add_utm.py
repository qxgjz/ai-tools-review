"""
Add UTM parameters to all affiliate links:
1. tools.json - affiliateUrl field
2. posts.json - content field affiliate links

UTM: ?utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={slug}
"""
import json, re
from pathlib import Path

BASE = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\data")

# === 1. tools.json ===
tools_path = BASE / "tools.json"
tools = json.loads(tools_path.read_text(encoding="utf-8"))

utm_seen_tools = 0
for t in tools:
    url = t.get("affiliateUrl", "")
    if not url:
        continue
    if "utm_source=aitoolcrux" in url:
        continue  # already has UTM
    # Determine separator
    sep = "&" if "?" in url else "?"
    slug = t.get("slug", "unknown")
    utm = f"{sep}utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={slug}"
    t["affiliateUrl"] = url + utm
    utm_seen_tools += 1
    print(f"  tools.json: {slug} -> {t['affiliateUrl']}")

tools_path.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ tools.json: {utm_seen_tools} links updated")

# === 2. posts.json ===
posts_path = BASE / "posts.json"
posts = json.loads(posts_path.read_text(encoding="utf-8"))

utm_seen_posts = 0
utm_link_count = [0]

for post in posts:
    slug = post.get("slug", "unknown")
    content = post.get("content", "")
    if not content:
        continue
    
    # Find external links in content (not aitoolcrux/internal links)
    # Match href="URL" or markdown links [text](URL)
    # We need to identify affiliate links - typically they have ref=, affiliate, partner, etc.
    # Or they go to known AI tool domains
    
    original = content
    
    # Pattern 1: Markdown links [text](url)
    def replace_md(m):
        text = m.group(1)
        url = m.group(2)
        # Skip internal links and non-affiliate
        if "aitoolcrux.com" in url:
            return m.group(0)
        if url.startswith("/"):
            return m.group(0)
        if "utm_source=aitoolcrux" in url:
            return m.group(0)
        # Only tag links that look like affiliate (have ref=, affiliate, partner tracking)
        # OR links to known tool domains
        if not any(kw in url.lower() for kw in ["ref=", "affiliate", "partner", "?ref", "utm_medium=affiliate"]):
            # Also tag links to known AI tool domains
            known_domains = ["try.elevenlabs.io", "midjourney", "notion.so", "canva.com", 
                           "jasper", "writesonic", "suno", "runway", "perplexity",
                           "elevenlabs", "cursor", "anthropic", "openai"]
            if not any(d in url.lower() for d in known_domains):
                return m.group(0)
        
        sep = "&" if "?" in url else "?"
        new_url = f"{url}{sep}utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={slug}"
        utm_link_count[0] += 1
        return f"[{text}]({new_url})"
    
    content = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', replace_md, content)
    
    # Pattern 2: HTML links <a href="url">
    def replace_html(m):
        url = m.group(1)
        if "aitoolcrux.com" in url or url.startswith("/"):
            return m.group(0)
        if "utm_source=aitoolcrux" in url:
            return m.group(0)
        if not any(kw in url.lower() for kw in ["ref=", "affiliate", "partner", "?ref"]):
            return m.group(0)
        sep = "&" if "?" in url else "?"
        new_url = f"{url}{sep}utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={slug}"
        utm_link_count[0] += 1
        return f'href="{new_url}"'
    
    content = re.sub(r'href="(https?://[^"]+)"', replace_html, content)
    
    if content != original:
        post["content"] = content
        utm_seen_posts += 1

posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ posts.json: {utm_seen_posts} posts updated, {utm_link_count[0]} links tagged")
print("\nDone.")
