#!/usr/bin/env python3
"""
Modal Engine Detailed Slot Analysis

Check if all modals are properly extracting to Aux/sub-aux slots.
"""

import sys
import os
import re

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.modal_engine import ModalEngine

def analyze_modal_slot_extraction():
    """Analyze detailed slot extraction for all modal types."""
    
    print("🔍 MODAL ENGINE DETAILED SLOT ANALYSIS")
    print("=" * 80)
    
    engine = ModalEngine()
    
    # Comprehensive test sentences for all modal types
    test_cases = [
        # Core modals - Should have modal in V, main verb in Aux
        ("I can swim well.", {"V": "can", "Aux": "swim", "S": "I"}),
        ("She could play piano.", {"V": "could", "Aux": "play", "S": "She"}),
        ("You may leave now.", {"V": "may", "Aux": "leave", "S": "You"}),
        ("It might rain tomorrow.", {"V": "might", "Aux": "rain", "S": "It"}),
        ("We will arrive soon.", {"V": "will", "Aux": "arrive", "S": "We"}),
        ("They would help us.", {"V": "would", "Aux": "help", "S": "They"}),
        ("You should study hard.", {"V": "should", "Aux": "study", "S": "You"}),
        ("Students must submit assignments.", {"V": "must", "Aux": "submit", "S": "Students"}),
        
        # Semi-modals - Should extract properly
        ("I have to go home.", {"V": "have to", "Aux": "go", "S": "I"}),
        ("She has to work late.", {"V": "has to", "Aux": "work", "S": "She"}),
        ("We had to wait long.", {"V": "had to", "Aux": "wait", "S": "We"}),
        ("I need to call mom.", {"V": "need to", "Aux": "call", "S": "I"}),
        ("You ought to be careful.", {"V": "ought to", "Aux": "be", "S": "You"}),
        ("She used to live there.", {"V": "used to", "Aux": "live", "S": "She"}),
        ("I am able to help you.", {"V": "am able to", "Aux": "help", "S": "I"}),
        ("They are able to solve it.", {"V": "are able to", "Aux": "solve", "S": "They"}),
        ("He was able to finish.", {"V": "was able to", "Aux": "finish", "S": "He"}),
        
        # Questions
        ("Can you help me?", {"V": "can", "Aux": "help", "S": "you"}),
        ("Would you like coffee?", {"V": "would", "Aux": "like", "S": "you"}),
        ("Should we start now?", {"V": "should", "Aux": "start", "S": "we"}),
        
        # Complex examples
        ("I would rather stay home.", {"V": "would rather", "Aux": "stay", "S": "I"}),
        ("You had better finish this.", {"V": "had better", "Aux": "finish", "S": "You"}),
    ]
    
    print(f"\n📊 Testing {len(test_cases)} modal constructions...")
    
    correct_extractions = 0
    aux_slot_issues = []
    v_slot_issues = []
    s_slot_issues = []
    
    for i, (sentence, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i:2d}: {sentence}")
        
        # Test modal detection
        if engine.is_applicable(sentence):
            slots = engine.process_sentence(sentence)
            modal_info = engine.extract_modal_info(sentence)
            
            print(f"   🔧 Detected Modal: {modal_info['modal_found']} ({modal_info['modal_function']})")
            print(f"   📝 Extracted Slots: {slots}")
            print(f"   🎯 Expected Slots: {expected}")
            
            # Check each important slot
            issues = []
            
            # Check V slot (modal)
            if 'V' in expected:
                if 'V' not in slots:
                    issues.append("Missing V slot")
                    v_slot_issues.append(sentence)
                elif slots['V'] != expected['V']:
                    issues.append(f"V slot mismatch: got '{slots['V']}', expected '{expected['V']}'")
                    v_slot_issues.append(sentence)
            
            # Check Aux slot (main verb) - CRITICAL
            if 'Aux' in expected:
                if 'Aux' not in slots:
                    issues.append("Missing Aux slot")
                    aux_slot_issues.append(sentence)
                elif slots['Aux'] != expected['Aux']:
                    issues.append(f"Aux slot mismatch: got '{slots['Aux']}', expected '{expected['Aux']}'")
                    aux_slot_issues.append(sentence)
            
            # Check S slot (subject)
            if 'S' in expected:
                if 'S' not in slots:
                    issues.append("Missing S slot")
                    s_slot_issues.append(sentence)
                elif slots['S'] != expected['S']:
                    issues.append(f"S slot mismatch: got '{slots['S']}', expected '{expected['S']}'")
                    s_slot_issues.append(sentence)
            
            if issues:
                print(f"   ⚠️  Issues: {'; '.join(issues)}")
            else:
                print(f"   ✅ Perfect extraction!")
                correct_extractions += 1
        else:
            print(f"   ❌ Not detected as modal sentence")
    
    print(f"\n🎯 DETAILED ANALYSIS RESULTS:")
    print(f"   Total test cases: {len(test_cases)}")
    print(f"   Perfect extractions: {correct_extractions}")
    print(f"   Accuracy: {(correct_extractions/len(test_cases)*100):.1f}%")
    
    print(f"\n⚠️  SLOT-SPECIFIC ISSUES:")
    print(f"   V slot issues: {len(v_slot_issues)} cases")
    print(f"   Aux slot issues: {len(aux_slot_issues)} cases - CRITICAL!")
    print(f"   S slot issues: {len(s_slot_issues)} cases")
    
    if aux_slot_issues:
        print(f"\n🔴 AUX SLOT PROBLEMS (main verbs not properly extracted):")
        for i, sentence in enumerate(aux_slot_issues[:5], 1):  # Show first 5
            print(f"   {i}. {sentence}")
    
    if v_slot_issues:
        print(f"\n🟡 V SLOT PROBLEMS (modals not properly extracted):")
        for i, sentence in enumerate(v_slot_issues[:5], 1):
            print(f"   {i}. {sentence}")
    
    # Identify the main issue
    if aux_slot_issues:
        print(f"\n🚨 CRITICAL ISSUE IDENTIFIED:")
        print(f"   Main verbs are NOT being properly extracted to Aux slot!")
        print(f"   This means the modal analysis is incomplete.")
        print(f"   Need to fix the _fallback_extraction method.")
    
    return correct_extractions, len(test_cases)

if __name__ == "__main__":
    analyze_modal_slot_extraction()
