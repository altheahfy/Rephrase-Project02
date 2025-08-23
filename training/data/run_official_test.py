#!/usr/bin/env python3
"""
正式テスト手順実行
final_54_test_data.jsonの基本文型テストケースを実行
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import json

def run_official_test():
    """正式テスト手順の実行"""
    
    # テストケース選択（基本5文型のみ：助動詞なし）
    test_cases = [
        {
            "id": "1",
            "sentence": "The car is red.",
            "expected": {
                "main_slots": {
                    "S": "The car",
                    "V": "is", 
                    "C1": "red"
                },
                "sub_slots": {}
            }
        },
        {
            "id": "2", 
            "sentence": "I love you.",
            "expected": {
                "main_slots": {
                    "S": "I",
                    "V": "love",
                    "O1": "you"
                },
                "sub_slots": {}
            }
        },
        {
            "id": "55",
            "sentence": "Birds fly.",
            "expected": {
                "main_slots": {
                    "S": "Birds",
                    "V": "fly"
                },
                "sub_slots": {}
            }
        },
        {
            "id": "58",
            "sentence": "She looks happy.",
            "expected": {
                "main_slots": {
                    "S": "She",
                    "V": "looks",
                    "C1": "happy"
                },
                "sub_slots": {}
            }
        },
        {
            "id": "64",
            "sentence": "I gave him a book.",
            "expected": {
                "main_slots": {
                    "S": "I",
                    "V": "gave",
                    "O1": "him",
                    "O2": "a book"
                },
                "sub_slots": {}
            }
        }
    ]
    
    mapper = DynamicGrammarMapper()
    
    # compare_results.pyが期待する形式
    results = {
        "results": {}
    }
    
    print("=== 正式テスト手順実行 ===\n")
    
    for test_case in test_cases:
        test_id = test_case["id"]
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        print(f"テスト {test_id}: {sentence}")
        
        # dynamic_grammar_mapper.pyに直接入力
        result = mapper.analyze_sentence(sentence)
        
        # compare_results.pyが期待する形式で保存
        results["results"][test_id] = {
            "sentence": sentence,
            "expected": expected,
            "analysis_result": result,
            "status": "success"
        }
        
        print(f"期待値: {expected}")
        print(f"実際値: {result.get('main_slots', {})}")
        print("-" * 60)
    
    # 結果をJSONファイルに保存
    output_file = "official_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"結果を保存: {output_file}")
    return output_file

if __name__ == "__main__":
    run_official_test()
