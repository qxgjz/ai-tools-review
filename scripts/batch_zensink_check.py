#!/usr/bin/env python3
"""用zens-ink批量检查所有文章内容质量"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zens_ink_toolkit import ZensInkToolkit

def main():
    with open('data/posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print(f"总文章数: {len(posts)}")
    
    zens = ZensInkToolkit()
    print(f"zens-ink状态: {zens.status()}")
    
    results = []
    low_quality = []
    keyword_issues = []
    
    print(f"\n开始批量检查...")
    for i, post in enumerate(posts):
        slug = post.get('slug', f'post-{i}')
        title = post.get('title', '')[:60]
        content = post.get('content', '')
        keyword = post.get('keyword', '') or post.get('primaryKeyword', '') or slug.replace('-', ' ')
        
        if not content or len(content) < 100:
            results.append({
                'slug': slug,
                'title': title,
                'score': 0,
                'issues': ['内容为空或过短'],
                'content_length': len(content)
            })
            continue
        
        try:
            result = zens.content_quality_check(content, keyword=keyword)
            item = {
                'slug': slug,
                'title': title,
                'score': result.get('overall_score', result.get('score', 0)),
                'readability': result.get('readability', {}),
                'keyword_density': result.get('keyword_density', {}),
                'structure': result.get('structure', {}),
                'issues': result.get('issues', result.get('warnings', [])),
                'content_length': len(content)
            }
            results.append(item)
            
            if item['score'] < 70:
                low_quality.append(item)
            
            kd = item.get('keyword_density', {})
            if isinstance(kd, dict):
                density = kd.get('density', kd.get('value', 0))
                if density and density < 0.5:
                    keyword_issues.append(item)
            
            if (i+1) % 20 == 0:
                print(f"  已检查 {i+1}/{len(posts)}...")
                
        except Exception as e:
            results.append({
                'slug': slug,
                'title': title,
                'score': -1,
                'issues': [f'检查失败: {str(e)[:100]}'],
                'content_length': len(content)
            })
    
    # 生成报告
    valid_results = [r for r in results if r['score'] >= 0]
    avg_score = sum(r['score'] for r in valid_results) / max(1, len(valid_results))
    
    print(f"\n{'='*60}")
    print(f"zens-ink 内容质量报告")
    print(f"{'='*60}")
    print(f"总检查数: {len(results)}")
    print(f"有效检查: {len(valid_results)}")
    print(f"平均分数: {avg_score:.1f}/100")
    print(f"低分(<70): {len(low_quality)}篇")
    print(f"关键词密度问题: {len(keyword_issues)}篇")
    
    # 分数分布
    score_ranges = {'90-100': 0, '80-89': 0, '70-79': 0, '60-69': 0, '<60': 0}
    for r in valid_results:
        s = r['score']
        if s >= 90: score_ranges['90-100'] += 1
        elif s >= 80: score_ranges['80-89'] += 1
        elif s >= 70: score_ranges['70-79'] += 1
        elif s >= 60: score_ranges['60-69'] += 1
        else: score_ranges['<60'] += 1
    
    print(f"\n分数分布:")
    for k, v in score_ranges.items():
        print(f"  {k}: {v}篇 ({v*100//max(1,len(valid_results))}%)")
    
    if low_quality:
        print(f"\n⚠️ 低分文章(<70):")
        for item in low_quality[:15]:
            print(f"  - {item['slug']}: 分数={item['score']}, 问题={item['issues'][:2]}")
        if len(low_quality) > 15:
            print(f"  ... 还有 {len(low_quality)-15} 篇")
    
    # 保存报告
    report = {
        'total': len(results),
        'valid': len(valid_results),
        'average_score': avg_score,
        'low_quality_count': len(low_quality),
        'keyword_issues_count': len(keyword_issues),
        'score_distribution': score_ranges,
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
