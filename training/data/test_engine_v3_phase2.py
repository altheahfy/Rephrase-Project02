#!/usr/bin/env python3
"""
Pure Stanza Engine v3 Phase 2 テスト
助動詞、受動態、疑問文、否定文など高頻度構文の動作確認
"""

from pure_stanza_engine_v3 import PureStanzaEngineV3

def test_engine_v3_phase2():
    """v3エンジンの高頻度構文テスト"""
    
    engine = PureStanzaEngineV3()
    
    # Phase 2: 高頻度構文のテスト
    test_sentences = [
        # 助動詞
        "I can swim.",
        "She will come.",
        "They have finished.",
        "We will have done it.",
        
        # 受動態
        "The book was read.",
        "It is being built.",
        "The letter will be sent.",
        
        # 疑問文
        "What is this?",
        "Where did you go?",
        "Who will come?",
        
        # 否定文
        "I don't know.",
        "She hasn't arrived.",
        "They won't come.",
        
        # There構文
        "There is a book.",
        "There will be a meeting.",
        
        # 復習: 基本文型
        "He is happy.",
        "I like you.",
        "We made him happy.",
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
    test_engine_v3_phase2()
