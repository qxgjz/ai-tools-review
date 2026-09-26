#!/usr/bin/env python3
"""
Real GEO/AEO Audit - AI Search Visibility Check
Based on: OrtaMarco/seo-geo-mcp-server methodology
Actually checks if AI crawlers can access and cite the website
"""

import requests
import re
import json
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "https://www.aitoolcrux.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# AI crawlers to check
AI_CRAWLERS = {
    "GPTBot": "OpenAI's crawler for ChatGPT",
    "ClaudeBot": "Anthropic's crawler for Claude",
    "Claude-Web": "Anthropic's web crawler",
    "PerplexityBot": "Perplexity's crawler",
    "Google-Extended": "Google's AI training crawler",
    "Applebot": "Apple's crawler for Siri/Apple Intelligence",
    "Amazonbot": "Amazon's crawler for Alexa/Rufus",
    "Bytespider": "ByteDance's crawler",
    "meta-externalagent": "Meta's external agent crawler",
    "OAI-SearchBot": "OpenAI Search crawler",
    "CCBot": "Common Crawl bot",
}

# Pages to check for AEO optimization
PAGES_TO_CHECK = [
    "/",
    "/tools/chatgpt",
    "/tools/midjourney",
    "/tools/cursor",
    "/blog/chatgpt-vs-claude-2026-comparison",
    "/alternatives/chatgpt-alternatives",
    "/methodology",
]

