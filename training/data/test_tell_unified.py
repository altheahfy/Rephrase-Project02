#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pure_data_driven_order_manager import PureDataDrivenOrderManager

def test_tell_group_unified():
    """tellグループの統一絶対順序分析"""
    
    print("🎯 tellグループ統一絶対順序分析")
    print("="*60)
    
    # tellグループの例文を手動で作成（JSONから抽出したもの）
    tell_sentences_data = [
        {
            'sentence': 'What did he tell her at the store?',
            'slots': {'O2': 'What', 'Aux': 'did', 'S': 'he', 'V': 'tell', 'O1': 'her', 'M2': 'at the store'}
        },
        {
            'sentence': 'Did he tell her a secret there?',
            'slots': {'Aux': 'Did', 'S': 'he', 'V': 'tell', 'O1': 'her', 'O2': 'a secret', 'M2': 'there'}
        },
        {
            'sentence': 'Did I tell him a truth in the kitchen?',
            'slots': {'Aux': 'Did', 'S': 'I', 'V': 'tell', 'O1': 'him', 'O2': 'a truth', 'M2': 'in the kitchen'}
        },
        {
            'sentence': 'Where did you tell me a story?',
            'slots': {'M2': 'Where', 'Aux': 'did', 'S': 'you', 'V': 'tell', 'O1': 'me', 'O2': 'a story'}
        }
    ]
    
    order_manager = PureDataDrivenOrderManager()
    
    try:
        print(f"📚 tellグループ統一分析開始 ({len(tell_sentences_data)}例文)")
        
        # PureDataDrivenOrderManagerで統一分析
        results = order_manager.process_adverb_group('tell', tell_sentences_data)
        
        if results:
            print(f"\n🎉 tellグループ統一分析完了")
            print(f"📊 分析結果: {len(results)}例文")
            
            # 統一順序の確認
            first_result = results[0]
            ordered_keys = list(first_result['ordered_slots'].keys())
            print(f"\n🔧 tellグループ統一絶対順序: {' → '.join(ordered_keys)}")
            
            # 各例文の結果表示
            print(f"\n📝 各例文の絶対順序結果:")
            for i, result in enumerate(results):
                print(f"  例文{i+1}: {result['sentence']}")
                order_display = []
                for pos, element in result['ordered_slots'].items():
                    order_display.append(f"{pos}:{element}")
                print(f"    絶対順序: {' | '.join(order_display)}")
                print()
                
        else:
            print("❌ tellグループの統一分析に失敗")
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tell_group_unified()
