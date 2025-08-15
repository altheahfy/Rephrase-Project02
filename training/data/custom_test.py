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
        # 基本例文
        "The car is red.",
        "I love you.",
        
        # 関係代名詞例文（明示的）
        "The man who lives there is kind.",
        "The book which I bought is expensive.", 
        "The place where we met is beautiful.",
        
        # 関係代名詞例文（省略）
        "The book I read yesterday was boring.",
        "The person standing over there is my teacher.",
        "The movie we watched last night was amazing.",
        
        # 受動態例文
        "The window was broken.",
        "The letter was written by John.",
        "The house was built in 1990.",
        "The cake was eaten by the children.",
        
        # 複合例文
        "The book which was written by Shakespeare is famous.",
        "The car that was bought by him is expensive.",
        
        # ここに新しい例文を追加 ↓
        # "Your sentence here...",
        # "Another sentence...",
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
