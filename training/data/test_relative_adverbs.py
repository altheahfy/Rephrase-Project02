#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
関係副詞テストケース一括テスト（111-120）
"""

import sys
import json
from central_controller import CentralController

def test_relative_adverb_cases():
    """関係副詞テストケース111-120の一括テスト"""
    print("=== 関係副詞テストケース一括テスト ===")
    
    # テストケース111-120
    test_cases = {
        "111": {
            "sentence": "The house where they lived was demolished.",
            "expected": {
                "main_slots": {"S": "", "Aux": "was", "V": "demolished"},
                "sub_slots": {"sub-m2": "The house where", "sub-s": "they", "sub-v": "lived", "_parent_slot": "S"}
            }
        },
        "112": {
            "sentence": "The day when we graduated was memorable.",
            "expected": {
                "main_slots": {"S": "", "V": "was", "C1": "memorable"},
                "sub_slots": {"sub-m2": "The day when", "sub-s": "we", "sub-v": "graduated", "_parent_slot": "S"}
            }
        },
        "113": {
            "sentence": "The reason why he quit is personal.",
            "expected": {
                "main_slots": {"S": "", "V": "is", "C1": "personal"},
                "sub_slots": {"sub-m2": "The reason why", "sub-s": "he", "sub-v": "quit", "_parent_slot": "S"}
            }
        },
        "114": {
            "sentence": "The way how she explained it helped everyone.",
            "expected": {
                "main_slots": {"S": "", "V": "helped", "O1": "everyone"},
                "sub_slots": {"sub-m2": "The way how", "sub-s": "she", "sub-v": "explained", "sub-o1": "it", "_parent_slot": "S"}
            }
        },
        "115": {
            "sentence": "The place where we first met holds special memories.",
            "expected": {
                "main_slots": {"S": "", "V": "holds", "O1": "special memories"},
                "sub_slots": {"sub-m2": "The place where", "sub-s": "we", "sub-v": "met", "sub-m3": "first", "_parent_slot": "S"}
            }
        },
        "116": {
            "sentence": "The time when everyone arrived was perfect.",
            "expected": {
                "main_slots": {"S": "", "V": "was", "C1": "perfect"},
                "sub_slots": {"sub-m2": "The time when", "sub-s": "everyone", "sub-v": "arrived", "_parent_slot": "S"}
            }
        },
        "117": {
            "sentence": "The way how they approach problems gets results.",
            "expected": {
                "main_slots": {"S": "", "V": "gets", "O1": "results"},
                "sub_slots": {"sub-m2": "The way how", "sub-s": "they", "sub-v": "approach", "sub-o1": "problems", "_parent_slot": "S"}
            }
        },
        "118": {
            "sentence": "The reason why technology changed became clear.",
            "expected": {
                "main_slots": {"S": "", "V": "became", "C1": "clear"},
                "sub_slots": {"sub-m2": "The reason why", "sub-s": "technology", "sub-v": "changed", "_parent_slot": "S"}
            }
        },
        "119": {
            "sentence": "The place where children play is safe.",
            "expected": {
                "main_slots": {"S": "", "V": "is", "C1": "safe"},
                "sub_slots": {"sub-m2": "The place where", "sub-s": "children", "sub-v": "play", "_parent_slot": "S"}
            }
        },
        "120": {
            "sentence": "The moment when she understood was beautiful.",
            "expected": {
                "main_slots": {"S": "", "V": "was", "C1": "beautiful"},
                "sub_slots": {"sub-m2": "The moment when", "sub-s": "she", "sub-v": "understood", "_parent_slot": "S"}
            }
        }
    }
    
    # CentralController初期化
    controller = CentralController()
    
    results = {}
    success_count = 0
    total_count = len(test_cases)
    
    for case_id, test_data in test_cases.items():
        print(f"\n--- Case {case_id} ---")
        sentence = test_data["sentence"]
        expected = test_data["expected"]
        
        print(f"テスト文: {sentence}")
        
        try:
            # 処理実行
            result = controller.process_sentence(sentence)
            
            # 結果比較
            main_match = result.get('main_slots') == expected['main_slots']
            sub_match = result.get('sub_slots') == expected['sub_slots']
            overall_match = main_match and sub_match
            
            if overall_match:
                success_count += 1
                print(f"✅ PASS - Main:{main_match}, Sub:{sub_match}")
            else:
                print(f"❌ FAIL - Main:{main_match}, Sub:{sub_match}")
                print(f"    Expected main: {expected['main_slots']}")
                print(f"    Actual main:   {result.get('main_slots')}")
                print(f"    Expected sub:  {expected['sub_slots']}")
                print(f"    Actual sub:    {result.get('sub_slots')}")
            
            results[case_id] = {
                "success": overall_match,
                "main_match": main_match,
                "sub_match": sub_match,
                "actual": result
            }
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results[case_id] = {"success": False, "error": str(e)}
    
    # 最終結果
    print(f"\n=== 最終結果 ===")
    print(f"成功: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    for case_id, result in results.items():
        status = "✅" if result.get("success") else "❌"
        print(f"  Case {case_id}: {status}")
    
    return success_count, total_count

if __name__ == "__main__":
    success, total = test_relative_adverb_cases()
    print(f"\n=== 関係副詞テスト完了: {success}/{total} 成功 ===")
    sys.exit(0 if success == total else 1)
