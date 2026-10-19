/* ============================================================
 * 评测生成器核心计算逻辑
 * 使用 data/tools-compact.json（精简字段，~118KB）替代全量
 * tools.json（~8MB），避免 'use client' 页把全量数据打包进 JS。
 * tools.json 更新后需重跑: python scripts/build_tools_compact.py
 * ============================================================ */

import toolsData from '@/data/tools-compact.json';
import type { Score, ScoreDimension } from '@/types';
import { calculateScoreResult, DIMENSION_LABELS } from '@/lib/scoring';

/** generator 页所需的精简工具结构（字段裁剪集见 build_tools_compact.py） */
export interface CompactTool {
  id: string;
  slug: string;
  name: string;
  vendor: string;
  category: string;
  scores: Score;
  hasFreeTier: boolean;
}

export type ScenarioType = 'writing' | 'design' | 'coding' | 'video' | 'office' | 'other';

export interface GeneratorInput {
  scenario: ScenarioType;
  priorityDimensions: ScoreDimension[];
}

export interface GeneratorResult {
  tool: CompactTool;
  matchScore: number;
  rank: number;
  recommendationReason: string;
  matchedDimensions: ScoreDimension[];
  scoreResult: ReturnType<typeof calculateScoreResult>;
}

export const SCENARIO_LABELS: Record<ScenarioType, string> = {
  writing: 'Content Writing',
  design: 'Design & Creation',
  coding: 'Programming',
  video: 'Video Production',
  office: 'Productivity',
  other: 'General Use',
};

export const SCENARIO_DESCRIPTIONS: Record<ScenarioType, string> = {
  writing: 'Copywriting, article writing, content polishing',
  design: 'Image generation, UI design, visual creation',
  coding: 'Coding, programming, tech development',
  video: 'Video generation, editing, multimedia creation',
  office: 'Document processing, meeting notes, team collaboration',
  other: 'General Use',
};

const SCENARIO_DIMENSION_BOOST: Record<ScenarioType, ScoreDimension[]> = {
  writing: ['functionality', 'ux', 'pricing'],
  design: ['functionality', 'ux', 'integration'],
  coding: ['functionality', 'integration', 'support'],
  video: ['functionality', 'ux', 'pricing'],
  office: ['ux', 'pricing', 'integration'],
  other: ['functionality', 'ux', 'pricing'],
};

const SCENARIO_CATEGORY_MAP: Record<ScenarioType, string[]> = {
  writing: ['writing', 'chat'],
  design: ['image', 'audio'],
  coding: ['code'],
  video: ['video', 'audio'],
  office: ['productivity', 'search'],
  other: [],
};

export function generateRecommendations(
  input: GeneratorInput,
  topN: number = 3,
): GeneratorResult[] {
  const { scenario, priorityDimensions } = input;
  const allPriorityDims = new Set<ScoreDimension>([
    ...priorityDimensions,
    ...(SCENARIO_DIMENSION_BOOST[scenario] || []),
  ]);

  const results: GeneratorResult[] = (toolsData as CompactTool[]).map((tool) => {
    const scoreResult = calculateScoreResult(tool.scores);
    let matchScore = scoreResult.total * 5;
    let priorityBonus = 0;
    const matchedDims: ScoreDimension[] = [];

    allPriorityDims.forEach((dim) => {
      const dimScore = tool.scores[dim];
      if (dimScore >= 7) {
        priorityBonus += dimScore * 1.5;
        matchedDims.push(dim);
      } else if (dimScore >= 5) {
        priorityBonus += dimScore * 0.5;
      }
    });

    let scenarioBonus = 0;
    if (SCENARIO_CATEGORY_MAP[scenario]?.includes(tool.category)) {
      scenarioBonus = 10;
    }

    matchScore = Math.min(100, Math.max(0, matchScore + priorityBonus + scenarioBonus));

    const recommendationReason = generateReason(tool, scoreResult.total, matchedDims, scenario);

    return {
      tool,
      matchScore: Math.round(matchScore * 10) / 10,
      rank: 0,
      recommendationReason,
      matchedDimensions: matchedDims,
      scoreResult,
    };
  });

  results.sort((a, b) => b.matchScore - a.matchScore);
  return results.slice(0, topN).map((r, i) => ({ ...r, rank: i + 1 }));
}

function generateReason(
  tool: CompactTool,
  total: number,
  matchedDims: ScoreDimension[],
  scenario: ScenarioType,
): string {
  const parts: string[] = [];
  parts.push(`${tool.name} overall score ${total.toFixed(1)}/10`);
  if (matchedDims.length > 0) {
    const dimNames = matchedDims.map((d) => DIMENSION_LABELS[d]).join(', ');
    parts.push(`stands out in ${dimNames}`);
  }
  if (tool.hasFreeTier) parts.push('Free version available to try');
  parts.push(`best suited for ${SCENARIO_LABELS[scenario] || 'General'} use cases`);
  return parts.join('. ') + '.';
}

export function getScenarioOptions() {
  return (Object.keys(SCENARIO_LABELS) as ScenarioType[]).map((key) => ({
    value: key,
    label: SCENARIO_LABELS[key],
    description: SCENARIO_DESCRIPTIONS[key],
  }));
}
