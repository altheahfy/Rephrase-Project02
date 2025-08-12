#!/usr/bin/env python3
"""
Comprehensive test suite for Subjunctive/Conditional Engine.

Tests all major conditional types and subjunctive patterns with precise
slot allocation validation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.subjunctive_conditional_engine import SubjunctiveConditionalEngine

def test_conditional_type1():
    """Test real conditionals (Type 1)."""
    engine = SubjunctiveConditionalEngine()
    
    test_cases = [
        {
            'sentence': "If it rains, I will stay home.",
            'expected_type': 'conditional_type1',
            'expected_slots': {
                'S': 'I',
                'V': 'stay',
                'Aux': 'will',
                'M1': 'If it rains',
                'sub-s': 'it',
                'sub-v': 'rains'
            }
        },
        {
            'sentence': "I will call you if I have time.",
            'expected_type': 'conditional_type1',
            'expected_slots': {
                'S': 'I',
                'V': 'call',
                'Aux': 'will',
                'O1': 'you',
                'M1': 'if I have time',
                'sub-s': 'I',
                'sub-v': 'have',
                'sub-o1': 'time'
            }
        }
    ]
    
    print("Testing Type 1 Conditionals (Real):")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected_type = test_case['expected_type']
        expected_slots = test_case['expected_slots']
        
        print(f"\nTest {i}: {sentence}")
        
        if not engine.is_applicable(sentence):
            print("✗ FAIL: Engine not applicable")
            continue
            
        result = engine.process(sentence)
        
        if not result['success']:
            print(f"✗ FAIL: Processing error: {result['error']}")
            continue
        
        # Verify conditional type
        actual_type = result['metadata']['conditional_type']
        if actual_type != expected_type:
            print(f"✗ FAIL: Expected type '{expected_type}', got '{actual_type}'")
            continue
            
        # Verify slot allocations
        actual_slots = result['slots']
        all_correct = True
        
        for slot_name, expected_value in expected_slots.items():
            actual_value = actual_slots.get(slot_name, '').strip()
            if actual_value != expected_value:
                print(f"✗ FAIL: {slot_name} expected '{expected_value}', got '{actual_value}'")
                all_correct = False
        
        if all_correct:
            print("✓ PASS: All slots correct")
        else:
            print("Actual slots:")
            for name, value in actual_slots.items():
                if value.strip():
                    print(f"  {name}: '{value}'")

def test_conditional_type2():
    """Test unreal present conditionals (Type 2)."""
    engine = SubjunctiveConditionalEngine()
    
    test_cases = [
        {
            'sentence': "If I were rich, I would travel the world.",
            'expected_type': 'conditional_type2',
            'expected_slots': {
                'S': 'I',
                'V': 'travel',
                'Aux': 'would', 
                'O1': 'the world',
                'M1': 'If I were rich',
                'sub-s': 'I',
                'sub-aux': 'were',
                'sub-c1': 'rich'
            }
        },
        {
            'sentence': "If she had more time, she could finish the project.",
            'expected_type': 'conditional_type2',
            'expected_slots': {
                'S': 'she',
                'V': 'finish',
                'Aux': 'could',
                'O1': 'the project',
                'M1': 'If she had more time',
                'sub-s': 'she',
                'sub-v': 'had',
                'sub-o1': 'more time'
            }
        }
    ]
    
    print("\n\nTesting Type 2 Conditionals (Unreal Present):")
    print("-" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected_type = test_case['expected_type']
        expected_slots = test_case['expected_slots']
        
        print(f"\nTest {i}: {sentence}")
        
        if not engine.is_applicable(sentence):
            print("✗ FAIL: Engine not applicable")
            continue
            
        result = engine.process(sentence)
        
        if not result['success']:
            print(f"✗ FAIL: Processing error: {result['error']}")
            continue
        
        # Verify conditional type
        actual_type = result['metadata']['conditional_type']
        if actual_type != expected_type:
            print(f"✗ FAIL: Expected type '{expected_type}', got '{actual_type}'")
            continue
            
        # Verify slot allocations
        actual_slots = result['slots']
        all_correct = True
        
        for slot_name, expected_value in expected_slots.items():
            actual_value = actual_slots.get(slot_name, '').strip()
            if actual_value != expected_value:
                print(f"✗ FAIL: {slot_name} expected '{expected_value}', got '{actual_value}'")
                all_correct = False
        
        if all_correct:
            print("✓ PASS: All slots correct")
        else:
            print("Actual slots:")
            for name, value in actual_slots.items():
                if value.strip():
                    print(f"  {name}: '{value}'")

def test_inverted_conditionals():
    """Test inverted conditional constructions."""
    engine = SubjunctiveConditionalEngine()
    
    test_cases = [
        {
            'sentence': "Were I rich, I would buy a house.",
            'expected_type': 'inverted_conditional',
            'expected_slots': {
                'S': 'I',
                'V': 'buy',
                'Aux': 'would',
                'O1': 'a house',
                'M1': 'Were I rich',
                'sub-s': 'I',
                'sub-aux': 'Were',
                'sub-c1': 'rich'
            }
        },
        {
            'sentence': "Had she known, she would have come.",
            'expected_type': 'inverted_conditional',
            'expected_slots': {
                'S': 'she',
                'V': 'come',
                'Aux': 'would',
                'M1': 'Had she known',
                'sub-s': 'she',
                'sub-aux': 'Had',
                'sub-v': 'known'
            }
        }
    ]
    
    print("\n\nTesting Inverted Conditionals:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected_type = test_case['expected_type']
        expected_slots = test_case['expected_slots']
        
        print(f"\nTest {i}: {sentence}")
        
        if not engine.is_applicable(sentence):
            print("✗ FAIL: Engine not applicable")
            continue
            
        result = engine.process(sentence)
        
        if not result['success']:
            print(f"✗ FAIL: Processing error: {result['error']}")
            continue
        
        # Verify conditional type
        actual_type = result['metadata']['conditional_type']
        if actual_type != expected_type:
            print(f"✗ FAIL: Expected type '{expected_type}', got '{actual_type}'")
            continue
            
        # Verify slot allocations
        actual_slots = result['slots']
        all_correct = True
        
        for slot_name, expected_value in expected_slots.items():
            actual_value = actual_slots.get(slot_name, '').strip()
            if actual_value != expected_value:
                print(f"✗ FAIL: {slot_name} expected '{expected_value}', got '{actual_value}'")
                all_correct = False
        
        if all_correct:
            print("✓ PASS: All slots correct")
        else:
            print("Actual slots:")
            for name, value in actual_slots.items():
                if value.strip():
                    print(f"  {name}: '{value}'")

def test_wish_subjunctives():
    """Test wish subjunctive constructions."""
    engine = SubjunctiveConditionalEngine()
    
    test_cases = [
        {
            'sentence': "I wish I were taller.",
            'expected_type': 'wish_subjunctive',
            'expected_slots': {
                'S': 'I',
                'V': 'wish',
                'M1': 'I were taller',
                'sub-s': 'I',
                'sub-aux': 'were',
                'sub-c1': 'taller'
            }
        },
        {
            'sentence': "She wishes she had more money.",
            'expected_type': 'wish_subjunctive',
            'expected_slots': {
                'S': 'She',
                'V': 'wish',
                'M1': 'she had more money',
                'sub-s': 'she',
                'sub-v': 'had',
                'sub-o1': 'more money'
            }
        }
    ]
    
    print("\n\nTesting Wish Subjunctives:")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case['sentence']
        expected_type = test_case['expected_type']
        expected_slots = test_case['expected_slots']
        
        print(f"\nTest {i}: {sentence}")
        
        if not engine.is_applicable(sentence):
            print("✗ FAIL: Engine not applicable")
            continue
            
        result = engine.process(sentence)
        
        if not result['success']:
            print(f"✗ FAIL: Processing error: {result['error']}")
            continue
        
        # Verify conditional type
        actual_type = result['metadata']['conditional_type']
        if actual_type != expected_type:
            print(f"✗ FAIL: Expected type '{expected_type}', got '{actual_type}'")
            continue
            
        # Verify slot allocations
        actual_slots = result['slots']
        all_correct = True
        
        for slot_name, expected_value in expected_slots.items():
            actual_value = actual_slots.get(slot_name, '').strip()
            if actual_value != expected_value:
                print(f"✗ FAIL: {slot_name} expected '{expected_value}', got '{actual_value}'")
                all_correct = False
        
        if all_correct:
            print("✓ PASS: All slots correct")
        else:
            print("Actual slots:")
            for name, value in actual_slots.items():
                if value.strip():
                    print(f"  {name}: '{value}'")

def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("COMPREHENSIVE SUBJUNCTIVE/CONDITIONAL ENGINE TESTS")
    print("=" * 60)
    
    test_conditional_type1()
    test_conditional_type2()
    test_inverted_conditionals()
    test_wish_subjunctives()
    
    print("\n" + "=" * 60)
    print("Testing completed. Review results above.")

if __name__ == "__main__":
    run_comprehensive_tests()
