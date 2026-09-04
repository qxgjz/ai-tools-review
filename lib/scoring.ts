/* ============================================================
 * 六维加权评分计算引擎
 * ============================================================ */

import type { Score, ScoreDimension, Grade, ScoreResult } from "@/types";

/** 六维权重配置（总和=100%） */
export const SCORE_WEIGHTS: Record<ScoreDimension, number> = {
  functionality: 0.25, // 功能与输出质量 25%
  ux: 0.2, // User Experience 20%
  pricing: 0.2, // 价格与价值 20%
  integration: 0.15, // 集成与开发者体验 15%
  support: 0.1, // 支持与可靠性 10%
  ethics: 0.1, // 伦理与透明度 10%
};

/** 六维中文标签 */
export const DIMENSION_LABELS: Record<ScoreDimension, string> = {
  functionality: "Functionality",
  ux: "User Experience",
  pricing: "Pricing & Value",
  integration: "Integrations",
  support: "Support & Reliability",
  ethics: "Ethics & Transparency",
};

/** 等级描述 */
export const GRADE_DESCRIPTIONS: Record<Grade, string> = {
  S: "卓越",
  A: "优秀",
  B: "良好",
  C: "一般",
  D: "较差",
  F: "不推荐",
};

/**
 * 计算加权总分
 * @param scores 六维评分
 * @returns 加权总分 0-10
 */
export function calculateTotal(scores: Score): number {
  return (
    scores.functionality * SCORE_WEIGHTS.functionality +
    scores.ux * SCORE_WEIGHTS.ux +
    scores.pricing * SCORE_WEIGHTS.pricing +
    scores.integration * SCORE_WEIGHTS.integration +
    scores.support * SCORE_WEIGHTS.support +
    scores.ethics * SCORE_WEIGHTS.ethics
  );
}

/**
 * 根据总分获取等级
 * 9.0+ = S | 8.0-8.9 = A | 7.0-7.9 = B | 6.0-6.9 = C | 5.0-5.9 = D | <5.0 = F
 */
export function getGrade(total: number): Grade {
  if (total >= 9.0) return "S";
  if (total >= 8.0) return "A";
  if (total >= 7.0) return "B";
  if (total >= 6.0) return "C";
  if (total >= 5.0) return "D";
  return "F";
}

/**
 * 获取等级对应的 Tailwind 颜色类
 */
export function getGradeColor(grade: Grade): string {
  const colors: Record<Grade, string> = {
    S: "text-amber-600",
    A: "text-emerald-600",
    B: "text-blue-600",
    C: "text-yellow-600",
    D: "text-red-600",
    F: "text-gray-500",
  };
  return colors[grade];
}

/**
 * 计算完整评分结果（总分 + 等级 + 各维度加权分）
 */
export function calculateScoreResult(scores: Score): ScoreResult {
  const total = calculateTotal(scores);
  const grade = getGrade(total);
  const breakdown = {} as Record<ScoreDimension, number>;

  (Object.keys(SCORE_WEIGHTS) as ScoreDimension[]).forEach((dim) => {
    breakdown[dim] = scores[dim] * SCORE_WEIGHTS[dim];
  });

  return { total, grade, breakdown };
}
