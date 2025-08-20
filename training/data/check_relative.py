import json

# 現在の結果を読み込み
with open('current_results.json') as f:
    current = json.load(f)

# 期待データを読み込み
with open('final_test_system/final_54_test_data.json') as f:
    expected_data = json.load(f)
    expected = expected_data['data']

# 相対副詞例文を確認
rel_adv_examples = [15, 16, 17, 18, 28, 41, 42]

for num in rel_adv_examples:
    str_num = str(num)
    if str_num in current['results'] and str_num in expected:
        print(f'=== Example {num} ===')
        curr_sub = current['results'][str_num]['analysis_result']['sub_slots']
        exp_sub = expected[str_num]['expected']['sub_slots']
        
        print('Current sub-slots:')
        for k, v in curr_sub.items():
            if k.startswith('sub-m'):
                print(f'  {k}: "{v}"')
        
        print('Expected sub-slots:')
        for k, v in exp_sub.items():
            if k.startswith('sub-m'):
                print(f'  {k}: "{v}"')
        print()
