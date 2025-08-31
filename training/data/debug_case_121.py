#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

def debug_case_121():
    """Case 121: I know that he is smart. の詳細デバッグ"""
    
    print("🔍 Case 121詳細分析: I know that he is smart.")
    
    controller = CentralController()
    result = controller.process_sentence("I know that he is smart.")
    
    print(f"\n📋 最終結果:")
    print(f"main_slots: {result.get('main_slots', {})}")
    print(f"sub_slots: {result.get('sub_slots', {})}")
    
    if result.get('sub_slots'):
        print(f"🔍 サブスロット順序:")
        sub_slots = result['sub_slots']
        for i, (key, value) in enumerate(sub_slots.items(), 1):
            if not key.startswith('_') and value:  # メタ情報を除外
                print(f"  {i}. {key}: '{value}'")

if __name__ == "__main__":
    debug_case_121()
