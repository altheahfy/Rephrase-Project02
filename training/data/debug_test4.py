#!/usr/bin/env python3
"""テスト4の主文欠落問題デバッグ"""

import logging

# デバッグログを有効化
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s'
)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_test4():
    """テスト4: The book which lies there is mine. の詳細デバッグ"""
    
    print("=" * 60)
    print("🔍 テスト4デバッグ: The book which lies there is mine.")
    print("=" * 60)
    
    mapper = UnifiedStanzaRephraseMapper()
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    
    # 処理実行
    result = mapper.process('The book which lies there is mine.')
    
    print("\n📊 最終結果:")
    slots = result.get('slots', {})
    sub_slots = result.get('sub_slots', {})
    
    print("上位スロット:")
    for key, value in slots.items():
        print(f"  {key:<4}: '{value}'")
    
    print("サブスロット:")  
    for key, value in sub_slots.items():
        print(f"  {key:<8}: '{value}'")
    
    # 期待値との比較
    print("\n🎯 期待値との比較:")
    expected_main = {
        'S': '',  # サブスロットにある
        'V': 'is',
        'C1': 'mine'
    }
    
    for key, expected in expected_main.items():
        actual = slots.get(key, 'なし')
        status = "✅" if actual == expected else "❌"
        print(f"  {key:<4}: 期待='{expected}' 実際='{actual}' {status}")

if __name__ == "__main__":
    debug_test4()
