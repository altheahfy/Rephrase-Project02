"""
Enhanced Adverb Precision System - Phase A Implementation
副詞配置精密化システム - フェーズA実装

修正すべき問題:
1. M1/M2/M3の動詞位置ベース分類が不正確
2. 複合副詞句（"very carefully"）の分離失敗
3. 前置詞句（"to school"）の目的語誤認識
4. 主語認識エラー（"She" → O1）

アプローチ:
1. spaCy依存構造解析でSV関係を正確に特定
2. 動詞位置ベースの正確なM1/M2/M3配置
3. 複合副詞句の統合処理
4. 前置詞句のM2配置優先
"""

import spacy
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass

@dataclass
class AdverbElement:
    """副詞要素の構造化表現"""
    text: str
    tokens: List
    start_idx: int
    end_idx: int
    adverb_type: str  # 'simple', 'compound', 'prepositional'
    position_relative_to_verb: str  # 'pre', 'post'
    
class EnhancedAdverbSystem:
    """副詞配置精密化システム"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # spaCy NLPモデルの初期化
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.error("spaCy英語モデルが見つかりません。`python -m spacy download en_core_web_sm`を実行してください。")
            self.nlp = None
            
        # 副詞句パターン辞書
        self.compound_adverb_patterns = {
            'very carefully', 'quite slowly', 'really fast', 'extremely well',
            'so quickly', 'too late', 'pretty good', 'somewhat difficult'
        }
        
        # 前置詞句の方向指示語
        self.directional_prepositions = {
            'to', 'from', 'into', 'onto', 'towards', 'through',
            'across', 'over', 'under', 'around', 'along', 'at', 'in', 'on'
        }
        
    def analyze_adverb_precision(self, sentence: str, current_result: Dict) -> Dict[str, str]:
        """
        副詞配置精密分析メイン関数
        
        Args:
            sentence: 分析対象文
            current_result: 既存の文法解析結果
            
        Returns:
            Dict: M1/M2/M3の正確な配置結果
        """
        if not self.nlp:
            return {}
            
        try:
            # spaCy解析実行
            doc = self.nlp(sentence)
            
            # Phase 1: 動詞位置の正確な特定
            main_verb_info = self._identify_main_verb_precise(doc)
            if not main_verb_info:
                self.logger.warning(f"メイン動詞が特定できません: {sentence}")
                return {}
                
            # Phase 2: 副詞要素の抽出と分類
            adverb_elements = self._extract_adverb_elements(doc, main_verb_info)
            
            # Phase 3: M1/M2/M3への正確な配置
            placement_result = self._assign_m1_m2_m3_precise(adverb_elements, main_verb_info)
            
            self.logger.info(f"副詞精密分析結果: {placement_result}")
            return placement_result
            
        except Exception as e:
            self.logger.error(f"副詞精密分析エラー: {e}")
            return {}
    
    def _identify_main_verb_precise(self, doc) -> Optional[Dict]:
        """
        メイン動詞の正確な特定（spaCy依存構造解析使用）
        
        Returns:
            Dict: {'token': spacy.Token, 'index': int, 'lemma': str}
        """
        # ROOTを探す（文の主動詞）
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                return {
                    'token': token,
                    'index': token.i,
                    'lemma': token.lemma_,
                    'text': token.text
                }
        
        # ROOTが見つからない場合は最初のVERBを使用
        for token in doc:
            if token.pos_ == "VERB":
                return {
                    'token': token,
                    'index': token.i,
                    'lemma': token.lemma_,
                    'text': token.text
                }
        
        return None
    
    def _extract_adverb_elements(self, doc, main_verb_info: Dict) -> List[AdverbElement]:
        """
        副詞要素の抽出と分類（複合副詞句対応）
        
        Returns:
            List[AdverbElement]: 構造化された副詞要素リスト
        """
        adverb_elements = []
        processed_indices = set()
        
        main_verb_idx = main_verb_info['index']
        
        for i, token in enumerate(doc):
            if i in processed_indices:
                continue
                
            # 1. 単純副詞の検出
            if token.pos_ == "ADV":
                # 複合副詞句かチェック
                compound_element = self._check_compound_adverb(doc, i)
                if compound_element:
                    adverb_elements.append(compound_element)
                    processed_indices.update(range(compound_element.start_idx, compound_element.end_idx + 1))
                else:
                    # 単純副詞
                    adverb_elements.append(AdverbElement(
                        text=token.text,
                        tokens=[token],
                        start_idx=i,
                        end_idx=i,
                        adverb_type='simple',
                        position_relative_to_verb='pre' if i < main_verb_idx else 'post'
                    ))
                    processed_indices.add(i)
            
            # 🔧 2. 時間副詞の検出（"Yesterday", "Today", "Tomorrow"等）
            elif token.text.lower() in ['yesterday', 'today', 'tomorrow', 'now', 'then', 'soon', 'always', 'never', 'often', 'sometimes']:
                adverb_elements.append(AdverbElement(
                    text=token.text,
                    tokens=[token],
                    start_idx=i,
                    end_idx=i,
                    adverb_type='temporal',
                    position_relative_to_verb='pre' if i < main_verb_idx else 'post'
                ))
                processed_indices.add(i)
            
            # 3. 前置詞句の検出（方向指示）
            elif token.pos_ == "ADP" and token.text.lower() in self.directional_prepositions:
                prep_phrase = self._extract_prepositional_phrase(doc, i)
                if prep_phrase:
                    adverb_elements.append(prep_phrase)
                    processed_indices.update(range(prep_phrase.start_idx, prep_phrase.end_idx + 1))
        
        return adverb_elements
    
    def _check_compound_adverb(self, doc, start_idx: int) -> Optional[AdverbElement]:
        """
        複合副詞句の検出（"very carefully"等）
        
        Args:
            doc: spaCy Doc
            start_idx: 開始位置
            
        Returns:
            AdverbElement or None
        """
        if start_idx >= len(doc) - 1:
            return None
            
        token = doc[start_idx]
        
        # パターン1: 強調副詞 + 程度副詞 ("very carefully")
        if (token.text.lower() in ['very', 'quite', 'really', 'extremely', 'so', 'too'] and
            start_idx + 1 < len(doc) and doc[start_idx + 1].pos_ == "ADV"):
            
            next_token = doc[start_idx + 1]
            compound_text = f"{token.text} {next_token.text}"
            
            return AdverbElement(
                text=compound_text,
                tokens=[token, next_token],
                start_idx=start_idx,
                end_idx=start_idx + 1,
                adverb_type='compound',
                position_relative_to_verb='pre' if start_idx < self._get_main_verb_index(doc) else 'post'
            )
        
        return None
    
    def _extract_prepositional_phrase(self, doc, prep_idx: int) -> Optional[AdverbElement]:
        """
        前置詞句の抽出（"to school"等）
        
        Args:
            doc: spaCy Doc
            prep_idx: 前置詞の位置
            
        Returns:
            AdverbElement or None
        """
        if prep_idx >= len(doc) - 1:
            return None
            
        prep_token = doc[prep_idx]
        phrase_tokens = [prep_token]
        phrase_text = prep_token.text
        
        # 前置詞の直後の名詞句を探す
        for i in range(prep_idx + 1, min(prep_idx + 3, len(doc))):
            next_token = doc[i]
            if next_token.pos_ in ["NOUN", "PROPN", "PRON"] or next_token.tag_ in ["DT"]:
                phrase_tokens.append(next_token)
                phrase_text += f" {next_token.text}"
            else:
                break
        
        if len(phrase_tokens) > 1:  # 前置詞 + 最低1語
            main_verb_idx = self._get_main_verb_index(doc)
            
            return AdverbElement(
                text=phrase_text,
                tokens=phrase_tokens,
                start_idx=prep_idx,
                end_idx=prep_idx + len(phrase_tokens) - 1,
                adverb_type='prepositional',
                position_relative_to_verb='pre' if prep_idx < main_verb_idx else 'post'
            )
        
        return None
    
    def _get_main_verb_index(self, doc) -> int:
        """メイン動詞のインデックス取得（ヘルパー）"""
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                return token.i
        return len(doc)  # 見つからない場合は文末
    
    def _assign_m1_m2_m3_precise(self, adverb_elements: List[AdverbElement], main_verb_info: Dict) -> Dict[str, str]:
        """
        M1/M2/M3への精密配置（Rephraseルール準拠）
        
        修正されたRephraseルール（テストケース期待値ベース）:
        - 動詞前副詞 → M1
        - 動詞直後副詞/前置詞句 → M2  
        - 文末副詞/時間表現 → M3
        - 1個: 動詞前→M1, 動詞後→M2
        - 2個: 動詞前1個→M1, 動詞後1個→M2
        - 3個以上: M1(動詞前), M2(動詞直後), M3(文末)
        
        Args:
            adverb_elements: 構造化副詞要素リスト
            main_verb_info: メイン動詞情報
            
        Returns:
            Dict: M1/M2/M3の配置結果
        """
        if not adverb_elements:
            return {}
        
        # 位置順にソート
        adverb_elements.sort(key=lambda x: x.start_idx)
        
        # 動詞前後の分類
        main_verb_idx = main_verb_info['index']
        pre_verb_adverbs = [adv for adv in adverb_elements if adv.position_relative_to_verb == 'pre']
        post_verb_adverbs = [adv for adv in adverb_elements if adv.position_relative_to_verb == 'post']
        
        self.logger.debug(f"動詞前副詞: {[adv.text for adv in pre_verb_adverbs]}")
        self.logger.debug(f"動詞後副詞: {[adv.text for adv in post_verb_adverbs]}")
        
        result = {}
        
        # 🔧 修正されたRephraseルール（テストケース期待値ベース）
        
        # 動詞前副詞 → M1配置（優先）
        if pre_verb_adverbs:
            result['M1'] = pre_verb_adverbs[0].text
            # 動詞前に複数ある場合は最初の1つのみM1
        
        # 動詞後副詞 → M2, M3配置
        if post_verb_adverbs:
            if len(post_verb_adverbs) == 1:
                # 動詞後1個 → M2
                result['M2'] = post_verb_adverbs[0].text
            elif len(post_verb_adverbs) >= 2:
                # 動詞後2個以上 → M2(最初), M3(最後)
                result['M2'] = post_verb_adverbs[0].text
                result['M3'] = post_verb_adverbs[-1].text  # 最後の要素
        
        # 動詞前副詞がなく、動詞後副詞のみの場合
        if not pre_verb_adverbs and post_verb_adverbs:
            if len(post_verb_adverbs) == 1:
                # 動詞後1個のみ → M2
                result['M2'] = post_verb_adverbs[0].text
            elif len(post_verb_adverbs) >= 2:
                # 動詞後2個以上 → M2, M3
                result['M2'] = post_verb_adverbs[0].text
                result['M3'] = post_verb_adverbs[1].text
        
        return result
    
    def validate_accuracy(self, test_cases: List[Dict]) -> float:
        """
        テストケースでの精度検証
        
        Args:
            test_cases: [{'sentence': str, 'expected': Dict}, ...]
            
        Returns:
            float: 精度（0.0-1.0）
        """
        if not test_cases:
            return 0.0
            
        correct_count = 0
        
        for test_case in test_cases:
            sentence = test_case['sentence']
            expected = test_case['expected']
            
            # 精密分析実行
            result = self.analyze_adverb_precision(sentence, {})
            
            # 期待値と比較
            is_correct = True
            for slot in ['M1', 'M2', 'M3']:
                expected_value = expected.get(slot, '')
                actual_value = result.get(slot, '')
                
                if expected_value != actual_value:
                    is_correct = False
                    self.logger.debug(f"不一致: {sentence} - {slot}: 期待='{expected_value}', 実際='{actual_value}'")
                    break
            
            if is_correct:
                correct_count += 1
                self.logger.debug(f"✅ 正解: {sentence}")
            else:
                self.logger.debug(f"❌ 不正解: {sentence}")
        
        accuracy = correct_count / len(test_cases)
        self.logger.info(f"副詞配置精度: {accuracy:.1%} ({correct_count}/{len(test_cases)})")
        
        return accuracy

# 使用例とテスト関数
def test_enhanced_adverb_system():
    """Enhanced Adverb Systemのテスト"""
    
    system = EnhancedAdverbSystem()
    
    # テストケース（test_adverb_precision.pyの期待値に基づく修正版）
    test_cases = [
        {
            'sentence': "She quickly runs to school.",
            'expected': {'M1': 'quickly', 'M2': 'to school'}  # テストケース11の期待値
        },
        {
            'sentence': "He carefully opened the door.",
            'expected': {'M1': 'carefully'}  # テストケース12の期待値
        },
        {
            'sentence': "They very carefully moved the furniture.",
            'expected': {'M1': 'very carefully'}  # 複合副詞のテスト
        },
        {
            'sentence': "Yesterday she spoke softly to him.",
            'expected': {'M1': 'Yesterday', 'M2': 'softly', 'M3': 'to him'}  # 3個副詞テスト
        }
    ]
    
    print("=== Enhanced Adverb Precision System Test ===")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['sentence']}")
        result = system.analyze_adverb_precision(test_case['sentence'], {})
        expected = test_case['expected']
        
        print(f"期待値: {expected}")
        print(f"結果:   {result}")
        
        # 一致チェック
        matches = all(result.get(k, '') == v for k, v in expected.items())
        print(f"判定:   {'✅ 正解' if matches else '❌ 不正解'}")
    
    # 全体精度計算
    accuracy = system.validate_accuracy(test_cases)
    print(f"\n=== 総合精度: {accuracy:.1%} ===")

if __name__ == "__main__":
    test_enhanced_adverb_system()
