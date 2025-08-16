#!/usr/bin/env python3
"""
Revert後の状態確認テスト
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_clean_state():
    print("🧪 Revert後の状態確認")
    print("=" * 40)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper()
    mapper.add_handler('relative_clause')
    mapper.add_handler('basic_five_pattern')
    
    # テスト例文
    test_sentence = "The car which was stolen is expensive"
    print(f"📖 テスト例文: '{test_sentence}'")
    print("-" * 40)
    
    try:
        result = mapper.process(test_sentence)
        
        # 結果表示
        print("✅ 処理成功")
        print(f"メインスロット: {len(result.get('slots', {}))} 個")
        print(f"サブスロット: {len(result.get('sub_slots', {}))} 個")
        
        # メインスロット詳細
        if result.get('slots'):
            print("\n📊 メインスロット:")
            for slot, value in result['slots'].items():
                print(f"  {slot}: '{value}'")
        
        # サブスロット詳細  
        if result.get('sub_slots'):
            print("\n🎯 サブスロット:")
            for sub_slot, value in result['sub_slots'].items():
                print(f"  {sub_slot}: '{value}'")
        
        # positional_sub_slotsの確認
        if result.get('positional_sub_slots'):
            print("\n⚠️ positional_sub_slots が残存")
            print("order機能の残骸が残っています")
        else:
            print("\n✅ positional_sub_slots なし - クリーン状態")
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_clean_state()
    print("\n🏁 状態確認完了")
