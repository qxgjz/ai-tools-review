"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, Sparkles } from "lucide-react";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

// Grade styles - solid colors, NO gradients (Taste Skill rule)
const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-amber-700 text-white",
  A: "bg-green-700 text-white",
  B: "bg-blue-700 text-white",
  C: "bg-yellow-600 text-white",
  D: "bg-red-700 text-white",
  F: "bg-zinc-500 text-white",
};

const GRADE_BAR_COLORS: Record<Grade, string> = {
  S: "bg-amber-600",
  A: "bg-green-600",
  B: "bg-blue-600",
  C: "bg-yellow-500",
  D: "bg-red-600",
  F: "bg-zinc-500",
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
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: Math.min(index * 0.04, 0.4), ease: [0.16, 1, 0.3, 1] }}
      className="h-full group"
    >
      <Link href={`/tools/${tool.slug}`} className="block h-full">
        <div className="relative h-full flex flex-col p-5 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:border-emerald-500 dark:hover:border-emerald-500 hover:shadow-md transition-all duration-200 overflow-hidden">
          {/* Header: Logo + Grade */}
          <div className="flex items-start justify-between mb-4">
            <div className="w-12 h-12 flex items-center justify-center rounded-lg bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xl font-bold">
              {tool.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex items-center gap-2">
              {isFeatured && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 text-[10px] font-semibold rounded">
                  <Sparkles className="w-3 h-3" />
                  TOP
                </span>
              )}
              <span className={`px-2 py-0.5 rounded text-xs font-bold ${GRADE_STYLES[grade]}`}>
                {grade}
              </span>
            </div>
          </div>

          {/* Name + Vendor */}
          <div className="mb-3">
            <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors line-clamp-1">
              {tool.name}
            </h3>
            <p className="mt-0.5 text-xs text-zinc-500 dark:text-zinc-400">{tool.vendor}</p>
          </div>

          {/* Category tag */}
          <div className="mb-3">
            <span className="inline-flex items-center px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 text-[10px] font-medium">
              {tool.category}
            </span>
          </div>

          {/* Description */}
          <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed line-clamp-2 flex-1 mb-4">
            {tool.description}
          </p>

          {/* Rating section */}
          <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-baseline gap-1">
                <span className="text-xl font-bold text-zinc-900 dark:text-zinc-100">{total.toFixed(1)}</span>
                <span className="text-xs text-zinc-400">/10</span>
              </div>
              <div className="w-7 h-7 flex items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                <ArrowUpRight className="w-3.5 h-3.5" />
              </div>
            </div>
            {/* Progress bar - solid color, no gradient */}
            <div className="h-1 w-full bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${scorePercent}%` }}
                transition={{ duration: 0.6, delay: Math.min(index * 0.04 + 0.2, 0.6), ease: "easeOut" }}
                className={`h-full rounded-full ${GRADE_BAR_COLORS[grade]}`}
              />
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
