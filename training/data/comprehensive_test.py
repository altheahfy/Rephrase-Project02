"""
包括的テスト実行スクリプト
実装済み機能（基本5文型、関係節、副詞、受動態）の正規テスト
"""

import sys
import os

# fast_test.pyをインポート
sys.path.append(os.path.dirname(__file__))
from fast_test import run_fast_test

def main():
    print("=== 実装済み機能 包括的テスト ===")
    
    # 基本5文型ケース（単文）
    basic_cases = [1, 2]  # "The car is red.", "I love you."
    print(f"\n🎯 基本5文型テスト (ケース {basic_cases})")
    for case in basic_cases:
        print(f"\nケース {case}:")
        result = run_fast_test([case])
        print(f"結果: {'✅ 成功' if result['success_rate'] == 100 else '❌ 失敗'}")
    
    # 関係節ケース（who, which, that, whose）
    relative_cases = [3, 4, 5, 6, 7, 8, 12, 13]  # 関係節の基本パターン
    print(f"\n🎯 関係節テスト (ケース {relative_cases})")
    for case in relative_cases:
        print(f"\nケース {case}:")
        result = run_fast_test([case])
        print(f"結果: {'✅ 成功' if result['success_rate'] == 100 else '❌ 失敗'}")
    
    # 関係節内受動態ケース
    relative_passive_cases = [9, 10, 11]  # "was crashed", "was written", "was sent"
    print(f"\n🎯 関係節内受動態テスト (ケース {relative_passive_cases})")
    for case in relative_passive_cases:
        print(f"\nケース {case}:")
        result = run_fast_test([case])
        print(f"結果: {'✅ 成功' if result['success_rate'] == 100 else '❌ 失敗'}")
    
    # 主節受動態ケース（Case 35）
    main_passive_cases = [35]  # "is respected greatly"
    print(f"\n🎯 主節受動態テスト (ケース {main_passive_cases})")
    for case in main_passive_cases:
        print(f"\nケース {case}:")
        result = run_fast_test([case])
        print(f"結果: {'✅ 成功' if result['success_rate'] == 100 else '❌ 失敗'}")
    
    # 副詞修飾語ケース
    adverb_cases = [3, 4, 5, 12, 35]  # "fast", "there", "here", "efficiently", "greatly"
    print(f"\n🎯 副詞修飾語テスト (ケース {adverb_cases})")
    result = run_fast_test(adverb_cases)
    print(f"副詞修飾語 成功率: {result['success_rate']:.1f}%")
    
    # 全機能統合テスト
    all_implemented_cases = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 35]
    print(f"\n🎯 全機能統合テスト (ケース {all_implemented_cases})")
    result = run_fast_test(all_implemented_cases)
    print(f"\n📊 最終結果:")
    print(f"全体成功率: {result['success_rate']:.1f}%")
    print(f"成功: {result['passed']}/{result['total']}")
    
    if result['failed_cases']:
        print(f"失敗ケース: {result['failed_cases']}")
    else:
        print("🎉 全ケース成功！")

if __name__ == "__main__":
    main()
