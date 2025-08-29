#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuestionHandler単体テスト - ケース86デバッグ
"""

from question_handler import QuestionHandler

def test_case_86():
    handler = QuestionHandler()
    
    test_sentence = "Where did you tell me a story?"
    print(f"テスト文: {test_sentence}")
    
    result = handler.process(test_sentence)
    
    print(f"成功: {result['success']}")
    print(f"タイプ: {result['question_type']}")
    print(f"スロット: {result['slots']}")
    print(f"期待: M2='Where', Aux='did', S='you', V='tell', O1='me', O2='a story'")

if __name__ == "__main__":
    test_case_86()
