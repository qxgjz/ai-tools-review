"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";

const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white",
};

interface ToolCardProps {
  tool: Tool;
  index?: number;
}

export function ToolCard({ tool, index = 0 }: ToolCardProps) {
  const { total, grade } = calculateScoreResult(tool.scores);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: Math.min(index * 0.05, 0.5) }}
      className="h-full"
    >
      <Link href={`/tools/${tool.slug}`} className="group block h-full">
        <div className="h-full flex flex-col p-5 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:shadow-blue-500/10 hover:border-blue-200 hover:-translate-y-1 transition-all duration-300">
          <div className="flex items-start justify-between mb-4">
            <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-xl font-extrabold shadow-md group-hover:scale-110 transition-transform">
              {tool.name.charAt(0).toUpperCase()}
            </div>
            <span className={`px-2.5 py-1 rounded-lg text-sm font-bold ${GRADE_STYLES[grade]}`}>
              {grade}
            </span>
          </div>

          <h3 className="text-base font-bold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1">
            {tool.name}
          </h3>
          <p className="mt-0.5 text-xs text-gray-400">{tool.vendor}</p>

          <p className="mt-3 text-sm text-gray-500 leading-relaxed line-clamp-2 flex-1">
            {tool.description}
          </p>

          <div className="mt-4 pt-4 border-t border-gray-50 flex items-center justify-between">
            <span className="text-2xl font-extrabold text-gray-900">{total.toFixed(1)}</span>
            <div className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-400 group-hover:bg-blue-500 group-hover:text-white transition-all">
              <ArrowUpRight className="w-4 h-4" />
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
