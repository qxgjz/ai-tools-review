with open('app/tools/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if FadeIn is already imported
if 'FadeIn' not in content:
    # Add FadeIn import after other imports
    content = content.replace(
        'import { calculateScoreResult } from "@/lib/scoring";',
        'import { calculateScoreResult } from "@/lib/scoring";\nimport { FadeIn } from "@/components/animations";'
    )
    print('Added FadeIn import')

# Wrap Quick Answer section with FadeIn
content = content.replace(
    '      {/* AEO/GEO Optimization: Quick Answer - Answer First for AI Search Citation */}\n      <section className="bg-emerald-50',
    '      {/* AEO/GEO Optimization: Quick Answer - Answer First for AI Search Citation */}\n      <FadeIn delay={0.1} y={20}>\n      <section className="bg-emerald-50'
)

# Close FadeIn after Quick Answer section (before Key Takeaways)
content = content.replace(
    '      </section>\n\n      {/* AEO/GEO Optimization: Key Takeaways',
    '      </section>\n      </FadeIn>\n\n      {/* AEO/GEO Optimization: Key Takeaways'
)

# Wrap Key Takeaways section with FadeIn
content = content.replace(
    '      {/* AEO/GEO Optimization: Key Takeaways - Structured for AI Citation */}\n      <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">',
    '      {/* AEO/GEO Optimization: Key Takeaways - Structured for AI Citation */}\n      <FadeIn delay={0.2} y={20}>\n      <section className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 mb-6">'
)

# Close FadeIn after Key Takeaways section (before Author Bio)
content = content.replace(
    '      </section>\n\n      {/* Author Bio - E-E-A-T Expertise & Authoritativeness signal */}',
    '      </section>\n      </FadeIn>\n\n      {/* Author Bio - E-E-A-T Expertise & Authoritativeness signal */}'
)

with open('app/tools/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Tool detail page motion optimized: added FadeIn scroll reveal to Quick Answer and Key Takeaways sections')
