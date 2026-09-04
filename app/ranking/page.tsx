import Link from "next/link";
import { ArrowLeft, Trophy } from "lucide-react";
import toolsData from "@/data/tools.json";
import type { Tool } from "@/types";
import { calculateScoreResult } from "@/lib/scoring";
import { ToolList } from "@/components/tools/ToolList";

export const metadata = {
  title: "AI Tool Ranking - AIToolCrux",
  description: "AI tool ranking based on six-dimension weighted scoring. Find the best AI tools quickly.",
};

export default function RankingPage() {
  const tools = toolsData as Tool[];
  const sortedTools = [...tools]
    .map((t) => ({ ...t, total: calculateScoreResult(t.scores).total }))
    .sort((a, b) => b.total - a.total);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 dark:text-gray-300 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 transition-all">
        <ArrowLeft className="w-4 h-4" />
        Back to Home
      </Link>

      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white flex items-center gap-3 mb-2">
          <Trophy className="w-8 h-8 text-amber-500" />
          AI Tool Ranking
        </h1>
        <p className="text-gray-500 dark:text-gray-400">Sorted by six-dimension weighted scoring, {sortedTools.length} tools total</p>
      </div>

      <ToolList tools={sortedTools} />
    </div>
  );
}
