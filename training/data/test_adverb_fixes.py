"""
副詞距離計算修正テスト
"""

import sys
sys.path.append('.')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_adverb_distance_fixes():
    """副詞距離計算修正テスト"""
    print("🧪 副詞距離計算修正テスト開始")
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # 全ハンドラー追加
    mapper.add_handler('auxiliary_complex')
    mapper.add_handler('adverbial_modifier')
    
    # 問題のあったテストケース
    test_cases = [
        ("The students study hard for exams.", "M1:hard, M2:for exams 期待"),
        ("The teacher explains grammar clearly to confused students daily.", "M1:clearly, M2:to confused students, M3:daily 期待"),
        ("The car was repaired last week.", "M2:last week 期待"),
        ("The problem was quickly solved by the expert team.", "M2:quickly, M3:by the expert team 期待")
    ]
    
    for sentence, expectation in test_cases:
        print(f"\n🔍 テスト: {sentence}")
        print(f"   期待: {expectation}")
        
        result = mapper.process(sentence)
        
        # M-slotのみ抽出
        slots = result.get('slots', {})
        m_slots = {k: v for k, v in slots.items() if k.startswith('M') and v}
        
        print(f"   結果: {m_slots}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_adverb_distance_fixes()
