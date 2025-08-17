#!/usr/bin/env python3
"""
54.7%精度時点でのエラー分析スクリプト
関係副詞sub-m1修正後の残存エラーパターンを特定
"""
import json

def analyze_errors():
    """残存エラーを分析して優先順位付け"""
    
    # 主要なエラーパターン
    error_patterns = [
        {
            "pattern": "sub-o1 missing",
            "examples": [18],
            "description": "関係副詞でのオブジェクト省略",
            "impact": 1,
        },
        {
            "pattern": "agent vs adverb priority", 
            "examples": [24, 37, 38, 39],
            "description": "agent句と副詞の配置優先順位",
            "impact": 4,
        },
        {
            "pattern": "省略関係代名詞",
            "examples": [19],
            "description": "省略関係代名詞の検出不足",
            "impact": 1,
        },
        {
            "pattern": "as if 構文",
            "examples": [28],
            "description": "as if節の未対応",
            "impact": 1,
        },
        {
            "pattern": "複合副詞配置",
            "examples": [31, 32, 33, 34, 46, 47, 48],
            "description": "関係節内副詞と主節副詞の配置混在",
            "impact": 7,
        },
        {
            "pattern": "関係代名詞主語認識",
            "examples": [35],
            "description": "関係代名詞主語の誤認識",
            "impact": 1,
        },
        {
            "pattern": "分詞構文",
            "examples": [49, 50, 51, 52],
            "description": "分詞構文の不完全対応",
            "impact": 4,
        },
        {
            "pattern": "副詞のM2/M3配置",
            "examples": [36, 53],
            "description": "副詞配置の微調整",
            "impact": 2,
        },
        {
            "pattern": "大文字小文字不整合",
            "examples": [40],
            "description": "期待値の大文字小文字不一致",
            "impact": 1,
        },
        {
            "pattern": "was/Aux認識",
            "examples": [42],
            "description": "be動詞のAux/V認識問題",
            "impact": 1,
        },
    ]
    
    print("🔍 54.7%精度時点での主要エラーパターン分析")
    print("=" * 60)
    
    total_impact = sum(p["impact"] for p in error_patterns)
    
    # 影響度順にソート
    error_patterns.sort(key=lambda x: x["impact"], reverse=True)
    
    for i, pattern in enumerate(error_patterns, 1):
        accuracy_gain = (pattern["impact"] / 53) * 100
        print(f"\n{i}. {pattern['pattern']}")
        print(f"   影響例文: {pattern['examples']}")
        print(f"   影響度: {pattern['impact']}例文 (+{accuracy_gain:.1f}%)")
        print(f"   説明: {pattern['description']}")
    
    print(f"\n📊 総残存エラー: {total_impact}/53例文")
    print(f"🎯 理論的最大精度: {((53-total_impact)/53)*100:.1f}%")
    
    # 次の取り組み提案
    print("\n🎯 次に取り組むべき優先順位:")
    for i, pattern in enumerate(error_patterns[:3], 1):
        print(f"{i}. {pattern['pattern']} ({pattern['impact']}例文)")

if __name__ == "__main__":
    analyze_errors()
