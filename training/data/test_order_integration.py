#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AbsoluteOrderManager統合確認テスト
CentralControllerでのabsolute_order処理確認
"""

from central_controller import CentralController

def test_order_integration():
    """orderシステム統合確認"""
    controller = CentralController()
    
    # tellグループのテストケース
    test_cases = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Where did you tell me a story?"
    ]
    
    print("🎯 AbsoluteOrderManager統合確認テスト")
    print("=" * 50)
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n📝 [{i}] {sentence}")
        
        try:
            result = controller.process_sentence(sentence)
            
            print(f"✅ Success: {result.get('success', False)}")
            print(f"📋 Slots: {result.get('slots', {})}")
            
            # absolute_orderが含まれているか確認
            if 'absolute_order' in result:
                print(f"🎯 Absolute Order: {result['absolute_order']}")
            else:
                print("❌ No absolute_order found in result")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_order_integration()
