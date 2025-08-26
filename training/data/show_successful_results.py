#!/usr/bin/env python3
"""
成功した分解結果の詳細出力
ユーザーが直接確認できる形式で出力
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def generate_detailed_results():
    """詳細な分解結果を生成"""
    
    print("🔍 成功した分解結果の詳細確認")
    print("=" * 80)
    
    controller = CentralController()
    
    # テストケース（成功例）
    test_cases = [
        # Phase 1: 基本5文型
        {
            'category': 'Phase 1 - 第2文型',
            'sentence': 'The car is red.',
            'expected': 'S-V-C構造'
        },
        {
            'category': 'Phase 1 - 第3文型',
            'sentence': 'I love you.',
            'expected': 'S-V-O構造'
        },
        {
            'category': 'Phase 1 - 第4文型',
            'sentence': 'I gave him a book.',
            'expected': 'S-V-O1-O2構造'
        },
        # Phase 2: 関係節（成功例）
        {
            'category': 'Phase 2 - who関係節',
            'sentence': 'The man who runs fast is strong.',
            'expected': 'who関係節+修飾語取得'
        },
        {
            'category': 'Phase 2 - which関係節（改善成功）',
            'sentence': 'The book which lies there is mine.',
            'expected': 'which関係節+sub-m2取得'
        },
        {
            'category': 'Phase 2 - that関係節',
            'sentence': 'The car that he drives is new.',
            'expected': 'that関係節処理'
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n【ケース{i}】{case['category']}")
        print(f"文: {case['sentence']}")
        print(f"期待: {case['expected']}")
        print("-" * 60)
        
        # 処理実行
        result = controller.process_sentence(case['sentence'])
        
        # 結果を見やすく整理
        organized_result = {
            'sentence': case['sentence'],
            'category': case['category'],
            'processing_success': result.get('success', False),
            'main_slots': result.get('main_slots', {}),
            'sub_slots': result.get('sub_slots', {}),
            'pattern_type': result.get('pattern_type', ''),
            'relative_pronoun': result.get('relative_pronoun', ''),
            'antecedent': result.get('antecedent', ''),
            'spacy_analysis': result.get('spacy_analysis', {})
        }
        
        results.append(organized_result)
        
        # コンソール出力
        print(f"処理成功: {organized_result['processing_success']}")
        print(f"メインスロット: {json.dumps(organized_result['main_slots'], ensure_ascii=False)}")
        if organized_result['sub_slots']:
            print(f"サブスロット: {json.dumps(organized_result['sub_slots'], ensure_ascii=False)}")
        if organized_result['pattern_type']:
            print(f"パターン: {organized_result['pattern_type']}")
        if organized_result['relative_pronoun']:
            print(f"関係代名詞: {organized_result['relative_pronoun']}")
        
        # 重要ポイントの強調
        if 'sub-m2' in organized_result['sub_slots']:
            sub_m2 = organized_result['sub_slots']['sub-m2']
            print(f"🎯 修飾語取得成功: sub-m2 = '{sub_m2}'")
    
    # JSONファイルとして保存
    output_file = 'successful_parsing_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n" + "=" * 80)
    print(f"📁 詳細結果保存先: {output_file}")
    print(f"📊 成功ケース数: {len([r for r in results if r['processing_success']])}/{len(results)}")
    
    return output_file

if __name__ == "__main__":
    output_file = generate_detailed_results()
    print(f"\n✅ ファイル '{output_file}' に詳細な分解結果を保存しました")
    print(f"🔍 このファイルを開いて分解結果を直接確認できます")
