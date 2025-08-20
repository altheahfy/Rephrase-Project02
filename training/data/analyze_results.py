#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# Load batch results
with open('batch_results_full_test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = data['meta']['total_sentences']
results = data['results']

# Count pass/fail
pass_count = sum(1 for result in results.values() if result.get('accuracy', 0) >= 0.9)
fail_cases = [int(key) for key, result in results.items() if result.get('accuracy', 0) < 0.9]

print("=== CASE 28修正後の最新結果 ===")
print(f"Total: {total}")
print(f"Pass: {pass_count}")
print(f"Fail: {len(fail_cases)}")
print(f"Accuracy: {pass_count / total * 100:.1f}%")

# Check case 28 specifically
case28 = results.get('28')
if case28:
    print(f"Case 28 accuracy: {case28.get('accuracy', 0):.1f}%")
else:
    print("Case 28 not found")

print("\nFirst 5 failing cases:")
for case_id in sorted(fail_cases)[:5]:
    case_data = results[str(case_id)]
    accuracy = case_data.get('accuracy', 0)
    sentence = case_data.get('sentence', 'N/A')
    print(f"  Case {case_id}: {accuracy:.1f}% - \"{sentence}\"")
