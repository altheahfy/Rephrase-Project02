#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pure_stanza_engine_v2 import PureStanzaEngine

def test_o2_c1_examples():
    """O2/C1スロットを含む例文でテスト"""
    
    engine = PureStanzaEngine()
    
    test_cases = [
        {
            "name": "O2テスト (間接目的語)",
            "sentence": "I gave him the book.",
            "expected_slots": ["S", "V", "O2", "O1"],
            "description": "him=O2, the book=O1"
        },
        {
            "name": "C1テスト (述語補語)", 
            "sentence": "She is happy.",
            "expected_slots": ["S", "V", "C1"],
            "description": "happy=C1"
        },
        {
            "name": "C1テスト (名詞補語)",
            "sentence": "He became a teacher.",
            "expected_slots": ["S", "V", "C1"], 
            "description": "a teacher=C1"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"🧪 テスト{i}: {test_case['name']}")
        print(f"例文: {test_case['sentence']}")
        print(f"期待: {test_case['description']}")
        print('='*60)
        
        try:
            result = engine.decompose(test_case['sentence'])
            
            print(f"\n📊 検出されたスロット:")
            if result:
                for slot_name, slot_data in result.items():
                    if isinstance(slot_data, dict) and 'main' in slot_data:
                        print(f"  ✅ {slot_name}: \"{slot_data['main']}\"")
                    else:
                        print(f"  ✅ {slot_name}: \"{slot_data}\"")
            else:
                print("  ❌ スロット検出なし")
                
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_o2_c1_examples()
