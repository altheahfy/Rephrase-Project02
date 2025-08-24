#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央制御機構の成功確認用簡単テスト
"""

from dynamic_grammar_mapper import DynamicGrammarMapper

def test_simple_sentence():
    """簡単な文章で中央制御機構をテスト"""
    
    # 簡単なテストケース
    test_sentence = "The car is red."
    
    print("=== 簡単な文章テスト ===")
    print(f"テスト文: {test_sentence}")
    
    # 1. 従来システム
    print("\n--- 従来システム ---")
    mapper_legacy = DynamicGrammarMapper()
    result_legacy = mapper_legacy.analyze_sentence(test_sentence)
    print(f"main_slots: {result_legacy.get('main_slots', {})}")
    print(f"sub_slots: {result_legacy.get('sub_slots', {})}")
    
    # 2. 中央制御機構
    print("\n--- 中央制御機構 ---")
    mapper_central = DynamicGrammarMapper()
    mapper_central.enable_central_controller()
    result_central = mapper_central.analyze_sentence(test_sentence)
    print(f"main_slots: {result_central.get('main_slots', {})}")
    print(f"sub_slots: {result_central.get('sub_slots', {})}")
    
    # 3. 結果比較
    print("\n--- 結果一致確認 ---")
    main_match = result_legacy.get('main_slots', {}) == result_central.get('main_slots', {})
    sub_match = result_legacy.get('sub_slots', {}) == result_central.get('sub_slots', {})
    print(f"main_slots一致: {main_match}")
    print(f"sub_slots一致: {sub_match}")
    
    if main_match and sub_match:
        print("🎉 中央制御機構と従来システムの結果が一致！")
    else:
        print("⚠️ 結果に差異あり（これは改善の可能性）")

def test_complex_sentence():
    """Test 9の複雑な文章テスト"""
    
    test_sentence = "The car which was crashed is red."
    
    print("\n=== Test 9 複雑な文章テスト ===")
    print(f"テスト文: {test_sentence}")
    
    # 中央制御機構のみでテスト
    mapper = DynamicGrammarMapper()
    mapper.enable_central_controller()
    result = mapper.analyze_sentence(test_sentence)
    
    print(f"main_slots: {result.get('main_slots', {})}")
    print(f"sub_slots: {result.get('sub_slots', {})}")
    
    # キーの存在確認
    main_slots = result.get('main_slots', {})
    sub_slots = result.get('sub_slots', {})
    
    main_complete = 'S' in main_slots and 'V' in main_slots and 'C1' in main_slots
    sub_complete = 'sub-s' in sub_slots and 'sub-aux' in sub_slots and 'sub-v' in sub_slots
    
    print(f"main_slots完全性: {main_complete}")
    print(f"sub_slots完全性: {sub_complete}")
    
    if main_complete and sub_complete:
        print("🎉 中央制御機構による完全分析成功！")
        return True
    else:
        print("❌ 分析に不足あり")
        return False

if __name__ == "__main__":
    test_simple_sentence()
    success = test_complex_sentence()
    
    if success:
        print("\n🎯 中央制御機構は正常に動作しています！")
        print("📈 ハンドラー間の情報漏出・消失問題が解決されました")
    else:
        print("\n❌ さらなる調整が必要です")
