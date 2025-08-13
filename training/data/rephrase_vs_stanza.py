#!/usr/bin/env python3
"""
Rephraseの求める構造 vs Stanzaの提供する構造
"""

import stanza

def rephrase_vs_stanza_conflict():
    nlp = stanza.Pipeline('en', verbose=False)
    
    examples = [
        "The cat is fed.",
        "The book that I read is good.",
        "When he arrives, I will leave.",
        "I think that she is smart."
    ]
    
    print("=== 🎭 Rephraseの求める構造 vs Stanzaの現実 ===")
    
    for text in examples:
        print(f"\n📝 文: {text}")
        
        doc = nlp(text)
        sent = doc.sentences[0]
        
        print("🔧 Rephraseが欲しい構造:")
        if "fed" in text:
            print("  → S: The cat, Aux: is, V: fed (受動態として)")
        elif "that I read" in text:
            print("  → S: The book, V: is, C1: good, sub-s: I, sub-v: read (関係節サブスロット)")
        elif "When" in text:
            print("  → sub-m1: when, sub-s: he, sub-v: arrives, S: I, V: leave (時間節サブスロット)")
        elif "think that" in text:
            print("  → S: I, V: think, sub-s: she, sub-v: is (目的語節サブスロット)")
        
        print("🤖 Stanzaが提供する構造:")
        for word in sent.words:
            head_word = sent.words[word.head - 1].text if word.head > 0 else "ROOT"
            pos_info = f"({word.upos})" if word.upos else ""
            print(f"    {word.text:12} {pos_info:8} ─({word.deprel:12})→ {head_word}")
        
        print("💥 ミスマッチポイント:")
        if "fed" in text:
            fed_word = next((w for w in sent.words if w.text == "fed"), None)
            if fed_word and fed_word.upos == "ADJ":
                print("    ❌ 'fed' が ADJ として解析（VERB の過去分詞として扱いたい）")
        elif "that I read" in text:
            print("    ❌ 関係節が acl:relcl で単純化（サブスロット構造にしたい）")
        elif "When" in text:
            print("    ❌ 時間節が advmod で処理（独立したサブスロット構造にしたい）")
        elif "think that" in text:
            print("    ❌ that節が ccomp で処理（目的語節サブスロット構造にしたい）")

if __name__ == "__main__":
    rephrase_vs_stanza_conflict()
