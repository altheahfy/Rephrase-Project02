#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
デバッグ用: 特定ケース詳細分析
"""

import json
import sys
import spacy
from central_controller import CentralController

def debug_case(case_id):
    """特定ケースの詳細デバッグ"""
    
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_case = data['data'].get(str(case_id))
    if not test_case:
        print(f"❌ ケース{case_id}が見つかりません")
        return
    
    sentence = test_case['sentence']
    expected = test_case['expected']['main_slots']
    
    print(f"🔍 ケース{case_id}詳細分析")
    print(f"📝 入力文: {sentence}")
    print(f"📋 期待値: {expected}")
    print("=" * 50)
    
    # spaCy分析
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    print("📊 spaCy POS分析:")
    for token in doc:
        print(f"  {token.text:>8} | {token.pos_:>8} | {token.tag_:>12} | {token.lemma_}")
    print()
    
    # Central Controller分析
    controller = CentralController()
    
    # 直接HandlerをDebugモードで実行
    from basic_five_pattern_handler import BasicFivePatternHandler
    handler = BasicFivePatternHandler()
    
    print("🔧 Handler直接実行:")
    handler_result = handler.process(sentence)
    print(f"Handler結果: {handler_result}")
    print()
    
    try:
        result = controller.process_sentence(sentence)
        print(f"🎯 処理結果:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        print()
        
        # スロット結果の詳細確認
        slots = result.get('slots', {})
        print(f"📊 実際のスロット:")
        for key, value in slots.items():
            print(f"  {key}: {value}")
        print()
        
        # 詳細比較
        print("🔍 詳細比較:")
        for slot, expected_value in expected.items():
            actual_value = slots.get(slot)
            if actual_value == expected_value:
                print(f"  ✅ {slot}: {actual_value}")
            else:
                print(f"  ❌ {slot}: 期待={expected_value} / 実際={actual_value}")
                
    except Exception as e:
        print(f"❌ 処理エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用法: python debug_specific.py case_id")
        sys.exit(1)
    
    case_id = int(sys.argv[1])
    debug_case(case_id)
