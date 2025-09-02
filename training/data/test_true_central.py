"""
Fast Test用の真の中央管理システム連携テスト
"""

import sys
sys.path.append('.')
from true_central_controller import TrueCentralController

def test_with_true_central_controller():
    """真の中央管理システムを使用したテスト"""
    controller = TrueCentralController()
    
    # 失敗ケースをテスト
    failed_cases = [96, 97, 98, 118, 164, 165, 166, 168, 170]
    
    print("🎯 True Central Controller - Failed Cases Test")
    print("=" * 60)
    
    import json
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    for case_id in failed_cases:
        case_key = str(case_id)
        if case_key in test_data['data']:
            sentence = test_data['data'][case_key]['sentence']
            print(f"\n📝 Case {case_id}: {sentence}")
            
            try:
                result = controller.process_sentence(sentence)
                
                print(f"✅ Success: {result.get('success', False)}")
                print(f"📊 Main Slots: {result.get('main_slots', {})}")
                print(f"📋 Sub Slots: {result.get('sub_slots', {})}")
                print(f"🔧 Completed Handlers: {result.get('metadata', {}).get('completed_handlers', [])}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print(f"\n❌ Case {case_id}: データが見つかりません")
    
    print("\n🏆 True Central Controller Test Complete")

if __name__ == "__main__":
    test_with_true_central_controller()
