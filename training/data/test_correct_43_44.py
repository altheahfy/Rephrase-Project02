#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# ログレベルを上げて出力を抑制
logging.getLogger('unified_stanza_rephrase_mapper.UnifiedMapper').setLevel(logging.WARNING)

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # 正しいCase 43と44の文章
    test_cases = {
        '43': {
            'sentence': 'The building is being constructed very carefully by skilled workers.',
            'expected_M1': 'very',
            'expected_M2': 'very carefully', 
            'expected_M3': 'by skilled workers'
        },
        '44': {
            'sentence': 'The teacher explains grammar clearly to confused students daily.',
            'expected_M1': 'clearly',
            'expected_M2': 'to confused students',
            'expected_M3': 'daily'
        }
    }
    
    for case_id, case_data in test_cases.items():
        sentence = case_data['sentence']
        print(f"🧪 Case {case_id}: {sentence}")
        
        try:
            result = mapper.process(sentence)
            actual_slots = result.get('slots', {})
            
            actual_M1 = actual_slots.get('M1', '')
            actual_M2 = actual_slots.get('M2', '')
            actual_M3 = actual_slots.get('M3', '')
            
            expected_M1 = case_data['expected_M1']
            expected_M2 = case_data['expected_M2']
            expected_M3 = case_data['expected_M3']
            
            print(f"  実際: M1='{actual_M1}', M2='{actual_M2}', M3='{actual_M3}'")
            print(f"  期待: M1='{expected_M1}', M2='{expected_M2}', M3='{expected_M3}'")
            
            # 一致チェック
            M1_match = str(actual_M1) == str(expected_M1)
            M2_match = str(actual_M2) == str(expected_M2)
            M3_match = str(actual_M3) == str(expected_M3)
            
            if M1_match and M2_match and M3_match:
                print("   ✅ 完全一致")
            else:
                print("   ⚠️  不一致:")
                if not M1_match: print(f"     M1: '{actual_M1}' ≠ '{expected_M1}'")
                if not M2_match: print(f"     M2: '{actual_M2}' ≠ '{expected_M2}'") 
                if not M3_match: print(f"     M3: '{actual_M3}' ≠ '{expected_M3}'")
            
        except Exception as e:
            print(f"   ❌ エラー: {e}")
        
        print()

if __name__ == "__main__":
    main()
