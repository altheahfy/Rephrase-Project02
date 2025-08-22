#!/usr/bin/env python3
"""
Sentence Type Detector - ダミー実装
"""

class SentenceTypeDetector:
    """文型認識エンジンのダミー実装"""
    
    def __init__(self):
        pass
    
    def detect_sentence_type(self, sentence: str) -> str:
        """文の種類を検出（ダミー実装）"""
        if sentence.strip().endswith('?'):
            return 'question'
        return 'statement'
    
    def get_detection_confidence(self, sentence: str) -> float:
        """検出信頼度（ダミー実装）"""
        return 0.9