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
        
        # 文型パターンルール（上位レベル用）
        self.sentence_patterns = self._load_sentence_patterns()
        
        # サブレベル専用パターンルール
        self.sublevel_patterns = self._load_sublevel_patterns()
        
        # 修飾語マッピングルール（上位レベル用）
        self.modifier_mappings = self._load_modifier_mappings()
        
        # サブレベル専用修飾語マッピング
        self.sublevel_modifiers = self._load_sublevel_modifiers()
        
        # 入れ子判定ルール
        self.nested_triggers = self._load_nested_triggers()
        
        print("🏗️ 統一再帰分解エンジン準備完了 (v3.1)")
        
    def _load_sentence_patterns(self) -> Dict[str, Any]:
        """統一文型パターンルール（上位レベル用）"""
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
    
    def _load_sublevel_patterns(self) -> Dict[str, Any]:
        """サブレベル専用パターンルール - Stanza入れ子構造対応"""
        return {
            # サブレベルでは中心語が常にrootになる
            "NOUN_PHRASE": {
                "required_relations": ["root"],
                "root_pos": ["NOUN", "PRON"],
                "mapping": {"root": "C1"}
            },
            "ADJ_PHRASE": {
                "required_relations": ["root"],
                "root_pos": ["ADJ"],
                "mapping": {"root": "C1"}
            },
            "ADV_PHRASE": {
                "required_relations": ["root"],
                "root_pos": ["ADV"],
                "mapping": {"root": "M2"}
            },
            "VERB_PHRASE": {
                "required_relations": ["root"],
                "root_pos": ["VERB"],
                "mapping": {"root": "V"}
            },
            # 前置詞句（"in the garden"など）
            "PREP_PHRASE": {
                "required_relations": ["root", "case"],
                "root_pos": ["NOUN"],
                "mapping": {"root": "C1", "case": "M1"}
            }
        }
    
    def _load_sublevel_modifiers(self) -> Dict[str, str]:
        """サブレベル専用修飾語マッピング"""
        return {
            "det": "M1",        # 限定詞: a, the, this → M1
            "amod": "M2",       # 形容詞修飾: tall, beautiful → M2  
            "advmod": "M3",     # 副詞修飾: very, quite → M3
            "case": "M1",       # 前置詞: in, on, at → M1
            "compound": "M2",   # 複合語: New York → M2
            "nummod": "M1",     # 数量詞: two, many → M1
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
        階層に応じて上位レベル/サブレベル専用処理を適用
        
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
        
        # ROOT語検出（階層に関係なく実行）
        root_word = self._find_root_word(sent)
        if not root_word:
            print(f"{'  ' * depth}⚠️ ROOT語未検出")
            return {"error": "No root word found"}
        
        print(f"{'  ' * depth}🎯 ROOT: '{root_word.text}' ({root_word.pos})")
        
        # 階層判定：上位レベル vs サブレベル
        is_sublevel = depth > 0
        
        if is_sublevel:
            # サブレベル専用処理
            print(f"{'  ' * depth}📊 サブレベル処理適用")
            basic_slots = self._extract_sublevel_slots(sent, root_word, depth)
        else:
            # 上位レベル処理（従来通り）
            print(f"{'  ' * depth}📊 上位レベル処理適用")
            basic_slots = self._extract_basic_slots(sent, root_word, depth)
        
        # 統一入れ子処理：8つの再帰可能スロットで再帰適用
        unified_result = self._apply_unified_nesting(basic_slots, depth)
        
        print(f"{'  ' * depth}📋 統一分解完了: {len([k for k, v in unified_result.items() if k != 'metadata'])}スロット")
        
        return unified_result
    
    def _find_root_word(self, sent) -> Optional[Any]:
        """ROOT語検出（階層共通）- 動詞以外も対応"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _find_root_verb(self, sent) -> Optional[Any]:
        """ROOT動詞検出（上位レベル互換用）"""
        return self._find_root_word(sent)
    
    def _extract_sublevel_slots(self, sent, root_word, depth: int) -> Dict[str, Any]:
        """サブレベル専用スロット抽出 - Stanza入れ子構造対応"""
        # 全依存関係を収集
        all_relations = {}
        for word in sent.words:
            all_relations[word.deprel] = word
        
        # サブレベル専用パターンマッチング
        matched_pattern = self._match_sublevel_pattern(sent, root_word, depth)
        
        if not matched_pattern:
            print(f"{'  ' * depth}❌ サブレベルパターン未検出")
            return {}
        
        print(f"{'  ' * depth}✅ サブマッチパターン: {matched_pattern}")
        
        # スロット抽出
        slots = {}
        
        # サブレベル専用コアスロット抽出
        self._extract_sublevel_core_slots(sent, root_word, slots, depth)
        
        # サブレベル専用修飾語処理
        self._process_sublevel_modifiers(sent, slots, depth)
        
        return slots
    
    def _match_sublevel_pattern(self, sent, root_word, depth: int) -> Optional[str]:
        """サブレベル専用パターンマッチング"""
        relations = {word.deprel: word for word in sent.words}
        root_pos = root_word.pos
        
        # サブレベルパターン判定
        for pattern_name, pattern_info in self.sublevel_patterns.items():
            required = set(pattern_info["required_relations"])
            available = set(relations.keys())
            
            if required.issubset(available) and root_pos in pattern_info["root_pos"]:
                return pattern_name
        
        # フォールバック：基本的な品詞ベース判定
        if root_pos in ["NOUN", "PRON"]:
            return "NOUN_PHRASE"
        elif root_pos == "ADJ":
            return "ADJ_PHRASE"
        elif root_pos == "ADV":
            return "ADV_PHRASE"
        elif root_pos == "VERB":
            return "VERB_PHRASE"
        
        return "NOUN_PHRASE"  # デフォルト
    
    def _extract_sublevel_core_slots(self, sent, root_word, slots: Dict[str, Any], depth: int):
        """サブレベル専用コアスロット抽出"""
        # ROOT語を適切なスロットにマッピング
        root_pos = root_word.pos
        
        if root_pos in ["NOUN", "PRON"]:
            slot_name = "C1"  # 補語として扱う
        elif root_pos == "ADJ":
            slot_name = "C1"  # 形容詞補語
        elif root_pos == "ADV":
            slot_name = "M2"  # 副詞修飾語
        elif root_pos == "VERB":
            slot_name = "V"   # 動詞
        else:
            slot_name = "C1"  # デフォルト
        
        slots[slot_name] = {
            "content": root_word.text,
            "pos": root_word.pos,
            "deprel": root_word.deprel,
            "word_obj": root_word
        }
        
        print(f"{'  ' * depth}📍 {slot_name}: '{root_word.text}' (サブレベルROOT)")
    
    def _process_sublevel_modifiers(self, sent, slots: Dict[str, Any], depth: int):
        """サブレベル専用修飾語処理"""
        for word in sent.words:
            if word.deprel in self.sublevel_modifiers:
                slot_mapping = self.sublevel_modifiers[word.deprel]
                
                # サブレベルでは直接スロットマッピング
                slots[slot_mapping] = {
                    "content": word.text,
                    "pos": word.pos,
                    "deprel": word.deprel,
                    "word_obj": word
                }
                print(f"{'  ' * depth}📍 {slot_mapping}: '{word.text}' (サブレベル修飾語: {word.deprel})")
    
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
        """コアスロットの抽出（SVOO重複問題修正版）"""
        # 文型判定
        relations = {word.deprel: word for word in sent.words}
        is_svoo = 'iobj' in relations and 'obj' in relations
        is_svo = 'obj' in relations and 'iobj' not in relations
        
        for word in sent.words:
            slot_name = None
            
            # 主語系
            if word.deprel == 'nsubj' or word.deprel == 'nsubj:pass':
                slot_name = 'S'
                # 複合主語の場合の処理
                subject_text = self._extract_compound_phrase(sent, word)
                word_text = subject_text if subject_text != word.text else word.text
            # 目的語系（文型に応じて適切に分類）
            elif word.deprel == 'iobj':
                slot_name = 'O1'  # 間接目的語 → 常にO1
                word_text = word.text
            elif word.deprel == 'obj':
                if is_svoo:
                    slot_name = 'O2'  # SVOO構文：直接目的語 → O2
                else:
                    slot_name = 'O1'  # SVO構文：目的語 → O1
                word_text = self._extract_compound_phrase(sent, word)
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
                
                # デバッグ情報に文型情報を追加
                pattern_info = ""
                if is_svoo and word.deprel in ['iobj', 'obj']:
                    pattern_info = f" [SVOO: {'間接' if word.deprel == 'iobj' else '直接'}目的語]"
                elif is_svo and word.deprel == 'obj':
                    pattern_info = " [SVO: 目的語]"
                
                print(f"{'  ' * depth}📍 {slot_name}: '{word_text}' (deprel: {word.deprel}){pattern_info}")
    
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
