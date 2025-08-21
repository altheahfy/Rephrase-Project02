#!/usr/bin/env python3
"""
AdverbialPattern - Phase 2 副詞構文処理システム
慎重なスモールステップ実装: Step 1 - 基本構造のみ
"""

from base_pattern import BasePattern
import logging

logger = logging.getLogger(__name__)

class AdverbialPattern(BasePattern):
    """
    複合副詞句の検出と処理を行うクラス
    Step 1: 基本構造のみ、実際の処理は未実装
    """
    
    def __init__(self):
        """初期化"""
        super().__init__()
        logger.debug("AdverbialPattern initialized (Step 1 - basic structure only)")
    
    def detect(self, doc, main_verb_id=None):
        """
        副詞構文の検出
        Step 1: 常にFalseを返す（まだ実装していない）
        
        Args:
            doc: Stanza解析結果
            main_verb_id: 主動詞のID (optional)
            
        Returns:
            bool: 副詞構文が検出されたかどうか
        """
        logger.debug("AdverbialPattern.detect() called - Step 1: always returns False")
        return False
    
    def correct(self, doc, main_verb_id=None):
        """
        副詞構文の修正処理
        Step 1: 何も処理しない
        
        Args:
            doc: Stanza解析結果
            main_verb_id: 主動詞のID (optional)
            
        Returns:
            dict: 空の辞書（何も修正しない）
        """
        logger.debug("AdverbialPattern.correct() called - Step 1: returns empty dict")
        return {}

# テスト用の簡単な動作確認
if __name__ == "__main__":
    pattern = AdverbialPattern()
    print("AdverbialPattern Step 1 - Basic structure created")
    print(f"detect() returns: {pattern.detect(None)}")
    print(f"correct() returns: {pattern.correct(None)}")
