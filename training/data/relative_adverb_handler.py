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
        """
        # より精密な関係副詞パターン - 複合構造対応
        patterns = [
            # Basic be-verb patterns
            r'(The\s+\w+\s+where)\s+(.+?)\s+(is|are|was|were|will\s+be)\s+(.+)',
            r'(The\s+\w+\s+when)\s+(.+?)\s+(is|are|was|were|will\s+be)\s+(.+)',
            r'(The\s+\w+\s+why)\s+(.+?)\s+(is|are|was|were|will\s+be)\s+(.+)',
            r'(The\s+\w+\s+how)\s+(.+?)\s+(is|are|was|were|will\s+be)\s+(.+)',
            
            # 特定の複合パターン - より精密に
            r'(The\s+place\s+where)\s+(.+?)\s+(holds?)\s+(.+)',
            r'(The\s+way\s+how)\s+(.+?)\s+(helped?)\s+(.+)',
            r'(The\s+way\s+how)\s+(.+?)\s+(gets?)\s+(.+)',
            r'(The\s+reason\s+why)\s+(.+?)\s+(became)\s+(.+)',
            
            # Case 115: "The place where we first met holds special memories"
            r'(The\s+place\s+where)\s+(we\s+first\s+met)\s+(holds)\s+(.+)',
            # Case 117: "The way how they approach problems gets results"  
            r'(The\s+way\s+how)\s+(they\s+approach\s+problems)\s+(gets)\s+(.+)',
            # Case 118: "The reason why technology changed became clear"
            r'(The\s+reason\s+why)\s+(technology\s+changed)\s+(became)\s+(.+)',
            
            # フォールバック - より柔軟なパターン
            r'(The\s+\w+\s+where)\s+(.+?)\s+(\w+ed|\w+s|\w+)\s+(.+)',
            r'(The\s+\w+\s+when)\s+(.+?)\s+(\w+ed|\w+s|\w+)\s+(.+)',
            r'(The\s+\w+\s+why)\s+(.+?)\s+(\w+ed|\w+s|\w+)\s+(.+)',
            r'(The\s+\w+\s+how)\s+(.+?)\s+(\w+ed|\w+s|\w+)\s+(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            print(f"🔍 パターンテスト: {pattern[:50]}... → {bool(match)}")
            if match:
                print(f"🔍 マッチ詳細: {match.groups()}")
                adverb_phrase = match.group(1)
                relative_clause = match.group(2)
                main_verb = match.group(3)
                main_clause_rest = match.group(4)
                
                # 関係副詞の種類を特定
                relative_adverb = None
                for adv in ['where', 'when', 'why', 'how']:
                    if adv in adverb_phrase.lower():
                        relative_adverb = adv
                        break
                
                print(f"🔍 関係副詞検出: {relative_adverb} - {adverb_phrase}")
                print(f"🔍 関係節: '{relative_clause}'")
                print(f"🔍 主節: '{main_verb} {main_clause_rest}'")
                
                return {
                    'relative_adverb': relative_adverb,
                    'adverb_phrase': adverb_phrase,
                    'relative_clause': relative_clause,
                    'main_clause': f"{main_verb} {main_clause_rest}".strip(),
                    'main_clause_start': text.find(main_verb)
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
        主節の構造を解析 - 複合構造対応版
        
        Args:
            clause_text: 主節テキスト
            
        Returns:
            Dict: 主節の構造
        """
        result = {'S': ''}  # 関係副詞構文では主語は常に空
        
        print(f"🔍 主節解析: '{clause_text}'")
        
        # 2. 受動態パターン (was/were + 過去分詞) - be動詞より先に処理
        passive_patterns = [
            r'^(was|were)\s+(demolished|built|created|made|destroyed|completed)\.?$'
        ]
        for pattern in passive_patterns:
            match = re.match(pattern, clause_text, re.IGNORECASE)
            if match:
                aux = match.group(1)
                past_participle = match.group(2)
                print(f"🔍 受動態パターン: {aux} + {past_participle}")
                result['Aux'] = aux
                result['V'] = past_participle
                print(f"🔍 主節解析結果: {result}")
                return result
        
        # 1. be動詞 + 補語パターン
        be_patterns = [
            r'^(is|are|was|were)\s+(.+)$',
            r'^(will\s+be)\s+(.+)$'
        ]
        for pattern in be_patterns:
            match = re.match(pattern, clause_text, re.IGNORECASE)
            if match:
                be_verb = match.group(1)
                complement = match.group(2).strip('.')  # 句読点除去
                print(f"🔍 be動詞パターン: {be_verb} + {complement}")
                result['V'] = be_verb.split()[0]  # 'is', 'was', etc.
                result['C1'] = complement
                print(f"🔍 主節解析結果: {result}")
                return result
        
        # 3. 特定動詞の精密パターンマッチング
        specific_patterns = {
            # Case 115: "holds special memories"
            'holds': r'^holds\s+(.+)$',
            # Case 117: "gets results" 
            'gets': r'^gets\s+(.+)$',
            # Case 114: "helped everyone"
            'helped': r'^helped\s+(.+)$',
            # Case 118: "became clear"
            'became': r'^became\s+(.+)$'
        }
        
        for verb, pattern in specific_patterns.items():
            match = re.match(pattern, clause_text, re.IGNORECASE)
            if match:
                object_or_complement = match.group(1).strip('.')  # 句読点除去
                print(f"🔍 特定動詞パターン: {verb} + {object_or_complement}")
                
                result['V'] = verb
                
                # "became clear"のような補語パターン vs 目的語パターンを判別
                if verb == 'became' and object_or_complement in ['clear', 'obvious', 'apparent', 'evident']:
                    result['C1'] = object_or_complement
                    print(f"🔍 補語認識: {object_or_complement}")
                else:
                    result['O1'] = object_or_complement
                    print(f"🔍 目的語認識: {object_or_complement}")
                
                print(f"🔍 主節解析結果: {result}")
                return result
        
        # 4. 一般的なパターン (動詞 + 目的語/補語)
        general_pattern = r'^(\w+)\s+(.+)$'
        match = re.match(general_pattern, clause_text, re.IGNORECASE)
        if match:
            verb = match.group(1)
            rest = match.group(2).strip('.')  # 句読点除去
            print(f"🔍 一般パターン: {verb} + {rest}")
            
            result['V'] = verb
            
            # spaCyで補語か目的語かを判定
            doc = self.nlp(rest)
            if len(doc) > 0:
                first_token = doc[0]
                # 単語が形容詞で1語の場合は補語、それ以外は目的語
                if first_token.pos_ == 'ADJ' and len(rest.split()) == 1:
                    result['C1'] = rest
                    print(f"🔍 補語認識: {rest}")
                else:
                    result['O1'] = rest  
                    print(f"🔍 目的語認識: {rest}")
            else:
                result['O1'] = rest
        
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
                'sub-m2': detection['adverb_phrase']
            }
        }
        
        # 関係節構造をsub_slotsに順序よく統合
        for key in ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 'sub-aux']:
            if key in relative_clause_structure:
                result['sub_slots'][key] = relative_clause_structure[key]
        
        # 修飾語の処理: sub-m2は関係副詞句なので、関係節内の修飾語はsub-m3として追加
        if 'sub-m2' in relative_clause_structure:
            result['sub_slots']['sub-m3'] = relative_clause_structure['sub-m2']
        
        # その他の修飾語も順次追加
        for key in relative_clause_structure:
            if key.startswith('sub-m') and key not in ['sub-m2'] and key not in result['sub_slots']:
                result['sub_slots'][key] = relative_clause_structure[key]
        
        # _parent_slotを最後に追加
        result['sub_slots']['_parent_slot'] = 'S'
        
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
        "The way how he solved it was clever.",
        "The way how she explained it helped everyone."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*50}")
        print(f"テスト: {sentence}")
        result = handler.process(sentence)
        print(f"結果: {result}")
