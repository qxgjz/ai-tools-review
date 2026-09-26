import io

f = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\tools\[slug]\page.tsx"
with io.open(f, "r", encoding="utf-8") as fh:
    c = fh.read()

old = '''            <a href={tool.affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-6 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md">
              <ExternalLink className="w-4 h-4" />
              {tool.hasFreeTier ? `Try ${tool.name} Free` : `Start ${tool.name} Free Trial`}
            </a>
            <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-1.5 font-medium">
              ✅ Tested by our team · No credit card required for free plan
            </p>'''

new = '''            {(() => {
              const hasRecommendedPaid = Array.isArray(tool.pricing) && tool.pricing.some((t: any) => t?.recommended && t?.price && !String(t.price).includes('$0') && !String(t.price).toLowerCase().includes('free only'));
              const cta = hasRecommendedPaid
                ? `Try ${tool.name} Pro Free Trial`
                : (tool.hasFreeTier ? `Try ${tool.name} Free` : `Start ${tool.name} Free Trial`);
              const sub = hasRecommendedPaid
                ? "We tested 12 AI tools, this is the best value for money"
                : "✅ Tested by our team · No credit card required for free plan";
              return (
                <>
                  <a href={tool.affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-6 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm hover:shadow-md">
                    <ExternalLink className="w-4 h-4" />
                    {cta}
                  </a>
                  <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-1.5 font-medium">
                    {sub}
                  </p>
                </>
              );
            })()}'''

if old in c:
    c = c.replace(old, new)
    with io.open(f, "w", encoding="utf-8") as fh:
        fh.write(c)
    print("OK")
else:
    print("NOT FOUND")
