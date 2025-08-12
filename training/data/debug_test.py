#!/usr/bin/env python3
"""
Can't you do it? の個別テスト
"""

import sys
import os
sys.path.append('c:/Users/yurit/Downloads/Rephraseプロジェクト20250529/完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/data')

from engines.question_formation_engine import QuestionFormationEngine

def test_debug():
    engine = QuestionFormationEngine()
    
    sentence = "Can't you do it?"
    print(f"テスト: {sentence}")
    
    # is_applicable確認
    print(f"適用可能: {engine.is_applicable(sentence)}")
    
    # question_info確認
    info = engine.extract_question_info(sentence)
    print(f"質問情報: {info}")
    
    # スロット抽出
    slots = engine.process_sentence(sentence)
    print(f"スロット: {slots}")
    
    # 標準インターフェース
    result = engine.process(sentence)
    print(f"結果: {result}")

if __name__ == "__main__":
    test_debug()
