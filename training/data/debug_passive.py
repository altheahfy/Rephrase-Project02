"""
🔍 受動態問題の詳細調査
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
import spacy

def debug_passive_voice():
    """受動態の詳細デバッグ"""
    print("🔍 受動態問題デバッグセッション")
    print("=" * 50)
    
    # spaCyでの解析結果を詳しく見る
    nlp = spacy.load("en_core_web_sm")
    sentence = "The letter was written by John."
    doc = nlp(sentence)
    
    print(f"📝 分析文: {sentence}")
    print("🔧 spaCy詳細解析:")
    for token in doc:
        print(f"   {token.text:<10} | {token.pos_:<8} | {token.dep_:<15} | {token.tag_}")
    
    print()
    print("🎯 agent依存関係検索:")
    for token in doc:
        if token.dep_ == 'agent':
            print(f"   Agent found: '{token.text}' (head: {token.head.text})")
            
            # 子要素を確認
            print(f"   Agent children:")
            for child in token.children:
                print(f"     - {child.text} ({child.dep_})")

if __name__ == "__main__":
    debug_passive_voice()
