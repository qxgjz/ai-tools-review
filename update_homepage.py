import re

page_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the article card image area with gradient backgrounds
old_image_block = '''<div className="h-36 bg-zinc-100 dark:bg-zinc-800 relative overflow-hidden">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <PenTool className="w-12 h-12 text-zinc-300 dark:text-zinc-700" />
                    </div>
                    <div className="absolute top-3 left-3">
                      <span className="px-2 py-0.5 bg-white/90 dark:bg-zinc-900/90 text-zinc-600 dark:text-zinc-400 text-xs font-medium rounded">
                        {post.category}
                      </span>
                    </div>
                  </div>'''

new_image_block = '''<div className="h-36 relative overflow-hidden bg-gradient-to-br from-emerald-500/10 via-zinc-100 to-zinc-200 dark:from-emerald-900/20 dark:via-zinc-800 dark:to-zinc-900">
                    {/* Decorative gradient orbs */}
                    <div className="absolute -top-8 -right-8 w-24 h-24 rounded-full bg-emerald-400/20 blur-2xl" />
                    <div className="absolute -bottom-6 -left-6 w-20 h-20 rounded-full bg-emerald-600/15 blur-xl" />
                    {/* Icon */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-14 h-14 flex items-center justify-center rounded-2xl bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm shadow-md">
                        <PenTool className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />
                      </div>
                    </div>
                    {/* Category badge */}
                    <div className="absolute top-3 left-3">
                      <span className="px-2.5 py-1 bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm text-zinc-700 dark:text-zinc-300 text-xs font-semibold rounded-md shadow-sm capitalize">
                        {post.category}
                      </span>
                    </div>
                  </div>'''

if old_image_block in content:
    content = content.replace(old_image_block, new_image_block)
    print("Article card image block replaced successfully")
else:
    print("WARNING: Could not find exact image block, trying alternative match...")
    # Try a more flexible replacement
    content = content.replace(
        'bg-zinc-100 dark:bg-zinc-800 relative overflow-hidden">\n                    <div className="absolute inset-0 flex items-center justify-center">\n                      <PenTool className="w-12 h-12 text-zinc-300 dark:text-zinc-700" />',
        'relative overflow-hidden bg-gradient-to-br from-emerald-500/10 via-zinc-100 to-zinc-200 dark:from-emerald-900/20 dark:via-zinc-800 dark:to-zinc-900">\n                    <div className="absolute -top-8 -right-8 w-24 h-24 rounded-full bg-emerald-400/20 blur-2xl" />\n                    <div className="absolute -bottom-6 -left-6 w-20 h-20 rounded-full bg-emerald-600/15 blur-xl" />\n                    <div className="absolute inset-0 flex items-center justify-center">\n                      <div className="w-14 h-14 flex items-center justify-center rounded-2xl bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm shadow-md">\n                        <PenTool className="w-7 h-7 text-emerald-600 dark:text-emerald-400" />'
    )
    print("Alternative replacement done")

# Also optimize Popular Tools by Category for mobile (2 columns on small screens)
content = content.replace(
    'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4',
    'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'
)
print("Popular Tools mobile layout optimized (sm:grid-cols-2)")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(content)

print("page.tsx updated successfully")
