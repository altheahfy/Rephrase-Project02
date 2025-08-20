import json

with open('full_test_results_20250820_233629.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== 残っているエラー詳細 ===')
print(f'総文数: {data["meta"]["total_sentences"]}')
print(f'エラー数: {data["meta"]["error_count"]}')
print(f'完璧なケース: {data["meta"]["perfect_count"]}')
print(f'高精度ケース: {data["meta"]["high_accuracy_count"]}')
print()

print('=== 精度別ケース分析 ===')
perfect_cases = []
high_accuracy_cases = []
low_accuracy_cases = []

for case_id, result in data['results'].items():
    accuracy = result.get('accuracy', 1.0)
    if accuracy == 1.0:
        perfect_cases.append(int(case_id))
    elif accuracy >= 0.9:
        high_accuracy_cases.append(int(case_id))
    else:
        low_accuracy_cases.append(int(case_id))

print(f'完璧(100%): {len(perfect_cases)}件')
print(f'高精度(90%以上): {len(high_accuracy_cases)}件 - {sorted(high_accuracy_cases)}')
print(f'低精度(90%未満): {len(low_accuracy_cases)}件 - {sorted(low_accuracy_cases)}')

if high_accuracy_cases or low_accuracy_cases:
    print()
    print('=== 問題のあるケース詳細 ===')
    problem_cases = sorted(high_accuracy_cases + low_accuracy_cases)
    for case_id in problem_cases:
        result = data['results'][str(case_id)]
        accuracy = result.get('accuracy', 1.0)
        print(f'Case {case_id}: {accuracy*100:.1f}% - "{result["sentence"]}"')
        
        # 期待値と実際の値の違いを表示
        expected = result['expected']
        actual = result['actual']
        
        print(f'  期待メイン: {expected["main_slots"]}')
        print(f'  実際メイン: {actual["slots"]}')
        print(f'  期待サブ: {expected["sub_slots"]}')
        print(f'  実際サブ: {actual["sub_slots"]}')
        print()
