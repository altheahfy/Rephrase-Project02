#!/usr/bin/env python3
"""
Advanced Grammar Detection Engine v1.0
==================================

Precision-Focused Grammar Pattern Recognition System
- 95%+ accuracy target using Stanza + spaCy dual analysis
- Replaces primitive regex pattern matching with advanced NLP
- Provides detailed grammar construction analysis for multi-engine coordination
- Handles complex linguistic patterns with semantic understanding

Architecture:
1. Dual NLP Pipeline: Stanza (dependency parsing) + spaCy (entity/syntax)
2. Confidence Scoring: Multi-layer validation with accuracy metrics
3. Pattern Hierarchy: Primary → Secondary → Tertiary construction detection
4. Semantic Context: Meaning-aware pattern recognition beyond surface forms

Performance Target: 95-98% accuracy vs. current 70-80% regex-based system
"""

import stanza
import spacy
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
import logging
import time
import re
from collections import Counter

class GrammarPattern(Enum):
    """Comprehensive grammar pattern enumeration with priority levels."""
    
    # Core Five Patterns (Priority 1-5)
    SV_PATTERN = "sv_pattern"                    # Priority 1: S + V (intransitive)
    SVO_PATTERN = "svo_pattern"                  # Priority 2: S + V + O (transitive)
    SVC_PATTERN = "svc_pattern"                  # Priority 3: S + V + C (linking verb)
    SVOO_PATTERN = "svoo_pattern"                # Priority 4: S + V + O + O (ditransitive)
    SVOC_PATTERN = "svoc_pattern"                # Priority 5: S + V + O + C (complex transitive)
    
    # Advanced Constructions (Priority 6-18)
    GERUND_PATTERN = "gerund_pattern"            # Priority 6: Gerund constructions
    PARTICIPLE_PATTERN = "participle_pattern"    # Priority 7: Participle constructions
    INFINITIVE_PATTERN = "infinitive_pattern"    # Priority 8: Infinitive constructions
    RELATIVE_PATTERN = "relative_pattern"        # Priority 9: Relative clause constructions
    NOUN_CLAUSE = "noun_clause"                  # Priority 10: Noun clause constructions (NEW)
    CONJUNCTION_PATTERN = "conjunction_pattern"  # Priority 11: Conjunction constructions
    PASSIVE_PATTERN = "passive_pattern"          # Priority 12: Passive voice constructions
    COMPARATIVE_PATTERN = "comparative_pattern"  # Priority 13: Comparative constructions
    PERFECT_PROGRESSIVE = "perfect_progressive"  # Priority 14: Perfect progressive constructions
    INVERSION_PATTERN = "inversion_pattern"      # Priority 15: Inversion constructions
    IMPERATIVE_PATTERN = "imperative_pattern"    # Priority 16: Command sentences
    EXISTENTIAL_THERE = "existential_there"      # Priority 17: There + be constructions
    SUBJUNCTIVE_PATTERN = "subjunctive_pattern"  # Priority 18: Subjunctive constructions

@dataclass
class GrammarDetectionResult:
    """Detailed result from advanced grammar detection."""
    primary_pattern: GrammarPattern
    confidence: float
    secondary_patterns: List[GrammarPattern]
    linguistic_features: Dict[str, Any]
    complexity_score: float
    processing_time: float
    stanza_analysis: Dict[str, Any]
    spacy_analysis: Dict[str, Any]
    recommended_engines: List[str]
    coordination_strategy: str
    error: Optional[str] = None

@dataclass
class DependencyInfo:
    """Dependency parsing information."""
    head: str
    relation: str
    dependent: str
    position: int

@dataclass
class SemanticContext:
    """Semantic context analysis."""
    entities: List[str]
    noun_phrases: List[str]
    verb_phrases: List[str]
    prep_phrases: List[str]
    clause_types: List[str]

