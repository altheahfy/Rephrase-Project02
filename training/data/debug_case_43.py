#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 43の詳細処理パス確認
"""

import sys
import json
sys.path.append('.')

from central_controller import CentralController

def test_case_43():
    """Case 43の詳細処理確認"""
    controller = CentralController()
    sentence = "The man who runs fast is strong."
    
    print(f"🔍 Case 43詳細分析: {sentence}")
    result = controller.process_sentence(sentence)
    
    print("\n📋 最終結果:")
    print(f"main_slots: {result.get('main_slots', {})}")
    print(f"sub_slots: {result.get('sub_slots', {})}")
    
    print("\n🔍 サブスロット順序:")
    sub_slots = result.get('sub_slots', {})
    for i, (key, value) in enumerate(sub_slots.items(), 1):
        if not key.startswith('_'):
            print(f"  {i}. {key}: '{value}'")
    
    return result

if __name__ == "__main__":
    test_case_43()
