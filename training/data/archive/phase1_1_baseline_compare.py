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
for i, (curr_case, base_case) in enumerate(zip(current_results, baseline_results)):
    curr_sentence = curr_case.get('input', {}).get('sentence', 'N/A')
    
    # 結果の比較（main_slotsとsub_slotsの両方）
    curr_main = curr_case.get('actual', {}).get('main_slots', {})
    base_main = base_case.get('actual', {}).get('main_slots', {})
    curr_sub = curr_case.get('actual', {}).get('sub_slots', {})
    base_sub = base_case.get('actual', {}).get('sub_slots', {})
    
    is_identical = (curr_main == base_main and curr_sub == base_sub)
    status = 'IDENTICAL' if is_identical else 'DIFFERENT'
    differences.append((i, curr_sentence, status))

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
            # 差異の詳細表示
            curr_case = current_results[i]
            base_case = baseline_results[i]
            print(f'  Current: main={curr_case.get("actual", {}).get("main_slots", {})}')
            print(f'           sub={curr_case.get("actual", {}).get("sub_slots", {})}')
            print(f'  Baseline: main={base_case.get("actual", {}).get("main_slots", {})}')
            print(f'            sub={base_case.get("actual", {}).get("sub_slots", {})}')
            print()
else:
    print('\n🎯 完璧！すべてのケースでベースラインと完全一致です。')
    print('Phase 1.1の依存関係無効化は100%精度を維持しています。')
