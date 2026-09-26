with open('app/alternatives/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Zap and BookOpen icons to imports
old_imports = 'import Link from "next/link";'
new_imports = '''import Link from "next/link";
import { Zap, BookOpen, CheckCircle2, Star, Lightbulb, Award } from "lucide-react";'''
content = content.replace(old_imports, new_imports, 1)

# 2. Insert Quick Answer and Key Takeaways after Hero Section and before Introduction
old_intro = '''      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Introduction */}
        <section className="mb-12">'''

new_intro_with_aeo = '''      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* AEO/GEO Optimization: Quick Answer - Answer First for AI Search Citation */}
        <section className="bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-100 dark:border-emerald-900/50 p-6 sm:p-8 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-xl font-bold text-zinc-900 dark:text-white">Quick Answer</h2>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">What are the best {page.targetTool} alternatives?</h3>
              <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">Based on our comprehensive six-dimension evaluation, the top {page.alternatives.length} alternatives to {page.targetTool} are {page.alternatives.slice(0, 3).map(a => a.name).join(", ")}. Each alternative offers different strengths in features, pricing, and use cases.</p>
            </div>
            <div>
              <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">Which alternative is best for me?</h3>
              <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">The best alternative depends on your specific needs: {page.alternatives[0]?.name} is ideal for {page.alternatives[0]?.reason || "most users"}, while {page.alternatives[1]?.name} excels at {page.alternatives[1]?.reason || "specific use cases"}. Compare features and pricing side-by-side below to find your best fit.</p>
            </div>
            <div>
              <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">Are these alternatives free to use?</h3>
              <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">Most alternatives offer free tiers or free trials. {page.alternatives.filter(a => "free" in (a.pricing || "").lower() || "$0" in a.pricing).length} of {page.alternatives.length} tools have free options available. We recommend starting with the free plan to evaluate whether the tool meets your needs before upgrading.</p>
            </div>
          </div>
        </section>

        {/* AEO/GEO Optimization: Key Takeaways - Structured for AI Citation */}
        <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-8">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-xl font-bold text-zinc-900 dark:text-white">Key Takeaways</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-emerald-100 dark:bg-emerald-900/30">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Best Overall</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">{page.alternatives[0]?.name || "Top pick"} - {page.alternatives[0]?.reason || "Best overall alternative based on our comprehensive evaluation"}.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
                <Star className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Top Rated</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">{page.alternatives[0]?.rating || "N/A"}/10 average rating across {page.alternatives.length} alternatives, independently evaluated by our editorial team.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-amber-100 dark:bg-amber-900/30">
                <Lightbulb className="w-4 h-4 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Key Consideration</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">Evaluate features, pricing, learning curve, and integration options. The cheapest option isn&apos;t always the best value long-term.</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
                <Award className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Expert Verdict</h4>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">Read detailed reviews below for each alternative, including pros, cons, pricing, and real-world use cases to make an informed decision.</p>
              </div>
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800">
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              <strong>Source:</strong> AIToolCrux Editorial Team | <strong>Last updated:</strong> 2026-09-11 | <strong>Methodology:</strong> Six-dimension evaluation | <Link href="/methodology" className="text-emerald-600 dark:text-emerald-400 hover:underline">Full methodology</Link>
            </p>
          </div>
        </section>

        {/* Introduction */}
        <section className="mb-12">'''

content = content.replace(old_intro, new_intro_with_aeo)

with open('app/alternatives/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Alternatives page updated with Quick Answer and Key Takeaways')
