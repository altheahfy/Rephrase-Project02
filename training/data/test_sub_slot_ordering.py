#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController
from ui_format_converter import UIFormatConverter

def test_sub_slot_ordering():
    """サブスロット順序付けシステムの統合テスト"""
    
    controller = CentralController()
    converter = UIFormatConverter()
    
    test_cases = [
        ("Case 43", "The man who runs fast is strong."),
        ("Case 121", "I know that he is smart.")
    ]
    
    for case_name, sentence in test_cases:
        print(f"\n{'='*50}")
        print(f"🎯 {case_name}: {sentence}")
        print(f"{'='*50}")
        
        # Central Controller処理
        result = controller.process_sentence(sentence)
        print(f"🔧 処理結果:")
        print(f"  main_slots: {result.get('main_slots', {})}")
        print(f"  sub_slots: {result.get('sub_slots', {})}")
        print(f"  ordered_sub_slots: {result.get('ordered_sub_slots', {})}")
        
        # UI変換
        ui_items = converter.convert_to_ui_format(
            controller_result=result,
            syntax_id="test",
            sentence_id="test"
        )
        
        print(f"🎨 UI変換結果:")
        for item in ui_items:
            if item.get('SubslotID'):  # サブスロットエントリのみ表示
                print(f"  {item['display_order']}. {item['SubslotID']}: '{item['SubslotElement']}'")

if __name__ == "__main__":
    test_sub_slot_ordering()
