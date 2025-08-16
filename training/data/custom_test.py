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
    
    # 実装済み4ハンドラー完全対応版54例文（正解データと完全一致版）
    your_test_sentences = [
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
