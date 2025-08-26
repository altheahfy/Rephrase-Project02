#!/usr/bin/env python3
"""
失敗ケースの抽出・分析
"""

import json
import os

def analyze_failures():
    """失敗ケースを分析して主要な問題パターンを特定"""
    
    report_path = "53_complete_test_report.json"
    
    if not os.path.exists(report_path):
        print(f"❌ レポートファイルが見つかりません: {report_path}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔍 失敗ケース分析")
    print("=" * 50)
    print(f"総テスト数: {data['meta']['total_tests']}")
    print(f"完全一致: {data['meta']['perfect_matches']} ({data['meta']['perfect_matches']/data['meta']['total_tests']*100:.1f}%)")
    print(f"失敗: {data['meta']['failures']} ({data['meta']['failures']/data['meta']['total_tests']*100:.1f}%)")
    
    print("\n❌ 失敗ケース詳細:")
    print("-" * 50)
    
    failure_patterns = {}
    
    for result in data['results']:
        if not result['perfect']:
            test_id = result['test_id']
            sentence = result['sentence']
            
            print(f"\n🧪 テスト{test_id}: {sentence}")
            
            # システム出力と期待値の差分を分析
            sys_main = result['system_output']['main_slots']
            sys_sub = result['system_output']['sub_slots']
            exp_main = result['expected']['main_slots']
            exp_sub = result['expected']['sub_slots']
            
            print("  システム出力:")
            for k, v in sys_main.items():
                if v:
                    print(f"    {k}: {v}")
            for k, v in sys_sub.items():
                if v:
                    print(f"    {k}: {v}")
            
            print("  期待値:")
            for k, v in exp_main.items():
                if v:
                    print(f"    {k}: {v}")
            for k, v in exp_sub.items():
                if v:
                    print(f"    {k}: {v}")
            
            # 失敗パターン分類
            main_issues = []
            for key in set(sys_main.keys()) | set(exp_main.keys()):
                if sys_main.get(key, '') != exp_main.get(key, ''):
                    main_issues.append(f"{key}不一致")
            
            sub_issues = []
            for key in set(sys_sub.keys()) | set(exp_sub.keys()):
                if sys_sub.get(key, '') != exp_sub.get(key, ''):
                    sub_issues.append(f"{key}不一致")
            
            if main_issues:
                pattern = "主節:" + ",".join(main_issues)
                failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1
            
            if sub_issues:
                pattern = "従属節:" + ",".join(sub_issues)
                failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1
    
    print("\n📊 失敗パターン統計:")
    print("-" * 50)
    for pattern, count in sorted(failure_patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pattern}: {count}回")

if __name__ == "__main__":
    analyze_failures()
