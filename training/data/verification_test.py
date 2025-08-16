#!/usr/bin/env python3
"""
精度検証テスト - expected_results_progress.jsonと実際の出力を詳細比較
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def load_expected_results():
    """正解データを読み込み"""
    with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['correct_answers']

def compare_slots(expected, actual, sentence_num, sentence):
    """スロット結果を詳細比較"""
    print(f"\n🔍 検証 {sentence_num}: {sentence}")
    print("-" * 80)
    
    # 期待値
    exp_main = expected.get('main_slots', {})
    exp_sub = expected.get('sub_slots', {})
    
    # 実際の結果
    act_main = actual.get('slots', {})
    act_sub = actual.get('sub_slots', {})
    
    # メインスロット比較
    main_match = True
    print("📊 メインスロット比較:")
    
    all_main_keys = set(exp_main.keys()) | set(act_main.keys())
    for key in sorted(all_main_keys):
        exp_val = exp_main.get(key, "").strip()
        act_val = act_main.get(key, "").strip()
        
        if exp_val or act_val:  # どちらかが空でない場合のみ表示
            match = exp_val == act_val
            if not match:
                main_match = False
            status = "✅" if match else "❌"
            print(f"  {key:4s}: 期待='{exp_val}' | 実際='{act_val}' {status}")
    
    # サブスロット比較
    sub_match = True
    if exp_sub or act_sub:
        print("📊 サブスロット比較:")
        
        all_sub_keys = set(exp_sub.keys()) | set(act_sub.keys())
        for key in sorted(all_sub_keys):
            exp_val = exp_sub.get(key, "").strip()
            act_val = act_sub.get(key, "").strip()
            
            if exp_val or act_val:  # どちらかが空でない場合のみ表示
                match = exp_val == act_val
                if not match:
                    sub_match = False
                status = "✅" if match else "❌"
                print(f"    {key}: 期待='{exp_val}' | 実際='{act_val}' {status}")
    
    overall_match = main_match and sub_match
    status_emoji = "✅" if overall_match else "❌"
    print(f"📈 総合判定: {status_emoji} {'完全一致' if overall_match else '不一致'}")
    
    return overall_match

def main():
    """メイン検証処理"""
    print("🔍 精度検証テスト開始 - 正解データとの詳細比較")
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')  # ログ抑制
    mapper.add_handler('basic_five_pattern')
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')
    
    # 正解データ読み込み
    expected_results = load_expected_results()
    
    # テスト例文（custom_test.pyと同じ順序）
    test_sentences = [
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
        "The door opened slowly creaked loudly.",
        "The book which was written by Shakespeare is famous.",
        "The car that was bought by him is expensive.",
        "The letter which was sent by her arrived today.",
        "The house where I was born is in Tokyo.",
        "The day when we first met was sunny.",
        "The reason why he quit was personal.",
        "The man who carefully drives slowly is cautious.",
        "The book which I recently bought is interesting.",
        "The place where we often go is crowded.",
        "The man who owns the car that was stolen is angry.",
        "The book which I read that was recommended is good.",
        "The student who studies harder than others will succeed.",
        "The car which runs faster than mine is expensive.",
        "The person who can speak French is helpful.",
        "The student who must study hard will pass.",
        "The man who should arrive soon is late.",
        "The book which I have read is interesting.",
        "The man who had left returned yesterday.",
        "The project which will have finished is important.",
        "The person who is running there is my brother.",
        "The car which was moving fast stopped suddenly.",
        "The man who runs fast and works hard is successful.",
        "The book which I bought but haven't read is thick.",
        "The place where we lived when I was young is gone.",
        "The window was broken.",
        "The letter was written by John.",
        "The house was built in 1990.",
        "The cake was eaten by the children."
    ]
    
    perfect_matches = 0
    total_tests = len(test_sentences)
    
    for i, sentence in enumerate(test_sentences, 1):
        try:
            # 実際の処理実行
            result = mapper.process(sentence)
            
            # 期待値取得（正しいパス）
            expected_entry = expected_results.get(str(i), {})
            expected = expected_entry.get('expected', {})
            
            # 詳細比較
            is_match = compare_slots(expected, result, i, sentence)
            
            if is_match:
                perfect_matches += 1
                
        except Exception as e:
            print(f"❌ 例文 {i} でエラー: {e}")
    
    # 最終結果
    print("\n" + "="*80)
    print("🎯 最終検証結果")
    print("="*80)
    print(f"📊 総テスト数: {total_tests}")
    print(f"📊 完全一致数: {perfect_matches}")
    print(f"📊 不一致数: {total_tests - perfect_matches}")
    print(f"📊 精度: {perfect_matches/total_tests*100:.1f}%")
    
    if perfect_matches == total_tests:
        print("\n🎉 すべてのテストが正解データと完全一致！詐欺なし！")
    else:
        print(f"\n⚠️  {total_tests - perfect_matches}件の不一致があります。詳細を確認してください。")

if __name__ == "__main__":
    main()
