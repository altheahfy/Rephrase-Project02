#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tellグループ専用テスト
DynamicAbsoluteOrderManagerの動作確認
"""

from central_controller import CentralController

def test_tell_group():
    """tellグループの様々なパターンをテスト"""
    
    controller = CentralController()
    
    # tellグループのテストケース
    test_cases = [
        "What did he tell her at the store?",    # 疑問詞 + 修飾語
        "Did he tell her a secret there?",       # 一般疑問文 + 修飾語  
        "Where did you tell me a story?",        # 場所疑問詞
        "Yesterday what did he tell her?",       # M1要素 + 疑問詞
        "Did I tell him a truth in the kitchen?", # 完全な例文
        "He told me the story yesterday.",       # 平叙文
        "Tell me what happened!",                # 命令文
    ]
    
    print("=== tellグループ専用テスト ===\n")
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"【テスト{i}】: {sentence}")
        result = controller.process_sentence(sentence)
        
        if result['success']:
            abs_order = result.get('absolute_order', {})
            if 'absolute_order' in abs_order:
                print(f"  ✅ 成功: グループ={abs_order.get('group', 'unknown')}")
                print(f"  絶対順序: {abs_order['absolute_order']}")
                print(f"  マッピング: {abs_order.get('mapping', {})}")
            else:
                print(f"  ⚠️ 処理成功だが絶対順序なし")
        else:
            print(f"  ❌ 処理失敗")
        
        print()

if __name__ == "__main__":
    test_tell_group()
