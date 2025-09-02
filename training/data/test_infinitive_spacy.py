#!/usr/bin/env python3
"""
spaCyベース不定詞ハンドラーの動作確認テスト
"""

import spacy
from infinitive_handler import InfinitiveHandler

def test_infinitive_handler():
    """不定詞ハンドラーのspaCy解析テスト"""
    
    print("🚀 spaCyベース不定詞ハンドラー動作確認開始\n")
    
    # ハンドラーのインスタンス化
    handler = InfinitiveHandler()
    
    # テスト例文セット
    test_sentences = [
        "I want to learn English.",      # xcomp不定詞
        "I came to help you.",           # advcl不定詞  
        "To study hard is important.",   # 名詞的用法
        "I have something to do.",       # 形容詞的用法
        "He decided to go home."         # ccomp不定詞
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"=" * 60)
        print(f"📝 テスト {i}: {sentence}")
        print("=" * 60)
        
        try:
            # can_handleチェック
            can_handle = handler.can_handle(sentence)
            print(f"🔍 can_handle結果: {can_handle}")
            
            if can_handle:
                # process実行
                result = handler.process(sentence)
                print(f"✅ 処理成功: {result.get('success', False)}")
                print(f"📊 メタデータ: {result.get('metadata', {})}")
                print(f"🎯 main_slots: {result.get('main_slots', {})}")
            else:
                print(f"❌ 処理対象外")
                
        except Exception as e:
            print(f"💥 エラー発生: {str(e)}")
        
        print()

if __name__ == "__main__":
    test_infinitive_handler()
