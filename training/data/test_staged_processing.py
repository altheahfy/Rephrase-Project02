"""
段階分離処理アプローチの検証
1. 節境界の検出能力確認
2. 節タイプ分類の精度確認  
3. 独立処理後の統合可能性確認
"""
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
import stanza
import spacy

def test_clause_boundary_detection():
    """StanzaとspaCyでの節境界検出能力をテスト"""
    
    print("🔍 Clause Boundary Detection Analysis")
    print("=" * 60)
    
    # テスト文
    test_sentence = "Having finished the project, the student submitted it confidently."
    print(f"Target: {test_sentence}")
    print()
    
    # Stanza解析
    print("📊 Stanza Analysis:")
    nlp_stanza = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)
    stanza_doc = nlp_stanza(test_sentence)
    
    for i, sent in enumerate(stanza_doc.sentences):
        print(f"Sentence {i+1}:")
        for word in sent.words:
            print(f"  {word.text:<15} | {word.upos:<8} | Head: {word.head} ({sent.words[word.head-1].text if word.head > 0 else 'ROOT'}) | Dep: {word.deprel}")
    
    print()
    
    # spaCy解析
    print("📊 spaCy Analysis:")
    nlp_spacy = spacy.load('en_core_web_sm')
    spacy_doc = nlp_spacy(test_sentence)
    
    for token in spacy_doc:
        print(f"  {token.text:<15} | {token.pos_:<8} | Head: {token.head.text:<12} | Dep: {token.dep_:<12} | Children: {[child.text for child in token.children]}")
    
    print()
    
    # 節境界の自動検出試行
    print("🎯 Automatic Clause Boundary Detection:")
    
    # Stanzaベースの節検出
    stanza_clauses = []
    for sent in stanza_doc.sentences:
        main_verbs = []
        subordinate_clauses = []
        
        for word in sent.words:
            if word.upos == 'VERB' and word.deprel in ['root', 'advcl', 'ccomp', 'xcomp', 'acl', 'acl:relcl']:
                clause_info = {
                    'verb': word.text,
                    'position': word.id,
                    'deprel': word.deprel,
                    'clause_type': 'main' if word.deprel == 'root' else 'subordinate'
                }
                
                # 節の範囲を推定
                clause_tokens = [word.text]
                for dep_word in sent.words:
                    if dep_word.head == word.id:
                        clause_tokens.append(dep_word.text)
                
                clause_info['tokens'] = clause_tokens
                clause_info['estimated_span'] = ' '.join(clause_tokens)
                
                if word.deprel == 'root':
                    main_verbs.append(clause_info)
                else:
                    subordinate_clauses.append(clause_info)
        
        stanza_clauses.append({
            'main_verbs': main_verbs,
            'subordinate_clauses': subordinate_clauses
        })
    
    for i, clause_analysis in enumerate(stanza_clauses):
        print(f"Clause Analysis {i+1}:")
        print(f"  Main clauses: {len(clause_analysis['main_verbs'])}")
        for j, main in enumerate(clause_analysis['main_verbs']):
            print(f"    Main {j+1}: {main['verb']} (deprel: {main['deprel']})")
            print(f"      Estimated span: {main['estimated_span']}")
        
        print(f"  Subordinate clauses: {len(clause_analysis['subordinate_clauses'])}")
        for j, sub in enumerate(clause_analysis['subordinate_clauses']):
            print(f"    Sub {j+1}: {sub['verb']} (deprel: {sub['deprel']})")
            print(f"      Estimated span: {sub['estimated_span']}")
    
    print()
    
    # 期待される境界との比較
    print("🎯 Expected vs Detected Boundaries:")
    expected_boundaries = [
        {
            'clause': 'Having finished the project',
            'type': 'subordinate',
            'function': 'adverbial (participle)',
            'span': (0, 4)  # token positions
        },
        {
            'clause': 'the student submitted it confidently',
            'type': 'main',
            'function': 'main clause',
            'span': (5, 9)
        }
    ]
    
    for expected in expected_boundaries:
        print(f"Expected: '{expected['clause']}' ({expected['type']}, {expected['function']})")
    
    return stanza_clauses

