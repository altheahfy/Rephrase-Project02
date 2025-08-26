"""
Step18改善結果分析 - Sスロット精度向上確認
"""

def analyze_s_slot_improvement():
    """Sスロット改善結果分析"""
    
    print("=" * 80)
    print("📈 Sスロット改善結果分析")
    print("=" * 80)
    
    # 改善前後の比較
    before_s = {
        'sub-s': 'manager who',           # ❌ theが欠如
        'sub-aux': 'had',                 # ✅
        'sub-m2': 'recently',             # ✅  
        'sub-v': 'taken',                 # ✅
        'sub-o1': 'charge'                # ❌ of the projectが欠如
    }
    
    after_s = {
        'sub-s': 'manager who',           # ❌ theまだ欠如
        'sub-aux': 'had',                 # ✅
        'sub-m2': 'recently',             # ✅
        'sub-v': 'taken',                 # ✅
        'sub-o1': 'charge of the project' # ✅ 前置詞句統合成功！
    }
    
    expected_s = {
        'sub-s': 'the manager who',
        'sub-aux': 'had',
        'sub-m2': 'recently',
        'sub-v': 'taken', 
        'sub-o1': 'charge of the project'
    }
    
    print("\n🔍 改善結果詳細:")
    
    improvements = 0
    remaining_issues = 0
    
    for key in expected_s:
        before_val = before_s.get(key, "❌ 欠如")
        after_val = after_s.get(key, "❌ 欠如") 
        expected_val = expected_s[key]
        
        if before_val != expected_val and after_val == expected_val:
            print(f"✅ {key}: 改善成功!")
            print(f"   改善前: '{before_val}'")
            print(f"   改善後: '{after_val}' ← 期待値と一致")
            improvements += 1
        elif after_val != expected_val:
            print(f"❌ {key}: まだ問題あり")
            print(f"   現在値: '{after_val}'")
            print(f"   期待値: '{expected_val}'")
            remaining_issues += 1
        else:
            print(f"✅ {key}: 既に正確")
            print(f"   値: '{after_val}'")
    
    # 精度計算
    total_subslots = len(expected_s)
    correct_after = sum(1 for k in expected_s if after_s.get(k) == expected_s[k])
    
    before_accuracy = 60.0  # 3/5
    after_accuracy = (correct_after / total_subslots) * 100
    
    print(f"\n📊 精度変化:")
    print(f"  改善前: {before_accuracy}% (3/5)")
    print(f"  改善後: {after_accuracy}% ({correct_after}/{total_subslots})")
    print(f"  改善度: +{after_accuracy - before_accuracy}%")
    
    if improvements > 0:
        print(f"\n🎉 成功した改善: {improvements}項目")
    
    if remaining_issues > 0:
        print(f"\n🔧 残る課題: {remaining_issues}項目")
        print("  次回改善ターゲット: sub-s の冠詞'the'統合")
    
    return after_accuracy

if __name__ == "__main__":
    analyze_s_slot_improvement()
