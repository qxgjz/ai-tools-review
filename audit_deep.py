"""Deep check: parse HTML content, check FAQ structure, images, sections."""
import json
import re
from pathlib import Path
from html.parser import HTMLParser

POSTS = Path(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\data\posts.json")
with open(POSTS, "r", encoding="utf-8") as f:
    posts = json.load(f)

n = len(posts)
idxs = [int(i * n / 10) for i in range(10)]
sample = [posts[i] for i in idxs]

class HParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.h2 = 0; self.h3 = 0
        self.imgs = 0; self.img_alts = 0
        self.headings = []
    def handle_starttag(self, tag, attrs):
        if tag == "h1": self.h1 += 1
        elif tag == "h2": self.h2 += 1
        elif tag == "h3": self.h3 += 1
        elif tag == "img":
            self.imgs += 1
            d = dict(attrs)
            if d.get("alt"): self.img_alts += 1

# Check FAQ structure on one post with faqs
print("=== FAQ structure sample (post 6) ===")
p6 = sample[6]
print("faqs raw:", json.dumps(p6.get("faqs", []), indent=2)[:500])

print("\n=== Content tags sample (post 6, first 1000 chars) ===")
print(p6.get("content", "")[:1000])

print("\n=== Per-post audit ===")
for i, p in enumerate(sample):
    content = p.get("content", "") or ""
    hp = HParser(); hp.feed(content)
    faqs = p.get("faqs", []) or []
    # Check FAQ field names
    faq_keys = set()
    for f in faqs[:2]:
        faq_keys.update(f.keys())
    # Check sections
    has_faq_section = bool(re.search(r"(?i)(<h2[^>]*>[^<]*faq|frequently asked)", content))
    has_pros = bool(re.search(r"(?i)(pros|good about|what we like)", content[:5000]))
    has_cons = bool(re.search(r"(?i)(cons|bad about|what we dislike|drawback)", content[:5000]))
    has_verdict = bool(re.search(r"(?i)(verdict|final thoughts|conclusion|bottom line)", content[-3000:]))
    # Word count (strip tags)
    text = re.sub(r"<[^>]+>", " ", content)
    words = len(re.findall(r"\b\w+\b", text))
    print(f"[{i}] {p.get('slug','?')[:50]}")
    print(f"    h1={hp.h1} h2={hp.h2} h3={hp.h3} imgs={hp.imgs}(alt={hp.img_alts}) words={words}")
    print(f"    faqs={len(faqs)} keys={faq_keys} faq_section={has_faq_section}")
    print(f"    pros={has_pros} cons={has_cons} verdict={has_verdict}")
