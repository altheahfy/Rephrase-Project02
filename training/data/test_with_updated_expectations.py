#!/usr/bin/env python3
"""
修正されたfinal_54_test_data.jsonで完全テストを実行
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import json
from pathlib import Path

def run_full_test():
    """修正された期待値で完全テストを実行"""
    
    print("🧪 修正された期待値での完全テスト実行")
    print("=" * 60)
    
    # テストデータ読み込み
    test_file = Path("final_test_system/final_54_test_data.json")
    if not test_file.exists():
        print(f"❌ エラー: {test_file} が見つかりません")
        return
    
    with open(test_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    mapper = DynamicGrammarMapper()
    
    # 結果統計
    total_tests = 0
    perfect_matches = 0
    main_slot_matches = 0
    sub_slot_matches = 0
    errors = 0
    
    print(f"📊 総テスト数: {len(test_data['data'])}件\n")
    
    for test_id, test_case in test_data["data"].items():
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        total_tests += 1
        print(f"テスト {test_id}: {sentence}")
        
        try:
            result = mapper.analyze_sentence(sentence)
            actual_main = result.get("main_slots", {})
            actual_sub = result.get("sub_slots", {})
            
            expected_main = expected["main_slots"]
            expected_sub = expected["sub_slots"]
            
            # メインスロット比較
            main_match = actual_main == expected_main
            if main_match:
                main_slot_matches += 1
            
            # サブスロット比較
            sub_match = actual_sub == expected_sub
            if sub_match:
                sub_slot_matches += 1
            
            # 完全一致判定
            perfect_match = main_match and sub_match
            if perfect_match:
                perfect_matches += 1
                print("   ✅ 完全一致")
            else:
                print("   ❌ 不一致")
                if not main_match:
                    print(f"     メイン期待: {expected_main}")
                    print(f"     メイン実際: {actual_main}")
                if not sub_match:
                    print(f"     サブ期待: {expected_sub}")
                    print(f"     サブ実際: {actual_sub}")
        
        except Exception as e:
            errors += 1
            print(f"   💥 エラー: {e}")
        
        print("-" * 50)
    
    # 最終統計
    print(f"📊 最終結果:")
    print(f"   総テスト数: {total_tests}")
    print(f"   完全一致: {perfect_matches} ({perfect_matches/total_tests*100:.1f}%)")
    print(f"   メインスロット一致: {main_slot_matches} ({main_slot_matches/total_tests*100:.1f}%)")
    print(f"   サブスロット一致: {sub_slot_matches} ({sub_slot_matches/total_tests*100:.1f}%)")
    print(f"   エラー: {errors}")
    
    return {
        "total": total_tests,
        "perfect": perfect_matches,
        "main_matches": main_slot_matches,
        "sub_matches": sub_slot_matches,
        "errors": errors,
        "accuracy": perfect_matches/total_tests*100 if total_tests > 0 else 0
    }

if __name__ == "__main__":
    run_full_test()
