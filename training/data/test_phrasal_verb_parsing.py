#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
チェック6: 「句動詞down」M2スロット確認テスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_phrasal_verb_down():
    """句動詞downのテスト例文"""
    test_sentences = [
        "Please write down the address.",      # 例文1: write down（書き留める）
        "I need to calm down quickly.",       # 例文2: calm down（落ち着く）
        "She broke down the data.",           # 例文3: break down（分析する）
        "They shut down the system.",         # 例文4: shut down（停止する）
    ]
    
    parser = CompleteRephraseParsingEngine()
    
    print("=== チェック6: 「句動詞down」M2スロット確認テスト ===\n")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 例文{i:02d}: '{sentence}'")
        
        # 解析実行
        result = parser.analyze_sentence(sentence)
        
        if result:
            # slotsフィールドからM2スロットを取得
            m2_slots = result.get('slots', {}).get('M2', [])
            
            # down確認（M2スロット内でdown値を探す）
            down_found = False
            for slot in m2_slots:
                if isinstance(slot, dict) and 'value' in slot:
                    if 'down' in slot['value'].lower():
                        down_found = True
                        break
            
            print(f"  🔍 M2スロット: {m2_slots}")
            
            if down_found:
                print(f"  ✅ 「down」がM2に正しく記録されています")
            else:
                print(f"  ❌ 「down」がM2に記録されていません")
                
        else:
            print(f"  ❌ 解析エラー")
        
        print()

if __name__ == "__main__":
    test_phrasal_verb_down()