results = {
    "audit_time": datetime.now().isoformat(),
    "base_url": BASE_URL,
    "ai_crawler_accessibility": {},
    "llms_txt_status": {},
    "aeo_optimization": {},
    "geo_readiness_score": 0,
    "findings": [],
    "recommendations": [],
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        return response, response.text
    except Exception as e:
        return None, str(e)

def check_robots_txt_ai_crawlers():
    """Check robots.txt for AI crawler configurations"""
    print("\n" + "=" * 70)
    print("CHECKING AI CRAWLER ACCESSIBILITY (robots.txt)")
    print("=" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/robots.txt", headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"❌ robots.txt returned {response.status_code}")
            return 0
        
        robots_content = response.text
        print(f"✅ robots.txt fetched ({len(robots_content)} bytes)")
        print()
        
        # Parse robots.txt
        lines = robots_content.split('\n')
        current_agent = None
        agent_rules = {}
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('user-agent:'):
                current_agent = line.split(':', 1)[1].strip()
                if current_agent not in agent_rules:
                    agent_rules[current_agent] = {'allow': [], 'disallow': []}
            elif line.lower().startswith('disallow:') and current_agent:
                path = line.split(':', 1)[1].strip()
                agent_rules[current_agent]['disallow'].append(path)
            elif line.lower().startswith('allow:') and current_agent:
                path = line.split(':', 1)[1].strip()
                agent_rules[current_agent]['allow'].append(path)
        
        # Check each AI crawler
        accessible = 0
        blocked = 0
        not_configured = 0
        
        for crawler, description in AI_CRAWLERS.items():
            if crawler in agent_rules:
                rules = agent_rules[crawler]
                disallow_all = any(d == '/' for d in rules['disallow'])
                if disallow_all:
                    status = "❌ BLOCKED"
                    blocked += 1
                    results["findings"].append(f"{crawler} is BLOCKED in robots.txt (Disallow: /)")
                else:
                    status = "✅ ACCESSIBLE"
                    accessible += 1
                    results["findings"].append(f"{crawler} is configured and accessible")
                print(f"  {status}: {crawler} ({description})")
                if rules['disallow']:
                    print(f"           Disallow: {', '.join(rules['disallow'][:3])}")
            else:
                # Check if wildcard (*) applies
                if '*' in agent_rules:
                    wildcard_rules = agent_rules['*']
                    disallow_all = any(d == '/' for d in wildcard_rules['disallow'])
                    if disallow_all:
                        status = "❌ BLOCKED (wildcard)"
                        blocked += 1
                    else:
                        status = "✅ ACCESSIBLE (wildcard)"
                        accessible += 1
                else:
                    status = "⚠️ NOT EXPLICITLY CONFIGURED"
                    not_configured += 1
                print(f"  {status}: {crawler} ({description})")
        
        print(f"\nSummary: {accessible} accessible, {blocked} blocked, {not_configured} not configured")
        
        score = (accessible / len(AI_CRAWLERS)) * 10
        results["ai_crawler_accessibility"] = {
            "accessible": accessible,
            "blocked": blocked,
            "not_configured": not_configured,
            "total": len(AI_CRAWLERS),
            "score": score,
        }
        
        return score
        
    except Exception as e:
        print(f"❌ Error checking robots.txt: {str(e)}")
        return 0

def check_llms_txt():
    """Check llms.txt and llms-full.txt"""
    print("\n" + "=" * 70)
    print("CHECKING llms.txt (AI Crawler Content Index)")
    print("=" * 70)
    
    # Check llms.txt
    try:
        response = requests.get(f"{BASE_URL}/llms.txt", headers=HEADERS, timeout=15)
        if response.status_code == 200 and len(response.text) > 100:
            content = response.text
            print(f"✅ llms.txt present ({len(content)} bytes)")
            
            # Check content quality
            has_title = "#" in content or "title" in content.lower()
            has_links = "http" in content or "/" in content
            has_structure = "##" in content or "###" in content
            
            print(f"   Has title/heading: {'✅' if has_title else '❌'}")
            print(f"   Has links: {'✅' if has_links else '❌'}")
            print(f"   Has structure (##): {'✅' if has_structure else '❌'}")
            
            # Count links
            link_count = len(re.findall(r'https?://', content))
            print(f"   External links found: {link_count}")
            
            llms_score = 10 if all([has_title, has_links, has_structure]) else 7
            results["llms_txt_status"]["llms.txt"] = {
                "present": True,
                "size": len(content),
                "score": llms_score,
            }
        else:
            print(f"❌ llms.txt missing or too short (status: {response.status_code})")
            llms_score = 0
            results["llms_txt_status"]["llms.txt"] = {"present": False, "score": 0}
            results["findings"].append("llms.txt is missing - AI crawlers won't have structured content index")
    except Exception as e:
        print(f"❌ Error checking llms.txt: {str(e)}")
        llms_score = 0
    
    # Check llms-full.txt
    try:
        response = requests.get(f"{BASE_URL}/llms-full.txt", headers=HEADERS, timeout=30)
        if response.status_code == 200 and len(response.text) > 1000:
            content = response.text
            print(f"\n✅ llms-full.txt present ({len(content)} bytes, {len(content.splitlines())} lines)")
            
            # Check content depth
            has_tool_pages = "/tools/" in content
            has_blog_posts = "/blog/" in content
            has_categories = "/category/" in content
            has_alternatives = "/alternatives/" in content
            
            print(f"   Contains tool pages: {'✅' if has_tool_pages else '❌'}")
            print(f"   Contains blog posts: {'✅' if has_blog_posts else '❌'}")
            print(f"   Contains categories: {'✅' if has_categories else '❌'}")
            print(f"   Contains alternatives: {'✅' if has_alternatives else '❌'}")
            
            full_score = 10 if all([has_tool_pages, has_blog_posts, has_categories]) else 7
            results["llms_txt_status"]["llms-full.txt"] = {
                "present": True,
                "size": len(content),
                "lines": len(content.splitlines()),
                "score": full_score,
            }
        else:
            print(f"\n⚠️ llms-full.txt missing or too small (status: {response.status_code})")
            full_score = 3
            results["llms_txt_status"]["llms-full.txt"] = {"present": False, "score": 3}
            results["findings"].append("llms-full.txt is missing - AI crawlers won't have full content for citation")
    except Exception as e:
        print(f"❌ Error checking llms-full.txt: {str(e)}")
        full_score = 0
    
    return (llms_score + full_score) / 2

def check_aeo_optimization():
    """Check AEO (Answer Engine Optimization) on key pages"""
    print("\n" + "=" * 70)
    print("CHECKING AEO OPTIMIZATION (Answer Engine Readiness)")
    print("=" * 70)
    
    aeo_scores = []
    
    for page_path in PAGES_TO_CHECK:
        url = urljoin(BASE_URL, page_path)
        print(f"\n--- {page_path} ---")
        
        response, content = fetch_page(url)
        if response is None:
            print(f"  ❌ Failed to fetch")
            continue
        
        page_score = 0
        checks_passed = 0
        total_checks = 8
        
        # Check 1: Quick Answer section (answer-first structure)
        has_quick_answer = "Quick Answer" in content or "quick answer" in content.lower()
        if has_quick_answer:
            print(f"  ✅ Quick Answer section present")
            checks_passed += 1
        else:
            print(f"  ❌ No Quick Answer section (AI engines prefer answer-first content)")
        
        # Check 2: Key Takeaways / TL;DR
        has_takeaways = "Key Takeaways" in content or "TL;DR" in content or "key takeaways" in content.lower()
        if has_takeaways:
            print(f"  ✅ Key Takeaways / TL;DR present")
            checks_passed += 1
        else:
            print(f"  ❌ No Key Takeaways (AI engines extract summaries)")
        
        # Check 3: FAQ section
        has_faq = "FAQ" in content or "Frequently Asked" in content or "faq" in content.lower()
        if has_faq:
            print(f"  ✅ FAQ section present")
            checks_passed += 1
        else:
            print(f"  ❌ No FAQ section (AI engines love Q&A format)")
        
        # Check 4: Structured data (JSON-LD)
        has_json_ld = "application/ld+json" in content
        if has_json_ld:
            print(f"  ✅ JSON-LD structured data present")
            checks_passed += 1
        else:
            print(f"  ❌ No JSON-LD structured data")
        
        # Check 5: Citation/source information
        has_citation = "Source:" in content or "Last updated" in content or "Updated:" in content or "Methodology" in content
        if has_citation:
            print(f"  ✅ Citation/source information present")
            checks_passed += 1
        else:
            print(f"  ❌ No citation/source information (AI engines prefer verifiable content)")
        
        # Check 6: Author/byline
        has_author = "author" in content.lower() or "Written by" in content or "Editorial Team" in content
        if has_author:
            print(f"  ✅ Author/byline present")
            checks_passed += 1
        else:
            print(f"  ❌ No clear author attribution")
        
        # Check 7: Tables/comparison data (AI engines love structured data)
        has_tables = "<table" in content or "comparison table" in content.lower() or "Comparison" in content
        if has_tables:
            print(f"  ✅ Tables/comparison data present")
            checks_passed += 1
        else:
            print(f"  ⚠️ No tables (structured data helps AI citation)")
        
        # Check 8: Clear headings structure
        has_h2 = "<h2" in content
        has_h3 = "<h3" in content
        if has_h2 and has_h3:
            print(f"  ✅ Clear heading structure (H2+H3)")
            checks_passed += 1
        else:
            print(f"  ⚠️ Heading structure could be improved")
        
        page_score = (checks_passed / total_checks) * 10
        aeo_scores.append(page_score)
        print(f"  AEO Score: {page_score:.1f}/10 ({checks_passed}/{total_checks} checks)")
        
        results["aeo_optimization"][page_path] = {
            "score": page_score,
            "checks_passed": checks_passed,
            "total_checks": total_checks,
        }
    
    avg_aeo = sum(aeo_scores) / len(aeo_scores) if aeo_scores else 0
    print(f"\nAverage AEO Score: {avg_aeo:.1f}/10")
    return avg_aeo

def check_geo_content_structure():
    """Check GEO (Generative Engine Optimization) content patterns"""
    print("\n" + "=" * 70)
    print("CHECKING GEO CONTENT STRUCTURE (Generative Engine Readiness)")
    print("=" * 70)
    
    # GEO best practices from research:
    # 1. Statistical data and numbers
    # 2. Expert quotes and testimonials
    # 3. Original research and case studies
    # 4. Clear definitions and explanations
    # 5. Step-by-step guides
    # 6. Comparison and contrast
    # 7. Real-world examples
    
    geo_checks = {
        "statistical_data": 0,
        "expert_quotes": 0,
        "original_research": 0,
        "clear_definitions": 0,
        "step_by_step": 0,
        "comparisons": 0,
        "real_examples": 0,
    }
    
    pages_checked = 0
    
    for page_path in ["/tools/chatgpt", "/blog/chatgpt-vs-claude-2026-comparison", "/alternatives/chatgpt-alternatives"]:
        url = urljoin(BASE_URL, page_path)
        response, content = fetch_page(url)
        if response is None:
            continue
        
        pages_checked += 1
        text_content = re.sub(r'<[^>]+>', ' ', content)
        text_content = re.sub(r'\s+', ' ', text_content)
        
        # Check for statistical data (numbers with context)
        stats_patterns = [r'\d+%', r'\d+\+', r'\d+ million', r'\d+ billion', r'rated \d+', r'score: \d+']
        if any(re.search(p, text_content, re.IGNORECASE) for p in stats_patterns):
            geo_checks["statistical_data"] += 1
        
        # Check for expert quotes
        if '"' in text_content and ('said' in text_content.lower() or 'according to' in text_content.lower() or 'states' in text_content.lower()):
            geo_checks["expert_quotes"] += 1
        
        # Check for original research/case studies
        if 'case study' in text_content.lower() or 'research' in text_content.lower() or 'study' in text_content.lower() or 'our test' in text_content.lower():
            geo_checks["original_research"] += 1
        
        # Check for clear definitions
        if 'what is' in text_content.lower() or 'defined as' in text_content.lower() or 'refers to' in text_content.lower():
            geo_checks["clear_definitions"] += 1
        
        # Check for step-by-step guides
        if 'step 1' in text_content.lower() or 'first,' in text_content.lower() or 'how to' in text_content.lower():
            geo_checks["step_by_step"] += 1
        
        # Check for comparisons
        if 'vs' in text_content.lower() or 'compared to' in text_content.lower() or 'versus' in text_content.lower() or 'alternative' in text_content.lower():
            geo_checks["comparisons"] += 1
        
        # Check for real examples
        if 'for example' in text_content.lower() or 'such as' in text_content.lower() or 'e.g.' in text_content.lower():
            geo_checks["real_examples"] += 1
    
    print(f"\nChecked {pages_checked} pages for GEO content patterns:")
    print()
    
    geo_score = 0
    for check, count in geo_checks.items():
        percentage = (count / pages_checked) * 100 if pages_checked > 0 else 0
        status = "✅" if percentage >= 66 else "⚠️" if percentage >= 33 else "❌"
        print(f"  {status} {check.replace('_', ' ').title()}: {count}/{pages_checked} pages ({percentage:.0f}%)")
        geo_score += percentage / 7
    
    print(f"\nGEO Content Score: {geo_score:.1f}/100")
    return geo_score / 10

# Main execution
print("=" * 70)
print("REAL GEO/AEO AUDIT - AI Search Visibility Check")
print("Based on: OrtaMarco/seo-geo-mcp-server methodology")
print("=" * 70)
print(f"Target: {BASE_URL}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Run all checks
crawler_score = check_robots_txt_ai_crawlers()
llms_score = check_llms_txt()
aeo_score = check_aeo_optimization()
geo_score = check_geo_content_structure()

# Calculate overall GEO/AEO readiness
overall_score = (crawler_score + llms_score + aeo_score + geo_score) / 4
results["geo_readiness_score"] = overall_score

# Summary
print("\n" + "=" * 70)
print("GEO/AEO AUDIT SUMMARY")
print("=" * 70)
print(f"\nAI Crawler Accessibility: {crawler_score:.1f}/10")
print(f"llms.txt Configuration: {llms_score:.1f}/10")
print(f"AEO Content Optimization: {aeo_score:.1f}/10")
print(f"GEO Content Structure: {geo_score:.1f}/10")
print(f"\nOverall GEO/AEO Readiness: {overall_score:.1f}/10")

if overall_score >= 8:
    grade = "A (Excellent - AI search ready)"
elif overall_score >= 6:
    grade = "B (Good - minor improvements needed)"
elif overall_score >= 4:
    grade = "C (Average - significant optimization needed)"
else:
    grade = "D (Poor - major AI visibility issues)"

print(f"Grade: {grade}")

# Key findings
print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)
for i, finding in enumerate(results["findings"][:10], 1):
    print(f"{i}. {finding}")

# Recommendations
print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)
recommendations = [
    "Ensure all key pages have Quick Answer sections (answer-first structure for AI citation)",
    "Add Key Takeaways/TL;DR to all article and tool pages",
    "Include statistical data and original research in content (AI engines cite data-heavy content)",
    "Add expert quotes and testimonials where appropriate",
    "Ensure all pages have clear author attribution and last updated dates",
    "Add comparison tables to tool pages (structured data helps AI extraction)",
    "Verify llms-full.txt contains all important pages for AI crawler ingestion",
]
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# Save results
with open("real_geo_aeo_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Full results saved to: real_geo_aeo_audit_results.json")
print("=" * 70)
