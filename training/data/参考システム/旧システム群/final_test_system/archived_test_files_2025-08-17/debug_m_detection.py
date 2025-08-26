#!/usr/bin/env python3
"""
M配置問題の詳細デバッグ - なぜM配置が検出されないのか？
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import stanza

def debug_m_detection():
    """M配置検出問題をデバッグ"""
    mapper = UnifiedStanzaRephraseMapper()
    
    # テストケース
    sentence = "The message was sent yesterday."
    
    print("🔍 M配置検出詳細デバッグ")
    print("=" * 60)
    print(f"テスト文: {sentence}")
    
    # Stanza解析を手動実行
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
    doc = nlp(sentence)
    
    print("\n📝 Stanza解析結果:")
    for sent in doc.sentences:
        for word in sent.words:
            print(f"  {word.id}: {word.text} ({word.upos}, {word.deprel}, head={word.head})")
    
    # システム出力
    print("\n🔧 システム解析結果:")
    result = mapper.process(sentence)
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    # adverbial_modifierハンドラーが動いているかチェック
    print("\n🎯 ハンドラー実行状況確認:")
    print(f"ハンドラー数: {len(mapper.handlers)}")
    for handler_name in mapper.handlers:
        print(f"  - {handler_name}")
    
    print("\n🧪 手動副詞検出テスト:")
    for sent in doc.sentences:
        for word in sent.words:
            if word.text == "yesterday":
                print(f"  yesterday: upos={word.upos}, deprel={word.deprel}")
                print(f"  副詞チェック結果:")
                print(f"    - upos == 'ADV': {word.upos == 'ADV'}")
                print(f"    - deprel in advmod,obl,obl:tmod: {word.deprel in ['advmod', 'obl', 'obl:tmod']}")

if __name__ == "__main__":
    debug_m_detection()
