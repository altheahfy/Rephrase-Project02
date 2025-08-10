#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rule Dictionary v2.0 - O1(直接目的語)サブスロット生成システム
spaCy依存構造解析による動的サブスロット抽出

直接目的語の複雑構造パターン:
1. 関係代名詞付き目的語: "The book that you recommended" → sub-o1: 'The book that', sub-v: 'recommended'
2. 同格that節: "The fact that he left" → sub-s: 'The fact that he', sub-v: 'left'  
3. 不定詞目的語: "To go home" → sub-v: 'To go', sub-o1: 'home'
4. 動名詞目的語: "Reading books" → sub-v: 'Reading', sub-o1: 'books'
5. 複合目的語: "apples and oranges" → word扱い (V構造なし)
"""

import spacy
from typing import Dict, List, Tuple, Any

class O1SubslotGenerator:
    """O1(直接目的語)サブスロット生成クラス"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def generate_o1_subslots(self, slot_phrase: str, phrase_type: str) -> Dict[str, Dict[str, Any]]:
        """
        O1(直接目的語)スロットのサブスロット生成
        
        Args:
            slot_phrase: 目的語フレーズ
            phrase_type: フレーズタイプ (word/phrase/clause)
            
        Returns:
            Dict: サブスロット辞書
        """
        doc = self.nlp(slot_phrase)
        
        if phrase_type == "word":
            # 単語の場合はサブスロット分解不要
            return {}
        elif phrase_type == "phrase":
            return self._extract_o1_phrase_subslots(doc)
        elif phrase_type == "clause":
            return self._extract_o1_clause_subslots(doc)
        else:
            return {}
    
    def _extract_o1_phrase_subslots(self, doc):
        """O1 Phraseサブスロット抽出"""
        subslots = {}
        
        # 関係代名詞の検出（より柔軟な条件）
        rel_pronouns = ["who", "whom", "whose", "which", "that"]
        rel_pronoun_token = None
        
        for token in doc:
            if token.text.lower() in rel_pronouns:
                # 関係代名詞の条件を緩和：nsubj以外も検出
                if token.dep_ in ["nsubj", "dobj", "pobj", "nsubjpass"] or token.pos_ == "PRON":
                    rel_pronoun_token = token
                    break
        
        if rel_pronoun_token:
            subslots.update(self._extract_relative_clause_subslots(doc, rel_pronoun_token))
        
        # 不定詞主語の処理: "To learn English is important"
        elif doc[0].text.lower() == "to" and doc[0].pos_ == "PART":
            subslots.update(self._extract_infinitive_subject_subslots(doc))
        
        # 動名詞主語の処理: "Reading books is fun"
        else:
            gerund_tokens = [token for token in doc if token.pos_ == "VERB" and token.tag_ == "VBG"]
            if gerund_tokens:
                subslots.update(self._extract_gerund_subject_subslots(doc, gerund_tokens[0]))
        
        # 複合主語の処理: "John and Mary are here"
        and_tokens = [token for token in doc if token.text.lower() == "and" and token.dep_ == "cc"]
        if and_tokens:
            subslots.update(self._extract_compound_subject_subslots(doc))
        
        # 位置ベース修飾語割り当て（sub-m1, sub-m2, sub-m3）
        modifier_subslots = self._assign_modifiers_by_position(doc)
        subslots.update(modifier_subslots)
        
        # sub-aux: 助動詞検出 (aux, auxpass)
        aux_tokens = [token for token in doc if token.dep_ in ["aux", "auxpass"]]
        if aux_tokens:
            aux_text = ' '.join([token.text for token in aux_tokens])
            subslots['sub-aux'] = {
                'text': aux_text,
                'tokens': [token.text for token in aux_tokens],
                'token_indices': [token.i for token in aux_tokens]
            }
            print(f"✅ sub-auxとして処理: '{aux_text}'")
        
        # sub-c2: 補語2検出 (xcomp, acomp, attr, ccomp)
        comp_tokens = [token for token in doc if token.dep_ in ["xcomp", "acomp", "attr", "ccomp"]]
        if comp_tokens:
            comp_text = ' '.join([token.text for token in comp_tokens])
            subslots['sub-c2'] = {
                'text': comp_text,
                'tokens': [token.text for token in comp_tokens],
                'token_indices': [token.i for token in comp_tokens]
            }
            print(f"✅ sub-c2として処理: '{comp_text}'")
        
        # sub-o1追加検出: nsubjが補語構造内にある場合
        nsubj_tokens = [token for token in doc if token.dep_ == "nsubj" and token.head.dep_ in ["ccomp", "xcomp"]]
        if nsubj_tokens and 'sub-o1' not in subslots:
            nsubj_text = ' '.join([token.text for token in nsubj_tokens])
            subslots['sub-o1'] = {
                'text': nsubj_text,
                'tokens': [token.text for token in nsubj_tokens],
                'token_indices': [token.i for token in nsubj_tokens]
            }
            print(f"✅ sub-o1として処理: '{nsubj_text}' (補語構造内主語)")
        

        
        # TODO: 完全な10個サブスロット検出を実装予定
        # complete_subslots = self._detect_all_subslots(doc)
        # subslots.update(complete_subslots)
        
        return subslots
    
    def _extract_o1_clause_subslots(self, doc):
        """O1 Clauseサブスロット抽出"""
        subslots = {}
        
        # 位置ベース修飾語割り当て
        modifier_subslots = self._assign_modifiers_by_position(doc)
        subslots.update(modifier_subslots)
        
        # sub-aux: 助動詞検出
        aux_tokens = [token for token in doc if token.dep_ == "aux"]
        if aux_tokens:
            aux_text = ' '.join([token.text for token in aux_tokens])
            subslots['sub-aux'] = {
                'text': aux_text,
                'tokens': [token.text for token in aux_tokens],
                'token_indices': [token.i for token in aux_tokens]
            }
            print(f"✅ sub-auxとして処理: '{aux_text}'")
        
        # まず同格that節を優先チェック
        that_token = None
        for token in doc:
            if token.text.lower() == "that":
                # that節の検出条件を広げる
                if token.dep_ in ["acl", "ccomp", "mark", "dobj"] or (token.pos_ == "SCONJ"):
                    that_token = token
                    break
        
        if that_token:
            # 同格that節かどうかを判定（名詞の後にthatがある場合）
            has_noun_before = False
            for token in doc:
                if token.i < that_token.i and token.pos_ in ["NOUN", "PROPN"]:
                    has_noun_before = True
                    break
            
            if has_noun_before:
                return self._extract_appositive_that_clause_subslots(doc, that_token)
        
        # 疑問詞節の検出（what, where, when, how など）
        wh_words = ["what", "where", "when", "how", "why", "which"]
        wh_word_token = None
        
        for token in doc:
            if token.text.lower() in wh_words:
                # 疑問詞の条件：dobj, advmod, nsubj などの関係
                if token.dep_ in ["dobj", "advmod", "nsubj", "pobj"] or token.pos_ in ["PRON", "SCONJ"]:
                    wh_word_token = token
                    break
        
        if wh_word_token:
            return self._extract_wh_clause_subslots(doc, wh_word_token)
        
        # 関係代名詞の検出（clause内）
        rel_pronouns = ["who", "whom", "whose", "which", "that"]
        rel_pronoun_token = None
        
        for token in doc:
            if token.text.lower() in rel_pronouns:
                rel_pronoun_token = token
                break
        
        if rel_pronoun_token:
            return self._extract_relative_clause_s_subslots(doc, rel_pronoun_token)
        
        # その他の関係節処理
        complex_subslots = self._extract_complex_s_clause(doc)
        subslots.update(complex_subslots)
        
        # TODO: 完全な10個サブスロット検出を実装予定
        # complete_subslots = self._detect_all_subslots(doc)
        # subslots.update(complete_subslots)
        
        return subslots
    
    def _extract_wh_clause_subslots(self, doc, wh_word_token):
        """疑問詞節のサブスロット抽出（what you said など）"""
        subslots = {}
        
        # 疑問詞節の構造解析: what(dobj) you(nsubj) said(ROOT)
        verb_token = None
        subject_tokens = []
        
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                verb_token = token
            elif token.dep_ in ["nsubj", "nsubjpass"]:
                subject_tokens.append(token)
        
        if verb_token and subject_tokens:
            # sub-o1: 疑問詞
            subslots['sub-o1'] = {
                'text': wh_word_token.text,
                'tokens': [wh_word_token.text],
                'token_indices': [wh_word_token.i]
            }
            
            # sub-s: 主語
            subject_text = ' '.join([t.text for t in subject_tokens])
            subslots['sub-s'] = {
                'text': subject_text,
                'tokens': [t.text for t in subject_tokens],
                'token_indices': [t.i for t in subject_tokens]
            }
            
            # sub-v: 動詞
            subslots['sub-v'] = {
                'text': verb_token.text,
                'tokens': [verb_token.text],
                'token_indices': [verb_token.i]
            }
        
        return subslots
    
    def _extract_relative_clause_s_subslots(self, doc, rel_pronoun_token):
        """関係代名詞を含むS Clauseのサブスロット抽出"""
        subslots = {}
        
        # 関係代名詞の前の名詞句を特定
        noun_phrase_tokens = []
        for token in doc:
            if token.i < rel_pronoun_token.i:
                noun_phrase_tokens.append(token)
        
        # 関係代名詞の役割を判定
        rel_verb = None
        for token in doc:
            if token.i > rel_pronoun_token.i and token.pos_ == "VERB":
                rel_verb = token
                break
        
        if rel_verb:
            # 関係代名詞が目的語の場合 (whom)
            if rel_pronoun_token.text.lower() == "whom":
                # sub-o1: 名詞句 + whom
                if noun_phrase_tokens:
                    noun_phrase_text = ' '.join([t.text for t in noun_phrase_tokens])
                    subslots['sub-o1'] = {
                        'text': f"{noun_phrase_text} {rel_pronoun_token.text}",
                        'tokens': [t.text for t in noun_phrase_tokens] + [rel_pronoun_token.text],
                        'token_indices': [t.i for t in noun_phrase_tokens] + [rel_pronoun_token.i]
                    }
            else:
                # 関係代名詞が主語の場合 (who)
                if noun_phrase_tokens:
                    noun_phrase_text = ' '.join([t.text for t in noun_phrase_tokens])
                    subslots['sub-s'] = {
                        'text': f"{noun_phrase_text} {rel_pronoun_token.text}",
                        'tokens': [t.text for t in noun_phrase_tokens] + [rel_pronoun_token.text],
                        'token_indices': [t.i for t in noun_phrase_tokens] + [rel_pronoun_token.i]
                    }
            
            # sub-v: 関係節内動詞
            subslots['sub-v'] = {
                'text': rel_verb.text,
                'tokens': [rel_verb.text],
                'token_indices': [rel_verb.i]
            }
            
            # sub-s: 関係節内主語 (whomの場合)
            subjects = [child for child in rel_verb.children if child.dep_ == "nsubj"]
            if subjects and rel_pronoun_token.text.lower() == "whom":
                subslots['sub-s'] = {
                    'text': subjects[0].text,
                    'tokens': [subjects[0].text],
                    'token_indices': [subjects[0].i]
                }
        
        return subslots
    
    def _extract_relative_clause_subslots(self, doc, rel_pronoun_token):
        """関係代名詞付き主語のサブスロット抽出"""
        subslots = {}
        
        # 関係代名詞の前にある名詞句を特定
        noun_phrase_tokens = []
        for token in doc:
            if token.i < rel_pronoun_token.i:
                noun_phrase_tokens.append(token)
        
        if noun_phrase_tokens:
            # sub-s: 名詞句 + 関係代名詞
            noun_phrase_text = ' '.join([t.text for t in noun_phrase_tokens])
            subslots['sub-s'] = {
                'text': f"{noun_phrase_text} {rel_pronoun_token.text}",
                'tokens': [t.text for t in noun_phrase_tokens] + [rel_pronoun_token.text],
                'token_indices': [t.i for t in noun_phrase_tokens] + [rel_pronoun_token.i]
            }
        
        # 関係節内の動詞を特定
        rel_clause_verb = None
        for token in doc:
            if token.i > rel_pronoun_token.i and token.pos_ == "VERB":
                rel_clause_verb = token
                break
        
        if rel_clause_verb:
            # sub-v: 関係節内動詞
            subslots['sub-v'] = {
                'text': rel_clause_verb.text,
                'tokens': [rel_clause_verb.text],
                'token_indices': [rel_clause_verb.i]
            }
            
            # 関係節内の主語を処理
            subjects = [child for child in rel_clause_verb.children if child.dep_ == "nsubj"]
            if subjects:
                # sub-s: 関係節内主語 (例: "The man whom I met" の "I")
                if 'sub-s' not in subslots:  # 既にsub-sがある場合は上書きしない
                    subslots['sub-s2'] = {  # 追加の主語として処理
                        'text': subjects[0].text,
                        'tokens': [subjects[0].text],
                        'token_indices': [subjects[0].i]
                    }
            
            # sub-o1: 関係節内目的語
            objects = [child for child in rel_clause_verb.children if child.dep_ == "dobj"]
            if objects:
                subslots['sub-o1'] = {
                    'text': objects[0].text,
                    'tokens': [objects[0].text],
                    'token_indices': [objects[0].i]
                }
        
        return subslots
    
    def _extract_infinitive_subject_subslots(self, doc):
        """不定詞主語のサブスロット抽出"""
        subslots = {}
        
        # "To learn English" の処理
        to_token = doc[0]  # "to"
        main_verb = None
        
        for token in doc[1:]:
            if token.pos_ == "VERB":
                main_verb = token
                break
        
        if main_verb:
            # sub-v: "to + 動詞" (Rephraseルール: 不定詞統合)
            subslots['sub-v'] = {
                'text': f"{to_token.text} {main_verb.text}",
                'tokens': [to_token.text, main_verb.text],
                'token_indices': [to_token.i, main_verb.i]
            }
            
            # sub-o1: 不定詞の目的語
            objects = [child for child in main_verb.children if child.dep_ == "dobj"]
            if objects:
                subslots['sub-o1'] = {
                    'text': objects[0].text,
                    'tokens': [objects[0].text],
                    'token_indices': [objects[0].i]
                }
        
        return subslots
    
    def _extract_gerund_subject_subslots(self, doc, gerund_token):
        """動名詞主語のサブスロット抽出"""
        subslots = {}
        
        # sub-v: 動名詞 (読む動作なので動詞として処理)
        subslots['sub-v'] = {
            'text': gerund_token.text,
            'tokens': [gerund_token.text],
            'token_indices': [gerund_token.i]
        }
        
        # sub-o1: 動名詞の目的語
        objects = [child for child in gerund_token.children if child.dep_ == "dobj"]
        if objects:
            subslots['sub-o1'] = {
                'text': objects[0].text,
                'tokens': [objects[0].text],
                'token_indices': [objects[0].i]
            }
        
        return subslots
    
    def _extract_compound_subject_subslots(self, doc):
        """複合主語のサブスロット抽出"""
        subslots = {}
        
        # "John and Mary" はV構造が無いのでサブスロット分解不要
        # wordタイプとして処理すべき
        return subslots
    
    def _extract_appositive_that_clause_subslots(self, doc, that_token):
        """同格that節のサブスロット抽出"""
        subslots = {}
        
        # that節の前の名詞句を特定（冠詞も含める）
        noun_phrase_tokens = []
        main_noun = None
        for token in doc:
            if token.i < that_token.i:
                if token.pos_ in ["NOUN", "PROPN"]:
                    main_noun = token
                elif token.pos_ == "DET" and not noun_phrase_tokens:
                    # 冠詞から名詞句の開始
                    noun_phrase_tokens.append(token)
        
        if main_noun:
            # 冠詞がある場合は含める
            if noun_phrase_tokens:
                noun_phrase_tokens.append(main_noun)
            else:
                noun_phrase_tokens = [main_noun]
        
        # that節内の主語を特定
        that_clause_subj = None
        that_clause_verb = None
        
        # まず動詞を見つけて、その主語を探す
        for token in doc:
            if token.i > that_token.i and token.pos_ == "VERB":
                that_clause_verb = token
                # その動詞の主語を探す
                subjects = [child for child in token.children if child.dep_ == "nsubj"]
                if subjects:
                    that_clause_subj = subjects[0]
                break
        
        if noun_phrase_tokens and that_clause_subj:
            # sub-s: 名詞句 + that + 主語 (Rephraseルール: 同格節統合)
            noun_phrase_text = ' '.join([t.text for t in noun_phrase_tokens])
            subslots['sub-s'] = {
                'text': f"{noun_phrase_text} that {that_clause_subj.text}",
                'tokens': [t.text for t in noun_phrase_tokens] + [that_token.text, that_clause_subj.text],
                'token_indices': [t.i for t in noun_phrase_tokens] + [that_token.i, that_clause_subj.i]
            }
        elif noun_phrase_tokens:
            # 主語が見つからない場合はthatまでを含める
            noun_phrase_text = ' '.join([t.text for t in noun_phrase_tokens])
            subslots['sub-s'] = {
                'text': f"{noun_phrase_text} that",
                'tokens': [t.text for t in noun_phrase_tokens] + [that_token.text],
                'token_indices': [t.i for t in noun_phrase_tokens] + [that_token.i]
            }
        
        # that節内の動詞を処理（すべてのケースで実行）
        if that_clause_verb:
            # sub-v: that節内動詞
            subslots['sub-v'] = {
                'text': that_clause_verb.text,
                'tokens': [that_clause_verb.text],
                'token_indices': [that_clause_verb.i]
            }
        
        return subslots
    
    def _extract_complex_s_clause(self, doc):
        """複雑なS節構造の処理"""
        subslots = {}
        # 必要に応じて複雑な関係節等の処理を実装
        return subslots
    
    def calculate_coverage(self, subslots: Dict, doc) -> Tuple[float, List[Tuple[str, int]]]:
        """カバレッジ計算"""
        covered_indices = set()
        for subslot_data in subslots.values():
            covered_indices.update(subslot_data['token_indices'])
        
        total_tokens = len(doc)
        covered_tokens = len(covered_indices)
        coverage = (covered_tokens / total_tokens) * 100 if total_tokens > 0 else 0
        
        # 未配置トークンの特定
        uncovered = []
        for token in doc:
            if token.i not in covered_indices:
                uncovered.append((token.text, token.i))
        
        return coverage, uncovered

    def _detect_all_subslots(self, doc):
        """完全な10個サブスロット検出エンジン"""
        subslots = {}
        
        for token in doc:
            # 既存の処理と重複しないように、新たに必要なサブスロットのみ検出
            
            # sub-m1: 前置修飾語 (形容詞、決定詞など)
            if token.dep_ in ["amod", "det", "nummod", "compound"] and 'sub-m1' not in subslots:
                subslots['sub-m1'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-m1検出: '{token.text}' (dep: {token.dep_})")
            
            # sub-aux: 助動詞
            elif token.dep_ == "aux" and 'sub-aux' not in subslots:
                subslots['sub-aux'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-aux検出: '{token.text}'")
            
            # sub-c1: 補語1 (attr, acomp)
            elif token.dep_ in ["attr", "acomp"] and 'sub-c1' not in subslots:
                subslots['sub-c1'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-c1検出: '{token.text}' (dep: {token.dep_})")
            
            # sub-o2: 間接目的語
            elif token.dep_ == "iobj" and 'sub-o2' not in subslots:
                subslots['sub-o2'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-o2検出: '{token.text}'")
            
            # sub-c2: 補語2 (xcomp, ccomp)
            elif token.dep_ in ["xcomp", "ccomp"] and 'sub-c2' not in subslots:
                subslots['sub-c2'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-c2検出: '{token.text}' (dep: {token.dep_})")
            
            # sub-m3: 後置修飾語 (prep, acl, relcl)
            elif token.dep_ in ["prep", "acl", "relcl"] and 'sub-m3' not in subslots:
                # 前置詞句全体を取得
                prep_phrase_tokens = [token]
                if token.dep_ == "prep":
                    # 前置詞句の目的語も含める
                    for child in token.children:
                        if child.dep_ == "pobj":
                            prep_phrase_tokens.append(child)
                
                prep_phrase_text = ' '.join([t.text for t in prep_phrase_tokens])
                subslots['sub-m3'] = {
                    'text': prep_phrase_text,
                    'tokens': [t.text for t in prep_phrase_tokens],
                    'token_indices': [t.i for t in prep_phrase_tokens]
                }
                print(f"🔍 sub-m3検出: '{prep_phrase_text}' (dep: {token.dep_})")
        
        return subslots
    
    def _assign_modifiers_by_position(self, doc):
        """位置ベースで修飾語をsub-m1, sub-m2, sub-m3に割り当て"""
        subslots = {}
        
        # 修飾語候補を収集
        modifier_candidates = []
        
        # advmod（副詞修飾語）
        advmod_tokens = [token for token in doc if token.dep_ == "advmod"]
        for token in advmod_tokens:
            modifier_candidates.append({
                'token': token,
                'text': token.text,
                'position': token.i,
                'type': 'advmod'
            })
        
        # 前置詞句 (prep + pobj)
        prep_tokens = [token for token in doc if token.dep_ in ["prep", "dative"]]
        for prep_token in prep_tokens:
            prep_phrase_tokens = [prep_token]
            prep_phrase_text = prep_token.text
            
            # 前置詞句の目的語も含める
            for child in prep_token.children:
                if child.dep_ == "pobj":
                    prep_phrase_tokens.append(child)
                    prep_phrase_text += " " + child.text
            
            modifier_candidates.append({
                'tokens': prep_phrase_tokens,
                'text': prep_phrase_text,
                'position': prep_token.i,
                'type': 'prep_phrase'
            })
        
        # det/amod（限定詞/形容詞修飾語）
        det_amod_tokens = [token for token in doc if token.dep_ in ["det", "amod"]]
        for token in det_amod_tokens:
            modifier_candidates.append({
                'token': token,
                'text': token.text,
                'position': token.i,
                'type': 'det_amod'
            })
        
        # 位置順でソート
        modifier_candidates.sort(key=lambda x: x['position'])
        
        if not modifier_candidates:
            return subslots
        
        # 文長を取得
        sentence_length = len(doc)
        
        # 位置ベースで割り当て
        for i, modifier in enumerate(modifier_candidates):
            # 相対位置を計算（0.0-1.0）
            relative_pos = modifier['position'] / sentence_length if sentence_length > 1 else 0.5
            
            # 位置に基づいてM slot を決定
            if relative_pos <= 0.33:  # 文頭1/3
                slot_name = 'sub-m1'
            elif relative_pos <= 0.67:  # 文中央1/3
                slot_name = 'sub-m2'
            else:  # 文尾1/3
                slot_name = 'sub-m3'
            
            # 既に同じslotが埋まっている場合は次のslotへ
            if slot_name in subslots:
                if slot_name == 'sub-m1':
                    slot_name = 'sub-m2' if 'sub-m2' not in subslots else 'sub-m3'
                elif slot_name == 'sub-m2':
                    slot_name = 'sub-m3' if 'sub-m3' not in subslots else 'sub-m1'
                # sub-m3の場合はそのまま上書き
            
            # sub slot に割り当て
            if 'tokens' in modifier:
                # 前置詞句の場合
                subslots[slot_name] = {
                    'text': modifier['text'],
                    'tokens': [t.text for t in modifier['tokens']],
                    'token_indices': [t.i for t in modifier['tokens']]
                }
            else:
                # 単独トークンの場合
                subslots[slot_name] = {
                    'text': modifier['text'],
                    'tokens': [modifier['token'].text],
                    'token_indices': [modifier['token'].i]
                }
            
            print(f"✅ {slot_name}として割り当て: '{modifier['text']}' (位置: {relative_pos:.2f}, {modifier['type']})")
        
        return subslots


def test_o1_subslots():
    """テスト用関数"""
    test_cases = [
        ("apple", "word"),
        ("car", "word"),
        ("apples and oranges", "word"),
        ("the book that you recommended", "clause"),
        ("the big red car that must have been made very carefully", "clause"),
        ("what you said yesterday at the meeting", "clause"),
        ("making her crazy for him", "clause"),
        ("to make the project successful", "phrase"),
        ("running very fast in the park", "phrase"),
        ("books on the table in the library", "phrase"),
        ("students studying abroad this year", "phrase"),
        ("home", "word")
    ]
    
    generator = O1SubslotGenerator()
    
    print("=== O1サブスロット生成テスト ===")
    
    for i, (slot_phrase, phrase_type) in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"O1 SlotPhrase: '{slot_phrase}'")
        print(f"PhraseType: {phrase_type}")
        print(f"{'='*50}")
        
        try:
            subslots = generator.generate_o1_subslots(slot_phrase, phrase_type)
            
            if not subslots:
                print(f"判定: {phrase_type}タイプ：サブスロット分解不要")
            else:
                print(f"✅ サブスロット抽出成功:")
                for sub_name, sub_data in subslots.items():
                    print(f"  {sub_name}: '{sub_data['text']}'")
                
                # カバレッジ計算
                import spacy
                nlp = spacy.load("en_core_web_sm")
                doc = nlp(slot_phrase)
                coverage_pct, uncovered_tokens = generator.calculate_coverage(subslots, doc)
                print(f"\n📊 カバレッジ: {coverage_pct:.1f}%")
                if uncovered_tokens:
                    uncovered_text = [token for token, _ in uncovered_tokens]
                    print(f"未カバー: {uncovered_text}")
        
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_o1_subslots()
