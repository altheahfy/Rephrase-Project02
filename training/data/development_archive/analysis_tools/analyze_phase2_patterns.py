#!/usr/bin/env python3
"""
Stanza依存関係パターン調査 Phase 2
高頻度構文（助動詞、時制、受動態、疑問文、否定文）の解析
"""

import stanza

def analyze_high_frequency_patterns():
    """高頻度構文のStanza解析パターンを体系的に調査"""
    nlp = stanza.Pipeline('en', verbose=False)
    
    # Phase 2: 高頻度構文パターン
    high_frequency_patterns = {
        "助動詞構文": [
            "I can swim.",
            "She will come.",
            "You must go.",
            "They should study.",
            "We may leave.",
            "He could help.",
        ],
        "完了・進行時制": [
            "I have finished.",
            "She has been working.",
            "They had left.",
            "We will have done it.",
            "He is running.",
            "She was sleeping.",
        ],
        "受動態": [
            "The book was read.",
            "It is being built.",
            "The project has been completed.",
            "The letter will be sent.",
        ],
        "疑問文": [
            "What is this?",
            "Where did you go?",
            "How can I help?",
            "Who will come?",
            "When does it start?",
        ],
        "否定文": [
            "I don't know.",
            "She hasn't arrived.",
            "They won't come.",
            "He can't swim.",
            "We didn't see it.",
        ],
        "There構文": [
            "There is a book.",
            "There are many people.",
            "There will be a meeting.",
        ],
        "It構文": [
            "It is raining.",
            "It seems good.",
            "It is important to study.",
        ]
    }
    
    pattern_rules = {}
    
    for category, sentences in high_frequency_patterns.items():
        print(f"\n{'='*80}")
        print(f"📋 {category}")
        print(f"{'='*80}")
        
        category_patterns = []
        
        for sentence in sentences:
            print(f"\n🎯 文: {sentence}")
            print(f"-" * 60)
            
            doc = nlp(sentence)
            sent = doc.sentences[0]
            
            # ROOT探索
            root_word = None
            for word in sent.words:
                if word.deprel == 'root':
                    root_word = word
                    break
            
            if not root_word:
                print("❌ ROOT が見つかりません")
                continue
                
            print(f"📌 ROOT: '{root_word.text}' (POS: {root_word.upos})")
            
            # 基本構造抽出
            structure = {}
            structure['root'] = {'word': root_word.text, 'pos': root_word.upos, 'id': root_word.id}
            
            # 各依存関係を分析
            relations = {}
            for word in sent.words:
                if word.deprel not in relations:
                    relations[word.deprel] = []
                relations[word.deprel].append({
                    'word': word.text,
                    'pos': word.upos,
                    'head': word.head,
                    'id': word.id
                })
            
            # 重要な関係を表示（Phase 2で新たに重要になった関係を追加）
            important_relations = [
                'nsubj', 'obj', 'iobj', 'cop', 'xcomp', 'amod', 'advmod', 'det', 'case', 'nmod',
                'aux', 'aux:pass', 'nsubj:pass', 'csubj', 'expl',  # 助動詞・受動態関連
                'mark', 'cc', 'conj',  # 接続関連
                'root', 'punct'  # 基本構造
            ]
            
            print("📋 重要な依存関係:")
            for rel in important_relations:
                if rel in relations:
                    for item in relations[rel]:
                        head_word = sent.words[item['head']-1].text if item['head'] > 0 else 'ROOT'
                        print(f"  {rel:15}: {item['word']:15} -> {head_word:15} (POS: {item['pos']})")
            
            # パターンを記録
            pattern_signature = []
            for word in sent.words:
                if word.deprel in important_relations and word.deprel != 'punct':
                    pattern_signature.append(f"{word.deprel}({word.upos})")
            
            structure['pattern'] = '+'.join(sorted(pattern_signature))
            category_patterns.append(structure)
            
            print(f"🔍 パターン: {structure['pattern']}")
            
            # 特別な構造の詳細分析
            if category == "助動詞構文":
                aux_words = [w for w in sent.words if w.deprel in ['aux', 'aux:pass']]
                if aux_words:
                    print(f"🔧 助動詞詳細: {[f'{w.text}({w.deprel})' for w in aux_words]}")
                    
            elif category == "受動態":
                passive_indicators = [w for w in sent.words if w.deprel in ['aux:pass', 'nsubj:pass']]
                if passive_indicators:
                    print(f"🔧 受動態詳細: {[f'{w.text}({w.deprel})' for w in passive_indicators]}")
                    
            elif category == "疑問文":
                wh_words = [w for w in sent.words if w.upos == 'PRON' and w.text.lower() in ['what', 'where', 'who', 'when', 'how']]
                if wh_words:
                    print(f"🔧 疑問詞詳細: {[f'{w.text}({w.deprel})' for w in wh_words]}")
        
        pattern_rules[category] = category_patterns
    
    # パターン統計
    print(f"\n{'='*80}")
    print("📊 Phase 2 パターン統計")
    print(f"{'='*80}")
    
    # 新発見の関係を特定
    new_relations = set()
    for category, patterns in pattern_rules.items():
        print(f"\n📋 {category}:")
        for pattern in patterns:
            signature = pattern['pattern']
            print(f"  - {signature}")
            # 新しい関係を抽出
            for rel in signature.split('+'):
                if rel and '(' in rel:
                    rel_name = rel.split('(')[0]
                    if rel_name not in ['nsubj', 'obj', 'iobj', 'cop', 'xcomp', 'amod', 'advmod', 'det', 'case', 'nmod', 'root']:
                        new_relations.add(rel_name)
    
    print(f"\n📋 新発見の重要な関係:")
    for rel in sorted(new_relations):
        print(f"  - {rel}")

if __name__ == "__main__":
    analyze_high_frequency_patterns()
