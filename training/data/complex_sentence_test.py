"""
🔍 統合エンジン実力テスト - 超複雑文チャレンジ
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator

def complex_sentence_challenge():
    """超複雑文チャレンジテスト"""
    print("🔥 統合エンジン実力テスト - 超複雑文チャレンジ")
    print("=" * 80)
    
    engine = SimpleUnifiedRephraseSlotIntegrator()
    
    # ユーザー提供の超複雑文
    complex_sentence = ("That afternoon at the crucial point in the presentation, "
                       "the manager who had recently taken charge of the project "
                       "had to make the committee responsible for implementation "
                       "deliver the final proposal flawlessly even though he was "
                       "under intense pressure so the outcome would reflect their full potential.")
    
    print("📝 テスト文:")
    print(f"   {complex_sentence}")
    print()
    print(f"📊 文の統計:")
    words = complex_sentence.split()
    print(f"   語数: {len(words)}語")
    print(f"   文字数: {len(complex_sentence)}文字")
    print()
    
    # 解析実行
    print("🔧 統合エンジン解析実行中...")
    print("-" * 50)
    
    try:
        result = engine.process(complex_sentence)
        
        if 'error' in result:
            print(f"❌ 解析エラー: {result['error']}")
            return
        
        print("✅ 解析成功！")
        print()
        
        # 基本情報
        print("📈 解析結果概要:")
        print(f"   🎯 主要文法: {result['primary_grammar']}")
        print(f"   📊 信頼度: {result['confidence']:.2f}")
        print(f"   🔬 複雑度: {result['complexity_score']:.2f}")
        print(f"   🔧 検出パターン数: {result['detected_patterns']}")
        print()
        
        # スロット分解結果詳細表示
        all_slots = result['slots']
        filled_slots = {k: v for k, v in all_slots.items() if v}
        
        print(f"🔧 スロット分解結果 (検出数: {len(filled_slots)}):")
        print("-" * 50)
        
        # 上位スロット（主構造）
        upper_slots = ['M1', 'S', 'Aux', 'M2', 'V', 'C1', 'O1', 'O2', 'C2', 'M3']
        print("🏗️ 主構造スロット:")
        upper_found = False
        for slot in upper_slots:
            if slot in filled_slots:
                content = filled_slots[slot]
                print(f"   {slot:4s}: '{content}'")
                upper_found = True
        
        if not upper_found:
            print("   (検出されませんでした)")
        
        print()
        
        # サブスロット（従属構造）  
        sub_slots = [k for k in filled_slots.keys() if k.startswith('sub-')]
        if sub_slots:
            print("🔗 従属構造スロット:")
            for slot in sorted(sub_slots):
                content = filled_slots[slot]
                print(f"   {slot:8s}: '{content}'")
        else:
            print("🔗 従属構造スロット: (なし)")
        
        print()
        
        # 構造分析
        print("🧐 構造分析:")
        print("-" * 30)
        
        # 主語の複雑さ
        if 'S' in filled_slots:
            subject = filled_slots['S']
            print(f"   主語: '{subject}'")
            if len(subject.split()) > 3:
                print("     → 複合主語として検出")
            else:
                print("     → シンプル主語として検出")
        
        # 動詞の検出
        if 'V' in filled_slots:
            verb = filled_slots['V']
            print(f"   動詞: '{verb}'")
        
        # 目的語の複雑さ
        if 'O1' in filled_slots:
            obj = filled_slots['O1']
            print(f"   目的語: '{obj}'")
            if len(obj.split()) > 5:
                print("     → 複合目的語として検出")
        
        # 修飾語の配置
        modifiers = ['M1', 'M2', 'M3']
        detected_mods = [m for m in modifiers if m in filled_slots]
        if detected_mods:
            print(f"   修飾語配置: {', '.join(detected_mods)}")
            for mod in detected_mods:
                print(f"     {mod}: '{filled_slots[mod]}'")
        
        print()
        
        # 精度評価
        print("📊 精度評価:")
        print("-" * 20)
        
        expected_elements = [
            "時間表現 (That afternoon)",
            "複合主語 (the manager who...)",
            "複合動詞句 (had to make)",
            "複合目的語 (the committee...)",
            "動詞句 (deliver)",
            "副詞節 (even though...)",
            "目的節 (so the outcome...)"
        ]
        
        detected_count = len(filled_slots)
        total_expected = len(expected_elements)
        
        print(f"   期待要素数: {total_expected}")
        print(f"   検出要素数: {detected_count}")
        
        if detected_count >= total_expected * 0.7:
            print("   ✅ 高精度検出 (70%以上)")
        elif detected_count >= total_expected * 0.5:
            print("   🔶 中精度検出 (50-70%)")
        else:
            print("   ❌ 低精度検出 (50%未満)")
        
        print()
        print("🎯 総合評価:")
        
        if len(filled_slots) >= 8 and 'S' in filled_slots and 'V' in filled_slots:
            print("   🏆 **優秀** - 超複雑文を適切に処理")
            print("   → 統合エンジンの実用性確認")
        elif len(filled_slots) >= 5:
            print("   ✅ **良好** - 基本構造は把握")
            print("   → 実用レベルに到達")
        else:
            print("   ⚠️ **要改善** - 複雑文への対応不足")
            print("   → さらなる改良が必要")
        
    except Exception as e:
        print(f"💥 解析中にエラーが発生: {str(e)}")
        print("   → 超複雑文による処理限界の可能性")

if __name__ == "__main__":
    complex_sentence_challenge()
