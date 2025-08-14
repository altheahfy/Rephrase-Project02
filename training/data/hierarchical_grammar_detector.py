#!/usr/bin/env python3
"""
Hierarchical Grammar Detection Engine v2.0
==========================================

Stanza-powered multi-clause, multi-pattern detection system.
Leverages Stanza's dependency parsing to detect ALL grammatical constructions
in complex sentences by analyzing each clause/phrase independently.

Architecture:
1. Dependency Tree Decomposition: Split sentence into clauses/phrases
2. Individual Pattern Analysis: Analyze each component separately  
3. Hierarchical Result Assembly: Combine all detected patterns
4. Multi-Engine Coordination: Recommend engines for each component

Target: 100% accuracy for both simple AND complex sentences
"""

import stanza
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
from advanced_grammar_detector import (
    AdvancedGrammarDetector, GrammarPattern, GrammarDetectionResult, 
    DependencyInfo
)

@dataclass
class ClauseInfo:
    """Information about a grammatical clause or phrase."""
    clause_type: str  # main, advcl, acl, xcomp, ccomp, etc.
    root_word: str
    dependencies: List[DependencyInfo]
    word_range: Tuple[int, int]  # start, end positions
    grammatical_pattern: Optional[GrammarPattern] = None
    confidence: float = 0.0
    
@dataclass
class HierarchicalGrammarResult:
    """Result containing all detected grammatical patterns in a complex sentence."""
    sentence: str
    main_clause: ClauseInfo
    subordinate_clauses: List[ClauseInfo]
    embedded_constructions: List[ClauseInfo]
    overall_complexity: float
    recommended_engines: List[str]
    coordination_strategy: str
    processing_time: float

