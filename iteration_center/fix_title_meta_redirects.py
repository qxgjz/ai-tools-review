"""
Fix P1-005/P1-006/P1-007:
1. Fix blog category redirects (add missing, fix wrong one)
2. Tighten tool page title truncation to ensure <=60 chars
3. Improve meta description truncation to word boundary
"""

# ========== 1. Fix next.config.mjs redirects ==========
with open('next.config.mjs', 'r', encoding='utf-8') as f:
    config = f.read()

# Fix: "tools" was incorrectly redirecting to "ai-audio", should be "ai-tools"
config = config.replace(
    '''      {
        source: "/blog/category/tools",
        destination: "/blog/category/ai-audio",
        permanent: true,
      },''',
    '''      {
        source: "/blog/category/tools",
        destination: "/blog/category/ai-tools",
        permanent: true,
      },
      {
        source: "/blog/category/coding",
        destination: "/blog/category/ai-coding",
        permanent: true,
      },
      {
        source: "/blog/category/chat",
        destination: "/blog/category/ai-chat",
        permanent: true,
      },
      {
        source: "/blog/category/search",
        destination: "/blog/category/ai-search",
        permanent: true,
      },'''
)

with open('next.config.mjs', 'w', encoding='utf-8') as f:
    f.write(config)
print("[OK] Fixed blog category redirects (tools→ai-tools, added coding/chat/search)")

# ========== 2. Fix tool page title truncation ==========
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    tool_page = f.read()

# Current: name truncated at 27, but " Review 2026: " + score + " | AIToolCrux" = ~34 chars overhead
# 27 + 34 = 61 chars > 60. Reduce to 24 chars for name to stay <=60
# New title: "{name} Review 2026: {score}/10 | AIToolCrux"
# Overhead = " Review 2026: " (14) + "10.0/10 | AIToolCrux" (21) = 35 chars
# Name budget = 60 - 35 = 25 chars, with ellipsis = 24 chars

# Replace all 3 occurrences of the title truncation logic
tool_page = tool_page.replace(
    'tool.name.length > 27 ? tool.name.slice(0, 27) + "…" : tool.name',
    'tool.name.length > 24 ? tool.name.slice(0, 24) + "…" : tool.name'
)

# ========== 3. Improve meta description word-boundary truncation ==========
# Replace description.slice(0, 160) with a word-boundary-aware version
# We need to add a helper function and use it
# Current: description: description.slice(0, 160)
# New: truncateDescription(description, 155)

# Add helper function after the imports
helper_func = '''
function truncateDescription(text: string, maxLen: number = 155): string {
  if (text.length <= maxLen) return text;
  const truncated = text.slice(0, maxLen);
  const lastSpace = truncated.lastIndexOf(' ');
  return (lastSpace > 120 ? truncated.slice(0, lastSpace) : truncated).replace(/[\\s,;:-]+$/, '') + '…';
}
'''

# Insert helper before generateMetadata
tool_page = tool_page.replace(
    'export async function generateMetadata(',
    helper_func + '\nexport async function generateMetadata('
)

# Replace all description.slice(0, 160) with truncateDescription(description)
tool_page = tool_page.replace(
    'description: description.slice(0, 160)',
    'description: truncateDescription(description)'
)

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(tool_page)
print("[OK] Tool title truncation: 27→24 chars, description word-boundary truncation added")

# ========== Verify ==========
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    verify = f.read()

title_count = verify.count('tool.name.length > 24')
desc_count = verify.count('truncateDescription(description)')
helper_exists = 'function truncateDescription' in verify
print(f"  Title truncation occurrences: {title_count}")
print(f"  Description truncation occurrences: {desc_count}")
print(f"  Helper function exists: {helper_exists}")

# Verify redirects
with open('next.config.mjs', 'r', encoding='utf-8') as f:
    config_verify = f.read()
print(f"  tools→ai-tools redirect: {'/blog/category/ai-tools' in config_verify and 'tools' in config_verify}")
print(f"  coding→ai-coding redirect: {'/blog/category/coding' in config_verify}")
print(f"  chat→ai-chat redirect: {'/blog/category/chat' in config_verify}")
print(f"  search→ai-search redirect: {'/blog/category/search' in config_verify}")
