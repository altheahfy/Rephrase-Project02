import json

with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# dataセクションを取得
cases = data.get('data', {})

case_83 = cases.get('83', {})
case_84 = cases.get('84', {})

print(f'case_83 V_group_key: {case_83.get("V_group_key")}')
print(f'case_84 V_group_key: {case_84.get("V_group_key")}')
print(f'case_83: {case_83.get("sentence", "")}')
print(f'case_84: {case_84.get("sentence", "")}')

# すべてのV_group_keyを確認
v_groups = set()
for key, value in cases.items():
    if isinstance(value, dict) and 'V_group_key' in value:
        v_groups.add(value['V_group_key'])

print(f'\n利用可能なV_group_key: {sorted(v_groups)}')
