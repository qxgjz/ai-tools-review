#!/usr/bin/env python3
"""
生成网站优化诊断摘要报告
汇总所有模块的诊断结果，生成Markdown格式的摘要报告
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_reports(reports_dir: str) -> list:
    """加载所有诊断报告"""
    reports = []
    
    if not os.path.exists(reports_dir):
        print(f"报告目录不存在: {reports_dir}", file=sys.stderr)
        return reports
    
    for filename in os.listdir(reports_dir):
        if filename.endswith('-report.json'):
            filepath = os.path.join(reports_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                    reports.append(report)
                    print(f"已加载: {filename}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"加载失败 {filename}: {e}", file=sys.stderr)
    
    return reports


def generate_summary(reports: list, output_file: str):
    """生成摘要报告"""
    
    # 按模块排序
    module_order = [
        'orchestrator', 'crawlability', 'renderability', 'indexability',
        'core_web_vitals', 'tool_page_content', 'article_page_content',
        'category_page_content', 'eeat', 'structured_data',
        'internal_linking', 'link_building', 'conversion_rate'
    ]
    
    module_names = {
        'orchestrator': '总控诊断',
        'crawlability': '可抓取性',
        'renderability': '可渲染性',
        'indexability': '可索引性',
        'core_web_vitals': 'Core Web Vitals',
        'tool_page_content': '工具页内容',
        'article_page_content': '文章页内容',
        'category_page_content': '分类页内容',
        'eeat': 'E-E-A-T',
        'structured_data': '结构化数据',
        'internal_linking': '内链优化',
        'link_building': '外链建设',
        'conversion_rate': '转化率优化'
    }
    
    # 排序报告
    reports.sort(key=lambda r: module_order.index(r.get('module', 'unknown')) 
                  if r.get('module') in module_order else 999)
    
    # 统计数据
    total_issues = 0
    p0_issues = []
    p1_issues = []
    p2_issues = []
    health_scores = {}
    
    for report in reports:
        module = report.get('module', 'unknown')
        summary = report.get('summary', {})
        health_scores[module] = summary.get('health_score', 0)
        
        issues = report.get('issues', [])
        total_issues += len(issues)
        
        for issue in issues:
            priority = issue.get('priority', 'P2')
            if priority == 'P0':
                p0_issues.append((module, issue))
            elif priority == 'P1':
                p1_issues.append((module, issue))
            else:
                p2_issues.append((module, issue))
    
    # 计算平均健康度
    avg_health = sum(health_scores.values()) / len(health_scores) if health_scores else 0
    
    # 生成Markdown
    md = []
    md.append(f"# 网站优化诊断摘要报告")
    md.append(f"")
    md.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"**网站URL**: https://www.aitoolcrux.com")
    md.append(f"**诊断模块数**: {len(reports)}")
    md.append(f"**平均健康度**: {avg_health:.1f}/100")
    md.append(f"**问题总数**: {total_issues}")
    md.append(f"**P0问题**: {len(p0_issues)}个")
    md.append(f"**P1问题**: {len(p1_issues)}个")
    md.append(f"**P2问题**: {len(p2_issues)}个")
    md.append(f"")
    
    # 总体结论
    md.append(f"## 📊 总体结论")
    md.append(f"")
    
    # 找出最严重的问题
    if p0_issues:
        md.append(f"### 🔴 最致命的P0问题（必须7天内解决）")
        md.append(f"")
        for module, issue in p0_issues[:10]:  # 最多显示10个
            module_name = module_names.get(module, module)
            md.append(f"- **[{module_name}]** {issue.get('title', '未知问题')}")
            md.append(f"  - 严重程度: {issue.get('severity', 'unknown')}")
            md.append(f"  - 影响: {issue.get('fix', {}).get('expected_impact', '未知')}")
        md.append(f"")
    
    # 各模块健康度
    md.append(f"## 📈 各模块健康度评分")
    md.append(f"")
    md.append(f"| 模块 | 健康度 | 问题数 | P0 | P1 | P2 |")
    md.append(f"|------|--------|--------|-----|-----|-----|")
    
    for report in reports:
        module = report.get('module', 'unknown')
        module_name = module_names.get(module, module)
        health = report.get('summary', {}).get('health_score', 0)
        issues = report.get('issues', [])
        p0_count = len([i for i in issues if i.get('priority') == 'P0'])
        p1_count = len([i for i in issues if i.get('priority') == 'P1'])
        p2_count = len([i for i in issues if i.get('priority') == 'P2'])
        
        # 健康度颜色
        if health >= 80:
            health_display = f"🟢 {health}/100"
        elif health >= 60:
            health_display = f"🟡 {health}/100"
        else:
            health_display = f"🔴 {health}/100"
        
        md.append(f"| {module_name} | {health_display} | {len(issues)} | {p0_count} | {p1_count} | {p2_count} |")
    
    md.append(f"")
    
    # 14天行动计划
    md.append(f"## 🚀 14天行动计划")
    md.append(f"")
    md.append(f"### 第1-7天：解决P0问题")
    md.append(f"")
    if p0_issues:
        for i, (module, issue) in enumerate(p0_issues[:7], 1):
            module_name = module_names.get(module, module)
            md.append(f"{i}. **[{module_name}]** {issue.get('title', '未知问题')}")
            md.append(f"   - 修复方案: {issue.get('fix', {}).get('description', '待补充')}")
            md.append(f"   - 预估工作量: {issue.get('fix', {}).get('estimated_effort', '未知')}")
    else:
        md.append(f"✅ 没有P0问题，继续保持！")
    md.append(f"")
    
    md.append(f"### 第8-14天：解决P1问题")
    md.append(f"")
    if p1_issues:
        for i, (module, issue) in enumerate(p1_issues[:7], 1):
            module_name = module_names.get(module, module)
            md.append(f"{i}. **[{module_name}]** {issue.get('title', '未知问题')}")
    else:
        md.append(f"✅ 没有P1问题，继续保持！")
    md.append(f"")
    
    # 预期效果
    md.append(f"## 🎯 预期效果")
    md.append(f"")
    md.append(f"### 短期（14天）")
    md.append(f"- 收录率提升: 解决技术障碍后，Google收录率预计显著提升")
    md.append(f"- 曝光量: 从0开始增长，首批关键词获得曝光")
    md.append(f"- 点击量: 获得首批自然搜索点击")
    md.append(f"")
    md.append(f"### 中期（90天）")
    md.append(f"- 自然流量: 预计达到500+会话/天")
    md.append(f"- 关键词排名: 50+长尾关键词进入前10页")
    md.append(f"- 转化率: 联盟链接点击率提升至2-5%")
    md.append(f"- 域名权重: 外链建设带动域名权重提升")
    md.append(f"")
    
    # 监测与止损
    md.append(f"## ⚠️ 监测与止损")
    md.append(f"")
    md.append(f"### 告警阈值")
    md.append(f"- 收录率下降>30%: 立即检查技术问题")
    md.append(f"- 自然流量下降>50%: 检查是否被降权")
    md.append(f"- CWV分数下降: 检查性能退化")
    md.append(f"- GSC出现手动操作: 立即启动应急恢复")
    md.append(f"")
    md.append(f"### 降权应急恢复步骤")
    md.append(f"1. 停止所有可疑操作")
    md.append(f"2. 全面审计网站，识别违规操作")
    md.append(f"3. 清理违规内容和外链")
    md.append(f"4. 提交复议请求")
    md.append(f"5. 持续优化，等待恢复（通常6-12个月）")
    md.append(f"")
    
    # 待核实清单
    md.append(f"## ❓ 待核实清单")
    md.append(f"")
    md.append(f"以下数据缺失，需要补充后才能做出更准确的诊断：")
    md.append(f"")
    md.append(f"1. **GSC覆盖报告**: 已编入索引/已发现未编入索引/已排除页面数")
    md.append(f"2. **GSC抓取统计**: 抓取请求数、下载字节数、平均下载时间")
    md.append(f"3. **GA4数据**: 自然会话数、关键事件数、用户留存率")
    md.append(f"4. **服务器日志**: Googlebot抓取频率、抓取深度、HTTP状态码分布（7天）")
    md.append(f"5. **外链数据**: 外链数、锚文本分布、域名权重（Ahrefs/Semrush/Moz）")
    md.append(f"6. **Core Web Vitals实测数据**: LCP/CLS/INP（Mobile/Desktop）")
    md.append(f"7. **内容AI生成比**: 随机10篇工具页和5篇文章的AI生成比/人工核验度")
    md.append(f"")
    
    # 详细报告链接
    md.append(f"## 📁 详细报告")
    md.append(f"")
    md.append(f"各模块的详细JSON报告已保存到 `reports/` 目录：")
    md.append(f"")
    for report in reports:
        module = report.get('module', 'unknown')
        module_name = module_names.get(module, module)
        md.append(f"- [{module_name}](reports/{module}-report.json)")
    md.append(f"")
    
    md.append(f"---")
    md.append(f"*本报告由GitHub Actions每周自动诊断工作流生成*")
    md.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # 保存报告
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    print(f"摘要报告已生成: {output_file}")
    print(f"诊断模块数: {len(reports)}")
    print(f"平均健康度: {avg_health:.1f}/100")
    print(f"问题总数: {total_issues} (P0: {len(p0_issues)}, P1: {len(p1_issues)}, P2: {len(p2_issues)})")


def main():
    parser = argparse.ArgumentParser(description='生成网站优化诊断摘要报告')
    parser.add_argument('--reports-dir', required=True, help='诊断报告目录')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 加载报告
    reports = load_reports(args.reports_dir)
    
    if not reports:
        print("没有找到任何诊断报告", file=sys.stderr)
        sys.exit(1)
    
    # 生成摘要
    generate_summary(reports, args.output)


if __name__ == '__main__':
    main()
