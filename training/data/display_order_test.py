#!/usr/bin/env python3
"""
表示順序機能のテスト
個別エンジンが位置情報と表示順序を正しく付与するかテスト
"""

import sys
import os
import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_display_order():
    """表示順序機能のテスト"""
    
    print("🔍 表示順序機能テスト開始")
    print("=" * 60)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    
    # ハンドラー追加
    mapper.add_handler('relative_clause')
    mapper.add_handler('basic_five_pattern')
    
    # テストケース
    test_cases = [
        {
            "sentence": "The car which was stolen is expensive",
            "expected_structure": {
                "S": "The car which was stolen",
                "V": "is", 
                "C1": "expensive",
                "S-sub-s": "The car which",
                "S-sub-aux": "was",
                "S-sub-v": "stolen"
            },
            "description": "関係節+受動態"
        },
        {
            "sentence": "The book that I read yesterday was interesting",
            "expected_structure": {
                "S": "The book that I read yesterday", 
                "V": "was",
                "C1": "interesting",
                "S-sub-o1": "The book that",
                "S-sub-s": "I",
                "S-sub-v": "read",
                "S-sub-m2": "yesterday"
            },
            "description": "関係節+副詞"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        description = test_case["description"]
        
        print(f"\n📖 テスト{i}: {description}")
        print(f"例文: '{sentence}'")
        print("-" * 50)
        
        try:
            result = mapper.process(sentence)
            
            # メインスロット表示
            slots = result.get('slots', {})
            print(f"\n📊 メインスロット:")
            for slot, value in slots.items():
                print(f"  {slot}: '{value}'")
            
            # 位置別サブスロット表示（表示順序付き）
            positional_sub_slots = result.get('positional_sub_slots', {})
            print(f"\n🎯 位置別サブスロット:")
            
            for position, sub_slots_dict in positional_sub_slots.items():
                print(f"  [{position}位置]:")
                
                # 表示順序でソート
                sorted_sub_slots = sorted(
                    sub_slots_dict.items(),
                    key=lambda x: x[1].get('display_order', 999) if isinstance(x[1], dict) else 999
                )
                
                for sub_slot_key, sub_slot_info in sorted_sub_slots:
                    if isinstance(sub_slot_info, dict):
                        value = sub_slot_info.get('value', '')
                        order = sub_slot_info.get('display_order', '?')
                        position_info = sub_slot_info.get('position', '?')
                        print(f"    {sub_slot_key}: '{value}' (順序:{order}, 位置:{position_info})")
                    else:
                        print(f"    {sub_slot_key}: '{sub_slot_info}' (レガシー)")
            
            # 処理時間表示
            processing_time = result.get('meta', {}).get('processing_time', 0)
            print(f"\n⏱️ 処理時間: {processing_time:.3f}s")
            
            # 表示順序によるDB形式出力
            print(f"\n💾 DB形式出力（表示順序準拠）:")
            print("  メインスロット:")
            for slot, value in slots.items():
                if value:  # 空でない場合のみ
                    print(f"    {slot}: '{value}' (slot_display_order: 自動算出)")
            
            print("  サブスロット:")
            for position, sub_slots_dict in positional_sub_slots.items():
                for sub_slot_key, sub_slot_info in sorted_sub_slots:
                    if isinstance(sub_slot_info, dict) and sub_slot_info.get('value'):
                        value = sub_slot_info['value']
                        order = sub_slot_info.get('display_order', 999)
                        formatted_key = f"{position}-{sub_slot_key}"
                        print(f"    {formatted_key}: '{value}' (display_order: {order})")
            
        except Exception as e:
            print(f"❌ テスト{i}エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🏁 表示順序機能テスト完了")

if __name__ == "__main__":
    test_display_order()
