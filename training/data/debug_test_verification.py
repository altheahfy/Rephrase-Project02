#!/usr/bin/env python3
"""
テスト検証ロジックの詳細調査
「The car is red.」の実際の出力とテスト期待値の比較
"""
from dynamic_grammar_mapper import DynamicGrammarMapper
import json

def debug_test_verification():
    """テスト検証ロジックの詳細調査"""
    
    mapper = DynamicGrammarMapper()
    sentence = "The car is red."
    
    print("=== テスト検証ロジック詳細調査 ===")
    print(f"対象文: {sentence}\n")
    
    # 実際の解析結果
    result = mapper.analyze_sentence(sentence)
    
    print("📊 実際の解析結果（完全版）:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # テストデータの期待値を確認
    print(f"\n📋 テストデータ確認:")
    
    try:
        with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        # Test 1を探す
        test_1_data = None
        for test_id, test_case in test_data.get("data", {}).items():
            if test_case.get("sentence") == sentence:
                test_1_data = test_case
                break
        
        if test_1_data:
            print(f"   テストID: {test_id}")
            print(f"   期待値:")
            print(json.dumps(test_1_data.get("expected", {}), indent=2, ensure_ascii=False))
        else:
            print("   該当するテストケースが見つかりません")
            
    except FileNotFoundError:
        print("   テストデータファイルが見つかりません")
    
    # Slotフィールドの詳細分析
    print(f"\n🔍 Slotフィールド詳細分析:")
    slots = result.get('Slot', [])
    print(f"   Slot配列: {slots}")
    
    # メインスロット情報の確認
    if 'main_slots' in result:
        print(f"\n📋 main_slots詳細:")
        main_slots = result['main_slots']
        for slot_name, slot_data in main_slots.items():
            print(f"   {slot_name}: {slot_data}")
    
    # 出力形式の問題を特定
    print(f"\n❓ 問題特定:")
    print("1. 内部認識は正常（C1: red 認識済み）")
    print("2. テスト結果で「C1: なし」と表示される")
    print("3. 出力形式変換またはテスト検証ロジックに問題の可能性")

if __name__ == "__main__":
    debug_test_verification()
