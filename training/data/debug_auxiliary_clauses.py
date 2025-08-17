"""
助動詞節レベル分離テスト
"""

import sys
sys.path.append('.')

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_auxiliary_clause_separation():
    """助動詞の節レベル分離テスト"""
    print("🧪 助動詞節レベル分離テスト開始")
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # 🚨 重要: ハンドラー追加
    mapper.add_handler('auxiliary_complex')
    
    # テストケース
    test_cases = [
        ("The car is red.", "連結詞は助動詞ではない"),
        ("The car is being repaired.", "複合助動詞 is being"),
        ("The car which was crashed is red.", "節分離: 主節is, 従属節was"),
        ("He has finished his homework.", "完了助動詞 has")
    ]
    
    for sentence, description in test_cases:
        print(f"\n🔍 テスト: {sentence}")
        print(f"   説明: {description}")
        
        result = mapper.process(sentence)
        
        # デバッグ情報表示
        print(f"   🔍 Raw result: {result}")
        
        # 結果表示
        slots = result.get('slots', {})
        sub_slots = result.get('sub_slots', {})
        
        print(f"   全スロット: {slots}")
        print(f"   全サブスロット: {sub_slots}")
        
        # 助動詞情報のみ抽出
        aux_info = {k: v for k, v in slots.items() if 'Aux' in k or 'aux' in k}
        sub_aux_info = {k: v for k, v in sub_slots.items() if 'aux' in k}
        
        print(f"   主節助動詞: {aux_info}")
        print(f"   従属節助動詞: {sub_aux_info}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_auxiliary_clause_separation()
