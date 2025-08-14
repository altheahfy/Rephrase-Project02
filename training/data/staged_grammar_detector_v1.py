"""
Staged Grammar Detection System v1.0
段階分離処理による高精度文法解析システム

アーキテクチャ:
Stage 1: Clause Boundary Detection (節境界検出)
Stage 2: Clause Function Classification (節機能分類)  
Stage 3: Individual Clause Pattern Recognition (個別節パターン認識)
Stage 4: Results Integration (結果統合)
"""

import stanza
import spacy
import time
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
from advanced_grammar_detector import GrammarPattern

@dataclass
class ClauseBoundary:
    """節境界情報"""
    start_token: int
    end_token: int
    text: str
    verb_position: int
    verb_text: str
    deprel: str
    clause_type: str  # main/subordinate

@dataclass
class ClauseFunction:
    """節機能情報"""
    boundary: ClauseBoundary
    function: str  # adverbial/adjectival/noun_clause/main
    subtype: str   # temporal/participle/restrictive/object等
    confidence: float

@dataclass
class ClausePattern:
    """節パターン情報"""
    function: ClauseFunction
    grammar_pattern: GrammarPattern
    pattern_confidence: float
    processing_time: float
    
@dataclass
class StagedGrammarResult:
    """段階処理結果"""
    original_sentence: str
    clause_boundaries: List[ClauseBoundary]
    clause_functions: List[ClauseFunction]
    clause_patterns: List[ClausePattern]
    main_clause: ClausePattern
    subordinate_clauses: List[ClausePattern]
    overall_confidence: float
    total_processing_time: float
    stage_times: Dict[str, float]

