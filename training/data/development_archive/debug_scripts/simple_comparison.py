"""
シンプルな正解データ vs 出力結果の並列表示
"""

def show_simple_comparison():
    print("=" * 100)
    print("ex007 - 正解データ vs 出力結果")
    print("=" * 100)
    
    # 正解データ
    expected = {
        'S': {
            'sub-s': 'the manager who',
            'sub-aux': 'had',
            'sub-m2': 'recently',
            'sub-v': 'taken',
            'sub-o1': 'charge of the project'
        },
        'V': {
            'v': 'had'
        },
        'O1': {
            'sub-aux': 'to',
            'sub-s': 'the committee',
            'sub-v': 'make',
            'sub-o1': 'the implementation',
            'sub-c2': 'responsible',
            'sub-m3': 'for'
        },
        'C2': {
            'sub-v': 'deliver',
            'sub-o1': 'the final proposal',
            'sub-m3': 'flawlessly'
        },
        'M2': {
            'sub-m1': 'even though',
            'sub-s': 'he',
            'sub-v': 'was',
            'sub-m2': 'under intense pressure'
        },
        'M3': {
            'sub-m1': 'so',
            'sub-s': 'the outcome',
            'sub-aux': 'would',
            'sub-v': 'reflect',
            'sub-o1': 'their full potential'
        }
    }
    
    # 現在の出力結果
    actual = {
        'S': {
            'sub-s': 'manager who',           # ❌ 'the'欠如
            'sub-aux': 'had',                 # ✅
            'sub-m2': 'recently',             # ✅
            'sub-v': 'taken',                 # ✅
            'sub-o1': 'charge of the project' # ✅
        },
        'V': {
            'v': 'had'                        # ✅
        },
        'O1': {
            'sub-aux': 'to',                  # ✅
            'sub-c2': 'responsible',          # ✅
            'sub-v': 'make'                   # ✅
            # 欠如: sub-s, sub-o1, sub-m3
        },
        'C2': {
            'sub-v': 'deliver',               # ✅
            'sub-o1': 'the final proposal',   # ✅
            'sub-m3': 'flawlessly'            # ✅
        },
        'M2': {
            'sub-m1': 'even though',          # ✅
            'sub-s': 'he',                    # ✅
            'sub-v': 'was under intense pressure',  # ❌ 'was'のみ期待
            'sub-m2': 'even',                 # ❌ 'under intense pressure'期待
            'sub-m3': 'under'                 # ❌ 不要
        },
        'M3': {
            'sub-m1': 'so',                   # ✅
            'sub-s': 'the outcome',           # ✅
            'sub-aux': 'would',               # ✅
            'sub-v': 'reflect',               # ✅
            'sub-o1': 'their full potential'  # ✅
        }
    }
    
    # 並列表示
    all_slots = sorted(set(expected.keys()) | set(actual.keys()))
    
    for slot in all_slots:
        print(f"\n【{slot}スロット】")
        print("-" * 80)
        
        exp_slot = expected.get(slot, {})
        act_slot = actual.get(slot, {})
        
        all_subslots = sorted(set(exp_slot.keys()) | set(act_slot.keys()))
        
        if all_subslots:
            print(f"{'サブスロット':<12} | {'正解データ':<30} | {'出力結果':<30} | 判定")
            print("-" * 80)
            
            for subslot in all_subslots:
                exp_val = exp_slot.get(subslot, "---")
                act_val = act_slot.get(subslot, "---")
                
                if exp_val == act_val:
                    status = "✅"
                elif exp_val == "---":
                    status = "🔸"  # 不要な出力
                elif act_val == "---":
                    status = "❌"  # 欠如
                else:
                    status = "❌"  # 不一致
                
                print(f"{subslot:<12} | {exp_val:<30} | {act_val:<30} | {status}")

if __name__ == "__main__":
    show_simple_comparison()
