#!/usr/bin/env python3
"""
Phase 3: spaCy境界精密化エンジン
Step18の境界検出技術を選択移植してPhase 2結果を精密化

設計原則:
1. Phase 2結果を基盤として境界のみを精密化
2. Step18から実証済みの境界検出技術を選択移植
3. v3+Phase2のアーキテクチャを破壊しない統合
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hierarchical_clause_engine import HierarchicalClauseEngine
import spacy
from typing import Dict, List, Optional, Any, Tuple

class SpacyBoundaryRefiner:
    """spaCy境界精密化エンジン（Phase 3）"""
    
    def __init__(self):
        """境界調整エンジン初期化"""
        print("🎯 Phase 3: spaCy境界精密化エンジン初期化中...")
        
        try:
            self.spacy_nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy準備完了")
        except Exception as e:
            print(f"❌ spaCy初期化エラー: {e}")
            raise
        
        # Step18から移植する境界拡張規則
        self.expand_deps = ['det', 'poss', 'compound', 'amod', 'case']
        self.connector_deps = ['mark']  # 接続詞を含める
        
        print("🏗️ 境界精密化ルール準備完了")
    
    def refine_complex_result(self, text: str, phase2_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2結果の境界精密化（メイン機能）"""
        print(f"\n🎯 Phase 3: 境界精密化開始 '{text}'")
        
        # spaCy解析
        spacy_doc = self.spacy_nlp(text)
        
        # Phase 2結果をコピーして精密化
        refined_result = phase2_result.copy()
        
        # 主節の境界精密化
        if 'main_clause' in refined_result and refined_result['main_clause']:
            refined_result['main_clause'] = self._refine_clause_boundaries(
                refined_result['main_clause'], spacy_doc, "main"
            )
        
        # 従属節の境界精密化
        if 'subordinate_clauses' in refined_result:
            refined_subordinate = []
            for i, sub_clause in enumerate(refined_result['subordinate_clauses']):
                refined_sub = self._refine_clause_boundaries(sub_clause, spacy_doc, f"sub_{i}")
                refined_subordinate.append(refined_sub)
            refined_result['subordinate_clauses'] = refined_subordinate
        
        return refined_result
    
    def _refine_clause_boundaries(self, clause_result: Dict[str, Any], spacy_doc, clause_type: str) -> Dict[str, Any]:
        """個別clause内のスロット境界精密化"""
        print(f"\n📋 {clause_type}節の境界精密化:")
        
        refined_clause = clause_result.copy()
        
        if 'slots' not in clause_result or not clause_result['slots']:
            print("  ⚠️ スロット情報なし - スキップ")
            return refined_clause
        
        # 各スロットの境界精密化
        refined_slots = {}
        for slot_name, slot_data in clause_result['slots'].items():
            if isinstance(slot_data, dict) and 'main' in slot_data:
                slot_text = slot_data['main']
                refined_text = self._refine_slot_boundary(slot_text, slot_name, spacy_doc)
                refined_slots[slot_name] = {'main': refined_text}
                
                if refined_text != slot_text:
                    print(f"  🔧 {slot_name}: '{slot_text}' → '{refined_text}'")
                else:
                    print(f"  ✅ {slot_name}: '{slot_text}' (変更なし)")
            else:
                refined_slots[slot_name] = slot_data
        
        refined_clause['slots'] = refined_slots
        return refined_clause
    
    def _refine_slot_boundary(self, slot_text: str, slot_name: str, spacy_doc) -> str:
        """個別スロットの境界精密化"""
        
        # スロットテキストに対応するspaCyトークンを特定
        target_tokens = self._find_matching_tokens(slot_text, spacy_doc)
        if not target_tokens:
            print(f"    ⚠️ '{slot_text}' のトークンが見つからない")
            return slot_text
        
        # Step18の境界拡張技術を適用
        expanded_tokens = self._expand_token_span(target_tokens, spacy_doc, slot_name)
        
        # 連続トークン範囲でテキスト再構成
        if expanded_tokens:
            start_i = min(token.i for token in expanded_tokens)
            end_i = max(token.i for token in expanded_tokens)
            refined_text = " ".join([spacy_doc[i].text for i in range(start_i, end_i + 1)])
            return refined_text
        
        return slot_text
    
    def _find_matching_tokens(self, slot_text: str, spacy_doc) -> List[Any]:
        """スロットテキストに対応するspaCyトークンを特定"""
        slot_words = slot_text.lower().split()
        if not slot_words:
            return []
        
        # 最初の単語を探す
        matching_tokens = []
        for token in spacy_doc:
            if token.text.lower() == slot_words[0]:
                # 連続する単語が一致するかチェック
                consecutive_match = True
                token_sequence = []
                
                for i, word in enumerate(slot_words):
                    if token.i + i < len(spacy_doc):
                        current_token = spacy_doc[token.i + i]
                        if current_token.text.lower() == word:
                            token_sequence.append(current_token)
                        else:
                            consecutive_match = False
                            break
                    else:
                        consecutive_match = False
                        break
                
                if consecutive_match and len(token_sequence) == len(slot_words):
                    matching_tokens = token_sequence
                    break
        
        return matching_tokens
    
    def _expand_token_span(self, target_tokens: List[Any], spacy_doc, slot_name: str) -> List[Any]:
        """Step18境界拡張技術の選択適用"""
        
        if not target_tokens:
            return target_tokens
        
        expanded_tokens = set(target_tokens)
        
        # 各ターゲットトークンから境界拡張
        for token in target_tokens:
            # Step18の基本拡張規則
            for child in token.children:
                if child.dep_ in self.expand_deps:
                    expanded_tokens.add(child)
                    print(f"    🔧 基本拡張: '{child.text}' ({child.dep_})")
            
            # 接続詞の特別処理（Phase 2で消失した「though」等を回復）
            for child in token.children:
                if child.dep_ in self.connector_deps:
                    expanded_tokens.add(child)
                    print(f"    🔧 接続詞回復: '{child.text}' ({child.dep_})")
            
            # 前置詞句の完全処理
            if token.pos_ == 'NOUN':
                for child in token.children:
                    if child.dep_ == 'case':  # 前置詞
                        expanded_tokens.add(child)
                        print(f"    🔧 前置詞追加: '{child.text}'")
        
        return list(expanded_tokens)

