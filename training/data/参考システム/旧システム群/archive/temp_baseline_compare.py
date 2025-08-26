import json

with open('official_test_results.json', 'r', encoding='utf-8') as f:
    current = json.load(f)
with open('backup_100_percent_baseline.json', 'r', encoding='utf-8') as f:
    baseline = json.load(f)

print('=== Phase 1.1 vs Baseline 詳細比較 ===')
print(f'Current: {len(current)} cases')
print(f'Baseline: {len(baseline)} cases')

differences = []
for i, (curr_case, base_case) in enumerate(zip(current, baseline)):
    if curr_case != base_case:
        differences.append((i, curr_case.get('sentence', 'N/A'), 'DIFFERENT'))
    else:
        differences.append((i, curr_case.get('sentence', 'N/A'), 'IDENTICAL'))

print(f'\n=== 比較結果 ===')
identical_count = sum(1 for _, _, status in differences if status == 'IDENTICAL')
different_count = len(differences) - identical_count

print(f'完全一致: {identical_count}/{len(differences)} ({identical_count/len(differences)*100:.1f}%)')
print(f'差異あり: {different_count}/{len(differences)} ({different_count/len(differences)*100:.1f}%)')

if different_count > 0:
    print(f'\n=== 差異詳細 ===')
    for i, sentence, status in differences:
        if status == 'DIFFERENT':
            print(f'Case {i+1}: {sentence}')
else:
    print('\n🎯 完璧！すべてのケースでベースラインと完全一致です。')
