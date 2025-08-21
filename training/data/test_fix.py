#!/usr/bin/env python3
"""修正されたハンドラー通信システムのテスト"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_relative_clause_fix():
    """関係節処理修正のテスト"""
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    # 問題のテストケース
    test_sentence = "The man whose car is red lives here."
    print(f"テスト文: {test_sentence}")
    
    # 分解実行
    result = mapper.process(test_sentence)
    
    if result and 'slots' in result:
        slots = result['slots']
        s_slot = slots.get('S', '')
        v_slot = slots.get('V', '')
        c1_slot = slots.get('C1', '')
        c2_slot = slots.get('C2', '')
        
        print(f'結果: S="{s_slot}" V="{v_slot}" C1="{c1_slot}" C2="{c2_slot}"')
        
        # 期待値と比較
        expected_s = ""
        expected_v = "lives"
        expected_c2 = "here"
        
        print(f"\n期待値: S=\"{expected_s}\" V=\"{expected_v}\" C2=\"{expected_c2}\"")
        
        if s_slot == expected_s and v_slot == expected_v and c2_slot == expected_c2:
            print("✅ テスト成功！修正が正しく動作しています")
            return True
        else:
            print("❌ テスト失敗")
            return False
    else:
        print("❌ 結果なし - エラー")
        return False

if __name__ == "__main__":
    test_relative_clause_fix()
