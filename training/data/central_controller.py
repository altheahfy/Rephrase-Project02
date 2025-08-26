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
from adverb_handler import AdverbHandler


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
        """初期化: spaCy POS解析器とハンドラー群の設定（協力アプローチ版）"""
        self.nlp = spacy.load('en_core_web_sm')
        
        # Phase 2: 基本ハンドラーたちを先に初期化
        basic_five_pattern_handler = BasicFivePatternHandler()
        adverb_handler = AdverbHandler()
        
        # 関係節ハンドラーに協力者を注入（Dependency Injection）
        collaborators = {
            'adverb': adverb_handler,
            'five_pattern': basic_five_pattern_handler
        }
        relative_clause_handler = RelativeClauseHandler(collaborators)
        
        # ハンドラー辞書に登録
        self.handlers = {
            'basic_five_pattern': basic_five_pattern_handler,
            'relative_clause': relative_clause_handler,
            'adverb': adverb_handler
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
        
        # 2. Phase 2順次処理: 修飾語分離→関係節→5文型の順
        final_result = {}
        processing_text = text  # 段階的に処理されるテキスト
        
        # Step 0: 修飾語処理（最初に実施）
        adverb_handler = self.handlers['adverb']
        adverb_result = adverb_handler.process(processing_text)
        
        if adverb_result['success']:
            # 修飾語分離結果を保存
            final_result['modifier_info'] = adverb_result
            processing_text = adverb_result['separated_text']
            print(f"🔧 修飾語分離: '{text}' → '{processing_text}'")
        else:
            print(f"ℹ️ 修飾語なし、元の文を継続使用")
        
        # Step 1: 関係節処理
        if 'relative_clause' in grammar_patterns:
            rel_handler = self.handlers['relative_clause']
            # オリジナルテキストも渡して修飾語情報を保持
            rel_result = rel_handler.process(processing_text, text)
            
            if rel_result['success']:
                # 関係節処理結果を保存
                final_result.update(rel_result)
                
                # 関係節を除去した簡略文を作成
                simplified_text = self._create_simplified_text(processing_text, rel_result)
                print(f"🔄 Phase 2 処理: 関係節検出 → 簡略文: '{simplified_text}'")
            else:
                simplified_text = processing_text
                print(f"⚠️ 関係節処理失敗、修飾語分離済み文を使用")
        else:
            simplified_text = processing_text
            print(f"📝 関係節なし、修飾語分離済み文で5文型処理: '{simplified_text}'")
        
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
            str: 関係節を除去した簡略文
        """
        # RelativeClauseHandlerの結果から代表語句と主節継続部分を取得
        detection_result = relative_result.get('detection_result', {})
        antecedent = relative_result.get('antecedent', '')
        main_continuation = relative_result.get('main_continuation', '')
        
        if antecedent and main_continuation:
            # 代表語句 + 主節継続部分で簡略文作成
            simplified = f"{antecedent} {main_continuation}"
            print(f"🔄 簡略文作成: '{original_text}' → '{simplified}'")
            return simplified
        
        # フォールバック: 元の文をそのまま返す
        print(f"⚠️ 簡略文作成失敗、元の文を使用: '{original_text}'")
        return original_text
    
    def _merge_results(self, text: str, relative_result: Dict, five_result: Dict) -> Dict[str, Any]:
        """
        関係節結果と5文型結果の統合（設計仕様書準拠）
        
        設計仕様: → 中央管理システム: サブ要素がある上位Sを""に設定
        
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
        
        # 🎯 設計仕様書ルール: 「サブ要素がある上位Sを""に設定」
        if sub_slots:
            # サブスロットがある場合、対応するメインスロットを空文字列に
            if any(slot.startswith('sub-') for slot in sub_slots.keys()):
                # 関係節の場合、主にSスロットが影響を受ける
                if 'sub-s' in sub_slots or 'sub-o1' in sub_slots:
                    main_slots['S'] = ''
                    print(f"🎯 設計仕様適用: S スロットを空文字列に設定 (sub-slots存在)")
        
        return {
            'original_text': text,
            'success': True,
            'main_slots': main_slots,  # 修正: main_slotsキーを追加
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
            'main_slots': slots,  # 修正: main_slotsキーを追加
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
