import Link from "next/link";
import {
  Home,
  Search,
  Trophy,
  Sparkles,
  FileText,
  Info,
  Shield,
  Mail,
  Download,
  Layers,
  ArrowRight,
  Clock,
} from "lucide-react";
import toolsData from "@/data/tools.json";
import postsData from "@/data/posts.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

// 分类配置
const CATEGORIES = [
  { slug: "chat", name: "AI Chat & Assistants", icon: "💬" },
  { slug: "writing", name: "AI Writing & Content", icon: "✍️" },
  { slug: "image", name: "AI Image & Art", icon: "🎨" },
  { slug: "code", name: "AI Coding & Dev", icon: "💻" },
  { slug: "video", name: "AI Video & Animation", icon: "🎬" },
  { slug: "audio", name: "AI Audio & Music", icon: "🎵" },
  { slug: "productivity", name: "AI Productivity", icon: "📊" },
  { slug: "search", name: "AI Search & Research", icon: "🔍" },
  { slug: "agent", name: "AI Agents & Automation", icon: "🤖" },
  { slug: "design", name: "AI Design & Creative", icon: "🎨" },
  { slug: "dev-tools", name: "AI Developer Tools", icon: "🛠️" },
  { slug: "database", name: "AI Database & Vector", icon: "🗄️" },
  { slug: "observability", name: "AI Observability", icon: "📈" },
];

// 主要页面
const MAIN_PAGES = [
  { href: "/", name: "Home", icon: Home, desc: "AI tools homepage with featured tools" },
  { href: "/ranking", name: "Tool Rankings", icon: Trophy, desc: "All AI tools ranked by 6-dimension score" },
  { href: "/generator", name: "AI Tool Matcher", icon: Sparkles, desc: "Find the perfect AI tool for your use case" },
  { href: "/compare", name: "Compare Tools", icon: Layers, desc: "Side-by-side comparison of AI tools" },
  { href: "/search", name: "Search", icon: Search, desc: "Search all AI tools and reviews" },
  { href: "/blog", name: "Blog & Reviews", icon: FileText, desc: "In-depth AI tool reviews and comparisons" },
  { href: "/free-ai-tools-guide", name: "Free AI Tools Guide", icon: Download, desc: "Download Top 50 AI tools guide (PDF)" },
];

// 信息页面
const INFO_PAGES = [
  { href: "/about", name: "About Us", icon: Info, desc: "Learn about AIToolCrux and our mission" },
  { href: "/privacy", name: "Privacy Policy", icon: Shield, desc: "How we handle your data and privacy" },
  { href: "/disclosure", name: "Affiliate Disclosure", icon: FileText, desc: "Transparency about affiliate relationships" },
  { href: "/contact", name: "Contact Us", icon: Mail, desc: "Get in touch with our team" },
];

