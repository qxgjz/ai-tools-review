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
    
    # 修复被破坏的 generateStaticParams：找到 "force-static";\n\n() {  恢复为 force-static";\n\nexport function generateStaticParams() {
    # 模式1：函数名被U+0001替换的情况
    broken = r'export const dynamic = "force-static";\s*\n\s*\(\) \{'
    fixed = 'export const dynamic = "force-static";\n\nexport function generateStaticParams() {'
    new_content = re.sub(broken, fixed, content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"FIXED: {rel}")
    else:
        # 检查是否已经正确
        if 'export function generateStaticParams()' in new_content and 'force-static' in new_content:
            print(f"OK: {rel}")
        else:
            print(f"NEEDS CHECK: {rel}")
