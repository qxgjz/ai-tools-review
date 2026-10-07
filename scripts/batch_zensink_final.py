#!/usr/bin/env python3
"""用zens-ink原生API批量检查所有文章（修正版）"""
import json
import sys
import os
import tempfile
import re
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zens_ink import content_qc

def main():
    with open('data/posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print(f"总文章数: {len(posts)}")
    
    tmp_dir = tempfile.mkdtemp(prefix='zens_check_')
    
    results = []
    low_quality = []
    failed_checks = {}
    
    print(f"\n开始批量检查...")
    for i, post in enumerate(posts):
        slug = post.get('slug', f'post-{i}')
        title = post.get('title', '')[:60]
        content = post.get('content', '')
        
        if not content or len(content) < 100:
            results.append({
                'slug': slug, 'title': title, 'score': 0,
                'issues': ['内容为空或过短'], 'content_length': len(content)
            })
            continue
        
        try:
            tmp_file = Path(tmp_dir) / f"{slug[:50]}.md"
            text_content = re.sub(r'<[^>]+>', '', content)
            text_content = re.sub(r'&nbsp;', ' ', text_content)
            text_content = re.sub(r'&amp;', '&', text_content)
            tmp_file.write_text(f"# {title}\n\n{text_content}", encoding='utf-8')
            
            draft_result = content_qc.check_draft(tmp_file)
            score = draft_result.get('score', 0)
            checks = draft_result.get('checks', [])
            
            # 提取未通过的检查项
            issues = []
            for check in checks:
                if not check.get('pass', False):
                    check_name = check.get('check', 'unknown')
                    issues.append(check_name)
                    failed_checks[check_name] = failed_checks.get(check_name, 0) + 1
            
            item = {
                'slug': slug,
                'title': title,
                'score': score,
                'word_count': draft_result.get('word_count', 0),
                'fact_density': draft_result.get('fact_density', 0),
                'vague_density': draft_result.get('vague_density', 0),
                'issues': issues,
                'content_length': len(content)
            }
            results.append(item)
            
            if score < 70:
                low_quality.append(item)
            
            if (i+1) % 20 == 0:
                print(f"  已检查 {i+1}/{len(posts)}...")
                
        except Exception as e:
            results.append({
                'slug': slug, 'title': title, 'score': -1,
                'issues': [f'检查失败: {str(e)[:100]}'], 'content_length': len(content)
            })
    
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)
    
    # 报告
    valid = [r for r in results if r['score'] >= 0]
    avg_score = sum(r['score'] for r in valid) / max(1, len(valid))
    
    # 分数分布
    ranges = {'90-100': 0, '80-89': 0, '70-79': 0, '60-69': 0, '50-59': 0, '<50': 0}
    for r in valid:
        s = r['score']
        if s >= 90: ranges['90-100'] += 1
        elif s >= 80: ranges['80-89'] += 1
        elif s >= 70: ranges['70-79'] += 1
        elif s >= 60: ranges['60-69'] += 1
        elif s >= 50: ranges['50-59'] += 1
        else: ranges['<50'] += 1
    
    print(f"\n{'='*60}")
    print(f"zens-ink 内容质量报告（145篇）")
    print(f"{'='*60}")
    print(f"总检查: {len(results)}, 有效: {len(valid)}")
    print(f"平均分数: {avg_score:.1f}/100")
    print(f"及格(>=70): {len(valid)-len(low_quality)}篇 ({(len(valid)-len(low_quality))*100//max(1,len(valid))}%)")
    print(f"不及格(<70): {len(low_quality)}篇")
    
    print(f"\n分数分布:")
    for k, v in ranges.items():
        print(f"  {k}: {v}篇 ({v*100//max(1,len(valid))}%)")
    
    print(f"\n最常见未通过项:")
    for check, count in sorted(failed_checks.items(), key=lambda x: -x[1])[:10]:
        print(f"  {check}: {count}篇 ({count*100//max(1,len(valid))}%)")
    
    if low_quality:
        print(f"\n⚠️ 最低分10篇:")
        for item in sorted(low_quality, key=lambda x: x['score'])[:10]:
            print(f"  {item['score']}分 - {item['slug']} (字数={item['word_count']})")
    
    # 保存
    report = {
        'total': len(results), 'valid': len(valid),
        'average_score': avg_score,
        'pass_count': len(valid) - len(low_quality),
        'fail_count': len(low_quality),
        'score_ranges': ranges,
        'common_failed_checks': failed_checks,
        'low_quality_articles': sorted(low_quality, key=lambda x: x['score'])[:30],
        'all_results': results
    }
    
    report_path = 'iteration_center/zensink_content_quality_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")
    
    return report

if __name__ == '__main__':
    main()
