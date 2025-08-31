#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pure_data_driven_order_manager import PureDataDrivenOrderManager

def test_tell_group_from_data():
    """JSON データからtellグループを抽出してテスト"""
    
    print("🎯 tellグループ絶対順序分析（データ駆動）")
    print("="*50)
    
    order_manager = PureDataDrivenOrderManager()
    
    try:
        # データからtellグループを抽出
        groups = order_manager.extract_adverb_groups()
        
        if 'tell' in groups:
            tell_examples = groups['tell']
            print(f"\n📚 tellグループ発見: {len(tell_examples)}例文")
            
            # tellグループを分析
            results = order_manager.process_adverb_group('tell', tell_examples)
            
            if results:
                print(f"\n🎉 tellグループ絶対順序分析完了")
                print(f"📊 分析された例文数: {len(results)}")
                
                # 最初の数例を表示
                for i, result in enumerate(results[:3]):  # 最初の3例のみ表示
                    print(f"\n📝 例文{i+1}: {result['sentence']}")
                    print(f"  🎯 絶対順序: {result['ordered_slots']}")
                
                if len(results) > 3:
                    print(f"\n... その他{len(results)-3}例文も正常に処理")
                
                # 統一順序の確認
                first_result = results[0]
                ordered_keys = list(first_result['ordered_slots'].keys())
                print(f"\n🔧 tellグループ統一絶対順序: {' → '.join(ordered_keys)}")
                
            else:
                print("❌ tellグループの分析に失敗")
        else:
            print("❌ tellグループが見つかりません")
            print(f"利用可能なグループ: {list(groups.keys())[:10]}...")  # 最初の10個
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tell_group_from_data()
