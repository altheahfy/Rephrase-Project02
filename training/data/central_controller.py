"""
Central Controller - 新規Rephrase文法分解システム
Phase 2: RelativeClauseHandler統合

設計方針:
- Central Controllerは文法処理を直接行わず、ハンドラーに委任
- Human Grammar Pattern: spaCy POS解析を情報源とした文法パターン認識
- 段階的100%精度達成（Phase 1: 5文型 → Phase 2: 関係節対応）
"""

import spacy
import json
from typing import Dict, List, Any, Optional
from basic_five_pattern_handler import BasicFivePatternHandler
from relative_clause_handler import RelativeClauseHandler


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
        
        # Phase 2: 5文型 + 関係節ハンドラー
        self.handlers = {
            'basic_five_pattern': BasicFivePatternHandler(),
            'relative_clause': RelativeClauseHandler()
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
        
        # Phase 2: 関係節 + 5文型の検出
        detected_patterns = []
        
        # 関係節検出（優先度最高）
        has_relative = any(token.text.lower() in ['who', 'which', 'that', 'whose', 'whom'] 
                          for token in doc)
        if has_relative:
            detected_patterns.append('relative_clause')
        
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
        
        # 2. Phase 2順次処理: 関係節→5文型の順
        final_result = {}
        
        # Step 1: 関係節処理（優先）
        if 'relative_clause' in grammar_patterns:
            rel_handler = self.handlers['relative_clause']
            rel_result = rel_handler.process(text)
            
            if rel_result['success']:
                # 関係節処理結果を保存
                final_result.update(rel_result)
                
                # 関係節が処理した代表語句をBasicFivePatternHandlerに渡す
                representative_subject = rel_result.get('main_slots', {}).get('_representative_subject', '')
                if representative_subject:
                    # 代表語句で置き換えた文を作成
                    simplified_text = self._create_simplified_text(text, rel_result)
                else:
                    simplified_text = text
            else:
                simplified_text = text
        else:
            simplified_text = text
        
        # Step 2: 5文型処理
        if 'basic_five_pattern' in grammar_patterns:
            five_handler = self.handlers['basic_five_pattern']
            five_result = five_handler.process(simplified_text)
            
            if five_result['success']:
                # 5文型結果をメインスロットとして統合
                if 'relative_clause' in grammar_patterns and final_result:
                    # 関係節結果と5文型結果を統合
                    return self._merge_results(text, final_result, five_result)
                else:
                    # 5文型のみの場合
                    return self._format_result(text, five_result['slots'])
            else:
                return self._create_error_result(text, five_result['error'])
        
        return self._create_error_result(text, "対応するハンドラーが見つかりませんでした")
    
    def _create_simplified_text(self, original_text: str, relative_result: Dict) -> str:
        """
        関係節処理結果から簡略化テキスト作成
        
        Args:
            original_text: 元の文
            relative_result: 関係節処理結果
            
        Returns:
            str: 代表語句で置き換えた簡略文
        """
        # 現在は代表語句をそのまま使用（改善余地あり）
        representative = relative_result.get('main_slots', {}).get('_representative_subject', '')
        if representative:
            # 簡易的な置き換え（より精密な実装は今後の課題）
            segments = relative_result.get('segments', {})
            main_clause_tokens = segments.get('main_clause', [])
            if main_clause_tokens:
                main_clause_text = ' '.join([t.text for t in main_clause_tokens])
                return f"{representative} {main_clause_text}"
        
        return original_text
    
    def _merge_results(self, text: str, relative_result: Dict, five_result: Dict) -> Dict[str, Any]:
        """
        関係節結果と5文型結果の統合
        
        Args:
            text: 元の文
            relative_result: 関係節処理結果
            five_result: 5文型処理結果
            
        Returns:
            Dict: 統合済み結果
        """
        # メインスロット: 5文型結果をベースに
        main_slots = five_result['slots'].copy()
        
        # サブスロット: 関係節結果から
        sub_slots = relative_result.get('sub_slots', {})
        
        # 代表語句で主語を更新
        representative = relative_result.get('main_slots', {}).get('_representative_subject', '')
        if representative and main_slots.get('S') == '':
            main_slots['S'] = representative
        
        return {
            'original_text': text,
            'success': True,
            'slots': main_slots,
            'sub_slots': sub_slots,
            'grammar_pattern': 'relative_clause + basic_five_pattern',
            'phase': 2
        }
    
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
            'phase': 2  # Phase 2に更新
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
