import os
import re

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app"

# 需要加 force-static 的页面（有 generateStaticParams 但没有 force-static）
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

results = []
for rel in pages:
    path = os.path.join(base, rel)
    if not os.path.exists(path):
        results.append(f"SKIP (not found): {rel}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'force-static' in content:
        results.append(f"ALREADY: {rel}")
        continue
    # 在 generateStaticParams 函数之前插入 force-static
    # 找 generateStaticParams 的位置，在它前面一行插入
    pattern = r'(export function generateStaticParams)'
    replacement = 'export const dynamic = "force-static";\n\n\1'
    new_content = re.sub(pattern, replacement, content, count=1)
    if new_content == content:
        # 尝试在 dynamicParams 之后插入
        pattern2 = r'(export const dynamicParams = false;)'
        replacement2 = r'\1\nexport const dynamic = "force-static";'
        new_content = re.sub(pattern2, replacement2, content, count=1)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        results.append(f"FIXED: {rel}")
    else:
        results.append(f"FAILED (no pattern): {rel}")

for r in results:
    print(r)
