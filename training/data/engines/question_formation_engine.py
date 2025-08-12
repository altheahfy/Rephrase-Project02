#!/usr/bin/env python3
"""
Question Formation Engine - 12th Unified Architecture Engine

This engine handles comprehensive question formation and decomposition in English:
1. Yes/No Questions: Do you like?, Can she come?, Is he here?
2. WH-Questions: What do you want?, Where are you going?, Who called?
3. Tag Questions: You're coming, aren't you?, She can't swim, can she?
4. Choice Questions: Do you want tea or coffee?
5. Embedded Questions: I wonder what time it is.
6. Question Word Orders: Subject-Auxiliary Inversion, WH-word placement

Question Types Covered:
- Auxiliary-based: Do/Does/Did, Be, Have, Modal questions
- WH-Questions: What, Where, When, Why, Who, Whom, Whose, Which, How
- Complex: Multiple questions, embedded questions, indirect questions
- Transformations: Statement → Question, Question → Statement

Architecture Compliance:
- Upper Slots: Q (question word), S, V, O1, O2, C1, C2, M1, M2, M3, Aux
- Question-specific: question_type, question_function, answer_type, formality_level
- Handles inversion patterns and WH-word movement accurately
"""

import re
from typing import Dict, List, Tuple, Optional, Any

try:
    import stanza
    STANZA_AVAILABLE = True
except ImportError:
    STANZA_AVAILABLE = False
    print("Note: Stanza not available. Using fallback processing only.")

