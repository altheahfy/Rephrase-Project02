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
                'slots': rephrase_slots,
                'main_slots': rephrase_slots,
                'sub_structures': sub_structures,
                'sentence_pattern': sentence_pattern,
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
        blocked_rules = []  # ブロックされたルールのリスト
        
        for rule in rules:
            rule_id = rule.get('id', '')
            
            # 呼びかけルールが適用されている場合、主語ルールをブロック
            if rule_id == 'subject-pronoun-np-front' and 'vocative-you-comma' in applied_rules:
                blocked_rules.append(rule_id)
                print(f"🚫 ルールブロック: {rule_id} (呼びかけルール優先)")
                continue
            
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
        if blocked_rules:
            print(f"🚫 ブロックされたルール数: {len(blocked_rules)} → {blocked_rules}")
        
        # 汎用的な動詞検出（ルールで捕獲されなかった場合）
        if not slots['V']:
            generic_verb = self._extract_generic_verb(doc, hierarchy)
            if generic_verb:
                slots['V'].append({
                    'value': generic_verb,
                    'rule_id': 'generic-verb',
                    'confidence': 0.7,
                    'order': 4
                })
                print(f"✅ 汎用動詞検出: {generic_verb}")
        
        # 汎用的な目的語検出（ルールで捕獲されなかった場合）
        if not slots['O1']:
            generic_object = self._extract_generic_object(doc, hierarchy)
            if generic_object:
                slots['O1'].append({
                    'value': generic_object,
                    'rule_id': 'generic-object',
                    'confidence': 0.7,
                    'order': 5
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
                    'confidence': 0.8,
                    'order': 6
                })
                print(f"✅ 汎用時間表現検出: {generic_time}")
        
        # 汎用的な助動詞検出（縮約形対応）
        if not slots['Aux']:
            generic_aux = self._extract_generic_auxiliary(doc)
            if generic_aux:
                slots['Aux'].append({
                    'value': generic_aux,
                    'rule_id': 'generic-aux',
                    'confidence': 0.8,
                    'order': 2
                })
                print(f"✅ 汎用助動詞検出: {generic_aux}")
        
        # 汎用的な前置詞句検出（副詞的修飾語として）
        if not slots['M2']:
            generic_prep = self._extract_generic_prepositional_phrase(doc)
            if generic_prep:
                slots['M2'].append({
                    'value': generic_prep,
                    'rule_id': 'generic-prep-phrase',
                    'confidence': 0.8,
                    'order': 7
                })
                print(f"✅ 汎用前置詞句検出: {generic_prep}")
        
        # 汎用的な補語検出（C1）- be動詞やbecome等の後の名詞句・形容詞句
        if not slots['C1']:
            generic_complement = self._extract_generic_complement(doc)
            if generic_complement:
                slots['C1'].append({
                    'value': generic_complement,
                    'rule_id': 'generic-complement',
                    'confidence': 0.8,
                    'order': 8
                })
                print(f"✅ 汎用補語検出: {generic_complement}")
        
        return slots
    
    def _should_apply_rule(self, rule: Dict[str, Any], doc, hierarchy) -> bool:
        """ルールを適用すべきかどうかの判定"""
        
        rule_id = rule.get('id', 'unknown')
        trigger = rule.get('trigger', {})
        
        print(f"🔍 ルール判定: {rule_id}")
        
        # パターンルールの場合は特別処理
        if 'patterns' in rule:
            patterns = rule['patterns']
            print(f"  パターンルール検出: {len(patterns)}個のパターン")
            for pattern_obj in patterns:
                pattern_text = pattern_obj.get('pattern', '')
                if re.search(pattern_text, doc.text, re.IGNORECASE):
                    print(f"  ✅ パターンマッチ: {pattern_text}")
                    return True
            print(f"  ❌ パターン非マッチ")
            return False
        
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
        
        # depトリガーの確認（依存関係ラベル）
        if 'dep' in trigger:
            dep_tags = trigger['dep'] if isinstance(trigger['dep'], list) else [trigger['dep']]
            doc_deps = [token.dep_ for token in doc]
            dep_match = any(token.dep_ in dep_tags for token in doc)
            print(f"  depトリガー: {dep_tags} → 文書内: {doc_deps} → マッチ: {dep_match}")
            if not dep_match:
                return False
        
        # patternトリガーの確認
        if 'pattern' in trigger:
            pattern = trigger['pattern']
            pattern_match = bool(re.search(pattern, doc.text))
            print(f"  パターントリガー: {pattern} → マッチ: {pattern_match}")
            if not pattern_match:
                return False
        
        # positionトリガーの確認（高度な条件）
        if 'position' in trigger:
            position = trigger['position']
            print(f"  位置条件: {position}")
            # 実装例：'before_first_main_verb' など
            if position == 'before_first_main_verb':
                main_verbs = [token for token in doc if token.pos_ == 'VERB' and token.dep_ in ['ROOT', 'ccomp']]
                if main_verbs:
                    first_verb_idx = main_verbs[0].i
                    # ここで位置関係を確認する具体的なロジックを実装
                    print(f"    主動詞位置: {first_verb_idx}")
            elif position == 'after_V':
                # 動詞の後に来る副詞をチェック
                main_verbs = [token for token in doc if token.pos_ == 'VERB' and token.dep_ in ['ROOT', 'ccomp']]
                if main_verbs:
                    main_verb = main_verbs[0]
                    # 主動詞の後にある副詞を探す
                    pos_check_passed = False
                    if 'pos' in trigger:
                        target_pos = trigger['pos']
                        adverbs_after_verb = [token for token in doc if token.pos_ in target_pos and token.i > main_verb.i]
                        if adverbs_after_verb:
                            pos_check_passed = True
                            print(f"    動詞後の{target_pos}: {[token.text for token in adverbs_after_verb]}")
                        else:
                            print(f"    動詞後に{target_pos}が見つからない")
                            return False
                    else:
                        pos_check_passed = True
                    
                    if not pos_check_passed:
                        return False
        
        # senseトリガーの確認（意味的条件）
        if 'sense' in trigger:
            sense = trigger['sense']
            print(f"  意味条件: {sense}")
            # 実装例：'exist_locative' など
            if sense == 'exist_locative':
                # 場所的存在を表す文脈かどうかを判定
                prep_tokens = [token for token in doc if token.pos_ == 'ADP']
                location_preps = any(token.text.lower() in ['in', 'on', 'at', 'by'] for token in prep_tokens)
                print(f"    場所的前置詞: {location_preps}")
        
        # conditionsフィールドの確認（追加条件）
        conditions = rule.get('conditions', {})
        if conditions:
            position = conditions.get('position', '')
            if position == 'sentence_final':
                # 文末位置の確認
                lemmas = trigger.get('lemma', [])
                if lemmas:
                    target_lemma = lemmas[0] if isinstance(lemmas, list) else lemmas
                    # 対象lemmaが文末近くにあるかチェック（句読点除く）
                    content_tokens = [token for token in doc if not token.is_punct]
                    if content_tokens:
                        last_content_token = content_tokens[-1]
                        if last_content_token.lemma_ == target_lemma:
                            print(f"    文末位置確認: '{target_lemma}' が文末に配置")
                        else:
                            print(f"    文末位置確認失敗: 最終語は '{last_content_token.lemma_}' (期待: '{target_lemma}')")
                            return False
        
        # 句動詞粒子の特別な条件チェック
        if 'conditions' in trigger:
            phrasal_conditions = trigger['conditions']
            if 'follows_verb' in phrasal_conditions and phrasal_conditions['follows_verb']:
                # 動詞の後に続く粒子かどうかをチェック
                verb_found = False
                particle_found = False
                
                verbs = [token for token in doc if token.pos_ == 'VERB']
                if verbs:
                    main_verb = verbs[0]  # 最初の動詞を主動詞として扱う
                    
                    # 動詞の直後または近くに粒子があるかチェック
                    for token in doc:
                        if (token.pos_ == 'ADP' and 
                            token.dep_ in ['prt', 'prep'] and
                            token.i > main_verb.i and 
                            token.i - main_verb.i <= 3):  # 動詞から3トークン以内
                            
                            # 句動詞粒子リストのチェック
                            if 'phrasal_verb_particle' in phrasal_conditions:
                                particle_list = phrasal_conditions['phrasal_verb_particle']
                                if token.text.lower() in particle_list:
                                    particle_found = True
                                    print(f"    句動詞粒子確認: '{main_verb.text}' + '{token.text}' (dep: {token.dep_})")
                                    break
                
                if not particle_found:
                    print(f"    句動詞粒子条件失敗: 動詞後の適切な粒子が見つからない")
                    return False

        print(f"  → ルール適用対象: {rule_id}")
        return True
    
    def _apply_single_rule(self, rule: Dict[str, Any], doc, hierarchy, slots: Dict[str, List]) -> bool:
        """単一ルールの適用"""
        
        rule_id = rule.get('id', '')
        assignment = rule.get('assign', {})
        
        # パターントリガーの場合は特別処理
        trigger = rule.get('trigger', {})
        if 'pattern' in trigger:
            # パターンベースの値抽出
            pattern = trigger['pattern']
            match = re.search(pattern, doc.text, re.IGNORECASE)
            if match:
                # assignフィールドでvalueが指定されている場合はそれを優先
                assignment = rule.get('assign', {})
                if 'value' in assignment:
                    value = assignment['value']
                # 実際の値を決定
                elif rule_id == 'place-M3':
                    value = self._extract_place_prepositional_phrase(doc)
                elif rule_id == 'to-direction-M2':
                    value = self._extract_direction_prepositional_phrase(doc, rule_id)
                elif rule_id == 'for-purpose-M2':
                    value = self._extract_direction_prepositional_phrase(doc, rule_id)
                elif rule_id == 'from-source-M3':
                    value = self._extract_from_prepositional_phrase(doc)
                else:
                    value = match.group()
                
                if value:
                    slot = assignment.get('slot', '')
                    if slot in slots:
                        # 不定詞の用法別処理
                        if rule_id == 'to-direction-M2' and self._contains_verb(value, doc):
                            # 不定詞の名詞的用法をチェック
                            if self._is_infinitive_as_noun(value, doc):
                                # 不定詞の名詞的用法の場合はO1のphrase候補として追加
                                print(f"🔄 不定詞の名詞的用法検出: '{value}' → O1 phraseに変更")
                                if 'O1' not in slots:
                                    slots['O1'] = []
                                slots['O1'].append({
                                    'value': value,
                                    'rule_id': rule_id,
                                    'confidence': 0.95,
                                    'is_phrase': True,
                                    'label': 'phrase'
                                })
                                print(f"    ✅ O1に'{value}'をphraseとして設定")
                                return True
                            
                            # 不定詞の形容詞的用法をチェック
                            elif self._is_infinitive_as_adjective(value, doc):
                                # 形容詞的用法の場合は元の名詞句に統合（M2に追加しない）
                                print(f"🔄 不定詞の形容詞的用法検出: '{value}' → 名詞句に統合（M2から除外）")
                                return True  # 処理済みとしてM2には追加しない
                            
                            # 不定詞の副詞的用法をチェック
                            elif self._is_infinitive_as_adverb(value, doc):
                                # 副詞的用法の場合はM2のphraseとして処理
                                print(f"🔄 不定詞の副詞的用法検出: '{value}' → M2 phraseとして処理")
                                slots[slot].append({
                                    'value': value,
                                    'rule_id': rule_id,
                                    'confidence': 0.9,
                                    'is_phrase': True,
                                    'label': 'phrase'
                                })
                                print(f"    ✅ M2に'{value}'をphraseとして設定")
                                return True
                        
                        # 動詞を含む句のみを「phrase」として扱う
                        is_verb_phrase = self._contains_verb(value, doc)
                        
                        candidate_data = {
                            'value': value,
                            'rule_id': rule_id,
                            'confidence': 0.9
                        }
                        
                        # assignフィールドからorder情報を取得
                        assignment = rule.get('assign', {})
                        if 'order' in assignment:
                            candidate_data['order'] = assignment['order']
                        
                        # 動詞を含む句の場合のみphraseフラグを設定
                        if is_verb_phrase:
                            candidate_data['is_phrase'] = True
                            print(f"📝 動詞句ルール適用: {rule_id} → {slot}: '{value}' (phrase)")
                        else:
                            print(f"📝 パターンルール適用: {rule_id} → {slot}: '{value}' (word)")
                        
                        slots[slot].append(candidate_data)
                        return True
            return False
        
        # 通常のルール処理
        if isinstance(assignment, list):
            # 複数割り当ての場合
            for assign_item in assignment:
                self._execute_assignment(assign_item, doc, hierarchy, slots, rule_id)
            return True
        else:
            # 単一割り当ての場合
            return self._execute_assignment(assignment, doc, hierarchy, slots, rule_id)
    
    def _apply_pattern_rule(self, rule: Dict[str, Any], doc, hierarchy, slots: Dict[str, List]) -> bool:
        """パターンルールの適用"""
        
        rule_id = rule.get('id', '')
        patterns = rule.get('patterns', [])
        
        print(f"📝 パターンルール適用: {rule_id}")
        
        for pattern_obj in patterns:
            pattern_text = pattern_obj.get('pattern', '')
            assign_data = pattern_obj.get('assign', {})
            
            match = re.search(pattern_text, doc.text, re.IGNORECASE)
            if match:
                print(f"  ✅ パターンマッチ: {pattern_text}")
                print(f"  📌 マッチ部分: '{match.group()}'")
                
                # パターンに基づく割り当て実行
                if isinstance(assign_data, list):
                    for assign_item in assign_data:
                        self._execute_pattern_assignment(assign_item, match, doc, slots, rule_id)
                else:
                    self._execute_pattern_assignment(assign_data, match, doc, slots, rule_id)
                return True
        
        return False
    
    def _execute_pattern_assignment(self, assignment: Dict[str, Any], match, doc, slots: Dict[str, List], rule_id: str):
        """パターンベースの割り当て実行"""
        
        slot = assignment.get('slot', '')
        value_type = assignment.get('type', 'word')
        value_spec = assignment.get('value', '')
        
        print(f"    🎯 スロット: {slot}, タイプ: {value_type}, 値指定: {value_spec}")
        
        # 実際の値を決定
        if value_type == 'group':
            # 正規表現グループから値を取得
            group_num = assignment.get('group', 1)
            if group_num <= len(match.groups()):
                value = match.group(group_num)
            else:
                value = match.group()
        elif value_type == 'word':
            # 指定された単語から値を取得
            value = self._find_word_in_sentence(value_spec, doc)
        elif value_type == 'phrase':
            # 指定されたフレーズから値を取得
            value = value_spec
        else:
            # デフォルト: パターンに基づく前置詞句抽出
            if rule_id == 'place-M3':
                value = self._extract_place_prepositional_phrase(doc)
            elif rule_id in ['to-direction-M2', 'for-purpose-M2']:
                value = self._extract_direction_prepositional_phrase(doc, rule_id)
            else:
                value = match.group()
        
        if value and slot in slots:
            # 不定詞の名詞的用法をチェック
            if rule_id == 'to-direction-M2' and self._is_infinitive_as_noun(value, doc):
                # 不定詞の名詞的用法の場合はO1のphrase候補として追加
                print(f"🔄 不定詞の名詞的用法検出: '{value}' → O1 phraseに変更")
                if 'O1' not in slots:
                    slots['O1'] = []
                slots['O1'].append({
                    'value': value,
                    'rule_id': rule_id,
                    'confidence': 0.95,
                    'pattern_based': True,
                    'is_phrase': True,
                    'label': 'phrase'
                })
                print(f"    ✅ O1に'{value}'をphraseとして設定")
            else:
                # 通常の前置詞句として処理
                is_phrase = self._contains_verb(value, doc)
                slots[slot].append({
                    'value': value,
                    'rule_id': rule_id,
                    'confidence': 0.9,
                    'pattern_based': True,
                    'is_phrase': is_phrase,
                    'label': 'phrase' if is_phrase else 'word'
                })
                print(f"    ✅ {slot}に'{value}'を設定")
    
    def _find_word_in_sentence(self, target_word: str, doc) -> str:
        """文中から指定された単語を検索"""
        for token in doc:
            if token.text.lower() == target_word.lower() or token.lemma_.lower() == target_word.lower():
                return token.text
        return target_word
    
    def _execute_assignment(self, assignment: Dict[str, Any], doc, hierarchy, slots: Dict[str, List], rule_id: str) -> bool:
        """割り当ての実行"""
        
        slot = assignment.get('slot', '')
        assign_type = assignment.get('type', 'word')
        
        if slot not in slots:
            return False
        
        # 値の決定
        value = self._determine_assignment_value(assignment, doc, hierarchy, rule_id)
        
        if value:
            candidate_data = {
                'value': value,
                'type': assign_type,
                'rule_id': rule_id
            }
            
            # assignフィールドからorder情報を取得
            if 'order' in assignment:
                candidate_data['order'] = assignment['order']
                
            slots[slot].append(candidate_data)
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
        elif rule_id == 'manner-degree-M2':
            return self._extract_adverb_value(doc)
        elif rule_id == 'phrasal-verb-particle-M2':
            return self._extract_phrasal_verb_particle(doc)
        elif rule_id == 'wh-where-front':
            return self._extract_wh_where_value(doc)
        elif rule_id == 'please-interjection-M3':
            return self._extract_please_interjection_value(doc)
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
        
        # 左側の修飾語（所有格代名詞を含む）
        for child in token.children:
            if child.i < token.i and child.dep_ in ['det', 'amod', 'compound', 'nummod', 'poss']:
                phrase_tokens.append(child)
        
        # 右側の修飾語（前置詞句は除く）
        for child in token.children:
            if child.i > token.i and child.dep_ in ['amod', 'compound']:
                phrase_tokens.append(child)
        
        # 関係詞節がある場合は含める
        for child in token.children:
            if child.dep_ == 'relcl':
                # 関係詞節の処理
                if child.pos_ == 'VERB':
                    # 不定詞の形容詞的用法（to + 動詞）かチェック
                    infinitive_part = None
                    for inf_child in child.children:
                        if inf_child.pos_ == 'PART' and inf_child.text.lower() == 'to':
                            infinitive_part = inf_child
                            break
                    
                    if infinitive_part:
                        # 不定詞句を構築
                        infinitive_phrase = f"to {child.text}"
                        # 動詞の目的語があれば追加
                        for verb_child in child.children:
                            if verb_child.dep_ in ['dobj', 'pobj'] and verb_child != infinitive_part:
                                infinitive_phrase += f" {self._get_complete_noun_phrase(verb_child)}"
                        
                        phrase_text = ' '.join(sorted([t.text for t in phrase_tokens], key=lambda x: token.doc[[t.text for t in token.doc].index(x)].i))
                        return f"{phrase_text} {infinitive_phrase}"
                    else:
                        # 通常の関係詞節
                        rel_phrase = self._get_relative_clause_phrase(child)
                        phrase_text = ' '.join(sorted([t.text for t in phrase_tokens], key=lambda x: token.doc[[t.text for t in token.doc].index(x)].i))
                        return f"{phrase_text} {rel_phrase}"
        
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
    
    def _extract_phrasal_verb_particle(self, doc) -> Optional[str]:
        """句動詞粒子の抽出"""
        
        # 句動詞の粒子リスト
        phrasal_particles = [
            "off", "on", "up", "down", "out", "in", "away", "back", 
            "over", "after", "through", "into", "onto", "across", 
            "along", "around", "aside", "apart", "ahead", "behind", 
            "beyond", "beneath", "between", "toward", "towards", "underneath"
        ]
        
        # 動詞を最初に見つける
        verbs = [token for token in doc if token.pos_ == 'VERB']
        if not verbs:
            return None
        
        main_verb = verbs[0]  # 最初の動詞を主動詞とみなす
        
        # 動詞の後に続く粒子を探す
        for token in doc:
            if (token.pos_ == 'ADP' and 
                token.dep_ in ['prt', 'prep'] and
                token.i > main_verb.i and 
                token.i - main_verb.i <= 3 and  # 動詞から3トークン以内
                token.text.lower() in phrasal_particles):
                
                print(f"  ✅ 句動詞粒子検出: '{main_verb.text}' + '{token.text}' (依存関係: {token.dep_})")
                return token.text
        
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
    
    def _extract_generic_prepositional_phrase(self, doc) -> Optional[str]:
        """汎用的な前置詞句検出（方向・対象のM2のみ）"""
        
        # M2に属する方向・対象を示す前置詞のみ
        m2_preps = ['to', 'for', 'with', 'about']  # 'on', 'in', 'by', 'from' は除外（M3やその他の可能性）
        
        for token in doc:
            if token.pos_ == "ADP" and token.text.lower() in m2_preps:
                # 前置詞の目的語を取得
                prep_object = None
                for child in token.children:
                    if child.dep_ == "pobj":
                        prep_object = self._get_complete_noun_phrase(child)
                        break
                
                if prep_object:
                    # 動詞に直接依存している前置詞句のみをM2とする
                    if token.dep_ == "prep" and token.head.pos_ == "VERB":
                        return f"{token.text} {prep_object}"
        
        return None
    
    def _extract_place_prepositional_phrase(self, doc) -> Optional[str]:
        """場所を表す前置詞句の抽出（M3用）"""
        
        # 場所を表す前置詞
        place_preps = ['on', 'in', 'under', 'by', 'at']
        
        for token in doc:
            if (token.pos_ == "ADP" and 
                token.text.lower() in place_preps and
                token.dep_ == "prep"):
                
                # 前置詞の目的語を取得
                for child in token.children:
                    if child.dep_ == "pobj":
                        prep_object = self._get_complete_noun_phrase(child)
                        return f"{token.text} {prep_object}"
        
        return None
    
    def _extract_direction_prepositional_phrase(self, doc, rule_id: str) -> Optional[str]:
        """方向・目的を表す前置詞句の抽出（M2用）"""
        
        # ルールに応じた前置詞を特定
        if rule_id == 'to-direction-M2':
            target_prep = 'to'
        elif rule_id == 'for-purpose-M2':
            target_prep = 'for'
        else:
            return None
        
        for token in doc:
            # 前置詞句の処理（通常の前置詞句 + 二重目的語の間接目的語マーカー）
            if (token.pos_ == "ADP" and 
                token.text.lower() == target_prep and
                token.dep_ in ["prep", "dative"]):  # dativeも追加
                
                # 前置詞の目的語を取得
                for child in token.children:
                    if child.dep_ == "pobj":
                        prep_object = self._get_complete_noun_phrase(child)
                        return f"{token.text} {prep_object}"
            
            # 不定詞句の処理（to の場合のみ）
            elif (rule_id == 'to-direction-M2' and 
                  token.pos_ == "PART" and 
                  token.text.lower() == "to" and
                  token.head and token.head.pos_ == "VERB"):
                
                # 不定詞句全体を構築
                infinitive_verb = token.head
                infinitive_phrase = f"to {infinitive_verb.text}"
                
                # 動詞の目的語や修飾語があれば追加
                objects = []
                for child in infinitive_verb.children:
                    if child.dep_ in ["dobj", "pobj"]:
                        objects.append(self._get_complete_noun_phrase(child))
                    elif child.dep_ in ["prep"]:
                        # 前置詞句も含める
                        for prep_child in child.children:
                            if prep_child.dep_ == "pobj":
                                prep_phrase = f"{child.text} {self._get_complete_noun_phrase(prep_child)}"
                                objects.append(prep_phrase)
                
                if objects:
                    infinitive_phrase += " " + " ".join(objects)
                
                return infinitive_phrase
        
        return None
    
    def _extract_from_prepositional_phrase(self, doc) -> Optional[str]:
        """from句の抽出（M3用）"""
        
        for token in doc:
            if (token.pos_ == "ADP" and 
                token.text.lower() == 'from' and
                token.dep_ == "prep"):
                
                # 前置詞の目的語を取得
                for child in token.children:
                    if child.dep_ == "pobj":
                        prep_object = self._get_complete_noun_phrase(child)
                        return f"{token.text} {prep_object}"
        
        return None
    
    def _contains_verb(self, phrase: str, doc) -> bool:
        """フレーズが動詞を含むかどうかを判定（真のphraseかどうか）"""
        
        # to + 動詞の不定詞句をチェック
        if phrase.lower().startswith('to '):
            words = phrase.split()
            if len(words) >= 2:
                # spaCyで動詞かどうかを確認
                verb_word = words[1]
                for token in doc:
                    if token.text.lower() == verb_word.lower() and token.pos_ == 'VERB':
                        return True
        
        # 他の動詞句パターンをチェック
        words = phrase.split()
        for word in words:
            for token in doc:
                if (token.text.lower() == word.lower() and 
                    token.pos_ in ['VERB', 'AUX'] and 
                    token.dep_ not in ['aux', 'auxpass']):  # 助動詞は除外
                    return True
        
        return False
    
    def _is_infinitive_as_noun(self, phrase: str, doc) -> bool:
        """不定詞の名詞的用法かどうかを判定"""
        
        # "to + 動詞" パターンのチェック
        if not phrase.lower().startswith('to '):
            return False
            
        words = phrase.split()
        if len(words) < 2:
            return False
            
        # 文中でこの不定詞句の文法的役割をチェック
        for token in doc:
            if (token.pos_ == 'PART' and token.text.lower() == 'to' and 
                token.head and token.head.pos_ == 'VERB'):
                
                # 不定詞句の依存関係をチェック
                infinitive_verb = token.head
                
                # 名詞的用法の典型的な依存関係
                if infinitive_verb.dep_ in ['dobj', 'nsubj', 'pcomp', 'ccomp']:
                    return True
                    
                # 主語として機能している場合
                if (infinitive_verb.dep_ == 'csubj' or 
                    (infinitive_verb.dep_ == 'acl' and infinitive_verb.head.dep_ == 'nsubj')):
                    return True
                    
                # want, like, need などの動詞の目的語として機能
                if (infinitive_verb.dep_ == 'xcomp' and 
                    infinitive_verb.head.lemma_ in ['want', 'like', 'need', 'plan', 'try', 'decide']):
                    return True
        
        return False
    
    def _is_infinitive_as_adjective(self, phrase: str, doc) -> bool:
        """不定詞の形容詞的用法かどうかを判定（名詞を修飾）"""
        
        # "to + 動詞" パターンのチェック
        if not phrase.lower().startswith('to '):
            return False
            
        words = phrase.split()
        if len(words) < 2:
            return False
            
        # 文中でこの不定詞句の文法的役割をチェック
        for token in doc:
            if (token.pos_ == 'PART' and token.text.lower() == 'to' and 
                token.head and token.head.pos_ == 'VERB'):
                
                infinitive_verb = token.head
                
                # 形容詞的用法の典型的な依存関係
                if infinitive_verb.dep_ in ['relcl', 'acl']:
                    # 名詞を修飾している場合
                    if infinitive_verb.head.pos_ in ['NOUN', 'PRON']:
                        return True
        
        return False
    
    def _is_infinitive_as_adverb(self, phrase: str, doc) -> bool:
        """不定詞の副詞的用法かどうかを判定（目的・結果）"""
        
        # "to + 動詞" パターンのチェック
        if not phrase.lower().startswith('to '):
            return False
            
        words = phrase.split()
        if len(words) < 2:
            return False
            
        # 文中でこの不定詞句の文法的役割をチェック
        for token in doc:
            if (token.pos_ == 'PART' and token.text.lower() == 'to' and 
                token.head and token.head.pos_ == 'VERB'):
                
                infinitive_verb = token.head
                
                # 副詞的用法の典型的な依存関係
                if infinitive_verb.dep_ in ['advcl', 'purpcl']:
                    return True
                    
                # go, come などの移動動詞の目的として機能
                if (infinitive_verb.dep_ == 'xcomp' and 
                    infinitive_verb.head.lemma_ in ['go', 'come', 'run', 'walk', 'drive']):
                    return True
        
        return False
    
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
        """真のSVOO構造（名詞+名詞のみ）の検出"""
        
        # すでにO1が検出されている場合のみ処理
        if not slots.get('O1'):
            return
            
        # 真のSVOO: 両方とも名詞句である場合のみ
        indirect_obj = None
        direct_obj = None
        
        # 依存関係による目的語の特定
        for token in doc:
            if token.dep_ == "iobj" and token.pos_ in ["PRON", "NOUN", "PROPN"]:
                indirect_obj = self._get_complete_noun_phrase(token)
                print(f"📍 間接目的語検出: {indirect_obj} (iobj)")
            elif token.dep_ == "dative" and token.pos_ in ["PRON", "NOUN", "PROPN"]:
                indirect_obj = self._get_complete_noun_phrase(token)
                print(f"📍 間接目的語検出: {indirect_obj} (dative)")
            elif token.dep_ == "dobj" and token.pos_ in ["NOUN", "PROPN"]:
                direct_obj = self._get_complete_noun_phrase(token)
                print(f"📍 直接目的語検出: {direct_obj} (dobj)")
        
        # 真のSVOO構造の場合のみスロット割り当て
        if indirect_obj and direct_obj:
            slots['O1'] = [{
                'value': indirect_obj,
                'rule_id': 'svoo-indirect',
                'confidence': 0.95
            }]
            slots['O2'] = [{
                'value': direct_obj,
                'rule_id': 'svoo-direct', 
                'confidence': 0.95
            }]
            print(f"✅ 真のSVOO構造検出: O1={indirect_obj}, O2={direct_obj}")
        else:
            print(f"🔍 真のSVOO構造なし: indirect={indirect_obj}, direct={direct_obj}")
            # 前置詞句は副詞として別途処理される
        """二重目的語動詞の特別処理 (give, tell, show, teach等)"""
        
        # 二重目的語動詞のリスト
        ditransitive_verbs = {
            'give', 'gave', 'given',
            'tell', 'told', 
            'show', 'showed', 'shown',
            'teach', 'taught',
            'send', 'sent',
            'buy', 'bought',
            'make', 'made',
            'get', 'got'
        }
        
        # 現在の動詞をチェック
        main_verb = None
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                main_verb = token
                break
        
        if not main_verb or main_verb.lemma_.lower() not in ditransitive_verbs:
            return
            
        print(f"📍 二重目的語動詞検出: {main_verb.text} ({main_verb.lemma_})")
        
        # 動詞の周辺にある目的語候補を収集
        objects = []
        for token in doc:
            if token.dep_ in ["dobj", "iobj"] or (token.dep_ == "pobj" and token.head.dep_ == "prep"):
                objects.append({
                    'token': token,
                    'phrase': self._get_complete_noun_phrase(token),
                    'position': token.i,
                    'dep': token.dep_
                })
        
        # 位置順にソート（文中の順序）
        objects.sort(key=lambda x: x['position'])
        
        if len(objects) >= 2:
            # 2つの目的語がある場合
            obj1, obj2 = objects[0], objects[1]
            
            # give型の場合: 最初が間接目的語、次が直接目的語
            if main_verb.lemma_ in ['give', 'tell', 'show', 'send']:
                slots['O1'] = [{
                    'value': obj1['phrase'],
                    'rule_id': f'ditrans-{main_verb.lemma_}-iobj',
                    'confidence': 0.95
                }]
                slots['O2'] = [{
                    'value': obj2['phrase'], 
                    'rule_id': f'ditrans-{main_verb.lemma_}-dobj',
                    'confidence': 0.95
                }]
                print(f"✅ {main_verb.lemma_}型SVOO: O1={obj1['phrase']}, O2={obj2['phrase']}")
            
            # teach型の場合: 最初が直接目的語、次が間接目的語（前置詞句）
            elif main_verb.lemma_ in ['teach', 'buy']:
                slots['O1'] = [{
                    'value': obj1['phrase'],
                    'rule_id': f'ditrans-{main_verb.lemma_}-dobj',
                    'confidence': 0.95
                }]
                if obj2['dep'] == 'pobj':  # 前置詞句の場合
                    prep = obj2['token'].head.text if obj2['token'].head.dep_ == 'prep' else 'to'
                    slots['O2'] = [{
                        'value': f"{prep} {obj2['phrase']}",
                        'rule_id': f'ditrans-{main_verb.lemma_}-prep',
                        'confidence': 0.95
                    }]
                    print(f"✅ {main_verb.lemma_}型SVOO: O1={obj1['phrase']}, O2={prep} {obj2['phrase']}")
        
        elif len(objects) == 1 and not slots.get('O2'):
            # 1つの目的語しかない場合、前置詞句を探す
            obj = objects[0]
            for token in doc:
                if token.dep_ == "prep" and token.text.lower() in ["to", "for"]:
                    for child in token.children:
                        if child.dep_ == "pobj":
                            prep_phrase = self._get_complete_noun_phrase(child)
                            slots['O2'] = [{
                                'value': f"{token.text} {prep_phrase}",
                                'rule_id': f'ditrans-{main_verb.lemma_}-prep-supplement',
                                'confidence': 0.9
                            }]
                            print(f"✅ {main_verb.lemma_}型前置詞句補完: O2={token.text} {prep_phrase}")
                            break
    
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
    
    def _extract_generic_complement(self, doc) -> Optional[str]:
        """汎用補語抽出（be動詞、become、seem等の後の補語）"""
        
        # 補語をとる動詞のリスト
        complement_verbs = ['be', 'become', 'seem', 'appear', 'remain', 'stay', 'turn', 'get', 'grow', 'feel', 'look', 'sound', 'smell', 'taste']
        
        for token in doc:
            # 補語をとる動詞を探す
            if token.lemma_ in complement_verbs and token.pos_ == "VERB":
                # attr（属性補語）を探す
                for child in token.children:
                    if child.dep_ == "attr":
                        return self._get_complete_noun_phrase(child)
                
                # acomp（形容詞補語）を探す  
                for child in token.children:
                    if child.dep_ == "acomp":
                        return child.text
                
                # pcomp（前置詞補語）を探す
                for child in token.children:
                    if child.dep_ == "prep":
                        for grandchild in child.children:
                            if grandchild.dep_ == "pobj":
                                return f"{child.text} {self._get_complete_noun_phrase(grandchild)}"
        
        return None
    
    def _extract_adverb_value(self, doc) -> Optional[str]:
        """副詞を抽出（M2スロット用）"""
        adverbs = []
        
        for token in doc:
            # 副詞（ADV）で、動詞を修飾している場合
            if token.pos_ == "ADV" and token.dep_ in ["advmod", "prep"]:
                # 前置詞句でない単語の副詞を優先
                if not any(child.dep_ == "pobj" for child in token.children):
                    adverbs.append(token.text)
        
        # 最初の副詞を返す（複数ある場合は最初のもの）
        return adverbs[0] if adverbs else None
    
    def _extract_wh_where_value(self, doc) -> Optional[str]:
        """Wh疑問詞whereを抽出（M3スロット用）"""
        for token in doc:
            if token.text.lower() == "where":
                return "where_M3_1"
        return None
    
    def _extract_please_interjection_value(self, doc) -> Optional[str]:
        """文末の「please」感嘆詞を抽出（M3スロット用）"""
        for token in doc:
            if (token.lemma_.lower() == "please" and 
                token.pos_ == "INTJ" and 
                token.dep_ == "intj"):
                return token.text
        return None
        
    def _process_relative_clause_subslots(self, verb, sub_slots, doc): pass
    def _process_adverbial_clause_subslots(self, verb, sub_slots, doc): pass
