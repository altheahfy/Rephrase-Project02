#!/usr/bin/env python3
"""
Central Controller正規テストスクリプト
正しいAPIを使用してcentral_controllerの真の性能を測定
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
from central_controller import CentralController
import json

def test_central_controller():
    """Central Controllerの性能テスト"""
    
    # テストケース定義
    test_cases = [
        {
            "id": 1,
            "sentence": "The car is red.",
            "expected_main": {'S': 'The car', 'V': 'is', 'C1': 'red'},
            "expected_sub": {}
        },
        {
            "id": 2,
            "sentence": "I love you.",
            "expected_main": {'S': 'I', 'V': 'love', 'O1': 'you'},
            "expected_sub": {}
        },
        {
            "id": 3,
            "sentence": "The man who runs fast is strong.",
            "expected_main": {'S': '', 'V': 'is', 'C1': 'strong'},
            "expected_sub": {'sub-s': 'The man who', 'sub-v': 'runs', 'sub-m2': 'fast', '_parent_slot': 'S'}
        },
        {
            "id": 4,
            "sentence": "The book which lies there is mine.",
            "expected_main": {'S': '', 'V': 'is', 'C1': 'mine'},
            "expected_sub": {'sub-s': 'The book which', 'sub-v': 'lies', 'sub-m2': 'there', '_parent_slot': 'S'}
        },
        {
            "id": 5,
            "sentence": "The person that works here is kind.",
            "expected_main": {'S': '', 'V': 'is', 'C1': 'kind'},
            "expected_sub": {'sub-s': 'The person that', 'sub-v': 'works', 'sub-m2': 'here', '_parent_slot': 'S'}
        }
    ]
    
    print("🎯 Central Controller Phase 2 正規テスト開始")
    print("=" * 60)
    
    # DynamicGrammarMapperを初期化
    mapper = DynamicGrammarMapper()
    
    # CentralControllerでラップ
    controller = CentralController(mapper)
    
    results = {
        "total_tests": len(test_cases),
        "successes": 0,
        "failures": [],
        "details": []
    }
    
    for test_case in test_cases:
        test_id = test_case["id"]
        sentence = test_case["sentence"]
        expected_main = test_case["expected_main"]
        expected_sub = test_case["expected_sub"]
        
        print(f"\nテスト {test_id}: {sentence}")
        print("-" * 40)
        
        try:
            # Central Controllerで解析
            result = controller.analyze_sentence(sentence)
            
            actual_main = result.get('main_slots', {})
            actual_sub = result.get('sub_slots', {})
            
            # 比較
            main_match = actual_main == expected_main
            sub_match = actual_sub == expected_sub
            
            success = main_match and sub_match
            
            print(f"期待値 main: {expected_main}")
            print(f"実際値 main: {actual_main}")
            print(f"Main一致: {'✅' if main_match else '❌'}")
            
            if expected_sub:
                print(f"期待値 sub: {expected_sub}")
                print(f"実際値 sub: {actual_sub}")
                print(f"Sub一致: {'✅' if sub_match else '❌'}")
            
            print(f"総合結果: {'✅ 成功' if success else '❌ 失敗'}")
            
            if success:
                results["successes"] += 1
            else:
                results["failures"].append({
                    "test_id": test_id,
                    "sentence": sentence,
                    "expected_main": expected_main,
                    "actual_main": actual_main,
                    "expected_sub": expected_sub,
                    "actual_sub": actual_sub
                })
            
            results["details"].append({
                "test_id": test_id,
                "sentence": sentence,
                "success": success,
                "main_match": main_match,
                "sub_match": sub_match,
                "result": result
            })
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            results["failures"].append({
                "test_id": test_id,
                "sentence": sentence,
                "error": str(e)
            })
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("🎯 テスト結果サマリー")
    print("=" * 60)
    
    success_rate = (results["successes"] / results["total_tests"]) * 100
    print(f"総テスト数: {results['total_tests']}")
    print(f"成功: {results['successes']}")
    print(f"失敗: {len(results['failures'])}")
    print(f"成功率: {success_rate:.1f}%")
    
    if results["failures"]:
        print("\n❌ 失敗したテスト:")
        for failure in results["failures"]:
            print(f"  - テスト {failure['test_id']}: {failure['sentence']}")
    
    # 結果をファイルに保存
    with open('central_controller_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 詳細結果を保存: central_controller_test_results.json")
    
    return success_rate

if __name__ == "__main__":
    success_rate = test_central_controller()
    print(f"\n🎯 Central Controller Phase 2 最終結果: {success_rate:.1f}%")
