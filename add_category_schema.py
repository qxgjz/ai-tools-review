#!/usr/bin/env python3
"""为分类页添加CollectionPage+ItemList结构化数据，并修复标题缺少空格的问题"""

import os

filepath = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\category\[slug]\page.tsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在return的div后面插入结构化数据
old_div = '''  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/"'''

new_div = '''  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* CollectionPage + ItemList structured data for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            name: `Best ${category.name} AI Tools 2026`,
            description: category.description,
            url: `https://www.aitoolcrux.com/category/${params.slug}`,
            isPartOf: {
              "@type": "WebSite",
              name: "AIToolCrux",
              url: "https://www.aitoolcrux.com",
            },
            mainEntity: {
              "@type": "ItemList",
              itemListElement: sortedTools.slice(0, 10).map((tool, index) => ({
                "@type": "ListItem",
                position: index + 1,
                item: {
                  "@type": "SoftwareApplication",
                  name: tool.name,
                  url: `https://www.aitoolcrux.com/tools/${tool.slug}`,
                  applicationCategory: "AIApplication",
                  operatingSystem: "Web",
                  aggregateRating: {
                    "@type": "AggregateRating",
                    ratingValue: calculateScoreResult(tool.scores).total.toFixed(1),
                    bestRating: "10",
                    worstRating: "0",
                    reviewCount: 1,
                  },
                },
              })),
            },
          }),
        }}
      />
      <Link href="/"'''

if old_div in content:
    content = content.replace(old_div, new_div)
    print("✅ 已插入CollectionPage+ItemList结构化数据")
else:
    print("❌ 未找到插入位置，检查文件内容")
    # 打印附近内容帮助调试
    idx = content.find('return (')
    if idx > 0:
        print("附近内容:")
        print(repr(content[idx:idx+200]))

# 2. 修复标题缺少空格的问题
# {category.name}Complete Guide -> {category.name} Complete Guide
old_title1 = '{category.name}Complete Guide'
new_title1 = '{category.name} Complete Guide'
if old_title1 in content:
    content = content.replace(old_title1, new_title1)
    print("✅ 已修复标题1: Complete Guide缺少空格")

# How to Choose the Right{category.name} -> How to Choose the Right {category.name}
old_title2 = 'How to Choose the Right{category.name}'
new_title2 = 'How to Choose the Right {category.name}'
if old_title2 in content:
    content = content.replace(old_title2, new_title2)
    print("✅ 已修复标题2: Right缺少空格")

# 写回文件
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 文件已更新")
