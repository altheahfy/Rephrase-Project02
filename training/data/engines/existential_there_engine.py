#!/usr/bin/env python3
"""
Existential There Engine - Priority 16 Grammar Engine

This engine handles existential "there" constructions in English:
1. Basic existence: There is/are + NP + (PP)
2. Modal existence: There will/can/must be + NP + (PP)  
3. Perfect existence: There has/have been + NP + (PP)
4. Progressive existence: There is/are being + NP + (PP)
5. Compound existence: There used to be + NP + (PP)

Architecture Compliance:
- Upper Slots: M1, S, Aux, M2, V, C1, O1, O2, C2, M3 (10-slot system)
- Sub Slots: sub-m1, sub-s, sub-aux, sub-m2, sub-v, sub-c1, sub-o1, sub-o2, sub-c2, sub-m3
- Boundary Expansion: Integrated via boundary_expansion_lib

Key Features:
- Subject-verb agreement analysis (is/are based on logical subject)
- Logical subject extraction (post-verbal NP)
- Location/time phrase processing
- Modal and tense variation support

Author: GitHub Copilot
Date: 2025-08-14
Priority: 16
Coverage: ~25-30% (high frequency in daily conversation)
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
import stanza

# Import boundary expansion library
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from boundary_expansion_lib import BoundaryExpansionLib

class ExistentialThereEngine:
    """
    Priority 16: Existential There constructions processing engine.
    
    Handles various "there + be" patterns with proper subject identification
    and location/modifier extraction.
    """
    
    def __init__(self):
        """Initialize the Existential There Engine with Stanza NLP."""
        try:
            # Initialize Stanza for advanced parsing
            self.nlp = stanza.Pipeline(
                lang='en', 
                processors='tokenize,pos,lemma,depparse',
                use_gpu=False,
                verbose=False
            )
            self.logger = logging.getLogger(__name__)
            self.boundary_lib = BoundaryExpansionLib()
            
            # Existential "there" patterns
            self.there_patterns = [
                # Basic patterns
                r'\bthere\s+(is|are|was|were)\b',
                r'\bthere\s+(will|would|can|could|may|might|must|should)\s+be\b',
                r'\bthere\s+(has|have|had)\s+been\b',
                r'\bthere\s+(is|are)\s+being\b',
                r'\bthere\s+used\s+to\s+be\b',
                r'\bthere\s+(isn\'t|aren\'t|wasn\'t|weren\'t)\b',
                r'\bthere\s+(won\'t|can\'t|couldn\'t|shouldn\'t)\s+be\b',
                r'\bthere\s+(hasn\'t|haven\'t|hadn\'t)\s+been\b'
            ]
            
            # Frequency and coverage data
            self.engine_info = {
                'priority': 16,
                'name': 'ExistentialThereEngine',
                'description': 'Existential there constructions processing',
                'coverage_rate': 0.28,  # 28% frequency
                'patterns': [
                    'There is', 'There are', 'There was', 'There were',
                    'There will be', 'There has been', 'There used to be',
                    "There isn't", "There won't be", 'There can be'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ExistentialThereEngine: {e}")
            raise

    def is_applicable(self, sentence: str) -> bool:
        """
        Check if sentence contains existential "there" patterns.
        
        Args:
            sentence: Input sentence to check
            
        Returns:
            bool: True if existential patterns detected
        """
        sentence_lower = sentence.lower()
        
        # Check for existential "there" patterns
        for pattern in self.there_patterns:
            if re.search(pattern, sentence_lower):
                return True
                
        return False

    def process(self, sentence: str) -> Dict[str, Any]:
        """
        Process existential there sentence with comprehensive slot extraction.
        
        Args:
            sentence: Input sentence
            
        Returns:
            Dict containing processing results with slots, confidence, metadata
        """
        try:
            if not self.is_applicable(sentence):
                return {
                    'success': False,
                    'confidence': 0.0,
                    'slots': {},
                    'metadata': {'error': 'Not applicable'},
                    'engine': 'existential_there'
                }

            # Apply boundary expansion for enhanced slot extraction
            enhanced_sentence = self.boundary_lib.expand_span_generic(sentence)
            
            # Parse with Stanza
            doc = self.nlp(enhanced_sentence)
            
            # Initialize slots
            slots = {}
            
            # Analyze existential structure
            structure_info = self._analyze_existential_structure(enhanced_sentence, doc)
            
            # Extract slots based on structure
            slots = self._extract_existential_slots(enhanced_sentence, doc, structure_info)
            
            # Calculate confidence based on slot completeness
            confidence = self._calculate_confidence(slots, structure_info)
            
            # Prepare metadata
            metadata = {
                'existential_type': structure_info.get('type', 'basic'),
                'logical_subject': structure_info.get('logical_subject', ''),
                'agreement': structure_info.get('agreement', ''),
                'tense': structure_info.get('tense', ''),
                'modality': structure_info.get('modality', ''),
                'polarity': structure_info.get('polarity', 'positive'),
                'boundary_enhanced': len(enhanced_sentence) != len(sentence)
            }
            
            return {
                'success': confidence > 0.5,
                'confidence': confidence,
                'slots': slots,
                'metadata': metadata,
                'engine': 'existential_there'
            }
            
        except Exception as e:
            self.logger.error(f"Error processing sentence '{sentence}': {str(e)}")
            return {
                'success': False,
                'confidence': 0.0,
                'slots': {},
                'metadata': {'error': str(e)},
                'engine': 'existential_there'
            }

    def _analyze_existential_structure(self, sentence: str, doc: Any) -> Dict[str, Any]:
        """
        Analyze the structure of existential there sentence.
        
        Args:
            sentence: Input sentence
            doc: Stanza parsed document
            
        Returns:
            Dict with structural analysis
        """
        structure = {
            'type': 'basic',
            'tense': 'present',
            'modality': '',
            'polarity': 'positive',
            'logical_subject': '',
            'agreement': '',
            'location': '',
            'time': ''
        }
        
        sentence_lower = sentence.lower()
        
        # Determine existential type and tense
        if re.search(r'there\s+(will|would|can|could|may|might|must|should)\s+be', sentence_lower):
            structure['type'] = 'modal'
            modal_match = re.search(r'there\s+(will|would|can|could|may|might|must|should)\s+be', sentence_lower)
            if modal_match:
                structure['modality'] = modal_match.group(1)
                structure['tense'] = 'future' if modal_match.group(1) in ['will', 'shall'] else 'modal'
        elif re.search(r'there\s+(has|have|had)\s+been', sentence_lower):
            structure['type'] = 'perfect'
            structure['tense'] = 'present_perfect' if re.search(r'there\s+(has|have)\s+been', sentence_lower) else 'past_perfect'
        elif re.search(r'there\s+(is|are)\s+being', sentence_lower):
            structure['type'] = 'progressive'
            structure['tense'] = 'present_progressive'
        elif re.search(r'there\s+used\s+to\s+be', sentence_lower):
            structure['type'] = 'used_to'
            structure['tense'] = 'past_habitual'
        elif re.search(r'there\s+(was|were)', sentence_lower):
            structure['type'] = 'basic'
            structure['tense'] = 'past'
        else:
            structure['type'] = 'basic'
            structure['tense'] = 'present'
            
        # Check polarity (negative patterns)
        if re.search(r'there\s+(isn\'t|aren\'t|wasn\'t|weren\'t|won\'t|can\'t|couldn\'t|shouldn\'t|hasn\'t|haven\'t|hadn\'t)', sentence_lower):
            structure['polarity'] = 'negative'
        
        # Find logical subject (post-verbal NP)
        structure['logical_subject'] = self._extract_logical_subject(sentence, doc)
        
        # Determine agreement
        if re.search(r'there\s+(is|was|has|isn\'t|wasn\'t|hasn\'t)', sentence_lower):
            structure['agreement'] = 'singular'
        elif re.search(r'there\s+(are|were|have|aren\'t|weren\'t|haven\'t)', sentence_lower):
            structure['agreement'] = 'plural'
            
        return structure

    def _extract_logical_subject(self, sentence: str, doc: Any) -> str:
        """
        Extract the logical subject (post-verbal NP) from existential sentence.
        
        Args:
            sentence: Input sentence
            doc: Stanza parsed document
            
        Returns:
            str: Logical subject (cleaned)
        """
        # Look for the NP that follows "there be"
        for sent in doc.sentences:
            for word in sent.words:
                # Find "there" as subject
                if word.lemma.lower() == 'there' and word.deprel == 'expl':
                    # Look for the actual logical subject (usually nsubj or obj)
                    for other_word in sent.words:
                        if other_word.head == word.head and other_word.deprel in ['nsubj', 'obj', 'nmod']:
                            subject = self._build_noun_phrase(sent, other_word)
                            return self._clean_duplicate_words(subject)
                            
                # Alternative: find main verb and look for its object
                elif word.upos in ['AUX', 'VERB'] and word.lemma.lower() == 'be':
                    for other_word in sent.words:
                        if other_word.head == word.id and other_word.deprel in ['nsubj', 'obj']:
                            subject = self._build_noun_phrase(sent, other_word)
                            return self._clean_duplicate_words(subject)
                            
        # Fallback: regex extraction with enhanced patterns
        patterns = [
            # Basic patterns - capture everything until preposition or end
            r'there\s+(?:is|are|was|were|will\s+be|has\s+been|have\s+been|used\s+to\s+be)\s+([^,.]+?)(?:\s+(?:in|on|at|by|with|for|from|to|under|over|near|behind|beside|during|since|until)\b|$|\.|,)',
            # Fallback - capture everything after "there be"
            r'there\s+(?:is|are|was|were|will\s+be|has\s+been|have\s+been|used\s+to\s+be)\s+([^,.]+)',
            # Handle contractions
            r'there\s+(?:isn\'t|aren\'t|wasn\'t|weren\'t|won\'t\s+be|hasn\'t\s+been|haven\'t\s+been)\s+([^,.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                return self._clean_duplicate_words(subject)
                
        return ''

    def _clean_duplicate_words(self, text: str) -> str:
        """Clean duplicate words that may result from boundary expansion."""
        if not text:
            return text
            
        words = text.split()
        cleaned_words = []
        
        for word in words:
            # Remove duplicate consecutive words (case insensitive) and common duplicates
            if not cleaned_words or (word.lower() != cleaned_words[-1].lower() and 
                                   not (len(cleaned_words) > 1 and word.lower() == cleaned_words[-2].lower())):
                cleaned_words.append(word)
                
        return ' '.join(cleaned_words)

    def _extract_existential_slots(self, sentence: str, doc: Any, structure: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract slots from existential there sentence.
        
        Args:
            sentence: Input sentence
            doc: Stanza parsed document
            structure: Structural analysis
            
        Returns:
            Dict with slot assignments
        """
        slots = {}
        
        # S slot: Always "There" (expletive subject)
        slots['S'] = 'There'
        
        # V slot: Main verb (always "be" in some form)
        verb_form = self._extract_main_verb(sentence, structure)
        if verb_form:
            slots['V'] = verb_form
            
        # Aux slot: Modal or auxiliary verbs
        aux_form = self._extract_auxiliary(sentence, structure)
        if aux_form:
            slots['Aux'] = aux_form
            
        # C1 slot: Subject complement (the thing that exists - logical subject)
        logical_subject = structure.get('logical_subject', '')
        if logical_subject:
            slots['C1'] = logical_subject
            
        # Location and time modifiers
        location_info = self._extract_location_modifiers(sentence, doc)
        
        if location_info.get('location'):
            # C2 for locative complements - clean duplicates
            location_clean = self._clean_duplicate_words(location_info['location'])
            if location_clean and location_clean not in ['in', 'on', 'at']:  # Avoid incomplete prep phrases
                slots['C2'] = location_clean
            
        if location_info.get('time'):
            # M2 for time modifiers - but avoid duplicating what's already in other slots
            time_clean = self._clean_duplicate_words(location_info['time'])
            if time_clean and time_clean not in [slots.get('C2', ''), slots.get('M3', '')]:
                slots['M2'] = time_clean
            
        # Additional modifiers and negation
        modifiers = self._extract_additional_modifiers(sentence, doc)
        if modifiers.get('manner') and modifiers['manner'] not in [slots.get('M2', ''), slots.get('C2', '')]:
            # Avoid duplicating information already in other slots
            slots['M3'] = modifiers['manner']
        
        # Handle negation patterns
        negation_info = self._handle_negation(sentence, structure)
        if negation_info.get('negation'):
            if negation_info['position'] == 'M1':
                slots['M1'] = negation_info['negation']
            elif negation_info['position'] == 'M2' and 'M2' not in slots:
                slots['M2'] = negation_info['negation']
            
        return slots

    def _extract_main_verb(self, sentence: str, structure: Dict[str, Any]) -> str:
        """Extract the main verb form."""
        sentence_lower = sentence.lower()
        
        if structure['type'] == 'modal':
            return 'be'
        elif structure['type'] == 'perfect':
            return 'been'
        elif structure['type'] == 'progressive':
            return 'being'
        elif structure['type'] == 'used_to':
            return 'be'
        else:
            # Basic form - extract is/are/was/were
            be_match = re.search(r'there\s+(is|are|was|were|isn\'t|aren\'t|wasn\'t|weren\'t)', sentence_lower)
            if be_match:
                verb = be_match.group(1)
                return verb.replace("n't", "") if "n't" in verb else verb
                
        return 'be'

    def _extract_auxiliary(self, sentence: str, structure: Dict[str, Any]) -> str:
        """Extract auxiliary or modal verbs."""
        sentence_lower = sentence.lower()
        
        if structure['type'] == 'modal':
            modal_match = re.search(r'there\s+(will|would|can|could|may|might|must|should|won\'t|can\'t|couldn\'t|shouldn\'t)', sentence_lower)
            if modal_match:
                aux = modal_match.group(1)
                return aux.replace("n't", "") if "n't" in aux else aux
        elif structure['type'] == 'perfect':
            perf_match = re.search(r'there\s+(has|have|had|hasn\'t|haven\'t|hadn\'t)', sentence_lower)
            if perf_match:
                aux = perf_match.group(1)
                return aux.replace("n't", "") if "n't" in aux else aux
        elif structure['type'] == 'used_to':
            return 'used to'
            
        return ''

    def _extract_location_modifiers(self, sentence: str, doc: Any) -> Dict[str, str]:
        """
        Extract location and time modifiers with complete prepositional phrases.
        
        Args:
            sentence: Input sentence
            doc: Stanza parsed document
            
        Returns:
            Dict with location and time information
        """
        info = {'location': '', 'time': ''}
        
        # Common prepositions for location and time
        location_preps = ['in', 'on', 'at', 'under', 'over', 'near', 'behind', 'beside', 'between', 'among', 'inside', 'outside']
        time_preps = ['at', 'on', 'in', 'during', 'after', 'before', 'since', 'until', 'by']
        
        # Parse prepositional phrases using Stanza
        for sent in doc.sentences:
            for word in sent.words:
                if word.upos == 'ADP':  # Preposition
                    prep_phrase = self._build_prepositional_phrase(sent, word)
                    
                    if word.lemma.lower() in location_preps:
                        if not info['location']:  # Take first location
                            info['location'] = prep_phrase
                    elif word.lemma.lower() in time_preps:
                        if not info['time']:  # Take first time
                            info['time'] = prep_phrase
                            
        # Enhanced regex fallback for better phrase extraction
        if not info['location']:
            # Enhanced regex fallback for better phrase extraction
            loc_patterns = [
                # Complete prepositional phrases
                r'\b(in|on|at|under|over|near|behind|beside|between|among|inside|outside)\s+(the\s+\w+(?:\s+\w+)*)',
                r'\b(in|on|at|under|over|near|behind|beside|between|among|inside|outside)\s+(a\s+\w+(?:\s+\w+)*)', 
                r'\b(in|on|at|under|over|near|behind|beside|between|among|inside|outside)\s+(\w+(?:\s+\w+)*?)(?:\s+(?:sleeping|peacefully|quietly|\w+ly)|\.|,|$)',
                # Simple preposition + noun
                r'\b(in|on|at|under|over|near|behind|beside|between|among|inside|outside)\s+(\w+)',
            ]
            
            for pattern in loc_patterns:
                loc_match = re.search(pattern, sentence, re.IGNORECASE)
                if loc_match:
                    prep = loc_match.group(1)
                    noun_phrase = loc_match.group(2).strip()
                    # Clean the extracted phrase
                    cleaned_phrase = self._clean_duplicate_words(f"{prep} {noun_phrase}")
                    if len(cleaned_phrase.split()) >= 2:  # Ensure we have preposition + at least one word
                        info['location'] = cleaned_phrase
                        break
                
        # Enhanced time extraction
        if not info['time']:
            time_patterns = [
                r'\b(yesterday|today|tomorrow|tonight|recently|now|then|soon|later)\b',
                r'\b(during|after|before|since|until|by)\s+([^,.]+)',
                r'\b(at|on|in)\s+(night|morning|afternoon|evening|\d+|the\s+\w+)',
            ]
            
            for pattern in time_patterns:
                time_match = re.search(pattern, sentence, re.IGNORECASE)
                if time_match:
                    if len(time_match.groups()) >= 2:
                        info['time'] = time_match.group(0).strip()
                    else:
                        info['time'] = time_match.group(1).strip()
                    break
                    
        return info

    def _extract_additional_modifiers(self, sentence: str, doc: Any) -> Dict[str, str]:
        """Extract additional modifiers like manner, degree, etc."""
        modifiers = {'manner': '', 'degree': ''}
        
        # Look for adverbial modifiers
        for sent in doc.sentences:
            for word in sent.words:
                if word.deprel == 'advmod' and word.upos == 'ADV':
                    if not modifiers['manner']:
                        modifiers['manner'] = word.text
                        
        return modifiers

    def _handle_negation(self, sentence: str, structure: Dict[str, Any]) -> Dict[str, str]:
        """Handle negation patterns in existential sentences."""
        text = sentence.lower()
        negation_info = {'negation': '', 'position': ''}
        
        # Pattern 1: "There is no/not any..."
        if re.search(r'\bthere\s+(is|are|was|were)\s+(no|not)', text):
            # Extract negation
            no_match = re.search(r'\bthere\s+(?:is|are|was|were)\s+(no)\b', text)
            not_match = re.search(r'\bthere\s+(?:is|are|was|were)\s+(not)(?:\s+any)?\b', text)
            
            if no_match:
                negation_info['negation'] = 'no'
                negation_info['position'] = 'M2'
            elif not_match:
                negation_info['negation'] = 'not'
                negation_info['position'] = 'M1'
                # Check for "any" after "not"
                if re.search(r'\bnot\s+any\b', text):
                    negation_info['negation'] = 'not any'
        
        # Pattern 2: Contractions "There isn't/aren't..."
        elif re.search(r'\bthere\s+(isn\'t|aren\'t|wasn\'t|weren\'t)', text):
            negation_info['negation'] = 'not'
            negation_info['position'] = 'M1'
        
        # Pattern 3: Modal negations "There won't/can't..."
        elif re.search(r'\bthere\s+(won\'t|can\'t|couldn\'t|shouldn\'t|mustn\'t)', text):
            negation_info['negation'] = 'not'
            negation_info['position'] = 'M1'
        
        # Pattern 4: Perfect negations "There hasn't/haven't..."
        elif re.search(r'\bthere\s+(hasn\'t|haven\'t|hadn\'t)', text):
            negation_info['negation'] = 'not'
            negation_info['position'] = 'M1'
        
        return negation_info

    def _build_noun_phrase(self, sent: Any, head_word: Any) -> str:
        """Build complete noun phrase from head word, avoiding duplicates."""
        phrase_words = []
        word_positions = []
        
        # Collect head word
        phrase_words.append(head_word.text)
        word_positions.append(head_word.id)
        
        # Collect modifiers (excluding duplicates)
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['det', 'amod', 'nummod', 'compound']:
                if word.text not in phrase_words:  # Avoid exact duplicates
                    phrase_words.append(word.text)
                    word_positions.append(word.id)
        
        # Sort by word order and join
        paired_words = list(zip(phrase_words, word_positions))
        paired_words.sort(key=lambda x: x[1])  # Sort by position
        
        # Build final phrase with additional duplicate cleaning
        final_words = []
        for word, _ in paired_words:
            if not final_words or word.lower() != final_words[-1].lower():
                final_words.append(word)
                
        result = ' '.join(final_words)
        return self._clean_duplicate_words(result)

    def _build_prepositional_phrase(self, sent: Any, prep_word: Any) -> str:
        """Build complete prepositional phrase, avoiding duplicates."""
        phrase_parts = [prep_word.text]
        
        # Find the object of preposition
        for word in sent.words:
            if word.head == prep_word.id and word.deprel == 'pobj':
                obj_phrase = self._build_noun_phrase(sent, word)
                phrase_parts.append(obj_phrase)
                break
                
        return ' '.join(phrase_parts)

    def _calculate_confidence(self, slots: Dict[str, str], structure: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on slot extraction success.
        
        Args:
            slots: Extracted slots
            structure: Structural analysis
            
        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        base_confidence = 0.8  # Base for existential pattern detection
        
        # Essential slots for existential sentences
        if 'S' in slots and slots['S'] == 'There':
            base_confidence += 0.1
        if 'V' in slots and slots['V']:
            base_confidence += 0.1
        if 'C1' in slots and slots['C1']:  # Subject complement is crucial
            base_confidence += 0.1
        else:
            base_confidence -= 0.2  # Penalty for missing subject complement
            
        # Bonus for additional slots
        additional_slots = ['Aux', 'C2', 'M2', 'M3']
        filled_additional = sum(1 for slot in additional_slots if slots.get(slot))
        base_confidence += (filled_additional * 0.05)
        
        # Structure complexity bonus
        if structure['type'] in ['modal', 'perfect', 'progressive']:
            base_confidence += 0.05
            
        return min(1.0, max(0.0, base_confidence))

    def get_engine_info(self) -> Dict[str, Any]:
        """Return engine information and statistics."""
        return self.engine_info.copy()

if __name__ == "__main__":
    # Test the engine
    engine = ExistentialThereEngine()
    
    test_sentences = [
        "There is a book on the table.",
        "There are many students in the classroom.",
        "There will be a party tonight.",
        "There has been a problem with the system.",
        "There used to be a restaurant here.",
        "There isn't any milk in the fridge.",
        "There won't be enough time to finish.",
        "There are three cats sleeping in the garden.",
        "There was nobody at home when I called.",
        "There have been several complaints about the service."
    ]
    
    print("🧪 Testing Existential There Engine")
    print("=" * 50)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\nTest {i}: {sentence}")
        
        if engine.is_applicable(sentence):
            result = engine.process(sentence)
            print(f"✅ Applicable | Success: {result['success']}")
            print(f"   Confidence: {result['confidence']:.3f}")
            print(f"   Slots: {result['slots']}")
            print(f"   Type: {result['metadata'].get('existential_type', 'N/A')}")
        else:
            print("❌ Not applicable")
