#!/usr/bin/env python3
"""
Modal Engine Slot Analysis - Direct Test

Test the _fallback_extraction method directly without Stanza dependency.
"""

import re
from typing import Dict, List, Tuple, Optional, Any

class MockModalEngine:
    """Modal Engine mock for testing slot extraction."""
    
    def __init__(self):
        """Initialize without Stanza dependency."""
        self.nlp = None
    
    # Modal classifications
    CORE_MODALS = {
        'can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must'
    }
    
    MODAL_FUNCTIONS = {
        'can': {'function': 'ability', 'certainty': 0.8, 'formality': 'neutral'},
        'could': {'function': 'ability_past', 'certainty': 0.6, 'formality': 'polite'},
        'may': {'function': 'permission', 'certainty': 0.7, 'formality': 'formal'},
        'might': {'function': 'permission_polite', 'certainty': 0.5, 'formality': 'very_polite'},
        'must': {'function': 'necessity', 'certainty': 0.95, 'formality': 'formal'},
        'have to': {'function': 'necessity', 'certainty': 0.9, 'formality': 'neutral'},
        'should': {'function': 'advice', 'certainty': 0.7, 'formality': 'neutral'},
        'will': {'function': 'future', 'certainty': 0.9, 'formality': 'neutral'},
        'would': {'function': 'conditional', 'certainty': 0.6, 'formality': 'polite'},
        'used to': {'function': 'past_habit', 'certainty': 0.95, 'formality': 'neutral'},
    }
    
    def extract_modal_info(self, sentence: str) -> Dict[str, Any]:
        """Extract modal information."""
        sentence_lower = sentence.lower()
        modal_info = {
            'modal_found': None,
            'modal_type': 'core',
            'modal_function': 'unknown',
            'is_question': sentence.strip().endswith('?')
        }
        
        # Check for core modals
        for modal in self.CORE_MODALS:
            if re.search(rf'\b{modal}\b', sentence_lower):
                modal_info['modal_found'] = modal
                modal_info['modal_type'] = 'core'
                if modal in self.MODAL_FUNCTIONS:
                    modal_info['modal_function'] = self.MODAL_FUNCTIONS[modal]['function']
                break
        
        # Check for semi-modals
        if not modal_info['modal_found']:
            semi_patterns = [
                (r'\b(?:have|has|had)\s+to\b', 'have to'),
                (r'\bused\s+to\b', 'used to'),
                (r'\b(?:am|is|are|was|were)\s+able\s+to\b', 'be able to'),
                (r'\bneed\s+to\b', 'need to'),
                (r'\bought\s+to\b', 'ought to'),
                (r'\bhad\s+better\b', 'had better'),
                (r'\bwould\s+rather\b', 'would rather'),
            ]
            
            for pattern, modal_name in semi_patterns:
                if re.search(pattern, sentence_lower):
                    modal_info['modal_found'] = modal_name
                    modal_info['modal_type'] = 'semi'
                    break
        
        return modal_info
    
    def _fallback_extraction_improved(self, sentence: str) -> Dict[str, str]:
        """Improved fallback extraction with proper Aux slot handling."""
        slots = {}
        modal_info = self.extract_modal_info(sentence)
        
        if not modal_info['modal_found']:
            return slots
        
        # Core modal processing
        if modal_info['modal_type'] == 'core':
            modal = modal_info['modal_found']
            
            # Standard pattern: Subject + Modal + Main_Verb + Rest
            pattern = rf'^(.*?)\b({re.escape(modal)})\s+(\w+)(.*)$'
            match = re.search(pattern, sentence, re.IGNORECASE)
            
            if match:
                subject, modal_verb, main_verb, rest = match.groups()
                slots['S'] = subject.strip() if subject.strip() else None
                slots['V'] = modal_verb  # Modal goes to V
                slots['Aux'] = main_verb  # Main verb goes to Aux ✅
                
                rest = rest.strip()
                if rest:
                    slots['O1'] = rest
            
            # Handle questions (Modal + Subject + Main_Verb)
            elif modal_info['is_question']:
                question_pattern = rf'^({re.escape(modal)})\s+(\w+)\s+(\w+)(.*)$'
                match = re.search(question_pattern, sentence, re.IGNORECASE)
                
                if match:
                    modal_verb, subject, main_verb, rest = match.groups()
                    slots['S'] = subject
                    slots['V'] = modal_verb
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
        
        # Clean up and return
        return {k: v for k, v in slots.items() if v and str(v).strip()}

