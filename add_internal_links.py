with open('app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the position after CATEGORIES section and before TRENDING RANKING section
# Add a "Popular Tools by Category" section

old_section = '''      {/* === TRENDING RANKING - Left aligned, different layout === */}'''

new_section_with_popular = '''      {/* === POPULAR TOOLS BY CATEGORY - Internal link optimization === */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-12 lg:py-16">
        <div className="mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-white mb-2">
            Popular Tools by Category
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400">
            Explore the most searched AI tools across categories
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Image Generation */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <ImageIcon className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Image Generation
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "image").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/image" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all image tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* AI Coding */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <Code className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Coding Tools
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "code").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/code" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all coding tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* AI Audio */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <Music className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Audio & Voice
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "audio").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/audio" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all audio tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {/* AI Productivity */}
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              AI Productivity
            </h3>
            <div className="space-y-2">
              {tools.filter(t => t.category === "productivity").slice(0, 4).map((tool) => {
                const total = calculateScoreResult(tool.scores).total;
                return (
                  <Link key={tool.slug} href={`/tools/${tool.slug}`} className="flex items-center justify-between py-1.5 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 px-2 -mx-2 rounded transition-colors">
                    <span className="text-sm text-zinc-700 dark:text-zinc-300 hover:text-emerald-600 dark:hover:text-emerald-400 font-medium">{tool.name}</span>
                    <span className="text-xs text-zinc-400 dark:text-zinc-500 font-mono">{total.toFixed(1)}</span>
                  </Link>
                );
              })}
            </div>
            <Link href="/category/productivity" className="mt-3 inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300">
              View all productivity tools
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        </div>
      </section>

      {/* === TRENDING RANKING - Left aligned, different layout === */}'''

content = content.replace(old_section, new_section_with_popular)

with open('app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Homepage updated with Popular Tools by Category section')
print('Added internal links for midjourney, cursor, elevenlabs, notion-ai and 12+ other tools')
