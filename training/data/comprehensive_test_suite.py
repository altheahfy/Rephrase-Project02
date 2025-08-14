#!/usr/bin/env python3
"""包括的テストスイートの実行"""

from hierarchical_grammar_detector_v5_1 import UniversalHierarchicalDetector
import traceback

def run_comprehensive_test():
    """25ケースの包括的テスト実行"""
    
    detector = UniversalHierarchicalDetector()
    
    test_cases = {
        "基本節タイプ": [
            "I think that he is smart.",  # ccomp - 既知
            "I want to go home.",  # xcomp - 新規
            "Being tired, she slept.",  # advcl-participle - 新規
            "If it rains, we stay home.",  # advcl-condition - 新規
            "The book that I read was good.",  # relcl - 既知
            "The man sitting there is my father.",  # acl - 新規
        ],
        
        "関係節バリエーション": [
            "The person who called you is here.",  # who
            "The place where we met was nice.",  # where  
            "The time when he came was perfect.",  # when
            "The reason why he left is unknown.",  # why
        ],
        
        "副詞節バリエーション": [
            "Although it was raining, we went out.",  # 譲歩
            "Because he was tired, he slept.",  # 理由
            "When I arrived, they had left.",  # 時
            "As you know, this is important.",  # 様態
            "Before you leave, call me.",  # 時（前）
        ],
        
        "複合・入れ子構造": [
            "I think that the book that he wrote is good.",  # ccomp + relcl
            "When I was young, I believed that Santa existed.",  # advcl + ccomp
            "The man who you met said that he would help.",  # relcl + ccomp
        ],
        
        "エッジケース": [
            "I think that he is smart and that she is kind.",  # 並列
            "Having been tired, she slept early.",  # 完了分詞
            "To succeed, you must work hard.",  # 不定詞副詞的用法
        ]
    }
    
    print("🧪 包括的テストスイート実行")
    print("=" * 70)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    error_summary = {}
    
    for category, sentences in test_cases.items():
        print(f"\n📋 {category} テスト:")
        print("-" * 50)
        
        for i, sentence in enumerate(sentences, 1):
            total_tests += 1
            print(f"\n{total_tests:2d}. {sentence}")
            
            try:
                result = detector.detect_universal_hierarchical_grammar(sentence)
                main_pattern = result.main_result.main_clause.grammatical_pattern.value if result.main_result.main_clause else 'Unknown'
                
                print(f"    ✅ 成功: Main={main_pattern}, Clauses={len(result.clause_results)}")
                passed_tests += 1
                
            except Exception as e:
                print(f"    ❌ エラー: {str(e)}")
                failed_tests += 1
                
                error_type = type(e).__name__
                if error_type not in error_summary:
                    error_summary[error_type] = []
                error_summary[error_type].append({
                    'sentence': sentence,
                    'error': str(e)
                })
    
    # 結果サマリー
    print(f"\n📊 テスト結果サマリー")
    print("=" * 50)
    print(f"総テスト数: {total_tests}")
    print(f"成功: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
    print(f"失敗: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
    
    if error_summary:
        print(f"\n🚨 エラー分析:")
        for error_type, errors in error_summary.items():
            print(f"\n{error_type} ({len(errors)}件):")
            for error in errors[:3]:  # 最初の3件のみ表示
                print(f"  📎 '{error['sentence']}' → {error['error']}")
            if len(errors) > 3:
                print(f"  ... 他{len(errors)-3}件")
    
    return total_tests, passed_tests, failed_tests, error_summary

if __name__ == "__main__":
    run_comprehensive_test()
