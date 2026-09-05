"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import tools from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult, DIMENSION_LABELS, GRADE_DESCRIPTIONS } from "@/lib/scoring";
import { RadarChart } from "@/components/charts/RadarChart";
import { MultiRadarChart } from "@/components/charts/MultiRadarChart";
import { AffiliateCTA } from "@/components/monetization/AffiliateCTA";

export default function ComparePage() {
  const [selectedSlugs, setSelectedSlugs] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const selectedTools = useMemo(
    () => tools.filter((t) => selectedSlugs.includes(t.slug)),
    [selectedSlugs]
  );

  const filteredTools = useMemo(() => {
    if (!searchQuery.trim()) return tools;
    const q = searchQuery.toLowerCase();
    return tools.filter(
      (t) =>
        t.name.toLowerCase().includes(q) ||
        t.vendor.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.tags.some((tag) => tag.toLowerCase().includes(q))
    );
  }, [searchQuery]);

  const toggleTool = (slug: string) => {
    setSelectedSlugs((prev) => {
      if (prev.includes(slug)) {
        return prev.filter((s) => s !== slug);
      }
      if (prev.length >= 3) {
        return prev; // 最多选3个
      }
      return [...prev, slug];
    });
  };

  const dimensions = [
    "functionality",
    "ux",
    "pricing",
    "integration",
    "support",
    "ethics",
  ] as const;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Schema.org 结构化数据 - Comparison */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            name: "AI Tool Comparison - AIToolCrux",
            url: "https://www.aitoolcrux.com/compare",
            description: "Compare AI tools side by side. Features, pricing, ratings, and more.",
            inLanguage: "en",
            mainEntity: {
              "@type": "ItemList",
              name: "AI Tool Comparisons",
              description: "Side-by-side comparisons of popular AI tools",
            },
          }),
        }}
      />
      {/* Page标题 */}
      <div className="mb-8">
        <Link
          href="/"
          className="inline-flex items-center text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 mb-4"
        >
          ← Back to Home
        </Link>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Tool Comparison</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Select up to 3 AI tools for side-by-side comparison based on the six-dimension scoring model
        </p>
      </div>

      {/* Tools选择器 */}
      <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Select Tools to Compare
            <span className="ml-2 text-sm font-normal text-gray-500 dark:text-gray-400">
              Selected {selectedSlugs.length}/3
            </span>
          </h2>
          {selectedSlugs.length > 0 && (
            <button
              onClick={() => setSelectedSlugs([])}
              className="text-sm text-red-500 hover:text-red-600"
            >
              Clear All
            </button>
          )}
        </div>

        {/* Search框 */}
        <input
          type="text"
          placeholder="Search tool name, vendor, or tags..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
        />

        {/* Tools列Table */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 max-h-64 overflow-y-auto">
          {filteredTools.map((tool) => {
            const isSelected = selectedSlugs.includes(tool.slug);
            const isDisabled = !isSelected && selectedSlugs.length >= 3;
            return (
              <button
                key={tool.slug}
                onClick={() => toggleTool(tool.slug)}
                disabled={isDisabled}
                className={`p-3 rounded-lg border text-left transition-all ${
                  isSelected
                    ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20 ring-1 ring-blue-500"
                    : isDisabled
                    ? "border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 opacity-50 cursor-not-allowed"
                    : "border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700 hover:bg-gray-50 dark:hover:bg-gray-800"
                }`}
              >
                <div className="flex items-center gap-2">
                  <div
                    className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                      isSelected
                        ? "border-blue-500 bg-blue-500"
                        : "border-gray-300 dark:border-gray-600"
                    }`}
                  >
                    {isSelected && (
                      <svg
                        className="w-3 h-3 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={3}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    )}
                  </div>
                  <span className="text-sm font-medium text-gray-900 dark:text-white truncate">
                    {tool.name}
                  </span>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 truncate">{tool.vendor}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Compare结果 */}
      {selectedTools.length >= 2 ? (
        <div className="space-y-8">
          {/* 总览卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {selectedTools.map((tool) => {
              const result = calculateScoreResult(tool.scores);
              return (
                <Link
                  key={tool.slug}
                  href={`/tools/${tool.slug}`}
                  className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-6 hover:shadow-md dark:hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 dark:text-white">{tool.name}</h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{tool.vendor}</p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-bold ${
                        result.grade === "S"
                          ? "bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400"
                          : result.grade === "A"
                          ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400"
                          : result.grade === "B"
                          ? "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400"
                          : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
                      }`}
                    >
                      {result.grade}
                    </span>
                  </div>
                  <div className="text-4xl font-bold text-gray-900 dark:text-white mb-1">
                    {result.total.toFixed(1)}
                    <span className="text-lg text-gray-400 font-normal">/10</span>
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {GRADE_DESCRIPTIONS[result.grade]} · Updated  {tool.lastUpdated}
                  </p>
                </Link>
              );
            })}
          </div>

          {/* 叠加雷达图Compare */}
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Six-Dimension Overlay Radar Chart Comparison</h2>
            <div className="flex justify-center">
              <MultiRadarChart
                tools={selectedTools.map((t, i) => ({
                  name: t.name,
                  scores: t.scores,
                  color: ["#3b82f6", "#10b981", "#f59e0b"][i % 3],
                }))}
                size={420}
              />
            </div>
          </div>

          {/* 按场景推荐 */}
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Recommendations by Use Case</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { scene: "Best Functionality", dim: "functionality", icon: "⚡", desc: "Core feature completeness, output accuracy" },
                { scene: "Best for Beginners", dim: "ux", icon: "🎯", desc: "Intuitive interface, gentle learning curve" },
                { scene: "Best Value for Money", dim: "pricing", icon: "💰", desc: "Generous free tier, transparent pricing" },
                { scene: "Best for Developers", dim: "integration", icon: "🔧", desc: "API quality, platform compatibility" },
                { scene: "Best Enterprise Reliability", dim: "support", icon: "🛡️", desc: "Uptime, update frequency" },
                { scene: "Best Data Privacy", dim: "ethics", icon: "🔒", desc: "Data privacy, responsible AI" },
              ].map(({ scene, dim, icon, desc }) => {
                const winner = selectedTools.reduce((best, t) =>
                  (t.scores as any)[dim] > (best.scores as any)[dim] ? t : best
                );
                return (
                  <div
                    key={dim}
                    className="p-4 rounded-lg border border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/30"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xl">{icon}</span>
                      <span className="text-sm font-semibold text-gray-900 dark:text-white">{scene}</span>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">{desc}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold text-blue-600 dark:text-blue-400">
                        Recommended: {winner.name}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {(winner.scores as any)[dim].toFixed(1)}/10
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 详细CompareTable格 */}
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden">
            <div className="p-6 border-b border-gray-100 dark:border-gray-800">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Detailed Specification Comparison</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50 dark:bg-gray-800/50">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400 w-32">
                      Feature
                    </th>
                    {selectedTools.map((tool) => (
                      <th
                        key={tool.slug}
                        className="text-left py-3 px-4 text-sm font-semibold text-gray-900 dark:text-white"
                      >
                        {tool.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                  {/* Vendor */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">Vendor</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4 text-sm text-gray-900 dark:text-white">
                        {tool.vendor}
                      </td>
                    ))}
                  </tr>
                  {/* Category */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">Category</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4 text-sm text-gray-900 dark:text-white">
                        {tool.category}
                      </td>
                    ))}
                  </tr>
                  {/* Overall Score */}
                  <tr className="bg-blue-50/50 dark:bg-blue-900/10">
                    <td className="py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Overall Score</td>
                    {selectedTools.map((tool) => {
                      const result = calculateScoreResult(tool.scores);
                      return (
                        <td key={tool.slug} className="py-3 px-4">
                          <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                            {result.total.toFixed(1)}
                          </span>
                          <span className="text-sm text-gray-400 ml-1">/10</span>
                        </td>
                      );
                    })}
                  </tr>
                  {/* Six-Dimension Scores */}
                  {dimensions.map((dim) => (
                    <tr key={dim}>
                      <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">
                        {DIMENSION_LABELS[dim]}
                      </td>
                      {selectedTools.map((tool) => {
                        const score = tool.scores[dim];
                        const maxScore = Math.max(...selectedTools.map((t) => t.scores[dim]));
                        const isMax = score === maxScore;
                        return (
                          <td key={tool.slug} className="py-3 px-4">
                            <div className="flex items-center gap-2">
                              <div className="flex-1 bg-gray-100 dark:bg-gray-800 rounded-full h-2 max-w-[100px]">
                                <div
                                  className={`h-2 rounded-full ${
                                    isMax ? "bg-blue-500" : "bg-gray-300 dark:bg-gray-600"
                                  }`}
                                  style={{ width: `${(score / 10) * 100}%` }}
                                />
                              </div>
                              <span
                                className={`text-sm font-medium ${
                                  isMax ? "text-blue-600 dark:text-blue-400" : "text-gray-600 dark:text-gray-400"
                                }`}
                              >
                                {score.toFixed(1)}
                              </span>
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                  {/* Free */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">Free</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        {tool.hasFreeTier ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400">
                            有Free
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
                            No Free Plan
                          </span>
                        )}
                      </td>
                    ))}
                  </tr>
                  {/* Starting Price */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">Starting Price</td>
                    {selectedTools.map((tool) => {
                      const paid = tool.pricing.find((p) => !p.price.includes("$0"));
                      return (
                        <td key={tool.slug} className="py-3 px-4 text-sm text-gray-900 dark:text-white">
                          {paid ? paid.price : "Free"}
                        </td>
                      );
                    })}
                  </tr>
                  {/* Key Strengths */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400 align-top">Key Strengths</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        <ul className="space-y-1">
                          {tool.pros.slice(0, 3).map((pro, i) => (
                            <li key={i} className="text-sm text-gray-700 dark:text-gray-300 flex items-start gap-1">
                              <span className="text-emerald-500 flex-shrink-0">✓</span>
                              <span>{pro}</span>
                            </li>
                          ))}
                        </ul>
                      </td>
                    ))}
                  </tr>
                  {/* Key Weaknesses */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400 align-top">Key Weaknesses</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        <ul className="space-y-1">
                          {tool.cons.slice(0, 3).map((con, i) => (
                            <li key={i} className="text-sm text-gray-700 dark:text-gray-300 flex items-start gap-1">
                              <span className="text-red-400 flex-shrink-0">✗</span>
                              <span>{con}</span>
                            </li>
                          ))}
                        </ul>
                      </td>
                    ))}
                  </tr>
                  {/* 官网链接 */}
                  <tr className="bg-gray-50 dark:bg-gray-800/50">
                    <td className="py-3 px-4 text-sm text-gray-500 dark:text-gray-400">Action</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        <div className="flex gap-2">
                          <Link
                            href={`/tools/${tool.slug}`}
                            className="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium"
                          >
                            View Details →
                          </Link>
                          {tool.officialUrl && (
                            <a
                              href={tool.officialUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                            >
                              官网 ↗
                            </a>
                          )}
                        </div>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Pricing方案详细Compare */}
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden">
            <div className="p-6 border-b border-gray-100 dark:border-gray-800">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Pricing Comparison</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50 dark:bg-gray-800/50">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600 dark:text-gray-400 w-32">
                      方案
                    </th>
                    {selectedTools.map((tool) => (
                      <th
                        key={tool.slug}
                        className="text-left py-3 px-4 text-sm font-semibold text-gray-900 dark:text-white"
                      >
                        {tool.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                  {/* Free */}
                  <tr>
                    <td className="py-3 px-4 text-sm font-medium text-gray-700 dark:text-gray-300">Free</td>
                    {selectedTools.map((tool) => {
                      const free = tool.pricing.find((p) => p.price.includes("$0"));
                      return (
                        <td key={tool.slug} className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">
                          {free ? (
                            <div>
                              <span className="font-semibold text-emerald-600 dark:text-emerald-400">{free.price}</span>
                              <p className="text-xs text-gray-500 dark:text-gray-500 mt-0.5">{free.description}</p>
                            </div>
                          ) : (
                            <span className="text-gray-400">No Free Plan</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                  {/* Starter */}
                  <tr>
                    <td className="py-3 px-4 text-sm font-medium text-gray-700 dark:text-gray-300">Starter</td>
                    {selectedTools.map((tool) => {
                      const paid = tool.pricing.filter((p) => !p.price.includes("$0"));
                      const entry = paid[0];
                      return (
                        <td key={tool.slug} className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">
                          {entry ? (
                            <div>
                              <span className="font-semibold">{entry.name}: {entry.price}</span>
                              <p className="text-xs text-gray-500 dark:text-gray-500 mt-0.5">{entry.description}</p>
                            </div>
                          ) : (
                            <span className="text-gray-400">-</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                  {/* Pro */}
                  <tr>
                    <td className="py-3 px-4 text-sm font-medium text-gray-700 dark:text-gray-300">Pro</td>
                    {selectedTools.map((tool) => {
                      const paid = tool.pricing.filter((p) => !p.price.includes("$0"));
                      const pro = paid[1] || paid[0];
                      return (
                        <td key={tool.slug} className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">
                          {pro && paid.length > 1 ? (
                            <div>
                              <span className="font-semibold">{pro.name}: {pro.price}</span>
                              <p className="text-xs text-gray-500 dark:text-gray-500 mt-0.5">{pro.description}</p>
                            </div>
                          ) : (
                            <span className="text-gray-400">-</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                  {/* Enterprise */}
                  <tr>
                    <td className="py-3 px-4 text-sm font-medium text-gray-700 dark:text-gray-300">Top Tier</td>
                    {selectedTools.map((tool) => {
                      const paid = tool.pricing.filter((p) => !p.price.includes("$0"));
                      const top = paid[paid.length - 1];
                      return (
                        <td key={tool.slug} className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">
                          {top && paid.length > 2 ? (
                            <div>
                              <span className="font-semibold">{top.name}: {top.price}</span>
                              <p className="text-xs text-gray-500 dark:text-gray-500 mt-0.5">{top.description}</p>
                            </div>
                          ) : (
                            <span className="text-gray-400">-</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* 底部联盟CTA */}
          <div className="space-y-4">
            {selectedTools.map((tool) => (
              <AffiliateCTA
                key={tool.slug}
                toolName={tool.name}
                officialUrl={tool.officialUrl}
                affiliateUrl={(tool as any).affiliateUrl}
                description={`Compare ${tool.name} with other AI tools and see our full review. Click to visit official site.`}
                variant="bottom"
              />
            ))}
          </div>
        </div>
      ) : (
        /* 空状态 */
        <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 p-12 text-center">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Select tools to compare</h3>
          <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
            从上方列Table中选择 2-3 个Tools，System将基于Six-Dimension Scores模型生成详细CompareReport
          </p>
        </div>
      )}
    </div>
  );
}
