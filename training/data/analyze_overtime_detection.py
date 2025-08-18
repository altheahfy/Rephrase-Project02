#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # Case 49でovertime検出問題を分析
    sentence = "The team working overtime completed the project successfully yesterday."
    print(f"🧪 Case 49 修飾語検出分析: {sentence}")
    
    # Stanza解析結果
    doc = mapper.nlp(sentence)
    stanza_sentence = doc.sentences[0]
    
    print(f"\n🔧 Stanza解析結果:")
    for word in stanza_sentence.words:
        marker = ""
        if word.text == "overtime":
            marker = " ← 検出対象"
        elif word.text in ["successfully", "yesterday"]:
            marker = " ← メイン副詞"
        print(f"  ID:{word.id:2} {word.text:12} | POS:{word.upos:4} | xPOS:{word.xpos:4} | HEAD:{word.head:2} | DEP:{word.deprel:10}{marker}")
    
    print(f"\n🎯 副詞検出すべき要素:")
    print(f"  - overtime (ID:4, HEAD:3=working, DEP:obj) → 分詞の目的語だが副詞的")
    print(f"  - successfully (ID:8, HEAD:9=yesterday, DEP:advmod) → メイン副詞")
    print(f"  - yesterday (ID:9, HEAD:5=completed, DEP:obl:unmarked) → メイン副詞")
    
    print(f"\n💡 副詞ハンドラーは 'overtime' を検出できるか？")
    print(f"   POSが NOUN なので通常の副詞検出にはかからない")
    print(f"   分詞構文特有の修飾語として特別処理が必要")

if __name__ == "__main__":
    main()
