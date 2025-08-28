#!/usr/bin/env python3
"""
_analyze_relative_clause関数のデバッグスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController
import json

def debug_analyze_relative_clause():
    """_analyze_relative_clause関数を直接デバッグ"""
    
    sentence = "The car that he drives is new."
    print(f"🔍 _analyze_relative_clause デバッグ: '{sentence}'")
    print("=" * 60)
    
    controller = CentralController()
    relative_handler = controller.handlers['relative_clause']
    
    print(f"🔍 _analyze_relative_clause直接呼び出し:")
    
    try:
        result = relative_handler._analyze_relative_clause(sentence, 'that')
        print(f"📊 結果:")
        print(f"  success: {result.get('success')}")
        print(f"  antecedent: {result.get('antecedent')}")
        print(f"  relative_verb: {result.get('relative_verb')}")
        print(f"  main_clause_start: {result.get('main_clause_start')}")
        print(f"  modifiers: {result.get('modifiers')}")
        print(f"  structure_analysis: {result.get('structure_analysis')}")
        print(f"  passive_analysis: {result.get('passive_analysis')}")
    except Exception as e:
        print(f"💥 エラー: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_analyze_relative_clause()
