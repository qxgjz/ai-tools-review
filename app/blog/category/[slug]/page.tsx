import Link from "next/link";
import { notFound } from "next/navigation";
import posts from "@/data/posts.json";

export const dynamic = "force-dynamic";

interface CategoryPageProps {
  params: { slug: string };
}

export function generateMetadata({ params }: CategoryPageProps) {
  const categoryPosts = posts.filter((p) => p.categorySlug === params.slug);
  const categoryName = categoryPosts.length > 0 ? categoryPosts[0].category : params.slug;
  return {
    title: `${categoryName} - AI工具测评台博客`,
    description: `AI工具测评台博客 - ${categoryName}分类的所有文章`,
  };
}

export default function CategoryPage({ params }: CategoryPageProps) {
  const categoryPosts = posts.filter((p) => p.categorySlug === params.slug);

  if (categoryPosts.length === 0) {
    notFound();
  }

  const categoryName = categoryPosts[0].category;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      {/* 返回按钮 */}
      <Link
        href="/blog"
        className="inline-flex items-center text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 mb-8 transition-colors"
      >
        ← 返回博客列表
      </Link>

      {/* 分类标题 */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          分类：{categoryName}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">共 {categoryPosts.length} 篇文章</p>
      </div>

      {/* 文章列表 */}
      <div className="space-y-4">
        {categoryPosts.map((post) => (
          <Link
            key={post.slug}
            href={`/blog/${post.slug}`}
            className="block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-md dark:hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center gap-2 mb-2">
              <Link
                href={`/blog/category/${post.categorySlug}`}
                className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-1 rounded hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
              >
                {post.category}
              </Link>
              <span className="text-xs text-gray-500 dark:text-gray-400">{post.readTime} 分钟阅读</span>
            </div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              {post.title}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">{post.excerpt}</p>
            <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <span>{post.author}</span>
              <span>{post.publishedAt}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