def test_improved_modal_extraction():
    """Test the improved modal extraction."""
    
    print("🔍 IMPROVED MODAL ENGINE SLOT ANALYSIS")
    print("=" * 80)
    
    engine = MockModalEngine()
    
    test_cases = [
        # Core modals
        ("I can swim well.", {"V": "can", "Aux": "swim", "S": "I"}),
        ("She could play piano.", {"V": "could", "Aux": "play", "S": "She"}),
        ("Students must submit homework.", {"V": "must", "Aux": "submit", "S": "Students"}),
        ("We will arrive soon.", {"V": "will", "Aux": "arrive", "S": "We"}),
        ("You should study hard.", {"V": "should", "Aux": "study", "S": "You"}),
        
        # Questions
        ("Can you help me?", {"V": "Can", "Aux": "help", "S": "you"}),
        ("Will they come today?", {"V": "Will", "Aux": "come", "S": "they"}),
        ("Should we start now?", {"V": "Should", "Aux": "start", "S": "we"}),
        
        # Semi-modals
        ("I have to go home.", {"V": "have to", "Aux": "go", "S": "I"}),
        ("She has to work late.", {"V": "has to", "Aux": "work", "S": "She"}),
        ("We had to wait long.", {"V": "had to", "Aux": "wait", "S": "We"}),
        ("I need to call mom.", {"V": "need to", "Aux": "call", "S": "I"}),
        ("You ought to be careful.", {"V": "ought to", "Aux": "be", "S": "You"}),
        ("She used to live there.", {"V": "used to", "Aux": "live", "S": "She"}),
        ("I am able to help you.", {"V": "am able to", "Aux": "help", "S": "I"}),
        ("They were able to finish.", {"V": "were able to", "Aux": "finish", "S": "They"}),
    ]
    
    print(f"\n📊 Testing {len(test_cases)} modal constructions with improved extraction...")
    
    perfect_matches = 0
    aux_correct = 0
    v_correct = 0
    
    for i, (sentence, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i:2d}: {sentence}")
        
        slots = engine._fallback_extraction_improved(sentence)
        modal_info = engine.extract_modal_info(sentence)
        
        print(f"   🔧 Modal: {modal_info['modal_found']}")
        print(f"   📝 Slots: {slots}")
        print(f"   🎯 Expected: {expected}")
        
        # Check critical slots
        aux_match = slots.get('Aux') == expected.get('Aux')
        v_match = slots.get('V') == expected.get('V')
        s_match = slots.get('S') == expected.get('S')
        
        if aux_match:
            aux_correct += 1
        if v_match:
            v_correct += 1
        
        if aux_match and v_match and s_match:
            perfect_matches += 1
            print(f"   ✅ Perfect!")
        else:
            issues = []
            if not aux_match:
                issues.append(f"Aux: got '{slots.get('Aux')}', want '{expected.get('Aux')}'")
            if not v_match:
                issues.append(f"V: got '{slots.get('V')}', want '{expected.get('V')}'")
            if not s_match:
                issues.append(f"S: got '{slots.get('S')}', want '{expected.get('S')}'")
            print(f"   ⚠️  Issues: {'; '.join(issues)}")
    
    print(f"\n🎯 IMPROVED EXTRACTION RESULTS:")
    print(f"   Perfect matches: {perfect_matches}/{len(test_cases)} ({perfect_matches/len(test_cases)*100:.1f}%)")
    print(f"   Aux slot correct: {aux_correct}/{len(test_cases)} ({aux_correct/len(test_cases)*100:.1f}%)")
    print(f"   V slot correct: {v_correct}/{len(test_cases)} ({v_correct/len(test_cases)*100:.1f}%)")
    
    if aux_correct == len(test_cases):
        print(f"\n✅ ALL MAIN VERBS PROPERLY EXTRACTED TO AUX SLOT!")
    else:
        print(f"\n⚠️  Still {len(test_cases) - aux_correct} Aux slot issues")
    
    return perfect_matches, len(test_cases)

if __name__ == "__main__":
    test_improved_modal_extraction()
