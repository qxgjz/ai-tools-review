/* ============================================================
 * 全局类型定义
 * ============================================================ */

/** 六维评分维度 */
export type ScoreDimension =
  | "functionality"
  | "ux"
  | "pricing"
  | "integration"
  | "support"
  | "ethics";

/** 六维评分数据 */
export interface Score {
  functionality: number; // 功能与输出质量
  ux: number; // 用户体验
  pricing: number; // 价格与价值
  integration: number; // 集成与开发者体验
  support: number; // 支持与可靠性
  ethics: number; // 伦理与透明度
}

/** 评分等级 */
export type Grade = "S" | "A" | "B" | "C" | "D" | "F";

/** 定价方案 */
export interface PricingTier {
  name: string;
  price: string;
  description?: string;
  recommended?: boolean;
}

/** 工具数据 */
export interface Tool {
  id: string;
  slug: string;
  name: string;
  category: string;
  vendor: string;
  description: string;
  scores: Score;
  pros: string[];
  cons: string[];
  pricing: PricingTier[];
  tags: string[];
  hasFreeTier: boolean;
  officialUrl?: string;
  lastUpdated: string;
  // Extended fields for rich content
  longDescription?: string;
  overallScore?: number;
  grade?: string;
  publishedDate?: string;
  author?: string | { name?: string; bio?: string };
  testingPeriod?: string;
  testingDetails?: string;
  bestFor?: string;
  notIdealFor?: string;
  verdict?: string;
  useCases?: string[];
  keyFeatures?: string[];
  alternatives?: Array<{ name?: string; slug?: string; reason?: string }> | string[];
  ratings?: Record<string, number>;
  related_tools?: Array<{ name?: string; slug?: string }> | string[];
  long_description?: string;
  review?: string;
  review_updated?: string;
  review_author?: string;
  faq?: Array<{ question: string; answer: string }>;
}

/** 评分结果 */
export interface ScoreResult {
  total: number;
  grade: Grade;
  breakdown: Record<ScoreDimension, number>;
}

/** 分类配置 */
export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  iconName: string;
}
