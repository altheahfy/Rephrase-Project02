import json

with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cases = data.get('data', {})

# case_117とcase_126の詳細確認
for case_num in ['117', '126']:
    case_data = cases.get(case_num, {})
    print(f'case_{case_num}:')
    print(f'  sentence: {case_data.get("sentence")}')
    print(f'  V_group_key: {case_data.get("V_group_key")}')
    print(f'  expected: {case_data.get("expected", {}).get("main_slots", {})}')
    print()

# tellグループ83-86の詳細確認
print("tellグループ疑問文系 (83-86):")
for case_num in ['83', '84', '85', '86']:
    case_data = cases.get(case_num, {})
    print(f'case_{case_num}: {case_data.get("sentence")}')
    print(f'  expected: {case_data.get("expected", {}).get("main_slots", {})}')
    print()
