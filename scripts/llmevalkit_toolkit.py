"""
AIToolCrux llmevalkit 内容质量评估工具包
封装llmevalkit的78个指标，用于AI内容质量检查、幻觉检测、合规性检查。

llmevalkit 6.0.2 真实模块结构（2026-10-09 指挥官核实）：
- 顶层: Evaluator, BLEUScore, ROUGEScore, TokenOverlap, SemanticSimilarity,
        KeywordCoverage, AnswerLength, ReadabilityScore, Faithfulness,
        Hallucination, AnswerRelevance, ContextRelevance, Coherence,
        Completeness, Toxicity, GEval (quality/toxicity 类在顶层)
- hallucination (12检测器): Entity/Numeric/Negation/Fabricated/Contradiction/
        SelfConsistency/ConfidenceCalibration/Instruction/SourceCoverage/
        Temporal/Causal/Ranking
- compliance (6): PIIDetector, HIPAACheck, GDPRCheck, DPDPCheck, EUAIActCheck, CustomRule
- governance (4): NISTCheck, CoSAICheck, ISO42001Check, SOC2Check
- security (2): PromptInjectionCheck, BiasDetector
- conversation (4-5): ConversationCompleteness, TurnRelevancy, KnowledgeRetention, TaskCompletion
- detection (6-8): AITextDetector, ContentOriginCheck, AIImageDetector, AIAudioDetector, ImagePixelAnalysis, DeepfakeTextDetector
- doceval (6): FieldAccuracy, FieldCompleteness, FieldHallucination, FormatValidation, ExtractionConsistency, TableExtractionAccuracy
- observe (5-7): EvalLogger, ScoreDrift, ThresholdAlert, EvalComparison, EvalReport
- groundtruth (6-7): ExactMatchAccuracy, FuzzyMatchAccuracy, GroundTruthF1, ContextualPrecision, ContextualRecall, JSONCorrectness
- redteam (4-5): ToxicityProbe, PIIExtractionProbe, JailbreakResistance, InstructionBypass
- anomaly (2-4): OutputAnomalyDetector, ScoreAnomalyDetector
- multimodal (6): OCRAccuracy, AudioTranscriptionAccuracy, ImageTextAlignment, VisionQAAccuracy, DocumentLayoutAccuracy, MultimodalConsistency

用法：
  from scripts.llmevalkit_toolkit import LMEvalKit
  evaluator = LMEvalKit()
  result = evaluator.evaluate_content(article_text, keyword="best ai tools")
  print(result["score"], result["hallucination_detected"])
"""
import os
import json
from typing import List, Dict, Optional, Any

try:
    import llmevalkit
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("[WARN] llmevalkit未安装。运行: pip install llmevalkit")


# 真实模块名映射（README描述名 → Python实际模块名）
# 之前用错的：ai_content_detection/document_parsing/observability/ground_truth/
#            red_team/anomaly_detection/quality/toxicity 全部不存在
REAL_MODULES = {
    "hallucination": "hallucination",
    "compliance": "compliance",
    "governance": "governance",
    "security": "security",
    "conversation": "conversation",
    "detection": "detection",           # 之前错写 ai_content_detection
    "doceval": "doceval",               # 之前错写 document_parsing
    "observe": "observe",               # 之前错写 observability
    "groundtruth": "groundtruth",       # 之前错写 ground_truth
    "redteam": "redteam",               # 之前错写 red_team
    "anomaly": "anomaly",               # 之前错写 anomaly_detection
    "multimodal": "multimodal",
}
# quality/toxicity 类在顶层 llmevalkit 直接导出，不是独立模块


