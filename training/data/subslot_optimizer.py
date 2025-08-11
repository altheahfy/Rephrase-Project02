#!/usr/bin/env python3
"""
Phase 5: 品質最適化 - サブスロット重複問題分析・解決
設計仕様書v3.0 Phase 5.1.1 サブスロット重複解消

目標:
1. 現在のサブスロット重複パターンの詳細分析
2. 重複解消ロジックの設計・実装
3. サブスロットコア抽出の精密化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from complete_sentence_engine import CompleteSentenceEngine
from typing import Dict, List, Any
import json

class SubslotOptimizer:
    """サブスロット最適化エンジン（Phase 5）"""
    
    def __init__(self):
        """サブスロット最適化初期化"""
        print("🔧 Phase 5: サブスロット最適化エンジン初期化中...")
        self.base_engine = CompleteSentenceEngine()
        
        # 重複パターン分析用設定
        self.redundancy_patterns = {
            'identical_content': [],  # 完全同一コンテンツ
            'partial_overlap': [],    # 部分重複  
            'core_vs_full': []       # コア vs フル重複
        }
        
        print("✅ サブスロット最適化エンジン準備完了")
    
    def analyze_subslot_redundancy(self, text: str) -> Dict[str, Any]:
        """サブスロット重複パターン詳細分析（Phase 5メイン機能）"""
        print(f"\n🔍 Phase 5: サブスロット重複分析開始 '{text}'")
        
        # 現在のシステム結果取得
        current_result = self.base_engine.analyze_complete_90_slots(text)
        
        # 重複分析実行
        redundancy_report = self._detect_redundancy_patterns(current_result)
        
        # 最適化提案生成
        optimization_suggestions = self._generate_optimization_suggestions(current_result, redundancy_report)
        
        # 統合レポート
        analysis_report = {
            'original_result': current_result,
            'redundancy_analysis': redundancy_report,
            'optimization_suggestions': optimization_suggestions,
            'improvement_potential': self._calculate_improvement_potential(redundancy_report)
        }
        
        return analysis_report
    
    def _detect_redundancy_patterns(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """重複パターン検出"""
        print("\n📊 重複パターン検出中...")
        
        redundancy_report = {
            'total_redundancies': 0,
            'redundancy_by_clause': {},
            'redundancy_types': {
                'identical_content': [],
                'partial_overlap': [],
                'core_vs_full': []
            }
        }
        
        # 主節の重複分析
        if 'main_clause' in result and 'slots' in result['main_clause']:
            main_redundancies = self._analyze_clause_redundancy(
                result['main_clause']['slots'], 'main_clause'
            )
            redundancy_report['redundancy_by_clause']['main_clause'] = main_redundancies
        
        # 従属節の重複分析
        if 'subordinate_clauses' in result:
            for i, sub_clause in enumerate(result['subordinate_clauses']):
                if 'slots' in sub_clause:
                    sub_redundancies = self._analyze_clause_redundancy(
                        sub_clause['slots'], f'subordinate_clause_{i}'
                    )
                    redundancy_report['redundancy_by_clause'][f'subordinate_clause_{i}'] = sub_redundancies
        
        # 全体統計計算
        total_redundancies = 0
        for clause_redundancies in redundancy_report['redundancy_by_clause'].values():
            total_redundancies += len(clause_redundancies.get('identical_content', []))
            total_redundancies += len(clause_redundancies.get('partial_overlap', []))
            total_redundancies += len(clause_redundancies.get('core_vs_full', []))
        
        redundancy_report['total_redundancies'] = total_redundancies
        
        print(f"📋 検出された重複: {total_redundancies}個")
        return redundancy_report
    
    def _analyze_clause_redundancy(self, clause_slots: Dict[str, Any], clause_name: str) -> Dict[str, List]:
        """個別clause内の重複分析"""
        redundancies = {
            'identical_content': [],
            'partial_overlap': [],
            'core_vs_full': []
        }
        
        for slot_name, slot_data in clause_slots.items():
            if isinstance(slot_data, dict) and 'main' in slot_data:
                main_text = slot_data['main']
                
                # mainと各サブスロットの比較
                for sub_name, sub_text in slot_data.items():
                    if sub_name != 'main':
                        redundancy_type = self._classify_redundancy(main_text, sub_text, slot_name, sub_name)
                        if redundancy_type:
                            redundancy_info = {
                                'clause': clause_name,
                                'main_slot': slot_name,
                                'main_text': main_text,
                                'sub_slot': sub_name,
                                'sub_text': sub_text,
                                'redundancy_details': self._analyze_text_overlap(main_text, sub_text)
                            }
                            redundancies[redundancy_type].append(redundancy_info)
                            
                            print(f"  🔍 {redundancy_type}: {slot_name}.{sub_name}")
                            print(f"    Main: '{main_text}'")
                            print(f"    Sub:  '{sub_text}'")
        
        return redundancies
    
    def _classify_redundancy(self, main_text: str, sub_text: str, slot_name: str, sub_name: str) -> str:
        """重複タイプ分類"""
        main_clean = main_text.strip().lower()
        sub_clean = sub_text.strip().lower()
        
        # 完全同一コンテンツ
        if main_clean == sub_clean:
            return 'identical_content'
        
        # 部分重複（一方が他方を完全含有）
        if sub_clean in main_clean or main_clean in sub_clean:
            return 'partial_overlap'
        
        # コア vs フル（設計上想定される重複）
        if sub_name == 'sub-S' and slot_name == 'S':
            # 主語の場合、mainが修飾付き、sub-Sがコア部分であることが期待される
            if len(sub_clean.split()) < len(main_clean.split()):
                return 'core_vs_full'
        
        return None  # 重複なし
    
    def _analyze_text_overlap(self, main_text: str, sub_text: str) -> Dict[str, Any]:
        """テキスト重複詳細分析"""
        main_words = set(main_text.lower().split())
        sub_words = set(sub_text.lower().split())
        
        overlap_words = main_words & sub_words
        overlap_ratio = len(overlap_words) / max(len(main_words), len(sub_words)) if main_words or sub_words else 0
        
        return {
            'main_word_count': len(main_words),
            'sub_word_count': len(sub_words),
            'overlap_words': list(overlap_words),
            'overlap_ratio': overlap_ratio,
            'unique_to_main': list(main_words - sub_words),
            'unique_to_sub': list(sub_words - main_words)
        }
    
    def _generate_optimization_suggestions(self, result: Dict[str, Any], redundancy_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """最適化提案生成"""
        print("\n💡 最適化提案生成中...")
        
        suggestions = []
        
        for clause_name, clause_redundancies in redundancy_report['redundancy_by_clause'].items():
            # identical_content対応提案
            for redundancy in clause_redundancies.get('identical_content', []):
                suggestion = {
                    'type': 'remove_identical_subslot',
                    'priority': 'high',
                    'clause': clause_name,
                    'target_slot': redundancy['main_slot'],
                    'target_subslot': redundancy['sub_slot'],
                    'reason': 'Identical content provides no additional value',
                    'action': f'Remove {redundancy["sub_slot"]} as it duplicates main content'
                }
                suggestions.append(suggestion)
            
            # core_vs_full対応提案
            for redundancy in clause_redundancies.get('core_vs_full', []):
                if redundancy['redundancy_details']['overlap_ratio'] > 0.8:
                    suggestion = {
                        'type': 'extract_true_core',
                        'priority': 'medium',
                        'clause': clause_name,
                        'target_slot': redundancy['main_slot'],
                        'target_subslot': redundancy['sub_slot'],
                        'reason': 'Sub-slot should contain core component only',
                        'action': 'Extract grammatical core without modifiers',
                        'suggested_core': self._suggest_core_extraction(redundancy)
                    }
                    suggestions.append(suggestion)
        
        print(f"💡 生成された提案: {len(suggestions)}個")
        return suggestions
    
    def _suggest_core_extraction(self, redundancy: Dict[str, Any]) -> str:
        """コア抽出提案"""
        main_text = redundancy['main_text']
        overlap_details = redundancy['redundancy_details']
        
        # 単純heuristic：最短の重複部分を抽出
        overlap_words = overlap_details['overlap_words']
        if overlap_words:
            # 最も短い重複単語をコアとして提案
            core_candidate = min(overlap_words, key=len)
            return core_candidate
        
        return "Needs manual analysis"
    
    def _calculate_improvement_potential(self, redundancy_report: Dict[str, Any]) -> Dict[str, Any]:
        """改善ポテンシャル計算"""
        total_redundancies = redundancy_report['total_redundancies']
        
        return {
            'total_redundancies': total_redundancies,
            'efficiency_gain_estimate': f"{total_redundancies * 5}% reduction in noise",
            'clarity_improvement': 'High' if total_redundancies > 5 else 'Medium' if total_redundancies > 2 else 'Low',
            'priority_level': 'Critical' if total_redundancies > 10 else 'High' if total_redundancies > 5 else 'Medium'
        }

def test_subslot_redundancy_analysis():
    """サブスロット重複分析テスト（Phase 5開始）"""
    print("🔧 Phase 5: サブスロット重複問題分析 テスト開始\n")
    
    try:
        optimizer = SubslotOptimizer()
        print("✅ サブスロット最適化エンジン初期化完了\n")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return
    
    # テスト文（重複が予想される文）
    test_sentences = [
        # 単文（基本的重複確認）
        "He succeeded.",
        
        # 複文（重複問題が顕著）  
        "The experienced manager completed the project successfully."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"📋 重複分析対象文: {sentence}")
        print('='*80)
        
        analysis_report = optimizer.analyze_subslot_redundancy(sentence)
        
        # 分析結果表示
        redundancy_analysis = analysis_report['redundancy_analysis']
        optimization_suggestions = analysis_report['optimization_suggestions']
        improvement_potential = analysis_report['improvement_potential']
        
        print(f"\n📊 重複分析サマリー:")
        print(f"  総重複数: {redundancy_analysis['total_redundancies']}")
        print(f"  改善ポテンシャル: {improvement_potential['priority_level']}")
        print(f"  効率向上見込み: {improvement_potential['efficiency_gain_estimate']}")
        
        print(f"\n💡 最適化提案 ({len(optimization_suggestions)}個):")
        for i, suggestion in enumerate(optimization_suggestions, 1):
            print(f"  {i}. [{suggestion['priority']}] {suggestion['type']}")
            print(f"     対象: {suggestion['target_slot']}.{suggestion['target_subslot']}")
            print(f"     理由: {suggestion['reason']}")
            print(f"     アクション: {suggestion['action']}")
            if 'suggested_core' in suggestion:
                print(f"     提案コア: '{suggestion['suggested_core']}'")

if __name__ == "__main__":
    test_subslot_redundancy_analysis()
