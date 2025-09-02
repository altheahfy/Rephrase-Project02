#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from infinitive_handler import InfinitiveHandler
import spacy

# spaCyモデル読み込み
nlp = spacy.load('en_core_web_sm')

# InfinitiveHandler初期化
handler = InfinitiveHandler(nlp)

# テスト文
test_cases = [
    "He seems to have finished his work.",
    "This problem needs to be solved quickly.", 
    "I don't know what to do.",
    "I want you to help me.",
    "The meeting is about to start.",
    "She studies hard in order to pass the exam.",
    "He left early so as to avoid traffic."
]

print("🔍 InfinitiveHandler.can_handle() テスト")
print("=" * 60)

for text in test_cases:
    can_handle_result = handler.can_handle(text)
    print(f"✅ can_handle('{text}'): {can_handle_result}")
    
    if can_handle_result:
        print(f"   ➜ パターン検出成功")
    else:
        print(f"   ➜ パターン検出失敗")
    print()
