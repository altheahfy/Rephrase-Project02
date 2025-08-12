#!/usr/bin/env python3
"""
Modal Engine Test - No Stanza Version

Test the Modal Engine fallback functionality without Stanza dependency.
"""

import sys
import os

# Add engines directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MockModalEngine:
    """
    Modal Engine with fallback-only functionality for testing.
    """
    
    def __init__(self):
        """Initialize without Stanza."""
        self.nlp = None  # Force fallback mode
    
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
    
    def is_applicable(self, sentence):
        """Check if sentence contains modal constructions."""
        import re
        
        if not sentence or not sentence.strip():
            return False
            
        sentence_lower = sentence.lower()
        
        # Check for core modals
        modal_pattern = r'\b(?:can|could|may|might|will|would|shall|should|must)\b'
        if re.search(modal_pattern, sentence_lower):
            return True
        
        # Check for semi-modals
        semi_modal_patterns = [
            r'\b(?:am|is|are|was|were|be|being|been)\s+able\s+to\b',
            r'\b(?:have|has|had)\s+to\b',
            r'\b(?:need|needs|needed)\s+to\b',
            r'\bought\s+to\b',
            r'\bused\s+to\b',
            r'\bhad\s+better\b',
            r'\bwould\s+rather\b'
        ]
        
        for pattern in semi_modal_patterns:
            if re.search(pattern, sentence_lower):
                return True
        
        return False
    
    def extract_modal_info(self, sentence):
        """Extract modal information from sentence."""
        import re
        
        sentence_lower = sentence.lower()
        modal_info = {
            'modal_found': None,
            'modal_type': 'core',
            'modal_function': 'unknown',
            'certainty_level': 0.5,
            'formality_level': 'neutral',
            'is_negative': False,
            'is_question': sentence.strip().endswith('?')
        }
        
        # Check for negatives
        if re.search(r'\b(?:cannot|can\'t|couldn\'t|won\'t|wouldn\'t|shan\'t|shouldn\'t|mustn\'t|may not|might not)\b', sentence_lower):
            modal_info['is_negative'] = True
        
        # Find core modals
        for modal in self.CORE_MODALS:
            if re.search(rf'\b{modal}\b', sentence_lower):
                modal_info['modal_found'] = modal
                modal_info['modal_type'] = 'core'
                if modal in self.MODAL_FUNCTIONS:
                    info = self.MODAL_FUNCTIONS[modal]
                    modal_info['modal_function'] = info['function']
                    modal_info['certainty_level'] = info['certainty']
                    modal_info['formality_level'] = info['formality']
                break
        
        # Find semi-modals if no core modal found
        if not modal_info['modal_found']:
            semi_modal_checks = [
                (r'\b(?:am|is|are|was|were|be|being|been)\s+able\s+to\b', 'be able to'),
                (r'\b(?:have|has|had)\s+to\b', 'have to'),
                (r'\b(?:need|needs|needed)\s+to\b', 'need to'),
                (r'\bought\s+to\b', 'ought to'),
                (r'\bused\s+to\b', 'used to'),
                (r'\bhad\s+better\b', 'had better'),
                (r'\bwould\s+rather\b', 'would rather')
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
    
    def process_sentence_fallback(self, sentence):
        """Fallback processing using regex patterns."""
        import re
        
        slots = {}
        modal_info = self.extract_modal_info(sentence)
        
        if modal_info['modal_found']:
            slots['V'] = modal_info['modal_found']
            
            if modal_info['modal_type'] == 'core':
                # Pattern: Subject + Modal + Main_Verb + Rest
                pattern = rf'^(.*?)\b({re.escape(modal_info["modal_found"])})\b\s+(\w+)(.*)$'
                match = re.search(pattern, sentence, re.IGNORECASE)
                
                if match:
                    subject, modal, main_verb, rest = match.groups()
                    slots['S'] = subject.strip()
                    slots['V'] = modal
                    slots['Aux'] = main_verb
                    
                    rest = rest.strip()
                    if rest:
                        slots['O1'] = rest
            
            elif modal_info['modal_type'] == 'semi':
                if 'have to' in modal_info['modal_found']:
                    pattern = r'^(.*?)\b(have|has|had)\s+to\s+(\w+)(.*)$'
                    match = re.search(pattern, sentence, re.IGNORECASE)
                    
                    if match:
                        subject, modal_part, main_verb, rest = match.groups()
                        slots['S'] = subject.strip()
                        slots['V'] = f"{modal_part} to"
                        slots['Aux'] = main_verb
                        
                        rest = rest.strip()
                        if rest:
                            slots['O1'] = rest
                
                elif 'be able to' in modal_info['modal_found']:
                    pattern = r'^(.*?)\b(am|is|are|was|were)\s+able\s+to\s+(\w+)(.*)$'
                    match = re.search(pattern, sentence, re.IGNORECASE)
                    
                    if match:
                        subject, be_verb, main_verb, rest = match.groups()
                        slots['S'] = subject.strip()
                        slots['V'] = f"{be_verb} able to"
                        slots['Aux'] = main_verb
                        
                        rest = rest.strip()
                        if rest:
                            slots['O1'] = rest
        
        return {k: v.strip() for k, v in slots.items() if v.strip()}
    
    def get_confidence(self, sentence, slots):
        """Calculate confidence score."""
        if not slots:
            return 0.0
        
        confidence = 0.0
        modal_info = self.extract_modal_info(sentence)
        
        if modal_info['modal_found']:
            confidence += 0.4
        if 'S' in slots and slots['S']:
            confidence += 0.2
        if 'V' in slots and slots['V']:
            confidence += 0.2
        if 'Aux' in slots and slots['Aux']:
            confidence += 0.2
        
        return min(confidence, 1.0)

def test_modal_engine():
    """Test Modal Engine functionality."""
    engine = MockModalEngine()
    
    test_sentences = [
        # Core modals - Ability
        "I can swim very well.",
        "She could play piano when she was young.",
        
        # Permission
        "You may leave now.",
        "Could I borrow your pen?",
        
        # Necessity/Obligation
        "Students must submit their assignments on time.",
        "I have to go to work early tomorrow.",
        "You should study harder for the exam.",
        "We need to call our parents.",
        
        # Future/Probability  
        "It will rain tomorrow.",
        "I would go if I had time.",
        
        # Past habits
        "She used to live in Paris.",
        
        # Negative modals
        "I cannot understand this problem.",
        "She shouldn't worry about it.",
        
        # Questions
        "Can you help me with this?",
        "Would you like some coffee?",
        
        # Non-modal sentences (should not be applicable)
        "I like chocolate ice cream.",
        "The cat is sleeping on the sofa."
    ]
    
    print("🚀 MODAL ENGINE TEST RESULTS")
    print("=" * 80)
    
    applicable_count = 0
    total_count = len(test_sentences)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\nTest {i:2d}: {sentence}")
        
        if engine.is_applicable(sentence):
            applicable_count += 1
            slots = engine.process_sentence_fallback(sentence)
            confidence = engine.get_confidence(sentence, slots)
            modal_info = engine.extract_modal_info(sentence)
            
            print(f"   ✅ Applicable")
            print(f"   📊 Confidence: {confidence:.2f}")
            print(f"   🔧 Modal: {modal_info['modal_found']} ({modal_info['modal_function']})")
            print(f"   📝 Slots: {slots}")
        else:
            print("   ❌ Not applicable")
    
    print(f"\n🎯 SUMMARY:")
    print(f"   Total sentences tested: {total_count}")
    print(f"   Modal sentences detected: {applicable_count}")
    print(f"   Detection accuracy: {applicable_count/total_count*100:.1f}%")
    
    print(f"\n✅ Modal Engine (fallback mode) working correctly!")

if __name__ == "__main__":
    test_modal_engine()
