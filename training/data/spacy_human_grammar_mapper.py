#!/usr/bin/env python3
"""
spaCy辞書 + 人間文法認識システム
現在のシステムからの移植版
"""

import spacy
import logging
from typing import Dict, List, Any, Optional, Tuple

class SpacyHumanGrammarMapper:
    """
    spaCy辞書 + 人間文法認識による英語5文型スロット分解システム
    """
    
    def __init__(self):
        """初期化"""
        # spaCy辞書システム初期化
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy辞書システム初期化完了")
        except OSError:
            print("❌ spaCy英語モデルが見つかりません")
            raise
        
        # ログ設定
        self.logger = logging.getLogger(__name__)
        
        # 人間文法認識パラメータ
        self.confidence_threshold = 0.8
        
    def analyze_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        文章を解析してRephraseスロット構造を生成
        
        Args:
            sentence (str): 解析対象の文章
            
        Returns:
            Dict[str, Any]: Rephraseスロット構造
        """
        try:
            # 1. spaCy語彙解析（辞書機能）
            lexical_info = self._extract_lexical_knowledge(sentence)
            
            # 2. 人間文法認識（構造認識）
            grammar_pattern = self._human_grammar_recognition(lexical_info)
            
            # 3. Rephraseスロット生成
            rephrase_slots = self._generate_rephrase_slots(lexical_info, grammar_pattern)
            
            return rephrase_slots
            
        except Exception as e:
            self.logger.error(f"文章解析エラー: {e}")
            return self._create_error_result(sentence, str(e))
    
    def _extract_lexical_knowledge(self, sentence: str) -> Dict[str, Any]:
        """
        spaCy辞書から語彙知識を抽出
        """
        doc = self.nlp(sentence)
        
        lexical_info = {
            'tokens': [],
            'sentence': sentence,
            'spacy_doc': doc
        }
        
        for token in doc:
            token_info = {
                'text': token.text,
                'pos': token.pos_,           # 主要品詞 (NOUN, VERB, etc.)
                'tag': token.tag_,           # 詳細品詞 (NNS, VBZ, etc.)
                'lemma': token.lemma_,       # 原形
                'morph': str(token.morph),   # 形態情報
                'is_stop': token.is_stop,    # ストップワード
                'is_alpha': token.is_alpha,  # アルファベット
                'index': token.i             # 位置
            }
            lexical_info['tokens'].append(token_info)
        
        self.logger.info(f"語彙解析完了: {len(lexical_info['tokens'])}語彙")
        return lexical_info
    
    def _human_grammar_recognition(self, lexical_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        人間文法認識による構造パターン検出
        """
        tokens = lexical_info['tokens']
        
        # 5文型パターン検出
        pattern_result = None
        
        # 第1文型（SV）検出
        sv_result = self._detect_sv_pattern_human(tokens)
        if sv_result['detected']:
            pattern_result = sv_result
        
        # 第2文型（SVC）検出
        if not pattern_result:
            svc_result = self._detect_svc_pattern_human(tokens)
            if svc_result['detected']:
                pattern_result = svc_result
        
        # 第3文型（SVO）検出
        if not pattern_result:
            svo_result = self._detect_svo_pattern_human(tokens)
            if svo_result['detected']:
                pattern_result = svo_result
        
        # 第4文型（SVOO）検出
        if not pattern_result:
            svoo_result = self._detect_svoo_pattern_human(tokens)
            if svoo_result['detected']:
                pattern_result = svoo_result
        
        # 第5文型（SVOC）検出
        if not pattern_result:
            svoc_result = self._detect_svoc_pattern_human(tokens)
            if svoc_result['detected']:
                pattern_result = svoc_result
        
        # デフォルト結果
        if not pattern_result:
            pattern_result = {
                'detected': False,
                'pattern': 'UNKNOWN',
                'confidence': 0.0,
                'elements': {},
                'error': '文型パターンを認識できませんでした'
            }
        
        return pattern_result
    
    def _detect_sv_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """
        第1文型（SV）人間文法認識
        
        人間の認識: [主語] + [自動詞] = 第1文型
        """
        if len(tokens) < 2:
            return {'detected': False, 'pattern': 'SV', 'confidence': 0.0}
        
        # 基本パターン: 2語（主語 + 動詞）
        if len(tokens) == 2:
            token1, token2 = tokens[0], tokens[1]
            
            # 主語候補判定（人間基準）
            is_subject = self._is_subject_human(token1)
            # 自動詞候補判定（人間基準）
            is_intransitive_verb = self._is_intransitive_verb_human(token2)
            
            if is_subject and is_intransitive_verb:
                return {
                    'detected': True,
                    'pattern': 'SV',
                    'confidence': 0.95,
                    'elements': {
                        'subject': token1,
                        'verb': token2
                    },
                    'slots': ['S', 'V'],
                    'slot_phrases': [token1['text'], token2['text']]
                }
        
        # 3語パターン: 冠詞 + 名詞 + 動詞
        elif len(tokens) == 3:
            token1, token2, token3 = tokens[0], tokens[1], tokens[2]
            
            # The dog runs パターン
            if (self._is_determiner_human(token1) and 
                self._is_noun_human(token2) and 
                self._is_intransitive_verb_human(token3)):
                
                return {
                    'detected': True,
                    'pattern': 'SV',
                    'confidence': 0.90,
                    'elements': {
                        'subject': f"{token1['text']} {token2['text']}",
                        'verb': token3
                    },
                    'slots': ['S', 'V'],
                    'slot_phrases': [f"{token1['text']} {token2['text']}", token3['text']]
                }
        
        return {'detected': False, 'pattern': 'SV', 'confidence': 0.0}
    
    def _detect_svc_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """第2文型（SVC）人間文法認識"""
        # 実装予定
        return {'detected': False, 'pattern': 'SVC', 'confidence': 0.0}
    
    def _detect_svo_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """第3文型（SVO）人間文法認識"""
        # 実装予定
        return {'detected': False, 'pattern': 'SVO', 'confidence': 0.0}
    
    def _detect_svoo_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """第4文型（SVOO）人間文法認識"""
        # 実装予定
        return {'detected': False, 'pattern': 'SVOO', 'confidence': 0.0}
    
    def _detect_svoc_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """第5文型（SVOC）人間文法認識"""
        # 実装予定
        return {'detected': False, 'pattern': 'SVOC', 'confidence': 0.0}
    
    # 人間基準判定関数群
    def _is_subject_human(self, token: Dict) -> bool:
        """人間基準での主語判定"""
        return token['pos'] in ['NOUN', 'PRON', 'PROPN']
    
    def _is_noun_human(self, token: Dict) -> bool:
        """人間基準での名詞判定"""
        return token['pos'] in ['NOUN', 'PROPN']
    
    def _is_determiner_human(self, token: Dict) -> bool:
        """人間基準での冠詞・限定詞判定"""
        return token['pos'] == 'DET'
    
    def _is_intransitive_verb_human(self, token: Dict) -> bool:
        """人間基準での自動詞判定"""
        # spaCy品詞で動詞を確認 + 語順による判定
        return token['pos'] == 'VERB' and token['tag'] in ['VBP', 'VBZ', 'VB']
    
    def _generate_rephrase_slots(self, lexical_info: Dict, grammar_pattern: Dict) -> Dict[str, Any]:
        """
        Rephraseスロット構造生成（現在システム互換）
        """
        if not grammar_pattern['detected']:
            return self._create_error_result(lexical_info['sentence'], 
                                           grammar_pattern.get('error', '文型認識失敗'))
        
        # Rephrase完全互換スロット構造
        slots = grammar_pattern['slots']
        slot_phrases = grammar_pattern['slot_phrases']
        
        result = {
            'Slot': slots,
            'SlotPhrase': slot_phrases,
            'Slot_display_order': list(range(1, len(slots) + 1)),
            'display_order': list(range(1, len(slots) + 1)),
            'PhraseType': self._determine_phrase_types(slots),
            'SubslotID': list(range(len(slots))),
            
            # 解析情報
            'pattern_detected': grammar_pattern['pattern'],
            'confidence': grammar_pattern['confidence'],
            'analysis_method': 'spacy_human_grammar',
            'lexical_tokens': len(lexical_info['tokens'])
        }
        
        return result
    
    def _determine_phrase_types(self, slots: List[str]) -> List[str]:
        """スロットに対応する句型を決定"""
        phrase_types = []
        for slot in slots:
            if slot == 'S':
                phrase_types.append('名詞句')
            elif slot == 'V':
                phrase_types.append('動詞句')
            elif slot == 'O':
                phrase_types.append('名詞句')
            elif slot == 'C':
                phrase_types.append('補語句')
            else:
                phrase_types.append('未分類')
        return phrase_types
    
    def _create_error_result(self, sentence: str, error_msg: str) -> Dict[str, Any]:
        """エラー結果生成"""
        return {
            'Slot': [],
            'SlotPhrase': [],
            'Slot_display_order': [],
            'display_order': [],
            'PhraseType': [],
            'SubslotID': [],
            'error': error_msg,
            'sentence': sentence,
            'analysis_method': 'spacy_human_grammar'
        }

def test_spacy_human_grammar_system():
    """spaCy人間文法認識システムのテスト"""
    print("=== spaCy辞書 + 人間文法認識システム テスト ===\n")
    
    # システム初期化
    mapper = SpacyHumanGrammarMapper()
    
    # テスト文章
    test_sentences = [
        "Children play",
        "The dog runs", 
        "Birds fly"
    ]
    
    for sentence in test_sentences:
        print(f"--- '{sentence}' ---")
        result = mapper.analyze_sentence(sentence)
        
        if 'error' in result:
            print(f"❌ エラー: {result['error']}")
        else:
            print(f"✅ パターン: {result['pattern_detected']}")
            print(f"   確信度: {result['confidence']:.1%}")
            print(f"   スロット: {result['Slot']}")
            print(f"   句: {result['SlotPhrase']}")
            print(f"   句型: {result['PhraseType']}")
        print()

if __name__ == '__main__':
    test_spacy_human_grammar_system()
