# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import urllib.request
import os, re
from collections import Counter

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# 抓 futurepedia sitemap
url = "https://futurepedia.io/sitemap.xml"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=30)
xml_content = resp.read().decode("utf-8")

root = ET.fromstring(xml_content)
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [loc.text for loc in root.findall(".//ns:loc", ns)]

# 提取分类路径（ai-tools/xxx/best 模式）
categories = []
for u in urls:
    m = re.search(r"/ai-tools/([^/]+)/(best|alternatives|vs)$", u)
    if m:
        categories.append(m.group(1))

cat_counts = Counter(categories)
print(f"Tool categories: {len(cat_counts)}")
print("\nTop 30 categories:")
for cat, c in cat_counts.most_common(30):
    print(f"  {cat}: {c} pages")

# 提取所有 URL 模式（路径结构）
patterns = []
for u in urls:
    path = u.replace("https://futurepedia.io", "").rstrip("/")
    # 把具体工具名替换成 {tool}
    pattern = re.sub(r"/ai-tools/[^/]+/[^/]+$", "/ai-tools/{category}/{type}", path)
    pattern = re.sub(r"/ai-tools/[^/]+$", "/ai-tools/{category}", pattern)
    patterns.append(pattern)

pattern_counts = Counter(patterns)
print(f"\nURL patterns: {len(pattern_counts)}")
print("\nAll patterns:")
for p, c in pattern_counts.most_common(20):
    print(f"  {p}: {c}")

# 保存分类列表
with open(os.path.join(BASE, "iteration_center", "futurepedia_categories.txt"), "w", encoding="utf-8") as f:
    for cat, c in cat_counts.most_common():
        f.write(f"{cat}\t{c}\n")

print(f"\nSaved to futurepedia_categories.txt")
