#!/usr/bin/env python3
"""
テスト32の詳細確認
"""
import sys
import json
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_32_specific():
    """テスト32の詳細分析"""
    
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    mapper = UnifiedStanzaRephraseMapper()
    
    print(f"📝 テスト32: {sentence}")
    print("=" * 60)
    
    # ハンドラーを追加
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause') 
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    mapper.add_handler('auxiliary_complex')
    
    result = mapper.process(sentence)
    
    print("📊 システム出力:")
    slots = result.get('slots', {})
    sub_slots = result.get('sub_slots', {})
    
    all_slots = {**slots, **sub_slots}
    for k, v in all_slots.items():
        if v:
            print(f"   {k}: {v}")
    
    print("\n📋 期待値:")
    expected = {
        "V": "runs", "M1": "smoothly",
        "sub-s": "The car that", "sub-v": "repaired", "sub-aux": "was",
        "sub-m1": "quickly", "sub-m2": "yesterday"
    }
    for k, v in expected.items():
        print(f"   {k}: {v}")
    
    print("\n❌ 問題分析:")
    # 副詞のスロット配置チェック
    result_adverbs = {}
    for k, v in all_slots.items():
        if k.startswith(('M', 'sub-m')) and v:
            result_adverbs[k] = v
    
    expected_adverbs = {k: v for k, v in expected.items() if k.startswith(('M', 'sub-m'))}
    
    print(f"システム副詞: {result_adverbs}")
    print(f"期待副詞: {expected_adverbs}")
    
    # 重複チェック
    for slot, value in result_adverbs.items():
        for other_slot, other_value in result_adverbs.items():
            if slot != other_slot and value.strip() in other_value.strip():
                print(f"🔴 重複検出: {slot}='{value}' が {other_slot}='{other_value}' に含まれている")

if __name__ == "__main__":
    test_32_specific()
