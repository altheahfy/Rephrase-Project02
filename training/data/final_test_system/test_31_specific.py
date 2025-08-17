#!/usr/bin/env python3
"""
テスト31の具体的な実行結果確認
"""
import sys
import json
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_31_specific():
    """テスト31の詳細分析"""
    
    sentence = "The book which was carefully written by Shakespeare is famous."
    mapper = UnifiedStanzaRephraseMapper()
    
    print(f"📝 テスト31: {sentence}")
    print("=" * 60)
    
    # ハンドラーを追加
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause') 
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    mapper.add_handler('auxiliary_complex')
    
    result = mapper.process(sentence)
    
    print("📊 システム出力:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n📋 期待値:")
    expected = {
        "V": "is", "C1": "famous",
        "sub-s": "The book which", "sub-v": "written", "sub-aux": "was",
        "sub-m1": "carefully", "sub-m2": "by Shakespeare"
    }
    print(json.dumps(expected, indent=2, ensure_ascii=False))
    
    print("\n❌ 問題分析:")
    # 実際の結果から副詞をチェック
    result_slots = result.get('slots', {})
    result_adverbs = {k: v for k, v in result_slots.items() if k.startswith(('M', 'sub-m')) and v}
    expected_adverbs = {k: v for k, v in expected.items() if k.startswith(('M', 'sub-m'))}
    
    print(f"システム副詞: {result_adverbs}")
    print(f"期待副詞: {expected_adverbs}")
    
    # 重複問題をチェック
    for slot, value in result_adverbs.items():
        for other_slot, other_value in result_adverbs.items():
            if slot != other_slot and value.strip() in other_value.strip():
                print(f"🔴 重複検出: {slot}='{value}' が {other_slot}='{other_value}' に含まれている")

if __name__ == "__main__":
    test_31_specific()
