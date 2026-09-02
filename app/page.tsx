import Link from "next/link";
import { Sparkles, Trophy, ArrowRight, MessageSquare, PenTool, Image as ImageIcon, Code, Video, Music, Briefcase, Search as SearchIcon, Bot, Palette } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { ToolList } from "@/components/tools/ToolList";

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

export default function HomePage() {
  const tools = toolsData as Tool[];
  const topTools = [...tools]
    .map((t) => ({ ...t, total: calculateScoreResult(t.scores).total }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 8);

  return (
    <div className="min-h-screen">
      {/* Schema.org 结构化数据 */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: "AI工具测评台",
            url: "https://www.aitoolcrux.com",
            description: "基于六维加权评分模型的专业AI工具测评与导航平台",
            potentialAction: {
              "@type": "SearchAction",
              target: "https://www.aitoolcrux.com/search?q={search_term_string}",
              "query-input": "required name=search_term_string",
            },
          }),
        }}
      />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 text-white py-20 px-4">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-white/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white/15 backdrop-blur-sm rounded-full text-sm mb-6">
            <Sparkles className="w-4 h-4" />
            六维加权评分模型 · 专业测评
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
            找到最适合你的
            <br />
            <span className="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">AI 工具</span>
          </h1>
          <p className="text-lg sm:text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            基于功能、体验、价格、集成、支持、伦理六维评分，为你精选最优质的AI工具，覆盖全品类
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/generator" className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 font-bold rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all">
              <Sparkles className="w-5 h-5" />
              智能匹配工具
            </Link>
            <Link href="/ranking" className="inline-flex items-center gap-2 px-8 py-4 bg-white/15 backdrop-blur-sm text-white font-bold rounded-xl border border-white/20 hover:bg-white/25 transition-all">
              <Trophy className="w-5 h-5" />
              查看排行榜
            </Link>
          </div>
          <div className="mt-10 flex items-center justify-center gap-8 text-sm text-blue-200">
            <div><span className="text-2xl font-bold text-white">{tools.length}+</span><br />精选工具</div>
            <div className="w-px h-10 bg-white/20" />
            <div><span className="text-2xl font-bold text-white">8</span><br />工具分类</div>
            <div className="w-px h-10 bg-white/20" />
            <div><span className="text-2xl font-bold text-white">6</span><br />评分维度</div>
          </div>
        </div>
      </section>

      {/* 分类网格 */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">浏览分类</h2>
          <Link href="/ranking" className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1">
            全部工具 <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {CATEGORIES.map((cat) => {
            const count = tools.filter((t) => t.category === cat.slug).length;
            const Icon = cat.icon;
            return (
              <Link key={cat.slug} href={`/category/${cat.slug}`} className="group p-5 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:shadow-blue-500/10 hover:border-blue-200 hover:-translate-y-1 transition-all duration-300">
                <div className={`w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-br ${cat.color} text-white shadow-md mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{cat.name}</h3>
                <p className="text-sm text-gray-400 mt-1">{count} 款工具</p>
              </Link>
            );
          })}
        </div>
      </section>

      {/* 热门排行榜 */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 pb-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900 flex items-center gap-2">
            <Trophy className="w-7 h-7 text-amber-500" />
            热门排行榜
          </h2>
          <Link href="/ranking" className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1">
            查看全部 <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        <ToolList tools={topTools} />
      </section>
    </div>
  );
}
