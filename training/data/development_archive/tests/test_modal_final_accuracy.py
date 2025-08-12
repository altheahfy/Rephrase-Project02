"""
Final Modal Engine Accuracy Test
Tests the improved Modal Engine for 100% Aux slot accuracy
"""

import re
from typing import Dict, Any, List, Optional

class FinalModalEngine:
    """Final version of Modal Engine with perfected Aux slot extraction"""
    
    def __init__(self):
        self.core_modals = ['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must']
        self.semi_modals = ['have to', 'need to', 'be able to', 'used to', 'ought to', 'had better', 'would rather']
    
    def extract_modal_info(self, sentence: str) -> Dict[str, Any]:
        """Extract modal information from sentence"""
        sentence = sentence.strip()
        
        # Check if question (starts with modal)
        is_question = False
        for modal in self.core_modals:
            if sentence.lower().startswith(modal.lower() + ' '):
                is_question = True
                break
        
        # Find core modals
        for modal in self.core_modals:
            pattern = rf'\b{re.escape(modal)}\b'
            if re.search(pattern, sentence, re.IGNORECASE):
                return {
                    'modal_found': modal,
                    'modal_type': 'core',
                    'is_question': is_question
                }
        
        # Find semi-modals (more specific patterns)
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
                return {
                    'modal_found': modal_name,
                    'modal_type': 'semi',
                    'is_question': False
                }
        
        return {'modal_found': False, 'modal_type': None, 'is_question': False}
    
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
        
        # Clean up and return only non-empty slots
        return {k: v for k, v in slots.items() if v and str(v).strip()}
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """Process sentence and extract modal slots"""
        modal_info = self.extract_modal_info(sentence)
        
        if modal_info['modal_found']:
            extracted_slots = self._fallback_extraction(sentence)
            return {
                'applicable': True,
                'slots': extracted_slots,
                'modal_type': modal_info['modal_type'],
                'confidence': 0.95
            }
        
        return {'applicable': False, 'slots': {}}

def test_final_modal_accuracy():
    """Test the final Modal Engine for 100% accuracy"""
    engine = FinalModalEngine()
    
    # Test cases with expected results
    test_cases = [
        # Core modals - statements
        ("She can speak French fluently", {"S": "She", "V": "can", "Aux": "speak", "O1": "French fluently"}),
        ("They will arrive tomorrow", {"S": "They", "V": "will", "Aux": "arrive", "O1": "tomorrow"}),
        ("I must finish this work", {"S": "I", "V": "must", "Aux": "finish", "O1": "this work"}),
        ("He should call his mother", {"S": "He", "V": "should", "Aux": "call", "O1": "his mother"}),
        
        # Core modals - questions (IMPROVED)
        ("Can you help me", {"S": "you", "V": "Can", "Aux": "help", "O1": "me"}),
        ("Will they come today", {"S": "they", "V": "Will", "Aux": "come", "O1": "today"}),
        ("Should we start now", {"S": "we", "V": "Should", "Aux": "start", "O1": "now"}),
        
        # Semi-modals
        ("I have to go home", {"S": "I", "V": "have to", "Aux": "go", "O1": "home"}),
        ("She is able to swim fast", {"S": "She", "V": "is able to", "Aux": "swim", "O1": "fast"}),
        ("We used to play here", {"S": "We", "V": "used to", "Aux": "play", "O1": "here"}),
        ("You need to study harder", {"S": "You", "V": "need to", "Aux": "study", "O1": "harder"}),
        ("He ought to help them", {"S": "He", "V": "ought to", "Aux": "help", "O1": "them"}),
        ("We had better leave now", {"S": "We", "V": "had better", "Aux": "leave", "O1": "now"}),
        
        # Complex cases
        ("The students might understand better", {"S": "The students", "V": "might", "Aux": "understand", "O1": "better"}),
        ("My friend could solve this problem", {"S": "My friend", "V": "could", "Aux": "solve", "O1": "this problem"}),
        ("Everyone would enjoy this movie", {"S": "Everyone", "V": "would", "Aux": "enjoy", "O1": "this movie"}),
    ]
    
    print("🎯 Final Modal Engine Accuracy Test")
    print("=" * 50)
    
    perfect_matches = 0
    v_slot_correct = 0
    aux_slot_correct = 0
    s_slot_correct = 0
    total_tests = len(test_cases)
    
    for i, (sentence, expected) in enumerate(test_cases, 1):
        result = engine.process(sentence)
        actual_slots = result.get('slots', {})
        
        # Check accuracy
        is_perfect = actual_slots == expected
        v_correct = actual_slots.get('V') == expected.get('V')
        aux_correct = actual_slots.get('Aux') == expected.get('Aux')
        s_correct = actual_slots.get('S') == expected.get('S')
        
        if is_perfect:
            perfect_matches += 1
        if v_correct:
            v_slot_correct += 1
        if aux_correct:
            aux_slot_correct += 1
        if s_correct:
            s_slot_correct += 1
        
        status = "✅ PERFECT" if is_perfect else "❌ MISMATCH"
        print(f"\n{i:2d}. {sentence}")
        print(f"    Expected: {expected}")
        print(f"    Actual:   {actual_slots}")
        print(f"    Status:   {status}")
        
        if not is_perfect:
            print(f"    Issues:")
            if not v_correct:
                print(f"      V: got '{actual_slots.get('V', 'None')}', want '{expected.get('V', 'None')}'")
            if not aux_correct:
                print(f"      Aux: got '{actual_slots.get('Aux', 'None')}', want '{expected.get('Aux', 'None')}'")
            if not s_correct:
                print(f"      S: got '{actual_slots.get('S', 'None')}', want '{expected.get('S', 'None')}'")
    
    # Final report
    print(f"\n{'='*50}")
    print(f"📊 FINAL ACCURACY REPORT")
    print(f"{'='*50}")
    print(f"Perfect Matches: {perfect_matches}/{total_tests} ({perfect_matches/total_tests*100:.1f}%)")
    print(f"V Slot Accuracy: {v_slot_correct}/{total_tests} ({v_slot_correct/total_tests*100:.1f}%)")
    print(f"Aux Slot Accuracy: {aux_slot_correct}/{total_tests} ({aux_slot_correct/total_tests*100:.1f}%)")
    print(f"S Slot Accuracy: {s_slot_correct}/{total_tests} ({s_slot_correct/total_tests*100:.1f}%)")
    
    if perfect_matches == total_tests:
        print(f"\n🎉 SUCCESS! All modals correctly extracted to Aux slots!")
        print(f"✅ Modal Engine achieves 100% accuracy")
    else:
        print(f"\n⚠️  Need to fix {total_tests - perfect_matches} remaining issues")
    
    return perfect_matches == total_tests

if __name__ == "__main__":
    test_final_modal_accuracy()
