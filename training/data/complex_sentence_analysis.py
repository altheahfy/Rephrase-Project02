#!/usr/bin/env python3
"""
実文テスト: "Because he was captured by bandits, I must go to the mountain where they live."
マルチエンジン協調システムによるRephrase式スロット分解
"""

import sys
import os
from typing import Dict, List, Any
import json

# 統合システムインポート
try:
    from integrated_multi_engine_coordinator import IntegratedMultiEngineCoordinator
except ImportError:
    print("⚠️ 統合システムが見つかりません")
    sys.exit(1)

def analyze_complex_sentence():
    """複雑文の詳細解析"""
    
    # 対象文
    target_sentence = "Because he was captured by bandits, I must go to the mountain where they live."
    
    print("🎯 Rephrase式スロット分解システム")
    print("=" * 80)
    print(f"対象文: '{target_sentence}'")
    print("=" * 80)
    
    # 統合協調システム初期化
    coordinator = IntegratedMultiEngineCoordinator()
    
    # この文に適用すべきエンジン群
    relevant_engines = [
        "Basic5Pattern",        # 基本5文型（主節・従属節両方）
        "PassiveVoice",         # 受動態（"was captured"）
        "ConditionalMood",      # 理由・条件節（"Because..."）
        "RelativePronoun",      # 関係代名詞（"where they live"）
        "AdverbialModifier",    # 副詞修飾
        "PrepositionalPhrase",  # 前置詞句（"by bandits", "to the mountain"）
        "TenseAspect"          # 時制・相（過去・現在・未来）
    ]
    
    # 文コンテキスト設定
    sentence_context = {
        "sentence_type": "complex",
        "has_subordinate_clause": True,
        "subordinate_types": ["reason", "relative"],
        "voice": "mixed",  # 能動態・受動態混在
        "tense": "mixed",  # 過去・現在・未来混在
        "complexity": "high"
    }
    
    print(f"\n🔧 適用エンジン群 ({len(relevant_engines)} エンジン):")
    for engine in relevant_engines:
        print(f"   • {engine}")
    
    print(f"\n📋 文コンテキスト:")
    for key, value in sentence_context.items():
        print(f"   • {key}: {value}")
    
    # マルチエンジン協調処理実行
    print(f"\n" + "="*80)
    result = coordinator.process_with_multi_engine_coordination(
        target_sentence,
        relevant_engines,
        sentence_context
    )
    print("="*80)
    
    # 詳細結果分析
    if result.success:
        print(f"\n✅ 協調処理成功!")
        print(f"   処理時間: {result.processing_time:.3f}秒")
        print(f"   総エンジン数: {sum(len(stage) for stage in result.execution_order)}")
        print(f"   実行段階数: {len(result.execution_order)}")
        
        # スロット分解結果
        print(f"\n🎯 **Rephrase式スロット分解結果**:")
        print("="*50)
        for slot, value in result.normalized_slots.items():
            print(f"   {slot:3} : '{value}'")
        
        # 品質レポート
        if result.quality_report:
            print(f"\n📊 **品質評価**:")
            print(f"   総合スコア: {result.quality_report.overall_score:.1f}%")
            print(f"   品質レベル: {result.quality_report.quality_level.value}")
            print(f"   検出問題数: {len(result.quality_report.issues)}")
            
            if result.quality_report.issues:
                print(f"\n⚠️ 検出された問題:")
                for i, issue in enumerate(result.quality_report.issues[:5], 1):
                    print(f"   {i}. {issue.description} ({issue.severity})")
            
            if result.quality_report.recommendations:
                print(f"\n💡 推奨改善:")
                for i, rec in enumerate(result.quality_report.recommendations[:3], 1):
                    print(f"   {i}. {rec}")
        
        # エンジン別結果詳細
        print(f"\n🔍 **エンジン別解析結果**:")
        print("="*50)
        for engine_name, engine_result in result.engine_results.items():
            print(f"\n   【{engine_name}】")
            for slot, value in engine_result.items():
                print(f"     {slot}: '{value}'")
        
        # 実行順序詳細
        print(f"\n⚡ **実行段階詳細**:")
        print("="*50)
        for stage_idx, stage_engines in enumerate(result.execution_order, 1):
            print(f"   段階{stage_idx}: {stage_engines}")
        
        # 文構造分析
        print(f"\n🏗️ **文構造分析**:")
        print("="*50)
        analyze_sentence_structure(result.normalized_slots, target_sentence)
        
    else:
        print(f"\n❌ 協調処理失敗: {result.error_message}")
    
    return result

def analyze_sentence_structure(slots: Dict[str, Any], original: str):
    """文構造詳細分析"""
    
    # 基本構造判定
    has_subject = 'S' in slots
    has_verb = 'V' in slots
    has_object = 'O1' in slots
    has_complement = 'C1' in slots or 'C2' in slots
    
    # 文型判定
    if has_subject and has_verb and not has_object and not has_complement:
        sentence_pattern = "SV (第1文型)"
    elif has_subject and has_verb and has_object and not has_complement:
        sentence_pattern = "SVO (第3文型)"
    elif has_subject and has_verb and not has_object and has_complement:
        sentence_pattern = "SVC (第2文型)"
    elif has_subject and has_verb and has_object and has_complement:
        sentence_pattern = "SVOC (第5文型)"
    elif 'O2' in slots:
        sentence_pattern = "SVOO (第4文型)"
    else:
        sentence_pattern = "複合文型"
    
    print(f"   基本文型: {sentence_pattern}")
    
    # 修飾語分析
    modifiers = [slot for slot in slots.keys() if slot.startswith('M')]
    if modifiers:
        print(f"   修飾語数: {len(modifiers)} 個")
        for mod in modifiers:
            print(f"     {mod}: '{slots[mod]}'")
    
    # 特殊構造分析
    special_structures = []
    
    if 'Aux' in slots:
        special_structures.append("助動詞構造")
    
    if any('REL_' in slot for slot in slots.keys()):
        special_structures.append("関係節構造")
    
    if any('PASS' in slot for slot in slots.keys()):
        special_structures.append("受動態構造")
    
    if any('COMP_' in slot for slot in slots.keys()):
        special_structures.append("比較構造")
    
    if special_structures:
        print(f"   特殊構造: {', '.join(special_structures)}")
    
    # 複雑度評価
    complexity_score = len(slots) + len(modifiers) * 2 + len(special_structures) * 3
    
    if complexity_score <= 5:
        complexity_level = "単純"
    elif complexity_score <= 10:
        complexity_level = "標準"
    elif complexity_score <= 15:
        complexity_level = "複雑"
    else:
        complexity_level = "高度複雑"
    
    print(f"   複雑度: {complexity_level} (スコア: {complexity_score})")
    
    # 元文との対応関係
    print(f"   スロット数: {len(slots)} 個")
    print(f"   元文長: {len(original.split())} 語")
    coverage_ratio = len(slots) / max(len(original.split()), 1) * 100
    print(f"   カバー率: {coverage_ratio:.1f}%")

if __name__ == "__main__":
    # 実行
    result = analyze_complex_sentence()
