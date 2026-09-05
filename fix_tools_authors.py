#!/usr/bin/env python3
"""修改tools.json中的作者字段为AIToolCrux Editorial Team集体署名"""

import json
import os

REPO_PATH = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
NEW_AUTHOR_NAME = "AIToolCrux Editorial Team"
NEW_AUTHOR_ROLE = "Independent AI Tool Review Team"
NEW_AUTHOR_BIO = "The AIToolCrux Editorial Team is a group of independent AI tool reviewers with collective experience testing and evaluating artificial intelligence software. Our team has tested over 500 AI tools across categories including chatbots, content generators, code assistants, and creative tools. We follow a transparent six-dimensional evaluation methodology and do not accept payment for higher ratings."

def fix_tools_authors():
    """修改tools.json中的作者字段"""
    filepath = os.path.join(REPO_PATH, "data", "tools.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    changed_author = 0
    changed_review_author = 0
    
    for tool in data:
        # 修改author对象
        if "author" in tool and tool["author"]:
            if isinstance(tool["author"], dict):
                old_name = tool["author"].get("name", "")
                if old_name != NEW_AUTHOR_NAME:
                    tool["author"]["name"] = NEW_AUTHOR_NAME
                    tool["author"]["role"] = NEW_AUTHOR_ROLE
                    tool["author"]["bio"] = NEW_AUTHOR_BIO
                    # 移除可能存在的虚构信息
                    for key in ["avatar", "expertise", "education", "experience"]:
                        if key in tool["author"]:
                            del tool["author"][key]
                    changed_author += 1
            elif isinstance(tool["author"], str):
                if tool["author"] != NEW_AUTHOR_NAME:
                    tool["author"] = {
                        "name": NEW_AUTHOR_NAME,
                        "role": NEW_AUTHOR_ROLE,
                        "bio": NEW_AUTHOR_BIO
                    }
                    changed_author += 1
        
        # 修改review_author字段
        if "review_author" in tool and tool["review_author"]:
            if tool["review_author"] != NEW_AUTHOR_NAME:
                tool["review_author"] = NEW_AUTHOR_NAME
                changed_review_author += 1
        
        # 修改reviewer字段（如果存在）
        if "reviewer" in tool and tool["reviewer"]:
            if isinstance(tool["reviewer"], str) and tool["reviewer"] != NEW_AUTHOR_NAME:
                tool["reviewer"] = NEW_AUTHOR_NAME
            elif isinstance(tool["reviewer"], dict):
                tool["reviewer"]["name"] = NEW_AUTHOR_NAME
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ tools.json:")
    print(f"   修改了 {changed_author} 个工具的author对象")
    print(f"   修改了 {changed_review_author} 个工具的review_author字段")
    return changed_author + changed_review_author

def main():
    print("=" * 60)
    print("修改tools.json作者字段为集体署名")
    print("=" * 60)
    
    fix_tools_authors()
    
    print("\n" + "=" * 60)
    print("✅ tools.json作者信息修改完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
