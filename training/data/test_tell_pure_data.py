#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pure_data_driven_order_manager import PureDataDrivenOrderManager

def test_tell_group_pure_data_driven():
    """tellグループのPureDataDriven単体テスト（循環参照回避）"""
    
    print("🎯 tellグループPureDataDriven単体テスト")
    print("="*50)
    
    order_manager = PureDataDrivenOrderManager()
    
    # tellグループの例文データ（手動で設定）
    tell_examples = [
        "I tell him the truth.",
        "She tells me the story.",
        "He told her the secret.",
        "They tell us everything.",
        "We told them the news."
    ]
    
    try:
        print(f"\n📚 tellグループ分析開始 ({len(tell_examples)}例文)")
        results = order_manager.process_adverb_group("tell", tell_examples)
        
        if results:
            print(f"\n🎉 tellグループ分析完了")
            for i, result in enumerate(results):
                print(f"📝 例文{i+1}: {result['sentence']}")
                print(f"  🎯 順序: {result['ordered_slots']}")
                print()
                
            # 統一順序の確認
            first_result = results[0]
            ordered_keys = list(first_result['ordered_slots'].keys())
            print(f"🔧 tellグループ統一順序: {' → '.join(ordered_keys)}")
            
        else:
            print("❌ tellグループの分析に失敗しました")
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tell_group_pure_data_driven()
