with open('components/tools/ToolCard.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the filled background progress bar (Taste Skill rule: NO scoring/progress bars with filled background tracks)
old_rating_section = '''          {/* Rating section */}
          <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-baseline gap-1">
                <span className="text-xl font-bold text-zinc-900 dark:text-zinc-100">{total.toFixed(1)}</span>
                <span className="text-xs text-zinc-400">/10</span>
              </div>
              <div className="w-7 h-7 flex items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                <ArrowUpRight className="w-3.5 h-3.5" />
              </div>
            </div>
            {/* Progress bar - solid color, no gradient */}
            <div className="h-1 w-full bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${scorePercent}%` }}
                transition={{ duration: 0.6, delay: Math.min(index * 0.04 + 0.2, 0.6), ease: "easeOut" }}
                className={`h-full rounded-full ${GRADE_BAR_COLORS[grade]}`}
              />
            </div>
          </div>'''

new_rating_section = '''          {/* Rating section - number + grade only, NO filled background progress bar (Taste Skill rule) */}
          <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800">
            <div className="flex items-center justify-between">
              <div className="flex items-baseline gap-2">
                <span className="text-xl font-bold text-zinc-900 dark:text-zinc-100">{total.toFixed(1)}</span>
                <span className="text-xs text-zinc-400">/10</span>
                <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${GRADE_STYLES[grade]}`}>
                  Grade {grade}
                </span>
              </div>
              <div className="w-7 h-7 flex items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                <ArrowUpRight className="w-3.5 h-3.5" />
              </div>
            </div>
          </div>'''

content = content.replace(old_rating_section, new_rating_section)

# Remove unused scorePercent variable and GRADE_BAR_COLORS if no longer needed
content = content.replace('  const scorePercent = Math.min((total / 10) * 100, 100);\n', '')
content = content.replace('''const GRADE_BAR_COLORS: Record<Grade, string> = {
  S: "bg-amber-600",
  A: "bg-green-600",
  B: "bg-blue-600",
  C: "bg-yellow-500",
  D: "bg-red-600",
  F: "bg-zinc-500",
};

''', '')

with open('components/tools/ToolCard.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('ToolCard optimized: removed filled background progress bar, replaced with number + grade display')
print('Removed unused scorePercent and GRADE_BAR_COLORS')
