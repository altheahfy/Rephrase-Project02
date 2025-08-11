"""
Step2: managerスパン拡張の修正実装
関係代名詞のみ含めて関係節動詞は除外
"""

def show_fix_approach():
    print("🔧 修正方法:")
    print("正解データ: 'the manager who'")
    print("現在結果  : 'the manager who had recently taken'")
    print("問題      : relcl拡張で関係節動詞まで含まれている")
    print()
    print("解決策    : relcl処理で関係代名詞(who)のみ含める")
    print("         関係節動詞(taken)とその修飾語は別のサブスロットで処理")
    print()
    print("修正後期待: 'the manager who'")

def create_fixed_expand_span():
    print("\n修正版_expand_span()ロジック:")
    print()
    print("```python")
    print("def _expand_span(self, token, doc):")
    print("    expand_deps = ['det', 'poss', 'compound', 'amod']  # relclを除外")
    print("    ")
    print("    start = token.i")
    print("    end = token.i") 
    print("    ")
    print("    # 基本的な子要素拡張")
    print("    for child in token.children:")
    print("        if child.dep_ in expand_deps:")
    print("            start = min(start, child.i)")
    print("            end = max(end, child.i)")
    print("    ")        
    print("    # 関係節の場合は関係代名詞のみ含める")
    print("    for child in token.children:")
    print("        if child.dep_ == 'relcl':")
    print("            # 関係代名詞(who)のみ探して含める")
    print("            for relcl_child in child.children:")
    print("                if (relcl_child.dep_ == 'nsubj' and ")
    print("                    relcl_child.pos_ == 'PRON'):")
    print("                    start = min(start, relcl_child.i)")
    print("                    # 関係代名詞のみなのでend更新不要")
    print("                    break")
    print("    ")
    print("    return ' '.join([doc[i].text for i in range(start, end + 1)])")
    print("```")

if __name__ == "__main__":
    show_fix_approach()
    create_fixed_expand_span()
