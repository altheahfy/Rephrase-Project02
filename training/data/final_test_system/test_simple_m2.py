#!/usr/bin/env python3
"""
シンプルなM2配置テスト
"""

import os
import sys

# プロジェクトルートパスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_simple_m2():
    mapper = UnifiedStanzaRephraseMapper()
    
    # ハンドラーを明示的に追加
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('adverbial_modifier')
    
    # シンプルな副詞文
    test_sentence = "She works carefully."
    
    print(f"📝 テスト: {test_sentence}")
    
    result = mapper.process(test_sentence)
    slots = result.get('slots', {})
    
    print(f"   システム出力: {slots}")
    
    # M2に配置されているか確認
    if 'M2' in slots and 'carefully' in slots['M2']:
        print("   ✅ M2優先配置成功")
    else:
        print("   ❌ M2配置失敗")

if __name__ == "__main__":
    test_simple_m2()
