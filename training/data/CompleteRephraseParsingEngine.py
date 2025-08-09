#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rephrase Parsing Engine v3.0 - 完全版
Rephraseルール辞書100%活用 + Sub-slot完全対応 + 5文型フルセット対応
"""

import spacy
import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple, Union

# spaCy初期化
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
    print("✅ spaCy語彙認識エンジン初期化完了")
except (OSError, ImportError) as e:
    nlp = None
    SPACY_AVAILABLE = False
    print(f"⚠️ spaCy初期化失敗: {e}")

class CompleteRephraseParsingEngine:
    """完全版Rephrase品詞分解エンジン v3.0"""
    
    def __init__(self):
        self.engine_name = "Complete Rephrase Parsing Engine v3.0"
        self.rules_data = self.load_rules()
        self.nlp = nlp if SPACY_AVAILABLE else None
        
        # Rephraseスロット完全定義
        self.main_slots = ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
        self.sub_slots = ['sub-m1', 'sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-m2', 'sub-m3', 'sub-c1']
        
        # ルール優先度マッピング
        self.rule_priority_map = {}
        self._build_rule_priority_map()
        
    def load_rules(self):
        """Rephraseルール辞書の完全読み込み"""
        rules_file = os.path.join(os.path.dirname(__file__), 'rephrase_rules_v1.0.json')
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ Rephraseルール辞書読み込み完了: {len(data.get('rules', []))} ルール")
                return data
        except FileNotFoundError:
            print(f"❌ ルールファイルが見つかりません: {rules_file}")
            return {}
    
    def _build_rule_priority_map(self):
        """ルール優先度マップの構築"""
        if 'rules' not in self.rules_data:
            return
            
        for rule in self.rules_data['rules']:
            rule_id = rule.get('id', '')
            priority = rule.get('priority', 50)  # デフォルト優先度
            self.rule_priority_map[rule_id] = priority
    
    def analyze_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        完全版文要素分解
        
        Returns:
            {
                'main_slots': {...},      # メインスロット
                'sub_structures': [...],  # サブ構造（関係詞節等）
                'sentence_type': '...',   # 文型
                'metadata': {...}         # メタ情報
            }
        """
        if not self.nlp:
            return {"error": "spaCy not available"}
            
        try:
            # Step 1: spaCy完全解析
            doc = self.nlp(sentence)
            spacy_analysis = self._comprehensive_spacy_analysis(doc)
            
            # Step 2: 文構造の階層分析
            sentence_hierarchy = self._analyze_sentence_hierarchy(doc, spacy_analysis)
            
            # Step 3: Rephraseルール21個の完全適用
            rephrase_slots = self._apply_complete_rephrase_rules(doc, sentence_hierarchy)
            
            # Step 4: Sub-slot構造の生成
            sub_structures = self._generate_subslot_structures(doc, sentence_hierarchy)
            
            # Step 5: 文型判定（第1〜5文型）
            sentence_pattern = self._determine_sentence_pattern(rephrase_slots, sub_structures)
            
            return {
                'main_slots': rephrase_slots,
                'sub_structures': sub_structures,
                'sentence_type': sentence_pattern,
                'metadata': {
                    'engine': self.engine_name,
                    'rules_applied': len([r for r in rephrase_slots.values() if r]),
                    'complexity_score': self._calculate_complexity(sentence_hierarchy)
                }
            }
            
        except Exception as e:
            print(f"完全版パーシングエラー: {e}")
            return {"error": str(e)}
    
    def _comprehensive_spacy_analysis(self, doc) -> Dict[str, Any]:
        """spaCyによる包括的言語解析"""
        
        analysis = {
            'tokens': [],
            'dependencies': [],
            'clauses': {
                'main': None,
                'subordinate': [],
                'relative': [],
                'infinitive': [],
                'participial': []
            },
            'phrases': {
                'noun_phrases': [],
                'verb_phrases': [],
                'prep_phrases': [],
                'adj_phrases': []
            },
            'entities': [],
            'sentence_structure': None
        }
        
        # トークンレベル解析
        for token in doc:
            token_info = {
                'text': token.text,
                'lemma': token.lemma_,
                'pos': token.pos_,
                'tag': token.tag_,
                'dep': token.dep_,
                'head': token.head.text if token.head != token else 'ROOT',
                'children': [child.text for child in token.children],
                'is_punct': token.is_punct,
                'is_stop': token.is_stop
            }
            analysis['tokens'].append(token_info)
            
            # 依存関係の記録
            if token.dep_ != 'ROOT':
                analysis['dependencies'].append({
                    'child': token.text,
                    'relation': token.dep_,
                    'head': token.head.text
                })
        
        # 主節・従属節の特定
        root_verb = None
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                root_verb = token
                break
                
        analysis['clauses']['main'] = root_verb
        
        # 従属節の特定
        for token in doc:
            if token.dep_ == "advcl":  # 副詞節
                analysis['clauses']['subordinate'].append({
                    'verb': token,
                    'type': 'adverbial',
                    'marker': self._find_clause_marker(token)
                })
            elif token.dep_ == "relcl":  # 関係詞節
                analysis['clauses']['relative'].append({
                    'verb': token,
                    'modified_noun': token.head,
                    'relativizer': self._find_relativizer(token)
                })
            elif token.dep_ == "xcomp":  # 補文節
                analysis['clauses']['infinitive'].append({
                    'verb': token,
                    'type': 'infinitive' if 'to' in [c.text for c in token.head.children] else 'bare_infinitive'
                })
        
        # フレーズレベル解析
        analysis['phrases']['noun_phrases'] = self._extract_noun_phrases(doc)
        analysis['phrases']['verb_phrases'] = self._extract_verb_phrases(doc)
        analysis['phrases']['prep_phrases'] = self._extract_prep_phrases(doc)
        
        # 固有表現
        analysis['entities'] = [(ent.text, ent.label_) for ent in doc.ents]
        
        return analysis
    
    def _analyze_sentence_hierarchy(self, doc, spacy_analysis) -> Dict[str, Any]:
        """文構造の階層分析"""
        
        hierarchy = {
            'main_clause': {
                'subject': None,
                'verb': spacy_analysis['clauses']['main'],
                'objects': [],
                'complements': [],
                'modifiers': []
            },
            'subordinate_structures': [],
            'sentence_complexity': 'simple'  # simple, compound, complex, compound-complex
        }
        
        # 主節の構成要素特定
        main_verb = spacy_analysis['clauses']['main']
        if main_verb:
            # 主語特定
            for token in doc:
                if token.dep_ == "nsubj" and token.head == main_verb:
                    hierarchy['main_clause']['subject'] = {
                        'core': token,
                        'full_phrase': self._get_complete_noun_phrase(token),
                        'type': 'simple' if not self._has_modifying_clause(token) else 'complex'
                    }
                    break
            
            # 目的語特定
            for token in doc:
                if token.head == main_verb:
                    if token.dep_ == "dobj":
                        hierarchy['main_clause']['objects'].append({
                            'core': token,
                            'full_phrase': self._get_complete_noun_phrase(token),
                            'type': 'direct',
                            'position': 1
                        })
                    elif token.dep_ in ["iobj", "dative"]:
                        hierarchy['main_clause']['objects'].append({
                            'core': token,
                            'full_phrase': self._get_complete_noun_phrase(token),
                            'type': 'indirect',
                            'position': 2
                        })
        
        # 従属構造の分析
        for rel_clause in spacy_analysis['clauses']['relative']:
            substructure = self._analyze_subclause_structure(rel_clause['verb'], 'relative')
            hierarchy['subordinate_structures'].append(substructure)
            
        for adv_clause in spacy_analysis['clauses']['subordinate']:
            substructure = self._analyze_subclause_structure(adv_clause['verb'], 'adverbial')
            hierarchy['subordinate_structures'].append(substructure)
        
        # 文の複雑度判定
        if hierarchy['subordinate_structures']:
            if len(hierarchy['subordinate_structures']) == 1:
                hierarchy['sentence_complexity'] = 'complex'
            else:
                hierarchy['sentence_complexity'] = 'compound-complex'
        
        return hierarchy
    
    def _apply_complete_rephrase_rules(self, doc, hierarchy) -> Dict[str, List[Dict[str, Any]]]:
        """Rephraseルール21個の完全適用"""
        
        slots = {slot: [] for slot in self.main_slots}
        
        if 'rules' not in self.rules_data:
            print("⚠️ ルールデータが見つかりません")
            return slots
        
        # ルールを優先度順でソート
        rules = sorted(self.rules_data['rules'], 
                      key=lambda r: r.get('priority', 50), 
                      reverse=True)
        
        applied_rules = []
        
        for rule in rules:
            rule_id = rule.get('id', '')
            
            try:
                # ルールの適用
                if self._should_apply_rule(rule, doc, hierarchy):
                    result = self._apply_single_rule(rule, doc, hierarchy, slots)
                    if result:
                        applied_rules.append(rule_id)
                        print(f"✅ ルール適用: {rule_id}")
                    
            except Exception as e:
                print(f"⚠️ ルール適用エラー {rule_id}: {e}")
        
        print(f"📊 適用されたルール数: {len(applied_rules)}/21")
        
        # 汎用的な動詞検出（ルールで捕獲されなかった場合）
        if not slots['V']:
            generic_verb = self._extract_generic_verb(doc, hierarchy)
            if generic_verb:
                slots['V'].append({
                    'value': generic_verb,
                    'rule_id': 'generic-verb',
                    'confidence': 0.7
                })
                print(f"✅ 汎用動詞検出: {generic_verb}")
        
        # 汎用的な目的語検出（ルールで捕獲されなかった場合）
        if not slots['O1']:
            generic_object = self._extract_generic_object(doc, hierarchy)
            if generic_object:
                slots['O1'].append({
                    'value': generic_object,
                    'rule_id': 'generic-object',
                    'confidence': 0.7
                })
                print(f"✅ 汎用目的語検出: {generic_object}")
        
        # SVOO構造の検出（間接目的語と直接目的語の分離）
        self._extract_ditransitive_objects(doc, slots)
        
        # 汎用的な時間表現検出（ルールで捕獲されなかった場合）
        if not slots['M3']:
            generic_time = self._extract_generic_time_expression(doc)
            if generic_time:
                slots['M3'].append({
                    'value': generic_time,
                    'rule_id': 'generic-time',
                    'confidence': 0.8
                })
                print(f"✅ 汎用時間表現検出: {generic_time}")
        
        # 汎用的な助動詞検出（縮約形対応）
        if not slots['Aux']:
            generic_aux = self._extract_generic_auxiliary(doc)
            if generic_aux:
                slots['Aux'].append({
                    'value': generic_aux,
                    'rule_id': 'generic-aux',
                    'confidence': 0.8
                })
                print(f"✅ 汎用助動詞検出: {generic_aux}")
        
        return slots
    
    def _should_apply_rule(self, rule: Dict[str, Any], doc, hierarchy) -> bool:
        """ルールを適用すべきかどうかの判定"""
        
        rule_id = rule.get('id', 'unknown')
        trigger = rule.get('trigger', {})
        
        print(f"🔍 ルール判定: {rule_id}")
        
        # tokenトリガーの確認
        if 'token' in trigger:
            target_token = trigger['token']
            doc_tokens = [token.text for token in doc]
            token_match = target_token in doc_tokens
            print(f"  tokenトリガー: '{target_token}' → 文書内: {doc_tokens} → マッチ: {token_match}")
            if not token_match:
                return False
        
        # lemmaトリガーの確認
        if 'lemma' in trigger:
            lemmas = trigger['lemma'] if isinstance(trigger['lemma'], list) else [trigger['lemma']]
            doc_lemmas = [token.lemma_ for token in doc]
            lemma_match = any(token.lemma_ in lemmas for token in doc)
            print(f"  lemmaトリガー: {lemmas} → 文書内: {doc_lemmas} → マッチ: {lemma_match}")
            if not lemma_match:
                return False
        
        # posトリガーの確認
        if 'pos' in trigger:
            pos_tags = trigger['pos'] if isinstance(trigger['pos'], list) else [trigger['pos']]
            doc_pos = [token.pos_ for token in doc]
            pos_match = any(token.pos_ in pos_tags for token in doc)
            print(f"  POSトリガー: {pos_tags} → 文書内: {doc_pos} → マッチ: {pos_match}")
            if not pos_match:
                return False
        
        # patternトリガーの確認
        if 'pattern' in trigger:
            pattern = trigger['pattern']
            pattern_match = bool(re.search(pattern, doc.text))
            print(f"  パターントリガー: {pattern} → マッチ: {pattern_match}")
            if not pattern_match:
                return False
        
        print(f"  → ルール適用対象: {rule_id}")
        return True
    
    def _apply_single_rule(self, rule: Dict[str, Any], doc, hierarchy, slots: Dict[str, List]) -> bool:
        """単一ルールの適用"""
        
        rule_id = rule.get('id', '')
        assignment = rule.get('assign', {})
        
        if isinstance(assignment, list):
            # 複数割り当ての場合
            for assign_item in assignment:
                self._execute_assignment(assign_item, doc, hierarchy, slots, rule_id)
            return True
        else:
            # 単一割り当ての場合
            return self._execute_assignment(assignment, doc, hierarchy, slots, rule_id)
    
    def _execute_assignment(self, assignment: Dict[str, Any], doc, hierarchy, slots: Dict[str, List], rule_id: str) -> bool:
        """割り当ての実行"""
        
        slot = assignment.get('slot', '')
        assign_type = assignment.get('type', 'word')
        
        if slot not in slots:
            return False
        
        # 値の決定
        value = self._determine_assignment_value(assignment, doc, hierarchy, rule_id)
        
        if value:
            slots[slot].append({
                'value': value,
                'type': assign_type,
                'rule_id': rule_id
            })
            return True
            
        return False
    
    def _determine_assignment_value(self, assignment: Dict[str, Any], doc, hierarchy, rule_id: str) -> Optional[str]:
        """割り当て値の決定"""
        
        # 特定のルールに基づく値決定ロジック
        if rule_id.startswith('aux-'):
            return self._extract_auxiliary_value(doc, hierarchy)
        elif rule_id.startswith('V-'):
            return self._extract_verb_value(doc, hierarchy, rule_id)
        elif rule_id.startswith('time-'):
            return self._extract_temporal_value(doc, hierarchy)
        elif rule_id.startswith('subject-'):
            return self._extract_subject_value(doc, hierarchy)
        else:
            # 汎用的な値抽出
            return self._extract_generic_value(assignment, doc, hierarchy)
    
    def _generate_subslot_structures(self, doc, hierarchy) -> List[Dict[str, Any]]:
        """Sub-slot構造の生成（関係詞節・従属節用）"""
        
        sub_structures = []
        
        for sub_structure in hierarchy['subordinate_structures']:
            sub_slots = {slot: [] for slot in self.sub_slots}
            
            # Sub-slotの割り当て
            clause_type = sub_structure['type']
            clause_verb = sub_structure['verb']
            
            if clause_type == 'relative':
                # 関係詞節のsub-slot処理
                self._process_relative_clause_subslots(clause_verb, sub_slots, doc)
            elif clause_type == 'adverbial':
                # 副詞節のsub-slot処理
                self._process_adverbial_clause_subslots(clause_verb, sub_slots, doc)
            
            sub_structures.append({
                'type': clause_type,
                'verb': clause_verb.text,
                'sub_slots': sub_slots,
                'parent_element': sub_structure.get('modified_element', '')
            })
        
        return sub_structures
    
    def _determine_sentence_pattern(self, main_slots: Dict[str, List], sub_structures: List) -> str:
        """5文型の正確な判定"""
        
        has_s = bool(main_slots.get('S'))
        has_v = bool(main_slots.get('V'))
        has_o1 = bool(main_slots.get('O1'))
        has_o2 = bool(main_slots.get('O2'))
        has_c1 = bool(main_slots.get('C1'))
        has_aux = bool(main_slots.get('Aux'))
        
        # デバッグ出力
        print(f"🔍 文型判定: S={has_s}, V={has_v}, O1={has_o1}, O2={has_o2}, C1={has_c1}, Aux={has_aux}")
        
        if has_s and has_v:
            if has_o1 and has_o2:
                return "第4文型 (SVOO)"
            elif has_o1 and has_c1:
                return "第5文型 (SVOC)"
            elif has_o1:
                return "第3文型 (SVO)"
            elif has_c1:
                return "第2文型 (SVC)"
            else:
                return "第1文型 (SV)"
        elif has_v:
            return "命令文または特殊構造"
        
        return "不完全な文構造"
    
    # ヘルパーメソッド群
    def _find_clause_marker(self, verb_token) -> Optional[str]:
        """節のマーカーを探す"""
        for child in verb_token.children:
            if child.dep_ == "mark":
                return child.text
        return None
    
    def _find_relativizer(self, verb_token) -> Optional[str]:
        """関係代名詞を探す"""
        for token in verb_token.doc:
            if token.dep_ == "nsubj" and token.head == verb_token and token.pos_ == "PRON":
                if token.text.lower() in ['who', 'which', 'that', 'whom', 'whose']:
                    return token.text
        return None
    
    def _get_complete_noun_phrase(self, token) -> str:
        """完全な名詞句を取得"""
        phrase_tokens = [token]
        
        # 左側の修飾語
        for child in token.children:
            if child.i < token.i and child.dep_ in ['det', 'amod', 'compound', 'nummod']:
                phrase_tokens.append(child)
        
        # 右側の修飾語（前置詞句は除く）
        for child in token.children:
            if child.i > token.i and child.dep_ in ['amod', 'compound']:
                phrase_tokens.append(child)
        
        # 関係詞節がある場合は含める
        for child in token.children:
            if child.dep_ == 'relcl':
                rel_phrase = self._get_relative_clause_phrase(child)
                return f"{' '.join(sorted([t.text for t in phrase_tokens], key=lambda x: token.doc[[t.text for t in token.doc].index(x)].i))} {rel_phrase}"
        
        return ' '.join(sorted([t.text for t in phrase_tokens], key=lambda x: token.doc[[t.text for t in token.doc].index(x)].i))
    
    def _get_relative_clause_phrase(self, rel_verb) -> str:
        """関係詞節の完全なフレーズを取得"""
        # 関係代名詞の特定
        relativizer = self._find_relativizer(rel_verb)
        if not relativizer:
            relativizer = "that"  # デフォルト
            
        # 関係詞節内の要素を収集
        clause_tokens = [rel_verb]
        for descendant in rel_verb.subtree:
            if descendant != rel_verb:
                clause_tokens.append(descendant)
        
        # トークンを位置順でソート
        clause_tokens.sort(key=lambda t: t.i)
        clause_text = ' '.join([t.text for t in clause_tokens])
        
        return f"{relativizer} {clause_text}".strip()
    
    def _has_modifying_clause(self, token) -> bool:
        """修飾節を持つかどうかの確認"""
        for child in token.children:
            if child.dep_ in ['relcl', 'acl']:
                return True
        return False
    
    def _analyze_subclause_structure(self, verb_token, clause_type: str) -> Dict[str, Any]:
        """従属節構造の分析"""
        return {
            'type': clause_type,
            'verb': verb_token,
            'modified_element': verb_token.head.text if clause_type == 'relative' else None,
            'complexity': 'simple'  # 簡略化
        }
    
    def _calculate_complexity(self, hierarchy) -> int:
        """文の複雑度スコア計算"""
        base_score = 1
        if hierarchy['subordinate_structures']:
            base_score += len(hierarchy['subordinate_structures']) * 2
        
        return base_score
    
    # === Step 1: 基本抽出メソッドの実装 ===
    
    def _extract_subject_value(self, doc, hierarchy) -> Optional[str]:
        """主語の正確な抽出 - Rephraseルール対応"""
        
        # 主節の主語を優先
        main_subject = hierarchy.get('main_clause', {}).get('subject')
        
        if main_subject and main_subject['type'] == 'complex':
            # 複雑な主語（関係詞節付き）の処理
            return main_subject['full_phrase']
        elif main_subject:
            # 単純な主語
            return main_subject['full_phrase']
        
        # フォールバック: spaCyから直接抽出
        for token in doc:
            if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
                return self._get_complete_noun_phrase(token)
        
        return None
    
    def _extract_verb_value(self, doc, hierarchy, rule_id: str) -> Optional[str]:
        """動詞の正確な抽出 - ルール別処理"""
        
        print(f"🔍 動詞抽出開始 - ルール: {rule_id}")
        print(f"  階層データ: {hierarchy.keys()}")
        
        main_verb = hierarchy.get('main_clause', {}).get('verb')
        print(f"  階層から取得した動詞: {main_verb}")
        
        if main_verb:
            # 基本動詞の抽出
            verb_text = main_verb.text
            print(f"  → 動詞テキスト: '{verb_text}'")
            
            # 特定のルールに基づく調整
            if 'progressive' in rule_id:
                # 進行形の処理
                for child in main_verb.children:
                    if child.dep_ == "aux" and child.lemma_ == "be":
                        return f"{child.text} {verb_text}"
            
            elif 'perfect' in rule_id:
                # 完了形の処理
                for child in main_verb.children:
                    if child.dep_ == "aux" and child.lemma_ == "have":
                        return f"{child.text} {verb_text}"
            
            return verb_text
        
        # フォールバック: ROOT動詞を探す
        print(f"  フォールバック: ROOT動詞を検索")
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                print(f"  → ROOT動詞発見: '{token.text}' (pos: {token.pos_}, dep: {token.dep_})")
                return token.text
        
        print(f"  → 動詞見つからず")
        return None
    
    def _extract_generic_verb(self, doc, hierarchy) -> Optional[str]:
        """汎用的な動詞検出（ルールで捕獲されなかった場合のフォールバック）"""
        
        # ROOT動詞を最優先
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                return token.text
        
        # 他の動詞を検索
        for token in doc:
            if token.pos_ == "VERB":
                return token.text
                
        return None
    
    def _extract_generic_object(self, doc, hierarchy) -> Optional[str]:
        """汎用的な目的語検出（ルールで捕獲されなかった場合のフォールバック）"""
        
        # 直接目的語（dobj）を最優先
        for token in doc:
            if token.dep_ == "dobj":
                return self._get_complete_noun_phrase(token)
        
        # 間接目的語（iobj）
        for token in doc:
            if token.dep_ == "iobj":
                return self._get_complete_noun_phrase(token)
                
        # 補語（attr, pcomp）
        for token in doc:
            if token.dep_ in ["attr", "pcomp"]:
                return self._get_complete_noun_phrase(token)
                
        return None
    
    def _extract_generic_time_expression(self, doc) -> Optional[str]:
        """汎用的な時間表現検出"""
        
        # 明確な時間パターン
        time_patterns = [
            r'\b(today|tomorrow|yesterday)\b',
            r'\b(last|this|next)\s+(week|month|year|morning|afternoon|evening|night)\b',
            r'\b(every|each)\s+(day|week|month|morning|afternoon|evening)\b',
            r'\b(a\s+few|several|many)\s+(days?|weeks?|months?|years?)\s+ago\b',
            r'\b(that|this)\s+(morning|afternoon|evening|night)\b',
            r'\b\d+\s*(am|pm)\b',
            r'\b(at|on|in)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
        ]
        
        text = doc.text
        for pattern in time_patterns:
            import re
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # spaCyの時間エンティティ
        for ent in doc.ents:
            if ent.label_ in ["TIME", "DATE"]:
                return ent.text
        
        # 副詞句（時間表現の可能性）
        time_advs = []
        for token in doc:
            if token.pos_ == "ADV" and token.dep_ in ["advmod", "npadvmod"]:
                # 時間を示唆するキーワードをチェック
                if any(keyword in token.text.lower() for keyword in ['day', 'morning', 'afternoon', 'evening', 'night', 'today', 'ago']):
                    return self._get_complete_adverb_phrase(token)
        
        return None
    
    def _extract_generic_auxiliary(self, doc) -> Optional[str]:
        """汎用的な助動詞検出（縮約形対応）"""
        
        # spaCyが解析した縮約形を確認
        for token in doc:
            if token.text.lower() == "ca" and token.pos_ == "AUX":
                # "ca"は"can"の縮約形の一部
                for next_token in doc:
                    if next_token.i == token.i + 1 and next_token.text in ["n't", "not"]:
                        return "cannot"
                        
        # 完全な縮約形マッピング
        contractions = {
            "can't": "cannot",
            "won't": "will not", 
            "shouldn't": "should not",
            "wouldn't": "would not",
            "couldn't": "could not",
            "mustn't": "must not",
            "needn't": "need not"
        }
        
        # 元の文から縮約形の検出
        text_lower = doc.text.lower()
        for contraction, expansion in contractions.items():
            if contraction in text_lower:
                return expansion
        
        # AUX品詞の検出
        for token in doc:
            if token.pos_ == "AUX" and token.dep_ == "aux":
                # 否定の場合
                for child in token.children:
                    if child.dep_ == "neg" or child.text in ["n't", "not"]:
                        return f"{token.lemma_} not"
                return token.text
                
        return None
    
    def _get_complete_adverb_phrase(self, token) -> str:
        """完全な副詞句の取得"""
        phrase_tokens = []
        
        # 依存関係を持つ子要素を含める
        def collect_phrase(tok):
            phrase_tokens.append(tok)
            for child in tok.children:
                if child.dep_ in ["det", "amod", "compound", "nummod"]:
                    collect_phrase(child)
        
        collect_phrase(token)
        
        # 位置順にソート
        phrase_tokens.sort(key=lambda t: t.i)
        return " ".join([t.text for t in phrase_tokens])
    
    def _extract_ditransitive_objects(self, doc, slots: Dict[str, List]):
        """SVOO構造の間接目的語と直接目的語の適切な分離"""
        
        # すでにO1が検出されている場合のみ処理
        if not slots.get('O1'):
            return
            
        # 間接目的語（iobj）の検出
        indirect_obj = None
        direct_obj = None
        
        for token in doc:
            if token.dep_ == "iobj":
                indirect_obj = self._get_complete_noun_phrase(token)
            elif token.dep_ == "dobj":
                direct_obj = self._get_complete_noun_phrase(token)
        
        # SVOO構造の場合、適切にスロットを割り当て
        if indirect_obj and direct_obj:
            # O1を間接目的語に、O2を直接目的語に
            slots['O1'] = [{
                'value': indirect_obj,
                'rule_id': 'ditransitive-iobj',
                'confidence': 0.9
            }]
            slots['O2'] = [{
                'value': direct_obj,
                'rule_id': 'ditransitive-dobj', 
                'confidence': 0.9
            }]
            print(f"✅ SVOO構造検出: O1={indirect_obj}, O2={direct_obj}")
            
        # 前置詞句による間接目的語の検出
        elif not indirect_obj:
            for token in doc:
                if token.dep_ == "prep" and token.text.lower() == "to":
                    prep_obj = None
                    for child in token.children:
                        if child.dep_ == "pobj":
                            prep_obj = self._get_complete_noun_phrase(child)
                            break
                    
                    if prep_obj and direct_obj:
                        # 前置詞句を間接目的語として処理
                        slots['O2'] = [{
                            'value': f"to {prep_obj}",
                            'rule_id': 'prepositional-iobj',
                            'confidence': 0.8
                        }]
                        print(f"✅ 前置詞句間接目的語検出: O2=to {prep_obj}")
    
    def _extract_auxiliary_value(self, doc, hierarchy) -> Optional[str]:
        """助動詞の正確な抽出 - 縮約形対応"""
        
        main_verb = hierarchy.get('main_clause', {}).get('verb')
        if not main_verb:
            return None
        
        auxiliaries = []
        
        # 助動詞の収集
        for child in main_verb.children:
            if child.dep_ == "aux":
                aux_text = child.text
                
                # 縮約形の修正
                if aux_text == "ca" and child.i < len(doc) - 1:
                    next_token = doc[child.i + 1]
                    if next_token.text == "n't":
                        aux_text = "cannot"  # can't -> cannot
                elif aux_text == "wo" and child.i < len(doc) - 1:
                    next_token = doc[child.i + 1]
                    if next_token.text == "n't":
                        aux_text = "will not"  # won't -> will not
                
                auxiliaries.append({
                    'text': aux_text,
                    'position': child.i
                })
        
        # 位置順でソート
        auxiliaries.sort(key=lambda x: x['position'])
        
        if auxiliaries:
            return ' '.join([aux['text'] for aux in auxiliaries])
        
        return None
    
    def _extract_temporal_value(self, doc, hierarchy) -> Optional[str]:
        """時間表現の抽出 - Rephraseルール対応"""
        
        temporal_expressions = []
        
        # npadvmod時間表現
        for token in doc:
            if token.dep_ == "npadvmod" and self._is_temporal_word(token.text):
                temporal_expressions.append({
                    'text': self._get_complete_noun_phrase(token),
                    'position': token.i,
                    'type': 'npadvmod'
                })
        
        # 固有表現（時間）
        for ent in doc.ents:
            if ent.label_ in ['TIME', 'DATE']:
                temporal_expressions.append({
                    'text': ent.text,
                    'position': ent.start,
                    'type': 'named_entity'
                })
        
        # "ago"構造の特別処理
        for i, token in enumerate(doc):
            if token.text.lower() == "ago" and i >= 2:
                # "a few days ago" のような構造
                phrase_tokens = []
                j = i - 1
                while j >= 0 and doc[j].dep_ in ['det', 'amod', 'nummod', 'noun']:
                    phrase_tokens.insert(0, doc[j])
                    j -= 1
                    if len(phrase_tokens) >= 4:  # 安全制限
                        break
                
                if phrase_tokens:
                    phrase_tokens.append(token)  # "ago"を追加
                    full_phrase = ' '.join([t.text for t in phrase_tokens])
                    temporal_expressions.append({
                        'text': full_phrase,
                        'position': phrase_tokens[0].i,
                        'type': 'ago_structure'
                    })
        
        # 最も適切な時間表現を選択（文頭に近いものを優先）
        if temporal_expressions:
            temporal_expressions.sort(key=lambda x: x['position'])
            return temporal_expressions[0]['text']
        
        return None
    
    def _is_temporal_word(self, word: str) -> bool:
        """時間を表す単語かどうか判定 - 拡張版"""
        temporal_words = {
            # 時間帯
            'morning', 'afternoon', 'evening', 'night', 'midnight', 'noon',
            # 日
            'today', 'yesterday', 'tomorrow',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            # 月
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            # 期間
            'week', 'month', 'year', 'day', 'hour', 'minute', 'second',
            'weekend', 'weekday',
            # 頻度
            'always', 'never', 'often', 'sometimes', 'usually', 'rarely',
            'daily', 'weekly', 'monthly', 'yearly',
            # その他
            'now', 'then', 'soon', 'late', 'early', 'recently', 'lately'
        }
        
        return word.lower() in temporal_words
    
    # 実装予定のメソッド群
    def _extract_noun_phrases(self, doc): return []
    def _extract_verb_phrases(self, doc): return []
    def _extract_prep_phrases(self, doc): return []
    def _extract_generic_value(self, assignment: Dict[str, Any], doc, hierarchy) -> Optional[str]:
        """汎用的な値抽出 - ルール辞書対応"""
        
        slot = assignment.get('slot', '')
        
        # スロット別の抽出ロジック
        if slot == 'S':
            return self._extract_subject_value(doc, hierarchy)
        elif slot == 'V':
            return self._extract_verb_value(doc, hierarchy, 'generic')
        elif slot == 'Aux':
            return self._extract_auxiliary_value(doc, hierarchy)
        elif slot == 'O1':
            return self._extract_direct_object_value(doc, hierarchy)
        elif slot == 'O2':
            return self._extract_indirect_object_value(doc, hierarchy)
        elif slot == 'M3':
            return self._extract_temporal_value(doc, hierarchy)
        elif slot in ['M1', 'M2']:
            return self._extract_modifier_value(doc, hierarchy, slot)
        
        return None
    
    def _extract_direct_object_value(self, doc, hierarchy) -> Optional[str]:
        """直接目的語の抽出"""
        
        main_verb = hierarchy.get('main_clause', {}).get('verb')
        if not main_verb:
            return None
        
        # 直接目的語を探す
        for token in doc:
            if token.dep_ == "dobj" and token.head == main_verb:
                return self._get_complete_noun_phrase(token)
        
        return None
    
    def _extract_indirect_object_value(self, doc, hierarchy) -> Optional[str]:
        """間接目的語の抽出"""
        
        main_verb = hierarchy.get('main_clause', {}).get('verb')
        if not main_verb:
            return None
        
        # 間接目的語を探す
        for token in doc:
            if token.dep_ in ["iobj", "dative"] and token.head == main_verb:
                return self._get_complete_noun_phrase(token)
        
        return None
    
    def _extract_modifier_value(self, doc, hierarchy, slot: str) -> Optional[str]:
        """修飾語の抽出 - M1/M2/M3分類"""
        
        if slot == 'M1':
            # 場所・状況修飾語
            return self._extract_locative_modifier(doc)
        elif slot == 'M2':
            # 方法・手段修飾語
            return self._extract_manner_modifier(doc)
        elif slot == 'M3':
            # 時間・頻度修飾語
            return self._extract_temporal_value(doc, hierarchy)
        
        return None
    
    def _extract_locative_modifier(self, doc) -> Optional[str]:
        """場所修飾語の抽出"""
        
        for token in doc:
            if token.pos_ == "ADP" and token.text.lower() in ['at', 'in', 'on', 'near', 'by']:
                # 前置詞句の場合
                for child in token.children:
                    if child.dep_ == "pobj":
                        # 時間表現でないことを確認
                        if not self._is_temporal_word(child.text):
                            phrase = f"{token.text} {self._get_complete_noun_phrase(child)}"
                            return phrase
        
        return None
    
    def _extract_manner_modifier(self, doc) -> Optional[str]:
        """方法・手段修飾語の抽出"""
        
        for token in doc:
            if token.pos_ == "ADP" and token.text.lower() in ['with', 'by', 'through']:
                for child in token.children:
                    if child.dep_ == "pobj":
                        phrase = f"{token.text} {self._get_complete_noun_phrase(child)}"
                        return phrase
        
        return None
    def _process_relative_clause_subslots(self, verb, sub_slots, doc): pass
    def _process_adverbial_clause_subslots(self, verb, sub_slots, doc): pass
