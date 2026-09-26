with open('app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the right column fake product preview with a real Top 3 Tools showcase
old_right_col = '''            {/* Right: Visual element (5 cols) */}
            <div className="lg:col-span-5 hidden lg:block">
              <FadeIn delay={0.3} y={30}>
                <div className="relative">
                  {/* Featured tool card mockup */}
                  <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 shadow-2xl">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-bold">
                          C
                        </div>
                        <div>
                          <div className="font-semibold text-white">ChatGPT</div>
                          <div className="text-xs text-zinc-500">OpenAI</div>
                        </div>
                      </div>
                      <span className="px-2 py-0.5 bg-green-700 text-white text-xs font-bold rounded">A</span>
                    </div>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-zinc-400">Features</span>
                          <span className="text-zinc-300">9.2</span>
                        </div>
                        <div className="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                          <div className="h-full bg-emerald-500 rounded-full" style={{ width: "92%" }} />
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-zinc-400">UX</span>
                          <span className="text-zinc-300">8.8</span>
                        </div>
                        <div className="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                          <div className="h-full bg-emerald-500 rounded-full" style={{ width: "88%" }} />
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-zinc-400">Pricing</span>
                          <span className="text-zinc-300">7.5</span>
                        </div>
                        <div className="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                          <div className="h-full bg-emerald-500 rounded-full" style={{ width: "75%" }} />
                        </div>
                      </div>
                    </div>
                    <div className="mt-4 pt-4 border-t border-zinc-800 flex items-center justify-between">
                      <span className="text-2xl font-bold text-white">8.7</span>
                      <span className="text-xs text-zinc-500">/ 10 Overall</span>
                    </div>
                  </div>
                  {/* Floating badge */}
                  <div className="absolute -top-3 -right-3 px-3 py-1.5 bg-emerald-600 text-white text-xs font-semibold rounded-lg shadow-lg">
                    #1 Ranked
                  </div>
                </div>
              </FadeIn>
            </div>'''

new_right_col = '''            {/* Right: Top 3 Tools showcase - real data, no fake UI (Taste Skill rule) */}
            <div className="lg:col-span-5 hidden lg:block">
              <FadeIn delay={0.3} y={30}>
                <div className="space-y-3">
                  <div className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">Top 3 Rated Tools</div>
                  {topTools.slice(0, 3).map((tool, i) => (
                    <Link
                      key={tool.slug}
                      href={`/tools/${tool.slug}`}
                      className="flex items-center gap-4 p-4 bg-zinc-900/50 border border-zinc-800 rounded-xl hover:border-emerald-500/50 hover:bg-zinc-900 transition-all group"
                    >
                      <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-lg bg-zinc-800 text-zinc-300 font-bold text-lg">
                        {tool.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-white group-hover:text-emerald-400 transition-colors truncate">{tool.name}</div>
                        <div className="text-xs text-zinc-500 truncate">{tool.vendor}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xl font-bold text-emerald-400">{tool.total.toFixed(1)}</div>
                        <div className="text-[10px] text-zinc-500">/10</div>
                      </div>
                      <div className="w-6 h-6 flex items-center justify-center rounded-full bg-zinc-800 text-zinc-500 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                        <ArrowRight className="w-3 h-3" />
                      </div>
                    </Link>
                  ))}
                  <Link href="/ranking" className="flex items-center justify-center gap-2 text-sm text-emerald-400 hover:text-emerald-300 transition-colors pt-2">
                    View all {tools.length} rankings
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </FadeIn>
            </div>'''

content = content.replace(old_right_col, new_right_col)

with open('app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Hero section optimized: removed div-based fake product preview, replaced with real Top 3 Tools showcase')
