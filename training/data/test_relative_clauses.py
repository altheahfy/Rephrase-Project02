#!/usr/bin/env python3
"""
関係節例文テスト
"""

from ui_format_converter import UIFormatConverter
from central_controller import CentralController
import json

def test_relative_clauses():
    """関係節例文のテスト"""
    controller = CentralController()
    converter = UIFormatConverter()
    
    # テスト例文
    test_sentences = [
        "The man who runs fast is strong.",
        "The book which I read yesterday was interesting.",
        "The woman who seemed indecisive finally made a decision."
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{'='*60}")
        print(f"テスト {i}: {sentence}")
        print('='*60)
        
        # CentralController処理
        result = controller.process_sentence(sentence)
        
        print("\n📊 CentralController出力:")
        print("main_slots:", result.get("main_slots", {}))
        print("sub_slots:", result.get("sub_slots", {}))
        print("ordered_slots:", result.get("ordered_slots", {}))
        
        # UI形式変換
        ui_items = converter.convert_to_ui_format(result, f'rel_test_{i}')
        
        # ファイル保存
        output_file = f'relative_clause_test_{i}.json'
        converter.save_ui_format(ui_items, output_file)
        
        print("\n🎯 UI変換結果:")
        for item in ui_items:
            slot = item["Slot"]
            phrase = item["SlotPhrase"]
            subslot_id = item["SubslotID"]
            subslot_element = item["SubslotElement"]
            slot_order = item["Slot_display_order"]
            display_order = item["display_order"]
            phrase_type = item["PhraseType"]
            
            if subslot_id:  # サブスロットエントリ
                print(f"  └─ {slot}[{subslot_id}]: {subslot_element} (順序{slot_order}.{display_order})")
            else:  # 上位スロットエントリ
                print(f"  順序{slot_order}: Slot={slot:<3} Phrase=\"{phrase:<20}\" Type={phrase_type}")
        
        # サブスロット情報の確認
        print("\n🔍 サブスロット情報:")
        sub_slots = result.get("sub_slots", {})
        for sub_key, sub_value in sub_slots.items():
            if sub_key != '_parent_slot':
                print(f"  {sub_key}: {sub_value}")

if __name__ == "__main__":
    test_relative_clauses()
