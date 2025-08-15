#!/usr/bin/env python3
"""
対話モードテスト - 自由に例文を入力してテストできます
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def main():
    print("🚀 Rephrase文法分解 - 対話テストモード")
    print("="*50)
    print("📝 英語の文章を入力すると、文法構造を分解します")
    print("💡 終了: 'quit', 'exit', 'q' を入力")
    print("="*50)
    
    # 初期化
    print("\n🔧 システム初期化中...")
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')  # ログを抑制
    
    # ハンドラー追加
    mapper.add_handler('relative_clause')   # 関係代名詞
    mapper.add_handler('passive_voice')     # 受動態
    print("✅ 初期化完了！")
    
    # 使用例表示
    print("\n📖 使用例:")
    examples = [
        "The car which we saw was red.",
        "The book I read was interesting.",
        "The letter was written by her.",
        "The person standing there is my friend."
    ]
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")
    
    print("\n" + "="*50)
    
    # 対話ループ
    test_count = 0
    while True:
        try:
            print("\n" + "-"*50)
            sentence = input("📝 英語文章を入力: ").strip()
            
            # 終了チェック
            if sentence.lower() in ['quit', 'exit', 'q', '']:
                break
            
            test_count += 1
            print(f"\n🔍 テスト{test_count}: 「{sentence}」")
            print("⏳ 処理中...")
            
            # 処理実行
            result = mapper.process(sentence)
            
            # 結果表示
            print(f"⏱️  処理時間: {result['meta']['processing_time']:.3f}秒")
            print("\n📊 **分解結果**:")
            
            # メインスロット
            slots = result.get('slots', {})
            if slots:
                print("  🎯 メインスロット:")
                for slot, value in slots.items():
                    if value:  # 空でない場合のみ表示
                        print(f"    {slot}: 「{value}」")
            else:
                print("  🎯 メインスロット: なし")
            
            # サブスロット
            sub_slots = result.get('sub_slots', {})
            if sub_slots:
                print("  📋 サブスロット:")
                for slot, value in sub_slots.items():
                    print(f"    {slot}: 「{value}」")
            
            # 文法情報
            grammar_info = result.get('grammar_info', {})
            patterns = grammar_info.get('detected_patterns', [])
            if patterns:
                print("  🔍 検出パターン:")
                for pattern in patterns:
                    if pattern == 'relative_clause':
                        contrib = grammar_info['handler_contributions']['relative_clause']
                        rel_type = contrib.get('rel_type', 'unknown')
                        rel_pronoun = contrib.get('rel_pronoun', 'unknown')
                        print(f"    📖 関係節: {rel_pronoun} ({rel_type})")
                        if rel_pronoun == '[omitted]':
                            print(f"      💡 省略関係代名詞を検出！")
                    
                    elif pattern == 'passive_voice':
                        contrib = grammar_info['handler_contributions']['passive_voice']
                        pass_type = contrib.get('passive_type', 'unknown')
                        print(f"    🔄 受動態: {pass_type}")
            else:
                print("  🔍 特別な文法パターン: 検出されず")
            
        except KeyboardInterrupt:
            print("\n\n👋 中断されました")
            break
        except Exception as e:
            print(f"❌ エラー: {e}")
            print("💡 別の文章で試してみてください")
    
    # 統計表示
    if test_count > 0:
        stats = mapper.get_stats()
        print(f"\n📈 テスト統計:")
        print(f"  総テスト数: {test_count}")
        print(f"  システム処理数: {stats['processing_count']}")
        print(f"  平均処理時間: {stats['average_processing_time']:.3f}秒")
        print(f"  成功ハンドラー: {stats['handler_success_count']}")
    
    print("\n🎉 テスト完了！お疲れ様でした。")

if __name__ == "__main__":
    main()
