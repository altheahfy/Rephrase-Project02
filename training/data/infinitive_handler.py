#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InfinitiveHandler: 不定詞処理ハンドラー
to不定詞の名詞的・形容詞的・副詞的用法の専門分解
専門分担型ハイブリッド解析（品詞分析 + 依存関係）+ 人間的文法認識
ハードコーディング極力排除・汎用的システム設計
"""

import spacy
from typing import Dict, Any, List, Tuple, Optional

class InfinitiveHandler:
    """不定詞処理ハンドラー（Human Grammar Pattern + spaCy解析）"""
    
    def __init__(self, nlp_model=None, collaborators=None):
        """
        初期化
        
        Args:
            nlp_model: spaCyモデル（品詞分析・依存関係解析用）
            collaborators: 他ハンドラーとの協力体制
        """
        self.nlp = nlp_model or spacy.load('en_core_web_sm')
        self.collaborators = collaborators or {}
        
        print("🔧 InfinitiveHandler初期化: Human Grammar Pattern + spaCy解析")
    
    def can_handle(self, text: str) -> bool:
        """
        不定詞構文を処理可能かチェック（spaCy依存関係解析ベース）
        
        Args:
            text: 処理対象の英文
            
        Returns:
            bool: 処理可能な場合True
        """
        try:
            doc = self.nlp(text)
            
            # spaCy依存関係解析による不定詞検出
            for token in doc:
                # to + VERB の依存関係パターンを検出
                if (token.text.lower() == 'to' and 
                    token.pos_ == 'PART' and  # to は PART (particle) として分類
                    any(child.pos_ == 'VERB' for child in token.children)):
                    return True
                
                # xcomp (open clausal complement) での不定詞検出
                if token.dep_ == 'xcomp' and token.pos_ == 'VERB':
                    # xcompの前にtoがあるかチェック
                    for child in token.children:
                        if child.text.lower() == 'to' and child.dep_ == 'aux':
                            return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ can_handle解析エラー: {e}")
            return False
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        不定詞構文の分解処理
        
        Args:
            text: 処理対象の英文
            
        Returns:
            Dict[str, Any]: 分解結果
        """
        print(f"🔧 InfinitiveHandler処理開始: '{text}'")
        
        try:
            # spaCy解析
            doc = self.nlp(text)
            
            # 不定詞の検出と分類
            infinitive_info = self._analyze_infinitive_structure(doc, text)
            
            if infinitive_info['found']:
                # 不定詞用法に応じた処理
                return self._process_by_usage_type(doc, text, infinitive_info)
            else:
                return {
                    'success': False,
                    'error': '不定詞構文が検出されませんでした',
                    'text': text
                }
                
        except Exception as e:
            print(f"❌ InfinitiveHandler処理エラー: {str(e)}")
            return {
                'success': False,
                'error': f'InfinitiveHandler処理エラー: {str(e)}',
                'text': text
            }
    
    def _analyze_infinitive_structure(self, doc, text: str) -> Dict[str, Any]:
        """
        不定詞構造の分析（spaCy依存関係解析ベース）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            
        Returns:
            Dict[str, Any]: 不定詞構造情報
        """
        print(f"🔍 不定詞構造解析開始: spaCy依存関係分析")
        
        infinitive_info = {
            'found': False,
            'infinitive_tokens': [],
            'usage_patterns': [],
            'syntactic_role': None,
            'dependency_info': []
        }
        
        # spaCy依存関係による不定詞検出
        for token in doc:
            # パターン1: xcomp (open clausal complement) + aux=to
            if token.dep_ == 'xcomp' and token.pos_ == 'VERB':
                for child in token.children:
                    if child.text.lower() == 'to' and child.dep_ == 'aux':
                        infinitive_info['found'] = True
                        infinitive_info['infinitive_tokens'].append({
                            'main_verb': token,
                            'to_token': child,
                            'pattern': 'xcomp_aux',
                            'head': token.head,
                            'dependency': token.dep_
                        })
                        print(f"   ✅ xcomp不定詞検出: '{child.text} {token.text}' (head: {token.head.text})")
            
            # パターン2: advcl (adverbial clause) + mark=to  
            elif token.dep_ == 'advcl' and token.pos_ == 'VERB':
                for child in token.children:
                    if child.text.lower() == 'to' and child.dep_ == 'mark':
                        infinitive_info['found'] = True
                        infinitive_info['infinitive_tokens'].append({
                            'main_verb': token,
                            'to_token': child,
                            'pattern': 'advcl_mark',
                            'head': token.head,
                            'dependency': token.dep_
                        })
                        print(f"   ✅ advcl不定詞検出: '{child.text} {token.text}' (head: {token.head.text})")
            
            # パターン3: ccomp (clausal complement) + aux=to
            elif token.dep_ == 'ccomp' and token.pos_ == 'VERB':
                for child in token.children:
                    if child.text.lower() == 'to' and child.dep_ == 'aux':
                        infinitive_info['found'] = True
                        infinitive_info['infinitive_tokens'].append({
                            'main_verb': token,
                            'to_token': child,
                            'pattern': 'ccomp_aux',
                            'head': token.head,
                            'dependency': token.dep_
                        })
                        print(f"   ✅ ccomp不定詞検出: '{child.text} {token.text}' (head: {token.head.text})")
        
        # 用法分類（依存関係ベース）
        if infinitive_info['found']:
            infinitive_info['syntactic_role'] = self._analyze_syntactic_role(doc, infinitive_info)
        
        return infinitive_info
    
    def _analyze_syntactic_role(self, doc, infinitive_info: Dict) -> str:
        """
        不定詞の統語的役割分析（spaCy依存関係ベース）
        
        Args:
            doc: spaCy解析結果
            infinitive_info: 不定詞情報
            
        Returns:
            str: 統語的役割
        """
        print(f"🧠 統語的役割分析: Human Grammar Pattern")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            pattern = inf_token['pattern']
            head = inf_token['head']
            dependency = inf_token['dependency']
            
            # xcomp: 通常は目的語補語（形容詞的・副詞的用法）
            if pattern == 'xcomp_aux':
                if head.pos_ == 'VERB':
                    print(f"   📝 xcomp + 動詞head → 目的語補語（形容詞的用法候補）")
                    return 'adjectival_complement'
                    
            # advcl: 副詞節（副詞的用法）
            elif pattern == 'advcl_mark':
                print(f"   📝 advcl + mark → 副詞節（副詞的用法）")
                return 'adverbial_clause'
                
            # ccomp: 補語節（名詞的用法候補）
            elif pattern == 'ccomp_aux':
                print(f"   📝 ccomp + 補語節 → 名詞的用法候補")
                return 'nominal_complement'
        
        return 'unknown'
    
    def _process_by_usage_type(self, doc, text: str, infinitive_info: Dict) -> Dict[str, Any]:
        """
        用法タイプ別の処理（spaCy依存関係解析ベース）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"🎯 用法別処理開始: {infinitive_info.get('syntactic_role', 'unknown')}")
        
        # スロット分類の実行
        slots = self._classify_slot_types(doc, infinitive_info)
        
        syntactic_role = infinitive_info.get('syntactic_role', 'unknown')
        
        if syntactic_role == 'nominal_complement':
            return self._process_nominal_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'adjectival_complement':
            return self._process_adjectival_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'adverbial_clause':
            return self._process_adverbial_infinitive(doc, text, infinitive_info, slots)
        else:
            return self._process_basic_infinitive(doc, text, infinitive_info, slots)
    
    def _classify_slot_types(self, doc, infinitive_info: Dict[str, Any]) -> Dict[str, str]:
        """
        不定詞構造のスロット分類（spaCy依存関係解析ベース）
        
        Args:
            doc: spaCy解析結果
            infinitive_info: 不定詞構造情報
            
        Returns:
            Dict[str, str]: スロット分類結果
        """
        print(f"🎯 スロット分類: spaCy依存関係による詳細解析")
        
        slots = {}
        
        for inf_token in infinitive_info['infinitive_tokens']:
            main_verb = inf_token['main_verb']
            to_token = inf_token['to_token']
            head = inf_token['head']
            pattern = inf_token['pattern']
            
            # 不定詞マーカー分類
            slots[to_token.text] = 'inf-marker'
            print(f"   📌 '{to_token.text}' → inf-marker")
            
            # 不定詞動詞分類
            slots[main_verb.text] = self._classify_infinitive_verb(main_verb, pattern, head)
            print(f"   🔧 '{main_verb.text}' → {slots[main_verb.text]}")
            
            # 主動詞分類
            if head.pos_ == 'VERB' and head.text not in slots:
                slots[head.text] = self._classify_main_verb(head, pattern)
                print(f"   ⚙️ '{head.text}' → {slots[head.text]}")
            
            # 不定詞の引数分析
            self._analyze_infinitive_arguments(main_verb, slots)
        
        return slots
    
    def _classify_infinitive_verb(self, verb_token, pattern: str, head) -> str:
        """
        不定詞動詞の分類
        
        Args:
            verb_token: 不定詞動詞トークン
            pattern: 依存関係パターン
            head: 統語的支配語
            
        Returns:
            str: スロット分類
        """
        # xcomp: 補語動詞
        if pattern == 'xcomp_aux':
            return 'inf-complement-verb'
        
        # advcl: 副詞句動詞
        elif pattern == 'advcl_mark':
            return 'inf-adverbial-verb'
        
        # ccomp: 補語節動詞
        elif pattern == 'ccomp_aux':
            return 'inf-clausal-verb'
        
        return 'inf-verb'
    
    def _classify_main_verb(self, verb_token, pattern: str) -> str:
        """
        主動詞の分類
        
        Args:
            verb_token: 主動詞トークン
            pattern: 依存関係パターン
            
        Returns:
            str: スロット分類
        """
        # 不定詞を支配する主動詞の特徴分析
        if pattern in ['xcomp_aux', 'ccomp_aux']:
            return 'inf-governing-verb'
        elif pattern == 'advcl_mark':
            return 'main-verb'
        
        return 'verb'
    
    def _analyze_infinitive_arguments(self, verb_token, slots: Dict[str, str]):
        """
        不定詞の引数構造分析
        
        Args:
            verb_token: 不定詞動詞トークン
            slots: スロット辞書（更新される）
        """
        print(f"   � 不定詞'{verb_token.text}'の引数構造解析")
        
        for child in verb_token.children:
            if child.dep_ == 'dobj':  # 直接目的語
                slots[child.text] = 'inf-object'
                print(f"     📦 '{child.text}' → inf-object")
            elif child.dep_ == 'nsubj':  # 主語
                slots[child.text] = 'inf-subject'
                print(f"     👤 '{child.text}' → inf-subject")
            elif child.dep_ == 'prep':  # 前置詞句
                slots[child.text] = 'inf-prep'
                print(f"     🔗 '{child.text}' → inf-prep")
                # 前置詞の目的語も分析
                for grandchild in child.children:
                    if grandchild.dep_ == 'pobj':
                        slots[grandchild.text] = 'inf-prep-object'
                        print(f"     📍 '{grandchild.text}' → inf-prep-object")
    
    def _process_nominal_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """名詞的用法の処理（spaCy依存関係ベース）"""
        print(f"📝 名詞的不定詞処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # 不定詞を主語として処理
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']
            
            main_slots['S'] = f"{to_token.text} {main_verb.text}"
            
            # 文の主動詞を検出
            for token in doc:
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    main_slots['V'] = token.text
                    break
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_nominal',
                'usage_type': 'nominal',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_adjectival_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """形容詞的用法の処理（spaCy依存関係ベース）"""
        print(f"📝 形容詞的不定詞処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # 修飾される名詞と不定詞の関係を分析
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']
            head = inf_token['head']
            
            # 主文の構造を抽出
            for token in doc:
                if token.dep_ == 'nsubj':
                    main_slots['S'] = token.text
                elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    main_slots['V'] = token.text
                elif token.dep_ == 'dobj':
                    main_slots['O1'] = token.text
            
            # 不定詞を修飾語として分類
            main_slots['M2'] = f"{to_token.text} {main_verb.text}"
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_adjectival',
                'usage_type': 'adjectival',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_adverbial_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """副詞的用法の処理（spaCy依存関係ベース）"""
        print(f"📝 副詞的不定詞処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # 主文の構造を抽出
        for token in doc:
            if token.dep_ == 'nsubj':
                main_slots['S'] = token.text
            elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                main_slots['V'] = token.text
            elif token.dep_ == 'dobj':
                main_slots['O1'] = token.text
        
        # 不定詞を副詞的修飾語として分類
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']
            
            main_slots['M2'] = f"{to_token.text} {main_verb.text}"
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_adverbial',
                'usage_type': 'adverbial',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_basic_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """基本的な不定詞処理（spaCy依存関係ベース）"""
        print(f"📝 基本不定詞処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # 基本的な文構造抽出
        for token in doc:
            if token.dep_ == 'nsubj':
                main_slots['S'] = token.text
            elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                main_slots['V'] = token.text
        
        # 不定詞を目的語として分類
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']
            
            main_slots['O1'] = f"{to_token.text} {main_verb.text}"
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_basic',
                'usage_type': 'basic',
                'confidence': 0.8,
                'spacy_analysis': True
            }
        }
