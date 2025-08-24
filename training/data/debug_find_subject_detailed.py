#!/usr/bin/env python3
"""
_find_subject詳細デバッグ: 内部処理の段階別追跡
"""

import spacy

def debug_find_subject_logic():
    """_find_subject関数の内部ロジックを段階別デバッグ"""
    
    # spaCyモデル
    nlp = spacy.load("en_core_web_sm")
    
    # テスト文
    text = "She quickly runs to school."
    doc = nlp(text)
    
    # トークン情報
    tokens = []
    for token in doc:
        tokens.append({
            'text': token.text,
            'pos': token.pos_,
            'tag': token.tag_,
            'lemma': token.lemma_
        })
    
    verb_idx = 2  # 'runs'
    
    print("=== Tokens ===")
    for i, token in enumerate(tokens):
        print(f"Index {i}: {token}")
    
    print(f"\n=== _find_subject Logic Simulation ===")
    print(f"verb_idx = {verb_idx}")
    
    subject_indices = []
    
    # 実際の_find_subjectロジックをシミュレート
    print(f"\n範囲: range({verb_idx - 1}, -1, -1) = {list(range(verb_idx - 1, -1, -1))}")
    
    for i in range(verb_idx - 1, -1, -1):
        token = tokens[i]
        print(f"\nIndex {i}: '{token['text']}' (pos={token['pos']}, tag={token['tag']})")
        
        # 助動詞チェック（簡略版）
        is_aux = token['pos'] == 'AUX' or token['lemma'] in ['be', 'have', 'do', 'will', 'would', 'can', 'could', 'should', 'may', 'might', 'must']
        if is_aux:
            print(f"  → 助動詞のためスキップ")
            continue
        
        # 主語候補チェック
        is_subject_candidate = (
            token['pos'] in ['NOUN', 'PROPN', 'PRON'] or 
            token['tag'] in ['DT', 'PRP', 'PRP$', 'WP']
        )
        
        print(f"  → 主語候補: {is_subject_candidate}")
        
        if is_subject_candidate:
            subject_indices.insert(0, i)
            print(f"  → 主語に追加: subject_indices = {subject_indices}")
        elif not subject_indices:
            print(f"  → まだ主語要素なし、継続")
            continue
        else:
            print(f"  → 主語の境界に到達、終了")
            break
    
    print(f"\n=== 最終結果 ===")
    print(f"subject_indices = {subject_indices}")
    subject_words = [tokens[i]['text'] for i in subject_indices]
    print(f"主語: {' '.join(subject_words)}")

if __name__ == "__main__":
    debug_find_subject_logic()
