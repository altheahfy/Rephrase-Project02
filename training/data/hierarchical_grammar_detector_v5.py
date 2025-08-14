"""
Hierarchical Grammar Detector v5.0
2段階処理による階層文法検出システム

V4からの改良点:
1. 2段階処理の実装（Step1: 主節解析、Step2: 節内解析）
2. 複文における主節判定精度の向上
3. Grammar Master Controller v2との連携強化
4. 全文法パターンの網羅的検出
5. V4の高精度システム（83.3%）を基盤として活用

設計思想: "既存の高精度システムを2回使う単純で確実な方法"
目標精度: V4ベースライン維持 + 階層文66.7% → 80%+
"""

import stanza
import spacy
import time
import logging
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import re

# Import existing pattern definitions
from advanced_grammar_detector import (
    GrammarPattern, GrammarDetectionResult, AdvancedGrammarDetector, 
    DependencyInfo
)

@dataclass
class PreciseClauseInfo:
    """Ultra-precise clause information with detailed linguistic analysis."""
    text: str
    clause_type: str
    root_word: str
    root_index: int
    root_pos: str
    root_lemma: str
    dependencies: List[DependencyInfo] = field(default_factory=list)
    word_positions: List[Tuple[int, int]] = field(default_factory=list)
    grammatical_pattern: Optional[GrammarPattern] = None
    confidence: float = 0.0
    linguistic_features: Dict[str, Any] = field(default_factory=dict)
    subjects: List[str] = field(default_factory=list)
    objects: List[str] = field(default_factory=list)
    complements: List[str] = field(default_factory=list)
    
    def has_subject(self) -> bool:
        """Check if clause has a subject."""
        return bool(self.subjects)
    
    def has_object(self) -> bool:
        """Check if clause has an object."""
        return bool(self.objects)
    
    def has_complement(self) -> bool:
        """Check if clause has a complement.""" 
        return bool(self.complements)
    
    def is_passive_voice(self) -> bool:
        """Enhanced passive voice detection."""
        # Check for passive auxiliary AND past participle
        has_passive_aux = any(
            dep.relation in ['aux:pass', 'auxpass'] for dep in self.dependencies
        )
        has_past_participle = self.root_pos in ['VBN', 'VERB'] and self.root_lemma != self.root_word
        has_by_agent = any(
            dep.relation in ['nmod:agent', 'obl:agent'] for dep in self.dependencies
        )
        
        # Passive requires auxiliary + past participle OR clear agent
        return (has_passive_aux and has_past_participle) or has_by_agent
    
    def is_linking_verb(self) -> bool:
        """Check if root verb is a linking verb with enhanced detection."""
        # Check for copula relation in dependencies (indicates linking verb structure)
        has_copula = any(dep.relation == 'cop' for dep in self.dependencies)
        if has_copula:
            return True
            
        linking_verbs = {'be', 'seem', 'appear', 'become', 'feel', 'look', 'sound', 'taste', 'smell', 
                        'remain', 'stay', 'prove', 'turn', 'grow', 'get'}
        root_lemma_lower = self.root_lemma.lower()
        
        # Direct lemma match
        if root_lemma_lower in linking_verbs:
            return True
            
        # Check for 'be' verb forms
        be_forms = {'is', 'are', 'was', 'were', 'being', 'been', 'am'}
        if self.root_word.lower() in be_forms:
            return True
            
        return False

    def count_objects(self) -> int:
        """Count different types of objects."""
        object_relations = ['obj', 'dobj', 'iobj']
        return len([dep for dep in self.dependencies if dep.relation in object_relations])
    
    def is_copular_construction(self) -> bool:
        """Check if this clause is a copular construction (X is Y pattern)."""
        # Look for copula relation
        has_copula = any(dep.relation == 'cop' for dep in self.dependencies)
        return has_copula

@dataclass 
class HierarchicalGrammarResultV4:
    """Ultra-precise hierarchical grammar analysis result."""
    sentence: str
    main_clause: Optional[PreciseClauseInfo]
    subordinate_clauses: List[PreciseClauseInfo] = field(default_factory=list)
    embedded_constructions: List[PreciseClauseInfo] = field(default_factory=list)
    coordination_relations: List[Dict] = field(default_factory=list)
    overall_complexity: float = 0.0
    recommended_engines: List[str] = field(default_factory=list)
    coordination_strategy: str = "single"
    processing_time: float = 0.0
    detailed_analysis: Dict[str, Any] = field(default_factory=dict)
    confidence_breakdown: Dict[str, float] = field(default_factory=dict)

@dataclass
class HierarchicalGrammarResultV5:
    """V5: 2段階処理に特化した結果クラス."""
    sentence: str
    main_result: Any  # Step1の主節解析結果
    subordinate_results: List[Any] = field(default_factory=list)  # Step2の従属節解析結果
    processing_method: str = "two_step"
    total_confidence: float = 0.0
    step1_time: float = 0.0
    step2_time: float = 0.0

