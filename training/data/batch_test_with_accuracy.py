#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def calculate_accuracy(expected, actual):
    """Calculate accuracy between expected and actual results"""
    total_slots = 0
    matching_slots = 0
    
    # Check main slots
    for slot in ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2']:
        total_slots += 1
        expected_val = expected.get('slots', {}).get(slot, '')
        actual_val = actual.get('slots', {}).get(slot, '')
        if expected_val == actual_val:
            matching_slots += 1
    
    # Check sub slots
    for slot in ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2']:
        total_slots += 1
        expected_val = expected.get('sub_slots', {}).get(slot, '')
        actual_val = actual.get('sub_slots', {}).get(slot, '')
        if expected_val == actual_val:
            matching_slots += 1
    
    return matching_slots / total_slots if total_slots > 0 else 0.0

def run_batch_test():
    """Run batch test with accuracy calculation"""
    
    # Load test data
    with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Initialize mapper
    mapper = UnifiedStanzaRephraseMapper()
    
    results = {
        'meta': {
            'input_file': 'final_test_system/final_54_test_data.json',
            'processed_at': datetime.now().isoformat(),
            'total_sentences': 0,
            'success_count': 0,
            'error_count': 0
        },
        'results': {}
    }
    
    total_accuracy = 0.0
    processed_count = 0
    
    for i, test_case in test_data['data'].items():
        i = int(i)  # Convert string key to int
        sentence = test_case['sentence']
        expected = test_case['expected']
        
        print(f"Processing case {i}: {sentence}")
        
        try:
            # Process sentence
            actual = mapper.process(sentence)
            
            # Calculate accuracy
            accuracy = calculate_accuracy(expected, actual)
            total_accuracy += accuracy
            processed_count += 1
            
            results['results'][str(i)] = {
                'sentence': sentence,
                'expected': expected,
                'actual': actual,
                'accuracy': accuracy,
                'status': 'success'
            }
            
            results['meta']['success_count'] += 1
            
            print(f"  Accuracy: {accuracy:.3f}")
            
        except Exception as e:
            print(f"  Error: {str(e)}")
            results['results'][str(i)] = {
                'sentence': sentence,
                'expected': expected,
                'error': str(e),
                'accuracy': 0.0,
                'status': 'error'
            }
            results['meta']['error_count'] += 1
    
    results['meta']['total_sentences'] = len(test_data['data'])
    results['meta']['overall_accuracy'] = total_accuracy / processed_count if processed_count > 0 else 0.0
    
    # Save results
    output_file = f'batch_results_with_accuracy_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== BATCH TEST RESULTS ===")
    print(f"Total: {results['meta']['total_sentences']}")
    print(f"Success: {results['meta']['success_count']}")
    print(f"Errors: {results['meta']['error_count']}")
    print(f"Overall Accuracy: {results['meta']['overall_accuracy']:.1%}")
    print(f"Results saved to: {output_file}")
    
    return output_file

if __name__ == "__main__":
    run_batch_test()
