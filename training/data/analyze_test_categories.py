#!/usr/bin/env python3
import json

# テストデータ読み込み
with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# データ構造確認
raw_data = data.get('data', {})

# 基本5文型カテゴリのケースを抽出
basic_5_cases = []
adverb_cases = []
for key, value in raw_data.items():
    if isinstance(value, dict):
        category = value.get('grammar_category')
        if category == 'basic_5_patterns':
            basic_5_cases.append((int(key), value))
        elif category == 'basic_adverbs':
            adverb_cases.append((int(key), value))

# ソート
basic_5_cases.sort(key=lambda x: x[0])
adverb_cases.sort(key=lambda x: x[0])

print(f"🔍 基本5文型ケース数: {len(basic_5_cases)}")
print(f"🔍 副詞ケース数: {len(adverb_cases)}")

print("\n📋 基本5文型テストケース一覧:")
for i, (test_id, case) in enumerate(basic_5_cases):
    text = case.get('sentence', case.get('text', 'N/A'))
    v_group = case.get('V_group_key', 'unknown')
    print(f"{i+1:2d}. test_id={test_id:2d}, V_group={v_group:10s}, text=\"{text}\"")

print(f"\n🎯 基本5文型テスト範囲: test_id {min(case[0] for case in basic_5_cases)} - {max(case[0] for case in basic_5_cases)}")
print(f"🎯 副詞テスト範囲: test_id {min(case[0] for case in adverb_cases)} - {max(case[0] for case in adverb_cases)}")

# 重複確認
basic_5_ids = set(case[0] for case in basic_5_cases)
adverb_ids = set(case[0] for case in adverb_cases)
overlap = basic_5_ids & adverb_ids

if overlap:
    print(f"\n⚠️ 重複するtest_id: {sorted(overlap)}")
else:
    print(f"\n✅ 基本5文型と副詞カテゴリに重複なし")
    
# 1-25の範囲分析
range_1_25 = set(range(1, 26))
basic_5_in_range = basic_5_ids & range_1_25
adverb_in_range = adverb_ids & range_1_25

print(f"\n📊 1-25範囲の内訳:")
print(f"  基本5文型: {len(basic_5_in_range)}件 - {sorted(basic_5_in_range)}")
print(f"  副詞: {len(adverb_in_range)}件 - {sorted(adverb_in_range)}")
print(f"  合計: {len(basic_5_in_range) + len(adverb_in_range)}件")

if len(basic_5_in_range) + len(adverb_in_range) == 25:
    print("✅ 1-25は基本5文型＋副詞の完全セット")
else:
    other_in_range = range_1_25 - basic_5_in_range - adverb_in_range
    print(f"⚠️ その他カテゴリも含む: {sorted(other_in_range)}")