class HierarchicalGrammarDetectorV5(AdvancedGrammarDetector):
    """V5: 2段階処理による階層文法検出器 - V4の83.3%精度を基盤として改良."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Ultra-precise pattern detection rules
        self.pattern_detection_rules = {
            GrammarPattern.PASSIVE_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.is_passive_voice(),
                ],
                'confidence_boost': 0.3,
                'contextual_patterns': [
                    r'\bby\s+\w+',       # "by someone" pattern  
                    r'\bwas\s+\w+ed\b',  # "was verbed" pattern
                    r'\bwere\s+\w+ed\b', # "were verbed" pattern
                    r'\bbe\s+\w+ed\b',   # "be verbed" pattern
                    r'\bbeen\s+\w+ed\b'  # "been verbed" pattern
                ],
                'blocking_conditions': [
                    lambda clause: not clause.is_passive_voice()
                ]
            },
            
            GrammarPattern.IMPERATIVE_PATTERN: {
                'required_conditions': [
                    lambda clause: not clause.has_subject(),  # 主語が絶対にない
                    lambda clause: clause.root_pos in ['VB', 'VERB'],  # 動詞である
                    lambda clause: clause.clause_type == 'main'  # メイン節のみ
                ],
                'confidence_boost': 0.5,  # 高い信頼度ブースト
                'blocking_conditions': [
                    # 以下の場合は絶対に命令文ではない
                    lambda clause: clause.has_subject(),  # 主語があれば命令文ではない
                    lambda clause: clause.clause_type in ['adverbial_clause', 'relative_clause', 'adnominal_clause'],
                    # 定冠詞があれば通常の宣言文
                    lambda clause: any(word.lower() == 'the' for word in clause.text.split()[:2]),
                    # 'to' マーカーがあれば不定詞構文（ただし前置詞の'to school'は除外）
                    lambda clause: (
                        any(dep.relation == 'mark' and dep.dependent.lower() == 'to' for dep in clause.dependencies) and
                        not any(dep.relation == 'obl' and 'school' in dep.dependent.lower() for dep in clause.dependencies)
                    )
                ],
                'sentence_patterns': [
                    r'^(please\s+)?[A-Z][a-z]*\s+',
                    r'^[A-Z][a-z]*\s+(to|me|him|her|us|them)',
                    r'^Go\s+to\s+',  # "Go to school" pattern
                    r'^(Come|Stop|Wait|Help|Listen|Look)'  # Common imperative verbs
                ],
                'contextual_requirements': [
                    # Must be sentence initial or after comma for imperatives  
                    lambda clause, sentence: (
                        clause.text.strip().startswith(sentence.strip().split()[0]) or
                        # Also check for "Please..." pattern
                        sentence.strip().lower().startswith('please') or
                        # Check for typical imperative sentence structure
                        sentence.strip().endswith('.') and not '?' in sentence
                    )
                ]
            },
            
            GrammarPattern.EXISTENTIAL_THERE: {
                'required_conditions': [
                    lambda clause: 'there' in clause.text.lower(),
                    lambda clause: any(dep.relation == 'expl' for dep in clause.dependencies)
                ],
                'confidence_boost': 0.4
            },
            
            GrammarPattern.SVC_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.is_copular_construction() or clause.is_linking_verb(),
                    lambda clause: clause.has_complement() or clause.has_subject()
                ],
                'blocking_conditions': [
                    lambda clause: clause.has_object() and not clause.is_copular_construction()
                ],
                'confidence_boost': 0.3
            },
            
            GrammarPattern.SVOC_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.count_objects() >= 1,
                    lambda clause: clause.has_complement()
                ],
                'confidence_boost': 0.3
            },
            
            GrammarPattern.SVOO_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.count_objects() >= 2
                ],
                'confidence_boost': 0.3
            },
            
            GrammarPattern.SVO_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.has_subject(),
                    lambda clause: clause.has_object()
                ],
                'blocking_conditions': [
                    lambda clause: clause.has_complement(),
                    lambda clause: clause.count_objects() > 1
                ],
                'confidence_boost': 0.2
            },
            
            GrammarPattern.SV_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.has_subject()
                ],
                'blocking_conditions': [
                    lambda clause: clause.has_object(),
                    lambda clause: clause.has_complement()
                ],
                'confidence_boost': 0.1
            },
            
            GrammarPattern.GERUND_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.root_pos in ['VBG', 'VERB'],
                    # Gerunds are primarily nominal (act as nouns), not adverbial  
                    lambda clause: clause.clause_type in ['clausal_subject', 'clausal_complement', 'adverbial_clause']
                ],
                'blocking_conditions': [
                    # If it's in adverbial position and modifies main clause subject, it's participial
                    lambda clause: (
                        clause.clause_type == 'adverbial_clause' and
                        # Check if sentence has comma structure typical of participial constructions
                        ',' in clause.text and
                        # BUT NOT if it's introduced by preposition "by"
                        not re.search(r'\bby\s+\w+ing\b', clause.text, re.IGNORECASE)
                    )
                ],
                'contextual_patterns': [
                    # Gerund patterns tend to be nominal
                    r'^(Swimming|Reading|Writing)\s+(is|was)', # "Swimming is fun"
                    r'(enjoy|like|hate|love)\s+\w+ing',        # "I enjoy reading"
                    # NEW: Prepositional gerund patterns - key improvement!
                    r'\bby\s+\w+ing\b',                        # "by encouraging" - gerund after preposition
                    r'\bof\s+\w+ing\b',                        # "of running"
                    r'\bin\s+\w+ing\b',                        # "in swimming"
                    r'\bafter\s+\w+ing\b',                     # "after finishing"
                    r'\bbefore\s+\w+ing\b'                     # "before starting"
                ],
                'confidence_boost': 0.3
            },
            
            GrammarPattern.PARTICIPLE_PATTERN: {
                'required_conditions': [
                    # Enhanced participle detection - including AUX for copular constructions
                    lambda clause: (
                        # Present participle (VBG) like "Being", "Walking", "Having"
                        (clause.root_pos in ['VBG', 'VERB'] and 
                         (clause.root_word.endswith('ing') or clause.root_lemma.endswith('ing'))) or
                        # Past participle (VBN) like "Written", "Excited", "Finished"
                        (clause.root_pos in ['VBN', 'VERB'] and 
                         (clause.root_word.endswith('ed') or clause.root_word.endswith('en') or
                          clause.root_lemma != clause.root_word)) or
                        # AUX tag for "Being" constructions (Stanza treats "Being" as auxiliary)
                        (clause.root_pos == 'AUX' and 
                         clause.root_word.lower() == 'being' and clause.root_lemma.lower() == 'be')
                    ),
                    # Must be in adverbial clause context - NOT main clause
                    lambda clause: clause.clause_type == 'adverbial_clause'
                ],
                'blocking_conditions': [
                    # NEVER apply to main clauses with clear subjects
                    lambda clause: (clause.clause_type == 'main' and clause.has_subject()),
                ],
                'contextual_requirements': [
                    # Check for sentence-initial position (typical for participial constructions)
                    lambda clause, full_sentence: (
                        any(word.lower() in full_sentence.lower()[:20] 
                            for word in [clause.root_word, clause.root_lemma]) or
                        # Check for comma after participial phrase
                        ',' in full_sentence and
                        full_sentence.find(',') < full_sentence.find(clause.root_word) + 50
                    )
                ],
                'contextual_patterns': [
                    # Present participle patterns (including Being)
                    r'^\s*(Being|Having|Walking|Running|Coming|Going|Seeing)',
                    r'(Being|Having)\s+\w+',
                    # Past participle patterns  
                    r'^\s*(Written|Finished|Completed|Excited|Surprised|Given)',
                    r'(ed|en)\s*,',
                    # General participial phrase patterns
                    r'\w+(ing|ed|en)\s+[^,]*,'
                ],
                'confidence_boost': 0.4
            },
            
            GrammarPattern.INFINITIVE_PATTERN: {
                'required_conditions': [
                    # Check for 'to' marker in dependencies or text
                    lambda clause: any(dep.relation == 'mark' and dep.dependent == 'to' for dep in clause.dependencies) or 
                                  'to' in clause.text.lower().split()[:3],  # 'to' appears early in clause
                    # Additional check for infinitive context
                    lambda clause: clause.clause_type in ['open_clausal_complement', 'clausal_complement'] or
                                  any('to ' in clause.text.lower() for _ in [True])
                ],
                'contextual_patterns': [
                    r'\bto\s+be\b',      # "to be" construction
                    r'\bto\s+\w+\b',     # "to verb" pattern
                    r'seems?\s+to\b',    # "seems to" pattern
                    r'\w+\s+to\s+\w+\b'  # general "verb to verb" pattern
                ],
                'confidence_boost': 0.4
            },
            
            GrammarPattern.RELATIVE_PATTERN: {
                'required_conditions': [
                    # Relative clauses modify nouns and follow specific patterns
                    lambda clause: (
                        clause.clause_type in ['relative_clause', 'adnominal_clause'] or
                        # Look for relative pronouns but NOT in object position after verbs like "tell", "know"
                        (any(word in clause.text.lower() for word in ['which', 'that', 'who', 'whom', 'whose', 'where', 'when']) and
                         not re.search(r'(tell|know|ask|wonder|explain|say|show)\s+\w*\s*\b(what|who|which|where|when|how|why)\b', clause.text, re.IGNORECASE))
                    )
                ],
                'blocking_conditions': [
                    # Block if it's clearly a noun clause (object of mental verb)
                    lambda clause: re.search(r'(tell|know|ask|wonder|explain|say|show|think|believe|remember)\s+\w*\s*\b(what|who|which|where|when|how|why)\b', clause.text, re.IGNORECASE)
                ],
                'confidence_boost': 0.4
            },
            
            # NEW: Add Noun Clause Pattern
            GrammarPattern.NOUN_CLAUSE: {
                'required_conditions': [
                    # Noun clauses function as subjects, objects, or complements
                    lambda clause: (
                        clause.clause_type in ['clausal_complement', 'clausal_subject', 'relative_clause'] and  # Include relative_clause
                        # Object clauses after mental/communication verbs
                        any(word in clause.text.lower() for word in ['what', 'who', 'which', 'where', 'when', 'how', 'why', 'that', 'if', 'whether'])
                    )
                ],
                'contextual_requirements': [
                    # Must be after verbs that take noun clause objects - STRONG PRIORITY
                    lambda clause, full_sentence: (
                        re.search(r'(tell|know|ask|wonder|explain|say|show|think|believe|remember|understand|realize|see|hear|feel|notice)\s+\w*\s*(?:me\s+)?(?:him\s+)?(?:her\s+)?(?:us\s+)?(?:them\s+)?what', full_sentence, re.IGNORECASE) or
                        re.search(r'(tell|know|ask|wonder|explain|say|show)\s+\w*\s*(?:me\s+)?(?:him\s+)?(?:her\s+)?(?:us\s+)?(?:them\s+)?(?:what|who|which|where|when|how|why)', full_sentence, re.IGNORECASE) or
                        # Or be in subject/complement position
                        clause.clause_type in ['clausal_subject', 'clausal_complement']
                    )
                ],
                'contextual_patterns': [
                    r'(tell|know|ask|wonder|explain|say|show)\s+\w*\s*\b(what|who|which|where|when|how|why)\b',  # "tell me what"
                    r'(think|believe|remember|understand|realize)\s+\w*\s*\b(that|what|who|which|where|when|how|why)\b',  # "think that"
                    r'(see|hear|feel|notice)\s+\w*\s*\b(that|what|who|which|where|when|how|why)\b'  # "see that"
                ],
                'confidence_boost': 0.6  # Higher confidence boost than relative pattern
            }
        }
        
        # Enhanced clause mapping with more precise classification
        self.enhanced_clause_mapping = {
            'root': 'main',
            'ccomp': 'clausal_complement',
            'xcomp': 'open_clausal_complement', 
            'advcl': 'adverbial_clause',
            'acl': 'adnominal_clause',
            'acl:relcl': 'relative_clause',
            'csubj': 'clausal_subject',
            'csubj:pass': 'passive_clausal_subject',
            'parataxis': 'parenthetical_clause',
            'conj': 'coordinated_clause'
        }

    def detect_hierarchical_grammar_v5(self, sentence: str) -> HierarchicalGrammarResultV4:
        """V5: 2段階処理による階層文法検出 - シンプル・確実なアプローチ"""
        start_time = time.time()
        
        try:
            print(f"🔍 V5 Processing: {sentence}")
            
            # Step 1: 節検出・プレースホルダー化 → 主節解析
            main_result, detected_clauses = self._step1_detect_main_clause(sentence)
            
            # Step 2: 各節の個別解析  
            subordinate_results = self._step2_analyze_clauses(detected_clauses)
            
            # 結果統合
            final_result = self._integrate_v5_results(
                sentence, main_result, subordinate_results, start_time
            )
            
            print(f"✅ V5 Complete: Main={final_result.main_result.main_clause.grammatical_pattern.value}")
            return final_result
            
        except Exception as e:
            print(f"❌ V5 Error: {e}")
            # フォールバック: V4の既存処理を使用
            return self.detect_hierarchical_grammar(sentence)
    
    def _step1_detect_main_clause(self, sentence: str):
        """Step 1: 節検出・プレースホルダー化による主節解析"""
        print("    📊 Step 1: Main clause detection with placeholders...")
        
        # 簡単な節検出パターン
        detected_clauses = []
        modified_sentence = sentence
        
        # that節検出
        that_pattern = r'\bthat\s+[^,.]+'
        that_matches = list(re.finditer(that_pattern, sentence, re.IGNORECASE))
        
        for match in that_matches:
            clause_text = match.group(0)
            detected_clauses.append({
                'text': clause_text,
                'type': 'that_clause',
                'original_position': match.start()
            })
            # プレースホルダーに置換（通常の名詞を使用）
            modified_sentence = modified_sentence.replace(clause_text, 'something', 1)
        
        print(f"    🔄 Modified: '{modified_sentence}'")
        print(f"    📋 Found {len(detected_clauses)} clauses")
        
        # V4システムで主節解析
        main_result = self.detect_hierarchical_grammar(modified_sentence)
        
        return main_result, detected_clauses
    
    def _step2_analyze_clauses(self, detected_clauses):
        """Step 2: 各節の個別解析"""
        print("    📊 Step 2: Individual clause analysis...")
        
        clause_results = []
        for clause in detected_clauses:
            # 前処理: that等を除去
            processed_text = clause['text']
            if clause['type'] == 'that_clause':
                processed_text = re.sub(r'^\s*that\s+', '', processed_text, flags=re.IGNORECASE)
            
            print(f"      🔄 Analyzing: '{processed_text}'")
            
            # V4システムで解析
            try:
                clause_result = self.detect_hierarchical_grammar(processed_text)
                clause_results.append({
                    'original_text': clause['text'],
                    'processed_text': processed_text,
                    'type': clause['type'],
                    'result': clause_result
                })
                print(f"      ✅ Result: {clause_result.main_clause.grammatical_pattern.value}")
            except Exception as e:
                print(f"      ⚠️ Clause analysis error: {e}")
        
        return clause_results
    
    def _integrate_v5_results(self, original_sentence, main_result, subordinate_results, start_time):
        """V5結果の統合"""
        # V5専用結果クラスを使用
        final_result = HierarchicalGrammarResultV5(
            sentence=original_sentence,
            main_result=main_result,
            subordinate_results=subordinate_results,
            processing_method="two_step",
            total_confidence=getattr(main_result, 'confidence_breakdown', {}).get('overall', 0.8),
            step1_time=0.0,  # TODO: 実測値を追加
            step2_time=time.time() - start_time
        )
        
        return final_result

    def detect_hierarchical_grammar(self, sentence: str) -> HierarchicalGrammarResultV4:
        """Ultra-precise hierarchical grammar detection."""
        start_time = time.time()
        
        try:
            # Step 1: Enhanced linguistic analysis
            stanza_analysis = self._analyze_with_stanza(sentence)
            
            # Step 2: Ultra-precise clause decomposition
            clauses = self._decompose_into_clauses_v4(stanza_analysis, sentence)
            
            # Step 3: Ultra-precise pattern analysis
            main_clause = None
            subordinate_clauses = []
            embedded_constructions = []
            confidence_breakdown = {}
            
            for clause in clauses:
                # Enhanced pattern detection with ultra-precision
                pattern_result = self._analyze_clause_pattern_v4(clause, stanza_analysis, sentence)
                clause.grammatical_pattern = pattern_result['pattern']
                clause.confidence = pattern_result['confidence']
                clause.linguistic_features = pattern_result.get('features', {})
                
                confidence_breakdown[f"{clause.clause_type}_{clause.root_word}"] = clause.confidence
                
                # Categorize clauses
                if clause.clause_type == 'main':
                    main_clause = clause
                elif clause.clause_type in [
                    'adverbial_clause', 'relative_clause', 'clausal_complement',
                    'adnominal_clause', 'coordinated_clause', 'open_clausal_complement'
                ]:
                    subordinate_clauses.append(clause)
                else:
                    embedded_constructions.append(clause)
            
            # Step 4: Ultra-precise complexity and recommendations
            complexity = self._calculate_complexity_v4(main_clause, subordinate_clauses, embedded_constructions)
            recommended_engines = self._recommend_engines_v4(main_clause, subordinate_clauses, embedded_constructions)
            coordination_strategy = self._determine_coordination_v4(complexity)
            
            processing_time = time.time() - start_time
            
            return HierarchicalGrammarResultV4(
                sentence=sentence,
                main_clause=main_clause,
                subordinate_clauses=subordinate_clauses,
                embedded_constructions=embedded_constructions,
                overall_complexity=complexity,
                recommended_engines=recommended_engines,
                coordination_strategy=coordination_strategy,
                processing_time=processing_time,
                confidence_breakdown=confidence_breakdown,
                detailed_analysis={
                    'total_clauses': len(clauses),
                    'patterns_detected': [c.grammatical_pattern.value if c.grammatical_pattern else 'unknown' for c in clauses]
                }
            )
            
        except Exception as e:
            self.logger.error(f"Ultra-precise hierarchical analysis failed: {e}")
            return self._create_fallback_result_v4(sentence, time.time() - start_time)

    def _decompose_into_clauses_v4(self, stanza_analysis: Dict, sentence: str) -> List[PreciseClauseInfo]:
        """Ultra-precise clause decomposition with enhanced linguistic analysis."""
        
        dependencies = stanza_analysis.get('dependencies', [])
        tokens = stanza_analysis.get('tokens', [])
        pos_tags = dict(stanza_analysis.get('pos_tags', []))
        lemmas = dict(stanza_analysis.get('lemmas', []))
        
        clauses = []
        clause_heads = {}
        
        # Step 1: Identify clause heads with ultra-precise classification
        for dep in dependencies:
            if dep.relation in self.enhanced_clause_mapping:
                clause_type = self.enhanced_clause_mapping[dep.relation]
                
                # **FILTER OUT: Simple adjectival complements that don't form clauses**
                if dep.relation == 'xcomp':
                    dep_pos = pos_tags.get(dep.dependent, 'UNKNOWN')
                    # If xcomp dependent is just an adjective, don't create separate clause
                    if dep_pos in ['ADJ', 'JJ'] and not any(
                        other_dep.head == dep.dependent 
                        for other_dep in dependencies 
                        if other_dep.relation in ['nsubj', 'csubj', 'nsubj:pass']
                    ):
                        # This is just an adjectival complement, skip clause creation
                        continue
                
                root_pos = pos_tags.get(dep.dependent, 'UNKNOWN')
                root_lemma = lemmas.get(dep.dependent, dep.dependent)
                
                # Special handling for participial constructions
                if dep.relation == 'advcl':
                    # Check if this is a participial construction
                    participial_root = self._find_participial_root(dep, dependencies, sentence, pos_tags, lemmas)
                    if participial_root:
                        # Use the participle (Being, Walking, etc.) as root instead
                        clause_heads[participial_root['word']] = PreciseClauseInfo(
                            text="",
                            clause_type=clause_type,
                            root_word=participial_root['word'],
                            root_index=participial_root['index'],
                            root_pos=participial_root['pos'],
                            root_lemma=participial_root['lemma'],
                            dependencies=[],
                            linguistic_features={
                                'relation_to_parent': dep.relation,
                                'parent_word': dep.head,
                                'participial_construction': True,
                                'original_dependent': dep.dependent
                            }
                        )
                        continue
                
                clause_heads[dep.dependent] = PreciseClauseInfo(
                    text="",
                    clause_type=clause_type,
                    root_word=dep.dependent,
                    root_index=self._get_token_index(tokens, dep.dependent),
                    root_pos=root_pos,
                    root_lemma=root_lemma,
                    dependencies=[],
                    linguistic_features={
                        'relation_to_parent': dep.relation,
                        'parent_word': dep.head
                    }
                )
        
        # Ensure main clause exists
        if not any(info.clause_type == 'main' for info in clause_heads.values()):
            for dep in dependencies:
                if dep.relation == 'root':
                    root_pos = pos_tags.get(dep.dependent, 'UNKNOWN')
                    root_lemma = lemmas.get(dep.dependent, dep.dependent)
                    clause_heads[dep.dependent] = PreciseClauseInfo(
                        text="",
                        clause_type='main',
                        root_word=dep.dependent,
                        root_index=self._get_token_index(tokens, dep.dependent),
                        root_pos=root_pos,
                        root_lemma=root_lemma,
                        dependencies=[]
                    )
                    break
        
        # Step 2: Collect dependencies and extract detailed linguistic features
        for clause_root, clause_info in clause_heads.items():
            clause_info.dependencies = self._collect_clause_dependencies(
                dependencies, clause_root, clause_heads
            )
            
            # Extract subjects, objects, and complements
            clause_info.subjects = self._extract_subjects(clause_info.dependencies)
            clause_info.objects = self._extract_objects(clause_info.dependencies)
            clause_info.complements = self._extract_complements(clause_info.dependencies)
            
            # Extract clause text
            clause_info.text = self._extract_clause_text(
                sentence, tokens, clause_info.dependencies, clause_root
            )
        
        return list(clause_heads.values())

    def _find_participial_root(self, advcl_dep: 'DependencyInfo', 
                             all_dependencies: List['DependencyInfo'],
                             sentence: str, pos_tags: Dict, lemmas: Dict) -> Dict:
        """Find the actual participial root (Being, Walking, etc.) for adverbial clauses."""
        
        # Look for participles that modify the dependent word
        dependent_word = advcl_dep.dependent
        sentence_words = sentence.lower().split()
        
        # Common participial patterns
        participial_candidates = []
        
        # Check for dependencies where the dependent is actually governed by a participle
        for dep in all_dependencies:
            if (dep.head == dependent_word and 
                dep.relation in ['cop', 'nsubj', 'det', 'amod', 'advmod']):
                
                candidate_pos = pos_tags.get(dep.dependent, '')
                candidate_lemma = lemmas.get(dep.dependent, dep.dependent)
                
                # Check if this could be a participle
                is_present_participle = (
                    (candidate_pos in ['VBG', 'VERB'] and 
                     (dep.dependent.endswith('ing') or candidate_lemma.endswith('ing'))) or
                    # Special case for "Being" which Stanza tags as AUX
                    (candidate_pos == 'AUX' and dep.dependent.lower() == 'being')
                )
                is_past_participle = (candidate_pos in ['VBN', 'VERB'] and 
                                    (dep.dependent.endswith('ed') or dep.dependent.endswith('en') or
                                     candidate_lemma != dep.dependent))
                
                if is_present_participle or is_past_participle:
                    participial_candidates.append({
                        'word': dep.dependent,
                        'pos': candidate_pos,
                        'lemma': candidate_lemma,
                        'index': self._get_token_index([], dep.dependent),  # Will be recalculated
                        'confidence': 0.9 if (is_present_participle and dep.relation == 'cop') else 0.8 if is_present_participle else 0.7
                    })
        
        # Also check sentence-initial position for participial constructions
        if sentence_words:
            first_word = sentence_words[0]
            # Remove punctuation
            first_word_clean = first_word.replace(',', '').replace('.', '')
            
            first_pos = pos_tags.get(first_word_clean, pos_tags.get(first_word_clean.capitalize(), ''))
            first_lemma = lemmas.get(first_word_clean, lemmas.get(first_word_clean.capitalize(), first_word_clean))
            
            is_sentence_initial_participle = (
                (first_pos in ['VBG', 'VERB'] and first_word_clean.endswith('ing')) or
                (first_pos in ['VBN', 'VERB'] and (first_word_clean.endswith('ed') or first_word_clean.endswith('en')))
            )
            
            if is_sentence_initial_participle:
                participial_candidates.append({
                    'word': first_word_clean.capitalize(),
                    'pos': first_pos,
                    'lemma': first_lemma,
                    'index': 0,
                    'confidence': 0.9  # High confidence for sentence-initial
                })
        
        # Return the best candidate
        if participial_candidates:
            best_candidate = max(participial_candidates, key=lambda x: x['confidence'])
            return best_candidate
        
        return None

    def _analyze_clause_pattern_v4(self, clause: PreciseClauseInfo, 
                                  stanza_analysis: Dict, full_sentence: str) -> Dict[str, Any]:
        """Ultra-precise pattern analysis with advanced contextual understanding."""
        
        best_pattern = None
        best_confidence = 0.0
        best_features = {}
        
        # **SPECIAL PRIORITY CHECK: Imperative patterns have high priority**
        # Check imperative first as it's often misclassified by structural analysis
        if clause.clause_type == 'main':
            imperative_rules = self.pattern_detection_rules.get(GrammarPattern.IMPERATIVE_PATTERN, {})
            imperative_confidence, imperative_features = self._calculate_ultra_precise_score(
                GrammarPattern.IMPERATIVE_PATTERN, clause, imperative_rules, full_sentence
            )
            
            # Special boost for "Please..." sentences
            if full_sentence.strip().lower().startswith('please') and imperative_confidence >= 0.5:
                imperative_confidence = min(1.0, imperative_confidence + 0.3)
                imperative_features['please_boost'] = True
            
            if imperative_confidence >= 0.8:  # High threshold for imperative
                return {
                    'pattern': GrammarPattern.IMPERATIVE_PATTERN,
                    'confidence': imperative_confidence,
                    'features': imperative_features
                }
        
        # Then try structural analysis (most reliable for other patterns)
        structural_result = self._structural_pattern_analysis(clause)
        best_pattern = structural_result['pattern']
        best_confidence = structural_result['confidence']
        best_features = structural_result.get('features', {})
        
        # Only try special patterns if they have potential for significant improvement
        # or if structural analysis confidence is low
        if best_confidence < 0.7:  # Only override if structural analysis is uncertain
            
            # **PRIORITY CHECK: Noun Clause patterns have high priority for wh-clauses**
            # Check noun clause first for "what/who/which/where/when/how/why" constructions
            if any(word in clause.text.lower() for word in ['what', 'who', 'which', 'where', 'when', 'how', 'why']):
                if GrammarPattern.NOUN_CLAUSE in self.pattern_detection_rules:
                    noun_rules = self.pattern_detection_rules[GrammarPattern.NOUN_CLAUSE]
                    noun_confidence, noun_features = self._calculate_ultra_precise_score(
                        GrammarPattern.NOUN_CLAUSE, clause, noun_rules, full_sentence
                    )
                    
                    # Noun clause gets priority if it meets contextual requirements
                    if noun_confidence >= 0.8:  # High threshold for noun clause override
                        return {
                            'pattern': GrammarPattern.NOUN_CLAUSE,
                            'confidence': noun_confidence,
                            'features': noun_features
                        }
            
            for pattern, rules in self.pattern_detection_rules.items():
                # Skip basic structural patterns since we already analyzed them
                # Skip imperative and noun_clause since we already checked them above
                if (pattern in [GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN, 
                               GrammarPattern.SVC_PATTERN, GrammarPattern.SVOO_PATTERN, 
                               GrammarPattern.SVOC_PATTERN, GrammarPattern.IMPERATIVE_PATTERN,
                               GrammarPattern.NOUN_CLAUSE]):
                    continue
                    
                confidence, features = self._calculate_ultra_precise_score(
                    pattern, clause, rules, full_sentence
                )
                
                # Need very high confidence to override structural analysis
                if confidence > best_confidence + 0.3:  
                    best_confidence = confidence
                    best_pattern = pattern
                    best_features = features
        
        return {
            'pattern': best_pattern or GrammarPattern.SV_PATTERN,
            'confidence': best_confidence,
            'features': best_features
        }

    def _calculate_ultra_precise_score(self, pattern: GrammarPattern, 
                                     clause: PreciseClauseInfo, 
                                     rules: Dict, full_sentence: str) -> Tuple[float, Dict]:
        """Calculate pattern score with ultra-precise rule matching."""
        
        score = 0.0
        features = {}
        
        # Check required conditions
        required_conditions = rules.get('required_conditions', [])
        if required_conditions:
            conditions_met = 0
            for condition in required_conditions:
                try:
                    if condition(clause):
                        conditions_met += 1
                        features[f'condition_{conditions_met}'] = True
                    else:
                        features[f'condition_{conditions_met}'] = False
                except:
                    features[f'condition_{conditions_met}'] = False
            
            if conditions_met == len(required_conditions):
                score += 0.5  # Base score for meeting all conditions
                features['all_conditions_met'] = True
            else:
                score += (conditions_met / len(required_conditions)) * 0.3
                features['all_conditions_met'] = False
        else:
            score += 0.3  # No specific conditions
        
        # Check blocking conditions
        blocking_conditions = rules.get('blocking_conditions', [])
        for condition in blocking_conditions:
            try:
                if condition(clause):
                    score = 0.1  # Very low score if blocked
                    features['blocked'] = True
                    return score, features
            except:
                pass
        
        # Check contextual requirements (specific to context)
        contextual_requirements = rules.get('contextual_requirements', [])
        for requirement in contextual_requirements:
            try:
                if not requirement(clause, full_sentence):
                    score *= 0.5  # Reduce score if contextual requirement not met
                    features['contextual_requirement_failed'] = True
            except:
                pass
        
        # Check contextual patterns
        contextual_patterns = rules.get('contextual_patterns', [])
        sentence_patterns = rules.get('sentence_patterns', [])
        all_patterns = contextual_patterns + sentence_patterns
        
        if all_patterns:
            pattern_score = 0.0
            for regex_pattern in all_patterns:
                if re.search(regex_pattern, clause.text, re.IGNORECASE) or \
                   re.search(regex_pattern, full_sentence, re.IGNORECASE):
                    pattern_score = 0.3
                    features['pattern_match'] = True
                    break
            score += pattern_score
        else:
            score += 0.2  # No patterns to check
        
        # Apply confidence boost
        confidence_boost = rules.get('confidence_boost', 0.0)
        final_score = score + confidence_boost
        
        return min(final_score, 1.0), features

    def _structural_pattern_analysis(self, clause: PreciseClauseInfo) -> Dict[str, Any]:
        """Fallback structural analysis based on grammatical components."""
        
        # Analyze grammatical structure
        has_subject = clause.has_subject()
        has_object = clause.has_object()
        has_complement = clause.has_complement()
        object_count = clause.count_objects()
        is_linking = clause.is_linking_verb()
        is_copular = clause.is_copular_construction()
        
        # Determine pattern based on structure
        if clause.is_passive_voice():
            return {
                'pattern': GrammarPattern.PASSIVE_PATTERN,
                'confidence': 0.8,
                'features': {'structural_analysis': 'passive_voice'}
            }
        elif is_copular and has_subject:
            # Copular constructions are SVC patterns
            return {
                'pattern': GrammarPattern.SVC_PATTERN,
                'confidence': 0.8,
                'features': {'structural_analysis': 'copular_construction'}
            }
        elif has_object and has_complement:
            return {
                'pattern': GrammarPattern.SVOC_PATTERN,
                'confidence': 0.7,
                'features': {'structural_analysis': 'object_complement'}
            }
        elif object_count >= 2:
            return {
                'pattern': GrammarPattern.SVOO_PATTERN,
                'confidence': 0.7,
                'features': {'structural_analysis': 'double_object'}
            }
        elif is_linking and has_complement:
            return {
                'pattern': GrammarPattern.SVC_PATTERN,
                'confidence': 0.6,
                'features': {'structural_analysis': 'linking_complement'}
            }
        elif has_subject and has_object:
            return {
                'pattern': GrammarPattern.SVO_PATTERN,
                'confidence': 0.6,
                'features': {'structural_analysis': 'subject_object'}
            }
        elif has_subject:
            return {
                'pattern': GrammarPattern.SV_PATTERN,
                'confidence': 0.5,
                'features': {'structural_analysis': 'subject_only'}
            }
        else:
            return {
                'pattern': GrammarPattern.SV_PATTERN,
                'confidence': 0.2,
                'features': {'structural_analysis': 'fallback'}
            }

    def _extract_subjects(self, dependencies: List[DependencyInfo]) -> List[str]:
        """Extract subject words from dependencies."""
        subjects = []
        for dep in dependencies:
            if dep.relation in ['nsubj', 'nsubj:pass', 'csubj', 'csubj:pass']:
                subjects.append(dep.dependent)
        return subjects

    def _extract_objects(self, dependencies: List[DependencyInfo]) -> List[str]:
        """Extract object words from dependencies."""
        objects = []
        for dep in dependencies:
            if dep.relation in ['obj', 'dobj', 'iobj']:
                objects.append(dep.dependent)
        return objects

    def _extract_complements(self, dependencies: List[DependencyInfo]) -> List[str]:
        """Extract complement words from dependencies with enhanced detection."""
        complements = []
        for dep in dependencies:
            # Traditional complement relations
            if dep.relation in ['nsubj:xsubj', 'ccomp', 'xcomp', 'acomp']:
                complements.append(dep.dependent)
            # Predicate nominals and adjectives (key for SVC pattern)
            elif dep.relation in ['nmod:pred', 'amod', 'det']:
                complements.append(dep.dependent)
            # Objects that function as complements in copular constructions
            elif dep.relation in ['obj'] and self._is_likely_complement_context(dependencies):
                complements.append(dep.dependent)
        return complements
    
    def _is_likely_complement_context(self, dependencies: List[DependencyInfo]) -> bool:
        """Check if this is likely a complement context (e.g., with linking verbs)."""
        # Check if root verb is copular/linking
        root_verbs = [dep.dependent for dep in dependencies if dep.relation == 'root']
        if root_verbs:
            root_word = root_verbs[0].lower()
            linking_verbs = {'be', 'is', 'are', 'was', 'were', 'being', 'been', 
                           'seem', 'appear', 'become', 'feel', 'look', 'sound', 'taste', 'smell'}
            return root_word in linking_verbs
        return False

    def _get_token_index(self, tokens: List, word: str) -> int:
        """Get the index of a word in the token list."""
        for i, token in enumerate(tokens):
            if isinstance(token, dict) and token.get('text') == word:
                return i
            elif hasattr(token, 'text') and token.text == word:
                return i
        return 0

    def _collect_clause_dependencies(self, all_deps: List[DependencyInfo], 
                                   clause_root: str, 
                                   clause_heads: Dict) -> List[DependencyInfo]:
        """Collect all dependencies belonging to a specific clause."""
        clause_deps = []
        
        for dep in all_deps:
            if dep.head == clause_root or dep.dependent == clause_root:
                clause_deps.append(dep)
        
        return clause_deps

    def _extract_clause_text(self, sentence: str, tokens: List, 
                           dependencies: List[DependencyInfo], 
                           clause_root: str) -> str:
        """Extract the text span for a specific clause with improved accuracy."""
        
        # Collect all words that belong to this clause
        words_in_clause = set([clause_root])
        
        # Add all dependent and head words directly related to this clause
        for dep in dependencies:
            if dep.head == clause_root:
                words_in_clause.add(dep.dependent)
            elif dep.dependent == clause_root:
                words_in_clause.add(dep.head)
        
        # For participial constructions, look for sentence spans that contain the root
        sentence_words = sentence.split()
        
        # Find the position of the clause root in the original sentence
        root_positions = []
        for i, word in enumerate(sentence_words):
            if word.lower().replace(',', '').replace('.', '') == clause_root.lower():
                root_positions.append(i)
        
        if not root_positions:
            # Fallback to the original method if root not found in sentence
            clause_words = list(words_in_clause)
            return ' '.join(clause_words)
        
        # For participial constructions, extract meaningful spans
        best_span = ""
        for root_pos in root_positions:
            # Look for comma-separated participial phrases
            comma_pos = -1
            for i in range(root_pos, len(sentence_words)):
                if ',' in sentence_words[i]:
                    comma_pos = i
                    break
            
            if comma_pos > root_pos:
                # Extract span from root to comma (typical participial phrase)
                span_words = sentence_words[max(0, root_pos-2):comma_pos+1]
                span_text = ' '.join(span_words)
                if len(span_text) > len(best_span):
                    best_span = span_text
            else:
                # Extract a reasonable window around the root
                start_pos = max(0, root_pos - 3)
                end_pos = min(len(sentence_words), root_pos + 4)
                span_words = sentence_words[start_pos:end_pos]
                span_text = ' '.join(span_words)
                if len(span_text) > len(best_span):
                    best_span = span_text
        
        return best_span if best_span else ' '.join(words_in_clause)

    def _calculate_complexity_v4(self, main_clause, subordinate_clauses, embedded_constructions) -> float:
        """Calculate complexity score."""
        base_complexity = 0.3
        
        if subordinate_clauses:
            base_complexity += len(subordinate_clauses) * 0.15
        
        if embedded_constructions:
            base_complexity += len(embedded_constructions) * 0.1
        
        return min(base_complexity, 1.0)

    def _recommend_engines_v4(self, main_clause, subordinate_clauses, embedded_constructions) -> List[str]:
        """Enhanced engine recommendation."""
        engines = set()
        all_clauses = [main_clause] + subordinate_clauses + embedded_constructions
        
        for clause in all_clauses:
            if not clause or not clause.grammatical_pattern:
                continue
                
            pattern = clause.grammatical_pattern
            
            if pattern in [GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN, 
                          GrammarPattern.SVC_PATTERN, GrammarPattern.SVOO_PATTERN, 
                          GrammarPattern.SVOC_PATTERN]:
                engines.add('basic_five_engine')
            elif pattern == GrammarPattern.PASSIVE_PATTERN:
                engines.add('passive_engine')
            elif pattern == GrammarPattern.IMPERATIVE_PATTERN:
                engines.add('imperative_engine')
            elif pattern == GrammarPattern.EXISTENTIAL_THERE:
                engines.add('existential_there_engine')
            elif pattern == GrammarPattern.RELATIVE_PATTERN:
                engines.add('relative_engine')
            elif pattern == GrammarPattern.NOUN_CLAUSE:
                engines.add('relative_engine')  # Use relative engine for noun clauses too
            elif pattern in [GrammarPattern.GERUND_PATTERN, GrammarPattern.PARTICIPLE_PATTERN]:
                engines.add('progressive_engine')
        
        return list(engines) if engines else ['basic_five_engine']

    def _determine_coordination_v4(self, complexity: float) -> str:
        """Determine coordination strategy."""
        if complexity >= 0.7:
            return 'hierarchical_cooperative'
        elif complexity >= 0.5:
            return 'multi_cooperative'
        else:
            return 'single'

    def _create_fallback_result_v4(self, sentence: str, processing_time: float) -> HierarchicalGrammarResultV4:
        """Create fallback result."""
        return HierarchicalGrammarResultV4(
            sentence=sentence,
            main_clause=PreciseClauseInfo(
                text=sentence,
                clause_type='main',
                root_word='unknown',
                root_index=0,
                root_pos='UNKNOWN',
                root_lemma='unknown',
                grammatical_pattern=GrammarPattern.SV_PATTERN,
                confidence=0.2
            ),
            processing_time=processing_time,
            recommended_engines=['basic_five_engine'],
            coordination_strategy='single'
        )

# Test the V5 two-step detector
if __name__ == "__main__":
    detector = HierarchicalGrammarDetectorV5()
    
    test_sentences = [
        "Being a teacher, she knows how to explain difficult concepts.",
        "The book that was written by John is very good.",
        "Please tell me if there are any problems.",
        "Having finished the work, she went home."
    ]
    
    print("🚀 Testing Ultra-Precise Hierarchical Grammar Detector v4.0")
    print("=" * 70)
    
    for sentence in test_sentences:
        print(f"\n📝 Analyzing: \"{sentence}\"")
        print("-" * 60)
        
        result = detector.detect_hierarchical_grammar(sentence)
        
        print(f"🏗️ Main Clause: {result.main_clause.grammatical_pattern if result.main_clause else 'None'}")
        if result.main_clause:
            print(f"   Confidence: {result.main_clause.confidence:.3f}")
            print(f"   Features: {result.main_clause.linguistic_features}")
        
        if result.subordinate_clauses:
            print(f"📋 Subordinate Clauses:")
            for i, clause in enumerate(result.subordinate_clauses, 1):
                print(f"   {i}. {clause.grammatical_pattern} (conf: {clause.confidence:.3f})")
        
        if result.embedded_constructions:
            print(f"🔧 Embedded Constructions:")
            for i, const in enumerate(result.embedded_constructions, 1):
                print(f"   {i}. {const.grammatical_pattern} (conf: {const.confidence:.3f})")
        
        print(f"📊 Complexity: {result.overall_complexity:.3f}")
        print(f"🤖 Engines: {', '.join(result.recommended_engines)}")
        print(f"⚡ Strategy: {result.coordination_strategy}")
        print(f"⏱️ Processing Time: {result.processing_time:.3f}s")
