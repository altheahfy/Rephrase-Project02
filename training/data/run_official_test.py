#!/usr/bin/env python3
"""
正式テスト手順実行（動的版）
- final_54_test_data.jsonから動的にテストケースを読み込み
- 文法項目別選択機能付き（実装していない文法の部分を除外可能）
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
from central_controller import CentralController
import json
import os
import argparse
from datetime import datetime
import argparse

def select_test_cases(test_cases, test_selection):
    """
    テスト選択文字列に基づいてテストケースを選択
    test_selection例:
    - "1,2,3": ID 1,2,3
    - "1-5": ID 1から5まで
    - "basic": 基本5文型
    - "relation": 関係節
    - "1,3-5,8": 複合指定
    """
    selected_ids = set()
    
    if test_selection.lower() == "basic":
        # 基本5文型のテストID（17件）
        selected_ids = {1, 2, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69}
    elif test_selection.lower() == "relation":
        # 関係節のテストID
        selected_ids = {3, 4, 5, 6, 7, 8, 12, 13, 14, 34, 35, 36}
    elif test_selection.lower() == "passive":
        # 受動態のテストID
        selected_ids = {9, 10, 11, 21, 22, 23, 24}
    else:
        # 数値指定の解析
        parts = test_selection.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                # 範囲指定 (例: "3-5")
                start, end = map(int, part.split('-'))
                selected_ids.update(range(start, end + 1))
            else:
                # 単一ID (例: "1")
                selected_ids.add(int(part))
    
    # 選択されたIDのテストケースを返す
    return [case for case in test_cases if case['id'] in selected_ids]

def load_test_cases():
    """final_54_test_data.jsonからテストデータを読み込み、リスト形式で返す"""
    test_file = "final_test_system/final_54_test_data.json"
    
    if not os.path.exists(test_file):
        raise FileNotFoundError(f"テストデータファイルが見つかりません: {test_file}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # 辞書形式のデータをリスト形式に変換
    test_cases = []
    for test_id, test_case in test_data['data'].items():
        test_case['id'] = int(test_id)  # IDを整数として追加
        test_cases.append(test_case)
    
    return test_cases

def classify_grammar_type(sentence):
    """文法タイプを自動分類"""
    sentence_lower = sentence.lower()
    
    # 関係節の判定
    if any(word in sentence_lower for word in ['who', 'whose', 'which', 'that']):
        if 'whose' in sentence_lower:
            return 'relative_whose'
        return 'relative_clause'
    
    # 受動態の判定
    passive_patterns = [
        'is ', 'are ', 'was ', 'were ', 'been ', 'being '
    ]
    if any(pattern in sentence_lower for pattern in passive_patterns):
        # さらに詳細な受動態判定が必要な場合はここで
        if any(word in sentence_lower for word in ['by ']):
            return 'passive_voice'
    
    # 複合時制の判定
    if any(aux in sentence_lower for aux in ['have ', 'has ', 'had ', 'will ', 'would ', 'can ', 'could ', 'may ', 'might ', 'should ', 'must ']):
        return 'auxiliary_complex'
    
    # デフォルトは基本5文型
    return 'basic_five_pattern'

def filter_tests_by_grammar(test_data, grammar_types=None):
    """文法タイプでテストケースをフィルタリング"""
    if grammar_types is None:
        # デフォルト：基本5文型 + 関係節のみ（受動態と複合時制を除外）
        grammar_types = ['basic_five_pattern', 'relative_clause', 'relative_whose']
    
    filtered_tests = {}
    for test_id, test_case in test_data['data'].items():
        sentence = test_case['sentence']
        grammar_type = classify_grammar_type(sentence)
        
        if grammar_type in grammar_types:
            filtered_tests[test_id] = test_case
    
    return filtered_tests

def run_official_test(grammar_types=None):
    """正式テスト手順の実行（動的版）"""
def run_official_test(grammar_types=None):
    """正式テスト手順の実行（動的版）"""
    
    # テストデータの読み込み
    try:
        test_cases = load_test_cases()
        print(f"✅ テストデータ読み込み完了: {len(test_cases)}件のテストケース")
    except FileNotFoundError as e:
        print(f"❌ エラー: {e}")
        return None
    
    # 文法タイプによるフィルタリング（選択されたケースのみ）
    if grammar_types:
        filtered_cases = []
        for case in test_cases:
            grammar_type = classify_grammar_type(case['sentence'])
            if grammar_type in grammar_types:
                filtered_cases.append(case)
    else:
        # デフォルト：基本5文型 + 関係節
        basic_cases = select_test_cases(test_cases, "basic")
        relation_cases = select_test_cases(test_cases, "relation")
        filtered_cases = basic_cases + relation_cases
    print(f"📋 フィルタリング結果: {len(filtered_cases)}件のテストケースを実行")
    
    # 新しい関数を使用
    return run_official_test_with_selected_cases(filtered_cases)

def run_official_test_with_selected_cases(selected_cases):
    """選択されたテストケースで正式テストを実行"""
    print("✅ spaCy動的文法認識システム初期化完了")
    
    # DynamicGrammarMapperを初期化してからCentral Controllerに渡す
    mapper = DynamicGrammarMapper()
    controller = CentralController(mapper)
    print("🎯 Central Controller初期化: Phase 2: Precision Enhancement Controller")
    print("🔥 Phase 1.0 ハンドラー管理システム初期化完了: 4個のハンドラーがアクティブ")
    print("   アクティブハンドラー: basic_five_pattern, relative_clause, passive_voice, auxiliary_complex")
    
    print(f"\n=== 正式テスト手順実行（選択されたテストケース {len(selected_cases)}件）===\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(selected_cases),
        "results": {}
    }
    
    grammar_counts = {}
    
    for test_case in selected_cases:
        test_id = test_case['id']
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        # 文法タイプの判定
        grammar_type = classify_grammar_type(sentence)
        grammar_counts[grammar_type] = grammar_counts.get(grammar_type, 0) + 1
        
        print(f"テスト {test_id} ({grammar_type}): {sentence}")
        
        try:
            # Central Controllerで分析実行
            result = controller.analyze_sentence(sentence)
            
            # compare_results.pyが期待する形式で保存
            results["results"][test_id] = {
                "sentence": sentence,
                "expected": expected,
                "analysis_result": result,
                "test_type": grammar_type,
                "status": "success"
            }
            
            print(f"期待値: {expected}")
            print(f"実際値: {result.get('slots', {})}")  # main_slots -> slots
            if expected.get('sub_slots'):
                print(f"サブ期待: {expected.get('sub_slots', {})}")
                print(f"サブ実際: {result.get('sub_slots', {})}")
                print(f"🔍 DEBUG: 完全なresult構造: {result}")  # デバッグ用
            
        except Exception as e:
            print(f"動的文法解析エラー: {e}")
            results["results"][test_id] = {
                "sentence": sentence,
                "expected": expected,
                "analysis_result": {},
                "test_type": grammar_type,
                "status": "error",
                "error": str(e)
            }
            print(f"期待値: {expected}")
            print(f"実際値: {{}}")
            if expected.get('sub_slots'):
                print(f"サブ期待: {expected.get('sub_slots', {})}")
                print(f"サブ実際: {{}}")
        
        print("-" * 60)
    
    print(f"\n=== テスト概要 ===")
    for grammar_type, count in grammar_counts.items():
        print(f"{grammar_type}テスト: {count}件")
    print(f"総テスト数: {len(selected_cases)}件")
    
    # 結果をJSONファイルに保存
    output_file = "official_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"結果を保存: {output_file}")
    return output_file

def main():
    """コマンドライン実行用メイン関数"""
    parser = argparse.ArgumentParser(description='正式テスト手順実行（動的版）')
    parser.add_argument('--tests', '-t', 
                       type=str,
                       help='実行するテスト番号（例: "1,2,3-5,8" または "basic" または "relation" または "passive"）')
    parser.add_argument('--all', action='store_true', help='全てのテストケースを実行')
    
    args = parser.parse_args()
    
    # テストケースをロード
    test_cases = load_test_cases()
    
    if args.all:
        # 全てのテストケースを実行
        selected_cases = test_cases
        print("🔥 全テストケースを実行します")
    elif args.tests:
        # 指定されたテストケースを実行
        selected_cases = select_test_cases(test_cases, args.tests)
        print(f"🎯 選択されたテスト: {args.tests}")
    else:
        # デフォルト: 基本5文型 + 関係節 + 受動態 (24件)
        basic_cases = select_test_cases(test_cases, "basic")
        relation_cases = select_test_cases(test_cases, "relation") 
        passive_cases = select_test_cases(test_cases, "passive")
        selected_cases = basic_cases + relation_cases + passive_cases
        print("🎯 デフォルト実行: 基本5文型 + 関係節 + 受動態 (24件)")
    
    run_official_test_with_selected_cases(selected_cases)

if __name__ == "__main__":
    main()
