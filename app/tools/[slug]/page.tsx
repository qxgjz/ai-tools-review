import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Check, X, Building2, Clock, Tag, ExternalLink, TrendingUp, Sparkles, Lightbulb } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool, Grade, ScoreDimension } from "@/types";
import { calculateScoreResult, DIMENSION_LABELS, SCORE_WEIGHTS, GRADE_DESCRIPTIONS } from "@/lib/scoring";
import { RadarChart } from "@/components/charts/RadarChart";
import { ToolList } from "@/components/tools/ToolList";
import Giscus from "@/components/comments/Giscus";

const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white",
};

const DIMENSION_ORDER: ScoreDimension[] = ["functionality", "ux", "pricing", "integration", "support", "ethics"];

export function generateStaticParams() {
  return toolsData.map((tool) => ({ slug: tool.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const tool = toolsData.find((t) => t.slug === params.slug);
  if (!tool) return { title: "工具未找到" };
  const { total, grade } = calculateScoreResult(tool.scores);
  return {
    title: `${tool.name} - ${total.toFixed(1)}分 ${grade}级 | AI工具测评台`,
    description: tool.description,
    keywords: [tool.name, tool.vendor, ...tool.tags, "AI工具测评"],
  };
}

export default function ToolDetailPage({ params }: { params: { slug: string } }) {
  const tool = toolsData.find((t) => t.slug === params.slug) as Tool | undefined;
  if (!tool) notFound();

  const { total, grade, breakdown } = calculateScoreResult(tool.scores);
  const relatedTools = toolsData
    .filter((t) => t.category === tool.category && t.slug !== tool.slug)
    .slice(0, 3);

  // Schema.org 结构化数据 - Review
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Review",
    itemReviewed: {
      "@type": "SoftwareApplication",
      name: tool.name,
      applicationCategory: "AIApplication",
      operatingSystem: "Web",
      offers: tool.pricing.map((tier) => ({
        "@type": "Offer",
        name: tier.name,
        price: tier.price.includes("$0") ? "0" : tier.price.replace(/[^0-9.]/g, ""),
        priceCurrency: "USD",
      })),
    },
    reviewRating: {
      "@type": "Rating",
      ratingValue: total.toFixed(1),
      bestRating: "10",
      worstRating: "0",
    },
    author: {
      "@type": "Organization",
      name: "AI工具测评台",
    },
    datePublished: tool.lastUpdated,
    reviewBody: tool.description,
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      {/* Schema.org 结构化数据 */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />

      <Link href="/ranking" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 bg-white rounded-xl border border-gray-200 shadow-sm hover:border-blue-300 hover:text-blue-600 transition-all">
        <ArrowLeft className="w-4 h-4" />
        返回排行榜
      </Link>

      {/* 头部 */}
      <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 sm:p-8 mb-6">
        <div className="flex flex-col sm:flex-row sm:items-start gap-6">
          <div className="w-20 h-20 flex-shrink-0 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-3xl font-extrabold shadow-lg">
            {tool.name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-3 mb-2">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900">{tool.name}</h1>
              <span className={`px-3 py-1 rounded-lg text-sm font-bold ${GRADE_STYLES[grade]}`}>
                {grade}级 · {GRADE_DESCRIPTIONS[grade]}
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-gray-500">
              <span className="inline-flex items-center gap-1.5"><Building2 className="w-4 h-4" />{tool.vendor}</span>
              <span className="inline-flex items-center gap-1.5"><Clock className="w-4 h-4" />更新于 {tool.lastUpdated}</span>
              <span className="inline-flex items-center gap-1.5"><Tag className="w-4 h-4" />{tool.category}</span>
              {tool.hasFreeTier && <span className="px-2 py-0.5 bg-emerald-50 text-emerald-600 rounded-md text-xs font-semibold">有免费版</span>}
            </div>
          </div>
          <div className="text-center sm:text-right">
            <div className="text-5xl font-extrabold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">{total.toFixed(1)}</div>
            <div className="text-xs text-gray-400 mt-1">综合评分 / 10</div>
          </div>
        </div>
        {tool.officialUrl && (
          <div className="mt-6 pt-6 border-t border-gray-50">
            <a href={tool.officialUrl} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold rounded-xl shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all">
              <ExternalLink className="w-4 h-4" />
              访问官网
            </a>
          </div>
        )}
      </section>

      {/* 评分卡 + 雷达图 */}
      <section className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-6">
        <div className="lg:col-span-3 bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            六维评分详情
          </h2>
          <div className="space-y-4">
            {DIMENSION_ORDER.map((dim) => {
              const score = tool.scores[dim];
              const percent = (score / 10) * 100;
              return (
                <div key={dim}>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm font-medium text-gray-700">
                      {DIMENSION_LABELS[dim]}
                      <span className="ml-2 text-xs text-gray-400">权重{(SCORE_WEIGHTS[dim] * 100).toFixed(0)}%</span>
                    </span>
                    <span className="text-sm font-bold text-gray-900">{score.toFixed(1)}</span>
                  </div>
                  <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-700" style={{ width: `${percent}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col items-center justify-center">
          <h2 className="text-lg font-bold text-gray-900 mb-4 self-start flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-600" />
            能力雷达图
          </h2>
          <RadarChart scores={tool.scores} size={260} showValues />
        </div>
      </section>

      {/* 优缺点 */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-bold text-emerald-600 mb-4 flex items-center gap-2">
            <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-50"><Check className="w-5 h-5" /></div>
            主要优势
          </h2>
          <ul className="space-y-3">
            {tool.pros.map((pro, i) => (
              <li key={i} className="flex gap-3 text-sm text-gray-600 leading-relaxed">
                <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-emerald-100 text-emerald-600 text-xs font-bold mt-0.5">{i + 1}</span>
                {pro}
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-bold text-red-500 mb-4 flex items-center gap-2">
            <div className="w-8 h-8 flex items-center justify-center rounded-lg bg-red-50"><X className="w-5 h-5" /></div>
            主要不足
          </h2>
          <ul className="space-y-3">
            {tool.cons.map((con, i) => (
              <li key={i} className="flex gap-3 text-sm text-gray-600 leading-relaxed">
                <span className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded-full bg-red-100 text-red-500 text-xs font-bold mt-0.5">!</span>
                {con}
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* 定价 */}
      <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 mb-6">
        <h2 className="text-lg font-bold text-gray-900 mb-5">价格方案</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead><tr className="border-b border-gray-100">
              <th className="text-left py-3 px-4 font-semibold text-gray-500">方案</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-500">价格</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-500">说明</th>
            </tr></thead>
            <tbody>
              {tool.pricing.map((tier, i) => (
                <tr key={i} className={`border-b border-gray-50 hover:bg-gray-50 ${tier.recommended ? "bg-blue-50/50" : ""}`}>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-gray-900">{tier.name}</span>
                      {tier.recommended && <span className="px-2 py-0.5 bg-blue-600 text-white text-xs rounded-md font-semibold">推荐</span>}
                    </div>
                  </td>
                  <td className="py-3 px-4"><span className="font-bold text-blue-600">{tier.price}</span></td>
                  <td className="py-3 px-4 text-gray-500">{tier.description ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* 评测摘要 */}
      <section className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-2xl border border-blue-100 p-6 sm:p-8 mb-6">
        <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-500" />
          编辑评测摘要
        </h2>
        <p className="text-sm sm:text-base text-gray-600 leading-relaxed">
          {tool.name} 是由 {tool.vendor} 推出的{tool.category}类AI工具，综合评分 {total.toFixed(1)}/10，等级为 {grade}（{GRADE_DESCRIPTIONS[grade]}）。{tool.pros[0]}。需要注意的是，{tool.cons[0]}。{tool.hasFreeTier ? "该工具提供免费版本，适合预算有限的用户先体验再决定是否升级。" : ""}综合来看，{total >= 8 ? "是一款值得推荐的优秀工具。" : total >= 7 ? "是一款表现良好的工具，适合特定场景用户。" : "整体表现一般，建议结合需求谨慎选择。"}
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {tool.tags.map((tag) => (
            <span key={tag} className="px-2.5 py-1 bg-white/70 text-gray-600 rounded-md text-xs font-medium border border-gray-200">#{tag}</span>
          ))}
        </div>
      </section>

      {/* 相关推荐 */}
      {relatedTools.length > 0 && (
        <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-600" />
            同类工具推荐
          </h2>
          <ToolList tools={relatedTools} />
        </section>
      )}

      {/* 评论区 */}
      <section className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 sm:p-8">
        <Giscus />
      </section>

      <div className="mt-8 text-center text-xs text-gray-400">
        评分基于公开测评方法论，联盟链接收入不影响评分。最后更新于 {tool.lastUpdated}。
      </div>
    </div>
  );
}
