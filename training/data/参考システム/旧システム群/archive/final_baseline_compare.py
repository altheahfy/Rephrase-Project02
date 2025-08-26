import json

with open('official_test_results.json', 'r', encoding='utf-8') as f:
    current_data = json.load(f)
with open('backup_100_percent_baseline.json', 'r', encoding='utf-8') as f:
    baseline_data = json.load(f)

# 実際のテスト結果を取得
current_results = current_data['results']
baseline_results = baseline_data['results']

print('=== Phase 1.1 vs Baseline 詳細比較 ===')
print(f'Current: {len(current_results)} cases')
print(f'Baseline: {len(baseline_results)} cases')

# ケース毎比較
differences = []
total_cases = len(current_results)

for case_id in current_results.keys():
    if case_id in baseline_results:
        curr_case = current_results[case_id]
        base_case = baseline_results[case_id]
        
        sentence = curr_case.get('sentence', 'N/A')
        
        # 結果の比較（actualの内容を比較）
        curr_actual = curr_case.get('actual', {})
        base_actual = base_case.get('actual', {})
        
        is_identical = (curr_actual == base_actual)
        status = 'IDENTICAL' if is_identical else 'DIFFERENT'
        differences.append((case_id, sentence, status, curr_actual, base_actual))
    else:
        differences.append((case_id, 'MISSING_IN_BASELINE', 'ERROR', {}, {}))

print(f'\n=== 比較結果 ===')
identical_count = sum(1 for _, _, status, _, _ in differences if status == 'IDENTICAL')
different_count = len(differences) - identical_count

print(f'完全一致: {identical_count}/{len(differences)} ({identical_count/len(differences)*100:.1f}%)')
print(f'差異あり: {different_count}/{len(differences)} ({different_count/len(differences)*100:.1f}%)')

if different_count > 0:
    print(f'\n=== 差異詳細 ===')
    for case_id, sentence, status, curr_actual, base_actual in differences:
        if status == 'DIFFERENT':
            print(f'Case {case_id}: {sentence}')
            print(f'  Current:  {curr_actual}')
            print(f'  Baseline: {base_actual}')
            print()
else:
    print('\n🎯 完璧！すべてのケースでベースラインと完全一致です。')
    print('Phase 1.1の依存関係無効化は100%精度を維持しています。')
    print('\n✅ spaCyの品詞分解能力活用 + 依存関係削除の戦略が成功！')
