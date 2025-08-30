#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現在のDynamicAbsoluteOrderManagerでの分解・番号付与結果を出力
JSONファイルから例文番号を指定してテスト実行
"""

import json
from datetime import datetime
from central_controller import CentralController

def load_test_data_from_json():
    """JSONファイルからテストデータを読み込み"""
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_test_cases_by_ids(test_data, test_ids):
    """指定されたIDの例文を取得"""
    test_cases = []
    
    for test_id in test_ids:
        test_id_str = str(test_id)
        if test_id_str in test_data['data']:
            test_case = test_data['data'][test_id_str]
            test_cases.append({
                "id": test_id,
                "sentence": test_case['sentence'],
                "category": f"{test_case.get('V_group_key', 'unknown')}_group",
                "grammar_category": test_case.get('grammar_category', 'unknown'),
                "expected": test_case.get('expected', {})
            })
        else:
            print(f"⚠️ 警告: ID {test_id} がJSONファイルに見つかりません")
    
    return test_cases

def generate_current_results():
    """現在のシステムで分解・番号付与結果を生成"""
    
    # JSONファイルから全データを読み込み
    test_data = load_test_data_from_json()
    
    # テスト対象の例文番号を指定
    test_ids = [
        # tellグループ (basic_5_patterns)
        83, 84, 85, 86,
        
        # basic_adverbsグループ - passiveグループ  
        18, 19, 20,
        
        # basic_adverbsグループ - studyグループ
        21, 22, 23,
        
        # basic_adverbsグループ - actionグループ
        32, 33, 34, 35, 36, 37, 38,
        
        # basic_adverbsグループ - communicationグループ
        29, 30, 31,
        
        # basic_adverbsグループ - completionグループ
        24, 25,
        
        # basic_adverbsグループ - becomeグループ
        39,
        
        # basic_adverbsグループ - transactionグループ
        42
    ]
    
    # 指定IDの例文を取得
    test_cases = get_test_cases_by_ids(test_data, test_ids)
    
    print(f"=== JSONファイルから{len(test_cases)}件のテストケースを読み込み ===")
    for case in test_cases:
        print(f"ID {case['id']}: {case['sentence']} ({case['grammar_category']} - {case['category']})")
    print()

    controller = CentralController()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "system": "DynamicAbsoluteOrderManager",
        "total_tests": len(test_cases),
        "test_source": "final_54_test_data_with_absolute_order_corrected.json",
        "test_ids": test_ids,
        "tell_group_mapping": None,
        "results": {}
    }
    
    print("=== DynamicAbsoluteOrderManager 分解・番号付与結果生成 ===\n")
    
    # tellグループマッピングを記録
    if hasattr(controller.absolute_order_manager, 'group_mappings') and 'tell' in controller.absolute_order_manager.group_mappings:
        results["tell_group_mapping"] = controller.absolute_order_manager.group_mappings['tell']
        print(f"tellグループマッピング: {results['tell_group_mapping']}\n")
    
    success_count = 0
    
    for test_case in test_cases:
        case_id = test_case["id"]
        sentence = test_case["sentence"]
        
        print(f"【テスト{case_id}】: {sentence}")
        print(f"  カテゴリ: {test_case['grammar_category']} - {test_case['category']}")
        
        try:
            result = controller.process_sentence(sentence)
            
            if result['success']:
                abs_order = result.get('absolute_order', {})
                
                case_result = {
                    "sentence": sentence,
                    "category": test_case["category"],
                    "grammar_category": test_case["grammar_category"],
                    "expected": test_case["expected"],
                    "success": True,
                    "main_slots": result.get('main_slots', {}),
                    "absolute_order": abs_order.get('absolute_order', {}),
                    "group": abs_order.get('group', 'unknown'),
                    "mapping": abs_order.get('mapping', {}),
                    "raw_result": result
                }
                
                print(f"  ✅ 成功")
                print(f"  スロット: {case_result['main_slots']}")
                print(f"  絶対順序: {case_result['absolute_order']}")
                print(f"  グループ: {case_result['group']}")
                success_count += 1
                
            else:
                case_result = {
                    "sentence": sentence,
                    "category": test_case["category"],
                    "grammar_category": test_case["grammar_category"],
                    "expected": test_case["expected"],
                    "success": False,
                    "error": "Processing failed",
                    "raw_result": result
                }
                print(f"  ❌ 処理失敗")
            
        except Exception as e:
            case_result = {
                "sentence": sentence,
                "category": test_case["category"],
                "grammar_category": test_case["grammar_category"],
                "expected": test_case["expected"],
                "success": False, 
                "error": str(e),
                "raw_result": None
            }
            print(f"  ❌ エラー: {e}")
        
        results["results"][str(case_id)] = case_result
        print()
    
    results["success_count"] = success_count
    results["success_rate"] = (success_count / len(test_cases)) * 100
    
    # 結果をファイルに保存
    output_file = f"dynamic_absolute_order_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"=== 結果サマリー ===")
    print(f"総テスト数: {len(test_cases)}")
    print(f"成功数: {success_count}")
    print(f"成功率: {results['success_rate']:.1f}%")
    print(f"結果ファイル: {output_file}")
    
    return output_file

if __name__ == "__main__":
    output_file = generate_current_results()
    print(f"\n📄 分解・番号付与結果ファイル: {output_file}")
