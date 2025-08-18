#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def main():
    mapper = UnifiedStanzaRephraseMapper()
    
    # Case 49の処理順序を詳細分析
    sentence = "The team working overtime completed the project successfully yesterday."
    print(f"🧪 処理順序分析: {sentence}")
    
    # Stanza解析
    doc = mapper.nlp(sentence)
    stanza_sentence = doc.sentences[0]
    
    print(f"\n🔧 Stanza解析結果:")
    for word in stanza_sentence.words:
        print(f"  ID:{word.id:2} {word.text:12} | POS:{word.upos:4} | xPOS:{word.xpos:4} | HEAD:{word.head:2} | DEP:{word.deprel:10}")
    
    print(f"\n📋 ハンドラー実行順序:")
    for i, handler in enumerate(mapper.active_handlers):
        print(f"  {i+1}. {handler}")
    
    # 各ハンドラーの期待される動作
    print(f"\n🎯 各ハンドラーの期待動作:")
    print(f"  1. basic_five_pattern: S=team, V=completed, O1=project")
    print(f"  2. relative_clause: (スキップすべき)")
    print(f"  3. passive_voice: (該当なし)")
    print(f"  4. participle_construction: S='', sub-v='the team working'")
    print(f"  5. adverbial_modifier: M2=successfully, M3=yesterday, sub-m2=overtime")
    print(f"  6. auxiliary_complex: (該当なし)")
    
    print(f"\n💡 提案: 分詞構文ハンドラーは構造分解のみ、副詞処理は副詞ハンドラーに委譲")

if __name__ == "__main__":
    main()
