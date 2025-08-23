import json

# 結果ファイルをロード
with open('official_test_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 関係節関連の結果のみ抽出
relative_tests = []
for test_id, test_data in results['results'].items():
    sentence = test_data['sentence']
    if any(word in sentence.lower() for word in ['who', 'whose', 'which', 'that']):
        # 受動態は除く
        if not any(word in sentence.lower() for word in ['was', 'were', 'been']):
            relative_tests.append((test_id, test_data))

print(f'関係節関連テスト（受動態除く）: {len(relative_tests)}件')
print('=' * 60)

total = len(relative_tests)
perfect = 0
main_ok = 0
sub_ok = 0

for test_id, test_data in relative_tests:
    sentence = test_data['sentence']
    expected = test_data['expected']
    actual = test_data['analysis_result']
    
    main_match = expected['main_slots'] == actual.get('main_slots', {})
    sub_match = expected.get('sub_slots', {}) == actual.get('sub_slots', {})
    perfect_match = main_match and sub_match
    
    if main_match:
        main_ok += 1
    if sub_match:
        sub_ok += 1
    if perfect_match:
        perfect += 1
    
    # 不一致の場合のみ表示
    if not perfect_match:
        print(f'❌ Test {test_id}: {sentence}')
        if not main_match:
            print(f'  メイン期待: {expected["main_slots"]}')
            print(f'  メイン実際: {actual.get("main_slots", {})}')
        if not sub_match:
            print(f'  サブ期待: {expected.get("sub_slots", {})}')
            print(f'  サブ実際: {actual.get("sub_slots", {})}')
        print()

print('=' * 60)
print(f'🎯 関係節テスト結果:')
print(f'   完全一致: {perfect}/{total} ({perfect/total*100:.1f}%)')
print(f'   メイン一致: {main_ok}/{total} ({main_ok/total*100:.1f}%)')
print(f'   サブ一致: {sub_ok}/{total} ({sub_ok/total*100:.1f}%)')

if perfect == total:
    print('🎉 全関係節テスト完全成功！')
else:
    print(f'⚠️  {total-perfect}件のテストで改善が必要')
