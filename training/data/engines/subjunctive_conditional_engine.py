#!/usr/bin/env python3
"""
Subjunctive/Conditional Engine - 10th Unified Architecture Engine

This engine handles all major subjunctive and conditional patterns in English:
1. Real conditionals (Type 1): If it rains, I will stay home
2. Unreal present conditionals (Type 2): If I were rich, I would travel
3. Unreal past conditionals (Type 3): If I had studied, I would have passed  
4. Mixed conditionals: If I had studied medicine, I would be a doctor now
5. Subjunctive mood: I wish I were taller / It's important that he be on time
6. Inverted conditionals: Were I rich, I would travel
7. Unless conditionals: Unless you hurry, you will be late

Architecture Compliance:
- Upper Slots: S, V, O1, C1, M1, M2, M3, Aux (primary clause structure)
- Sub-slots: sub-s, sub-v, sub-o1, sub-c1, sub-m1, sub-m2, sub-m3, sub-aux (subordinate clause)
- Conjunction Delegation: Complex sentences with multiple conjunctions delegated to conjunction engine
"""

import re
import stanza
from typing import Dict, List, Tuple, Optional, Any

class SubjunctiveConditionalEngine:
    """
    Unified architecture engine for processing subjunctive and conditional constructions.
    Handles all major conditional types and subjunctive moods with precise slot allocation.
    """
    
    def __init__(self):
        """Initialize the Stanza NLP pipeline for dependency parsing."""
        try:
            self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
        except:
            print("Stanza model not found. Please install with: stanza.download('en')")
            self.nlp = None
    
    def is_applicable(self, sentence: str) -> bool:
        """
        Determine if this engine should handle the given sentence.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            bool: True if sentence contains subjunctive/conditional patterns
        """
        if not sentence or not sentence.strip():
            return False
            
        # Check for conjunction patterns that should be delegated
        if self._contains_complex_conjunction(sentence):
            return False
            
        sentence_lower = sentence.lower().strip()
        
        # Conditional indicators
        conditional_patterns = [
            r'\bif\b',           # if clauses
            r'\bunless\b',       # unless clauses
            r'^(were|had|should)\s+\w+.*,', # inverted conditionals (Were I...)
        ]
        
        # Subjunctive indicators
        subjunctive_patterns = [
            r'\bwish(es)?\b',    # wish clauses
            r'\bif only\b',      # if only clauses
            r'\bas if\b',        # as if clauses
            r'\bas though\b',    # as though clauses
            r'\bwould rather\b', # would rather clauses
            r'\bit\'s\s+(important|necessary|essential|crucial)\s+that\b', # subjunctive that-clauses
            r'\bi\s+(suggest|recommend|demand|insist|require)\s+that\b',   # subjunctive that-clauses
        ]
        
        all_patterns = conditional_patterns + subjunctive_patterns
        
        for pattern in all_patterns:
            if re.search(pattern, sentence_lower):
                return True
                
        # Check for modal patterns indicating conditionals
        modal_patterns = [
            r'\bwould\b.*\bif\b',
            r'\bcould\b.*\bif\b', 
            r'\bmight\b.*\bif\b',
            r'\bshould\b.*\bif\b',
        ]
        
        for pattern in modal_patterns:
            if re.search(pattern, sentence_lower):
                return True
        
        return False
    
    def _contains_complex_conjunction(self, sentence: str) -> bool:
        """
        Check if sentence contains complex conjunctions requiring delegation.
        
        Args:
            sentence: Input sentence to check
            
        Returns:
            bool: True if complex conjunctions found
        """
        # Multiple conjunction words (excluding conditional conjunctions)
        conjunctions = ['and', 'but', 'or', 'so', 'yet', 'for', 'nor']
        conjunction_count = 0
        
        sentence_lower = sentence.lower()
        for conj in conjunctions:
            conjunction_count += len(re.findall(r'\b' + conj + r'\b', sentence_lower))
        
        # If more than one non-conditional conjunction, delegate
        if conjunction_count > 1:
            return True
            
        # Check for complex coordination patterns
        complex_patterns = [
            r'\b(and|but|or)\b.*\b(and|but|or)\b',  # Multiple coordinating conjunctions
            r'\bnot only\b.*\bbut also\b',          # Correlative conjunctions
            r'\beither\b.*\bor\b',                  # Either...or
            r'\bneither\b.*\bnor\b',               # Neither...nor
        ]
        
        for pattern in complex_patterns:
            if re.search(pattern, sentence_lower):
                return True
                
        return False
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        Process a subjunctive/conditional sentence and allocate to slots.
        
        Args:
            sentence: Input sentence to process
            
        Returns:
            Dict containing slot allocations and metadata
        """
        if not self.nlp:
            return self._create_error_result("Stanza pipeline not available")
            
        if not self.is_applicable(sentence):
            return self._create_error_result("Sentence not applicable for subjunctive/conditional processing")
        
        try:
            # Parse sentence with Stanza
            doc = self.nlp(sentence)
            
            # Detect conditional/subjunctive type and structure
            conditional_type = self._detect_conditional_type(sentence, doc)
            structure = self._analyze_conditional_structure(sentence, doc, conditional_type)
            
            # Allocate to unified architecture slots
            result = self._allocate_slots(sentence, doc, conditional_type, structure)
            
            return result
            
        except Exception as e:
            return self._create_error_result(f"Processing error: {str(e)}")
    
    def _detect_conditional_type(self, sentence: str, doc: Any) -> str:
        """
        Detect the type of conditional or subjunctive construction.
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            
        Returns:
            str: Type of conditional/subjunctive
        """
        sentence_lower = sentence.lower()
        
        # Inverted conditionals
        if re.search(r'^(were|had|should)\s+\w+', sentence_lower):
            return "inverted_conditional"
        # Also check for inverted patterns after punctuation
        if re.search(r'(^|\.|!|\?)\s*(were|had|should)\s+\w+', sentence_lower):
            return "inverted_conditional"
            
        # Unless conditionals
        if 'unless' in sentence_lower:
            return "unless_conditional"
            
        # Wish clauses
        if re.search(r'\bwish(es)?\b', sentence_lower):
            return "wish_subjunctive"
            
        # Subjunctive that-clauses
        if re.search(r'\b(suggest|recommend|demand|insist|require|important|necessary|essential)\b.*\bthat\b', sentence_lower):
            return "subjunctive_that"
            
        # Standard if conditionals - determine type by verb forms
        if 'if' in sentence_lower:
            # Check for conditional markers
            if re.search(r'\bwould\s+have\b.*\bhad\b', sentence_lower):
                return "conditional_type3"  # Unreal past
            elif re.search(r'\bwould\b.*\bif\b.*\bwere\b', sentence_lower):
                return "conditional_type2"  # Unreal present  
            elif re.search(r'\bwill\b.*\bif\b', sentence_lower) or re.search(r'\bif\b.*\bwill\b', sentence_lower):
                return "conditional_type1"  # Real conditional
            else:
                # Analyze verb forms more carefully
                return self._analyze_conditional_verb_forms(sentence, doc)
        
        return "general_conditional"
    
    def _analyze_conditional_verb_forms(self, sentence: str, doc: Any) -> str:
        """
        Analyze verb forms to determine conditional type.
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            
        Returns:
            str: Specific conditional type based on verb analysis
        """
        sentence_lower = sentence.lower()
        
        # Check for Type 3 (unreal past) patterns
        type3_patterns = [
            r'\bhad\s+\w+.*would\s+have\b',
            r'\bwould\s+have\b.*\bhad\s+\w+',
            r'\bif\s+.*had\s+\w+.*would\s+have',
        ]
        
        for pattern in type3_patterns:
            if re.search(pattern, sentence_lower):
                return "conditional_type3"
                
        # Check for Type 2 (unreal present) patterns
        type2_patterns = [
            r'\bwere\b.*\bwould\b',
            r'\bwould\b.*\bwere\b',
            r'\bif\s+.*were\b.*would\b',
            r'\bcould\b.*\bif\b.*\bwere\b',
            r'\bmight\b.*\bif\b.*\bwere\b',
        ]
        
        for pattern in type2_patterns:
            if re.search(pattern, sentence_lower):
                return "conditional_type2"
        
        # Check for modal + "had" patterns (also Type 2)
        if re.search(r'\b(could|might|should)\b.*\bif\b.*\bhad\b', sentence_lower) and 'would have' not in sentence_lower:
            return "conditional_type2"
            
        # Check for "had" + modal patterns (Type 2) 
        if re.search(r'\bif\b.*\bhad\b.*\b(could|might|would)\b', sentence_lower) and 'would have' not in sentence_lower:
            return "conditional_type2"
        
        # Default to Type 1 (real conditional)
        return "conditional_type1"
    
    def _analyze_conditional_structure(self, sentence: str, doc: Any, conditional_type: str) -> Dict[str, Any]:
        """
        Analyze the structure of the conditional sentence.
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            conditional_type: Type of conditional detected
            
        Returns:
            Dict containing structural analysis
        """
        structure = {
            'main_clause': '',
            'subordinate_clause': '',
            'conditional_marker': '',
            'clause_order': 'if_first',  # or 'main_first'
            'has_comma': ',' in sentence
        }
        
        # Handle inverted conditionals
        if conditional_type == "inverted_conditional":
            return self._analyze_inverted_structure(sentence, doc, structure)
            
        # Find conditional markers and split clauses
        sentence_lower = sentence.lower()
        
        # Common conditional markers
        markers = ['if', 'unless', 'when', 'whenever', 'as long as', 'provided that', 'suppose', 'supposing']
        
        for marker in markers:
            if marker in sentence_lower:
                structure['conditional_marker'] = marker
                break
        
        # Split into clauses based on comma or marker position
        if structure['conditional_marker']:
            marker_pos = sentence_lower.find(structure['conditional_marker'])
            
            if marker_pos < len(sentence) // 2:  # Marker in first half
                structure['clause_order'] = 'if_first'
                parts = sentence.split(',', 1) if ',' in sentence else [sentence[:marker_pos + 20], sentence[marker_pos + 20:]]
                if len(parts) == 2:
                    structure['subordinate_clause'] = parts[0].strip()
                    structure['main_clause'] = parts[1].strip()
            else:  # Marker in second half
                structure['clause_order'] = 'main_first' 
                parts = sentence.split(',', 1) if ',' in sentence else [sentence[:marker_pos], sentence[marker_pos:]]
                if len(parts) == 2:
                    structure['main_clause'] = parts[0].strip()
                    structure['subordinate_clause'] = parts[1].strip()
        
        return structure
    
    def _analyze_inverted_structure(self, sentence: str, doc: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze inverted conditional structures (Were I rich, I would travel).
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document  
            structure: Structure dict to populate
            
        Returns:
            Dict: Updated structure information
        """
        # Inverted conditionals start with auxiliary verb
        parts = sentence.split(',', 1)
        if len(parts) == 2:
            structure['subordinate_clause'] = parts[0].strip()  # "Were I rich"
            structure['main_clause'] = parts[1].strip()         # "I would travel"
            structure['clause_order'] = 'if_first'
            structure['conditional_marker'] = 'inverted'
        
        return structure
    
    def _allocate_slots(self, sentence: str, doc: Any, conditional_type: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Allocate sentence components to unified architecture slots.
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            conditional_type: Type of conditional
            structure: Structural analysis
            
        Returns:
            Dict: Complete slot allocation result
        """
        slots = {
            # Upper slots (main clause)
            'S': '',     # Subject of main clause
            'V': '',     # Main verb of main clause
            'O1': '',    # Object 1 of main clause
            'C1': '',    # Complement 1 of main clause
            'M1': '',    # Modifier 1 (often entire conditional clause)
            'M2': '',    # Modifier 2
            'M3': '',    # Modifier 3
            'Aux': '',   # Auxiliary verb
            
            # Sub-slots (subordinate clause)
            'sub-s': '',   # Subject of conditional clause
            'sub-v': '',   # Verb of conditional clause
            'sub-o1': '',  # Object of conditional clause
            'sub-c1': '',  # Complement of conditional clause
            'sub-m1': '',  # Modifier in conditional clause
            'sub-m2': '',  # Additional modifier
            'sub-m3': '',  # Additional modifier
            'sub-aux': '', # Auxiliary in conditional clause
        }
        
        metadata = {
            'engine': 'subjunctive_conditional',
            'version': '1.0',
            'sentence': sentence,
            'conditional_type': conditional_type,
            'structure': structure,
            'parsing_method': 'stanza_dependency'
        }
        
        try:
            # Process based on conditional type
            if conditional_type == "inverted_conditional":
                slots = self._process_inverted_conditional(sentence, doc, structure, slots)
            elif conditional_type in ["conditional_type1", "conditional_type2", "conditional_type3"]:
                slots = self._process_standard_conditional(sentence, doc, structure, slots, conditional_type)
            elif conditional_type == "unless_conditional":
                slots = self._process_unless_conditional(sentence, doc, structure, slots)
            elif conditional_type == "wish_subjunctive":
                slots = self._process_wish_subjunctive(sentence, doc, structure, slots)
            elif conditional_type == "subjunctive_that":
                slots = self._process_subjunctive_that(sentence, doc, structure, slots)
            else:
                slots = self._process_general_conditional(sentence, doc, structure, slots)
                
            return {
                'slots': slots,
                'metadata': metadata,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            return self._create_error_result(f"Slot allocation error: {str(e)}")
    
    def _process_inverted_conditional(self, sentence: str, doc: Any, structure: Dict[str, Any], slots: Dict[str, str]) -> Dict[str, str]:
        """
        Process inverted conditional sentences (Were I rich, I would travel).
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            structure: Structural analysis
            slots: Slot dictionary to populate
            
        Returns:
            Dict: Updated slots
        """
        main_clause = structure.get('main_clause', '').strip()
        sub_clause = structure.get('subordinate_clause', '').strip()
        
        # Parse main clause for upper slots
        if main_clause:
            main_doc = self.nlp(main_clause)
            main_analysis = self._analyze_clause_components(main_doc, main_clause)
            
            slots['S'] = main_analysis.get('subject', '')
            slots['V'] = main_analysis.get('main_verb', '')
            slots['Aux'] = main_analysis.get('auxiliary', '')
            slots['O1'] = main_analysis.get('object', '')
            slots['C1'] = main_analysis.get('complement', '')
        
        # Parse subordinate clause for sub-slots
        if sub_clause:
            # Handle inverted structure: "Were I rich" -> subject="I", aux="Were", complement="rich"
            sub_doc = self.nlp(sub_clause)
            sub_analysis = self._analyze_inverted_clause(sub_doc, sub_clause)
            
            slots['sub-s'] = sub_analysis.get('subject', '')
            slots['sub-v'] = sub_analysis.get('main_verb', '')
            slots['sub-aux'] = sub_analysis.get('auxiliary', '')
            slots['sub-c1'] = sub_analysis.get('complement', '')
        
        # Set M1 to the entire conditional clause
        slots['M1'] = sub_clause
        
        return slots
    
    def _process_standard_conditional(self, sentence: str, doc: Any, structure: Dict[str, Any], slots: Dict[str, str], conditional_type: str) -> Dict[str, str]:
        """
        Process standard if-then conditionals.
        
        Args:
            sentence: Original sentence  
            doc: Stanza parsed document
            structure: Structural analysis
            slots: Slot dictionary to populate
            conditional_type: Specific conditional type
            
        Returns:
            Dict: Updated slots
        """
        main_clause = structure.get('main_clause', '').strip()
        sub_clause = structure.get('subordinate_clause', '').strip()
        
        # Determine which clause is main vs subordinate based on structure
        if structure.get('clause_order') == 'if_first':
            # "If I were rich, I would travel" - subordinate first, main second
            conditional_clause = sub_clause
            result_clause = main_clause
        else:
            # "I would travel if I were rich" - main first, subordinate second  
            conditional_clause = sub_clause
            result_clause = main_clause
        
        # Parse main clause (result clause)
        if result_clause:
            main_doc = self.nlp(result_clause)
            main_analysis = self._analyze_clause_components(main_doc, result_clause)
            
            slots['S'] = main_analysis.get('subject', '')
            slots['V'] = main_analysis.get('main_verb', '')
            slots['Aux'] = main_analysis.get('auxiliary', '')
            slots['O1'] = main_analysis.get('object', '')
            slots['C1'] = main_analysis.get('complement', '')
        
        # Parse conditional clause (if clause)
        if conditional_clause:
            sub_doc = self.nlp(conditional_clause)
            sub_analysis = self._analyze_clause_components(sub_doc, conditional_clause)
            
            slots['sub-s'] = sub_analysis.get('subject', '')
            slots['sub-v'] = sub_analysis.get('main_verb', '')
            slots['sub-aux'] = sub_analysis.get('auxiliary', '')
            slots['sub-o1'] = sub_analysis.get('object', '')
            slots['sub-c1'] = sub_analysis.get('complement', '')
        
        # Set M1 to the entire conditional clause (clean up punctuation)
        clean_conditional = conditional_clause.rstrip('.').rstrip(',')
        slots['M1'] = clean_conditional
        
        return slots
    
    def _process_unless_conditional(self, sentence: str, doc: Any, structure: Dict[str, Any], slots: Dict[str, str]) -> Dict[str, str]:
        """
        Process unless conditionals (Unless you hurry, you will be late).
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document  
            structure: Structural analysis
            slots: Slot dictionary to populate
            
        Returns:
            Dict: Updated slots
        """
        # Unless conditionals work similarly to if conditionals
        return self._process_standard_conditional(sentence, doc, structure, slots, "unless_conditional")
    
    def _process_wish_subjunctive(self, sentence: str, doc: Any, structure: Dict[str, Any], slots: Dict[str, str]) -> Dict[str, str]:
        """
        Process wish subjunctive sentences (I wish I were taller).
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            structure: Structural analysis  
            slots: Slot dictionary to populate
            
        Returns:
            Dict: Updated slots
        """
        # Find "wish" and split the sentence
        wish_match = re.search(r'\bwish(es)?\b', sentence.lower())
        if not wish_match:
            return slots
            
        wish_end = wish_match.end()
        # Main clause: "I wish" or "She wishes"
        main_part = sentence[:wish_match.start() + len(wish_match.group())].strip()
        # Subordinate clause: "I were taller"
        sub_part = sentence[wish_end:].strip()
        
        # Parse main clause
        if main_part:
            main_doc = self.nlp(main_part)
            main_analysis = self._analyze_clause_components(main_doc, main_part)
            
            slots['S'] = main_analysis.get('subject', '')
            slots['V'] = 'wish'  # Main verb is always "wish"
            slots['Aux'] = main_analysis.get('auxiliary', '')
        
        # Parse subordinate clause (wish content)
        if sub_part:
            sub_doc = self.nlp(sub_part)
            sub_analysis = self._analyze_clause_components(sub_doc, sub_part)
            
            slots['sub-s'] = sub_analysis.get('subject', '')
            slots['sub-v'] = sub_analysis.get('main_verb', '')
            slots['sub-aux'] = sub_analysis.get('auxiliary', '')
            slots['sub-c1'] = sub_analysis.get('complement', '')
            slots['sub-o1'] = sub_analysis.get('object', '')
        
        # Set M1 to the wish content (clean up punctuation)
        clean_sub_part = sub_part.rstrip('.').rstrip(',')
        slots['M1'] = clean_sub_part
        
        return slots
    
    def _process_subjunctive_that(self, sentence: str, doc: Any, structure: Dict[str, Any], slots: Dict[str, str]) -> Dict[str, str]:
        """
        Process subjunctive that-clauses (It's important that he be on time).
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            structure: Structural analysis
            slots: Slot dictionary to populate
            
        Returns:
            Dict: Updated slots  
        """
        # Find "that" and split
        that_pos = sentence.lower().find('that')
        if that_pos == -1:
            return slots
            
        main_part = sentence[:that_pos].strip()
        sub_part = sentence[that_pos + 4:].strip()  # Skip "that"
        
        # Parse main clause
        if main_part:
            main_doc = self.nlp(main_part)
            main_analysis = self._analyze_clause_components(main_doc, main_part)
            
            slots['S'] = main_analysis.get('subject', '')
            slots['V'] = main_analysis.get('main_verb', '')
            slots['Aux'] = main_analysis.get('auxiliary', '')
            slots['C1'] = main_analysis.get('complement', '')
        
        # Parse subordinate clause
        if sub_part:
            sub_doc = self.nlp(sub_part)
            sub_analysis = self._analyze_clause_components(sub_doc, sub_part)
            
            slots['sub-s'] = sub_analysis.get('subject', '')
            slots['sub-v'] = sub_analysis.get('main_verb', '')
            slots['sub-aux'] = sub_analysis.get('auxiliary', '')
            slots['sub-o1'] = sub_analysis.get('object', '')
        
        # Set M1 to the that-clause
        slots['M1'] = f"that {sub_part}"
        
        return slots
    
    def _process_general_conditional(self, sentence: str, doc: Any, structure: Dict[str, Any], slots: Dict[str, str]) -> Dict[str, str]:
        """
        Process general conditional patterns not covered by specific types.
        
        Args:
            sentence: Original sentence
            doc: Stanza parsed document
            structure: Structural analysis
            slots: Slot dictionary to populate
            
        Returns:
            Dict: Updated slots
        """
        # Default to standard conditional processing
        return self._process_standard_conditional(sentence, doc, structure, slots, "general")
    
    def _analyze_clause_components(self, doc: Any, clause: str) -> Dict[str, str]:
        """
        Analyze a clause to extract grammatical components.
        
        Args:
            doc: Stanza parsed document
            clause: Original clause text
            
        Returns:
            Dict: Grammatical components
        """
        components = {
            'subject': '',
            'main_verb': '',
            'auxiliary': '',
            'object': '',
            'complement': '',
            'modifiers': []
        }
        
        if not doc.sentences:
            return components
            
        sent = doc.sentences[0]
        
        # Find root verb
        root_verb = None
        for word in sent.words:
            if word.deprel == 'root':
                if word.upos in ['VERB', 'AUX']:
                    root_verb = word
                    break
                elif word.upos == 'ADJ':  # For predicative adjectives
                    components['complement'] = word.text
                    # Find auxiliary for predicative constructions
                    for aux_word in sent.words:
                        if aux_word.head == word.id and aux_word.upos == 'AUX':
                            components['auxiliary'] = aux_word.text
                            break
                    # Find subject
                    for subj_word in sent.words:
                        if subj_word.head == word.id and subj_word.deprel in ['nsubj']:
                            components['subject'] = self._build_noun_phrase(sent, subj_word)
                            break
                    return components
        
        if root_verb:
            components['main_verb'] = root_verb.text
            
            # Find subject
            for word in sent.words:
                if word.head == root_verb.id and word.deprel in ['nsubj', 'nsubj:pass']:
                    components['subject'] = self._build_noun_phrase(sent, word)
                    break
            
            # Find auxiliary
            for word in sent.words:
                if word.head == root_verb.id and word.deprel == 'aux':
                    components['auxiliary'] = word.text
                    break
            
            # Find object
            for word in sent.words:
                if word.head == root_verb.id and word.deprel in ['obj', 'dobj']:
                    components['object'] = self._build_noun_phrase(sent, word)
                    break
            
            # Find complement (predicate adjectives, nouns, etc.)
            for word in sent.words:
                if word.head == root_verb.id and word.deprel in ['xcomp', 'ccomp', 'acomp']:
                    components['complement'] = self._build_complement_phrase(sent, word)
                    break
        
        return components
    
    def _analyze_inverted_clause(self, doc: Any, clause: str) -> Dict[str, str]:
        """
        Analyze inverted conditional clauses (Were I rich, Had she known).
        
        Args:
            doc: Stanza parsed document
            clause: Original clause text
            
        Returns:
            Dict: Components of inverted clause
        """
        components = {
            'subject': '',
            'auxiliary': '',
            'main_verb': '',
            'complement': ''
        }
        
        if not doc.sentences:
            return components
            
        sent = doc.sentences[0]
        words = [w.text for w in sent.words]
        
        if len(words) >= 3:
            # Pattern: [AUX] [SUBJECT] [COMPLEMENT/VERB/PREDICATE]
            components['auxiliary'] = words[0]
            components['subject'] = words[1]
            
            # Check if the rest is a complement (adjective) or verb
            remaining = ' '.join(words[2:])
            
            # If it's a past participle after "had", it's a main verb
            if words[0].lower() == 'had':
                components['main_verb'] = words[2] if len(words) > 2 else ''
            else:
                # For "were" constructions, usually a complement
                components['complement'] = remaining
            
        elif len(words) == 2:
            components['auxiliary'] = words[0]  
            components['subject'] = words[1]
        
        return components
    
    def _build_noun_phrase(self, sent: Any, head_word: Any) -> str:
        """
        Build complete noun phrase including modifiers.
        
        Args:
            sent: Stanza sentence object
            head_word: Head word of the noun phrase
            
        Returns:
            str: Complete noun phrase
        """
        phrase_words = [head_word]
        
        # Find modifiers of this noun
        for word in sent.words:
            if word.head == head_word.id and word.deprel in [
                'det', 'amod', 'nmod', 'compound', 'nummod', 'advmod'
            ]:
                phrase_words.append(word)
        
        # Sort by word position in sentence
        phrase_words.sort(key=lambda w: w.id)
        
        return ' '.join(word.text for word in phrase_words)
    
    def _build_complement_phrase(self, sent: Any, head_word: Any) -> str:
        """
        Build complement phrase including dependencies.
        
        Args:
            sent: Stanza sentence object  
            head_word: Head word of complement
            
        Returns:
            str: Complete complement phrase
        """
        phrase_words = [head_word]
        
        # Find dependencies of the complement
        for word in sent.words:
            if word.head == head_word.id:
                phrase_words.append(word)
        
        # Sort by position
        phrase_words.sort(key=lambda w: w.id)
        
        return ' '.join(word.text for word in phrase_words)
    
    def _create_error_result(self, error_msg: str) -> Dict[str, Any]:
        """
        Create standardized error result.
        
        Args:
            error_msg: Error message
            
        Returns:
            Dict: Error result structure
        """
        return {
            'slots': {},
            'metadata': {
                'engine': 'subjunctive_conditional',
                'version': '1.0',
                'error': error_msg
            },
            'success': False,
            'error': error_msg
        }

# Test function for engine validation
def test_engine():
    """Test the Subjunctive/Conditional Engine with sample sentences."""
    engine = SubjunctiveConditionalEngine()
    
    test_sentences = [
        "If it rains, I will stay home.",              # Type 1 conditional
        "If I were rich, I would travel the world.",  # Type 2 conditional  
        "If I had studied, I would have passed.",     # Type 3 conditional
        "Were I rich, I would buy a house.",          # Inverted conditional
        "I wish I were taller.",                      # Wish subjunctive
        "Unless you hurry, you will be late.",        # Unless conditional
        "It's important that he be on time.",         # Subjunctive that-clause
    ]
    
    print("Testing Subjunctive/Conditional Engine:")
    print("=" * 50)
    
    for sentence in test_sentences:
        print(f"\nSentence: {sentence}")
        
        if engine.is_applicable(sentence):
            result = engine.process(sentence)
            
            if result['success']:
                print("✓ Successfully processed")
                slots = result['slots']
                print(f"Type: {result['metadata']['conditional_type']}")
                
                # Print non-empty slots
                for slot_name, value in slots.items():
                    if value.strip():
                        print(f"  {slot_name}: '{value}'")
            else:
                print(f"✗ Error: {result['error']}")
        else:
            print("✗ Not applicable for this engine")

if __name__ == "__main__":
    test_engine()
