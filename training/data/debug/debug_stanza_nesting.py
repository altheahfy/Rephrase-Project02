#!/usr/bin/env python3
"""
Stanzaの入れ子構造デバッグ：上位レベルとサブレベルの依存関係比較
"""

import stanza
import json

def analyze_stanza_differences():
    """上位レベルとサブレベルでのStanza出力比較"""
    
    nlp = stanza.Pipeline('en', verbose=False)
    
    # テストケース
    test_cases = [
        {
            "full_sentence": "I gave him a book.",
            "subphrase": "a book"
        },
        {
            "full_sentence": "The tall man runs fast.",
            "subphrase": "The tall man"
        },
        {
            "full_sentence": "She bought a beautiful red car.",
            "subphrase": "a beautiful red car"
        }
    ]
    
    for case in test_cases:
        print(f"\n{'='*60}")
        print(f"📝 テストケース: {case['full_sentence']}")
        print(f"🎯 サブフレーズ: '{case['subphrase']}'")
        print('='*60)
        
        # 完全文の解析
        print("\n🔵 完全文の依存関係:")
        full_doc = nlp(case['full_sentence'])
        full_sent = full_doc.sentences[0]
        
        for word in full_sent.words:
            print(f"  {word.id:2d} {word.text:12} | {word.deprel:12} | head:{word.head:2d} | {word.pos}")
            
        # サブフレーズの解析
        print(f"\n🔴 サブフレーズ '{case['subphrase']}' の依存関係:")
        sub_doc = nlp(case['subphrase'])
        sub_sent = sub_doc.sentences[0]
        
        for word in sub_sent.words:
            print(f"  {word.id:2d} {word.text:12} | {word.deprel:12} | head:{word.head:2d} | {word.pos}")
            
        # 差異の分析
        print(f"\n🔍 依存関係ラベルの差異分析:")
        full_deprels = {word.text: word.deprel for word in full_sent.words}
        sub_deprels = {word.text: word.deprel for word in sub_sent.words}
        
        for word_text in sub_deprels:
            if word_text in full_deprels:
                full_rel = full_deprels[word_text]
                sub_rel = sub_deprels[word_text]
                if full_rel != sub_rel:
                    print(f"  ⚠️  '{word_text}': 完全文={full_rel} → サブ={sub_rel}")
                else:
                    print(f"  ✅ '{word_text}': {full_rel} (同じ)")
            else:
                print(f"  🆕 '{word_text}': サブのみ={sub_deprels[word_text]}")

def analyze_root_differences():
    """ROOTの検出差異を詳しく分析"""
    
    nlp = stanza.Pipeline('en', verbose=False)
    
    test_phrases = [
        "a book",
        "The tall man", 
        "a beautiful red car",
        "very quickly",
        "in the garden"
    ]
    
    print(f"\n{'='*50}")
    print("🎯 ROOT検出の差異分析")
    print('='*50)
    
    for phrase in test_phrases:
        print(f"\n📝 フレーズ: '{phrase}'")
        
        doc = nlp(phrase)
        sent = doc.sentences[0]
        
        # ROOT語の特定
        root_words = [word for word in sent.words if word.deprel == 'root']
        
        print(f"  ROOT語: {[w.text for w in root_words]}")
        print("  全依存関係:")
        for word in sent.words:
            marker = " 🎯" if word.deprel == 'root' else ""
            print(f"    {word.text:12} | {word.deprel:12} | {word.pos}{marker}")

if __name__ == "__main__":
    print("🔍 Stanza入れ子構造デバッグ開始")
    
    analyze_stanza_differences()
    analyze_root_differences()
    
    print(f"\n{'='*60}")
    print("🎯 分析完了: サブレベルでの依存関係パターンを確認")
    print('='*60)
