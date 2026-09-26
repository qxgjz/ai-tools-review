import io, re

f = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\blog\[slug]\page.tsx"
with io.open(f, "r", encoding="utf-8") as fh:
    c = fh.read()

# Add hasFreeTier prop to all <AffiliateCTA ... /> calls (before closing />)
# Pattern: find <AffiliateCTA ... /> blocks and inject hasFreeTier={tool?.hasFreeTier} if missing
old1 = '''        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Ready to try ${toolName}? Click below to visit the official site and get started.`}
          variant="banner"
        />'''
new1 = '''        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Ready to try ${toolName}? Click below to visit the official site and get started.`}
          variant="banner"
          hasFreeTier={tool?.hasFreeTier}
        />'''

old2 = '''        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Still considering ${toolName}? Read our verdict below, or visit the official site now.`}
          variant="banner"
        />'''
new2 = '''        <AffiliateCTA
          toolName={toolName}
          officialUrl={officialUrl}
          affiliateUrl={affiliateUrl}
          description={`Still considering ${toolName}? Read our verdict below, or visit the official site now.`}
          variant="banner"
          hasFreeTier={tool?.hasFreeTier}
        />'''

old3 = '''      <AffiliateCTA
        toolName={toolName}
        officialUrl={officialUrl}
        affiliateUrl={affiliateUrl}
        description={`Read our full review above, then visit ${toolName} official site to try it for yourself.`}
        variant="bottom"
      />'''
new3 = '''      <AffiliateCTA
        toolName={toolName}
        officialUrl={officialUrl}
        affiliateUrl={affiliateUrl}
        description={`Read our full review above, then visit ${toolName} official site to try it for yourself.`}
        variant="bottom"
        hasFreeTier={tool?.hasFreeTier}
      />'''

n = 0
for o, nw in [(old1, new1), (old2, new2), (old3, new3)]:
    if o in c:
        c = c.replace(o, nw)
        n += 1

with io.open(f, "w", encoding="utf-8") as fh:
    fh.write(c)
print(f"Updated {n}/3 blog CTA calls")
