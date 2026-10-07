"""
AIToolCrux CrewAI 多Agent自动化流水线
用CrewAI把6个窗口角色代码化，实现全自动协作：
关键词研究 → 内容生成 → QC检查 → 自动重写 → 发布准备 → 数据监控

CrewAI (52.8K stars) 是基于角色的多Agent框架，60%财富500强使用。

6个Agent角色：
1. 架构师 (Architect) - 技术架构、SEO技术审计、网站修复
2. 创作家 (Creator) - 内容生产、文章撰写、关键词研究
3. 拓荒者 (Pioneer) - 外链建设、增长黑客、社区运营
4. 分析师 (Analyst) - 数据分析、GSC/GA4监控、问题诊断
5. 打磨师 (Polisher) - 内容优化、QC检查、重写提升
6. 体验官 (UX) - 用户体验、转化率优化、A/B测试

用法：
  from scripts.crewai_pipeline import AIToolCruxCrew
  crew = AIToolCruxCrew()
  result = crew.run_content_pipeline(keyword="best ai tools 2026")
  print(result)
"""
import os
import json
from typing import List, Dict, Optional, Any

try:
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import tool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("[WARN] CrewAI未安装。运行: pip install crewai")


class AIToolCruxCrew:
    """AIToolCrux多Agent自动化流水线"""

    def __init__(self, llm=None):
        self.available = CREWAI_AVAILABLE
        self.llm = llm
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        """初始化6个Agent角色"""
        if not self.available:
            return

        # 1. 架构师 - 技术架构师
        self.agents["architect"] = Agent(
            role="Senior Full-Stack Architect & SEO Engineer",
            goal="Ensure the website is technically perfect, fast, and SEO-optimized",
            backstory="""You are a senior full-stack architect with 10 years of experience.
            You specialize in Next.js, TypeScript, Cloudflare, and technical SEO.
            You have built and optimized hundreds of websites.
            You are obsessed with Core Web Vitals, structured data, and crawlability.
            You never ship broken code and always verify before deploying.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        # 2. 创作家 - 内容策略师
        self.agents["creator"] = Agent(
            role="Content Strategist & SEO Writer",
            goal="Create high-quality, SEO-optimized content that ranks and converts",
            backstory="""You are an expert content strategist specializing in AI tool reviews.
            You have written over 500 articles that rank on page 1 of Google.
            You know exactly what users want: real experiences, honest comparisons,
            practical tutorials, and actionable advice.
            You never write generic AI slop - every article has unique insights,
            personal experiences, and verified data.
            You always include screenshots, FAQ sections, and internal links.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        # 3. 拓荒者 - 增长黑客
        self.agents["pioneer"] = Agent(
            role="Growth Hacker & Backlink Builder",
            goal="Build high-quality backlinks and drive targeted traffic through community growth",
            backstory="""You are a growth hacker who has grown 10+ websites from 0 to 100k visitors/month.
            You specialize in community-driven growth: Hacker News, Reddit, Product Hunt,
            AI tool directories, and strategic partnerships.
            You know how to write comments that get upvoted, posts that go viral,
            and outreach emails that get responses.
            You never spam - every interaction is genuine and value-first.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        # 4. 分析师 - 数据分析师
        self.agents["analyst"] = Agent(
            role="Data Analyst & SEO Strategist",
            goal="Turn raw data into actionable insights that drive traffic growth",
            backstory="""You are a data analyst who specializes in SEO and website analytics.
            You can read GSC, GA4, Cloudflare, and server logs and find hidden opportunities.
            You identify ranking drops before they happen, find keyword gaps competitors miss,
            and spot technical issues that hurt crawlability.
            You always back up your recommendations with data, never guesses.
            You present findings in clear, actionable reports with specific next steps.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        # 5. 打磨师 - 内容优化师
        self.agents["polisher"] = Agent(
            role="Content Quality Expert & AI Content Detector",
            goal="Ensure every piece of content is high-quality, original, and conversion-optimized",
            backstory="""You are a content quality expert who can spot AI slop from a mile away.
            You have reviewed over 10,000 articles and know exactly what makes content rank and convert.
            You check for: hallucinations, fake data, generic phrasing, missing screenshots,
            weak FAQ sections, poor internal linking, and keyword stuffing.
            You give specific, actionable feedback that turns mediocre articles into top-10 rankings.
            You are ruthless about quality - if an article doesn't meet the bar, it gets rewritten.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

        # 6. 体验官 - UX优化师
        self.agents["ux"] = Agent(
            role="UX Designer & Conversion Rate Optimizer",
            goal="Maximize user engagement, time on site, and conversion rates",
            backstory="""You are a UX designer and CRO expert who has optimized 50+ websites.
            You know how to design pages that keep users reading, clicking, and converting.
            You specialize in: navigation design, content layout, call-to-action optimization,
            mobile experience, page speed, and A/B testing.
            You always think from the user's perspective: what do they want, what's confusing,
            what's stopping them from taking action?
            You make data-driven recommendations, not subjective opinions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

    def status(self) -> Dict[str, Any]:
        """获取流水线状态"""
        return {
            "crewai_installed": self.available,
            "agents_initialized": len(self.agents),
            "agents": list(self.agents.keys()),
        }

    def run_content_pipeline(self, keyword: str, topic: str = "") -> Dict[str, Any]:
        """
        运行完整内容生产流水线：
        1. 分析师：关键词研究+竞品分析
        2. 创作家：撰写文章
        3. 打磨师：QC检查+重写建议
        4. 创作家：根据建议修改
        5. 体验官：UX优化建议
        6. 架构师：技术SEO检查
        """
        if not self.available:
            return {"error": "CrewAI未安装", "keyword": keyword}

        # 任务1：关键词研究
        research_task = Task(
            description=f"""Research the keyword: {keyword}
            1. Analyze search intent (informational/commercial/transactional)
            2. Find 5-10 related long-tail keywords
            3. Analyze top 3 ranking competitors: what they cover, what they miss
            4. Identify content gaps and unique angles
            5. Recommend article structure (headings, sections, FAQ topics)
            Output a detailed content brief with all findings.""",
            agent=self.agents["analyst"],
            expected_output="Detailed content brief with keyword analysis, competitor gaps, and article structure",
        )

        # 任务2：撰写文章
        write_task = Task(
            description=f"""Write a comprehensive article about: {keyword}
            Use the content brief from the research task.
            Requirements:
            - 2000+ words
            - Include real user experiences and practical advice
            - Add comparison tables if applicable
            - Include FAQ section with 5-8 questions
            - Add internal links to related articles
            - Include placeholders for 2-5 screenshots
            - Write in a conversational, helpful tone (not AI slop)
            - All data must be verifiable, no made-up statistics""",
            agent=self.agents["creator"],
            expected_output="Complete 2000+ word article with FAQ, tables, and internal links",
        )

        # 任务3：QC检查
        qc_task = Task(
            description=f"""Review the article about: {keyword}
            Check for:
            1. Hallucinations and fake data (CRITICAL)
            2. AI content patterns and generic phrasing
            3. Word count (must be 2000+)
            4. FAQ section quality
            5. Screenshot placeholders (need 2-5)
            6. Internal links (need 2-3)
            7. Keyword density (0.5-2%)
            8. Overall quality and usefulness
            Give specific, actionable feedback for each issue found.
            Rate the article 0-100 and say if it passes or needs rewrite.""",
            agent=self.agents["polisher"],
            expected_output="Detailed QC report with score, issues found, and specific rewrite recommendations",
        )

        # 任务4：UX优化
        ux_task = Task(
            description=f"""Review the article about: {keyword} from a UX perspective
            Check for:
            1. Content layout and readability
            2. Call-to-action placement and effectiveness
            3. Navigation and related content suggestions
            4. Mobile-friendliness considerations
            5. Engagement opportunities (quizzes, comparisons, interactive elements)
            6. Conversion optimization (affiliate links, newsletter signup, tool usage)
            Give specific recommendations to improve user engagement and conversions.""",
            agent=self.agents["ux"],
            expected_output="UX optimization report with specific recommendations for engagement and conversion",
        )

        # 任务5：技术SEO检查
        seo_task = Task(
            description=f"""Review the article about: {keyword} for technical SEO
            Check for:
            1. Title tag optimization (50-60 chars, includes keyword)
            2. Meta description (150-160 chars, compelling)
            3. Heading structure (H1-H3 hierarchy)
            4. Image alt text for all screenshots
            5. Internal linking structure
            6. Schema.org markup recommendations (Article, FAQPage, Product)
            7. URL slug optimization
            8. Canonical tag
            Give specific technical SEO recommendations.""",
            agent=self.agents["architect"],
            expected_output="Technical SEO report with specific recommendations for each element",
        )

        # 创建Crew并运行
        crew = Crew(
            agents=[
                self.agents["analyst"],
                self.agents["creator"],
                self.agents["polisher"],
                self.agents["ux"],
                self.agents["architect"],
            ],
            tasks=[research_task, write_task, qc_task, ux_task, seo_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        return {
            "keyword": keyword,
            "topic": topic,
            "result": str(result),
            "tasks_completed": 5,
            "agents_used": 5,
        }

    def run_audit_pipeline(self, url: str = "https://aitoolcrux.com") -> Dict[str, Any]:
        """运行全站审计流水线"""
        if not self.available:
            return {"error": "CrewAI未安装"}

        # 技术审计
        tech_audit = Task(
            description=f"""Perform a full technical SEO audit of {url}
            Check: crawlability, indexability, sitemap, robots.txt,
            Core Web Vitals, mobile-friendliness, HTTPS, structured data,
            broken links, duplicate content, pagination issues.
            Prioritize issues by severity (P0 critical, P1 high, P2 medium).
            Give specific fixes for each issue found.""",
            agent=self.agents["architect"],
            expected_output="Complete technical SEO audit with prioritized issues and fixes",
        )

        # 内容审计
        content_audit = Task(
            description=f"""Audit the content quality of {url}
            Check: article quality, word counts, FAQ coverage,
            screenshot usage, internal linking, content gaps,
            keyword targeting, duplicate content, thin content.
            Identify the worst-performing pages that need rewriting.
            Give specific content improvement recommendations.""",
            agent=self.agents["polisher"],
            expected_output="Content quality audit report with specific pages to improve",
        )

        # 数据分析
        data_audit = Task(
            description=f"""Analyze the SEO performance data for {url}
            Check: keyword rankings, traffic trends, click-through rates,
            indexing status, crawl errors, top-performing pages,
            declining pages, competitor comparison.
            Identify the biggest opportunities for traffic growth.
            Give data-backed recommendations.""",
            agent=self.agents["analyst"],
            expected_output="Data analysis report with traffic growth opportunities",
        )

        crew = Crew(
            agents=[self.agents["architect"], self.agents["polisher"], self.agents["analyst"]],
            tasks=[tech_audit, content_audit, data_audit],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return {"url": url, "result": str(result), "tasks_completed": 3}


# 命令行使用
if __name__ == "__main__":
    import sys

    crew = AIToolCruxCrew()
    status = crew.status()

    print("=== CrewAI 多Agent流水线状态 ===")
    print(f"CrewAI已安装: {status['crewai_installed']}")
    print(f"Agent数量: {status['agents_initialized']}")
    print(f"Agent角色: {', '.join(status['agents'])}")

    if len(sys.argv) > 1:
        if sys.argv[1] == "content" and len(sys.argv) > 2:
            keyword = " ".join(sys.argv[2:])
            print(f"\n=== 运行内容流水线: {keyword} ===")
            result = crew.run_content_pipeline(keyword)
            print(f"完成: {result.get('tasks_completed', 0)}个任务")
        elif sys.argv[1] == "audit":
            print("\n=== 运行全站审计 ===")
            result = crew.run_audit_pipeline()
            print(f"完成: {result.get('tasks_completed', 0)}个任务")
    else:
        print("\n用法:")
        print("  python crewai_pipeline.py                  # 查看状态")
        print("  python crewai_pipeline.py content <关键词>  # 运行内容生产流水线")
        print("  python crewai_pipeline.py audit             # 运行全站审计")
