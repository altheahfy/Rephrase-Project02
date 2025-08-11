#!/usr/bin/env python3
"""
Pure Stanza Engine v3 従属節・複文テスト
「even though he was under intense pressure」などの複文構造の確認
"""

from pure_stanza_engine_v3 import PureStanzaEngineV3

def test_complex_sentences():
    """従属節・複文のテスト"""
    
    engine = PureStanzaEngineV3()
    
    # 複文・従属節のテスト
    test_sentences = [
        # 従属節（単体）
        "even though he was under intense pressure",
        "because she is very intelligent",
        "while they are working",
        "if you like books",
        
        # 主節 + 従属節
        "He succeeded even though he was under intense pressure.",
        "She passed the test because she is very intelligent.",
        "We waited while they are working.",
        "I will help you if you need it.",
        
        # 関係節
        "The man who is tall walks quickly.",
        "The book that she reads is interesting.",
        
        # その他の複文
        "I know that he is happy.",
        "She said she will come.",
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"テスト文: {sentence}")
        print(f"{'='*80}")
        
        try:
            result = engine.decompose(sentence)
            
            print(f"\n📊 分解結果:")
            for slot_name, slot_data in result.items():
                main_text = slot_data.get('main', '<なし>')
                print(f"  {slot_name}: '{main_text}'")
                
            # 特に従属節の処理を確認
            if 'M2' in result or 'M3' in result:
                print("🔍 修飾句/従属節が検出されました")
            elif not result:
                print("⚠️ スロットが検出されませんでした（文型パターン未対応の可能性）")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_complex_sentences()
