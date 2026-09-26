import re

layout_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\layout.tsx"

with open(layout_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add BackToTop import
content = content.replace(
    'import { Header } from "@/components/layout/Header";\nimport { ThemeProvider } from "@/components/theme/ThemeProvider";',
    'import { Header } from "@/components/layout/Header";\nimport { BackToTop } from "@/components/layout/BackToTop";\nimport { ThemeProvider } from "@/components/theme/ThemeProvider";'
)

# 2. Change main padding from pt-24 to pt-8 (Header now has internal spacer)
content = content.replace(
    '<main className="pt-24">{children}</main>',
    '<main id="main-content" className="pt-8">{children}</main>'
)

# 3. Add BackToTop before closing ThemeProvider
content = content.replace(
    '        </ThemeProvider>',
    '        <BackToTop />\n        </ThemeProvider>'
)

# 4. Change footer link colors from blue to emerald for consistency
content = content.replace('hover:text-blue-600 dark:hover:text-blue-400', 'hover:text-emerald-600 dark:hover:text-emerald-400')

# 5. Change the "Get Free AI Tools Guide" link color
content = content.replace('text-blue-600 dark:text-blue-400 hover:underline', 'text-emerald-600 dark:text-emerald-400 hover:underline')

with open(layout_path, "w", encoding="utf-8") as f:
    f.write(content)

print("layout.tsx updated successfully")
print(f"BackToTop import added: {'BackToTop' in content}")
print(f"BackToTop component added: {'<BackToTop />' in content}")
print(f"main id added: {'id=\"main-content\"' in content}")
