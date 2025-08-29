#!/usr/bin/env python3
"""
CentralController統合処理デバッグ - ケース84,85専用
"""

from central_controller import CentralController

def debug_cases_84_85():
    """ケース84,85のCentralController処理をデバッグ"""
    controller = CentralController()
    
    test_cases = [
        {
            'id': 84,
            'text': 'Did he tell her a secret there?',
            'expected': {
                'S': 'he', 'V': 'tell', 'O1': 'her', 'O2': 'secret', 
                'Aux': 'Did', 'M2': 'there'
            }
        },
        {
            'id': 85,
            'text': 'Did I tell him a truth in the kitchen?',
            'expected': {
                'S': 'I', 'V': 'tell', 'O1': 'him', 'O2': 'truth', 
                'Aux': 'Did', 'M2': 'in the kitchen'
            }
        }
    ]
    
    for case in test_cases:
        print(f"=== ケース{case['id']} ===")
        print(f"テスト文: {case['text']}")
        print(f"期待結果: {case['expected']}")
        print()
        
        # CentralController処理
        result = controller.process_sentence(case['text'])
        
        print(f"結果: {result}")
        print(f"成功: {result.get('success', False)}")
        if result.get('success'):
            print(f"スロット: {result.get('main_slots', {})}")
        else:
            print(f"エラー: {result.get('error', 'Unknown error')}")
        print()
        print("-" * 50)
        print()

if __name__ == "__main__":
    debug_cases_84_85()