class QuestionFormationEngine:
    """
    Unified architecture engine for processing all types of English questions.
    Handles question formation, decomposition, and transformation patterns.
    """
    
    def __init__(self):
        """Initialize the Stanza NLP pipeline for dependency parsing."""
        if STANZA_AVAILABLE:
            try:
                self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', download_method=None)
            except:
                print("Stanza model not found. Using fallback processing only.")
                self.nlp = None
        else:
            self.nlp = None
    
    # Question word classifications
    WH_WORDS = {
        'what', 'where', 'when', 'why', 'who', 'whom', 'whose', 'which', 'how',
        'whatever', 'wherever', 'whenever', 'whoever', 'whomever', 'whichever', 'however'
    }
    
    AUXILIARY_VERBS = {
        'do', 'does', 'did', 'am', 'is', 'are', 'was', 'were', 'be', 'being', 'been',
        'have', 'has', 'had', 'having', 'will', 'would', 'shall', 'should', 'can', 'could',
        'may', 'might', 'must', 'ought', 'dare', 'need', 'used'
    }
    
    # Question types and their characteristics
    QUESTION_TYPES = {
        'yes_no': {
            'pattern': r'^(?:do|does|did|am|is|are|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\b',
            'answer_type': 'yes_no',
            'inversion': True
        },
        'wh_question': {
            'pattern': r'^(?:what|where|when|why|who|whom|whose|which|how)\b',
            'answer_type': 'information',
            'wh_movement': True
        },
        'tag_question': {
            'pattern': r'.*,\s*(?:isn\'t|aren\'t|wasn\'t|weren\'t|don\'t|doesn\'t|didn\'t|haven\'t|hasn\'t|hadn\'t|won\'t|wouldn\'t|can\'t|couldn\'t|shouldn\'t|mustn\'t)\s+(?:he|she|it|they|you|we)\?',
            'answer_type': 'confirmation',
            'tag_structure': True
        },
        'choice_question': {
            'pattern': r'.*\bor\b.*\?',
            'answer_type': 'choice',
            'alternatives': True
        },
        'embedded_question': {
            'pattern': r'(?:wonder|know|ask|tell|show).*(?:what|where|when|why|who|whom|whose|which|how)\b',
            'answer_type': 'embedded',
            'indirect': True
        }
    }
    
    def is_applicable(self, sentence: str) -> bool:
        """
        Determine if this engine should handle the given sentence.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            bool: True if sentence contains question patterns
        """
        if not sentence or not sentence.strip():
            return False
            
        sentence_clean = sentence.strip()
        
        # Direct question mark check
        if sentence_clean.endswith('?'):
            return True
            
        # Check for embedded questions (indirect questions)
        sentence_lower = sentence.lower()
        embedded_patterns = [
            r'\b(?:wonder|ask|know|tell|show|explain|understand|realize)\b.*\b(?:what|where|when|why|who|whom|whose|which|how)\b',
            r'\b(?:question|inquiry)\b.*\b(?:about|regarding)\b'
        ]
        
        for pattern in embedded_patterns:
            if re.search(pattern, sentence_lower):
                return True
        
        return False
    
    def extract_question_info(self, sentence: str) -> Dict[str, Any]:
        """
        Extract detailed information about the question structure.
        
        Args:
            sentence: Input sentence
            
        Returns:
            Dictionary with question analysis
        """
        info = {
            'question_found': False,
            'question_type': None,
            'question_word': None,
            'auxiliary': None,
            'subject': None,
            'main_verb': None,
            'is_inverted': False,
            'answer_type': None,
            'formality_level': 'neutral',
            'embedded': False
        }
        
        if not self.is_applicable(sentence):
            return info
            
        info['question_found'] = True
        sentence_lower = sentence.lower().strip()
        
        # Identify question type
        for qtype, characteristics in self.QUESTION_TYPES.items():
            if re.search(characteristics['pattern'], sentence_lower):
                info['question_type'] = qtype
                info['answer_type'] = characteristics['answer_type']
                
                if 'inversion' in characteristics:
                    info['is_inverted'] = characteristics['inversion']
                if 'embedded' in characteristics:
                    info['embedded'] = characteristics.get('indirect', False)
                break
        
        # Extract WH-word if present
        wh_match = re.search(r'^(\b(?:' + '|'.join(self.WH_WORDS) + r')\b)', sentence_lower)
        if wh_match:
            info['question_word'] = wh_match.group(1)
        
        # Extract auxiliary verb
        aux_pattern = r'^(?:' + '|'.join(self.AUXILIARY_VERBS) + r')\b'
        if info['question_type'] == 'wh_question':
            # For WH-questions, auxiliary comes after WH-word
            aux_pattern = r'\b(?:' + '|'.join(self.AUXILIARY_VERBS) + r')\b'
            aux_match = re.search(aux_pattern, sentence_lower)
            if aux_match:
                info['auxiliary'] = aux_match.group(0)
        else:
            # For Yes/No questions, auxiliary comes first
            aux_match = re.search(aux_pattern, sentence_lower)
            if aux_match:
                info['auxiliary'] = aux_match.group(0)
        
        return info
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        Standard engine interface for compatibility with grammar master controller.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            Dict[str, Any]: Standardized result with slots, metadata, success
        """
        slots = self.process_sentence(sentence)
        
        # Return standardized format for grammar master controller
        return {
            'slots': slots,
            'metadata': {
                'engine': 'question_formation',
                'question_type': getattr(self, '_last_question_type', 'unknown'),
                'confidence_raw': len(slots) * 0.2  # Basic confidence calculation
            },
            'success': bool(slots),
            'error': None if slots else "No question pattern detected"
        }
    
    def process_sentence(self, sentence: str) -> Dict[str, str]:
        """
        Process a sentence containing question structures and extract slots.
        
        Args:
            sentence: Input sentence to analyze
            
        Returns:
            Dictionary containing slot assignments
        """
        return self._extract_question_slots(sentence)
    
    def _extract_question_slots(self, sentence: str) -> Dict[str, str]:
        """
        Extract slot assignments from question structures.
        """
        slots = {}
        question_info = self.extract_question_info(sentence)
        
        if not question_info['question_found']:
            self._last_question_type = None
            return slots
        
        qtype = question_info['question_type']
        self._last_question_type = qtype
        
        # Handle WH-Questions
        if qtype == 'wh_question':
            slots = self._handle_wh_question(sentence, question_info)
        
        # Handle Yes/No Questions
        elif qtype == 'yes_no':
            slots = self._handle_yes_no_question(sentence, question_info)
        
        # Handle Tag Questions
        elif qtype == 'tag_question':
            slots = self._handle_tag_question(sentence, question_info)
        
        # Handle Choice Questions
        elif qtype == 'choice_question':
            slots = self._handle_choice_question(sentence, question_info)
        
        # Handle Embedded Questions
        elif qtype == 'embedded_question':
            slots = self._handle_embedded_question(sentence, question_info)
        
        # Add question-specific metadata (no invalid slots)
        if qtype:
            slots[f'_meta_question_type'] = qtype
        if question_info.get('answer_type'):
            slots[f'_meta_answer_type'] = question_info['answer_type']
        
        # Clean up empty slots and metadata
        return {k: v for k, v in slots.items() if v and str(v).strip()}
    
    def _handle_wh_question(self, sentence: str, info: Dict) -> Dict[str, str]:
        """Handle WH-questions with proper Rephrase slot assignment"""
        slots = {}
        
        # WH-question patterns with proper slot assignment
        patterns = [
            # What/How many + auxiliary + subject + verb + (object)?
            r'^(what|how\s+many\s+\w+|how\s+much)\s+(do|does|did|are|is|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s*(.*)\?',
            
            # Where/When + auxiliary + subject + verb (M3 position)
            r'^(where|when)\s+(do|does|did|are|is|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s*(.*)\?',
            
            # Who/What + verb + object? (subject questions)
            r'^(who|what)\s+(\w+)\s*(.*)\?',
            
            # Which/Whose + noun + auxiliary + subject + verb?
            r'^(which|whose)\s+(\w+)\s+(do|does|did|are|is|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s*(.*)\?'
        ]
        
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                if i == 0:  # Pattern 1: What/How many (O1 position)
                    wh_word, aux, subject, verb, obj = groups
                    slots['O1'] = wh_word  # What/How many = target object
                    slots['Aux'] = aux
                    slots['S'] = subject
                    slots['V'] = verb
                    if obj.strip():
                        slots['O2'] = obj.strip()  # Additional object if present
                        
                elif i == 1:  # Pattern 2: Where/When (M3 position)
                    wh_word, aux, subject, verb, obj = groups
                    slots['M3'] = wh_word  # Where/When = modifier
                    slots['Aux'] = aux
                    slots['S'] = subject
                    slots['V'] = verb
                    if obj.strip():
                        slots['O1'] = obj.strip()
                        
                elif i == 2:  # Pattern 3: Who/What as subject
                    wh_word, verb, obj = groups
                    slots['S'] = wh_word  # Who/What = subject
                    slots['V'] = verb
                    if obj.strip():
                        slots['O1'] = obj.strip()
                        
                elif i == 3:  # Pattern 4: Which/Whose + noun
                    wh_word, noun, aux, subject, verb, obj = groups
                    slots['O1'] = f"{wh_word} {noun}"  # Which book = target object
                    slots['Aux'] = aux
                    slots['S'] = subject
                    slots['V'] = verb
                    if obj.strip():
                        slots['O2'] = obj.strip()
                
                return slots  # Match found, return slots
        
        return slots
    
    def _handle_yes_no_question(self, sentence: str, info: Dict) -> Dict[str, str]:
        """Handle Yes/No questions with proper word separation"""
        slots = {}
        
        # Improved Yes/No question patterns with proper word separation
        patterns = [
            # Modal + subject + verb + object?
            r'^(can|could|will|would|may|might|must|shall|should)\s+(\w+)\s+(\w+)(?:\s+(.+))?\?',
            
            # Do/Does/Did + subject + verb + object?
            r'^(do|does|did)\s+(\w+)\s+(\w+)(?:\s+(.+))?\?',
            
            # Be + subject + verb/complement?
            r'^(am|is|are|was|were)\s+(\w+)\s+(\w+)(?:\s+(.+))?\?',
            
            # Have/Has/Had + subject + verb + object?
            r'^(have|has|had)\s+(\w+)\s+(\w+)(?:\s+(.+))?\?'
        ]
        
        for i, pattern in enumerate(patterns):
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                groups = match.groups()
                aux, subject, main_word = groups[0], groups[1], groups[2]
                obj = groups[3] if len(groups) > 3 and groups[3] else None
                
                slots['Aux'] = aux
                slots['S'] = subject
                
                # Handle different auxiliary types
                if i == 0 or i == 1:  # Modal or Do-support
                    slots['V'] = main_word  # Main verb
                    if obj:
                        slots['O1'] = obj.strip()
                        
                elif i == 2:  # Be verb
                    if main_word.endswith('ing'):  # Progressive
                        slots['V'] = main_word
                        if obj:
                            slots['O1'] = obj.strip()
                    else:  # Be + complement
                        slots['V'] = aux  # Be is the main verb
                        slots['C1'] = main_word  # Complement
                        if obj:
                            slots['C2'] = obj.strip()
                            
                elif i == 3:  # Perfect tense
                    slots['V'] = main_word  # Past participle
                    if obj:
                        slots['O1'] = obj.strip()
                
                return slots
        
        return slots
    
    def _handle_tag_question(self, sentence: str, info: Dict) -> Dict[str, str]:
        """Handle tag questions with M3 for tag part"""
        slots = {}
        
        # Tag question pattern: statement + tag
        tag_pattern = r'^(.+),\s*((?:isn\'t|aren\'t|wasn\'t|weren\'t|don\'t|doesn\'t|didn\'t|haven\'t|hasn\'t|hadn\'t|won\'t|wouldn\'t|can\'t|couldn\'t|shouldn\'t|mustn\'t|am|is|are|was|were|do|does|did|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(?:he|she|it|they|you|we|i))\?'
        
        match = re.search(tag_pattern, sentence, re.IGNORECASE)
        if match:
            main_clause, tag = match.groups()
            
            # Extract slots from main clause
            slots = self._extract_statement_slots(main_clause.strip())
            
            # Add tag as M3 (modifier)
            slots['M3'] = tag.strip()
        
        return slots
        
        return slots
    
    def _handle_choice_question(self, sentence: str, info: Dict) -> Dict[str, str]:
        """Handle choice questions: tea or coffee as single O1"""
        slots = {}
        
        # Choice question pattern: auxiliary + subject + verb + choice_options
        choice_pattern = r'^(do|does|did|am|is|are|was|were|have|has|had|will|would|can|could|may|might|must|shall|should)\s+(\w+)\s+(\w+)\s+(.+\s+or\s+.+)\?'
        
        match = re.search(choice_pattern, sentence, re.IGNORECASE)
        if match:
            aux, subject, verb, choices = match.groups()
            
            slots['Aux'] = aux
            slots['S'] = subject
            slots['V'] = verb
            slots['O1'] = choices.strip()  # "tea or coffee" as single unit
        
        return slots
    
    def _handle_embedded_question(self, sentence: str, info: Dict) -> Dict[str, str]:
        """Handle embedded questions with sub-slots"""
        slots = {}
        
        # Pattern for embedded questions
        embedded_patterns = [
            # I wonder what time it is
            r'^(\w+)\s+(wonder|ask|know)\s+(what|who)\s+(.+)$',
            # Tell me where you live  
            r'^(\w+)\s+(\w+)\s+(where|when|why|how)\s+(.+)$'
        ]
        
        for pattern in embedded_patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                if len(groups) == 4:
                    subject, verb, wh_word, embedded_part = groups
                    
                    # Main clause slots
                    slots['S'] = subject
                    slots['V'] = verb
                    
                    # Embedded clause as O1 or O2 with sub-slots
                    embedded_clause = f"{wh_word} {embedded_part}"
                    
                    if verb.lower() == 'tell':
                        slots['O1'] = 'me'  # Indirect object
                        slots['O2'] = embedded_clause  # Direct object
                        slots['sub-m3'] = wh_word  # Where/when/why in embedded clause
                        slots['sub-s'] = self._extract_embedded_subject(embedded_part)
                        slots['sub-v'] = self._extract_embedded_verb(embedded_part)
                    else:
                        slots['O1'] = embedded_clause
                        if wh_word.lower() in ['where', 'when', 'why', 'how']:
                            slots['sub-m3'] = wh_word
                        else:
                            slots['sub-c1'] = wh_word  # what, who
                        slots['sub-s'] = self._extract_embedded_subject(embedded_part)
                        slots['sub-v'] = self._extract_embedded_verb(embedded_part)
                
                break
        
        return slots
    
    def _extract_embedded_subject(self, embedded_part: str) -> str:
        """Extract subject from embedded clause"""
        words = embedded_part.strip().split()
        if words:
            return words[0]  # Simple heuristic: first word as subject
        return ""
    
    def _extract_embedded_verb(self, embedded_part: str) -> str:
        """Extract verb from embedded clause"""
        words = embedded_part.strip().split()
        if len(words) > 1:
            return words[1]  # Simple heuristic: second word as verb
        return ""
    
    def _extract_statement_slots(self, statement: str) -> Dict[str, str]:
        """Helper method to extract slots from a statement (used for tag questions)."""
        slots = {}
        
        # Simple statement pattern: Subject + Verb + Object/Complement
        statement_patterns = [
            r'^(\w+)\s+(\w+)\s*(.*)$'
        ]
        
        for pattern in statement_patterns:
            match = re.search(pattern, statement.strip(), re.IGNORECASE)
            if match:
                subject, verb, rest = match.groups()
                slots['S'] = subject
                slots['V'] = verb
                if rest.strip():
                    slots['O1'] = rest.strip()
                break
        
        return slots
    
    def generate_question(self, statement: str, question_type: str = 'yes_no') -> str:
        """
        Generate a question from a given statement.
        
        Args:
            statement: Input statement
            question_type: Type of question to generate ('yes_no', 'wh_what', 'wh_where', etc.)
            
        Returns:
            Generated question string
        """
        # This would be implemented for question generation
        # For now, return the original sentence
        return statement
    
    def transform_to_statement(self, question: str) -> str:
        """
        Transform a question back to a statement form.
        
        Args:
            question: Input question
            
        Returns:
            Transformed statement
        """
        # This would be implemented for question-to-statement transformation
        # For now, return the original sentence
        return question

# Example usage and testing
if __name__ == "__main__":
    engine = QuestionFormationEngine()
    
    test_questions = [
        "What do you want?",
        "Where are you going?", 
        "Can you help me?",
        "Do you like coffee?",
        "You're coming, aren't you?",
        "Do you want tea or coffee?",
        "I wonder what time it is.",
        "Who called you yesterday?",
        "Which book did you read?"
    ]
    
    print("=== Question Formation Engine Test ===")
    for question in test_questions:
        print(f"\nInput: {question}")
        result = engine.process_sentence(question)
        print(f"Output: {result}")
        
        info = engine.extract_question_info(question)
        print(f"Type: {info.get('question_type', 'unknown')}")
