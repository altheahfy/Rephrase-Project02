"""
Hierarchical Grammar Detector v3.0
最高精度を追求した階層文法検出システム

主な改善点:
1. より精密なStanza依存関係分析
2. 改良された節分解アルゴリズム
3. 特殊構文（受動態、命令法、分詞構文）の高精度検出
4. 文脈を考慮した文法パターン認識
"""

import stanza
import spacy
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re

# Import existing pattern definitions
from advanced_grammar_detector import (
    GrammarPattern, GrammarDetectionResult, AdvancedGrammarDetector, 
    DependencyInfo
)

@dataclass
class EnhancedClauseInfo:
    """Enhanced clause information with detailed linguistic analysis."""
    text: str
    clause_type: str  # main, adverbial_clause, relative_clause, etc.
    root_word: str
    root_index: int
    root_pos: str
    dependencies: List[DependencyInfo] = field(default_factory=list)
    word_positions: List[Tuple[int, int]] = field(default_factory=list)  # (start, end) positions
    grammatical_pattern: Optional[GrammarPattern] = None
    confidence: float = 0.0
    linguistic_features: Dict[str, Any] = field(default_factory=dict)
    
    def get_subjects(self) -> List[str]:
        """Extract subject words from dependencies."""
        subjects = []
        for dep in self.dependencies:
            if dep.relation in ['nsubj', 'nsubj:pass', 'csubj', 'csubj:pass']:
                subjects.append(dep.dependent)
        return subjects
    
    def get_objects(self) -> List[str]:
        """Extract object words from dependencies."""
        objects = []
        for dep in self.dependencies:
            if dep.relation in ['obj', 'dobj', 'iobj', 'ccomp', 'xcomp']:
                objects.append(dep.dependent)
        return objects
    
    def has_passive_auxiliary(self) -> bool:
        """Check if clause has passive auxiliary verbs."""
        for dep in self.dependencies:
            if dep.relation in ['aux:pass', 'auxpass']:
                return True
        return False
    
    def is_imperative_structure(self) -> bool:
        """Check if clause has imperative structure."""
        # Imperative typically has no explicit subject
        subjects = self.get_subjects()
        if not subjects and self.root_pos in ['VERB', 'VB', 'VBP']:
            return True
        return False

@dataclass
class HierarchicalGrammarResultV3:
    """Enhanced hierarchical grammar analysis result."""
    sentence: str
    main_clause: Optional[EnhancedClauseInfo]
    subordinate_clauses: List[EnhancedClauseInfo] = field(default_factory=list)
    embedded_constructions: List[EnhancedClauseInfo] = field(default_factory=list)
    coordination_relations: List[Dict] = field(default_factory=list)
    overall_complexity: float = 0.0
    recommended_engines: List[str] = field(default_factory=list)
    coordination_strategy: str = "single"
    processing_time: float = 0.0
    detailed_analysis: Dict[str, Any] = field(default_factory=dict)

