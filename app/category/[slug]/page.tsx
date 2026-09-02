import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, MessageSquare, PenTool, Image as ImageIcon, Code, Video, Music, Briefcase, Search as SearchIcon, Layers, Palette, Bot } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { ToolList } from "@/components/tools/ToolList";

const CATEGORIES: Record<string, { name: string; description: string; icon: LucideIcon; gradient: string }> = {
  chat: { name: "AI 对话助手", description: "智能对话、问答交互、多轮聊天", icon: MessageSquare, gradient: "from-blue-600 to-cyan-500" },
  writing: { name: "AI 写作工具", description: "文章撰写、文案创作、内容润色", icon: PenTool, gradient: "from-purple-600 to-pink-500" },
  image: { name: "AI 绘画设计", description: "图像生成、艺术创作、设计辅助", icon: ImageIcon, gradient: "from-orange-500 to-red-500" },
  code: { name: "AI 编程开发", description: "代码生成、程序开发、技术辅助", icon: Code, gradient: "from-emerald-600 to-teal-500" },
  video: { name: "AI 视频制作", description: "视频生成、剪辑制作、多媒体创作", icon: Video, gradient: "from-rose-500 to-orange-500" },
  audio: { name: "AI 音频音乐", description: "语音合成、音乐生成、音频处理", icon: Music, gradient: "from-violet-600 to-purple-500" },
  productivity: { name: "AI 效率办公", description: "文档处理、会议纪要、团队协作", icon: Briefcase, gradient: "from-indigo-600 to-blue-500" },
  search: { name: "AI 智能搜索", description: "智能搜索、信息检索、知识问答", icon: SearchIcon, gradient: "from-sky-600 to-blue-500" },
  agent: { name: "AI Agent 框架", description: "智能体开发、自动化工作流、自主AI系统", icon: Bot, gradient: "from-indigo-600 to-purple-600" },
  design: { name: "AI 设计工具", description: "UI设计、原型制作、创意设计辅助", icon: Palette, gradient: "from-pink-500 to-rose-500" },
};

export function generateStaticParams() {
  const categories = new Set(toolsData.map((t) => t.category));
  return Array.from(categories).map((slug) => ({ slug }));
}

export default function CategoryPage({ params }: { params: { slug: string } }) {
  const category = CATEGORIES[params.slug];
  if (!category) notFound();

  const Icon = category.icon;
  const tools = toolsData.filter((t) => t.category === params.slug) as Tool[];
  const sortedTools = [...tools].sort((a, b) => calculateScoreResult(b.scores).total - calculateScoreResult(a.scores).total);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 bg-white rounded-xl border border-gray-200 shadow-sm hover:border-blue-300 hover:text-blue-600 transition-all">
        <ArrowLeft className="w-4 h-4" />
        返回首页
      </Link>

      <section className={`relative overflow-hidden rounded-2xl bg-gradient-to-r ${category.gradient} p-8 text-white mb-8 shadow-lg`}>
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-2xl" />
        <div className="relative flex items-center gap-6">
          <div className="w-16 h-16 flex items-center justify-center rounded-2xl bg-white/20 backdrop-blur-sm shadow-lg flex-shrink-0">
            <Icon className="w-8 h-8" />
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-3xl font-extrabold mb-2">{category.name}</h1>
            <p className="text-white/80">{category.description}</p>
          </div>
          <div className="text-center flex-shrink-0">
            <div className="text-4xl font-extrabold">{sortedTools.length}</div>
            <div className="text-sm text-white/70">款工具</div>
          </div>
        </div>
      </section>

      <ToolList tools={sortedTools} emptyTitle="该分类暂无工具" emptyDescription="敬请期待，我们正在持续收录更多优质工具。" />

      <section className="mt-12 pt-8 border-t border-gray-100">
        <h2 className="text-lg font-bold text-gray-900 mb-4">浏览其他分类</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {Object.entries(CATEGORIES).filter(([slug]) => slug !== params.slug).slice(0, 4).map(([slug, cat]) => {
            const CatIcon = cat.icon;
            const count = toolsData.filter((t) => t.category === slug).length;
            return (
              <Link key={slug} href={`/category/${slug}`} className="group flex items-center gap-3 p-4 bg-white rounded-xl border border-gray-100 hover:border-blue-200 hover:shadow-md transition-all">
                <div className={`w-10 h-10 flex items-center justify-center rounded-lg bg-gradient-to-br ${cat.gradient} text-white shadow-sm group-hover:scale-110 transition-transform flex-shrink-0`}>
                  <CatIcon className="w-5 h-5" />
                </div>
                <div className="min-w-0">
                  <div className="text-sm font-semibold text-gray-900 group-hover:text-blue-600 transition-colors truncate">{cat.name}</div>
                  <div className="text-xs text-gray-400">{count} 款工具</div>
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </div>
  );
}
