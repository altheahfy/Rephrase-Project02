#!/usr/bin/env python3
"""
Phase 4: サブスロット完全対応エンジン
Step18のサブスロット構造を統合して90スロット完全対応を実現

設計原則:
1. Phase 1-3の成果を破壊しない統合
2. Step18のdep_to_subslotマッピングを選択移植
3. Rephraseスロット体系（上位10 + サブ80）への完全対応
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spacy_boundary_refiner import CompleteBoundaryEngine
import spacy
from typing import Dict, List, Optional, Any, Tuple

class SubslotStructureProcessor:
    """サブスロット構造処理エンジン（Phase 4）"""
    
    def __init__(self):
        """サブスロット処理エンジン初期化"""
        print("🎯 Phase 4: サブスロット構造処理エンジン初期化中...")
        
        try:
            self.spacy_nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy準備完了")
        except Exception as e:
            print(f"❌ spaCy初期化エラー: {e}")
            raise
        
        # Step18から移植：Stanza依存関係→サブスロットマッピング
        self.dep_to_subslot = {
            # Stanza版への変換
            'nsubj': 'sub-S',
            'nsubj:pass': 'sub-S', 
            'aux': 'sub-Aux',
            'aux:pass': 'sub-Aux',
            'obj': 'sub-O1',
            'iobj': 'sub-O2',
            'cop': 'sub-V',  # be動詞
            'xcomp': 'sub-C2',
            'ccomp': 'sub-C1',
            'advmod': 'sub-M2',
            'amod': 'sub-M3',
            'case': 'sub-M1',  # 前置詞
            'mark': 'sub-M1',  # 従属接続詞
            'acl:relcl': 'sub-M3',  # 関係詞節
            'det': 'sub-M1',  # 限定詞
        }
        
        # Rephraseスロット体系：各メインスロットが持つサブスロット種類
        self.main_slot_subslots = {
            'M1': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            'S': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'], 
            'O1': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            'O2': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            'C1': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            'C2': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            'M2': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            'M3': ['sub-M1', 'sub-S', 'sub-Aux', 'sub-M2', 'sub-V', 'sub-C1', 'sub-O1', 'sub-O2', 'sub-C2', 'sub-M3'],
            # AuxとVはサブスロットなし（設計仕様書に従い）
        }
        
        print("🏗️ サブスロット構造ルール準備完了（90スロット対応）")
    
    def process_complete_subslots(self, text: str, phase3_result: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3結果にサブスロット処理を統合（メイン機能）"""
        print(f"\n🎯 Phase 4: サブスロット完全処理開始 '{text}'")
        
        # spaCy解析
        spacy_doc = self.spacy_nlp(text)
        
        # Phase 3結果をコピーして拡張
        complete_result = phase3_result.copy()
        
        # 主節のサブスロット処理
        if 'main_clause' in complete_result and complete_result['main_clause']:
            complete_result['main_clause'] = self._process_clause_subslots(
                complete_result['main_clause'], spacy_doc, "main"
            )
        
        # 従属節のサブスロット処理
        if 'subordinate_clauses' in complete_result:
            complete_subordinate = []
            for i, sub_clause in enumerate(complete_result['subordinate_clauses']):
                complete_sub = self._process_clause_subslots(sub_clause, spacy_doc, f"sub_{i}")
                complete_subordinate.append(complete_sub)
            complete_result['subordinate_clauses'] = complete_subordinate
        
        # 統計情報の追加
        total_slots = self._count_total_slots(complete_result)
        complete_result['total_slots'] = total_slots
        
        print(f"\n📊 最終スロット統計: {total_slots}スロット（目標90スロット）")
        
        return complete_result
    
    def _process_clause_subslots(self, clause_result: Dict[str, Any], spacy_doc, clause_type: str) -> Dict[str, Any]:
        """個別clause内のサブスロット処理"""
        print(f"\n📋 {clause_type}節のサブスロット処理:")
        
        complete_clause = clause_result.copy()
        
        if 'slots' not in clause_result or not clause_result['slots']:
            print("  ⚠️ スロット情報なし - スキップ")
            return complete_clause
        
        # 各メインスロットのサブスロット分解
        complete_slots = {}
        for slot_name, slot_data in clause_result['slots'].items():
            if isinstance(slot_data, dict) and 'main' in slot_data:
                slot_text = slot_data['main']
                
                # Aux, Vはサブスロットなし（設計仕様書準拠）
                if slot_name in ['Aux', 'V']:
                    complete_slots[slot_name] = {'main': slot_text}
                    print(f"  ✅ {slot_name}: サブスロットなし（設計仕様）")
                    continue
                
                # サブスロット分解実行
                subslots = self._extract_subslots_for_main_slot(slot_text, slot_name, spacy_doc)
                complete_slots[slot_name] = {
                    'main': slot_text,
                    **subslots  # サブスロットを統合
                }
                
                print(f"  📊 {slot_name}: {len(subslots)}個のサブスロット")
                for sub_name, sub_text in subslots.items():
                    print(f"    {sub_name}: '{sub_text}'")
            else:
                complete_slots[slot_name] = slot_data
        
        complete_clause['slots'] = complete_slots
        return complete_clause
    
    def _extract_subslots_for_main_slot(self, slot_text: str, main_slot_name: str, spacy_doc) -> Dict[str, str]:
        """メインスロット内のサブスロット抽出"""
        
        # Step18の技術：スロットテキストに対応するspaCyトークンを特定
        target_tokens = self._find_matching_tokens(slot_text, spacy_doc)
        if not target_tokens:
            print(f"    ⚠️ '{slot_text}' のトークンが見つからない")
            return {}
        
        subslots = {}
        
        # 各トークンを依存関係に基づいてサブスロットに分類
        for token in target_tokens:
            # 依存関係からサブスロット種類を特定
            if token.dep_ in self.dep_to_subslot:
                subslot_type = self.dep_to_subslot[token.dep_]
                
                # このメインスロットが該当サブスロットを持つかチェック
                if (main_slot_name in self.main_slot_subslots and 
                    subslot_type in self.main_slot_subslots[main_slot_name]):
                    
                    # Step18技術：境界拡張してサブスロットテキスト抽出
                    expanded_text = self._expand_subslot_span(token, spacy_doc)
                    
                    # 既存のサブスロットと結合（複数トークンの場合）
                    if subslot_type in subslots:
                        subslots[subslot_type] = f"{subslots[subslot_type]} {expanded_text}"
                    else:
                        subslots[subslot_type] = expanded_text
                    
                    print(f"    🔧 {token.dep_} → {subslot_type}: '{expanded_text}'")
        
        return subslots
    
    def _find_matching_tokens(self, slot_text: str, spacy_doc) -> List[Any]:
        """スロットテキストに対応するspaCyトークンを特定（Phase 3から移植）"""
        slot_words = slot_text.lower().split()
        if not slot_words:
            return []
        
        # 最初の単語を探す
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
                    return token_sequence
        
        return []
    
    def _expand_subslot_span(self, token, spacy_doc) -> str:
        """Step18技術移植：サブスロット境界拡張"""
        expand_deps = ['det', 'compound', 'amod']
        
        expanded_tokens = {token}
        
        # 基本拡張
        for child in token.children:
            if child.dep_ in expand_deps:
                expanded_tokens.add(child)
        
        # 連続範囲でテキスト構成
        if expanded_tokens:
            start_i = min(t.i for t in expanded_tokens)
            end_i = max(t.i for t in expanded_tokens)
            return " ".join([spacy_doc[i].text for i in range(start_i, end_i + 1)])
        
        return token.text
    
    def _count_total_slots(self, result: Dict[str, Any]) -> int:
        """総スロット数カウント"""
        total = 0
        
        # 主節のスロット
        if 'main_clause' in result and 'slots' in result['main_clause']:
            for slot_data in result['main_clause']['slots'].values():
                if isinstance(slot_data, dict):
                    total += len(slot_data)  # main + サブスロット
        
        # 従属節のスロット
        if 'subordinate_clauses' in result:
            for sub_clause in result['subordinate_clauses']:
                if 'slots' in sub_clause:
                    for slot_data in sub_clause['slots'].values():
                        if isinstance(slot_data, dict):
                            total += len(slot_data)  # main + サブスロット
        
        return total

