#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NounClauseHandler: 名詞節処理ハンドラー
that節・wh-節・間接疑問文の専門分解
専門分担型ハイブリッド解析（品詞分析 + 依存関係）
"""

import re
import spacy
from typing import Dict, Any, List, Tuple, Optional

class NounClauseHandler:
    """名詞節処理ハンドラー（専門分担型ハイブリッド解析）"""
    
    def __init__(self, nlp_model=None, collaborators=None):
        """
        初期化
        
        Args:
            nlp_model: spaCyモデル（オプション）
            collaborators: 協力者ハンドラー辞書
             # 助動詞と否定を同時検出
        aux_token = None
        neg_token = None
        for child in main_verb.children:
            if child.dep_ == 'aux':
                aux_token = child
                print(f"   助動詞候補: '{child.text}'")
            elif child.dep_ == 'neg':
                neg_token = child
                print(f"   否定候補: '{child.text}'")
        
        if aux_token:
            # 否定の場合は結合（doesn't, won't等）
            aux_text = aux_token.text
            if neg_token:
                aux_text += neg_token.text
                print(f"   否定結合: '{aux_token.text}' + '{neg_token.text}' = '{aux_text}'")
            main_slots['Aux'] = aux_text
            print(f"   助動詞検出: '{aux_text}'")- 'adverb': AdverbHandler（修飾語分離）
                - 'five_pattern': BasicFivePatternHandler（5文型分析）
                - 'passive': PassiveVoiceHandler（受動態理解）
                - 'modal': ModalHandler（助動詞処理）
        """
        self.name = "NounClauseHandler"
        self.version = "v1.0"
        self.nlp = nlp_model if nlp_model is not None else spacy.load('en_core_web_sm')
        
        # 協力者ハンドラーたち
        if collaborators:
            self.adverb_handler = collaborators.get('adverb')
            self.five_pattern_handler = collaborators.get('five_pattern')
            self.passive_handler = collaborators.get('passive')
            self.modal_handler = collaborators.get('modal')
        else:
            self.adverb_handler = None
            self.five_pattern_handler = None
            self.passive_handler = None
            self.modal_handler = None
        
        # 名詞節接続詞・疑問詞パターン
        self.noun_clause_connectors = {
            'that_clause': ['that'],
            'wh_clause': ['what', 'who', 'whom', 'whose', 'which', 'where', 'when', 'why', 'how'],
            'whether_clause': ['whether'],
            'if_clause': ['if']
        }
    
    def _extract_full_phrase(self, token, doc):
        """
        Extract complete phrase including modifiers for a token
        
        Args:
            token: Main token
            doc: spaCy parsed document
            
        Returns:
            str: Complete phrase including modifiers
        """
        # List to collect phrase tokens
        phrase_tokens = []
        
        # Collect children of main token (modifiers, determiners, etc.)
        for child in token.children:
            if child.dep_ in ['amod', 'det', 'compound', 'nummod']:
                phrase_tokens.append((child.i, child.text))
        
        # Add main token
        phrase_tokens.append((token.i, token.text))
        
        # Sort by index to maintain natural word order
        phrase_tokens.sort(key=lambda x: x[0])
        
        # Build phrase
        phrase = ' '.join([text for _, text in phrase_tokens])
        
        return phrase
    
    def process(self, text: str, original_text: str = None) -> Dict[str, Any]:
        """
        名詞節処理メイン
        
        Args:
            text: 処理対象の英語文
            original_text: オリジナルテキスト（参考用）
            
        Returns:
            Dict: 処理結果
        """
        print(f"🔍 NounClauseHandler.process: '{text}'")
        
        try:
            # Step 1: spaCy解析
            doc = self.nlp(text)
            
            # Step 2: 名詞節検出
            noun_clause_info = self._detect_noun_clauses(doc, text)
            
            if not noun_clause_info:
                print(f"ℹ️ 名詞節未検出: '{text}'")
                return self._create_failure_result(text, "名詞節未検出")
            
            # Step 3: 名詞節タイプ別処理
            result = self._process_noun_clause(doc, text, noun_clause_info)
            
            if result['success']:
                print(f"✅ NounClauseHandler成功: {result['main_slots']}")
                print(f"📋 サブスロット: {result['sub_slots']}")
            
            return result
            
        except Exception as e:
            print(f"❌ NounClauseHandler.process エラー: {e}")
            return self._create_failure_result(text, f"処理エラー: {str(e)}")
    
    def detect_noun_clauses(self, text: str) -> List[Dict[str, Any]]:
        """
        名詞節検出（CentralController用パブリックメソッド）
        
        Args:
            text: 分析対象文
            
        Returns:
            List[Dict]: 検出された名詞節情報のリスト
        """
        try:
            doc = self.nlp(text)
            noun_clause_info = self._detect_noun_clauses(doc, text)
            return [noun_clause_info] if noun_clause_info else []
        except Exception:
            return []
    
    def _detect_noun_clauses(self, doc, sentence: str) -> Optional[Dict[str, Any]]:
        """
        名詞節検出（専門分担型ハイブリッド解析）
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            
        Returns:
            Dict: 名詞節情報 or None
        """
        print(f"🔍 名詞節検出開始: '{sentence}'")
        
        # 🎯 Wish文専用検出（最優先）
        wish_result = self._detect_wish_clause(doc, sentence)
        if wish_result:
            return wish_result
        
        # spaCy依存関係による名詞節検出
        for token in doc:
            print(f"   {token.text}: dep={token.dep_}, pos={token.pos_}, tag={token.tag_}")
            
            # ccomp: 補語節（that節・wh-節）
            if token.dep_ == 'ccomp':
                print(f"🎯 ccomp検出: '{token.text}' (依存関係使用: 名詞節構造のため)")
                return self._analyze_ccomp_clause(doc, token, sentence)
                
            # csubj: 節主語（That節・wh-節が主語）
            elif token.dep_ == 'csubj':
                print(f"🎯 csubj検出: '{token.text}' (依存関係使用: 節主語のため)")
                return self._analyze_csubj_clause(doc, token, sentence)
        
        # 品詞分析による補完検出
        return self._detect_by_pos_analysis(doc, sentence)
    
    def _analyze_ccomp_clause(self, doc, ccomp_token, sentence: str) -> Dict[str, Any]:
        """
        ccomp節（補語節）の分析
        
        Args:
            doc: spaCy解析結果
            ccomp_token: ccomp要素のトークン
            sentence: 処理対象文
            
        Returns:
            Dict: 名詞節情報
        """
        print(f"📋 ccomp節分析: '{ccomp_token.text}'")
        
        # 接続詞検出（markライクトークン）
        connector = None
        for child in ccomp_token.children:
            if child.dep_ == 'mark' or child.text.lower() in ['that', 'whether', 'if']:
                connector = child.text.lower()
                print(f"   接続詞検出: '{connector}'")
                break
        
        # wh-節の場合（接続詞なし）
        if not connector:
            for token in doc:
                if (token.pos_ in ['PRON', 'ADV'] and 
                    token.text.lower() in self.noun_clause_connectors['wh_clause']):
                    connector = token.text.lower()
                    print(f"   wh-要素検出: '{connector}'")
                    break
                # 追加: where, how, when等の副詞系wh-語
                elif (token.pos_ in ['SCONJ', 'ADV'] and 
                      token.text.lower() in ['where', 'when', 'how', 'why']):
                    connector = token.text.lower()
                    print(f"   wh-副詞検出: '{connector}'")
                    break
        
        return {
            'type': self._determine_clause_type(connector),
            'position': 'object',  # ccompは通常目的語位置
            'connector': connector,
            'main_verb': ccomp_token.text,
            'clause_range': self._get_clause_range(doc, ccomp_token)
        }
    
    def _analyze_csubj_clause(self, doc, csubj_token, sentence: str) -> Dict[str, Any]:
        """
        csubj節（節主語）の分析
        
        Args:
            doc: spaCy解析結果
            csubj_token: csubj要素のトークン
            sentence: 処理対象文
            
        Returns:
            Dict: 名詞節情報
        """
        print(f"📋 csubj節分析: '{csubj_token.text}'")
        
        # 接続詞検出
        connector = None
        for token in doc:
            if (token.i < csubj_token.i and 
                token.text.lower() in ['that', 'whether', 'if'] + self.noun_clause_connectors['wh_clause']):
                connector = token.text.lower()
                print(f"   接続詞検出: '{connector}'")
                break
        
        return {
            'type': self._determine_clause_type(connector),
            'position': 'subject',  # csubjは主語位置
            'connector': connector,
            'main_verb': csubj_token.text,
            'clause_range': self._get_clause_range(doc, csubj_token)
        }
    
    def _detect_by_pos_analysis(self, doc, sentence: str) -> Optional[Dict[str, Any]]:
        """
        品詞分析による名詞節検出（補完）
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            
        Returns:
            Dict: 名詞節情報 or None
        """
        print(f"🔍 品詞分析補完検出: '{sentence}'")
        
        # 簡単なパターンマッチング
        for i, token in enumerate(doc):
            if token.text.lower() in ['that', 'whether', 'if']:
                # 前置詞句内のif節検出
                if i > 0 and doc[i-1].pos_ == 'ADP':  # 前置詞
                    print(f"   前置詞+名詞節検出: '{doc[i-1].text} {token.text}' (品詞使用: 単純パターンのため)")
                    return {
                        'type': 'if_clause_noun',
                        'position': 'prepositional_object',
                        'connector': token.text.lower(),
                        'preposition': doc[i-1].text,
                        'clause_range': (i, len(doc))
                    }
        
        return None
    
    def _detect_wish_clause(self, doc, sentence: str) -> Optional[Dict[str, Any]]:
        """
        Wish文専用検出
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            
        Returns:
            Dict: Wish節情報 or None
        """
        import re
        
        # Wishパターン検出
        wish_pattern = r'\b(?:wish|wishes|wished)\s+'
        if not re.search(wish_pattern, sentence, re.IGNORECASE):
            return None
        
        print(f"🎯 Wish文検出: '{sentence}'")
        
        # Wish動詞を特定
        wish_verb = None
        wish_token = None
        for token in doc:
            if token.text.lower() in ['wish', 'wishes', 'wished']:
                wish_verb = token.text
                wish_token = token
                print(f"   Wish動詞: '{wish_verb}' (位置: {token.i})")
                break
        
        if not wish_token:
            return None
        
        # Wish文のccomp節を特定
        ccomp_token = None
        for child in wish_token.children:
            if child.dep_ == 'ccomp':
                ccomp_token = child
                print(f"   Wish節検出: '{child.text}' (ccomp)")
                break
        
        if not ccomp_token:
            return None
        
        return {
            'type': 'wish_clause',
            'position': 'object',
            'connector': None,  # 暗黙の[that]
            'main_verb': wish_verb,
            'wish_token': wish_token,
            'ccomp_token': ccomp_token,
            'clause_range': (ccomp_token.i, len(doc))
        }
    
    def _detect_by_pos_analysis(self, doc, sentence: str) -> Optional[Dict[str, Any]]:
        """
        品詞分析による補完検出
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            
        Returns:
            Dict: 名詞節情報 or None
        """
        print(f"🔍 品詞分析による補完検出: '{sentence}'")
        
        # 現在の実装では追加検出なし
        return None
    
    def _determine_clause_type(self, connector: str) -> str:
        """
        接続詞から名詞節タイプを判定
        
        Args:
            connector: 接続詞
            
        Returns:
            str: 節タイプ
        """
        if not connector:
            return 'unknown_clause'
        
        if connector == 'that':
            return 'that_clause'
        elif connector in self.noun_clause_connectors['wh_clause']:
            return 'wh_clause'
        elif connector in ['where', 'when', 'how', 'why']:
            return 'wh_clause'  # where, how等も名詞節として処理
        elif connector == 'whether':
            return 'whether_clause'
        elif connector == 'if':
            return 'if_clause'
        else:
            return 'unknown_clause'
    
    def _get_clause_range(self, doc, main_token) -> Tuple[int, int]:
        """
        節の範囲を取得
        
        Args:
            doc: spaCy解析結果
            main_token: 節の主要トークン
            
        Returns:
            Tuple: (開始位置, 終了位置)
        """
        # 簡単な実装: 主要トークンから文末まで
        start_pos = main_token.i
        end_pos = len(doc)
        
        # より正確な範囲検出は今後の拡張で
        return (start_pos, end_pos)
    
    def _process_noun_clause(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        名詞節タイプ別処理
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: 名詞節情報
            
        Returns:
            Dict: 処理結果
        """
        clause_type = noun_clause_info['type']
        position = noun_clause_info['position']
        
        print(f"📋 名詞節処理: type={clause_type}, position={position}")
        
        if clause_type == 'wish_clause':
            return self._process_wish_clause(doc, sentence, noun_clause_info)
        elif clause_type == 'that_clause':
            return self._process_that_clause(doc, sentence, noun_clause_info)
        elif clause_type == 'wh_clause':
            return self._process_wh_clause(doc, sentence, noun_clause_info)
        elif clause_type == 'whether_clause':
            return self._process_whether_clause(doc, sentence, noun_clause_info)
        elif clause_type in ['if_clause', 'if_clause_noun']:
            return self._process_if_clause(doc, sentence, noun_clause_info)
        else:
            return self._create_failure_result(sentence, f"未対応の節タイプ: {clause_type}")
    
    def _process_wish_clause(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wish文処理
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: Wish節情報
            
        Returns:
            Dict: 処理結果
        """
        print(f"📋 Wish文処理開始")
        
        wish_token = noun_clause_info['wish_token']
        ccomp_token = noun_clause_info['ccomp_token']
        
        # 主節構造（I wish）
        main_subject = None
        for token in doc:
            if token.dep_ == 'nsubj' and token.head == wish_token:
                main_subject = token.text
                print(f"   主節主語: '{main_subject}'")
                break
        
        # 従節は空のO1スロットとして表現
        main_slots = {
            'S': main_subject or '',
            'V': wish_token.text,
            'O1': ''  # Wish文の従節は暗黙的
        }
        
        # 従節構造分析 (I were taller → sub-s: "I", sub-v: "were", sub-c1: "taller")
        sub_slots = {'_parent_slot': 'O1'}
        
        # 従節内の要素を分析 - ccompの範囲全体をチェック
        clause_start = ccomp_token.i
        for i in range(clause_start, len(doc)):
            token = doc[i]
            
            # 動詞検出: ccomp自体
            if token == ccomp_token:
                sub_slots['sub-v'] = token.text
                print(f"      従節動詞検出: {token.text} (dep: {token.dep_})")
                
                # この動詞の主語を検出
                for child in token.children:
                    if child.dep_ == 'nsubj':
                        sub_slots['sub-s'] = child.text
                        print(f"      従節主語検出: {child.text} (dep: {child.dep_}, head: {child.head.text})")
                
                # この動詞の補語を検出
                for child in token.children:
                    if child.dep_ in ['acomp', 'attr', 'dobj']:
                        if child.pos_ == 'ADJ':
                            sub_slots['sub-c1'] = child.text
                            print(f"      従節補語検出: {child.text} (dep: {child.dep_})")
                        else:
                            # Extract full phrase including modifiers for objects
                            obj_phrase = self._extract_full_phrase(child, doc)
                            sub_slots['sub-o1'] = obj_phrase
                            print(f"      従節目的語検出: {obj_phrase} (dep: {child.dep_})")
        
        print(f"   主節: {main_slots}")
        print(f"   従節: {sub_slots}")
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'collaboration': ['noun_clause', 'basic_five_pattern'],
            'primary_handler': 'noun_clause',
            'metadata': {
                'handler': 'wish_clause',
                'clause_type': 'wish_clause',
                'confidence': 0.95
            }
        }
    
    def _process_that_clause(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        that節処理
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: 名詞節情報
            
        Returns:
            Dict: 処理結果
        """
        print(f"📋 that節処理開始")
        
        # 基本構造解析
        main_slots, sub_slots = self._extract_basic_structure(doc, sentence, noun_clause_info)
        
        # that節の内部構造解析
        clause_structure = self._analyze_clause_internal_structure(doc, noun_clause_info)
        
        # サブスロットに統合
        sub_slots.update(clause_structure)
        
        # _parent_slot設定（that節は通常目的語位置）
        position = noun_clause_info.get('position', 'object')
        if position == 'subject':
            sub_slots['_parent_slot'] = 'S'
        elif position == 'object':
            sub_slots['_parent_slot'] = 'O1'
        else:
            sub_slots['_parent_slot'] = 'O1'  # デフォルト
        
        return {
            'success': True,
            'text': sentence,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'handler': self.name,
            'clause_type': 'that_clause'
        }
    
    def _process_wh_clause(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        wh-節処理
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: 名詞節情報
            
        Returns:
            Dict: 処理結果
        """
        print(f"📋 wh-節処理開始")
        
        # 基本構造解析
        main_slots, sub_slots = self._extract_basic_structure(doc, sentence, noun_clause_info)
        
        # wh-節の内部構造解析
        clause_structure = self._analyze_clause_internal_structure(doc, noun_clause_info)
        
        # wh-要素の適切な配置
        connector = noun_clause_info.get('connector', '')
        if connector in ['what']:
            clause_structure['sub-o1'] = connector
        elif connector in ['who', 'whom']:
            clause_structure['sub-s'] = connector
        elif connector in ['where', 'when', 'why', 'how']:
            # howの場合、形容詞と結合して処理
            if connector == 'how' and 'sub-c1' in clause_structure:
                clause_structure['sub-m2'] = f"{connector} {clause_structure['sub-c1']}"
                # sub-c1は既にsub-m2に含まれたので削除
                del clause_structure['sub-c1']
                print(f"   how+形容詞結合: sub-m2='{clause_structure['sub-m2']}'")
            else:
                clause_structure['sub-m2'] = connector
        
        # サブスロットに統合
        sub_slots.update(clause_structure)
        
        # _parent_slot設定
        position = noun_clause_info.get('position', 'object')
        if position == 'subject':
            sub_slots['_parent_slot'] = 'S'
        elif position == 'object':
            sub_slots['_parent_slot'] = 'O1'
        else:
            sub_slots['_parent_slot'] = 'O1'  # デフォルト
        
        return {
            'success': True,
            'text': sentence,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'handler': self.name,
            'clause_type': 'wh_clause'
        }
    
    def _process_whether_clause(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        whether節処理
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: 名詞節情報
            
        Returns:
            Dict: 処理結果
        """
        print(f"📋 whether節処理開始")
        
        # 基本構造解析
        main_slots, sub_slots = self._extract_basic_structure(doc, sentence, noun_clause_info)
        
        # whether節の内部構造解析
        clause_structure = self._analyze_clause_internal_structure(doc, noun_clause_info)
        
        # サブスロットに統合
        sub_slots.update(clause_structure)
        
        # _parent_slot設定
        position = noun_clause_info.get('position', 'object')
        if position == 'subject':
            sub_slots['_parent_slot'] = 'S'
        elif position == 'object':
            sub_slots['_parent_slot'] = 'O1'
        else:
            sub_slots['_parent_slot'] = 'O1'  # デフォルト
        
        return {
            'success': True,
            'text': sentence,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'handler': self.name,
            'clause_type': 'whether_clause'
        }
    
    def _process_if_clause(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        if節（名詞用法）処理
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: 名詞節情報
            
        Returns:
            Dict: 処理結果
        """
        print(f"📋 if節（名詞用法）処理開始")
        
        # 基本構造解析
        main_slots, sub_slots = self._extract_basic_structure(doc, sentence, noun_clause_info)
        
        # if節の内部構造解析
        clause_structure = self._analyze_clause_internal_structure(doc, noun_clause_info)
        
        # 前置詞句の場合の特別処理
        if noun_clause_info.get('preposition'):
            preposition = noun_clause_info['preposition']
            connector = noun_clause_info.get('connector', 'if')
            # "on if you" の形式（重複回避）
            subject_part = clause_structure.get('sub-s', '').replace(f'{connector} ', '')
            clause_structure['sub-s'] = f"{preposition} {connector} {subject_part}"
        
        # サブスロットに統合
        sub_slots.update(clause_structure)
        
        # _parent_slot設定
        position = noun_clause_info.get('position', 'object')
        if position == 'subject':
            sub_slots['_parent_slot'] = 'S'
        elif position == 'object':
            sub_slots['_parent_slot'] = 'O1'
        elif position == 'prepositional_object':
            sub_slots['_parent_slot'] = 'M2'
            # 前置詞+if節の場合、M2を空にする
            main_slots['M2'] = ""
            print(f"   前置詞+if節検出: M2空化")
        else:
            sub_slots['_parent_slot'] = 'O1'  # デフォルト
        
        return {
            'success': True,
            'text': sentence,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'handler': self.name,
            'clause_type': 'if_clause_noun'
        }
    
    def _extract_basic_structure(self, doc, sentence: str, noun_clause_info: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        基本構造（主文）の抽出
        
        Args:
            doc: spaCy解析結果
            sentence: 処理対象文
            noun_clause_info: 名詞節情報
            
        Returns:
            Tuple: (main_slots, sub_slots)
        """
        print(f"📋 基本構造抽出開始")
        
        main_slots = {}
        sub_slots = {}
        
        # ROOT動詞検出（主文の動詞）
        main_verb = None
        for token in doc:
            if token.dep_ == 'ROOT':
                main_verb = token
                print(f"   主動詞検出: '{token.text}' (依存関係使用: 複文構造のため)")
                break
        
        if not main_verb:
            print("❌ 主動詞未検出")
            return main_slots, sub_slots
        
        main_slots['V'] = main_verb.text
        
        # 助動詞検出（主動詞の子として）
        for child in main_verb.children:
            if child.dep_ == 'aux':
                # 否定の場合は結合（doesn't, won't等）
                aux_text = child.text
                for grandchild in child.children:
                    if grandchild.dep_ == 'neg':
                        aux_text += grandchild.text
                main_slots['Aux'] = aux_text
                print(f"   助動詞検出: '{aux_text}'")
                break
        
        # 主語検出
        for child in main_verb.children:
            if child.dep_ in ['nsubj', 'csubj']:
                if child.dep_ == 'csubj':
                    # 節主語の場合は空にしてサブスロットで処理
                    main_slots['S'] = ""
                    print(f"   節主語検出: S空化")
                else:
                    main_slots['S'] = child.text
                    print(f"   主語検出: '{child.text}'")
                break
        
        # 目的語・補語検出
        for child in main_verb.children:
            if child.dep_ == 'dobj':
                main_slots['O1'] = child.text
                print(f"   目的語検出: '{child.text}'")
            elif child.dep_ == 'iobj':
                main_slots['O1'] = child.text  # 間接目的語は通常O1
                print(f"   間接目的語検出: '{child.text}'")
            elif child.dep_ == 'acomp':
                main_slots['C1'] = child.text
                print(f"   補語検出: '{child.text}'")
            elif child.dep_ == 'ccomp':
                # 補語節の場合は空にしてサブスロットで処理
                if not main_slots.get('O1'):
                    main_slots['O1'] = ""
                    print(f"   補語節検出: O1空化")
                else:
                    main_slots['O2'] = ""
                    print(f"   補語節検出: O2空化")
            elif child.dep_ == 'prep':
                # 前置詞句検出（名詞節がある場合のM2対応）
                prep_phrase_text = self._extract_prep_phrase(child, noun_clause_info)
                if prep_phrase_text and 'if' in prep_phrase_text.lower():
                    # if節を含む前置詞句の場合はM2空化
                    main_slots['M2'] = ""
                    print(f"   前置詞句節検出: M2空化")
                elif prep_phrase_text:
                    main_slots['M2'] = prep_phrase_text
                    print(f"   前置詞句検出: '{prep_phrase_text}'")
        
        return main_slots, sub_slots
    
    def _extract_prep_phrase(self, prep_token, noun_clause_info: Dict[str, Any]) -> str:
        """
        前置詞句の抽出（名詞節対応）
        
        Args:
            prep_token: spaCy前置詞トークン
            noun_clause_info: 名詞節情報
            
        Returns:
            str: 前置詞句テキスト（節を含む場合は空文字）
        """
        prep_phrase_parts = [prep_token.text]
        
        # 前置詞の子要素（目的語等）を収集
        for child in prep_token.children:
            if child.dep_ == 'pobj':
                # 前置詞の目的語が名詞節の場合は空にする
                connector = noun_clause_info.get('connector', '')
                if connector in child.subtree:
                    # 名詞節が含まれる場合は空文字を返す
                    return ""
                else:
                    prep_phrase_parts.append(child.text)
        
        return ' '.join(prep_phrase_parts) if len(prep_phrase_parts) > 1 else ""
    
    def _analyze_clause_internal_structure(self, doc, noun_clause_info: Dict[str, Any]) -> Dict[str, str]:
        """
        節内部構造の解析
        
        Args:
            doc: spaCy解析結果
            noun_clause_info: 名詞節情報
            
        Returns:
            Dict: 節内部のスロット構造
        """
        print(f"📋 節内部構造解析開始")
        
        clause_structure = {}
        
        # 簡単な実装: 接続詞以降の基本要素を抽出
        connector = noun_clause_info.get('connector', '')
        position = noun_clause_info.get('position', 'object')  # 位置情報を取得
        
        # 節内の主語・動詞・補語検出
        clause_tokens = []
        start_collecting = False
        
        for token in doc:
            # 接続詞以降から収集開始
            if token.text.lower() == connector.lower():
                start_collecting = True
                continue
            
            if start_collecting:
                clause_tokens.append(token)
        
        # 節内部の5文型分析（簡単版）
        clause_subject = None
        clause_verb = None
        clause_complement = None
        clause_aux = None
        
        for token in clause_tokens:
            # 主文の要素は節内に含めない（主語節の場合の 'wonderful' 等）
            if token.dep_ in ['acomp', 'attr'] and token.head.dep_ == 'ROOT':
                continue  # 主文の補語はスキップ
                
            if token.dep_ in ['nsubj', 'nsubjpass'] and not clause_subject:
                # wh-語が主語の場合は除外、目的語wh-語（what）の場合は主語として処理
                if connector not in ['who', 'whom']:
                    clause_structure['sub-s'] = token.text
                    clause_subject = token
                    print(f"   節内主語: '{token.text}'")
            elif token.pos_ in ['VERB'] and not clause_verb:
                clause_structure['sub-v'] = token.text
                clause_verb = token
                print(f"   節内動詞: '{token.text}'")
            elif token.pos_ in ['AUX'] and not clause_verb:
                # be動詞等は動詞として優先処理
                if token.text.lower() in ['is', 'are', 'was', 'were', 'am']:
                    clause_structure['sub-v'] = token.text
                    clause_verb = token
                    print(f"   節内動詞(be): '{token.text}'")
                elif not clause_aux:
                    # 助動詞として処理（will, can等）
                    clause_structure['sub-aux'] = token.text
                    clause_aux = token
                    print(f"   節内助動詞: '{token.text}'")
            elif token.dep_ in ['acomp', 'attr'] and not clause_complement:
                clause_structure['sub-c1'] = token.text
                clause_complement = token
                print(f"   節内補語: '{token.text}'")
            elif token.dep_ in ['advmod'] and token.pos_ in ['ADV']:
                clause_structure['sub-m2'] = token.text
                print(f"   節内副詞: '{token.text}'")
            elif token.dep_ in ['prep'] and token.pos_ in ['ADP']:
                # 前置詞句の検出（"to the party"等）
                prep_phrase = token.text
                for child in token.children:
                    if child.dep_ == 'pobj':
                        prep_phrase += f" {child.text}"
                        # さらにその修飾語も追加
                        for grandchild in child.children:
                            if grandchild.dep_ == 'det':
                                prep_phrase = token.text + f" {grandchild.text} {child.text}"
                clause_structure['sub-m2'] = prep_phrase
                print(f"   節内前置詞句: '{prep_phrase}'")
        
        # 接続詞のみが主語に含まれていない場合の修正（that節等）
        if connector in ['that', 'whether'] and clause_subject and 'sub-s' in clause_structure:
            # 主語節の場合は大文字化、目的語節の場合は小文字
            if position == 'subject':
                clause_structure['sub-s'] = f"{connector.capitalize()} {clause_structure['sub-s']}"
            else:
                clause_structure['sub-s'] = f"{connector.lower()} {clause_structure['sub-s']}"
        
        # if節の場合は前置詞句で処理済みなので重複回避
        if connector == 'if' and clause_subject and 'sub-s' in clause_structure:
            # 既に前置詞句として処理済みの場合はそのまま
            pass
        
        return clause_structure
    
    def _create_failure_result(self, text: str, reason: str) -> Dict[str, Any]:
        """
        失敗結果の作成
        
        Args:
            text: 処理対象文
            reason: 失敗理由
            
        Returns:
            Dict: 失敗結果
        """
        return {
            'success': False,
            'text': text,
            'main_slots': {},
            'sub_slots': {},
            'handler': self.name,
            'reason': reason
        }
