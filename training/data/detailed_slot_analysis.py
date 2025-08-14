"""
🔍 統合Rephraseスロット分解 - 詳細検証・修正フェーズ
分解結果の精度向上とエラー修正
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator

def detailed_analysis_session():
    """詳細分析セッション - 分解結果チェック用"""
    print("🔍 統合Rephraseスロット分解 - 詳細検証セッション")
    print("=" * 70)
    
    integrator = SimpleUnifiedRephraseSlotIntegrator()
    
    # より詳細なテスト文例
    detailed_test_cases = [
        {
            'sentence': "I study English.",
            'expected': {
                'S': 'I',
                'V': 'study', 
                'O1': 'English'
            },
            'description': '基本SVO'
        },
        {
            'sentence': "She is a teacher.",
            'expected': {
                'S': 'She',
                'V': 'is',
                'C1': 'a teacher'  # 冠詞"a"を含む
            },
            'description': '基本SVC'
        },
        {
            'sentence': "There are many students.",
            'expected': {
                'S': 'There',
                'V': 'are',
                'O1': 'many students'  # ← C1ではなくO1？
            },
            'description': 'There構文'
        },
        {
            'sentence': "I think that he is right.",
            'expected': {
                'S': 'I',  # ← 主文の主語
                'V': 'think',
                'O1': 'that he is right',  # ← 名詞節全体
                'sub-s': 'he',
                'sub-v': 'is',
                'sub-c1': 'right'
            },
            'description': '名詞節（that節）'
        },
        {
            'sentence': "The letter was written by John.",
            'expected': {
                'S': 'The letter',
                'Aux': 'was',
                'V': 'written',
                'M2': 'by John'  # 修飾語として正しく配置
            },
            'description': '受動態'
        },
        {
            'sentence': "Yesterday, I carefully finished my work early.",
            'expected': {
                'M1': 'Yesterday',  # ← 文頭副詞
                'S': 'I',
                'M2': 'carefully',
                'V': 'finished',
                'O1': 'my work',  # ← 所有格も含める？
                'M3': 'early'
            },
            'description': '複数修飾語'
        }
    ]
    
    print("📊 現在の分解結果と期待値の比較:")
    print()
    
    for i, test_case in enumerate(detailed_test_cases, 1):
        sentence = test_case['sentence']
        expected = test_case['expected']
        description = test_case['description']
        
        print(f"🧪 テスト {i}: {description}")
        print(f"   📝 入力: \"{sentence}\"")
        
        # 実際の分解実行
        result = integrator.process(sentence)
        actual_slots = {k: v for k, v in result['slots'].items() if v}
        
        print(f"   🔧 実際の結果:")
        for slot, content in actual_slots.items():
            print(f"      {slot}: '{content}'")
        
        print(f"   🎯 期待値:")
        for slot, content in expected.items():
            print(f"      {slot}: '{content}'")
        
        # 比較・問題点指摘
        print(f"   📋 検証結果:")
        issues = []
        
        for exp_slot, exp_content in expected.items():
            actual_content = actual_slots.get(exp_slot, "")
            if actual_content != exp_content:
                if not actual_content:
                    issues.append(f"❌ {exp_slot}が未検出 (期待:'{exp_content}')")
                else:
                    issues.append(f"⚠️ {exp_slot}が不正確 (実際:'{actual_content}' vs 期待:'{exp_content}')")
        
        # 余計なスロット検出
        for act_slot, act_content in actual_slots.items():
            if act_slot not in expected:
                issues.append(f"❓ 予期しない{act_slot}:'{act_content}'")
        
        if issues:
            for issue in issues:
                print(f"      {issue}")
        else:
            print(f"      ✅ 完全一致")
        
        print()
    
    print("=" * 70)
    print("🎯 修正が必要な主要問題:")
    print("1. SVC文でのV(be動詞)検出漏れ")
    print("2. There構文でのO1/C1判定")
    print("3. 複文での主文・従属文スロット分離")
    print("4. 受動態のby句重複問題")
    print("5. 冠詞・所有格を含む句の範囲")
    print("6. 文頭副詞の位置判定")
    print()
    print("🔧 どの問題から修正を開始しますか？")

if __name__ == "__main__":
    detailed_analysis_session()
