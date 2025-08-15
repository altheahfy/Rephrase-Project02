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
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    print("✅ システム準備完了")
    
    # ここに好きな例文を追加してください！
    your_test_sentences = [
        # === 基本例文 ===
        "The car is red.",
        "I love you.",
        
        # === 関係代名詞（明示的） ===
        
        ## 主語関係代名詞
        "The man who runs fast is strong.",              # who + 能動態
        "The book which lies there is mine.",            # which + 能動態  
        "The person that works here is kind.",           # that + 能動態
        
        ## 目的語関係代名詞
        "The book which I bought is expensive.",         # which + 能動態
        "The man whom I met is tall.",                   # whom（正式）
        "The car that he drives is new.",                # that + 能動態
        
        ## 受動態関係代名詞
        "The car which was crashed is red.",             # which + 受動態
        "The book that was written is famous.",          # that + 受動態
        "The letter which was sent arrived.",            # which + 受動態
        
        ## 所有格関係代名詞
        "The man whose car is red lives here.",          # whose + 所有
        "The student whose book I borrowed is smart.",   # whose + 複合
        "The woman whose dog barks is my neighbor.",     # whose + 能動態
        
        # === 関係副詞 ===
        "The place where we met is beautiful.",          # where（場所）
        "The time when he arrived was late.",            # when（時間）
        "The reason why she left is unclear.",           # why（理由）
        "The way how he solved it was clever.",          # how（方法）
        
        # === 関係代名詞（省略） ===
        
        ## 省略目的語関係代名詞（能動態）
        "The book I read yesterday was boring.",         # [that] I read
        "The movie we watched last night was amazing.",  # [which] we watched
        "The food she cooked was delicious.",            # [that] she cooked
        "The person you mentioned is here.",             # [whom] you mentioned
        
        ## 省略主語関係代名詞（分詞構文）
        "The person standing there is my friend.",       # [who is] standing
        "The car parked outside is mine.",               # [which is] parked
        "The students studying hard will succeed.",      # [who are] studying
        "The door opened slowly creaked loudly.",        # [which was] opened
        
        # === 複雑な関係節 ===
        
        ## 関係節 + 受動態 + by句
        "The book which was written by Shakespeare is famous.",     # 完全受動態
        "The car that was bought by him is expensive.",             # by句付き
        "The letter which was sent by her arrived today.",         # 時間副詞付き
        
        ## 関係節 + 前置詞句
        "The house where I was born is in Tokyo.",                 # where + 場所
        "The day when we first met was sunny.",                    # when + 形容詞
        "The reason why he quit was personal.",                    # why + 形容詞
        
        ## 関係節 + 修飾語
        "The man who carefully drives slowly is cautious.",        # 副詞修飾
        "The book which I recently bought is interesting.",        # 時間副詞
        "The place where we often go is crowded.",                 # 頻度副詞
        
        ## 二重関係節（入れ子）
        "The man who owns the car that was stolen is angry.",      # 関係節in関係節
        "The book which I read that was recommended is good.",     # 二重関係
        
        # === 特殊構造 ===
        
        ## 関係節 + 比較級
        "The student who studies harder than others will succeed.", # 比較構造
        "The car which runs faster than mine is expensive.",        # 比較 + 所有格
        
        ## 関係節 + 助動詞
        "The person who can speak French is helpful.",              # can + 動詞
        "The student who must study hard will pass.",               # must + 動詞
        "The man who should arrive soon is late.",                  # should + 動詞
        
        ## 関係節 + 完了形
        "The book which I have read is interesting.",               # 現在完了
        "The man who had left returned yesterday.",                 # 過去完了
        "The project which will have finished is important.",      # 未来完了
        
        ## 関係節 + 進行形
        "The person who is running there is my brother.",           # 現在進行形
        "The car which was moving fast stopped suddenly.",         # 過去進行形
        
        # === 複合文 ===
        "The man who runs fast and works hard is successful.",     # 並列関係節
        "The book which I bought but haven't read is thick.",      # 対比関係節
        "The place where we lived when I was young is gone.",      # 時間 + 場所関係節
        
        # === 受動態例文（対比用） ===
        "The window was broken.",
        "The letter was written by John.",
        "The house was built in 1990.",
        "The cake was eaten by the children."
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
