#!/usr/bin/env python3
"""批量检查所有文章的幻觉问题"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llmevalkit_toolkit import LMEvalKit

def main():
    # 读取文章
    with open('data/posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    print(f"总文章数: {len(posts)}")
    print(f"文章keys: {list(posts[0].keys()) if posts else '空'}")
    
    # 初始化评估器
    evaluator = LMEvalKit()
    print(f"\nllmevalkit状态: 已安装={evaluator.available}, 模块数={len(evaluator._modules)}")
    
    # 批量检查
    results = []
    hallucinated = []
    low_score = []
    
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
                'hallucination': 'N/A',
                'warnings': ['内容为空或过短'],
                'content_length': len(content)
            })
            continue
        
        try:
            result = evaluator.evaluate_content(content, keyword=keyword)
            item = {
                'slug': slug,
                'title': title,
                'score': result.get('score', 0),
                'hallucination': result.get('hallucination_detected', False),
                'ai_probability': result.get('ai_content_probability', 0),
                'warnings': result.get('warnings', []),
                'content_length': len(content)
            }
            results.append(item)
            
            if item['hallucination']:
                hallucinated.append(item)
            if item['score'] < 60:
                low_score.append(item)
                
            if (i+1) % 20 == 0:
                print(f"  已检查 {i+1}/{len(posts)}...")
                
        except Exception as e:
            results.append({
                'slug': slug,
                'title': title,
                'score': -1,
                'hallucination': 'ERROR',
                'warnings': [f'检查失败: {str(e)[:100]}'],
                'content_length': len(content)
            })
    
    # 生成报告
    print(f"\n{'='*60}")
    print(f"幻觉检测报告")
    print(f"{'='*60}")
    print(f"总检查数: {len(results)}")
    print(f"检测到幻觉: {len(hallucinated)}篇")
    print(f"低分(<60): {len(low_score)}篇")
    print(f"平均分数: {sum(r['score'] for r in results if r['score'] >= 0) / max(1, len([r for r in results if r['score'] >= 0])):.1f}")
    
    if hallucinated:
        print(f"\n⚠️ 检测到幻觉的文章:")
        for item in hallucinated[:20]:
            print(f"  - {item['slug']}: 分数={item['score']}, 警告={item['warnings'][:2]}")
        if len(hallucinated) > 20:
            print(f"  ... 还有 {len(hallucinated)-20} 篇")
    
    if low_score:
        print(f"\n⚠️ 低分文章(<60):")
        for item in low_score[:20]:
            print(f"  - {item['slug']}: 分数={item['score']}, 字数={item['content_length']}")
        if len(low_score) > 20:
            print(f"  ... 还有 {len(low_score)-20} 篇")
    
    # 保存报告
    report = {
        'total': len(results),
        'hallucinated_count': len(hallucinated),
        'low_score_count': len(low_score),
        'average_score': sum(r['score'] for r in results if r['score'] >= 0) / max(1, len([r for r in results if r['score'] >= 0])),
        'hallucinated_articles': hallucinated,
        'low_score_articles': low_score,
        'all_results': results
    }
    
    report_path = 'iteration_center/hallucination_audit_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")
    
    return report

if __name__ == '__main__':
    main()
