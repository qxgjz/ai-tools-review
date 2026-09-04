"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Home, Search, ArrowLeft, TrendingUp, Sparkles, FileText } from "lucide-react";
import tools from "@/data/tools.json";
import posts from "@/data/posts.json";
import { calculateScoreResult } from "@/lib/scoring";

export default function NotFound() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");

  // 获取热门工具（按评分排序，取前6个）
  const popularTools = [...tools]
    .sort((a, b) => {
      const scoreA = calculateScoreResult(a.scores).total;
      const scoreB = calculateScoreResult(b.scores).total;
      return scoreB - scoreA;
    })
    .slice(0, 6);

  // 热门分类
  const popularCategories = [
    { slug: "chat", name: "AI Chatbots", icon: "💬" },
    { slug: "image", name: "AI Image", icon: "🎨" },
    { slug: "writing", name: "AI Writing", icon: "✍️" },
    { slug: "code", name: "AI Coding", icon: "💻" },
    { slug: "video", name: "AI Video", icon: "🎬" },
    { slug: "audio", name: "AI Audio", icon: "🎵" },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-12">
      <div className="text-center max-w-2xl w-full">
        {/* 404 标题 */}
        <div className="mb-6">
          <h1 className="text-8xl md:text-9xl font-extrabold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
            404
          </h1>
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-3">
            Page Not Found
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
            The page you're looking for doesn't exist or has been moved.
            Try searching or explore our popular content below.
          </p>
        </div>

        {/* 搜索框 */}
        <form onSubmit={handleSearch} className="mb-10 max-w-md mx-auto">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search AI tools, reviews, comparisons..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>
          <button
            type="submit"
            className="mt-3 w-full sm:w-auto px-6 py-2.5 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Search
          </button>
        </form>

        {/* 快速导航按钮 */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center mb-12">
          <Link
            href="/"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            <Home className="w-4 h-4" />
            Back to Home
          </Link>
          <Link
            href="/blog"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg font-semibold border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 transition-colors"
          >
            <Sparkles className="w-4 h-4" />
            Browse Reviews
          </Link>
          <Link
            href="/compare"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg font-semibold border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 transition-colors"
          >
            <TrendingUp className="w-4 h-4" />
            Compare Tools
          </Link>
        </div>

        {/* 热门分类 */}
        <div className="mb-10">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
            Popular Categories
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {popularCategories.map((cat) => (
              <Link
                key={cat.slug}
                href={`/category/${cat.slug}`}
                className="flex items-center gap-2 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors text-left"
              >
                <span className="text-xl">{cat.icon}</span>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {cat.name}
                </span>
              </Link>
            ))}
          </div>
        </div>

        {/* 热门工具 */}
        <div className="mb-10">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
            Top Rated AI Tools
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {popularTools.map((tool) => {
              const result = calculateScoreResult(tool.scores);
              return (
                <Link
                  key={tool.slug}
                  href={`/tools/${tool.slug}`}
                  className="p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-100 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all text-left"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-semibold text-gray-900 dark:text-white truncate">
                      {tool.name}
                    </span>
                    <span className="text-xs font-bold text-blue-600 dark:text-blue-400">
                      {result.total.toFixed(1)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                    {tool.vendor}
                  </p>
                </Link>
              );
            })}
          </div>
        </div>

        {/* 最新文章 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Latest Reviews & Guides
          </h3>
          <div className="space-y-2">
            {posts.slice(0, 4).map((post: any) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="flex items-center gap-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-100 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all text-left"
              >
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-gray-900 dark:text-white truncate">
                    {post.title}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    {post.category} · {post.readTime} min read
                  </div>
                </div>
                <ArrowLeft className="w-4 h-4 text-gray-400 rotate-180 flex-shrink-0" />
              </Link>
            ))}
          </div>
          <div className="mt-4 text-center">
            <Link
              href="/blog"
              className="inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
            >
              View all articles
              <ArrowLeft className="w-3 h-3 rotate-180" />
            </Link>
          </div>
        </div>

        {/* 返回链接 */}
        <div className="mt-10">
          <button
            onClick={() => router.back()}
            className="inline-flex items-center gap-1 text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            <ArrowLeft className="w-4 h-4" />
            Go back to previous page
          </button>
        </div>
      </div>
    </div>
  );
}
