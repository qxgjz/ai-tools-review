"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import tools from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult, DIMENSION_LABELS, GRADE_DESCRIPTIONS } from "@/lib/scoring";
import { RadarChart } from "@/components/charts/RadarChart";

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
      {/* 页面标题 */}
      <div className="mb-8">
        <Link
          href="/"
          className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
        >
          ← 返回首页
        </Link>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">工具对比</h1>
        <p className="text-gray-600">
          选择最多 3 个 AI 工具，基于六维评分模型进行横向对比
        </p>
      </div>

      {/* 工具选择器 */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            选择对比工具
            <span className="ml-2 text-sm font-normal text-gray-500">
              已选 {selectedSlugs.length}/3
            </span>
          </h2>
          {selectedSlugs.length > 0 && (
            <button
              onClick={() => setSelectedSlugs([])}
              className="text-sm text-red-500 hover:text-red-600"
            >
              清空选择
            </button>
          )}
        </div>

        {/* 搜索框 */}
        <input
          type="text"
          placeholder="搜索工具名称、厂商或标签..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
        />

        {/* 工具列表 */}
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
                    ? "border-blue-500 bg-blue-50 ring-1 ring-blue-500"
                    : isDisabled
                    ? "border-gray-100 bg-gray-50 opacity-50 cursor-not-allowed"
                    : "border-gray-200 hover:border-blue-300 hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <div
                    className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                      isSelected
                        ? "border-blue-500 bg-blue-500"
                        : "border-gray-300"
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
                  <span className="text-sm font-medium text-gray-900 truncate">
                    {tool.name}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1 truncate">{tool.vendor}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* 对比结果 */}
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
                  className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900">{tool.name}</h3>
                      <p className="text-sm text-gray-500">{tool.vendor}</p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-bold ${
                        result.grade === "S"
                          ? "bg-amber-100 text-amber-700"
                          : result.grade === "A"
                          ? "bg-emerald-100 text-emerald-700"
                          : result.grade === "B"
                          ? "bg-blue-100 text-blue-700"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {result.grade}
                    </span>
                  </div>
                  <div className="text-4xl font-bold text-gray-900 mb-1">
                    {result.total.toFixed(1)}
                    <span className="text-lg text-gray-400 font-normal">/10</span>
                  </div>
                  <p className="text-sm text-gray-500">
                    {GRADE_DESCRIPTIONS[result.grade]} · 更新于 {tool.lastUpdated}
                  </p>
                </Link>
              );
            })}
          </div>

          {/* 雷达图对比 */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">六维能力雷达图对比</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {selectedTools.map((tool) => (
                <div key={tool.slug} className="text-center">
                  <h3 className="text-md font-semibold text-gray-900 mb-4">{tool.name}</h3>
                  <RadarChart scores={tool.scores} size={250} />
                </div>
              ))}
            </div>
          </div>

          {/* 详细对比表格 */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-lg font-semibold text-gray-900">详细参数对比</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600 w-32">
                      对比项
                    </th>
                    {selectedTools.map((tool) => (
                      <th
                        key={tool.slug}
                        className="text-left py-3 px-4 text-sm font-semibold text-gray-900"
                      >
                        {tool.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {/* 厂商 */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500">厂商</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4 text-sm text-gray-900">
                        {tool.vendor}
                      </td>
                    ))}
                  </tr>
                  {/* 分类 */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500">分类</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4 text-sm text-gray-900">
                        {tool.category}
                      </td>
                    ))}
                  </tr>
                  {/* 综合评分 */}
                  <tr className="bg-blue-50/50">
                    <td className="py-3 px-4 text-sm font-semibold text-gray-700">综合评分</td>
                    {selectedTools.map((tool) => {
                      const result = calculateScoreResult(tool.scores);
                      return (
                        <td key={tool.slug} className="py-3 px-4">
                          <span className="text-lg font-bold text-blue-600">
                            {result.total.toFixed(1)}
                          </span>
                          <span className="text-sm text-gray-400 ml-1">/10</span>
                        </td>
                      );
                    })}
                  </tr>
                  {/* 六维评分 */}
                  {dimensions.map((dim) => (
                    <tr key={dim}>
                      <td className="py-3 px-4 text-sm text-gray-500">
                        {DIMENSION_LABELS[dim]}
                      </td>
                      {selectedTools.map((tool) => {
                        const score = tool.scores[dim];
                        const maxScore = Math.max(...selectedTools.map((t) => t.scores[dim]));
                        const isMax = score === maxScore;
                        return (
                          <td key={tool.slug} className="py-3 px-4">
                            <div className="flex items-center gap-2">
                              <div className="flex-1 bg-gray-100 rounded-full h-2 max-w-[100px]">
                                <div
                                  className={`h-2 rounded-full ${
                                    isMax ? "bg-blue-500" : "bg-gray-300"
                                  }`}
                                  style={{ width: `${(score / 10) * 100}%` }}
                                />
                              </div>
                              <span
                                className={`text-sm font-medium ${
                                  isMax ? "text-blue-600" : "text-gray-600"
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
                  {/* 免费版 */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500">免费版</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        {tool.hasFreeTier ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700">
                            有免费版
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-500">
                            无免费版
                          </span>
                        )}
                      </td>
                    ))}
                  </tr>
                  {/* 起步价 */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500">起步价</td>
                    {selectedTools.map((tool) => {
                      const paid = tool.pricing.find((p) => !p.price.includes("$0"));
                      return (
                        <td key={tool.slug} className="py-3 px-4 text-sm text-gray-900">
                          {paid ? paid.price : "免费"}
                        </td>
                      );
                    })}
                  </tr>
                  {/* 主要优势 */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 align-top">主要优势</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        <ul className="space-y-1">
                          {tool.pros.slice(0, 3).map((pro, i) => (
                            <li key={i} className="text-sm text-gray-700 flex items-start gap-1">
                              <span className="text-emerald-500 flex-shrink-0">✓</span>
                              <span>{pro}</span>
                            </li>
                          ))}
                        </ul>
                      </td>
                    ))}
                  </tr>
                  {/* 主要不足 */}
                  <tr>
                    <td className="py-3 px-4 text-sm text-gray-500 align-top">主要不足</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        <ul className="space-y-1">
                          {tool.cons.slice(0, 3).map((con, i) => (
                            <li key={i} className="text-sm text-gray-700 flex items-start gap-1">
                              <span className="text-red-400 flex-shrink-0">✗</span>
                              <span>{con}</span>
                            </li>
                          ))}
                        </ul>
                      </td>
                    ))}
                  </tr>
                  {/* 官网链接 */}
                  <tr className="bg-gray-50">
                    <td className="py-3 px-4 text-sm text-gray-500">操作</td>
                    {selectedTools.map((tool) => (
                      <td key={tool.slug} className="py-3 px-4">
                        <div className="flex gap-2">
                          <Link
                            href={`/tools/${tool.slug}`}
                            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                          >
                            查看详情 →
                          </Link>
                          {tool.officialUrl && (
                            <a
                              href={tool.officialUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-gray-500 hover:text-gray-700"
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
        </div>
      ) : (
        /* 空状态 */
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
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
          <h3 className="text-lg font-semibold text-gray-900 mb-2">选择工具开始对比</h3>
          <p className="text-gray-500 max-w-md mx-auto">
            从上方列表中选择 2-3 个工具，系统将基于六维评分模型生成详细对比报告
          </p>
        </div>
      )}
    </div>
  );
}
