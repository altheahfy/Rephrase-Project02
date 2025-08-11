"""
冠詞'the'欠如問題の詳細分析と修正アプローチ
"""

import spacy

def analyze_det_issue():
    """冠詞'the'問題の構造分析"""
    
    print("=" * 60)
    print("🔍 冠詞'the'欠如問題の構造分析") 
    print("=" * 60)
    
    nlp = spacy.load('en_core_web_sm')
    
    # 問題のある部分を抽出
    fragment = "the manager who had recently taken charge"
    doc = nlp(fragment)
    
    print(f"🎯 対象フラグメント: '{fragment}'")
    print("\n依存関係詳細:")
    
    for token in doc:
        print(f"  {token.text:<10} | {token.dep_:<10} | {token.pos_:<8} | head: {token.head.text}")
    
    print("\n🔍 現在のスパン拡張が'the'を含めない理由:")
    
    manager_token = None
    the_token = None
    
    for token in doc:
        if token.text == 'manager':
            manager_token = token
        elif token.text == 'the':
            the_token = token
    
    if manager_token and the_token:
        print(f"  'the'のhead: {the_token.head.text} (dep: {the_token.dep_})")
        print(f"  'manager'のhead: {manager_token.head.text} (dep: {manager_token.dep_})")
        print(f"  'the'は'manager'の子要素: {the_token.head == manager_token}")
        
        # 子要素確認
        manager_children = list(manager_token.children)
        print(f"  'manager'の子要素: {[child.text for child in manager_children]}")
        
    print(f"\n🛠️ 修正アプローチ:")
    print(f"  1. スパン拡張時にdet依存関係の子要素を確実に含める")
    print(f"  2. 左方向への拡張処理を強化")

if __name__ == "__main__":
    analyze_det_issue()
