#!/usr/bin/env python3
"""「倒置構造」の詳細分析 - 実際に何が検出されているか？"""

import spacy
from hierarchical_grammar_detector_v5_1 import UniversalHierarchicalDetector
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4

def analyze_inversion_sentence():
    """倒置構造の詳細分析"""
    
    sentence = "Never have I seen such a beautiful sunset."
    
    print(f"🔍 詳細分析: {sentence}")
    print("=" * 60)
    
    # spaCy分析
    nlp_spacy = spacy.load("en_core_web_sm")
    doc = nlp_spacy(sentence)
    
    print("📋 spaCy詳細解析:")
    for token in doc:
        print(f"  {token.text:10} | POS: {token.pos_:6} | DEP: {token.dep_:10} | HEAD: {token.head.text}")
    
    print("\n🔍 節構造検出:")
    clause_deps = ['ccomp', 'xcomp', 'advcl', 'acl', 'relcl', 'pcomp']
    found_clauses = 0
    for token in doc:
        if token.dep_ in clause_deps:
            found_clauses += 1
            print(f"  📎 {token.dep_}: {token.text}")
    
    if found_clauses == 0:
        print("  ❌ 節構造検出なし - これが問題！")
    
    print("\n🔍 V4単体での分析:")
    try:
        v4_detector = HierarchicalGrammarDetectorV4()
        v4_result = v4_detector.detect_hierarchical_grammar(sentence)
        print(f"  📊 V4結果: {v4_result.main_clause.grammatical_pattern.value if v4_result.main_clause else 'None'}")
        print(f"  📊 信頼度: {v4_result.main_clause.confidence if v4_result.main_clause else 'None'}")
    except Exception as e:
        print(f"  ❌ V4エラー: {e}")
    
    print("\n🔍 V5.1での分析:")
    try:
        v51_detector = UniversalHierarchicalDetector()
        v51_result = v51_detector.detect_universal_hierarchical_grammar(sentence)
        print("V5.1は上記の通り")
    except Exception as e:
        print(f"  ❌ V5.1エラー: {e}")
    
    print("\n🚨 問題点の特定:")
    print("1. 倒置構造 (Never have I seen) → 通常語順でない")
    print("2. 助動詞 + 過去分詞 (have seen) → 完了時制")
    print("3. 強調副詞 (Never) → 文頭で意味変化")
    print("4. 現在のシステムは「単純文」として誤認")

def test_other_complex_cases():
    """他の見過ごされている複雑ケースのテスト"""
    
    complex_cases = [
        "Little did I know what would happen.",  # 倒置
        "Had I known earlier, I would have acted.",  # 仮定法倒置
        "Not only is he smart, but he is also kind.",  # not only倒置
        "Rarely do we see such dedication.",  # 副詞倒置
        "Under no circumstances should you do this.",  # 否定語句倒置
    ]
    
    print(f"\n🧪 他の複雑構造テスト")
    print("=" * 50)
    
    detector = UniversalHierarchicalDetector()
    
    for i, sentence in enumerate(complex_cases, 1):
        print(f"\n{i}. {sentence}")
        try:
            result = detector.detect_universal_hierarchical_grammar(sentence)
            main_pattern = result.main_result.main_clause.grammatical_pattern.value if result.main_result.main_clause else 'Unknown'
            print(f"   結果: {main_pattern}, Clauses={len(result.clause_results)}")
            
            if len(result.clause_results) == 0:
                print("   ❌ 複雑構造が見逃されている可能性")
        except Exception as e:
            print(f"   ❌ エラー: {e}")

if __name__ == "__main__":
    analyze_inversion_sentence()
    test_other_complex_cases()
