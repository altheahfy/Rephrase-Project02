"""
ex007正解データとStep18階層システム比較
"""

def compare_ex007_results():
    """ex007の正解データと階層システム結果比較"""
    
    # 正解データ（expected）
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
    
    # Step18完全システム結果（最終版）
    step18_result = {
        'S': {
            'sub-s': 'manager who',           # 期待: 'the manager who'
            'sub-aux': 'had',                # ✅
            'sub-m2': 'recently',            # ✅
            'sub-v': 'taken',                # ✅
            'sub-o1': 'charge'               # 期待: 'charge of the project'
        },
        'V': {
            'v': 'had'                       # ✅
        },
        'O1': {
            'sub-aux': 'to',                 # ✅
            'sub-c2': 'responsible',         # ✅
            'sub-v': 'make'                  # ✅
            # 欠如: sub-s, sub-o1, sub-m3
        },
        'C2': {
            'sub-v': 'deliver',              # ✅
            'sub-o1': 'the final proposal',  # ✅
            'sub-m3': 'flawlessly'           # ✅
        },
        'M2': {
            'sub-m1': 'even though',         # ✅
            'sub-s': 'he',                   # ✅
            'sub-v': 'was under intense pressure',  # 期待: 'was'
            'sub-m2': 'even',                # 期待: 'under intense pressure'
            'sub-m3': 'under'                # 不要（M2では想定外）
        },
        'M3': {
            'sub-m1': 'so',                  # ✅
            'sub-s': 'the outcome',          # ✅
            'sub-aux': 'would',              # ✅
            'sub-v': 'reflect',              # ✅
            'sub-o1': 'their full potential' # ✅
        }
    }
    
    print("=== ex007 正解データ vs Step18階層システム比較 ===\n")
    
    all_slots = set(expected.keys()) | set(step18_result.keys())
    
    for slot in sorted(all_slots):
        print(f"📋 {slot}スロット:")
        
        expected_slot = expected.get(slot, {})
        step18_slot = step18_result.get(slot, {})
        
        all_subslots = set(expected_slot.keys()) | set(step18_slot.keys())
        
        matches = 0
        total_subslots = len(all_subslots)
        
        for subslot in sorted(all_subslots):
            exp_val = expected_slot.get(subslot, "❌ 欠如")
            step18_val = step18_slot.get(subslot, "❌ 欠如")
            
            if exp_val == step18_val:
                status = "✅"
                matches += 1
            else:
                status = "❌"
            
            print(f"  {subslot:<10} {status}")
            print(f"    期待値   : \"{exp_val}\"")
            print(f"    Step18   : \"{step18_val}\"")
        
        accuracy = (matches / total_subslots * 100) if total_subslots > 0 else 0
        print(f"  精度: {matches}/{total_subslots} ({accuracy:.1f}%)\n")

if __name__ == "__main__":
    compare_ex007_results()
