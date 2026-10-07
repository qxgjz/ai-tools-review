"""
AIToolCrux zens-ink 全模块工具包
封装zens-ink的23个功能模块，提供统一接口，所有窗口都可以调用。

zens-ink模块清单：
1.  kd - 关键词难度分析
2.  search_intent - 搜索意图分类
3.  keyword_research - 关键词研究
4.  keyword_volume - 关键词搜索量
5.  keyword_cluster - 关键词聚类
6.  kgr_auto - KGR（关键词黄金比例）自动化
7.  content_qc - 内容质量检查
8.  content_matrix - 内容矩阵规划
9.  onpage_audit - 页面SEO审计
10. site_audit - 全站SEO审计
11. rank_tracker - 排名追踪
12. serp_intent - SERP意图分析
13. search_performance - 搜索表现分析
14. competitor_gap - 竞品差距分析
15. domain_rating - 域名评级
16. backlink_analysis - 外链分析
17. reddit_blueocean - Reddit蓝海机会
18. geo_fanout - GEO（生成式引擎优化）分发
19. ai_crawler_audit - AI爬虫审计
20. brave_volume - Brave搜索量
21. llms_gen - LLM内容生成
22. setup_gsc - GSC设置
23. mcp - MCP协议服务

用法：
  from scripts.zens_ink_toolkit import ZensInkToolkit
  toolkit = ZensInkToolkit()
  difficulty = toolkit.keyword_difficulty("best ai tools 2026")
  intent = toolkit.search_intent("how to use chatgpt")
"""
import os
import json
from typing import List, Dict, Optional, Any

try:
    import zens_ink
    ZENS_AVAILABLE = True
except ImportError:
    ZENS_AVAILABLE = False
    print("[WARN] zens-ink未安装。运行: pip install zens-ink")


