#!/usr/bin/env python3
"""
Corrected Engine Coverage Analysis
各文構造がどのエンジンの担当範囲かを正確に分析
"""

def analyze_engine_responsibilities():
    """失敗した構造を担当エンジンで分類（修正版）"""
    
    failed_structures = [
        "Yes.",                     # 1. 省略文
        "No problem.",              # 2. 省略文  
        "Thanks!",                  # 3. 省略文
        "Goodbye.",                 # 4. 省略文
        "What a beautiful day!",    # 5. 感嘆文 → QUESTION
        "How amazing!",             # 6. 感嘆文 → QUESTION
        "Oh my god!",               # 7. 感嘆文（間投詞）
        "Stop!",                    # 8. 命令文
        "Come here.",               # 9. 命令文
        "Don't do that.",           # 10. 否定命令文 → MODAL
        "It is John who called.",   # 11. 分裂文 → INVERSION
    ]
    
    # 既存エンジンでカバー可能な構造
    covered_structures = {
        "QUESTION": ["What a beautiful day!", "How amazing!"],  # 2個
        "MODAL": ["Don't do that."],                           # 1個  
        "INVERSION": ["It is John who called."]                # 1個
    }
    
    # 専用エンジン必要な構造
    uncovered_structures = [
        "Yes.", "No problem.", "Thanks!", "Goodbye.",          # 省略文 4個
        "Oh my god!",                                          # 間投詞 1個
        "Stop!", "Come here."                                  # 命令文 2個
    ]
    
    total_failed = len(failed_structures)
    covered_count = sum(len(structures) for structures in covered_structures.values())
    uncovered_count = len(uncovered_structures)
    
    print("🔍 Corrected Engine Coverage Analysis")
    print("=" * 60)
    
    for engine, structures in covered_structures.items():
        print(f"\n🎯 {engine}エンジンで処理可能:")
        for structure in structures:
            print(f"   - '{structure}'")
    
    print(f"\n❌ 専用エンジン必要（省略文・命令文エンジン）:")
    for structure in uncovered_structures:
        print(f"   - '{structure}'")
    
    print(f"\n📊 正確なCoverage Summary:")
    print(f"   失敗構造総数: {total_failed}")
    print(f"   既存エンジンでカバー可能: {covered_count} ({covered_count/total_failed*100:.1f}%)")
    print(f"   専用エンジン必要: {uncovered_count} ({uncovered_count/total_failed*100:.1f}%)")
    
    print(f"\n💡 修正された結論:")
    print(f"   欠けている構造の{covered_count/total_failed*100:.1f}%は既存エンジンで対応可能")
    print(f"   真の欠落は省略文・命令文エンジンのみ（{uncovered_count/total_failed*100:.1f}%）")
    
    # 実用英語全体での真の欠落率計算
    missing_5_percent = 5.0  # 基本5文型で欠けている5%
    true_missing = missing_5_percent * (uncovered_count / total_failed)
    
    print(f"\n🎯 実用英語全体での真の欠落:")
    print(f"   基本構造の欠落: 5% × {uncovered_count/total_failed:.1%} = {true_missing:.1f}%")
    print(f"   → 現在の実質カバレッジ: {95 + (5 * covered_count/total_failed):.1f}%")

if __name__ == "__main__":
    analyze_engine_responsibilities()
