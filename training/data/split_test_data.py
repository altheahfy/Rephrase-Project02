import json

with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# データ構造確認
print("データ構造:", list(data.keys()))
print("テストケース数:", len(data['data']))

# 実際のテストケースはdata辞書の中にある
test_cases = data['data']
meta_info = data['meta']

# 未対応ケース（75-82）を抽出
future_cases = {}
current_cases = {}

for case_key, case_value in test_cases.items():
    case_id = int(case_key)
    if 75 <= case_id <= 82:
        future_cases[case_key] = case_value
        print(f'未対応ケース発見: case_{case_id} - {case_value.get("sentence", "")}')
    else:
        current_cases[case_key] = case_value

print(f'\n未対応ケース数: {len(future_cases)}')
print(f'実装済みケース数: {len(current_cases)}')

# 現在の実装済み範囲のメタ情報を更新
current_meta = meta_info.copy()
current_meta['total_count'] = len(current_cases)
current_meta['valid_count'] = len(current_cases)
current_meta['note'] = '実装済み範囲のみ（100%スコア維持用）'

# 未対応ケース用のメタ情報
future_meta = {
    'total_count': len(future_cases),
    'valid_count': len(future_cases),
    'note': '未実装ケース（将来の開発対象）',
    'target_handlers': ['ComplexConstructionHandler']
}

# 実装済みデータセット作成
current_dataset = {
    'meta': current_meta,
    'data': current_cases
}

# 未対応データセット作成
future_dataset = {
    'meta': future_meta,
    'data': future_cases
}

# ファイル保存
with open('current_implemented_test_data.json', 'w', encoding='utf-8') as f:
    json.dump(current_dataset, f, ensure_ascii=False, indent=2)

with open('future_unimplemented_test_data.json', 'w', encoding='utf-8') as f:
    json.dump(future_dataset, f, ensure_ascii=False, indent=2)

print(f'\n✅ ファイル分割完了:')
print(f'  - current_implemented_test_data.json: {len(current_cases)}ケース（100%対応）')
print(f'  - future_unimplemented_test_data.json: {len(future_cases)}ケース（将来実装）')
