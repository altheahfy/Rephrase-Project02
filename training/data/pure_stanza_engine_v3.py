#!/usr/bin/env python3
"""
Pure Stanza Engine v3 - ゼロハードコーディング版
体系的な依存関係パターンマッピングによる汎用的文分解エンジン
"""

import stanza
import spacy
import json
from typing import Dict, List, Optional, Tuple, Any

class PureStanzaEngineV3:
    """
    Pure Stanza Engine v3 - 完全設定駆動型
    
    設計原則:
    1. ゼロハードコーディング - 特定の語彙・構造に依存しない
    2. パターン駆動 - Stanza依存関係パターンからRephraseスロットへのマッピング
    3. 拡張可能 - 新しいパターンは設定追加のみで対応
    """
    
    def __init__(self):
        """エンジン初期化"""
        print("🎯 PureStanzaEngine v3 初期化中...")
        
        # Stanza NLP パイプライン
        self.nlp = stanza.Pipeline('en', verbose=False)
        print("✅ Stanza準備完了")
        
        # spaCy（境界調整用）
        self.spacy_nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy準備完了")
        
        # 文型パターンルール
        self.sentence_patterns = self._load_sentence_patterns()
        
        # 修飾語マッピングルール
        self.modifier_mappings = self._load_modifier_mappings()
        
        print("🏗️ 設定駆動型エンジン準備完了 (v3)")
        
    def _load_sentence_patterns(self) -> Dict[str, Any]:
        """文型パターンルールをロード"""
        return {
            # 第1文型 (SV): nsubj -> root(VERB)
            "SV": {
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj": "S",
                    "root": "V"
                }
            },
            
            # 助動詞構文: nsubj -> aux -> root(VERB)
            "S_AUX_V": {
                "required_relations": ["nsubj", "aux", "root"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj": "S",
                    "aux": "Aux",
                    "root": "V"
                }
            },
            
            # 助動詞 + 目的語: nsubj -> aux -> root(VERB) -> obj
            "S_AUX_V_O": {
                "required_relations": ["nsubj", "aux", "root", "obj"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj": "S",
                    "aux": "Aux",
                    "root": "V",
                    "obj": "O1"
                }
            },
            
            # 受動態: nsubj:pass -> aux:pass -> root(VERB)
            "PASSIVE": {
                "required_relations": ["nsubj:pass", "aux:pass", "root"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj:pass": "S",
                    "aux:pass": "Aux",
                    "root": "V"
                }
            },
            
            # 受動態 + 助動詞: nsubj:pass -> aux -> aux:pass -> root(VERB)
            "PASSIVE_AUX": {
                "required_relations": ["nsubj:pass", "aux", "aux:pass", "root"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj:pass": "S",
                    "aux": "Aux",
                    "aux:pass": "Aux",  # 複数のAuxは統合処理
                    "root": "V"
                }
            },
            
            # There構文: expl -> root(VERB) -> nsubj
            "THERE_BE": {
                "required_relations": ["expl", "nsubj", "root"],
                "root_pos": ["VERB"],
                "expl_check": True,
                "mapping": {
                    "expl": "M1",  # "There" を M1 に配置
                    "root": "V",
                    "nsubj": "O1"  # 真の主語は O1 に配置
                }
            },
            
            # 疑問文（疑問詞がROOT）: root(PRON) -> cop -> nsubj
            "WH_BE": {
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["PRON"],
                "mapping": {
                    "root": "O1",  # 疑問詞を O1 に配置
                    "cop": "V",
                    "nsubj": "S"
                }
            },
            
            # 第2文型 (SVC): nsubj -> cop -> root(ADJ/NOUN)  
            "SVC_BE": {
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {
                    "nsubj": "S",
                    "cop": "V", 
                    "root": "C1"
                }
            },
            
            # 第2文型変形: nsubj -> root(VERB) -> xcomp(ADJ)
            "SVC_LOOKS": {
                "required_relations": ["nsubj", "root", "xcomp"],
                "root_pos": ["VERB"],
                "xcomp_pos": ["ADJ"],
                "mapping": {
                    "nsubj": "S",
                    "root": "V",
                    "xcomp": "C1"
                }
            },
            
            # 第3文型 (SVO): nsubj -> root(VERB) -> obj
            "SVO": {
                "required_relations": ["nsubj", "root", "obj"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj": "S",
                    "root": "V",
                    "obj": "O1"
                }
            },
            
            # 第4文型 (SVOO): nsubj -> root(VERB) -> obj + iobj
            "SVOO": {
                "required_relations": ["nsubj", "root", "obj", "iobj"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj": "S",
                    "root": "V",
                    "iobj": "O1",  # 間接目的語が先
                    "obj": "O2"    # 直接目的語が後
                }
            },
            
            # 第5文型 (SVOC): nsubj -> root(VERB) -> obj -> xcomp
            "SVOC": {
                "required_relations": ["nsubj", "root", "obj", "xcomp"],
                "root_pos": ["VERB"],
                "mapping": {
                    "nsubj": "S",
                    "root": "V",
                    "obj": "O1",
                    "xcomp": "C2"
                }
            }
        }
        
    def _load_modifier_mappings(self) -> Dict[str, str]:
        """修飾語マッピングルール"""
        return {
            "advmod": "M2",      # 副詞修飾語・否定辞 → M2
            "amod": "subslot",   # 形容詞修飾語 → サブスロット内処理
            "det": "subslot",    # 限定詞 → サブスロット内処理
            "case": "subslot",   # 前置詞 → サブスロット内処理
            "nmod": "M1",        # 名詞修飾語 → M1 (文脈により変更可能)
            "mark": "subslot",   # 従属節マーカー → サブスロット内処理
            "csubj": "O1",       # 節主語 → O1
        }
    
    def decompose(self, text: str) -> Dict[str, Any]:
        """
        テキストをRephraseスロット構造に分解
        
        Args:
            text: 入力文
            
        Returns:
            Rephraseスロット構造辞書
        """
        print(f"\n🎯 Stanza基本分解開始: '{text}...'")
        
        # Stanza解析
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # ROOT動詞特定
        root_verb = self._find_root_verb(sent)
        if not root_verb:
            print("❌ ROOT動詞が見つかりません")
            return {}
            
        print(f"📌 ROOT: '{root_verb.text}' (POS: {root_verb.upos})")
        
        # 文型パターン識別
        sentence_pattern = self._identify_sentence_pattern(sent, root_verb)
        if not sentence_pattern:
            print("❌ 対応する文型パターンが見つかりません")
            return {}
            
        print(f"🔍 文型パターン: {sentence_pattern}")
        
        # 基本スロット抽出
        basic_slots = self._extract_basic_slots(sent, root_verb, sentence_pattern)
        
        # 修飾語スロット抽出
        modifier_slots = self._extract_modifier_slots(sent, root_verb)
        
        # 統合
        all_slots = {**basic_slots, **modifier_slots}
        
        # サブスロット処理
        result_slots = self._extract_all_subslots(sent, all_slots)
        
        return result_slots
        
    def _find_root_verb(self, sent) -> Optional[Any]:
        """ROOT動詞を特定"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
        
    def _identify_sentence_pattern(self, sent, root_verb) -> Optional[str]:
        """文型パターンを識別"""
        
        # 文中の依存関係を収集
        present_relations = set()
        pos_info = {}
        
        for word in sent.words:
            present_relations.add(word.deprel)
            if word.deprel == 'root':
                pos_info['root'] = word.upos
            elif word.deprel == 'xcomp':
                pos_info['xcomp'] = word.upos
                
        print(f"🔍 検出された関係: {sorted(present_relations)}")
                
        # パターン優先順位付き検査（より具体的なものから）
        pattern_priority = [
            # 特殊構文
            "PASSIVE_AUX", "PASSIVE", "THERE_BE", "WH_BE",
            # 助動詞系
            "S_AUX_V_O", "S_AUX_V",
            # 基本文型
            "SVOO", "SVOC", "SVO", "SVC_LOOKS", "SVC_BE", "SV"
        ]
        
        for pattern_name in pattern_priority:
            if pattern_name not in self.sentence_patterns:
                continue
                
            pattern_config = self.sentence_patterns[pattern_name]
            required_relations = set(pattern_config["required_relations"])
            
            # 必須関係がすべて存在するか
            if not required_relations.issubset(present_relations):
                continue
                
            # ROOTのPOS制約チェック
            if "root_pos" in pattern_config:
                if pos_info.get('root') not in pattern_config["root_pos"]:
                    continue
                    
            # xcompのPOS制約チェック（該当する場合）
            if "xcomp_pos" in pattern_config:
                if pos_info.get('xcomp') not in pattern_config["xcomp_pos"]:
                    continue
                    
            # There構文の特別チェック
            if "expl_check" in pattern_config:
                if 'expl' not in present_relations:
                    continue
                    
            print(f"✅ マッチしたパターン: {pattern_name}")
            return pattern_name
            
        print("❌ マッチするパターンなし")
        return None
        
    def _extract_basic_slots(self, sent, root_verb, pattern_name: str) -> Dict[str, Dict[str, str]]:
        """基本スロット抽出（パターン駆動）"""
        pattern_config = self.sentence_patterns[pattern_name]
        mapping = pattern_config["mapping"]
        
        slots = {}
        
        # 依存関係ごとにスロット抽出
        aux_words = []  # 複数のAuxを統合
        
        for word in sent.words:
            if word.deprel in mapping:
                slot_name = mapping[word.deprel]
                
                # Auxスロットの特別処理（複数のauxを統合）
                if slot_name == "Aux":
                    aux_words.append(word)
                    continue
                
                # スロット境界を取得
                slot_range = self._get_slot_boundary(sent, word, word.deprel)
                slot_text = self._extract_text_range(sent, slot_range)
                
                print(f"📍 {slot_name}検出: '{slot_text}' (deprel: {word.deprel})")
                
                slots[slot_name] = {'main': slot_text}
        
        # 複数のAuxを統合処理
        if aux_words:
            aux_texts = [word.text for word in sorted(aux_words, key=lambda w: w.id)]
            aux_combined = " ".join(aux_texts)
            print(f"📍 Aux検出: '{aux_combined}' (統合: {len(aux_words)}個)")
            slots["Aux"] = {'main': aux_combined}
                
        return slots
        
    def _extract_modifier_slots(self, sent, root_verb) -> Dict[str, Dict[str, str]]:
        """修飾語スロット抽出"""
        modifier_slots = {}
        
        for word in sent.words:
            if word.deprel in self.modifier_mappings:
                slot_mapping = self.modifier_mappings[word.deprel]
                
                if slot_mapping == "subslot":
                    # サブスロット内で処理（ここでは無視）
                    continue
                elif slot_mapping in ["M1", "M2", "M3"]:
                    # 修飾語スロットに配置
                    slot_text = word.text  # 基本的に単語そのもの
                    print(f"📍 {slot_mapping}検出: '{slot_text}' (修飾語: {word.deprel})")
                    modifier_slots[slot_mapping] = {'main': slot_text}
                    
        return modifier_slots
        
    def _get_slot_boundary(self, sent, word, deprel: str) -> Tuple[int, int]:
        """スロット境界を決定（関係タイプに応じて）"""
        
        if deprel in ["cop", "aux", "aux:pass"]:
            # be動詞・助動詞は単語そのもの
            return (word.start_char, word.end_char)
        elif deprel == "root" and word.upos == "VERB":
            # 動詞ROOTは動詞単体のみ
            return (word.start_char, word.end_char)
        elif deprel in ["nsubj", "nsubj:pass", "obj", "iobj"]:
            # 主語・目的語は限定詞・修飾語を含む
            return self._find_noun_phrase_boundary(sent, word)
        elif deprel == "root" and word.upos in ["ADJ", "NOUN", "PRON"]:
            # be動詞構文の補語・疑問詞
            return self._find_complement_boundary(sent, word)
        elif deprel == "xcomp":
            # 補語は修飾語を含む
            return self._find_complement_boundary(sent, word)
        elif deprel == "expl":
            # "There"は単語そのもの
            return (word.start_char, word.end_char)
        elif deprel == "csubj":
            # 節主語は完全な下位ツリー
            return self._find_complete_subtree_range(sent, word)
        else:
            # その他は完全な下位ツリー
            return self._find_complete_subtree_range(sent, word)
            
    def _find_noun_phrase_boundary(self, sent, noun_word) -> Tuple[int, int]:
        """名詞句境界検出（限定詞・形容詞修飾語を含む）"""
        min_idx = noun_word.id
        max_idx = noun_word.id
        
        # 修飾要素を収集
        for word in sent.words:
            if word.head == noun_word.id and word.deprel in ['det', 'amod', 'compound']:
                min_idx = min(min_idx, word.id)
                max_idx = max(max_idx, word.id)
                
        # 文字位置に変換
        start_char = sent.words[min_idx-1].start_char
        end_char = sent.words[max_idx-1].end_char
        return (start_char, end_char)
        
    def _find_complement_boundary(self, sent, comp_word) -> Tuple[int, int]:
        """補語境界検出（be動詞構文用）"""
        complement_words = {comp_word.id}
        
        # 補語の修飾語を収集（主語・be動詞は除外）
        for word in sent.words:
            if word.head == comp_word.id and word.deprel in ['det', 'amod', 'case']:
                complement_words.add(word.id)
                # 下位ツリーも追加
                descendants = self._collect_descendants(sent, word)
                complement_words.update(descendants)
                
        # 句読点を除外
        complement_words = {word_id for word_id in complement_words 
                          if sent.words[word_id-1].upos != 'PUNCT'}
        
        if not complement_words:
            return (comp_word.start_char, comp_word.end_char)
            
        min_idx = min(complement_words)
        max_idx = max(complement_words)
        
        start_char = sent.words[min_idx-1].start_char
        end_char = sent.words[max_idx-1].end_char
        return (start_char, end_char)
        
    def _collect_descendants(self, sent, root_word) -> set:
        """単語の下位ツリーのIDを収集"""
        descendants = set()
        for word in sent.words:
            if word.head == root_word.id:
                descendants.add(word.id)
                descendants.update(self._collect_descendants(sent, word))
        return descendants
        
    def _find_complete_subtree_range(self, sent, word) -> Tuple[int, int]:
        """完全な下位ツリーの範囲を取得"""
        subtree_ids = {word.id}
        subtree_ids.update(self._collect_descendants(sent, word))
        
        # 句読点を除外
        subtree_ids = {word_id for word_id in subtree_ids 
                      if sent.words[word_id-1].upos != 'PUNCT'}
        
        if not subtree_ids:
            return (word.start_char, word.end_char)
            
        min_idx = min(subtree_ids)
        max_idx = max(subtree_ids)
        
        start_char = sent.words[min_idx-1].start_char
        end_char = sent.words[max_idx-1].end_char
        return (start_char, end_char)
        
    def _extract_text_range(self, sent, char_range: Tuple[int, int]) -> str:
        """文字範囲からテキストを抽出"""
        full_text = sent.text
        start_char, end_char = char_range
        return full_text[start_char:end_char].strip()
        
    def _extract_all_subslots(self, sent, slots: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
        """全スロットに対してサブスロット処理を実行"""
        result = {}
        
        for slot_name, slot_data in slots.items():
            if 'main' in slot_data and slot_data['main']:
                # 現在はmainのみをコピー（サブスロット処理は将来実装）
                result[slot_name] = {'main': slot_data['main']}
            else:
                result[slot_name] = slot_data
                
        return result
