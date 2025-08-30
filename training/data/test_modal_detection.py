#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ModalHandler助動詞検出テスト
"""

from modal_handler import ModalHandler

def test_modal_detection():
    handler = ModalHandler()
    
    test_cases = [
        "They had already left the building.",
        "They had left the building.",
        "I have completed the project.",
        "She has lived here for ten years."
    ]
    
    for text in test_cases:
        print(f"\n=== テスト: {text} ===")
        modal_info = handler.detect_modal_structure(text)
        print(f"助動詞検出結果: {modal_info}")
        
        if modal_info.get('has_modal', False):
            print(f"✅ 助動詞検出成功: {modal_info['auxiliary']}")
        else:
            print("❌ 助動詞検出失敗")

if __name__ == "__main__":
    test_modal_detection()
