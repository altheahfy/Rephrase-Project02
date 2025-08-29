#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ケース84,85デバッグ
"""

from question_handler import QuestionHandler

def test_cases_84_85():
    handler = QuestionHandler()
    
    test_cases = [
        "Did he tell her a secret there?",
        "Did I tell him a truth in the kitchen?"
    ]
    
    for i, sentence in enumerate(test_cases, 84):
        print(f"\n=== ケース{i} ===")
        print(f"テスト文: {sentence}")
        
        # 修飾語分離後の文をシミュレート
        if "there" in sentence:
            clean_sentence = sentence.replace(" there", " ")
        elif "in the kitchen" in sentence:
            clean_sentence = sentence.replace(" in the kitchen", " ")
        else:
            clean_sentence = sentence
            
        print(f"修飾語分離後: {clean_sentence}")
        
        result = handler.process(clean_sentence)
        
        print(f"成功: {result['success']}")
        print(f"タイプ: {result['question_type']}")
        print(f"スロット: {result['slots']}")

if __name__ == "__main__":
    test_cases_84_85()