class CompleteBoundaryEngine(HierarchicalClauseEngine):
    """Phase 2 + Phase 3統合エンジン"""
    
    def __init__(self):
        super().__init__()
        self.boundary_refiner = SpacyBoundaryRefiner()
    
    def analyze_with_refined_boundaries(self, text: str) -> Dict[str, Any]:
        """境界精密化付き完全分析"""
        print(f"\n🎯 Phase2+3統合分析: '{text}'")
        
        # Phase 2: 階層的clause分解
        phase2_result = super().analyze_complex_sentence(text)
        
        # Phase 3: 境界精密化
        refined_result = self.boundary_refiner.refine_complex_result(text, phase2_result)
        
        return refined_result

def test_boundary_refinement():
    """Phase 3境界精密化テスト"""
    print("🎯 Phase 3: spaCy境界精密化エンジン テスト開始\n")
    
    try:
        engine = CompleteBoundaryEngine()
        print("✅ Phase 2+3統合エンジン初期化完了\n")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return
    
    # Phase 2で問題が見つかった文を重点テスト
    test_sentences = [
        "He succeeded even though he was under intense pressure.",
        "She passed the test because she is very intelligent.",
        "The man who is tall walks quickly.",
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"テスト文: {sentence}")
        print('='*80)
        
        result = engine.analyze_with_refined_boundaries(sentence)
        
        print(f"\n📊 Phase3 境界精密化結果:")
        print(f"📋 文型: {result.get('sentence_type', 'unknown')}")
        print(f"📋 節数: {result.get('total_clauses', 0)}")
        
        # 主節結果
        main_clause = result.get('main_clause', {})
        print(f"\n🏛️ 主節（境界精密化後）:")
        print(f"  テキスト: '{main_clause.get('text', 'N/A')}'")
        print(f"  スロット:")
        for slot_name, slot_data in main_clause.get('slots', {}).items():
            if isinstance(slot_data, dict) and 'main' in slot_data:
                print(f"    {slot_name}: '{slot_data['main']}'")
        
        # 従属節結果
        for i, sub_clause in enumerate(result.get('subordinate_clauses', [])):
            print(f"\n🔗 従属節 {i+1}（境界精密化後）:")
            print(f"  接続: '{sub_clause.get('connector', '')}' ({sub_clause.get('relation', 'N/A')})")
            print(f"  テキスト: '{sub_clause.get('text', 'N/A')}'")
            print(f"  スロット:")
            for slot_name, slot_data in sub_clause.get('slots', {}).items():
                if isinstance(slot_data, dict) and 'main' in slot_data:
                    print(f"    {slot_name}: '{slot_data['main']}'")

if __name__ == "__main__":
    test_boundary_refinement()
