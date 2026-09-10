"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowLeft, Trophy, Star, ArrowRight } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { ToolList } from "@/components/tools/ToolList";
import { FadeIn, GradientText, StackingCard, StackingCardsContainer, GradientButton, Magnet } from "@/components/animations";

export default function RankingPage() {
  const tools = toolsData as Tool[];
  const sortedTools = [...tools]
    .map((t) => ({ ...t, total: calculateScoreResult(t.scores).total }))
    .sort((a, b) => b.total - a.total);

  const top10 = sortedTools.slice(0, 10);
  const [showAll, setShowAll] = useState(false);
  const displayTools = showAll ? sortedTools : sortedTools.slice(0, 50);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <Link href="/" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 dark:text-gray-300 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 transition-all">
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>

        <FadeIn delay={0.1} y={30}>
          <div className="mb-8 text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 rounded-full text-sm font-medium mb-4">
              <Trophy className="w-4 h-4" />
              Top 10 Showcase
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white mb-4">
              AI Tool <GradientText from="#F59E0B" to="#FBBF24" className="font-black">Ranking</GradientText>
            </h1>
            <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
              Sorted by six-dimension weighted scoring. Scroll to explore the top 10 tools in stunning card stack view.
            </p>
          </div>
        </FadeIn>
      </div>

      {/* Top 10 Card Stacking */}
      <StackingCardsContainer className="px-4 sm:px-6 pb-20">
        {top10.map((tool, index) => (
          <StackingCard key={tool.slug} index={index} totalCards={10}>
            <div className="rounded-[40px] sm:rounded-[50px] md:rounded-[60px] border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-6 sm:p-8 md:p-10 shadow-2xl">
              <div className="flex flex-col lg:flex-row gap-8 items-center">
                {/* Left: Rank + Tool Info */}
                <div className="flex-1 text-center lg:text-left">
                  <div className="text-6xl sm:text-7xl md:text-8xl font-black bg-gradient-to-br from-amber-400 to-orange-500 bg-clip-text text-transparent mb-4">
                    #{index + 1}
                  </div>
                  <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-3">
                    {tool.name}
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                    {tool.description}
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center lg:justify-start mb-6">
                    {tool.tags?.slice(0, 3).map((tag: string) => (
                      <span key={tag} className="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-xs font-medium">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <Magnet padding={80} strength={4}>
                    <GradientButton href={`/tools/${tool.slug}`}>
                      View Review
                      <ArrowRight className="w-4 h-4" />
                    </GradientButton>
                  </Magnet>
                </div>

                {/* Right: Score */}
                <div className="flex-shrink-0">
                  <div className="relative w-32 h-32 sm:w-40 sm:h-40">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="8" className="text-gray-200 dark:text-gray-700" />
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        fill="none"
                        stroke="url(#scoreGradient)"
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={`${(tool.total / 100) * 283} 283`}
                      />
                      <defs>
                        <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                          <stop offset="0%" stopColor="#F59E0B" />
                          <stop offset="100%" stopColor="#EF4444" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-3xl sm:text-4xl font-black text-gray-900 dark:text-white">
                        {tool.total.toFixed(1)}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">/ 100</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-center gap-1 mt-4">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-5 h-5 ${i < Math.round(tool.total / 20) ? "text-amber-400 fill-amber-400" : "text-gray-300 dark:text-gray-600"}`}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </StackingCard>
        ))}
      </StackingCardsContainer>

      {/* Full List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
        <FadeIn delay={0.1} y={30}>
          <div className="text-center mb-10">
            <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white mb-3">
              Complete Ranking
            </h2>
            <p className="text-gray-500 dark:text-gray-400">
              Showing {displayTools.length} of {sortedTools.length} tools sorted by score
            </p>
          </div>
        </FadeIn>
        <ToolList tools={displayTools} />
        {!showAll && sortedTools.length > 50 && (
          <div className="text-center mt-8">
            <button
              onClick={() => setShowAll(true)}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition-colors shadow-lg hover:shadow-xl"
            >
              Show All {sortedTools.length} Tools
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
