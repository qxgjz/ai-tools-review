#!/usr/bin/env python3
"""
批量修复页面title中的重复品牌名问题
layout.tsx中的template是 "%s | AIToolCrux"，所以页面title不应再包含 " | AIToolCrux"
"""

import os
import re

def fix_title_in_file(filepath):
    """修复单个文件中的title重复问题"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return 0
    
    original_content = content
    fixes = 0
    
    # 模式1: title: "XXX | AIToolCrux"  -> title: "XXX"
    # 但要排除 layout.tsx 中的 default title（那个是完整的，不会经过template）
    if 'layout.tsx' not in filepath:
        # 修复 export const metadata 中的 title
        pattern1 = r'(title:\s*")([^"|]+\s*\|\s*AIToolCrux)(")'
        def repl1(m):
            nonlocal fixes
            full_title = m.group(2)
            # 去掉末尾的 " | AIToolCrux"
            clean_title = re.sub(r'\s*\|\s*AIToolCrux\s*$', '', full_title)
            fixes += 1
            return m.group(1) + clean_title + m.group(3)
        
        content = re.sub(pattern1, repl1, content)
        
        # 模式2: title: `XXX | AIToolCrux` (模板字符串)
        pattern2 = r'(title:\s*`)([^`|]+\s*\|\s*AIToolCrux)(`)'
        def repl2(m):
            nonlocal fixes
            full_title = m.group(2)
            clean_title = re.sub(r'\s*\|\s*AIToolCrux\s*$', '', full_title)
            fixes += 1
            return m.group(1) + clean_title + m.group(3)
        
        content = re.sub(pattern2, repl2, content)
    
    # 写回文件
    if fixes > 0 and content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ 修复 {fixes} 处")
        except Exception as e:
            print(f"  ❌ 写回失败: {e}")
    else:
        print(f"  ✅ 无需修复")
    
    return fixes

def main():
    base_dir = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app"
    
    # 收集所有tsx/ts文件
    files_to_fix = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.tsx', '.ts')) and 'layout.tsx' not in file:
                files_to_fix.append(os.path.join(root, file))
    
    print(f"找到 {len(files_to_fix)} 个待检查文件")
    
    total = 0
    for filepath in sorted(files_to_fix):
        rel_path = os.path.relpath(filepath, base_dir)
        print(f"\n处理: {rel_path}")
        total += fix_title_in_file(filepath)
    
    print(f"\n{'='*60}")
    print(f"处理完成！共修复 {total} 处title重复")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