export default function SitemapPage() {
  const tools = toolsData as Tool[];
  const posts = postsData;

  // 按分类分组工具
  const toolsByCategory: Record<string, Tool[]> = {};
  for (const tool of tools) {
    if (!toolsByCategory[tool.category]) {
      toolsByCategory[tool.category] = [];
    }
    toolsByCategory[tool.category].push(tool);
  }

  // 按评分排序每个分类的工具
  for (const cat of Object.keys(toolsByCategory)) {
    toolsByCategory[cat].sort(
      (a, b) => calculateScoreResult(b.scores).total - calculateScoreResult(a.scores).total
    );
  }

  // 热门工具（Top 20）
  const topTools = [...tools]
    .map((t) => ({ ...t, total: calculateScoreResult(t.scores).total }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 20);

  // 按分类分组博客文章
  const postsByCategory: Record<string, any[]> = {};
  for (const post of posts) {
    const cat = (post as any).category || "General";
    if (!postsByCategory[cat]) {
      postsByCategory[cat] = [];
    }
    postsByCategory[cat].push(post);
  }

  // 按发布日期排序每个分类的文章（最新的在前）
  for (const cat of Object.keys(postsByCategory)) {
    postsByCategory[cat].sort(
      (a, b) =>
        new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* 页面头部 */}
      <section className="bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 text-white py-16 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
              <Layers className="w-6 h-6" />
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold">Sitemap</h1>
          </div>
          <p className="text-blue-100 text-lg max-w-2xl">
            Complete overview of all pages on AIToolCrux. Browse by category,
            explore top-rated tools, and discover our latest reviews.
          </p>
          <div className="mt-6 flex flex-wrap gap-4 text-sm">
            <span className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full">
              <Layers className="w-4 h-4" /> {tools.length}+ Tools
            </span>
            <span className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full">
              <FileText className="w-4 h-4" /> {posts.length} Articles
            </span>
            <span className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full">
              <Clock className="w-4 h-4" /> Updated Daily
            </span>
          </div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-4 py-12">
        {/* 主要页面 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <Home className="w-6 h-6 text-blue-600" />
            Main Pages
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {MAIN_PAGES.map((page) => (
              <Link
                key={page.href}
                href={page.href}
                className="group bg-white dark:bg-gray-900 rounded-xl p-5 border border-gray-100 dark:border-gray-800 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-lg transition-all"
              >
                <div className="flex items-start justify-between mb-2">
                  <page.icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                  <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
                </div>
                <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                  {page.name}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {page.desc}
                </p>
              </Link>
            ))}
          </div>
        </section>

        {/* 分类页面 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <Layers className="w-6 h-6 text-purple-600" />
            Tool Categories
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {CATEGORIES.filter((cat) => toolsByCategory[cat.slug]?.length > 0).map(
              (cat) => (
                <Link
                  key={cat.slug}
                  href={`/category/${cat.slug}`}
                  className="group bg-white dark:bg-gray-900 rounded-xl p-5 border border-gray-100 dark:border-gray-800 hover:border-purple-300 dark:hover:border-purple-700 hover:shadow-lg transition-all"
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-2xl">{cat.icon}</span>
                    <span className="text-xs font-semibold text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/30 px-2 py-1 rounded-full">
                      {toolsByCategory[cat.slug]?.length || 0} tools
                    </span>
                  </div>
                  <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                    {cat.name}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Top: {toolsByCategory[cat.slug]?.[0]?.name || "N/A"}
                  </p>
                </Link>
              )
            )}
          </div>
        </section>

        {/* 热门工具 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <Trophy className="w-6 h-6 text-amber-500" />
            Top 20 Rated Tools
          </h2>
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 overflow-hidden">
            <div className="grid grid-cols-1 sm:grid-cols-2 divide-y sm:divide-y-0 sm:divide-x divide-gray-100 dark:divide-gray-800">
              {topTools.map((tool, index) => (
                <Link
                  key={tool.slug}
                  href={`/tools/${tool.slug}`}
                  className="flex items-center gap-3 p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                >
                  <span className="w-8 h-8 flex items-center justify-center bg-gradient-to-br from-amber-400 to-orange-500 text-white text-sm font-bold rounded-lg flex-shrink-0">
                    {index + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-gray-900 dark:text-white truncate">
                      {tool.name}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {tool.category} · {tool.vendor}
                    </div>
                  </div>
                  <span className="text-lg font-bold text-blue-600 dark:text-blue-400 flex-shrink-0">
                    {tool.total.toFixed(1)}
                  </span>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* 博客文章 - 按分类分组 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <FileText className="w-6 h-6 text-emerald-600" />
            All Articles & Reviews
          </h2>
          <div className="space-y-8">
            {Object.entries(postsByCategory).map(([category, categoryPosts]) => (
              <div key={category}>
                <div className="flex items-center gap-2 mb-4">
                  <span className="px-3 py-1 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-sm font-semibold rounded-full">
                    {category}
                  </span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {categoryPosts.length} articles
                  </span>
                  <Link
                    href={`/blog/category/${categoryPosts[0]?.categorySlug || category.toLowerCase()}`}
                    className="text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium ml-auto"
                  >
                    View all →
                  </Link>
                </div>
                <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 divide-y divide-gray-100 dark:divide-gray-800">
                  {categoryPosts.map((post: any) => (
                    <Link
                      key={post.slug}
                      href={`/blog/${post.slug}`}
                      className="flex items-center gap-4 p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                    >
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-gray-900 dark:text-white truncate">
                          {post.title}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {post.publishedAt} · {post.readTime} min read · {post.author}
                        </div>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-400 flex-shrink-0" />
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 信息页面 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            <Info className="w-6 h-6 text-gray-600" />
            Information Pages
          </h2>
          <div className="grid sm:grid-cols-2 gap-4">
            {INFO_PAGES.map((page) => (
              <Link
                key={page.href}
                href={page.href}
                className="group bg-white dark:bg-gray-900 rounded-xl p-5 border border-gray-100 dark:border-gray-800 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-lg transition-all"
              >
                <div className="flex items-start justify-between mb-2">
                  <page.icon className="w-6 h-6 text-gray-600 dark:text-gray-400" />
                  <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all" />
                </div>
                <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                  {page.name}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {page.desc}
                </p>
              </Link>
            ))}
          </div>
        </section>

        {/* XML Sitemap 链接 */}
        <section className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 rounded-2xl p-8 border border-blue-100 dark:border-blue-900/30 text-center">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            XML Sitemap for Search Engines
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Search engines can crawl our complete sitemap at the URL below.
          </p>
          <a
            href="/sitemap.xml"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            <FileText className="w-5 h-5" />
            View XML Sitemap
          </a>
        </section>
      </div>
    </div>
  );
}
