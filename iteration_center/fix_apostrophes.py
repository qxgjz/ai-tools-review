"""Fix TypeScript errors: apostrophes in single-quoted strings"""

with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix line 670: "If you're" -> use double quotes for the outer string
content = content.replace(
    "'Users who want to leverage AI to save time and improve their workflow. If you're evaluating tools in this category, this one is worth trying.'",
    "\"Users who want to leverage AI to save time and improve their workflow. If you're evaluating tools in this category, this one is worth trying.\""
)

# Fix line 684: "tool's" -> use double quotes
content = content.replace(
    "'If you only need basic AI features occasionally, you might not need this tool's full feature set. Try the free tier or a simpler alternative first to see what you actually need.'",
    "\"If you only need basic AI features occasionally, you might not need this tool's full feature set. Try the free tier or a simpler alternative first to see what you actually need.\""
)

# Fix line 702: "there's" -> use double quotes
content = content.replace(
    "'Check if there's a free tier or open-source alternative in this category before committing to a paid plan.'",
    "\"Check if there's a free tier or open-source alternative in this category before committing to a paid plan.\""
)

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Fixed apostrophe escaping in single-quoted strings")
