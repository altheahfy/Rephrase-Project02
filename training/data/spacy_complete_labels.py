#!/usr/bin/env python3
"""
spaCyの全依存関係タグとPOS品詞タグの完全リスト取得
"""

import spacy

def get_spacy_complete_labels():
    print("🔍 spaCy完全ラベル体系調査")
    
    try:
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy語彙認識エンジン初期化完了")
    except Exception as e:
        print(f"❌ spaCy初期化失敗: {e}")
        return
    
    # 全依存関係ラベル
    print(f"\n📊 spaCy全依存関係ラベル:")
    dep_labels = list(nlp.get_pipe("parser").labels)
    print(f"  総数: {len(dep_labels)}種類")
    
    print("\n🏷️ 全依存関係ラベル一覧:")
    for i, dep in enumerate(sorted(dep_labels), 1):
        print(f"  {i:2d}. {dep}")
    
    # 全POS品詞ラベル
    print(f"\n📊 spaCyPOS品詞ラベル:")
    pos_labels = list(nlp.get_pipe("tagger").labels)
    print(f"  総数: {len(pos_labels)}種類")
    
    print("\n🏷️ 全POS品詞ラベル一覧:")
    for i, pos in enumerate(sorted(pos_labels), 1):
        print(f"  {i:2d}. {pos}")
    
    # 今回検出された21種類との比較
    detected_deps = {
        "nsubj", "ROOT", "poss", "dobj", "punct", "dative", "det", "amod", 
        "acl", "advmod", "aux", "prep", "pobj", "npadvmod", "acomp", "prt", 
        "intj", "mark", "advcl", "csubj", "relcl"
    }
    
    print(f"\n🔍 今回の検証結果との比較:")
    print(f"  今回検出: {len(detected_deps)}種類")
    print(f"  spaCy全体: {len(dep_labels)}種類")
    print(f"  未検出: {len(dep_labels) - len(detected_deps)}種類")
    
    missing_deps = set(dep_labels) - detected_deps
    print(f"\n❌ 今回未検出の依存関係ラベル ({len(missing_deps)}種類):")
    for i, dep in enumerate(sorted(missing_deps), 1):
        print(f"  {i:2d}. {dep}")

if __name__ == "__main__":
    get_spacy_complete_labels()
