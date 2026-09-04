"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight, Sparkles, Star } from "lucide-react";
import type { Tool, Grade } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

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

export function ToolCardV2({ tool, index = 0 }: ToolCardProps) {
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
        <Card className="relative h-full flex flex-col overflow-hidden hover:shadow-xl hover:shadow-blue-500/10 dark:hover:shadow-blue-500/20 hover:border-blue-200 dark:hover:border-blue-800 hover:-translate-y-1.5 transition-all duration-300">
          {/* 微光悬停效果 */}
          <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
            <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-500/5 via-transparent to-transparent rotate-45 transform translate-x-full group-hover:translate-x-0 transition-transform duration-1000" />
          </div>

          {/* FeaturedTags */}
          {isFeatured && (
            <div className="absolute top-3 right-3 z-10">
              <Badge className="bg-gradient-to-r from-amber-400 to-orange-500 text-white border-0 shadow-lg shadow-amber-500/30">
                <Sparkles className="w-3 h-3 mr-1" />
                TOP
              </Badge>
            </div>
          )}

          <CardHeader className="pb-4">
            {/* 头部：Logo + 等级 */}
            <div className="flex items-start justify-between">
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

            {/* 名称 + 厂商 */}
            <div className="mt-4">
              <CardTitle className="text-base group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-1">
                {tool.name}
              </CardTitle>
              <CardDescription className="mt-0.5 text-xs">{tool.vendor}</CardDescription>
            </div>

            {/* CategoriesTags */}
            <div className="mt-2">
              <Badge variant="outline" className="text-xs">
                {tool.category}
              </Badge>
            </div>
          </CardHeader>

          <CardContent className="flex-1">
            {/* 描述 */}
            <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed line-clamp-2">
              {tool.description}
            </p>
          </CardContent>

          <CardFooter className="pt-4 border-t">
            <div className="w-full">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-extrabold text-gray-900 dark:text-white">{total.toFixed(1)}</span>
                  <span className="text-xs text-gray-400">/10</span>
                </div>
                <div className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 dark:bg-gray-800 text-gray-400 dark:text-gray-500 group-hover:bg-blue-500 group-hover:text-white group-hover:scale-110 transition-all duration-300">
                  <ArrowUpRight className="w-4 h-4" />
                </div>
              </div>
              {/* Rating进度条 - 使用shadcn/ui Progress */}
              <Progress value={scorePercent} className="h-1.5" />
            </div>
          </CardFooter>
        </Card>
      </Link>
    </motion.div>
  );
}
