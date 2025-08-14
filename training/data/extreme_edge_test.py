#!/usr/bin/env python3
"""最終検証: 極限のエッジケースでテスト"""

from hierarchical_grammar_detector_v5_1 import UniversalHierarchicalDetector

def extreme_edge_case_test():
    """極限エッジケースでの検証"""
    
    detector = UniversalHierarchicalDetector()
    
    extreme_cases = [
        # 超複雑な入れ子構造
        "I believe that the student who studies hard will succeed when he tries.",
        
        # 3重入れ子
        "She said that she knows that the book that I mentioned is good.",
        
        # 分詞+関係節+補文の組み合わせ
        "The man sitting there said that the woman who came yesterday knows where we should go.",
        
        # 省略構造
        "Though tired, she continued working.",
        
        # 倒置構造  
        "Never have I seen such a beautiful sunset.",
        
        # 複数の並列節
        "I think that he is smart, that she is kind, and that they work well together.",
    ]
    
    print("🚀 極限エッジケーステスト")
    print("=" * 60)
    
    success_count = 0
    
    for i, sentence in enumerate(extreme_cases, 1):
        print(f"\n{i}. {sentence}")
        print("-" * 50)
        
        try:
            result = detector.detect_universal_hierarchical_grammar(sentence)
            main_pattern = result.main_result.main_clause.grammatical_pattern.value if result.main_result.main_clause else 'Unknown'
            
            print(f"✅ 成功: Main={main_pattern}, Clauses={len(result.clause_results)}")
            success_count += 1
            
            # 詳細情報
            for j, clause in enumerate(result.clause_results):
                sv_type = "SV-clause" if clause.has_subject and clause.has_verb else "phrase"
                print(f"  📎 {clause.clause_type}: '{clause.text}' ({sv_type})")
            
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
    
    print(f"\n🎯 極限テスト結果: {success_count}/{len(extreme_cases)} = {success_count/len(extreme_cases)*100:.1f}%")
    
    if success_count == len(extreme_cases):
        print("🏆 完璧！真の汎用システム確認")
    else:
        print("🚨 まだ改善の余地あり")

if __name__ == "__main__":
    extreme_edge_case_test()
