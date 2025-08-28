#!/usr/bin/env python3
"""
ケース1, 2のデバッグ
"""

import json
from central_controller import CentralController

def debug_case(case_num, sentence):
    print(f"=== ケース{case_num} デバッグ ===")
    print(f"入力: {sentence}")
    
    controller = CentralController()
    result = controller.process_sentence(sentence)
    
    print(f"\n📊 実際の出力:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    debug_case(1, "The car is red.")
    print("\n" + "="*50 + "\n")
    debug_case(2, "I love you.")
