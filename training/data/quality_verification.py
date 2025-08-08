# ===== Step 12品質検証・修正フェーズ =====
# 目標: 100％統合されたルールの品質向上と意図との一致確認

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from step12_cognitive_verbs import RephraseIntegrationStep12

def run_comprehensive_tests():
    """包括的品質検証テスト"""
    print("=== ChatGPT 34ルール統合 品質検証テスト ===")
    print("目標: 意図と実装の一致確認と修正\n")
    
    analyzer = RephraseIntegrationStep12()
    
    # カテゴリー別テストケース
    test_categories = {
        "基本助動詞": [
            "I will go",
            "I have done it", 
            "I am running",
        ],
        
        "受動態": [
            "The book is written by John",
            "The window was broken yesterday",
            "The book should be written",
        ],
        
        "モーダル完了形": [
            "I could have done it",
            "She must have finished",
            "They might have been there",
        ],
        
        "認知動詞": [
            "I think that he is smart",
            "I believe you are right",  
            "She knows that it is true",  # 問題箇所
            "We realized that time was running out",  # 問題箇所
            "I figure out the problem",
        ],
        
        "第4文型": [
            "I give you a book",
            "She told me that she was tired",
            "He showed us the way",
        ],
        
        "連結動詞": [
            "I become happy",
            "She seems tired",
            "They appear confused",
        ],
        
        "複合パターン": [
            "I think that the book should be written",
            "She believes that I could have done better", 
            "We know that they might have been there",
        ]
    }
    
    issues_found = []
    
    for category, sentences in test_categories.items():
        print(f"\n=== {category}カテゴリー ===")
        
        for sentence in sentences:
            print(f"\n入力: {sentence}")
            try:
                slots = analyzer.analyze_sentence(sentence)
                
                # 結果表示
                slot_found = False
                for slot, candidates in slots.items():
                    if candidates:
                        slot_found = True
                        candidate = candidates[0]
                        pattern_info = f" [{candidate.get('pattern', '')}]" if candidate.get('pattern') else ""
                        print(f"  {slot}: {candidate['value']} ({candidate.get('note', candidate['type'])}){pattern_info}")
                
                if not slot_found:
                    print("  ❌ スロットが検出されませんでした")
                    issues_found.append(f"{category}: {sentence} - スロット未検出")
                
                # 問題パターンの自動検出
                if 'V' not in slots or not slots['V']:
                    issues_found.append(f"{category}: {sentence} - 動詞未検出")
                elif 'S' not in slots or not slots['S']:
                    issues_found.append(f"{category}: {sentence} - 主語未検出")
                    
            except Exception as e:
                print(f"  ❌ エラー: {e}")
                issues_found.append(f"{category}: {sentence} - エラー: {e}")
    
    # 問題点の総括
    print(f"\n=== 品質検証結果 ===")
    print(f"検出された問題: {len(issues_found)}件")
    
    if issues_found:
        print("\n🔧 修正が必要な項目:")
        for i, issue in enumerate(issues_found, 1):
            print(f"{i}. {issue}")
    else:
        print("\n✅ 全テストケース正常動作")
    
    return issues_found

def analyze_specific_issues():
    """特定問題の詳細分析"""
    print("\n=== 特定問題の詳細分析 ===")
    
    analyzer = RephraseIntegrationStep12()
    
    problem_cases = [
        "She knows that it is true",
        "We realized that time was running out"
    ]
    
    for sentence in problem_cases:
        print(f"\n🔍 詳細分析: {sentence}")
        words = sentence.split()
        print(f"  単語分解: {words}")
        
        # 各ルールの適用結果を個別チェック
        print("  ルール適用結果:")
        
        # 認知動詞ルールの適用結果
        cognitive_results = analyzer.rule_cognition_verb_that_clause(words)
        print(f"    認知動詞ルール: {len(cognitive_results)}件")
        for result in cognitive_results:
            print(f"      {result['slot']}: {result['value']} (rule_id: {result['rule_id']})")

if __name__ == "__main__":
    issues = run_comprehensive_tests()
    analyze_specific_issues()
