# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import urllib.request
import os, re
from collections import Counter

# 抓 futurepedia sitemap
url = "https://futurepedia.io/sitemap.xml"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=30)
xml_content = resp.read().decode("utf-8")

# 解析所有 URL
root = ET.fromstring(xml_content)
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [loc.text for loc in root.findall(".//ns:loc", ns)]
print(f"Total URLs: {len(urls)}")

# 提取 blog/文章类 URL（排除工具页和分类页）
blog_urls = [u for u in urls if "/blog/" in u or "/resources/" in u or "/tutorials/" in u]
print(f"Blog/resource URLs: {len(blog_urls)}")

# 从 URL 提取关键词
keywords = []
for u in blog_urls:
    # 提取最后一段路径
    slug = u.rstrip("/").split("/")[-1]
    # 去掉年份和数字
    slug = re.sub(r"-20\d{2}", "", slug)
    slug = re.sub(r"\d+", "", slug)
    # 分词
    words = slug.split("-")
    words = [w for w in words if len(w) > 2]
    keywords.extend(words)

# 统计高频词
word_counts = Counter(keywords).most_common(30)
print("\nTop 30 keywords from futurepedia blog:")
for w, c in word_counts:
    print(f"  {w}: {c}")

# 提取所有 blog slug，用于对比我们已有的
blog_slugs = set()
for u in blog_urls:
    slug = u.rstrip("/").split("/")[-1]
    blog_slugs.add(slug)

print(f"\nUnique blog slugs: {len(blog_slugs)}")

# 保存到文件
with open(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\futurepedia_blog_slugs.txt", "w", encoding="utf-8") as f:
    for s in sorted(blog_slugs):
        f.write(s + "\n")

print("Saved to futurepedia_blog_slugs.txt")
