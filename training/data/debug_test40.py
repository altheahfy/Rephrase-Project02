#!/usr/bin/env python3
"""
Test 40の問題分析用デバッグスクリプト
"""

import json
import sys
import os

# パスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    test_sentence = "The house whose roof was damaged badly needs immediate repair."
    print(f"分析対象: {test_sentence}")
    
    try:
        mapper = UnifiedStanzaRephraseMapper()
        
        # 内部メソッドを直接呼び出し
        doc = mapper.nlp(test_sentence)
        
        # Stanza解析結果を詳しく見る
        print("\n=== Stanza解析結果 ===")
        sentence = doc.sentences[0]
        for word in sentence.words:
            print(f"ID:{word.id} '{word.text}' head:{word.head} deprel:{word.deprel} upos:{word.upos}")
        
        result = mapper._unified_mapping(test_sentence, doc)
        
        print("\n=== システム出力結果 ===")
        print(f"Main slots: {result.get('slots', {})}")
        print(f"Sub slots: {result.get('sub_slots', {})}")
        
        # "badly"がどこに配置されているかチェック
        main_slots = result.get('slots', {})
        sub_slots = result.get('sub_slots', {})
        
        badly_location = None
        for slot, value in main_slots.items():
            if 'badly' in str(value):
                badly_location = f"main-{slot}"
                break
        
        if not badly_location:
            for slot, value in sub_slots.items():
                if 'badly' in str(value):
                    badly_location = f"sub-{slot}"
                    break
        
        print(f"\n'badly'の配置: {badly_location}")
        
        # 期待値と比較
        expected_badly = "sub-m2"  # 関係詞節内なのでsub-m2に配置されるべき
        actual_badly = badly_location
        
        print(f"期待値: {expected_badly}")
        print(f"実際値: {actual_badly}")
        print(f"一致: {'✅' if expected_badly == actual_badly else '❌'}")
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
