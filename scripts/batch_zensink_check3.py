#!/usr/bin/env python3
"""用zens-ink原生API批量检查所有文章（保存临时文件方式）"""
import json
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zens_ink import content_qc

def main():
    with open('data/posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print(f"总文章数: {len(posts)}")
    
    # 创建临时目录
    tmp_dir = tempfile.mkdtemp(prefix='zens_check_')
    print(f"临时目录: {tmp_dir}")
    
    results = []
    low_quality = []
    issues_count = {}
    
    print(f"\n开始批量检查...")
    for i, post in enumerate(posts):
        slug = post.get('slug', f'post-{i}')
        title = post.get('title', '')[:60]
        content = post.get('content', '')
        
        if not content or len(content) < 100:
            results.append({
                'slug': slug,
                'title': title,
                'grade': 'F',
                'score': 0,
                'issues': ['内容为空或过短'],
                'content_length': len(content)
            })
            continue
        
        try:
            # 保存为临时markdown文件
            tmp_file = Path(tmp_dir) / f"{slug[:50]}.md"
            # 把HTML内容转为纯文本（zens-ink期望markdown）
            import re
            text_content = re.sub(r'<[^>]+>', '', content)
            text_content = re.sub(r'&nbsp;', ' ', text_content)
            text_content = re.sub(r'&amp;', '&', text_content)
            tmp_file.write_text(f"# {title}\n\n{text_content}", encoding='utf-8')
            
            # 调用check_draft
            draft_result = content_qc.check_draft(tmp_file)
            grade = content_qc.grade(draft_result)
            
            # 提取问题
            issues = []
            if isinstance(draft_result, dict):
                for key, value in draft_result.items():
                    if key in ['word_count', 'reading_time', 'flesch_kincaid', 'flesch_reading_ease']:
                        continue
                    if isinstance(value, (int, float)) and value == 0:
                        issues.append(f"{key}: 缺失")
                    elif isinstance(value, list) and len(value) > 0:
                        issues.append(f"{key}: {len(value)}个问题")
                    elif isinstance(value, dict):
                        for k2, v2 in value.items():
                            if isinstance(v2, (int, float)) and v2 == 0:
                                issues.append(f"{key}.{k2}: 缺失")
                            elif isinstance(v2, list) and len(v2) > 0:
                                issues.append(f"{key}.{k2}: {len(v2)}个问题")
            
            # grade转分数
            grade_scores = {'A+': 95, 'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 40, 'N/A': 0}
            score = grade_scores.get(grade, 50)
            
            item = {
                'slug': slug,
                'title': title,
                'grade': grade,
                'score': score,
                'issues': issues[:5],
                'word_count': draft_result.get('word_count', 0) if isinstance(draft_result, dict) else 0,
                'content_length': len(content)
            }
            results.append(item)
            
            if score < 70:
                low_quality.append(item)
            
            for issue in issues:
                issue_type = issue.split(':')[0] if ':' in issue else issue
                issues_count[issue_type] = issues_count.get(issue_type, 0) + 1
            
            if (i+1) % 20 == 0:
                print(f"  已检查 {i+1}/{len(posts)}...")
                
        except Exception as e:
            results.append({
                'slug': slug,
                'title': title,
                'grade': 'ERROR',
                'score': -1,
                'issues': [f'检查失败: {str(e)[:100]}'],
                'content_length': len(content)
            })
    
    # 清理临时文件
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)
    
    # 生成报告
    valid_results = [r for r in results if r['score'] >= 0]
    avg_score = sum(r['score'] for r in valid_results) / max(1, len(valid_results))
    
    grade_dist = {}
    for r in valid_results:
        g = r['grade']
        grade_dist[g] = grade_dist.get(g, 0) + 1
    
    print(f"\n{'='*60}")
    print(f"zens-ink 内容质量报告")
    print(f"{'='*60}")
    print(f"总检查数: {len(results)}")
    print(f"有效检查: {len(valid_results)}")
    print(f"平均分数: {avg_score:.1f}/100")
    print(f"低分(<70): {len(low_quality)}篇")
    
    print(f"\nGrade分布:")
    for g in ['A+', 'A', 'B', 'C', 'D', 'F', 'N/A', 'ERROR']:
        if g in grade_dist:
            print(f"  {g}: {grade_dist[g]}篇 ({grade_dist[g]*100//max(1,len(valid_results))}%)")
    
    print(f"\n最常见问题:")
    for issue, count in sorted(issues_count.items(), key=lambda x: -x[1])[:10]:
        print(f"  {issue}: {count}篇")
    
    if low_quality:
        print(f"\n⚠️ 低分文章(<70):")
        for item in low_quality[:15]:
            print(f"  - {item['slug']}: grade={item['grade']}, 字数={item.get('word_count',0)}, 问题={item['issues'][:2]}")
        if len(low_quality) > 15:
            print(f"  ... 还有 {len(low_quality)-15} 篇")
    
    # 保存报告
    report = {
        'total': len(results),
        'valid': len(valid_results),
        'average_score': avg_score,
        'low_quality_count': len(low_quality),
        'grade_distribution': grade_dist,
        'common_issues': issues_count,
        'low_quality_articles': low_quality,
        'all_results': results
    }
    
    report_path = 'iteration_center/zensink_content_quality_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")
    
    return report

if __name__ == '__main__':
    main()
