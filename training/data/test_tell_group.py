#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from central_controller import CentralController

def test_tell_group_ordering():
    """tellグループの絶対順序システムテスト"""
    
    controller = CentralController()
    
    # tellグループの例文をテスト
    tell_sentences = [
        "I tell him the truth.",
        "She tells me the story.",
        "He told her the secret."
    ]
    
    print("🎯 tellグループ絶対順序システムテスト")
    print("="*50)
    
    for i, sentence in enumerate(tell_sentences, 1):
        print(f"\n📝 例文{i}: {sentence}")
        
        result = controller.process_sentence(sentence)
        
        print(f"🔧 処理結果:")
        print(f"  main_slots: {result.get('main_slots', {})}")
        print(f"  ordered_slots: {result.get('ordered_slots', {})}")
        print(f"  v_group_key: {result.get('v_group_key', 'unknown')}")
        
        # サブスロットがある場合は表示
        if result.get('sub_slots'):
            print(f"  sub_slots: {result.get('sub_slots', {})}")
        
        if result.get('ordered_sub_slots'):
            print(f"  ordered_sub_slots: {result.get('ordered_sub_slots', {})}")

if __name__ == "__main__":
    test_tell_group_ordering()
