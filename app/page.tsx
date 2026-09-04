import Link from "next/link";
import dynamic from "next/dynamic";
import {
  Sparkles,
  Trophy,
  ArrowRight,
  MessageSquare,
  PenTool,
  Image as ImageIcon,
  Code,
  Video,
  Music,
  Briefcase,
  Search as SearchIcon,
  Bot,
  Palette,
  CheckCircle2,
  Star,
  Zap,
  Shield,
  Layers,
  TrendingUp,
  FileText,
} from "lucide-react";
import toolsData from "@/data/tools.json";
import postsData from "@/data/posts.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

// 动态导入重型组件，减少首屏JS包大小
const ToolList = dynamic(() => import("@/components/tools/ToolList").then(m => m.ToolList), {
  loading: () => <div className="animate-pulse h-64 bg-gray-100 dark:bg-gray-800 rounded-xl" />,
});
const NewsletterSignup = dynamic(() => import("@/components/monetization/NewsletterSignup").then(m => m.NewsletterSignup), {
  ssr: false,
  loading: () => null,
});

const CATEGORIES = [
  { slug: "chat", name: "AI对话", icon: MessageSquare, color: "from-blue-500 to-cyan-500" },
  { slug: "writing", name: "AI写作", icon: PenTool, color: "from-purple-500 to-pink-500" },
  { slug: "image", name: "AI绘画", icon: ImageIcon, color: "from-orange-500 to-red-500" },
  { slug: "code", name: "AI编程", icon: Code, color: "from-emerald-500 to-teal-500" },
  { slug: "video", name: "AI视频", icon: Video, color: "from-rose-500 to-orange-500" },
  { slug: "audio", name: "AI音频", icon: Music, color: "from-violet-500 to-purple-500" },
  { slug: "productivity", name: "AI办公", icon: Briefcase, color: "from-indigo-500 to-blue-500" },
  { slug: "search", name: "AI搜索", icon: SearchIcon, color: "from-sky-500 to-blue-500" },
  { slug: "agent", name: "AI Agent", icon: Bot, color: "from-indigo-500 to-purple-600" },
  { slug: "design", name: "AI设计", icon: Palette, color: "from-pink-500 to-rose-500" },
];

const METHODOLOGY = [
  { icon: Zap, title: "功能与输出质量", weight: "25%", desc: "核心功能完整性、输出准确性、用例覆盖" },
  { icon: Layers, title: "用户体验", weight: "20%", desc: "界面设计、上手曲线、文档质量" },
  { icon: Star, title: "价格与价值", weight: "20%", desc: "成本透明度、免费额度、投资回报率" },
  { icon: Code, title: "集成与开发者", weight: "15%", desc: "API 质量、平台兼容性、生态系统" },
  { icon: Shield, title: "支持与可靠性", weight: "10%", desc: "正常运行时间、更新频率、客服响应" },
  { icon: CheckCircle2, title: "伦理与透明度", weight: "10%", desc: "数据隐私、偏见披露、负责任 AI" },
];

