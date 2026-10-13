# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import urllib.request
import os, re
from collections import Counter

url = "https://futurepedia.io/sitemap.xml"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=30)
xml_content = resp.read().decode("utf-8")

root = ET.fromstring(xml_content)
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [loc.text for loc in root.findall(".//ns:loc", ns)]

# 所有 /ai-tools/ 开头的 URL
ai_tool_urls = [u for u in urls if "/ai-tools/" in u]
print(f"ai-tools URLs: {len(ai_tool_urls)}")

# 提取第二段路径（分类名）
categories = []
for u in ai_tool_urls:
    m = re.search(r"/ai-tools/([^/]+)", u)
    if m:
        categories.append(m.group(1))

cat_counts = Counter(categories)
print(f"Unique categories: {len(cat_counts)}")
print("\nAll categories:")
for cat, c in cat_counts.most_common():
    print(f"  {cat}: {c}")

# 保存
with open(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\futurepedia_categories_full.txt", "w", encoding="utf-8") as f:
    for cat, c in cat_counts.most_common():
        f.write(f"{cat}\t{c}\n")
