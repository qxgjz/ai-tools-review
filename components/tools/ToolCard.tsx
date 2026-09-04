"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, Sparkles } from "lucide-react";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white shadow-amber-500/30",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white shadow-emerald-500/30",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white shadow-blue-500/30",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white shadow-yellow-500/30",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white shadow-red-500/30",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white shadow-gray-500/30",
};

const GRADE_BAR_COLORS: Record<Grade, string> = {
  S: "from-amber-400 to-amber-600",
  A: "from-emerald-400 to-emerald-600",
  B: "from-blue-400 to-blue-600",
  C: "from-yellow-400 to-yellow-500",
  D: "from-red-400 to-red-600",
  F: "from-gray-400 to-gray-500",
};

interface ToolCardProps {
  tool: Tool;
  index?: number;
}

export function ToolCard({ tool, index = 0 }: ToolCardProps) {
  const { total, grade } = calculateScoreResult(tool.scores);
  const scorePercent = Math.min((total / 10) * 100, 100);
  const isFeatured = total >= 8.5;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: Math.min(index * 0.05, 0.5) }}
      className="h-full group"
    >
      <Link href={`/tools/${tool.slug}`} className="block h-full">
        <div className="relative h-full flex flex-col p-5 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-2xl hover:shadow-blue-500/10 dark:hover:shadow-blue-500/20 hover:border-blue-200 dark:hover:border-blue-800 hover:-translate-y-1.5 transition-all duration-300 overflow-hidden">
          {/* 微光悬停效果（参考Magic UI） */}
          <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
            <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-500/5 via-transparent to-transparent rotate-45 transform translate-x-full group-hover:translate-x-0 transition-transform duration-1000" />
          </div>

          {/* 精选标签已移到评分区域，避免与Logo和评级标签重叠 */}

          {/* 头部：Logo + 等级 */}
          <div className="flex items-start justify-between mb-4 relative z-10">
            <div className="relative">
              <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-xl font-extrabold shadow-lg shadow-blue-500/30 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                {tool.name.charAt(0).toUpperCase()}
              </div>
              {/* Logo微光效果 */}
              <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-blue-400 to-indigo-500 opacity-0 group-hover:opacity-20 blur-md transition-opacity duration-300" />
            </div>
            <span className={`px-2.5 py-1 rounded-lg text-sm font-bold shadow-lg ${GRADE_STYLES[grade]}`}>
              {grade}
            </span>
          </div>

          {/* 名称 + 厂商 + 精选标签 */}
          <div className="relative z-10">
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-1 flex-1">
                {tool.name}
              </h3>
              {isFeatured && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-gradient-to-r from-amber-400 to-orange-500 text-white text-[10px] font-bold rounded-full shadow-lg shadow-amber-500/30 flex-shrink-0">
                  <Sparkles className="w-3 h-3" />
                  TOP
                </span>
              )}
            </div>
            <p className="mt-0.5 text-xs text-gray-400 dark:text-gray-500">{tool.vendor}</p>
          </div>

          {/* 分类标签（参考shadcn/ui Badge） */}
          <div className="mt-2 relative z-10">
            <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-[10px] font-medium border border-gray-100 dark:border-gray-700">
              {tool.category}
            </span>
          </div>

          {/* 描述 */}
          <p className="mt-3 text-sm text-gray-500 dark:text-gray-400 leading-relaxed line-clamp-2 flex-1 relative z-10">
            {tool.description}
          </p>

          {/* 评分区域（参考shadcn/ui Progress + Aceternity UI） */}
          <div className="mt-4 pt-4 border-t border-gray-50 dark:border-gray-800 relative z-10">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-baseline gap-1">
                <span className="text-2xl font-extrabold text-gray-900 dark:text-white">{total.toFixed(1)}</span>
                <span className="text-xs text-gray-400">/10</span>
              </div>
              <div className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 dark:bg-gray-800 text-gray-400 dark:text-gray-500 group-hover:bg-blue-500 group-hover:text-white group-hover:scale-110 transition-all duration-300">
                <ArrowUpRight className="w-4 h-4" />
              </div>
            </div>
            {/* 评分进度条（参考shadcn/ui Progress） */}
            <div className="h-1.5 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${scorePercent}%` }}
                transition={{ duration: 1, delay: Math.min(index * 0.05 + 0.3, 0.8), ease: "easeOut" }}
                className={`h-full bg-gradient-to-r ${GRADE_BAR_COLORS[grade]} rounded-full`}
              />
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
