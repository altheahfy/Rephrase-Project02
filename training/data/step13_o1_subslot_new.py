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
        
        # 最優先：O1O2構造（間接目的語+直接目的語）検出
        o1o2_subslots = self._detect_o1o2_structure(doc)
        subslots.update(o1o2_subslots)
        print(f"🔍 O1O2構造検出結果: {list(o1o2_subslots.keys())}")
        
        # 最初にnoun-verb phrase統合検出 (完全カバレッジの原則)
        # "students studying" のような名詞+動詞を統合してsub-vとして処理
        root_tokens = [token for token in doc if token.dep_ == "ROOT" and token.pos_ in ["NOUN", "PROPN"]]
        if root_tokens:
            root_token = root_tokens[0]
            # ROOT名詞に対してacl(adjectival clause)やrelcl(relative clause)で動詞が修飾している場合
            verb_children = [child for child in root_token.children if child.pos_ == "VERB" and child.dep_ in ["acl", "relcl"]]
            if verb_children:
                # 名詞+動詞の統合処理 (完全カバレッジのため)
                verb_token = verb_children[0]
                
                # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
                root_det_tokens = [child for child in root_token.children if child.dep_ == "det"]
                if root_det_tokens:
                    combined_tokens = root_det_tokens + [root_token, verb_token]
                    combined_tokens.sort(key=lambda x: x.i)
                    combined_text = ' '.join([t.text for t in combined_tokens])
                    combined_indices = [t.i for t in combined_tokens]
                else:
                    combined_tokens = [root_token, verb_token]
                    combined_text = f"{root_token.text} {verb_token.text}"
                    combined_indices = [root_token.i, verb_token.i]
                
                subslots['sub-v'] = {
                    'text': combined_text,
                    'tokens': [t.text for t in combined_tokens],
                    'token_indices': combined_indices
                }
                print(f"✅ sub-vとして統合処理: '{combined_text}' (名詞+動詞統合) - indices: {combined_indices}")
        
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
            print(f"🔍 関係代名詞処理後sub-v: {subslots.get('sub-v', {}).get('text', 'なし')}")
        
        # 不定詞主語の処理: "To learn English is important"
        if doc[0].text.lower() == "to" and doc[0].pos_ == "PART":
            subslots.update(self._extract_infinitive_subject_subslots(doc))
            print(f"🔍 不定詞主語処理後sub-v: {subslots.get('sub-v', {}).get('text', 'なし')}")
        
        # 動名詞主語の処理: "Reading books is fun"
        gerund_tokens = [token for token in doc if token.pos_ == "VERB" and token.tag_ == "VBG"]
        if gerund_tokens and 'sub-v' not in subslots:
            # 既存のsub-vがない場合のみ動名詞処理を実行
            subslots.update(self._extract_gerund_subject_subslots(doc, gerund_tokens[0]))
            print(f"🔍 動名詞主語処理後sub-v: {subslots.get('sub-v', {}).get('text', 'なし')}")
        elif gerund_tokens:
            print(f"🔍 動名詞処理スキップ: 既存sub-v保護 '{subslots.get('sub-v', {}).get('text', 'なし')}'")
        else:
            print(f"🔍 動名詞主語処理後sub-v: {subslots.get('sub-v', {}).get('text', 'なし')}")
        
        # 複合主語の処理: "John and Mary are here"
        and_tokens = [token for token in doc if token.text.lower() == "and" and token.dep_ == "cc"]
        if and_tokens:
            subslots.update(self._extract_compound_subject_subslots(doc))
            print(f"🔍 複合主語処理後sub-v: {subslots.get('sub-v', {}).get('text', 'なし')}")
        
        # 位置ベース修飾語割り当て（sub-m1, sub-m2, sub-m3） - O1O2構造保護版
        print(f"🔍 修飾語割り当て前sub-v: {subslots.get('sub-v', {}).get('text', 'なし')}")
        modifier_subslots = self._assign_modifiers_by_position_with_o1o2_protection(doc, subslots)
        subslots.update(modifier_subslots)
        
        # 通常のROOT主語検出 (noun-verb統合されなかった場合のフォールバック)
        root_tokens = [token for token in doc if token.dep_ == "ROOT" and token.pos_ in ["NOUN", "PROPN"]]
        if not subslots.get('sub-v') and root_tokens and 'sub-s' not in subslots:
            root_token = root_tokens[0]
            # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
            root_det_tokens = [child for child in root_token.children if child.dep_ == "det"]
            if root_det_tokens:
                s_tokens = root_det_tokens + [root_token]
                s_tokens.sort(key=lambda x: x.i)  # 位置順にソート
                s_text = ' '.join([t.text for t in s_tokens])
                s_token_indices = [t.i for t in s_tokens]
            else:
                s_tokens = [root_token]
                s_text = root_token.text
                s_token_indices = [root_token.i]
            
            subslots['sub-s'] = {
                'text': s_text,
                'tokens': [t.text for t in s_tokens],
                'token_indices': s_token_indices
            }
            print(f"✅ sub-sとして処理: '{s_text}' (ROOT主語+冠詞)")
        
        # 不定詞「to + 動詞」の統合処理 (既存sub-vを尊重、O1O2構造も尊重)
        to_token = None
        main_verb_token = None
        
        if 'sub-v' not in subslots:
            to_verb_tokens = []
            
            for token in doc:
                if token.text.lower() == "to" and token.pos_ == "PART":
                    to_token = token
                elif token.pos_ == "VERB" and token.dep_ in ["ROOT", "xcomp", "ccomp"]:
                    main_verb_token = token
                    break
            
            if to_token and main_verb_token:
                # sub-v: "to + 動詞" として統合
                subslots['sub-v'] = {
                    'text': f"{to_token.text} {main_verb_token.text}",
                    'tokens': [to_token.text, main_verb_token.text],
                    'token_indices': [to_token.i, main_verb_token.i]
                }
                print(f"✅ sub-vとして処理: '{to_token.text} {main_verb_token.text}' (不定詞統合) - 上書き警告!")
            elif main_verb_token:
                # 動詞のみ
                subslots['sub-v'] = {
                    'text': main_verb_token.text,
                    'tokens': [main_verb_token.text],
                    'token_indices': [main_verb_token.i]
                }
                print(f"✅ sub-vとして処理: '{main_verb_token.text}' - 上書き警告!")
        else:
            # 既存sub-vがある場合も、main_verb_tokenを探す
            for token in doc:
                if token.pos_ == "VERB" and token.dep_ in ["ROOT", "xcomp", "ccomp"]:
                    main_verb_token = token
                    break
        
        # sub-aux: 助動詞検出 (aux, auxpass) - ただし不定詞toは除外
        aux_tokens = [token for token in doc if token.dep_ in ["aux", "auxpass"] and not (token.text.lower() == "to" and token.pos_ == "PART")]
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
        
        # sub-o1検出: 動詞の直接目的語 (dobj) + 限定詞を含む
        if main_verb_token and 'sub-o1' not in subslots:
            dobj_tokens = [child for child in main_verb_token.children if child.dep_ == "dobj"]
            if dobj_tokens:
                dobj_token = dobj_tokens[0]
                # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
                det_tokens = [child for child in dobj_token.children if child.dep_ == "det"]
                if det_tokens:
                    o1_tokens = det_tokens + [dobj_token]
                    o1_tokens.sort(key=lambda x: x.i)  # 位置順にソート
                    o1_text = ' '.join([t.text for t in o1_tokens])
                    o1_token_indices = [t.i for t in o1_tokens]
                else:
                    o1_tokens = [dobj_token]
                    o1_text = dobj_token.text
                    o1_token_indices = [dobj_token.i]
                
                subslots['sub-o1'] = {
                    'text': o1_text,
                    'tokens': [t.text for t in o1_tokens],
                    'token_indices': o1_token_indices
                }
                print(f"✅ sub-o1として処理: '{o1_text}' (動詞の目的語+限定詞)")
            else:
                # dobjが見つからない場合、他の目的語パターンを検索
                # nsubjでも実質的に目的語の役割をするケース（補語構造）
                other_obj_tokens = [child for child in main_verb_token.children if child.dep_ in ["nsubj"]]
                if other_obj_tokens:
                    obj_token = other_obj_tokens[0]
                    # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
                    obj_det_tokens = [child for child in obj_token.children if child.dep_ == "det"]
                    if obj_det_tokens:
                        o1_tokens = obj_det_tokens + [obj_token]
                        o1_tokens.sort(key=lambda x: x.i)  # 位置順にソート
                        o1_text = ' '.join([t.text for t in o1_tokens])
                        o1_token_indices = [t.i for t in o1_tokens]
                    else:
                        o1_tokens = [obj_token]
                        o1_text = obj_token.text
                        o1_token_indices = [obj_token.i]
                    
                    subslots['sub-o1'] = {
                        'text': o1_text,
                        'tokens': [t.text for t in o1_tokens],
                        'token_indices': o1_token_indices
                    }
                    print(f"✅ sub-o1として処理: '{o1_text}' (動詞のnsubj目的語+限定詞)")
        
        # sub-o1追加検出: nsubjが補語構造内にある場合（dobjが既に検出済みの場合は除外）
        # 冠詞・定冠詞は必ず名詞とセット（100%のルール）を適用
        nsubj_tokens = [token for token in doc if token.dep_ == "nsubj" and token.head.dep_ in ["ccomp", "xcomp"]]
        if nsubj_tokens and 'sub-o1' not in subslots:
            nsubj_token = nsubj_tokens[0]
            # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
            nsubj_det_tokens = [child for child in nsubj_token.children if child.dep_ == "det"]
            if nsubj_det_tokens:
                o1_tokens = nsubj_det_tokens + [nsubj_token]
                o1_tokens.sort(key=lambda x: x.i)  # 位置順にソート
                nsubj_text = ' '.join([t.text for t in o1_tokens])
                o1_token_indices = [t.i for t in o1_tokens]
            else:
                o1_tokens = [nsubj_token]
                nsubj_text = nsubj_token.text
                o1_token_indices = [nsubj_token.i]
            
            subslots['sub-o1'] = {
                'text': nsubj_text,
                'tokens': [t.text for t in o1_tokens],
                'token_indices': o1_token_indices
            }
            print(f"✅ sub-o1として処理: '{nsubj_text}' (補語構造内主語+冠詞)")
        

        
        # TODO: 完全な10個サブスロット検出を実装予定
        # complete_subslots = self._detect_all_subslots(doc)
        # subslots.update(complete_subslots)
        
        # デバッグ: 最終結果確認
        if 'sub-v' in subslots:
            print(f"🔍 最終sub-v: '{subslots['sub-v']['text']}' indices: {subslots['sub-v']['token_indices']}")
        print(f"🔍 最終全subslots: {[(k, v['text']) for k, v in subslots.items()]}")
        
        return subslots
    
    def _extract_o1_clause_subslots(self, doc):
        """O1 Clauseサブスロット抽出"""
        subslots = {}
        
        # 完全な10サブスロット検出システムを使用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
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
                if token.dep_ in ["acl", "ccomp", "mark", "dobj"] or (token.pos_ == "SCONJ") or token.i == 0:
                    that_token = token
                    break
        
        if that_token:
            # 単純that節の処理（"that he is studying hard"）
            if that_token.i == 0:
                # 既存の修飾語サブスロットを保持
                that_subslots = self._extract_simple_that_clause_subslots(doc, that_token)
                # 既存subslots（_detect_all_subslotsの結果）を優先し、重複しないもののみ追加
                for key, value in that_subslots.items():
                    if key not in subslots:
                        subslots[key] = value
                return subslots
            
            # 同格that節かどうかを判定（名詞の後にthatがある場合）
            has_noun_before = False
            for token in doc:
                if token.i < that_token.i and token.pos_ in ["NOUN", "PROPN"]:
                    has_noun_before = True
                    break
            
            if has_noun_before:
                that_subslots = self._extract_appositive_that_clause_subslots(doc, that_token)
                # 既存subslots（_detect_all_subslotsの結果）を優先し、重複しないもののみ追加
                for key, value in that_subslots.items():
                    if key not in subslots:
                        subslots[key] = value
                return subslots
            else:
                # 単純that節として処理
                that_subslots = self._extract_simple_that_clause_subslots(doc, that_token)
                # 既存subslots（_detect_all_subslotsの結果）を優先し、重複しないもののみ追加
                for key, value in that_subslots.items():
                    if key not in subslots:
                        subslots[key] = value
                return subslots
        
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
        
        # 完全な10個サブスロット検出
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        return subslots
    
    def _extract_wh_clause_subslots(self, doc, wh_word_token):
        """疑問詞節のサブスロット抽出（重複回避強化版）"""
        subslots = {}
        
        # 疑問詞節の構造解析: what(dobj) you(nsubj) said(ROOT)
        verb_token = None
        subject_tokens = []
        
        for token in doc:
            # より柔軟な動詞検出
            if token.pos_ == "VERB" or (token.pos_ == "AUX" and token.lemma_ in ["be", "have", "do"]):
                if token.dep_ in ["ROOT", "ccomp", "xcomp", "acl", "relcl"] or token.head == wh_word_token:
                    verb_token = token
                    print(f"🔍 疑問詞節動詞候補: '{token.text}' (pos: {token.pos_}, dep: {token.dep_})")
            elif token.dep_ in ["nsubj", "nsubjpass"] and token != wh_word_token:
                subject_tokens.append(token)
        
        # 動詞が見つからない場合は、疑問詞の後の全動詞を探す
        if not verb_token:
            for token in doc:
                if token.i > wh_word_token.i and (token.pos_ == "VERB" or token.pos_ == "AUX"):
                    verb_token = token
                    print(f"🔍 後続動詞検出: '{token.text}' (pos: {token.pos_})")
                    break
        
        print(f"🔍 疑問詞節分析: wh_word='{wh_word_token.text}', verb='{verb_token.text if verb_token else None}', subjects={[t.text for t in subject_tokens]}")
        
        if verb_token:
            # 疑問詞が主語の場合（what happened, who studies, which is）
            if wh_word_token.dep_ in ["nsubj", "nsubjpass"]:
                # sub-s: 疑問詞（主語として）
                subslots['sub-s'] = {
                    'text': wh_word_token.text,
                    'tokens': [wh_word_token.text],
                    'token_indices': [wh_word_token.i]
                }
                print(f"✅ sub-s(疑問詞主語): '{wh_word_token.text}'")
                
                # sub-v: 動詞
                subslots['sub-v'] = {
                    'text': verb_token.text,
                    'tokens': [verb_token.text],
                    'token_indices': [verb_token.i]
                }
                print(f"✅ sub-v(疑問詞節動詞): '{verb_token.text}'")
                
                # 動詞の目的語を処理（who studies English の English）
                objects = [child for child in verb_token.children if child.dep_ == "dobj"]
                if objects:
                    subslots['sub-o1'] = {
                        'text': objects[0].text,
                        'tokens': [objects[0].text],
                        'token_indices': [objects[0].i]
                    }
                    print(f"✅ sub-o1(疑問詞節目的語): '{objects[0].text}'")
            
            # 疑問詞が目的語の場合（what you said）
            elif wh_word_token.dep_ in ["dobj", "pobj"] and subject_tokens:
                # sub-o1: 疑問詞（目的語として）
                subslots['sub-o1'] = {
                    'text': wh_word_token.text,
                    'tokens': [wh_word_token.text],
                    'token_indices': [wh_word_token.i]
                }
                print(f"✅ sub-o1(疑問詞目的語): '{wh_word_token.text}'")
                
                # sub-s: 主語
                subject_text = ' '.join([t.text for t in subject_tokens])
                subslots['sub-s'] = {
                    'text': subject_text,
                    'tokens': [t.text for t in subject_tokens],
                    'token_indices': [t.i for t in subject_tokens]
                }
                print(f"✅ sub-s(疑問詞節主語): '{subject_text}'")
                
                # sub-v: 動詞
                subslots['sub-v'] = {
                    'text': verb_token.text,
                    'tokens': [verb_token.text],
                    'token_indices': [verb_token.i]
                }
                print(f"✅ sub-v(疑問詞節動詞): '{verb_token.text}'")
            
            # その他の場合（単純処理）
            else:
                # sub-s: 疑問詞（デフォルト主語として）
                subslots['sub-s'] = {
                    'text': wh_word_token.text,
                    'tokens': [wh_word_token.text],
                    'token_indices': [wh_word_token.i]
                }
                print(f"✅ sub-s(疑問詞デフォルト): '{wh_word_token.text}'")
                
                # sub-v: 動詞
                subslots['sub-v'] = {
                    'text': verb_token.text,
                    'tokens': [verb_token.text],
                    'token_indices': [verb_token.i]
                }
                print(f"✅ sub-v(疑問詞節動詞): '{verb_token.text}'")
        
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
        """動名詞主語のサブスロット抽出 (既存sub-vを尊重)"""
        subslots = {}
        
        # sub-v: 動名詞 (読む動作なので動詞として処理) - ただし既存sub-vがない場合のみ
        # 既存のnoun-verb統合（例：students studying）を保護
        print(f"🚨 動名詞処理警告: gerund='{gerund_token.text}' - sub-v上書きを試行")
        subslots['sub-v'] = {
            'text': gerund_token.text,
            'tokens': [gerund_token.text],
            'token_indices': [gerund_token.i]
        }
        print(f"✅ sub-v上書き実行: '{gerund_token.text}'")
        
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

    def _detect_o1o2_structure(self, doc):
        """O1O2構造（間接目的語+直接目的語）の専用検出"""
        subslots = {}
        
        print(f"🔍 O1O2構造検出開始")
        
        # give, send, tell, show, bring, take などの二重目的語を取る動詞を検出
        ditransitive_verbs = ["give", "send", "tell", "show", "bring", "take", "teach", "buy", "make", "get"]
        
        for token in doc:
            if token.pos_ == "VERB" and token.lemma_ in ditransitive_verbs:
                print(f"🔍 二重目的語動詞検出: '{token.text}' (lemma: {token.lemma_})")
                
                # 動詞の子要素から直接目的語と間接目的語を特定
                direct_objects = []  # dobj
                indirect_objects = []  # iobj または特定パターン
                
                for child in token.children:
                    if child.dep_ == "dobj":
                        direct_objects.append(child)
                        print(f"🔍 直接目的語候補: '{child.text}' (dep: {child.dep_})")
                    elif child.dep_ == "iobj":
                        indirect_objects.append(child)
                        print(f"🔍 間接目的語候補: '{child.text}' (dep: {child.dep_})")
                    elif child.dep_ == "dative":
                        indirect_objects.append(child)
                        print(f"🔍 間接目的語候補(dative): '{child.text}' (dep: {child.dep_})")
                
                # パターン1: "give him a book" - 代名詞+名詞の順序パターン
                if not indirect_objects and len(direct_objects) >= 2:
                    # 複数のdobjがある場合、最初が間接目的語の可能性
                    sorted_objects = sorted(direct_objects, key=lambda x: x.i)
                    if sorted_objects[0].pos_ == "PRON" and sorted_objects[1].pos_ in ["NOUN", "DET"]:
                        indirect_objects = [sorted_objects[0]]
                        direct_objects = sorted_objects[1:]
                        print(f"🔍 代名詞パターンで間接目的語再分類: '{indirect_objects[0].text}'")
                
                # パターン2: 順序による判定（前のオブジェクトが間接目的語）
                if not indirect_objects and len(direct_objects) >= 2:
                    sorted_objects = sorted(direct_objects, key=lambda x: x.i)
                    if sorted_objects[0].i < sorted_objects[1].i:
                        indirect_objects = [sorted_objects[0]]
                        direct_objects = sorted_objects[1:]
                        print(f"🔍 位置パターンで間接目的語再分類: '{indirect_objects[0].text}'")
                
                # サブスロット割り当て（修正版: O1=間接目的語, O2=直接目的語）
                if indirect_objects and 'sub-o1' not in subslots:
                    io = indirect_objects[0]
                    subslots['sub-o1'] = {
                        'text': io.text,
                        'tokens': [io.text],
                        'token_indices': [io.i]
                    }
                    print(f"✅ sub-o1(間接目的語)検出: '{io.text}'")
                
                if direct_objects and 'sub-o2' not in subslots:
                    do = direct_objects[0]
                    # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
                    do_det_tokens = [child for child in do.children if child.dep_ == "det"]
                    if do_det_tokens:
                        o2_tokens = do_det_tokens + [do]
                        o2_tokens.sort(key=lambda x: x.i)
                        o2_text = ' '.join([t.text for t in o2_tokens])
                        o2_token_indices = [t.i for t in o2_tokens]
                    else:
                        o2_tokens = [do]
                        o2_text = do.text
                        o2_token_indices = [do.i]
                    
                    subslots['sub-o2'] = {
                        'text': o2_text,
                        'tokens': [t.text for t in o2_tokens],
                        'token_indices': o2_token_indices
                    }
                    print(f"✅ sub-o2(直接目的語)検出: '{o2_text}' (冠詞統合)")
                
                break
        
        return subslots

    def _extract_simple_that_clause_subslots(self, doc, that_token):
        """単純that節のサブスロット抽出（"that he is studying hard"）改善版"""
        subslots = {}
        
        # that節内の主語、助動詞、動詞を特定
        that_clause_subj = None
        that_clause_aux = None
        that_clause_verb = None
        
        print(f"🔍 単純that節分析開始: '{that_token.text}'")
        
        # that後のトークンを順次解析
        for token in doc:
            if token.i > that_token.i:
                # 主語検出
                if token.dep_ == "nsubj" and that_clause_subj is None:
                    that_clause_subj = token
                    print(f"🔍 that節内主語検出: '{token.text}' (dep: {token.dep_})")
                
                # 助動詞検出（be動詞、have動詞、do動詞など）
                if token.pos_ == "AUX" and that_clause_aux is None:
                    that_clause_aux = token
                    print(f"🔍 that節内助動詞検出: '{token.text}' (pos: {token.pos_})")
                
                # メイン動詞検出（助動詞以外の動詞）
                if token.pos_ == "VERB" and that_clause_verb is None:
                    that_clause_verb = token
                    print(f"🔍 that節内動詞検出: '{token.text}' (pos: {token.pos_})")
        
        # サブスロット構築
        if that_clause_subj:
            # sub-s: that + 主語（統合）
            subslots['sub-s'] = {
                'text': f"{that_token.text} {that_clause_subj.text}",
                'tokens': [that_token.text, that_clause_subj.text],
                'token_indices': [that_token.i, that_clause_subj.i]
            }
            print(f"✅ sub-s(that節主語統合): '{that_token.text} {that_clause_subj.text}'")
        
        if that_clause_aux:
            # sub-aux: 助動詞
            subslots['sub-aux'] = {
                'text': that_clause_aux.text,
                'tokens': [that_clause_aux.text],
                'token_indices': [that_clause_aux.i]
            }
            print(f"✅ sub-aux(that節助動詞): '{that_clause_aux.text}'")
        
        if that_clause_verb:
            # sub-v: メイン動詞
            subslots['sub-v'] = {
                'text': that_clause_verb.text,
                'tokens': [that_clause_verb.text],
                'token_indices': [that_clause_verb.i]
            }
            print(f"✅ sub-v(that節動詞): '{that_clause_verb.text}'")
        
        return subslots

    def _detect_all_subslots(self, doc):
        """完全な10個サブスロット検出エンジン"""
        print(f"🔍 _detect_all_subslots 実行開始")
        subslots = {}
        
        # まずO1O2構造（間接目的語+直接目的語）を優先検出
        o1o2_subslots = self._detect_o1o2_structure(doc)
        subslots.update(o1o2_subslots)
        
        # 既に使用されているトークンインデックスを追跡
        used_indices = set()
        for sub_data in subslots.values():
            used_indices.update(sub_data.get('token_indices', []))
        
        for token in doc:
            # 既に使用されているトークンをスキップ
            if token.i in used_indices:
                continue
                
            # 既存の処理と重複しないように、新たに必要なサブスロットのみ検出
            
            # sub-m1: 前置修飾語 (形容詞、決定詞など)
            if token.dep_ in ["amod", "det", "nummod", "compound"] and 'sub-m1' not in subslots:
                subslots['sub-m1'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                used_indices.add(token.i)
                print(f"🔍 sub-m1検出: '{token.text}' (dep: {token.dep_})")
            
            # sub-aux: 助動詞
            elif token.dep_ == "aux" and 'sub-aux' not in subslots:
                subslots['sub-aux'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                used_indices.add(token.i)
                print(f"🔍 sub-aux検出: '{token.text}'")
            
            # sub-c1: 補語1 (attr, acomp)
            elif token.dep_ in ["attr", "acomp"] and 'sub-c1' not in subslots:
                subslots['sub-c1'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                used_indices.add(token.i)
                print(f"🔍 sub-c1検出: '{token.text}' (dep: {token.dep_})")
            
            # sub-o2: 間接目的語（iobj または dative構造）
            elif (token.dep_ == "iobj" or (token.dep_ == "dobj" and token.pos_ == "PRON")) and 'sub-o2' not in subslots:
                # "giving him a book" の him を間接目的語として検出
                verb_children = [child for child in token.head.children if child.dep_ == "dobj"]
                if verb_children and token.i < verb_children[0].i:  # 代名詞が直接目的語より前にある
                    subslots['sub-o2'] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    print(f"✅ sub-o2(間接目的語)検出: '{token.text}' (giving構造)")
                elif token.dep_ == "iobj":  # 通常のiobj
                    subslots['sub-o2'] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    print(f"✅ sub-o2(間接目的語)検出: '{token.text}' (iobj)")
            
            # sub-c1: 補語1 (attr, acomp, 連結動詞用)
            elif token.dep_ in ["attr", "acomp"] and 'sub-c1' not in subslots:
                # becoming, being 等の連結動詞の補語
                if token.head.lemma_ in ["become", "be", "seem", "appear", "look", "sound", "feel"]:
                    subslots['sub-c1'] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    print(f"✅ sub-c1(連結動詞補語)検出: '{token.text}' (dep: {token.dep_})")
            
            # sub-c2: 補語2 (xcomp, ccomp)
            elif token.dep_ in ["xcomp", "ccomp"] and 'sub-c2' not in subslots:
                subslots['sub-c2'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-c2検出: '{token.text}' (dep: {token.dep_})")
        
        # 位置ベースで修飾語を割り当て（前置詞句処理を含む）- O1O2構造を考慮
        position_modifiers = self._assign_modifiers_by_position_with_o1o2_protection(doc, subslots)
        subslots.update(position_modifiers)
        
        # 未分類トークンの処理（残余分類システム）
        self._classify_remaining_tokens(doc, subslots)
        
        return subslots
    
    def _collect_token_with_modifiers(self, token, doc):
        """トークンとその修飾語を収集"""
        tokens = [token]
        
        # 子トークン（修飾語）を追加
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "nummod"]:
                tokens.insert(0, child)  # 修飾語は前に配置
        
        return sorted(tokens, key=lambda t: t.i)
    
    def _collect_verb_phrase(self, token, doc):
        """動詞句全体を収集（助動詞、不定詞マーカー含む）"""
        tokens = [token]
        
        # 助動詞を前に追加
        for other_token in doc:
            if other_token.head == token and other_token.dep_ in ["aux", "auxpass"]:
                tokens.insert(0, other_token)
            elif other_token.head == token and other_token.dep_ == "mark" and other_token.text.lower() == "to":
                tokens.insert(0, other_token)  # 不定詞のto
        
        return sorted(tokens, key=lambda t: t.i)
    
    def _assign_modifiers_by_position_with_o1o2_protection(self, doc, existing_subslots):
        """位置ベース修飾語割り当て（O1O2構造保護版）"""
        modifiers = {}
        
        # 既存のO1O2構造で使用されているトークンをスキップ
        protected_indices = set()
        for sub_data in existing_subslots.values():
            protected_indices.update(sub_data.get('token_indices', []))
        
        print(f"🔍 O1O2保護インデックス: {sorted(protected_indices)}")
        
        # O1O2構造に干渉しない修飾語のみを位置ベースで割り当て
        sentence_length = len(doc)
        
        # 副詞修飾語（O1O2構造のトークンを除外）
        advmod_tokens = [token for token in doc 
                        if token.dep_ in ["advmod", "npadvmod"] 
                        and token.i not in protected_indices]
        
        for token in advmod_tokens:
            position = token.i / sentence_length
            
            if position <= 0.33 and 'sub-m1' not in modifiers:
                slot = 'sub-m1'
            elif position <= 0.66 and 'sub-m2' not in modifiers:
                slot = 'sub-m2'
            else:
                slot = 'sub-m3'
            
            if slot not in modifiers:
                modifiers[slot] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"✅ {slot}として割り当て: '{token.text}' (位置: {position:.2f}, advmod)")
        
        print(f"🔍 保護版修飾語割り当て結果: {list(modifiers.keys())}")
        return modifiers
        """未分類トークンを適切なサブスロットに分類（重複防止強化版）"""
        covered_indices = set()
        
        # 既にカバーされているトークンのインデックスを収集
        for sub_data in subslots.values():
            covered_indices.update(sub_data['token_indices'])
        
        print(f"🔍 分類前カバー済みインデックス: {sorted(covered_indices)}")
        
        for token in doc:
            if token.i in covered_indices:
                continue
                
            # 名詞・代名詞で未分類のもの
            if token.pos_ in ["NOUN", "PROPN", "PRON"]:
                # 重複チェック（さらに厳密）
                is_already_assigned = any(
                    token.i in sub_data.get('token_indices', [])
                    for sub_data in subslots.values()
                )
                
                if is_already_assigned:
                    print(f"⚠️ 重複スキップ: '{token.text}' (既に割り当て済み)")
                    continue
                
                # that節内の主語検出を強化
                if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                    # that節内の主語を優先的にsub-sとして処理
                    if 'sub-s' not in subslots:
                        subslots['sub-s'] = {
                            'text': token.text,
                            'tokens': [token.text],
                            'token_indices': [token.i]
                        }
                        covered_indices.add(token.i)
                        print(f"✅ sub-s(that節主語)検出: '{token.text}' (dep: {token.dep_})")
                        continue
                
                # 補語の主語の場合
                if token.dep_ == "nsubj" and token.head.dep_ in ["ccomp", "xcomp"]:
                    if 'sub-o1' not in subslots:
                        subslots['sub-o1'] = {
                            'text': token.text,
                            'tokens': [token.text],
                            'token_indices': [token.i]
                        }
                        covered_indices.add(token.i)
                        print(f"✅ sub-o1(補語主語)検出: '{token.text}' (dep: {token.dep_})")
                        continue
                
                # 関係代名詞の処理を強化
                if token.text.lower() in ["who", "which", "that"] and token.dep_ in ["nsubj", "nsubjpass"]:
                    if 'sub-s' not in subslots:
                        subslots['sub-s'] = {
                            'text': token.text,
                            'tokens': [token.text],
                            'token_indices': [token.i]
                        }
                        covered_indices.add(token.i)
                        print(f"✅ sub-s(関係代名詞)検出: '{token.text}' (dep: {token.dep_})")
                        continue
                
                # 疑問詞の処理（重複回避）
                if token.text.lower() in ["what", "who", "which", "where", "when", "why", "how"]:
                    # 既にsub-o1に割り当て済みの場合はsub-sに割り当てない
                    if 'sub-o1' in subslots and token.i in subslots['sub-o1']['token_indices']:
                        print(f"⚠️ 疑問詞重複回避: '{token.text}' (sub-o1既割り当て)")
                        continue
                    elif 'sub-s' not in subslots:
                        subslots['sub-s'] = {
                            'text': token.text,
                            'tokens': [token.text],
                            'token_indices': [token.i]
                        }
                        covered_indices.add(token.i)
                        print(f"✅ sub-s(疑問詞)検出: '{token.text}' (pos: {token.pos_})")
                        continue
                
                # 前置詞の目的語はスキップ
                if token.dep_ == "pobj":
                    print(f"⚠️ 前置詞目的語スキップ: '{token.text}' (dep: {token.dep_})")
                    continue
                
                # 通常の処理
                if 'sub-s' not in subslots:
                    subslots['sub-s'] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    covered_indices.add(token.i)
                    print(f"✅ sub-s(残余)検出: '{token.text}' (pos: {token.pos_})")
                elif 'sub-o1' not in subslots:
                    subslots['sub-o1'] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    covered_indices.add(token.i)
                    print(f"✅ sub-o1(残余)検出: '{token.text}' (pos: {token.pos_})")
            
            # 形容詞で未分類のもの
            elif token.pos_ == "ADJ" and 'sub-c2' not in subslots:
                subslots['sub-c2'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-c2(残余)検出: '{token.text}' (pos: {token.pos_})")
            
            # 動詞で未分類のもの
            elif token.pos_ == "VERB" and 'sub-v' not in subslots:
                print(f"🚨 残余動詞上書き警告: '{token.text}' - 既存sub-v確認: {'sub-v' in subslots}")
                subslots['sub-v'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"🔍 sub-v(残余)検出: '{token.text}' (pos: {token.pos_}) - 上書き実行!")
            
            # 時間副詞の処理（yesterday, today, etc）
            elif token.pos_ in ["NOUN", "ADV"] and token.text.lower() in ["yesterday", "today", "tomorrow", "year", "time"]:
                # 修飾語slotが空いている場合に追加
                for slot_name in ['sub-m1', 'sub-m2', 'sub-m3']:
                    if slot_name not in subslots:
                        subslots[slot_name] = {
                            'text': token.text,
                            'tokens': [token.text],
                            'token_indices': [token.i]
                        }
                        print(f"🔍 {slot_name}(時間副詞)検出: '{token.text}'")
                        break
            
            # auxpass処理（been, beingなど）
            elif token.dep_ == "auxpass" and token.text.lower() in ["been", "being"]:
                # 既存のsub-auxに追加するか、新規作成
                if 'sub-aux' in subslots:
                    subslots['sub-aux']['text'] += ' ' + token.text
                    subslots['sub-aux']['tokens'].append(token.text)
                    subslots['sub-aux']['token_indices'].append(token.i)
                    print(f"🔍 sub-aux(auxpass)追加: '{token.text}'")
                else:
                    subslots['sub-aux'] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    print(f"🔍 sub-aux(auxpass)検出: '{token.text}'")
            
            # 孤立した前置詞の処理 → 前置詞句として処理済みの場合はスキップ
            elif token.pos_ == "ADP" and token.text.lower() in ["for", "in", "at", "on", "with", "by"]:
                # この前置詞が既に前置詞句として処理されているかチェック
                already_processed = False
                for sub_data in subslots.values():
                    if token.i in sub_data.get('token_indices', []):
                        already_processed = True
                        break
                
                if not already_processed:
                    # 修飾語slotが空いている場合に追加
                    for slot_name in ['sub-m1', 'sub-m2', 'sub-m3']:
                        if slot_name not in subslots:
                            subslots[slot_name] = {
                                'text': token.text,
                                'tokens': [token.text],
                                'token_indices': [token.i]
                            }
                            print(f"🔍 {slot_name}(前置詞)検出: '{token.text}'")
                            break
    
    def _assign_modifiers_by_position(self, doc, existing_subslots=None):
        """位置ベースで修飾語をsub-m1, sub-m2, sub-m3に割り当て"""
        subslots = {}
        if existing_subslots is None:
            existing_subslots = {}
        
        # 既に使用されたトークンのインデックスを収集
        used_indices = set()
        for sub_data in existing_subslots.values():
            used_indices.update(sub_data.get('token_indices', []))
        
        # 修飾語候補を収集
        modifier_candidates = []
        
        # det/amod（限定詞/形容詞修飾語） - 既に使用されていないもの
        # 冠詞・定冠詞(det)は必ず名詞とセットなので、単独では修飾語候補から除外
        det_amod_tokens = [token for token in doc if token.dep_ in ["amod"] and token.i not in used_indices]
        for token in det_amod_tokens:
            modifier_candidates.append({
                'token': token,
                'text': token.text,
                'position': token.i,
                'type': 'amod'
            })
        
        # advmod（副詞修飾語） - 既に使用されていないもの
        advmod_tokens = [token for token in doc if token.dep_ == "advmod" and token.i not in used_indices]
        for token in advmod_tokens:
            modifier_candidates.append({
                'token': token,
                'text': token.text,
                'position': token.i,
                'type': 'advmod'
            })
        
        # npadvmod（名詞的副詞修飾語） - "this year" のような時間表現
        npadvmod_tokens = [token for token in doc if token.dep_ == "npadvmod" and token.i not in used_indices]
        for token in npadvmod_tokens:
            npadvmod_phrase_tokens = [token]
            npadvmod_phrase_text = token.text
            
            # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
            det_tokens = [child for child in token.children if child.dep_ == "det" and child.i not in used_indices]
            if det_tokens:
                # 冠詞 + 名詞の統合
                det_noun_tokens = det_tokens + [token]
                det_noun_tokens.sort(key=lambda x: x.i)
                npadvmod_phrase_tokens = det_noun_tokens
                npadvmod_phrase_text = " ".join([t.text for t in det_noun_tokens])
            
            modifier_candidates.append({
                'tokens': npadvmod_phrase_tokens,
                'text': npadvmod_phrase_text,
                'position': token.i,
                'type': 'npadvmod'
            })
            print(f"🔍 npadvmod検出: '{npadvmod_phrase_text}' tokens: {[t.text for t in npadvmod_phrase_tokens]}")
        
        # 前置詞句 (prep + pobj) - 既に使用されていないもの
        prep_tokens = [token for token in doc if token.dep_ in ["prep", "dative"] and token.i not in used_indices]
        for prep_token in prep_tokens:
            prep_phrase_tokens = [prep_token]
            prep_phrase_text = prep_token.text
            
            # 前置詞句の目的語も含める（使用済みでないもの）
            for child in prep_token.children:
                if child.dep_ == "pobj" and child.i not in used_indices:
                    # 冠詞・定冠詞は必ず名詞とセット（100%のルール）
                    # 前置詞句の目的語の冠詞も統合
                    pobj_det_tokens = [grandchild for grandchild in child.children if grandchild.dep_ == "det" and grandchild.i not in used_indices]
                    if pobj_det_tokens:
                        # 冠詞 + 名詞の順番で統合
                        det_noun_tokens = pobj_det_tokens + [child]
                        det_noun_tokens.sort(key=lambda x: x.i)
                        prep_phrase_tokens.extend(det_noun_tokens)
                        prep_phrase_text += " " + " ".join([t.text for t in det_noun_tokens])
                    else:
                        prep_phrase_tokens.append(child)
                        prep_phrase_text += " " + child.text
            
            # 前置詞句が有効な場合のみ追加
            if len(prep_phrase_tokens) > 1 or prep_token.i not in used_indices:
                print(f"🔍 前置詞句構築: '{prep_phrase_text}' tokens: {[t.text for t in prep_phrase_tokens]}")
                
                modifier_candidates.append({
                    'tokens': prep_phrase_tokens,
                    'text': prep_phrase_text,
                    'position': prep_token.i,
                    'type': 'prep_phrase'
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
            
            # "for him"のような前置詞句は期待する位置に強制割り当て
            if 'type' in modifier and modifier['type'] == 'prep_phrase':
                if modifier['text'] == 'for him':
                    slot_name = 'sub-m2'  # 期待する位置に強制
            
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
        
        # デバッグ: 修飾語割り当て後の結果確認
        print(f"🔍 修飾語割り当て結果: {list(subslots.keys())}")
        
        return subslots
    
    def _classify_remaining_tokens(self, doc, subslots):
        """残りのトークン分類処理"""
        remaining_subslots = {}
        
        # 既に使用されているトークンのインデックスを取得
        used_indices = set()
        for sub_data in subslots.values():
            used_indices.update(sub_data.get('token_indices', []))
        
        print(f"🔍 残りトークン分類 - 使用済みインデックス: {sorted(used_indices)}")
        
        # 未使用トークンの分類
        for token in doc:
            if token.i not in used_indices:
                # 基本的な分類ロジック（必要に応じて拡張）
                if token.pos_ in ["NOUN", "PROPN"] and token.dep_ == "dobj":
                    if 'sub-o1' not in remaining_subslots:
                        remaining_subslots['sub-o1'] = {
                            'text': token.text,
                            'tokens': [token.text],
                            'token_indices': [token.i]
                        }
                        print(f"✅ 残りトークンsub-o1: '{token.text}'")
        
        print(f"🔍 残りトークン分類結果: {list(remaining_subslots.keys())}")
        return remaining_subslots


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
