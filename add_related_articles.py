import re

filepath = 'app/tools/[slug]/page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 添加posts数据导入
old_import = 'import toolsData from "@/data/tools.json";'
new_import = 'import toolsData from "@/data/tools.json";\nimport postsData from "@/data/posts.json";'
content = content.replace(old_import, new_import)
print("✓ Added postsData import")

# 2. 在relatedTools计算之后添加relatedArticles计算
old_related_tools = '''  const relatedTools = toolsData
    .filter((t) => t.category === tool.category && t.slug !== tool.slug)
    .slice(0, 6);'''

new_related_tools = '''  const relatedTools = toolsData
    .filter((t) => t.category === tool.category && t.slug !== tool.slug)
    .slice(0, 6);

  // 智能Related Articles推荐：工具名匹配(50%) + 分类匹配(30%) + 标签匹配(20%)
  const toolNameWords = tool.name.toLowerCase().split(/\\s+/).filter(w => w.length > 2);
  const relatedArticles = postsData
    .filter((p: any) => p.slug !== `${tool.slug}-review-2026`)
    .map((post: any) => {
      let relevance = 0;
      const postTitle = post.title.toLowerCase();
      const postTags = (post.tags || []).map((t: string) => t.toLowerCase());
      const postCategory = (post.category || "").toLowerCase();

      // 工具名匹配（最高权重）
      for (const word of toolNameWords) {
        if (postTitle.includes(word)) relevance += 15;
        if (postTags.includes(word)) relevance += 10;
      }
      if (postTitle.includes(tool.name.toLowerCase())) relevance += 25;

      // 分类匹配
      if (postCategory.includes(tool.category) || tool.category.includes(postCategory)) {
        relevance += 20;
      }

      // 标签匹配
      const categoryKeywords: Record<string, string[]> = {
        code: ["coding", "programming", "developer", "code", "software"],
        chat: ["chatbot", "conversation", "assistant", "chat", "ai assistant"],
        writing: ["writing", "content", "copywriting", "text"],
        image: ["image", "art", "design", "visual", "generation"],
        video: ["video", "animation", "editing", "motion"],
        audio: ["audio", "music", "voice", "speech", "sound"],
        productivity: ["productivity", "workflow", "automation", "efficiency"],
        agent: ["agent", "autonomous", "automation", "workflow"],
        search: ["search", "research", "discovery", "find"],
      };
      const keywords = categoryKeywords[tool.category] || [];
      for (const kw of keywords) {
        if (postTitle.includes(kw) || postTags.includes(kw)) relevance += 8;
      }

      return { post, relevance };
    })
    .filter((item: any) => item.relevance > 0)
    .sort((a: any, b: any) => b.relevance - a.relevance)
    .slice(0, 4)
    .map((item: any) => item.post);'''

content = content.replace(old_related_tools, new_related_tools)
print("✓ Added relatedArticles calculation")

# 3. 在Similar Tools Recommended部分之后添加Related Articles部分
old_similar_tools_end = '''          <ToolList tools={relatedTools} />
        </div>
      )}'''

new_similar_tools_end = '''          <ToolList tools={relatedTools} />
        </div>
      )}

      {/* Related Articles - 双向内链闭环 */}
      {relatedArticles.length > 0 && (
        <div className="mt-12 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                Related Articles & Guides
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                In-depth reviews and comparisons related to {tool.name}
              </p>
            </div>
            <Link
              href="/blog"
              className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
            >
              View all articles
              <ArrowLeft className="w-4 h-4 rotate-180" />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {relatedArticles.map((article: any) => (
              <Link
                key={article.slug}
                href={`/blog/${article.slug}`}
                className="block bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 hover:shadow-lg hover:border-blue-300 dark:hover:border-blue-700 transition-all"
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-0.5 rounded">
                    {article.category || "AI Tools"}
                  </span>
                  <span className="text-xs text-gray-400">{article.readTime || "5"} min read</span>
                </div>
                <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  {article.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                  {article.excerpt || article.description || ""}
                </p>
              </Link>
            ))}
          </div>
        </div>
      )}'''

content = content.replace(old_similar_tools_end, new_similar_tools_end)
print("✓ Added Related Articles section to UI")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== Related Articles Addition Complete ===")
print("  - Added postsData import")
print("  - Added smart related articles calculation (name/category/tags matching)")
print("  - Added Related Articles UI section with 4 articles")
print("  - Creates bidirectional internal linking: tool page -> article page")
print("  - Article pages already have Related Tools section (article -> tool)")
