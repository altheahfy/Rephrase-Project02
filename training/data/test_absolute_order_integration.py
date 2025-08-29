#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Central Controller + AbsoluteOrderManager 統合テスト
"""

from central_controller import CentralController


def test_absolute_order_integration():
    """AbsoluteOrderManagerの統合テスト"""
    
    controller = CentralController()
    
    # テスト例文（各グループ）
    test_cases = [
        # 基本副詞グループ
        "The teacher explains grammar clearly to confused students daily.",
        "The cake is being baked by my mother.",
        
        # tellグループ（疑問文）
        "What did he tell her at the store?",
        "Where did you tell me a story?",
        
        # gaveグループ
        "He gave me a message.",
        "She gave him a money."
    ]
    
    print("=" * 80)
    print("Central Controller + AbsoluteOrderManager 統合テスト")
    print("=" * 80)
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n【テスト{i}】: {sentence}")
        print("-" * 50)
        
        try:
            result = controller.process_sentence(sentence)
            
            if result['success']:
                # 基本スロット表示
                print("✅ 処理成功")
                print(f"メインスロット: {result.get('main_slots', {})}")
                
                # AbsoluteOrder結果表示
                if 'absolute_order' in result:
                    abs_result = result['absolute_order']
                    print(f"🎯 グループ: {abs_result['group']}")
                    print(f"🎯 列数: {abs_result['columns']}")
                    print(f"🎯 絶対配置: {abs_result['absolute_order']}")
                    
                    # 表形式表示
                    if hasattr(controller.absolute_order_manager, 'generate_table_display'):
                        table = controller.absolute_order_manager.generate_table_display(abs_result)
                        print(f"🎯 表形式:")
                        print(table)
                else:
                    print("⚠️ AbsoluteOrder結果が見つかりません")
                    
            else:
                print(f"❌ 処理失敗: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 例外発生: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_absolute_order_integration()
