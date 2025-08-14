#!/usr/bin/env python3
"""
Priority 15・16エンジンの問題確認テスト
正しいRephrase的スロット分解仕様に基づく検証
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from grammar_master_controller_v2 import GrammarMasterControllerV2

def test_priority_15_16_issues():
    """Priority 15・16エンジンの問題を具体的に確認"""
    print("🔍 Priority 15・16エンジン問題確認テスト")
    print("=" * 60)
    
    controller = GrammarMasterControllerV2()
    
    # Priority 15 (ImperativeEngine) テストケース
    imperative_tests = [
        {
            'sentence': "Go!",
            'expected': {'V': 'Go'},
            'description': '最简命令文'
        },
        {
            'sentence': "Don't go!",
            'expected': {'Aux': "Don't", 'V': 'go'},
            'description': '否定命令文'
        },
        {
            'sentence': "Give me the book.",
            'expected': {'V': 'Give', 'O2': 'me', 'O1': 'the book'},
            'description': '二重目的語命令文'
        },
        {
            'sentence': "Put the book on the table carefully.",
            'expected': {'V': 'Put', 'O1': 'the book', 'C2': 'on the table', 'M3': 'carefully'},
            'description': '複雑命令文'
        }
    ]
    
    # Priority 16 (ExistentialThereEngine) テストケース
    existential_tests = [
        {
            'sentence': "There is a book on the table.",
            'expected': {'S': 'There', 'V': 'is', 'C1': 'a book', 'C2': 'on the table'},
            'description': '基本存在文'
        },
        {
            'sentence': "There are many students.",
            'expected': {'S': 'There', 'V': 'are', 'C1': 'many students'},
            'description': '複数存在文'
        },
        {
            'sentence': "There will be a party tonight.",
            'expected': {'S': 'There', 'Aux': 'will', 'V': 'be', 'C1': 'a party', 'M3': 'tonight'},
            'description': '未来存在文'
        },
        {
            'sentence': "There have been several complaints recently.",
            'expected': {'S': 'There', 'Aux': 'have', 'V': 'been', 'C1': 'several complaints', 'M3': 'recently'},
            'description': '完了存在文'
        }
    ]
    
    # Priority 15テスト実行
    print("\n📋 Priority 15 (ImperativeEngine) 問題確認")
    print("-" * 50)
    
    imperative_issues = []
    
    for i, test_case in enumerate(imperative_tests, 1):
        sentence = test_case['sentence']
        expected = test_case['expected']
        description = test_case['description']
        
        result = controller.process_sentence(sentence)
        
        # EngineResultオブジェクトのプロパティにアクセス
        selected_engines = [result.engine_type.name] if hasattr(result.engine_type, 'name') else [str(result.engine_type)]
        actual_slots = result.slots
        confidence = result.confidence
        
        print(f"Test {i}: {sentence} ({description})")
        print(f"  Selected: {selected_engines}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual_slots}")
        print(f"  Confidence: {confidence:.3f}")
        
        # 問題点の確認
        issues = []
        
        # エンジン選択の確認
        if 'IMPERATIVE' not in [eng.upper() for eng in selected_engines]:
            issues.append(f"ImperativeEngineが選択されていない (選択: {selected_engines})")
        
        # スロット分解の確認
        for key, expected_value in expected.items():
            if key not in actual_slots:
                issues.append(f"スロット {key} が不足 (期待値: '{expected_value}')")
            elif actual_slots[key] != expected_value:
                issues.append(f"スロット {key} が不正 (期待: '{expected_value}', 実際: '{actual_slots[key]}')")
        
        # 不要なサブスロットの確認
        for key in actual_slots:
            if key.startswith('sub-') and actual_slots[key]:
                issues.append(f"単文なのにサブスロット {key} に値 '{actual_slots[key]}' が入っている")
        
        if issues:
            print(f"  🚨 問題: {len(issues)}件")
            for issue in issues:
                print(f"    - {issue}")
            imperative_issues.extend(issues)
        else:
            print("  ✅ 問題なし")
        
        print()
    
    # Priority 16テスト実行
    print("📋 Priority 16 (ExistentialThereEngine) 問題確認")
    print("-" * 50)
    
    existential_issues = []
    
    for i, test_case in enumerate(existential_tests, 1):
        sentence = test_case['sentence']
        expected = test_case['expected']
        description = test_case['description']
        
        result = controller.process_sentence(sentence)
        
        # EngineResultオブジェクトのプロパティにアクセス
        selected_engines = [result.engine_type.name] if hasattr(result.engine_type, 'name') else [str(result.engine_type)]
        actual_slots = result.slots
        confidence = result.confidence
        
        print(f"Test {i}: {sentence} ({description})")
        print(f"  Selected: {selected_engines}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual_slots}")
        print(f"  Confidence: {confidence:.3f}")
        
        # 問題点の確認
        issues = []
        
        # エンジン選択の確認
        if 'EXISTENTIAL_THERE' not in [eng.upper() for eng in selected_engines]:
            issues.append(f"ExistentialThereEngineが選択されていない (選択: {selected_engines})")
        
        # スロット分解の確認
        for key, expected_value in expected.items():
            if key not in actual_slots:
                issues.append(f"スロット {key} が不足 (期待値: '{expected_value}')")
            elif actual_slots[key] != expected_value:
                # C1, C2は部分一致も許可
                if key in ['C1', 'C2'] and expected_value.lower() in actual_slots[key].lower():
                    continue
                issues.append(f"スロット {key} が不正 (期待: '{expected_value}', 実際: '{actual_slots[key]}')")
        
        # O1の誤用確認（存在文ではC1が正しい）
        if 'O1' in actual_slots and actual_slots['O1']:
            issues.append(f"存在文でO1に値 '{actual_slots['O1']}' が入っている（C1であるべき）")
        
        # 不要なサブスロットの確認
        for key in actual_slots:
            if key.startswith('sub-') and actual_slots[key]:
                issues.append(f"単文なのにサブスロット {key} に値 '{actual_slots[key]}' が入っている")
        
        if issues:
            print(f"  🚨 問題: {len(issues)}件")
            for issue in issues:
                print(f"    - {issue}")
            existential_issues.extend(issues)
        else:
            print("  ✅ 問題なし")
        
        print()
    
    # 総合結果
    total_issues = len(imperative_issues) + len(existential_issues)
    
    print("🏁 問題確認結果サマリー")
    print("=" * 60)
    print(f"📊 Priority 15 (ImperativeEngine): {len(imperative_issues)}件の問題")
    print(f"📊 Priority 16 (ExistentialThereEngine): {len(existential_issues)}件の問題")
    print(f"🎯 総合: {total_issues}件の問題")
    
    if total_issues > 0:
        print("\n🚨 確認された主要な問題:")
        all_issues = imperative_issues + existential_issues
        # 問題の種類別集計
        issue_types = {}
        for issue in all_issues:
            if "エンジンが選択されていない" in issue:
                issue_types["エンジン選択エラー"] = issue_types.get("エンジン選択エラー", 0) + 1
            elif "サブスロット" in issue:
                issue_types["サブスロット誤用"] = issue_types.get("サブスロット誤用", 0) + 1
            elif "O1に値" in issue:
                issue_types["O1/C1混同"] = issue_types.get("O1/C1混同", 0) + 1
            elif "スロット" in issue and "不足" in issue:
                issue_types["必要スロット不足"] = issue_types.get("必要スロット不足", 0) + 1
            elif "スロット" in issue and "不正" in issue:
                issue_types["スロット値不正"] = issue_types.get("スロット値不正", 0) + 1
        
        for issue_type, count in issue_types.items():
            print(f"  - {issue_type}: {count}件")
        
        print(f"\n💡 Priority 15・16エンジンには修正が必要です。")
        return True
    else:
        print(f"\n🎉 Priority 15・16エンジンに問題は見つかりませんでした！")
        return False

if __name__ == "__main__":
    has_issues = test_priority_15_16_issues()
    
    if has_issues:
        print("\n🔧 修正推奨アクション:")
        print("1. ImperativeEngineでサブスロット使用を削除")
        print("2. ExistentialThereEngineでO1→C1修正、サブスロット削除")
        print("3. 各エンジンの選択条件を調整")
    else:
        print("\n✅ 両エンジンとも正常に動作しています。")
