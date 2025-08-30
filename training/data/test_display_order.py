#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIFormatConverter順序テスト
"""

from central_controller import CentralController
from ui_format_converter import UIFormatConverter

def test_display_order():
    controller = CentralController()
    converter = UIFormatConverter()
    
    text = "The woman who seemed indecisive finally made a decision."
    result = controller.process_sentence(text)
    
    print(f"テスト文: {text}")
    print(f"CentralController Ordered Slots: {result['ordered_slots']}")
    print()
    
    ui_data = converter.convert_to_ui_format(result)
    print("UI Items with display orders:")
    for item in ui_data:
        slot = item['Slot']
        phrase = item.get('SlotPhrase', '')
        display_order = item.get('Slot_display_order', '')
        print(f'  {slot}: "{phrase}" → Order: {display_order}')
    
    print("\n期待される順序:")
    print("  S (関係節): Order 1 ← 現在4になっている問題")
    print("  M2 (finally): Order 2 ← 正しい")
    print("  V (made): Order 3 ← 正しい") 
    print("  O1 (a decision): Order 4 ← 正しい")

if __name__ == "__main__":
    test_display_order()
