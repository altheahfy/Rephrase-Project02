"""
🔍 超複雑文の詳細分解結果表示
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator

def show_detailed_breakdown():
    """詳細分解結果表示"""
    print("🔍 超複雑文の詳細分解結果")
    print("=" * 80)
    
    engine = SimpleUnifiedRephraseSlotIntegrator()
    
    complex_sentence = ("That afternoon at the crucial point in the presentation, "
                       "the manager who had recently taken charge of the project "
                       "had to make the committee responsible for implementation "
                       "deliver the final proposal flawlessly even though he was "
                       "under intense pressure so the outcome would reflect their full potential.")
    
    print("📝 入力文:")
    print(f"   {complex_sentence}")
    print()
    
    # 解析実行
    result = engine.process(complex_sentence)
    
    if 'error' in result:
        print(f"❌ エラー: {result['error']}")
        return
    
    # **全スロット**の詳細表示
    all_slots = result['slots']
    
    print("🔧 **全スロット分解結果（空を含む）**:")
    print("=" * 60)
    
    # 上位スロット
    upper_slots = ['M1', 'S', 'Aux', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3']
    print("🏗️  上位スロット:")
    for slot in upper_slots:
        content = all_slots.get(slot, "")
        status = "✅" if content else "⬜"
        print(f"   {status} {slot:4s}: '{content}'")
    
    print()
    
    # サブスロット
    sub_slots = ['sub-m1', 'sub-s', 'sub-aux', 'sub-m2', 'sub-v', 
                 'sub-c1', 'sub-o1', 'sub-o2', 'sub-c2', 'sub-m3']
    print("🔗 サブスロット:")
    for slot in sub_slots:
        content = all_slots.get(slot, "")
        status = "✅" if content else "⬜"
        print(f"   {status} {slot:8s}: '{content}'")
    
    print()
    print("📊 メタデータ:")
    print(f"   🎯 主要文法: {result['primary_grammar']}")
    print(f"   📈 信頼度: {result['confidence']:.3f}")
    print(f"   🔬 複雑度: {result['complexity_score']:.3f}")
    print(f"   🔧 検出パターン数: {result['detected_patterns']}")
    print(f"   ⚙️  エンジン: {result['engine']}")
    print()
    
    # 期待される分解との比較
    print("🎯 **期待される理想的な分解:**")
    print("=" * 60)
    
    expected = {
        'M1': 'That afternoon at the crucial point in the presentation',
        'S': 'the manager who had recently taken charge of the project', 
        'Aux': 'had to',
        'V': 'make',
        'O1': 'the committee responsible for implementation',
        'O2': 'deliver the final proposal flawlessly',
        'M2': 'even though he was under intense pressure',
        'M3': 'so the outcome would reflect their full potential'
    }
    
    print("🏗️  期待される上位スロット:")
    for slot in upper_slots:
        expected_content = expected.get(slot, "")
        actual_content = all_slots.get(slot, "")
        
        if expected_content:
            match_status = "✅" if actual_content == expected_content else ("🔶" if actual_content else "❌")
            print(f"   {match_status} {slot:4s}: '{expected_content}'")
            if actual_content and actual_content != expected_content:
                print(f"        実際: '{actual_content}'")
        else:
            if actual_content:
                print(f"   ❓ {slot:4s}: (期待なし) → 実際: '{actual_content}'")
    
    print()
    print("📋 **詳細比較結果:**")
    print("=" * 40)
    
    matches = 0
    partial_matches = 0
    total_expected = len([k for k, v in expected.items() if v])
    
    for slot, expected_content in expected.items():
        if expected_content:
            actual_content = all_slots.get(slot, "")
            if actual_content == expected_content:
                matches += 1
                print(f"   ✅ {slot}: 完全一致")
            elif actual_content:
                if expected_content.lower() in actual_content.lower() or actual_content.lower() in expected_content.lower():
                    partial_matches += 1
                    print(f"   🔶 {slot}: 部分一致")
                else:
                    print(f"   ❌ {slot}: 不一致")
            else:
                print(f"   ⬜ {slot}: 未検出")
    
    print()
    print(f"📊 **最終評価:**")
    print(f"   完全一致: {matches}/{total_expected} ({matches/total_expected*100:.1f}%)")
    print(f"   部分一致: {partial_matches}/{total_expected} ({partial_matches/total_expected*100:.1f}%)")
    print(f"   総合精度: {(matches + partial_matches*0.5)/total_expected*100:.1f}%")

if __name__ == "__main__":
    show_detailed_breakdown()
