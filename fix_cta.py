import io

f = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\tools\[slug]\page.tsx"
with io.open(f, "r", encoding="utf-8") as fh:
    c = fh.read()

old = '''            <a href={tool.affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-6 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md">
              <ExternalLink className="w-4 h-4" />
              {tool.affiliateUrl ? `Try ${tool.name} Free` : "Visit Official Website"}
            </a>
            {tool.affiliateUrl && tool.hasFreeTier && (
              <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-1.5 font-medium">
                No credit card required
              </p>
            )}'''

new = '''            <a href={tool.affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-6 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md">
              <ExternalLink className="w-4 h-4" />
              {tool.hasFreeTier ? `Try ${tool.name} Free` : `Start ${tool.name} Free Trial`}
            </a>
            <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-1.5 font-medium">
              ✅ Tested by our team · No credit card required for free plan
            </p>'''

if old in c:
    c = c.replace(old, new)
    with io.open(f, "w", encoding="utf-8") as fh:
        fh.write(c)
    print("OK hero CTA replaced")
else:
    print("NOT FOUND")
