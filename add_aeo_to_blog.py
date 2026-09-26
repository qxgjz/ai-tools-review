import re

with open('app/blog/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Zap and BookOpen icons to imports
old_imports = 'import { ArrowRight, Image as ImageIcon } from "lucide-react";'
new_imports = 'import { ArrowRight, Image as ImageIcon, Zap, BookOpen, CheckCircle2, Star, Lightbulb, Award } from "lucide-react";'
content = content.replace(old_imports, new_imports)

# 2. Find the position after Author bio and before article excerpt
# Insert Quick Answer and Key Takeaways after the excerpt block
old_excerpt = '''      {/* 文章摘要 */}
      <div className="bg-gray-50 dark:bg-gray-900 border-l-4 border-blue-500 p-4 mb-6 rounded-r">
        <p className="text-gray-700 dark:text-gray-300 italic">{post.excerpt}</p>
      </div>'''

new_excerpt_with_aeo = '''      {/* 文章摘要 */}
      <div className="bg-zinc-50 dark:bg-zinc-900 border-l-4 border-emerald-500 p-4 mb-6 rounded-r">
        <p className="text-zinc-700 dark:text-zinc-300 italic">{post.excerpt}</p>
      </div>

      {/* AEO/GEO Optimization: Quick Answer - Answer First for AI Search Citation */}
      <section className="bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-100 dark:border-emerald-900/50 p-6 sm:p-8 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Zap className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-xl font-bold text-zinc-900 dark:text-white">Quick Answer</h2>
        </div>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">What is this article about?</h3>
            <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">{post.excerpt} This comprehensive guide covers key features, pricing, pros and cons, and real-world use cases.</p>
          </div>
          <div>
            <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">What are the key findings?</h3>
            <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">Based on our hands-on testing and six-dimension evaluation framework, we analyze the tool&apos;s strengths, weaknesses, pricing value, and ideal use cases. Our editorial team provides an independent, affiliate-free assessment.</p>
          </div>
          <div>
            <h3 className="font-semibold text-zinc-800 dark:text-zinc-200 mb-2">Who should read this?</h3>
            <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">This article is for users evaluating {toolName || "AI tools"} for personal or business use, technology decision-makers comparing solutions, and anyone seeking an independent, expert review before committing to a subscription.</p>
          </div>
        </div>
      </section>

      {/* AEO/GEO Optimization: Key Takeaways - Structured for AI Citation */}
      <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">
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
              <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Best For</h4>
              <p className="text-zinc-600 dark:text-zinc-400 text-sm">Users seeking an in-depth, independent review of {toolName || "this AI tool"} before making a purchase decision.</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
              <Star className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Our Rating</h4>
              <p className="text-zinc-600 dark:text-zinc-400 text-sm">{avgScore > 0 ? `${Math.round(avgScore * 10) / 10}/10 based on our six-dimension evaluation` : "Rated independently by our editorial team using a transparent six-dimension framework"}.</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-amber-100 dark:bg-amber-900/30">
              <Lightbulb className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            </div>
            <div>
              <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Top Insight</h4>
              <p className="text-zinc-600 dark:text-zinc-400 text-sm">We provide hands-on testing, real-world use cases, and direct comparisons with alternatives to help you make an informed decision.</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
              <Award className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <h4 className="font-semibold text-zinc-800 dark:text-zinc-200 text-sm">Expert Verdict</h4>
              <p className="text-zinc-600 dark:text-zinc-400 text-sm">Read the full review below for detailed analysis, pricing breakdown, pros and cons, and our final recommendation.</p>
            </div>
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-zinc-100 dark:border-zinc-800">
          <p className="text-xs text-zinc-500 dark:text-zinc-400">
            <strong>Source:</strong> AIToolCrux Editorial Team | <strong>Last updated:</strong> {post.publishedAt || "2026"} | <strong>Methodology:</strong> Six-dimension evaluation | <Link href="/methodology" className="text-emerald-600 dark:text-emerald-400 hover:underline">Full methodology</Link>
          </p>
        </div>
      </section>'''

content = content.replace(old_excerpt, new_excerpt_with_aeo)

with open('app/blog/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Blog page updated with Quick Answer and Key Takeaways')
