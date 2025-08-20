#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def safe_json_dump(data, filepath):
    """Circular reference対応のJSONダンプ"""
    def clean_circular_refs(obj, seen=None):
        if seen is None:
            seen = set()
        
        if isinstance(obj, dict):
            obj_id = id(obj)
            if obj_id in seen:
                return {"<circular_reference>": str(obj_id)}
            seen.add(obj_id)
            cleaned = {}
            for k, v in obj.items():
                try:
                    cleaned[k] = clean_circular_refs(v, seen.copy())
                except:
                    cleaned[k] = str(v)
            return cleaned
        elif isinstance(obj, list):
            return [clean_circular_refs(item, seen.copy()) for item in obj]
        else:
            return obj
    
    try:
        cleaned_data = clean_circular_refs(data)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"JSON保存エラー: {e}")
        return False

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def calculate_accuracy(expected, actual):
    """Calculate accuracy between expected and actual results"""
    total_slots = 0
    matching_slots = 0
    
    # Main slots to check (including Aux)
    main_slot_keys = ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'Aux']
    for slot in main_slot_keys:
        total_slots += 1
        expected_val = expected.get('main_slots', {}).get(slot, '')
        actual_val = actual.get('slots', {}).get(slot, '')
        if expected_val == actual_val:
            matching_slots += 1
    
    # Sub slots to check (including all possible sub-slots)
    sub_slot_keys = ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux']
    for slot in sub_slot_keys:
        total_slots += 1
        expected_val = expected.get('sub_slots', {}).get(slot, '')
        actual_val = actual.get('sub_slots', {}).get(slot, '')
        if expected_val == actual_val:
            matching_slots += 1
    
    return matching_slots / total_slots if total_slots > 0 else 0.0

def get_detailed_comparison(expected, actual):
    """Get detailed slot-by-slot comparison"""
    differences = []
    
    # Check main slots
    main_slot_keys = ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'Aux']
    for slot in main_slot_keys:
        expected_val = expected.get('main_slots', {}).get(slot, '')
        actual_val = actual.get('slots', {}).get(slot, '')
        if expected_val != actual_val:
            differences.append(f"Main {slot}: '{expected_val}' -> '{actual_val}'")
    
    # Check sub slots
    sub_slot_keys = ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux']
    for slot in sub_slot_keys:
        expected_val = expected.get('sub_slots', {}).get(slot, '')
        actual_val = actual.get('sub_slots', {}).get(slot, '')
        if expected_val != actual_val:
            differences.append(f"Sub {slot}: '{expected_val}' -> '{actual_val}'")
    
    return differences

def run_full_test():
    """Run full 53-sentence test with accurate reporting"""
    
    # Load test data
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Initialize mapper
    print("Initializing UnifiedStanzaRephraseMapper...")
    mapper = UnifiedStanzaRephraseMapper()
    print("Mapper initialized successfully.\n")
    
    results = {
        'meta': {
            'input_file': 'final_test_system/final_54_test_data.json',
            'processed_at': datetime.now().isoformat(),
            'total_sentences': 0,
            'success_count': 0,
            'error_count': 0,
            'perfect_count': 0,
            'high_accuracy_count': 0
        },
        'results': {},
        'summary': {
            'perfect_cases': [],
            'high_accuracy_cases': [],
            'low_accuracy_cases': [],
            'failed_cases': []
        }
    }
    
    total_accuracy = 0.0
    processed_count = 0
    
    print("=== 53例文全体テスト開始 ===\n")
    
    for case_id, test_case in test_data['data'].items():
        case_num = int(case_id)
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"Case {case_num}: {sentence}")
        
        try:
            # Process sentence
            actual = mapper.process(sentence)
            
            # Calculate accuracy
            accuracy = calculate_accuracy(expected, actual)
            total_accuracy += accuracy
            processed_count += 1
            
            # Get detailed comparison
            differences = get_detailed_comparison(expected, actual)
            
            case_result = {
                'sentence': sentence,
                'expected': expected,
                'actual': actual,
                'accuracy': accuracy,
                'differences': differences,
                'status': 'success'
            }
            
            results['results'][case_id] = case_result
            results['meta']['success_count'] += 1
            
            # Categorize results
            if accuracy >= 1.0:
                results['meta']['perfect_count'] += 1
                results['summary']['perfect_cases'].append(case_num)
                print(f"  ✅ Perfect: {accuracy:.1%}")
            elif accuracy >= 0.9:
                results['meta']['high_accuracy_count'] += 1
                results['summary']['high_accuracy_cases'].append(case_num)
                print(f"  🔶 High: {accuracy:.1%} - Issues: {len(differences)}")
                for diff in differences[:3]:  # Show first 3 differences
                    print(f"    - {diff}")
            else:
                results['summary']['low_accuracy_cases'].append(case_num)
                print(f"  ❌ Low: {accuracy:.1%} - Issues: {len(differences)}")
                for diff in differences[:3]:  # Show first 3 differences
                    print(f"    - {diff}")
            
        except Exception as e:
            print(f"  💥 Error: {str(e)}")
            results['results'][case_id] = {
                'sentence': sentence,
                'expected': expected,
                'error': str(e),
                'accuracy': 0.0,
                'differences': [],
                'status': 'error'
            }
            results['meta']['error_count'] += 1
            results['summary']['failed_cases'].append(case_num)
    
    results['meta']['total_sentences'] = len(test_data['data'])
    results['meta']['overall_accuracy'] = total_accuracy / processed_count if processed_count > 0 else 0.0
    
    # Save detailed results
    output_file = f'full_test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    if safe_json_dump(results, output_file):
        print(f"\n結果を {output_file} に保存しました")
    else:
        print(f"\n結果保存に失敗しましたが、テストは完了しました")
    
    # Print summary
    print(f"\n=== テスト完了 ===")
    print(f"総文数: {results['meta']['total_sentences']}")
    print(f"成功: {results['meta']['success_count']}")
    print(f"エラー: {results['meta']['error_count']}")
    print(f"全体精度: {results['meta']['overall_accuracy']:.1%}")
    print(f"完璧なケース: {results['meta']['perfect_count']}")
    print(f"高精度ケース: {results['meta']['high_accuracy_count']}")
    print(f"結果保存: {output_file}")
    
    print(f"\n=== カテゴリ別詳細 ===")
    if results['summary']['perfect_cases']:
        print(f"✅ 完璧 ({len(results['summary']['perfect_cases'])}件): {results['summary']['perfect_cases']}")
    
    if results['summary']['high_accuracy_cases']:
        print(f"🔶 高精度 ({len(results['summary']['high_accuracy_cases'])}件): {results['summary']['high_accuracy_cases']}")
    
    if results['summary']['low_accuracy_cases']:
        print(f"❌ 低精度 ({len(results['summary']['low_accuracy_cases'])}件): {results['summary']['low_accuracy_cases']}")
        print("次の修正対象候補:")
        for case_id in results['summary']['low_accuracy_cases'][:5]:
            case_result = results['results'][str(case_id)]
            print(f"  Case {case_id}: {case_result['accuracy']:.1%} - \"{case_result['sentence']}\"")
    
    if results['summary']['failed_cases']:
        print(f"💥 エラー ({len(results['summary']['failed_cases'])}件): {results['summary']['failed_cases']}")
    
    return output_file

if __name__ == "__main__":
    run_full_test()
