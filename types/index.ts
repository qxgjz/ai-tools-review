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
  subcategory?: string;
  vendor: string;
  description: string;
  scores: Score;
  pros: string[];
  cons: string[];
  pricing: PricingTier[];
  tags: string[];
  hasFreeTier: boolean;
  officialUrl?: string;
  affiliateUrl?: string;
  lastUpdated: string;
  // Extended fields for rich content
  longDescription?: string;
  overallScore?: number;
  grade?: string;
  publishedDate?: string;
  author?: string | { name?: string; role?: string; bio?: string };
  testingPeriod?: string;
  testingDetails?: string | { testing_methodology?: string; benchmark_tests?: string[] };
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
  // Extended pricing fields
  no_credit_card?: boolean;
  free_quota?: string;
  hidden_cost?: string;
  // Extended author (with role)
  // Extended review content
  realExperience?: string;
  usageScenarios?: string[];
  notableObservations?: string[];
  testMetrics?: Array<{ name?: string; value?: string; score?: number; metric?: string; test?: string; comparison?: string }>;
}

/** 文章数据 */
export interface Post {
  slug: string;
  title: string;
  description?: string;
  excerpt?: string;
  content?: string;
  category: string;
  categorySlug?: string;
  date?: string;
  publishedAt?: string;
  updatedAt?: string;
  lastUpdated?: string;
  tags?: string[];
  author?: string;
  image?: string | null;
  readingTime?: string | number;
  readTime?: string | number;
  wordCount?: number;
  hasRealScreenshots?: boolean;
  featured?: boolean;
  faq?: Array<{ q?: string; a?: string; question?: string; answer?: string }>;
  relatedTools?: string[];
}

/** 对比页数据 */
export interface Comparison {
  slug: string;
  title?: string;
  description?: string;
  tools?: Array<{ slug?: string; name?: string; scores?: Record<string, number> }>;
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
