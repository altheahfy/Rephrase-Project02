#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現在のDynamicAbsoluteOrderManagerでの分解・番号付与結果を出力
"""

import json
from datetime import datetime
from central_controller import CentralController

def generate_current_results():
    """現在のシステムで分解・番号付与結果を生成"""
    
    controller = CentralController()
    
    # tellグループのテストケース
    test_cases = [
        {
            "id": 83,
            "sentence": "What did he tell her at the store?",
            "category": "tell_group"
        },
        {
            "id": 84, 
            "sentence": "Did he tell her a secret there?",
            "category": "tell_group"
        },
        {
            "id": 85,
            "sentence": "Did I tell him a truth in the kitchen?", 
            "category": "tell_group"
        },
        {
            "id": 86,
            "sentence": "Where did you tell me a story?",
            "category": "tell_group"
        },
        # 追加のtellグループテスト
        {
            "id": 87,
            "sentence": "He told me the truth yesterday.",
            "category": "tell_group"
        },
        {
            "id": 88,
            "sentence": "I will tell him a story tomorrow.",
            "category": "tell_group"
        },
        {
            "id": 89,
            "sentence": "Did you tell her the secret?",
            "category": "tell_group"
        },
        
        # basic_adverbsグループ - passiveグループ
        {
            "id": 18,
            "sentence": "The cake is being baked by my mother.",
            "category": "passive_group"
        },
        {
            "id": 19,
            "sentence": "The cake was eaten by the children.",
            "category": "passive_group"
        },
        {
            "id": 20,
            "sentence": "The door was opened by the key.",
            "category": "passive_group"
        },
        
        # basic_adverbsグループ - studyグループ
        {
            "id": 21,
            "sentence": "The students study hard for exams.",
            "category": "study_group"
        },
        {
            "id": 22,
            "sentence": "Tomorrow I study.",
            "category": "study_group"
        },
        {
            "id": 23,
            "sentence": "Students often study here.",
            "category": "study_group"
        },
        
        # basic_adverbsグループ - actionグループ
        {
            "id": 32,
            "sentence": "She sings beautifully.",
            "category": "action_group"
        },
        {
            "id": 33,
            "sentence": "We always eat breakfast together.",
            "category": "action_group"
        },
        {
            "id": 38,
            "sentence": "Every morning, he jogs slowly in the park.",
            "category": "action_group"
        },
        
        # basic_adverbsグループ - communicationグループ
        {
            "id": 29,
            "sentence": "The teacher explains grammar clearly to confused students daily.",
            "category": "communication_group"
        },
        {
            "id": 30,
            "sentence": "The student writes essays carefully for better grades.",
            "category": "communication_group"
        },
        {
            "id": 31,
            "sentence": "She always speaks English fluently at work.",
            "category": "communication_group"
        }
    ]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "system": "DynamicAbsoluteOrderManager",
        "total_tests": len(test_cases),
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
        
        try:
            result = controller.process_sentence(sentence)
            
            if result['success']:
                abs_order = result.get('absolute_order', {})
                
                case_result = {
                    "sentence": sentence,
                    "category": test_case["category"],
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
                    "success": False,
                    "error": "Processing failed",
                    "raw_result": result
                }
                print(f"  ❌ 処理失敗")
            
        except Exception as e:
            case_result = {
                "sentence": sentence,
                "category": test_case["category"],
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
