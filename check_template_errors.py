#!/usr/bin/env python3
"""检查posts.json和tools.json中是否有模板变量错误"""

import json
import os

base_dir = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

def check_posts():
    print("=" * 60)
    print("检查 posts.json 中的模板变量错误")
    print("=" * 60)
    
    filepath = os.path.join(base_dir, 'data', 'posts.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    error_patterns = ['undefined', 'NaN', '[object Object]', 'null']
    errors = []
    
    for post in data:
        slug = post.get('slug', 'unknown')
        content = post.get('content', '')
        
        for i, line in enumerate(content.split('\n')):
            # 跳过正常的null字段引用
            if any(pattern in line for pattern in error_patterns):
                # 检查是否是内容中的真实错误（不是代码示例）
                if not line.strip().startswith('```') and 'coverImage' not in line:
                    errors.append((slug, i, line.strip()[:120]))
    
    print(f"找到 {len(errors)} 个潜在模板变量错误")
    for slug, line_num, line in errors[:30]:
        print(f"  [{slug}] 行{line_num}: {line}")
    
    return len(errors)

def check_tools():
    print("\n" + "=" * 60)
    print("检查 tools.json 中的模板变量错误")
    print("=" * 60)
    
    filepath = os.path.join(base_dir, 'data', 'tools.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    error_patterns = ['undefined', 'NaN', '[object Object]']
    errors = []
    
    for i, tool in enumerate(data):
        slug = tool.get('slug', f'unknown-{i}')
        name = tool.get('name', 'unknown')
        
        # 检查所有字符串字段
        for key, value in tool.items():
            if isinstance(value, str):
                if any(pattern in value for pattern in error_patterns):
                    errors.append((slug, key, value[:100]))
    
    print(f"找到 {len(errors)} 个潜在模板变量错误")
    for slug, key, value in errors[:30]:
        print(f"  [{slug}] {key}: {value}")
    
    return len(errors)

def check_chinese_punctuation():
    print("\n" + "=" * 60)
    print("验证中文全角标点是否已全部修复")
    print("=" * 60)
    
    chinese_punct = ['：', '，', '。', '；', '？', '！', '（', '）', '【', '】']
    
    for filename in ['posts.json', 'tools.json']:
        filepath = os.path.join(base_dir, 'data', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        total = 0
        for punct in chinese_punct:
            count = content.count(punct)
            if count > 0:
                print(f"  {filename}: 仍有 {count} 个 '{punct}'")
                total += count
        
        if total == 0:
            print(f"  {filename}: ✅ 无中文全角标点")
    
    return total

if __name__ == '__main__':
    post_errors = check_posts()
    tool_errors = check_tools()
    chinese_remaining = check_chinese_punctuation()
    
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    print(f"  posts.json 模板错误: {post_errors}")
    print(f"  tools.json 模板错误: {tool_errors}")
    print(f"  剩余中文全角标点: {chinese_remaining}")
