"""
Modal Handler - 助動詞処理専門ハンドラー
Phase 6: ModalHandler実装

設計方針:
- Modal動詞: can, could, will, would, shall, should, may, might, must
- 助動詞: do, does, did, have, has, had
- 半助動詞: be going to, used to, ought to
- 完了形・進行形の複合構造処理
- Rephraseスロット構造完全準拠
- Human Grammar Pattern: spaCy POS解析を活用した助動詞パターン認識
"""

import spacy
from typing import Dict, List, Any, Optional


class ModalHandler:
    """
    助動詞処理専門ハンドラー
    
    責任:
    - 助動詞・法助動詞の検出と分類
    - 複合助動詞（should have, will be等）の処理
    - 疑問文での助動詞倒置処理
    - 完了形・進行形の助動詞処理
    - 否定形助動詞の処理
    
    対象範囲:
    - Modal verbs: can/could/will/would/shall/should/may/might/must
    - Auxiliary verbs: do/does/did/have/has/had/be/am/is/are/was/were
    - Semi-modals: be going to/used to/ought to
    - Complex modals: should have/will be/might have等
    """
    
    def __init__(self, nlp=None):
        """初期化: spaCy POS解析器と助動詞パターンの設定"""
        self.nlp = nlp if nlp else spacy.load('en_core_web_sm')
        
        # 助動詞分類マッピング
        self._initialize_modal_patterns()
        
        # デバッグメッセージ削除済み
    
    def _initialize_modal_patterns(self):
        """助動詞パターンの初期化"""
        
        # 基本法助動詞
        self.modal_verbs = {
            'can', 'could', 'will', 'would', 'shall', 'should', 
            'may', 'might', 'must'
        }
        
        # 助動詞do系
        self.do_auxiliaries = {'do', 'does', 'did', "don't", "doesn't", "didn't"}
        
        # 助動詞have系（完了形）
        self.have_auxiliaries = {'have', 'has', 'had', "haven't", "hasn't", "hadn't"}
        
        # 助動詞be系
        self.be_auxiliaries = {
            'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being',
            "isn't", "aren't", "wasn't", "weren't"
        }
        
        # 複合助動詞パターン
        self.complex_modals = {
            'be going to': r'\b(is|am|are|was|were)\s+going\s+to\b',
            'used to': r'\bused\s+to\b',
            'ought to': r'\bought\s+to\b',
            'have to': r'\b(have|has|had)\s+to\b',
            'will be': r'\bwill\s+be\b',
            'would be': r'\bwould\s+be\b',
            'should be': r'\bshould\s+be\b',
            'could be': r'\bcould\s+be\b',
            'might be': r'\bmight\s+be\b',
            'must be': r'\bmust\s+be\b',
            'should have': r'\bshould\s+have\b',
            'could have': r'\bcould\s+have\b',
            'would have': r'\bwould\s+have\b',
            'might have': r'\bmight\s+have\b',
            'must have': r'\bmust\s+have\b',
            'will have': r'\bwill\s+have\b',
            'have been': r'\b(have|has|had)\s+been\b',
            'will be': r'\bwill\s+be\b'
        }
        
        # デバッグメッセージ削除済み
    
    def detect_modal_structure(self, text: str) -> Dict[str, Any]:
        """
        助動詞構造の検出
        
        Args:
            text: 分析対象の英語文
            
        Returns:
            Dict: 検出された助動詞情報
        """
        doc = self.nlp(text)
        
        result = {
            'has_modal': False,
            'modal_type': None,
            'auxiliary': None,
            'main_verb': None,
            'is_question': False,
            'is_negative': False,
            'structure_type': 'simple'
        }
        
        # 複合助動詞の検出（優先）
        complex_modal = self._detect_complex_modal(text)
        if complex_modal:
            result.update(complex_modal)
            return result
        
        # 基本助動詞の検出
        modal_info = self._detect_basic_modal(doc)
        if modal_info:
            result.update(modal_info)
            return result
        
        return result
    
    def _detect_complex_modal(self, text: str) -> Optional[Dict[str, Any]]:
        """複合助動詞の検出（実際の動詞形を返す）"""
        import re
        
        text_lower = text.lower()
        
        for modal_phrase, pattern in self.complex_modals.items():
            match = re.search(pattern, text_lower)
            if match:
                # 実際にマッチした部分を取得
                actual_auxiliary = match.group(0)
                
                return {
                    'has_modal': True,
                    'modal_type': 'complex',
                    'auxiliary': actual_auxiliary,
                    'structure_type': 'complex_modal'
                }
        
        return None
    
    def _detect_basic_modal(self, doc) -> Optional[Dict[str, Any]]:
        """基本助動詞の検出（否定形対応）"""
        
        for i, token in enumerate(doc):
            token_lower = token.text.lower()
            
            # 法助動詞
            if token_lower in self.modal_verbs:
                return {
                    'has_modal': True,
                    'modal_type': 'modal_verb',
                    'auxiliary': token.text,
                    'structure_type': 'modal'
                }
            
            # do系助動詞（否定形チェック）
            if token_lower in {'do', 'does', 'did'}:
                # 次のトークンが"n't"かチェック
                auxiliary_text = token.text
                is_negative = False
                
                if (i + 1 < len(doc) and 
                    doc[i + 1].text.lower() in {"n't", "not"}):
                    auxiliary_text = token.text + "n't"
                    is_negative = True
                
                return {
                    'has_modal': True,
                    'modal_type': 'do_auxiliary',
                    'auxiliary': auxiliary_text,
                    'is_question': self._is_question_structure(doc),
                    'is_negative': is_negative,
                    'structure_type': 'auxiliary'
                }
            
            # have系助動詞（完了形）
            if token_lower in self.have_auxiliaries and self._is_perfect_tense(doc, token):
                return {
                    'has_modal': True,
                    'modal_type': 'perfect_auxiliary',
                    'auxiliary': token.text,
                    'structure_type': 'perfect'
                }
        
        return None
    
    def _is_question_structure(self, doc) -> bool:
        """疑問文構造の判定"""
        text = doc.text
        return (text.strip().endswith('?') or 
                any(token.text.lower() in ['what', 'where', 'when', 'why', 'how', 'who', 'which'] 
                    for token in doc[:2]))
    
    def _is_perfect_tense(self, doc, have_token) -> bool:
        """完了形の判定（have/has/had + 過去分詞）副詞介在対応"""
        have_idx = have_token.i
        
        # have/has/hadの後のトークンを順番に確認（副詞をスキップ）
        for i in range(have_idx + 1, len(doc)):
            token = doc[i]
            
            # 句読点や接続詞で区切られたら停止
            if token.pos_ in ['PUNCT', 'CCONJ']:
                break
                
            # 副詞はスキップして継続
            if token.pos_ == 'ADV':
                continue
                
            # 過去分詞を発見
            if token.tag_ in ['VBN']:  # past participle
                return True
                
            # beenの場合（完了進行形）
            if token.text.lower() == 'been':
                return True
                
            # 動詞以外の品詞が来たら完了形ではない
            if token.pos_ not in ['VERB', 'AUX']:
                break
        
        return False
    
    def process(self, text: str, collaborators: Optional[Dict] = None) -> Dict[str, Any]:
        """
        助動詞分解処理のメイン関数
        
        Args:
            text: 分析対象の英語文
            collaborators: 他のハンドラーとの協力者（未使用、将来の拡張用）
            
        Returns:
            Dict: Rephraseスロット形式の分解結果
        """
        print(f"🔄 ModalHandler処理開始: '{text}'")
        
        try:
            # 助動詞構造の検出
            modal_info = self.detect_modal_structure(text)
            
            if not modal_info.get('has_modal', False):
                return {
                    'success': False,
                    'reason': 'no_modal_detected',
                    'text': text
                }
            
            # Rephraseスロット分解実行
            result = self._decompose_to_rephrase_slots(text, modal_info)
            
            print(f"✅ ModalHandler処理完了: {result.get('success', False)}")
            return result
            
        except Exception as e:
            print(f"❌ ModalHandler処理エラー: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': text
            }
    
    def _decompose_to_rephrase_slots(self, text: str, modal_info: Dict) -> Dict[str, Any]:
        """Rephraseスロット形式への分解"""
        
        doc = self.nlp(text)
        
        # 基本スロット構造
        main_slots = {}
        sub_slots = {}
        
        # 助動詞の配置
        auxiliary = modal_info.get('auxiliary', '')
        if auxiliary:
            main_slots['Aux'] = auxiliary
        
        # 主語・動詞・目的語等の抽出
        self._extract_basic_elements(doc, main_slots, modal_info)
        
        # 修飾語の処理
        self._extract_modifiers(doc, main_slots, modal_info)
        
        return {
            'success': True,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'modal_info': modal_info,
            'text': text
        }
    
    def _extract_basic_elements(self, doc, main_slots: Dict, modal_info: Dict):
        """基本要素（主語・動詞・目的語・補語）の抽出"""
        
        auxiliary = modal_info.get('auxiliary', '').lower()
        
        for token in doc:
            # 主語の抽出（修飾語を含めた完全な名詞句）
            if token.dep_ == 'nsubj' and 'S' not in main_slots:
                main_slots['S'] = self._extract_noun_phrase(token)
            
            # 動詞の抽出（助動詞以外）
            elif (token.pos_ == 'VERB' and 
                  token.text.lower() not in auxiliary and
                  'V' not in main_slots):
                main_slots['V'] = token.text
            
            # 目的語の抽出（修飾語を含めた完全な名詞句）
            elif token.dep_ == 'dobj' and 'O1' not in main_slots:
                main_slots['O1'] = self._extract_noun_phrase(token)
            
            # 間接目的語（修飾語を含めた完全な名詞句）
            elif token.dep_ == 'iobj' and 'O2' not in main_slots:
                main_slots['O2'] = self._extract_noun_phrase(token)
            
            # 補語の抽出（修飾語を含めた完全な名詞句）
            elif token.dep_ in ['attr', 'acomp'] and 'C1' not in main_slots:
                main_slots['C1'] = self._extract_noun_phrase(token)
    
    def _extract_noun_phrase(self, head_token) -> str:
        """名詞句の抽出（修飾語を含めた完全な句を取得）"""
        phrase_tokens = []
        
        # 主要な名詞から始まる句を語順通りに収集
        for token in head_token.subtree:
            if token.pos_ not in ['PUNCT']:  # 句読点を除く
                phrase_tokens.append((token.i, token.text))
        
        # インデックス順でソートして正しい語順に
        phrase_tokens.sort(key=lambda x: x[0])
        
        return ' '.join([text for _, text in phrase_tokens])
    
    def _extract_modifiers(self, doc, main_slots: Dict, modal_info: Dict):
        """修飾語の抽出（Rephrase副詞配置ルール準拠）"""
        
        modifiers = []
        
        for token in doc:
            # 副詞の検出
            if token.pos_ == 'ADV':
                modifiers.append(token.text)
            
            # 前置詞句の検出
            elif token.dep_ == 'prep':
                prep_phrase = self._extract_prepositional_phrase(token)
                if prep_phrase:
                    modifiers.append(prep_phrase)
        
        # Rephrase副詞配置ルール適用
        self._apply_modifier_placement_rules(modifiers, main_slots)
    
    def _extract_prepositional_phrase(self, prep_token) -> str:
        """前置詞句の抽出（正しい語順で）"""
        phrase_tokens = []
        
        # 前置詞から始まる句を語順通りに収集
        for token in prep_token.subtree:
            if token.pos_ not in ['PUNCT']:  # 句読点を除く
                phrase_tokens.append((token.i, token.text))
        
        # インデックス順でソートして正しい語順に
        phrase_tokens.sort(key=lambda x: x[0])
        
        return ' '.join([text for _, text in phrase_tokens])
    
    def _apply_modifier_placement_rules(self, modifiers: List[str], main_slots: Dict):
        """Rephrase副詞配置ルール適用（個数ベース配置）"""
        
        if not modifiers:
            return
        
        modifier_count = len(modifiers)
        
        if modifier_count == 1:
            # 1個のみ → M2に配置
            main_slots['M2'] = modifiers[0]
        
        elif modifier_count == 2:
            # 2個 → 動詞位置で判定が必要だが、簡略化してM2, M3に配置
            main_slots['M2'] = modifiers[0]
            main_slots['M3'] = modifiers[1]
        
        elif modifier_count >= 3:
            # 3個以上 → M1, M2, M3に順次配置
            main_slots['M1'] = modifiers[0]
            main_slots['M2'] = modifiers[1]
            main_slots['M3'] = modifiers[2]
            # 4個以上は無視（Rephraseスロット制限）
    
    def get_debug_info(self) -> Dict[str, Any]:
        """デバッグ情報の取得"""
        return {
            'handler_name': 'ModalHandler',
            'modal_verbs_count': len(self.modal_verbs),
            'complex_modals_count': len(self.complex_modals),
            'supported_patterns': list(self.modal_verbs) + list(self.complex_modals.keys())
        }


# テスト用の実行部分
if __name__ == "__main__":
    handler = ModalHandler()
    
    # テストケース
    test_cases = [
        "I can swim.",
        "She could speak English fluently.",
        "You will succeed in your career.",
        "He has finished his homework.",
        "They should have called me earlier.",
        "Don't touch that button!"
    ]
    
    print("🧪 ModalHandler テスト実行")
    for test_text in test_cases:
        result = handler.process(test_text)
        print(f"📝 '{test_text}' → {result.get('main_slots', {})}")
