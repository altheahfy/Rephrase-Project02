#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# パスを追加してモジュールをインポート
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from central_controller import CentralController

def test_case_111():
    """Case 111単体テスト"""
    print("=== Case 111 単体テスト ===")
    
    # テストケース
    text = "The house where they lived was demolished."
    expected_main = {'S': '', 'Aux': 'was', 'V': 'demolished'}
    expected_sub = {'sub-m2': 'The house where', 'sub-s': 'they', 'sub-v': 'lived', '_parent_slot': 'S'}
    
    # CentralController初期化
    controller = CentralController()
    
    print(f"文: {text}")
    
    # 文法解析実行
    result = controller.analyze_grammar_structure(text)
    print(f"解析結果: {result}")
    
    if result and len(result) > 0:
        handler_name = result[0]
        print(f"使用ハンドラー: {handler_name}")
        
        # process_sentenceを使用
        processed_result = controller.process_sentence(text)
        print(f"処理結果: {processed_result}")
        
        if processed_result and processed_result.get('success'):
            # 結果チェック
            actual_main = processed_result.get('main_slots', {})
            actual_sub = processed_result.get('sub_slots', {})
            
            print(f"実際の主節: {actual_main}")
            print(f"期待の主節: {expected_main}")
            print(f"実際の従節: {actual_sub}")
            print(f"期待の従節: {expected_sub}")
            
            main_match = actual_main == expected_main
            sub_match = actual_sub == expected_sub
            
            print(f"主節一致: {main_match}")
            print(f"従節一致: {sub_match}")
            
            if main_match and sub_match:
                print("総合: ✅ PASS")
                return True
            else:
                print("総合: ❌ FAIL")
                return False
        else:
            print(f"❌ 処理結果エラー: {processed_result}")
            return False
    else:
        print(f"❌ 解析失敗: {result}")
        return False

if __name__ == "__main__":
    test_case_111()
