#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RelativeAdverbHandler: 関係副詞処理ハンドラー
where/when/why/how構文を適切なsub_slotsに分解する専門ハンドラー
"""

import re
import spacy
from typing import Dict, Any, Tuple, Optional

class RelativeAdverbHandler:
    """関係副詞処理ハンドラー"""
    
    def __init__(self, collaborators=None):
        """
        初期化
        
        Args:
            collaborators: 協力者ハンドラー辞書
                - 'adverb': AdverbHandler（修飾語分離）
                - 'five_pattern': BasicFivePatternHandler（5文型分析）
                - 'passive': PassiveVoiceHandler（受動態理解）
                - 'modal': ModalHandler（助動詞処理）
        """
        self.name = "RelativeAdverbHandler"
        self.version = "v1.0"
        self.nlp = spacy.load('en_core_web_sm')
        
        # 協力者ハンドラーたち
        if collaborators:
            self.adverb_handler = collaborators.get('adverb') or collaborators.get('AdverbHandler')
            self.five_pattern_handler = collaborators.get('five_pattern') or collaborators.get('FivePatternHandler')
            self.passive_handler = collaborators.get('passive') or collaborators.get('PassiveHandler')
            self.modal_handler = collaborators.get('modal') or collaborators.get('ModalHandler')
        else:
            self.adverb_handler = None
            self.five_pattern_handler = None
            self.passive_handler = None
            self.modal_handler = None
    
    def detect_relative_adverb(self, text: str) -> Optional[Dict[str, Any]]:
        """
        関係副詞構文を検出する
        
        Args:
            text: 検査対象テキスト
            
        Returns:
            Dict: 検出結果 or None
                {
                    'relative_adverb': 'where'|'when'|'why'|'how',
                    'adverb_phrase': 'The place where',
                    'relative_clause': 'we met',
                    'main_clause': 'is beautiful',
                    'main_clause_start': int
                }
        """
        # より柔軟な関係副詞パターン
        patterns = [
            # The [noun] where [subject] [verb] [rest] [main_verb] [rest]
            r'(The\s+\w+\s+where)\s+([^.]+?)\s+(is|are|was|were|will\s+be|became|become|gets?|got|helps?|helped|holds?|held)',
            # The [noun] when [subject] [verb] [rest] [main_verb] [rest]  
            r'(The\s+\w+\s+when)\s+([^.]+?)\s+(is|are|was|were|will\s+be|became|become|gets?|got|helps?|helped|changed?|changes)',
            # The [noun] why [subject] [verb] [rest] [main_verb] [rest]
            r'(The\s+\w+\s+why)\s+([^.]+?)\s+(is|are|was|were|will\s+be|became|become|gets?|got)',
            # The [noun] how [subject] [verb] [rest] [main_verb] [rest]
            r'(The\s+\w+\s+how)\s+([^.]+?)\s+(is|are|was|were|will\s+be|became|become|gets?|got|helps?|helped|was)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                adverb_phrase = match.group(1)
                full_middle = match.group(2)  # 関係節 + 主節の動詞まで
                main_verb = match.group(3)
                
                # 関係副詞の種類を特定
                relative_adverb = None
                for adv in ['where', 'when', 'why', 'how']:
                    if adv in adverb_phrase.lower():
                        relative_adverb = adv
                        break
                
                # 関係節と主節を分離（主節の動詞位置を基準に）
                # まず主節の動詞位置を特定
                main_verb_match = re.search(rf'\b{re.escape(main_verb)}\b', text)
                if main_verb_match:
                    main_clause_start = main_verb_match.start()
                    main_clause = text[main_clause_start:].strip()
                    
                    # 関係節は adverb_phrase の後から main_verb の前まで
                    adverb_end = text.find(adverb_phrase) + len(adverb_phrase)
                    relative_clause = text[adverb_end:main_clause_start].strip()
                    
                    print(f"🔍 関係副詞検出: {relative_adverb} - {adverb_phrase}")
                    print(f"🔍 関係節: '{relative_clause}'")
                    print(f"🔍 主節: '{main_clause}'")
                    
                    return {
                        'relative_adverb': relative_adverb,
                        'adverb_phrase': adverb_phrase,
                        'relative_clause': relative_clause,
                        'main_clause': main_clause,
                        'main_clause_start': main_clause_start
                    }
        
        return None
    
    def parse_relative_clause(self, clause_text: str) -> Dict[str, Any]:
        """
        関係節内の構造を解析
        
        Args:
            clause_text: 関係節テキスト ('we met', 'he arrived', etc.)
            
        Returns:
            Dict: 関係節の構造
        """
        result = {}
        
        # spaCyで解析
        doc = self.nlp(clause_text)
        tokens = [token for token in doc]
        
        # 修飾語があるかチェック（協力者に依頼）
        modifier_result = {}
        if self.adverb_handler:
            adverb_processing = self.adverb_handler.process(clause_text)
            if adverb_processing.get('success'):
                modifier_result = adverb_processing.get('modifier_slots', {})
                if modifier_result:
                    print(f"🎯 関係節内修飾語検出: {modifier_result}")
        
        # 基本的なS-V-O構造を検出
        subject = None
        verb = None
        objects = []
        aux_verb = None
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # 助動詞検出
            if token.pos_ == 'AUX' or token.lemma_ in ['will', 'would', 'can', 'could', 'may', 'might', 'should', 'must']:
                aux_verb = token.text
                print(f"🔍 関係節内助動詞: {aux_verb}")
                
            # 主語検出（代名詞・名詞）
            elif token.pos_ in ['PRON', 'NOUN', 'PROPN'] and not subject:
                subject = token.text
                
            # 動詞検出
            elif token.pos_ == 'VERB' and not verb:
                verb = token.text
                
            # 目的語検出（動詞の後の名詞句）
            elif token.pos_ in ['NOUN', 'PRON', 'PROPN'] and verb and subject:
                # 複数語の目的語をまとめて取得
                obj_parts = [token.text]
                j = i + 1
                while j < len(tokens) and tokens[j].pos_ in ['DET', 'ADJ', 'NOUN']:
                    obj_parts.append(tokens[j].text)
                    j += 1
                objects.append(' '.join(obj_parts))
                i = j - 1  # ループを調整
                
            i += 1
        
        # 結果構築
        if subject:
            result['sub-s'] = subject
        if aux_verb:
            result['sub-aux'] = aux_verb
        if verb:
            result['sub-v'] = verb
        if objects:
            for idx, obj in enumerate(objects, 1):
                result[f'sub-o{idx}'] = obj
        
        # 修飾語も追加
        if modifier_result:
            for key, value in modifier_result.items():
                if key.startswith('M') and value:
                    result[f'sub-m{key[1:]}'] = value
        
        print(f"🔍 関係節解析結果: {result}")
        return result
    
    def parse_main_clause(self, clause_text: str) -> Dict[str, Any]:
        """
        主節の構造を解析
        
        Args:
            clause_text: 主節テキスト
            
        Returns:
            Dict: 主節の構造
        """
        result = {}
        
        # spaCyで基本解析
        doc = self.nlp(clause_text)
        tokens = [token for token in doc]
        
        # 基本的なS-V-O-C構造を検出
        subject = ''  # 関係副詞構文では主語は空
        verb = None
        aux_verb = None
        complement = None
        objects = []
        
        # be動詞 + 形容詞/名詞 のパターンを優先的に検出
        if re.search(r'(is|are|was|were)\s+(\w+)', clause_text):
            be_match = re.search(r'(is|are|was|were)\s+(\w+)', clause_text)
            if be_match:
                aux_verb = be_match.group(1)
                complement = be_match.group(2)
                # be動詞の場合、VとAuxが同じ場合がある
                verb = aux_verb
                print(f"🔍 be動詞パターン: {aux_verb} + {complement}")
        
        # その他の動詞パターン
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # 助動詞検出（まだ設定されていない場合）
            if not aux_verb and (token.pos_ == 'AUX' or token.lemma_ in ['will', 'would', 'can', 'could', 'may', 'might', 'should', 'must']):
                aux_verb = token.text
                print(f"🔍 主節助動詞: {aux_verb}")
                
            # 動詞検出（まだ設定されていない場合）
            elif not verb and token.pos_ == 'VERB':
                verb = token.text
                print(f"🔍 主節動詞: {verb}")
                
            # 形容詞（補語）検出（まだ設定されていない場合）
            elif not complement and token.pos_ == 'ADJ':
                complement = token.text
                print(f"🔍 主節補語: {complement}")
                
            # 目的語検出（動詞の後の名詞句）
            elif token.pos_ in ['NOUN', 'PRON', 'PROPN'] and verb and not complement:
                # 複数語の目的語をまとめて取得
                obj_parts = [token.text]
                j = i + 1
                while j < len(tokens) and tokens[j].pos_ in ['DET', 'ADJ', 'NOUN']:
                    obj_parts.append(tokens[j].text)
                    j += 1
                objects.append(' '.join(obj_parts))
                i = j - 1  # ループを調整
                print(f"🔍 主節目的語: {' '.join(obj_parts)}")
                
            i += 1
        
        # 結果構築
        result['S'] = subject  # 関係副詞構文では常に空
        
        # be動詞の場合の特別処理
        if aux_verb in ['is', 'are', 'was', 'were'] and complement:
            result['V'] = aux_verb
            result['C1'] = complement
        else:
            if aux_verb and verb and aux_verb != verb:
                result['Aux'] = aux_verb
            if verb:
                result['V'] = verb
            if complement:
                result['C1'] = complement
        
        if objects:
            for idx, obj in enumerate(objects, 1):
                result[f'O{idx}'] = obj
        
        print(f"🔍 主節解析結果: {result}")
        return result
    
    def process(self, text: str, original_text: str = None) -> Dict[str, Any]:
        """
        関係副詞処理メイン
        
        Args:
            text: 処理対象テキスト
            original_text: オリジナルテキスト
            
        Returns:
            Dict: 処理結果
        """
        print(f"🔍 関係副詞ハンドラー開始: '{text}'")
        
        # 関係副詞構文検出
        detection = self.detect_relative_adverb(text)
        if not detection:
            return {'success': False, 'reason': 'No relative adverb detected'}
        
        # 関係節解析
        relative_clause_structure = self.parse_relative_clause(detection['relative_clause'])
        
        # 主節解析
        main_clause_structure = self.parse_main_clause(detection['main_clause'])
        
        # 結果統合
        result = {
            'success': True,
            'handler': self.name,
            'relative_adverb': detection['relative_adverb'],
            'main_slots': main_clause_structure,
            'sub_slots': {
                'sub-m2': detection['adverb_phrase'],
                '_parent_slot': 'S'
            }
        }
        
        # 関係節構造をsub_slotsに統合
        result['sub_slots'].update(relative_clause_structure)
        
        # 主節のSを空にする（関係副詞構文では主語がsub_slotsに移動）
        if 'S' in result['main_slots']:
            result['main_slots']['S'] = ''
        
        print(f"✅ 関係副詞処理完了: {result}")
        return result

if __name__ == "__main__":
    # テスト用
    handler = RelativeAdverbHandler()
    
    test_sentences = [
        "The place where we met is beautiful.",
        "The time when he arrived was late.",
        "The reason why she left is unclear.",
        "The way how he solved it was clever."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*50}")
        print(f"テスト: {sentence}")
        result = handler.process(sentence)
        print(f"結果: {result}")
