#!/usr/bin/env python3
"""
网站优化诊断脚本
调用豆包API，使用指定的提示词对网站进行诊断，输出JSON格式报告
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests


def load_prompt(prompt_file: str) -> dict:
    """加载提示词文件"""
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def call_doubao_api(prompt: str, api_key: str, endpoint_id: str) -> str:
    """
    调用豆包API进行诊断
    
    Args:
        prompt: 提示词内容
        api_key: 豆包API Key
        endpoint_id: 豆包Endpoint ID
    
    Returns:
        API返回的文本内容
    """
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": endpoint_id,
        "messages": [
            {
                "role": "system",
                "content": "你是一位专业的网站优化诊断专家。你的输出必须是严格的JSON格式，不得包含任何Markdown、解释文字或其他格式。直接输出JSON对象。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 8000,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"API调用失败: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}", file=sys.stderr)
        raise


def extract_json_from_response(response_text: str) -> dict:
    """
    从API响应中提取JSON对象
    处理API可能返回的Markdown代码块或其他格式
    """
    # 尝试直接解析
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # 尝试从Markdown代码块中提取
    import re
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # 尝试找到第一个{和最后一个}之间的内容
    first_brace = response_text.find('{')
    last_brace = response_text.rfind('}')
    if first_brace != -1 and last_brace != -1:
        try:
            return json.loads(response_text[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass
    
    raise ValueError(f"无法从响应中提取JSON: {response_text[:500]}")


def validate_report(report: dict, module: str) -> list:
    """验证报告格式是否正确，返回错误列表"""
    errors = []
    
    required_fields = ['report_id', 'generated_at', 'website_url', 'module', 'summary', 'issues', 'action_plan']
    
    for field in required_fields:
        if field not in report:
            errors.append(f"缺少必填字段: {field}")
    
    if 'module' in report and report['module'] != module:
        errors.append(f"module不匹配: 期望{module}, 实际{report['module']}")
    
    if 'summary' in report:
        if 'health_score' not in report['summary']:
            errors.append("summary缺少health_score")
        if 'most_critical_issue' not in report['summary']:
            errors.append("summary缺少most_critical_issue")
    
    if 'issues' in report:
        for i, issue in enumerate(report['issues']):
            if 'id' not in issue:
                errors.append(f"issue[{i}]缺少id")
            if 'priority' not in issue:
                errors.append(f"issue[{i}]缺少priority")
            if 'fix' not in issue:
                errors.append(f"issue[{i}]缺少fix")
    
    return errors


def main():
    parser = argparse.ArgumentParser(description='网站优化诊断脚本')
    parser.add_argument('--module', required=True, help='诊断模块名称')
    parser.add_argument('--prompt-file', required=True, help='提示词文件路径')
    parser.add_argument('--output-dir', required=True, help='输出目录')
    parser.add_argument('--website-url', default='https://www.aitoolcrux.com', help='网站URL')
    
    args = parser.parse_args()
    
    # 获取API配置
    api_key = os.environ.get('DOUBAO_API_KEY', '')
    endpoint_id = os.environ.get('DOUBAO_ENDPOINT_ID', '')
    
    if not api_key or not endpoint_id:
        print("错误: 未设置DOUBAO_API_KEY或DOUBAO_ENDPOINT_ID环境变量", file=sys.stderr)
        sys.exit(1)
    
    # 加载提示词
    print(f"加载提示词文件: {args.prompt_file}")
    prompt_data = load_prompt(args.prompt_file)
    prompt_content = prompt_data['prompt']
    
    # 添加网站URL到提示词
    full_prompt = f"{prompt_content}\n\n# 当前诊断的网站URL\n{args.website_url}\n\n# 当前时间\n{datetime.now().isoformat()}\n\n请立即开始诊断，输出严格的JSON格式报告。"
    
    # 调用API
    print(f"调用豆包API进行诊断... 模块: {args.module}")
    start_time = time.time()
    
    try:
        response_text = call_doubao_api(full_prompt, api_key, endpoint_id)
    except Exception as e:
        print(f"API调用失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    elapsed = time.time() - start_time
    print(f"API调用完成，耗时: {elapsed:.1f}秒")
    
    # 提取JSON
    try:
        report = extract_json_from_response(response_text)
    except ValueError as e:
        print(f"JSON提取失败: {e}", file=sys.stderr)
        # 保存原始响应用于调试
        os.makedirs(args.output_dir, exist_ok=True)
        debug_file = os.path.join(args.output_dir, f"{args.module}-raw-response.txt")
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(response_text)
        print(f"原始响应已保存到: {debug_file}", file=sys.stderr)
        sys.exit(1)
    
    # 验证报告
    errors = validate_report(report, args.module)
    if errors:
        print(f"报告验证警告 ({len(errors)}个):")
        for error in errors:
            print(f"  - {error}")
    
    # 确保report_id正确
    report['report_id'] = f"{args.module}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    report['generated_at'] = datetime.now().isoformat()
    report['website_url'] = args.website_url
    report['module'] = args.module
    
    # 保存报告
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, f"{args.module}-report.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"报告已保存: {output_file}")
    print(f"健康度评分: {report.get('summary', {}).get('health_score', 'N/A')}/100")
    print(f"问题数量: {len(report.get('issues', []))}")
    print(f"P0问题数量: {len([i for i in report.get('issues', []) if i.get('priority') == 'P0'])}")


if __name__ == '__main__':
    main()
