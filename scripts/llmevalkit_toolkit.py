"""
AIToolCrux llmevalkit 内容质量评估工具包
封装llmevalkit的78个指标，用于AI内容质量检查、幻觉检测、合规性检查。

llmevalkit 6.0.0 功能：
- LLM评估、幻觉检测、AI内容检测
- 合规性、文档解析、治理、安全
- 可观测性、ground truth测试
- 对话评估、红队测试、异常检测
- 78个指标，13个模块

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


class LMEvalKit:
    """llmevalkit封装，提供内容质量评估接口"""

    def __init__(self):
        self.available = LLM_AVAILABLE
        self._modules = {}
        self._init_modules()

    def _init_modules(self):
        """初始化可用模块"""
        if not self.available:
            return

        module_names = [
            "hallucination", "ai_content_detection", "compliance",
            "document_parsing", "governance", "security",
            "observability", "ground_truth", "conversation",
            "red_team", "anomaly_detection", "quality", "toxicity"
        ]

        for name in module_names:
            try:
                module = __import__(f"llmevalkit.{name}", fromlist=[name])
                self._modules[name] = module
            except (ImportError, AttributeError):
                pass

    def status(self) -> Dict[str, Any]:
        """获取工具包状态"""
        return {
            "llmevalkit_installed": self.available,
            "available_modules": len(self._modules),
            "modules": list(self._modules.keys()),
            "total_metrics": 78 if self.available else 0,
        }

    def evaluate_content(self, content: str, keyword: str = "", context: str = "") -> Dict[str, Any]:
        """
        综合内容质量评估
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

        # 1. 幻觉检测（最重要，防止AI编造假数据）
        try:
            if "hallucination" in self._modules:
                hall_result = self._modules["hallucination"].detect(content, context=context)
                result["checks"]["hallucination"] = hall_result
                if hall_result.get("detected", False):
                    result["hallucination_detected"] = True
                    result["warnings"].append(f"检测到幻觉: {hall_result.get('details', '')}")
                    result["recommendations"].append("文章中存在可能编造的虚假数据，请核实所有数据来源")
        except Exception as e:
            result["checks"]["hallucination"] = {"error": str(e)}

        # 2. AI内容检测
        try:
            if "ai_content_detection" in self._modules:
                ai_result = self._modules["ai_content_detection"].detect(content)
                result["checks"]["ai_content"] = ai_result
                result["ai_content_probability"] = ai_result.get("probability", 0)
                if ai_result.get("probability", 0) > 0.8:
                    result["warnings"].append(f"AI内容概率过高: {ai_result.get('probability'):.1%}")
                    result["recommendations"].append("增加个人经验、真实案例、独特观点，降低AI内容痕迹")
        except Exception as e:
            result["checks"]["ai_content"] = {"error": str(e)}

        # 3. 质量评估
        try:
            if "quality" in self._modules:
                quality_result = self._modules["quality"].evaluate(content)
                result["checks"]["quality"] = quality_result
                result["score"] = quality_result.get("overall_score", 0)
        except Exception as e:
            result["checks"]["quality"] = {"error": str(e)}

        # 4. 合规性检查
        try:
            if "compliance" in self._modules:
                comp_result = self._modules["compliance"].check(content)
                result["checks"]["compliance"] = comp_result
                if comp_result.get("violations", []):
                    result["warnings"].append(f"合规性问题: {len(comp_result['violations'])}项")
        except Exception as e:
            result["checks"]["compliance"] = {"error": str(e)}

        # 5. 基础检查（字数、关键词密度等）
        result = self._basic_check(content, keyword, result)

        # 计算综合分数
        if result["score"] == 0:
            base_score = 100
            if result["hallucination_detected"]:
                base_score -= 30
            if result["ai_content_probability"] > 0.8:
                base_score -= 15
            if len(content) < 2000:
                base_score -= 10
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
