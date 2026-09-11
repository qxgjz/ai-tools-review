import re

filepath = r"app\blog\[slug]\page.tsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 添加import（已经添加了，检查一下）
if 'ReadingProgress' not in content:
    content = content.replace(
        'import { ToolScreenshot } from "@/components/content/ToolScreenshot";',
        'import { ToolScreenshot } from "@/components/content/ToolScreenshot";\nimport { ReadingProgress } from "@/components/blog/ReadingProgress";\nimport { TableOfContents } from "@/components/blog/TableOfContents";\nimport { PostNavigation } from "@/components/blog/PostNavigation";'
    )

# 2. 修改return部分 - 添加阅读进度条和布局
old_return = '''  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">'''

new_return = '''  // 计算上一篇/下一篇文章
  const currentIndex = posts.findIndex((p) => p.slug === post.slug);
  const previousPost = currentIndex > 0 ? posts[currentIndex - 1] : undefined;
  const nextPost = currentIndex < posts.length - 1 ? posts[currentIndex + 1] : undefined;

  return (
    <>
      {/* 阅读进度条 */}
      <ReadingProgress />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* 主内容区 - 优化排版 */}
          <div className="flex-1 min-w-0 max-w-3xl">'''

content = content.replace(old_return, new_return)

# 3. 修改文章内容区域 - 优化prose样式
old_article = '''      {/* 文章内容 */}
      <article
        className="prose prose-lg dark:prose-invert max-w-none mb-10"
        dangerouslySetInnerHTML={{ __html: post.content }}
      />'''

new_article = '''      {/* 文章内容 - 优化排版：行高1.75，段落间距，最大阅读宽度 */}
      <article
        className="prose prose-lg dark:prose-invert max-w-none mb-10
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
          prose-pre:bg-gray-900 prose-pre:rounded-xl prose-pre:p-4 prose-pre:my-6 prose-pre:overflow-x-auto"
        dangerouslySetInnerHTML={{ __html: post.content }}
      />'''

content = content.replace(old_article, new_article)

# 4. 在相关文章之前添加上下篇导航
old_related_tools = '''      {/* 相关Tools推荐 */}'''

new_related_tools = '''      {/* 上一篇/下一篇导航 */}
      <div className="mb-12">
        <PostNavigation
          previousPost={previousPost}
          nextPost={nextPost}
        />
      </div>

      {/* 相关Tools推荐 */}'''

content = content.replace(old_related_tools, new_related_tools)

# 5. 在文件末尾添加右侧目录边栏并关闭标签
# 找到最后的</div>和</div>（主内容和外层）
old_ending = '''      {/* Comments */}
      <section className="border-t border-gray-200 dark:border-gray-800 pt-10">
        <Giscus />
      </section>
    </div>
  );
}'''

new_ending = '''      {/* Comments */}
      <section className="border-t border-gray-200 dark:border-gray-800 pt-10">
        <Giscus />
      </section>
          </div>

          {/* 右侧边栏 - 目录（桌面端固定） */}
          <aside className="hidden lg:block w-64 flex-shrink-0">
            <div className="sticky top-24">
              <TableOfContents contentHtml={post.content} />
            </div>
          </aside>
        </div>
      </div>
    </>
  );
}'''

content = content.replace(old_ending, new_ending)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Blog layout updated successfully!")
print("Added: ReadingProgress, TableOfContents sidebar, PostNavigation")
print("Optimized: prose typography, spacing, layout")
