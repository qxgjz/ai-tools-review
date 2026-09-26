import os

path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\blog\[slug]\page.tsx"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 重命名 import
content = content.replace('import dynamic from "next/dynamic";', 'import nextDynamic from "next/dynamic";')
# 重命名两处使用
content = content.replace('const Giscus = dynamic(() =>', 'const Giscus = nextDynamic(() =>')
content = content.replace('const ReviewTabs = dynamic(() =>', 'const ReviewTabs = nextDynamic(() =>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Verifying...")
# 验证
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
print("nextDynamic import:", 'import nextDynamic' in c)
print("Giscus nextDynamic:", 'const Giscus = nextDynamic' in c)
print("ReviewTabs nextDynamic:", 'const ReviewTabs = nextDynamic' in c)
print("old dynamic import gone:", 'import dynamic from' not in c)
