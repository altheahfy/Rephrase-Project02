#!/usr/bin/env python3
"""
UI例文表示デバッグスクリプト
最初の例文の全スロット情報を確認
"""

import json

def debug_first_example():
    """最初の例文の詳細を確認"""
    
    filename = "slot_order_data_第4文型と極性.json"
    
    print(f"🔍 {filename} デバッグ分析")
    print("=" * 60)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return
    
    # 最初の例文IDを特定
    first_example_id = None
    for record in data:
        if record.get("例文ID"):
            first_example_id = record["例文ID"]
            break
    
    if not first_example_id:
        print("❌ 例文IDが見つかりません")
        return
    
    print(f"🎯 最初の例文ID: {first_example_id}")
    print()
    
    # 該当例文のすべてのスロットを抽出
    example_slots = []
    for record in data:
        if record.get("例文ID") == first_example_id:
            example_slots.append(record)
    
    print(f"📊 例文 {first_example_id} のスロット情報:")
    print("-" * 60)
    
    for i, slot in enumerate(example_slots, 1):
        slot_name = slot.get("Slot", "N/A")
        slot_phrase = slot.get("SlotPhrase", "")
        slot_text = slot.get("SlotText", "")
        display_order = slot.get("Slot_display_order", 0)
        
        print(f"{i:2d}. スロット: {slot_name:4s} | 表示順: {display_order} | フレーズ: '{slot_phrase}' | テキスト: '{slot_text}'")
    
    print()
    print(f"✅ 合計スロット数: {len(example_slots)}")
    
    # スロット名の一覧
    slot_names = [slot.get("Slot") for slot in example_slots]
    unique_slots = list(set(slot_names))
    
    print(f"📋 ユニークスロット: {sorted(unique_slots)}")
    
    # 表示順序確認
    display_orders = [(slot.get("Slot"), slot.get("Slot_display_order", 0)) for slot in example_slots]
    display_orders.sort(key=lambda x: x[1])
    
    print()
    print("🔄 表示順序:")
    for slot_name, order in display_orders:
        print(f"  {order}: {slot_name}")
    
    # 可能性のある問題をチェック
    print()
    print("🚨 潜在的問題チェック:")
    
    issues = []
    
    # display_orderが0のスロットをチェック
    zero_order_slots = [slot.get("Slot") for slot in example_slots if slot.get("Slot_display_order", 0) == 0]
    if zero_order_slots:
        issues.append(f"display_order=0のスロット: {zero_order_slots}")
    
    # 重複表示順序をチェック
    orders = [slot.get("Slot_display_order", 0) for slot in example_slots]
    if len(orders) != len(set(orders)):
        issues.append("重複した表示順序が存在")
    
    # 空のSlotPhraseをチェック
    empty_phrases = [slot.get("Slot") for slot in example_slots if not slot.get("SlotPhrase", "").strip()]
    if empty_phrases:
        issues.append(f"空のSlotPhraseのスロット: {empty_phrases}")
    
    if issues:
        for issue in issues:
            print(f"  ⚠️ {issue}")
    else:
        print("  ✅ 特に問題は見つかりませんでした")

if __name__ == "__main__":
    debug_first_example()
