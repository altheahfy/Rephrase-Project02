#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
54例文の完全テストデータ統合
- 破損した23例文: confirmed_correct_answers.jsonから取得
- 正常な31例文: expected_results_progress.jsonから取得
- 結果: final_test_data.json として出力
"""

import json
import codecs

def extract_custom_test_sentences():
    """custom_test.pyから54例文を抽出"""
    sentences = [
        "The car is red.",
        "I love you.",
        "The man who runs fast is strong.",
        "The book which lies there is mine.",
        "The person that works here is kind.",
        "The book which I bought is expensive.",
        "The man whom I met is tall.",
        "The car that he drives is new.",
        "The car which was crashed is red.",
        "The book that was written is famous.",
        "The letter which was sent arrived.",
        "The man whose car is red lives here.",
        "The student whose book I borrowed is smart.",
        "The woman whose dog barks is my neighbor.",
        "The place where we met is beautiful.",
        "The time when he arrived was late.",
        "The reason why she left is unclear.",
        "The way how he solved it was clever.",
        "The book I read yesterday was boring.",
        "The movie we watched last night was amazing.",
        "The food she cooked was delicious.",
        "The person you mentioned is here.",
        "The person standing there is my friend.",
        "The car parked outside is mine.",
        "The students studying hard will succeed.",
        "The building under construction is tall.",
        "The woman running in the park is fit.",
        "The children playing in the garden are happy.",
        "The dog sleeping on the sofa is cute.",
        "The picture hanging on the wall is beautiful.",
        "The letter lying on the table is important.",
        "The cake being baked smells good.",
        "The car being washed is mine.",
        "The house being built is modern.",
        "The song being played is relaxing.",
        "The movie being watched is exciting.",
        "The book being read is interesting.",
        "The project being completed is important.",
        "The cake is being baked by my mother.",
        "The cake was eaten by the children.",
        "The door was opened by the key.",
        "The message was sent yesterday.",
        "If it rains, I stay home.",
        "She acts as if she knows everything.",
        "The students study hard for exams.",
        "The car was repaired last week.",
        "The book was published in 2020.",
        "I went to the store and bought some milk.",
        "She was tired, but she continued working.",
        "Although it was raining, we went for a walk.",
        "Because he was late, he missed the train.",
        "The room was cleaned this morning.",
        "The man who is standing there is my father.",
        "The girl whom I met yesterday is very smart.",
        "The house that we visited last week is for sale.",
        "The teacher whose class I attended was excellent."
    ]
    return sentences

def load_confirmed_answers():
    """確認済み23例文の正解データを読み込み"""
    try:
        with codecs.open('confirmed_correct_answers.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('correct_answers', {})
    except FileNotFoundError:
        print("❌ confirmed_correct_answers.json が見つかりません")
        return {}

def load_expected_results():
    """既存の54例文正解データを読み込み"""
    try:
        with codecs.open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ expected_results_progress.json が見つかりません")
        return {}

def integrate_test_data():
    """54例文の完全テストデータを統合"""
    
    print("🔧 54例文完全テストデータ統合開始")
    print("=" * 60)
    
    # データ読み込み
    custom_sentences = extract_custom_test_sentences()
    confirmed_data = load_confirmed_answers()
    expected_data = load_expected_results()
    
    print(f"📖 custom_test.py例文数: {len(custom_sentences)}")
    print(f"✅ 確認済み正解データ: {len(confirmed_data)}")
    print(f"📊 既存正解データ: {len(expected_data)}")
    
    # 統合データ作成
    final_test_data = {
        "meta": {
            "description": "54例文完全テストセット", 
            "confirmed_count": len(confirmed_data),
            "existing_count": 0,
            "total_count": len(custom_sentences),
            "integration_date": "2025-08-17"
        },
        "data": {}
    }
    
    # 各例文を処理
    confirmed_ids = set(confirmed_data.keys())
    
    for i, sentence in enumerate(custom_sentences, 1):
        test_id = str(i)
        
        # 確認済みデータを優先使用
        if test_id in confirmed_ids:
            final_test_data['data'][test_id] = confirmed_data[test_id]
            print(f"✅ {i:2d}: 確認済みデータ使用 - {sentence[:50]}...")
        
        # 既存データを使用（破損チェック付き）
        elif test_id in expected_data:
            existing = expected_data[test_id]
            # 文の一致確認
            if existing.get('sentence', '').strip() == sentence.strip():
                final_test_data['data'][test_id] = existing
                final_test_data['meta']['existing_count'] += 1
                print(f"📊 {i:2d}: 既存データ使用 - {sentence[:50]}...")
            else:
                # 破損データの場合は空で保持
                final_test_data['data'][test_id] = {
                    "sentence": sentence,
                    "expected": {},
                    "status": "破損データ・要手動確認"
                }
                print(f"❌ {i:2d}: 破損データ検出 - {sentence[:50]}...")
        
        else:
            # データなしの場合
            final_test_data['data'][test_id] = {
                "sentence": sentence,
                "expected": {},
                "status": "データなし・要手動確認"
            }
            print(f"⚠️  {i:2d}: データなし - {sentence[:50]}...")
    
    # 結果保存
    with codecs.open('final_test_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_test_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 統合結果:")
    print(f"  確認済み正解データ: {len(confirmed_ids)}件")
    print(f"  既存有効データ: {final_test_data['meta']['existing_count']}件")
    print(f"  総統合データ: {len(final_test_data['data'])}件")
    print(f"\n💾 final_test_data.json に保存完了")
    
    return final_test_data

if __name__ == "__main__":
    integrate_test_data()
