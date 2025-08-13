#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"The cat is fed." 問題の詳細分析
"""

from engines.passive_voice_engine import PassiveVoiceEngine
import stanza

def main():
    # Stanzaで直接構造を確認
    nlp = stanza.Pipeline('en', verbose=False)
    text = "The cat is fed."
    
    print(f"=== 📊 '{text}' の詳細分析 ===")
    
    doc = nlp(text)
    sent = doc.sentences[0]
    
    print("\n🔍 Stanza構造解析:")
    for word in sent.words:
        print(f"  {word.id}: '{word.text}' - POS: {word.upos}, DEPREL: {word.deprel}, HEAD: {word.head}")
    
    print("\n🔍 受動態の条件チェック:")
    
    # 受動態の判定条件を確認
    has_passive_aux = False
    has_past_participle = False
    
    for word in sent.words:
        # be動詞チェック
        if word.lemma in ['be'] and word.upos == 'AUX':
            print(f"  ✅ be動詞発見: '{word.text}' (lemma: {word.lemma}, pos: {word.upos})")
            has_passive_aux = True
        elif word.lemma in ['be']:
            print(f"  🔍 be動詞候補: '{word.text}' (lemma: {word.lemma}, pos: {word.upos})")
        
        # 過去分詞チェック  
        if word.upos == 'VERB' and hasattr(word, 'feats') and word.feats:
            if 'VerbForm=Part' in word.feats and 'Tense=Past' in word.feats:
                print(f"  ✅ 過去分詞発見: '{word.text}' (feats: {word.feats})")
                has_past_participle = True
            else:
                print(f"  🔍 動詞: '{word.text}' (feats: {word.feats})")
        elif word.upos == 'VERB':
            print(f"  🔍 動詞（feats無し）: '{word.text}'")
    
    print(f"\n📋 判定結果:")
    print(f"  be動詞: {has_passive_aux}")
    print(f"  過去分詞: {has_past_participle}")
    print(f"  受動態判定: {has_passive_aux and has_past_participle}")
    
    print("\n🔧 PassiveVoiceEngineでのテスト:")
    engine = PassiveVoiceEngine()
    result = engine.process(text)
    print(f"  結果: {result}")

if __name__ == "__main__":
    main()
