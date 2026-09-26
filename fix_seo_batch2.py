"""
Batch SEO fix script for OpenSEO audit issues.
Fixes: 404 redirects, thin tag noindex, footer links, long titles.
"""
import re

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# ============================================================
# 1. Fix 404 tool slugs in next.config.mjs
# ============================================================
# Mapping: slug -> destination category
REDIRECT_MAP = {
    "llama": "/category/chat",
    "anthropic-claude": "/category/chat",
    "google": "/category/chat",
    "firefly": "/category/design",
    "figma": "/category/design",
    "visme": "/category/design",
    "snappa": "/category/design",
    "stencil": "/category/design",
    "playground": "/category/image",
    "getimg": "/category/image",
    "recraft": "/category/image",
    "tensor-art": "/category/image",
    "mutable-ai": "/category/image",
    "bolt-new": "/category/code",
    "replit-agent": "/category/code",
    "jetbrains-ai": "/category/code",
    "amazon-q-developer": "/category/code",
    "amazon-polly": "/category/audio",
    "coqui": "/category/audio",
    "google-text-to-speech": "/category/audio",
    "natural-reader": "/category/audio",
    "resemble-ai": "/category/audio",
    "lumen5": "/category/video",
    "anytype": "/category/productivity",
    "capacities": "/category/productivity",
    "coda": "/category/productivity",
    "craft": "/category/productivity",
    "heptabase": "/category/productivity",
    "ink": "/category/productivity",
    "logseq": "/category/productivity",
    "mem-ai": "/category/productivity",
    "reflect": "/category/productivity",
    "tana": "/category/productivity",
    "closerscopy": "/category/writing",
    "frase": "/category/writing",
    "surfer": "/category/writing",
}

def fix_next_config():
    path = BASE + r"\next.config.mjs"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build redirect entries
    new_entries = []
    # Add /tools -> /ranking redirect (tools list page doesn't exist)
    new_entries.append('''      // OpenSEO fix: /tools list page 404 -> redirect to rankings
      {
        source: "/tools",
        destination: "/ranking",
        permanent: true,
      },''')

    for slug, dest in sorted(REDIRECT_MAP.items()):
        entry = f'''      // OpenSEO fix: /tools/{slug} 404 -> {dest}
      {{
        source: "/tools/{slug}",
        destination: "{dest}",
        permanent: true,
      }},'''
        new_entries.append(entry)

    new_block = "\n".join(new_entries)

    # Insert before the closing "];\n  },\n};" of redirects()
    # Find the last entry in redirects array and append after it
    # The pattern: find the closing of redirects array
    insert_marker = "      // GSC 404 fix - /category root\n      {\n        source: \"/category\",\n        destination: \"/\",\n        permanent: true,\n      },\n    ];"

    if insert_marker in content:
        replacement = insert_marker.replace(
            "    ];",
            new_block + "\n    ];"
        )
        content = content.replace(insert_marker, replacement)
    else:
        # Fallback: find "    ];" after "redirects"
        idx = content.find("async redirects()")
        if idx >= 0:
            # Find the closing ];
            close_idx = content.find("    ];", idx)
            if close_idx >= 0:
                content = content[:close_idx] + new_block + "\n" + content[close_idx:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] next.config.mjs: added {len(new_entries)} redirects")


# ============================================================
# 2. Fix blog tag page: noindex + shorter title
# ============================================================
def fix_blog_tag_page():
    path = BASE + r"\app\blog\tag\[slug]\page.tsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix title: shorten from "Best {tagName} AI Tools & Articles 2026 | AIToolCrux"
    # to "{tagName} AI Tools Reviews | AIToolCrux" (<=60 chars)
    old_title = 'title: `Best ${tagName} AI Tools & Articles 2026 | AIToolCrux`,'
    new_title = 'title: `${tagName} AI Tools Reviews | AIToolCrux`,'
    content = content.replace(old_title, new_title)

    # Add noindex,follow robots to metadata
    old_return = """  return {
    title: `${tagName} AI Tools Reviews | AIToolCrux`,
    description: `Explore ${articleCount} expert-reviewed ${tagName} AI tools and articles on AIToolCrux. In-depth comparisons and honest reviews.`,
    alternates: {
      canonical: `https://www.aitoolcrux.com/blog/tag/${params.slug}`,
    },
  };"""
    new_return = """  return {
    title: `${tagName} AI Tools Reviews | AIToolCrux`,
    description: `Explore ${articleCount} expert-reviewed ${tagName} AI tools and articles on AIToolCrux. In-depth comparisons and honest reviews.`,
    alternates: {
      canonical: `https://www.aitoolcrux.com/blog/tag/${params.slug}`,
    },
    robots: {
      index: false,
      follow: true,
    },
  };"""
    content = content.replace(old_return, new_return)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] blog/tag/[slug]/page.tsx: noindex added, title shortened")


# ============================================================
# 3. Fix blog category page: shorter title
# ============================================================
def fix_blog_category_page():
    path = BASE + r"\app\blog\category\[slug]\page.tsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_title = 'title: `Best ${categoryName} Articles & Reviews 2026 | AIToolCrux`,'
    new_title = 'title: `${categoryName} AI Tools Reviews | AIToolCrux`,'
    content = content.replace(old_title, new_title)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] blog/category/[slug]/page.tsx: title shortened")


# ============================================================
# 4. Add /ai-policy and /terms links to footer in layout.tsx
# ============================================================
def fix_footer():
    path = BASE + r"\app\layout.tsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Add /ai-policy and /terms to the Resources column
    # Find the Privacy Policy link and add after it
    old_privacy = '''                    <li><Link href="/privacy" className="text-sm text-gray-500 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">Privacy Policy</Link></li>'''
    new_privacy = '''                    <li><Link href="/privacy" className="text-sm text-gray-500 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">Privacy Policy</Link></li>
                    <li><Link href="/terms" className="text-sm text-gray-500 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">Terms of Service</Link></li>
                    <li><Link href="/ai-policy" className="text-sm text-gray-500 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">AI Policy</Link></li>'''
    content = content.replace(old_privacy, new_privacy)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] layout.tsx: added /terms and /ai-policy links to footer")


# ============================================================
# Run all
# ============================================================
if __name__ == "__main__":
    fix_next_config()
    fix_blog_tag_page()
    fix_blog_category_page()
    fix_footer()
    print("\n=== All fixes applied ===")
