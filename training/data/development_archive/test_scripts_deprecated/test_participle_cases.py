#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを上げて出力を抑制
logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.WARNING)

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # 失敗していた4ケースをテスト
    failed_cases = {
        '49': 'The team working overtime completed the project successfully yesterday.',
        '50': 'The woman standing quietly near the door was waiting patiently.',
        '51': 'The children playing happily in the garden were supervised carefully.',
        '52': 'The documents being reviewed thoroughly will be approved soon.'
    }
    
    print("🎯 失敗4ケースの分詞構文ハンドラーテスト")
    print("=" * 60)
    
    for case_id, sentence in failed_cases.items():
        print(f"Case {case_id}: {sentence}")
        
        try:
            result = mapper.process(sentence)
            
            # 結果表示
            main_slots = result.get('slots', {})
            sub_slots = result.get('sub_slots', {})
            
            print("  Main slots:")
            for key, value in main_slots.items():
                print(f"    {key}: '{value}'")
            
            print("  Sub slots:")
            for key, value in sub_slots.items():
                print(f"    {key}: '{value}'")
            
            print("  ✅ 処理完了")
            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
        
        print()

if __name__ == "__main__":
    main()
