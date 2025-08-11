"""
Step4: 簡易版修正確認
エンコーディング問題を避けてロジック確認
"""

def simulate_fixed_expand_span():
    """修正版スパン拡張のシミュレーション"""
    
    print("🔧 修正版スパン拡張のシミュレーション")
    print("=" * 50)
    
    # 想定されるmanagerトークンの情報
    print("入力データ:")
    print("  トークン: 'manager'")
    print("  子要素: ['the' (det), 'taken' (relcl)]") 
    print("  taken の子要素: ['who' (nsubj, PRON), ...]")
    
    print(f"\n修正版ロジック実行:")
    
    # 1. 基本拡張処理
    print("Step1: 基本的な子要素拡張")
    print("  expand_deps = ['det', 'poss', 'compound', 'amod']")
    print("  'the' (det) → 拡張対象 ✅")
    print("  範囲: [0, 1] = 'the manager'")
    
    # 2. 関係節処理  
    print("\nStep2: 関係節処理")
    print("  'taken' (relcl) → 関係節として特別処理")
    print("  taken の子要素から関係代名詞検索:")
    print("    'who' (nsubj, PRON) → 関係代名詞 ✅")
    print("    'who'のindex=2 を start に反映")
    print("  範囲: [0, 1] (endは更新しない)")
    
    # 3. 最終結果
    print(f"\nStep3: 最終結果")
    print("  スパン範囲: [0, 1]")  
    print("  結果: 'the manager'")
    
    print(f"\n❌ 問題発見:")
    print("  期待値: 'the manager who'")
    print("  結果  : 'the manager'")
    print("  問題  : 関係代名詞'who'が含まれない")
    
    print(f"\n🔧 追加修正が必要:")
    print("  関係代名詞のindexもend範囲に含める必要がある")

def show_additional_fix():
    """追加修正方法の表示"""
    
    print(f"\n{'='*50}")
    print("🔧 追加修正アプローチ")
    print("="*50)
    
    print("問題: 関係代名詞'who'のindexがend範囲に反映されない")
    print("解決策: 関係代名詞発見時にendも更新する")
    
    print(f"\n修正後のロジック:")
    print("```python")
    print("# 関係節の関係代名詞処理")
    print("if relcl_child.dep_ == 'nsubj' and relcl_child.pos_ == 'PRON':")
    print("    start = min(start, relcl_child.i)")
    print("    end = max(end, relcl_child.i)      # ← この行を追加")
    print("```")
    
    print(f"\n期待される修正後結果:")
    print("  範囲: [0, 2] = 'the manager who'")

if __name__ == "__main__":
    simulate_fixed_expand_span()
    show_additional_fix()
