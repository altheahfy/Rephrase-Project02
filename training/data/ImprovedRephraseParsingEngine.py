#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rephrase Parsing Engine v2.0 - 改良版
spaCy学術的分解 → Rephraseルール適用の段階的アプローチ
"""

import spacy
import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple

# spaCy初期化
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
    print("✅ spaCy語彙認識エンジン初期化完了")
except (OSError, ImportError) as e:
    nlp = None
    SPACY_AVAILABLE = False
    print(f"⚠️ spaCy初期化失敗: {e}")

class ImprovedRephraseParsingEngine:
    """改良版Rephrase品詞分解エンジン - spaCy + Rephraseルール統合"""
    
    def __init__(self):
        self.engine_name = "Improved Rephrase Parsing Engine v2.0"
        self.rules_data = self.load_rules()
        self.nlp = nlp if SPACY_AVAILABLE else None
        
        # Rephraseスロット定義
        self.slot_priorities = {
            'S': 1, 'Aux': 2, 'V': 3, 'O1': 4, 'O2': 5,
            'C1': 6, 'C2': 7, 'M1': 8, 'M2': 9, 'M3': 10
        }
        
    def load_rules(self):
        """Rephraseルールデータを読み込み"""
        rules_file = os.path.join(os.path.dirname(__file__), 'rephrase_rules_v1.0.json')
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: {rules_file} が見つかりません")
            return {}
    
    def analyze_sentence(self, sentence: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        段階的句分解: spaCy学術分析 → Rephraseルール適用
        
        Args:
            sentence: 分解対象の英文
            
        Returns:
            Rephraseスロット形式の分解結果
        """
        if not self.nlp:
            return {"error": "spaCy not available"}
            
        try:
            # ステップ1: spaCy学術的構文解析
            doc = self.nlp(sentence)
            academic_analysis = self._extract_academic_structure(doc)
            
            # ステップ2: 文構造の階層理解
            sentence_structure = self._identify_sentence_structure(doc, academic_analysis)
            
            # ステップ3: Rephraseルール適用
            rephrase_slots = self._apply_rephrase_rules(doc, sentence_structure)
            
            # ステップ4: 網羅性確保（全要素をスロットに配置）
            complete_slots = self._ensure_complete_coverage(doc, rephrase_slots)
            
            return complete_slots
            
        except Exception as e:
            print(f"パーシングエラー: {e}")
            return {"error": str(e)}
    
    def _extract_academic_structure(self, doc) -> Dict[str, Any]:
        """spaCyによる学術的構文解析の抽出"""
        structure = {
            'root_verb': None,
            'subjects': [],
            'objects': [],
            'modifiers': [],
            'clauses': [],
            'dependencies': []
        }
        
        for token in doc:
            # 主動詞（ROOT）の特定
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                structure['root_verb'] = token
                
            # 主語の特定
            elif token.dep_ in ["nsubj", "nsubjpass"]:
                # 主語の完全なフレーズを取得
                subject_phrase = self._get_noun_phrase(token)
                structure['subjects'].append({
                    'token': token,
                    'phrase': subject_phrase,
                    'head': token.head
                })
                
            # 目的語の特定
            elif token.dep_ in ["dobj", "iobj", "pobj", "dative"]:
                object_phrase = self._get_noun_phrase(token)
                structure['objects'].append({
                    'token': token,
                    'phrase': object_phrase,
                    'type': token.dep_,
                    'head': token.head
                })
                
            # 修飾語の特定
            elif token.dep_ in ["advmod", "amod", "npadvmod", "prep"]:
                structure['modifiers'].append({
                    'token': token,
                    'type': token.dep_,
                    'head': token.head
                })
                
            # 依存関係の記録
            structure['dependencies'].append({
                'token': token,
                'dep': token.dep_,
                'head': token.head,
                'pos': token.pos_
            })
        
        return structure
    
    def _identify_sentence_structure(self, doc, academic_analysis) -> Dict[str, Any]:
        """文構造の階層理解（主節・従属節・関係詞節の判別）"""
        
        structure = {
            'main_clause': {
                'verb': academic_analysis['root_verb'],
                'subject': None,
                'objects': [],
                'modifiers': []
            },
            'subordinate_clauses': [],
            'relative_clauses': [],
            'temporal_modifiers': [],
            'sentence_type': 'declarative'  # declarative, interrogative, imperative
        }
        
        # 主節の要素を特定
        root_verb = academic_analysis['root_verb']
        if root_verb:
            # 主節に直接依存する主語を特定
            for subj in academic_analysis['subjects']:
                if subj['head'] == root_verb:
                    structure['main_clause']['subject'] = subj
                    break
                    
            # 主節に直接依存する目的語を特定
            for obj in academic_analysis['objects']:
                if obj['head'] == root_verb:
                    structure['main_clause']['objects'].append(obj)
        
        # 従属節の特定（advcl, relcl等）
        for token in doc:
            if token.dep_ == "advcl":  # 副詞節
                structure['subordinate_clauses'].append({
                    'verb': token,
                    'type': 'adverbial',
                    'marker': self._find_subordinating_conjunction(token)
                })
            elif token.dep_ == "relcl":  # 関係詞節
                structure['relative_clauses'].append({
                    'verb': token,
                    'modified_noun': token.head
                })
        
        # 時間修飾語の特定
        structure['temporal_modifiers'] = self._extract_temporal_modifiers(doc)
        
        return structure
    
    def _apply_rephrase_rules(self, doc, sentence_structure) -> Dict[str, List[Dict[str, Any]]]:
        """Rephraseルールに基づくスロット割り当て"""
        
        slots = {slot: [] for slot in self.slot_priorities.keys()}
        
        main_clause = sentence_structure['main_clause']
        
        # S (主語) スロットの割り当て
        if main_clause['subject']:
            slots['S'].append({
                'value': main_clause['subject']['phrase'],
                'type': 'subject',
                'rule_id': 'improved-main-subject'
            })
        
        # V (動詞) スロットの割り当て
        if main_clause['verb']:
            slots['V'].append({
                'value': main_clause['verb'].text,
                'type': 'main_verb', 
                'rule_id': 'improved-main-verb'
            })
            
            # 助動詞の特定
            aux_tokens = []
            for child in main_clause['verb'].children:
                if child.dep_ == "aux" or child.pos_ == "AUX":
                    aux_tokens.append(child)
            
            if aux_tokens:
                aux_phrase = " ".join([token.text for token in sorted(aux_tokens, key=lambda t: t.i)])
                slots['Aux'].append({
                    'value': aux_phrase,
                    'type': 'auxiliary',
                    'rule_id': 'improved-auxiliary'
                })
        
        # O1, O2 (目的語) スロットの割り当て
        direct_objects = [obj for obj in main_clause['objects'] if obj['type'] in ['dobj']]
        indirect_objects = [obj for obj in main_clause['objects'] if obj['type'] in ['iobj', 'dative']]
        
        if direct_objects:
            slots['O1'].append({
                'value': direct_objects[0]['phrase'],
                'type': 'direct_object',
                'rule_id': 'improved-direct-object'
            })
            
        if indirect_objects:
            slots['O2'].append({
                'value': indirect_objects[0]['phrase'],
                'type': 'indirect_object',
                'rule_id': 'improved-indirect-object'
            })
        elif len(direct_objects) > 1:  # SVOO構造
            slots['O2'].append({
                'value': direct_objects[1]['phrase'],
                'type': 'second_object',
                'rule_id': 'improved-second-object'
            })
        
        # M1, M2, M3 (修飾語) スロットの割り当て - Rephraseルール適用
        self._assign_modifiers_by_rephrase_rules(doc, sentence_structure, slots)
        
        return slots
    
    def _assign_modifiers_by_rephrase_rules(self, doc, sentence_structure, slots):
        """Rephraseルールに基づく修飾語の分類"""
        
        # 時間修飾語 → M3
        for temporal_mod in sentence_structure['temporal_modifiers']:
            slots['M3'].append({
                'value': temporal_mod['phrase'],
                'type': 'temporal_modifier',
                'rule_id': 'improved-temporal'
            })
        
        # 前置詞句の分類
        prep_phrases = self._extract_prepositional_phrases(doc)
        
        for prep_phrase in prep_phrases:
            prep = prep_phrase['preposition'].lower()
            
            # Rephraseルールに基づく分類
            if prep in ['at', 'in', 'on', 'during'] and self._is_temporal_context(prep_phrase):
                # 時間表現 → M3
                slots['M3'].append({
                    'value': prep_phrase['phrase'],
                    'type': 'temporal_prep',
                    'rule_id': 'improved-temporal-prep'
                })
            elif prep in ['to', 'for', 'with', 'by'] and self._is_manner_context(prep_phrase):
                # 方法・手段 → M2
                slots['M2'].append({
                    'value': prep_phrase['phrase'],
                    'type': 'manner_prep',
                    'rule_id': 'improved-manner-prep'
                })
            else:
                # その他 → M1
                slots['M1'].append({
                    'value': prep_phrase['phrase'],
                    'type': 'other_prep',
                    'rule_id': 'improved-other-prep'
                })
    
    def _ensure_complete_coverage(self, doc, slots) -> Dict[str, List[Dict[str, Any]]]:
        """全要素がスロットに配置されることを確保（Rephraseの網羅性要件）"""
        
        assigned_tokens = set()
        
        # 既に割り当てられたトークンを記録
        for slot_list in slots.values():
            for item in slot_list:
                # トークンのインデックスを記録（簡略化のため、valueに基づく）
                pass  # 実装の詳細は省略
        
        # 未割り当てのトークンをM1に配置
        for token in doc:
            if (token.pos_ not in ['PUNCT', 'SPACE'] and 
                token.dep_ not in ['det', 'case'] and  # 冠詞・格変化は除外
                token.i not in assigned_tokens):
                
                # 適切なスロットが見つからない場合はM1に配置
                slots['M1'].append({
                    'value': token.text,
                    'type': 'unassigned_coverage',
                    'rule_id': 'coverage-fallback'
                })
        
        return slots
    
    def _get_noun_phrase(self, token) -> str:
        """名詞句の完全な形を取得"""
        # 左の修飾語を収集
        left_tokens = []
        for child in token.children:
            if child.i < token.i and child.dep_ in ['det', 'amod', 'compound', 'nmod']:
                left_tokens.append(child)
        
        # 右の修飾語を収集
        right_tokens = []
        for child in token.children:
            if child.i > token.i and child.dep_ in ['prep', 'relcl']:
                # 前置詞句や関係詞節は含める場合と含めない場合がある
                pass
        
        # トークンを順序通りに並べて結合
        all_tokens = sorted(left_tokens + [token] + right_tokens, key=lambda t: t.i)
        return " ".join([t.text for t in all_tokens])
    
    def _extract_temporal_modifiers(self, doc) -> List[Dict[str, Any]]:
        """時間修飾語の抽出"""
        temporal_modifiers = []
        
        for token in doc:
            # npadvmod で時間を表すもの
            if token.dep_ == "npadvmod" and self._is_temporal_word(token.text):
                phrase = self._get_noun_phrase(token)
                temporal_modifiers.append({
                    'token': token,
                    'phrase': phrase,
                    'type': 'npadvmod_temporal'
                })
        
        # 時間を表すNER
        for ent in doc.ents:
            if ent.label_ in ['TIME', 'DATE']:
                temporal_modifiers.append({
                    'phrase': ent.text,
                    'type': 'named_entity_temporal'
                })
        
        return temporal_modifiers
    
    def _extract_prepositional_phrases(self, doc) -> List[Dict[str, Any]]:
        """前置詞句の抽出"""
        prep_phrases = []
        
        for token in doc:
            if token.pos_ == "ADP":  # 前置詞
                # 前置詞に依存する名詞を探す
                pobj = None
                for child in token.children:
                    if child.dep_ == "pobj":
                        pobj = child
                        break
                
                if pobj:
                    phrase = f"{token.text} {self._get_noun_phrase(pobj)}"
                    prep_phrases.append({
                        'preposition': token.text,
                        'object': pobj,
                        'phrase': phrase,
                        'token': token
                    })
        
        return prep_phrases
    
    def _is_temporal_word(self, word: str) -> bool:
        """単語が時間表現かどうか判定"""
        temporal_words = [
            'morning', 'afternoon', 'evening', 'night', 'today', 'yesterday', 'tomorrow',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
        return word.lower() in temporal_words
    
    def _is_temporal_context(self, prep_phrase: Dict[str, Any]) -> bool:
        """前置詞句が時間文脈かどうか判定"""
        obj_text = prep_phrase['object'].text.lower()
        return self._is_temporal_word(obj_text)
    
    def _is_manner_context(self, prep_phrase: Dict[str, Any]) -> bool:
        """前置詞句が方法・手段の文脈かどうか判定"""
        prep = prep_phrase['preposition'].lower()
        return prep in ['with', 'by'] and not self._is_temporal_context(prep_phrase)
    
    def _find_subordinating_conjunction(self, verb_token) -> Optional[str]:
        """従属接続詞を探す"""
        for child in verb_token.children:
            if child.dep_ == "mark":
                return child.text
        return None
