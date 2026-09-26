import io, re

f = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\blog\[slug]\page.tsx"
with io.open(f, "r", encoding="utf-8") as fh:
    c = fh.read()

# Inject a derived const before first AffiliateCTA usage:
# const isFreeAccessPost = /free/i.test(post.title || "");
# Find where post is in scope. We'll add right after affiliateUrl is computed.
# Simpler: add inline expression at each call site.

# For each of the 3 AffiliateCTA calls, add freeAccess={/free/i.test(post.title || "")}
# Pattern: lines ending with `hasFreeTier={tool?.hasFreeTier}`
old = '          hasFreeTier={tool?.hasFreeTier}\n        />'
new = '          hasFreeTier={tool?.hasFreeTier}\n          freeAccess={/free/i.test(post.title || "")}\n        />'
n1 = c.count(old)
c = c.replace(old, new)

old2 = '        hasFreeTier={tool?.hasFreeTier}\n      />'
new2 = '        hasFreeTier={tool?.hasFreeTier}\n        freeAccess={/free/i.test(post.title || "")}\n      />'
n2 = c.count(old2)
c = c.replace(old2, new2)

with io.open(f, "w", encoding="utf-8") as fh:
    fh.write(c)
print(f"banner calls: {n1}, bottom call: {n2}")
