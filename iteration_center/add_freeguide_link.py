"""Add a /free-ai-tools-guide internal link banner to blog post pages"""

with open('app/blog/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The insertion point: right before the "Related Articles" section
# We look for the comment marker {/* Related Articles - 智能推荐 */}
old_marker = '      {/* Related Articles - 智能推荐 */}'

free_guide_banner = '''      {/* Free AI Tools Guide cross-link */}
      <section className="mb-16">
        <Link
          href="/free-ai-tools-guide"
          className="block bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/10 dark:to-teal-900/10 rounded-xl border border-emerald-200 dark:border-emerald-900/30 p-6 hover:shadow-lg transition-all"
        >
          <div className="flex items-center gap-3">
            <div className="flex-1">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                Looking for free AI tools?
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Browse our curated guide to AI tools with no credit card required and no hidden fees.
              </p>
            </div>
            <span className="inline-flex items-center gap-1 text-sm font-medium text-emerald-600 dark:text-emerald-400 whitespace-nowrap">
              View Guide <ArrowRight className="w-4 h-4" />
            </span>
          </div>
        </Link>
      </section>

      {/* Related Articles - 智能推荐 */}'''

if old_marker in content:
    content = content.replace(old_marker, free_guide_banner)
    print("[OK] Added free-ai-tools-guide cross-link banner")
else:
    print("[ERROR] Could not find the Related Articles marker")

with open('app/blog/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('app/blog/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    verify = f.read()
print(f"  Free guide link present: {'/free-ai-tools-guide' in verify}")
print(f"  Related Tools still present: {'Related AI Tools' in verify}")
print(f"  Related Articles still present: {'You might also like' in verify}")
