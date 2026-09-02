/* ============================================================
 * 评测生成器核心计算逻辑
 * ============================================================ */

import toolsData from "@/data/tools.json";
import type { Tool, ScoreDimension } from "@/types";
import { calculateScoreResult, DIMENSION_LABELS } from "@/lib/scoring";

export type ScenarioType =
  | "writing"
  | "design"
  | "coding"
  | "video"
  | "office"
  | "other";

export interface GeneratorInput {
  scenario: ScenarioType;
  priorityDimensions: ScoreDimension[];
}

export interface GeneratorResult {
  tool: Tool;
  matchScore: number;
  rank: number;
  recommendationReason: string;
  matchedDimensions: ScoreDimension[];
  scoreResult: ReturnType<typeof calculateScoreResult>;
}

export const SCENARIO_LABELS: Record<ScenarioType, string> = {
  writing: "内容写作",
  design: "设计创作",
  coding: "编程开发",
  video: "视频制作",
  office: "效率办公",
  other: "其他通用",
};

export const SCENARIO_DESCRIPTIONS: Record<ScenarioType, string> = {
  writing: "文案创作、文章撰写、内容润色",
  design: "图像生成、UI设计、视觉创作",
  coding: "代码编写、程序开发、技术研发",
  video: "视频生成、剪辑制作、多媒体创作",
  office: "文档处理、会议纪要、团队协作",
  other: "其他通用AI使用场景",
};

const SCENARIO_DIMENSION_BOOST: Record<ScenarioType, ScoreDimension[]> = {
  writing: ["functionality", "ux", "pricing"],
  design: ["functionality", "ux", "integration"],
  coding: ["functionality", "integration", "support"],
  video: ["functionality", "ux", "pricing"],
  office: ["ux", "pricing", "integration"],
  other: ["functionality", "ux", "pricing"],
};

const SCENARIO_CATEGORY_MAP: Record<ScenarioType, string[]> = {
  writing: ["writing", "chat"],
  design: ["image", "audio"],
  coding: ["code"],
  video: ["video", "audio"],
  office: ["productivity", "search"],
  other: [],
};

export function generateRecommendations(
  input: GeneratorInput,
  topN: number = 3
): GeneratorResult[] {
  const { scenario, priorityDimensions } = input;
  const allPriorityDims = new Set<ScoreDimension>([
    ...priorityDimensions,
    ...(SCENARIO_DIMENSION_BOOST[scenario] || []),
  ]);

  const results: GeneratorResult[] = (toolsData as Tool[]).map((tool) => {
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
  tool: Tool,
  total: number,
  matchedDims: ScoreDimension[],
  scenario: ScenarioType
): string {
  const parts: string[] = [];
  parts.push(`${tool.name} 综合评分 ${total.toFixed(1)} 分`);
  if (matchedDims.length > 0) {
    const dimNames = matchedDims.map((d) => DIMENSION_LABELS[d]).join("、");
    parts.push(`在${dimNames}方面表现突出`);
  }
  if (tool.hasFreeTier) parts.push("提供免费版本可先体验");
  parts.push(`适合${SCENARIO_LABELS[scenario] || "通用"}场景使用`);
  return parts.join("，") + "。";
}

export function getScenarioOptions() {
  return (Object.keys(SCENARIO_LABELS) as ScenarioType[]).map((key) => ({
    value: key,
    label: SCENARIO_LABELS[key],
    description: SCENARIO_DESCRIPTIONS[key],
  }));
}
