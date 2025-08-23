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
            
            # 1.5. 関係節構造の検出と処理
            relative_clause_info = self._detect_relative_clause(tokens, sentence)
            sub_slots = {}
            if relative_clause_info['found']:
                self.logger.debug(f"関係節検出: {relative_clause_info['type']} (信頼度: {relative_clause_info['confidence']})")
                tokens, sub_slots = self._process_relative_clause(tokens, relative_clause_info)
            
            # 2. 文の核要素を特定
            core_elements = self._identify_core_elements(tokens)
            
            # 3. 動詞の性質から文型を推定
            sentence_pattern = self._determine_sentence_pattern(core_elements, tokens)
            
            # 4. 文法要素を動的に割り当て（関係節情報も考慮）
            grammar_elements = self._assign_grammar_roles(tokens, sentence_pattern, core_elements, relative_clause_info)
            
            # 5. Rephraseスロット形式に変換
            rephrase_result = self._convert_to_rephrase_format(grammar_elements, sentence_pattern, sub_slots)
            
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
                'dep': token.dep_,  # 依存関係
                'head': token.head.text,
                'head_idx': token.head.i,  # 🆕 依存関係のヘッドインデックス
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
        メイン動詞を特定（人間的文法認識）
        品詞情報と語順のみを使用、依存関係は使わない
        """
        verb_candidates = []
        
        for i, token in enumerate(tokens):
            # 動詞の品詞タグ
            if (token['tag'].startswith('VB') and token['pos'] == 'VERB') or token['pos'] == 'AUX':
                verb_candidates.append((i, token))
        
        if not verb_candidates:
            return None
        
        # 人間的判定：関係節を除外してメイン動詞を特定
        non_relative_verbs = []
        
        for i, token in verb_candidates:
            # 関係代名詞の直後の動詞は関係節内動詞として除外
            is_in_relative_clause = False
            
            # 前の単語を確認
            for j in range(max(0, i-5), i):  # 5語前まで確認
                prev_token = tokens[j]
                if prev_token['text'].lower() in ['who', 'which', 'that', 'whose', 'where', 'when']:
                    # 関係代名詞から動詞までの距離が近い場合、関係節内動詞
                    if i - j <= 4:  # 4語以内なら関係節内
                        is_in_relative_clause = True
                        break
            
            if not is_in_relative_clause:
                non_relative_verbs.append((i, token))
        
        if non_relative_verbs:
            # メイン動詞候補から助動詞でないものを優先
            main_verbs = [(i, token) for i, token in non_relative_verbs if not self._is_auxiliary_verb(token)]
            if main_verbs:
                # 文の後半にあるメイン動詞を優先（関係節の後）
                return main_verbs[-1][0]
            return non_relative_verbs[-1][0]
        
        # 最後の手段として、どの動詞でも選択
        return verb_candidates[-1][0]
    
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
        関係節を含む場合は関係節全体を主語に含める
        """
        subject_indices = []
        
        # 🆕 関係節を含む主語の特定（改良版）
        # トークンに関係節マーカーがある場合の処理
        antecedent_idx = None
        relative_clause_end_idx = None
        
        for i, token in enumerate(tokens):
            if token.get('is_antecedent', False):
                antecedent_idx = i
            if token.get('is_relative_pronoun', False):
                # 関係節の実際の終了位置を使用
                relative_clause_end_idx = token.get('relative_clause_end', verb_idx - 1)
                break
        
        # 関係節を含む主語の場合
        if antecedent_idx is not None and relative_clause_end_idx is not None:
            # 先行詞の冠詞から関係節の最後まで全体を主語とする
            subject_start = antecedent_idx
            # 冠詞があれば含める
            if subject_start > 0 and tokens[subject_start - 1]['pos'] == 'DET':
                subject_start -= 1
            
            subject_indices = list(range(subject_start, relative_clause_end_idx + 1))
            self.logger.debug(f"関係節含む主語検出: indices {subject_indices} -> '{' '.join([tokens[i]['text'] for i in subject_indices])}'")
            return subject_indices
        
        # 通常の主語検出（関係節なし）
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
    
    def _assign_grammar_roles(self, tokens: List[Dict], pattern: str, core_elements: Dict, relative_info: Dict = None) -> List[GrammarElement]:
        """
        文型パターンに基づいて文法的役割を動的に割り当て
        関係節がある場合は該当スロットを空にする
        """
        if relative_info is None:
            relative_info = {'found': False}
            
        elements = []
        used_indices = set()
        
        # 関係節がある場合の処理
        relative_slot_to_empty = None
        if relative_info['found']:
            relative_slot_to_empty = self._determine_relative_slot_position(tokens, relative_info)
        
        # 主語
        if core_elements['subject_indices']:
            # 関係節がS位置にある場合は空にする
            if relative_slot_to_empty == 'S':
                subject_element = GrammarElement(
                    text="",  # 空文字列
                    tokens=[],
                    role='S',
                    start_idx=min(core_elements['subject_indices']),
                    end_idx=max(core_elements['subject_indices']),
                    confidence=0.95
                )
            else:
                # 通常の主語処理
                subject_text = self._clean_relative_clause_from_text(core_elements['subject'], relative_info)
                subject_element = GrammarElement(
                    text=subject_text,
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
        
        # 文型別の割り当て（関係節情報を渡す）
        if pattern == 'SVC':
            elements.extend(self._assign_svc_elements(remaining_tokens, relative_slot_to_empty))
        elif pattern == 'SVO':
            elements.extend(self._assign_svo_elements(remaining_tokens, relative_slot_to_empty))
        elif pattern == 'SVOO':
            elements.extend(self._assign_svoo_elements(remaining_tokens, relative_slot_to_empty))
        elif pattern == 'SVOC':
            elements.extend(self._assign_svoc_elements(remaining_tokens, relative_slot_to_empty))
        else:  # SV or other
            elements.extend(self._assign_modifiers(remaining_tokens))
        
        return elements
    
    def _assign_svc_elements(self, remaining_tokens: List[Tuple[int, Dict]], relative_slot_to_empty: str = None) -> List[GrammarElement]:
        """SVC文型の要素を割り当て - 複合句対応"""
        elements = []
        complement_assigned = False
        used_indices = set()
        
        i = 0
        while i < len(remaining_tokens):
            idx, token = remaining_tokens[i]
            
            # 既に使用済みのインデックスはスキップ
            if idx in used_indices:
                i += 1
                continue
            
            if not complement_assigned and (self._can_be_complement(token) or token['tag'] == 'DT'):
                # C1として複合句を検出（冠詞から始まる場合も含む）
                phrase_indices, phrase_text = self._find_noun_phrase(remaining_tokens, i)
                if phrase_indices:
                    elements.append(GrammarElement(
                        text=phrase_text,
                        tokens=[remaining_tokens[j][1] for j in range(i, i + len(phrase_indices))],
                        role='C1',
                        start_idx=min(phrase_indices),
                        end_idx=max(phrase_indices),
                        confidence=0.9
                    ))
                    used_indices.update(phrase_indices)
                    complement_assigned = True
                    i += len(phrase_indices)
                else:
                    i += 1
            else:
                # 修飾語として処理
                if idx not in used_indices:
                    elements.append(self._create_modifier_element(idx, token))
                i += 1
        
        return elements
    
    def _assign_svo_elements(self, remaining_tokens: List[Tuple[int, Dict]], relative_slot_to_empty: str = None) -> List[GrammarElement]:
        """SVO文型の要素を割り当て（関係節対応）"""
        elements = []
        object_assigned = False
        
        # 関係節により目的語スロットを抽出
        object_text = ""
        if relative_slot_to_empty == 'O1':
            # O1に関係節がある場合は空文字列
            object_text = ""
        else:
            # 通常の目的語処理 - 複数トークンをまとめる
            object_tokens = []
            for i, token in remaining_tokens:
                if self._can_be_object(token) or token['pos'] in ['DET', 'ADJ']:
                    object_tokens.append((i, token))
                elif object_tokens:  # 目的語句が終了
                    break
            
            if object_tokens:
                object_text = ' '.join([token['text'] for _, token in object_tokens])
                used_indices = {i for i, _ in object_tokens}
                
                elements.append(GrammarElement(
                    text=object_text,
                    tokens=[token for _, token in object_tokens],
                    role='O1',
                    start_idx=object_tokens[0][0],
                    end_idx=object_tokens[-1][0],
                    confidence=0.9
                ))
                object_assigned = True
                
                # 残りの要素を修飾語として処理
                for i, token in remaining_tokens:
                    if i not in used_indices:
                        elements.append(self._create_modifier_element(i, token))
            
        # 関係節がある場合は空のO1要素を作成
        if relative_slot_to_empty == 'O1' and not object_assigned:
            elements.append(GrammarElement(
                text="",  # 空文字列
                tokens=[],
                role='O1',
                start_idx=0,
                end_idx=0,
                confidence=0.9
            ))
            
            # 残りを修飾語として処理
            for i, token in remaining_tokens:
                elements.append(self._create_modifier_element(i, token))
        
        return elements
    
    def _assign_svoo_elements(self, remaining_tokens: List[Tuple[int, Dict]], relative_slot_to_empty: str = None) -> List[GrammarElement]:
        """SVOO文型の要素を割り当て - O1/O2分離対応"""
        elements = []
        o1_assigned = False
        o2_assigned = False
        used_indices = set()
        
        i = 0
        while i < len(remaining_tokens):
            idx, token = remaining_tokens[i]
            
            # 既に使用済みのインデックスはスキップ
            if idx in used_indices:
                i += 1
                continue
            
            if not o1_assigned and (self._can_be_object(token) or token['tag'] == 'DT'):
                # SVOO文型のO1は通常単一語（代名詞など）
                if token['pos'] == 'PRON':
                    # 代名詞の場合は単語のみでO1
                    elements.append(GrammarElement(
                        text=token['text'],
                        tokens=[token],
                        role='O1',
                        start_idx=idx,
                        end_idx=idx,
                        confidence=0.9
                    ))
                    used_indices.add(idx)
                    o1_assigned = True
                    i += 1
                else:
                    # 代名詞以外も単語のみでO1として扱う
                    elements.append(GrammarElement(
                        text=token['text'],
                        tokens=[token],
                        role='O1',
                        start_idx=idx,
                        end_idx=idx,
                        confidence=0.85
                    ))
                    used_indices.add(idx)
                    o1_assigned = True
                    i += 1
            elif not o2_assigned and (self._can_be_object(token) or token['tag'] == 'DT'):
                # O2として複合句を検出（冠詞から始まる場合も含む）
                phrase_indices, phrase_text = self._find_noun_phrase(remaining_tokens, i)
                if phrase_indices:
                    elements.append(GrammarElement(
                        text=phrase_text,
                        tokens=[remaining_tokens[j][1] for j in range(i, i + len(phrase_indices))],
                        role='O2',
                        start_idx=min(phrase_indices),
                        end_idx=max(phrase_indices),
                        confidence=0.85
                    ))
                    used_indices.update(phrase_indices)
                    o2_assigned = True
                    i += len(phrase_indices)
                else:
                    i += 1
            else:
                # 修飾語として処理
                if idx not in used_indices:
                    elements.append(self._create_modifier_element(idx, token))
                i += 1
        
        return elements
    
    def _assign_svoc_elements(self, remaining_tokens: List[Tuple[int, Dict]], relative_slot_to_empty: str = None) -> List[GrammarElement]:
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
                    role='C2',  # 🔧 SVOCのCはC2に修正
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
    
    def _find_noun_phrase(self, tokens: List[Tuple[int, Dict]], start_idx: int) -> Tuple[List[int], str]:
        """
        指定位置から複合名詞句を検出
        
        Args:
            tokens: トークンリスト [(index, token), ...]
            start_idx: 検索開始位置
            
        Returns:
            Tuple[List[int], str]: (インデックスリスト, 結合したフレーズ)
        """
        phrase_indices = []
        phrase_tokens = []
        
        # 開始位置から連続する名詞句要素を収集
        for i in range(start_idx, len(tokens)):
            idx, token = tokens[i]
            
            # 名詞句の構成要素かチェック
            if (token['pos'] in ['NOUN', 'PROPN', 'PRON'] or 
                token['tag'] in ['DT', 'CD', 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS']):
                phrase_indices.append(idx)
                phrase_tokens.append(token['text'])
            else:
                # 名詞句の終了
                break
        
        if phrase_indices:
            phrase_text = ' '.join(phrase_tokens)
            return phrase_indices, phrase_text
        else:
            return [], ""

    def _can_be_object(self, token: Dict) -> bool:
        """目的語になれるかの判定"""
        return token['pos'] in ['NOUN', 'PROPN', 'PRON'] or token['tag'] in ['PRP', 'DT']
    
    def _can_be_complement(self, token: Dict) -> bool:
        """補語になれるかの判定"""
        return token['pos'] in ['ADJ', 'NOUN', 'PROPN'] or token['tag'] in ['JJ', 'NN', 'NNS']
    
    def _convert_to_rephrase_format(self, elements: List[GrammarElement], pattern: str, sub_slots: Dict = None) -> Dict[str, Any]:
        """Rephraseスロット形式に変換"""
        if sub_slots is None:
            sub_slots = {}
            
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
            # 統一形式: 常にO1, O2, C1, C2を使用
            
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
            'sub_slots': sub_slots,    # � サブスロット追加
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
            'sub_slots': {},     # 🔧 サブスロット（現在は空）
            'slots': {},         # 🔧 統一システム互換性
            'error': error,
            'sentence': sentence,
            'analysis_method': 'dynamic_grammar'
        }

    # ============================================
    # 関係節処理メソッド群
    # ============================================
    
    def _detect_relative_clause(self, tokens: List[Dict], sentence: str) -> Dict[str, Any]:
        """関係節構造の検出"""
        result = {
            'found': False,
            'type': None,
            'confidence': 0.0,
            'relative_pronoun_idx': None,
            'antecedent_idx': None,
            'clause_start_idx': None,
            'clause_end_idx': None
        }
        
        sentence_lower = sentence.lower()
        
        # 関係代名詞の検出
        relative_pronouns = ['who', 'which', 'that', 'whose', 'where', 'when', 'why', 'how']
        
        for rel_pronoun in relative_pronouns:
            if rel_pronoun in sentence_lower:
                # トークンリストで関係代名詞を探す
                for i, token in enumerate(tokens):
                    if token['text'].lower() == rel_pronoun:
                        result.update({
                            'found': True,
                            'type': f'{rel_pronoun}_clause',
                            'confidence': 0.8,
                            'relative_pronoun_idx': i
                        })
                        
                        # 先行詞を探す（関係代名詞の直前の名詞）
                        if i > 0 and tokens[i-1]['pos'] in ['NOUN', 'PROPN']:
                            result['antecedent_idx'] = i - 1
                            result['confidence'] = 0.9
                        
                        # 関係節の範囲を決定（改良版）
                        result['clause_start_idx'] = i
                        result['clause_end_idx'] = self._find_relative_clause_end(tokens, i, rel_pronoun)
                        
                        self.logger.debug(f"関係節検出: {rel_pronoun} at position {i}, end at {result['clause_end_idx']}")
                        break
                
                if result['found']:
                    break
        
        return result
    
    def _find_relative_clause_end(self, tokens: List[Dict], rel_start_idx: int, rel_type: str) -> int:
        """関係節の終了位置を特定"""
        
        # whose構文の特別処理
        if rel_type == 'whose':
            return self._find_whose_clause_end(tokens, rel_start_idx)
        
        # 一般的な関係節の終了位置（ROOT動詞の直前）
        for i, token in enumerate(tokens):
            if token.get('dep') == 'ROOT' and i > rel_start_idx:
                return i - 1
        
        # ROOTが見つからない場合、文末
        return len(tokens) - 1
    
    def _find_whose_clause_end(self, tokens: List[Dict], whose_idx: int) -> int:
        """whose構文の関係節終了位置を特定（堅牢版）"""
        
        # 基本戦略: whose + [名詞] + [動詞] + [補語/目的語] のパターンマッチング
        
        clause_end = whose_idx
        
        # Step 1: whose の直後の名詞を探す
        possessed_noun_idx = None
        for i in range(whose_idx + 1, min(whose_idx + 3, len(tokens))):
            if tokens[i]['pos'] in ['NOUN', 'PROPN']:
                possessed_noun_idx = i
                break
        
        if possessed_noun_idx is None:
            self.logger.debug(f"whose構文: 所有される名詞が見つからない")
            return whose_idx + 1
        
        # Step 2: その後の動詞を探す（be動詞または一般動詞）
        relcl_verb_idx = None
        for i in range(possessed_noun_idx + 1, min(possessed_noun_idx + 4, len(tokens))):
            if tokens[i]['pos'] in ['VERB', 'AUX']:
                relcl_verb_idx = i
                break
        
        if relcl_verb_idx is None:
            self.logger.debug(f"whose構文: 関係節動詞が見つからない")
            return possessed_noun_idx
        
        # Step 3: 動詞の後の補語/目的語を探す（語順ベース）
        clause_end = relcl_verb_idx
        
        # be動詞の場合：形容詞/名詞の補語を探す
        if tokens[relcl_verb_idx]['lemma'].lower() in ['be', 'am', 'is', 'are', 'was', 'were']:
            for i in range(relcl_verb_idx + 1, min(relcl_verb_idx + 4, len(tokens))):
                token = tokens[i]
                if token['pos'] in ['ADJ', 'NOUN', 'PROPN']:
                    clause_end = i
                elif token['pos'] in ['ADV'] and token['text'].lower() in ['always', 'very', 'quite', 'really']:
                    # 修飾語は飛ばして次を確認
                    continue
                else:
                    break
        
        # 一般動詞の場合：目的語を探す
        else:
            for i in range(relcl_verb_idx + 1, min(relcl_verb_idx + 3, len(tokens))):
                token = tokens[i]
                if token['pos'] in ['NOUN', 'PROPN']:
                    clause_end = i
                else:
                    break
        
        # Step 4: 安全制限 - 明らかにメイン文の動詞を含まないように
        # 位置的にROOT動詞より前で止める
        for i, token in enumerate(tokens):
            if (token['pos'] in ['VERB', 'AUX'] and 
                i > clause_end and 
                token['text'].lower() not in ['is', 'are', 'was', 'were', 'am'] and
                len(token['text']) > 2):  # 短い補助動詞を除く
                
                # この動詞がメイン動詞の可能性が高い場合、その前で止める
                clause_end = min(clause_end, i - 1)
                break
        
        # 最小限の安全確保
        clause_end = max(clause_end, whose_idx + 1)
        
        self.logger.debug(f"whose句終了位置(堅牢版): {clause_end} ('{tokens[clause_end]['text'] if clause_end < len(tokens) else 'EOF'}'), possessed: {possessed_noun_idx}, verb: {relcl_verb_idx}")
        return clause_end
    
    def _process_relative_clause(self, tokens: List[Dict], relative_info: Dict) -> Tuple[List[Dict], Dict]:
        """関係節の処理とサブスロット分解（Rephrase仕様準拠）
        
        正しいRephrase的分解:
        - 関係節を含む上位スロットは空文字列
        - サブスロットに先行詞+関係代名詞、動詞、修飾語を格納
        """
        self.logger.debug(f"関係節処理: {relative_info['type']} (信頼度: {relative_info['confidence']})")
        
        # 関係節の範囲を特定
        rel_pronoun_idx = relative_info.get('relative_pronoun_idx')
        clause_end_idx = relative_info.get('clause_end_idx')
        antecedent_idx = relative_info.get('antecedent_idx')
        
        if rel_pronoun_idx is None or clause_end_idx is None or antecedent_idx is None:
            return tokens, {}
        
        # トークンにマーカーを追加
        tokens[rel_pronoun_idx]['is_relative_pronoun'] = True
        tokens[rel_pronoun_idx]['relative_clause_type'] = relative_info['type']
        tokens[rel_pronoun_idx]['relative_clause_end'] = clause_end_idx
        tokens[antecedent_idx]['is_antecedent'] = True
        
        # Rephrase的サブスロット分解実装
        sub_slots = self._create_rephrase_subslots(tokens, relative_info)
        
        self.logger.debug(f"生成されたサブスロット: {sub_slots}")
        
        return tokens, sub_slots

    def _create_rephrase_subslots(self, tokens: List[Dict], relative_info: Dict) -> Dict:
        """Rephrase仕様に準拠したサブスロット生成
        
        正しい分解例:
        "The man who runs fast" → sub-s: "The man who", sub-v: "runs", sub-m2: "fast"
        "The book which I bought" → sub-o1: "The book which", sub-s: "I", sub-v: "bought"
        """
        rel_pronoun_idx = relative_info['relative_pronoun_idx']
        clause_end_idx = relative_info['clause_end_idx']
        antecedent_idx = relative_info['antecedent_idx']
        
        # 1. 先行詞 + 関係代名詞を取得
        antecedent_text = self._extract_antecedent_phrase(tokens, antecedent_idx, rel_pronoun_idx)
        rel_pronoun_text = tokens[rel_pronoun_idx]['text']
        
        # 2. 関係節内部の要素を分析
        rel_clause_start = rel_pronoun_idx + 1  # 関係代名詞の次から
        rel_clause_tokens = tokens[rel_clause_start:clause_end_idx + 1]
        
        # 3. 関係代名詞の役割を判定
        verb_idx = None
        for i, token in enumerate(rel_clause_tokens):
            if token['tag'].startswith('VB') and token['pos'] == 'VERB':
                verb_idx = i
                break
        
        # 4. Rephrase的サブスロット構造を構築
        sub_slots = {}
        
        if verb_idx is not None:
            rel_pronoun_role = self._determine_relative_pronoun_role(rel_clause_tokens, verb_idx)
            
            if rel_pronoun_role == 'subject':
                # 関係代名詞が主語の場合
                sub_slots['sub-s'] = f"{antecedent_text} {rel_pronoun_text}"
            else:
                # 関係代名詞が目的語の場合
                sub_slots['sub-o1'] = f"{antecedent_text} {rel_pronoun_text}"
        else:
            # 動詞が見つからない場合はデフォルトで主語扱い
            sub_slots['sub-s'] = f"{antecedent_text} {rel_pronoun_text}"
        
        # 5. 関係節内の他の要素を分析
        self._analyze_relative_clause_elements(rel_clause_tokens, sub_slots)
        
        return sub_slots
    
    def _extract_antecedent_phrase(self, tokens: List[Dict], antecedent_idx: int, rel_pronoun_idx: int) -> str:
        """先行詞句を抽出（冠詞・形容詞含む）"""
        # 先行詞の前の修飾語も含めて抽出
        start_idx = antecedent_idx
        
        # 前方の修飾語を探す
        for i in range(antecedent_idx - 1, -1, -1):
            if tokens[i]['pos'] in ['DET', 'ADJ']:  # 冠詞・形容詞
                start_idx = i
            else:
                break
        
        # 先行詞句を構築
        antecedent_phrase = ' '.join([tokens[i]['text'] for i in range(start_idx, rel_pronoun_idx)])
        return antecedent_phrase.strip()
    
    def _analyze_relative_clause_elements(self, rel_tokens: List[Dict], sub_slots: Dict):
        """関係節内の要素をRephrase的に分析"""
        if not rel_tokens:
            return
        
        # 動詞を探す
        verb_idx = None
        for i, token in enumerate(rel_tokens):
            if token['tag'].startswith('VB') and token['pos'] == 'VERB':
                verb_idx = i
                sub_slots['sub-v'] = token['text']
                break
        
        if verb_idx is None:
            return
        
        # 関係代名詞の役割を判定（主語か目的語か）
        rel_pronoun_role = self._determine_relative_pronoun_role(rel_tokens, verb_idx)
        
        # 動詞前の要素を分析（主語）
        pre_verb_tokens = rel_tokens[:verb_idx]
        for token in pre_verb_tokens:
            if token['pos'] in ['NOUN', 'PRON', 'PROPN']:
                # 関係代名詞が目的語の場合、ここに主語がある
                if rel_pronoun_role == 'object':
                    sub_slots['sub-s'] = token['text']
        
        # 動詞後の要素を分析
        post_verb_tokens = rel_tokens[verb_idx + 1:]
        modifier_count = 0
        
        for token in post_verb_tokens:
            if token['pos'] in ['NOUN', 'PRON', 'PROPN']:
                # 目的語
                if 'sub-o1' not in sub_slots:
                    sub_slots['sub-o1'] = token['text']
                elif 'sub-o2' not in sub_slots:
                    sub_slots['sub-o2'] = token['text']
            elif token['pos'] == 'ADJ':
                # 補語
                sub_slots['sub-c1'] = token['text']
            elif token['pos'] == 'ADV':
                # 修飾語 - Rephrase仕様のM2優先ルール
                modifier_count += 1
                if modifier_count == 1:
                    sub_slots['sub-m2'] = token['text']
                elif modifier_count == 2:
                    sub_slots['sub-m3'] = token['text']
    
    def _determine_relative_pronoun_role(self, rel_tokens: List[Dict], verb_idx: int) -> str:
        """関係代名詞が主語か目的語かを判定"""
        # 動詞の前に代名詞・名詞があるかチェック
        pre_verb_tokens = rel_tokens[:verb_idx]
        has_subject_before_verb = any(
            token['pos'] in ['NOUN', 'PRON', 'PROPN'] 
            for token in pre_verb_tokens
        )
        
        if has_subject_before_verb:
            # 動詞前に主語があるなら、関係代名詞は目的語
            return 'object'
        else:
            # 動詞前に主語がないなら、関係代名詞は主語
            return 'subject'

    def _determine_relative_slot_position(self, tokens: List[Dict], relative_info: Dict) -> str:
        """関係節がどのスロット位置にあるかを判定"""
        antecedent_idx = relative_info.get('antecedent_idx')
        if antecedent_idx is None:
            return None
        
        # 簡単な判定：動詞の前なら主語、後なら目的語
        verb_indices = [i for i, token in enumerate(tokens) if token['tag'].startswith('VB') and token['pos'] == 'VERB']
        if not verb_indices:
            return 'O1'  # デフォルト
        
        main_verb_idx = verb_indices[0]  # 最初の動詞をメイン動詞とする
        
        if antecedent_idx < main_verb_idx:
            return 'S'   # 主語位置
        else:
            return 'O1'  # 目的語位置
    
    def _clean_relative_clause_from_text(self, text: str, relative_info: Dict) -> str:
        """テキストから関係節部分を除去"""
        if not relative_info['found']:
            return text
        
        # 簡易実装：関係代名詞以降を削除
        rel_type = relative_info.get('type', '')
        if rel_type in text:
            parts = text.split(rel_type)
            return parts[0].strip()
        
        return text

    def _analyze_relative_clause_structure(self, rel_tokens: List[Dict], clause_type: str) -> Dict:
        """関係節内部の構造を5文型で解析
        
        Args:
            rel_tokens: 関係節のトークンリスト
            clause_type: 関係節の種類（who, which, whose等）
            
        Returns:
            Dict: サブスロット構造
        """
        if not rel_tokens:
            return {}
        
        self.logger.debug(f"関係節構造解析開始: {[t['text'] for t in rel_tokens]}")
        
        # 1. 関係節内の動詞を特定
        verb_idx = self._find_verb_in_relative_clause(rel_tokens)
        if verb_idx is None:
            return {}
        
        # 2. 5文型パターンを適用
        sub_slots = {}
        
        # 関係代名詞をサブ主語として処理
        if clause_type in ['who', 'which', 'that']:
            sub_slots['sub-s'] = rel_tokens[0]['text']  # 関係代名詞
        elif clause_type == 'whose':
            # whose の場合は所有格なので特別処理
            if len(rel_tokens) > 1 and rel_tokens[1]['pos'] == 'NOUN':
                sub_slots['sub-s'] = f"{rel_tokens[0]['text']} {rel_tokens[1]['text']}"
            else:
                sub_slots['sub-s'] = rel_tokens[0]['text']
        
        # 動詞をサブ動詞として処理
        sub_slots['sub-v'] = rel_tokens[verb_idx]['text']
        
        # 3. 動詞の後の要素を解析（目的語、補語、修飾語）
        self._analyze_post_verb_elements_in_relative(rel_tokens, verb_idx, sub_slots)
        
        return sub_slots
    
    def _find_verb_in_relative_clause(self, rel_tokens: List[Dict]) -> Optional[int]:
        """関係節内の動詞を特定
        
        5文型ハンドラーの動詞検出技術を適用
        """
        for i, token in enumerate(rel_tokens):
            if token['tag'].startswith('VB') and token['pos'] == 'VERB':
                return i
        return None
    
    def _analyze_post_verb_elements_in_relative(self, rel_tokens: List[Dict], verb_idx: int, sub_slots: Dict):
        """関係節内の動詞後要素を解析
        
        5文型パターン認識技術を適用
        """
        if verb_idx >= len(rel_tokens) - 1:
            return
        
        post_verb_tokens = rel_tokens[verb_idx + 1:]
        
        # 目的語、補語、修飾語を順次解析
        processed_positions = set()
        
        for i, token in enumerate(post_verb_tokens):
            if i in processed_positions:
                continue
                
            if token['pos'] in ['NOUN', 'PRON', 'PROPN']:
                # 名詞類 → 目的語として処理
                if 'sub-o1' not in sub_slots:
                    sub_slots['sub-o1'] = token['text']
                elif 'sub-o2' not in sub_slots:
                    sub_slots['sub-o2'] = token['text']
                processed_positions.add(i)
            elif token['pos'] == 'ADJ':
                # 形容詞 → 補語として処理
                sub_slots['sub-c1'] = token['text']
                processed_positions.add(i)
            elif token['pos'] == 'ADV':
                # 副詞 → 修飾語として処理
                if 'sub-m' not in sub_slots:
                    sub_slots['sub-m'] = token['text']
                else:
                    sub_slots['sub-m'] += f" {token['text']}"
                processed_positions.add(i)
        
        # 連続する要素をまとめる（簡素化版）
        self._consolidate_relative_clause_elements_simple(rel_tokens, verb_idx, sub_slots)

    def _consolidate_relative_clause_elements_simple(self, rel_tokens: List[Dict], verb_idx: int, sub_slots: Dict):
        """関係節内の要素を統合（簡素版）"""
        # 現在は基本的な重複除去のみ
        if 'sub-m' in sub_slots:
            # 重複した修飾語を除去
            m_words = sub_slots['sub-m'].split()
            unique_words = []
            for word in m_words:
                if word not in unique_words:
                    unique_words.append(word)
            sub_slots['sub-m'] = ' '.join(unique_words)

    def _consolidate_relative_clause_elements(self, rel_tokens: List[Dict], verb_idx: int, sub_slots: Dict):
        """関係節内の要素を統合
        
        連続する名詞句や修飾語句を一つにまとめる
        """
        if verb_idx >= len(rel_tokens) - 1:
            return
        
        post_verb_tokens = rel_tokens[verb_idx + 1:]
        current_phrase = []
        current_type = None
        
        for token in post_verb_tokens:
            if token['pos'] in ['NOUN', 'PRON', 'PROPN', 'DET', 'ADJ']:
                if current_type == 'noun_phrase':
                    current_phrase.append(token['text'])
                else:
                    # 新しい名詞句の開始
                    if current_phrase and current_type:
                        self._assign_phrase_to_subslot(current_phrase, current_type, sub_slots)
                    current_phrase = [token['text']]
                    current_type = 'noun_phrase'
            elif token['pos'] in ['ADV', 'ADP']:
                if current_type == 'adverbial_phrase':
                    current_phrase.append(token['text'])
                else:
                    # 新しい副詞句の開始
                    if current_phrase and current_type:
                        self._assign_phrase_to_subslot(current_phrase, current_type, sub_slots)
                    current_phrase = [token['text']]
                    current_type = 'adverbial_phrase'
            else:
                # その他の品詞で句が終了
                if current_phrase and current_type:
                    self._assign_phrase_to_subslot(current_phrase, current_type, sub_slots)
                current_phrase = []
                current_type = None
        
        # 最後の句を処理
        if current_phrase and current_type:
            self._assign_phrase_to_subslot(current_phrase, current_type, sub_slots)
    
    def _assign_phrase_to_subslot(self, phrase: List[str], phrase_type: str, sub_slots: Dict):
        """句をサブスロットに割り当て"""
        phrase_text = ' '.join(phrase)
        
        if phrase_type == 'noun_phrase':
            if 'sub-o1' not in sub_slots:
                sub_slots['sub-o1'] = phrase_text
            elif 'sub-o2' not in sub_slots:
                sub_slots['sub-o2'] = phrase_text
            else:
                # 補語として処理
                sub_slots['sub-c1'] = phrase_text
        elif phrase_type == 'adverbial_phrase':
            if 'sub-m' not in sub_slots:
                sub_slots['sub-m'] = phrase_text
            else:
                sub_slots['sub-m'] += f" {phrase_text}"

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
