#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完了進行形構文エンジン (Perfect Progressive Engine)
統合アーキテクチャ Phase 2: 高頻度構文パターン

完了進行形構文の上位+サブスロット二重分解処理
"""

import stanza
from typing import Dict, List, Optional, Any

class PerfectProgressiveEngine:
    """完了進行形構文の統合アーキテクチャエンジン"""
    
    def __init__(self):
        """エンジン初期化"""
        print("🚀 完了進行形構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
        
        # 完了進行形パターン定義
        self.auxiliary_patterns = {
            'present_perfect_progressive': ['have', 'has', 'been'],
            'past_perfect_progressive': ['had', 'been'],
            'future_perfect_progressive': ['will', 'have', 'been'],
            'conditional_perfect_progressive': ['would', 'have', 'been']
        }
        
        self.time_markers = {
            'duration': ['for', 'since'],
            'point_in_time': ['when', 'while', 'by', 'until'],
            'frequency': ['already', 'just', 'still', 'recently', 'lately']
        }
        
        print("✅ 初期化完了")
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        独立文としての完了進行形構文処理
        上位スロット + サブスロット の二重分解
        """
        print(f"  🎯 完了進行形エンジン統合処理: {sentence}")
        
        # 接続詞を含む複文の場合は処理を中止（接続詞エンジンに委譲）
        if self._contains_conjunction(sentence):
            print("  ⚠️ 接続詞を検出：接続詞エンジンに委譲")
            return {}
        
        doc = self.nlp(sentence)
        sent = doc.sentences[0]
        
        # 完了進行形構文検出
        perfect_progressive_info = self._detect_perfect_progressive_structure(sent)
        
        if not perfect_progressive_info['detected']:
            print("  ❌ 完了進行形構文が検出されませんでした")
            return {}
        
        # 時制別処理
        tense = perfect_progressive_info['tense']
        if tense == 'present_perfect_progressive':
            return self._process_present_perfect_progressive(sent, perfect_progressive_info)
        elif tense == 'past_perfect_progressive':
            return self._process_past_perfect_progressive(sent, perfect_progressive_info)
        elif tense == 'future_perfect_progressive':
            return self._process_future_perfect_progressive(sent, perfect_progressive_info)
        elif tense == 'perfect_progressive_passive':
            return self._process_perfect_progressive_passive(sent, perfect_progressive_info)
        
        return {}
    
    def process_as_subslot(self, sentence: str) -> Dict[str, str]:
        """
        従属節内完了進行形のサブスロット専用処理
        基本スロット構造 (sub-s, sub-v, sub-aux, sub-m1, etc.) のみ使用
        """
        print(f"  🔧 サブスロット完了進行形処理開始")
        
        doc = self.nlp(sentence)
        sent = doc.sentences[0]
        
        # 完了進行形構文検出
        perfect_progressive_info = self._detect_perfect_progressive_structure(sent)
        
        if not perfect_progressive_info['detected']:
            # 非完了進行形の場合は基本構造で処理
            return self._process_basic_as_subslot(sent)
        
        # 完了進行形のサブスロット処理
        return self._process_perfect_progressive_as_subslot(sent, perfect_progressive_info)
    
    def _detect_perfect_progressive_structure(self, sent) -> Dict[str, Any]:
        """完了進行形構文の検出と分類"""
        perfect_progressive_info = {
            'detected': False,
            'tense': None,
            'auxiliary_chain': [],
            'main_verb': None,
            'present_participle': None,
            'subject': None,
            'time_expressions': [],
            'duration_phrases': [],
            'is_passive': False,
            'is_interrogative': False
        }
        
        # 助動詞と動詞の収集（完了進行形に関連するもののみ）
        auxiliaries = []
        main_verb = None
        present_participle = None
        been_found = False
        
        # 完了進行形パターンに関連する助動詞のみを収集
        for word in sent.words:
            # 助動詞収集（完了進行形文脈のみ）
            if word.upos == 'AUX':
                # have/has/had been や will have been のパターンをチェック
                if word.text.lower() in ['have', 'has', 'had', 'will', 'would', 'been', 'being']:
                    # 完了進行形の文脈かチェック（been + Ving パターン）
                    if self._is_perfect_progressive_context(sent, word):
                        auxiliaries.append(word.text.lower())
                        if word.text.lower() == 'been':
                            been_found = True
            
            # 主動詞・現在分詞検出
            elif word.deprel == 'root':
                main_verb = word
                if word.text.endswith('ing') and word.upos == 'VERB':
                    present_participle = word
            
            # advcl内の現在分詞検出
            elif word.deprel == 'advcl' and word.text.endswith('ing') and word.upos == 'VERB':
                present_participle = word
            
            # 主語検出
            elif word.deprel in ['nsubj', 'nsubj:pass']:
                perfect_progressive_info['subject'] = word
                if word.deprel == 'nsubj:pass':
                    perfect_progressive_info['is_passive'] = True
            
            # 時間表現検出
            elif word.text.lower() in ['for', 'since', 'when', 'while', 'by', 'until', 'already', 'just', 'still']:
                perfect_progressive_info['time_expressions'].append(word)
            
            # 期間表現検出
            elif word.deprel in ['obl', 'obl:tmod', 'obl:unmarked']:
                perfect_progressive_info['duration_phrases'].append(word)
        
        perfect_progressive_info['auxiliary_chain'] = auxiliaries
        perfect_progressive_info['main_verb'] = main_verb
        perfect_progressive_info['present_participle'] = present_participle
        
        # 完了進行形パターン判定
        if been_found and present_participle:
            if 'have' in auxiliaries or 'has' in auxiliaries:
                perfect_progressive_info['tense'] = 'present_perfect_progressive'
                perfect_progressive_info['detected'] = True
            elif 'had' in auxiliaries:
                perfect_progressive_info['tense'] = 'past_perfect_progressive'
                perfect_progressive_info['detected'] = True
            elif 'will' in auxiliaries and 'have' in auxiliaries:
                perfect_progressive_info['tense'] = 'future_perfect_progressive'
                perfect_progressive_info['detected'] = True
            elif 'would' in auxiliaries and 'have' in auxiliaries:
                perfect_progressive_info['tense'] = 'conditional_perfect_progressive'
                perfect_progressive_info['detected'] = True
        
        # 受動完了進行形判定
        if been_found and 'being' in auxiliaries and perfect_progressive_info['is_passive']:
            perfect_progressive_info['tense'] = 'perfect_progressive_passive'
            perfect_progressive_info['detected'] = True
        
        # 疑問文判定
        if auxiliaries and sent.words[0].upos in ['AUX', 'ADV'] and sent.words[-1].text == '?':
            perfect_progressive_info['is_interrogative'] = True
        
        print(f"  📋 完了進行形検出結果: {perfect_progressive_info['tense']}")
        return perfect_progressive_info
    
    def _process_present_perfect_progressive(self, sent, perfect_progressive_info) -> Dict[str, Any]:
        """現在完了進行形処理 (have/has been + Ving)"""
        print(f"  🎯 現在完了進行形処理開始")
        
        result = {
            'tense_type': 'present_perfect_progressive',
            'metadata': {
                'auxiliary_chain': ' '.join(perfect_progressive_info['auxiliary_chain']),
                'main_verb': perfect_progressive_info['present_participle'].text if perfect_progressive_info['present_participle'] else None,
                'duration': None,
                'is_interrogative': perfect_progressive_info['is_interrogative']
            }
        }
        
        # 基本要素の検出
        subject = None
        auxiliary_phrase = None
        main_verb = None
        duration_phrases = []
        location_phrases = []
        wh_phrase = None
        
        # 疑問詞検出 (How long, How many, etc.)
        for word in sent.words:
            if word.upos == 'ADV' and word.deprel == 'advmod' and word.id < 3:
                next_word = sent.words[word.id] if word.id < len(sent.words) else None
                if next_word and next_word.text.lower() == 'long':
                    wh_phrase = f"{word.text} {next_word.text}"
                else:
                    wh_phrase = word.text
        
        # 主語検出
        if perfect_progressive_info['subject']:
            subject = self._build_phrase(sent, perfect_progressive_info['subject'])
        
        # 助動詞句構築
        auxiliary_phrase = self._build_auxiliary_phrase(perfect_progressive_info['auxiliary_chain'])
        
        # 主動詞
        if perfect_progressive_info['present_participle']:
            main_verb = perfect_progressive_info['present_participle'].text
        
        # 期間・場所・目的語の分類
        for word in sent.words:
            if word.deprel == 'obl':
                phrase = self._build_phrase_with_preposition(sent, word)
                if any(time_word in phrase.lower() for time_word in ['for', 'since']):
                    duration_phrases.append(phrase)
                    result['metadata']['duration'] = phrase
                elif any(loc_word in phrase.lower() for loc_word in ['here', 'there', 'at', 'in', 'on']):
                    location_phrases.append(phrase)
            elif word.deprel == 'obj':
                result['O1'] = self._build_phrase(sent, word)
            elif word.deprel == 'advmod' and word.text.lower() in ['here', 'there']:
                location_phrases.append(word.text)
        
        # 上位スロット配置
        if wh_phrase:
            result['M1'] = wh_phrase
        if subject:
            result['S'] = subject
        if auxiliary_phrase:
            result['Aux'] = auxiliary_phrase
        if main_verb:
            result['V'] = main_verb
        if location_phrases:
            slot_key = 'M1' if 'M1' not in result else 'M2'
            result[slot_key] = location_phrases[0]
        if duration_phrases:
            slot_key = 'M2' if 'M2' not in result else 'M3'
            result[slot_key] = duration_phrases[0]
        
        # サブスロット分解 (同じ構造)
        if wh_phrase:
            result['sub-m1'] = wh_phrase
        if subject:
            result['sub-s'] = subject
        if auxiliary_phrase:
            result['sub-aux'] = auxiliary_phrase
        if main_verb:
            result['sub-v'] = main_verb
        if location_phrases:
            slot_key = 'sub-m1' if 'sub-m1' not in result else 'sub-m2'
            result[slot_key] = location_phrases[0]
        if duration_phrases:
            slot_key = 'sub-m2' if 'sub-m2' not in result else 'sub-m3'
            result[slot_key] = duration_phrases[0]
        
        # O1のサブスロット配置
        if 'O1' in result:
            result['sub-o1'] = result['O1']
        
        print(f"  ✅ 現在完了進行形分解完了: {result}")
        return result
    
    def _process_past_perfect_progressive(self, sent, perfect_progressive_info) -> Dict[str, Any]:
        """過去完了進行形処理 (had been + Ving)"""
        print(f"  🎯 過去完了進行形処理開始")
        
        result = {
            'tense_type': 'past_perfect_progressive',
            'metadata': {
                'auxiliary_chain': ' '.join(perfect_progressive_info['auxiliary_chain']),
                'main_verb': perfect_progressive_info['present_participle'].text if perfect_progressive_info['present_participle'] else None,
                'time_clause': None
            }
        }
        
        # 基本要素処理 (現在完了進行形と同様のロジック)
        subject = None
        auxiliary_phrase = None
        main_verb = None
        duration_phrases = []
        time_clauses = []
        
        if perfect_progressive_info['subject']:
            subject = self._build_phrase(sent, perfect_progressive_info['subject'])
        
        auxiliary_phrase = self._build_auxiliary_phrase(perfect_progressive_info['auxiliary_chain'])
        
        if perfect_progressive_info['present_participle']:
            main_verb = perfect_progressive_info['present_participle'].text
        
        # 完了進行形の構成要素のみを処理（接続詞は除外）
        for word in sent.words:
            if word.deprel == 'obl':
                phrase = self._build_phrase_with_preposition(sent, word)
                if any(time_word in phrase.lower() for time_word in ['for', 'since']):
                    duration_phrases.append(phrase)
        
        # 上位スロット配置（完了進行形の主要素のみ）
        if subject:
            result['S'] = subject
        if auxiliary_phrase:
            result['Aux'] = auxiliary_phrase
        if main_verb:
            result['V'] = main_verb
        if duration_phrases:
            result['M1'] = duration_phrases[0]
        
        # サブスロット分解（完了進行形部分のみ）
        if subject:
            result['sub-s'] = subject
        if auxiliary_phrase:
            result['sub-aux'] = auxiliary_phrase
        if main_verb:
            result['sub-v'] = main_verb
        if duration_phrases:
            result['sub-m1'] = duration_phrases[0]
        
        print(f"  ✅ 過去完了進行形分解完了: {result}")
        return result
    
    def _process_future_perfect_progressive(self, sent, perfect_progressive_info) -> Dict[str, Any]:
        """未来完了進行形処理 (will have been + Ving)"""
        print(f"  🎯 未来完了進行形処理開始")
        
        result = {
            'tense_type': 'future_perfect_progressive',
            'metadata': {
                'auxiliary_chain': ' '.join(perfect_progressive_info['auxiliary_chain']),
                'main_verb': perfect_progressive_info['present_participle'].text if perfect_progressive_info['present_participle'] else None,
                'time_reference': None
            }
        }
        
        # 基本要素処理
        subject = None
        auxiliary_phrase = None
        main_verb = None
        time_reference = []
        duration_phrases = []
        location_phrases = []
        
        if perfect_progressive_info['subject']:
            subject = self._build_phrase(sent, perfect_progressive_info['subject'])
        
        auxiliary_phrase = self._build_auxiliary_phrase(perfect_progressive_info['auxiliary_chain'])
        
        if perfect_progressive_info['present_participle']:
            main_verb = perfect_progressive_info['present_participle'].text
        
        # By句・for句の検出
        for word in sent.words:
            if word.deprel == 'obl':
                phrase = self._build_phrase_with_preposition(sent, word)
                if phrase.lower().startswith('by'):
                    time_reference.append(phrase)
                    result['metadata']['time_reference'] = phrase
                elif phrase.lower().startswith('for'):
                    duration_phrases.append(phrase)
            elif word.deprel == 'advmod' and word.text.lower() in ['here', 'there']:
                location_phrases.append(word.text)
        
        # 上位スロット配置
        if time_reference:
            result['M1'] = time_reference[0]
        if subject:
            result['S'] = subject
        if auxiliary_phrase:
            result['Aux'] = auxiliary_phrase
        if main_verb:
            result['V'] = main_verb
        if location_phrases:
            slot_key = 'M2' if 'M1' in result else 'M1'
            result[slot_key] = location_phrases[0]
        if duration_phrases:
            slot_key = 'M3' if 'M2' in result else ('M2' if 'M1' in result else 'M1')
            result[slot_key] = duration_phrases[0]
        
        # サブスロット分解
        if time_reference:
            result['sub-m1'] = time_reference[0]
        if subject:
            result['sub-s'] = subject
        if auxiliary_phrase:
            result['sub-aux'] = auxiliary_phrase
        if main_verb:
            result['sub-v'] = main_verb
        if location_phrases:
            slot_key = 'sub-m2' if 'sub-m1' in result else 'sub-m1'
            result[slot_key] = location_phrases[0]
        if duration_phrases:
            slot_key = 'sub-m3' if 'sub-m2' in result else ('sub-m2' if 'sub-m1' in result else 'sub-m1')
            result[slot_key] = duration_phrases[0]
        
        print(f"  ✅ 未来完了進行形分解完了: {result}")
        return result
    
    def _process_perfect_progressive_passive(self, sent, perfect_progressive_info) -> Dict[str, Any]:
        """受動完了進行形処理 (has been being + Ved)"""
        print(f"  🎯 受動完了進行形処理開始")
        
        result = {
            'tense_type': 'perfect_progressive_passive',
            'metadata': {
                'auxiliary_chain': ' '.join(perfect_progressive_info['auxiliary_chain']),
                'main_verb': perfect_progressive_info['main_verb'].text if perfect_progressive_info['main_verb'] else None,
                'voice': 'passive'
            }
        }
        
        # 基本要素処理
        subject = None
        auxiliary_phrase = None
        main_verb = None
        time_phrases = []
        
        if perfect_progressive_info['subject']:
            subject = self._build_phrase(sent, perfect_progressive_info['subject'])
        
        auxiliary_phrase = self._build_auxiliary_phrase(perfect_progressive_info['auxiliary_chain'])
        
        if perfect_progressive_info['main_verb']:
            main_verb = perfect_progressive_info['main_verb'].text
        
        # since句の検出
        for word in sent.words:
            if word.deprel == 'obl':
                phrase = self._build_phrase_with_preposition(sent, word)
                if phrase.lower().startswith('since'):
                    time_phrases.append(phrase)
        
        # 上位スロット配置
        if subject:
            result['S'] = subject
        if auxiliary_phrase:
            result['Aux'] = auxiliary_phrase
        if main_verb:
            result['V'] = main_verb
        if time_phrases:
            result['M1'] = time_phrases[0]
        
        # サブスロット分解
        if subject:
            result['sub-s'] = subject
        if auxiliary_phrase:
            result['sub-aux'] = auxiliary_phrase
        if main_verb:
            result['sub-v'] = main_verb
        if time_phrases:
            result['sub-m1'] = time_phrases[0]
        
        print(f"  ✅ 受動完了進行形分解完了: {result}")
        return result
    
    def _process_perfect_progressive_as_subslot(self, sent, perfect_progressive_info) -> Dict[str, str]:
        """完了進行形のサブスロット専用処理"""
        result = {}
        
        # 主語
        if perfect_progressive_info['subject']:
            result['sub-s'] = self._build_phrase(sent, perfect_progressive_info['subject'])
        
        # 助動詞
        auxiliary_phrase = self._build_auxiliary_phrase(perfect_progressive_info['auxiliary_chain'])
        if auxiliary_phrase:
            result['sub-aux'] = auxiliary_phrase
        
        # 主動詞
        if perfect_progressive_info['present_participle']:
            result['sub-v'] = perfect_progressive_info['present_participle'].text
        elif perfect_progressive_info['main_verb']:
            result['sub-v'] = perfect_progressive_info['main_verb'].text
        
        # その他の要素
        m_slot_counter = 1
        for word in sent.words:
            if word.deprel == 'obj':
                result['sub-o1'] = self._build_phrase(sent, word)
            elif word.deprel in ['obl', 'advmod'] and word.text.lower() not in perfect_progressive_info['auxiliary_chain']:
                if word.deprel == 'obl':
                    phrase = self._build_phrase_with_preposition(sent, word)
                else:
                    phrase = word.text
                
                slot_key = f'sub-m{m_slot_counter}'
                if slot_key not in result:
                    result[slot_key] = phrase
                    m_slot_counter += 1
        
        return result
    
    def _process_basic_as_subslot(self, sent) -> Dict[str, str]:
        """非完了進行形の基本サブスロット処理"""
        result = {}
        
        for word in sent.words:
            if word.deprel == 'nsubj':
                result['sub-s'] = self._build_phrase(sent, word)
            elif word.deprel == 'root':
                result['sub-v'] = word.text
            elif word.deprel == 'obj':
                result['sub-o1'] = self._build_phrase(sent, word)
        
        return result
    
    def _build_auxiliary_phrase(self, auxiliary_chain: List[str]) -> str:
        """助動詞句の構築"""
        return ' '.join(auxiliary_chain)
    
    def _build_phrase(self, sent, head_word):
        """語句の構築 (修飾語含む)"""
        phrase_words = [head_word]
        
        # 修飾語を収集
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['det', 'amod', 'nmod:poss', 'nummod', 'compound']:
                phrase_words.append(word)
        
        # 位置順でソート
        phrase_words.sort(key=lambda x: x.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _build_phrase_with_preposition(self, sent, head_word):
        """前置詞句の構築"""
        # 前置詞を探す
        prep = None
        for word in sent.words:
            if word.deprel == 'case' and word.head == head_word.id:
                prep = word.text
                break
        
        main_phrase = self._build_phrase(sent, head_word)
        return f"{prep} {main_phrase}" if prep else main_phrase
    
    def _build_advcl_phrase(self, sent, head_word):
        """副詞節句の構築"""
        # 接続詞を探す
        conjunction = None
        for word in sent.words:
            if word.deprel == 'mark' and word.head == head_word.id:
                conjunction = word.text
                break
        
        # 副詞節の構成要素を収集
        clause_words = [head_word]
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['nsubj', 'aux', 'obj', 'obl', 'advmod']:
                clause_words.append(word)
        
        clause_words.sort(key=lambda x: x.id)
        clause_text = ' '.join(w.text for w in clause_words)
        
        return f"{conjunction} {clause_text}" if conjunction else clause_text

    def _decompose_time_clause_to_subslots(self, result, time_clause):
        """時間節をサブスロットに分解"""
        # 簡単な分解（when I arrived → sub-s: I, sub-v: arrived）
        if 'when' in time_clause.lower():
            parts = time_clause.lower().replace('when ', '').strip()
            if ' ' in parts:
                words = parts.split()
                if len(words) >= 2:
                    result['sub-s'] = words[0]  # 主語
                    result['sub-v'] = words[1]  # 動詞
        elif 'because' in time_clause.lower():
            # because節の処理は別エンジンに委譲
            pass
    
    def _is_perfect_progressive_context(self, sent, aux_word):
        """助動詞が完了進行形の文脈かを判定"""
        # been の後に現在分詞があるかチェック
        if aux_word.text.lower() == 'been':
            for word in sent.words:
                if (word.id > aux_word.id and 
                    word.text.endswith('ing') and 
                    word.upos == 'VERB' and
                    abs(word.id - aux_word.id) <= 3):  # been の近くにある
                    return True
        
        # have/has/had の後に been があるかチェック
        elif aux_word.text.lower() in ['have', 'has', 'had']:
            for word in sent.words:
                if (word.id > aux_word.id and 
                    word.text.lower() == 'been' and
                    abs(word.id - aux_word.id) <= 2):  # have の近くにある
                    return True
        
        # will/would の後に have been があるかチェック
        elif aux_word.text.lower() in ['will', 'would']:
            next_words = [w.text.lower() for w in sent.words if w.id > aux_word.id and w.id <= aux_word.id + 3]
            if 'have' in next_words and 'been' in next_words:
                return True
        
        return False
    
    def _contains_conjunction(self, sentence):
        """接続詞を含む複文かどうかを判定"""
        conjunctions = ['when', 'because', 'since', 'while', 'although', 'though', 'if', 'unless', 'before', 'after']
        sentence_lower = sentence.lower()
        
        for conj in conjunctions:
            if f' {conj} ' in sentence_lower or sentence_lower.startswith(f'{conj} '):
                return True
        return False
