#!/usr/bin/env python3
"""
ケース4のデバッグ
"""

import json
from central_controller import CentralController

def debug_case4():
    print("=== ケース4 デバッグ ===")
    sentence = "The book which lies there is mine."
    print(f"入力: {sentence}")
    
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    print(f"\n📊 実際の出力:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print(f"\n📋 期待値:")
    expected = {
        "main_slots": {
          "S": "",
          "V": "is",
          "C1": "mine"
        },
        "sub_slots": {
          "sub-s": "The book which",
          "sub-v": "lies",
          "sub-m2": "there",
          "_parent_slot": "S"
        }
    }
    print(json.dumps(expected, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    debug_case4()
