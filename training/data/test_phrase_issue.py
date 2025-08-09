#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_phrase_issue():
    """ユーザーの報告した問題の具体的テスト"""
    
    # エンジン初期化
    try:
        engine = CompleteRephraseParsingEngine()
        print("✅ Rephraseエンジン初期化完了")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return

    # 問題の例文をテスト
    test_sentences = [
        "I sleep on the bed.",
        "I see the building.",
        "I talk to a bald man.",
        "The cat is under the table.",
        "She lives in the house."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"テスト文: {sentence}")
        print('='*60)
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # 結果構造を確認
            if 'slots' in result:
                slots_data = result['slots']
                print(f"\n📊 スロット分析:")
                
                # スロットごとに詳細分析
                for slot, items in slots_data.items():
                    if not items:
                        continue
                        
                    print(f"\n  {slot}:")
                    for item in items:
                        item_type = "PHRASE" if item.get('type') == 'phrase' else "word"
                        content = item.get('content', 'EMPTY_CONTENT')
                        print(f"    - '{content}' [{item_type}]")
                        print(f"      🔍 詳細: {item}")
                        
                        # PHRASEの場合、動詞の有無をチェック
                        if item.get('type') == 'phrase':
                            print(f"      ❌ 不正なPHRASE: '{content}'")
                        
        except Exception as e:
            print(f"❌ パースエラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_phrase_issue()
