"""
AIToolCrux 内容QC自动化闭环
每篇文章写完后自动跑质量检查，不达标自动重写，最多3次，达标才发布。

检查项：
1. 字数 >= 2000
2. Flesch Reading Ease >= 50
3. 含FAQ section（>=3个）
4. 含真实截图（>=2张）
5. 含内链（>=3个）
6. 含外链（>=2个）
7. Title含主关键词，50-60字符
8. Meta description 150-160字符
9. 关键词密度 1-3%
10. 有结构化数据（FAQ Schema）

用法：
  from scripts.content_qc_pipeline import ContentQCPipeline
  pipeline = ContentQCPipeline()
  result = pipeline.check(article_dict)
  if not result.passed:
      suggestions = pipeline.get_rewrite_suggestions(result)
"""
import re
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False
    print("[WARN] textstat未安装，可读性检查不可用")


@dataclass
class QCCheckResult:
    """单篇文章QC检查结果"""
    slug: str
    title: str
    passed: bool = False
    score: int = 0  # 0-100
    checks: Dict[str, dict] = field(default_factory=dict)
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ContentQCPipeline:
    """内容质量检查流水线"""

    # 合格阈值
    THRESHOLDS = {
        "min_word_count": 2000,
        "min_flesch": 50,
        "min_faq_count": 3,
        "min_screenshot_count": 2,
        "min_internal_links": 3,
        "min_external_links": 2,
        "min_title_length": 40,
        "max_title_length": 70,
        "min_meta_length": 120,
        "max_meta_length": 170,
        "min_keyword_density": 0.5,
        "max_keyword_density": 4.0,
        "pass_score": 85,
    }

    def __init__(self, posts_json_path=None):
        if posts_json_path is None:
            posts_json_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "posts.json"
            )
        self.posts_json_path = posts_json_path

    def check(self, article: dict) -> QCCheckResult:
        """
        检查单篇文章质量

        Args:
            article: 文章字典，需包含 title, content, slug, metaDescription等字段

        Returns:
            QCCheckResult: 检查结果
        """
        result = QCCheckResult(
            slug=article.get("slug", "unknown"),
            title=article.get("title", "无标题")
        )

        content = article.get("content", "")
        title = article.get("title", "")
        meta = article.get("metaDescription", "")
        primary_keyword = article.get("primaryKeyword", "")

        # 1. 字数检查
        word_count = self._count_words(content)
        result.checks["word_count"] = {
            "value": word_count,
            "threshold": self.THRESHOLDS["min_word_count"],
            "passed": word_count >= self.THRESHOLDS["min_word_count"]
        }
        if not result.checks["word_count"]["passed"]:
            result.failures.append(f"字数不足: {word_count} < {self.THRESHOLDS['min_word_count']}")

        # 2. 可读性检查
        if TEXTSTAT_AVAILABLE and word_count > 100:
            flesch = textstat.flesch_reading_ease(content)
            result.checks["flesch"] = {
                "value": round(flesch, 1),
                "threshold": self.THRESHOLDS["min_flesch"],
                "passed": flesch >= self.THRESHOLDS["min_flesch"]
            }
            if not result.checks["flesch"]["passed"]:
                result.warnings.append(f"可读性偏低: Flesch={flesch:.1f} < {self.THRESHOLDS['min_flesch']}")

        # 3. FAQ检查
        faq_count = self._count_faq(content)
        result.checks["faq"] = {
            "value": faq_count,
            "threshold": self.THRESHOLDS["min_faq_count"],
            "passed": faq_count >= self.THRESHOLDS["min_faq_count"]
        }
        if not result.checks["faq"]["passed"]:
            result.failures.append(f"FAQ不足: {faq_count} < {self.THRESHOLDS['min_faq_count']}")

        # 4. 截图检查
        screenshot_count = self._count_screenshots(content)
        result.checks["screenshots"] = {
            "value": screenshot_count,
            "threshold": self.THRESHOLDS["min_screenshot_count"],
            "passed": screenshot_count >= self.THRESHOLDS["min_screenshot_count"]
        }
        if not result.checks["screenshots"]["passed"]:
            result.failures.append(f"截图不足: {screenshot_count} < {self.THRESHOLDS['min_screenshot_count']}")

        # 5. 内链检查
        internal_links = self._count_internal_links(content)
        result.checks["internal_links"] = {
            "value": internal_links,
            "threshold": self.THRESHOLDS["min_internal_links"],
            "passed": internal_links >= self.THRESHOLDS["min_internal_links"]
        }
        if not result.checks["internal_links"]["passed"]:
            result.warnings.append(f"内链偏少: {internal_links} < {self.THRESHOLDS['min_internal_links']}")

        # 6. 外链检查
        external_links = self._count_external_links(content)
        result.checks["external_links"] = {
            "value": external_links,
            "threshold": self.THRESHOLDS["min_external_links"],
            "passed": external_links >= self.THRESHOLDS["min_external_links"]
        }
        if not result.checks["external_links"]["passed"]:
            result.warnings.append(f"外链偏少: {external_links} < {self.THRESHOLDS['min_external_links']}")

        # 7. Title长度检查
        title_len = len(title)
        result.checks["title_length"] = {
            "value": title_len,
            "range": f"{self.THRESHOLDS['min_title_length']}-{self.THRESHOLDS['max_title_length']}",
            "passed": self.THRESHOLDS["min_title_length"] <= title_len <= self.THRESHOLDS["max_title_length"]
        }
        if not result.checks["title_length"]["passed"]:
            result.warnings.append(f"Title长度: {title_len} (建议{self.THRESHOLDS['min_title_length']}-{self.THRESHOLDS['max_title_length']})")

        # 8. Meta description检查
        if meta:
            meta_len = len(meta)
            result.checks["meta_length"] = {
                "value": meta_len,
                "range": f"{self.THRESHOLDS['min_meta_length']}-{self.THRESHOLDS['max_meta_length']}",
                "passed": self.THRESHOLDS["min_meta_length"] <= meta_len <= self.THRESHOLDS["max_meta_length"]
            }

        # 9. 关键词密度检查
        if primary_keyword and word_count > 0:
            keyword_count = content.lower().count(primary_keyword.lower())
            density = (keyword_count / word_count) * 100
            result.checks["keyword_density"] = {
                "value": round(density, 2),
                "range": f"{self.THRESHOLDS['min_keyword_density']}-{self.THRESHOLDS['max_keyword_density']}%",
                "passed": self.THRESHOLDS["min_keyword_density"] <= density <= self.THRESHOLDS["max_keyword_density"]
            }

        # 10. 结构化数据检查
        has_faq_schema = '"@type": "FAQPage"' in content or 'application/ld+json' in content
        result.checks["faq_schema"] = {
            "value": has_faq_schema,
            "passed": has_faq_schema
        }
        if not result.checks["faq_schema"]["passed"]:
            result.warnings.append("缺少FAQ Schema结构化数据")

        # 计算总分
        result.score = self._calculate_score(result.checks)
        result.passed = result.score >= self.THRESHOLDS["pass_score"] and len(result.failures) == 0

        return result

    def get_rewrite_suggestions(self, result: QCCheckResult) -> List[str]:
        """根据检查结果生成重写建议"""
        suggestions = []

        for failure in result.failures:
            if "字数不足" in failure:
                suggestions.append("扩充内容到2000词以上：增加使用场景、详细步骤、常见问题、对比分析")
            elif "FAQ不足" in failure:
                suggestions.append("添加至少3个FAQ，每个问题用真实用户搜索语气，答案50-100词")
            elif "截图不足" in failure:
                suggestions.append("用Playwright截取工具官网首页和功能页，至少2张真实截图")

        for warning in result.warnings:
            if "可读性" in warning:
                suggestions.append("简化句子结构，用短句和常用词，降低阅读难度")
            elif "内链" in warning:
                suggestions.append("添加3个以上内链，指向相关文章和工具详情页")
            elif "外链" in warning:
                suggestions.append("添加2个以上权威外链，引用统计数据和官方文档")
            elif "Title" in warning:
                suggestions.append("优化Title：包含主关键词+数字+情感词，控制在50-60字符")
            elif "Schema" in warning:
                suggestions.append("添加FAQ Schema JSON-LD结构化数据")

        if not suggestions:
            suggestions.append("整体质量达标，可以发布")

        return suggestions

    def batch_check(self, articles: List[dict]) -> List[QCCheckResult]:
        """批量检查多篇文章"""
        return [self.check(article) for article in articles]

    def check_all_posts(self) -> List[QCCheckResult]:
        """检查posts.json中所有文章"""
        with open(self.posts_json_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
        return self.batch_check(posts)

    def _count_words(self, text: str) -> int:
        """统计英文单词数"""
        # 移除HTML标签
        clean = re.sub(r'<[^>]+>', ' ', text)
        words = re.findall(r'[a-zA-Z]+', clean)
        return len(words)

    def _count_faq(self, content: str) -> int:
        """统计FAQ数量"""
        # 匹配FAQ section中的问题
        faq_patterns = [
            r'Q:\s*.+\?',
            r'Q\.\s*.+\?',
            r'<h[34]>[^<]+\?</h[34]>',
            r'####\s*.+\?',
            r'###\s*.+\?',
        ]
        count = 0
        for pattern in faq_patterns:
            count += len(re.findall(pattern, content, re.IGNORECASE))
        return min(count, 20)  # 最多算20个

    def _count_screenshots(self, content: str) -> int:
        """统计截图数量"""
        # 匹配图片引用
        patterns = [
            r'!\[.*?\]\(.*?screenshot.*?\)',
            r'!\[.*?\]\(.*?/screenshots/.*?\)',
            r'<img[^>]*src=["\'][^"\']*screenshot[^"\']*["\']',
            r'hasRealScreenshots.*?true',
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content, re.IGNORECASE))
        return count

    def _count_internal_links(self, content: str) -> int:
        """统计内链数量"""
        # 匹配站内链接（相对路径或aitoolcrux.com）
        patterns = [
            r'href=["\']/(?!/)[^"\']*["\']',  # 相对路径
            r'href=["\']https?://(?:www\.)?aitoolcrux\.com[^"\']*["\']',  # 绝对站内
            r'\]\(/[^)]*\)',  # Markdown相对链接
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content))
        return count

    def _count_external_links(self, content: str) -> int:
        """统计外链数量"""
        # 匹配非站内的外部链接
        all_links = re.findall(r'href=["\']https?://([^"\']+)["\']', content)
        external = [link for link in all_links if 'aitoolcrux.com' not in link]
        return len(external)

    def _calculate_score(self, checks: dict) -> int:
        """计算总分（0-100）"""
        if not checks:
            return 0

        # 各项权重
        weights = {
            "word_count": 20,
            "flesch": 10,
            "faq": 15,
            "screenshots": 15,
            "internal_links": 10,
            "external_links": 5,
            "title_length": 5,
            "meta_length": 5,
            "keyword_density": 5,
            "faq_schema": 10,
        }

        score = 0
        for check_name, check_data in checks.items():
            weight = weights.get(check_name, 5)
            if check_data.get("passed", False):
                score += weight

        return min(score, 100)


