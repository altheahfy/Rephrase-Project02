"""
命令文ハンドラー

命令文の特殊な構造を期待値データに合わせて処理:
- 暗示的主語の除去
- pleaseなどの感嘆詞のスロット調整
- 条件文コンテキストでの特別処理
"""

import spacy
from typing import Dict, Any, Optional, List
import re

class ImperativeHandler:
    def __init__(self):
        """命令文ハンドラーの初期化"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("🎯 ImperativeHandler初期化完了")
        except Exception as e:
            print(f"❌ ImperativeHandler初期化エラー: {e}")
            self.nlp = None

    def process(self, text: str, context: str = "normal") -> Dict[str, Any]:
        """
        命令文を処理
        
        Args:
            text: 処理対象テキスト
            context: コンテキスト ("conditional", "normal")
        
        Returns:
            Dict: 処理結果
        """
        try:
            print(f"🎯 ImperativeHandler処理開始: '{text}' (context: {context})")
            
            if not self.nlp:
                return {'success': False, 'error': 'spaCy not loaded'}
            
            # spaCy解析
            doc = self.nlp(text)
            
            # 基本命令文パターンを検出
            if not self._is_imperative(doc):
                return {'success': False, 'error': 'Not an imperative sentence'}
            
            # 命令文を分解
            result = self._decompose_imperative(doc, context)
            
            if result['success']:
                print(f"✅ ImperativeHandler処理完了: {result}")
                return result
            else:
                return {'success': False, 'error': 'Decomposition failed'}
                
        except Exception as e:
            print(f"❌ ImperativeHandler処理エラー: {e}")
            return {'success': False, 'error': str(e)}

    def _is_imperative(self, doc) -> bool:
        """命令文かどうか判定"""
        # 基本パターン: 動詞で始まる、またはplease + 動詞
        if len(doc) == 0:
            return False
        
        # please call me パターン
        if doc[0].text.lower() == "please" and len(doc) > 1 and doc[1].pos_ == "VERB":
            return True
        
        # call me パターン (動詞で始まる)
        if doc[0].pos_ == "VERB" and doc[0].tag_ in ["VB", "VBP"]:
            return True
        
        return False

    def _decompose_imperative(self, doc, context: str) -> Dict[str, Any]:
        """命令文を分解"""
        main_slots = {}
        
        # 主動詞を特定
        main_verb = None
        please_pos = None
        
        for i, token in enumerate(doc):
            if token.text.lower() == "please":
                please_pos = i
            elif token.pos_ == "VERB" and token.tag_ in ["VB", "VBP"]:
                if main_verb is None:  # 最初の動詞を主動詞とする
                    main_verb = token
                    main_verb_idx = i
        
        if not main_verb:
            return {'success': False, 'error': 'No main verb found'}
        
        # 基本スロットを抽出
        main_slots['V'] = main_verb.text
        
        # 目的語を特定
        for token in doc:
            if token.head == main_verb and token.dep_ in ["dobj", "iobj"]:
                if "O1" not in main_slots:
                    main_slots['O1'] = token.text
                elif "O2" not in main_slots:
                    main_slots['O2'] = token.text
        
        # コンテキストに応じてpleaseの配置を調整
        if please_pos is not None:
            if context == "conditional":
                # 条件文コンテキスト: 期待値に合わせてM2に配置
                main_slots['M1'] = ""
                main_slots['M2'] = "please"
                print(f"🔧 条件文コンテキスト: please → M2")
            else:
                # 通常コンテキスト: M1に配置
                main_slots['M1'] = "please"
                print(f"🔧 通常コンテキスト: please → M1")
        
        # 暗示的主語は除去（期待値に合わせる）
        # main_slots['S'] = "(you)" は含めない
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': {},
            'collaboration': ['imperative'],
            'primary_handler': 'imperative'
        }
