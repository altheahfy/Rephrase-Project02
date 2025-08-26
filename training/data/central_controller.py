"""
Central Controller - 新規Rephrase文法分解システム
Phase 1: BasicFivePatternHandler統合

設計方針:
- Central Controllerは文法処理を直接行わず、ハンドラーに委任
- Human Grammar Pattern: spaCy POS解析を情報源とした文法パターン認識
- 段階的100%精度達成（Phase 1: 5文型のみ）
"""

import spacy
import json
from typing import Dict, List, Any, Optional
from basic_five_pattern_handler import BasicFivePatternHandler


class CentralController:
    """
    中央管理システム - 文法解析→ハンドラー選択→結果統合
    
    責任:
    - 文法項目特定
    - 適切なハンドラーへの処理委任
    - 結果統合・order管理
    
    禁止:
    - 直接的な文法処理
    - spaCy依存関係解析の使用
    - ハードコーディング
    """
    
    def __init__(self):
        """初期化: spaCy POS解析器とハンドラー群の設定"""
        self.nlp = spacy.load('en_core_web_sm')
        
        # Phase 1: 5文型ハンドラーのみ
        self.handlers = {
            'basic_five_pattern': BasicFivePatternHandler()
        }
        
        # Rephraseスロット定義読み込み
        self.slot_structure = self._load_slot_structure()
        
    def _load_slot_structure(self) -> Dict[str, Any]:
        """slot_order_data.jsonからRephraseスロット構造を読み込み"""
        try:
            with open('slot_order_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("slot_order_data.json が見つかりません")
    
    def analyze_grammar_structure(self, text: str) -> List[str]:
        """
        文法構造分析: 使用されている文法項目を特定
        
        Args:
            text: 分析対象の英語文
            
        Returns:
            List[str]: 検出された文法項目リスト（優先度順）
        """
        doc = self.nlp(text)
        
        # Phase 1: 5文型のみ検出
        detected_patterns = []
        
        # 基本5文型の存在確認（POS解析ベース）
        has_verb = any(token.pos_ in ['VERB', 'AUX'] for token in doc)
        has_noun = any(token.pos_ in ['NOUN', 'PRON', 'PROPN'] for token in doc)
        
        if has_verb and has_noun:
            detected_patterns.append('basic_five_pattern')
            
        return detected_patterns
    
    def process_sentence(self, text: str) -> Dict[str, Any]:
        """
        文の処理: 文法分析→ハンドラー委任→結果統合
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: Rephraseスロット形式の結果
        """
        # 1. 文法構造分析
        grammar_patterns = self.analyze_grammar_structure(text)
        
        if not grammar_patterns:
            return self._create_error_result(text, "文法パターンが検出されませんでした")
        
        # 2. ハンドラー選択・処理委任
        # Phase 1: basic_five_patternのみ
        if 'basic_five_pattern' in grammar_patterns:
            handler = self.handlers['basic_five_pattern']
            result = handler.process(text)
            
            if result['success']:
                return self._format_result(text, result['slots'])
            else:
                return self._create_error_result(text, result['error'])
        
        return self._create_error_result(text, "対応するハンドラーが見つかりませんでした")
    
    def _format_result(self, text: str, slots: Dict[str, str]) -> Dict[str, Any]:
        """
        結果フォーマット: Rephraseスロット形式に整形
        
        Args:
            text: 元の文
            slots: ハンドラーからの結果
            
        Returns:
            Dict: 整形済み結果
        """
        return {
            'original_text': text,
            'success': True,
            'slots': slots,
            'grammar_pattern': 'basic_five_pattern',
            'phase': 1
        }
    
    def _create_error_result(self, text: str, error_message: str) -> Dict[str, Any]:
        """エラー結果作成"""
        return {
            'original_text': text,
            'success': False,
            'error': error_message,
            'phase': 1
        }


if __name__ == "__main__":
    # Phase 1テスト
    controller = CentralController()
    
    test_sentences = [
        "She is happy.",           # 第2文型
        "I love you.",             # 第3文型  
        "He gave me a book.",      # 第4文型
        "We made him happy."       # 第5文型
    ]
    
    print("=== Phase 1: Central Controller テスト ===")
    for sentence in test_sentences:
        print(f"\n入力: {sentence}")
        result = controller.process_sentence(sentence)
        print(f"結果: {result}")
