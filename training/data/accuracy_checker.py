#!/usr/bin/env python3
"""
正確性検証スクリプト - システム出力と正解データベースの詳細照合
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json
from datetime import datetime

# 54例文リスト（custom_test.pyと同じ）
SENTENCES = [
    "I love you.",
    "She reads books.",
    "The cat sleeps.",
    "He gives me a book.",
    "I find it interesting.",
    "The flowers are beautiful.",
    "I eat breakfast every morning.",
    "She studies English twice a week.",
    "He visits his grandmother on Sundays.",
    "We go to the beach in summer.",
    "They play tennis after school.",
    "She is going to visit Paris next month.",
    "He has finished his homework.",
    "I went to the store and bought some milk.",
    "She was tired, but she continued working.",
    "Although it was raining, we went for a walk.",
    "Because he was late, he missed the train.",
    "If it rains, I stay home.",
    "She acts as if she knows everything.",
    "The students study hard for exams.",
    "The person that works here is kind.",
    "The car which was parked outside is mine.",
    "The house where I was born is old.",
    "The day when we met was sunny.",
    "The reason why he left is unclear.",
    "The man whose car was stolen called the police.",
    "I know the person that you mentioned.",
    "The book which I read was fascinating.",
    "The place where we lived was peaceful.",
    "The time when you called was perfect.",
    "The woman whose idea won the contest is my sister.",
    "I like the movie that you recommended.",
    "The restaurant where we ate was expensive.",
    "The moment when I realized the truth was shocking.",
    "I am running quickly to catch the bus.",
    "She sings beautifully at the concert.",
    "The dog barks loudly in the yard.",
    "He works diligently on his project.",
    "They dance gracefully at the party.",
    "The window was broken.",
    "The letter was written by John.",
    "The house was built in 1990.",
    "The book was written by a famous author.",
    "The cake is being baked by my mother.",
    "The cake was eaten by the children.",
    "The door was opened by the key.",
    "The message was sent yesterday.",
    "The car was repaired last week.",
    "The book was published in 2020.",
    "The room was cleaned this morning.",
    "The man who is standing there is my father.",
    "The girl whom I met yesterday is very smart.",
    "The house that we visited last week is for sale.",
    "The teacher whose class I attended was excellent."
]

def load_expected_results():
    """正解データベース読み込み"""
    try:
        with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('correct_answers', {})
    except FileNotFoundError:
        print("❌ 正解データベースが見つかりません")
        return {}

def normalize_result(result):
    """結果を正規化（比較用）"""
    if not result:
        return {"main_slots": {}, "sub_slots": {}}
    
    # main_slotsとsub_slotsを分離
    main_slots = {}
    sub_slots = {}
    
    for key, value in result.items():
        if key.startswith('sub-'):
            sub_slots[key] = value
        else:
            main_slots[key] = value
    
    return {
        "main_slots": main_slots,
        "sub_slots": sub_slots
    }

def compare_results(system_result, expected_result):
    """結果比較"""
    sys_norm = normalize_result(system_result)
    exp_norm = expected_result.get('expected', {}) if isinstance(expected_result, dict) else expected_result
    
    # 空の場合のデフォルト値
    if not exp_norm:
        exp_norm = {"main_slots": {}, "sub_slots": {}}
    
    # main_slotsの比較
    main_slots_match = sys_norm['main_slots'] == exp_norm.get('main_slots', {})
    
    # sub_slotsの比較
    sub_slots_match = sys_norm['sub_slots'] == exp_norm.get('sub_slots', {})
    
    return main_slots_match and sub_slots_match, sys_norm, exp_norm

def main():
    print("🔍 正確性検証開始 - システム出力 vs 正解データベース")
    print("=" * 60)
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='WARNING')  # ログを抑制
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    # 正解データ読み込み
    expected_results = load_expected_results()
    
    total_tests = len(SENTENCES)
    correct_matches = 0
    errors = []
    
    for i, sentence in enumerate(SENTENCES, 1):
        print(f"\n🧪 テスト {i}: {sentence}")
        print("-" * 50)
        
        # システム分解実行
        try:
            system_result = mapper.parse_sentence(sentence)
        except Exception as e:
            print(f"❌ システムエラー: {e}")
            errors.append(f"例文{i}: システムエラー - {e}")
            continue
        
        # 正解データ取得
        expected_result = expected_results.get(str(i), {})
        
        if not expected_result:
            print(f"⚠️  正解データなし（例文{i}）")
            errors.append(f"例文{i}: 正解データなし")
            continue
        
        # 結果比較
        is_match, sys_norm, exp_norm = compare_results(system_result, expected_result)
        
        if is_match:
            print("✅ 正解と一致！")
            correct_matches += 1
        else:
            print("❌ 正解と不一致")
            print(f"システム出力: {sys_norm}")
            print(f"正解データ: {exp_norm}")
            errors.append(f"例文{i}: 出力不一致")
    
    # 最終結果
    print("\n" + "=" * 60)
    print("📊 最終結果:")
    print(f"  総テスト数: {total_tests}")
    print(f"  正解一致数: {correct_matches}")
    print(f"  正確率: {correct_matches/total_tests*100:.1f}%")
    print(f"  エラー数: {len(errors)}")
    
    if errors:
        print("\n❌ エラー詳細:")
        for error in errors:
            print(f"  {error}")
    else:
        print("\n🎉 全例文で正解データと完全一致！")

if __name__ == "__main__":
    main()