class AdvancedGrammarDetector:
    """
    High-precision grammar detection engine with dual NLP analysis.
    
    Uses Stanza for dependency parsing and spaCy for semantic analysis
    to achieve 95%+ accuracy in grammar pattern recognition.
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize dual NLP pipeline system."""
        self._setup_logging(log_level)
        self._initialize_nlp_pipelines()
        self._initialize_pattern_rules()
        
        # Performance tracking
        self.detection_count = 0
        self.total_processing_time = 0.0
        self.accuracy_samples = []
    
    def _setup_logging(self, level: str):
        """Configure logging for detection engine."""
        self.logger = logging.getLogger(f"{__name__}.AdvancedGrammarDetector")
        self.logger.setLevel(getattr(logging, level.upper()))
    
    def _initialize_nlp_pipelines(self):
        """Initialize Stanza and spaCy NLP pipelines."""
        try:
            # Initialize Stanza for dependency parsing
            self.logger.info("🚀 Initializing Stanza pipeline...")
            self.stanza_nlp = stanza.Pipeline(
                'en', 
                processors='tokenize,pos,lemma,depparse,ner',
                download_method=None,
                verbose=False
            )
            self.logger.info("✅ Stanza pipeline initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Stanza initialization failed: {e}")
            self.stanza_nlp = None
        
        try:
            # Initialize spaCy for semantic analysis
            self.logger.info("🚀 Initializing spaCy pipeline...")
            self.spacy_nlp = spacy.load("en_core_web_sm")
            self.logger.info("✅ spaCy pipeline initialized")
            
        except Exception as e:
            self.logger.error(f"❌ spaCy initialization failed: {e}")
            self.logger.info("💡 Install with: python -m spacy download en_core_web_sm")
            self.spacy_nlp = None
    
    def _initialize_pattern_rules(self):
        """Initialize advanced pattern recognition rules."""
        
        # Dependency pattern signatures for each grammar construction
        self.dependency_patterns = {
            GrammarPattern.SV_PATTERN: {
                'required_relations': ['nsubj'],
                'verb_types': ['VERB'],
                'exclude_relations': ['obj', 'iobj'],
                'confidence_base': 0.85
            },
            
            GrammarPattern.SVO_PATTERN: {
                'required_relations': ['nsubj', 'obj'],
                'verb_types': ['VERB'],
                'exclude_relations': ['iobj'],
                'confidence_base': 0.90
            },
            
            GrammarPattern.SVC_PATTERN: {
                'required_relations': ['nsubj'],
                'verb_types': ['VERB', 'AUX'],
                'linking_verbs': ['be', 'become', 'seem', 'appear', 'look', 'sound', 'feel', 'smell', 'taste'],
                'complement_relations': ['acomp', 'attr', 'xcomp', 'oprd', 'cop'],  # Added 'cop' for copula
                'confidence_base': 0.88
            },
            
            GrammarPattern.SVOO_PATTERN: {
                'required_relations': ['nsubj', 'obj', 'iobj'],
                'verb_types': ['VERB'],
                'confidence_base': 0.92
            },
            
            GrammarPattern.SVOC_PATTERN: {
                'required_relations': ['nsubj', 'obj'],
                'verb_types': ['VERB'],
                'complement_relations': ['xcomp', 'acomp'],
                'confidence_base': 0.87
            },
            
            GrammarPattern.PASSIVE_PATTERN: {
                'required_relations': ['nsubj:pass', 'nsubjpass'],  # Both forms
                'verb_forms': ['VBN'],
                'aux_patterns': ['aux:pass', 'auxpass'],  # Both forms
                'confidence_base': 0.93
            },
            
            GrammarPattern.IMPERATIVE_PATTERN: {
                'sentence_start_verbs': True,
                'missing_subject': True,
                'verb_forms': ['VB', 'VERB'],
                'confidence_base': 0.89
            },
            
            GrammarPattern.EXISTENTIAL_THERE: {
                'existential_there': True,
                'required_relations': ['expl'],
                'be_verbs': ['be', 'is', 'are', 'was', 'were'],
                'confidence_base': 0.91
            },
            
            GrammarPattern.RELATIVE_PATTERN: {
                'relative_pronouns': ['who', 'whom', 'whose', 'which', 'that'],
                'required_relations': ['acl:relcl', 'relcl'],
                'confidence_base': 0.86
            },
            
            GrammarPattern.GERUND_PATTERN: {
                'verb_forms': ['VBG'],
                'noun_functions': ['nsubj', 'obj', 'pobj'],
                'confidence_base': 0.84
            },
            
            GrammarPattern.INFINITIVE_PATTERN: {
                'to_infinitive': True,
                'required_relations': ['xcomp', 'ccomp'],
                'confidence_base': 0.83
            }
        }
        
        # Semantic patterns for enhanced detection
        self.semantic_patterns = {
            'command_indicators': ['please', 'do not', "don't", 'never', 'always'],
            'question_indicators': ['?', 'who', 'what', 'when', 'where', 'why', 'how'],
            'conditional_indicators': ['if', 'unless', 'provided that', 'supposing'],
            'comparison_indicators': ['than', 'as...as', 'more', 'less', 'better', 'worse']
        }
        
        # Engine recommendation mapping
        self.engine_recommendations = {
            GrammarPattern.SV_PATTERN: ['basic_five_engine'],
            GrammarPattern.SVO_PATTERN: ['basic_five_engine'],
            GrammarPattern.SVC_PATTERN: ['basic_five_engine'],
            GrammarPattern.SVOO_PATTERN: ['basic_five_engine'],
            GrammarPattern.SVOC_PATTERN: ['basic_five_engine'],
            GrammarPattern.GERUND_PATTERN: ['gerund_engine'],
            GrammarPattern.PARTICIPLE_PATTERN: ['participle_engine'],
            GrammarPattern.INFINITIVE_PATTERN: ['infinitive_engine'],
            GrammarPattern.RELATIVE_PATTERN: ['relative_engine'],
            GrammarPattern.CONJUNCTION_PATTERN: ['conjunction_engine'],
            GrammarPattern.PASSIVE_PATTERN: ['passive_engine'],
            GrammarPattern.COMPARATIVE_PATTERN: ['comparative_engine'],
            GrammarPattern.PERFECT_PROGRESSIVE: ['perfect_progressive_engine'],
            GrammarPattern.INVERSION_PATTERN: ['inversion_engine'],
            GrammarPattern.IMPERATIVE_PATTERN: ['imperative_engine'],
            GrammarPattern.EXISTENTIAL_THERE: ['existential_there_engine'],
            GrammarPattern.SUBJUNCTIVE_PATTERN: ['subjunctive_engine']
        }
    
    def detect_grammar_pattern(self, sentence: str) -> GrammarDetectionResult:
        """
        Main detection method with 95%+ accuracy target.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            GrammarDetectionResult with detailed analysis
        """
        start_time = time.time()
        self.detection_count += 1
        
        try:
            # Phase 1: Dual NLP Analysis
            stanza_analysis = self._analyze_with_stanza(sentence)
            spacy_analysis = self._analyze_with_spacy(sentence)
            
            # Phase 2: Pattern Recognition
            pattern_scores = self._calculate_pattern_scores(sentence, stanza_analysis, spacy_analysis)
            
            # Phase 3: Primary Pattern Selection
            primary_pattern, confidence = self._select_primary_pattern(pattern_scores)
            
            # Phase 4: Secondary Pattern Detection
            secondary_patterns = self._detect_secondary_patterns(pattern_scores)
            
            # Phase 5: Linguistic Feature Extraction
            linguistic_features = self._extract_linguistic_features(stanza_analysis, spacy_analysis)
            
            # Phase 6: Complexity Analysis
            complexity_score = self._calculate_complexity(linguistic_features)
            
            # Phase 7: Engine Coordination Strategy
            recommended_engines = self._recommend_engines(primary_pattern, secondary_patterns)
            coordination_strategy = self._determine_coordination_strategy(primary_pattern, complexity_score)
            
            processing_time = time.time() - start_time
            self.total_processing_time += processing_time
            
            result = GrammarDetectionResult(
                primary_pattern=primary_pattern,
                confidence=confidence,
                secondary_patterns=secondary_patterns,
                linguistic_features=linguistic_features,
                complexity_score=complexity_score,
                processing_time=processing_time,
                stanza_analysis=stanza_analysis,
                spacy_analysis=spacy_analysis,
                recommended_engines=recommended_engines,
                coordination_strategy=coordination_strategy
            )
            
            self.logger.debug(f"🎯 Detection complete: {primary_pattern.value} (confidence: {confidence:.3f})")
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"❌ Detection error: {e}")
            
            return GrammarDetectionResult(
                primary_pattern=GrammarPattern.SV_PATTERN,  # Fallback
                confidence=0.0,
                secondary_patterns=[],
                linguistic_features={},
                complexity_score=0.0,
                processing_time=processing_time,
                stanza_analysis={},
                spacy_analysis={},
                recommended_engines=['basic_five_engine'],
                coordination_strategy='single_optimal',
                error=str(e)
            )
    
    def _analyze_with_stanza(self, sentence: str) -> Dict[str, Any]:
        """Analyze sentence with Stanza for dependency parsing."""
        if not self.stanza_nlp:
            return {}
        
        try:
            doc = self.stanza_nlp(sentence)
            
            # Extract dependency information
            dependencies = []
            pos_tags = []
            lemmas = []
            entities = []
            
            for sent in doc.sentences:
                for word in sent.words:
                    dependencies.append(DependencyInfo(
                        head=sent.words[word.head-1].text if word.head > 0 else 'ROOT',
                        relation=word.deprel,
                        dependent=word.text,
                        position=word.id
                    ))
                    pos_tags.append((word.text, word.pos))
                    lemmas.append((word.text, word.lemma))
            
            # Extract entities
            for ent in doc.entities:
                entities.append({
                    'text': ent.text,
                    'type': ent.type,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            
            return {
                'dependencies': dependencies,
                'pos_tags': pos_tags,
                'lemmas': lemmas,
                'entities': entities,
                'sentences': len(doc.sentences)
            }
            
        except Exception as e:
            self.logger.warning(f"⚠️ Stanza analysis failed: {e}")
            return {}
    
    def _analyze_with_spacy(self, sentence: str) -> Dict[str, Any]:
        """Analyze sentence with spaCy for semantic analysis."""
        if not self.spacy_nlp:
            return {}
        
        try:
            doc = self.spacy_nlp(sentence)
            
            # Extract semantic information
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            
            # Extract syntactic information
            pos_tags = [(token.text, token.pos_) for token in doc]
            dep_labels = [(token.text, token.dep_) for token in doc]
            
            # Extract phrase structures
            verb_phrases = []
            prep_phrases = []
            
            for token in doc:
                if token.pos_ == 'VERB':
                    # Simple verb phrase extraction
                    phrase = [token.text]
                    for child in token.children:
                        if child.dep_ in ['aux', 'auxpass', 'neg']:
                            phrase.insert(0, child.text)
                    verb_phrases.append(' '.join(phrase))
                
                elif token.pos_ == 'ADP':  # Preposition
                    # Simple prepositional phrase extraction
                    phrase = [token.text]
                    for child in token.children:
                        if child.dep_ == 'pobj':
                            phrase.append(child.text)
                            # Add modifiers
                            for grandchild in child.children:
                                if grandchild.dep_ in ['det', 'amod']:
                                    phrase.insert(-1, grandchild.text)
                    if len(phrase) > 1:
                        prep_phrases.append(' '.join(phrase))
            
            return {
                'noun_chunks': noun_chunks,
                'entities': entities,
                'pos_tags': pos_tags,
                'dep_labels': dep_labels,
                'verb_phrases': verb_phrases,
                'prep_phrases': prep_phrases,
                'tokens': len(doc),
                'sentences': len(list(doc.sents))
            }
            
        except Exception as e:
            self.logger.warning(f"⚠️ spaCy analysis failed: {e}")
            return {}
    
    def _calculate_pattern_scores(self, sentence: str, stanza_analysis: Dict, spacy_analysis: Dict) -> Dict[GrammarPattern, float]:
        """Calculate confidence scores for each grammar pattern."""
        scores = {}
        
        # Prepare analysis data
        dependencies = stanza_analysis.get('dependencies', [])
        pos_tags = dict(stanza_analysis.get('pos_tags', []))
        dep_relations = {dep.relation for dep in dependencies}
        
        # Special patterns get priority scoring first
        special_patterns = [
            GrammarPattern.IMPERATIVE_PATTERN,
            GrammarPattern.EXISTENTIAL_THERE,
            GrammarPattern.PASSIVE_PATTERN,
            GrammarPattern.SVC_PATTERN
        ]
        
        for pattern in special_patterns:
            if pattern == GrammarPattern.IMPERATIVE_PATTERN:
                scores[pattern] = self._check_imperative_pattern(sentence, dependencies, pos_tags)
            elif pattern == GrammarPattern.EXISTENTIAL_THERE:
                scores[pattern] = self._check_existential_there(sentence, dependencies)
            elif pattern == GrammarPattern.PASSIVE_PATTERN:
                scores[pattern] = self._check_passive_pattern(dependencies, pos_tags)
            elif pattern == GrammarPattern.SVC_PATTERN:
                scores[pattern] = self._check_linking_verb_pattern(dependencies, pos_tags, self.dependency_patterns[pattern])
        
        # If any special pattern has high confidence, suppress competing patterns
        max_special_score = max((scores.get(p, 0.0) for p in special_patterns), default=0.0)
        suppress_general = max_special_score > 0.8  # Increased threshold
        
        for pattern, rules in self.dependency_patterns.items():
            if pattern in special_patterns:
                continue  # Already processed
                
            score = 0.0
            base_confidence = rules.get('confidence_base', 0.5)
            
            # Apply suppression for general patterns when special pattern detected
            if suppress_general and pattern in [GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN, 
                                              GrammarPattern.SVOO_PATTERN, GrammarPattern.SVOC_PATTERN]:
                base_confidence *= 0.2  # Stronger suppression
            
            # SVC gets special treatment - less suppression when linking verb detected
            if pattern == GrammarPattern.SVC_PATTERN:
                # Don't suppress if we detect linking verb + complement
                linking_verb_detected = self._quick_check_linking_verb(sentence)
                if linking_verb_detected and suppress_general:
                    base_confidence = rules.get('confidence_base', 0.5) * 0.8  # Less suppression
            
            # Check required dependency relations
            required_relations = rules.get('required_relations', [])
            if required_relations:
                matches = sum(1 for rel in required_relations if rel in dep_relations)
                score += (matches / len(required_relations)) * base_confidence
            
            # Check excluded relations (penalty)
            exclude_relations = rules.get('exclude_relations', [])
            if exclude_relations:
                excludes = sum(1 for rel in exclude_relations if rel in dep_relations)
                if excludes == 0:
                    score += 0.1  # Bonus for clean pattern
                else:
                    score -= excludes * 0.05  # Penalty for conflicts
            
            scores[pattern] = max(0.0, min(1.0, score))
        
        return scores
    
    def _quick_check_linking_verb(self, sentence: str) -> bool:
        """Quick check for linking verbs in sentence."""
        linking_verbs = {'be', 'is', 'are', 'was', 'were', 'seem', 'seems', 'appear', 'appears', 
                        'look', 'looks', 'sound', 'sounds', 'feel', 'feels', 'taste', 'tastes',
                        'smell', 'smells', 'become', 'becomes'}
        words = sentence.lower().split()
        return any(word in linking_verbs for word in words)
    
    def _check_passive_pattern(self, dependencies: List, pos_tags: Dict) -> float:
        """Check for passive voice patterns."""
        score = 0.0
        
        # Strong indicators: passive subject relations (both Stanza forms)
        passive_subj_relations = {'nsubj:pass', 'nsubjpass'}
        if any(dep.relation in passive_subj_relations for dep in dependencies):
            score += 0.7
        
        # Strong indicators: passive auxiliary relations (both Stanza forms)
        passive_aux_relations = {'aux:pass', 'auxpass'}
        if any(dep.relation in passive_aux_relations for dep in dependencies):
            score += 0.6
        
        # Check for past participle (VBN) - essential for passive
        has_past_participle = any(pos_tags.get(dep.dependent, '') == 'VBN' for dep in dependencies)
        if has_past_participle:
            score += 0.4
        
        # Check for agent phrase with 'by' (classic passive indicator)
        agent_relations = {'obl:agent', 'agent'}
        if any(dep.relation in agent_relations for dep in dependencies):
            score += 0.3
        
        # Alternative check: look for "by + agent" pattern in dependencies
        has_by_case = any(dep.dependent.lower() == 'by' and dep.relation == 'case' for dep in dependencies)
        if has_by_case:
            score += 0.2
        
        return min(score, 1.0)
    
    def _check_linking_verb_pattern(self, dependencies: List, pos_tags: Dict, rules: Dict) -> float:
        """Check for linking verb constructions (SVC pattern)."""
        score = 0.0
        
        linking_verbs = rules.get('linking_verbs', [])
        
        # Find the root element
        root_element = None
        for dep in dependencies:
            if dep.relation == 'root':
                root_element = dep.dependent.lower()
                break
        
        # Check if root is a linking verb OR if there's a copula relationship
        has_copula = any(dep.relation == 'cop' for dep in dependencies)
        linking_verb_root = root_element and root_element in linking_verbs
        
        # Method 1: Traditional linking verb as root (e.g., "seems happy")
        if linking_verb_root:
            score += 0.8
        
        # Method 2: Copula relationship (e.g., "is a teacher" where 'is' is copula to 'teacher')
        elif has_copula:
            # Check if the copula is a form of 'be'
            copula_verbs = [dep for dep in dependencies if dep.relation == 'cop']
            for cop in copula_verbs:
                if cop.dependent.lower() in ['is', 'are', 'was', 'were', 'be', 'been', 'being', 'am']:
                    score += 0.8
                    break
        
        # Strong indicator: complement relations (multiple forms)
        complement_rels = rules.get('complement_relations', [])
        complement_matches = [dep for dep in dependencies if dep.relation in complement_rels]
        
        if complement_matches:
            score += 0.6  # Increased weight
            # Bonus for multiple complements
            if len(complement_matches) > 1:
                score += 0.2
            
            # Extra bonus if both linking verb/copula AND complement present
            if linking_verb_root or has_copula:
                score += 0.3
        
        # Additional SVC indicators based on complement types
        # Check for adjective complements
        adj_complement_relations = {'acomp', 'attr', 'oprd'}  # Added 'oprd' for spaCy
        adj_complements = [dep for dep in dependencies 
                          if dep.relation in adj_complement_relations and 
                          pos_tags.get(dep.dependent, '') in ['ADJ', 'JJ']]
        
        if adj_complements:
            score += 0.4
        
        # Check for noun phrase complements (including via copula)
        np_complement_relations = {'attr', 'oprd'}
        np_complements = [dep for dep in dependencies 
                         if dep.relation in np_complement_relations and 
                         pos_tags.get(dep.dependent, '') in ['NOUN', 'NN', 'NNS', 'PROPN']]
        
        # Special case: when copula links to noun, the noun complement is implicit
        if has_copula and not np_complements:
            # Find nouns that are root (common in copula constructions)
            root_nouns = [dep for dep in dependencies 
                         if dep.relation == 'root' and 
                         pos_tags.get(dep.dependent, '') in ['NOUN', 'NN', 'NNS', 'PROPN']]
            if root_nouns:
                score += 0.5  # Strong indicator of "is a teacher" type construction
                np_complements = root_nouns  # For consistency
        
        if np_complements:
            score += 0.3
        
        # Check for xcomp with adjectives (seems happy, looks good)
        xcomp_adj = [dep for dep in dependencies 
                    if dep.relation == 'xcomp' and 
                    pos_tags.get(dep.dependent, '') in ['ADJ', 'JJ']]
        
        if xcomp_adj and (linking_verb_root or has_copula):
            score += 0.5
        
        return min(score, 1.0)
    
    def _check_imperative_pattern(self, sentence: str, dependencies: List, pos_tags: Dict) -> float:
        """Check for imperative sentence patterns."""
        score = 0.0
        words = sentence.split()
        
        if not words:
            return 0.0
        
        # Strong indicator: sentence starts with base verb (VB) or imperative verb
        first_word = words[0]
        first_pos = pos_tags.get(first_word, '')
        if first_pos in ['VB', 'VERB']:
            score += 0.7  # Increased weight
        
        # Strong indicator: missing explicit subject (no nsubj relation)
        has_nsubj = any(dep.relation == 'nsubj' for dep in dependencies)
        if not has_nsubj:
            score += 0.4  # Increased weight
        
        # Command indicators boost score
        command_indicators = {'please', 'do', "don't", 'never', 'always', 'let'}
        if any(word.lower() in command_indicators for word in words):
            score += 0.3
        
        # Negative indicator: interrogative sentences are not imperatives
        if sentence.strip().endswith('?'):
            score -= 0.5
        
        # Strong pattern: Verb + Object structure without subject
        has_obj = any(dep.relation in ['obj', 'dobj'] for dep in dependencies)
        if (first_pos in ['VB', 'VERB'] and 
            not has_nsubj and 
            has_obj):
            score += 0.5
        
        # Context check: short, direct sentences are more likely commands
        if 2 <= len(words) <= 6:
            score += 0.2
        elif len(words) <= 2:
            score += 0.1
        
        # Additional pattern: Let-imperatives
        if words[0].lower() == 'let' and len(words) > 2:
            score += 0.4
        
        return min(score, 1.0)
    
    def _check_existential_there(self, sentence: str, dependencies: List) -> float:
        """Check for existential there constructions."""
        score = 0.0
        
        # Strong indicator: explicit existential there relation
        if any(dep.relation == 'expl' for dep in dependencies):
            score += 0.7
        
        # Check sentence pattern: "There + be verb"
        words = [w.lower() for w in sentence.split()]
        if len(words) >= 2 and words[0] == 'there':
            be_verbs = {'is', 'are', 'was', 'were', 'be', 'been', 'being'}
            if words[1] in be_verbs:
                score += 0.6
            # Handle contractions
            elif words[1] in {"'s", "'re"}:
                score += 0.6
        
        # Handle "There's" and "There're" as single tokens
        if sentence.lower().startswith(('there\'s', 'there\'re', 'there is', 'there are', 'there was', 'there were')):
            score += 0.6
        
        # Additional confirmation: typical existential structure
        # "There be + NP + (location/description)"
        if score > 0.5:
            # Check for noun phrase after be verb
            has_noun_after_be = False
            for i, word in enumerate(words):
                if word in {'is', 'are', 'was', 'were'} and i + 1 < len(words):
                    # Simple check for noun/determiner after be verb
                    next_words = words[i+1:i+3]
                    if any(w in {'a', 'an', 'the', 'some', 'many', 'several'} for w in next_words):
                        has_noun_after_be = True
                        break
            
            if has_noun_after_be:
                score += 0.2
        
        return min(score, 1.0)
    
    def _select_primary_pattern(self, pattern_scores: Dict[GrammarPattern, float]) -> Tuple[GrammarPattern, float]:
        """Select the primary grammar pattern with highest confidence."""
        if not pattern_scores:
            return GrammarPattern.SV_PATTERN, 0.5
        
        # Find pattern with highest score
        primary_pattern = max(pattern_scores.items(), key=lambda x: x[1])
        return primary_pattern[0], primary_pattern[1]
    
    def _detect_secondary_patterns(self, pattern_scores: Dict[GrammarPattern, float], threshold: float = 0.3) -> List[GrammarPattern]:
        """Detect secondary patterns above threshold."""
        secondary = []
        sorted_patterns = sorted(pattern_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Skip the primary pattern and include others above threshold
        for pattern, score in sorted_patterns[1:]:
            if score >= threshold:
                secondary.append(pattern)
        
        return secondary
    
    def _extract_linguistic_features(self, stanza_analysis: Dict, spacy_analysis: Dict) -> Dict[str, Any]:
        """Extract detailed linguistic features."""
        features = {}
        
        # Basic counts
        features['token_count'] = spacy_analysis.get('tokens', 0)
        features['sentence_count'] = max(stanza_analysis.get('sentences', 1), spacy_analysis.get('sentences', 1))
        features['dependency_count'] = len(stanza_analysis.get('dependencies', []))
        
        # Syntactic features
        features['noun_chunks'] = len(spacy_analysis.get('noun_chunks', []))
        features['verb_phrases'] = len(spacy_analysis.get('verb_phrases', []))
        features['prep_phrases'] = len(spacy_analysis.get('prep_phrases', []))
        features['entities'] = len(spacy_analysis.get('entities', []))
        
        # Dependency relations
        dep_relations = [dep.relation for dep in stanza_analysis.get('dependencies', [])]
        features['unique_relations'] = len(set(dep_relations))
        features['relation_counts'] = dict(Counter(dep_relations))
        
        # POS distribution
        pos_tags = [pos for _, pos in stanza_analysis.get('pos_tags', [])]
        features['pos_counts'] = dict(Counter(pos_tags))
        
        return features
    
    def _calculate_complexity(self, linguistic_features: Dict[str, Any]) -> float:
        """Calculate sentence complexity score (0-1 scale)."""
        complexity = 0.0
        
        # Length-based complexity
        token_count = linguistic_features.get('token_count', 0)
        complexity += min(token_count / 20, 0.3)  # Max 0.3 for length
        
        # Syntactic complexity
        unique_relations = linguistic_features.get('unique_relations', 0)
        complexity += min(unique_relations / 15, 0.3)  # Max 0.3 for relations
        
        # Phrase complexity
        total_phrases = (
            linguistic_features.get('noun_chunks', 0) +
            linguistic_features.get('verb_phrases', 0) +
            linguistic_features.get('prep_phrases', 0)
        )
        complexity += min(total_phrases / 10, 0.2)  # Max 0.2 for phrases
        
        # Entity complexity
        entities = linguistic_features.get('entities', 0)
        complexity += min(entities / 5, 0.2)  # Max 0.2 for entities
        
        return min(complexity, 1.0)
    
    def _recommend_engines(self, primary_pattern: GrammarPattern, secondary_patterns: List[GrammarPattern]) -> List[str]:
        """Recommend engines for processing based on detected patterns."""
        engines = set()
        
        # Primary engine
        primary_engines = self.engine_recommendations.get(primary_pattern, ['basic_five_engine'])
        engines.update(primary_engines)
        
        # Secondary engines
        for pattern in secondary_patterns:
            secondary_engines = self.engine_recommendations.get(pattern, [])
            engines.update(secondary_engines)
        
        return list(engines)
    
    def _determine_coordination_strategy(self, primary_pattern: GrammarPattern, complexity_score: float) -> str:
        """Determine optimal coordination strategy."""
        
        # High complexity patterns benefit from multi-engine coordination
        if complexity_score > 0.7:
            return 'multi_cooperative'
        
        # Special patterns that work well with specialists
        specialist_patterns = {
            GrammarPattern.IMPERATIVE_PATTERN,
            GrammarPattern.EXISTENTIAL_THERE,
            GrammarPattern.PASSIVE_PATTERN,
            GrammarPattern.SUBJUNCTIVE_PATTERN
        }
        
        if primary_pattern in specialist_patterns:
            return 'foundation_plus_specialist'
        
        # Default to balanced approach
        if complexity_score > 0.4:
            return 'foundation_plus_specialist'
        else:
            return 'single_optimal'
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        avg_processing_time = self.total_processing_time / max(self.detection_count, 1)
        
        return {
            'detection_count': self.detection_count,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': avg_processing_time,
            'stanza_available': self.stanza_nlp is not None,
            'spacy_available': self.spacy_nlp is not None
        }

# Test function for development
def test_advanced_grammar_detector():
    """Test the advanced grammar detector with various sentence types."""
    detector = AdvancedGrammarDetector()
    
    test_sentences = [
        "The cat sits on the mat.",           # SV with prepositional phrase
        "She gave him a book.",               # SVOO
        "There are many students here.",      # Existential there
        "Close the door.",                    # Imperative
        "The book was written by John.",      # Passive
        "Running is good exercise.",          # Gerund
        "She seems happy today."              # SVC
    ]
    
    for sentence in test_sentences:
        print(f"\n=== Analyzing: {sentence} ===")
        result = detector.detect_grammar_pattern(sentence)
        
        print(f"Primary Pattern: {result.primary_pattern.value}")
        print(f"Confidence: {result.confidence:.3f}")
        print(f"Secondary Patterns: {[p.value for p in result.secondary_patterns]}")
        print(f"Recommended Engines: {result.recommended_engines}")
        print(f"Coordination Strategy: {result.coordination_strategy}")
        print(f"Complexity Score: {result.complexity_score:.3f}")
        print(f"Processing Time: {result.processing_time:.3f}s")
        
        if result.error:
            print(f"Error: {result.error}")
    
    # Performance summary
    stats = detector.get_performance_stats()
    print(f"\n=== Performance Summary ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_advanced_grammar_detector()
