#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excelデータ準拠テスト - Rephraseルール検証
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_excel_compliance():
    print("=== Excelデータ準拠テスト ===\n")
    
    engine = CompleteRephraseParsingEngine()
    
    # テストケース1: Excelから確認した関係詞節の例
    test_cases = [
        {
            'sentence': 'The manager who had recently taken charge of the project had to make decisions.',
            'expected_main_s': 'the manager who had recently taken charge of the project',
            'expected_subslots': [
                ('sub-s', 'the manager who'),
                ('sub-aux', 'had'),  
                ('sub-m2', 'recently'),
                ('sub-v', 'taken'),
                ('sub-o1', 'charge of the project')
            ]
        },
        {
            'sentence': 'The boy who plays soccer is my friend.',
            'expected_main_s': 'the boy who plays soccer',
            'expected_subslots': [
                ('sub-s', 'the boy who'),
                ('sub-v', 'plays'),
                ('sub-o1', 'soccer')
            ]
        },
        {
            'sentence': 'The book that I bought yesterday is interesting.',
            'expected_main_s': 'the book that I bought yesterday',
            'expected_subslots': [
                ('sub-o1', 'the book that'),  # 関係代名詞目的語
                ('sub-s', 'I'),
                ('sub-v', 'bought'),
                ('sub-m3', 'yesterday')
            ]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"=== テストケース{i}: {test_case['sentence']} ===")
        
        result = engine.analyze_sentence(test_case['sentence'])
        slots = result.get('rephrase_slots', {})
        
        # メインスロットの確認
        main_s = slots.get('S', [])
        main_s_text = main_s[0] if main_s else ''
        
        print(f"期待するメインS: {test_case['expected_main_s']}")
        print(f"実際のメインS: {main_s_text}")
        print(f"\n結果の全キー: {list(result.keys())}")
        print(f"slotsの全キー: {list(slots.keys()) if slots else 'スロットなし'}")
        if 'sub_slots' in result:
            print(f"sub_slotsの全キー: {list(result['sub_slots'].keys())}")
        
        if test_case['expected_main_s'].lower() in main_s_text.lower():
            print("✅ メインスロットS: 関係詞節込みの完全な名詞句が正しく配置")
        else:
            print("❌ メインスロットS: 期待される構造と異なる")
        
        # サブスロットの確認
        print("\n期待するサブスロット構造:")
        for slot_type, expected_value in test_case['expected_subslots']:
            print(f"  {slot_type}: {expected_value}")
        
        print("\n実際のサブスロット:")
        sub_slots = result.get('sub_slots', {})
        sub_structures = result.get('sub_structures', {})
        
        if sub_slots:
            print("  sub_slotsから:")
            for slot_type, slot_values in sub_slots.items():
                if slot_values:
                    for value in slot_values:
                        if isinstance(value, dict):
                            print(f"    {slot_type}: {value.get('value', value)}")
                        else:
                            print(f"    {slot_type}: {value}")
                            
        if sub_structures:
            print("  sub_structuresから:")
            for key, value in sub_structures.items():
                print(f"    {key}: {value}")
                
        if not sub_slots and not sub_structures:
            print("  サブスロットデータが見つかりません")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_excel_compliance()
