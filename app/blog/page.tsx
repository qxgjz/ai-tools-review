import Link from "next/link";
import posts from "@/data/posts.json";
import { BlogListClient } from "@/components/blog/BlogListClient";
import { Rss } from "lucide-react";

export const metadata = {
  title: "Blog - AI Tool Reviews & Comparisons | AIToolCrux",
  description: "Expert AI tool reviews, comparisons, buying guides, and industry news. Find the best AI tools for your needs with our 6-dimension evaluation methodology.",
};

export default function BlogPage() {
  const allPosts = posts as any[];
  const featuredPosts = allPosts.filter((p) => p.featured);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      {/* 页面标题 */}
      <div className="mb-8 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Blog & Reviews
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Expert AI tool reviews, comparisons, and buying guides
          </p>
        </div>
        <a
          href="/rss.xml"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-4 py-2 bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400 rounded-lg border border-orange-200 dark:border-orange-800 hover:bg-orange-100 dark:hover:bg-orange-900/30 transition-colors text-sm font-medium"
        >
          <Rss className="w-4 h-4" />
          Subscribe RSS
        </a>
      </div>

      {/* 精选文章 */}
      {featuredPosts.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Featured Articles
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {featuredPosts.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="block bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl border border-blue-100 dark:border-blue-900/30 p-6 hover:shadow-lg hover:border-blue-200 dark:hover:border-blue-800 transition-all"
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs font-medium text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded">
                    Featured
                  </span>
                  <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-1 rounded">
                    {post.category}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {post.readTime} min read
                  </span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  {post.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-3">
                  {post.excerpt}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                  <span>{post.author}</span>
                  <span>{post.publishedAt}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* 全部文章 - 带筛选和排序 */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          All Articles
        </h2>
        <BlogListClient posts={allPosts} />
      </div>
    </div>
  );
}
