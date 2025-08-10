#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
チェック5: 「文尾please」M3スロット確認テスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_please_sentences():
    """文尾pleaseのテスト例文"""
    test_sentences = [
        "Help me, please.",           # 例文1: 標準的な文尾please
        "Call her back, please.",     # 例文2: 句動詞+please
        "Come here quickly, please.", # 例文3: 副詞+please
        "Give it to him, please.",    # 例文4: SVOO+please
    ]
    
    parser = CompleteRephraseParsingEngine()
    
    print("=== チェック5: 「文尾please」M3スロット確認テスト ===\n")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 例文{i:02d}: '{sentence}'")
        
        # 解析実行
        result = parser.analyze_sentence(sentence)
        
        if result:  # analyze_sentenceは直接辞書を返す
            # slotsフィールドからM3スロットを取得
            m3_slots = result.get('slots', {}).get('M3', [])
            
            # please確認（M3スロット内でplease値を探す）
            please_found = False
            for slot in m3_slots:
                if isinstance(slot, dict) and 'value' in slot:
                    if 'please' in slot['value'].lower():
                        please_found = True
                        break
            
            print(f"  🔍 M3スロット: {m3_slots}")
            
            if please_found:
                print(f"  ✅ 「please」がM3に正しく記録されています")
            else:
                print(f"  ❌ 「please」がM3に記録されていません")
                
        else:
            print(f"  ❌ 解析エラー")
        
        print()

if __name__ == "__main__":
    test_please_sentences()