class CompleteSentenceEngine(CompleteBoundaryEngine):
    """Phase 1-4統合：完全90スロット対応エンジン"""
    
    def __init__(self):
        super().__init__()
        self.subslot_processor = SubslotStructureProcessor()
    
    def analyze_complete_90_slots(self, text: str) -> Dict[str, Any]:
        """90スロット完全対応分析（最終版）"""
        print(f"\n🎯 完全90スロットエンジン分析: '{text}'")
        
        # Phase 1-3: 境界精密化付き階層分解
        phase3_result = super().analyze_with_refined_boundaries(text)
        
        # Phase 4: サブスロット完全処理
        complete_result = self.subslot_processor.process_complete_subslots(text, phase3_result)
        
        return complete_result

def test_complete_90_slot_system():
    """90スロット完全対応システムテスト"""
    print("🎯 Phase 1-4統合: 90スロット完全対応システム テスト開始\n")
    
    try:
        engine = CompleteSentenceEngine()
        print("✅ 完全90スロットエンジン初期化完了\n")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return
    
    # 段階的テスト
    test_sentences = [
        # 単文（Phase 1基盤確認）
        "He succeeded.",
        
        # 複文（Phase 2-4統合確認）  
        "He succeeded even though he was under intense pressure.",
        
        # 複雑文（90スロット完全対応確認）
        "The experienced manager who had recently taken charge completed the project successfully."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"テスト文: {sentence}")
        print('='*80)
        
        result = engine.analyze_complete_90_slots(sentence)
        
        print(f"\n📊 90スロット完全分析結果:")
        print(f"📋 文型: {result.get('sentence_type', 'unknown')}")
        print(f"📋 節数: {result.get('total_clauses', 0)}")
        print(f"📊 総スロット数: {result.get('total_slots', 0)}/90")
        
        # 詳細スロット表示
        print(f"\n🏛️ 主節スロット詳細:")
        main_clause = result.get('main_clause', {})
        for slot_name, slot_data in main_clause.get('slots', {}).items():
            if isinstance(slot_data, dict):
                print(f"  📋 {slot_name}:")
                for sub_name, sub_text in slot_data.items():
                    print(f"    {sub_name}: '{sub_text}'")
        
        # 従属節スロット表示
        for i, sub_clause in enumerate(result.get('subordinate_clauses', [])):
            print(f"\n🔗 従属節 {i+1} スロット詳細:")
            for slot_name, slot_data in sub_clause.get('slots', {}).items():
                if isinstance(slot_data, dict):
                    print(f"  📋 {slot_name}:")
                    for sub_name, sub_text in slot_data.items():
                        print(f"    {sub_name}: '{sub_text}'")

if __name__ == "__main__":
    test_complete_90_slot_system()
