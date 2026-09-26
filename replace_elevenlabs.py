"""Replace all ElevenLabs direct links with PartnerStack affiliate link."""
import json, re
from pathlib import Path

p = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\data\posts.json")
posts = json.loads(p.read_text(encoding="utf-8"))

EL_LINK = "https://try.elevenlabs.io/e45ubw2ct0ag"
replaced = [0]
affected_posts = []

for post in posts:
    slug = post.get("slug", "unknown")
    content = post.get("content", "")
    if not content:
        continue
    if "elevenlabs" not in content.lower():
        continue
    
    original = content
    
    # Replace markdown links to elevenlabs.io with PartnerStack link
    # Match [text](https://elevenlabs.io...any)
    def replace_el(m):
        text = m.group(1)
        utm = f"utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={slug}"
        new_url = f"{EL_LINK}?{utm}"
        replaced[0] += 1
        return f"[{text}]({new_url})"
    
    # Match any elevenlabs.io link (with or without existing query)
    content = re.sub(
        r'\[([^\]]+)\]\(https?://(?:www\.)?elevenlabs\.io[^)]*\)',
        replace_el,
        content,
        flags=re.IGNORECASE
    )
    
    # Also replace HTML href links
    def replace_html(m):
        utm = f"utm_source=aitoolcrux&utm_medium=affiliate&utm_campaign=review&utm_content={slug}"
        replaced[0] += 1
        return f'href="{EL_LINK}?{utm}"'
    
    content = re.sub(
        r'href="https?://(?:www\.)?elevenlabs\.io[^"]*"',
        replace_html,
        content,
        flags=re.IGNORECASE
    )
    
    if content != original:
        post["content"] = content
        affected_posts.append(slug)

p.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ Replaced {replaced[0]} ElevenLabs links in {len(affected_posts)} posts")
for s in affected_posts:
    print(f"  - {s}")
