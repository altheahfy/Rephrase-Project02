#!/usr/bin/env python3
"""
Modal Engine - 11th Unified Architecture Engine

This engine handles all major modal auxiliary verbs and their variations in English:
1. Ability/Possibility: can, could, be able to
2. Permission: may, can, could, might
3. Necessity/Obligation: must, have to, need to, should, ought to
4. Probability/Certainty: will, would, shall, should, may, might, could
5. Advice/Suggestion: should, ought to, had better, could
6. Volition/Intention: will, would, shall
7. Habit (past): would, used to
8. Polite requests: could, would, may, might

Modal Characteristics:
- No third person -s: He can go (not "cans")
- Followed by bare infinitive: can go, must leave
- No do-support in questions/negatives: Can you...? / You cannot...
- Semi-modals: be able to, have to, need to, ought to, used to

Architecture Compliance:
- Upper Slots: S, V (modal), O1, C1, M1, M2, M3, Aux (infinitive verb after modal)
- Modal-specific: modal_type, modal_function, certainty_level, formality_level
- Delegation: Complex sentences with multiple clauses delegated to conjunction engine
"""

import re
import stanza
from typing import Dict, List, Tuple, Optional, Any

class ModalEngine:
    """
    Unified architecture engine for processing modal auxiliary constructions.
    Handles all major modals, semi-modals, and their semantic functions.
    """
    
    def __init__(self):
        """Initialize the Stanza NLP pipeline for dependency parsing."""
        try:
            self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
        except:
            print("Stanza model not found. Please install with: stanza.download('en')")
            self.nlp = None
    
    # Modal verb classifications
    CORE_MODALS = {
        'can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must'
    }
    
    SEMI_MODALS = {
        'be able to', 'have to', 'has to', 'had to', 'need to', 'needs to', 'needed to',
        'ought to', 'used to', 'dare to', 'had better', "had better'd", 'would rather'
    }
    
    # Modal functions and their certainty levels
    MODAL_FUNCTIONS = {
        # Ability/Possibility
        'can': {'function': 'ability', 'certainty': 0.8, 'formality': 'neutral'},
        'could': {'function': 'ability_past', 'certainty': 0.6, 'formality': 'polite'},
        'be able to': {'function': 'ability', 'certainty': 0.9, 'formality': 'formal'},
        
        # Permission
        'may': {'function': 'permission', 'certainty': 0.7, 'formality': 'formal'},
        'might': {'function': 'permission_polite', 'certainty': 0.5, 'formality': 'very_polite'},
        
        # Necessity/Obligation
        'must': {'function': 'necessity', 'certainty': 0.95, 'formality': 'formal'},
        'have to': {'function': 'necessity', 'certainty': 0.9, 'formality': 'neutral'},
        'should': {'function': 'advice', 'certainty': 0.7, 'formality': 'neutral'},
        'ought to': {'function': 'advice', 'certainty': 0.75, 'formality': 'formal'},
        'need to': {'function': 'necessity', 'certainty': 0.8, 'formality': 'neutral'},
        
        # Future/Probability
        'will': {'function': 'future', 'certainty': 0.9, 'formality': 'neutral'},
        'would': {'function': 'conditional', 'certainty': 0.6, 'formality': 'polite'},
        'shall': {'function': 'future_formal', 'certainty': 0.85, 'formality': 'very_formal'},
        
        # Habit (past)
        'used to': {'function': 'past_habit', 'certainty': 0.95, 'formality': 'neutral'},
        
        # Polite expressions
        'had better': {'function': 'strong_advice', 'certainty': 0.85, 'formality': 'neutral'},
        'would rather': {'function': 'preference', 'certainty': 0.8, 'formality': 'neutral'}
    }
    
    def is_applicable(self, sentence: str) -> bool:
        """
        Determine if this engine should handle the given sentence.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            bool: True if sentence contains modal constructions
        """
        if not sentence or not sentence.strip():
            return False
            
        sentence_lower = sentence.lower()
        
        # Check for core modals (as standalone words)
        modal_pattern = r'\b(?:can|could|may|might|will|would|shall|should|must)\b'
        if re.search(modal_pattern, sentence_lower):
            return True
        
        # Check for semi-modals (multi-word patterns)
        semi_modal_patterns = [
            r'\b(?:am|is|are|was|were|be|being|been)\s+able\s+to\b',
            r'\b(?:have|has|had)\s+to\b',
            r'\b(?:need|needs|needed)\s+to\b',
            r'\bought\s+to\b',
            r'\bused\s+to\b',
            r'\bhad\s+better\b',
            r'\bwould\s+rather\b',
            r'\bdare\s+to\b'
        ]
        
        for pattern in semi_modal_patterns:
            if re.search(pattern, sentence_lower):
                return True
        
        # Check for modal-like constructions in questions
        question_modal_patterns = [
            r'^(?:can|could|may|might|will|would|shall|should|must)\b',
            r'^(?:do|does|did).*\b(?:need|dare)\s+to\b'
        ]
        
        for pattern in question_modal_patterns:
            if re.search(pattern, sentence_lower):
                return True
        
        return False
    
    def extract_modal_info(self, sentence: str) -> Dict[str, Any]:
        """
        Extract modal information from sentence.
        Returns dictionary with modal details including type and question status.
        """
        sentence = sentence.strip()
        
        # Initialize modal info
        modal_info = {
            'modal_found': False,
            'modal_type': None,
            'is_question': False,
            'modal_function': 'unknown',
            'certainty_level': 0.5,
            'formality_level': 'neutral',
            'is_negative': False
        }
        
        # Check for negatives
        if re.search(r'\b(?:cannot|can\'t|couldn\'t|won\'t|wouldn\'t|shan\'t|shouldn\'t|mustn\'t|may not|might not)\b', sentence.lower()):
            modal_info['is_negative'] = True
        
        # Check if question (starts with modal)
        for modal in self.CORE_MODALS:
            if sentence.lower().startswith(modal.lower() + ' '):
                modal_info['is_question'] = True
                break
        
        # Find core modals with word boundary checking
        for modal in self.CORE_MODALS:
            pattern = rf'\b{re.escape(modal)}\b'
            if re.search(pattern, sentence, re.IGNORECASE):
                modal_info['modal_found'] = modal
                modal_info['modal_type'] = 'core'
                
                # Add function information if available
                if modal in self.MODAL_FUNCTIONS:
                    info = self.MODAL_FUNCTIONS[modal]
                    modal_info['modal_function'] = info['function']
                    modal_info['certainty_level'] = info['certainty']
                    modal_info['formality_level'] = info['formality']
                return modal_info
        
        # Find semi-modals with specific patterns (more accurate)
        semi_modal_patterns = [
            (r'\b(have|has|had)\s+to\b', 'have to'),
            (r'\b(need|needs|needed)\s+to\b', 'need to'),
            (r'\b(am|is|are|was|were)\s+able\s+to\b', 'be able to'),
            (r'\bused\s+to\b', 'used to'),
            (r'\bought\s+to\b', 'ought to'),
            (r'\bhad\s+better\b', 'had better'),
            (r'\bwould\s+rather\b', 'would rather')
        ]
        
        for pattern, modal_name in semi_modal_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                modal_info['modal_found'] = modal_name
                modal_info['modal_type'] = 'semi'
                
                # Add function information if available
                if modal_name in self.MODAL_FUNCTIONS:
                    info = self.MODAL_FUNCTIONS[modal_name]
                    modal_info['modal_function'] = info['function']
                    modal_info['certainty_level'] = info['certainty']
                    modal_info['formality_level'] = info['formality']
                return modal_info
        
        # If question detected but no modal found above, check question patterns
        if sentence.strip().endswith('?') or re.match(r'^(?:do|does|did)\b', sentence.lower()):
            modal_info['is_question'] = True
        
        return modal_info
        
        # Find semi-modals if no core modal found
        if not modal_info['modal_found']:
            semi_modal_checks = [
                (r'\b(?:am|is|are|was|were|be|being|been)\s+able\s+to\b', 'be able to'),
                (r'\b(?:have|has|had)\s+to\b', 'have to'),
                (r'\b(?:need|needs|needed)\s+to\b', 'need to'),
                (r'\bought\s+to\b', 'ought to'),
                (r'\bused\s+to\b', 'used to'),
                (r'\bhad\s+better\b', 'had better'),
                (r'\bwould\s+rather\b', 'would rather'),
                (r'\bdare\s+to\b', 'dare to')
            ]
            
            for pattern, modal_name in semi_modal_checks:
                if re.search(pattern, sentence_lower):
                    modal_info['modal_found'] = modal_name
                    modal_info['modal_type'] = 'semi'
                    if modal_name in self.MODAL_FUNCTIONS:
                        info = self.MODAL_FUNCTIONS[modal_name]
                        modal_info['modal_function'] = info['function']
                        modal_info['certainty_level'] = info['certainty']
                        modal_info['formality_level'] = info['formality']
                    break
        
        return modal_info
    
    def process_sentence(self, sentence: str) -> Dict[str, str]:
        """
        Process a sentence containing modal constructions and extract slots.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            Dictionary containing slot assignments
        """
        # Always use fallback extraction since Stanza may not be available
        return self._fallback_extraction(sentence)
    
    def _fallback_extraction(self, sentence: str) -> Dict[str, str]:
        """
        Improved fallback extraction with proper Aux slot handling.
        Ensures main verbs are correctly placed in Aux slot.
        """
        slots = {}
        modal_info = self.extract_modal_info(sentence)
        
        if not modal_info['modal_found']:
            return slots
        
        # Core modal processing
        if modal_info['modal_type'] == 'core':
            modal = modal_info['modal_found']
            
            # Handle questions: Modal + Subject + Main_Verb + Rest
            if modal_info['is_question']:
                question_pattern = rf'^({re.escape(modal)})\s+(\w+)\s+(\w+)(.*)$'
                match = re.search(question_pattern, sentence, re.IGNORECASE)
                
                if match:
                    modal_verb, subject, main_verb, rest = match.groups()
                    slots['S'] = subject
                    slots['V'] = modal_verb  # Modal to V
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
                    return {k: v for k, v in slots.items() if v and str(v).strip()}
            
            # Standard declarative: Subject + Modal + Main_Verb + Rest
            pattern = rf'^(.*?)\b({re.escape(modal)})\s+(\w+)(.*)$'
            match = re.search(pattern, sentence, re.IGNORECASE)
            
            if match:
                subject, modal_verb, main_verb, rest = match.groups()
                slots['S'] = subject.strip() if subject.strip() else None
                slots['V'] = modal_verb  # Modal to V
                slots['Aux'] = main_verb  # Main verb to Aux ✅
                
                rest = rest.strip()
                if rest:
                    slots['O1'] = rest
        
        # Semi-modal processing
        elif modal_info['modal_type'] == 'semi':
            modal_found = modal_info['modal_found']
            
            if 'have to' in modal_found:
                pattern = r'^(.*?)\b(have|has|had)\s+to\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, aux_verb, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = f"{aux_verb} to"  # Semi-modal to V
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif 'be able to' in modal_found:
                pattern = r'^(.*?)\b(am|is|are|was|were)\s+able\s+to\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, be_verb, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = f"{be_verb} able to"  # Semi-modal to V
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif 'used to' in modal_found:
                pattern = r'^(.*?)\bused\s+to\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = 'used to'  # Semi-modal to V
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif 'need to' in modal_found:
                pattern = r'^(.*?)\b(need|needs|needed)\s+to\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, need_verb, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = f"{need_verb} to"
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif 'ought to' in modal_found:
                pattern = r'^(.*?)\bought\s+to\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = 'ought to'
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif 'had better' in modal_found:
                pattern = r'^(.*?)\bhad\s+better\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = 'had better'
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif 'would rather' in modal_found:
                pattern = r'^(.*?)\bwould\s+rather\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = 'would rather'
                    slots['Aux'] = main_verb  # Main verb to Aux ✅
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
        
        # Clean up and return only non-empty slots
        return {k: v for k, v in slots.items() if v and str(v).strip()}
    
    def get_confidence(self, sentence: str, slots: Dict[str, str]) -> float:
        """
        Calculate confidence score for the slot extraction.
        
        Args:
            sentence: Original sentence
            slots: Extracted slots
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not slots:
            return 0.0
        
        confidence = 0.0
        
        # Base confidence for modal detection
        modal_info = self.extract_modal_info(sentence)
        if modal_info['modal_found']:
            confidence += 0.4
        
        # Subject detection
        if 'S' in slots and slots['S']:
            confidence += 0.2
        
        # Modal verb detection  
        if 'V' in slots and slots['V']:
            confidence += 0.2
        
        # Main verb detection
        if 'Aux' in slots and slots['Aux']:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def get_pattern_type(self, sentence: str) -> str:
        """
        Identify the specific modal pattern type.
        
        Args:
            sentence: Input sentence
            
        Returns:
            String describing the modal pattern type
        """
        modal_info = self.extract_modal_info(sentence)
        
        if not modal_info['modal_found']:
            return "no_modal"
        
        modal = modal_info['modal_found']
        function = modal_info['modal_function']
        
        # Classify pattern types
        if function in ['ability', 'ability_past']:
            return "ability_modal"
        elif function in ['permission', 'permission_polite']:
            return "permission_modal"
        elif function in ['necessity', 'advice', 'strong_advice']:
            return "necessity_modal"
        elif function in ['future', 'future_formal']:
            return "future_modal"
        elif function == 'conditional':
            return "conditional_modal"
        elif function == 'past_habit':
            return "habit_modal"
        elif function == 'preference':
            return "preference_modal"
        else:
            return "general_modal"

def main():
    """Test the Modal Engine with various examples."""
    engine = ModalEngine()
    
    test_sentences = [
        # Core modals - Ability
        "I can swim very well.",
        "She could play piano when she was young.",
        "We will be able to finish this project tomorrow.",
        
        # Permission
        "You may leave now.",
        "Could I borrow your pen?",
        "Might I suggest a different approach?",
        
        # Necessity/Obligation
        "Students must submit their assignments on time.",
        "I have to go to work early tomorrow.",
        "You should study harder for the exam.",
        "We ought to help our neighbors.",
        "You need to call your mother.",
        
        # Future/Probability  
        "It will rain tomorrow.",
        "I would go if I had time.",
        "We shall overcome these challenges.",
        
        # Past habits
        "She used to live in Paris.",
        "He would always arrive early.",
        
        # Advice/Preference
        "You had better finish your homework.",
        "I would rather stay home tonight.",
        
        # Negative modals
        "I cannot understand this problem.",
        "She shouldn't worry about it.",
        "You mustn't touch that button.",
        
        # Questions
        "Can you help me with this?",
        "Would you like some coffee?",
        "Should we start the meeting now?",
        
        # Complex examples
        "If I could choose, I would rather travel to Japan.",
        "Students who have to work part-time often struggle with their studies."
    ]
    
    print("🚀 Modal Engine Test Results")
    print("=" * 80)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\nTest {i}: {sentence}")
        
        if engine.is_applicable(sentence):
            slots = engine.process_sentence(sentence)
            confidence = engine.get_confidence(sentence, slots)
            pattern_type = engine.get_pattern_type(sentence)
            modal_info = engine.extract_modal_info(sentence)
            
            print(f"  ✅ Applicable (Pattern: {pattern_type})")
            print(f"  📊 Confidence: {confidence:.2f}")
            print(f"  🔧 Modal Info: {modal_info['modal_found']} ({modal_info['modal_function']})")
            print(f"  📝 Slots: {slots}")
        else:
            print("  ❌ Not applicable")

if __name__ == "__main__":
    main()
