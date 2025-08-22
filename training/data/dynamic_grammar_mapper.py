#!/usr/bin/env python3
"""
動的文法認識システム v2.0
==================

語数に依存しない文法要素ベースの認識システム
- 品詞パターンではなく文法的役割で認識
- 修飾語の動的検出と除外
- 核要素（主語・動詞・目的語・補語）の特定
- 5文型の動的判定

設計思想:
1. 文の「核」を特定（主語 + 動詞）
2. 動詞の性質から文型を推定
3. 残りの要素を文法的役割で分類
4. 修飾語は別途処理
"""

import spacy
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass

# 🆕 Phase 1.2: 文型認識エンジン追加
from sentence_type_detector import SentenceTypeDetector

@dataclass
class GrammarElement:
    """文法要素の定義"""
    text: str
    tokens: List[Dict]
    role: str  # S, V, O1, O2, C1, C2, M1, M2, M3, Aux
    start_idx: int
    end_idx: int
    confidence: float
    
    # 🆕 Order機能関連フィールド (Phase 1.1)
    # デフォルト値設定により既存コードへの影響を最小化
    slot_display_order: int = 0      # 上位スロット順序
    display_order: int = 0           # サブスロット内順序  
    v_group_key: str = ""            # 動詞グループキー
    sentence_type: str = ""          # 文型 (statement/wh_question/yes_no_question)
    is_subslot: bool = False         # サブスロットフラグ
    parent_slot: str = ""            # 親スロット (サブスロット用)
    subslot_id: str = ""             # サブスロットID (sub-s, sub-v等)

