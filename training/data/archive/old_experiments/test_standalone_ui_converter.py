#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIFormatConverter単独テスト
"""

from ui_format_converter import UIFormatConverter
import json

def test_standalone_ui_converter():
    """UIFormatConverterの単独動作テスト"""
    
    print("🧪 UIFormatConverter単独動作テスト")
    print("=" * 50)
    
    converter = UIFormatConverter()
    
    # CentralControllerの出力形式をシミュレート
    sample_controller_result = {
        "success": True,
        "text": "I love you very much.",
        "main_slots": {
            "S": "I",
            "V": "love", 
            "O1": "you",
            "M2": "very much"
        },
        "sub_slots": {},
        "ordered_slots": {
            "1": "I",
            "2": "love", 
            "3": "you",
            "4": "very much"
        }
    }
    
    print(f"入力データ: {sample_controller_result}")
    print()
    
    # UIFormatConverterで変換
    ui_data = converter.convert_to_ui_format(
        controller_result=sample_controller_result,
        sentence_id="test001",
        syntax_id="basic"
    )
    
    print("✅ 変換成功!")
    print(f"生成されたUIアイテム数: {len(ui_data)}")
    print()
    
    print("📱 UI形式データ:")
    for i, item in enumerate(ui_data, 1):
        slot = item['Slot']
        phrase = item.get('SlotPhrase', '')
        order = item.get('Slot_display_order', '')
        phrase_type = item.get('PhraseType', '')
        print(f"  {i}. {slot}: '{phrase}' (Order: {order}, Type: {phrase_type})")
    
    # JSONファイルに出力
    output_file = "standalone_ui_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ui_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 出力ファイル: {output_file}")
    
    return ui_data

def test_complex_example():
    """より複雑な例での単独テスト"""
    
    print("\n" + "=" * 50)
    print("🔬 複雑な例でのテスト")
    print("=" * 50)
    
    converter = UIFormatConverter()
    
    # 関係節の例をシミュレート
    complex_result = {
        "success": True,
        "text": "The woman who seemed indecisive finally made a decision.",
        "main_slots": {
            "S": "",  # 空化されたスロット
            "V": "made",
            "O1": "a decision", 
            "M2": "finally"
        },
        "sub_slots": {
            "sub-s": "The woman who",
            "sub-v": "seemed",
            "sub-c1": "indecisive",
            "_parent_slot": "S"
        },
        "ordered_slots": {
            "1": "",  # Sスロット（空）
            "2": "finally",  # M2（動詞前）
            "3": "made",  # V
            "4": "a decision"  # O1
        }
    }
    
    print(f"入力データ（関係節）: {complex_result}")
    print()
    
    ui_data = converter.convert_to_ui_format(
        controller_result=complex_result,
        sentence_id="complex001"
    )
    
    print("✅ 関係節変換成功!")
    print(f"生成されたUIアイテム数: {len(ui_data)}")
    print()
    
    print("📱 関係節UI形式データ:")
    for i, item in enumerate(ui_data, 1):
        slot = item['Slot']
        phrase = item.get('SlotPhrase', '')
        order = item.get('Slot_display_order', '')
        phrase_type = item.get('PhraseType', '')
        print(f"  {i}. {slot}: '{phrase}' (Order: {order}, Type: {phrase_type})")
    
    # 複雑な例の出力
    complex_output_file = "complex_ui_output.json"
    with open(complex_output_file, 'w', encoding='utf-8') as f:
        json.dump(ui_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 複雑例出力ファイル: {complex_output_file}")
    
    return ui_data

if __name__ == "__main__":
    # 基本テスト
    basic_result = test_standalone_ui_converter()
    
    # 複雑なテスト
    complex_result = test_complex_example()
    
    print("\n🎉 UIFormatConverter単独動作確認完了!")
    print("👍 CentralControllerなしでも完全に動作します。")
