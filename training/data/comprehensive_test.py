#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

def comprehensive_system_test():
    """包括的システムテスト - 絶対順序とサブスロット順序の両方"""
    
    controller = CentralController()
    
    test_cases = [
        # 絶対順序システムテスト（副詞含む）
        ("副詞グループ - action", "She sings beautifully."),
        ("副詞グループ - study", "Students often study here."),
        
        # 絶対順序システムテスト（副詞なし）
        ("非副詞グループ - tell", "I tell him the truth."),
        ("非副詞グループ - basic", "He is a teacher."),
        
        # サブスロット順序システムテスト
        ("サブスロット - 関係節", "The man who runs fast is strong."),
        ("サブスロット - 名詞節", "I know that he is smart."),
        
        # 複合テスト
        ("複合 - 関係節+副詞", "The student who studies hard is successful."),
    ]
    
    print("🎯 システム包括テスト")
    print("="*60)
    
    for test_name, sentence in test_cases:
        print(f"\n📝 {test_name}: {sentence}")
        print("-" * 50)
        
        try:
            result = controller.process_sentence(sentence)
            
            # 基本情報
            print(f"🔧 v_group_key: {result.get('v_group_key', 'unknown')}")
            print(f"🔧 main_slots: {result.get('main_slots', {})}")
            
            # 絶対順序結果
            if result.get('ordered_slots'):
                ordered_slots = result['ordered_slots']
                print(f"🎯 絶対順序: {ordered_slots}")
                
            # サブスロット結果
            if result.get('sub_slots'):
                sub_slots = result['sub_slots']
                # _parent_slotを除外して表示
                display_sub_slots = {k: v for k, v in sub_slots.items() if not k.startswith('_')}
                print(f"🔗 サブスロット: {display_sub_slots}")
                
            # サブスロット順序結果
            if result.get('ordered_sub_slots'):
                ordered_sub_slots = result['ordered_sub_slots']
                # _parent_slotを除外して順序表示
                sub_order = []
                for key, data in ordered_sub_slots.items():
                    if not key.startswith('_'):
                        if isinstance(data, dict) and 'display_order' in data:
                            sub_order.append((data['display_order'], key, data['value']))
                        else:
                            sub_order.append((99, key, data))
                
                if sub_order:
                    sub_order.sort()
                    print(f"🎯 サブスロット順序:")
                    for order, key, value in sub_order:
                        print(f"    {order}. {key}: '{value}'")
            
            print("✅ 処理成功")
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    comprehensive_system_test()
