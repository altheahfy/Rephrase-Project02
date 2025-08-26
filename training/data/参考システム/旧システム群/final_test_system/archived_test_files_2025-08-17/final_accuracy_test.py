#!/usr/bin/env python3
"""
最終精度測定
"""

import os
import sys
import json

# プロジェクトルートパスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def final_accuracy_test():
    # テストデータ読み込み
    with open('final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data_raw = json.load(f)
    
    # データ形式変換
    test_data = []
    for key, value in test_data_raw['data'].items():
        test_data.append(value)
    
    mapper = UnifiedStanzaRephraseMapper()
    
    # 必要なハンドラー追加
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    mapper.add_handler('auxiliary_complex')
    
    perfect_matches = 0
    total_tests = len(test_data)
    
    print(f"🎯 最終精度測定: {total_tests}例文")
    print("=" * 50)
    
    for i, test_case in enumerate(test_data, 1):
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        result = mapper.process(sentence)
        
        # 期待値形式に合わせて結果を整形
        formatted_result = {
            "main_slots": {},
            "sub_slots": {}
        }
        
        # main_slotsとsub_slotsに分離
        for key, value in result.items():
            if key.startswith('sub-'):
                formatted_result["sub_slots"][key] = value
            else:
                formatted_result["main_slots"][key] = value
        
        # スロット比較
        if formatted_result == expected:
            perfect_matches += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} Test{i:2d}: {sentence[:50]}...")
    
    accuracy = (perfect_matches / total_tests) * 100
    
    print("=" * 50)
    print(f"📊 最終結果")
    print(f"完全一致: {perfect_matches}/{total_tests}")
    print(f"🎯 完全一致率: {accuracy:.1f}%")
    
    if accuracy >= 50:
        print("🎉 Migration source活用 + Rephrase配置ルール適用成功！")
    else:
        print("⚠️ さらなる調整が必要")

if __name__ == "__main__":
    final_accuracy_test()
