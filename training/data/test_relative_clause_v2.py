#!/usr/bin/env python3
"""
関係節の正確なRephrase処理テスト v2
「The book that he bought」→ O1:"The book that", sub-s:"he", sub-v:"bought"
"""

from pure_stanza_engine_v3_1_unified import PureStanzaEngineV31
import json

def test_relative_clause_precise():
    """関係節の精密処理テスト"""
    print("="*60)
    print("🎯 関係節精密処理テスト - The book that he bought")
    print("="*60)
    
    engine = PureStanzaEngineV31()
    
    # テスト文
    test_text = "The book that he bought"
    
    print(f"\n📖 テスト文: '{test_text}'")
    print("期待される結果:")
    print("  O1: 'The book that'")
    print("  sub-s: 'he'") 
    print("  sub-v: 'bought'")
    
    print("\n" + "-"*50)
    result = engine.decompose_unified(test_text)
    
    print("\n📊 実際の結果:")
    for k, v in sorted(result.items()):
        if not k.startswith('_'):
            if isinstance(v, dict):
                print(f"  {k}: {json.dumps(v, ensure_ascii=False, indent=2)}")
            else:
                print(f"  {k}: '{v}'")
    
    return result

def analyze_stanza_structure(text: str):
    """Stanzaの構造解析（デバッグ用）"""
    print(f"\n🔬 Stanza構造解析: '{text}'")
    print("-" * 40)
    
    import stanza
    nlp = stanza.Pipeline('en', verbose=False)
    doc = nlp(text)
    sent = doc.sentences[0]
    
    print("語順とdeprel:")
    for word in sent.words:
        print(f"  {word.id}: '{word.text}' ({word.pos}) → {word.deprel} (head: {word.head})")
    
    print("\n依存関係:")
    for word in sent.words:
        if word.head != 0:
            head = next(w for w in sent.words if w.id == word.head)
            print(f"  '{head.text}' ←[{word.deprel}]← '{word.text}'")

if __name__ == "__main__":
    # Stanza構造を先に確認
    analyze_stanza_structure("The book that he bought")
    
    # Rephrase処理テスト
    result = test_relative_clause_precise()
    
    print("\n" + "="*60)
    print("🎯 関係節処理分析完了")
    print("="*60)
