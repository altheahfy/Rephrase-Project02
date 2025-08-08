# ===== 複文（サブクローズ）対応テスト =====
# 5文型フルセットのような複文構造への対応確認

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from step12_cognitive_verbs import RephraseIntegrationStep12

def test_complex_sentences():
    """複文・サブクローズ対応テスト"""
    print("=== 複文（サブクローズ）対応テスト ===")
    print("目標: 5文型フルセットのような複雑な文構造への対応確認\n")
    
    analyzer = RephraseIntegrationStep12()
    
    # 複文テストケース
    complex_test_cases = {
        "M1内のSV": [
            "When I arrived, he was sleeping",  # M1: When I arrived
            "If she comes, we will start",      # M1: If she comes  
            "Because you helped me, I succeeded", # M1: Because you helped me
        ],
        
        "S内のSV": [
            "The man who came yesterday is my friend",        # S: The man who came yesterday
            "What he said was interesting",                   # S: What he said  
            "The book that you gave me is excellent",         # S: The book that you gave me
        ],
        
        "O1内のSV": [
            "I know what he thinks",                          # O1: what he thinks
            "She believes that I can do it",                 # O1: that I can do it
            "We discussed where we should go",               # O1: where we should go  
        ],
        
        "C1内のSV": [
            "The problem is that we have no money",          # C1: that we have no money
            "My dream is what I want to achieve",            # C1: what I want to achieve
        ],
        
        "深い入れ子": [
            "I think that the man who came yesterday knows what we need",  # 多重入れ子
            "When I realized that she was the person who helped us, I was surprised",  # 複雑な構造
        ]
    }
    
    subclause_issues = []
    
    for category, sentences in complex_test_cases.items():
        print(f"\n=== {category} ===")
        
        for sentence in sentences:
            print(f"\n入力: {sentence}")
            try:
                slots = analyzer.analyze_sentence(sentence)
                
                has_substructure = False
                for slot, candidates in slots.items():
                    if candidates:
                        candidate = candidates[0]
                        value = candidate['value']
                        
                        # サブ構造の検出
                        if (('that' in value and len(value.split()) > 3) or 
                            ('who' in value and len(value.split()) > 2) or
                            ('what' in value and len(value.split()) > 2) or
                            ('when' in value and len(value.split()) > 3) or
                            ('where' in value and len(value.split()) > 3) or
                            ('if' in value and len(value.split()) > 3)):
                            has_substructure = True
                            
                        pattern_info = f" [{candidate.get('pattern', '')}]" if candidate.get('pattern') else ""
                        print(f"  {slot}: {value} ({candidate.get('note', candidate['type'])}){pattern_info}")
                        
                        # サブ構造があるかチェック
                        if has_substructure and 'sub-' not in str(candidate):
                            subclause_issues.append(f"{category}: {sentence} - サブ構造未分解")
                
            except Exception as e:
                print(f"  ❌ エラー: {e}")
                subclause_issues.append(f"{category}: {sentence} - エラー: {e}")
    
    # サブクローズ対応の評価
    print(f"\n=== サブクローズ対応評価 ===")
    print(f"サブ構造未分解の問題: {len(subclause_issues)}件")
    
    if subclause_issues:
        print("\n🔧 サブクローズ対応が必要な項目:")
        for i, issue in enumerate(subclause_issues, 1):
            print(f"{i}. {issue}")
    else:
        print("\n✅ サブクローズ構造も正常に処理されています")
    
    return subclause_issues

def analyze_subclause_capability():
    """現在のサブクローズ処理能力分析"""
    print("\n=== 現在のサブクローズ処理能力分析 ===")
    
    # 単純なthat節の分析
    analyzer = RephraseIntegrationStep12()
    test_sentence = "I think that he is smart"
    
    print(f"分析対象: {test_sentence}")
    slots = analyzer.analyze_sentence(test_sentence)
    
    for slot, candidates in slots.items():
        if candidates and slot == 'O1':
            candidate = candidates[0]
            that_clause = candidate['value']
            print(f"\nO1スロット内容: '{that_clause}'")
            
            # that節内の語分析
            if that_clause.startswith('that '):
                inner_words = that_clause[5:].split()  # 'that 'を除く
                print(f"サブクローズ内の語: {inner_words}")
                print("現在の処理: that節全体を1つの塊として扱い")
                print("理想の処理: sub-s:he, sub-aux:is, sub-v:smart への分解")

if __name__ == "__main__":
    issues = test_complex_sentences()
    analyze_subclause_capability()
