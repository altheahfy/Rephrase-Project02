#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
省略関係詞ハンドラー (OmittedRelativePronounHandler)

省略された関係代名詞（that, which, whom等）を検出し、
適切に復元して文法構造を分解する専門ハンドラー

Examples:
- "The book I read was interesting." → "The book [that] I read"
- "The man I met yesterday was kind." → "The man [whom] I met"
"""

import spacy
import re
from typing import Dict, List, Any, Optional, Tuple

class OmittedRelativePronounHandler:
    """省略関係詞構造専門ハンドラー"""
    
    def __init__(self):
        """初期化"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("⚠️ spaCy英語モデルが見つかりません")
            self.nlp = None
        
        # 省略関係詞パターン（先行詞 + 主語 + 動詞）
        self.omitted_patterns = [
            # 基本パターン: The + 名詞 + 代名詞 + 動詞
            r'\b(The\s+\w+)\s+(I|you|he|she|it|we|they)\s+(\w+)',
            # 複数形パターン
            r'\b(The\s+\w+)\s+(I|you|he|she|it|we|they)\s+(\w+(?:ed|s)?)',
            # 一般名詞パターン
            r'\b([A-Z]\w*(?:\s+\w+)*)\s+(I|you|he|she|it|we|they)\s+(\w+)'
        ]
    
    def can_handle(self, text: str) -> bool:
        """省略関係詞構造の検出"""
        if not self.nlp:
            return False
            
        # 基本的な省略関係詞パターンの検出
        for pattern in self.omitted_patterns:
            if re.search(pattern, text):
                print(f"🔍 省略関係詞パターン検出: {pattern}")
                return True
        
        # spaCyによる詳細分析
        if self._has_omitted_relative_structure(text):
            print(f"🔍 spaCy分析による省略関係詞検出: {text}")
            return True
            
        return False
    
    def _has_omitted_relative_structure(self, text: str) -> bool:
        """spaCyを使用した省略関係詞構造の検出"""
        try:
            doc = self.nlp(text)
            
            # 以下の条件を満たす場合、省略関係詞と判定
            # 1. 明示的な関係代名詞がない
            # 2. 複数の動詞がある
            # 3. 先行詞となる名詞がある
            
            relative_pronouns = ['who', 'which', 'that', 'whom', 'whose']
            has_explicit_relative = any(token.text.lower() in relative_pronouns for token in doc)
            
            if has_explicit_relative:
                return False  # 明示的な関係詞がある場合は対象外
            
            # 動詞の数をカウント
            verbs = [token for token in doc if token.pos_ in ['VERB', 'AUX'] and token.dep_ != 'aux']
            
            # 主語の候補をチェック
            subjects = [token for token in doc if token.dep_ in ['nsubj', 'nsubjpass']]
            
            # 複数の動詞と主語がある場合、省略関係詞の可能性
            if len(verbs) >= 2 and len(subjects) >= 1:
                print(f"  📊 動詞数: {len(verbs)}, 主語数: {len(subjects)}")
                return True
                
        except Exception as e:
            print(f"⚠️ spaCy分析エラー: {e}")
            
        return False
    
    def handle(self, text: str) -> Dict[str, Any]:
        """省略関係詞構造の分解処理"""
        try:
            print(f"🚀 省略関係詞ハンドラー開始: '{text}'")
            
            # spaCy解析
            if not self.nlp:
                return self._create_error_result(text, "spaCyモデルが利用できません")
            
            doc = self.nlp(text)
            self._print_dependency_analysis(doc)
            
            # 省略関係詞の復元と分解
            restoration_result = self._restore_omitted_relative(text, doc)
            if not restoration_result['success']:
                return restoration_result
            
            # 主節と関係節の分離
            separation_result = self._separate_main_and_relative_clauses(
                text, doc, restoration_result['restored_relative']
            )
            
            if not separation_result['success']:
                return separation_result
            
            # 最終結果の構築
            result = self._build_final_result(text, separation_result)
            print(f"✅ 省略関係詞処理完了: {result}")
            
            return result
            
        except Exception as e:
            print(f"❌ 省略関係詞処理エラー: {e}")
            return self._create_error_result(text, str(e))
    
    def _restore_omitted_relative(self, text: str, doc) -> Dict[str, Any]:
        """省略された関係代名詞の復元"""
        try:
            # パターンマッチングによる復元
            for pattern in self.omitted_patterns:
                match = re.search(pattern, text)
                if match:
                    antecedent = match.group(1)  # 先行詞
                    subject = match.group(2)     # 関係節内主語
                    verb = match.group(3)        # 関係節内動詞
                    
                    # 人称に応じた関係代名詞の選択
                    if 'person' in antecedent.lower() or 'man' in antecedent.lower() or 'woman' in antecedent.lower():
                        relative_pronoun = 'whom' if self._is_object_position(text, antecedent) else 'who'
                    else:
                        relative_pronoun = 'that'
                    
                    restored = f"{antecedent} [{relative_pronoun}]"
                    
                    print(f"🔧 関係詞復元: '{antecedent}' → '{restored}'")
                    
                    return {
                        'success': True,
                        'restored_relative': restored,
                        'antecedent': antecedent,
                        'relative_pronoun': relative_pronoun,
                        'relative_subject': subject,
                        'relative_verb': verb
                    }
            
            return {
                'success': False,
                'error': '省略関係詞パターンが見つかりません'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'関係詞復元エラー: {e}'
            }
    
    def _is_object_position(self, text: str, antecedent: str) -> bool:
        """先行詞が関係節内で目的語の位置にあるかチェック"""
        # 簡易的な判定: 関係節内に他の目的語がある場合、先行詞は目的語位置
        pattern = antecedent + r'\s+\w+\s+\w+\s+\w+'  # 先行詞 + 主語 + 動詞 + その他
        if re.search(pattern, text):
            return True
        return False
    
    def _separate_main_and_relative_clauses(self, text: str, doc, restored_relative: str) -> Dict[str, Any]:
        """主節と関係節の分離"""
        try:
            # テキストを主節と関係節に分離
            verbs = [token for token in doc if token.pos_ in ['VERB', 'AUX'] and token.dep_ != 'aux']
            
            if len(verbs) < 2:
                return {
                    'success': False,
                    'error': '主節・関係節の分離に必要な動詞が不足'
                }
            
            # 最初の動詞を関係節、最後の動詞を主節として分類
            relative_verb = verbs[0]
            main_verb = verbs[-1]
            
            # 関係節の構成要素を抽出
            relative_elements = self._extract_relative_elements(doc, relative_verb, restored_relative)
            
            # 主節の構成要素を抽出
            main_elements = self._extract_main_elements(doc, main_verb)
            
            return {
                'success': True,
                'main_elements': main_elements,
                'relative_elements': relative_elements,
                'main_verb': main_verb.text,
                'relative_verb': relative_verb.text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'節分離エラー: {e}'
            }
    
    def _extract_relative_elements(self, doc, relative_verb, restored_relative: str) -> Dict[str, str]:
        """関係節要素の抽出"""
        elements = {}
        
        # 関係節の主語を検出
        for token in doc:
            if token.head == relative_verb and token.dep_ == 'nsubj':
                elements['sub-s'] = token.text
                break
        
        # 関係節の動詞
        elements['sub-v'] = relative_verb.text
        
        # 関係節の目的語・修飾語を検出
        for child in relative_verb.children:
            if child.dep_ == 'dobj':
                # 直接目的語の位置に応じてスロット決定
                if restored_relative.endswith('[that]') or restored_relative.endswith('[which]'):
                    elements['sub-o1'] = child.text
                else:
                    elements['sub-o2'] = restored_relative
                    elements['sub-o1'] = child.text
            elif child.dep_ == 'iobj':
                elements['sub-o1'] = child.text
            elif child.dep_ in ['prep', 'advmod', 'npadvmod']:
                # 修飾語句を完全に抽出（依存語も含める）
                modifier_text = self._extract_complete_phrase(child)
                if 'sub-m2' not in elements:
                    elements['sub-m2'] = modifier_text
                else:
                    elements['sub-m3'] = modifier_text
        
        # 先行詞を適切なスロットに配置
        if 'sub-o1' not in elements:
            elements['sub-o1'] = restored_relative
        elif 'sub-o2' not in elements:
            elements['sub-o2'] = restored_relative
        
        elements['_parent_slot'] = 'S'
        
        return elements
    
    def _extract_complete_phrase(self, token) -> str:
        """トークンとその依存語を含む完全なフレーズを抽出"""
        # 形容詞修飾語やその他の修飾語を含めて完全なフレーズを構築
        phrase_tokens = []
        
        # 修飾語を収集（left children）
        for child in token.lefts:
            if child.dep_ in ['amod', 'det', 'advmod', 'compound']:
                phrase_tokens.append(child.text)
        
        # メインのトークン
        phrase_tokens.append(token.text)
        
        # 後置修飾語を収集（right children）
        for child in token.rights:
            if child.dep_ in ['compound', 'prep', 'advmod']:
                phrase_tokens.append(child.text)
        
        return ' '.join(phrase_tokens) if phrase_tokens else token.text
    
    def _extract_main_elements(self, doc, main_verb) -> Dict[str, str]:
        """主節要素の抽出"""
        elements = {}
        
        # 主節の動詞
        elements['V'] = main_verb.text
        
        # 主語は空（関係節に含まれるため）
        elements['S'] = ''
        
        # 主節の補語・目的語・修飾語を検出
        for child in main_verb.children:
            if child.dep_ in ['attr', 'acomp', 'oprd']:  # oprdを追加
                elements['C1'] = child.text
            elif child.dep_ == 'dobj' and 'O1' not in elements:
                elements['O1'] = child.text
            elif child.dep_ == 'iobj':
                elements['O1'] = child.text
            elif child.dep_ in ['prep', 'advmod', 'npadvmod']:
                if 'M2' not in elements:
                    elements['M2'] = child.text
                else:
                    elements['M3'] = child.text
            elif child.dep_ == 'aux':
                if 'Aux' not in elements:
                    elements['Aux'] = child.text
        
        return elements
    
    def _build_final_result(self, text: str, separation_result: Dict) -> Dict[str, Any]:
        """最終結果の構築"""
        return {
            'success': True,
            'text': text,
            'main_slots': separation_result['main_elements'],
            'sub_slots': separation_result['relative_elements'],
            'metadata': {
                'handler': 'omitted_relative_pronoun',
                'relative_verb': separation_result['relative_verb'],
                'main_verb': separation_result['main_verb'],
                'confidence': 0.85
            }
        }
    
    def _create_error_result(self, text: str, error_message: str) -> Dict[str, Any]:
        """エラー結果の作成"""
        return {
            'success': False,
            'text': text,
            'error': error_message,
            'handler': 'omitted_relative_pronoun'
        }
    
    def _print_dependency_analysis(self, doc):
        """依存関係分析の表示（デバッグ用）"""
        print("🔍 spaCy依存関係分析:")
        for token in doc:
            print(f"   {token.text}: dep={token.dep_}, pos={token.pos_}, tag={token.tag_}")


def test_omitted_relative_pronoun_handler():
    """省略関係詞ハンドラーのテスト"""
    print("🧪 省略関係詞ハンドラー テスト開始")
    print("=" * 50)
    
    handler = OmittedRelativePronounHandler()
    
    test_sentences = [
        "The book I read was interesting.",
        "The man I met yesterday was kind.",
        "The car she drives looks expensive.",
        "The movie we watched last night was amazing.",
        "The gift he bought her was expensive."
    ]
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【テスト {i}】: {sentence}")
        
        # 検出テスト
        can_handle = handler.can_handle(sentence)
        print(f"  検出結果: {can_handle}")
        
        if can_handle:
            # 処理テスト
            result = handler.handle(sentence)
            print(f"  処理結果: {result.get('success', False)}")
            
            if result.get('success'):
                print(f"  主節: {result['main_slots']}")
                print(f"  関係節: {result['sub_slots']}")
            else:
                print(f"  エラー: {result.get('error', 'Unknown error')}")
        
        print("-" * 30)


if __name__ == "__main__":
    test_omitted_relative_pronoun_handler()
