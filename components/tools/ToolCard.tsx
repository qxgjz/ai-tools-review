"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, Sparkles } from "lucide-react";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

// Grade styles - solid colors, NO gradients (Taste Skill + UI/UX Pro Max rule)
const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-amber-700 text-white",
  A: "bg-green-700 text-white",
  B: "bg-blue-700 text-white",
  C: "bg-yellow-600 text-white",
  D: "bg-red-700 text-white",
  F: "bg-zinc-500 text-white",
};

interface ToolCardProps {
  tool: Tool;
  index?: number;
}

export function ToolCard({ tool, index = 0 }: ToolCardProps) {
  const { total, grade } = calculateScoreResult(tool.scores);
  const isFeatured = total >= 8.5;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.35,
        delay: Math.min(index * 0.05, 0.5),
        ease: [0.16, 1, 0.3, 1],
      }}
      className="h-full group"
    >
      <Link
        href={`/tools/${tool.slug}`}
        className="block h-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 rounded-xl"
        aria-label={`${tool.name} review - rated ${total.toFixed(1)}/10, Grade ${grade}. Click to read full review.`}
      >
        <div className="relative h-full flex flex-col p-5 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:border-emerald-500/60 dark:hover:border-emerald-500/60 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 overflow-hidden">
          {/* Subtle top accent line on hover */}
          <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-emerald-500 to-emerald-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />

          {/* Header: Logo + Grade */}
          <div className="flex items-start justify-between mb-4">
            <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 text-xl font-bold transition-colors group-hover:bg-emerald-100 dark:group-hover:bg-emerald-900/30 group-hover:text-emerald-600 dark:group-hover:text-emerald-400">
              {tool.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex items-center gap-2">
              {isFeatured && (
                <span
                  className="inline-flex items-center gap-1 px-2 py-0.5 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 text-[10px] font-semibold rounded-md"
                  title="Top rated tool (score >= 8.5)"
                >
                  <Sparkles className="w-3 h-3" aria-hidden="true" />
                  TOP
                </span>
              )}
              <span
                className={`px-2 py-0.5 rounded-md text-xs font-bold ${GRADE_STYLES[grade]}`}
                title={`Grade ${grade} - based on 6-dimension scoring`}
              >
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
            <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 text-[10px] font-medium capitalize">
              {tool.category}
            </span>
          </div>

          {/* Description */}
          <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed line-clamp-2 flex-1 mb-4">
            {tool.description}
          </p>

          {/* Rating section - number + grade only, NO filled background progress bar */}
          <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800">
            <div className="flex items-center justify-between">
              <div className="flex items-baseline gap-2">
                <span className="text-xl font-bold text-zinc-900 dark:text-zinc-100">
                  {total.toFixed(1)}
                </span>
                <span className="text-xs text-zinc-400">/10</span>
                <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${GRADE_STYLES[grade]}`}>
                  Grade {grade}
                </span>
              </div>
              <div className="w-7 h-7 flex items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 group-hover:bg-emerald-600 group-hover:text-white transition-all duration-200 group-hover:scale-110">
                <ArrowUpRight className="w-3.5 h-3.5" aria-hidden="true" />
              </div>
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
