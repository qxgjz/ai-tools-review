with open('app/blog/[slug]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace prose styles with more editorial typography
old_prose = '''        className="prose prose-lg dark:prose-invert max-w-none mb-10
          prose-headings:scroll-mt-24
          prose-h2:text-2xl prose-h2:font-bold prose-h2:mt-12 prose-h2:mb-4
          prose-h3:text-xl prose-h3:font-semibold prose-h3:mt-8 prose-h3:mb-3
          prose-p:leading-relaxed prose-p:mb-6 prose-p:text-gray-700 dark:prose-p:text-gray-300
          prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline
          prose-strong:text-gray-900 dark:prose-strong:text-white
          prose-ul:my-6 prose-li:mb-2
          prose-blockquote:border-l-4 prose-blockquote:border-blue-500 prose-blockquote:bg-blue-50 dark:prose-blockquote:bg-blue-900/10 prose-blockquote:py-2 prose-blockquote:px-4 prose-blockquote:rounded-r
          prose-img:rounded-xl prose-img:shadow-md prose-img:my-8
          prose-table:w-full prose-table:border-collapse prose-table:my-8
          prose-th:bg-gray-100 dark:prose-th:bg-gray-800 prose-th:p-3 prose-th:text-left prose-th:font-semibold
          prose-td:p-3 prose-td:border-b prose-td:border-gray-200 dark:prose-td:border-gray-700
          prose-code:bg-gray-100 dark:prose-code:bg-gray-800 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:text-pink-600 dark:prose-code:text-pink-400
          prose-pre:bg-gray-900 prose-pre:rounded-xl prose-pre:p-4 prose-pre:my-6 prose-pre:overflow-x-auto"'''

new_prose = '''        className="prose prose-lg dark:prose-invert max-w-none mb-10
          prose-headings:scroll-mt-24
          prose-h2:text-3xl prose-h2:font-bold prose-h2:mt-16 prose-h2:mb-6 prose-h2:tracking-tight prose-h2:text-gray-900 dark:prose-h2:text-white
          prose-h3:text-2xl prose-h3:font-semibold prose-h3:mt-12 prose-h3:mb-4 prose-h3:text-gray-800 dark:prose-h3:text-gray-200
          prose-p:leading-[1.85] prose-p:mb-8 prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-p:text-[1.05rem]
          prose-a:text-emerald-600 dark:prose-a:text-emerald-400 prose-a:no-underline hover:prose-a:underline prose-a:font-medium
          prose-strong:text-gray-900 dark:prose-strong:text-white prose-strong:font-semibold
          prose-ul:my-8 prose-li:mb-3 prose-li:leading-relaxed
          prose-blockquote:border-l-4 prose-blockquote:border-emerald-500 prose-blockquote:bg-emerald-50/50 dark:prose-blockquote:bg-emerald-900/10 prose-blockquote:py-4 prose-blockquote:px-6 prose-blockquote:rounded-r-lg prose-blockquote:my-8 prose-blockquote:italic prose-blockquote:text-gray-600 dark:prose-blockquote:text-gray-400
          prose-img:rounded-2xl prose-img:shadow-lg prose-img:my-10 prose-img:border prose-img:border-gray-200 dark:prose-img:border-gray-800
          prose-table:w-full prose-table:border-collapse prose-table:my-10 prose-table:text-sm
          prose-th:bg-gray-50 dark:prose-th:bg-gray-800/50 prose-th:p-4 prose-th:text-left prose-th:font-semibold prose-th:text-gray-900 dark:prose-th:text-white prose-th:border-b prose-th:border-gray-200 dark:prose-th:border-gray-700
          prose-td:p-4 prose-td:border-b prose-td:border-gray-100 dark:prose-td:border-gray-800 prose-td:text-gray-600 dark:prose-td:text-gray-400
          prose-code:bg-gray-100 dark:prose-code:bg-gray-800 prose-code:px-2 prose-code:py-1 prose-code:rounded-md prose-code:text-sm prose-code:text-pink-600 dark:prose-code:text-pink-400 prose-code:font-mono
          prose-pre:bg-gray-900 prose-pre:rounded-2xl prose-pre:p-6 prose-pre:my-8 prose-pre:overflow-x-auto prose-pre:text-sm
          first-letter:text-5xl first-letter:font-bold first-letter:float-left first-letter:mr-3 first-letter:leading-none first-letter:text-emerald-600 dark:first-letter:text-emerald-400 first-letter:mt-1"'''

content = content.replace(old_prose, new_prose)

with open('app/blog/[slug]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Article page optimized: editorial typography with drop cap, elegant blockquotes, improved hierarchy')
print('- Drop cap first letter (5xl, emerald, float left)')
print('- Larger H2/H3 with more spacing')
print('- Increased line height (1.85) for better readability')
print('- Elegant blockquote styling (emerald accent, italic, more padding)')
print('- Better image styling (rounded-2xl, shadow-lg, border)')
print('- Improved table styling (more padding, better contrast)')