class ZensInkToolkit:
    """zens-ink全模块封装，提供统一接口"""

    def __init__(self, serper_api_key=None):
        self.serper_api_key = serper_api_key or os.environ.get("SERPER_API_KEY", "")
        self._modules = {}
        self._available_modules = []
        self._unavailable_modules = []

        if ZENS_AVAILABLE:
            self._init_modules()

    def _init_modules(self):
        """初始化所有可用模块"""
        module_names = [
            "kd", "search_intent", "keyword_research", "keyword_volume",
            "keyword_cluster", "kgr_auto", "content_qc", "content_matrix",
            "onpage_audit", "site_audit", "rank_tracker", "serp_intent",
            "search_performance", "competitor_gap", "domain_rating",
            "reddit_blueocean", "geo_fanout", "ai_crawler_audit",
            "brave_volume", "llms_gen", "setup_gsc", "mcp"
        ]

        for name in module_names:
            try:
                module = __import__(f"zens_ink.{name}", fromlist=[name])
                self._modules[name] = module
                self._available_modules.append(name)
            except (ImportError, AttributeError) as e:
                self._unavailable_modules.append(f"{name} ({str(e)[:50]})")

    def status(self) -> Dict[str, Any]:
        """获取工具包状态"""
        return {
            "zens_ink_installed": ZENS_AVAILABLE,
            "available_modules": len(self._available_modules),
            "unavailable_modules": len(self._unavailable_modules),
            "available": self._available_modules,
            "unavailable": self._unavailable_modules,
        }

    # ========== 关键词研究模块 ==========

    def keyword_difficulty(self, keyword: str) -> Dict:
        """关键词难度分析"""
        if "kd" not in self._modules:
            return {"error": "kd模块不可用"}
        try:
            return self._modules["kd"].analyze(keyword)
        except Exception as e:
            return {"error": str(e), "keyword": keyword}

    def search_intent(self, keyword: str) -> Dict:
        """搜索意图分类（信息型/导航型/交易型/商业型）"""
        if "search_intent" not in self._modules:
            return {"error": "search_intent模块不可用"}
        try:
            return self._modules["search_intent"].classify(keyword)
        except Exception as e:
            return {"error": str(e), "keyword": keyword}

    def keyword_research(self, seed_keyword: str, limit: int = 50) -> List[Dict]:
        """关键词研究，从种子词扩展相关关键词"""
        if "keyword_research" not in self._modules:
            return [{"error": "keyword_research模块不可用"}]
        try:
            return self._modules["keyword_research"].research(seed_keyword, limit=limit)
        except Exception as e:
            return [{"error": str(e), "seed": seed_keyword}]

    def keyword_volume(self, keywords: List[str]) -> Dict[str, int]:
        """批量查询关键词搜索量"""
        if "keyword_volume" not in self._modules:
            return {"error": "keyword_volume模块不可用"}
        try:
            return self._modules["keyword_volume"].get_volumes(keywords)
        except Exception as e:
            return {"error": str(e)}

    def keyword_cluster(self, keywords: List[str]) -> Dict[str, List[str]]:
        """关键词聚类，按主题分组"""
        if "keyword_cluster" not in self._modules:
            return {"error": "keyword_cluster模块不可用"}
        try:
            return self._modules["keyword_cluster"].cluster(keywords)
        except Exception as e:
            return {"error": str(e)}

    def kgr_analysis(self, keyword: str) -> Dict:
        """KGR（关键词黄金比例）分析，找出低竞争高价值关键词"""
        if "kgr_auto" not in self._modules:
            return {"error": "kgr_auto模块不可用"}
        try:
            return self._modules["kgr_auto"].analyze(keyword)
        except Exception as e:
            return {"error": str(e), "keyword": keyword}

    # ========== 内容模块 ==========

    def content_quality_check(self, content: str, keyword: str = "") -> Dict:
        """内容质量检查（可读性、关键词密度、结构完整性）"""
        if "content_qc" not in self._modules:
            return {"error": "content_qc模块不可用"}
        try:
            return self._modules["content_qc"].analyze(content, keyword=keyword)
        except Exception as e:
            return {"error": str(e)}

    def content_matrix(self, topic: str) -> Dict:
        """内容矩阵规划，找出主题下应该写的所有内容类型"""
        if "content_matrix" not in self._modules:
            return {"error": "content_matrix模块不可用"}
        try:
            return self._modules["content_matrix"].generate(topic)
        except Exception as e:
            return {"error": str(e), "topic": topic}

    # ========== SEO审计模块 ==========

    def onpage_audit(self, url: str) -> Dict:
        """单页面SEO审计"""
        if "onpage_audit" not in self._modules:
            return {"error": "onpage_audit模块不可用"}
        try:
            return self._modules["onpage_audit"].audit(url)
        except Exception as e:
            return {"error": str(e), "url": url}

    def site_audit(self, domain: str) -> Dict:
        """全站SEO审计"""
        if "site_audit" not in self._modules:
            return {"error": "site_audit模块不可用"}
        try:
            return self._modules["site_audit"].audit(domain)
        except Exception as e:
            return {"error": str(e), "domain": domain}

    # ========== 排名与SERP模块 ==========

    def rank_tracker(self, domain: str, keywords: List[str]) -> Dict:
        """排名追踪，监控域名在指定关键词的排名"""
        if "rank_tracker" not in self._modules:
            return {"error": "rank_tracker模块不可用"}
        try:
            return self._modules["rank_tracker"].track(domain, keywords)
        except Exception as e:
            return {"error": str(e), "domain": domain}

    def serp_intent(self, keyword: str) -> Dict:
        """SERP意图分析，分析搜索结果页的内容类型和排名特征"""
        if "serp_intent" not in self._modules:
            return {"error": "serp_intent模块不可用"}
        try:
            return self._modules["serp_intent"].analyze(keyword)
        except Exception as e:
            return {"error": str(e), "keyword": keyword}

    def search_performance(self, domain: str) -> Dict:
        """搜索表现分析，综合评估域名的SEO表现"""
        if "search_performance" not in self._modules:
            return {"error": "search_performance模块不可用"}
        try:
            return self._modules["search_performance"].analyze(domain)
        except Exception as e:
            return {"error": str(e), "domain": domain}

    # ========== 竞品与外链模块 ==========

    def competitor_gap(self, domain: str, competitors: List[str]) -> Dict:
        """竞品差距分析，找出竞品有但你没有的关键词和内容"""
        if "competitor_gap" not in self._modules:
            return {"error": "competitor_gap模块不可用"}
        try:
            return self._modules["competitor_gap"].analyze(domain, competitors)
        except Exception as e:
            return {"error": str(e), "domain": domain}

    def domain_rating(self, domain: str) -> Dict:
        """域名评级（DR），评估域名权威度"""
        if "domain_rating" not in self._modules:
            return {"error": "domain_rating模块不可用"}
        try:
            return self._modules["domain_rating"].get(domain)
        except Exception as e:
            return {"error": str(e), "domain": domain}

    # ========== 增长机会模块 ==========

    def reddit_blueocean(self, subreddit: str = "all") -> List[Dict]:
        """Reddit蓝海机会，找出高赞低评论的帖子（内容机会）"""
        if "reddit_blueocean" not in self._modules:
            return [{"error": "reddit_blueocean模块不可用"}]
        try:
            return self._modules["reddit_blueocean"].find(subreddit)
        except Exception as e:
            return [{"error": str(e)}]

    def geo_optimization(self, content: str, keyword: str) -> Dict:
        """GEO（生成式引擎优化）优化，让内容更容易被AI搜索引用"""
        if "geo_fanout" not in self._modules:
            return {"error": "geo_fanout模块不可用"}
        try:
            return self._modules["geo_fanout"].optimize(content, keyword)
        except Exception as e:
            return {"error": str(e)}

    def ai_crawler_audit(self, url: str) -> Dict:
        """AI爬虫审计，检查网站对AI爬虫的友好度"""
        if "ai_crawler_audit" not in self._modules:
            return {"error": "ai_crawler_audit模块不可用"}
        try:
            return self._modules["ai_crawler_audit"].audit(url)
        except Exception as e:
            return {"error": str(e), "url": url}

    # ========== 综合工具 ==========

    def full_keyword_analysis(self, keyword: str) -> Dict:
        """完整关键词分析（难度+意图+搜索量+KGR+SERP）"""
        return {
            "keyword": keyword,
            "difficulty": self.keyword_difficulty(keyword),
            "intent": self.search_intent(keyword),
            "kgr": self.kgr_analysis(keyword),
            "serp_intent": self.serp_intent(keyword),
        }

    def full_seo_audit(self, domain: str) -> Dict:
        """完整SEO审计（全站+页面+排名+AI爬虫）"""
        return {
            "domain": domain,
            "site_audit": self.site_audit(domain),
            "domain_rating": self.domain_rating(domain),
            "search_performance": self.search_performance(domain),
            "ai_crawler_audit": self.ai_crawler_audit(f"https://{domain}"),
        }


