"use client";

import { useState } from "react";
import Link from "next/link";
import { Sparkles, ArrowLeft, Check, Trophy, Lightbulb, Loader2, Share2, CheckCircle2 } from "lucide-react";
import type { ScoreDimension, Grade } from "@/types";
import { DIMENSION_LABELS, SCORE_WEIGHTS } from "@/lib/scoring";
import { generateRecommendations, getScenarioOptions, SCENARIO_LABELS, type GeneratorResult, type ScenarioType } from "@/lib/generator";
import { RadarChart } from "@/components/charts/RadarChart";

const GRADE_STYLES: Record<Grade, string> = {
  S: "bg-gradient-to-br from-amber-400 to-amber-600 text-white",
  A: "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white",
  B: "bg-gradient-to-br from-blue-400 to-blue-600 text-white",
  C: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white",
  D: "bg-gradient-to-br from-red-400 to-red-600 text-white",
  F: "bg-gradient-to-br from-gray-400 to-gray-500 text-white",
};

const DIMENSION_OPTIONS: ScoreDimension[] = ["functionality", "ux", "pricing", "integration", "support", "ethics"];

export default function GeneratorPage() {
  const [scenario, setScenario] = useState<ScenarioType>("writing");
  const [priorityDims, setPriorityDims] = useState<ScoreDimension[]>([]);
  const [results, setResults] = useState<GeneratorResult[] | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [copied, setCopied] = useState(false);

  const scenarioOptions = getScenarioOptions();

  const toggleDimension = (dim: ScoreDimension) => {
    setPriorityDims((prev) => (prev.includes(dim) ? prev.filter((d) => d !== dim) : [...prev, dim]));
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const recs = generateRecommendations({ scenario, priorityDimensions: priorityDims }, 3);
      setResults(recs);
      setIsGenerating(false);
    }, 800);
  };

  const handleReset = () => {
    setScenario("writing");
    setPriorityDims([]);
    setResults(null);
  };

  const handleShare = async () => {
    const shareText = results
      ? `I found the perfect tools for ${SCENARIO_LABELS[scenario]} on AIToolCrux - Top 3 tools: ${results.map((r) => `${r.rank}.${r.tool.name}(${r.matchScore}/10)`).join("、")}`
      : "Try AI Tool Matcher now!";
    try {
      await navigator.clipboard.writeText(`${shareText}\n${window.location.href}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      alert("Copy failed");
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <Link href="/" className="inline-flex items-center gap-2 px-4 py-2 mb-6 text-sm font-medium text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 transition-all">
        <ArrowLeft className="w-4 h-4" />
        Back to Home
      </Link>

      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-100 dark:border-blue-800 rounded-full text-sm text-blue-700 dark:text-blue-400 font-medium">
          <Sparkles className="w-4 h-4" />
          AI Matcher Engine
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 dark:text-white mb-3">
          Find the Perfect <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">AI Tools</span>
        </h1>
        <p className="text-gray-500 dark:text-gray-400 max-w-xl mx-auto">Select your use case and priority dimensions. Our system will recommend the Top 3 tools based on the six-dimension scoring model.</p>
      </div>

      <section className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8 mb-8">
        <div className="mb-8">
          <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">1. Your Primary Use Case</label>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {scenarioOptions.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setScenario(opt.value)}
                className={`p-4 rounded-xl border-2 text-left transition-all ${scenario === opt.value ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-md shadow-blue-500/10" : "border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50 hover:border-gray-200 dark:hover:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"}`}
              >
                <div className={`text-sm font-bold mb-1 ${scenario === opt.value ? "text-blue-700 dark:text-blue-400" : "text-gray-700 dark:text-gray-300"}`}>{opt.label}</div>
                <div className="text-xs text-gray-400 dark:text-gray-500 leading-relaxed">{opt.description}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">2. Priority Dimensions (Multi-select)</label>
          <p className="text-xs text-gray-400 dark:text-gray-500 mb-3">Selected dimensions get higher weight in recommendations</p>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {DIMENSION_OPTIONS.map((dim) => {
              const isSelected = priorityDims.includes(dim);
              return (
                <button
                  key={dim}
                  onClick={() => toggleDimension(dim)}
                  className={`flex items-center gap-3 p-3.5 rounded-xl border-2 transition-all ${isSelected ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20 shadow-md shadow-indigo-500/10" : "border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50 hover:border-gray-200 dark:hover:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"}`}
                >
                  <div className={`w-5 h-5 flex-shrink-0 flex items-center justify-center rounded-md border-2 transition-all ${isSelected ? "bg-indigo-500 border-indigo-500" : "border-gray-300 dark:border-gray-600"}`}>
                    {isSelected && <Check className="w-3.5 h-3.5 text-white" />}
                  </div>
                  <div className="text-left min-w-0">
                    <div className={`text-sm font-semibold ${isSelected ? "text-indigo-700 dark:text-indigo-400" : "text-gray-700 dark:text-gray-300"}`}>{DIMENSION_LABELS[dim]}</div>
                    <div className="text-xs text-gray-400 dark:text-gray-500">Weight {(SCORE_WEIGHTS[dim] * 100).toFixed(0)}%</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-10 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl hover:-translate-y-0.5 transition-all disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {isGenerating ? (<><Loader2 className="w-5 h-5 animate-spin" />Matching...</>) : (<><Sparkles className="w-5 h-5" />Generate My Recommendations</>)}
          </button>
          {results && (
            <button onClick={handleReset} className="inline-flex items-center gap-2 px-6 py-4 text-gray-500 dark:text-gray-400 font-medium hover:text-gray-700 dark:hover:text-gray-300 transition-colors">
              Reset
            </button>
          )}
        </div>
      </section>

      {results && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h2 className="text-2xl font-extrabold text-gray-900 dark:text-white flex items-center gap-2">
                <Trophy className="w-6 h-6 text-amber-500" />
                Top 3 Recommended Tools
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Based on "{SCENARIO_LABELS[scenario]}" scenario{priorityDims.length > 0 && `, focusing on ${priorityDims.map((d) => DIMENSION_LABELS[d]).join("、")}`}</p>
            </div>
            <button onClick={handleShare} className="inline-flex items-center gap-2 px-4 py-2.5 bg-white dark:bg-gray-900 text-gray-600 dark:text-gray-400 text-sm font-medium rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm hover:border-blue-300 dark:hover:border-blue-700 hover:text-blue-600 dark:hover:text-blue-400 transition-all">
              {copied ? (<><CheckCircle2 className="w-4 h-4 text-emerald-500" />Copied</>) : (<><Share2 className="w-4 h-4" />Share Results</>)}
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {results.map((result) => (
              <div key={result.tool.id} className={`relative bg-white dark:bg-gray-900 rounded-2xl border-2 shadow-sm overflow-hidden transition-all ${result.rank === 1 ? "border-amber-300 dark:border-amber-600 shadow-amber-500/10" : result.rank === 2 ? "border-gray-300 dark:border-gray-700" : "border-orange-200 dark:border-orange-800"}`}>
                <div className={`absolute top-0 right-0 w-12 h-12 flex items-center justify-center text-white font-extrabold text-lg ${result.rank === 1 ? "bg-gradient-to-br from-amber-400 to-amber-600" : result.rank === 2 ? "bg-gradient-to-br from-gray-400 to-gray-600" : "bg-gradient-to-br from-orange-400 to-orange-600"}`} style={{ clipPath: "polygon(0 0, 100% 0, 100% 100%)" }}>
                  {result.rank}
                </div>
                <div className="p-6">
                  <div className="flex items-start gap-4 mb-4 pr-8">
                    <div className="w-14 h-14 flex-shrink-0 flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-2xl font-extrabold shadow-md">
                      {result.tool.name.charAt(0).toUpperCase()}
                    </div>
                    <div className="min-w-0">
                      <h3 className="text-lg font-bold text-gray-900 dark:text-white truncate">{result.tool.name}</h3>
                      <p className="text-xs text-gray-400 dark:text-gray-500">{result.tool.vendor}</p>
                      <div className="flex items-center gap-2 mt-1.5">
                        <span className={`px-2 py-0.5 rounded-md text-xs font-bold ${GRADE_STYLES[result.scoreResult.grade]}`}>{result.scoreResult.grade} Grade</span>
                        <span className="text-xs text-gray-400 dark:text-gray-500">Overall {result.scoreResult.total.toFixed(1)}/10</span>
                      </div>
                    </div>
                  </div>
                  <div className="mb-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Match Score</span>
                      <span className="text-xl font-extrabold text-blue-600 dark:text-blue-400">{result.matchScore.toFixed(1)}<span className="text-xs text-gray-400 dark:text-gray-500 font-normal">/100</span></span>
                    </div>
                    <div className="h-2 bg-white dark:bg-gray-800 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-700" style={{ width: `${result.matchScore}%` }} />
                    </div>
                  </div>
                  <div className="mb-4">
                    <div className="flex items-center gap-1.5 mb-2">
                      <Lightbulb className="w-4 h-4 text-amber-500" />
                      <span className="text-xs font-semibold text-gray-600 dark:text-gray-400">Why Recommended</span>
                    </div>
                    <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{result.recommendationReason}</p>
                  </div>
                  {result.matchedDimensions.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mb-4">
                      {result.matchedDimensions.map((dim) => (
                        <span key={dim} className="px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-md text-xs font-medium">✓ {DIMENSION_LABELS[dim]}</span>
                      ))}
                    </div>
                  )}
                  <Link href={`/tools/${result.tool.slug}`} className="block w-full py-2.5 text-center text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 rounded-xl hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors">
                    View Full Review →
                  </Link>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 shadow-sm p-6 sm:p-8">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-600" />
              Six-Dimension Radar Chart Comparison
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {results.map((result) => (
                <div key={result.tool.id} className="text-center">
                  <div className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">{result.rank}. {result.tool.name}</div>
                  <div className="flex justify-center">
                    <RadarChart scores={result.tool.scores} size={240} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
