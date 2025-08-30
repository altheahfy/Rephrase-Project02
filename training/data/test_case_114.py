#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Case 114 関係副詞テスト
"""

import sys
import json
from central_controller import CentralController

def test_case_114():
    """case_114の単体テスト"""
    print("=== Case 114 関係副詞テスト ===")
    
    # テストケース
    test_sentence = "The way how she explained it helped everyone."
    print(f"テスト文: {test_sentence}")
    
    # CentralControllerでテスト
    controller = CentralController()
    result = controller.process_sentence(test_sentence)
    
    print(f"\n【処理結果】")
    print(f"Success: {result.get('success')}")
    print(f"Main slots: {result.get('main_slots')}")
    print(f"Sub slots: {result.get('sub_slots')}")
    print(f"Metadata: {result.get('metadata')}")
    
    # 期待値
    expected = {
        "main_slots": {
            "S": "",
            "V": "helped",
            "O1": "everyone"
        },
        "sub_slots": {
            "sub-m2": "The way how",
            "sub-s": "she",
            "sub-v": "explained",
            "sub-o1": "it",
            "_parent_slot": "S"
        }
    }
    
    print(f"\n【期待値】")
    print(f"Expected main slots: {expected['main_slots']}")
    print(f"Expected sub slots: {expected['sub_slots']}")
    
    # 比較
    main_match = result.get('main_slots') == expected['main_slots']
    sub_match = result.get('sub_slots') == expected['sub_slots']
    
    print(f"\n【結果比較】")
    print(f"Main slots match: {main_match}")
    print(f"Sub slots match: {sub_match}")
    print(f"Overall match: {main_match and sub_match}")
    
    return main_match and sub_match

if __name__ == "__main__":
    success = test_case_114()
    print(f"\n=== テスト結果: {'SUCCESS' if success else 'FAILED'} ===")
    sys.exit(0 if success else 1)
