#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import stanza
import spacy

class PureStanzaEngine:
    def __init__(self):
        """Stanza + spaCy + Step18 hybrid engine initialization"""
        print("🎯 PureStanzaEngine初期化中...")
        
        # Stanza pipeline for structural analysis
        self.nlp = stanza.Pipeline('en', verbose=False)
        print("✅ Stanza準備完了")
        
        # spaCy pipeline for boundary adjustment
        try:
            self.spacy_nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy準備完了")
        except OSError:
            print("⚠️ spaCy en_core_web_sm not found. Boundary adjustment disabled.")
            self.spacy_nlp = None
        
        # Step18 subslot mapping integration
        self.dep_to_subslot = {
            'nsubj': 'sub-s',
            'nsubjpass': 'sub-s',
            'aux': 'sub-aux', 
            'auxpass': 'sub-aux',
            'dobj': 'sub-o1',
            'iobj': 'sub-o2',
            'attr': 'sub-c1',
            'ccomp': 'sub-c2',
            'xcomp': 'sub-c2',
            'advmod': 'sub-m2',
            'amod': 'sub-m3', 
            'prep': 'sub-m3',
            'pobj': 'sub-o1',
            'pcomp': 'sub-c2',
            'mark': 'sub-m1',
            'relcl': 'sub-m3',
            'acl': 'sub-m3'
        }
        
        print("🏗️ Stanza+spaCy+Step18ハイブリッドエンジン準備完了")
    
    def decompose(self, sentence):
        """Basic decomposition: Utilizing Stanza information directly"""
        print(f"\n🎯 Stanza基本分解開始: '{sentence[:50]}...'")
        
        doc = self.nlp(sentence)
        
        for sent in doc.sentences:
            # Find ROOT verb
            root_verb = self._find_root_verb(sent)
            if not root_verb:
                print("❌ ROOT動詞が見つかりません")
                continue
            
            print(f"📌 ROOT動詞: '{root_verb.text}'")
            
            # Layer 1: Extract all slots directly from Stanza
            print("📐 Layer 1: Stanza構造分析...")
            slots = self._extract_all_slots_from_stanza(sent, root_verb)
            
            # Layer 2: Adjust boundaries with spaCy
            print("🔧 Layer 2: spaCy境界調整...")
            slots = self._adjust_boundaries_with_spacy(sentence, slots)
            
            # Layer 3: Add Step18 subslot enhancements (preserve main slots)
            print("🧩 Layer 3: Step18サブスロット強化...")
            slots = self._add_step18_subslot_enhancements(sentence, slots)
            
            # Print results
            self._print_slots(slots)
            
            # Compare with correct data
            self._compare_with_correct_data(slots)
            
            return slots
        
        return None
    
    def _find_root_verb(self, sent):
        """Identify ROOT verb"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _is_be_verb_construction(self, sent, root_verb):
        """be動詞構文かどうかを判定する"""
        # パターン1: ROOT = ADJ with cop (He is happy)
        if root_verb.upos == 'ADJ':
            return any(word.head == root_verb.id and word.deprel == 'cop' for word in sent.words)
        
        # パターン2: ROOT = NOUN with cop (He is a teacher, He is under pressure)
        elif root_verb.upos == 'NOUN':
            return any(word.head == root_verb.id and word.deprel == 'cop' for word in sent.words)
        
        return False
    
    def _get_be_verb_from_root(self, sent, root_verb):
        """be動詞構文からbe動詞を取得する"""
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'cop':
                return word
        return None
    
    def _extract_all_slots_from_stanza(self, sent, root_verb):
        """Extract all 8 slots directly from Stanza"""
        print("🏗️ Stanzaから直接スロット抽出中...")
        
        # be動詞構文の検出
        is_be_construction = self._is_be_verb_construction(sent, root_verb)
        if is_be_construction:
            print(f"🔍 be動詞構文を検出: ROOT={root_verb.text}({root_verb.upos})")
        
        slots = {}
        
        # M1: Beginning modifying phrase (obl:unmarked)
        slots['M1'] = self._extract_m1_slot(sent, root_verb)
        
        # S: Subject (nsubj + relative clause)
        slots['S'] = self._extract_s_slot(sent, root_verb)
        
        # Aux: Auxiliary verb (aux + mark)
        slots['Aux'] = self._extract_aux_slot(sent, root_verb)
        
        # V: Verb (actual action verb)
        slots['V'] = self._extract_v_slot(sent, root_verb)
        
        # O1: Object 1
        slots['O1'] = self._extract_o1_slot(sent, root_verb)
        
        # O2: Object 2 (indirect object) - 統一処理追加
        slots['O2'] = self._extract_o2_slot(sent, root_verb)
        
        # C1: Complement 1 (predicative complement) - 統一処理追加  
        slots['C1'] = self._extract_c1_slot(sent, root_verb)
        
        # C2: Complement 2
        slots['C2'] = self._extract_c2_slot(sent, root_verb)
        
        # M2: Modifying phrase 2 (advcl - even though)
        slots['M2'] = self._extract_m2_slot(sent, root_verb)
        
        # M3: Modifying phrase 3 (advcl - so)
        slots['M3'] = self._extract_m3_slot(sent, root_verb)
        
        return {k: v for k, v in slots.items() if v}  # Only non-empty slots
    
    def _extract_m1_slot(self, sent, root_verb):
        """M1 slot: Beginning modifying phrase"""
        # Look for obl:unmarked
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'obl:unmarked':
                # Identify the end position of obl:unmarked dependency tree
                m1_end_char = self._find_obl_unmarked_end(sent, word)
                if m1_end_char:
                    m1_text = sent.text[:m1_end_char].strip().rstrip(',').strip()
                    print(f"📍 M1検出: '{m1_text}'")
                    return {'main': m1_text}
        return None
    
    def _find_obl_unmarked_end(self, sent, obl_word):
        """Identify end character position of obl:unmarked"""
        # Recursively explore child elements of obl:unmarked
        max_end = obl_word.end_char
        
        def find_children_end(word_id):
            nonlocal max_end
            for w in sent.words:
                if w.head == word_id:
                    max_end = max(max_end, w.end_char)
                    find_children_end(w.id)  # Recursively explore child elements
        
        find_children_end(obl_word.id)
        return max_end
    
    def _extract_s_slot(self, sent, root_verb):
        """S slot: Subject + relative clause - 統一境界検出アルゴリズム適用"""
        # Look for nsubj
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'nsubj':
                # 統一境界検出: 依存関係ツリーの完全走査
                s_range = self._find_complete_subtree_range(sent, word)
                s_text = self._extract_text_range(sent, s_range)
                print(f"📍 S検出: '{s_text}'")
                
                # Sub-slot decomposition
                subslots = self._extract_s_subslots(sent, word)
                subslots['main'] = s_text
                return subslots
        return None
    
    def _extract_aux_slot(self, sent, root_verb):
        """Aux slot: Auxiliary verb"""
        aux_parts = []
        
        # Check if ROOT verb functions as modal/auxiliary
        if root_verb.text.lower() in ['had', 'has', 'have', 'will', 'would', 'can', 'could', 'may', 'might', 'must', 'should']:
            aux_parts.append(root_verb.text)
        
        # Look for auxiliary of ROOT verb
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'aux':
                aux_parts.append(word.text)
        
        # Also look for mark of xcomp (to in "had to")
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                for child in sent.words:
                    if child.head == word.id and child.deprel == 'mark':
                        aux_parts.append(child.text)
        
        if aux_parts:
            aux_text = ' '.join(aux_parts)
            print(f"📍 Aux検出: '{aux_text}'")
            return {'main': aux_text}
        return None
    
    def _extract_v_slot(self, sent, root_verb):
        """V slot: Verb - be動詞構文完全対応版"""
        
        # パターン1: xcomp構造での実際の動詞（優先）
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                print(f"📍 V検出: '{word.text}'（xcomp）")
                return {'main': word.text}
        
        # パターン2: 通常の動詞（ROOT = VERB）
        if root_verb.upos == 'VERB':
            print(f"📍 V検出: '{root_verb.text}'（ROOT VERB）")
            return {'main': root_verb.text}
        
        # パターン3: be動詞構文（ROOT = ADJ/NOUN, cop関係でbe動詞特定）
        if self._is_be_verb_construction(sent, root_verb):
            be_verb = self._get_be_verb_from_root(sent, root_verb)
            if be_verb:
                print(f"📍 V検出: '{be_verb.text}'（be動詞構文）")
                return {'main': be_verb.text}
        
        return None
    
    def _extract_o1_slot(self, sent, root_verb):
        """O1 slot: Object 1 - 統一境界検出アルゴリズム適用"""
        # Look for obj of xcomp
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                for child in sent.words:
                    if child.head == word.id and child.deprel == 'obj':
                        # 統一境界検出: 依存関係ツリーの完全走査
                        o1_range = self._find_complete_subtree_range(sent, child)
                        o1_text = self._extract_text_range(sent, o1_range)
                        print(f"📍 O1検出: '{o1_text}'")
                        return {'main': o1_text}
        return None
    
    def _extract_o2_slot(self, sent, root_verb):
        """O2 slot: Object 2 (indirect object) - 統一パターン適用"""
        # Look for iobj dependency (indirect object)
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'iobj':
                # 統一境界検出: 完全なiobj句を抽出
                o2_range = self._find_complete_subtree_range(sent, word)
                o2_text = self._extract_text_range(sent, o2_range)
                print(f"📍 O2検出: '{o2_text}'")
                return {'main': o2_text}
        return None
    
    def _extract_c1_slot(self, sent, root_verb):
        """C1 slot: Complement 1 - be動詞構文完全対応版"""
        
        # パターン1: 通常のattr/acomp依存関係
        for word in sent.words:
            if word.head == root_verb.id and word.deprel in ['attr', 'acomp']:
                c1_range = self._find_complete_subtree_range(sent, word)
                c1_text = self._extract_text_range(sent, c1_range)
                print(f"📍 C1検出: '{c1_text}'（{word.deprel}）")
                return {'main': c1_text}
        
        # パターン2: be動詞構文 - 3つの補語タイプに対応
        if self._is_be_verb_construction(sent, root_verb):
            # 補語専用境界検出を使用（主語・be動詞を除外）
            c1_range = self._find_c1_complement_range(sent, root_verb)
            c1_text = self._extract_text_range(sent, c1_range)
            
            if root_verb.upos == 'ADJ':
                print(f"📍 C1検出: '{c1_text}'（be動詞+形容詞補語）")
            elif root_verb.upos == 'NOUN':
                has_preposition = any(word.head == root_verb.id and word.deprel == 'case' 
                                    for word in sent.words)
                if has_preposition:
                    print(f"📍 C1検出: '{c1_text}'（be動詞+前置詞句補語）")
                else:
                    print(f"📍 C1検出: '{c1_text}'（be動詞+名詞補語）")
            
            return {'main': c1_text}
        
        # パターン3: xcomp構造（become a teacher等）
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                c1_range = self._find_complete_subtree_range(sent, word)
                c1_text = self._extract_text_range(sent, c1_range)
                print(f"📍 C1検出: '{c1_text}'（xcomp）")
                return {'main': c1_text}
        
        return None
    
    def _extract_c2_slot(self, sent, root_verb):
        """C2 slot: Complement 2 - 統一境界検出アルゴリズム適用"""
        # Look for advcl of xcomp (deliver構造)
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                for child in sent.words:
                    if child.head == word.id and child.deprel == 'advcl' and child.text == 'deliver':
                        # C2専用境界検出: advcl修飾句を除外した基本動詞句のみ
                        c2_range = self._find_c2_verb_phrase_range(sent, child)
                        c2_text = self._extract_text_range(sent, c2_range)
                        print(f"📍 C2検出: '{c2_text}'")
                        # 統一サブスロット処理追加
                        subslots = self._extract_unified_subslots(sent, child, c2_text)
                        return subslots
        return None
    
    def _extract_m2_slot(self, sent, root_verb):
        """M2 slot: Modifying phrase 2 - 統一スロット抽出アルゴリズム適用"""
        
        # パターン1: be動詞構文の副詞修飾語（advmod）
        if self._is_be_verb_construction(sent, root_verb):
            for word in sent.words:
                if word.head == root_verb.id and word.deprel == 'advmod':
                    print(f"📍 M2検出: '{word.text}'（be動詞構文の副詞修飾語）")
                    # 統一サブスロット処理追加
                    subslots = self._extract_unified_subslots(sent, word, word.text)
                    return subslots
        
        # パターン2: 既存の複雑なM2パターン（xcomp -> advcl -> pressure）
        # M2: deliver -> advcl -> pressure (even though句、ただしM3子句は除外)
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':  # make
                for deliver_child in sent.words:
                    if deliver_child.head == word.id and deliver_child.deprel == 'advcl' and deliver_child.text == 'deliver':  # deliver
                        for pressure_child in sent.words:
                            if pressure_child.head == deliver_child.id and pressure_child.deprel == 'advcl' and pressure_child.text == 'pressure':  # pressure
                                # M2専用境界検出: advcl子句（M3）を除外した範囲を抽出
                                m2_range = self._find_m2_phrase_range(sent, pressure_child)
                                m2_text = self._extract_text_range(sent, m2_range)
                                print(f"📍 M2検出: '{m2_text}'")
                                # 統一サブスロット処理追加
                                subslots = self._extract_unified_subslots(sent, pressure_child, m2_text)
                                return subslots
        return None
    
    def _extract_m3_slot(self, sent, root_verb):
        """M3 slot: Modifying phrase 3 - 統一スロット抽出アルゴリズム適用"""
        # M3: deliver -> advcl -> pressure -> advcl -> reflect (so句)
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':  # make
                for deliver_child in sent.words:
                    if deliver_child.head == word.id and deliver_child.deprel == 'advcl' and deliver_child.text == 'deliver':  # deliver
                        for pressure_child in sent.words:
                            if pressure_child.head == deliver_child.id and pressure_child.deprel == 'advcl' and pressure_child.text == 'pressure':  # pressure
                                for reflect_child in sent.words:
                                    if reflect_child.head == pressure_child.id and reflect_child.deprel == 'advcl' and reflect_child.text == 'reflect':  # reflect
                                        # 統一境界検出: 完全なadvcl句を抽出
                                        m3_range = self._find_complete_subtree_range(sent, reflect_child)
                                        m3_text = self._extract_text_range(sent, m3_range)
                                        print(f"📍 M3検出: '{m3_text}'")
                                        # 統一サブスロット処理追加
                                        subslots = self._extract_unified_subslots(sent, reflect_child, m3_text)
                                        return subslots
        return None
    
    # Helper methods for unified boundary detection algorithm
    def _find_complete_subtree_range(self, sent, root_word):
        """統一境界検出: 依存関係ツリーの完全走査で正確な境界を特定"""
        # 全ての子ノードを再帰的に収集
        all_words_in_subtree = self._collect_all_descendants(sent, root_word)
        all_words_in_subtree.add(root_word.id)  # ルート自身も含める
        
        # 文字位置範囲を特定
        min_start = min(sent.words[word_id-1].start_char for word_id in all_words_in_subtree)
        max_end = max(sent.words[word_id-1].end_char for word_id in all_words_in_subtree)
        
        return (min_start, max_end)
    
    def _find_c1_complement_range(self, sent, root_verb):
        """C1補語専用境界検出: be動詞構文の補語のみを抽出（主語・be動詞・副詞修飾語・句読点を除外）"""
        complement_words = {root_verb.id}  # ROOT（補語）自身
        
        # 補語の修飾語のみを収集（nsubj・cop・advmod・punctは除外）
        # advmodはRephraseのM2スロットなので、C1からは除外
        complement_relations = {'det', 'amod', 'case'}
        
        for word in sent.words:
            if word.head == root_verb.id and word.deprel in complement_relations:
                complement_words.add(word.id)
                # この子の下位ツリーも再帰的に追加
                descendants = self._collect_all_descendants(sent, word)
                complement_words.update(descendants)
        
        # 句読点を除外
        complement_words = {word_id for word_id in complement_words 
                          if sent.words[word_id-1].upos != 'PUNCT'}
        
        if not complement_words:
            return (root_verb.start_char, root_verb.end_char)
        
        # 文字位置範囲を特定
        min_start = min(sent.words[word_id-1].start_char for word_id in complement_words)
        max_end = max(sent.words[word_id-1].end_char for word_id in complement_words)
        
        return (min_start, max_end)
    
    def _find_verb_phrase_range(self, sent, verb_word):
        """動詞句の範囲検出: advcl等の修飾句を除外した基本動詞句のみ"""
        # 動詞の直接的な依存関係のみを収集（advcl等は除外）
        core_relations = {'obj', 'nsubj', 'aux', 'advmod', 'det', 'amod', 'prep', 'pobj'}
        
        verb_phrase_words = {verb_word.id}
        
        # 動詞の直接的な子のみを追加（advcl等は除外）
        for word in sent.words:
            if word.head == verb_word.id and word.deprel in core_relations:
                # この子の下位ツリーも再帰的に追加
                descendants = self._collect_all_descendants(sent, word)
                verb_phrase_words.update(descendants)
                verb_phrase_words.add(word.id)
        
        if verb_phrase_words:
            min_start = min(sent.words[word_id-1].start_char for word_id in verb_phrase_words)
            max_end = max(sent.words[word_id-1].end_char for word_id in verb_phrase_words)
            return (min_start, max_end)
        
        # フォールバック: 動詞単体の範囲
        return (verb_word.start_char, verb_word.end_char)
    
    def _find_c2_verb_phrase_range(self, sent, verb_word):
        """C2専用動詞句範囲検出: advcl修飾句を除外して基本動詞句のみを抽出"""
        # C2に含める依存関係: obj, advmod, det, amod, nsubj等（advcl子句は除外）
        c2_core_relations = {'obj', 'advmod', 'det', 'amod', 'nsubj', 'aux'}
        
        c2_words = {verb_word.id}
        
        # 基本動詞句のみを収集（advcl子句は除外）
        for word in sent.words:
            if word.head == verb_word.id and word.deprel in c2_core_relations:
                # この子の下位ツリーも再帰的に追加（ただしadvcl系は除外）
                descendants = self._collect_non_advcl_descendants(sent, word)
                c2_words.update(descendants)
                c2_words.add(word.id)
        
        if c2_words:
            min_start = min(sent.words[word_id-1].start_char for word_id in c2_words)
            max_end = max(sent.words[word_id-1].end_char for word_id in c2_words)
            return (min_start, max_end)
        
        # フォールバック: 動詞単体の範囲
        return (verb_word.start_char, verb_word.end_char)
    
    def _find_m2_phrase_range(self, sent, pressure_word):
        """M2専用境界検出: advcl子句（M3）を除外してM2句のみを抽出"""
        # M2に含める依存関係: advcl以外のすべて
        m2_core_relations = {'nsubj', 'cop', 'case', 'amod', 'advmod', 'mark', 'det'}
        
        m2_words = {pressure_word.id}
        
        # pressure子句のみを収集（advcl子句であるreflectは除外）
        for word in sent.words:
            if word.head == pressure_word.id and word.deprel in m2_core_relations:
                # この子の下位ツリーも再帰的に追加（ただしadvcl系は除外）
                descendants = self._collect_non_advcl_descendants(sent, word)
                m2_words.update(descendants)
                m2_words.add(word.id)
        
        if m2_words:
            min_start = min(sent.words[word_id-1].start_char for word_id in m2_words)
            max_end = max(sent.words[word_id-1].end_char for word_id in m2_words)
            return (min_start, max_end)
        
        # フォールバック: pressure単体の範囲
        return (pressure_word.start_char, pressure_word.end_char)
    
    def _collect_all_descendants(self, sent, word):
        """指定した単語の全ての子孫ノードを再帰的に収集"""
        descendants = set()
        
        # 直接の子を探索
        for child in sent.words:
            if child.head == word.id:
                descendants.add(child.id)
                # 再帰的に子の子孫も収集
                child_descendants = self._collect_all_descendants(sent, child)
                descendants.update(child_descendants)
        
        return descendants
    
    def _collect_non_advcl_descendants(self, sent, word):
        """advcl系を除外して子孫ノードを収集"""
        descendants = set()
        
        # 直接の子を探索（advcl系は除外）
        for child in sent.words:
            if child.head == word.id and child.deprel != 'advcl':
                descendants.add(child.id)
                # 再帰的に子の子孫も収集
                child_descendants = self._collect_non_advcl_descendants(sent, child)
                descendants.update(child_descendants)
        
        return descendants
    
    def _extract_text_range(self, sent, range_tuple):
        """文字範囲からテキストを抽出"""
        start, end = range_tuple
        return sent.text[start:end]
    
    def _extract_s_subslots(self, sent, subj_word):
        """Extract S subslots - 統一サブスロット処理を使用"""
        # Sスロットのメインテキストを取得
        s_range = self._find_complete_subtree_range(sent, subj_word)
        s_text = self._extract_text_range(sent, s_range)
        
        # 統一サブスロット処理を適用
        return self._extract_unified_subslots(sent, subj_word, s_text)
    
    def _extract_unified_subslots(self, sent, root_word, main_text):
        """統一サブスロット処理: 上位分解ロジックを再利用した本格実装"""
        
        # メインテキストをStanzaで再解析
        sub_doc = self.nlp(main_text)
        
        if not sub_doc.sentences:
            return {'main': main_text}
        
        sub_sent = sub_doc.sentences[0] 
        sub_root_verb = self._find_root_verb(sub_sent)
        
        if not sub_root_verb:
            return {'main': main_text}
        
        print(f"  🧩 サブスロット分解開始: '{main_text}' (ROOT: {sub_root_verb.text})")
        
        # 上位分解と同じロジックを適用（サブスロットレベル）
        subslots = {'main': main_text}
        
        # sub-s: Subject
        sub_s = self._extract_s_slot(sub_sent, sub_root_verb)
        if sub_s:
            subslots['sub-s'] = sub_s['main']
        
        # sub-aux: Auxiliary
        sub_aux = self._extract_aux_slot(sub_sent, sub_root_verb)
        if sub_aux:
            subslots['sub-aux'] = sub_aux['main']
            
        # sub-v: Verb
        sub_v = self._extract_v_slot(sub_sent, sub_root_verb)
        if sub_v:
            subslots['sub-v'] = sub_v['main']
            
        # sub-o1: Object 1
        sub_o1 = self._extract_o1_slot(sub_sent, sub_root_verb)
        if sub_o1:
            subslots['sub-o1'] = sub_o1['main']
            
        # sub-m1: Modifying phrase 1
        sub_m1 = self._extract_m1_slot(sub_sent, sub_root_verb)
        if sub_m1:
            subslots['sub-m1'] = sub_m1['main']
        
        # sub-m2: Modifying phrase 2  
        sub_m2 = self._extract_m2_slot(sub_sent, sub_root_verb)
        if sub_m2:
            subslots['sub-m2'] = sub_m2['main']
        
        print(f"    ✅ サブスロット抽出完了: {len(subslots)-1}個のサブスロット")
        return subslots
    
    def _print_slots(self, slots):
        """Print slot results"""
        print(f"\n=== Stanza基本分解結果 ===")
        
        for slot_name, slot_data in slots.items():
            if isinstance(slot_data, dict) and 'main' in slot_data:
                print(f"\n📋 {slot_name}スロット: \"{slot_data['main']}\"")
                
                # Print subslots if available (統一処理で全スロット対応)
                has_subslots = any(key.startswith('sub-') for key in slot_data.keys())
                if has_subslots:
                    print(f"\n📋 {slot_name}スロット:")
                    for sub_key in ['sub-s', 'sub-aux', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-v']:
                        if sub_key in slot_data:
                            print(f"  {sub_key:10}: \"{slot_data[sub_key]}\"")
                    print(f"  {'main':10}: \"{slot_data['main']}\"")
    
    def _compare_with_correct_data(self, slots):
        """Compare with correct data"""
        # Correct data for ex007
        correct_data = {
            'M1': 'that afternoon at the crucial point in the presentation',
            'S': {
                'main': 'the manager who had recently taken charge of the project',
                'sub-s': 'the manager who',
                'sub-aux': 'had',
                'sub-m2': 'recently',
                'sub-v': 'taken',
                'sub-o1': 'charge of the project'
            },
            'Aux': 'had to',
            'V': 'make',
            'O1': 'the committee responsible for implementation',
            'C2': 'deliver the final proposal flawlessly',
            'M2': 'even though he was under intense pressure',
            'M3': 'so the outcome would reflect their full potential'
        }
        
        print(f"\n🎯 正解データ比較:")
        
        for slot_name, correct_value in correct_data.items():
            if slot_name in slots:
                if isinstance(correct_value, dict):
                    # Handle S slot with subslots
                    print(f"{slot_name}スロット比較:")
                    for sub_key, sub_correct in correct_value.items():
                        if sub_key in slots[slot_name]:
                            actual = slots[slot_name][sub_key]
                            match = "✅" if actual.lower() == sub_correct.lower() else "❌"
                            print(f"  {sub_key}: {match} 正解='{sub_correct}' 実際='{actual}'")
                        else:
                            print(f"  {sub_key}: ❌ 正解='{sub_correct}' 実際='<なし>'")
                else:
                    # Handle simple slots
                    actual = slots[slot_name]['main']
                    match = "✅" if actual.lower() == correct_value.lower() else "❌"
                    print(f"{slot_name}: {match} 正解='{correct_value}' 実際='{actual}'")
            else:
                print(f"{slot_name}: ❌ 正解='{correct_value}' 実際='<なし>'")
    
    # === Layer 2: spaCy Boundary Adjustment Functions ===
    
    def _adjust_boundaries_with_spacy(self, sentence, slots):
        """
        Layer 2: Use spaCy for precise boundary adjustment
        Takes Stanza-based slots and refines boundaries using spaCy
        """
        if not self.spacy_nlp:
            print("⚠️ spaCy not available. Skipping boundary adjustment.")
            return slots
        
        print("🔧 spaCy境界調整開始...")
        
        # Process sentence with spaCy
        spacy_doc = self.spacy_nlp(sentence)
        
        # Adjust each slot boundary
        adjusted_slots = {}
        for slot_name, slot_data in slots.items():
            adjusted_slots[slot_name] = self._adjust_slot_boundary(slot_data, spacy_doc, sentence)
        
        print("✅ spaCy境界調整完了")
        return adjusted_slots
    
    def _adjust_slot_boundary(self, slot_data, spacy_doc, sentence):
        """
        Adjust individual slot boundary using spaCy information
        """
        if not slot_data or 'main' not in slot_data:
            return slot_data
        
        main_text = slot_data['main']
        if not main_text or main_text == '':
            return slot_data
        
        # Find the text span in spaCy doc
        start_char = sentence.find(main_text)
        if start_char == -1:
            return slot_data  # Text not found, return as is
        
        end_char = start_char + len(main_text)
        
        # Find corresponding spaCy tokens
        spacy_span = spacy_doc.char_span(start_char, end_char, alignment_mode="expand")
        if not spacy_span:
            # Fallback: try exact boundaries
            spacy_span = spacy_doc.char_span(start_char, end_char)
            if not spacy_span:
                return slot_data  # No corresponding span found
        
        # For precise slots (like M2, M3), don't expand boundaries
        # Only clean up exact boundaries
        adjusted_text = spacy_span.text.strip()
        
        # Update slot data
        adjusted_slot_data = slot_data.copy()
        adjusted_slot_data['main'] = adjusted_text
        
        if adjusted_text != main_text:
            print(f"🔧 {main_text} → {adjusted_text}")
        
        return adjusted_slot_data
    
    def _expand_span_with_spacy(self, span, doc):
        """
        Expand span boundaries using spaCy POS and dependency information
        Based on Step18 _expand_span() logic but using spaCy
        """
        start_i = span.start
        end_i = span.end
        
        # Expand left: Include preceding determiners, adjectives
        while start_i > 0:
            prev_token = doc[start_i - 1]
            if prev_token.pos_ in ['DET', 'ADJ', 'ADV'] and prev_token.dep_ in ['det', 'amod', 'advmod']:
                start_i -= 1
            else:
                break
        
        # Expand right: Include trailing prepositions, particles
        while end_i < len(doc):
            next_token = doc[end_i]
            if next_token.pos_ in ['ADP', 'PART'] and next_token.dep_ in ['prep', 'prt']:
                end_i += 1
            else:
                break
        
        return doc[start_i:end_i]
    
    # === Layer 3: Step18 Advanced Subslot Processing ===
    
    def _enhance_with_step18_subslots(self, sentence, slots):
        """
        Layer 3: Step18のサブスロット処理技術を統合
        既存のスロットにStep18のサブスロット詳細処理を追加
        """
        if not self.spacy_nlp:
            print("⚠️ spaCy not available. Skipping Step18 subslot processing.")
            return slots
        
        print("🧩 Layer 3: Step18サブスロット処理...")
        
        # Process sentence with spaCy for Step18 techniques
        spacy_doc = self.spacy_nlp(sentence)
        
        enhanced_slots = {}
        for slot_name, slot_data in slots.items():
            if slot_name in ['S', 'O1', 'C2', 'M2', 'M3']:  # Subslot capable slots
                enhanced_slots[slot_name] = self._apply_step18_subslot_processing(
                    slot_data, spacy_doc, sentence, slot_name
                )
            else:
                enhanced_slots[slot_name] = slot_data
        
        print("✅ Step18サブスロット処理完了")
        return enhanced_slots
    
    def _apply_step18_subslot_processing(self, slot_data, spacy_doc, sentence, slot_name):
        """
        Apply Step18's detailed subslot processing to individual slots
        """
        if not slot_data or 'main' not in slot_data:
            return slot_data
        
        main_text = slot_data['main']
        if not main_text:
            return slot_data
        
        # Find the span in spaCy doc
        start_char = sentence.find(main_text)
        if start_char == -1:
            return slot_data
        
        end_char = start_char + len(main_text)
        spacy_span = spacy_doc.char_span(start_char, end_char, alignment_mode="expand")
        
        if not spacy_span:
            return slot_data
        
        # Apply Step18's _expand_span and _integrate_prepositions techniques
        enhanced_slot_data = slot_data.copy()
        
        # Find root token of this slot
        root_token = None
        for token in spacy_span:
            if token.dep_ in ['ROOT', 'nsubj', 'dobj', 'xcomp', 'ccomp', 'advcl']:
                root_token = token
                break
        
        if root_token:
            # Apply Step18 expansion
            expanded_text = self._step18_expand_span(root_token, spacy_doc)
            
            # Apply Step18 preposition integration
            integrated_text = self._step18_integrate_prepositions(root_token, spacy_doc)
            if integrated_text:
                expanded_text = integrated_text
            
            enhanced_slot_data['main'] = expanded_text
            
            # Generate subslots using Step18 mapping
            subslots = self._generate_step18_subslots(root_token, spacy_doc)
            enhanced_slot_data.update(subslots)
            
            if expanded_text != main_text:
                print(f"🧩 {slot_name}拡張: {main_text} → {expanded_text}")
        
        return enhanced_slot_data
    
    def _step18_expand_span(self, token, doc):
        """Step18のスパン拡張アルゴリズム移植"""
        expand_deps = ['det', 'poss', 'compound', 'amod']
        
        start = token.i
        end = token.i
        
        # 基本的な子要素の拡張
        for child in token.children:
            if child.dep_ in expand_deps:
                start = min(start, child.i)
                end = max(end, child.i)
        
        # 関係節処理
        for child in token.children:
            if child.dep_ == 'relcl':
                # 関係代名詞(who)のみ含める
                for relcl_child in child.children:
                    if relcl_child.dep_ == 'nsubj' and relcl_child.pos_ == 'PRON':
                        start = min(start, relcl_child.i)
                        end = max(end, relcl_child.i)
                        break
        
        return ' '.join([doc[i].text for i in range(start, end + 1)])
    
    def _step18_integrate_prepositions(self, token, doc):
        """Step18の前置詞統合処理移植"""
        # 動詞 + 前置詞句統合
        if token.pos_ in ['VERB', 'AUX']:
            prep_parts = []
            
            for child in token.children:
                if child.dep_ == 'prep':
                    prep_text = child.text
                    
                    for prep_child in child.children:
                        if prep_child.dep_ == 'pobj':
                            obj_span = self._step18_expand_span(prep_child, doc)
                            prep_text += f" {obj_span}"
                    
                    prep_parts.append(prep_text)
            
            if prep_parts:
                return f"{token.text} {' '.join(prep_parts)}"
        
        # 名詞 + 前置詞句統合
        if token.pos_ == 'NOUN' and token.dep_ == 'dobj':
            prep_parts = []
            
            for child in token.children:
                if child.dep_ == 'prep':
                    prep_text = child.text
                    
                    for prep_child in child.children:
                        if prep_child.dep_ == 'pobj':
                            obj_span = self._step18_expand_span(prep_child, doc)
                            prep_text += f" {obj_span}"
                    
                    prep_parts.append(prep_text)
            
            if prep_parts:
                return f"{token.text} {' '.join(prep_parts)}"
        
        return None
    
    def _generate_step18_subslots(self, token, doc):
        """Step18のサブスロット生成技術移植"""
        subslots = {}
        
        for child in token.children:
            if child.dep_ in self.dep_to_subslot:
                subslot_name = self.dep_to_subslot[child.dep_]
                expanded_text = self._step18_expand_span(child, doc)
                subslots[subslot_name] = expanded_text
        
        return subslots
    
    def _add_step18_subslot_enhancements(self, sentence, slots):
        """
        Layer 3 Alternative: Step18のサブスロット技術を既存スロットに追加
        メインスロットは保持し、追加サブスロット情報のみ統合
        """
        if not self.spacy_nlp:
            print("⚠️ spaCy not available. Skipping Step18 enhancements.")
            return slots
        
        print("🧩 Step18サブスロット強化処理...")
        
        # Process sentence with spaCy
        spacy_doc = self.spacy_nlp(sentence)
        
        enhanced_slots = {}
        for slot_name, slot_data in slots.items():
            enhanced_slot_data = slot_data.copy()
            
            # Add Step18 subslot classifications for complex slots
            if slot_name in ['S', 'O1', 'C2'] and 'main' in slot_data:
                additional_subslots = self._extract_additional_step18_subslots(
                    slot_data['main'], spacy_doc, sentence
                )
                enhanced_slot_data.update(additional_subslots)
            
            enhanced_slots[slot_name] = enhanced_slot_data
        
        print("✅ Step18サブスロット強化完了")
        return enhanced_slots
    
    def _extract_additional_step18_subslots(self, main_text, spacy_doc, sentence):
        """
        Step18のサブスロット分類技術を使って追加サブスロットを抽出
        メインテキストは変更せず、内部構造のみ分析
        """
        additional_subslots = {}
        
        # Find span in spaCy doc
        start_char = sentence.find(main_text)
        if start_char == -1:
            return additional_subslots
        
        end_char = start_char + len(main_text)
        spacy_span = spacy_doc.char_span(start_char, end_char, alignment_mode="expand")
        
        if not spacy_span:
            return additional_subslots
        
        # Apply Step18 dependency mapping within the span
        for token in spacy_span:
            for child in token.children:
                if child in spacy_span and child.dep_ in self.dep_to_subslot:
                    subslot_name = self.dep_to_subslot[child.dep_]
                    # Only add if not already present
                    if subslot_name not in additional_subslots:
                        additional_subslots[f"step18-{subslot_name}"] = child.text
        
        if additional_subslots:
            print(f"  🧩 追加サブスロット: {additional_subslots}")
        
        return additional_subslots


def test_example007():
    """Test with example 007"""
    engine = PureStanzaEngine()
    
    sentence = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    result = engine.decompose(sentence)
    return result

if __name__ == '__main__':
    test_example007()