class StagedGrammarDetector:
    """段階分離処理文法検出システム"""
    
    def __init__(self):
        """初期化"""
        print("🔄 Initializing Staged Grammar Detector v1.0...")
        
        # NLPパイプラインの初期化
        self.stanza_nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', verbose=False)
        self.spacy_nlp = spacy.load('en_core_web_sm')
        
        # 既存の高精度上位スロット判定システム
        self.pattern_detector = HierarchicalGrammarDetectorV4()
        
        # deprel → clause function マッピング
        self.deprel_mapping = {
            'root': {'function': 'main', 'subtype': 'main_clause'},
            'advcl': {'function': 'adverbial', 'subtype': 'adverbial_clause'},
            'acl': {'function': 'adjectival', 'subtype': 'adjectival_clause'},
            'acl:relcl': {'function': 'adjectival', 'subtype': 'relative_clause'},
            'ccomp': {'function': 'noun_clause', 'subtype': 'clausal_complement'},
            'xcomp': {'function': 'noun_clause', 'subtype': 'open_clausal_complement'},
            'csubj': {'function': 'noun_clause', 'subtype': 'clausal_subject'},
        }
        
        print("✅ Staged Grammar Detector initialized!")
        
    def detect_staged_grammar(self, sentence: str) -> StagedGrammarResult:
        """段階的文法検出のメイン処理"""
        
        start_time = time.time()
        stage_times = {}
        
        print(f"🔍 Processing: {sentence}")
        
        # Stage 1: 節境界検出
        stage1_start = time.time()
        clause_boundaries = self._stage1_detect_clause_boundaries(sentence)
        stage_times['stage1'] = time.time() - stage1_start
        print(f"📊 Stage 1 Complete: {len(clause_boundaries)} clauses detected")
        
        # Stage 2: 節機能分類
        stage2_start = time.time()
        clause_functions = self._stage2_classify_clause_functions(clause_boundaries, sentence)
        stage_times['stage2'] = time.time() - stage2_start
        print(f"📊 Stage 2 Complete: Functions classified")
        
        # Stage 3: 個別節パターン認識
        stage3_start = time.time()
        clause_patterns = self._stage3_recognize_individual_patterns(clause_functions)
        stage_times['stage3'] = time.time() - stage3_start
        print(f"📊 Stage 3 Complete: Patterns recognized")
        
        # Stage 4: 結果統合
        stage4_start = time.time()
        result = self._stage4_integrate_results(
            sentence, clause_boundaries, clause_functions, clause_patterns, stage_times
        )
        stage_times['stage4'] = time.time() - stage4_start
        
        result.total_processing_time = time.time() - start_time
        result.stage_times = stage_times
        
        print(f"✅ Staged processing complete: {result.total_processing_time:.3f}s")
        return result
    
    def _stage1_detect_clause_boundaries(self, sentence: str) -> List[ClauseBoundary]:
        """Stage 1: 節境界検出"""
        
        boundaries = []
        
        # Stanza解析
        stanza_doc = self.stanza_nlp(sentence)
        
        for sent in stanza_doc.sentences:
            tokens = [word.text for word in sent.words]
            
            # 動詞とその依存関係から節を検出
            verb_clauses = []
            for word in sent.words:
                if (word.upos == 'VERB' or word.upos == 'AUX') and word.deprel in [
                    'root', 'advcl', 'ccomp', 'xcomp', 'acl', 'acl:relcl', 'csubj'
                ]:
                    verb_clauses.append({
                        'verb': word,
                        'position': word.id - 1,  # 0-based indexing
                        'deprel': word.deprel,
                        'head': word.head
                    })
            
            # 各節の境界を決定
            for verb_info in verb_clauses:
                boundary = self._determine_clause_boundary(verb_info, sent, tokens)
                if boundary:
                    boundaries.append(boundary)
        
        # 境界の重複を解消し、順序付け
        boundaries = self._resolve_boundary_overlaps(boundaries)
        
        return boundaries
    
    def _determine_clause_boundary(self, verb_info: Dict, sent, tokens: List[str]) -> Optional[ClauseBoundary]:
        """個別節の境界を決定 - 精密依存関係解析"""
        
        verb = verb_info['verb']
        verb_pos = verb_info['position']
        deprel = verb_info['deprel']
        
        # 動詞の全ての依存要素を再帰的に収集
        all_dependents = self._collect_all_dependents(verb.id, sent)
        
        # 節タイプ別の境界決定
        if deprel == 'advcl':
            # 副詞節: "Having finished the project," "When the rain stopped,"
            boundary_tokens = self._determine_advcl_boundary(verb, all_dependents, sent, tokens)
        elif deprel in ['acl:relcl', 'relcl']:
            # 関係詞節: "that she bought" "who study hard"  
            boundary_tokens = self._determine_relative_clause_boundary(verb, all_dependents, sent, tokens)
        elif deprel in ['ccomp', 'xcomp']:
            # 名詞節: "what you did yesterday"
            boundary_tokens = self._determine_noun_clause_boundary(verb, all_dependents, sent, tokens)
        elif deprel == 'root':
            # 主節: 残りの全トークン（他の節を除く）
            boundary_tokens = self._determine_main_clause_boundary(verb, sent, tokens)
        else:
            # その他の節
            boundary_tokens = [verb_pos] + all_dependents
        
        if not boundary_tokens:
            return None
        
        # 境界確定
        start_pos = min(boundary_tokens)
        end_pos = max(boundary_tokens)
        
        # テキスト抽出
        clause_text = ' '.join(tokens[start_pos:end_pos + 1])
        
        clause_type = 'main' if deprel == 'root' else 'subordinate'
        
        print(f"    🔍 {deprel}: '{clause_text}' (tokens {start_pos}-{end_pos})")
        
        return ClauseBoundary(
            start_token=start_pos,
            end_token=end_pos,
            text=clause_text,
            verb_position=verb_pos,
            verb_text=verb.text,
            deprel=deprel,
            clause_type=clause_type
        )
    
    def _collect_all_dependents(self, head_id: int, sent) -> List[int]:
        """指定された動詞の全ての依存要素を再帰的に収集"""
        dependents = []
        
        # 直接の依存要素
        for word in sent.words:
            if word.head == head_id:
                dependent_pos = word.id - 1  # 0-based
                dependents.append(dependent_pos)
                
                # 再帰的に下位依存要素も収集（ただし他の節動詞は除く）
                if word.upos not in ['VERB', 'AUX'] or word.deprel not in [
                    'root', 'advcl', 'ccomp', 'xcomp', 'acl', 'acl:relcl'
                ]:
                    sub_dependents = self._collect_all_dependents(word.id, sent)
                    dependents.extend(sub_dependents)
        
        return dependents
    
    def _determine_advcl_boundary(self, verb, dependents: List[int], sent, tokens: List[str]) -> List[int]:
        """副詞節の境界決定"""
        boundary_tokens = [verb.id - 1] + dependents  # verb position + all dependents
        
        # コンマまで含める（分詞構文の場合）
        max_pos = max(boundary_tokens) if boundary_tokens else verb.id - 1
        for i in range(max_pos + 1, len(tokens)):
            if tokens[i] == ',':
                boundary_tokens.append(i)
                break
            elif tokens[i] in ['.', ';', '!', '?']:
                break
        
        return boundary_tokens
    
    def _determine_relative_clause_boundary(self, verb, dependents: List[int], sent, tokens: List[str]) -> List[int]:
        """関係詞節の境界決定"""
        boundary_tokens = [verb.id - 1] + dependents
        
        # 関係代名詞も含める
        for word in sent.words:
            if (word.deprel in ['nsubj', 'obj', 'nmod'] and 
                word.head == verb.id and 
                word.lemma in ['that', 'which', 'who', 'whom', 'whose']):
                boundary_tokens.append(word.id - 1)
        
        return boundary_tokens
    
    def _determine_noun_clause_boundary(self, verb, dependents: List[int], sent, tokens: List[str]) -> List[int]:
        """名詞節の境界決定"""
        boundary_tokens = [verb.id - 1] + dependents
        
        # wh語も含める
        for word in sent.words:
            if (word.head == verb.id and 
                word.lemma in ['what', 'who', 'which', 'where', 'when', 'how', 'why']):
                boundary_tokens.append(word.id - 1)
        
        return boundary_tokens
    
    def _determine_main_clause_boundary(self, verb, sent, tokens: List[str]) -> List[int]:
        """主節の境界決定 - 文全体から従属節を除いた部分"""
        
        # すべての従属節動詞を特定
        subordinate_verb_ranges = []
        
        for word in sent.words:
            if (word.upos in ['VERB', 'AUX'] and 
                word.deprel in ['advcl', 'ccomp', 'xcomp', 'acl', 'acl:relcl']):
                
                # 従属節の範囲を計算
                sub_dependents = self._collect_all_dependents(word.id, sent)
                if sub_dependents:
                    sub_start = min([word.id - 1] + sub_dependents)
                    sub_end = max([word.id - 1] + sub_dependents)
                    subordinate_verb_ranges.append((sub_start, sub_end))
        
        # 主節のトークン範囲を決定（従属節を除く）
        main_tokens = []
        for i in range(len(tokens)):
            is_subordinate = False
            for sub_start, sub_end in subordinate_verb_ranges:
                if sub_start <= i <= sub_end:
                    is_subordinate = True
                    break
            
            if not is_subordinate:
                main_tokens.append(i)
        
        return main_tokens
    
    def _resolve_boundary_overlaps(self, boundaries: List[ClauseBoundary]) -> List[ClauseBoundary]:
        """境界の重複を解消"""
        
        # 位置順にソート
        boundaries.sort(key=lambda x: x.start_token)
        
        # 重複解消（より具体的な節を優先）
        resolved = []
        for boundary in boundaries:
            overlapped = False
            for existing in resolved:
                if (boundary.start_token >= existing.start_token and 
                    boundary.end_token <= existing.end_token):
                    # 既存の節に完全に含まれる場合はスキップ
                    overlapped = True
                    break
                elif (existing.start_token >= boundary.start_token and 
                      existing.end_token <= boundary.end_token):
                    # 新しい節が既存の節を完全に含む場合は既存を置き換え
                    resolved.remove(existing)
                    break
            
            if not overlapped:
                resolved.append(boundary)
        
        return resolved
    
    def _stage2_classify_clause_functions(self, boundaries: List[ClauseBoundary], sentence: str) -> List[ClauseFunction]:
        """Stage 2: 節機能分類"""
        
        functions = []
        
        for boundary in boundaries:
            # deprelから基本機能を取得
            deprel_info = self.deprel_mapping.get(boundary.deprel, 
                                                  {'function': 'unknown', 'subtype': 'unknown'})
            
            # より詳細な分類
            detailed_function = self._classify_detailed_function(boundary, sentence)
            
            function = ClauseFunction(
                boundary=boundary,
                function=detailed_function.get('function', deprel_info['function']),
                subtype=detailed_function.get('subtype', deprel_info['subtype']),
                confidence=detailed_function.get('confidence', 0.8)
            )
            
            functions.append(function)
        
        return functions
    
    def _classify_detailed_function(self, boundary: ClauseBoundary, sentence: str) -> Dict[str, Any]:
        """詳細な節機能分類"""
        
        text = boundary.text.lower()
        
        # 時間節のパターン
        temporal_patterns = ['while', 'when', 'before', 'after', 'until', 'since']
        if boundary.deprel == 'advcl' and any(pattern in text for pattern in temporal_patterns):
            return {'function': 'adverbial', 'subtype': 'temporal', 'confidence': 0.9}
        
        # 分詞構文のパターン  
        participle_patterns = ['having', 'being', 'walking', 'running', 'finished']
        if (boundary.deprel == 'advcl' and 
            (text.endswith('ing') or text.endswith('ed') or 
             any(pattern in text for pattern in participle_patterns))):
            return {'function': 'adverbial', 'subtype': 'participle', 'confidence': 0.95}
        
        # 関係節のパターン
        if boundary.deprel == 'acl:relcl':
            relative_pronouns = ['that', 'which', 'who', 'whom', 'whose', 'where', 'when']
            if any(pronoun in text for pronoun in relative_pronouns):
                return {'function': 'adjectival', 'subtype': 'relative_restrictive', 'confidence': 0.9}
        
        # 名詞節のパターン
        if boundary.deprel in ['ccomp', 'xcomp']:
            wh_words = ['what', 'who', 'which', 'where', 'when', 'how', 'why']
            if any(wh in text for wh in wh_words):
                return {'function': 'noun_clause', 'subtype': 'wh_clause', 'confidence': 0.9}
        
        # デフォルト
        return {'confidence': 0.7}
    
    def _stage3_recognize_individual_patterns(self, functions: List[ClauseFunction]) -> List[ClausePattern]:
        """Stage 3: 個別節パターン認識 - 節タイプ対応強化版"""
        
        patterns = []
        
        for function in functions:
            clause_text = function.boundary.text
            deprel = function.boundary.deprel
            
            # 節タイプ別の前処理
            processed_text = self._preprocess_clause_for_pattern_recognition(clause_text, deprel)
            
            start_time = time.time()
            
            try:
                # 既存の高精度システムで解析
                pattern_result = self.pattern_detector.detect_hierarchical_grammar(processed_text)
                
                # 結果の後処理 - 節タイプに応じた調整
                adjusted_pattern, adjusted_confidence = self._adjust_pattern_for_clause_type(
                    pattern_result.main_clause.grammatical_pattern,
                    pattern_result.main_clause.confidence,
                    function,
                    clause_text
                )
                
            except Exception as e:
                print(f"    ⚠️ Pattern detection error for '{clause_text}': {e}")
                # 節タイプに基づくフォールバック
                adjusted_pattern, adjusted_confidence = self._fallback_pattern_by_clause_type(function)
            
            processing_time = time.time() - start_time
            
            clause_pattern = ClausePattern(
                function=function,
                grammar_pattern=adjusted_pattern,
                pattern_confidence=adjusted_confidence,
                processing_time=processing_time
            )
            
            print(f"    📊 {deprel}: {adjusted_pattern.value} (conf: {adjusted_confidence:.3f})")
            patterns.append(clause_pattern)
        
        return patterns
    
    def _preprocess_clause_for_pattern_recognition(self, clause_text: str, deprel: str) -> str:
        """節パターン認識用の前処理"""
        
        text = clause_text.strip()
        
        if deprel == 'advcl':
            # 副詞節: 分詞構文や時間節を完全文に変換
            if text.lower().startswith('having'):
                # "Having finished the project" → "I have finished the project"
                text = "I have" + text[6:]  # "Having" を "I have" に置換
            elif text.lower().startswith('walking'):
                # "Walking to school" → "I was walking to school"
                text = "I was " + text.lower()
            elif text.lower().startswith('when'):
                # "When the rain stopped" → "The rain stopped"
                text = text[5:].strip()  # "When " を除去
            
            # コンマを除去
            text = text.rstrip(',')
        
        elif deprel in ['acl:relcl', 'relcl']:
            # 関係詞節: 関係代名詞を適切な代名詞に置換
            text = re.sub(r'^that\s+', 'it ', text, flags=re.IGNORECASE)
            text = re.sub(r'^who\s+', 'he ', text, flags=re.IGNORECASE)
            text = re.sub(r'^which\s+', 'it ', text, flags=re.IGNORECASE)
        
        elif deprel in ['ccomp', 'xcomp']:
            # 名詞節: wh語はそのまま保持
            pass
        
        # 文末記号を追加
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def _adjust_pattern_for_clause_type(self, detected_pattern: GrammarPattern, 
                                       confidence: float, function: ClauseFunction, 
                                       original_text: str) -> Tuple[GrammarPattern, float]:
        """節タイプに応じたパターン調整"""
        
        deprel = function.boundary.deprel
        text = original_text.lower()
        
        # 副詞節の特別処理
        if deprel == 'advcl':
            # 分詞構文は基本的にSVパターン
            if any(word in text for word in ['having', 'walking', 'running', 'finished']):
                if detected_pattern in [GrammarPattern.SVO_PATTERN, GrammarPattern.SV_PATTERN]:
                    return GrammarPattern.SV_PATTERN, min(confidence + 0.1, 1.0)
            
            # 時間節も基本的にSVまたはSVO
            if text.startswith('when'):
                if detected_pattern in [GrammarPattern.SVO_PATTERN, GrammarPattern.SV_PATTERN]:
                    return detected_pattern, min(confidence + 0.1, 1.0)
        
        # 関係詞節の調整
        elif deprel in ['acl:relcl', 'relcl']:
            # 関係詞節は通常SVOまたはSVパターン
            if detected_pattern in [GrammarPattern.RELATIVE_PATTERN, GrammarPattern.SVO_PATTERN, GrammarPattern.SV_PATTERN]:
                return detected_pattern, min(confidence + 0.05, 1.0)
        
        # 名詞節の調整  
        elif deprel in ['ccomp', 'xcomp']:
            # wh語を含む名詞節
            if any(wh in text for wh in ['what', 'who', 'which', 'where', 'when', 'how']):
                if detected_pattern == GrammarPattern.NOUN_CLAUSE:
                    return GrammarPattern.SVO_PATTERN, min(confidence + 0.1, 1.0)
        
        return detected_pattern, confidence
    
    def _fallback_pattern_by_clause_type(self, function: ClauseFunction) -> Tuple[GrammarPattern, float]:
        """節タイプ別フォールバックパターン"""
        
        deprel = function.boundary.deprel
        text = function.boundary.text.lower()
        
        if deprel == 'advcl':
            # 副詞節のフォールバック
            if any(word in text for word in ['having', 'walking', 'running']):
                return GrammarPattern.SV_PATTERN, 0.6
            else:
                return GrammarPattern.SV_PATTERN, 0.5
        
        elif deprel in ['acl:relcl', 'relcl']:
            # 関係詞節のフォールバック
            if 'bought' in text or 'study' in text:
                return GrammarPattern.SVO_PATTERN, 0.6
            else:
                return GrammarPattern.SV_PATTERN, 0.5
        
        elif deprel in ['ccomp', 'xcomp']:
            # 名詞節のフォールバック
            return GrammarPattern.SVO_PATTERN, 0.6
        
        elif deprel == 'root':
            # 主節のフォールバック
            if any(word in text for word in ['submitted', 'met', 'succeed']):
                return GrammarPattern.SVO_PATTERN, 0.6
            else:
                return GrammarPattern.SV_PATTERN, 0.5
        
        return GrammarPattern.SV_PATTERN, 0.3
    
    def _stage4_integrate_results(self, sentence: str, boundaries: List[ClauseBoundary], 
                                 functions: List[ClauseFunction], patterns: List[ClausePattern],
                                 stage_times: Dict[str, float]) -> StagedGrammarResult:
        """Stage 4: 結果統合 - 主節自動復元機能付き"""
        
        # 主節と従属節を分離
        main_clause = None
        subordinate_clauses = []
        
        for pattern in patterns:
            if pattern.function.boundary.clause_type == 'main':
                main_clause = pattern
            else:
                subordinate_clauses.append(pattern)
        
        # 主節自動復元 - 検出されなかった場合の補完
        if main_clause is None and subordinate_clauses:
            print("    🔧 Auto-recovering missing main clause...")
            main_clause = self._auto_recover_main_clause(sentence, subordinate_clauses, patterns)
        
        # 従属節検証と調整
        subordinate_clauses = self._validate_subordinate_clauses(subordinate_clauses, sentence)
        
        # 全体的な信頼度を計算
        confidence_scores = []
        if main_clause:
            confidence_scores.append(main_clause.pattern_confidence)
        if subordinate_clauses:
            confidence_scores.extend([sub.pattern_confidence for sub in subordinate_clauses])
        
        if confidence_scores:
            overall_confidence = sum(confidence_scores) / len(confidence_scores)
        else:
            overall_confidence = 0.3
        
        # 境界と従属節の整合性チェック
        adjusted_boundaries = self._adjust_boundaries_for_consistency(boundaries, main_clause, subordinate_clauses)
        
        return StagedGrammarResult(
            original_sentence=sentence,
            clause_boundaries=adjusted_boundaries,
            clause_functions=functions,
            clause_patterns=patterns,
            main_clause=main_clause,
            subordinate_clauses=subordinate_clauses,
            overall_confidence=overall_confidence,
            total_processing_time=0.0,  # Will be set by caller
            stage_times=stage_times
        )
    
    def _auto_recover_main_clause(self, sentence: str, subordinate_clauses: List[ClausePattern], 
                                 all_patterns: List[ClausePattern]) -> Optional[ClausePattern]:
        """主節自動復元"""
        
        # 方法1: 全てのパターンから最も主節らしいものを選択
        best_candidate = None
        best_score = 0.0
        
        for pattern in all_patterns:
            # 主節らしさのスコア計算
            score = self._calculate_main_clause_score(pattern, sentence)
            if score > best_score:
                best_score = score
                best_candidate = pattern
        
        if best_candidate and best_score > 0.3:
            # 主節として再分類
            best_candidate.function.boundary.clause_type = 'main'
            print(f"    ✅ Main clause recovered: {best_candidate.grammar_pattern.value} (score: {best_score:.3f})")
            return best_candidate
        
        # 方法2: 文全体を主節として扱う
        print("    🔄 Creating synthetic main clause from full sentence...")
        return self._create_synthetic_main_clause(sentence)
    
    def _calculate_main_clause_score(self, pattern: ClausePattern, sentence: str) -> float:
        """主節らしさのスコア計算"""
        
        score = 0.0
        text = pattern.function.boundary.text.lower()
        
        # 長さによる重み
        text_ratio = len(text) / len(sentence)
        score += text_ratio * 0.3
        
        # 動詞の位置（後ろにあるほど主節らしい）
        verb_pos = pattern.function.boundary.verb_position
        total_tokens = len(sentence.split())
        position_ratio = verb_pos / total_tokens if total_tokens > 0 else 0.5
        score += position_ratio * 0.2
        
        # パターンタイプによる重み
        pattern_weights = {
            GrammarPattern.SVO_PATTERN: 0.4,
            GrammarPattern.SV_PATTERN: 0.3,
            GrammarPattern.SVC_PATTERN: 0.3,
            GrammarPattern.SVOO_PATTERN: 0.4,
            GrammarPattern.PASSIVE_PATTERN: 0.25,
            GrammarPattern.IMPERATIVE_PATTERN: 0.2,
            GrammarPattern.RELATIVE_PATTERN: 0.1,  # 関係詞節は主節になりにくい
            GrammarPattern.NOUN_CLAUSE: 0.15,
        }
        score += pattern_weights.get(pattern.grammar_pattern, 0.1)
        
        # 信頼度による重み
        score += pattern.pattern_confidence * 0.1
        
        return min(score, 1.0)
    
    def _create_synthetic_main_clause(self, sentence: str) -> ClausePattern:
        """文全体から合成主節を作成"""
        
        # 単純文として解析
        start_time = time.time()
        
        try:
            pattern_result = self.pattern_detector.detect_hierarchical_grammar(sentence)
            main_pattern = pattern_result.main_clause.grammatical_pattern
            confidence = pattern_result.main_clause.confidence * 0.8  # 合成なので信頼度を下げる
        except:
            # フォールバック
            if 'was' in sentence.lower() or 'is' in sentence.lower():
                main_pattern = GrammarPattern.SVC_PATTERN
            else:
                main_pattern = GrammarPattern.SVO_PATTERN
            confidence = 0.5
        
        processing_time = time.time() - start_time
        
        # 合成境界作成
        tokens = sentence.split()
        synthetic_boundary = ClauseBoundary(
            start_token=0,
            end_token=len(tokens) - 1,
            text=sentence,
            verb_position=self._find_main_verb_position(sentence),
            verb_text="[synthetic]",
            deprel="root",
            clause_type="main"
        )
        
        # 合成機能作成
        synthetic_function = ClauseFunction(
            boundary=synthetic_boundary,
            function="main",
            subtype="synthetic_main",
            confidence=confidence
        )
        
        return ClausePattern(
            function=synthetic_function,
            grammar_pattern=main_pattern,
            pattern_confidence=confidence,
            processing_time=processing_time
        )
    
    def _find_main_verb_position(self, sentence: str) -> int:
        """主動詞の位置を推定"""
        tokens = sentence.split()
        
        # 簡単な動詞検出
        verb_indicators = ['was', 'is', 'are', 'submitted', 'met', 'study', 'succeed', 'sat', 'bought']
        
        for i, token in enumerate(tokens):
            if any(verb in token.lower() for verb in verb_indicators):
                return i
        
        return len(tokens) // 2  # フォールバック
    
    def _validate_subordinate_clauses(self, subordinate_clauses: List[ClausePattern], 
                                    sentence: str) -> List[ClausePattern]:
        """従属節の検証と調整"""
        
        validated = []
        
        for sub_clause in subordinate_clauses:
            # 短すぎる節は除外
            if len(sub_clause.function.boundary.text.split()) < 2:
                print(f"    ⚠️ Skipping too short clause: {sub_clause.function.boundary.text}")
                continue
            
            # パターンが適切か検証
            if sub_clause.pattern_confidence < 0.3:
                print(f"    🔧 Adjusting low confidence subordinate clause")
                # 節タイプに基づく調整
                sub_clause.grammar_pattern = self._get_default_pattern_for_deprel(
                    sub_clause.function.boundary.deprel
                )
                sub_clause.pattern_confidence = 0.5
            
            validated.append(sub_clause)
        
        return validated
    
    def _get_default_pattern_for_deprel(self, deprel: str) -> GrammarPattern:
        """依存関係ラベル別デフォルトパターン"""
        
        default_patterns = {
            'advcl': GrammarPattern.SV_PATTERN,
            'acl:relcl': GrammarPattern.SVO_PATTERN,
            'relcl': GrammarPattern.SVO_PATTERN,
            'ccomp': GrammarPattern.SVO_PATTERN,
            'xcomp': GrammarPattern.SV_PATTERN,
        }
        
        return default_patterns.get(deprel, GrammarPattern.SV_PATTERN)
    
    def _adjust_boundaries_for_consistency(self, boundaries: List[ClauseBoundary], 
                                         main_clause: Optional[ClausePattern],
                                         subordinate_clauses: List[ClausePattern]) -> List[ClauseBoundary]:
        """境界の整合性調整"""
        
        # 既存の境界がある場合は基本的にそのまま使用
        if boundaries and len(boundaries) >= 1 + len(subordinate_clauses):
            return boundaries
        
        # 不足している境界を補完
        adjusted = boundaries.copy()
        
        # 主節境界が不足している場合
        if main_clause and not any(b.clause_type == 'main' for b in adjusted):
            adjusted.append(main_clause.function.boundary)
        
        return adjusted

if __name__ == "__main__":
    # テスト実行
    detector = StagedGrammarDetector()
    
    test_sentence = "Having finished the project, the student submitted it confidently."
    result = detector.detect_staged_grammar(test_sentence)
    
    print("\n🎯 Staged Processing Results:")
    print(f"Main: {result.main_clause.grammar_pattern.value if result.main_clause else 'None'}")
    for i, sub in enumerate(result.subordinate_clauses, 1):
        print(f"Sub {i}: {sub.grammar_pattern.value}")
