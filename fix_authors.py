#!/usr/bin/env python3
"""批量修改作者信息为AIToolCrux Editorial Team集体署名"""

import json
import os

REPO_PATH = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
NEW_AUTHOR = "AIToolCrux Editorial Team"

def fix_posts_authors():
    """修改posts.json中的作者字段"""
    filepath = os.path.join(REPO_PATH, "data", "posts.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    old_authors = set()
    changed = 0
    
    for post in data:
        old_author = post.get("author", "")
        if old_author and old_author != NEW_AUTHOR:
            old_authors.add(old_author)
            post["author"] = NEW_AUTHOR
            changed += 1
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ posts.json: 修改了 {changed} 篇文章的作者")
    print(f"   原作者: {old_authors}")
    print(f"   新作者: {NEW_AUTHOR}")
    return changed

def check_tools_authors():
    """检查tools.json中是否有作者字段"""
    filepath = os.path.join(REPO_PATH, "data", "tools.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    author_fields = set()
    for tool in data:
        for key in tool.keys():
            if "author" in key.lower() or "reviewer" in key.lower():
                author_fields.add(key)
    
    if author_fields:
        print(f"⚠️ tools.json中发现作者相关字段: {author_fields}")
    else:
        print("✅ tools.json: 无作者字段")
    return len(author_fields)

def check_authors_page():
    """检查是否有单独的作者页面数据"""
    authors_dir = os.path.join(REPO_PATH, "data")
    for filename in os.listdir(authors_dir):
        if "author" in filename.lower():
            print(f"⚠️ 发现作者数据文件: {filename}")
    
    # 检查app/authors目录
    authors_page = os.path.join(REPO_PATH, "app", "authors")
    if os.path.exists(authors_page):
        print(f"⚠️ 发现作者页面目录: app/authors/")
        # 列出文件
        for root, dirs, files in os.walk(authors_page):
            for f in files:
                print(f"   - {os.path.relpath(os.path.join(root, f), REPO_PATH)}")

def main():
    print("=" * 60)
    print("批量修改作者信息为集体署名")
    print("=" * 60)
    
    print("\n1. 修改posts.json作者字段...")
    fix_posts_authors()
    
    print("\n2. 检查tools.json作者字段...")
    check_tools_authors()
    
    print("\n3. 检查作者页面...")
    check_authors_page()
    
    print("\n" + "=" * 60)
    print("✅ 作者信息修改完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
