#!/usr/bin/env python3
"""
SVOC文型のC2補語認識問題を詳細調査
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import json

def debug_svoc_pattern():
    """SVOC文型の詳細解析"""
    mapper = DynamicGrammarMapper()
    
    # SVOC文型のテストケース
    test_cases = [
        "We call him Tom.",
        "I found it interesting.", 
        "They made her happy."
    ]
    
    print("=== SVOC文型 C2補語認識問題調査 ===\n")
    
    for sentence in test_cases:
        print(f"📝 分析対象: {sentence}")
        
        result = mapper.analyze_sentence(sentence)
        
        print(f"🔍 認識された文型: {result.get('pattern_detected', 'UNKNOWN')}")
        print(f"📊 Slot配列: {result.get('Slot', [])}")
        print(f"📋 SlotPhrase配列: {result.get('SlotPhrase', [])}")
        
        main_slots = result.get('main_slots', {})
        print(f"🎯 main_slots:")
        for slot, phrase in main_slots.items():
            print(f"   {slot}: {phrase}")
        
        # 期待されるC2を確認
        expected_c2 = {
            "We call him Tom.": "Tom",
            "I found it interesting.": "interesting", 
            "They made her happy.": "happy"
        }
        
        expected = expected_c2.get(sentence, "")
        actual_c2 = main_slots.get('C2', '')
        
        print(f"❓ C2補語認識:")
        print(f"   期待値: '{expected}'")
        print(f"   実際値: '{actual_c2}'")
        
        if actual_c2 == expected:
            print("   ✅ 正常認識")
        else:
            print("   ❌ 認識失敗")
        
        print("-" * 60)

if __name__ == "__main__":
    debug_svoc_pattern()
