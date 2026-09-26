with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace GRADE_STYLES gradients with solid colors
old_grade_styles = '''const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white",
};'''

new_grade_styles = '''const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-amber-700 text-white",
  A: "bg-green-700 text-white",
  B: "bg-blue-700 text-white",
  C: "bg-yellow-600 text-white",
  D: "bg-red-700 text-white",
  F: "bg-zinc-500 text-white",
};'''

content = content.replace(old_grade_styles, new_grade_styles)

# 2. Replace tool logo gradient with neutral color
old_logo = '''<div className="w-20 h-20 flex-shrink-0 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-3xl font-extrabold shadow-lg">'''
new_logo = '''<div className="w-20 h-20 flex-shrink-0 flex items-center justify-center rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-3xl font-bold">'''
content = content.replace(old_logo, new_logo)

# 3. Replace score number gradient with solid color
old_score = '''<div className="text-5xl font-extrabold bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">{total.toFixed(1)}</div>'''
new_score = '''<div className="text-5xl font-bold text-zinc-900 dark:text-white">{total.toFixed(1)}</div>'''
content = content.replace(old_score, new_score)

# 4. Replace CTA button gradient with solid color
old_cta = '''<a href={(tool as any).affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold rounded-xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all">'''
new_cta = '''<a href={(tool as any).affiliateUrl || tool.officialUrl} target="_blank" rel="noopener noreferrer sponsored" className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition-colors">'''
content = content.replace(old_cta, new_cta)

# 5. Replace Quick Answer gradient background with solid background
old_qa_bg = '''<section className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 rounded-2xl border border-blue-100 dark:border-blue-900/50 p-6 sm:p-8 mb-6">'''
new_qa_bg = '''<section className="bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-100 dark:border-emerald-900/50 p-6 sm:p-8 mb-6">'''
content = content.replace(old_qa_bg, new_qa_bg)

# 6. Replace Quick Answer icon color
old_qa_icon = '''<Zap className="w-5 h-5 text-blue-600 dark:text-blue-400" />'''
new_qa_icon = '''<Zap className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />'''
content = content.replace(old_qa_icon, new_qa_icon)

# 7. Replace score progress bar gradient with solid color
old_progress = '''<div className="h-2.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-700" style={{ width: `${percent}%` }} />
                  </div>'''
new_progress = '''<div className="h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-emerald-500 transition-all duration-500" style={{ width: `${percent}%` }} />
                  </div>'''
content = content.replace(old_progress, new_progress)

# 8. Replace section card styling - unified radius and shadow
old_card = '''bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6'''
new_card = '''bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6'''
content = content.replace(old_card, new_card)

# 9. Replace header card styling
old_header_card = '''<section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-6">'''
new_header_card = '''<section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">'''
content = content.replace(old_header_card, new_header_card)

# 10. Replace text colors - gray to zinc
content = content.replace('text-gray-900', 'text-zinc-900')
content = content.replace('text-gray-700', 'text-zinc-700')
content = content.replace('text-gray-600', 'text-zinc-600')
content = content.replace('text-gray-500', 'text-zinc-500')
content = content.replace('text-gray-400', 'text-zinc-400')
content = content.replace('bg-gray-900', 'bg-zinc-900')
content = content.replace('bg-gray-100', 'bg-zinc-100')
content = content.replace('bg-gray-50', 'bg-zinc-50')
content = content.replace('border-gray-100', 'border-zinc-100')
content = content.replace('border-gray-800', 'border-zinc-800')
content = content.replace('border-gray-200', 'border-zinc-200')

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Tool detail page updated successfully')
