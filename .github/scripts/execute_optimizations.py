#!/usr/bin/env python3
"""
自动执行网站优化
根据诊断报告中的P0问题和代码修改建议，自动执行代码修改
"""

import argparse
import json
import os
import shutil
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
            except (json.JSONDecodeError, IOError) as e:
                print(f"加载失败 {filename}: {e}", file=sys.stderr)
    
    return reports


def extract_optimizations(reports: list, priority: str = 'P0', module_filter: str = 'all') -> list:
    """从报告中提取需要执行的优化"""
    optimizations = []
    
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
        
        # 模块过滤
        if module_filter != 'all' and module != module_filter:
            continue
        
        module_name = module_names.get(module, module)
        
        for issue in report.get('issues', []):
            # 优先级过滤
            if issue.get('priority') != priority:
                continue
            
            code_changes = issue.get('code_changes', [])
            
            # 只处理有代码修改建议的问题
            if not code_changes:
                print(f"跳过 [{module_name}] {issue.get('title')}: 无代码修改建议")
                continue
            
            optimizations.append({
                'module': module,
                'module_name': module_name,
                'issue': issue,
                'code_changes': code_changes
            })
    
    return optimizations


def backup_file(filepath: str, backup_dir: str) -> str:
    """备份文件"""
    if not os.path.exists(filepath):
        return None
    
    # 创建备份目录
    os.makedirs(backup_dir, exist_ok=True)
    
    # 生成备份文件名
    filename = os.path.basename(filepath)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_filename = f"{filename}.{timestamp}.bak"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # 复制文件
    shutil.copy2(filepath, backup_path)
    
    return backup_path


def apply_code_change(change: dict, project_root: str, backup_dir: str) -> dict:
    """
    应用单个代码修改
    
    Args:
        change: 代码修改信息
        project_root: 项目根目录
        backup_dir: 备份目录
    
    Returns:
        执行结果
    """
    file_path = change.get('file_path', '')
    change_type = change.get('change_type', 'modify')
    description = change.get('description', '')
    code_snippet = change.get('code_snippet', '')
    
    full_path = os.path.join(project_root, file_path)
    
    result = {
        'file_path': file_path,
        'change_type': change_type,
        'description': description,
        'success': False,
        'message': ''
    }
    
    try:
        if change_type == 'create':
            # 创建新文件
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(code_snippet)
            
            result['success'] = True
            result['message'] = f"文件创建成功: {file_path}"
            
        elif change_type == 'modify':
            # 修改现有文件
            if not os.path.exists(full_path):
                result['message'] = f"文件不存在: {file_path}"
                return result
            
            # 备份原文件
            backup_path = backup_file(full_path, backup_dir)
            result['backup_path'] = backup_path
            
            # 如果有old_code_snippet，尝试替换
            old_code = change.get('old_code_snippet', '')
            if old_code and code_snippet:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_code in content:
                    content = content.replace(old_code, code_snippet)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    result['success'] = True
                    result['message'] = f"代码替换成功: {file_path}"
                else:
                    result['message'] = f"未找到要替换的代码: {file_path}"
            else:
                # 没有old_code，记录需要人工审核
                result['success'] = True
                result['message'] = f"需要人工审核修改: {file_path} (已备份)"
                
        elif change_type == 'delete':
            # 删除文件
            if os.path.exists(full_path):
                # 备份后删除
                backup_path = backup_file(full_path, backup_dir)
                result['backup_path'] = backup_path
                
                os.remove(full_path)
                result['success'] = True
                result['message'] = f"文件删除成功: {file_path} (已备份)"
            else:
                result['message'] = f"文件不存在: {file_path}"
                
    except Exception as e:
        result['message'] = f"执行失败: {str(e)}"
    
    return result


def main():
    parser = argparse.ArgumentParser(description='自动执行网站优化')
    parser.add_argument('--reports-dir', required=True, help='诊断报告目录')
    parser.add_argument('--priority', default='P0', choices=['P0', 'P1', 'P2', 'all'], help='执行优先级')
    parser.add_argument('--module', default='all', help='执行的模块（all或具体模块名）')
    parser.add_argument('--project-root', default='.', help='项目根目录')
    parser.add_argument('--output-dir', required=True, help='输出目录（保存执行日志和备份）')
    
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    backup_dir = os.path.join(args.output_dir, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # 加载报告
    reports = load_reports(args.reports_dir)
    
    if not reports:
        print("没有找到任何诊断报告", file=sys.stderr)
        sys.exit(1)
    
    print(f"加载了 {len(reports)} 个诊断报告")
    
    # 提取优化项
    priority = args.priority if args.priority != 'all' else None
    optimizations = []
    
    if priority:
        optimizations = extract_optimizations(reports, priority, args.module)
    else:
        for p in ['P0', 'P1', 'P2']:
            optimizations.extend(extract_optimizations(reports, p, args.module))
    
    print(f"找到 {len(optimizations)} 个需要执行的优化项")
    
    if not optimizations:
        print("没有需要执行的优化项")
        return
    
    # 执行优化
    all_results = []
    success_count = 0
    failed_count = 0
    
    for i, opt in enumerate(optimizations, 1):
        module_name = opt['module_name']
        issue = opt['issue']
        code_changes = opt['code_changes']
        
        print(f"\n[{i}/{len(optimizations)}] 执行优化: [{module_name}] {issue.get('title')}")
        
        issue_results = []
        
        for change in code_changes:
            result = apply_code_change(change, args.project_root, backup_dir)
            issue_results.append(result)
            
            if result['success']:
                print(f"  ✅ {result['message']}")
            else:
                print(f"  ❌ {result['message']}")
        
        # 统计
        issue_success = sum(1 for r in issue_results if r['success'])
        issue_failed = sum(1 for r in issue_results if not r['success'])
        success_count += issue_success
        failed_count += issue_failed
        
        all_results.append({
            'module': opt['module'],
            'module_name': module_name,
            'issue_title': issue.get('title'),
            'priority': issue.get('priority'),
            'results': issue_results
        })
    
    # 保存执行日志
    log_file = os.path.join(args.output_dir, f"optimization-log-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'reports_dir': args.reports_dir,
        'priority': args.priority,
        'module': args.module,
        'project_root': args.project_root,
        'total_optimizations': len(optimizations),
        'total_changes': success_count + failed_count,
        'success_count': success_count,
        'failed_count': failed_count,
        'results': all_results
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    # 输出总结
    print(f"\n{'='*60}")
    print(f"执行总结")
    print(f"{'='*60}")
    print(f"优化项总数: {len(optimizations)}")
    print(f"代码修改总数: {success_count + failed_count}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"执行日志: {log_file}")
    print(f"备份目录: {backup_dir}")
    
    if failed_count > 0:
        print(f"\n⚠️  有 {failed_count} 个修改失败，需要人工审核")
        sys.exit(1)


if __name__ == '__main__':
    main()
