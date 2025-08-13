#!/usr/bin/env python3
"""
現在の動作確認テスト - 依存関係回避版

実際に現在のgrammar_master_controller_v2.pyのエンジン選択ロジックがどう動作するかテスト
"""

import sys
import os
from typing import Dict, List, Optional, Any
from enum import Enum

# 最小限のモック定義
class EngineType(Enum):
    BASIC_FIVE_PATTERN = "basic_five_pattern"
    MODAL = "modal"
    CONJUNCTION = "conjunction"
    RELATIVE = "relative"
    PASSIVE = "passive"
    PROGRESSIVE = "progressive"
    PREPOSITIONAL = "prepositional"
    PERFECT_PROGRESSIVE = "perfect_progressive"
    SUBJUNCTIVE = "subjunctive"
    INVERSION = "inversion"
    COMPARATIVE = "comparative"
    GERUND = "gerund"
    PARTICIPLE = "participle"
    INFINITIVE = "infinitive"
    QUESTION = "question"

class MockEngineInfo:
    def __init__(self, engine_type, priority, patterns):
        self.engine_type = engine_type
        self.priority = priority
        self.patterns = patterns

def create_mock_engine_registry():
    """現在のV2のエンジン登録を模擬"""
    registry = {}
    
    # V2のエンジン構成（優先度付き）
    engine_configs = [
        (EngineType.BASIC_FIVE_PATTERN, 0, ["the", "a", "an"]),  # 常に適用可能
        (EngineType.MODAL, 1, ["can", "could", "will", "would", "must", "should", "may", "might"]),
        (EngineType.CONJUNCTION, 2, ["because", "although", "while", "since", "if"]),
        (EngineType.RELATIVE, 3, ["who", "which", "that", "where", "when"]),
        (EngineType.PASSIVE, 4, ["was", "were", "been", "being", "by"]),
        (EngineType.PROGRESSIVE, 5, ["am", "is", "are", "was", "were", "-ing", "being"]),
        (EngineType.PREPOSITIONAL, 6, ["in", "on", "at", "by", "with", "for", "during"]),
        (EngineType.PERFECT_PROGRESSIVE, 7, ["has been", "had been", "will have been"]),
        (EngineType.SUBJUNCTIVE, 8, ["if", "were", "wish", "unless"]),
        (EngineType.INVERSION, 9, ["never", "rarely", "seldom", "hardly", "not only"]),
        (EngineType.COMPARATIVE, 10, ["more", "most", "than", "-er", "-est"]),
        (EngineType.GERUND, 11, ["-ing", "swimming", "reading", "working"]),
        (EngineType.PARTICIPLE, 12, ["-ing", "-ed", "running", "broken"]),
        (EngineType.INFINITIVE, 13, ["to", "to be", "to have", "to do"]),
        (EngineType.QUESTION, 14, ["what", "where", "when", "who", "how", "why", "do", "does", "did"]),
    ]
    
    for engine_type, priority, patterns in engine_configs:
        registry[engine_type] = MockEngineInfo(engine_type, priority, patterns)
    
    return registry

