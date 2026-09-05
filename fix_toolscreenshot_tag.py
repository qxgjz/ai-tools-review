#!/usr/bin/env python3
"""修复ToolScreenshot组件的闭合标签"""

filepath = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\tools\[slug]\page.tsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复ToolScreenshot组件缺少闭合标签的问题
old_pattern = '''        <ToolScreenshot
          toolSlug={tool.slug}
          toolName={tool.name}
          vendor={tool.vendor}
      </section>'''

new_pattern = '''        <ToolScreenshot
          toolSlug={tool.slug}
          toolName={tool.name}
          vendor={tool.vendor}
        />
      </section>'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern, 1)
    print("✅ 已修复ToolScreenshot组件闭合标签")
else:
    print("❌ 未找到需要修复的模式")
    # 检查当前状态
    if "vendor={tool.vendor}\n      </section>" in content:
        print("   确认：ToolScreenshot组件缺少闭合标签")
    elif "vendor={tool.vendor}\n        />" in content:
        print("   ToolScreenshot组件已有闭合标签")

# 写回文件
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 文件已更新")
