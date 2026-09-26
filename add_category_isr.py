import os

file_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\category\[slug]\page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add revalidate before generateStaticParams
if "export const revalidate" not in content:
    content = content.replace(
        "export async function generateStaticParams",
        "// ISR: Cache for 30 minutes, category pages change infrequently\nexport const revalidate = 1800;\n\nexport async function generateStaticParams"
    )
    print("Added ISR revalidate=1800 to category page")
else:
    print("revalidate already exists")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
