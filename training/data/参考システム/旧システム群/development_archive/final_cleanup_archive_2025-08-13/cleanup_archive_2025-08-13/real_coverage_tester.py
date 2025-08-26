#!/usr/bin/env python3
"""
Real Coverage Tester
実際のエンジン動作に基づく正確なカバレッジ測定
"""

import os
import sys
from typing import Dict, List, Optional, Tuple

# 現在のディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class RealCoverageTester:
    """実際のエンジン動作テスター"""
    
    def __init__(self):
        self.test_sentences = {
            # 受動態テスト (10%の使用頻度)
            "passive_voice": [
                "The book was written by John.",
                "The house is being built by workers.",
                "The problem has been solved.",
                "The car was repaired yesterday.",
                "This song is loved by many people."
            ],
            
            # 完了時制テスト (8%の使用頻度)
            "perfect_tenses": [
                "I have finished my homework.",
                "She had already left when I arrived.",
                "They will have completed the project by tomorrow.",
                "He has been working here for five years.",
                "We had been waiting for two hours."
            ],
            
            # 関係節テスト (7%の使用頻度)
            "relative_clauses": [
                "The man who lives next door is friendly.",
                "This is the book that I recommended.",
                "The place where we met is special.",
                "The reason why she left is unclear.",
                "The woman whose car was stolen called police."
            ],
            
            # 従属接続詞テスト (3%の使用頻度)
            "subordinate_conjunctions": [
                "Because it was raining, we stayed inside.",
                "Although he studied hard, he failed the test.",
                "When she arrives, we will start the meeting.",
                "If you study hard, you will pass the exam.",
                "Since you're here, let's begin."
            ],
            
            # 比較級・最上級テスト (1%の使用頻度)
            "comparative_superlative": [
                "This book is more interesting than that one.",
                "She is the smartest student in the class.",
                "Today is warmer than yesterday.",
                "This is the best movie I've ever seen.",
                "He runs faster than his brother."
            ],
            
            # 動名詞テスト (1%の使用頻度)
            "gerunds": [
                "Swimming is good exercise.",
                "I enjoy reading books.",
                "Thank you for helping me.",
                "She is good at playing piano.",
                "Stop talking and listen."
            ],
            
            # 不定詞テスト (1%の使用頻度)
            "infinitives": [
                "I want to learn English.",
                "She decided to quit her job.",
                "It's important to be honest.",
                "I have something to tell you.",
                "He came here to see me."
            ]
        }
        
        # エンジンの使用頻度マッピング
        self.usage_frequencies = {
            "passive_voice": 10.0,
            "perfect_tenses": 8.0,
            "relative_clauses": 7.0,
            "subordinate_conjunctions": 3.0,
            "comparative_superlative": 1.0,
            "gerunds": 1.0,
            "infinitives": 1.0
        }

    def test_engine_accuracy(self, engine_name: str) -> Tuple[float, Dict]:
        """指定されたエンジンの実際の精度を測定"""
        print(f"\n🧪 Testing {engine_name.replace('_', ' ').title()} Engine")
        print("-" * 50)
        
        if engine_name not in self.test_sentences:
            return 0.0, {"error": "No test sentences for this engine"}
        
        test_sentences = self.test_sentences[engine_name]
        results = {
            "total_tests": len(test_sentences),
            "successful": 0,
            "failed": 0,
            "errors": [],
            "details": []
        }
        
        try:
            # エンジンをインポート・初期化
            engine = self._import_engine(engine_name)
            if not engine:
                return 0.0, {"error": f"Failed to import {engine_name} engine"}
            
            # 各テスト文を処理
            for i, sentence in enumerate(test_sentences, 1):
                print(f"Test {i}: {sentence}")
                
                try:
                    # エンジンによる処理
                    result = engine.process(sentence)
                    
                    if result and self._validate_result(result, engine_name):
                        print(f"  ✅ Success: {result}")
                        results["successful"] += 1
                        results["details"].append({
                            "sentence": sentence,
                            "status": "success",
                            "result": result
                        })
                    else:
                        print(f"  ❌ Failed: Invalid result")
                        results["failed"] += 1
                        results["errors"].append(f"Invalid result for: {sentence}")
                        results["details"].append({
                            "sentence": sentence,
                            "status": "failed",
                            "result": result
                        })
                        
                except Exception as e:
                    print(f"  💥 Error: {str(e)}")
                    results["failed"] += 1
                    results["errors"].append(f"Error processing '{sentence}': {str(e)}")
                    results["details"].append({
                        "sentence": sentence,
                        "status": "error",
                        "error": str(e)
                    })
            
            # 精度計算
            accuracy = (results["successful"] / results["total_tests"]) * 100
            print(f"\n📊 Results: {results['successful']}/{results['total_tests']} passed")
            print(f"🎯 Accuracy: {accuracy:.1f}%")
            
            return accuracy, results
            
        except Exception as e:
            print(f"💥 Engine test failed: {str(e)}")
            return 0.0, {"error": str(e)}

    def _import_engine(self, engine_name: str):
        """エンジンをインポート"""
        try:
            if engine_name == "passive_voice":
                from engines.passive_voice_engine import PassiveVoiceEngine
                return PassiveVoiceEngine()
            elif engine_name == "perfect_tenses":
                from engines.perfect_progressive_engine import PerfectProgressiveEngine
                return PerfectProgressiveEngine()
            elif engine_name == "relative_clauses":
                from engines.relative_clause_engine import RelativeClauseEngine
                return RelativeClauseEngine()
            elif engine_name == "subordinate_conjunctions":
                from engines.conjunction_engine import ConjunctionEngine
                return ConjunctionEngine()
            elif engine_name == "comparative_superlative":
                from engines.comparative_engine import ComparativeEngine
                return ComparativeEngine()
            elif engine_name == "gerunds":
                from engines.gerund_engine import GerundEngine
                return GerundEngine()
            elif engine_name == "infinitives":
                from engines.infinitive_engine import InfinitiveEngine
                return InfinitiveEngine()
            else:
                return None
        except ImportError as e:
            print(f"⚠️ Cannot import {engine_name}: {str(e)}")
            return None

    def _validate_result(self, result: Dict, engine_name: str) -> bool:
        """結果の妥当性を検証"""
        if not result:
            return False
        
        # 基本的な構造チェック
        if not isinstance(result, dict):
            return False
            
        # エンジン固有の検証
        if engine_name == "passive_voice":
            # 受動態なら'Aux'スロットがあるべき
            return 'V' in result and ('Aux' in result or 'aux' in result)
        elif engine_name == "perfect_tenses":
            # 完了時制なら助動詞があるべき
            return 'V' in result and ('Aux' in result or 'aux' in result)
        elif engine_name == "relative_clauses":
            # 関係節なら修飾構造があるべき
            return 'S' in result and 'V' in result
        else:
            # 最低限の文構造があるかチェック
            return 'V' in result or 'S' in result

    def run_full_test(self) -> Dict:
        """全エンジンの実測カバレッジを計算"""
        print("🚀 Real Coverage Testing - Based on Actual Engine Performance")
        print("=" * 70)
        
        total_effective_coverage = 0.0
        engine_results = {}
        
        for engine_name in self.test_sentences.keys():
            accuracy, details = self.test_engine_accuracy(engine_name)
            usage_freq = self.usage_frequencies[engine_name]
            
            # 実効カバレッジ = 使用頻度 × 実測精度
            effective_coverage = (usage_freq * accuracy) / 100
            total_effective_coverage += effective_coverage
            
            engine_results[engine_name] = {
                "usage_frequency": usage_freq,
                "measured_accuracy": accuracy,
                "effective_coverage": effective_coverage,
                "details": details
            }
            
            print(f"📈 {engine_name}: {usage_freq:.1f}% × {accuracy:.1f}% = {effective_coverage:.2f}% effective")
        
        print(f"\n🎯 TOTAL MEASURED EFFECTIVE COVERAGE: {total_effective_coverage:.1f}%")
        print("=" * 70)
        
        return {
            "total_effective_coverage": total_effective_coverage,
            "engine_results": engine_results
        }

def main():
    """メイン実行"""
    tester = RealCoverageTester()
    results = tester.run_full_test()
    
    print("\n📊 Summary:")
    print(f"Real Coverage (measured): {results['total_effective_coverage']:.1f}%")
    print(f"Estimated Coverage (50% assumption): {sum(tester.usage_frequencies.values()) * 0.5:.1f}%")
    print(f"Difference: {results['total_effective_coverage'] - (sum(tester.usage_frequencies.values()) * 0.5):.1f}%")

if __name__ == "__main__":
    main()
