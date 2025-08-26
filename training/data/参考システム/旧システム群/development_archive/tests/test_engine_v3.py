#!/usr/bin/env python3
"""
Pure Stanza Engine v3 テスト
ゼロハードコーディング版の動作確認
"""

from pure_stanza_engine_v3 import PureStanzaEngineV3

def test_engine_v3():
    """v3エンジンの基本動作テスト"""
    
    engine = PureStanzaEngineV3()
    
    # 基本5文型のテスト
    test_sentences = [
        # 第1文型 (SV)
        "Birds fly.",
        "The sun rises.",
        
        # 第2文型 (SVC)  
        "He is happy.",
        "She is a teacher.",
        "They are in the room.",
        "The sky looks blue.",
        
        # 第3文型 (SVO)
        "I like you.",
        "She reads books.",
        
        # 第4文型 (SVOO)
        "I gave him a book.",
        "She told me the truth.",
        
        # 第5文型 (SVOC)
        "We made him happy.",
        "I found it interesting.",
        
        # 修飾語テスト
        "The tall man walks quickly.",
        "She is very intelligent.",
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
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_engine_v3()
