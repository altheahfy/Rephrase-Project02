#!/usr/bin/env python3
"""
Pure Stanza Engine v3.1 - Unified Recursive Engine
Rephraseの統一入れ子構造実装版

統一分解原則:
1. Aux, V以外の8スロット（M1,S,O1,O2,C1,C2,M2,M3）は再帰構造
2. 各スロットが同じ10スロット構造を内包
3. 統一アルゴリズムで全階層に対応
4. phrase/clause時の上位スロット空化
"""

import stanza
import spacy
import json
from typing import Dict, List, Optional, Tuple, Any

class PureStanzaEngineV31:
    """
    Pure Stanza Engine v3.1 - Unified Recursive Engine
    
    Rephraseの統一入れ子構造実装:
    - 8つの再帰可能スロット: M1,S,O1,O2,C1,C2,M2,M3
    - 2つの語彙専用スロット: Aux,V
    - 統一分解アルゴリズムによる無限階層対応
    """
    
    def __init__(self):
        """統一再帰分解エンジン初期化"""
        print("🚀 統一再帰分解エンジン v3.1 初期化中...")
        
        # Stanza NLP パイプライン
        self.nlp = stanza.Pipeline('en', verbose=False)
        print("✅ Stanza準備完了")
        
        # spaCy（境界調整用）
        self.spacy_nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy準備完了")
        
        # Rephraseの統一スロット構造定義
        self.RECURSIVE_SLOTS = ['M1', 'S', 'O1', 'O2', 'C1', 'C2', 'M2', 'M3']
        self.WORD_ONLY_SLOTS = ['Aux', 'V']
        self.ALL_SLOTS = self.RECURSIVE_SLOTS + self.WORD_ONLY_SLOTS
        
        # 文型パターンルール
        self.sentence_patterns = self._load_sentence_patterns()
        
        # 修飾語マッピングルール
        self.modifier_mappings = self._load_modifier_mappings()
        
        # 入れ子判定ルール
        self.nested_triggers = self._load_nested_triggers()
        
        print("🏗️ 統一再帰分解エンジン準備完了 (v3.1)")
        
    def _load_sentence_patterns(self) -> Dict[str, Any]:
        """統一文型パターンルール"""
        return {
            # 基本5文型
            "SV": {
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"}
            },
            "SVC": {
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SVO": {
                "required_relations": ["nsubj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "root": "V"}
            },
            "SVOO": {
                "required_relations": ["nsubj", "iobj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "iobj": "O1", "obj": "O2", "root": "V"}
            },
            "SVOC": {
                "required_relations": ["nsubj", "obj", "xcomp", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "xcomp": "C2", "root": "V"}
            },
            # 助動詞構文
            "S_AUX_V": {
                "required_relations": ["nsubj", "aux", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "aux": "Aux", "root": "V"}
            },
            # 受動態
            "PASSIVE": {
                "required_relations": ["nsubj:pass", "aux:pass", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj:pass": "S", "aux:pass": "Aux", "root": "V"}
            }
        }
    
    def _load_modifier_mappings(self) -> Dict[str, str]:
        """修飾語スロットマッピング"""
        return {
            "advmod": "M2",     # 副詞修飾語
            "amod": "nested",   # 形容詞修飾語 → サブスロット
            "det": "nested",    # 限定詞 → サブスロット
            "case": "nested",   # 前置詞 → サブスロット
            "nmod": "M1",       # 名詞修飾語
            "mark": "nested",   # 従属節マーカー → サブスロット
        }
    
    def _load_nested_triggers(self) -> Dict[str, str]:
        """入れ子分解トリガー条件"""
        return {
            "phrase": "multi_word",      # 複数語句
            "clause": "has_verb",        # 動詞を含む句
            "complex": "has_modifiers"   # 修飾語を含む句
        }
    
    def decompose_unified(self, text: str, depth: int = 0) -> Dict[str, Any]:
        """
        統一分解アルゴリズム - Rephraseの核心実装
        
        Args:
            text: 分解対象テキスト
            depth: 再帰深度（デバッグ用）
            
        Returns:
            統一10スロット構造 + サブスロット
        """
        print(f"{'  ' * depth}🔍 統一分解開始: '{text[:30]}...' (depth={depth})")
        
        # Stanza構文解析
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # ROOT動詞検出
        root_verb = self._find_root_verb(sent)
        if not root_verb:
            print(f"{'  ' * depth}⚠️ ROOT動詞未検出")
            return {"error": "No root verb found"}
        
        print(f"{'  ' * depth}🎯 ROOT: '{root_verb.text}' ({root_verb.pos})")
        
        # 基本10スロット分解
        basic_slots = self._extract_basic_slots(sent, root_verb, depth)
        
        # 統一入れ子処理：8つの再帰可能スロットで再帰適用
        unified_result = self._apply_unified_nesting(basic_slots, depth)
        
        print(f"{'  ' * depth}📋 統一分解完了: {len([k for k, v in unified_result.items() if k != 'metadata'])}スロット")
        
        return unified_result
    
    def _find_root_verb(self, sent) -> Optional[Any]:
        """ROOT動詞検出（統一アルゴリズム用）"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _extract_basic_slots(self, sent, root_verb, depth: int) -> Dict[str, Any]:
        """基本10スロット抽出（統一ベース処理）"""
        # 全依存関係を収集
        all_relations = {}
        for word in sent.words:
            all_relations[word.deprel] = word
        
        # 文型パターンマッチング
        matched_pattern = self._match_sentence_pattern_enhanced(sent, root_verb)
        
        if not matched_pattern:
            print(f"{'  ' * depth}❌ 文型パターン未検出")
            return {}
        
        print(f"{'  ' * depth}✅ マッチしたパターン: {matched_pattern}")
        
        # スロット抽出
        slots = {}
        
        # 基本スロット抽出
        self._extract_core_slots(sent, root_verb, slots, depth)
        
        # 修飾語処理
        self._process_modifiers(sent, slots, depth)
        
        return slots
    
    def _match_sentence_pattern_enhanced(self, sent, root_verb) -> Optional[str]:
        """強化された文型パターンマッチング"""
        relations = {word.deprel: word for word in sent.words}
        
        # SVO系パターンの詳細判定
        if 'nsubj' in relations and root_verb.pos == 'VERB':
            if 'obj' in relations and 'iobj' in relations:
                return "SVOO"  # 第4文型
            elif 'obj' in relations and 'xcomp' in relations:
                return "SVOC"  # 第5文型 
            elif 'obj' in relations:
                return "SVO"   # 第3文型
            elif 'aux' in relations:
                return "S_AUX_V"  # 助動詞構文
            else:
                return "SV"    # 第1文型
        
        # SVC系パターン
        if 'nsubj' in relations and 'cop' in relations:
            return "SVC"  # 第2文型
        
        # 受動態
        if 'nsubj:pass' in relations and 'aux:pass' in relations:
            return "PASSIVE"
        
        return "SV"  # デフォルト
    
    def _extract_core_slots(self, sent, root_verb, slots: Dict[str, Any], depth: int):
        """コアスロットの抽出"""
        for word in sent.words:
            slot_name = None
            
            # 主語系
            if word.deprel == 'nsubj' or word.deprel == 'nsubj:pass':
                slot_name = 'S'
                # 複合主語の場合の処理
                subject_text = self._extract_compound_phrase(sent, word)
                word_text = subject_text if subject_text != word.text else word.text
            # 目的語系  
            elif word.deprel == 'obj':
                slot_name = 'O1'
                word_text = self._extract_compound_phrase(sent, word)
            elif word.deprel == 'iobj':
                slot_name = 'O1' 
                word_text = word.text
            # 補語系
            elif word.deprel == 'xcomp':
                slot_name = 'C2'
                word_text = word.text
            elif word.deprel == 'root' and word.pos in ['ADJ', 'NOUN']:
                slot_name = 'C1'
                word_text = word.text
            # 動詞系
            elif word.deprel == 'root' and word.pos == 'VERB':
                slot_name = 'V'
                word_text = word.text
            elif word.deprel == 'cop':
                slot_name = 'V'
                word_text = word.text
            elif word.deprel == 'aux' or word.deprel == 'aux:pass':
                slot_name = 'Aux'
                word_text = word.text
            else:
                continue
            
            if slot_name:
                slots[slot_name] = {
                    "content": word_text,
                    "pos": word.pos,
                    "deprel": word.deprel,
                    "word_obj": word
                }
                print(f"{'  ' * depth}📍 {slot_name}: '{word_text}' (deprel: {word.deprel})")
    
    def _extract_compound_phrase(self, sent, head_word) -> str:
        """複合句の抽出（限定詞・形容詞などを含む）"""
        phrase_words = [head_word]
        
        # 依存語を収集
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['det', 'amod', 'compound', 'case']:
                phrase_words.append(word)
        
        # 位置順にソート
        phrase_words.sort(key=lambda w: w.id)
        
        return ' '.join(word.text for word in phrase_words)
    
    def _match_sentence_pattern(self, relations: List[str], root_pos: str) -> Optional[str]:
        """文型パターンマッチング"""
        for pattern_name, pattern_info in self.sentence_patterns.items():
            required = set(pattern_info["required_relations"])
            available = set(relations)
            
            if required.issubset(available) and root_pos in pattern_info["root_pos"]:
                return pattern_name
        
        return None
    
    def _process_modifiers(self, sent, slots: Dict[str, Any], depth: int):
        """修飾語処理（統一アルゴリズム）"""
        for word in sent.words:
            if word.deprel in self.modifier_mappings:
                slot_mapping = self.modifier_mappings[word.deprel]
                
                if slot_mapping == "nested":
                    # サブスロット候補として記録
                    if "modifiers" not in slots:
                        slots["modifiers"] = []
                    slots["modifiers"].append({
                        "word": word.text,
                        "deprel": word.deprel,
                        "head_id": word.head
                    })
                elif slot_mapping in self.ALL_SLOTS:
                    # 直接スロットマッピング
                    slots[slot_mapping] = {
                        "content": word.text,
                        "pos": word.pos,
                        "deprel": word.deprel
                    }
                    print(f"{'  ' * depth}📍 {slot_mapping}: '{word.text}' (修飾語: {word.deprel})")
    
    def _apply_unified_nesting(self, basic_slots: Dict[str, Any], depth: int) -> Dict[str, Any]:
        """
        統一入れ子処理 - Rephraseの核心実装
        8つの再帰可能スロットに統一アルゴリズムを適用
        """
        result = {}
        
        for slot_name in self.ALL_SLOTS:
            if slot_name in basic_slots:
                slot_data = basic_slots[slot_name]
                
                if slot_name in self.RECURSIVE_SLOTS:
                    # 再帰可能スロット：入れ子判定して再帰適用
                    result[slot_name] = self._process_recursive_slot(slot_data, slot_name, depth)
                else:
                    # 語彙専用スロット：そのまま保持
                    result[slot_name] = {slot_name.lower(): slot_data["content"]}
        
        return result
    
    def _process_recursive_slot(self, slot_data: Dict[str, Any], slot_name: str, depth: int) -> Dict[str, Any]:
        """
        再帰可能スロット処理
        入れ子条件を満たす場合は統一アルゴリズムを再帰適用
        """
        content = slot_data["content"]
        
        # 入れ子判定
        if self._needs_nesting(content, slot_data):
            print(f"{'  ' * depth}📍 {slot_name}スロット: '{content}' → 統一再帰分解")
            
            # 統一アルゴリズムを再帰適用
            subslot_result = self.decompose_unified(content, depth + 1)
            
            if "error" not in subslot_result:
                # 上位スロット空化（Rephraseルール）
                return {
                    "content": "",  # 上位を空化
                    "subslots": subslot_result  # 統一分解結果を格納
                }
        
        # 単語レベル：そのまま保持
        return {slot_name.lower(): content}
    
    def _needs_nesting(self, content: str, slot_data: Dict[str, Any]) -> bool:
        """入れ子分解判定"""
        # 複数語句判定
        if len(content.split()) > 1:
            return True
        
        # 動詞を含む判定（将来の句・節対応）
        # TODO: より詳細な判定ロジック実装
        
        return False

# テスト用の簡単な実行関数
def test_unified_engine():
    """統一再帰分解エンジンのテスト"""
    engine = PureStanzaEngineV31()
    
    test_cases = [
        "I sleep.",
        "She is happy.", 
        "He plays tennis.",
        "I gave him a book.",
        "The tall man runs fast.",  # 入れ子テスト用
    ]
    
    for sentence in test_cases:
        print(f"\n{'='*50}")
        print(f"テスト文: {sentence}")
        print('='*50)
        
        result = engine.decompose_unified(sentence)
        print(f"結果: {json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_unified_engine()