def test_clause_type_classification():
    """節タイプの分類精度をテスト"""
    
    print("\n" + "=" * 60)
    print("🔍 Clause Type Classification Test")
    print("=" * 60)
    
    test_cases = [
        {
            "sentence": "Having finished the project, the student submitted it confidently.",
            "expected_clauses": [
                {"text": "Having finished the project", "type": "adverbial", "subtype": "participle"},
                {"text": "the student submitted it confidently", "type": "main", "subtype": "svo"}
            ]
        },
        {
            "sentence": "While she was reading, she discovered what made the story compelling.",
            "expected_clauses": [
                {"text": "While she was reading", "type": "adverbial", "subtype": "temporal"},
                {"text": "she discovered what made the story compelling", "type": "main", "subtype": "svo"},
                {"text": "what made the story compelling", "type": "noun_clause", "subtype": "object"}
            ]
        },
        {
            "sentence": "The book that he wrote became very popular.",
            "expected_clauses": [
                {"text": "The book became very popular", "type": "main", "subtype": "svc"},
                {"text": "that he wrote", "type": "relative", "subtype": "restrictive"}
            ]
        }
    ]
    
    detector = HierarchicalGrammarDetectorV4()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 Test Case {i}:")
        print(f"Sentence: {test_case['sentence']}")
        
        # 現在の検出結果
        result = detector.detect_hierarchical_grammar(test_case['sentence'])
        
        print("Current Detection:")
        print(f"  Main: {result.main_clause.grammatical_pattern.value} - '{result.main_clause.text[:40]}...'")
        for j, sub in enumerate(result.subordinate_clauses, 1):
            print(f"  Sub {j}: {sub.grammatical_pattern.value} - '{sub.text[:40]}...'")
        
        print("Expected Clauses:")
        for j, expected in enumerate(test_case['expected_clauses'], 1):
            print(f"  Expected {j}: {expected['type']} ({expected['subtype']}) - '{expected['text']}'")
        
        print()
    
    return True

def propose_staged_processing_architecture():
    """段階処理アーキテクチャの提案"""
    
    print("\n" + "=" * 60)
    print("🏗️ Staged Processing Architecture Proposal")
    print("=" * 60)
    
    architecture = """
    🎯 提案されたアーキテクチャ:
    
    Stage 1: Clause Boundary Detection
    ├─ StanzaとspaCyによる依存構造解析
    ├─ 動詞の依存関係からclause境界を特定
    ├─ 各節の開始・終了位置を決定
    └─ 節タイプの粗分類 (main/subordinate/relative/noun_clause)
    
    Stage 2: Clause Function Classification  
    ├─ 各節の上位文構造での機能を判定
    ├─ 副詞節/形容詞節/名詞節の細分類
    ├─ 主節の位置情報の決定
    └─ 入れ子関係の階層マッピング
    
    Stage 3: Individual Clause Pattern Recognition
    ├─ 各節を独立した「上位スロット」として扱い
    ├─ 既存の高精度上位スロット判定システムを適用
    ├─ SV/SVO/SVC/SVOO/SVOC等の詳細パターン判定
    └─ 各節内部での最適エンジン選択
    
    Stage 4: Results Integration
    ├─ Stage 2の階層情報 + Stage 3のパターン情報を統合
    ├─ Rephraseスロット構造への変換
    ├─ 主節・副節の最終的な組み合わせ決定
    └─ 信頼度スコアの統合計算
    """
    
    print(architecture)
    
    advantages = """
    💡 このアプローチの利点:
    
    1. 問題の分離化
       ├─ 節境界検出 (構造的問題)
       ├─ 節機能分類 (意味的問題)  
       └─ パターン認識 (語法的問題)
    
    2. 既存システムの活用
       ├─ 83.3%の高精度上位スロット判定を再利用
       ├─ 複雑性を段階的に処理
       └─ デバッグ・改善が容易
    
    3. スケーラビリティ
       ├─ 各段階を独立して改善可能
       ├─ 新しい節タイプの追加が容易
       └─ エラーの局所化が可能
    
    4. Rephrase設計との整合性
       ├─ 二重入れ子制限の自然な実装
       ├─ 上位・サブスロットの明確な分離
       └─ Type phraseの構造との対応
    """
    
    print(advantages)
    
    implementation_plan = """
    🛠️ 実装計画:
    
    Phase 1: 現状調査 (本テストで実施中)
    ├─ Stanza/spaCyの節境界検出能力確認 ✅
    ├─ 既存システムとの統合点確認 
    └─ 技術的実現性の検証
    
    Phase 2: Stage 1プロトタイプ
    ├─ 節境界検出アルゴリズムの実装
    ├─ 基本的な節タイプ分類
    └─ 境界検出精度の評価
    
    Phase 3: Stage 2-3統合
    ├─ 節機能分類器の開発
    ├─ 既存パターン認識システムの適用
    └─ 個別処理結果の統合
    
    Phase 4: 最適化とテスト
    ├─ 全体的な精度改善
    ├─ Rephraseシステムとの統合
    └─ 大規模テストとデバッグ
    """
    
    print(implementation_plan)
    
    return True

if __name__ == "__main__":
    # Stage 1: 節境界検出能力の確認
    clause_analysis = test_clause_boundary_detection()
    
    # Stage 2: 節タイプ分類の確認
    classification_test = test_clause_type_classification()
    
    # Stage 3: アーキテクチャ提案
    architecture_proposal = propose_staged_processing_architecture()