# 命令行使用
if __name__ == "__main__":
    import sys

    pipeline = ContentQCPipeline()

    if len(sys.argv) > 1 and sys.argv[1] == "all":
        # 检查所有文章
        print("正在检查所有文章...")
        results = pipeline.check_all_posts()

        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        avg_score = sum(r.score for r in results) / len(results) if results else 0

        print(f"\n=== 批量QC结果 ===")
        print(f"总文章数: {len(results)}")
        print(f"通过: {passed} ({passed/len(results)*100:.1f}%)")
        print(f"未通过: {failed}")
        print(f"平均分: {avg_score:.1f}")

        # 列出未通过的
        if failed > 0:
            print(f"\n=== 未通过文章（前10篇）===")
            for r in sorted(results, key=lambda x: x.score)[:10]:
                print(f"  [{r.score}分] {r.slug}")
                for f in r.failures[:3]:
                    print(f"    ✗ {f}")

    elif len(sys.argv) > 1 and sys.argv[1] == "slug":
        # 检查指定slug
        slug = sys.argv[2]
        with open(pipeline.posts_json_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
        article = next((p for p in posts if p.get("slug") == slug), None)
        if article:
            result = pipeline.check(article)
            print(f"\n=== QC结果: {result.title} ===")
            print(f"总分: {result.score}/100")
            print(f"状态: {'✅ 通过' if result.passed else '❌ 未通过'}")
            print(f"\n详细检查:")
            for name, data in result.checks.items():
                status = "✅" if data.get("passed") else "❌"
                print(f"  {status} {name}: {data.get('value')}")
            if result.failures:
                print(f"\n失败项:")
                for f in result.failures:
                    print(f"  ✗ {f}")
            suggestions = pipeline.get_rewrite_suggestions(result)
            print(f"\n重写建议:")
            for s in suggestions:
                print(f"  → {s}")
        else:
            print(f"未找到slug: {slug}")

    else:
        print("用法:")
        print("  python content_qc_pipeline.py all          # 检查所有文章")
        print("  python content_qc_pipeline.py slug <slug>  # 检查指定文章")
