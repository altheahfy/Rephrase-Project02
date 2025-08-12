#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
比較級・最上級構文エンジン (Comparative/Superlative Engine)
統合アーキテクチャ Phase 2: 高頻度構文パターン

比較級・最上級構文の上位+サブスロット二重分解処理
"""

import stanza
from typing import Dict, List, Optional, Any

class ComparativeSuperlativeEngine:
    """比較級・最上級構文の統合アーキテクチャエンジン"""
    
    def __init__(self):
        """エンジン初期化"""
        print("🚀 比較級・最上級構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
        
        # 比較構文パターン定義
        self.comparative_markers = {
            'more', 'less', 'better', 'worse', 'greater', 'smaller',
            'larger', 'higher', 'lower', 'faster', 'slower', 'bigger', 
            'smaller', 'older', 'younger', 'stronger', 'weaker'
        }
        
        self.superlative_markers = {
            'most', 'least', 'best', 'worst', 'greatest', 'smallest',
            'largest', 'highest', 'lowest', 'fastest', 'slowest', 'biggest',
            'oldest', 'youngest', 'strongest', 'weakest'
        }
        
        print("✅ 初期化完了")
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        独立文としての比較級・最上級構文処理
        上位スロット + サブスロット の二重分解
        """
        print(f"  🎯 比較級・最上級エンジン統合処理: {sentence}")
        
        doc = self.nlp(sentence)
        sent = doc.sentences[0]
        
        # 比較構文検出
        comparative_info = self._detect_comparative_structure(sent)
        
        if not comparative_info['detected']:
            print("  ❌ 比較構文が検出されませんでした")
            return {}
        
        # パターン別処理
        if comparative_info['type'] == 'comparative':
            return self._process_comparative(sent, comparative_info)
        elif comparative_info['type'] == 'superlative':
            return self._process_superlative(sent, comparative_info)
        elif comparative_info['type'] == 'equal':
            return self._process_equal_comparison(sent, comparative_info)
        elif comparative_info['type'] == 'proportional':
            return self._process_proportional_comparison(sent, comparative_info)
        
        return {}
    
    def process_as_subslot(self, sentence: str) -> Dict[str, str]:
        """
        従属節内比較構文のサブスロット専用処理
        基本スロット構造 (sub-s, sub-v, sub-c1, sub-m1, etc.) のみ使用
        """
        print(f"  🔧 サブスロット比較級・最上級処理開始")
        
        doc = self.nlp(sentence)
        sent = doc.sentences[0]
        
        # 比較構文検出
        comparative_info = self._detect_comparative_structure(sent)
        
        if not comparative_info['detected']:
            # 非比較構文の場合は基本構造で処理
            return self._process_basic_as_subslot(sent)
        
        # 比較構文のサブスロット処理
        if comparative_info['type'] == 'comparative':
            return self._process_comparative_as_subslot(sent, comparative_info)
        elif comparative_info['type'] == 'superlative':
            return self._process_superlative_as_subslot(sent, comparative_info)
        elif comparative_info['type'] == 'equal':
            return self._process_equal_as_subslot(sent, comparative_info)
        
        return {}
    
    def _detect_comparative_structure(self, sent) -> Dict[str, Any]:
        """比較構文の検出と分類"""
        comparative_info = {
            'detected': False,
            'type': None,
            'comparative_word': None,
            'than_phrase': None,
            'as_phrases': [],
            'superlative_word': None,
            'scope_phrase': None,
            'proportional_elements': []
        }
        
        # 比較級・最上級語の検出
        for word in sent.words:
            word_lower = word.text.lower()
            
            # 比較級検出
            if (word_lower in self.comparative_markers or 
                word.text.endswith('er') and word.upos in ['ADJ', 'ADV']):
                comparative_info['comparative_word'] = word
                comparative_info['detected'] = True
                comparative_info['type'] = 'comparative'
                
            # 最上級検出  
            elif (word_lower in self.superlative_markers or
                  word.text.endswith('est') and word.upos in ['ADJ', 'ADV']):
                comparative_info['superlative_word'] = word
                comparative_info['detected'] = True
                comparative_info['type'] = 'superlative'
                
            # than句検出
            elif word_lower == 'than':
                comparative_info['than_phrase'] = word
                
            # as句検出
            elif word_lower == 'as':
                comparative_info['as_phrases'].append(word)
        
        # as...as構文判定
        if len(comparative_info['as_phrases']) >= 2:
            comparative_info['type'] = 'equal'
            comparative_info['detected'] = True
        
        # the...the構文判定 (proportional comparison)
        if self._detect_proportional_pattern(sent):
            comparative_info['type'] = 'proportional'
            comparative_info['detected'] = True
            comparative_info['proportional_elements'] = self._extract_proportional_elements(sent)
        
        print(f"  📋 比較構文検出結果: {comparative_info['type']}")
        return comparative_info
    
    def _detect_proportional_pattern(self, sent) -> bool:
        """the...the構文の検出"""
        the_count = 0
        comparative_count = 0
        
        for word in sent.words:
            if word.text.lower() == 'the':
                the_count += 1
            elif (word.text.lower() in self.comparative_markers or 
                  word.text.endswith('er') and word.upos in ['ADJ', 'ADV']):
                comparative_count += 1
        
        return the_count >= 2 and comparative_count >= 2
    
    def _extract_proportional_elements(self, sent) -> List[Dict]:
        """the...the構文の要素抽出"""
        elements = []
        current_element = {'the': None, 'comparative': None, 'clause_words': []}
        
        for word in sent.words:
            if word.text.lower() == 'the':
                if current_element['the'] is not None:
                    elements.append(current_element)
                    current_element = {'the': word, 'comparative': None, 'clause_words': []}
                else:
                    current_element['the'] = word
            elif (word.text.lower() in self.comparative_markers or 
                  word.text.endswith('er') and word.upos in ['ADJ', 'ADV']):
                current_element['comparative'] = word
            
            current_element['clause_words'].append(word)
        
        if current_element['the'] is not None:
            elements.append(current_element)
        
        return elements
    
    def _process_comparative(self, sent, comparative_info) -> Dict[str, Any]:
        """比較級構文処理 (more/er + than)"""
        print(f"  🎯 比較級処理開始")
        
        result = {
            'comparison_type': 'comparative',
            'metadata': {
                'comparative_word': comparative_info['comparative_word'].text if comparative_info['comparative_word'] else None,
                'than_object': None
            }
        }
        
        # 基本要素の検出
        subject = None
        main_verb = None
        comparative_phrase = None
        than_phrase = None
        
        for word in sent.words:
            # 主語検出
            if word.deprel == 'nsubj':
                subject = self._build_phrase(sent, word)
            # 動詞検出 (比較構文では形容詞がrootになることが多い)
            elif word.deprel == 'root':
                if word.upos == 'VERB':
                    main_verb = word.text
                elif word.upos == 'ADJ':
                    # be動詞を探す
                    for w in sent.words:
                        if w.upos == 'AUX' and w.deprel == 'cop':
                            main_verb = w.text
                            break
                    if not main_verb:
                        main_verb = word.text  # 形容詞をVに設定
            # 比較句検出
            elif word == comparative_info['comparative_word']:
                comparative_phrase = self._build_comparative_phrase(sent, word)
            # than句検出 
            elif word.deprel == 'obl' and comparative_info['than_phrase']:
                than_phrase = f"than {self._build_phrase(sent, word)}"
                result['metadata']['than_object'] = self._build_phrase(sent, word)
        
        # 上位スロット配置
        if subject:
            result['S'] = subject
        if main_verb:
            result['V'] = main_verb
        if comparative_phrase:
            # 比較級の配置位置を判定
            comp_word = comparative_info['comparative_word']
            if comp_word.deprel == 'amod':  # 形容詞修飾 → O1
                result['O1'] = comparative_phrase
            elif comp_word.deprel in ['advmod', 'xcomp']:  # 副詞修飾 → M1
                result['M1'] = comparative_phrase  
            else:  # その他 → C1
                result['C1'] = comparative_phrase
        if than_phrase:
            result['M2'] = than_phrase
        
        # サブスロット分解 (同じ構造)
        if subject:
            result['sub-s'] = subject
        if main_verb:
            result['sub-v'] = main_verb
        if comparative_phrase:
            comp_word = comparative_info['comparative_word']
            if comp_word.deprel == 'amod':
                result['sub-o1'] = comparative_phrase
            elif comp_word.deprel in ['advmod', 'xcomp']:
                result['sub-m1'] = comparative_phrase
            else:
                result['sub-c1'] = comparative_phrase
        if than_phrase:
            result['sub-m2'] = than_phrase
        
        print(f"  ✅ 比較級分解完了: {result}")
        return result
    
    def _process_superlative(self, sent, comparative_info) -> Dict[str, Any]:
        """最上級構文処理 (most/est)"""
        print(f"  🎯 最上級処理開始")
        
        result = {
            'comparison_type': 'superlative',
            'metadata': {
                'superlative_word': comparative_info['superlative_word'].text if comparative_info['superlative_word'] else None,
                'scope': None
            }
        }
        
        # 基本要素の検出
        subject = None
        main_verb = None
        superlative_phrase = None
        scope_phrase = None
        
        for word in sent.words:
            # 主語検出
            if word.deprel == 'nsubj':
                subject = self._build_phrase(sent, word)
            # 動詞検出
            elif word.deprel == 'root' and word.upos in ['VERB', 'AUX', 'ADJ', 'NOUN']:
                main_verb = word.text
            # 最上級句検出
            elif word == comparative_info['superlative_word']:
                superlative_phrase = self._build_superlative_phrase(sent, word)
            # 範囲句検出 (in, among, of)
            elif word.deprel == 'nmod':
                scope_phrase = self._build_scope_phrase(sent, word)
                result['metadata']['scope'] = scope_phrase
        
        # 上位スロット配置
        if subject:
            result['S'] = subject
        if main_verb:
            result['V'] = main_verb
        if superlative_phrase:
            result['C1'] = superlative_phrase
        if scope_phrase:
            result['M2'] = scope_phrase
        
        # サブスロット分解 (同じ構造)
        if subject:
            result['sub-s'] = subject
        if main_verb:
            result['sub-v'] = main_verb
        if superlative_phrase:
            result['sub-c1'] = superlative_phrase
        if scope_phrase:
            result['sub-m2'] = scope_phrase
        
        print(f"  ✅ 最上級分解完了: {result}")
        return result
    
    def _process_equal_comparison(self, sent, comparative_info) -> Dict[str, Any]:
        """同等比較構文処理 (as...as)"""
        print(f"  🎯 同等比較処理開始")
        
        result = {
            'comparison_type': 'equal_comparison',
            'metadata': {
                'comparison_target': None
            }
        }
        
        # as...as構文の要素検出
        subject = None
        main_verb = None
        as_adjective = None
        as_target = None
        
        for word in sent.words:
            if word.deprel == 'nsubj':
                subject = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                main_verb = word.text
            elif word.deprel == 'obl':  # as his brother
                as_target = f"as {self._build_phrase(sent, word)}"
                result['metadata']['comparison_target'] = self._build_phrase(sent, word)
        
        # as + 形容詞の検出
        for word in sent.words:
            if word.upos == 'ADJ' and any(w.text.lower() == 'as' and w.deprel == 'advmod' for w in sent.words):
                as_adjective = f"as {word.text}"
                break
        
        # 上位スロット配置
        if subject:
            result['S'] = subject
        if main_verb:
            result['V'] = main_verb
        if as_adjective:
            result['C1'] = as_adjective
        if as_target:
            result['M2'] = as_target
        
        # サブスロット分解
        if subject:
            result['sub-s'] = subject
        if main_verb:
            result['sub-v'] = main_verb
        if as_adjective:
            result['sub-c1'] = as_adjective
        if as_target:
            result['sub-m2'] = as_target
        
        print(f"  ✅ 同等比較分解完了: {result}")
        return result
    
    def _process_proportional_comparison(self, sent, comparative_info) -> Dict[str, Any]:
        """比例比較構文処理 (the...the)"""
        print(f"  🎯 比例比較処理開始")
        
        result = {
            'comparison_type': 'proportional_comparison',
            'metadata': {
                'condition_clause': None,
                'result_clause': None
            }
        }
        
        elements = comparative_info['proportional_elements']
        if len(elements) >= 2:
            # 第一要素: The harder you work
            first_element = elements[0]
            condition_words = [w.text for w in first_element['clause_words'] if w.text != ',']
            condition_clause = ' '.join(condition_words[:5])  # 適切な長さで切り取り
            
            result['M1'] = condition_clause
            result['metadata']['condition_clause'] = condition_clause
            
            # M1内部のサブスロット分解
            if first_element['comparative']:
                result['sub-m1'] = f"the {first_element['comparative'].text}"
            
            # 主語・動詞の検出
            for word in first_element['clause_words']:
                if word.deprel == 'nsubj':
                    result['sub-s'] = word.text
                elif word.upos == 'VERB':
                    result['sub-v'] = word.text
            
            # 第二要素: the more successful you become
            second_element = elements[1]
            if second_element['comparative']:
                result['M2'] = f"the {second_element['comparative'].text}"
                
            # 主文の要素検出
            for word in sent.words:
                if word.deprel == 'root':
                    result['V'] = word.text
                elif word.deprel == 'nsubj' and word.head == sent.words[word.head-1].id:
                    if sent.words[word.head-1].deprel == 'root':
                        result['S'] = word.text
                elif word.upos == 'ADJ' and word.deprel == 'root':
                    result['C1'] = word.text
        
        print(f"  ✅ 比例比較分解完了: {result}")
        return result
    
    def _process_comparative_as_subslot(self, sent, comparative_info) -> Dict[str, str]:
        """比較級のサブスロット専用処理"""
        result = {}
        
        # 基本的な文構造をサブスロットに配置
        for word in sent.words:
            if word.deprel == 'nsubj':
                result['sub-s'] = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                result['sub-v'] = word.text
            elif word == comparative_info['comparative_word']:
                comp_phrase = self._build_comparative_phrase(sent, word)
                if word.deprel == 'amod':
                    result['sub-o1'] = comp_phrase
                elif word.deprel in ['advmod', 'xcomp']:
                    result['sub-m1'] = comp_phrase
                else:
                    result['sub-c1'] = comp_phrase
            elif word.deprel == 'obl' and comparative_info['than_phrase']:
                result['sub-m2'] = f"than {self._build_phrase(sent, word)}"
        
        return result
    
    def _process_superlative_as_subslot(self, sent, comparative_info) -> Dict[str, str]:
        """最上級のサブスロット専用処理"""
        result = {}
        
        for word in sent.words:
            if word.deprel == 'nsubj':
                result['sub-s'] = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                result['sub-v'] = word.text
            elif word == comparative_info['superlative_word']:
                result['sub-c1'] = self._build_superlative_phrase(sent, word)
            elif word.deprel == 'nmod':
                result['sub-m2'] = self._build_scope_phrase(sent, word)
        
        return result
    
    def _process_equal_as_subslot(self, sent, comparative_info) -> Dict[str, str]:
        """同等比較のサブスロット専用処理"""
        result = {}
        
        for word in sent.words:
            if word.deprel == 'nsubj':
                result['sub-s'] = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                result['sub-v'] = word.text
            elif word.upos == 'ADJ':
                result['sub-c1'] = f"as {word.text}"
            elif word.deprel == 'obl':
                result['sub-m2'] = f"as {self._build_phrase(sent, word)}"
        
        return result
    
    def _process_basic_as_subslot(self, sent) -> Dict[str, str]:
        """非比較構文の基本サブスロット処理"""
        result = {}
        
        for word in sent.words:
            if word.deprel == 'nsubj':
                result['sub-s'] = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                result['sub-v'] = word.text
            elif word.deprel == 'obj':
                result['sub-o1'] = self._build_phrase(sent, word)
        
        return result
    
    def _build_phrase(self, sent, head_word):
        """語句の構築 (修飾語含む)"""
        phrase_words = [head_word]
        
        # 修飾語を収集
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['det', 'amod', 'nmod:poss']:
                phrase_words.append(word)
        
        # 位置順でソート
        phrase_words.sort(key=lambda x: x.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _build_comparative_phrase(self, sent, comparative_word):
        """比較級句の構築"""
        if comparative_word.text.lower() == 'more':
            # more + 形容詞の場合
            for word in sent.words:
                # 同じheadを持つ形容詞を探す（more interesting構造）
                if (word.head == comparative_word.head and 
                    word.upos == 'ADJ' and 
                    word != comparative_word):
                    return f"more {word.text}"
                # moreが修飾する形容詞を探す（more efficient構造）  
                elif (comparative_word.head == word.id and 
                      word.upos == 'ADJ'):
                    return f"more {word.text}"
            # more + 名詞の場合（more money構造）
            for word in sent.words:
                if (comparative_word.deprel == 'amod' and
                    comparative_word.head == word.id and 
                    word.upos == 'NOUN'):
                    return f"more {word.text}"
            return comparative_word.text
        else:
            return comparative_word.text
    
    def _build_superlative_phrase(self, sent, superlative_word):
        """最上級句の構築"""
        phrase_words = []
        
        # 定冠詞theを探す
        for word in sent.words:
            if word.text.lower() == 'the' and word.deprel == 'det':
                phrase_words.append(word)
                break
        
        if superlative_word.text.lower() == 'most':
            # most + 形容詞 + 名詞の場合
            phrase_words.append(superlative_word)
            
            # 形容詞を探す
            for word in sent.words:
                if word.head == superlative_word.head and word.upos == 'ADJ' and word != superlative_word:
                    phrase_words.append(word)
                    break
                elif superlative_word.head == word.id and word.upos == 'ADJ':
                    phrase_words.append(word)
                    break
            
            # 名詞を探す (root または head)
            for word in sent.words:
                if ((word.deprel == 'root' and word.upos == 'NOUN') or
                    (superlative_word.head == word.id and word.upos == 'NOUN')):
                    phrase_words.append(word)
                    break
        else:
            # -est形の最上級
            phrase_words.append(superlative_word)
            
            # 関連する名詞を探す
            for word in sent.words:
                if word.deprel == 'root' and word.upos == 'NOUN':
                    phrase_words.append(word)
                    break
        
        phrase_words.sort(key=lambda x: x.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _build_scope_phrase(self, sent, scope_word):
        """範囲句の構築 (in, among, of)"""
        # 前置詞を探す
        prep = None
        for word in sent.words:
            if word.deprel == 'case' and word.head == scope_word.id:
                prep = word.text
                break
        
        scope_phrase = self._build_phrase(sent, scope_word)
        return f"{prep} {scope_phrase}" if prep else scope_phrase
