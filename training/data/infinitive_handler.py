#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InfinitiveHandler: 不定詞処理ハンドラー
to不定詞の名詞的・形容詞的・副詞的用法の専門分解
専門分担型ハイブリッド解析（品詞分析 + 依存関係）+ 人間的            # パターン1: xcomp (complement) + aux=to
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
                        
                        # too...to構文の特別判定
                        if self._is_too_to_pattern(doc, token):
                            infinitive_info['infinitive_tokens'][-1]['pattern'] = 'too_to_pattern'
                            print(f"   🎯 too...to構文検出: '{child.text} {token.text}'")
                        # enough...to構文の特別判定  
                        elif self._is_enough_to_pattern(doc, token):
                            infinitive_info['infinitive_tokens'][-1]['pattern'] = 'enough_to_pattern'
                            print(f"   🎯 enough...to構文検出: '{child.text} {token.text}'")
                        else:
                            print(f"   📝 通常のxcomp処理: '{child.text} {token.text}'")ング極力排除・汎用的システム設計
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
            
            # spaCy依存関係解析による不定詞検出（複数パターン対応）
            for token in doc:
                # パターン1: to + VERB の直接的な子関係
                if (token.text.lower() == 'to' and 
                    token.pos_ == 'PART' and  # to は PART (particle) として分類
                    any(child.pos_ == 'VERB' for child in token.children)):
                    return True
                
                # パターン2: VERB (advcl/xcomp) + to (aux) の関係（case159対応）
                if (token.pos_ == 'VERB' and 
                    token.dep_ in ['advcl', 'xcomp'] and
                    any(child.text.lower() == 'to' and child.dep_ == 'aux' 
                        for child in token.children)):
                    return True
                
                # パターン3: xcomp (open clausal complement) での不定詞検出
                if token.dep_ == 'xcomp' and token.pos_ == 'VERB':
                    # xcompの前にtoがあるかチェック
                    for child in token.children:
                        if child.text.lower() == 'to' and child.dep_ == 'aux':
                            return True
                
                # パターン4: csubj (clausal subject) での不定詞検出 - 名詞的用法
                if (token.pos_ == 'VERB' and 
                    token.dep_ == 'csubj' and
                    any(child.text.lower() == 'to' and child.dep_ == 'aux' 
                        for child in token.children)):
                    return True
                
                # パターン5: relcl (relative clause) での不定詞検出 - 形容詞的用法
                if (token.pos_ == 'VERB' and 
                    token.dep_ == 'relcl' and
                    any(child.text.lower() == 'to' and child.dep_ == 'aux' 
                        for child in token.children)):
                    return True
            
            # 高度なパターン検出（case164-170対応）
            text_lower = text.lower()
            
            # 完了不定詞: to have + 過去分詞
            if 'to have' in text_lower and any(token.tag_ in ['VBN'] for token in doc):
                return True
            
            # 受動不定詞: to be + 過去分詞
            if 'to be' in text_lower and any(token.tag_ in ['VBN'] for token in doc):
                return True
            
            # 疑問詞+不定詞: what/how/when/where to do
            if any(token.text.lower() in ['what', 'how', 'when', 'where', 'which', 'who'] and 
                   token.pos_ in ['PRON', 'ADV'] for token in doc) and 'to ' in text_lower:
                return True
            
            # 使役構文: want + 人 + to do
            for token in doc:
                if (token.lemma_.lower() in ['want', 'ask', 'tell', 'expect', 'allow', 'cause'] and
                    'to ' in text_lower):
                    return True
            
            # be about to構文
            if 'about to' in text_lower:
                return True
            
            # in order to構文
            if 'in order to' in text_lower:
                return True
            
            # so as to構文
            if 'so as to' in text_lower:
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
        
        # 高度なパターン検出（case164-170対応）
        text_lower = text.lower()
        
        # 完了不定詞パターン検出: to have + 過去分詞
        if 'to have' in text_lower:
            for i, token in enumerate(doc):
                if (token.text.lower() == 'to' and i + 1 < len(doc) and 
                    doc[i + 1].text.lower() == 'have'):
                    # 過去分詞を探す
                    for j in range(i + 2, len(doc)):
                        if doc[j].tag_ == 'VBN':  # 過去分詞
                            infinitive_info['found'] = True
                            infinitive_info['infinitive_tokens'].append({
                                'main_verb': doc[i + 1],  # have
                                'to_token': token,
                                'pattern': 'perfect_infinitive',
                                'head': doc[i + 1].head,
                                'dependency': 'xcomp',
                                'participle': doc[j]
                            })
                            print(f"   ✅ 完了不定詞検出: 'to have {doc[j].text}'")
                            break
                    break
        
        # 受動不定詞パターン検出: to be + 過去分詞
        if 'to be' in text_lower:
            for i, token in enumerate(doc):
                if (token.text.lower() == 'to' and i + 1 < len(doc) and 
                    doc[i + 1].text.lower() == 'be'):
                    # 過去分詞を探す
                    for j in range(i + 2, len(doc)):
                        if doc[j].tag_ == 'VBN':  # 過去分詞
                            infinitive_info['found'] = True
                            infinitive_info['infinitive_tokens'].append({
                                'main_verb': doc[i + 1],  # be
                                'to_token': token,
                                'pattern': 'passive_infinitive',
                                'head': doc[i + 1].head,
                                'dependency': 'xcomp',
                                'participle': doc[j]
                            })
                            print(f"   ✅ 受動不定詞検出: 'to be {doc[j].text}'")
                            break
                    break
        
        # 疑問詞+不定詞パターン検出
        wh_words = ['what', 'how', 'when', 'where', 'which', 'who']
        for token in doc:
            if (token.text.lower() in wh_words and 
                token.pos_ in ['PRON', 'ADV']):
                # その後にto+動詞があるかチェック
                for next_token in doc[token.i + 1:]:
                    if (next_token.text.lower() == 'to' and 
                        next_token.dep_ == 'aux'):
                        for verb_token in next_token.children:
                            if verb_token.pos_ == 'VERB':
                                infinitive_info['found'] = True
                                infinitive_info['infinitive_tokens'].append({
                                    'main_verb': verb_token,
                                    'to_token': next_token,
                                    'pattern': 'wh_infinitive',
                                    'head': verb_token.head,
                                    'dependency': 'xcomp',
                                    'wh_word': token
                                })
                                print(f"   ✅ 疑問詞+不定詞検出: '{token.text} to {verb_token.text}'")
                                break
                        break
                break
        
        # 使役構文パターン検出
        causative_verbs = ['want', 'ask', 'tell', 'expect', 'allow', 'cause']
        for token in doc:
            if (token.lemma_.lower() in causative_verbs and 
                token.pos_ == 'VERB'):
                # "I want you to help me" パターン
                object_person = None
                infinitive_verb = None
                to_token = None
                
                # ccomp構文での不定詞検出
                for child in token.children:
                    if child.dep_ == 'ccomp' and child.pos_ == 'VERB':
                        infinitive_verb = child
                        # toトークンを探す
                        for inf_child in child.children:
                            if inf_child.text.lower() == 'to' and inf_child.dep_ == 'aux':
                                to_token = inf_child
                                break
                        
                        # 不定詞の主語（causativeの目的語）を探す
                        for inf_child in child.children:
                            if inf_child.dep_ == 'nsubj':
                                object_person = inf_child
                                break
                        
                        break
                
                if infinitive_verb and object_person:
                    infinitive_info['found'] = True
                    infinitive_info['infinitive_tokens'].append({
                        'main_verb': infinitive_verb,
                        'to_token': to_token,
                        'pattern': 'causative',
                        'head': token,
                        'dependency': 'ccomp',
                        'causative_verb': token,
                        'object': object_person
                    })
                    print(f"   ✅ 使役構文検出: '{token.text} {object_person.text} to {infinitive_verb.text}'")
        
        # be about to構文検出
        if 'about to' in text_lower:
            for i, token in enumerate(doc):
                if (token.text.lower() == 'about' and 
                    i + 1 < len(doc) and doc[i + 1].text.lower() == 'to'):
                    # その後の動詞を探す
                    for j in range(i + 2, len(doc)):
                        if doc[j].pos_ == 'VERB':
                            infinitive_info['found'] = True
                            infinitive_info['infinitive_tokens'].append({
                                'main_verb': doc[j],
                                'to_token': doc[i + 1],
                                'pattern': 'be_about_to',
                                'head': token.head,
                                'dependency': 'xcomp',
                                'about_token': token
                            })
                            print(f"   ✅ be about to構文検出: 'about to {doc[j].text}'")
                            break
                    break
        
        # in order to構文検出
        if 'in order to' in text_lower:
            for i, token in enumerate(doc):
                if (token.text.lower() == 'in' and 
                    i + 2 < len(doc) and 
                    doc[i + 1].text.lower() == 'order' and 
                    doc[i + 2].text.lower() == 'to'):
                    # その後の動詞を探す
                    for j in range(i + 3, len(doc)):
                        if doc[j].pos_ == 'VERB':
                            infinitive_info['found'] = True
                            infinitive_info['infinitive_tokens'].append({
                                'main_verb': doc[j],
                                'to_token': doc[i + 2],
                                'pattern': 'in_order_to',
                                'head': doc[j].head,
                                'dependency': 'acl'
                            })
                            print(f"   ✅ in order to構文検出: 'in order to {doc[j].text}'")
                            break
                    break
        
        # so as to構文検出
        if 'so as to' in text_lower:
            for i, token in enumerate(doc):
                if (token.text.lower() == 'so' and 
                    i + 2 < len(doc) and 
                    doc[i + 1].text.lower() == 'as' and 
                    doc[i + 2].text.lower() == 'to'):
                    # その後の動詞を探す
                    for j in range(i + 3, len(doc)):
                        if doc[j].pos_ == 'VERB':
                            infinitive_info['found'] = True
                            infinitive_info['infinitive_tokens'].append({
                                'main_verb': doc[j],
                                'to_token': doc[i + 2],
                                'pattern': 'so_as_to',
                                'head': doc[j].head,
                                'dependency': 'advcl'
                            })
                            print(f"   ✅ so as to構文検出: 'so as to {doc[j].text}'")
                            break
                    break
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
                        
                        # too...to構文の特別判定
                        if self._is_too_to_pattern(doc, token):
                            infinitive_info['infinitive_tokens'][-1]['pattern'] = 'too_to_pattern'
                            print(f"   🎯 too...to構文検出: '{child.text} {token.text}'")
                        # enough...to構文の特別判定  
                        elif self._is_enough_to_pattern(doc, token):
                            infinitive_info['infinitive_tokens'][-1]['pattern'] = 'enough_to_pattern'
                            print(f"   🎯 enough...to構文検出: '{child.text} {token.text}'")
                        else:
                            print(f"   📝 通常のxcomp処理: '{child.text} {token.text}'")
            
            # パターン2: advcl (adverbial clause) + aux/mark=to  
            elif token.dep_ == 'advcl' and token.pos_ == 'VERB':
                for child in token.children:
                    if child.text.lower() == 'to' and child.dep_ in ['mark', 'aux']:
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
            
            # パターン4: csubj (clausal subject) + aux=to - 名詞的用法・主語
            elif token.dep_ == 'csubj' and token.pos_ == 'VERB':
                for child in token.children:
                    if child.text.lower() == 'to' and child.dep_ == 'aux':
                        infinitive_info['found'] = True
                        infinitive_info['infinitive_tokens'].append({
                            'main_verb': token,
                            'to_token': child,
                            'pattern': 'csubj_aux',
                            'head': token.head,
                            'dependency': token.dep_
                        })
                        print(f"   ✅ csubj不定詞検出: '{child.text} {token.text}' (head: {token.head.text})")
            
            # パターン5: relcl (relative clause) + aux=to - 形容詞的用法
            elif token.dep_ == 'relcl' and token.pos_ == 'VERB':
                for child in token.children:
                    if child.text.lower() == 'to' and child.dep_ == 'aux':
                        infinitive_info['found'] = True
                        infinitive_info['infinitive_tokens'].append({
                            'main_verb': token,
                            'to_token': child,
                            'pattern': 'relcl_aux',
                            'head': token.head,
                            'dependency': token.dep_
                        })
                        print(f"   ✅ relcl不定詞検出: '{child.text} {token.text}' (head: {token.head.text})")
        
        # 高度なパターン検出（case164-170）
        text_lower = text.lower()
        
        # 完了不定詞検出: to have + 過去分詞
        if not infinitive_info['found'] and 'to have' in text_lower:
            for token in doc:
                if (token.text.lower() == 'have' and 
                    any(child.text.lower() == 'to' and child.dep_ == 'aux' for child in token.children) and
                    any(child.tag_ == 'VBN' for child in token.children)):
                    infinitive_info['found'] = True
                    infinitive_info['infinitive_tokens'].append({
                        'main_verb': token,
                        'to_token': next((child for child in token.children if child.text.lower() == 'to'), None),
                        'pattern': 'perfect_infinitive',
                        'head': token.head,
                        'dependency': token.dep_
                    })
                    print(f"   ✅ 完了不定詞検出: 'to have + 過去分詞' (head: {token.head.text})")
        
        # 受動不定詞検出: to be + 過去分詞
        if not infinitive_info['found'] and 'to be' in text_lower:
            for token in doc:
                if (token.lemma_ == 'be' and 
                    any(child.text.lower() == 'to' and child.dep_ == 'aux' for child in token.children) and
                    any(child.tag_ == 'VBN' for child in token.children)):
                    infinitive_info['found'] = True
                    infinitive_info['infinitive_tokens'].append({
                        'main_verb': token,
                        'to_token': next((child for child in token.children if child.text.lower() == 'to'), None),
                        'pattern': 'passive_infinitive',
                        'head': token.head,
                        'dependency': token.dep_
                    })
                    print(f"   ✅ 受動不定詞検出: 'to be + 過去分詞' (head: {token.head.text})")
        
        # 疑問詞+不定詞検出: what/how/when/where to do
        if not infinitive_info['found']:
            for token in doc:
                if (token.text.lower() in ['what', 'how', 'when', 'where', 'which', 'who'] and
                    token.pos_ in ['PRON', 'ADV']):
                    # 次のtoを探す
                    for next_token in doc[token.i+1:]:
                        if (next_token.text.lower() == 'to' and next_token.pos_ == 'PART' and
                            next_token.i < len(doc) - 1 and doc[next_token.i + 1].pos_ == 'VERB'):
                            infinitive_info['found'] = True
                            infinitive_info['infinitive_tokens'].append({
                                'main_verb': doc[next_token.i + 1],
                                'to_token': next_token,
                                'pattern': 'wh_infinitive',
                                'wh_word': token,
                                'head': token.head,
                                'dependency': token.dep_
                            })
                            print(f"   ✅ 疑問詞+不定詞検出: '{token.text} to {doc[next_token.i + 1].text}'")
                            break
        
        # be about to構文検出
        if not infinitive_info['found'] and 'about to' in text_lower:
            for token in doc:
                if (token.text.lower() == 'about' and token.i < len(doc) - 2 and
                    doc[token.i + 1].text.lower() == 'to' and doc[token.i + 2].pos_ == 'VERB'):
                    infinitive_info['found'] = True
                    infinitive_info['infinitive_tokens'].append({
                        'main_verb': doc[token.i + 2],
                        'to_token': doc[token.i + 1],
                        'pattern': 'be_about_to',
                        'about_token': token,
                        'head': token.head,
                        'dependency': token.dep_
                    })
                    print(f"   ✅ be about to構文検出: 'about to {doc[token.i + 2].text}'")
        
        # in order to構文検出
        if not infinitive_info['found'] and 'in order to' in text_lower:
            for token in doc:
                if (token.text.lower() == 'order' and token.i < len(doc) - 2 and
                    doc[token.i + 1].text.lower() == 'to' and doc[token.i + 2].pos_ == 'VERB'):
                    infinitive_info['found'] = True
                    infinitive_info['infinitive_tokens'].append({
                        'main_verb': doc[token.i + 2],
                        'to_token': doc[token.i + 1],
                        'pattern': 'in_order_to',
                        'order_token': token,
                        'head': token.head,
                        'dependency': token.dep_
                    })
                    print(f"   ✅ in order to構文検出: 'in order to {doc[token.i + 2].text}'")
        
        # so as to構文検出
        if not infinitive_info['found'] and 'so as to' in text_lower:
            for token in doc:
                if (token.text.lower() == 'as' and token.i < len(doc) - 2 and
                    doc[token.i + 1].text.lower() == 'to' and doc[token.i + 2].pos_ == 'VERB' and
                    token.i > 0 and doc[token.i - 1].text.lower() == 'so'):
                    infinitive_info['found'] = True
                    infinitive_info['infinitive_tokens'].append({
                        'main_verb': doc[token.i + 2],
                        'to_token': doc[token.i + 1],
                        'pattern': 'so_as_to',
                        'as_token': token,
                        'head': token.head,
                        'dependency': token.dep_
                    })
                    print(f"   ✅ so as to構文検出: 'so as to {doc[token.i + 2].text}'")
        
        # 使役構文検出: want + 人 + to do
        if not infinitive_info['found']:
            for token in doc:
                if (token.lemma_.lower() in ['want', 'ask', 'tell', 'expect', 'allow', 'cause'] and
                    token.pos_ == 'VERB'):
                    # 目的語 + to + 動詞の構造を探す
                    for child in token.children:
                        if child.dep_ == 'dobj':  # 直接目的語
                            # 次のtoを探す
                            for next_token in doc[child.i+1:]:
                                if (next_token.text.lower() == 'to' and next_token.pos_ == 'PART' and
                                    next_token.i < len(doc) - 1 and doc[next_token.i + 1].pos_ == 'VERB'):
                                    infinitive_info['found'] = True
                                    infinitive_info['infinitive_tokens'].append({
                                        'main_verb': doc[next_token.i + 1],
                                        'to_token': next_token,
                                        'pattern': 'causative',
                                        'causative_verb': token,
                                        'object': child,
                                        'head': token,
                                        'dependency': 'causative'
                                    })
                                    print(f"   ✅ 使役構文検出: '{token.text} {child.text} to {doc[next_token.i + 1].text}'")
                                    break
        
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
            
            # 特別パターンの処理
            if pattern == 'too_to_pattern':
                print(f"   📝 too...to構文 → 結果の副詞的用法")
                return 'too_to_adverbial'
            elif pattern == 'enough_to_pattern':
                print(f"   📝 enough...to構文 → 結果の副詞的用法")
                return 'enough_to_adverbial'
            
            # 高度なパターンの処理（case164-170）
            elif pattern == 'perfect_infinitive':
                print(f"   📝 完了不定詞 → 助動詞形式")
                return 'perfect_infinitive'
            elif pattern == 'passive_infinitive':
                print(f"   📝 受動不定詞 → 名詞的用法（目的語）")
                return 'passive_infinitive'
            elif pattern == 'wh_infinitive':
                print(f"   📝 疑問詞+不定詞 → 名詞的用法（目的語）")
                return 'wh_infinitive'
            elif pattern == 'causative':
                print(f"   📝 使役構文 → 目的語補語")
                return 'causative'
            elif pattern == 'be_about_to':
                print(f"   📝 be about to構文 → 助動詞形式")
                return 'be_about_to'
            elif pattern == 'in_order_to':
                print(f"   📝 in order to構文 → 目的の副詞的用法")
                return 'in_order_to'
            elif pattern == 'so_as_to':
                print(f"   📝 so as to構文 → 目的の副詞的用法")
                return 'so_as_to'
            
            # xcomp: 通常は目的語補語（形容詞的・副詞的用法）
            elif pattern == 'xcomp_aux':
                if head.pos_ == 'VERB':
                    # want to do 形式は名詞的用法（目的語）
                    if head.lemma_.lower() in ['want', 'need', 'like', 'love', 'hate', 'prefer', 'decide', 'hope', 'plan', 'try', 'attempt']:
                        print(f"   📝 xcomp + 欲求・意思動詞 → 名詞的用法（目的語）")
                        return 'nominal_object'
                    else:
                        print(f"   📝 xcomp + 動詞head → 目的語補語（形容詞的用法候補）")
                        return 'adjectival_complement'
                    
            # advcl: 副詞節（副詞的用法）
            # advcl: for構文の場合は形式主語構文、それ以外は副詞的用法
            elif pattern == 'advcl_mark':
                # "It is easy for me to understand" 構文をチェック
                tokens = [token.text.lower() for token in doc]
                print(f"   📝 advcl検証: tokens={tokens}")
                print(f"   📝 advcl検証: head={head.text}, head.lemma={head.lemma_}")
                
                # It is ... for ... to ...構文の判定
                has_it = 'it' in tokens
                has_be = head.lemma_.lower() in ['be', 'is', 'are', 'was', 'were']
                has_for = 'for' in tokens
                has_to = 'to' in tokens
                
                print(f"   📝 formal_subject判定: it={has_it}, be={has_be}, for={has_for}, to={has_to}")
                
                if has_it and has_be and has_for and has_to:
                    print(f"   📝 advcl + for構文 → 形式主語構文")
                    return 'formal_subject'
                else:
                    print(f"   📝 advcl + mark → 副詞節（副詞的用法）")
                    return 'adverbial_clause'
                    
            # ccomp: 補語節（名詞的用法候補）
            elif pattern == 'ccomp_aux':
                print(f"   📝 ccomp + 補語節 → 名詞的用法候補")
                return 'nominal_complement'
                
            # csubj: 節主語（名詞的用法・主語）
            elif pattern == 'csubj_aux':
                print(f"   📝 csubj + 節主語 → 名詞的用法（主語）")
                return 'nominal_subject'
                
            # relcl: 関係節・形容詞的用法
            elif pattern == 'relcl_aux':
                print(f"   📝 relcl + 関係節 → 形容詞的用法")
                return 'adjectival_modifier'
        
        return 'unknown'
    
    def _is_too_to_pattern(self, doc, infinitive_verb):
        """too...to構文の判定"""
        print(f"   🔍 too...to判定開始: infinitive_verb={infinitive_verb.text}")
        # 'too'が形容詞を修飾している構造を探す
        for token in doc:
            print(f"      🔍 token='{token.text}', dep={token.dep_}, pos={token.pos_}")
            if token.text.lower() == 'too' and token.dep_ == 'advmod':
                print(f"      ✅ too検出: head={token.head.text}, head.pos={token.head.pos_}")
                # tooが修飾している形容詞
                if token.head.pos_ == 'ADJ':
                    print(f"      ✅ too...to構文判定成功: 'too {token.head.text} to {infinitive_verb.text}'")
                    return True
        print(f"      ❌ too...to構文判定失敗")
        return False
    
    def _is_enough_to_pattern(self, doc, infinitive_verb):
        """enough...to構文の判定"""
        print(f"   🔍 enough...to判定開始: infinitive_verb={infinitive_verb.text}")
        # 'enough'が形容詞または副詞を修飾している構造を探す
        for token in doc:
            print(f"      🔍 token='{token.text}', dep={token.dep_}, pos={token.pos_}")
            if token.text.lower() == 'enough' and token.dep_ == 'advmod':
                print(f"      ✅ enough検出: head={token.head.text}, head.pos={token.head.pos_}")
                # enoughが修飾している形容詞/副詞
                if token.head.pos_ in ['ADJ', 'ADV']:
                    print(f"      ✅ enough...to構文判定成功: '{token.head.text} enough to {infinitive_verb.text}'")
                    return True
        print(f"      ❌ enough...to構文判定失敗")
        return False
    
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
        elif syntactic_role == 'nominal_subject':
            return self._process_nominal_subject_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'nominal_object':
            return self._process_nominal_object_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'adjectival_complement':
            return self._process_adjectival_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'adjectival_modifier':
            return self._process_adjectival_modifier_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'formal_subject':
            return self._process_formal_subject_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'too_to_adverbial':
            return self._process_too_to_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'enough_to_adverbial':
            return self._process_enough_to_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'adverbial_clause':
            return self._process_adverbial_infinitive(doc, text, infinitive_info, slots)
        
        # 高度なパターンの処理（case164-170）
        elif syntactic_role == 'perfect_infinitive':
            return self._process_perfect_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'passive_infinitive':
            return self._process_passive_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'wh_infinitive':
            return self._process_wh_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'causative':
            return self._process_causative_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'be_about_to':
            return self._process_be_about_to_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'in_order_to':
            return self._process_in_order_to_infinitive(doc, text, infinitive_info, slots)
        elif syntactic_role == 'so_as_to':
            return self._process_so_as_to_infinitive(doc, text, infinitive_info, slots)
        
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
    
    def _process_nominal_subject_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """名詞的用法・主語の処理（csubj構造対応）"""
        print(f"📝 名詞的不定詞・主語処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # case156: "To study English is important."
        # 期待値: main_slots={'S': '', 'V': 'is', 'C1': 'important'}
        #        sub_slots={'sub-v': 'To study', 'sub-o1': 'English', '_parent_slot': 'S'}
        
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']  # study
            head = inf_token['head']  # is
            
            # メインスロット: 文の主動詞（is）とその補語
            main_slots['S'] = ''  # 主語は空（不定詞がサブスロットとして処理）
            main_slots['V'] = head.text  # is
            
            # 補語（C1）を検出
            for child in head.children:
                if child.dep_ in ['acomp', 'attr'] and child.pos_ == 'ADJ':
                    main_slots['C1'] = child.text
                    print(f"   📍 補語検出: C1 = '{child.text}'")
            
            # サブスロット: 不定詞部分
            sub_slots['sub-v'] = f"{to_token.text} {main_verb.text}"  # "To study"
            sub_slots['_parent_slot'] = 'S'
            
            # 不定詞の目的語を検出
            for child in main_verb.children:
                if child.dep_ == 'dobj' and child.pos_ in ['NOUN', 'PROPN']:
                    sub_slots['sub-o1'] = child.text
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{child.text}'")
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_nominal_subject',
                'usage_type': 'nominal_subject',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_nominal_object_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """名詞的用法・目的語の処理（xcomp構造対応）"""
        print(f"📝 名詞的不定詞・目的語処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # case157: "I want to learn programming."
        # 期待値: main_slots={'S': 'I', 'V': 'want', 'O1': ''}
        #        sub_slots={'sub-v': 'to learn', 'sub-o1': 'programming', '_parent_slot': 'O1'}
        
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']  # learn
            head = inf_token['head']  # want
            
            # メインスロット: 主動詞（want）とその主語
            for token in doc:
                if token.dep_ == 'nsubj' and token.head == head:
                    main_slots['S'] = token.text
                    print(f"   📍 主語検出: S = '{token.text}'")
            
            main_slots['V'] = head.text  # want
            main_slots['O1'] = ''  # 目的語は空（不定詞がサブスロットとして処理）
            
            # サブスロット: 不定詞部分
            sub_slots['sub-v'] = f"{to_token.text} {main_verb.text}"  # "to learn"
            sub_slots['_parent_slot'] = 'O1'
            
            # 不定詞の目的語を検出
            for child in main_verb.children:
                if child.dep_ == 'dobj' and child.pos_ in ['NOUN', 'PROPN']:
                    sub_slots['sub-o1'] = child.text
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{child.text}'")
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_nominal_object',
                'usage_type': 'nominal_object',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_adjectival_modifier_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """形容詞的用法・修飾語の処理（relcl構造対応）"""
        print(f"📝 形容詞的不定詞・修飾語処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # case158: "She has something to tell you."
        # 期待値: main_slots={'S': 'She', 'V': 'has', 'O1': ''}
        #        sub_slots={'sub-v': 'something to tell', 'sub-o1': 'you', '_parent_slot': 'O1'}
        
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']  # tell
            head = inf_token['head']  # something
            
            # メインスロット: 主動詞とその主語・目的語
            for token in doc:
                if token.dep_ == 'ROOT':
                    main_slots['V'] = token.text  # has
                    # 主語を探す
                    for child in token.children:
                        if child.dep_ == 'nsubj':
                            main_slots['S'] = child.text
                            print(f"   📍 主語検出: S = '{child.text}'")
                        # 目的語を探す（head=somethingの親）
                        elif child.dep_ == 'dobj' and child == head:
                            main_slots['O1'] = ''  # 目的語は不定詞でサブスロット化
                            print(f"   📍 目的語検出（不定詞修飾対象）: '{child.text}' → O1空欄")
            
            # サブスロット: 不定詞部分
            sub_slots['sub-v'] = f"{head.text} {to_token.text} {main_verb.text}"  # "something to tell"
            sub_slots['_parent_slot'] = 'O1'
            
            # 不定詞の目的語を検出
            for child in main_verb.children:
                if child.dep_ == 'dobj':
                    sub_slots['sub-o1'] = child.text
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{child.text}'")
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_adjectival_modifier',
                'usage_type': 'adjectival_modifier',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_formal_subject_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """形式主語構文の処理（It is ... for 人 to ...）"""
        print(f"📝 形式主語不定詞処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # case161: "It is easy for me to understand this."
        # 期待値: main_slots={'S': 'It', 'V': 'is', 'C1': 'easy', 'M2': 'for me', 'M3': ''}
        #        sub_slots={'sub-v': 'to understand', 'sub-o1': 'this', '_parent_slot': 'M3'}
        
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']  # understand
            
            # メインスロット構造を構築
            main_slots['S'] = 'It'  # 形式主語
            
            # be動詞と補語を探す
            for token in doc:
                if token.dep_ == 'ROOT' and token.lemma_.lower() == 'be':
                    main_slots['V'] = token.text  # is
                    # 補語（形容詞）を探す
                    for child in token.children:
                        if child.dep_ == 'acomp':
                            main_slots['C1'] = child.text  # easy
                            print(f"   📍 補語検出: C1 = '{child.text}'")
            
            # for句を探す
            for token in doc:
                if token.text.lower() == 'for' and token.dep_ == 'mark':
                    # for句の対象を探す
                    for child in token.children:
                        if child.dep_ == 'nsubj':
                            main_slots['M2'] = f"for {child.text}"
                            print(f"   📍 for句検出: M2 = 'for {child.text}'")
                    # または親の兄弟から探す
                    if 'M2' not in main_slots:
                        parent = token.head
                        for sibling in parent.children:
                            if sibling.dep_ == 'nsubj' and sibling != token:
                                main_slots['M2'] = f"for {sibling.text}"
                                print(f"   📍 for句検出: M2 = 'for {sibling.text}'")
                                break
            
            # M2が見つからない場合、別の方法で探す
            if 'M2' not in main_slots:
                for token in doc:
                    if token.text.lower() == 'me' and token.dep_ == 'nsubj':
                        main_slots['M2'] = 'for me'
                        print(f"   📍 for句検出（代替）: M2 = 'for me'")
                        break
            
            main_slots['M3'] = ''  # 不定詞部分は空でサブスロット化
            
            # サブスロット: 不定詞部分
            sub_slots['sub-v'] = f"{to_token.text} {main_verb.text}"  # "to understand"
            sub_slots['_parent_slot'] = 'M3'
            
            # 不定詞の目的語を検出
            for child in main_verb.children:
                if child.dep_ == 'dobj':
                    sub_slots['sub-o1'] = child.text
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{child.text}'")
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_formal_subject',
                'usage_type': 'formal_subject',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_too_to_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """too...to構文の処理"""
        print(f"📝 too...to構文処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # case162: "This box is too heavy to carry."
        # 期待値: main_slots={'S': 'This box', 'V': 'is', 'C1': 'too heavy', 'M2': ''}
        #        sub_slots={'sub-v': 'to carry', '_parent_slot': 'M2'}
        
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']  # carry
            
            # メイン構造を解析
            for token in doc:
                if token.dep_ == 'nsubj':
                    # 主語: 限定詞 + 名詞
                    if token.i > 0 and doc[token.i-1].pos_ == 'DET':
                        main_slots['S'] = f"{doc[token.i-1].text} {token.text}"
                    else:
                        main_slots['S'] = token.text
                elif token.dep_ == 'ROOT' and token.pos_ in ['AUX', 'VERB']:
                    main_slots['V'] = token.text  # is
                    
                    # 補語: too + 形容詞
                    for child in token.children:
                        if child.dep_ == 'acomp' and child.pos_ == 'ADJ':
                            # tooが修飾している形容詞
                            for grandchild in child.children:
                                if grandchild.text.lower() == 'too' and grandchild.dep_ == 'advmod':
                                    main_slots['C1'] = f"too {child.text}"
                                    print(f"   📍 too+形容詞検出: C1 = 'too {child.text}'")
                                    break
                            if 'C1' not in main_slots:
                                main_slots['C1'] = child.text
            
            main_slots['M2'] = ''  # 不定詞部分は空でサブスロット化
            
            # サブスロット: 不定詞部分
            sub_slots['sub-v'] = f"{to_token.text} {main_verb.text}"  # "to carry"
            sub_slots['_parent_slot'] = 'M2'
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_too_to',
                'usage_type': 'too_to_adverbial',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_enough_to_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """enough...to構文の処理"""
        print(f"📝 enough...to構文処理: {text}")
        
        main_slots = {}
        sub_slots = {}
        
        # case163: "She is old enough to drive a car."
        # 期待値: main_slots={'S': 'She', 'V': 'is', 'C1': 'old', 'M2': ''}
        #        sub_slots={'sub-v': 'enough to drive', 'sub-o1': 'a car', '_parent_slot': 'M2'}
        
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']  # drive
            
            # メイン構造を解析
            for token in doc:
                if token.dep_ == 'nsubj':
                    main_slots['S'] = token.text  # She
                elif token.dep_ == 'ROOT' and token.pos_ in ['AUX', 'VERB']:
                    main_slots['V'] = token.text  # is
                    
                    # 補語: 形容詞（enoughが修飾している）
                    for child in token.children:
                        if child.dep_ == 'acomp' and child.pos_ == 'ADJ':
                            # enoughが修飾している形容詞
                            for grandchild in child.children:
                                if grandchild.text.lower() == 'enough' and grandchild.dep_ == 'advmod':
                                    main_slots['C1'] = child.text  # old (enoughは除く)
                                    print(f"   📍 enough+形容詞検出: C1 = '{child.text}'")
                                    break
                            if 'C1' not in main_slots:
                                main_slots['C1'] = child.text
            
            main_slots['M2'] = ''  # 不定詞部分は空でサブスロット化
            
            # サブスロット: enough + 不定詞部分
            sub_slots['sub-v'] = f"enough {to_token.text} {main_verb.text}"  # "enough to drive"
            sub_slots['_parent_slot'] = 'M2'
            
            # 不定詞の目的語を検出
            for child in main_verb.children:
                if child.dep_ == 'dobj':
                    # 限定詞 + 名詞
                    if child.i > 0 and doc[child.i-1].pos_ == 'DET':
                        sub_slots['sub-o1'] = f"{doc[child.i-1].text} {child.text}"
                    else:
                        sub_slots['sub-o1'] = child.text
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{sub_slots['sub-o1']}'")
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_enough_to',
                'usage_type': 'enough_to_adverbial',
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
            elif token.dep_ == 'dobj' and token.head.dep_ == 'ROOT':
                # メイン動詞の直接目的語のみ
                main_slots['O1'] = token.text
        
        # 副詞的不定詞の詳細分析と出力形式決定
        if infinitive_info['infinitive_tokens']:
            inf_token = infinitive_info['infinitive_tokens'][0]
            to_token = inf_token['to_token']
            main_verb = inf_token['main_verb']
            
            # 不定詞の意味的分類（目的 vs 結果 vs その他）
            infinitive_purpose = self._is_purpose_infinitive(doc, inf_token)
            infinitive_result = self._is_result_infinitive(doc, inf_token)
            
            if infinitive_purpose:
                # 目的の副詞的不定詞：サブスロット構造で出力
                print(f"🎯 目的の副詞的不定詞：サブスロット構造で処理")
                main_slots['M3'] = ""  # 空文字列
                
                # 不定詞部分をサブスロットに分解
                sub_slots['sub-v'] = f"{to_token.text} {main_verb.text}"
                sub_slots['_parent_slot'] = "M3"
                
                # 不定詞の目的語を検出
                for token in doc:
                    if (token.head == main_verb and 
                        token.dep_ == 'dobj'):
                        # "his friend" のように所有格+名詞を結合
                        obj_text = self._get_full_noun_phrase(token)
                        sub_slots['sub-o1'] = obj_text
                        break
                        
            elif infinitive_result:
                # 結果の副詞的不定詞：Aux+V形式で出力（例：grew up to become）
                print(f"🎯 結果の副詞的不定詞：Aux+V形式で処理")
                
                # メイン動詞に付属する要素を含めてAux構築
                main_verb_head = inf_token['head']
                
                # "grew up" のような句動詞＋to不定詞を一つのAuxとして扱う
                aux_parts = [main_verb_head.text]
                
                # 句動詞の副詞的小詞（prt）を検索
                for child in main_verb_head.children:
                    if child.dep_ == 'prt':  # particle（up, down, etc.）
                        aux_parts.append(child.text)
                
                # to不定詞部分を追加
                aux_parts.extend([to_token.text])
                
                main_slots['Aux'] = ' '.join(aux_parts)
                main_slots['V'] = main_verb.text
                
                # 不定詞の補語を検出（become a teacherのa teacher）
                for token in doc:
                    if (token.head == main_verb and 
                        token.dep_ in ['attr', 'dobj']):
                        # "a teacher" のような名詞句を結合
                        comp_text = self._get_full_noun_phrase(token)
                        main_slots['C1'] = comp_text
                        break
            else:
                # 結果・方法等の副詞的不定詞：メインスロット構造
                print(f"🎯 結果/方法の副詞的不定詞：メインスロット構造で処理")
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
    
    def _is_purpose_infinitive(self, doc, inf_token: Dict) -> bool:
        """
        不定詞が目的の副詞的用法かどうかを判定
        
        Args:
            doc: spaCy解析結果
            inf_token: 不定詞トークン情報
            
        Returns:
            bool: 目的の副詞的用法の場合True
        """
        # 基本的に "came to see" のような移動動詞＋to不定詞は目的用法
        main_verb_lemma = inf_token['head'].lemma_.lower()
        
        # 移動・到着を表す動詞 + to不定詞 = 目的用法
        purpose_verbs = ['come', 'go', 'run', 'walk', 'drive', 'travel', 'move', 'rush', 'hurry']
        
        if main_verb_lemma in purpose_verbs:
            return True
            
        # その他の判定条件（将来拡張可能）
        return False
    
    def _is_result_infinitive(self, doc, inf_token: Dict) -> bool:
        """
        不定詞が結果の副詞的用法かどうかを判定
        
        Args:
            doc: spaCy解析結果
            inf_token: 不定詞トークン情報
            
        Returns:
            bool: 結果の副詞的用法の場合True
        """
        # "grew up to become" のような成長・変化動詞 + to不定詞 = 結果用法
        main_verb_lemma = inf_token['head'].lemma_.lower()
        
        # 成長・変化を表す動詞 + to不定詞 = 結果用法
        result_verbs = ['grow', 'rise', 'wake', 'turn', 'come', 'live', 'get']
        
        if main_verb_lemma in result_verbs:
            # 句動詞（grow up, wake up等）の場合も結果用法
            for child in inf_token['head'].children:
                if child.dep_ == 'prt':  # particle
                    return True
            return True
            
        return False
    
    def _get_full_noun_phrase(self, token) -> str:
        """
        名詞句全体を取得（所有格等を含む）
        
        Args:
            token: 中心となる名詞トークン
            
        Returns:
            str: 完全な名詞句
        """
        # 所有格や形容詞等の修飾語を含む名詞句を構築
        phrase_tokens = []
        
        # 前置修飾語を収集
        for child in token.children:
            if child.dep_ in ['poss', 'det', 'amod', 'compound']:
                phrase_tokens.append((child.i, child.text))
        
        # 中心語を追加
        phrase_tokens.append((token.i, token.text))
        
        # 位置順でソートして結合
        phrase_tokens.sort(key=lambda x: x[0])
        return ' '.join([t[1] for t in phrase_tokens])

    # ========== 高度な不定詞構文処理メソッド（case164-170） ==========
    
    def _process_perfect_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        完了不定詞の処理（case164: He seems to have finished his work）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 完了不定詞処理: {text}")
        
        # 文構造を特定: He seems to have finished his work
        main_subject = None      # He
        governing_verb = None    # seems  
        perfect_verb = None      # finished
        object_part = None       # his work
        
        # spaCy解析で各要素を検出
        for token in doc:
            if token.dep_ == 'nsubj' and token.head.pos_ == 'VERB':
                main_subject = token.text
            elif token.lemma_ in ['seem', 'appear', 'happen'] and token.pos_ == 'VERB':
                governing_verb = token.text
            elif token.dep_ == 'xcomp' and token.pos_ == 'VERB':
                perfect_verb = token.text
                # 完了不定詞の目的語を検出
                for child in token.children:
                    if child.dep_ == 'dobj':
                        # 所有格も含めて目的語を構築
                        obj_parts = []
                        for obj_child in child.children:
                            if obj_child.dep_ == 'poss':
                                obj_parts.append(obj_child.text)
                        obj_parts.append(child.text)
                        object_part = ' '.join(obj_parts)
        
        print(f"   📍 主語検出: S = '{main_subject}'")
        print(f"   📍 完了助動詞統合: Aux = '{governing_verb} to have'")
        print(f"   📍 過去分詞検出: V = '{perfect_verb}'")
        if object_part:
            print(f"   📍 目的語検出: O1 = '{object_part}'")
        
        # 期待される形式で結果を構築
        main_slots = {
            'S': main_subject or '',
            'Aux': f"{governing_verb} to have" if governing_verb else "to have",
            'V': perfect_verb or '',
            'O1': object_part or ''
        }
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': {},
            'collaboration': ['infinitive'],
            'primary_handler': 'infinitive',
            'metadata': {
                'handler': 'infinitive_perfect',
                'usage_type': 'perfect_infinitive',
                'confidence': 0.9,
                'spacy_analysis': True
            }
        }
    
    def _process_passive_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        受動不定詞の処理（case165: This problem needs to be solved quickly）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 受動不定詞処理: {text}")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            if inf_token['pattern'] == 'passive_infinitive':
                be_verb = inf_token['main_verb']  # be
                
                # 真の主動詞を探す: beの支配語の支配語をチェック
                governing_verb = be_verb.head
                if governing_verb.dep_ == 'xcomp':
                    # xcompの場合は、その支配語が真の主動詞
                    main_verb = governing_verb.head
                else:
                    main_verb = governing_verb
                
                print(f"   🔍 be動詞: {be_verb.text}")
                print(f"   🔍 be動詞の支配語: {governing_verb.text} (dep: {governing_verb.dep_})")
                print(f"   🔍 DEBUG: governing_verb tag = {governing_verb.tag_}")
                print(f"   🔍 真の主動詞候補: {main_verb.text}")
                
                # 過去分詞と修飾語を探す
                past_participle = None
                
                # governing_verb自身が過去分詞かチェック
                if governing_verb.tag_ == 'VBN':
                    past_participle = governing_verb
                    print(f"   🔍 governing_verb自身が過去分詞: {governing_verb.text}")
                adverb = None
                
                # be動詞の子要素から過去分詞を探す
                print(f"   🔍 DEBUG: be動詞'{be_verb.text}'の子要素をチェック")
                for child in be_verb.children:
                    print(f"   🔍 DEBUG: be動詞の子: {child.text} (tag: {child.tag_}, dep: {child.dep_})")
                    if child.tag_ == 'VBN':  # 過去分詞
                        past_participle = child
                        print(f"   🔍 be動詞の子から過去分詞発見: {child.text}")
                    elif child.dep_ == 'advmod':  # 副詞修飾語
                        adverb = child.text
                        print(f"   🔍 be動詞の子から副詞発見: {child.text}")
                
                # be動詞の兄弟（governingの子要素）から過去分詞を探す
                if not past_participle:
                    print(f"   🔍 DEBUG: governing verb '{governing_verb.text}'の子要素をチェック")
                    for child in governing_verb.children:
                        print(f"   🔍 DEBUG: governing verbの子: {child.text} (tag: {child.tag_}, dep: {child.dep_})")
                        if child.tag_ == 'VBN':
                            past_participle = child
                            print(f"   🔍 governing verbの子から過去分詞発見: {child.text}")
                
                # 過去分詞の子要素から副詞を探す
                if past_participle and not adverb:
                    for child in past_participle.children:
                        if child.dep_ == 'advmod':
                            adverb = child.text
                            print(f"   🔍 過去分詞の子から副詞発見: {child.text}")
                            break
                
                # 文全体から 'quickly' のような副詞を探す（フォールバック）
                if not adverb:
                    for token in doc:
                        if token.pos_ == 'ADV' and token.dep_ == 'advmod':
                            # 過去分詞に依存する副詞を優先
                            if past_participle and token.head == past_participle:
                                adverb = token.text
                                print(f"   🔍 フォールバック: 過去分詞に依存する副詞発見: {token.text}")
                                break
                            # または動詞に依存する副詞
                            elif token.head == governing_verb:
                                adverb = token.text
                                print(f"   🔍 フォールバック: governing verbに依存する副詞発見: {token.text}")
                                break
                
                # 主語を検出: 真の主動詞の主語を探す
                subject = None
                for token in doc:
                    if token.dep_ == 'nsubj' and token.head == main_verb:
                        subject = self._get_full_noun_phrase(token)
                        break
                
                print(f"   📍 主語検出: S = '{subject}'")
                print(f"   📍 主動詞検出: V = '{main_verb.text}'")
                print(f"   📍 受動不定詞目的語: O1 = 空（サブスロット使用）")
                print(f"   📍 受動助動詞検出: sub-aux = 'to be'")
                print(f"   📍 受動動詞検出: sub-v = '{past_participle.text if past_participle else 'unknown'}'")
                if adverb:
                    print(f"   📍 副詞修飾語検出: sub-m2 = '{adverb}'")
                
                result = {
                    'success': True,
                    'main_slots': {
                        'S': subject or '',
                        'V': main_verb.text,
                        'O1': ''
                    },
                    'sub_slots': {
                        'sub-aux': 'to be',
                        'sub-v': past_participle.text if past_participle else '',
                        '_parent_slot': 'O1'
                    },
                    'collaboration': ['infinitive'],
                    'primary_handler': 'infinitive',
                    'metadata': {
                        'handler': 'infinitive_passive',
                        'usage_type': 'passive_infinitive',
                        'confidence': 0.9,
                        'spacy_analysis': True
                    }
                }
                
                if adverb:
                    result['sub_slots']['sub-m2'] = adverb
                
                return result
        
        return {'success': False, 'error': '受動不定詞の解析に失敗しました'}
    
    def _process_wh_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        疑問詞+不定詞の処理（case166: I don't know what to do）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 疑問詞+不定詞処理: {text}")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            if inf_token['pattern'] == 'wh_infinitive':
                main_verb = inf_token['main_verb']
                wh_word = inf_token['wh_word']
                head = inf_token['head']
                
                # 主語と助動詞を検出
                subject = None
                auxiliary = None
                
                # より正確な主語・助動詞検出
                for token in doc:
                    if token.dep_ == 'nsubj' and token.head == head:
                        subject = token.text
                    elif token.dep_ == 'aux' and token.head == head:
                        # 助動詞と否定の組み合わせをチェック
                        neg_token = None
                        for child in token.head.children:
                            if child.dep_ == 'neg':
                                neg_token = child
                                break
                        
                        if neg_token:
                            auxiliary = f"{token.text}{neg_token.text}"
                        else:
                            auxiliary = token.text
                
                print(f"   📍 主語検出: S = '{subject}'")
                if auxiliary:
                    print(f"   📍 助動詞検出: Aux = '{auxiliary}'")
                print(f"   📍 主動詞検出: V = '{head.text}'")
                print(f"   📍 疑問詞+不定詞目的語: O1 = 空（サブスロット使用）")
                print(f"   📍 疑問詞検出: sub-o1 = '{wh_word.text}'")
                print(f"   📍 不定詞動詞検出: sub-v = 'to {main_verb.text}'")
                
                # main_slotsに助動詞も含める
                main_slots = {
                    'S': subject or '',
                    'V': head.text,
                    'O1': ''
                }
                
                if auxiliary:
                    main_slots['Aux'] = auxiliary
                
                result = {
                    'success': True,
                    'main_slots': main_slots,
                    'sub_slots': {
                        'sub-o1': wh_word.text,
                        'sub-v': f'to {main_verb.text}',
                        '_parent_slot': 'O1'
                    },
                    'collaboration': ['infinitive'],
                    'primary_handler': 'infinitive',
                    'metadata': {
                        'handler': 'infinitive_wh_question',
                        'usage_type': 'wh_infinitive',
                        'confidence': 0.9,
                        'spacy_analysis': True
                    }
                }
                
                if auxiliary:
                    result['main_slots']['Aux'] = auxiliary
                
                return result
        
        return {'success': False, 'error': '疑問詞+不定詞の解析に失敗しました'}
    
    def _process_causative_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        使役構文の処理（case167: I want you to help me）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 使役構文処理: {text}")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            if inf_token['pattern'] == 'causative':
                main_verb = inf_token['main_verb']
                causative_verb = inf_token['causative_verb']
                object_person = inf_token.get('object')
                
                # 主語を検出
                subject = None
                for token in doc:
                    if token.dep_ == 'nsubj' and token.head == causative_verb:
                        subject = token.text
                        break
                
                # 不定詞の目的語を検出
                infinitive_object = None
                for child in main_verb.children:
                    if child.dep_ == 'dobj':
                        infinitive_object = child.text
                        break
                
                print(f"   📍 主語検出: S = '{subject}'")
                print(f"   📍 使役動詞検出: V = '{causative_verb.text}'")
                if object_person:
                    print(f"   📍 直接目的語検出: O1 = '{object_person.text}'")
                else:
                    print(f"   ⚠️ 直接目的語検出失敗")
                print(f"   📍 目的語補語: C2 = 空（サブスロット使用）")
                print(f"   📍 不定詞動詞検出: sub-v = 'to {main_verb.text}'")
                if infinitive_object:
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{infinitive_object}'")
                
                result = {
                    'success': True,
                    'main_slots': {
                        'S': subject or '',
                        'V': causative_verb.text,
                        'O1': object_person.text if object_person else '',
                        'C2': ''
                    },
                    'sub_slots': {
                        'sub-v': f'to {main_verb.text}',
                        'sub-o1': infinitive_object or '',
                        '_parent_slot': 'C2'
                    },
                    'collaboration': ['infinitive'],
                    'primary_handler': 'infinitive',
                    'metadata': {
                        'handler': 'infinitive_causative',
                        'usage_type': 'causative',
                        'confidence': 0.9,
                        'spacy_analysis': True
                    }
                }
                
                if infinitive_object:
                    result['sub_slots']['sub-o1'] = infinitive_object
                
                return result
        
        return {'success': False, 'error': '使役構文の解析に失敗しました'}
    
    def _process_be_about_to_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        be about to構文の処理（case168: The meeting is about to start）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 be about to構文処理: {text}")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            if inf_token['pattern'] == 'be_about_to':
                main_verb = inf_token['main_verb']
                about_token = inf_token['about_token']
                
                # 主語とbe動詞を検出
                subject = None
                be_verb = None
                
                for token in doc:
                    if token.dep_ == 'nsubj':
                        subject = self._get_full_noun_phrase(token)
                    elif token.lemma_ == 'be' and token.pos_ == 'AUX':
                        be_verb = token.text
                
                print(f"   📍 主語検出: S = '{subject}'")
                print(f"   📍 be about to助動詞統合: Aux = '{be_verb} about to'")
                print(f"   📍 不定詞動詞検出: V = '{main_verb.text}'")
                
                return {
                    'success': True,
                    'main_slots': {
                        'S': subject or '',
                        'Aux': f'{be_verb} about to' if be_verb else 'about to',
                        'V': main_verb.text
                    },
                    'sub_slots': {},
                    'collaboration': ['infinitive'],
                    'primary_handler': 'infinitive',
                    'metadata': {
                        'handler': 'infinitive_be_about_to',
                        'usage_type': 'be_about_to',
                        'confidence': 0.9,
                        'spacy_analysis': True
                    }
                }
        
        return {'success': False, 'error': 'be about to構文の解析に失敗しました'}
    
    def _process_in_order_to_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        in order to構文の処理（case169: She studies hard in order to pass the exam）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 in order to構文処理: {text}")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            if inf_token['pattern'] == 'in_order_to':
                main_verb = inf_token['main_verb']
                
                # 主語と主動詞を検出
                subject = None
                main_verb_word = None
                adverb = None
                
                for token in doc:
                    if token.dep_ == 'nsubj':
                        subject = token.text
                    elif token.dep_ == 'ROOT':
                        main_verb_word = token.text
                    elif token.dep_ == 'advmod' and token.head.dep_ == 'ROOT':
                        adverb = token.text
                
                # 不定詞の目的語を検出
                infinitive_object = None
                for child in main_verb.children:
                    if child.dep_ == 'dobj':
                        infinitive_object = self._get_full_noun_phrase(child)
                        break
                
                print(f"   📍 主語検出: S = '{subject}'")
                print(f"   📍 主動詞検出: V = '{main_verb_word}'")
                if adverb:
                    print(f"   📍 副詞修飾語検出: M2 = '{adverb}'")
                print(f"   📍 目的の副詞句: M3 = 空（サブスロット使用）")
                print(f"   📍 in order to動詞検出: sub-v = 'in order to {main_verb.text}'")
                if infinitive_object:
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{infinitive_object}'")
                
                result = {
                    'success': True,
                    'main_slots': {
                        'S': subject or '',
                        'V': main_verb_word or '',
                        'M3': ''
                    },
                    'sub_slots': {
                        'sub-v': f'in order to {main_verb.text}',
                        '_parent_slot': 'M3'
                    },
                    'collaboration': ['infinitive'],
                    'primary_handler': 'infinitive',
                    'metadata': {
                        'handler': 'infinitive_in_order_to',
                        'usage_type': 'in_order_to',
                        'confidence': 0.9,
                        'spacy_analysis': True
                    }
                }
                
                if adverb:
                    result['main_slots']['M2'] = adverb
                if infinitive_object:
                    result['sub_slots']['sub-o1'] = infinitive_object
                
                return result
        
        return {'success': False, 'error': 'in order to構文の解析に失敗しました'}
    
    def _process_so_as_to_infinitive(self, doc, text: str, infinitive_info: Dict, slots: Dict) -> Dict[str, Any]:
        """
        so as to構文の処理（case170: He left early so as to avoid traffic）
        
        Args:
            doc: spaCy解析結果
            text: 元の英文
            infinitive_info: 不定詞情報
            slots: スロット分類
            
        Returns:
            Dict[str, Any]: 処理結果
        """
        print(f"📝 so as to構文処理: {text}")
        
        for inf_token in infinitive_info['infinitive_tokens']:
            if inf_token['pattern'] == 'so_as_to':
                main_verb = inf_token['main_verb']
                
                # 主語と主動詞を検出
                subject = None
                main_verb_word = None
                adverb = None
                
                for token in doc:
                    if token.dep_ == 'nsubj':
                        subject = token.text
                    elif token.dep_ == 'ROOT':
                        main_verb_word = token.text
                    elif token.dep_ == 'advmod' and token.head.dep_ == 'ROOT':
                        adverb = token.text
                
                # 不定詞の目的語を検出
                infinitive_object = None
                for child in main_verb.children:
                    if child.dep_ == 'dobj':
                        infinitive_object = child.text
                        break
                
                print(f"   📍 主語検出: S = '{subject}'")
                print(f"   📍 主動詞検出: V = '{main_verb_word}'")
                if adverb:
                    print(f"   📍 副詞修飾語検出: M2 = '{adverb}'")
                print(f"   📍 目的の副詞句: M3 = 空（サブスロット使用）")
                print(f"   📍 so as to動詞検出: sub-v = 'so as to {main_verb.text}'")
                if infinitive_object:
                    print(f"   📍 不定詞目的語検出: sub-o1 = '{infinitive_object}'")
                
                result = {
                    'success': True,
                    'main_slots': {
                        'S': subject or '',
                        'V': main_verb_word or '',
                        'M3': ''
                    },
                    'sub_slots': {
                        'sub-v': f'so as to {main_verb.text}',
                        '_parent_slot': 'M3'
                    },
                    'collaboration': ['infinitive'],
                    'primary_handler': 'infinitive',
                    'metadata': {
                        'handler': 'infinitive_so_as_to',
                        'usage_type': 'so_as_to',
                        'confidence': 0.9,
                        'spacy_analysis': True
                    }
                }
                
                if adverb:
                    result['main_slots']['M2'] = adverb
                if infinitive_object:
                    result['sub_slots']['sub-o1'] = infinitive_object
                
                return result
        
        return {'success': False, 'error': 'so as to構文の解析に失敗しました'}
