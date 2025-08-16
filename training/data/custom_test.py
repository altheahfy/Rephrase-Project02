#!/usr/bin/env python3
"""
カスタム例文テスト - ここに好きな例文を追加してテスト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_custom_sentences():
    """カスタム例文テスト"""
    print("🧪 カスタム例文テスト開始")
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    
    # 全ハンドラーを追加（Phase 4統合完了版）
    mapper.add_handler('basic_five_pattern')  # 🎯 基本5文型ハンドラー追加！
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    mapper.add_handler('adverbial_modifier')  # 🎯 副詞エンジン追加！
    print("✅ システム準備完了")
    
    # 正解データベースに基づく54例文（expected_results_progress.jsonから取得）
    your_test_sentences = [
        "I love you.",
        "She reads books.",
        "The cat sleeps.",
        "He gives me a book.",
        "I find it interesting.",
        "The book is good.",
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
        "I eat breakfast every morning.",
        "She studies English twice a week.",
        "He visits his grandmother on Sundays.",
        "We go to the beach in summer.",
        "They play tennis after school.",
        "I will call you tomorrow.",
        "She is going to visit Paris next month.",
        "He has finished his homework.",
        "The letter was written by John.",
        "The house was built in 1990.",
        "The book was written by a famous author.",
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
    
    print(f"\n📖 テスト例文数: {len(your_test_sentences)}")
    print("="*60)
    
    success_count = 0
    for i, sentence in enumerate(your_test_sentences, 1):
        print(f"\n🧪 テスト{i:2d}: {sentence}")
        print("-" * 50)
        
        try:
            result = mapper.process(sentence)
            processing_time = result['meta']['processing_time']
            
            print(f"⏱️  処理時間: {processing_time:.3f}秒")
            
            # 結果詳細表示
            slots = result.get('slots', {})
            sub_slots = result.get('sub_slots', {})
            
            if slots or sub_slots:
                print("📊 分解結果:")
                
                # メインスロット
                if slots:
                    for slot, value in slots.items():
                        if value.strip():  # 空でない場合
                            print(f"  {slot:4s}: {value}")
                
                # サブスロット
                if sub_slots:
                    print("  サブスロット:")
                    for slot, value in sub_slots.items():
                        print(f"    {slot}: {value}")
                
                success_count += 1
                print("✅ 分解成功")
            else:
                print("📊 分解結果: スロット検出なし")
                print("⚠️  単純文として処理")
            
            # 特別パターン検出
            grammar_info = result.get('grammar_info', {})
            patterns = grammar_info.get('detected_patterns', [])
            if patterns:
                pattern_names = {
                    'relative_clause': '関係代名詞節',
                    'passive_voice': '受動態'
                }
                detected = [pattern_names.get(p, p) for p in patterns]
                print(f"🔍 検出パターン: {', '.join(detected)}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    # 最終統計
    stats = mapper.get_stats()
    print(f"\n📈 最終統計:")
    print(f"  総テスト数: {len(your_test_sentences)}")
    print(f"  分解成功数: {success_count}")
    print(f"  成功率: {success_count/len(your_test_sentences)*100:.1f}%")
    print(f"  平均処理時間: {stats['average_processing_time']:.3f}秒")
    print(f"  ハンドラー成功: {stats['handler_success_count']}")
    
    print("\n🎉 カスタム例文テスト完了！")

if __name__ == "__main__":
    test_custom_sentences()
