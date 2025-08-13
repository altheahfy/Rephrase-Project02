#!/usr/bin/env python3
"""
Stanzaの依存構造 vs 句構造の比較デモ
"""

import stanza

def analyze_dependency_vs_constituency():
    nlp = stanza.Pipeline('en', verbose=False)
    text = "The book that I read yesterday was very interesting."
    
    print("=== 📊 依存構造 vs 句構造の比較 ===")
    print(f"文: {text}")
    
    doc = nlp(text)
    sent = doc.sentences[0]
    
    print(f"\n🔗 【依存構造】- Stanzaの採用方式:")
    print("語 -> 語の直接的関係")
    for word in sent.words:
        head_word = sent.words[word.head - 1].text if word.head > 0 else "ROOT"
        print(f"  {word.text:12} ─({word.deprel:12})→ {head_word}")
    
    print(f"\n📖 【句構造】- 伝統文法的解析:")
    print("入れ子構造")
    print("  [S")
    print("    [NP")
    print("      [NP The book]")
    print("      [RelClause that")
    print("        [S I read yesterday]")
    print("      ]")
    print("    ]")
    print("    [VP was")
    print("      [AdvP very]")
    print("      [AdjP interesting]")
    print("    ]")
    print("  ]")
    
    print(f"\n⚡ 【処理効率比較】:")
    print("依存構造: O(n) - 線形処理")
    print("句構造: O(n²) - 入れ子処理")
    
    print(f"\n🌍 【言語普遍性】:")
    print("依存構造: 語順に依存しない (日本語, 英語, ドイツ語で共通)")
    print("句構造: 語順に強く依存 (言語ごとに異なる)")

if __name__ == "__main__":
    analyze_dependency_vs_constituency()
