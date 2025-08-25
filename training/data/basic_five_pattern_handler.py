"""
Phase A2: 真のBasicFivePatternHandler実装
レガシー分解機能をハンドラー内に完全移行

作成日: 2025年8月25日
目的: Central Control            # 1. コア要素特定（レガシー機能移行）
            self.logger.debug("🔍 Step 1: Starting core elements identification")
            core_elements = self.identify_core_elements_enhanced(filtered_tokens)
            self.logger.debug(f"🔍 Step 1 complete: {core_elements}")
            
            # 2. 文型パターン判定（レガシー機能移行）
            self.logger.debug("🔍 Step 2: Starting pattern determination")
            sentence_pattern = self.determine_pattern_enhanced(filtered_tokens, core_elements)
            self.logger.debug(f"🔍 Step 2 complete: {sentence_pattern}")
            
            # 3. 文法役割割り当て（レガシー機能移行）
            self.logger.debug("🔍 Step 3: Starting roles assignment")
            grammar_elements = self.assign_roles_enhanced(filtered_tokens, sentence_pattern, core_elements, relative_clause_info)
            self.logger.debug(f"🔍 Step 3 complete: {len(grammar_elements) if grammar_elements else 0} elements")能を移行し、純粋中央管理を実現
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
        
        # レガシー機能移行: 曖昧語辞書
        self.ambiguous_words = {
            'lives': ['NOUN', 'VERB'],    # life複数形 vs live三人称単数
            'works': ['NOUN', 'VERB'],    # work複数形 vs work三人称単数  
            'runs': ['NOUN', 'VERB'],     # run複数形 vs run三人称単数
            'goes': ['NOUN', 'VERB'],     # go複数形 vs go三人称単数
            'comes': ['NOUN', 'VERB'],    # come複数形 vs come三人称単数
            'stays': ['NOUN', 'VERB'],    # stay複数形 vs stay三人称単数
            'plays': ['NOUN', 'VERB'],    # play複数形 vs play三人称単数
            'looks': ['NOUN', 'VERB'],    # look複数形 vs look三人称単数
            'walks': ['NOUN', 'VERB'],    # walk複数形 vs walk三人称単数
            'talks': ['NOUN', 'VERB'],    # talk複数形 vs talk三人称単数
            'moves': ['NOUN', 'VERB'],    # move複数形 vs move三人称単数
            'drives': ['NOUN', 'VERB'],   # drive複数形 vs drive三人称単数
            'flies': ['NOUN', 'VERB'],    # fly複数形 vs fly三人称単数
            'rides': ['NOUN', 'VERB'],    # ride複数形 vs ride三人称単数
            'sits': ['NOUN', 'VERB']      # sit複数形 vs sit三人称単数
        }
    
    def analyze_basic_pattern(self, filtered_tokens: List[Dict], relative_clause_info: Dict) -> Dict[str, Any]:
        """
        🎯 Phase A3: 統合エントリーポイント
        レガシー分解機能を統合した文型解析
        
        Args:
            filtered_tokens: 関係節要素を除外した解析対象トークン
            relative_clause_info: 関係節情報
            
        Returns:
            Dict containing:
            - core_elements: 特定されたコア要素
            - sentence_pattern: 判定された文型パターン  
            - grammar_elements: 文法役割が割り当てられた要素
        """
        try:
            # 1. コア要素特定（レガシー機能移行）
            core_elements = self.identify_core_elements_enhanced(filtered_tokens)
            
            # 2. 文型パターン判定（レガシー機能移行）
            sentence_pattern = self.determine_pattern_enhanced(filtered_tokens, core_elements)
            
            # 3. 文法役割割り当て（レガシー機能移行）
            grammar_elements = self.assign_roles_enhanced(filtered_tokens, sentence_pattern, core_elements)
            
            return {
                'core_elements': core_elements,
                'sentence_pattern': sentence_pattern,
                'grammar_elements': grammar_elements,
                'handler_success': True,
                'analysis_method': 'basic_five_pattern_enhanced'
            }
            
        except Exception as e:
            self.logger.error(f"BasicFivePatternHandler.analyze_basic_pattern error: {e}")
            return {
                'core_elements': {},
                'sentence_pattern': 'unknown',
                'grammar_elements': [],
                'handler_success': False,
                'error': str(e)
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
        try:
            # デバッグ：トークンの検証
            if not isinstance(tokens, list):
                raise TypeError(f"Expected list of tokens, got {type(tokens)}")
                
            for i, token in enumerate(tokens):
                if not isinstance(token, dict):
                    raise TypeError(f"Token at index {i} is not a dict: {type(token)} = {token}")
                if 'text' not in token:
                    self.logger.warning(f"Token at index {i} missing 'text' field: {token}")
                    
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
            
        except Exception as e:
            self.logger.error(f"identify_core_elements_enhanced error: {e}")
            raise
    
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
            # 補語（フレーズ全体を取得）
            comp_tokens = []
            comp_indices = []
            
            # 補語として適切なすべてのトークンを取得
            for i, (idx, token) in enumerate(remaining_tokens):
                if self._can_be_complement_enhanced(token):
                    comp_tokens.append(token)
                    comp_indices.append(idx)
                elif comp_tokens:  # 既に補語があり、補語でない場合は停止
                    break
            
            if comp_tokens:
                comp_text = ' '.join(t['text'] for t in comp_tokens)
                comp_element = GrammarElement(
                    text=comp_text,
                    tokens=comp_tokens,
                    role='C1',
                    start_idx=comp_indices[0],
                    end_idx=comp_indices[-1],
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
        曖昧語解決4段階プロセス実装
        """
        try:
            # 🎯 Step 1: ハードコーディングリスト化による曖昧語認識
            self.logger.debug(f"🔍 [曖昧語解決] Step 1: 曖昧語候補検索開始")
            ambiguous_candidates = []
            for i, token in enumerate(tokens):
                if token['text'].lower() in self.ambiguous_words:
                    ambiguous_candidates.append((i, token))
                    self.logger.debug(f"🔍 [曖昧語解決] 曖昧語発見: {token['text']} (位置{i})")
            
            # POSベースと文脈ベースの両方を取得
            pos_candidates = []
            for i, token in enumerate(tokens):
                # 動詞の品詞タグ
                if (token['tag'].startswith('VB') and token['pos'] == 'VERB') or token['pos'] == 'AUX':
                    pos_candidates.append((i, token))
                    
            self.logger.debug(f"🔍 [曖昧語解決] POS動詞候補: {[(i, t['text'], t['pos'], t['tag']) for i, t in pos_candidates]}")
            
            # 文脈的動詞識別（POS誤認識対策）
            contextual_candidates = self._find_contextual_verbs_enhanced(tokens)
            
            # 両方を統合（重複除去）
            verb_candidates = pos_candidates.copy()
            for i, token in contextual_candidates:
                # 既に存在しない場合のみ追加
                if not any(existing_i == i for existing_i, _ in verb_candidates):
                    verb_candidates.append((i, token))
            
            self.logger.debug(f"🔍 [曖昧語解決] 全動詞候補: {[(i, t['text']) for i, t in verb_candidates]}")
            
            if not verb_candidates:
                return None
            
            # 🎯 Step 2-4: 曖昧語の両ケース検証プロセス
            if ambiguous_candidates:
                resolved_verb = self._resolve_ambiguous_words(tokens, verb_candidates, ambiguous_candidates)
                if resolved_verb is not None:
                    self.logger.debug(f"🔥 [曖昧語解決] 文法的完整性により解決: 位置{resolved_verb} = '{tokens[resolved_verb]['text']}'")
                    return resolved_verb
            
            # 🔥 Phase A3: spaCy POSタグを優先（曖昧語解決後）
            # VERBタグの動詞を優先選択
            verb_tagged_candidates = [(i, token) for i, token in verb_candidates if token['pos'] == 'VERB']
            if verb_tagged_candidates:
                # 最後のVERBタグ動詞を選択（メイン動詞として）
                return verb_tagged_candidates[-1][0]
            
            # 人間的判定：関係節を除外してメイン動詞を特定
            non_relative_verbs = []
            
            for i, token in verb_candidates:
                # 関係代名詞の直後の動詞は関係節内動詞として除外
                is_in_relative_clause = False
                
                # 🔥 Phase A3: filtered_tokensでは関係節は既に除外済み
                # 追加の関係節検出は不要（重複処理回避）
                
                # 前の単語を確認（filtered_tokensでない場合のみ）
                # Phase A3では関係節処理は中央管理で実行済み
                
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
            
        except Exception as e:
            self.logger.error(f"_find_main_verb_enhanced error: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    def _resolve_ambiguous_words(self, tokens: List[Dict], verb_candidates: List[Tuple[int, Dict]], 
                                ambiguous_candidates: List[Tuple[int, Dict]]) -> Optional[int]:
        """
        曖昧語解決4段階プロセス実装
        文法的完整性をケース選択の最終判定基準とする
        """
        self.logger.debug(f"🔍 [曖昧語解決] Step 2: 両ケース可能性付与開始")
        
        for amb_idx, amb_token in ambiguous_candidates:
            word = amb_token['text'].lower()
            self.logger.debug(f"🔍 [曖昧語解決] 検証対象: '{word}' (位置{amb_idx})")
            
            # Step 3: ケース1検証（名詞解釈）
            noun_case_valid = self._validate_noun_case(tokens, amb_idx, word)
            self.logger.debug(f"🔍 [曖昧語解決] ケース1（名詞解釈）: {noun_case_valid}")
            
            # Step 4: ケース2検証（動詞解釈）  
            verb_case_valid = self._validate_verb_case(tokens, amb_idx, word)
            self.logger.debug(f"🔍 [曖昧語解決] ケース2（動詞解釈）: {verb_case_valid}")
            
            # 文法的完整性による最終判定
            if verb_case_valid and not noun_case_valid:
                # 動詞として解釈することで文が完成する場合
                return amb_idx
            elif not verb_case_valid and noun_case_valid:
                # 名詞として解釈すべき場合、他の動詞を探す
                continue
                
        # 曖昧語解決に失敗した場合、従来ロジックに戻る
        return None
    
    def _validate_noun_case(self, tokens: List[Dict], amb_idx: int, word: str) -> bool:
        """
        Step 3: 名詞解釈での文法的完整性検証
        例：lives → life複数形（名詞）として扱った場合の文の完整性
        """
        # spaCy POS解析結果を重視：NOUNとタグ付けされているものは名詞として扱う
        actual_pos = tokens[amb_idx]['pos']
        if actual_pos == 'NOUN':
            self.logger.debug(f"🔍 [曖昧語解決] spaCy解析: '{word}' は NOUN タグ → 名詞解釈有効")
            return True
            
        # 名詞として扱った場合、主語・動詞・目的語が適切に配置されているかチェック
        sentence_tokens = [t['text'] for t in tokens]
        
        # 関係節の境界を認識
        relative_pronouns = ['who', 'whom', 'which', 'that', 'whose', 'where', 'when']
        relative_start = None
        
        for i, token in enumerate(tokens):
            if token['text'].lower() in relative_pronouns:
                relative_start = i
                break
        
        if relative_start is not None and amb_idx > relative_start:
            # 関係節内の語として名詞解釈の場合
            # 関係節だけで完結した文になるかチェック
            relative_clause_tokens = tokens[relative_start:amb_idx+1]
            
            # 関係節内に動詞があるかチェック
            has_relative_verb = any(t['pos'] == 'VERB' and t['tag'].startswith('VB') 
                                  for t in relative_clause_tokens if t != tokens[amb_idx])
            
            if has_relative_verb:
                # 関係節内に他の動詞があり、この語を名詞とすると関係節が完結
                # しかし主文の動詞がない状態 → 文法的に不完全
                main_clause_tokens = tokens[amb_idx+1:]
                has_main_verb = any(t['pos'] == 'VERB' and t['tag'].startswith('VB') 
                                  for t in main_clause_tokens)
                
                if not has_main_verb:
                    self.logger.debug(f"🔍 [曖昧語解決] 名詞解釈→関係節完結するが主文に動詞なし → 不完整")
                    return False
                    
        return True
    
    def _validate_verb_case(self, tokens: List[Dict], amb_idx: int, word: str) -> bool:
        """
        Step 4: 動詞解釈での文法的完整性検証
        例：lives → 動詞として扱った場合の文の完整性
        """
        # spaCy POS解析結果を重視：NOUNとタグ付けされているものは動詞解釈無効
        actual_pos = tokens[amb_idx]['pos']
        if actual_pos == 'NOUN':
            self.logger.debug(f"🔍 [曖昧語解決] spaCy解析: '{word}' は NOUN タグ → 動詞解釈無効")
            return False
            
        # 動詞として扱った場合の文の構造チェック
        sentence_tokens = [t['text'] for t in tokens]
        
        # 関係節の境界を認識
        relative_pronouns = ['who', 'whom', 'which', 'that', 'whose', 'where', 'when']
        relative_start = None
        
        for i, token in enumerate(tokens):
            if token['text'].lower() in relative_pronouns:
                relative_start = i
                break
                
        if relative_start is not None and amb_idx > relative_start:
            # 関係節の後の位置での動詞解釈
            # 主文の動詞として機能するかチェック
            
            # 主語の存在確認（関係節より前）
            has_subject = any(t['dep'] in ['nsubj', 'nsubj:pass'] 
                            for t in tokens[:relative_start])
            
            if has_subject:
                self.logger.debug(f"🔍 [曖昧語解決] 動詞解釈→主語あり、完全な文として成立")
                return True
                
        return True  # デフォルトで有効とする
    
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
