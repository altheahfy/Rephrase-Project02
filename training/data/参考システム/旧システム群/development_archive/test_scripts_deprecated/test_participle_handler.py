#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # ハンドラーリストの確認
    print("🔍 登録されたハンドラー:")
    for i, handler in enumerate(mapper.active_handlers):
        print(f"  {i+1}. {handler}")
    
    # Case 49の実行過程をデバッグ
    sentence = "The team working overtime completed the project successfully yesterday."
    print(f"\n🧪 実行テスト: {sentence}")
    
    # ステップごとの実行を追跡
    print("\n🔧 Stanza解析結果:")
    doc = mapper.nlp(sentence)
    stanza_sentence = doc.sentences[0]
    
    for word in stanza_sentence.words:
        print(f"  ID:{word.id:2} {word.text:12} | POS:{word.upos:4} | xPOS:{word.xpos:4} | HEAD:{word.head:2} | DEP:{word.deprel:10}")
    
    # 分詞構文ハンドラーを直接テスト
    print(f"\n🔧 分詞構文ハンドラー直接テスト:")
    base_result = {'slots': {}, 'sub_slots': {}}
    
    # 検出テスト
    participle_info = mapper._analyze_participle_structure(stanza_sentence)
    if participle_info:
        print(f"  ✅ 分詞構文検出成功: {participle_info}")
        
        # 処理テスト
        result = mapper._process_participle_construction(stanza_sentence, participle_info, base_result)
        print(f"  ✅ 処理結果: {result}")
    else:
        print(f"  ❌ 分詞構文検出失敗")

if __name__ == "__main__":
    main()
