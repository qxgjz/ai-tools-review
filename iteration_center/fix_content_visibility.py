"""
Fix: properly add cv-auto class to below-the-fold sections on tool detail page.
Remove the accidental @ts-ignore comment.
"""

with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the accidental @ts-ignore comment
content = content.replace(
    '{/* Alternatives - E-E-A-T comparison signal (below fold - cv-auto) */}\n      {/* @ts-ignore */}',
    '{/* Alternatives - E-E-A-T comparison signal (below fold - cv-auto) */}'
)

# 2. Add cv-auto to Alternatives section
content = content.replace(
    '{/* Alternatives - E-E-A-T comparison signal (below fold - cv-auto) */}\n      {(tool as any).alternatives && (tool as any).alternatives.length > 0 && (\n        <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">',
    '{/* Alternatives - E-E-A-T comparison signal (below fold - cv-auto) */}\n      {(tool as any).alternatives && (tool as any).alternatives.length > 0 && (\n        <section className="cv-auto bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">'
)

# 3. Add cv-auto to Related recommendations section
content = content.replace(
    '{/* Related recommendations (below fold - cv-auto) */}\n      {relatedTools.length > 0 && (\n        <section className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-100 dark:border-zinc-800 shadow-sm p-6 mb-6">',
    '{/* Related recommendations (below fold - cv-auto) */}\n      {relatedTools.length > 0 && (\n        <section className="cv-auto bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-100 dark:border-zinc-800 shadow-sm p-6 mb-6">'
)

# 4. Add cv-auto to Popular tools section
content = content.replace(
    '{/* 跨分类热门工具推荐 - P1-004 增加重要工具入链 */}\n      {popularTools.length > 0 && (\n        <section className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20 rounded-2xl border border-amber-100 dark:border-amber-900/50 shadow-sm p-6 mb-6">',
    '{/* 跨分类热门工具推荐 - P1-004 增加重要工具入链 (below fold - cv-auto) */}\n      {popularTools.length > 0 && (\n        <section className="cv-auto bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20 rounded-2xl border border-amber-100 dark:border-amber-900/50 shadow-sm p-6 mb-6">'
)

# 5. Add cv-auto to Comparison pages section
content = content.replace(
    '{/* Comparison pages - hub-and-spoke internal linking */}\n      {relevantComparisons.length > 0 && (\n        <section className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/20 dark:to-teal-950/20 rounded-2xl border border-emerald-100 dark:border-emerald-900/50 shadow-sm p-6 mb-6">',
    '{/* Comparison pages - hub-and-spoke internal linking (below fold - cv-auto) */}\n      {relevantComparisons.length > 0 && (\n        <section className="cv-auto bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/20 dark:to-teal-950/20 rounded-2xl border border-emerald-100 dark:border-emerald-900/50 shadow-sm p-6 mb-6">'
)

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    verify = f.read()

count = verify.count('cv-auto')
print(f"[OK] cv-auto applied {count} times in tool detail page")
print(f"[OK] @ts-ignore removed: {'@ts-ignore' not in verify}")
