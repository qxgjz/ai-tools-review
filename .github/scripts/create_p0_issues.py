#!/usr/bin/env python3
"""
根据诊断报告创建GitHub Issue（P0问题）
自动为每个P0问题创建一个GitHub Issue，方便跟踪和管理
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests


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
            except (json.JSONDecodeError, IOError) as e:
                print(f"加载失败 {filename}: {e}", file=sys.stderr)
    
    return reports


def extract_p0_issues(reports: list) -> list:
    """从报告中提取所有P0问题"""
    p0_issues = []
    
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
    
    for report in reports:
        module = report.get('module', 'unknown')
        module_name = module_names.get(module, module)
        
        for issue in report.get('issues', []):
            if issue.get('priority') == 'P0':
                p0_issues.append({
                    'module': module,
                    'module_name': module_name,
                    'issue': issue
                })
    
    return p0_issues


def create_github_issue(
    token: str,
    repo: str,
    title: str,
    body: str,
    labels: list = None
) -> dict:
    """
    创建GitHub Issue
    
    Args:
        token: GitHub Token
        repo: 仓库名（owner/repo）
        title: Issue标题
        body: Issue内容
        labels: 标签列表
    
    Returns:
        创建的Issue信息
    """
    url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "title": title,
        "body": body,
        "labels": labels or []
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"创建Issue失败: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}", file=sys.stderr)
        raise


def generate_issue_body(module_name: str, issue: dict) -> str:
    """生成Issue内容"""
    fix = issue.get('fix', {})
    evidence = issue.get('evidence', {})
    code_changes = issue.get('code_changes', [])
    
    body = []
    body.append(f"## 问题描述")
    body.append(f"")
    body.append(f"**模块**: {module_name}")
    body.append(f"**严重程度**: {issue.get('severity', 'unknown')}")
    body.append(f"**优先级**: {issue.get('priority', 'P0')}")
    body.append(f"")
    body.append(f"### 问题详情")
    body.append(f"{issue.get('title', '未知问题')}")
    body.append(f"")
    body.append(f"### 证据")
    body.append(f"{evidence.get('description', '无')}")
    body.append(f"")
    
    if evidence.get('affected_urls'):
        body.append(f"**受影响的URL**:")
        for url in evidence['affected_urls'][:5]:  # 最多显示5个
            body.append(f"- {url}")
        body.append(f"")
    
    body.append(f"### 修复方案")
    body.append(f"{fix.get('description', '待补充')}")
    body.append(f"")
    
    if fix.get('steps'):
        body.append(f"**执行步骤**:")
        for i, step in enumerate(fix['steps'], 1):
            body.append(f"{i}. {step}")
        body.append(f"")
    
    body.append(f"**预估工作量**: {fix.get('estimated_effort', '未知')}")
    body.append(f"**预期效果**: {fix.get('expected_impact', '未知')}")
    body.append(f"")
    
    if fix.get('rollback_plan'):
        body.append(f"**回滚方案**: {fix['rollback_plan']}")
        body.append(f"")
    
    if code_changes:
        body.append(f"### 需要修改的文件")
        body.append(f"")
        for change in code_changes:
            body.append(f"- **{change.get('change_type', 'modify')}**: `{change.get('file_path', 'unknown')}`")
            body.append(f"  - {change.get('description', '')}")
        body.append(f"")
    
    body.append(f"---")
    body.append(f"*此Issue由GitHub Actions自动诊断工作流创建*")
    body.append(f"*创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return '\n'.join(body)


def main():
    parser = argparse.ArgumentParser(description='根据诊断报告创建GitHub Issue')
    parser.add_argument('--reports-dir', required=True, help='诊断报告目录')
    parser.add_argument('--github-token', required=True, help='GitHub Token')
    parser.add_argument('--repo', default='qxgjz/ai-tools-review', help='GitHub仓库名')
    
    args = parser.parse_args()
    
    # 加载报告
    reports = load_reports(args.reports_dir)
    
    if not reports:
        print("没有找到任何诊断报告", file=sys.stderr)
        sys.exit(1)
    
    # 提取P0问题
    p0_issues = extract_p0_issues(reports)
    
    print(f"找到 {len(p0_issues)} 个P0问题")
    
    if not p0_issues:
        print("没有P0问题，无需创建Issue")
        return
    
    # 创建Issue
    created_issues = []
    failed_issues = []
    
    for i, p0_data in enumerate(p0_issues, 1):
        module_name = p0_data['module_name']
        issue = p0_data['issue']
        
        title = f"[P0][{module_name}] {issue.get('title', '未知问题')}"
        body = generate_issue_body(module_name, issue)
        labels = ['P0', 'auto-diagnosis', module_name.lower().replace('_', '-')]
        
        print(f"[{i}/{len(p0_issues)}] 创建Issue: {title}")
        
        try:
            result = create_github_issue(
                token=args.github_token,
                repo=args.repo,
                title=title,
                body=body,
                labels=labels
            )
            created_issues.append(result)
            print(f"  ✅ 创建成功: {result.get('html_url', 'unknown')}")
        except Exception as e:
            failed_issues.append((title, str(e)))
            print(f"  ❌ 创建失败: {e}", file=sys.stderr)
        
        # 避免API限流
        if i < len(p0_issues):
            import time
            time.sleep(1)
    
    # 输出总结
    print(f"")
    print(f"=== 创建总结 ===")
    print(f"成功创建: {len(created_issues)} 个Issue")
    print(f"创建失败: {len(failed_issues)} 个Issue")
    
    if created_issues:
        print(f"")
        print(f"创建的Issue链接:")
        for issue in created_issues:
            print(f"  - {issue.get('title', 'unknown')}: {issue.get('html_url', 'unknown')}")


if __name__ == '__main__':
    main()
