"""
Fix: Blog post CTA buttons pointing to Google search instead of official website.

Root cause (line 213):
  const officialUrl = tool?.officialUrl || `https://www.google.com/search?q=${encodeURIComponent(toolName)}`;

When a blog post has no matching tool in tools.json (or the tool has no officialUrl),
the CTA falls back to a Google search URL. Also, toolName becomes the first word of
the post title (e.g. "Best" from "Best AI Tools for..."), producing nonsensical
buttons like "Start Best Free Trial" linking to google.com/search?q=Best.

Fix:
1. Remove Google search fallback - officialUrl should be undefined when no tool match
2. Only render CTAs when there's a valid officialUrl or affiliateUrl
3. When no tool match, use a generic tool name instead of first word of title
"""
import re

FILE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\blog\[slug]\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Replace the Google search fallback
old_line = '  const officialUrl = tool?.officialUrl || `https://www.google.com/search?q=${encodeURIComponent(toolName)}`;'
new_line = '  const officialUrl = tool?.officialUrl || undefined;'

if old_line in content:
    content = content.replace(old_line, new_line)
    print("[OK] Fixed officialUrl fallback (removed Google search URL)")
else:
    print("[SKIP] officialUrl line not found (may already be fixed)")

# Fix 2: When no tool match, use generic name instead of first word of title
old_toolname = '  const toolName = tool?.name || post.title.split(" ")[0] || "this tool";'
new_toolname = '  const toolName = tool?.name || "this AI tool";'

if old_toolname in content:
    content = content.replace(old_toolname, new_toolname)
    print("[OK] Fixed toolName fallback (no more 'Best' from title)")
else:
    print("[SKIP] toolName line not found")

# Fix 3: The bottom CTA always renders (line ~554). Add guard so it only renders
# when there's a valid URL.
# Find the bottom CTA block and wrap it in a condition.
old_bottom_cta = '''      {/* 底部联盟CTA */}
      <AffiliateCTA
        toolName={toolName}
        officialUrl={officialUrl}
        affiliateUrl={affiliateUrl}
        description={`Read our full review above, then visit ${toolName} official site to try it for yourself.`}
        variant="bottom"
        hasFreeTier={tool?.hasFreeTier}
        freeAccess={/free/i.test(post.title || "")}
      />'''

new_bottom_cta = '''      {/* 底部联盟CTA - only show when there is a valid official URL */}
      {(officialUrl || affiliateUrl) && (
        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Read our full review above, then visit ${toolName} official site to try it for yourself.`}
          variant="bottom"
          hasFreeTier={tool?.hasFreeTier}
          freeAccess={/free/i.test(post.title || "")}
        />
      )}'''

if old_bottom_cta in content:
    content = content.replace(old_bottom_cta, new_bottom_cta)
    print("[OK] Added guard to bottom CTA (only renders with valid URL)")
else:
    print("[SKIP] bottom CTA block not found")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone. Run npx tsc --noEmit to verify.")