class HierarchicalGrammarDetector(AdvancedGrammarDetector):
    """
    Advanced grammar detector that analyzes complex sentences by
    decomposing them into constituent clauses and phrases.
    """
    
    def __init__(self, log_level: str = "INFO"):
        super().__init__(log_level)
        self._initialize_clause_patterns()
        
    def _initialize_clause_patterns(self):
        """Initialize patterns for different clause types."""
        
        # Mapping of dependency relations to clause types
        self.clause_relation_mapping = {
            'root': 'main',
            'advcl': 'adverbial_clause',
            'acl:relcl': 'relative_clause', 
            'acl': 'adjectival_clause',
            'xcomp': 'infinitive_complement',
            'ccomp': 'clausal_complement',
            'conj': 'coordinate_clause'
        }
        
        # Patterns that are particularly relevant for different clause types
        self.clause_pattern_preferences = {
            'main': [GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN, 
                    GrammarPattern.SVC_PATTERN, GrammarPattern.SVOO_PATTERN, 
                    GrammarPattern.SVOC_PATTERN, GrammarPattern.IMPERATIVE_PATTERN,
                    GrammarPattern.PASSIVE_PATTERN, GrammarPattern.EXISTENTIAL_THERE],
                    
            'adverbial_clause': [GrammarPattern.GERUND_PATTERN, GrammarPattern.PARTICIPLE_PATTERN,
                               GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN],
                               
            'relative_clause': [GrammarPattern.RELATIVE_PATTERN, GrammarPattern.PASSIVE_PATTERN,
                              GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN],
                              
            'infinitive_complement': [GrammarPattern.INFINITIVE_PATTERN, GrammarPattern.SV_PATTERN],
            
            'clausal_complement': [GrammarPattern.SV_PATTERN, GrammarPattern.SVO_PATTERN,
                                 GrammarPattern.EXISTENTIAL_THERE]
        }
    
    def detect_hierarchical_grammar(self, sentence: str) -> HierarchicalGrammarResult:
        """
        Main method for hierarchical grammar detection.
        Decomposes sentence into clauses and analyzes each separately.
        """
        import time
        start_time = time.time()
        
        try:
            # Step 1: Get Stanza analysis
            stanza_analysis = self._analyze_with_stanza(sentence)
            dependencies = stanza_analysis.get('dependencies', [])
            
            # Step 2: Decompose into clauses
            clauses = self._decompose_into_clauses(dependencies, sentence)
            
            # Step 3: Analyze each clause separately
            main_clause = None
            subordinate_clauses = []
            embedded_constructions = []
            
            for clause in clauses:
                # Analyze grammatical pattern for this clause
                pattern_result = self._analyze_clause_pattern(clause, stanza_analysis)
                clause.grammatical_pattern = pattern_result['pattern']
                clause.confidence = pattern_result['confidence']
                
                if clause.clause_type == 'main':
                    main_clause = clause
                elif clause.clause_type in ['adverbial_clause', 'relative_clause', 'clausal_complement']:
                    subordinate_clauses.append(clause)
                else:
                    embedded_constructions.append(clause)
            
            # Step 4: Calculate overall complexity
            complexity = self._calculate_hierarchical_complexity(
                main_clause, subordinate_clauses, embedded_constructions
            )
            
            # Step 5: Recommend engines and coordination strategy
            recommended_engines = self._recommend_hierarchical_engines(
                main_clause, subordinate_clauses, embedded_constructions
            )
            
            coordination_strategy = self._determine_hierarchical_coordination(complexity)
            
            processing_time = time.time() - start_time
            
            return HierarchicalGrammarResult(
                sentence=sentence,
                main_clause=main_clause,
                subordinate_clauses=subordinate_clauses,
                embedded_constructions=embedded_constructions,
                overall_complexity=complexity,
                recommended_engines=recommended_engines,
                coordination_strategy=coordination_strategy,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Hierarchical analysis failed: {e}")
            # Fallback to simple analysis
            simple_result = self.detect_grammar_pattern(sentence)
            return self._convert_to_hierarchical_result(sentence, simple_result, time.time() - start_time)
    
    def _decompose_into_clauses(self, dependencies: List[DependencyInfo], sentence: str) -> List[ClauseInfo]:
        """Decompose sentence into constituent clauses based on dependency structure."""
        
        clauses = []
        processed_words = set()
        
        # Find clause heads (roots of different clauses)
        clause_heads = {}
        
        for dep in dependencies:
            if dep.relation in self.clause_relation_mapping:
                clause_type = self.clause_relation_mapping[dep.relation]
                if dep.relation == 'root':
                    clause_heads[dep.dependent] = {
                        'type': clause_type,
                        'root': dep.dependent,
                        'dependencies': []
                    }
                else:
                    clause_heads[dep.dependent] = {
                        'type': clause_type,
                        'root': dep.dependent,
                        'dependencies': []
                    }
        
        # Assign dependencies to appropriate clauses
        for dep in dependencies:
            assigned = False
            
            # Try to assign to existing clause heads
            for clause_root, clause_info in clause_heads.items():
                if (dep.head == clause_root or 
                    dep.dependent == clause_root or
                    self._is_dependent_of_clause(dep, clause_info['dependencies'])):
                    clause_info['dependencies'].append(dep)
                    assigned = True
                    break
            
            # If not assigned to any clause, add to main clause (root)
            if not assigned:
                main_clause_root = None
                for clause_root, clause_info in clause_heads.items():
                    if clause_info['type'] == 'main':
                        main_clause_root = clause_root
                        break
                
                if main_clause_root:
                    clause_heads[main_clause_root]['dependencies'].append(dep)
                else:
                    # Create main clause if it doesn't exist
                    root_dep = next((d for d in dependencies if d.relation == 'root'), None)
                    if root_dep:
                        clause_heads[root_dep.dependent] = {
                            'type': 'main',
                            'root': root_dep.dependent,
                            'dependencies': [dep]
                        }
        
        # Convert to ClauseInfo objects
        word_positions = {word: i for i, word in enumerate(sentence.split())}
        
        for clause_root, clause_data in clause_heads.items():
            clause_words = set([clause_root])
            for dep in clause_data['dependencies']:
                clause_words.update([dep.head, dep.dependent])
            
            # Calculate word range
            positions = [word_positions.get(word, 0) for word in clause_words if word in word_positions]
            word_range = (min(positions, default=0), max(positions, default=0))
            
            clauses.append(ClauseInfo(
                clause_type=clause_data['type'],
                root_word=clause_root,
                dependencies=clause_data['dependencies'],
                word_range=word_range
            ))
        
        return clauses
    
    def _is_dependent_of_clause(self, dep: DependencyInfo, clause_deps: List[DependencyInfo]) -> bool:
        """Check if a dependency belongs to a clause based on existing dependencies."""
        for clause_dep in clause_deps:
            if (dep.head == clause_dep.dependent or 
                dep.dependent == clause_dep.head):
                return True
        return False
    
    def _analyze_clause_pattern(self, clause: ClauseInfo, full_analysis: Dict) -> Dict:
        """Analyze the grammatical pattern of a specific clause."""
        
        # Create a focused analysis for just this clause
        clause_deps = clause.dependencies
        clause_pos_tags = {}
        
        # Extract POS tags for words in this clause
        full_pos_tags = dict(full_analysis.get('pos_tags', []))
        clause_words = set([clause.root_word])
        for dep in clause_deps:
            clause_words.update([dep.head, dep.dependent])
        
        for word in clause_words:
            if word in full_pos_tags:
                clause_pos_tags[word] = full_pos_tags[word]
        
        # Get candidate patterns for this clause type
        candidate_patterns = self.clause_pattern_preferences.get(
            clause.clause_type, 
            list(self.dependency_patterns.keys())
        )
        
        # Calculate scores only for relevant patterns
        best_pattern = None
        best_confidence = 0.0
        
        for pattern in candidate_patterns:
            if pattern in self.dependency_patterns:
                score = self._calculate_clause_pattern_score(
                    pattern, clause_deps, clause_pos_tags, clause.clause_type
                )
                if score > best_confidence:
                    best_confidence = score
                    best_pattern = pattern
        
        return {
            'pattern': best_pattern or GrammarPattern.SV_PATTERN,
            'confidence': best_confidence
        }
    
    def _calculate_clause_pattern_score(self, pattern: GrammarPattern, 
                                       clause_deps: List[DependencyInfo], 
                                       clause_pos_tags: Dict, 
                                       clause_type: str) -> float:
        """Calculate pattern score for a specific clause."""
        
        if pattern not in self.dependency_patterns:
            return 0.0
        
        rules = self.dependency_patterns[pattern]
        score = 0.0
        base_confidence = rules.get('confidence_base', 0.5)
        
        # Adjust base confidence based on clause type relevance
        if clause_type in self.clause_pattern_preferences:
            if pattern in self.clause_pattern_preferences[clause_type]:
                base_confidence *= 1.2  # Boost for relevant patterns
        
        dep_relations = {dep.relation for dep in clause_deps}
        
        # Check required relations
        required_relations = rules.get('required_relations', [])
        if required_relations:
            matches = sum(1 for rel in required_relations if rel in dep_relations)
            score += (matches / len(required_relations)) * base_confidence
        
        # Apply pattern-specific checks
        if pattern == GrammarPattern.GERUND_PATTERN and clause_type == 'adverbial_clause':
            # Look for VBG in this clause
            vbg_count = sum(1 for pos in clause_pos_tags.values() if pos in ['VBG'])
            if vbg_count > 0:
                score += 0.4
        
        elif pattern == GrammarPattern.RELATIVE_PATTERN and clause_type == 'relative_clause':
            # Relative clauses get automatic boost
            score += 0.5
            
        elif pattern == GrammarPattern.INFINITIVE_PATTERN and clause_type == 'infinitive_complement':
            # Look for infinitive markers
            if any(dep.relation == 'mark' and dep.dependent == 'to' for dep in clause_deps):
                score += 0.5
        
        return min(score, 1.0)
    
    def _calculate_hierarchical_complexity(self, main_clause: Optional[ClauseInfo], 
                                         subordinate_clauses: List[ClauseInfo],
                                         embedded_constructions: List[ClauseInfo]) -> float:
        """Calculate overall sentence complexity based on hierarchical structure."""
        
        complexity = 0.0
        
        # Base complexity from main clause
        if main_clause:
            complexity += 0.3
        
        # Add complexity for each subordinate clause
        complexity += len(subordinate_clauses) * 0.2
        
        # Add complexity for embedded constructions
        complexity += len(embedded_constructions) * 0.15
        
        # Bonus for high individual clause complexity
        all_clauses = [main_clause] + subordinate_clauses + embedded_constructions
        high_complexity_clauses = [c for c in all_clauses if c and c.confidence > 0.8]
        complexity += len(high_complexity_clauses) * 0.05
        
        return min(complexity, 1.0)
    
    def _recommend_hierarchical_engines(self, main_clause: Optional[ClauseInfo],
                                       subordinate_clauses: List[ClauseInfo],
                                       embedded_constructions: List[ClauseInfo]) -> List[str]:
        """Recommend engines based on all detected patterns."""
        
        engines = set()
        
        # Engines for main clause
        if main_clause and main_clause.grammatical_pattern:
            pattern_engines = self.engine_recommendations.get(main_clause.grammatical_pattern, [])
            engines.update(pattern_engines)
        
        # Engines for subordinate clauses
        for clause in subordinate_clauses:
            if clause.grammatical_pattern:
                pattern_engines = self.engine_recommendations.get(clause.grammatical_pattern, [])
                engines.update(pattern_engines)
        
        # Engines for embedded constructions
        for clause in embedded_constructions:
            if clause.grammatical_pattern:
                pattern_engines = self.engine_recommendations.get(clause.grammatical_pattern, [])
                engines.update(pattern_engines)
        
        # Always include basic five engine as foundation
        engines.add('basic_five_engine')
        
        return list(engines)
    
    def _determine_hierarchical_coordination(self, complexity: float) -> str:
        """Determine coordination strategy based on hierarchical complexity."""
        
        if complexity >= 0.8:
            return 'sequential_multi_cooperative'  # New strategy for very complex sentences
        elif complexity >= 0.5:
            return 'multi_cooperative'
        else:
            return 'foundation_plus_specialist'
    
    def _convert_to_hierarchical_result(self, sentence: str, simple_result: GrammarDetectionResult, 
                                      processing_time: float) -> HierarchicalGrammarResult:
        """Convert simple result to hierarchical format as fallback."""
        
        main_clause = ClauseInfo(
            clause_type='main',
            root_word='unknown',
            dependencies=[],
            word_range=(0, len(sentence.split()) - 1),
            grammatical_pattern=simple_result.primary_pattern,
            confidence=simple_result.confidence
        )
        
        return HierarchicalGrammarResult(
            sentence=sentence,
            main_clause=main_clause,
            subordinate_clauses=[],
            embedded_constructions=[],
            overall_complexity=simple_result.complexity_score,
            recommended_engines=simple_result.recommended_engines,
            coordination_strategy=simple_result.coordination_strategy,
            processing_time=processing_time
        )

def test_hierarchical_detector():
    """Test the hierarchical grammar detector on complex sentences."""
    
    detector = HierarchicalGrammarDetector(log_level="INFO")
    
    test_sentences = [
        "Being a teacher, she knows how to explain difficult concepts.",
        "The book that was written by John is very good.", 
        "Please tell me if there are any problems.",
        "Having finished the work, she went home.",
        "When she was young, she seemed very happy."
    ]
    
    print("🎯 Hierarchical Grammar Detection Test")
    print("=" * 60)
    
    for sentence in test_sentences:
        print(f"\n📝 Analyzing: \"{sentence}\"")
        print("-" * 50)
        
        result = detector.detect_hierarchical_grammar(sentence)
        
        print(f"🏗️ Main Clause:")
        if result.main_clause:
            print(f"   Pattern: {result.main_clause.grammatical_pattern.value if result.main_clause.grammatical_pattern else 'None'}")
            print(f"   Confidence: {result.main_clause.confidence:.3f}")
            print(f"   Root: {result.main_clause.root_word}")
        
        print(f"📋 Subordinate Clauses ({len(result.subordinate_clauses)}):")
        for i, clause in enumerate(result.subordinate_clauses):
            print(f"   {i+1}. Type: {clause.clause_type}")
            print(f"      Pattern: {clause.grammatical_pattern.value if clause.grammatical_pattern else 'None'}")
            print(f"      Confidence: {clause.confidence:.3f}")
        
        print(f"🔧 Embedded Constructions ({len(result.embedded_constructions)}):")
        for i, clause in enumerate(result.embedded_constructions):
            print(f"   {i+1}. Type: {clause.clause_type}")
            print(f"      Pattern: {clause.grammatical_pattern.value if clause.grammatical_pattern else 'None'}")
        
        print(f"📊 Overall Complexity: {result.overall_complexity:.3f}")
        print(f"🤖 Recommended Engines: {result.recommended_engines}")
        print(f"⚡ Coordination Strategy: {result.coordination_strategy}")
        print(f"⏱️ Processing Time: {result.processing_time:.3f}s")

if __name__ == "__main__":
    test_hierarchical_detector()
