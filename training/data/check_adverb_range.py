#!/usr/bin/env python3
import json

# テストデータ読み込み
with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# データ構造確認
print(f"データ型: {type(data)}")
if isinstance(data, dict):
    print(f"辞書キー: {list(data.keys())}")
    if 'data' in data:
        test_data = data['data']
        print(f"test_data型: {type(test_data)}, 長さ: {len(test_data) if hasattr(test_data, '__len__') else 'N/A'}")
        
        if hasattr(test_data, '__len__') and len(test_data) > 0:
            print(f"最初の要素: {test_data[0] if isinstance(test_data, list) else 'Not a list'}")
            
            # 最初の数要素を確認
            sample_items = test_data[:3] if isinstance(test_data, list) else []
            for i, item in enumerate(sample_items):
                print(f"要素{i+1}: {item}")
    
    if 'meta' in data:
        meta = data['meta']
        print(f"メタ情報: {meta.get('category_counts', {})}")

# 修正: dataの中のdataを使う
raw_data = data.get('data', [])
print(f"\n🔍 実際のテストデータ数: {len(raw_data) if hasattr(raw_data, '__len__') else 'N/A'}")

if isinstance(raw_data, dict):
    # 辞書の場合、キーを確認
    keys = list(raw_data.keys())[:10]  # 最初の10キー
    print(f"🔍 データキー例: {keys}")
    
    # 各キーの値を確認
    for key in keys:
        value = raw_data[key]
        print(f"  {key}: {type(value)} - {value}")
        break  # 最初の一つだけ詳細表示

# 副詞カテゴリのケースを抽出
raw_data = data.get('data', [])
if isinstance(raw_data, list):
    adverb_cases = [item for item in raw_data if isinstance(item, dict) and item.get('grammar_category') == 'basic_adverbs']
elif isinstance(raw_data, dict):
    # 辞書の場合、値を検査
    adverb_cases = []
    for key, value in raw_data.items():
        if isinstance(value, dict) and value.get('grammar_category') == 'basic_adverbs':
            adverb_cases.append(value)
else:
    adverb_cases = []

print(f"🔍 副詞ケース数: {len(adverb_cases)}")

if len(adverb_cases) == 0:
    # 全カテゴリを確認
    if isinstance(raw_data, dict):
        categories = set()
        sample_items = []
        for i, (key, value) in enumerate(raw_data.items()):
            if isinstance(value, dict):
                categories.add(value.get('grammar_category', 'unknown'))
                if i < 3:  # 最初の3要素をサンプルとして保存
                    sample_items.append((key, value))
        print(f"🔍 全カテゴリ: {sorted(categories)}")
        print(f"🔍 サンプル要素: {sample_items}")
        
        # basic_adverbsの類似カテゴリを探す
        adverb_related = [cat for cat in categories if 'adverb' in str(cat).lower()]
        print(f"🔍 副詞関連カテゴリ: {adverb_related}")
        
        # 実際にadverb関連のケースを抽出
        if adverb_related:
            for cat in adverb_related:
                related_cases = [value for value in raw_data.values() if isinstance(value, dict) and value.get('grammar_category') == cat]
                print(f"📋 {cat}カテゴリ: {len(related_cases)}件")
                adverb_cases.extend(related_cases)

print(f"🔍 副詞ケース数: {len(adverb_cases)}")

if len(adverb_cases) > 0:
    print("\n📋 副詞テストケース一覧:")
    test_ids = []
    for i, case in enumerate(adverb_cases):
        test_id = case.get('test_id', i+1)  # test_idがない場合はインデックス使用
        text = case.get('text', case.get('sentence', 'N/A'))  # textまたはsentence
        v_group = case.get('V_group_key', 'unknown')
        test_ids.append(test_id)
        print(f"{i+1:2d}. test_id={test_id if test_id is not None else i+1:2d}, V_group={v_group:10s}, text=\"{text}\"")

    # test_idの範囲計算
    valid_test_ids = [tid for tid in test_ids if tid is not None and isinstance(tid, int)]
    if valid_test_ids:
        print(f"\n🎯 副詞テスト範囲: test_id {min(valid_test_ids)} - {max(valid_test_ids)}")
    else:
        print(f"\n🎯 副詞テスト範囲: インデックス 1 - {len(adverb_cases)}")
else:
    print("❌ 副詞ケースが見つかりませんでした")
