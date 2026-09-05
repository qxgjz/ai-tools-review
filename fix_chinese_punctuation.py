#!/usr/bin/env python3
"""
批量修复JSON文件中的中文全角标点符号
- 中文全角冒号： 替换为 英文半角冒号:
- 中文全角逗号，替换为 英文半角逗号,
- 中文全角句号。替换为 英文半角句号.
- 中文全角分号；替换为 英文半角分号;
- 中文全角问号？替换为 英文半角问号?
- 中文全角感叹号！替换为 英文半角感叹号!
"""

import json
import os
import sys

def fix_punctuation_in_string(text):
    """修复字符串中的中文全角标点"""
    if not isinstance(text, str):
        return text
    
    replacements = {
        '：': ':',  # 中文全角冒号
        '，': ',',  # 中文全角逗号
        '。': '.',  # 中文全角句号
        '；': ';',  # 中文全角分号
        '？': '?',  # 中文全角问号
        '！': '!',  # 中文全角感叹号
        '（': '(',  # 中文全角左括号
        '）': ')',  # 中文全角右括号
        '【': '[',  # 中文全角左方括号
        '】': ']',  # 中文全角右方括号
        '“': '"',  # 中文左双引号
        '”': '"',  # 中文右双引号
        '‘': "'",  # 中文左单引号
        '’': "'",  # 中文右单引号
    }
    
    result = text
    count = 0
    for old, new in replacements.items():
        if old in result:
            c = result.count(old)
            count += c
            result = result.replace(old, new)
    
    return result, count

def process_json_file(filepath):
    """处理单个JSON文件"""
    print(f"\n处理文件: {filepath}")
    
    # 读取文件
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return 0
    
    total_replacements = 0
    
    def process_item(item, path=""):
        nonlocal total_replacements
        if isinstance(item, str):
            fixed, count = fix_punctuation_in_string(item)
            if count > 0:
                total_replacements += count
                print(f"  修复 {count} 处: {path[:80]}...")
            return fixed
        elif isinstance(item, dict):
            return {k: process_item(v, f"{path}.{k}") for k, v in item.items()}
        elif isinstance(item, list):
            return [process_item(v, f"{path}[{i}]") for i, v in enumerate(item)]
        else:
            return item
    
    # 处理数据
    fixed_data = process_item(data)
    
    # 写回文件
    if total_replacements > 0:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(fixed_data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 已写回文件，共修复 {total_replacements} 处")
        except Exception as e:
            print(f"  ❌ 写回失败: {e}")
    else:
        print(f"  ✅ 无需修复")
    
    return total_replacements

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    files_to_process = [
        os.path.join(data_dir, 'tools.json'),
        os.path.join(data_dir, 'posts.json'),
    ]
    
    # 检查文件是否存在
    existing_files = [f for f in files_to_process if os.path.exists(f)]
    print(f"找到 {len(existing_files)} 个待处理文件")
    
    total = 0
    for filepath in existing_files:
        total += process_json_file(filepath)
    
    print(f"\n{'='*60}")
    print(f"处理完成！共修复 {total} 处中文全角标点")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