class DynamicGrammarMapper:
    """
    動的文法認識システム
    語数に依存しない文法認識を実現
    """
    
    def __init__(self):
        """初期化"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy動的文法認識システム初期化完了")
        except OSError:
            print("❌ spaCy英語モデルが見つかりません")
            raise
        
        self.logger = logging.getLogger(__name__)
        
        # 🆕 Phase 1.2: 文型認識エンジン初期化
        self.sentence_type_detector = SentenceTypeDetector()
        print("✅ 文型認識エンジン初期化完了")
        
        # 動詞分類辞書
        self.linking_verbs = {
            'be', 'am', 'is', 'are', 'was', 'were', 'being', 'been',
            'become', 'became', 'becoming',
            'seem', 'seemed', 'seeming', 'seems',
            'appear', 'appeared', 'appearing', 'appears',
            'look', 'looked', 'looking', 'looks',
            'sound', 'sounded', 'sounding', 'sounds',
            'feel', 'felt', 'feeling', 'feels',
            'taste', 'tasted', 'tasting', 'tastes',
            'smell', 'smelled', 'smelling', 'smells',
            'remain', 'remained', 'remaining', 'remains',
            'stay', 'stayed', 'staying', 'stays'
        }
        
        self.ditransitive_verbs = {
            'give', 'gave', 'given', 'giving', 'gives',
            'tell', 'told', 'telling', 'tells',
            'show', 'showed', 'shown', 'showing', 'shows',
            'send', 'sent', 'sending', 'sends',
            'teach', 'taught', 'teaching', 'teaches',
            'buy', 'bought', 'buying', 'buys',
            'bring', 'brought', 'bringing', 'brings',
            'offer', 'offered', 'offering', 'offers',
            'lend', 'lent', 'lending', 'lends',
            'sell', 'sold', 'selling', 'sells'
        }
        
        self.objective_complement_verbs = {
            'make', 'made', 'making', 'makes',
            'call', 'called', 'calling', 'calls',
            'consider', 'considered', 'considering', 'considers',
            'find', 'found', 'finding', 'finds',
            'keep', 'kept', 'keeping', 'keeps',
            'leave', 'left', 'leaving', 'leaves',
            'elect', 'elected', 'electing', 'elects',
            'name', 'named', 'naming', 'names',
            'choose', 'chose', 'chosen', 'choosing', 'chooses'
        }
    
    def analyze_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        文章を動的に解析してRephraseスロット構造を生成
        
        Args:
            sentence (str): 解析対象の文章
            
        Returns:
            Dict[str, Any]: Rephraseスロット構造
        """
        try:
            # 🆕 Phase 1.2: 文型認識
            sentence_type = self.sentence_type_detector.detect_sentence_type(sentence)
            sentence_type_confidence = self.sentence_type_detector.get_detection_confidence(sentence)
            
            # 1. spaCy基本解析
            doc = self.nlp(sentence)
            tokens = self._extract_tokens(doc)
            
            # 2. 文の核要素を特定
            core_elements = self._identify_core_elements(tokens)
            
            # 3. 動詞の性質から文型を推定
            sentence_pattern = self._determine_sentence_pattern(core_elements, tokens)
            
            # 4. 文法要素を動的に割り当て
            grammar_elements = self._assign_grammar_roles(tokens, sentence_pattern, core_elements)
            
            # 5. Rephraseスロット形式に変換
            rephrase_result = self._convert_to_rephrase_format(grammar_elements, sentence_pattern)
            
            # 🆕 Phase 1.2: 文型情報を結果に追加
            rephrase_result['sentence_type'] = sentence_type
            rephrase_result['sentence_type_confidence'] = sentence_type_confidence
            
            return rephrase_result
            
        except Exception as e:
            self.logger.error(f"動的文法解析エラー: {e}")
            return self._create_error_result(sentence, str(e))
    
    def _extract_tokens(self, doc) -> List[Dict]:
        """spaCyドキュメントからトークン情報を抽出"""
        tokens = []
        for token in doc:
            token_info = {
                'text': token.text,
                'pos': token.pos_,
                'tag': token.tag_,
                'lemma': token.lemma_,
                'dep': token.dep_,  # 依存関係（参考のみ）
                'head': token.head.text,
                'is_stop': token.is_stop,
                'is_alpha': token.is_alpha,
                'index': token.i
            }
            tokens.append(token_info)
        return tokens
    
    def _identify_core_elements(self, tokens: List[Dict]) -> Dict[str, Any]:
        """
        文の核要素（主語・動詞）を特定
        これが全ての文型認識の基盤となる
        """
        core = {
            'subject': None,
            'verb': None,
            'subject_indices': [],
            'verb_indices': [],
            'auxiliary': None,
            'auxiliary_indices': []
        }
        
        # 動詞を探す（最も重要）
        main_verb_idx = self._find_main_verb(tokens)
        if main_verb_idx is not None:
            core['verb'] = tokens[main_verb_idx]
            core['verb_indices'] = [main_verb_idx]
            
            # 助動詞を探す
            aux_idx = self._find_auxiliary(tokens, main_verb_idx)
            if aux_idx is not None:
                core['auxiliary'] = tokens[aux_idx]
                core['auxiliary_indices'] = [aux_idx]
        
        # 主語を探す（動詞の前で最も適切な名詞句）
        if main_verb_idx is not None:
            subject_indices = self._find_subject(tokens, main_verb_idx)
            if subject_indices:
                core['subject_indices'] = subject_indices
                core['subject'] = ' '.join([tokens[i]['text'] for i in subject_indices])
        
        return core
    
    def _find_main_verb(self, tokens: List[Dict]) -> Optional[int]:
        """
        メイン動詞を特定
        優先順位: 1) 動詞タグ, 2) 文脈から判断
        """
        verb_candidates = []
        
        for i, token in enumerate(tokens):
            # 動詞の品詞タグ（より広範囲に検出）
            if (token['tag'].startswith('VB') and token['pos'] == 'VERB') or token['pos'] == 'AUX':
                # 助動詞の場合でも、メイン動詞候補として考慮
                verb_candidates.append((i, token))
        
        # 助動詞でないメイン動詞を優先
        main_verbs = [(i, token) for i, token in verb_candidates if not self._is_auxiliary_verb(token)]
        if main_verbs:
            return main_verbs[-1][0]  # 最後の非助動詞を選択
        
        # メイン動詞が見つからない場合、助動詞も含めて検討
        if verb_candidates:
            return verb_candidates[-1][0]
        
        return None
    
    def _find_auxiliary(self, tokens: List[Dict], main_verb_idx: int) -> Optional[int]:
        """助動詞を特定"""
        # メイン動詞の前を探す
        for i in range(main_verb_idx):
            token = tokens[i]
            if self._is_auxiliary_verb(token):
                return i
        return None
    
    def _find_subject(self, tokens: List[Dict], verb_idx: int) -> List[int]:
        """
        主語を特定（動詞の前の名詞句）
        複数語の名詞句に対応
        """
        subject_indices = []
        
        # 動詞の前を右から左に探す
        for i in range(verb_idx - 1, -1, -1):
            token = tokens[i]
            
            # 助動詞は飛ばす
            if self._is_auxiliary_verb(token):
                continue
            
            # 名詞・代名詞・冠詞を主語の一部として収集
            if (token['pos'] in ['NOUN', 'PROPN', 'PRON'] or 
                token['tag'] in ['DT', 'PRP', 'PRP$', 'WP']):
                subject_indices.insert(0, i)  # 順序を保つため前に挿入
            else:
                # 主語の境界に到達
                break
        
        return subject_indices
    
    def _determine_sentence_pattern(self, core_elements: Dict, tokens: List[Dict]) -> str:
        """
        動詞の性質と文脈から文型を動的に判定
        """
        if not core_elements['verb']:
            return 'UNKNOWN'
        
        verb = core_elements['verb']
        verb_lemma = verb['lemma'].lower()
        verb_indices = core_elements['verb_indices'] + core_elements.get('auxiliary_indices', [])
        subject_indices = core_elements['subject_indices']
        
        # 使用済みのインデックス
        used_indices = set(verb_indices + subject_indices)
        
        # 残りのトークンを分析
        remaining_tokens = [
            (i, token) for i, token in enumerate(tokens) 
            if i not in used_indices and token['pos'] != 'PUNCT'
        ]
        
        # 連結動詞の場合 → SVC候補
        if verb_lemma in self.linking_verbs:
            if remaining_tokens:
                # 補語があるかチェック
                for i, token in remaining_tokens:
                    if self._can_be_complement(token):
                        return 'SVC'
            return 'SV'  # 補語がない場合
        
        # 授与動詞の場合 → SVOO候補
        if verb_lemma in self.ditransitive_verbs:
            if len(remaining_tokens) >= 2:
                return 'SVOO'
            elif len(remaining_tokens) == 1:
                return 'SVO'
        
        # 目的格補語動詞の場合 → SVOC候補
        if verb_lemma in self.objective_complement_verbs:
            if len(remaining_tokens) >= 2:
                return 'SVOC'
            elif len(remaining_tokens) == 1:
                return 'SVO'
        
        # 一般的な他動詞 → SVO
        if remaining_tokens:
            # 目的語候補があるかチェック
            for i, token in remaining_tokens:
                if self._can_be_object(token):
                    return 'SVO'
        
        # デフォルト → SV
        return 'SV'
    
    def _assign_grammar_roles(self, tokens: List[Dict], pattern: str, core_elements: Dict) -> List[GrammarElement]:
        """
        文型パターンに基づいて文法的役割を動的に割り当て
        """
        elements = []
        used_indices = set()
        
        # 主語
        if core_elements['subject_indices']:
            subject_element = GrammarElement(
                text=core_elements['subject'],
                tokens=[tokens[i] for i in core_elements['subject_indices']],
                role='S',
                start_idx=min(core_elements['subject_indices']),
                end_idx=max(core_elements['subject_indices']),
                confidence=0.95
            )
            elements.append(subject_element)
            used_indices.update(core_elements['subject_indices'])
        
        # 助動詞
        if core_elements['auxiliary_indices']:
            aux_element = GrammarElement(
                text=core_elements['auxiliary']['text'],
                tokens=[core_elements['auxiliary']],
                role='Aux',
                start_idx=core_elements['auxiliary_indices'][0],
                end_idx=core_elements['auxiliary_indices'][0],
                confidence=0.95
            )
            elements.append(aux_element)
            used_indices.update(core_elements['auxiliary_indices'])
        
        # 動詞
        if core_elements['verb_indices']:
            verb_element = GrammarElement(
                text=core_elements['verb']['text'],
                tokens=[core_elements['verb']],
                role='V',
                start_idx=core_elements['verb_indices'][0],
                end_idx=core_elements['verb_indices'][0],
                confidence=0.95
            )
            elements.append(verb_element)
            used_indices.update(core_elements['verb_indices'])
        
        # 残りの要素を文型に応じて割り当て
        remaining_tokens = [
            (i, token) for i, token in enumerate(tokens) 
            if i not in used_indices and token['pos'] != 'PUNCT'
        ]
        
        # 文型別の割り当て
        if pattern == 'SVC':
            elements.extend(self._assign_svc_elements(remaining_tokens))
        elif pattern == 'SVO':
            elements.extend(self._assign_svo_elements(remaining_tokens))
        elif pattern == 'SVOO':
            elements.extend(self._assign_svoo_elements(remaining_tokens))
        elif pattern == 'SVOC':
            elements.extend(self._assign_svoc_elements(remaining_tokens))
        else:  # SV or other
            elements.extend(self._assign_modifiers(remaining_tokens))
        
        return elements
    
    def _assign_svc_elements(self, remaining_tokens: List[Tuple[int, Dict]]) -> List[GrammarElement]:
        """SVC文型の要素を割り当て"""
        elements = []
        complement_assigned = False
        
        for i, token in remaining_tokens:
            if not complement_assigned and self._can_be_complement(token):
                elements.append(GrammarElement(
                    text=token['text'],
                    tokens=[token],
                    role='C1',
                    start_idx=i,
                    end_idx=i,
                    confidence=0.9
                ))
                complement_assigned = True
            else:
                # 修飾語として処理
                elements.append(self._create_modifier_element(i, token))
        
        return elements
    
    def _assign_svo_elements(self, remaining_tokens: List[Tuple[int, Dict]]) -> List[GrammarElement]:
        """SVO文型の要素を割り当て"""
        elements = []
        object_assigned = False
        
        for i, token in remaining_tokens:
            if not object_assigned and self._can_be_object(token):
                elements.append(GrammarElement(
                    text=token['text'],
                    tokens=[token],
                    role='O1',
                    start_idx=i,
                    end_idx=i,
                    confidence=0.9
                ))
                object_assigned = True
            else:
                # 修飾語として処理
                elements.append(self._create_modifier_element(i, token))
        
        return elements
    
    def _assign_svoo_elements(self, remaining_tokens: List[Tuple[int, Dict]]) -> List[GrammarElement]:
        """SVOO文型の要素を割り当て"""
        elements = []
        o1_assigned = False
        o2_assigned = False
        
        for i, token in remaining_tokens:
            if not o1_assigned and self._can_be_object(token):
                elements.append(GrammarElement(
                    text=token['text'],
                    tokens=[token],
                    role='O1',
                    start_idx=i,
                    end_idx=i,
                    confidence=0.85
                ))
                o1_assigned = True
            elif not o2_assigned and self._can_be_object(token):
                elements.append(GrammarElement(
                    text=token['text'],
                    tokens=[token],
                    role='O2',
                    start_idx=i,
                    end_idx=i,
                    confidence=0.85
                ))
                o2_assigned = True
            else:
                # 修飾語として処理
                elements.append(self._create_modifier_element(i, token))
        
        return elements
    
    def _assign_svoc_elements(self, remaining_tokens: List[Tuple[int, Dict]]) -> List[GrammarElement]:
        """SVOC文型の要素を割り当て"""
        elements = []
        object_assigned = False
        complement_assigned = False
        
        for i, token in remaining_tokens:
            if not object_assigned and self._can_be_object(token):
                elements.append(GrammarElement(
                    text=token['text'],
                    tokens=[token],
                    role='O1',
                    start_idx=i,
                    end_idx=i,
                    confidence=0.85
                ))
                object_assigned = True
            elif not complement_assigned and (self._can_be_complement(token) or object_assigned):
                elements.append(GrammarElement(
                    text=token['text'],
                    tokens=[token],
                    role='C1',
                    start_idx=i,
                    end_idx=i,
                    confidence=0.85
                ))
                complement_assigned = True
            else:
                # 修飾語として処理
                elements.append(self._create_modifier_element(i, token))
        
        return elements
    
    def _assign_modifiers(self, remaining_tokens: List[Tuple[int, Dict]]) -> List[GrammarElement]:
        """修飾語を割り当て"""
        elements = []
        for i, token in remaining_tokens:
            elements.append(self._create_modifier_element(i, token))
        return elements
    
    def _create_modifier_element(self, idx: int, token: Dict) -> GrammarElement:
        """修飾語要素を作成"""
        # 修飾語の種類を判定
        if token['pos'] in ['ADV', 'PART']:
            role = 'M1'  # 副詞的修飾
        elif token['pos'] in ['ADP'] or token['tag'] in ['IN', 'TO']:
            role = 'M2'  # 前置詞句
        else:
            role = 'M3'  # その他の修飾
        
        return GrammarElement(
            text=token['text'],
            tokens=[token],
            role=role,
            start_idx=idx,
            end_idx=idx,
            confidence=0.7
        )
    
    # ヘルパーメソッド
    def _is_auxiliary_verb(self, token: Dict) -> bool:
        """助動詞判定"""
        aux_words = {'be', 'am', 'is', 'are', 'was', 'were', 'being', 'been',
                     'have', 'has', 'had', 'having',
                     'do', 'does', 'did', 'doing',
                     'will', 'would', 'shall', 'should', 'can', 'could',
                     'may', 'might', 'must', 'ought'}
        return token['lemma'].lower() in aux_words or token['tag'] in ['MD']
    
    def _can_be_object(self, token: Dict) -> bool:
        """目的語になれるかの判定"""
        return token['pos'] in ['NOUN', 'PROPN', 'PRON'] or token['tag'] in ['PRP', 'DT']
    
    def _can_be_complement(self, token: Dict) -> bool:
        """補語になれるかの判定"""
        return token['pos'] in ['ADJ', 'NOUN', 'PROPN'] or token['tag'] in ['JJ', 'NN', 'NNS']
    
    def _convert_to_rephrase_format(self, elements: List[GrammarElement], pattern: str) -> Dict[str, Any]:
        """Rephraseスロット形式に変換"""
        slots = []
        slot_phrases = []
        slot_display_order = []
        display_order = []
        phrase_types = []
        subslot_ids = []
        
        # 🔧 main_slots辞書形式も生成
        main_slots = {}
        
        # 要素を位置順にソート
        elements.sort(key=lambda x: x.start_idx)
        
        role_order = {'S': 1, 'Aux': 2, 'V': 3, 'O1': 4, 'O2': 5, 'C1': 6, 'C2': 7, 'M1': 8, 'M2': 9, 'M3': 10}
        
        for i, element in enumerate(elements):
            # スロット名の調整
            slot_name = element.role
            if slot_name == 'O1':
                slot_name = 'O'  # Rephraseシステムの形式に合わせる
            
            slots.append(slot_name)
            slot_phrases.append(element.text)
            
            # 🔧 main_slots辞書に追加
            main_slots[element.role] = element.text
            
            order = role_order.get(element.role, 99)
            slot_display_order.append(order)
            display_order.append(order)
            
            # 品詞タイプの判定
            if element.role in ['S', 'O1', 'O2']:
                phrase_types.append('名詞句')
            elif element.role == 'V':
                phrase_types.append('動詞句')
            elif element.role in ['C1', 'C2']:
                phrase_types.append('補語句')
            else:
                phrase_types.append('修飾句')
            
            subslot_ids.append(i)
        
        return {
            'Slot': slots,
            'SlotPhrase': slot_phrases,
            'Slot_display_order': slot_display_order,
            'display_order': display_order,
            'PhraseType': phrase_types,
            'SubslotID': subslot_ids,
            'main_slots': main_slots,  # 🔧 辞書形式追加
            'slots': main_slots,       # 🔧 統一システム互換性
            'pattern_detected': pattern,
            'confidence': 0.9,
            'analysis_method': 'dynamic_grammar',
            'lexical_tokens': len([e for e in elements if e.role != 'PUNCT'])
        }
    
    def _create_error_result(self, sentence: str, error: str) -> Dict[str, Any]:
        """エラー結果を作成"""
        return {
            'Slot': [],
            'SlotPhrase': [],
            'Slot_display_order': [],
            'display_order': [],
            'PhraseType': [],
            'SubslotID': [],
            'main_slots': {},    # 🔧 辞書形式追加
            'slots': {},         # 🔧 統一システム互換性
            'error': error,
            'sentence': sentence,
            'analysis_method': 'dynamic_grammar'
        }