def test_current_engine_selection():
    """現在のV2のエンジン選択ロジックをテスト"""
    
    print("=" * 80)
    print("🔍 現在の動作確認テスト - Grammar Master Controller V2")
    print("=" * 80)
    
    engine_registry = create_mock_engine_registry()
    
    # 元のV2の_get_applicable_engines_fastを模擬
    def get_applicable_engines_original_v2(sentence: str) -> List[EngineType]:
        """元のV2の実装を模擬（Basic Five常に含む）"""
        applicable = []
        sentence_lower = sentence.lower()
        
        # Basic Five Pattern Engine is always applicable (fundamental structure)
        if EngineType.BASIC_FIVE_PATTERN in engine_registry:
            applicable.append(EngineType.BASIC_FIVE_PATTERN)
        
        for engine_type, engine_info in engine_registry.items():
            # Skip basic_five (already added)
            if engine_type == EngineType.BASIC_FIVE_PATTERN:
                continue
                
            # Pattern-based detection
            for pattern in engine_info.patterns:
                if pattern.lower() in sentence_lower:
                    applicable.append(engine_type)
                    break
        
        # Sort by priority (lower number = higher priority)
        applicable.sort(key=lambda x: engine_registry[x].priority)
        
        return applicable
    
    # 元のV2の_select_optimal_engineを模擬
    def select_optimal_engine_original_v2(sentence: str, applicable_engines: List[EngineType]) -> EngineType:
        """元のV2の高度ヒューリスティック選択を模擬"""
        if len(applicable_engines) == 1:
            return applicable_engines[0]
        
        sentence_lower = sentence.lower()
        
        # Priority 1: Conjunction patterns
        if EngineType.CONJUNCTION in applicable_engines:
            conjunction_indicators = ["because", "although", "while", "since", "even though"]
            if any(indicator in sentence_lower for indicator in conjunction_indicators):
                return EngineType.CONJUNCTION
        
        # Priority 2: Conditional patterns  
        if EngineType.SUBJUNCTIVE in applicable_engines:
            conditional_indicators = ["if", "were", "would", "could", "might", "wish"]
            conditional_count = sum(1 for indicator in conditional_indicators if indicator in sentence_lower)
            if conditional_count >= 2:
                return EngineType.SUBJUNCTIVE
        
        # Priority 3: Passive voice
        if EngineType.PASSIVE in applicable_engines:
            if "by" in sentence_lower and any(aux in sentence_lower for aux in ["was", "were", "been"]):
                return EngineType.PASSIVE
        
        # Priority 4: Inversion
        if EngineType.INVERSION in applicable_engines:
            inversion_starters = ["never", "rarely", "seldom", "hardly", "not only"]
            for starter in inversion_starters:
                if sentence_lower.startswith(starter):
                    return EngineType.INVERSION
        
        # Default: Use priority order (first in list has highest priority)
        return applicable_engines[0]
    
    # テストケース
    test_sentences = [
        # 関係詞を含む複文
        "The book that I bought yesterday is expensive.",
        "The man who helped me was very kind.",
        
        # 接続詞を含む複文
        "I stayed home because it was raining.",
        "Although he studied hard, he failed the exam.",
        
        # 受動態
        "The report was written by Mary.",
        "The project was completed by the team.",
        
        # 複雑な複文（関係詞+受動態）
        "The book that was written by Shakespeare is famous.",
        
        # 法動詞
        "She can speak three languages fluently.",
        
        # シンプルな文
        "The cat sits on the mat."
    ]
    
    print("📋 各文に対するエンジン選択テスト:")
    print()
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"{i}. 📝 テスト文: '{sentence}'")
        
        # エンジン検出
        applicable = get_applicable_engines_original_v2(sentence)
        print(f"   🔍 検出エンジン: {[e.value for e in applicable]}")
        
        # 最適エンジン選択
        selected = select_optimal_engine_original_v2(sentence, applicable)
        print(f"   ⚡ 選択エンジン: {selected.value}")
        
        # 分析
        if "that" in sentence.lower() or "who" in sentence.lower():
            expected = "関係詞エンジン期待"
            actual = "✅ 正常" if selected == EngineType.RELATIVE else "❌ Basic Five選択"
            print(f"   📊 関係詞文の処理: {actual}")
        
        if "because" in sentence.lower() or "although" in sentence.lower():
            expected = "接続詞エンジン期待"  
            actual = "✅ 正常" if selected == EngineType.CONJUNCTION else "❌ Basic Five選択"
            print(f"   📊 接続詞文の処理: {actual}")
            
        if "by" in sentence.lower() and any(aux in sentence.lower() for aux in ["was", "were"]):
            expected = "受動態エンジン期待"
            actual = "✅ 正常" if selected == EngineType.PASSIVE else "❌ Basic Five選択"
            print(f"   📊 受動態文の処理: {actual}")
        
        print()
    
    print("=" * 80)
    print("📈 分析結果:")
    print("現在のV2システムでは、専門エンジンが適切に選択されているかどうか確認できました")
    print("Basic Five Pattern Engine (priority 0) が常に最優先になる問題があるかを検証")
    print("=" * 80)

if __name__ == "__main__":
    test_current_engine_selection()
