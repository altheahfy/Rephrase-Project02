#!/usr/bin/env python3
"""
5文型完全テストスイート - 問題分析用
"""

from spacy_human_grammar_mapper import SpacyHumanGrammarMapper

def test_five_patterns_complete():
    """5文型完全テスト"""
    print("=== 5文型完全テスト - 問題分析 ===\n")
    
    mapper = SpacyHumanGrammarMapper()
    
    # テストケース
    test_cases = [
        # 第1文型（SV）
        ("Children play", "SV"),
        ("The dog runs", "SV"),
        ("Birds fly", "SV"),
        
        # 第2文型（SVC）
        ("She is happy", "SVC"),
        ("The cat became angry", "SVC"),
        ("He looks tired", "SVC"),
        
        # 第3文型（SVO）
        ("I love you", "SVO"),
        ("She reads books", "SVO"),
        ("They eat apples", "SVO"),
        
        # 第4文型（SVOO）
        ("I give you money", "SVOO"),
        ("He told me stories", "SVOO"),
        ("She bought him gifts", "SVOO"),
        
        # 第5文型（SVOC）
        ("We made her happy", "SVOC"),
        ("I found it interesting", "SVOC"),
        ("They painted the wall blue", "SVOC"),
    ]
    
    success_count = 0
    pattern_stats = {"SV": 0, "SVC": 0, "SVO": 0, "SVOO": 0, "SVOC": 0}
    pattern_totals = {"SV": 0, "SVC": 0, "SVO": 0, "SVOO": 0, "SVOC": 0}
    
    for sentence, expected_pattern in test_cases:
        pattern_totals[expected_pattern] += 1
        
        print(f"--- '{sentence}' (期待: {expected_pattern}) ---")
        
        # 語彙解析詳細
        lexical_info = mapper._extract_lexical_knowledge(sentence)
        print("語彙解析:")
        for token in lexical_info['tokens']:
            print(f"  {token['text']}: {token['pos']} ({token['tag']})")
        
        result = mapper.analyze_sentence(sentence)
        
        if 'error' in result:
            print(f"❌ エラー: {result['error']}")
        else:
            detected = result['pattern_detected']
            print(f"検出パターン: {detected}")
            
            if detected == expected_pattern:
                print(f"✅ 正解！")
                success_count += 1
                pattern_stats[expected_pattern] += 1
            else:
                print(f"❌ 不正解（期待: {expected_pattern}）")
                
                # 個別パターン検出テスト
                tokens = lexical_info['tokens']
                print("個別パターン検出結果:")
                
                sv_result = mapper._detect_sv_pattern_human(tokens)
                print(f"  SV: {sv_result['detected']} (確信度: {sv_result.get('confidence', 0):.2f})")
                
                svc_result = mapper._detect_svc_pattern_human(tokens)
                print(f"  SVC: {svc_result['detected']} (確信度: {svc_result.get('confidence', 0):.2f})")
                
                svo_result = mapper._detect_svo_pattern_human(tokens)
                print(f"  SVO: {svo_result['detected']} (確信度: {svo_result.get('confidence', 0):.2f})")
                
                svoo_result = mapper._detect_svoo_pattern_human(tokens)
                print(f"  SVOO: {svoo_result['detected']} (確信度: {svoo_result.get('confidence', 0):.2f})")
                
                svoc_result = mapper._detect_svoc_pattern_human(tokens)
                print(f"  SVOC: {svoc_result['detected']} (確信度: {svoc_result.get('confidence', 0):.2f})")
        
        print()
    
    # 結果サマリー
    print("=== 結果サマリー ===")
    print(f"全体成功率: {success_count}/{len(test_cases)} ({success_count/len(test_cases):.1%})")
    
    for pattern in pattern_stats:
        total = pattern_totals[pattern]
        success = pattern_stats[pattern]
        if total > 0:
            print(f"{pattern}: {success}/{total} ({success/total:.1%})")

if __name__ == '__main__':
    test_five_patterns_complete()
