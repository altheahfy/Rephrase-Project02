"""
Phase A2: 真のBasicFivePatternHandler実装
レガシー分解機能をハンドラー内に完全移行

作成日: 2025年8月25日
目的: Central Controllerから分解機能を移行し、純粋中央管理を実現
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
from collections import namedtuple

# GrammarElement定義（既存コードとの互換性）
GrammarElement = namedtuple('GrammarElement', [
    'text', 'tokens', 'role', 'start_idx', 'end_idx', 'confidence'
])

class BasicFivePatternHandler:
    """
    🎯 拡張版基本5文型ハンドラー
    
    Phase A2実装:
    ├─ レガシー分解機能の完全統合
    ├─ 主語・動詞・目的語・補語の精密特定
    ├─ 文型パターン自動判定  
    └─ スロット配置の完全自動化
    
    移行対象機能:
    ├─ _identify_core_elements() → identify_core_elements_enhanced()
    ├─ _determine_sentence_pattern() → determine_pattern_enhanced()
    └─ _assign_grammar_roles() → assign_roles_enhanced()
    """
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        
        # レガシー機能移行: 語彙リスト
        self.linking_verbs = {
            'be', 'is', 'am', 'are', 'was', 'were', 'been', 'being',
            'become', 'became', 'get', 'got', 'seem', 'seemed', 'appear', 'appeared',
            'look', 'looked', 'sound', 'sounded', 'feel', 'felt', 'taste', 'tasted',
            'smell', 'smelled', 'remain', 'remained', 'stay', 'stayed', 'keep', 'kept',
            'turn', 'turned', 'grow', 'grew', 'prove', 'proved'
        }
        
        self.ditransitive_verbs = {
            'give', 'gave', 'given', 'tell', 'told', 'show', 'showed', 'shown',
            'send', 'sent', 'bring', 'brought', 'teach', 'taught', 'offer', 'offered',
            'sell', 'sold', 'buy', 'bought', 'lend', 'lent', 'hand', 'handed',
            'pass', 'passed', 'throw', 'threw', 'thrown'
        }
        
        # 同形語処理（既存ロジック継承）
        self.ambiguous_words = {
            'works': ['NOUN', 'VERB'],   # work複数形 vs work三人称単数
            'runs': ['NOUN', 'VERB'],    # run複数形 vs run三人称単数
            'calls': ['NOUN', 'VERB'],   # call複数形 vs call三人称単数
            'studies': ['NOUN', 'VERB'], # study複数形 vs study三人称単数
            'rides': ['NOUN', 'VERB'],   # ride複数形 vs ride三人称単数
            'sits': ['NOUN', 'VERB']     # sit複数形 vs sit三人称単数
        }
    
    def handle(self, tokens: List[Dict], context: Dict) -> Dict[str, Any]:
        """
        🎯 メインハンドラー処理
        
        統合されたレガシー機能を順次実行:
        Step 1: 基本要素特定
        Step 2: 文型判定
        Step 3: 役割割り当て
        Step 4: 結果生成
        """
        try:
            # Step 1: 基本要素特定（旧_identify_core_elements統合）
            core_elements = self.identify_core_elements_enhanced(tokens)
            
            # Step 2: 文型判定（旧_determine_sentence_pattern統合）
            pattern = self.determine_pattern_enhanced(tokens, core_elements)
            
            # Step 3: 役割割り当て（旧_assign_grammar_roles統合）
            grammar_elements = self.assign_roles_enhanced(tokens, pattern, core_elements)
            
            # Step 4: 結果生成
            result = self._convert_to_handler_result(grammar_elements, pattern, tokens)
            
            return result
            
        except Exception as e:
            self.logger.error(f"BasicFivePatternHandler error: {e}")
            return {'success': False, 'error': str(e)}
    
    def identify_core_elements_enhanced(self, tokens: List[Dict]) -> Dict[str, Any]:
        """
        🎯 レガシー機能統合版: 基本要素特定
        
        旧_identify_core_elements()ロジックを完全移行・強化
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
        main_verb_idx = self._find_main_verb_enhanced(tokens)
        if main_verb_idx is not None:
            core['verb'] = tokens[main_verb_idx]
            core['verb_indices'] = [main_verb_idx]
            
            # 助動詞を探す
            aux_idx = self._find_auxiliary_enhanced(tokens, main_verb_idx)
            if aux_idx is not None:
                core['auxiliary'] = tokens[aux_idx]
                core['auxiliary_indices'] = [aux_idx]
        
        # 主語を探す（動詞の前で最も適切な名詞句）
        if main_verb_idx is not None:
            subject_indices = self._find_subject_enhanced(tokens, main_verb_idx)
            if subject_indices:
                core['subject_indices'] = subject_indices
                core['subject'] = ' '.join([tokens[i]['text'] for i in subject_indices])
        
        return core
    
    def determine_pattern_enhanced(self, tokens: List[Dict], core_elements: Dict) -> str:
        """
        🎯 レガシー機能統合版: 文型パターン判定
        
        旧_determine_sentence_pattern()ロジックを完全移行・強化
        """
        if not core_elements['verb']:
            return 'UNKNOWN'
        
        verb = core_elements['verb']
        verb_lemma = verb['lemma'].lower()
        verb_indices = core_elements['verb_indices'] + core_elements.get('auxiliary_indices', [])
        subject_indices = core_elements['subject_indices']
        
        # 自動詞リスト（レガシー継承）
        intransitive_verbs = {
            'arrive', 'arrived', 'come', 'came', 'go', 'went', 'sleep', 'slept',
            'walk', 'walked', 'run', 'ran', 'happen', 'happened', 'occur', 'occurred',
            'exist', 'existed', 'fall', 'fell', 'rise', 'rose', 'sit', 'sat',
            'stand', 'stood', 'lie', 'lay', 'work', 'worked', 'laugh', 'laughed',
            'cry', 'cried', 'smile', 'smiled', 'die', 'died'
        }
        
        # 使用済みのインデックス
        used_indices = set(verb_indices + subject_indices)
        
        # 残りのトークンを分析
        remaining_tokens = [
            (i, token) for i, token in enumerate(tokens) 
            if i not in used_indices and token['pos'] != 'PUNCT'
        ]
        
        # 自動詞の場合は強制的にSVパターン
        if verb_lemma in intransitive_verbs or verb['text'].lower() in intransitive_verbs:
            return 'SV'
        
        # 連結動詞の場合 → SVC候補
        if verb_lemma in self.linking_verbs:
            if remaining_tokens:
                # 補語があるかチェック
                for i, token in remaining_tokens:
                    if self._can_be_complement_enhanced(token):
                        return 'SVC'
            return 'SV'  # 補語がない場合
        
        # 授与動詞の場合 → SVOO候補
        if verb_lemma in self.ditransitive_verbs:
            if len(remaining_tokens) >= 2:
                return 'SVOO'
            elif len(remaining_tokens) == 1:
                return 'SVO'
        
        # その他の場合：残りトークン数で判定
        if len(remaining_tokens) >= 2:
            return 'SVOC'  # SVOC候補
        elif len(remaining_tokens) == 1:
            return 'SVO'   # SVO候補
        else:
            return 'SV'    # SV
    
    def assign_roles_enhanced(self, tokens: List[Dict], pattern: str, core_elements: Dict) -> List[GrammarElement]:
        """
        🎯 レガシー機能統合版: 文法的役割割り当て
        
        旧_assign_grammar_roles()ロジックを完全移行・強化
        """
        elements = []
        used_indices = set()
        
        # 主語処理
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
        
        # 助動詞処理
        if core_elements['auxiliary_indices']:
            aux_element = GrammarElement(
                text=core_elements['auxiliary']['text'],
                tokens=[core_elements['auxiliary']],
                role='Aux',
                start_idx=core_elements['auxiliary_indices'][0],
                end_idx=core_elements['auxiliary_indices'][0],
                confidence=0.9
            )
            elements.append(aux_element)
            used_indices.update(core_elements['auxiliary_indices'])
        
        # 動詞処理
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
        
        # パターン別処理
        remaining_tokens = [
            (i, token) for i, token in enumerate(tokens)
            if i not in used_indices and token['pos'] != 'PUNCT'
        ]
        
        if pattern == 'SVO' and len(remaining_tokens) >= 1:
            # 目的語
            obj_idx, obj_token = remaining_tokens[0]
            obj_element = GrammarElement(
                text=obj_token['text'],
                tokens=[obj_token],
                role='O1',
                start_idx=obj_idx,
                end_idx=obj_idx,
                confidence=0.8
            )
            elements.append(obj_element)
        
        elif pattern == 'SVC' and len(remaining_tokens) >= 1:
            # 補語
            comp_idx, comp_token = remaining_tokens[0]
            comp_element = GrammarElement(
                text=comp_token['text'],
                tokens=[comp_token],
                role='C1',
                start_idx=comp_idx,
                end_idx=comp_idx,
                confidence=0.8
            )
            elements.append(comp_element)
        
        elif pattern == 'SVOO' and len(remaining_tokens) >= 2:
            # 間接目的語
            obj1_idx, obj1_token = remaining_tokens[0]
            obj1_element = GrammarElement(
                text=obj1_token['text'],
                tokens=[obj1_token],
                role='O1',
                start_idx=obj1_idx,
                end_idx=obj1_idx,
                confidence=0.8
            )
            elements.append(obj1_element)
            
            # 直接目的語
            obj2_idx, obj2_token = remaining_tokens[1]
            obj2_element = GrammarElement(
                text=obj2_token['text'],
                tokens=[obj2_token],
                role='O2',
                start_idx=obj2_idx,
                end_idx=obj2_idx,
                confidence=0.8
            )
            elements.append(obj2_element)
        
        return elements
    
    def _find_main_verb_enhanced(self, tokens: List[Dict]) -> Optional[int]:
        """
        レガシー機能移行: メイン動詞特定
        既存ロジックを継承・強化
        """
        # POSベースと文脈ベースの両方を取得
        pos_candidates = []
        for i, token in enumerate(tokens):
            # 動詞の品詞タグ
            if (token['tag'].startswith('VB') and token['pos'] == 'VERB') or token['pos'] == 'AUX':
                pos_candidates.append((i, token))
        
        # 文脈的動詞識別（POS誤認識対策）
        contextual_candidates = self._find_contextual_verbs_enhanced(tokens)
        
        # 両方を統合（重複除去）
        verb_candidates = pos_candidates.copy()
        for i, token in contextual_candidates:
            # 既に存在しない場合のみ追加
            if not any(existing_i == i for existing_i, _ in verb_candidates):
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
                if prev_token['text'].lower() in ['who', 'whom', 'which', 'that', 'whose', 'where', 'when']:
                    # whose構文の特別処理: 動詞/名詞同形語は関係節外のメイン動詞として扱う
                    if (prev_token['text'].lower() == 'whose' and 
                        token['text'].lower() in self.ambiguous_words and
                        token.get('contextual_override', False)):
                        # whose構文での同形語動詞は関係節外として扱う
                        is_in_relative_clause = False
                        break
                    
                    # 関係代名詞から動詞までの距離が近い場合、関係節内動詞
                    if i - j <= 4:  # 4語以内なら関係節内
                        is_in_relative_clause = True
                        break
            
            if not is_in_relative_clause:
                non_relative_verbs.append((i, token))
        
        if non_relative_verbs:
            # メイン動詞候補から助動詞でないものを優先
            main_verbs = [(i, token) for i, token in non_relative_verbs if not self._is_auxiliary_verb_enhanced(token)]
            if main_verbs:
                # 文の後半にあるメイン動詞を優先（関係節の後）
                return main_verbs[-1][0]
            return non_relative_verbs[-1][0]
        
        # 最後の手段として、どの動詞でも選択
        return verb_candidates[-1][0]
    
    def _find_contextual_verbs_enhanced(self, tokens: List[Dict]) -> List[Tuple[int, Dict]]:
        """
        レガシー機能移行: 文脈的動詞識別
        """
        contextual_verbs = []
        sentence_text = ' '.join([token['text'] for token in tokens])
        
        for i, token in enumerate(tokens):
            # 既に動詞として認識されているもの
            if token['pos'] in ['VERB', 'AUX']:
                continue
            
            # 同形語チェック
            if token['text'].lower() in self.ambiguous_words:
                if 'VERB' in self.ambiguous_words[token['text'].lower()]:
                    # 文脈から動詞として判定
                    if self._contextual_verb_check_enhanced(tokens, i, sentence_text):
                        # フラグを追加して動詞として扱う
                        enhanced_token = token.copy()
                        enhanced_token['contextual_override'] = True
                        enhanced_token['pos'] = 'VERB'
                        contextual_verbs.append((i, enhanced_token))
        
        return contextual_verbs
    
    def _contextual_verb_check_enhanced(self, tokens: List[Dict], token_idx: int, sentence: str) -> bool:
        """
        レガシー機能移行: 文脈的動詞判定
        """
        token = tokens[token_idx]
        
        # 後続に目的語らしき要素があるか
        for i in range(token_idx + 1, min(len(tokens), token_idx + 3)):
            if i < len(tokens) and tokens[i]['pos'] in ['NOUN', 'PRON']:
                return True
        
        # 前に主語らしき要素があるか
        for i in range(max(0, token_idx - 3), token_idx):
            if tokens[i]['pos'] in ['NOUN', 'PRON']:
                return True
        
        return False
    
    def _find_auxiliary_enhanced(self, tokens: List[Dict], main_verb_idx: int) -> Optional[int]:
        """
        レガシー機能移行: 助動詞特定
        """
        # メイン動詞の前を探索
        for i in range(main_verb_idx - 1, -1, -1):
            token = tokens[i]
            if self._is_auxiliary_verb_enhanced(token):
                return i
            # 名詞が来たら探索終了
            if token['pos'] in ['NOUN', 'PRON']:
                break
        return None
    
    def _find_subject_enhanced(self, tokens: List[Dict], verb_idx: int) -> List[int]:
        """
        レガシー機能移行: 主語特定
        """
        subject_indices = []
        
        # 動詞の前で最初に見つかる名詞句を主語とする
        for i in range(verb_idx - 1, -1, -1):
            token = tokens[i]
            if token['pos'] in ['NOUN', 'PRON']:
                subject_indices.insert(0, i)  # 語順を保持
            elif token['pos'] in ['DET', 'ADJ']:
                subject_indices.insert(0, i)  # 修飾語も含める
            elif subject_indices:  # 名詞句が開始されたら継続
                break
        
        return subject_indices
    
    def _is_auxiliary_verb_enhanced(self, token: Dict) -> bool:
        """
        レガシー機能移行: 助動詞判定
        """
        aux_verbs = {
            'am', 'is', 'are', 'was', 'were', 'be', 'being', 'been',
            'have', 'has', 'had', 'having',
            'do', 'does', 'did',
            'will', 'would', 'shall', 'should',
            'can', 'could', 'may', 'might',
            'must', 'ought'
        }
        return token['lemma'].lower() in aux_verbs or token['pos'] == 'AUX'
    
    def _can_be_complement_enhanced(self, token: Dict) -> bool:
        """
        レガシー機能移行: 補語判定
        """
        return token['pos'] in ['NOUN', 'ADJ', 'PRON']
    
    def _convert_to_handler_result(self, grammar_elements: List[GrammarElement], pattern: str, tokens: List[Dict]) -> Dict[str, Any]:
        """
        GrammarElementsを統合ハンドラー形式に変換
        """
        slots = {}
        
        for element in grammar_elements:
            if element.text and element.text.strip():
                slots[element.role] = element.text.strip()
        
        return {
            'success': True,
            'slots': slots,
            'pattern_detected': pattern,
            'confidence': 0.9,
            'handler_name': 'basic_five_pattern_enhanced',
            'processing_notes': f'Enhanced pattern: {pattern}, elements: {len(grammar_elements)}'
        }