class LMEvalKit:
    """llmevalkit封装，提供内容质量评估接口"""

    def __init__(self):
        self.available = LLM_AVAILABLE
        self._modules = {}
        self._top_level = {}  # 顶层 quality/toxicity 类
        self._init_modules()

    def _init_modules(self):
        """初始化可用模块（用真实模块名）"""
        if not self.available:
            return

        for key, mod_name in REAL_MODULES.items():
            try:
                module = __import__(f"llmevalkit.{mod_name}", fromlist=[mod_name])
                self._modules[key] = module
            except (ImportError, AttributeError):
                pass

        # 顶层 quality/toxicity 类
        try:
            for cls_name in ["BLEUScore", "ROUGEScore", "TokenOverlap",
                             "SemanticSimilarity", "KeywordCoverage",
                             "AnswerLength", "ReadabilityScore",
                             "Faithfulness", "Hallucination",
                             "AnswerRelevance", "ContextRelevance",
                             "Coherence", "Completeness", "Toxicity", "GEval"]:
                if hasattr(llmevalkit, cls_name):
                    self._top_level[cls_name] = getattr(llmevalkit, cls_name)
        except Exception:
            pass

    def status(self) -> Dict[str, Any]:
        """获取工具包状态"""
        return {
            "llmevalkit_installed": self.available,
            "available_modules": len(self._modules),
            "modules": list(self._modules.keys()),
            "top_level_classes": list(self._top_level.keys()),
            "total_metrics": 78 if self.available else 0,
        }

    def evaluate_content(self, content: str, keyword: str = "", context: str = "") -> Dict[str, Any]:
        """
        综合内容质量评估（用真实API: evaluate(answer=..., context=...)）
        返回：分数、幻觉检测、AI内容检测、合规性、质量指标
        """
        result = {
            "content_length": len(content),
            "keyword": keyword,
            "checks": {},
            "warnings": [],
            "score": 0,
            "hallucination_detected": False,
            "ai_content_probability": 0.0,
            "recommendations": [],
        }

        if not self.available:
            result["warnings"].append("llmevalkit未安装，使用基础检查")
            return self._basic_check(content, keyword, result)

        # context 策略：有外部参考用外部参考；无外部参考时用全文自比（仅检测内部矛盾）
        # 注意：绝不能用文章前1/3当context——会导致后半部分数字/实体全被误报为幻觉
        has_external_context = bool(context and context.strip())
        ctx = context if has_external_context else content

        # 1. 幻觉检测
        # - 有外部context：跑全部4检测器（实体/数字/矛盾/编造）
        # - 无外部context：只跑 ContradictionDetector（内部矛盾），其余自比无意义（文章永远匹配自己）
        try:
            if "hallucination" in self._modules:
                hall = self._modules["hallucination"]
                hall_scores = {}
                if has_external_context:
                    detectors = [
                        ("EntityHallucination", "entity"),
                        ("NumericHallucination", "numeric"),
                        ("ContradictionDetector", "contradiction"),
                        ("FabricatedInfo", "fabricated"),
                    ]
                else:
                    # 自对照模式（context=answer）：ContradictionDetector 在纯规则模式下
                    # 误报率 100%（表格 vs 正文重复陈述被误判为 negation_flip）。
                    # 已实测 23/23 误报。跳过，避免误扣分。
                    detectors = []
                    result["warnings"].append(
                        "无外部参考资料，跳过 contradiction 自对照检测（规则模式误报率100%）；"
                        "建议提供工具官网/权威数据作为context做真幻觉检测"
                    )
                for cls_name, label in detectors:
                    try:
                        cls = getattr(hall, cls_name)
                        detector = cls(use_llm=False)
                        r = detector.evaluate(answer=content, context=ctx)
                        hall_scores[label] = {"score": r.score, "reason": r.reason}
                    except Exception:
                        pass
                result["checks"]["hallucination"] = hall_scores
                # 有外部context时才用<0.5判定幻觉；自比模式只看contradiction
                if has_external_context:
                    low = [k for k, v in hall_scores.items() if v["score"] < 0.5]
                    if low:
                        result["hallucination_detected"] = True
                        result["warnings"].append(f"幻觉风险: {', '.join(low)} 分数偏低（与外部参考不符）")
                        result["recommendations"].append("核实文章中所有数据、实体、引用来源，删除无法验证的信息")
                else:
                    # 自比模式：只有contradiction<0.5才算问题
                    if hall_scores.get("contradiction", {}).get("score", 1.0) < 0.5:
                        result["hallucination_detected"] = True
                        result["warnings"].append("文章内部存在前后矛盾")
                        result["recommendations"].append("修正文章中前后不一致的说法")
        except Exception as e:
            result["checks"]["hallucination"] = {"error": str(e)}

        # 2. AI内容检测
        try:
            if "detection" in self._modules:
                det = self._modules["detection"]
                if hasattr(det, "AITextDetector"):
                    detector = det.AITextDetector()
                    r = detector.evaluate(answer=content)
                    # score: 0.0=likely AI, 1.0=likely human
                    ai_prob = 1.0 - r.score
                    result["checks"]["ai_content"] = {"score": r.score, "ai_probability": ai_prob}
                    result["ai_content_probability"] = ai_prob
                    if ai_prob > 0.8:
                        result["warnings"].append(f"AI内容概率过高: {ai_prob:.1%}")
                        result["recommendations"].append("增加个人经验、真实案例、独特观点，降低AI内容痕迹")
        except Exception as e:
            result["checks"]["ai_content"] = {"error": str(e)}

        # 3. 隐私泄漏检测（PII）
        try:
            if "compliance" in self._modules:
                comp = self._modules["compliance"]
                if hasattr(comp, "PIIDetector"):
                    detector = comp.PIIDetector(use_llm=False)
                    r = detector.evaluate(answer=content)
                    result["checks"]["pii"] = {"score": r.score, "details": str(r.details)[:200]}
                    if r.score < 1.0:
                        result["warnings"].append("检测到潜在隐私信息(PII)")
                        result["recommendations"].append("移除文章中的个人隐私信息")
        except Exception as e:
            result["checks"]["pii"] = {"error": str(e)}

        # 4. 异常检测（内容是否异常：过短/重复/主题漂移）
        try:
            if "anomaly" in self._modules:
                anom = self._modules["anomaly"]
                if hasattr(anom, "OutputAnomalyDetector"):
                    detector = anom.OutputAnomalyDetector()
                    r = detector.evaluate(answer=content, context=ctx)
                    result["checks"]["anomaly"] = {"score": r.score, "details": str(r.details)[:200]}
        except Exception as e:
            result["checks"]["anomaly"] = {"error": str(e)}

        # 5. 基础检查（字数、关键词密度等）
        result = self._basic_check(content, keyword, result)

        # 计算综合分数（0-100）
        if result["score"] == 0:
            base_score = 100
            if result["hallucination_detected"]:
                base_score -= 30
            if result["ai_content_probability"] > 0.8:
                base_score -= 15
            if len(content) < 2000:
                base_score -= 10
            # 幻觉各检测器分数拉低
            hall = result["checks"].get("hallucination", {})
            if isinstance(hall, dict):
                for k, v in hall.items():
                    if isinstance(v, dict) and "score" in v:
                        base_score -= int((1 - v["score"]) * 5)
            result["score"] = max(0, base_score)

        return result

    def _basic_check(self, content: str, keyword: str, result: Dict) -> Dict:
        """基础内容检查（llmevalkit不可用时的降级方案）"""
        word_count = len(content.split())
        char_count = len(content)

        # 字数检查
        if word_count < 2000:
            result["warnings"].append(f"字数不足: {word_count}词 < 2000词")
            result["recommendations"].append("扩充内容到2000词以上，增加深度分析")

        # FAQ检查
        has_faq = "faq" in content.lower() or "q:" in content.lower() or "问：" in content
        if not has_faq:
            result["warnings"].append("缺少FAQ部分")
            result["recommendations"].append("添加FAQ部分，回答5-8个常见问题")

        # 截图/图片检查
        has_images = "![" in content or "<img" in content or "screenshot" in content.lower()
        if not has_images:
            result["warnings"].append("缺少截图/图片")
            result["recommendations"].append("添加2-5张高质量截图或对比图")

        # 内链检查
        has_internal_links = "/blog/" in content or "/tools/" in content or "/compare/" in content
        if not has_internal_links:
            result["recommendations"].append("添加2-3个内部链接，提升网站SEO")

        # 关键词密度
        if keyword:
            keyword_count = content.lower().count(keyword.lower())
            density = keyword_count / max(word_count, 1) * 100
            result["keyword_density"] = f"{density:.2f}%"
            if density > 3:
                result["warnings"].append(f"关键词密度过高: {density:.2f}% > 3%")
            elif density < 0.5:
                result["warnings"].append(f"关键词密度过低: {density:.2f}% < 0.5%")

        result["word_count"] = word_count
        result["char_count"] = char_count
        return result

    def batch_evaluate(self, articles: List[Dict[str, str]]) -> List[Dict]:
        """批量评估多篇文章"""
        results = []
        for article in articles:
            result = self.evaluate_content(
                content=article.get("content", ""),
                keyword=article.get("keyword", ""),
                context=article.get("context", ""),
            )
            result["title"] = article.get("title", "")
            result["slug"] = article.get("slug", "")
            results.append(result)
        return results

    def get_rewrite_recommendations(self, evaluation: Dict) -> List[str]:
        """根据评估结果生成具体的重写建议"""
        recs = []
        if evaluation.get("hallucination_detected"):
            recs.append("【P0】核实文章中所有数据、统计数字、引用来源，删除无法验证的虚假信息")
        if evaluation.get("ai_content_probability", 0) > 0.8:
            recs.append("【P0】增加个人使用体验、真实案例、独特观点，加入口语化表达")
        if evaluation.get("word_count", 0) < 2000:
            recs.append("【P1】扩充内容到2000词以上，增加：使用教程、对比表格、优缺点分析、适用场景")
        if "缺少FAQ部分" in str(evaluation.get("warnings", [])):
            recs.append("【P1】添加FAQ部分，回答5-8个用户最常问的问题")
        if "缺少截图/图片" in str(evaluation.get("warnings", [])):
            recs.append("【P1】添加2-5张高质量截图：工具界面、使用流程、对比效果")
        if not recs:
            recs.append("文章质量良好，无需重大修改")
        return recs


# 命令行使用
if __name__ == "__main__":
    import sys

    evaluator = LMEvalKit()
    status = evaluator.status()

    print("=== llmevalkit 工具包状态 ===")
    print(f"已安装: {status['llmevalkit_installed']}")
    print(f"可用模块: {status['available_modules']}")
    print(f"总指标数: {status['total_metrics']}")
    print(f"模块: {', '.join(status['modules'])}")
    print(f"顶层类: {', '.join(status['top_level_classes'])}")

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_content = """
        ChatGPT is the best AI tool in 2026. It has 1 billion users and can do anything.
        According to a study by Harvard, ChatGPT is 99% accurate.
        """
        print("\n=== 测试评估 ===")
        result = evaluator.evaluate_content(test_content, keyword="ChatGPT")
        print(f"分数: {result['score']}")
        print(f"幻觉检测: {result['hallucination_detected']}")
        print(f"AI内容概率: {result['ai_content_probability']:.1%}")
        print(f"警告: {result['warnings']}")
        print(f"建议: {result['recommendations']}")
