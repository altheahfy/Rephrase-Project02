"""
Hierarchical Grammar Detector v4.0
超高精度階層文法検出システム

主要改善点:
1. 受動態の過剰検出を修正
2. 主節パターン（SVC, SVOC, SVO）の精密区別
3. 分詞構文と動名詞の正確な識別
4. より精密な文脈分析による誤分類の削減
5. 依存関係の深い解析による構造理解の向上

目標精度: 90%+
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

class HierarchicalGrammarDetectorV4(AdvancedGrammarDetector):
    """Ultra-precise hierarchical grammar detector with 90%+ accuracy target."""
    
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
                    lambda clause: clause.clause_type in ['adverbial_clause', 'relative_clause'],
                    # 定冠詞があれば通常の宣言文
                    lambda clause: any(word.lower() == 'the' for word in clause.text.split()[:2])
                ],
                'sentence_patterns': [
                    r'^(please\s+)?[A-Z][a-z]*\s+',
                    r'^[A-Z][a-z]*\s+(to|me|him|her|us|them)'
                ],
                'contextual_requirements': [
                    # Must be sentence initial or after comma for imperatives  
                    lambda clause, sentence: clause.text.strip().startswith(sentence.strip().split()[0])
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
                    lambda clause: clause.clause_type == 'adverbial_clause'
                ],
                'contextual_patterns': [
                    r'^(Being|Having|Seeing|Knowing)',
                    r'ing\s+[a-z]'
                ],
                'confidence_boost': 0.3
            },
            
            GrammarPattern.PARTICIPLE_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.root_pos in ['VBN', 'VBG', 'VERB'],
                    lambda clause: clause.clause_type == 'adverbial_clause'
                ],
                'contextual_patterns': [
                    r'^(Having\s+\w+ed|Written|Finished)',
                    r'(ed|en)\s*,'
                ],
                'confidence_boost': 0.3
            },
            
            GrammarPattern.INFINITIVE_PATTERN: {
                'required_conditions': [
                    lambda clause: any(dep.relation == 'mark' and dep.dependent == 'to' for dep in clause.dependencies)
                ],
                'confidence_boost': 0.4
            },
            
            GrammarPattern.RELATIVE_PATTERN: {
                'required_conditions': [
                    lambda clause: clause.clause_type == 'relative_clause'
                ],
                'confidence_boost': 0.4
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
                
                root_pos = pos_tags.get(dep.dependent, 'UNKNOWN')
                root_lemma = lemmas.get(dep.dependent, dep.dependent)
                
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

    def _analyze_clause_pattern_v4(self, clause: PreciseClauseInfo, 
                                  stanza_analysis: Dict, full_sentence: str) -> Dict[str, Any]:
        """Ultra-precise pattern analysis with advanced contextual understanding."""
        
        best_pattern = None
        best_confidence = 0.0
        best_features = {}
        
        # First, always try structural analysis (most reliable)
        structural_result = self._structural_pattern_analysis(clause)
        best_pattern = structural_result['pattern']
        best_confidence = structural_result['confidence']
        best_features = structural_result.get('features', {})
        
        # Only try special patterns if they have potential for significant improvement
        # or if structural analysis confidence is low
        if best_confidence < 0.7:  # Only override if structural analysis is uncertain
            for pattern, rules in self.pattern_detection_rules.items():
                # Skip basic structural patterns since we already analyzed them
                if (pattern in [GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN, 
                               GrammarPattern.SVC_PATTERN, GrammarPattern.SVOO_PATTERN, 
                               GrammarPattern.SVOC_PATTERN]):
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
        """Extract the text span for a specific clause."""
        words_in_clause = set([clause_root])
        for dep in dependencies:
            words_in_clause.add(dep.head)
            words_in_clause.add(dep.dependent)
        
        clause_words = sorted(words_in_clause)
        if clause_words:
            return ' '.join(clause_words)
        return sentence

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

# Test the ultra-precise detector
if __name__ == "__main__":
    detector = HierarchicalGrammarDetectorV4()
    
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
