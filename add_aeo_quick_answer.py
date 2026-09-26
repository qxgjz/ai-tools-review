import re

filepath = r'app/tools/[slug]/page.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original size: {len(content)} bytes')

# 检查是否已经添加了Quick Answer
if 'Quick Answer' in content:
    print('Quick Answer already exists, skipping')
else:
    # 在Header section之后、Author Bio之前插入
    marker = """      </section>

      {/* Author Bio - E-E-A-T Expertise & Authoritativeness signal */}"""

    aeo_section = """      </section>

      {/* AEO/GEO Optimization: Quick Answer - Answer First for AI Search Citation */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 rounded-2xl border border-blue-100 dark:border-blue-900/50 p-6 sm:p-8 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Zap className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Quick Answer</h2>
        </div>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">What is {tool.name}?</h3>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{tool.description} Developed by {tool.vendor}, it is categorized as a {tool.category} AI solution.</p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">How good is {tool.name}?</h3>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{tool.name} achieves a <strong>{total.toFixed(1)}/10</strong> overall score ({grade} grade) in our comprehensive 6-dimension evaluation. It performs strongest in {Object.entries(tool.scores || {}).sort((a,b) => b[1]-a[1])[0]?.[0] || "functionality"} ({Object.entries(tool.scores || {}).sort((a,b) => b[1]-a[1])[0]?.[1] || "N/A"}/10).</p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Is {tool.name} free?</h3>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{tool.pricing.some(t => t.price?.includes("$0") || t.price?.toLowerCase().includes("free")) ? "Yes, " + tool.name + " offers a free tier. " : tool.name + " pricing starts at " + (tool.pricing[0]?.price || "contact vendor") + ". "}It offers {tool.pricing.length} pricing tier{tool.pricing.length > 1 ? "s" : ""}: {tool.pricing.map(t => t.name).join(", ")}.</p>
          </div>
        </div>
      </section>

      {/* AEO/GEO Optimization: Key Takeaways - Structured for AI Citation */}
      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Key Takeaways</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-emerald-100 dark:bg-emerald-900/30">
              <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">Best For</h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">{tool.useCases?.[0] || "Users seeking " + tool.category + " AI solutions"}</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
              <Award className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">Overall Rating</h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">{total.toFixed(1)}/10 ({grade} grade) - {GRADE_DESCRIPTIONS[grade]}</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-amber-100 dark:bg-amber-900/30">
              <Sparkles className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">Top Feature</h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">{tool.keyFeatures?.[0] || tool.pros?.[0] || "Comprehensive feature set"}</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
              <ShieldCheck className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">Ethics Score</h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">{tool.scores?.ethics || "N/A"}/10 - Evaluated for data privacy and responsible AI practices</p>
            </div>
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            <strong>Source:</strong> AIToolCrux Editorial Team | <strong>Last updated:</strong> {tool.lastUpdated} | <strong>Methodology:</strong> 6-dimension evaluation | <Link href="/methodology" className="text-blue-600 dark:text-blue-400 hover:underline">Full methodology</Link>
          </p>
        </div>
      </section>

      {/* Author Bio - E-E-A-T Expertise & Authoritativeness signal */}"""

    if marker in content:
        content = content.replace(marker, aeo_section)
        print('Added Quick Answer and Key Takeaways sections')
    else:
        print('Could not find insertion marker')

    # 添加缺失的import
    if 'Zap' not in content:
        old_import = 'import { ArrowLeft, Check, X, Building2, Clock, Tag, ExternalLink, TrendingUp, Sparkles, Lightbulb, Image as ImageIcon, Award, Target, Users, Wrench, GitCompare, Microscope, Quote } from "lucide-react";'
        new_import = 'import { ArrowLeft, Check, X, Building2, Clock, Tag, ExternalLink, TrendingUp, Sparkles, Lightbulb, Image as ImageIcon, Award, Target, Users, Wrench, GitCompare, Microscope, Quote, Zap, BookOpen, ShieldCheck } from "lucide-react";'
        if old_import in content:
            content = content.replace(old_import, new_import)
            print('Added Zap, BookOpen, ShieldCheck to imports')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'New size: {len(content)} bytes')
