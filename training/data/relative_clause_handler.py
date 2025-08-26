#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RelativeClauseHandler: 関係節処理専用ハンドラー

Phase 2対応: 関係節検出・分解・サブスロット生成
POS解析のみ使用（dependency parsing禁止）
"""

import spacy
from typing import Dict, List, Any, Optional, Tuple

class RelativeClauseHandler:
    """
    関係節処理ハンドラー
    
    処理手順:
    1. 関係詞検出（who, which, that, whose）
    2. 関係節境界特定
    3. 先行詞特定
    4. サブスロット生成（sub-s, sub-v, sub-m, etc.）
    5. 親スロット情報付与（_parent_slot）
    """
    
    def __init__(self):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        
        # 関係詞分類
        self.relative_pronouns = {
            'subjective': ['who', 'which', 'that'],    # 主格
            'objective': ['whom', 'which', 'that'],    # 目的格  
            'possessive': ['whose'],                   # 所有格
            'adverbial': ['where', 'when', 'why', 'how']  # 関係副詞
        }
        
        # 全関係詞リスト
        self.all_relatives = []
        for rel_list in self.relative_pronouns.values():
            self.all_relatives.extend(rel_list)
        self.all_relatives = list(set(self.all_relatives))  # 重複除去
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        関係節処理メイン
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, main_slots, sub_slots, segments）
        """
        try:
            doc = self.nlp(text)
            
            # 1. 関係詞存在確認
            relative_info = self._detect_relative_pronouns(doc)
            if not relative_info:
                return {'success': False, 'error': '関係詞が見つかりませんでした'}
            
            # 2. 関係節境界特定
            segments = self._identify_clause_boundaries(doc, relative_info)
            if not segments:
                return {'success': False, 'error': '関係節境界を特定できませんでした'}
            
            # 3. 先行詞特定と代表語句作成
            antecedent_info = self._identify_antecedent(doc, segments)
            
            # 4. サブスロット生成
            sub_slots = self._generate_sub_slots(doc, segments, antecedent_info)
            
            # 5. メインスロット調整（代表語句のみ）
            main_slots = self._create_main_slots(antecedent_info)
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'segments': segments,
                'antecedent_info': antecedent_info
            }
            
        except Exception as e:
            return {'success': False, 'error': f'処理エラー: {str(e)}'}
    
    def _detect_relative_pronouns(self, doc) -> List[Dict[str, Any]]:
        """
        関係詞検出
        
        Args:
            doc: spaCy Doc オブジェクト
            
        Returns:
            List[Dict]: 検出された関係詞情報
        """
        relatives = []
        
        for i, token in enumerate(doc):
            if token.text.lower() in self.all_relatives:
                # 関係詞タイプ判定
                rel_type = None
                for type_name, type_list in self.relative_pronouns.items():
                    if token.text.lower() in type_list:
                        rel_type = type_name
                        break
                
                relatives.append({
                    'token': token,
                    'index': i,
                    'text': token.text,
                    'type': rel_type,
                    'lemma': token.lemma_
                })
        
        return relatives
    
    def _identify_clause_boundaries(self, doc, relative_info: List[Dict]) -> Dict[str, Any]:
        """
        関係節境界特定
        
        Args:
            doc: spaCy Doc オブジェクト
            relative_info: 検出された関係詞情報
            
        Returns:
            Dict: セグメント情報（antecedent, relative_clause, main_clause）
        """
        if not relative_info:
            return {}
        
        # 最初の関係詞を基準に処理（複数関係詞の場合は最初のものを優先）
        rel_pronoun = relative_info[0]
        rel_index = rel_pronoun['index']
        
        # 先行詞部分（関係詞の前）
        antecedent_tokens = [token for token in doc[:rel_index] if token.pos_ != 'PUNCT']
        
        # 関係節部分（関係詞から次の主動詞まで）
        relative_clause_tokens = []
        main_clause_start = len(doc)
        
        # 関係詞から開始
        relative_clause_tokens.append(doc[rel_index])
        
        # 関係節の終了点を検出
        verb_count = 0
        for i in range(rel_index + 1, len(doc)):
            token = doc[i]
            
            if token.pos_ == 'PUNCT':
                continue
            
            # 動詞カウント
            if token.pos_ in ['VERB', 'AUX']:
                verb_count += 1
                
            relative_clause_tokens.append(token)
            
            # 関係節終了条件：2番目の動詞の直前まで
            if verb_count >= 2:
                # 現在の動詞は主節の動詞なので、それより前で関係節終了
                relative_clause_tokens.pop()  # 主節動詞を除去
                main_clause_start = i
                break
        
        # 主節部分（関係節終了後）
        main_clause_tokens = [token for token in doc[main_clause_start:] if token.pos_ != 'PUNCT']
        
        return {
            'antecedent': antecedent_tokens,
            'relative_clause': relative_clause_tokens,
            'main_clause': main_clause_tokens,
            'relative_pronoun': rel_pronoun
        }
    
    def _identify_antecedent(self, doc, segments: Dict) -> Dict[str, Any]:
        """
        先行詞特定と代表語句作成
        
        Args:
            doc: spaCy Doc オブジェクト  
            segments: セグメント情報
            
        Returns:
            Dict: 先行詞情報（representative_phrase, original_phrase）
        """
        antecedent_tokens = segments.get('antecedent', [])
        relative_pronoun = segments.get('relative_pronoun', {})
        
        if not antecedent_tokens:
            return {}
        
        # 先行詞の核となる名詞を特定
        head_noun = None
        for token in reversed(antecedent_tokens):  # 後ろから検索
            if token.pos_ in ['NOUN', 'PROPN', 'PRON']:
                head_noun = token
                break
        
        if not head_noun:
            return {}
        
        # 代表語句作成（先行詞 + 関係詞）
        original_phrase = ' '.join([t.text for t in antecedent_tokens])
        relative_text = relative_pronoun.get('text', '')
        representative_phrase = f"{original_phrase} {relative_text}"
        
        return {
            'head_noun': head_noun,
            'original_phrase': original_phrase,
            'representative_phrase': representative_phrase,
            'tokens': antecedent_tokens
        }
    
    def _generate_sub_slots(self, doc, segments: Dict, antecedent_info: Dict) -> Dict[str, Any]:
        """
        サブスロット生成
        
        Args:
            doc: spaCy Doc オブジェクト
            segments: セグメント情報
            antecedent_info: 先行詞情報
            
        Returns:
            Dict: サブスロット情報
        """
        relative_clause = segments.get('relative_clause', [])
        relative_pronoun = segments.get('relative_pronoun', {})
        
        if not relative_clause:
            return {}
        
        sub_slots = {}
        
        # 関係詞タイプに応じたサブスロット生成
        rel_type = relative_pronoun.get('type')
        rel_text = relative_pronoun.get('text', '')
        
        if rel_type == 'subjective':
            # 主格関係代名詞: who/which/that runs
            sub_slots['sub-s'] = antecedent_info.get('representative_phrase', '')
            
            # 関係節内の動詞検出
            for token in relative_clause[1:]:  # 関係詞の次から
                if token.pos_ in ['VERB', 'AUX']:
                    sub_slots['sub-v'] = token.text
                    break
            
            # 関係節内の修飾語検出  
            modifiers = []
            for token in relative_clause[1:]:
                if token.pos_ in ['ADV', 'ADJ'] and token.text not in sub_slots.values():
                    modifiers.append(token.text)
            
            if modifiers:
                sub_slots['sub-m2'] = ' '.join(modifiers)
        
        elif rel_type == 'objective':
            # 目的格関係代名詞: which I bought
            # 関係節内の主語検出
            for token in relative_clause[1:]:
                if token.pos_ in ['PRON', 'NOUN', 'PROPN']:
                    sub_slots['sub-s'] = token.text
                    break
            
            # 関係節内の動詞検出
            for token in relative_clause[1:]:
                if token.pos_ in ['VERB', 'AUX']:
                    sub_slots['sub-v'] = token.text
                    break
                    
        elif rel_type == 'possessive':
            # 所有格関係代名詞: whose car
            # whose の次の名詞が所有物
            for i, token in enumerate(relative_clause):
                if token.text.lower() == 'whose' and i + 1 < len(relative_clause):
                    possessed = relative_clause[i + 1]
                    if possessed.pos_ in ['NOUN', 'PROPN']:
                        sub_slots['sub-s'] = f"whose {possessed.text}"
                        break
            
            # 関係節内の動詞検出
            for token in relative_clause[1:]:
                if token.pos_ in ['VERB', 'AUX']:
                    sub_slots['sub-v'] = token.text
                    break
        
        # 親スロット情報（とりあえずSとして設定、後で調整）
        sub_slots['_parent_slot'] = 'S'
        
        return sub_slots
    
    def _create_main_slots(self, antecedent_info: Dict) -> Dict[str, str]:
        """
        メインスロット作成（代表語句のみ）
        
        Args:
            antecedent_info: 先行詞情報
            
        Returns:
            Dict: メインスロット（関係節部分は空文字列でマスク）
        """
        representative = antecedent_info.get('representative_phrase', '')
        
        return {
            'S': '',  # 関係節を含む主語は空でマスク（後でBasicFivePatternHandlerが処理）
            '_representative_subject': representative  # 代表語句情報を保持
        }


if __name__ == "__main__":
    # 基本テスト
    handler = RelativeClauseHandler()
    
    test_cases = [
        "The man who runs fast is strong.",
        "The book which lies there is mine.",
        "The car whose owner is here is red."
    ]
    
    print("🔍 RelativeClauseHandler テスト実行")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 テストケース {i}: {test_case}")
        result = handler.process(test_case)
        
        if result['success']:
            print(f"✅ 成功")
            print(f"  メインスロット: {result['main_slots']}")
            print(f"  サブスロット: {result['sub_slots']}")
        else:
            print(f"❌ 失敗: {result['error']}")
