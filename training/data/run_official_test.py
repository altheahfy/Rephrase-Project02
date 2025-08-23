#!/usr/bin/env python3
"""
正式テスト手順実行
- 基本5文型テストケース（既存）
- 関係節関連テストケース（受動態除く、新規追加）
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import json

def run_official_test():
    """正式テスト手順の実行"""
    
    # テストケース選択（基本5文型 + 関係節関連）
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
        },
        # 🆕 関係節関連テストケース（受動態除く）
        {
            "id": "3",
            "sentence": "The man who runs fast is strong.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "strong"}, "sub_slots": {"sub-s": "The man who", "sub-v": "runs", "sub-m2": "fast"}}
        },
        {
            "id": "4",
            "sentence": "The book which lies there is mine.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "mine"}, "sub_slots": {"sub-s": "The book which", "sub-v": "lies", "sub-m2": "there"}}
        },
        {
            "id": "5",
            "sentence": "The person that works here is kind.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "kind"}, "sub_slots": {"sub-s": "The person that", "sub-v": "works", "sub-m2": "here"}}
        },
        {
            "id": "6",
            "sentence": "The book which I bought is expensive.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "expensive"}, "sub_slots": {"sub-o1": "The book which", "sub-s": "I", "sub-v": "bought"}}
        },
        {
            "id": "7",
            "sentence": "The man whom I met is tall.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "tall"}, "sub_slots": {"sub-o1": "The man whom", "sub-s": "I", "sub-v": "met"}}
        },
        {
            "id": "8",
            "sentence": "The car that he drives is new.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "new"}, "sub_slots": {"sub-o1": "The car that", "sub-s": "he", "sub-v": "drives"}}
        },
        {
            "id": "12",
            "sentence": "The man whose car is red lives here.",
            "expected": {"main_slots": {"S": "", "V": "lives", "M2": "here"}, "sub_slots": {"sub-s": "The man whose car", "sub-v": "is", "sub-c1": "red"}}
        },
        {
            "id": "13",
            "sentence": "The student whose book I borrowed is smart.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "smart"}, "sub_slots": {"sub-o1": "The student whose book", "sub-s": "I", "sub-v": "borrowed"}}
        },
        {
            "id": "14",
            "sentence": "The woman whose dog barks is my neighbor.",
            "expected": {"main_slots": {"S": "", "V": "is", "C1": "my neighbor"}, "sub_slots": {"sub-s": "The woman whose dog", "sub-v": "barks"}}
        },
        {
            "id": "34",
            "sentence": "The student who studies diligently always succeeds academically.",
            "expected": {"main_slots": {"S": "", "V": "succeeds", "M2": "academically"}, "sub_slots": {"sub-s": "The student who", "sub-v": "studies", "sub-m2": "diligently always"}}
        },
        {
            "id": "35",
            "sentence": "The teacher whose class runs efficiently is respected greatly.",
            "expected": {"main_slots": {"S": "", "Aux": "is", "V": "respected", "M2": "greatly"}, "sub_slots": {"sub-s": "The teacher whose class", "sub-v": "runs", "sub-m2": "efficiently"}}
        },
        {
            "id": "36",
            "sentence": "The doctor who works carefully saves lives successfully.",
            "expected": {"main_slots": {"S": "", "V": "saves", "O1": "lives", "M2": "successfully"}, "sub_slots": {"sub-s": "The doctor who", "sub-v": "works", "sub-m2": "carefully"}}
        }
    ]
    
    mapper = DynamicGrammarMapper()
    
    # compare_results.pyが期待する形式
    results = {
        "results": {}
    }
    
    print("=== 正式テスト手順実行（基本5文型 + 関係節）===\n")
    
    basic_tests = 0
    relative_tests = 0
    
    for test_case in test_cases:
        test_id = test_case["id"]
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        # テストタイプの判定
        is_relative = any(word in sentence.lower() for word in ['who', 'whose', 'which', 'that'])
        if is_relative:
            relative_tests += 1
        else:
            basic_tests += 1
        
        test_type = "関係節" if is_relative else "基本5文型"
        print(f"テスト {test_id} ({test_type}): {sentence}")
        
        # dynamic_grammar_mapper.pyに直接入力
        result = mapper.analyze_sentence(sentence)
        
        # compare_results.pyが期待する形式で保存
        results["results"][test_id] = {
            "sentence": sentence,
            "expected": expected,
            "analysis_result": result,
            "test_type": test_type,
            "status": "success"
        }
        
        print(f"期待値: {expected}")
        print(f"実際値: {result.get('main_slots', {})}")
        if expected.get('sub_slots'):
            print(f"サブ期待: {expected.get('sub_slots', {})}")
            print(f"サブ実際: {result.get('sub_slots', {})}")
        print("-" * 60)
    
    print(f"\n=== テスト概要 ===")
    print(f"基本5文型テスト: {basic_tests}件")
    print(f"関係節テスト: {relative_tests}件")
    print(f"総テスト数: {len(test_cases)}件")
    
    # 結果をJSONファイルに保存
    output_file = "official_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"結果を保存: {output_file}")
    return output_file

if __name__ == "__main__":
    run_official_test()
