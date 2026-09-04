"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Filter, ArrowUpDown, Check } from "lucide-react";

type SortOption = "newest" | "oldest" | "title";
type CategoryFilter = "all" | string;

interface Post {
  slug: string;
  title: string;
  excerpt: string;
  category: string;
  categorySlug: string;
  tags: string[];
  author: string;
  publishedAt: string;
  readTime: number;
  featured: boolean;
}

interface BlogListClientProps {
  posts: Post[];
}

export function BlogListClient({ posts }: BlogListClientProps) {
  const [sortBy, setSortBy] = useState<SortOption>("newest");
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>("all");

  // 获取所有Categories
  const categories = useMemo(() => {
    const catSet = new Set<string>();
    posts.forEach((p) => catSet.add(p.category));
    return Array.from(catSet).sort();
  }, [posts]);

  // 筛选和排序文章
  const filteredAndSortedPosts = useMemo(() => {
    let result = [...posts];

    // 按Categories筛选
    if (categoryFilter !== "all") {
      result = result.filter((post) => post.category === categoryFilter);
    }

    // 排序
    switch (sortBy) {
      case "newest":
        result.sort(
          (a, b) =>
            new Date(b.publishedAt).getTime() -
            new Date(a.publishedAt).getTime()
        );
        break;
      case "oldest":
        result.sort(
          (a, b) =>
            new Date(a.publishedAt).getTime() -
            new Date(b.publishedAt).getTime()
        );
        break;
      case "title":
        result.sort((a, b) => a.title.localeCompare(b.title));
        break;
    }

    return result;
  }, [posts, sortBy, categoryFilter]);

  const sortOptions: { value: SortOption; label: string }[] = [
    { value: "newest", label: "Newest First" },
    { value: "oldest", label: "Oldest First" },
    { value: "title", label: "Title A-Z" },
  ];

  return (
    <div className="mb-8">
      {/* 筛选和排序Tools栏 */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800">
        {/* Categories筛选 */}
        <div className="flex items-center gap-2 flex-wrap">
          <Filter className="w-4 h-4 text-gray-500 dark:text-gray-400 flex-shrink-0" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300 mr-2">
            Category:
          </span>
          <div className="flex gap-1 flex-wrap">
            <button
              onClick={() => setCategoryFilter("all")}
              className={`px-3 py-1.5 text-sm rounded-lg font-medium transition-all ${
                categoryFilter === "all"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
            >
              All
            </button>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategoryFilter(cat)}
                className={`px-3 py-1.5 text-sm rounded-lg font-medium transition-all ${
                  categoryFilter === cat
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* 排序选项 */}
        <div className="flex items-center gap-2">
          <ArrowUpDown className="w-4 h-4 text-gray-500 dark:text-gray-400 flex-shrink-0" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Sort:
          </span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortOption)}
            className="px-3 py-1.5 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {sortOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 结果Statistics */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Showing{" "}
          <span className="font-semibold text-gray-900 dark:text-white">
            {filteredAndSortedPosts.length}
          </span>{" "}
          of <span className="font-semibold">{posts.length}</span> articles
          {categoryFilter !== "all" && (
            <span className="ml-1">
              · filtered by{" "}
              <span className="font-medium text-blue-600 dark:text-blue-400">
                {categoryFilter}
              </span>
            </span>
          )}
        </p>
        {categoryFilter !== "all" && (
          <button
            onClick={() => setCategoryFilter("all")}
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium flex items-center gap-1"
          >
            <Check className="w-3 h-3" />
            Clear filter
          </button>
        )}
      </div>

      {/* 文章列Table */}
      {filteredAndSortedPosts.length > 0 ? (
        <div className="space-y-4">
          {filteredAndSortedPosts.map((post) => (
            <Link
              key={post.slug}
              href={`/blog/${post.slug}`}
              className="block bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-6 hover:shadow-md dark:hover:shadow-lg hover:border-blue-200 dark:hover:border-blue-800 transition-all"
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-1 rounded">
                  {post.category}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {post.readTime} min read
                </span>
                {post.featured && (
                  <span className="text-xs font-medium text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded">
                    Featured
                  </span>
                )}
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                {post.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">
                {post.excerpt}
              </p>
              <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                <span>{post.author}</span>
                <span>{post.publishedAt}</span>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800">
          <p className="text-gray-500 dark:text-gray-400 mb-2">
            No articles found in this category.
          </p>
          <button
            onClick={() => setCategoryFilter("all")}
            className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
          >
            View all articles
          </button>
        </div>
      )}
    </div>
  );
}
