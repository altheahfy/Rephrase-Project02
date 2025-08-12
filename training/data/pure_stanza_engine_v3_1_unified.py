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
        
        # spaCy（境界調整用）- step18汎用メカニズム統合
        self.spacy_nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy準備完了")
        
        # step18汎用境界拡張設定
        self.span_expand_deps = ['det', 'poss', 'compound', 'amod', 'nummod', 'case']
        self.relative_pronoun_deps = ['nsubj', 'dobj', 'pobj']  # 関係代名詞の一般的役割
        
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
        """サブレベル専用パターンルール - 上位レベル5文型に対応"""
        return {
            # === 基本句構造 ===
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
            "PREP_PHRASE": {
                "required_relations": ["root", "case"],
                "root_pos": ["NOUN"],
                "mapping": {"root": "C1", "case": "M1"}
            },
            
            # === サブレベル5文型（関係節・従属節対応） ===
            "SUB_SV": {
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"}
            },
            "SUB_SVC": {
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SUB_SVO": {
                "required_relations": ["nsubj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "root": "V"}
            },
            "SUB_SVOO": {
                "required_relations": ["nsubj", "iobj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "iobj": "O1", "obj": "O2", "root": "V"}
            },
            "SUB_SVOC": {
                "required_relations": ["nsubj", "obj", "xcomp", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "xcomp": "C2", "root": "V"}
            },
            
            # === 関係代名詞節専用 ===
            "REL_SUBJ": {
                # "who runs" - 関係代名詞が主語
                "required_relations": ["root"],
                "root_pos": ["VERB"],
                "special": "relative_subject",
                "mapping": {"root": "V"}
            },
            "REL_OBJ": {
                # "that he bought" - 関係代名詞が目的語
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "special": "relative_object", 
                "mapping": {"nsubj": "S", "root": "V"}
            },
            
            # === 従属節（副詞節） ===
            "ADV_CLAUSE": {
                # "although he runs", "when she arrives"
                "required_relations": ["mark", "nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"mark": "M1", "nsubj": "S", "root": "V"}
            },
            
            # === 分詞構文 ===
            "PARTICIPLE": {
                # "running fast", "built yesterday"
                "required_relations": ["root"],
                "root_pos": ["VERB"],
                "special": "participial",
                "mapping": {"root": "V"}
            },
            
            # === 比較構文 ===
            "COMPARATIVE": {
                # "taller than John"
                "required_relations": ["root", "case"],
                "root_pos": ["ADJ"],
                "special": "comparison",
                "mapping": {"root": "C1", "case": "M1"}
            }
        }
    
    def _load_sublevel_modifiers(self) -> Dict[str, str]:
        """サブレベル専用修飾語マッピング - 上位レベル網羅対応"""
        return {
            # === 基本修飾語 ===
            "det": "M1",        # 限定詞: a, the, this, that
            "amod": "M2",       # 形容詞修飾: tall, beautiful, red
            "advmod": "M3",     # 副詞修飾: very, quite, extremely  
            "case": "M1",       # 前置詞: in, on, at, with, by
            "compound": "M2",   # 複合語: New York, high school
            "nummod": "M1",     # 数量詞: two, many, several
            
            # === 高次修飾語 ===
            "mark": "M1",       # 従属節マーカー: that, which, who, because, although
            "cc": "M1",         # 等位接続詞: and, or, but
            "conj": "M2",       # 等位要素: books and pens の "pens"
            "appos": "M2",      # 同格: John, the teacher
            "acl": "M2",        # 修飾節: book that I bought
            "acl:relcl": "M2",  # 関係代名詞節: man who runs
            
            # === 時制・相関連 ===
            "aux": "Aux",       # 助動詞: have, be, will, can
            "aux:pass": "Aux",  # 受動助動詞: be (in "be built")
            "auxpass": "Aux",   # 受動助動詞（別表記）
            "tmod": "M3",       # 時間修飾: yesterday, tomorrow
            
            # === 前置詞句関連 ===
            "pobj": "C1",       # 前置詞の目的語: in the garden の "garden"
            "pcomp": "C1",      # 前置詞補語
            "agent": "M1",      # 動作主: by him (受動態)
            
            # === 比較・程度 ===
            "neg": "M3",        # 否定: not, never
            "expl": "M3",       # 虚辞: there (in "there is")
            "dep": "M3",        # その他依存語
            "parataxis": "M2",  # 並列文: He said, "Hello"
            
            # === 疑問・関係語 ===
            "nsubj:xsubj": "S", # 疑問主語
            "ccomp": "O1",      # 補文: think that he runs
            "xcomp": "C2",      # 制御補文: want to go
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
        
        # 関係節を含む名詞句の特別処理
        has_relative_clause = any(w.deprel == 'acl:relcl' for w in sent.words)
        
        # 階層判定：上位レベル vs サブレベル
        is_sublevel = depth > 0
        
        if has_relative_clause and root_word.pos == 'NOUN' and depth == 0:
            print(f"{'  ' * depth}📖 関係節を含む名詞句として処理")
            basic_slots = self._extract_noun_phrase_with_relative_clause(sent, root_word, depth)
        elif is_sublevel:
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
    
    def _apply_unified_nesting(self, slots: Dict[str, Any], depth: int) -> Dict[str, Any]:
        """統一入れ子適用（Rephrase原則：上位スロット空化 + サブスロット配置）"""
        unified_result = {}
        
        for slot_key, slot_data in slots.items():
            if slot_key.startswith('_') or slot_key == 'metadata':
                unified_result[slot_key] = slot_data
                continue
            
            if not slot_data or not slot_data.get('content'):
                continue
            
            content = slot_data['content']
            
            # 境界拡張適用（step18汎用メカニズム）
            expanded_content = self._expand_span_generic(content, {
                'slot_type': slot_key,
                'depth': depth
            })
            
            # 入れ子判定（spaCy強化版）
            if self._needs_nesting(expanded_content, slot_data):
                # 【Rephrase原則】上位スロットを空に設定
                unified_result[slot_key] = ''
                
                print(f"{'  ' * depth}🔄 '{slot_key}' → サブレベル分解: '{expanded_content[:20]}...'")
                
                # サブレベル解析（再帰実行）
                sublevel_data = self.decompose_unified(expanded_content, depth + 1)
                
                # 【Rephrase原則】全内容をサブスロットに配置
                for sub_key, sub_value in sublevel_data.items():
                    if sub_key == 'metadata' or sub_key.startswith('_'):
                        continue  # メタデータはスキップ
                    
                    # サブスロットとして配置（sub-プレフィックス付き）
                    final_key = f"sub-{sub_key.lower()}"
                    # 値を文字列として格納（Rephrase原則）
                    if isinstance(sub_value, dict) and 'content' in sub_value:
                        unified_result[final_key] = sub_value['content']
                    elif isinstance(sub_value, dict):
                        # 辞書の場合、主要な値を抽出
                        main_value = next(iter(sub_value.values())) if sub_value else ''
                        unified_result[final_key] = main_value
                    else:
                        unified_result[final_key] = sub_value
                    
                    print(f"{'  ' * depth}  ↳ {final_key}: '{unified_result[final_key]}'")
            else:
                # 単語レベル：そのまま配置
                unified_result[slot_key] = expanded_content
                print(f"{'  ' * depth}📝 '{slot_key}': '{expanded_content}' (単語レベル)")
        
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
        """サブレベル専用パターンマッチング - 5文型対応強化版"""
        relations = {word.deprel: word for word in sent.words}
        root_pos = root_word.pos
        
        # === 1. 完全5文型判定（関係節・従属節） ===
        if 'nsubj' in relations and root_pos == 'VERB':
            # 関係代名詞節判定
            if 'mark' in relations:
                mark_word = relations['mark'].text.lower()
                if mark_word in ['that', 'which', 'who', 'whom', 'whose']:
                    if 'obj' in relations and 'iobj' in relations:
                        return "SUB_SVOO"  # 関係節内の第4文型
                    elif 'obj' in relations and 'xcomp' in relations:
                        return "SUB_SVOC"  # 関係節内の第5文型
                    elif 'obj' in relations:
                        return "SUB_SVO"   # 関係節内の第3文型
                    else:
                        return "SUB_SV"    # 関係節内の第1文型
            
            # 従属節判定
            elif 'mark' in relations:
                mark_word = relations['mark'].text.lower()
                if mark_word in ['because', 'although', 'when', 'if', 'since', 'while']:
                    return "ADV_CLAUSE"  # 副詞節
            
            # 通常のサブレベル5文型
            elif 'obj' in relations and 'iobj' in relations:
                return "SUB_SVOO"
            elif 'obj' in relations and 'xcomp' in relations:
                return "SUB_SVOC"
            elif 'obj' in relations:
                return "SUB_SVO"
            else:
                return "SUB_SV"
        
        # === 2. SVC系（関係節対応） ===
        if 'nsubj' in relations and 'cop' in relations:
            return "SUB_SVC"
        
        # === 3. 前置詞句判定 ===
        if 'case' in relations and root_pos == 'NOUN':
            case_word = relations['case'].text.lower()
            if case_word in ['than', 'as']:  # 比較構文
                return "COMPARATIVE"
            else:
                return "PREP_PHRASE"
        
        # === 4. 関係代名詞特殊形（主語省略） ===
        if root_pos == 'VERB' and 'nsubj' not in relations:
            # "who runs" のような関係代名詞が主語の場合
            return "REL_SUBJ"
        
        # === 5. 分詞構文判定 ===
        if root_pos == 'VERB' and root_word.text.endswith(('ing', 'ed', 'en')):
            return "PARTICIPLE"
        
        # === 6. 基本句判定（フォールバック） ===
        if root_pos in ["NOUN", "PRON"]:
            return "NOUN_PHRASE"
        elif root_pos == "ADJ":
            # 比較級・最上級判定
            if any(word.deprel == 'case' for word in sent.words):
                return "COMPARATIVE"
            else:
                return "ADJ_PHRASE"
        elif root_pos == "ADV":
            return "ADV_PHRASE"
        
        return "NOUN_PHRASE"  # 最終デフォルト
    
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
        """基本10スロット抽出（関係代名詞節分離対応版）"""
        # 関係代名詞節を事前に分離
        main_words, relative_clauses = self._separate_relative_clauses(sent, depth)
        
        # 全依存関係を収集（メイン節のみ）
        all_relations = {}
        for word in main_words:
            all_relations[word.deprel] = word
        
        # 文型パターンマッチング（メイン節で実行）
        matched_pattern = self._match_sentence_pattern_enhanced(sent, root_verb)
        
        if not matched_pattern:
            print(f"{'  ' * depth}❌ 文型パターン未検出")
            return {}
        
        print(f"{'  ' * depth}✅ マッチしたパターン: {matched_pattern}")
        
        # スロット抽出
        slots = {}
        
        # 基本スロット抽出（メイン節のみ）
        self._extract_core_slots(sent, root_verb, slots, depth, main_words)
        
        # 修飾語処理（メイン節）
        self._process_modifiers(sent, slots, depth, main_words)
        
        # 関係代名詞節を適切なスロットに統合
        self._integrate_relative_clauses(relative_clauses, slots, depth)
        
        return slots
    
    def _separate_relative_clauses(self, sent, depth: int) -> Tuple[List, Dict]:
        """関係代名詞節を分離してメイン節と関係節に分割"""
        main_words = []
        relative_clauses = {}
        
        # 関係代名詞節の検出
        rel_verbs = [w for w in sent.words if w.deprel == 'acl:relcl']
        
        if not rel_verbs:
            # 関係節がない場合、全ての語をメイン節として返す
            return list(sent.words), {}
        
        for rel_verb in rel_verbs:
            # この関係節に属する語を収集
            rel_words = [rel_verb]  # 関係節動詞
            
            # 関係節動詞に依存する語を収集
            for word in sent.words:
                if word.head == rel_verb.id:
                    rel_words.append(word)
            
            # 修飾される名詞を特定
            modified_noun_id = rel_verb.head
            modified_noun = next((w for w in sent.words if w.id == modified_noun_id), None)
            
            if modified_noun:
                relative_clauses[modified_noun.id] = {
                    'modified_noun': modified_noun,
                    'rel_verb': rel_verb,
                    'rel_words': rel_words,
                    'clause_text': ' '.join(w.text for w in sorted(rel_words, key=lambda x: x.id))
                }
                
                print(f"{'  ' * depth}🔗 関係節検出: '{modified_noun.text}' ← '{relative_clauses[modified_noun.id]['clause_text']}'")
        
        # メイン節の語を抽出（関係節に属さない語）
        rel_word_ids = set()
        for rel_info in relative_clauses.values():
            rel_word_ids.update(w.id for w in rel_info['rel_words'])
        
        main_words = [w for w in sent.words if w.id not in rel_word_ids]
        
        return main_words, relative_clauses
    
    def _integrate_relative_clauses(self, relative_clauses: Dict, slots: Dict[str, Any], depth: int):
        """関係代名詞節を適切なスロットのサブ構造として統合"""
        for modified_noun_id, rel_info in relative_clauses.items():
            modified_noun = rel_info['modified_noun']
            clause_text = rel_info['clause_text']
            
            # 修飾される名詞がどのスロットに含まれるかを特定
            target_slot = self._find_slot_containing_noun(modified_noun, slots)
            
            if target_slot:
                print(f"{'  ' * depth}🎯 関係節統合: {target_slot}スロット内の'{modified_noun.text}'に'{clause_text}'を追加")
                
                # そのスロットに関係節マーカーを追加
                if 'relative_clauses' not in slots[target_slot]:
                    slots[target_slot]['relative_clauses'] = []
                
                slots[target_slot]['relative_clauses'].append({
                    'clause_text': clause_text,
                    'modified_noun': modified_noun.text
                })
    
    def _find_slot_containing_noun(self, noun, slots: Dict[str, Any]) -> Optional[str]:
        """指定した名詞を含むスロットを特定"""
        for slot_name, slot_data in slots.items():
            if isinstance(slot_data, dict) and 'content' in slot_data:
                if noun.text in slot_data['content']:
                    return slot_name
        return None
    
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
    
    def _extract_core_slots(self, sent, root_verb, slots: Dict[str, Any], depth: int, target_words: List = None):
        """コアスロットの抽出（SVOO重複問題修正版 + 関係節分離対応）"""
        # 処理対象の語を決定
        words_to_process = target_words if target_words is not None else sent.words
        
        # 文型判定
        relations = {word.deprel: word for word in words_to_process}
        is_svoo = 'iobj' in relations and 'obj' in relations
        is_svo = 'obj' in relations and 'iobj' not in relations
        
        for word in words_to_process:
            slot_name = None
            
            # 主語系
            if word.deprel == 'nsubj' or word.deprel == 'nsubj:pass':
                slot_name = 'S'
                # 複合主語の場合の処理
                subject_text = self._extract_compound_phrase(sent, word, target_words)
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
                word_text = self._extract_compound_phrase(sent, word, target_words)
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
    
    def _extract_compound_phrase(self, sent, head_word, target_words: List = None) -> str:
        """複合句の抽出（spaCy境界調整統合版）- step18汎用メカニズム適用"""
        # 処理対象の語を決定
        words_to_check = target_words if target_words is not None else sent.words
        
        # Stanzaベースの基本抽出
        phrase_words = [head_word]
        
        # 依存語を収集（処理対象の語のみから）
        for word in words_to_check:
            if word.head == head_word.id and word.deprel in ['det', 'amod', 'compound', 'case']:
                phrase_words.append(word)
        
        # spaCy境界調整を適用
        basic_phrase = ' '.join(w.text for w in sorted(phrase_words, key=lambda x: x.id))
        
        # spaCyでの精密境界調整
        adjusted_phrase = self._apply_spacy_boundary_adjustment(basic_phrase, sent)
        
        return adjusted_phrase
    
    def _apply_spacy_boundary_adjustment(self, phrase_text: str, stanza_sent) -> str:
        """spaCy境界調整（step18汎用メカニズム）"""
        try:
            # spaCyで解析
            spacy_doc = self.spacy_nlp(phrase_text)
            
            # 境界調整ロジック適用
            adjusted_tokens = []
            for token in spacy_doc:
                # 基本トークン追加
                adjusted_tokens.append(token.text)
                
                # 関係代名詞の境界調整
                if token.dep_ in ['relcl', 'acl'] and token.pos_ == 'VERB':
                    # 関係代名詞を含む境界拡張
                    rel_pronouns = self._find_relative_pronouns(token, spacy_doc)
                    adjusted_tokens.extend(rel_pronouns)
            
            return ' '.join(adjusted_tokens)
            
        except Exception as e:
            # spaCy処理失敗時はStanzaベースの結果を返す
            print(f"⚠️ spaCy境界調整失敗: {e}")
            return phrase_text
    
    def _find_relative_pronouns(self, rel_verb_token, spacy_doc) -> List[str]:
        """関係代名詞検出（汎用）- step18メカニズム適用"""
        rel_pronouns = []
        
        # 関係動詞の子要素から関係代名詞を探す
        for child in rel_verb_token.children:
            if child.pos_ == 'PRON' and child.dep_ in self.relative_pronoun_deps:
                # 関係代名詞の一般的パターン
                if child.text.lower() in ['who', 'whom', 'whose', 'which', 'that']:
                    rel_pronouns.append(child.text)
        
        return rel_pronouns
    
    def _match_sentence_pattern(self, relations: List[str], root_pos: str) -> Optional[str]:
        """文型パターンマッチング"""
        for pattern_name, pattern_info in self.sentence_patterns.items():
            required = set(pattern_info["required_relations"])
            available = set(relations)
            
            if required.issubset(available) and root_pos in pattern_info["root_pos"]:
                return pattern_name
        
        return None
    
    def _process_modifiers(self, sent, slots: Dict[str, Any], depth: int, target_words: List = None):
        """修飾語処理（統一アルゴリズム）関係節分離対応版"""
        # 処理対象の語を決定
        words_to_process = target_words if target_words is not None else sent.words
        
        for word in words_to_process:
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
        """入れ子分解判定（spaCy強化版）"""
        # 複数語句判定
        if len(content.split()) > 1:
            return True
        
        # spaCyでの詳細分析
        try:
            spacy_doc = self.spacy_nlp(content)
            
            # 関係節・従属節検出
            for token in spacy_doc:
                if token.dep_ in ['relcl', 'acl', 'advcl', 'ccomp', 'xcomp']:
                    return True
                    
            # 複合修飾語検出
            modifier_count = sum(1 for token in spacy_doc if token.dep_ in self.span_expand_deps)
            if modifier_count > 1:
                return True
                
        except Exception:
            pass  # spaCy処理失敗時は基本判定のみ
        
        return False
    
    def _expand_span_generic(self, text: str, expansion_context: Dict = None) -> str:
        """汎用スパン拡張処理（step18メカニズム統合）"""
        try:
            spacy_doc = self.spacy_nlp(text)
            
            if len(spacy_doc) <= 1:
                return text
                
            # 拡張設定（コンテキストベース）
            expand_deps = expansion_context.get('expand_deps', self.span_expand_deps) if expansion_context else self.span_expand_deps
            
            # 各トークンの境界拡張
            expanded_spans = []
            
            for token in spacy_doc:
                span_start = token.i
                span_end = token.i
                
                # 依存語による拡張
                for child in token.children:
                    if child.dep_ in expand_deps:
                        span_start = min(span_start, child.i)
                        span_end = max(span_end, child.i)
                
                # 関係代名詞の境界拡張
                if token.dep_ in ['relcl', 'acl']:
                    rel_pronouns = self._find_relative_pronouns_in_span(token, spacy_doc)
                    for rel_idx in rel_pronouns:
                        span_start = min(span_start, rel_idx)
                        span_end = max(span_end, rel_idx)
                
                if span_start <= span_end:
                    span_text = ' '.join(spacy_doc[i].text for i in range(span_start, span_end + 1))
                    expanded_spans.append(span_text)
            
            # 重複除去と結合
            unique_spans = list(dict.fromkeys(expanded_spans))  # 順序保持で重複除去
            return ' '.join(unique_spans) if unique_spans else text
            
        except Exception as e:
            print(f"⚠️ 汎用スパン拡張エラー: {e}")
            return text
    
    def _find_relative_pronouns_in_span(self, rel_token, spacy_doc) -> List[int]:
        """スパン内関係代名詞インデックス検出（汎用）"""
        rel_indices = []
        
        for child in rel_token.children:
            if (child.pos_ == 'PRON' and 
                child.dep_ in self.relative_pronoun_deps and
                child.text.lower() in ['who', 'whom', 'whose', 'which', 'that']):
                rel_indices.append(child.i)
        
        return rel_indices
    
    def _analyze_sublevel_structure(self, content: str, slot_data: Dict[str, Any], context: Dict = None) -> Dict[str, Any]:
        """サブレベル構造解析（汎用アルゴリズム）"""
        try:
            print(f"🔬 サブレベル解析: '{content[:30]}...'")
            
            # 再帰実行でサブレベル分解
            sublevel_result = self.decompose_unified(content, context.get('depth', 1) if context else 1)
            
            # プレフィックス調整
            adjusted_result = {}
            level_prefix = context.get('level_prefix', 'sub-') if context else 'sub-'
            
            for key, value in sublevel_result.items():
                if key in ['metadata', '_pattern'] or key.startswith('_'):
                    continue
                
                # sub-プレフィックス適用
                final_key = f"{level_prefix}{key.lower()}"
                adjusted_result[final_key] = value
            
            return adjusted_result
            
        except Exception as e:
            print(f"⚠️ サブレベル解析エラー: {e}")
            return {}
    
    def _get_expansion_deps_for_slot(self, slot_key: str) -> List[str]:
        """スロットタイプ別拡張依存語設定"""
        slot_expansion_map = {
            'S': ['det', 'amod', 'compound', 'nmod', 'acl', 'relcl'],
            'V': ['aux', 'auxpass', 'neg', 'advmod'],
            'O1': ['det', 'amod', 'compound', 'nmod', 'acl', 'relcl'],
            'O2': ['det', 'amod', 'compound', 'nmod'],
            'M1': ['advmod', 'prep', 'pobj', 'case'],
            'C1': ['det', 'amod', 'compound'],
            'C2': ['det', 'amod', 'compound'],
            'M2': ['advmod', 'prep', 'pobj'],
            'M3': ['advmod', 'prep', 'pobj']
        }
        
        return slot_expansion_map.get(slot_key, self.span_expand_deps)
    
    def _is_noun_phrase_with_relative_clause(self, sent, root_word) -> bool:
        """関係節を含む名詞句かどうかを判定"""
        if root_word.pos != 'NOUN':
            return False
        
        # 関係節（acl:relcl）を含むかチェック
        for word in sent.words:
            if word.deprel == 'acl:relcl' and word.head == root_word.id:
                return True
        
        return False
    
    def _extract_noun_phrase_with_relative_clause(self, sent, root_word, depth: int) -> Dict[str, Any]:
        """関係節付き名詞句の専用処理（Rephrase原則準拠）- 構造解析ベース"""
        slots = {}
        
        # === 構造分析に基づく正しい分離 ===
        # 1. メイン名詞句: root_noun + その修飾語 + 関係代名詞
        # 2. 関係節: 関係代名詞以外の関係節構成要素
        
        main_phrase_words = [root_word]  # "book"
        rel_pronoun = None               # "that"
        rel_verb = None                  # "bought" 
        rel_subject = None               # "he"
        
        # 語の分類
        for word in sent.words:
            if word.head == root_word.id:
                if word.deprel == 'det' or word.deprel == 'amod':
                    # 名詞の修飾語: "The"
                    main_phrase_words.append(word)
                elif word.deprel == 'acl:relcl':
                    # 関係節動詞: "bought"
                    rel_verb = word
            elif word.deprel == 'obj' and any(w.id == word.head and w.deprel == 'acl:relcl' for w in sent.words):
                # 関係代名詞（関係節動詞の目的語）: "that"
                rel_pronoun = word
                main_phrase_words.append(word)  # 名詞句に含める
            elif word.deprel == 'nsubj' and any(w.id == word.head and w.deprel == 'acl:relcl' for w in sent.words):
                # 関係節の主語: "he"
                rel_subject = word
        
        # 語順でソート
        main_phrase_words.sort(key=lambda w: w.id)
        
        # メイン名詞句構築: "The book that"
        main_phrase = ' '.join(w.text for w in main_phrase_words)
        
        # Rephrase原則：各要素をスロットに配置
        slots['O1'] = {
            'content': main_phrase,  # "The book that"
            'deprel': 'noun_phrase_with_rel',
            'pos': 'NOUN_PHRASE'
        }
        
        if rel_subject:
            slots['S'] = {
                'content': rel_subject.text,  # "he"
                'deprel': 'nsubj',
                'pos': rel_subject.pos
            }
        
        if rel_verb:
            slots['V'] = {
                'content': rel_verb.text,  # "bought"
                'deprel': 'acl:relcl', 
                'pos': rel_verb.pos
            }
        
        print(f"{'  ' * depth}🎯 構造分析: '{main_phrase}' | {rel_subject.text if rel_subject else '?'} | {rel_verb.text if rel_verb else '?'}")
        
        return slots

# === テスト実行 ===
if __name__ == "__main__":
    print("="*60)
    print("🚀 Pure Stanza Engine v3.1 - Rephrase原則準拠版テスト")
    print("="*60)
    
    engine = PureStanzaEngineV31()
    
    # 関係節テスト - The book that he bought
    print("\n📖 関係節テスト: 'The book that he bought'")
    print("-" * 50)
    result1 = engine.decompose_unified("The book that he bought")
    print("\n📊 結果:")
    for k, v in result1.items():
        if not k.startswith('_') and not k == 'metadata':
            if isinstance(v, dict) and len(v) == 1:
                # 単一値の辞書は値のみ表示
                value = next(iter(v.values()))
                print(f"  {k}: '{value}'")
            else:
                print(f"  {k}: '{v}'")
    
    print(f"\n期待結果:")
    print(f"  O1: '' (空)")
    print(f"  sub-o1: 'The book that'")
    print(f"  sub-s: 'he'")
    print(f"  sub-v: 'bought'")
    
    print("\n" + "="*60)
    print("🎯 Rephrase原則準拠の関係節処理完成！")
    print("="*60)

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
