import os
import re

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app"

pages = [
    r"tools\[slug]\page.tsx",
    r"blog\[slug]\page.tsx",
    r"category\[slug]\page.tsx",
    r"subcategory\[slug]\page.tsx",
    r"compare\[slug]\page.tsx",
    r"alternatives\[slug]\page.tsx",
    r"authors\[slug]\page.tsx",
    r"best-for\[audience]\page.tsx",
    r"blog\category\[slug]\page.tsx",
]

for rel in pages:
    path = os.path.join(base, rel)
    if not os.path.exists(path):
        print(f"SKIP: {rel}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配: force-static";\n\n[任意字符]() {  替换为正确的函数声明
    # U+0001 或其他残留字符可能在 () 前面
    pattern = r'(export const dynamic = "force-static";\s*\n\s*).*?\(\) \{'
    replacement = r'\1export function generateStaticParams() {'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"FIXED: {rel}")
    else:
        if 'export function generateStaticParams()' in new_content:
            print(f"OK: {rel}")
        else:
            print(f"STILL BROKEN: {rel}")