export default function HomePage() {
  const tools = toolsData as Tool[];
  const topTools = [...tools]
    .map((t) => ({ ...t, total: calculateScoreResult(t.scores).total }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 8);

  const latestPosts = postsData.slice(0, 3);

  return (
    <div className="min-h-screen">
      {/* Schema.org 结构化数据 - WebSite */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: "AIToolCrux",
            alternateName: "AI工具测评台",
            url: "https://www.aitoolcrux.com",
            description: "Professional AI tool reviews, comparisons, and recommendations based on a six-dimensional evaluation framework. Discover the best AI tools for creators, developers, and businesses.",
            inLanguage: ["en", "zh-CN"],
            potentialAction: {
              "@type": "SearchAction",
              target: {
                "@type": "EntryPoint",
                urlTemplate: "https://www.aitoolcrux.com/search?q={search_term_string}",
              },
              "query-input": "required name=search_term_string",
            },
          }),
        }}
      />

      {/* Hero - 更现代的设计 */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950 text-white py-24 px-4">
        {/* 背景装饰 */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-0 right-1/4 w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-[120px] -translate-y-1/2" />
          <div className="absolute bottom-0 left-1/4 w-[400px] h-[400px] bg-purple-500/20 rounded-full blur-[100px] translate-y-1/2" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[150px]" />
        </div>

        {/* 网格背景 */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "linear-gradient(to right, white 1px, transparent 1px), linear-gradient(to bottom, white 1px, transparent 1px)",
            backgroundSize: "60px 60px",
          }}
        />

        <div className="relative max-w-5xl mx-auto text-center">
          {/* 标签 */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white/10 backdrop-blur-md rounded-full text-sm mb-8 border border-white/10">
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-blue-100">六维加权评分模型 · 专业独立测评</span>
          </div>

          {/* 主标题 */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold mb-6 leading-[1.1] tracking-tight">
            找到最适合你的
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent">
              AI 工具
            </span>
          </h1>

          {/* 副标题 */}
          <p className="text-lg sm:text-xl text-blue-200/80 mb-10 max-w-2xl mx-auto leading-relaxed">
            基于功能、体验、价格、集成、支持、伦理六维深度测评，
            <br className="hidden sm:block" />
            为你精选 {tools.length}+ 款优质 AI 工具，覆盖全品类
          </p>

          {/* CTA 按钮 */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
            <Link
              href="/generator"
              className="group inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-bold rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 hover:-translate-y-0.5 transition-all duration-300"
            >
              <Sparkles className="w-5 h-5" />
              智能匹配工具
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/ranking"
              className="inline-flex items-center gap-2 px-8 py-4 bg-white/10 backdrop-blur-md text-white font-bold rounded-xl border border-white/20 hover:bg-white/20 hover:border-white/30 transition-all duration-300"
            >
              <Trophy className="w-5 h-5 text-yellow-400" />
              查看排行榜
            </Link>
          </div>

          {/* Lead Magnet 小横幅 */}
          <Link
            href="/free-ai-tools-guide"
            className="inline-flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-amber-500/20 to-orange-500/20 backdrop-blur-md rounded-xl border border-amber-400/30 hover:border-amber-400/50 hover:from-amber-500/30 hover:to-orange-500/30 transition-all duration-300 group"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg flex items-center justify-center">
              <FileText className="w-4 h-4 text-white" />
            </div>
            <div className="text-left">
              <div className="text-sm font-bold text-amber-100">
                📚 免费下载：2026 AI工具指南
              </div>
              <div className="text-xs text-amber-200/70">
                Top 50工具深度测评 · 六维评分 · 可保存为PDF
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-amber-300 group-hover:translate-x-1 transition-transform" />
          </Link>

          {/* 统计数据 */}
          <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-12">
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                {tools.length}+
              </div>
              <div className="text-sm text-blue-300/70 mt-1">精选工具</div>
            </div>
            <div className="w-px h-12 bg-white/10 hidden sm:block" />
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                10
              </div>
              <div className="text-sm text-blue-300/70 mt-1">工具分类</div>
            </div>
            <div className="w-px h-12 bg-white/10 hidden sm:block" />
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                6
              </div>
              <div className="text-sm text-blue-300/70 mt-1">评分维度</div>
            </div>
            <div className="w-px h-12 bg-white/10 hidden sm:block" />
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                100%
              </div>
              <div className="text-sm text-blue-300/70 mt-1">独立测评</div>
            </div>
          </div>
        </div>

        {/* 底部波浪 */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full">
            <path
              d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z"
              className="fill-gray-50 dark:fill-gray-950"
            />
          </svg>
        </div>
      </section>

      {/* 分类网格 - 更精致的卡片 */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-20">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-sm font-medium mb-4">
            <Layers className="w-4 h-4" />
            全品类覆盖
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
            浏览分类
          </h2>
          <p className="text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
            从对话到绘画，从编程到视频，覆盖 AI 全场景应用
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {CATEGORIES.map((cat) => {
            const count = tools.filter((t) => t.category === cat.slug).length;
            const Icon = cat.icon;
            return (
              <Link
                key={cat.slug}
                href={`/category/${cat.slug}`}
                className="group relative p-6 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-xl hover:shadow-blue-500/10 dark:hover:shadow-blue-500/20 hover:border-blue-200 dark:hover:border-blue-800 hover:-translate-y-1 transition-all duration-300 overflow-hidden"
              >
                {/* 悬停渐变背景 */}
                <div
                  className={`absolute inset-0 bg-gradient-to-br ${cat.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}
                />

                <div className="relative">
                  <div
                    className={`w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-br ${cat.color} text-white shadow-lg mb-4 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300`}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-base font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {cat.name}
                  </h3>
                  <p className="text-sm text-gray-400 dark:text-gray-500 mt-1 flex items-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    {count} 款工具
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* 热门排行榜 */}
      <section className="bg-gray-50 dark:bg-gray-900/50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 rounded-full text-sm font-medium mb-4">
                <Trophy className="w-4 h-4" />
                精选推荐
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white">
                热门排行榜
              </h2>
              <p className="text-gray-500 dark:text-gray-400 mt-2">
                基于六维加权评分，为你精选最优质的 AI 工具
              </p>
            </div>
            <Link
              href="/ranking"
              className="group inline-flex items-center gap-2 px-5 py-2.5 bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 font-medium rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all"
            >
              查看全部
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          <ToolList tools={topTools} />
        </div>
      </section>

      {/* 测评方法论 - 新增区块 */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-20">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-full text-sm font-medium mb-4">
            <CheckCircle2 className="w-4 h-4" />
            专业方法论
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
            六维加权评分体系
          </h2>
          <p className="text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
            我们采用科学、可量化、可复现的六维评分框架，确保每一个评分都有依据
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {METHODOLOGY.map((item, index) => {
            const Icon = item.icon;
            return (
              <div
                key={index}
                className="group p-6 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-lg hover:border-blue-200 dark:hover:border-blue-800 transition-all duration-300"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-md group-hover:scale-110 transition-transform">
                    <Icon className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg text-sm font-bold">
                    {item.weight}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                  {item.title}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
                  {item.desc}
                </p>
              </div>
            );
          })}
        </div>

        <div className="mt-12 text-center">
          <Link
            href="/about"
            className="inline-flex items-center gap-2 text-blue-600 dark:text-blue-400 font-medium hover:text-blue-700 dark:hover:text-blue-300"
          >
            了解完整测评方法论
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* 最新博客 - 新增区块 */}
      {latestPosts.length > 0 && (
        <section className="bg-gray-50 dark:bg-gray-900/50 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 rounded-full text-sm font-medium mb-4">
                  <PenTool className="w-4 h-4" />
                  深度内容
                </div>
                <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white">
                  最新文章
                </h2>
                <p className="text-gray-500 dark:text-gray-400 mt-2">
                  AI 工具深度测评、选型指南、行业动态
                </p>
              </div>
              <Link
                href="/blog"
                className="group inline-flex items-center gap-2 px-5 py-2.5 bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 font-medium rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-md transition-all"
              >
                全部文章
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {latestPosts.map((post) => (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  className="group flex flex-col bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-xl hover:border-blue-200 dark:hover:border-blue-800 hover:-translate-y-1 transition-all duration-300 overflow-hidden"
                >
                  <div className="h-40 bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600 relative overflow-hidden">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <PenTool className="w-16 h-16 text-white/20" />
                    </div>
                    <div className="absolute top-4 left-4">
                      <span className="px-3 py-1 bg-white/20 backdrop-blur-sm text-white text-xs font-medium rounded-full">
                        {post.category}
                      </span>
                    </div>
                  </div>
                  <div className="p-6 flex-1 flex flex-col">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 mb-3">
                      {post.title}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-3 flex-1 mb-4">
                      {post.excerpt}
                    </p>
                    <div className="flex items-center justify-between text-xs text-gray-400 dark:text-gray-500">
                      <span>{post.publishedAt}</span>
                      <span className="inline-flex items-center gap-1 text-blue-600 dark:text-blue-400 font-medium group-hover:gap-2 transition-all">
                        阅读全文
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA 区域 - 新增区块 */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-20">
        <div className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 dark:from-blue-700 dark:via-indigo-700 dark:to-purple-800 rounded-3xl p-12 sm:p-16 text-center text-white">
          {/* 背景装饰 */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            <div className="absolute bottom-0 left-0 w-80 h-80 bg-white/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
          </div>

          <div className="relative">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white/15 backdrop-blur-sm rounded-full text-sm mb-6">
              <Sparkles className="w-4 h-4 text-yellow-300" />
              智能匹配
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold mb-6">
              不知道选哪个 AI 工具？
            </h2>
            <p className="text-lg text-blue-100 mb-10 max-w-2xl mx-auto">
              告诉我们你的使用场景和优先级，我们会基于六维评分模型为你智能匹配最适合的 AI 工具
            </p>
            <Link
              href="/generator"
              className="group inline-flex items-center gap-2 px-10 py-4 bg-white text-blue-600 font-bold rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all"
            >
              <Sparkles className="w-5 h-5" />
              开始智能匹配
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>

      {/* 邮件订阅 - 变现组件 */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 pb-20">
        <NewsletterSignup />
      </section>
    </div>
  );
}
