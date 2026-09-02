import Link from "next/link";
import { ArrowLeft, Search, TrendingUp, PackageSearch } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { ToolList } from "@/components/tools/ToolList";

const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white",
};

function HighlightText({ text, query }: { text: string; query: string }) {
  if (!query.trim()) return <>{text}</>;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escaped})`, "gi");
  const parts = text.split(regex);
  return (
    <>
      {parts.map((part, i) =>
        regex.test(part) ? (
          <mark key={i} className="bg-yellow-200/80 text-gray-900 px-0.5 rounded font-semibold">{part}</mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

export default function SearchPage({ searchParams }: { searchParams: { q?: string } }) {
  const query = searchParams.q?.trim() ?? "";
  const q = query.toLowerCase();
  const results = query ? toolsData.filter((tool) =>
    tool.name.toLowerCase().includes(q) ||
    tool.vendor.toLowerCase().includes(q) ||
    tool.description.toLowerCase().includes(q) ||
    tool.tags.some((tag) => tag.toLowerCase().includes(q))
  ) as Tool[] : [];

  const hotTools = [...toolsData].map((t) => ({ ...t, total: calculateScoreResult(t.scores).total })).sort((a, b) => b.total - a.total).slice(0, 6);
  const hotKeywords = ["ChatGPT", "Midjourney", "写作", "编程", "视频", "设计", "Claude", "办公"];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 bg-white rounded-xl border border-gray-200 shadow-sm hover:border-blue-300 hover:text-blue-600 transition-all">
        <ArrowLeft className="w-4 h-4" />
        返回首页
      </Link>

      {!query && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 text-center">
          <div className="w-16 h-16 mx-auto mb-4 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50">
            <Search className="w-8 h-8 text-blue-500" />
          </div>
          <h1 className="text-2xl font-extrabold text-gray-900 mb-2">搜索 AI 工具</h1>
          <p className="text-gray-500 mb-6">输入工具名称、厂商或功能标签</p>
          <div className="flex flex-wrap justify-center gap-2 max-w-lg mx-auto">
            {hotKeywords.map((kw) => (
              <Link key={kw} href={`/search?q=${encodeURIComponent(kw)}`} className="px-3.5 py-1.5 bg-gray-50 text-gray-600 text-sm rounded-lg border border-gray-100 hover:border-blue-200 hover:text-blue-600 hover:bg-blue-50 transition-all">
                {kw}
              </Link>
            ))}
          </div>
        </div>
      )}

      {query && (
        <>
          <div className="mb-8">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-2">
              搜索结果：<span className="text-blue-600">"{query}"</span>
            </h1>
            <p className="text-sm text-gray-500">共找到 <span className="font-bold text-gray-700">{results.length}</span> 个匹配工具</p>
          </div>

          {results.length > 0 ? (
            <div className="space-y-4">
              {results.map((tool) => {
                const { total, grade } = calculateScoreResult(tool.scores);
                return (
                  <Link key={tool.id} href={`/tools/${tool.slug}`} className="group block bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:border-blue-200 hover:-translate-y-0.5 transition-all p-5 sm:p-6">
                    <div className="flex flex-col sm:flex-row sm:items-start gap-4">
                      <div className="flex sm:flex-col items-center sm:items-start gap-3 flex-shrink-0">
                        <div className="w-14 h-14 flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-2xl font-extrabold shadow-md group-hover:scale-105 transition-transform">
                          {tool.name.charAt(0).toUpperCase()}
                        </div>
                        <div className="text-center sm:text-left">
                          <div className="text-2xl font-extrabold text-gray-900">{total.toFixed(1)}</div>
                          <span className={`inline-block px-2 py-0.5 rounded-md text-xs font-bold ${GRADE_STYLES[grade]}`}>{grade}级</span>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors mb-1">
                          <HighlightText text={tool.name} query={query} />
                        </h3>
                        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-gray-400 mb-2">
                          <span>{tool.vendor}</span>
                          <span>{tool.category}</span>
                          <span>更新于 {tool.lastUpdated}</span>
                        </div>
                        <p className="text-sm text-gray-500 leading-relaxed line-clamp-2 mb-3">
                          <HighlightText text={tool.description} query={query} />
                        </p>
                        <div className="flex flex-wrap gap-1.5">
                          {tool.tags.slice(0, 5).map((tag) => (
                            <span key={tag} className="px-2 py-0.5 bg-gray-50 text-gray-500 rounded-md text-xs font-medium border border-gray-100">
                              <HighlightText text={tag} query={query} />
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </Link>
                );
              })}
            </div>
          ) : (
            <div>
              <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-10 text-center mb-8">
                <div className="w-20 h-20 mx-auto mb-5 flex items-center justify-center rounded-3xl bg-gradient-to-br from-gray-50 to-gray-100">
                  <PackageSearch className="w-10 h-10 text-gray-300" />
                </div>
                <h2 className="text-xl font-bold text-gray-700 mb-2">没有找到与 "{query}" 匹配的工具</h2>
                <p className="text-sm text-gray-400 mb-6">试试更换关键词，或浏览以下热门工具</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {hotKeywords.map((kw) => (
                    <Link key={kw} href={`/search?q=${encodeURIComponent(kw)}`} className="px-3.5 py-1.5 bg-gray-50 text-gray-600 text-sm rounded-lg border border-gray-100 hover:border-blue-200 hover:text-blue-600 hover:bg-blue-50 transition-all">
                      {kw}
                    </Link>
                  ))}
                </div>
              </div>
              <div className="mb-5 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-orange-500" />
                <h3 className="text-lg font-bold text-gray-900">热门工具推荐</h3>
              </div>
              <ToolList tools={hotTools} />
            </div>
          )}
        </>
      )}
    </div>
  );
}
