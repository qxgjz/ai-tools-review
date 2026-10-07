"""
AIToolCrux opengtm 工具包封装
opengtm是开源AI GTM工具包，用Gemini + Google Search grounding，真实数据无幻觉。

功能：
- 找线索、评分ICP fit
- 生成外联邮件
- 审计AEO健康（AI Engine Optimization）
- 关键词研究（Google Search grounding，无幻觉）
- 与Claude Code原生集成

用法：
  from scripts.opengtm_toolkit import OpenGTMToolkit
  gtm = OpenGTMToolkit()
  result = gtm.keyword_research("best ai tools")
  aeo = gtm.aeo_audit("https://aitoolcrux.com")
"""
import os
import json
from typing import List, Dict, Optional, Any

try:
    import opengtm
    GT_AVAILABLE = True
except ImportError:
    GT_AVAILABLE = False
    print("[WARN] opengtm未安装。运行: pip install opengtm")


class OpenGTMToolkit:
    """opengtm封装，提供AEO审计和关键词研究接口"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        self.available = GT_AVAILABLE
        self._modules = {}
        self._init_modules()

    def _init_modules(self):
        """初始化可用模块"""
        if not self.available:
            return

        module_names = [
            "keywords", "research", "outreach", "qualify",
            "discover", "analytics", "sitemap", "blog", "sync"
        ]

        for name in module_names:
            try:
                module = __import__(f"opengtm.{name}", fromlist=[name])
                self._modules[name] = module
            except (ImportError, AttributeError):
                pass

    def status(self) -> Dict[str, Any]:
        """获取工具包状态"""
        return {
            "opengtm_installed": self.available,
            "available_modules": len(self._modules),
            "modules": list(self._modules.keys()),
            "google_api_key_configured": bool(self.api_key),
        }

    def keyword_research(self, seed_keyword: str, limit: int = 20) -> Dict[str, Any]:
        """
        关键词研究（用Google Search grounding，无幻觉）
        返回：相关关键词、搜索量、竞争度、搜索意图
        """
        if not self.available:
            return {"error": "opengtm未安装", "seed": seed_keyword}

        try:
            if "keyword_research" in self._modules:
                result = self._modules["keyword_research"].research(
                    seed_keyword,
                    limit=limit,
                    api_key=self.api_key,
                )
                return result
            else:
                return self._fallback_keyword_research(seed_keyword)
        except Exception as e:
            return {"error": str(e), "seed": seed_keyword, "fallback": self._fallback_keyword_research(seed_keyword)}

    def _fallback_keyword_research(self, seed: str) -> Dict[str, Any]:
        """降级方案：基础关键词扩展"""
        prefixes = ["best", "top", "free", "cheap", "vs", "alternative", "how to use", "review", "tutorial"]
        suffixes = ["2026", "for beginners", "for business", "for students", "reddit", "quora"]

        keywords = []
        for p in prefixes:
            keywords.append(f"{p} {seed}")
        for s in suffixes:
            keywords.append(f"{seed} {s}")

        return {
            "seed": seed,
            "keywords": keywords[:15],
            "note": "使用基础扩展，建议安装opengtm获取真实搜索量数据",
        }

    def aeo_audit(self, url: str) -> Dict[str, Any]:
        """
        AEO（AI Engine Optimization）健康审计
        检查网站对AI搜索引擎的友好度：
        - 内容是否容易被AI引用
        - 结构化数据是否完善
        - 答案质量是否高
        - 是否有清晰的事实和数据
        """
        if not self.available:
            return {"error": "opengtm未安装", "url": url}

        try:
            if "aeo_audit" in self._modules:
                result = self._modules["aeo_audit"].audit(url, api_key=self.api_key)
                return result
            else:
                return self._basic_aeo_audit(url)
        except Exception as e:
            return {"error": str(e), "url": url, "fallback": self._basic_aeo_audit(url)}

    def _basic_aeo_audit(self, url: str) -> Dict[str, Any]:
        """基础AEO审计（降级方案）"""
        return {
            "url": url,
            "score": 0,
            "checks": {
                "structured_data": "需要检查Article/FAQPage/Product schema",
                "answer_quality": "需要检查是否有清晰的问答格式内容",
                "fact_verifiability": "需要检查数据是否有来源引用",
                "content_depth": "需要检查内容深度是否足够被AI引用",
                "entity_recognition": "需要检查是否有清晰的实体标注",
            },
            "recommendations": [
                "添加FAQPage schema，让AI更容易引用问答内容",
                "添加Article schema，标注作者、发布日期、更新日期",
                "在文章中使用清晰的问答格式，AI偏好引用直接答案",
                "所有数据和统计都要有来源链接，AI不信任无来源数据",
                "使用清晰的标题层级（H1-H3），AI更容易理解内容结构",
            ],
            "note": "基础AEO审计，建议安装opengtm获取完整评估",
        }

    def competitor_gap(self, domain: str, competitors: List[str]) -> Dict[str, Any]:
        """竞品差距分析（用Google Search grounding）"""
        if not self.available:
            return {"error": "opengtm未安装", "domain": domain}

        try:
            if "search_grounding" in self._modules:
                result = self._modules["search_grounding"].analyze_competitors(
                    domain, competitors, api_key=self.api_key
                )
                return result
            else:
                return {"error": "search_grounding模块不可用", "domain": domain}
        except Exception as e:
            return {"error": str(e), "domain": domain}


# 命令行使用
if __name__ == "__main__":
    import sys

    gtm = OpenGTMToolkit()
    status = gtm.status()

    print("=== opengtm 工具包状态 ===")
    print(f"已安装: {status['opengtm_installed']}")
    print(f"可用模块: {status['available_modules']}")
    print(f"模块: {', '.join(status['modules'])}")
    print(f"Google API Key: {'已配置' if status['google_api_key_configured'] else '未配置'}")

    if len(sys.argv) > 1:
        if sys.argv[1] == "keyword" and len(sys.argv) > 2:
            keyword = " ".join(sys.argv[2:])
            print(f"\n=== 关键词研究: {keyword} ===")
            result = gtm.keyword_research(keyword)
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

        elif sys.argv[1] == "aeo" and len(sys.argv) > 2:
            url = sys.argv[2]
            print(f"\n=== AEO审计: {url} ===")
            result = gtm.aeo_audit(url)
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print("\n用法:")
        print("  python opengtm_toolkit.py                  # 查看状态")
        print("  python opengtm_toolkit.py keyword <词>     # 关键词研究")
        print("  python opengtm_toolkit.py aeo <URL>        # AEO健康审计")
