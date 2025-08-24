#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央制御機構テスト用スクリプト
Test 9のみ実行して中央制御機構の効果を確認
"""

import json
from dynamic_grammar_mapper import DynamicGrammarMapper

def test_central_controller():
    """中央制御機構のテスト"""
    
    # テストケース 9
    test_sentence = "The car which was crashed is red."
    expected_main = {'S': '', 'V': 'is', 'C1': 'red'}
    expected_sub = {'sub-s': 'The car which', 'sub-aux': 'was', 'sub-v': 'crashed', '_parent_slot': 'S'}
    
    # 1. 従来システムでのテスト
    print("=== 従来システム実行 ===")
    mapper_legacy = DynamicGrammarMapper()
    result_legacy = mapper_legacy.analyze_sentence(test_sentence)
    
    print(f"従来システム結果:")
    print(f"  main_slots: {result_legacy.get('main_slots', {})}")
    print(f"  sub_slots: {result_legacy.get('sub_slots', {})}")
    
    # 2. 中央制御機構でのテスト
    print("\n=== 中央制御機構実行 ===")
    mapper_central = DynamicGrammarMapper()
    
    # 中央制御機構を有効化
    success = mapper_central.enable_central_controller()
    print(f"中央制御機構有効化: {'成功' if success else '失敗'}")
    
    if success:
        result_central = mapper_central.analyze_sentence(test_sentence)
        
        print(f"中央制御機構結果:")
        print(f"  main_slots: {result_central.get('main_slots', {})}")
        print(f"  sub_slots: {result_central.get('sub_slots', {})}")
        
        # 3. 結果比較
        print("\n=== 結果比較 ===")
        print(f"期待値main: {expected_main}")
        print(f"期待値sub:  {expected_sub}")
        
        main_match_legacy = result_legacy.get('main_slots', {}) == expected_main
        sub_match_legacy = result_legacy.get('sub_slots', {}) == expected_sub
        
        main_match_central = result_central.get('main_slots', {}) == expected_main
        sub_match_central = result_central.get('sub_slots', {}) == expected_sub
        
        print(f"\n従来システム: main={main_match_legacy}, sub={sub_match_legacy}")
        print(f"中央制御機構: main={main_match_central}, sub={sub_match_central}")
        
        if main_match_central and sub_match_central:
            print("🎉 中央制御機構で正解！")
        elif main_match_legacy and sub_match_legacy:
            print("⚠️ 従来システムでも正解（中央制御機構の改善効果なし）")
        else:
            print("❌ 両システムとも不正解")
    
    else:
        print("❌ 中央制御機構の有効化に失敗")

if __name__ == "__main__":
    test_central_controller()