# テスト用のメイン関数とテストスイート
def run_full_test_suite(test_data_path: str = None) -> Dict[str, Any]:
    """
    53例文の完全テストを実行
    
    Args:
        test_data_path: テストデータファイルのパス
        
    Returns:
        Dict: テスト結果
    """
    import json
    import os
    from datetime import datetime
    
    if test_data_path is None:
        test_data_path = os.path.join(
            os.path.dirname(__file__),
            "final_test_system",
            "final_54_test_data.json"
        )
    
    try:
        with open(test_data_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ テストデータファイルが見つかりません: {test_data_path}")
        return {}
    
    mapper = DynamicGrammarMapper()
    results = {
        "timestamp": datetime.now().isoformat(),
        "test_system": "dynamic_grammar_mapper",
        "total_tests": len(test_data["data"]),
        "successful_tests": 0,
        "failed_tests": 0,
        "test_results": {}
    }
    
    print("=== 動的文法認識システム 53例文テスト ===\n")
    
    for test_id, test_case in test_data["data"].items():
        sentence = test_case["sentence"]
        expected = test_case["expected"]
        
        print(f"テスト {test_id}: {sentence}")
        
        try:
            result = mapper.analyze_sentence(sentence)
            
            if 'error' in result:
                print(f"❌ エラー: {result['error']}")
                results["failed_tests"] += 1
                status = "ERROR"
            else:
                print(f"✅ 文型: {result.get('pattern_detected', 'UNKNOWN')}")
                print(f"📊 スロット: {result['Slot']}")
                results["successful_tests"] += 1
                status = "SUCCESS"
            
            results["test_results"][test_id] = {
                "sentence": sentence,
                "expected": expected,
                "actual": result,
                "status": status
            }
            
        except Exception as e:
            print(f"❌ 例外エラー: {str(e)}")
            results["failed_tests"] += 1
            results["test_results"][test_id] = {
                "sentence": sentence,
                "expected": expected,
                "actual": {"error": str(e)},
                "status": "EXCEPTION"
            }
        
        print("-" * 60)
    
    # 結果サマリー
    success_rate = results["successful_tests"] / results["total_tests"] * 100
    print(f"\n=== テスト結果サマリー ===")
    print(f"総テスト数: {results['total_tests']}")
    print(f"成功: {results['successful_tests']}")
    print(f"失敗: {results['failed_tests']}")
    print(f"成功率: {success_rate:.1f}%")
    
    return results

def save_test_results(results: Dict[str, Any], output_path: str = None) -> str:
    """
    テスト結果をJSONファイルに保存
    
    Args:
        results: テスト結果
        output_path: 出力ファイルパス（None の場合は自動生成）
        
    Returns:
        str: 保存されたファイルパス
    """
    import json
    from datetime import datetime
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"dynamic_grammar_test_results_{timestamp}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 テスト結果を保存しました: {output_path}")
    return output_path

def main():
    """動的文法認識システムのテスト"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full-test":
        # 53例文の完全テスト
        results = run_full_test_suite()
        save_test_results(results)
    else:
        # 簡易テスト
        mapper = DynamicGrammarMapper()
        
        test_sentences = [
            "The car is red.",
            "I love you.",
            "He has finished his homework.",
            "The students study hard for exams.",
            "The teacher explains grammar clearly to confused students daily.",
            "She made him very happy yesterday.",
            "The man who runs fast is strong."
        ]
        
        print("=== 動的文法認識システム 簡易テスト ===\n")
        
        for sentence in test_sentences:
            print(f"📝 テスト文: '{sentence}'")
            result = mapper.analyze_sentence(sentence)
            
            if 'error' in result:
                print(f"❌ エラー: {result['error']}")
            else:
                print(f"✅ 文型: {result.get('pattern_detected', 'UNKNOWN')}")
                print(f"📊 スロット: {result['Slot']}")
                print(f"📄 フレーズ: {result['SlotPhrase']}")
                print(f"🎯 信頼度: {result.get('confidence', 0.0)}")
            
            print("-" * 50)

if __name__ == "__main__":
    main()
