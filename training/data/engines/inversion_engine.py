#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
倒置構文エンジン (Inversion Engine)
統合アーキテクチャ準拠 - 9番目のエンジン

対応パターン:
1. 否定の倒置 (Never have I seen...)
2. 副詞句の倒置 (On the table lay...)
3. 条件文の倒置 (Had I known...)
4. 比較の倒置 (So beautiful was...)
5. 場所の倒置 (Down the hill ran...)
"""

import stanza
from typing import Dict, Any, List

class InversionEngine:
    def __init__(self):
        """倒置構文エンジン初期化"""
        print("🚀 倒置構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
        print("✅ 初期化完了")
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        独立文としての倒置構文処理
        上位スロット + サブスロット の二重分解
        """
        print(f"  🎯 倒置構文エンジン統合処理: {sentence}")
        
        # 接続詞を含む複文の場合は処理を中止（接続詞エンジンに委譲）
        if self._contains_conjunction(sentence):
            print("  ⚠️ 接続詞を検出：接続詞エンジンに委譲")
            return {}
        
        doc = self.nlp(sentence)
        sent = doc.sentences[0]
        
        # 倒置構文検出
        inversion_info = self._detect_inversion_structure(sent)
        
        if not inversion_info['detected']:
            print("  ❌ 倒置構文が検出されませんでした")
            return {}
        
        # 倒置パターン別処理
        pattern = inversion_info['pattern']
        if pattern == 'negative_inversion':
            return self._process_negative_inversion(sent, inversion_info)
        elif pattern == 'adverbial_inversion':
            return self._process_adverbial_inversion(sent, inversion_info)
        elif pattern == 'conditional_inversion':
            return self._process_conditional_inversion(sent, inversion_info)
        elif pattern == 'comparative_inversion':
            return self._process_comparative_inversion(sent, inversion_info)
        elif pattern == 'locative_inversion':
            return self._process_locative_inversion(sent, inversion_info)
        else:
            print(f"  ❌ 未対応の倒置パターン: {pattern}")
            return {}
    
    def process_as_subslot(self, sentence: str) -> Dict[str, Any]:
        """
        従属節内倒置構文のサブスロット専用処理
        基本スロット構造 (sub-s, sub-v, sub-aux, sub-m1, etc.) のみ使用
        """
        print(f"  🔧 サブスロット倒置構文処理開始")
        
        doc = self.nlp(sentence)
        sent = doc.sentences[0]
        
        # 倒置構文検出
        inversion_info = self._detect_inversion_structure(sent)
        
        if not inversion_info['detected']:
            # 非倒置の場合は基本構造で処理
            return self._process_basic_as_subslot(sent)
        
        # 倒置構文のサブスロット処理
        return self._process_inversion_as_subslot(sent, inversion_info)
    
    def _detect_inversion_structure(self, sent) -> Dict[str, Any]:
        """倒置構文の検出と分類"""
        inversion_info = {
            'detected': False,
            'pattern': None,
            'inversion_trigger': None,
            'auxiliary': None,
            'main_verb': None,
            'subject': None,
            'complement': None,
            'adverbial': None,
            'is_question': False
        }
        
        words = sent.words
        first_word = words[0] if words else None
        
        # 1. 否定の倒置検出 (Never, Not only, Hardly, etc.)
        negative_triggers = ['never', 'not', 'hardly', 'rarely', 'seldom', 'little', 'nowhere']
        if first_word and any(trigger in first_word.text.lower() for trigger in negative_triggers):
            inversion_info['pattern'] = 'negative_inversion'
            inversion_info['inversion_trigger'] = first_word.text
            inversion_info['detected'] = True
            print(f"  📋 否定倒置検出: {first_word.text}")
        
        # 2. 副詞句の倒置検出 (On the table, In the garden, etc.)
        elif first_word and first_word.upos in ['ADP', 'ADV']:
            # 前置詞や副詞で始まる場合
            inversion_info['pattern'] = 'adverbial_inversion'
            inversion_info['inversion_trigger'] = first_word.text
            inversion_info['detected'] = True
            print(f"  📋 副詞句倒置検出: {first_word.text}")
        
        # 3. 条件文の倒置検出 (Had I known, Were I you, etc.)
        elif first_word and first_word.upos == 'AUX' and first_word.text.lower() in ['had', 'were', 'should']:
            inversion_info['pattern'] = 'conditional_inversion'
            inversion_info['auxiliary'] = first_word
            inversion_info['detected'] = True
            print(f"  📋 条件倒置検出: {first_word.text}")
        
        # 4. 比較の倒置検出 (So beautiful was, Such was, etc.)
        elif first_word and first_word.text.lower() in ['so', 'such']:
            inversion_info['pattern'] = 'comparative_inversion'
            inversion_info['inversion_trigger'] = first_word.text
            inversion_info['detected'] = True
            print(f"  📋 比較倒置検出: {first_word.text}")
        
        # 5. 場所の倒置検出 (Down, Up, Away, etc.)
        elif first_word and first_word.text.lower() in ['down', 'up', 'away', 'out', 'in', 'here', 'there']:
            inversion_info['pattern'] = 'locative_inversion'
            inversion_info['inversion_trigger'] = first_word.text
            inversion_info['detected'] = True
            print(f"  📋 場所倒置検出: {first_word.text}")
        
        # 主語・動詞・その他の要素を収集
        if inversion_info['detected']:
            for word in words:
                if word.deprel in ['nsubj', 'nsubj:pass']:
                    inversion_info['subject'] = word
                elif word.deprel == 'root':
                    inversion_info['main_verb'] = word
                elif word.upos == 'AUX' and not inversion_info['auxiliary']:
                    inversion_info['auxiliary'] = word
        
        return inversion_info
    
    def _process_negative_inversion(self, sent, inversion_info) -> Dict[str, Any]:
        """否定倒置処理 (Never have I seen...)"""
        print(f"  🎯 否定倒置処理開始")
        
        result = {
            'tense_type': 'negative_inversion',
            'metadata': {
                'inversion_trigger': inversion_info['inversion_trigger'],
                'pattern': 'negative_inversion'
            }
        }
        
        # 倒置された要素の収集
        trigger = inversion_info['inversion_trigger']
        subject = None
        auxiliary = None
        main_verb = None
        object_phrase = None
        
        if inversion_info['subject']:
            subject = self._build_phrase(sent, inversion_info['subject'])
        if inversion_info['auxiliary']:
            auxiliary = inversion_info['auxiliary'].text
        if inversion_info['main_verb']:
            main_verb = inversion_info['main_verb'].text
        
        # 目的語検出
        for word in sent.words:
            if word.deprel == 'obj':
                object_phrase = self._build_phrase(sent, word)
                break
        
        # 上位スロット配置（倒置構造を反映）
        result['M1'] = trigger  # 倒置のトリガー
        if auxiliary:
            result['Aux'] = auxiliary
        if main_verb:
            result['V'] = main_verb
        if subject:
            result['S'] = subject
        if object_phrase:
            result['O1'] = object_phrase
        
        # サブスロット分解（正常語順）
        if subject:
            result['sub-s'] = subject
        if auxiliary:
            result['sub-aux'] = auxiliary
        if main_verb:
            result['sub-v'] = main_verb
        if object_phrase:
            result['sub-o1'] = object_phrase
        result['sub-m1'] = trigger
        
        print(f"  ✅ 否定倒置分解完了: {result}")
        return result
    
    def _process_adverbial_inversion(self, sent, inversion_info) -> Dict[str, Any]:
        """副詞句倒置処理 (On the table lay...)"""
        print(f"  🎯 副詞句倒置処理開始")
        
        result = {
            'tense_type': 'adverbial_inversion',
            'metadata': {
                'inversion_trigger': inversion_info['inversion_trigger'],
                'pattern': 'adverbial_inversion'
            }
        }
        
        # 副詞句の構築
        adverbial_phrase = self._build_adverbial_phrase(sent)
        subject = None
        main_verb = None
        
        if inversion_info['subject']:
            subject = self._build_phrase(sent, inversion_info['subject'])
        if inversion_info['main_verb']:
            main_verb = inversion_info['main_verb'].text
        
        # 上位スロット配置（実際の語順）
        if adverbial_phrase:
            result['M2'] = adverbial_phrase  # 副詞句はM2位置
        if main_verb:
            result['V'] = main_verb
        if subject:
            result['S'] = subject
        
        # サブスロット分解（同じ構造をサブスロットにも）
        if adverbial_phrase:
            result['sub-m2'] = adverbial_phrase
        if main_verb:
            result['sub-v'] = main_verb
        if subject:
            result['sub-s'] = subject
        
        print(f"  ✅ 副詞句倒置分解完了: {result}")
        return result
    
    def _process_conditional_inversion(self, sent, inversion_info) -> Dict[str, Any]:
        """条件倒置処理 (Had I known...)"""
        print(f"  🎯 条件倒置処理開始")
        
        result = {
            'tense_type': 'conditional_inversion',
            'metadata': {
                'auxiliary': inversion_info['auxiliary'].text if inversion_info['auxiliary'] else None,
                'pattern': 'conditional_inversion'
            }
        }
        
        # 条件句全体の構築
        conditional_phrase = self._build_conditional_phrase(sent)
        
        # 主節の要素検出（カンマ後の部分）
        main_subject = None
        main_auxiliary = None
        main_verb = None
        
        # 簡易的に主節を検出（カンマ後の部分）
        sentence_text = ' '.join([w.text for w in sent.words])
        if ',' in sentence_text:
            main_part = sentence_text.split(',', 1)[1].strip()
            # 主節の基本要素を抽出
            main_words = main_part.split()
            if len(main_words) >= 3:
                main_subject = main_words[0]  # I
                main_auxiliary = ' '.join(main_words[1:3])  # would have
                main_verb = main_words[3] if len(main_words) > 3 else main_words[-1]  # come
        
        # 上位スロット配置
        if conditional_phrase:
            result['M1'] = conditional_phrase  # 条件句全体をM1に
        if main_subject:
            result['S'] = main_subject
        if main_auxiliary:
            result['Aux'] = main_auxiliary
        if main_verb:
            result['V'] = main_verb
        
        # サブスロット分解（条件句の内部構造）
        auxiliary = inversion_info['auxiliary'].text if inversion_info['auxiliary'] else None
        subject = None
        verb = None
        
        if inversion_info['subject']:
            subject = self._build_phrase(sent, inversion_info['subject'])
        if inversion_info['main_verb']:
            verb = inversion_info['main_verb'].text
        
        if auxiliary:
            result['sub-aux'] = auxiliary
        if subject:
            result['sub-s'] = subject
        if verb:
            result['sub-v'] = verb
        
        print(f"  ✅ 条件倒置分解完了: {result}")
        return result
    
    def _process_comparative_inversion(self, sent, inversion_info) -> Dict[str, Any]:
        """比較倒置処理 (Such was his anger that...)"""
        print(f"  🎯 比較倒置処理開始")
        
        result = {
            'tense_type': 'comparative_inversion',
            'metadata': {
                'inversion_trigger': inversion_info['inversion_trigger'],
                'pattern': 'comparative_inversion'
            }
        }
        
        # 比較句全体の構築（that節まで含む）
        comparative_phrase = self._build_comparative_phrase(sent)
        
        # 主節の要素検出（that節後の部分）
        main_subject = None
        main_auxiliary = None
        main_verb = None
        
        # that節後の主節を検出
        sentence_text = ' '.join([w.text for w in sent.words])
        if ' that ' in sentence_text:
            main_part = sentence_text.split(' that ', 1)[1].strip()
            main_words = main_part.split()
            if len(main_words) >= 2:
                main_subject = main_words[0]  # he
                if len(main_words) >= 3 and main_words[1] in ['could', 'would', 'should', 'might', 'couldn\'t', 'wouldn\'t']:
                    main_auxiliary = main_words[1]  # couldn't
                    main_verb = main_words[2] if len(main_words) > 2 else None  # speak
                else:
                    main_verb = main_words[1]
        
        # 上位スロット配置
        if comparative_phrase:
            result['M1'] = comparative_phrase  # 比較句全体をM1に
        if main_subject:
            result['S'] = main_subject
        if main_auxiliary:
            result['Aux'] = main_auxiliary
        if main_verb:
            result['V'] = main_verb
        
        # サブスロット分解（比較句の内部構造）
        trigger = inversion_info['inversion_trigger']  # Such
        subject = None
        verb = None
        complement = None
        
        if inversion_info['subject']:
            subject = self._build_phrase(sent, inversion_info['subject'])
        if inversion_info['main_verb']:
            verb = inversion_info['main_verb'].text
        
        # 補語検出
        for word in sent.words:
            if word.deprel in ['acomp', 'xcomp', 'nsubj'] and word.text.lower() not in ['he', 'she', 'it', 'they']:
                complement = self._build_phrase(sent, word)
                break
        
        if trigger:
            result['sub-c1'] = trigger.lower()  # such
        if verb:
            result['sub-v'] = verb  # was
        if subject:
            result['sub-s'] = subject  # his anger
        result['sub-m2'] = 'that'  # that
        
        print(f"  ✅ 比較倒置分解完了: {result}")
        return result
    
    def _process_locative_inversion(self, sent, inversion_info) -> Dict[str, Any]:
        """場所倒置処理 (Down the hill ran...)"""
        print(f"  🎯 場所倒置処理開始")
        
        result = {
            'tense_type': 'locative_inversion',
            'metadata': {
                'inversion_trigger': inversion_info['inversion_trigger'],
                'pattern': 'locative_inversion'
            }
        }
        
        trigger = inversion_info['inversion_trigger']
        subject = None
        main_verb = None
        location_phrase = None
        
        if inversion_info['subject']:
            subject = self._build_phrase(sent, inversion_info['subject'])
        if inversion_info['main_verb']:
            main_verb = inversion_info['main_verb'].text
        
        # 場所句の構築
        location_phrase = self._build_location_phrase(sent)
        
        # 上位スロット配置
        if location_phrase:
            result['M1'] = location_phrase
        if main_verb:
            result['V'] = main_verb
        if subject:
            result['S'] = subject
        
        # サブスロット分解
        if subject:
            result['sub-s'] = subject
        if main_verb:
            result['sub-v'] = main_verb
        if location_phrase:
            result['sub-m1'] = location_phrase
        
        print(f"  ✅ 場所倒置分解完了: {result}")
        return result
    
    def _process_inversion_as_subslot(self, sent, inversion_info) -> Dict[str, Any]:
        """倒置構文のサブスロット処理"""
        result = {}
        
        # 基本要素をサブスロットに配置
        if inversion_info['subject']:
            result['sub-s'] = self._build_phrase(sent, inversion_info['subject'])
        if inversion_info['main_verb']:
            result['sub-v'] = inversion_info['main_verb'].text
        if inversion_info['auxiliary']:
            result['sub-aux'] = inversion_info['auxiliary'].text
        if inversion_info['inversion_trigger']:
            result['sub-m1'] = inversion_info['inversion_trigger']
        
        return result
    
    def _process_basic_as_subslot(self, sent) -> Dict[str, Any]:
        """基本構造のサブスロット処理"""
        result = {}
        
        for word in sent.words:
            if word.deprel in ['nsubj', 'nsubj:pass']:
                result['sub-s'] = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                result['sub-v'] = word.text
            elif word.upos == 'AUX':
                result['sub-aux'] = word.text
        
        return result
    
    def _build_phrase(self, sent, head_word):
        """単語を中心とした句の構築"""
        phrase_words = [head_word]
        
        # 依存関係にある単語を収集
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['det', 'amod', 'compound', 'nmod']:
                phrase_words.append(word)
        
        # 語順で並び替え
        phrase_words.sort(key=lambda w: w.id)
        return ' '.join([w.text for w in phrase_words])
    
    def _build_adverbial_phrase(self, sent):
        """副詞句の構築（文頭から動詞まで）"""
        words = []
        for word in sent.words:
            if word.upos in ['ADP', 'ADV', 'DET', 'NOUN'] and word.deprel in ['obl', 'advmod', 'det', 'pobj']:
                words.append(word)
            elif word.upos == 'VERB':
                break
        
        words.sort(key=lambda w: w.id)
        return ' '.join([w.text for w in words]) if words else None
    
    def _build_location_phrase(self, sent):
        """場所句の構築"""
        words = []
        for word in sent.words:
            if word.id <= 3:  # 文頭の3語まで
                words.append(word)
            elif word.upos == 'VERB':
                break
        
        words.sort(key=lambda w: w.id)
        return ' '.join([w.text for w in words]) if words else None
    
    def _build_conditional_phrase(self, sent):
        """条件句の構築（カンマまで）"""
        words = []
        sentence_text = ' '.join([w.text for w in sent.words])
        
        if ',' in sentence_text:
            conditional_part = sentence_text.split(',', 1)[0].strip()
            return conditional_part
        else:
            # カンマがない場合は最初の3-4語
            for i, word in enumerate(sent.words):
                if i < 4:
                    words.append(word)
                else:
                    break
            words.sort(key=lambda w: w.id)
            return ' '.join([w.text for w in words])
    
    def _build_comparative_phrase(self, sent):
        """比較句の構築（that節まで含む）"""
        sentence_text = ' '.join([w.text for w in sent.words])
        
        if ' that ' in sentence_text:
            comparative_part = sentence_text.split(' that ')[0].strip() + ' that'
            return comparative_part
        else:
            # that がない場合は最初の部分
            words = []
            for i, word in enumerate(sent.words):
                if i < 5:
                    words.append(word)
                else:
                    break
            words.sort(key=lambda w: w.id)
            return ' '.join([w.text for w in words])
    
    def _contains_conjunction(self, sentence):
        """接続詞を含む複文かどうかを判定"""
        conjunctions = ['when', 'because', 'since', 'while', 'although', 'though', 'if', 'unless', 'before', 'after']
        sentence_lower = sentence.lower()
        
        for conj in conjunctions:
            if f' {conj} ' in sentence_lower or sentence_lower.startswith(f'{conj} '):
                return True
        return False