class HierarchicalGrammarDetectorV3(AdvancedGrammarDetector):
    """Enhanced hierarchical grammar detector with maximum precision."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Enhanced clause relation mapping with more precise categories
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
        
        # Enhanced pattern detection with contextual rules
        self.contextual_pattern_rules = {
            GrammarPattern.PASSIVE_PATTERN: {
                'required_features': ['aux:pass', 'nsubj:pass'],
                'alternative_features': [['auxpass'], ['agent']],
                'pos_requirements': {'root': ['VERB', 'VBN']},
                'confidence_base': 0.95
            },
            GrammarPattern.IMPERATIVE_PATTERN: {
                'required_features': [],
                'blocking_features': ['nsubj'],  # No explicit subject
                'pos_requirements': {'root': ['VERB', 'VB', 'VBP']},
                'sentence_start_patterns': [r'^(please\s+)?[A-Z][a-z]*\s+'],
                'confidence_base': 0.9
            },
            GrammarPattern.EXISTENTIAL_THERE: {
                'required_features': ['expl'],
                'required_words': ['there'],
                'pos_requirements': {'root': ['VERB', 'VBZ', 'VBP']},
                'confidence_base': 0.95
            },
            GrammarPattern.GERUND_PATTERN: {
                'pos_requirements': {'root': ['VERB', 'VBG']},
                'dependency_patterns': ['advcl'],
                'confidence_base': 0.85
            },
            GrammarPattern.PARTICIPLE_PATTERN: {
                'pos_requirements': {'root': ['VERB', 'VBN', 'VBG']},
                'dependency_patterns': ['advcl'],
                'confidence_base': 0.8
            },
            GrammarPattern.INFINITIVE_PATTERN: {
                'required_features': ['mark'],
                'required_words': ['to'],
                'dependency_patterns': ['xcomp'],
                'confidence_base': 0.9
            }
        }
        
        # Clause-specific pattern preferences with priorities
        self.clause_pattern_priorities = {
            'main': [
                GrammarPattern.PASSIVE_PATTERN,
                GrammarPattern.IMPERATIVE_PATTERN,
                GrammarPattern.EXISTENTIAL_THERE,
                GrammarPattern.SVOO_PATTERN,
                GrammarPattern.SVOC_PATTERN,
                GrammarPattern.SVO_PATTERN,
                GrammarPattern.SVC_PATTERN,
                GrammarPattern.SV_PATTERN
            ],
            'adverbial_clause': [
                GrammarPattern.GERUND_PATTERN,
                GrammarPattern.PARTICIPLE_PATTERN,
                GrammarPattern.PASSIVE_PATTERN,
                GrammarPattern.SVO_PATTERN,
                GrammarPattern.SV_PATTERN
            ],
            'relative_clause': [
                GrammarPattern.RELATIVE_PATTERN,
                GrammarPattern.PASSIVE_PATTERN,
                GrammarPattern.SVO_PATTERN,
                GrammarPattern.SV_PATTERN
            ],
            'open_clausal_complement': [
                GrammarPattern.INFINITIVE_PATTERN,
                GrammarPattern.SVO_PATTERN,
                GrammarPattern.SV_PATTERN
            ]
        }

    def detect_hierarchical_grammar(self, sentence: str) -> HierarchicalGrammarResultV3:
        """Enhanced hierarchical grammar detection with maximum precision."""
        start_time = time.time()
        
        try:
            # Step 1: Enhanced linguistic analysis
            stanza_analysis = self._analyze_with_stanza(sentence)
            spacy_analysis = self._analyze_with_spacy(sentence)
            
            # Step 2: Enhanced clause decomposition
            clauses = self._decompose_into_clauses_v3(stanza_analysis, sentence)
            
            # Step 3: Contextual pattern analysis for each clause
            main_clause = None
            subordinate_clauses = []
            embedded_constructions = []
            
            for clause in clauses:
                # Enhanced pattern detection with context
                pattern_result = self._analyze_clause_pattern_v3(
                    clause, stanza_analysis, spacy_analysis, sentence
                )
                clause.grammatical_pattern = pattern_result['pattern']
                clause.confidence = pattern_result['confidence']
                clause.linguistic_features = pattern_result.get('features', {})
                
                # Categorize clauses
                if clause.clause_type == 'main':
                    main_clause = clause
                elif clause.clause_type in [
                    'adverbial_clause', 'relative_clause', 'clausal_complement',
                    'adnominal_clause', 'coordinated_clause'
                ]:
                    subordinate_clauses.append(clause)
                else:
                    embedded_constructions.append(clause)
            
            # Step 4: Enhanced complexity calculation
            complexity = self._calculate_enhanced_complexity(
                main_clause, subordinate_clauses, embedded_constructions
            )
            
            # Step 5: Precise engine recommendations
            recommended_engines = self._recommend_engines_v3(
                main_clause, subordinate_clauses, embedded_constructions
            )
            
            coordination_strategy = self._determine_coordination_v3(complexity)
            
            processing_time = time.time() - start_time
            
            return HierarchicalGrammarResultV3(
                sentence=sentence,
                main_clause=main_clause,
                subordinate_clauses=subordinate_clauses,
                embedded_constructions=embedded_constructions,
                overall_complexity=complexity,
                recommended_engines=recommended_engines,
                coordination_strategy=coordination_strategy,
                processing_time=processing_time,
                detailed_analysis={
                    'stanza_deps': len(stanza_analysis.get('dependencies', [])),
                    'clause_count': len(clauses),
                    'patterns_detected': [c.grammatical_pattern for c in clauses if c.grammatical_pattern]
                }
            )
            
        except Exception as e:
            self.logger.error(f"Enhanced hierarchical analysis failed: {e}")
            # Enhanced fallback
            return self._create_fallback_result(sentence, time.time() - start_time)

    def _decompose_into_clauses_v3(self, stanza_analysis: Dict, sentence: str) -> List[EnhancedClauseInfo]:
        """Enhanced clause decomposition with precise boundary detection."""
        
        dependencies = stanza_analysis.get('dependencies', [])
        tokens = stanza_analysis.get('tokens', [])
        pos_tags = dict(stanza_analysis.get('pos_tags', []))
        
        clauses = []
        clause_heads = {}
        
        # Step 1: Identify clause heads with enhanced classification
        for dep in dependencies:
            if dep.relation in self.enhanced_clause_mapping:
                clause_type = self.enhanced_clause_mapping[dep.relation]
                
                # Find token information
                root_pos = pos_tags.get(dep.dependent, 'UNKNOWN')
                
                clause_heads[dep.dependent] = EnhancedClauseInfo(
                    text="",  # Will be filled later
                    clause_type=clause_type,
                    root_word=dep.dependent,
                    root_index=self._get_token_index(tokens, dep.dependent),
                    root_pos=root_pos,
                    dependencies=[],
                    linguistic_features={
                        'relation_to_parent': dep.relation,
                        'parent_word': dep.head
                    }
                )
        
        # Ensure main clause exists
        if not any(info.clause_type == 'main' for info in clause_heads.values()):
            # Find the root verb
            for dep in dependencies:
                if dep.relation == 'root':
                    root_pos = pos_tags.get(dep.dependent, 'UNKNOWN')
                    clause_heads[dep.dependent] = EnhancedClauseInfo(
                        text="",
                        clause_type='main',
                        root_word=dep.dependent,
                        root_index=self._get_token_index(tokens, dep.dependent),
                        root_pos=root_pos,
                        dependencies=[]
                    )
                    break
        
        # Step 2: Assign dependencies to appropriate clauses
        for clause_root, clause_info in clause_heads.items():
            clause_info.dependencies = self._collect_clause_dependencies(
                dependencies, clause_root, clause_heads
            )
            
            # Extract clause text
            clause_info.text = self._extract_clause_text(
                sentence, tokens, clause_info.dependencies, clause_root
            )
        
        return list(clause_heads.values())

    def _analyze_clause_pattern_v3(self, clause: EnhancedClauseInfo, 
                                  stanza_analysis: Dict, spacy_analysis: Dict,
                                  full_sentence: str) -> Dict[str, Any]:
        """Enhanced pattern analysis with contextual understanding."""
        
        # Get clause-specific patterns based on clause type
        candidate_patterns = self.clause_pattern_priorities.get(
            clause.clause_type,
            list(self.contextual_pattern_rules.keys())
        )
        
        best_pattern = None
        best_confidence = 0.0
        best_features = {}
        
        for pattern in candidate_patterns:
            score, features = self._calculate_contextual_pattern_score(
                pattern, clause, stanza_analysis, spacy_analysis, full_sentence
            )
            
            if score > best_confidence:
                best_confidence = score
                best_pattern = pattern
                best_features = features
        
        # Fallback to basic pattern detection if no specific pattern matches well
        if best_confidence < 0.3:
            basic_result = self._detect_basic_clause_pattern(clause)
            best_pattern = basic_result['pattern']
            best_confidence = basic_result['confidence']
        
        return {
            'pattern': best_pattern or GrammarPattern.SV_PATTERN,
            'confidence': best_confidence,
            'features': best_features
        }

    def _calculate_contextual_pattern_score(self, pattern: GrammarPattern, 
                                          clause: EnhancedClauseInfo,
                                          stanza_analysis: Dict,
                                          spacy_analysis: Dict,
                                          full_sentence: str) -> Tuple[float, Dict]:
        """Calculate pattern score with full contextual analysis."""
        
        if pattern not in self.contextual_pattern_rules:
            return 0.0, {}
        
        rules = self.contextual_pattern_rules[pattern]
        score = 0.0
        features = {}
        
        # Base confidence
        base_confidence = rules.get('confidence_base', 0.5)
        
        # Check required features
        required_features = rules.get('required_features', [])
        feature_matches = 0
        
        for feature in required_features:
            if self._has_dependency_relation(clause.dependencies, feature):
                feature_matches += 1
                features[f'has_{feature}'] = True
            else:
                features[f'has_{feature}'] = False
        
        if required_features:
            feature_score = feature_matches / len(required_features)
            score += feature_score * 0.4
        else:
            score += 0.4  # No specific requirements
        
        # Check blocking features
        blocking_features = rules.get('blocking_features', [])
        blocked = False
        for feature in blocking_features:
            if self._has_dependency_relation(clause.dependencies, feature):
                blocked = True
                features[f'blocked_by_{feature}'] = True
                break
        
        if blocked:
            return 0.1, features  # Very low score if blocked
        
        # Check POS requirements
        pos_requirements = rules.get('pos_requirements', {})
        if pos_requirements:
            pos_score = 0.0
            for pos_type, allowed_tags in pos_requirements.items():
                if pos_type == 'root' and clause.root_pos in allowed_tags:
                    pos_score = 1.0
                    features['pos_match'] = True
                    break
            score += pos_score * 0.3
        else:
            score += 0.3
        
        # Check required words
        required_words = rules.get('required_words', [])
        if required_words:
            word_score = 0.0
            for word in required_words:
                if word.lower() in clause.text.lower():
                    word_score = 1.0
                    features[f'has_word_{word}'] = True
                    break
            score += word_score * 0.2
        else:
            score += 0.2
        
        # Check sentence patterns (for imperative detection)
        sentence_patterns = rules.get('sentence_start_patterns', [])
        if sentence_patterns:
            pattern_score = 0.0
            for regex_pattern in sentence_patterns:
                if re.match(regex_pattern, full_sentence.strip()):
                    pattern_score = 1.0
                    features['sentence_pattern_match'] = True
                    break
            score += pattern_score * 0.1
        else:
            score += 0.1
        
        # Special handling for specific patterns
        if pattern == GrammarPattern.PASSIVE_PATTERN:
            if clause.has_passive_auxiliary():
                score += 0.2
                features['passive_auxiliary'] = True
        
        elif pattern == GrammarPattern.IMPERATIVE_PATTERN:
            if clause.is_imperative_structure():
                score += 0.2
                features['imperative_structure'] = True
        
        return min(score * base_confidence, 1.0), features

    def _has_dependency_relation(self, dependencies: List[DependencyInfo], relation: str) -> bool:
        """Check if dependencies contain a specific relation."""
        return any(dep.relation == relation for dep in dependencies)

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
        
        # Add dependencies where this word is the head
        for dep in all_deps:
            if dep.head == clause_root:
                clause_deps.append(dep)
        
        # Add the root dependency
        for dep in all_deps:
            if dep.dependent == clause_root:
                clause_deps.append(dep)
        
        return clause_deps

    def _extract_clause_text(self, sentence: str, tokens: List, 
                           dependencies: List[DependencyInfo], 
                           clause_root: str) -> str:
        """Extract the text span for a specific clause."""
        # For now, use a simple approach - can be enhanced later
        words_in_clause = set([clause_root])
        for dep in dependencies:
            words_in_clause.add(dep.head)
            words_in_clause.add(dep.dependent)
        
        # Find the span in the original sentence
        clause_words = sorted(words_in_clause)
        if clause_words:
            return ' '.join(clause_words)
        return sentence

    def _detect_basic_clause_pattern(self, clause: EnhancedClauseInfo) -> Dict[str, Any]:
        """Fallback basic pattern detection for clauses."""
        
        subjects = clause.get_subjects()
        objects = clause.get_objects()
        
        if subjects and objects:
            if len(objects) > 1:
                return {'pattern': GrammarPattern.SVOO_PATTERN, 'confidence': 0.6}
            else:
                return {'pattern': GrammarPattern.SVO_PATTERN, 'confidence': 0.6}
        elif subjects:
            return {'pattern': GrammarPattern.SV_PATTERN, 'confidence': 0.5}
        else:
            return {'pattern': GrammarPattern.SV_PATTERN, 'confidence': 0.3}

    def _calculate_enhanced_complexity(self, main_clause, subordinate_clauses, embedded_constructions) -> float:
        """Calculate enhanced complexity score."""
        base_complexity = 0.3  # Base for any sentence
        
        # Add complexity for subordinate structures
        if subordinate_clauses:
            base_complexity += len(subordinate_clauses) * 0.15
        
        if embedded_constructions:
            base_complexity += len(embedded_constructions) * 0.1
        
        # Add complexity for difficult patterns
        all_clauses = [main_clause] + subordinate_clauses + embedded_constructions
        difficult_patterns = [
            GrammarPattern.PASSIVE_PATTERN,
            GrammarPattern.GERUND_PATTERN,
            GrammarPattern.PARTICIPLE_PATTERN
        ]
        
        for clause in all_clauses:
            if clause and clause.grammatical_pattern in difficult_patterns:
                base_complexity += 0.1
        
        return min(base_complexity, 1.0)

    def _recommend_engines_v3(self, main_clause, subordinate_clauses, embedded_constructions) -> List[str]:
        """Enhanced engine recommendation based on detected patterns."""
        
        engines = set()
        all_clauses = [main_clause] + subordinate_clauses + embedded_constructions
        
        for clause in all_clauses:
            if not clause or not clause.grammatical_pattern:
                continue
                
            pattern = clause.grammatical_pattern
            
            # Map patterns to engines
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

    def _determine_coordination_v3(self, complexity: float) -> str:
        """Determine coordination strategy based on complexity."""
        if complexity >= 0.7:
            return 'hierarchical_cooperative'
        elif complexity >= 0.5:
            return 'multi_cooperative'
        else:
            return 'single'

    def _create_fallback_result(self, sentence: str, processing_time: float) -> HierarchicalGrammarResultV3:
        """Create fallback result when analysis fails."""
        
        return HierarchicalGrammarResultV3(
            sentence=sentence,
            main_clause=EnhancedClauseInfo(
                text=sentence,
                clause_type='main',
                root_word='unknown',
                root_index=0,
                root_pos='UNKNOWN',
                grammatical_pattern=GrammarPattern.SV_PATTERN,
                confidence=0.2
            ),
            processing_time=processing_time,
            recommended_engines=['basic_five_engine'],
            coordination_strategy='single'
        )

# Test the enhanced detector
if __name__ == "__main__":
    detector = HierarchicalGrammarDetectorV3()
    
    test_sentences = [
        "Being a teacher, she knows how to explain difficult concepts.",
        "The book that was written by John is very good.",
        "Please tell me if there are any problems.",
        "Having finished the work, she went home."
    ]
    
    print("🚀 Testing Enhanced Hierarchical Grammar Detector v3.0")
    print("=" * 60)
    
    for sentence in test_sentences:
        print(f"\n📝 Analyzing: \"{sentence}\"")
        print("-" * 50)
        
        result = detector.detect_hierarchical_grammar(sentence)
        
        print(f"🏗️ Main Clause: {result.main_clause.grammatical_pattern if result.main_clause else 'None'}")
        print(f"   Confidence: {result.main_clause.confidence:.3f}" if result.main_clause else "")
        
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
