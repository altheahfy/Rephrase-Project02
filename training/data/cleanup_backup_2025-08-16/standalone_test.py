#!/usr/bin/env python3
"""
Unified Stanza-Rephrase Mapper - スタンドアロン単体テスト
ローカル環境での個別文章処理テスト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

def test_single_sentence():
    """単一文章のテスト"""
    print("🧪 スタンドアロンテスト開始...")
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
    
    # ハンドラー追加
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    print("✅ ハンドラー追加完了")
    
    # テスト文章
    test_sentences = [
        "The car which we saw was red.",
        "The book I read was interesting.",
        "The letter was written by her.",
        "The person standing there is my friend."
    ]
    
    print("\n" + "="*60)
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📖 テスト{i}: {sentence}")
        print("-" * 40)
        
        try:
            result = mapper.process(sentence)
            
            print(f"✅ 処理成功 ({result['meta']['processing_time']:.3f}s)")
            print(f"📊 メインスロット: {result['slots']}")
            print(f"📊 サブスロット: {result['sub_slots']}")
            
            # 関係代名詞情報
            grammar_info = result.get('grammar_info', {})
            if 'relative_clause' in grammar_info.get('detected_patterns', []):
                rel_contrib = grammar_info['handler_contributions']['relative_clause']
                print(f"🔍 関係節: {rel_contrib['rel_pronoun']} ({rel_contrib['rel_type']})")
            
            # 受動態情報
            if 'passive_voice' in grammar_info.get('detected_patterns', []):
                pass_contrib = grammar_info['handler_contributions']['passive_voice']
                print(f"🔄 受動態: {pass_contrib['passive_type']}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    # 統計表示
    stats = mapper.get_stats()
    print(f"\n📈 処理統計:")
    print(f"  総処理数: {stats['processing_count']}")
    print(f"  平均処理時間: {stats['average_processing_time']:.3f}s")
    print(f"  ハンドラー成功: {stats['handler_success_count']}")

def test_interactive_mode():
    """対話モード"""
    print("\n🎮 対話モードテスト（'quit'で終了）")
    
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')  # ログ抑制
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    
    print("✅ 対話モード準備完了")
    
    while True:
        try:
            sentence = input("\n📝 テスト文章を入力: ").strip()
            
            if sentence.lower() in ['quit', 'exit', 'q']:
                break
            
            if not sentence:
                continue
                
            print(f"🔍 処理中: {sentence}")
            result = mapper.process(sentence)
            
            print(f"⏱️  処理時間: {result['meta']['processing_time']:.3f}s")
            print(f"📊 結果: {json.dumps(result['slots'], ensure_ascii=False, indent=2)}")
            
            if result['sub_slots']:
                print(f"📋 サブスロット: {json.dumps(result['sub_slots'], ensure_ascii=False, indent=2)}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    print("\n👋 対話モード終了")

if __name__ == "__main__":
    print("🚀 Unified Stanza-Rephrase Mapper - スタンドアロンテスト")
    print("="*60)
    
    # 単体テスト
    test_single_sentence()
    
    # 対話モード（オプション）
    user_input = input("\n🎮 対話モードも試しますか？ (y/n): ").strip().lower()
    if user_input in ['y', 'yes']:
        test_interactive_mode()
    
    print("\n🎉 テスト完了！")
