#!/usr/bin/env python3
"""
Pure Stanza Engine v4 評価テスト
複文分解機能の実用性を確認
"""

from pure_stanza_engine_v4 import PureStanzaEngine_v4
import traceback

def test_v4_complex_sentences():
    """v4エンジンの複文分解テスト"""
    engine = PureStanzaEngine_v4()
    engine.initialize()

    # 複文テストケース
    test_sentences = [
        "I know that she is happy.",
        "The man who came yesterday was my friend.", 
        "When I arrived, he was sleeping.",
        "I think he will come.",
        "The book that I read was interesting."
    ]

    results = {}
    
    for sentence in test_sentences:
        print(f"\n=== {sentence} ===")
        try:
            result = engine.analyze_complex_sentence(sentence)
            print("✅ 分解成功")
            
            # メイン節の表示
            main_clause = result.get("main_clause", {})
            print(f"メイン節: {main_clause}")
            
            # 従属節の表示
            subordinate_clauses = result.get("subordinate_clauses", [])
            if subordinate_clauses:
                for i, sub_clause in enumerate(subordinate_clauses):
                    print(f"従属節{i+1}: {sub_clause}")
            else:
                print("従属節: なし")
                
            results[sentence] = {"success": True, "result": result}
            
        except Exception as e:
            print(f"❌ エラー: {e}")
            results[sentence] = {"success": False, "error": str(e)}
            traceback.print_exc()
    
    # 評価サマリー
    print(f"\n=== 評価サマリー ===")
    successful = sum(1 for r in results.values() if r["success"])
    total = len(results)
    print(f"成功率: {successful}/{total} ({successful/total*100:.1f}%)")
    
    return results

if __name__ == "__main__":
    test_v4_complex_sentences()