# 命令行使用
if __name__ == "__main__":
    import sys

    toolkit = ZensInkToolkit()
    status = toolkit.status()

    print("=== zens-ink 工具包状态 ===")
    print(f"已安装: {status['zens_ink_installed']}")
    print(f"可用模块: {status['available_modules']}/23")
    print(f"可用: {', '.join(status['available'])}")
    if status['unavailable']:
        print(f"不可用: {', '.join(status['unavailable'])}")

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "keyword" and len(sys.argv) > 2:
            keyword = " ".join(sys.argv[2:])
            print(f"\n=== 关键词分析: {keyword} ===")
            result = toolkit.full_keyword_analysis(keyword)
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

        elif command == "audit" and len(sys.argv) > 2:
            domain = sys.argv[2]
            print(f"\n=== SEO审计: {domain} ===")
            result = toolkit.full_seo_audit(domain)
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

        elif command == "reddit":
            print("\n=== Reddit蓝海机会 ===")
            results = toolkit.reddit_blueocean()
            for r in results[:10]:
                print(f"  - {r.get('title', '?')[:80]} (赞: {r.get('ups', 0)}, 评论: {r.get('num_comments', 0)})")
    else:
        print("\n用法:")
        print("  python zens_ink_toolkit.py                  # 查看状态")
        print("  python zens_ink_toolkit.py keyword <词>     # 关键词分析")
        print("  python zens_ink_toolkit.py audit <域名>     # SEO审计")
        print("  python zens_ink_toolkit.py reddit            # Reddit蓝海机会")
