#!/usr/bin/env python3
"""
Pure Stanza Engine v3 be動詞・短文テスト
以前に失敗していた文の改善確認
"""

from pure_stanza_engine_v3 import PureStanzaEngineV3

def test_problematic_sentences():
    """以前に問題があった文のテスト"""
    
    engine = PureStanzaEngineV3()
    
    # 以前に問題があった文
    test_sentences = [
        # be動詞構文（以前の問題文）
        "He is happy.",
        "She is very intelligent.",
        "He is a teacher.",
        "They are in the room.",
        "He was under intense pressure.",
        
        # 短い基本文
        "I like you.",
        "Birds fly.",
        "She reads books.",
        
        # 複雑なbe動詞
        "The sky looks blue.",
        "She is a brilliant student.",
        
        # 助動詞付きbe動詞（新パターン）
        "He will be happy.",
        "They can be teachers.",
        "She must be intelligent.",
        
        # その他の短文
        "We see the mountain.",
        "I gave him a book.",
        "We made him happy.",
    ]
    
    success_count = 0
    total_count = len(test_sentences)
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"テスト文: {sentence}")
        print(f"{'='*80}")
        
        try:
            result = engine.decompose(sentence)
            
            print(f"\n📊 分解結果:")
            slots_found = []
            for slot_name, slot_data in result.items():
                main_text = slot_data.get('main', '<なし>')
                print(f"  {slot_name}: '{main_text}'")
                if main_text and main_text != '<なし>':
                    slots_found.append(slot_name)
            
            if slots_found:
                success_count += 1
                print(f"✅ 成功 - 検出スロット数: {len(slots_found)}")
            else:
                print(f"❌ 失敗 - スロット検出なし")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    print(f"\n{'='*80}")
    print(f"📊 総合結果")
    print(f"{'='*80}")
    print(f"成功: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 全ての問題文が解決されました！")
    elif success_count > total_count * 0.8:
        print("🎯 大部分の問題が解決されました")
    else:
        print("⚠️ まだ改善が必要です")

if __name__ == "__main__":
    test_problematic_sentences()
