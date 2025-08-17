#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
53例文精度検証システム
システム出力 vs 正解データの完全照合
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
import codecs

def accuracy_validation():
    """53例文精度検証実行"""
    print("🎯 53例文精度検証開始")
    print("="*60)
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')  # ログを最小化
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause') 
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    # テストデータ読み込み
    test_data = json.load(codecs.open('final_54_test_data.json', 'r', 'utf-8'))
    confirmed_data = json.load(codecs.open('confirmed_correct_answers.json', 'r', 'utf-8'))
    
    print(f"📊 データ読み込み完了:")
    print(f"  統合テストデータ: {len(test_data['data'])}件")
    print(f"  承認済み正解データ: {confirmed_data['meta']['total_entries']}件")
    print()
    
    # 精度測定
    total_tests = 0
    perfect_matches = 0
    partial_matches = 0
    failures = 0
    
    accuracy_results = []
    
    for test_id, test_case in test_data['data'].items():
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        total_tests += 1
        print(f"🧪 テスト {total_tests}: {sentence}")
        
        # システム実行
        try:
            result = mapper.process(sentence)
            if result and 'slots' in result:
                # メインスロットとサブスロットを統合
                system_output = result['slots'].copy()
                if 'sub_slots' in result:
                    system_output.update(result['sub_slots'])
                
                # 精度判定
                match_result = compare_slots(system_output, expected)
                
                if match_result['perfect']:
                    perfect_matches += 1
                    print("  ✅ 完全一致")
                elif match_result['partial']:
                    partial_matches += 1
                    print(f"  ⚠️  部分一致 - 差異: {match_result['differences']}")
                else:
                    failures += 1
                    print(f"  ❌ 不一致 - 差異: {match_result['differences']}")
                
                accuracy_results.append({
                    'test_id': test_id,
                    'sentence': sentence,
                    'system_output': system_output,
                    'expected': expected,
                    'match_result': match_result
                })
                
            else:
                failures += 1
                print("  ❌ システム処理失敗")
                
        except Exception as e:
            failures += 1
            print(f"  ❌ エラー: {str(e)}")
        
        print()
    
    # 結果レポート
    print("="*60)
    print("📈 精度検証結果レポート")
    print("="*60)
    print(f"総テスト数: {total_tests}")
    print(f"完全一致: {perfect_matches} ({perfect_matches/total_tests*100:.1f}%)")
    print(f"部分一致: {partial_matches} ({partial_matches/total_tests*100:.1f}%)")  
    print(f"不一致: {failures} ({failures/total_tests*100:.1f}%)")
    print()
    
    overall_accuracy = (perfect_matches + partial_matches * 0.5) / total_tests * 100
    print(f"🎯 総合精度: {overall_accuracy:.1f}%")
    
    # 詳細結果保存
    detailed_report = {
        'meta': {
            'total_tests': total_tests,
            'perfect_matches': perfect_matches,
            'partial_matches': partial_matches,
            'failures': failures,
            'overall_accuracy': overall_accuracy
        },
        'detailed_results': accuracy_results
    }
    
    with codecs.open('accuracy_validation_report.json', 'w', 'utf-8') as f:
        json.dump(detailed_report, f, ensure_ascii=False, indent=2)
    
    print("📄 詳細レポート保存完了: accuracy_validation_report.json")
    
    return overall_accuracy

def compare_slots(system_output, expected):
    """スロット比較関数"""
    differences = []
    perfect = True
    
    # メインスロット比較
    main_slots = expected.get('main_slots', {})
    for slot, expected_value in main_slots.items():
        system_value = system_output.get(slot, '')
        if system_value != expected_value:
            differences.append(f"{slot}: システム'{system_value}' vs 期待'{expected_value}'")
            perfect = False
    
    # サブスロット比較
    sub_slots = expected.get('sub_slots', {})
    for slot, expected_value in sub_slots.items():
        system_value = system_output.get(slot, '')
        if system_value != expected_value:
            differences.append(f"{slot}: システム'{system_value}' vs 期待'{expected_value}'")
            perfect = False
    
    # システムにあるが期待にないスロット
    all_expected = set(main_slots.keys()) | set(sub_slots.keys())
    for slot in system_output:
        if slot not in all_expected:
            differences.append(f"予期しないスロット: {slot}='{system_output[slot]}'")
            perfect = False
    
    partial = len(differences) > 0 and len(differences) <= 3  # 3個以下の差異は部分一致
    
    return {
        'perfect': perfect,
        'partial': partial and not perfect,
        'differences': differences
    }

if __name__ == "__main__":
    accuracy_validation()
