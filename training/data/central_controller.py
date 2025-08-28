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
from passive_voice_handler import PassiveVoiceHandler


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
        
        # Phase 3: 基本ハンドラーたちを先に初期化
        basic_five_pattern_handler = BasicFivePatternHandler()
        adverb_handler = AdverbHandler()
        passive_voice_handler = PassiveVoiceHandler()
        
        # 関係節ハンドラーに協力者を注入（Dependency Injection）
        collaborators = {
            'adverb': adverb_handler,
            'five_pattern': basic_five_pattern_handler,
            'passive': passive_voice_handler
        }
        relative_clause_handler = RelativeClauseHandler(collaborators)
        
        # ハンドラー辞書に登録
        self.handlers = {
            'basic_five_pattern': basic_five_pattern_handler,
            'relative_clause': relative_clause_handler,
            'adverb': adverb_handler,
            'passive_voice': passive_voice_handler
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
        has_relative = any(token.text.lower() in ['who', 'which', 'that', 'whose', 'whom', 'where', 'when', 'why', 'how'] 
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
        
        # 2. Phase 2順次処理: 関係節優先→主節処理の順
        final_result = {}
        
        # 🎯 アーキテクチャ修正: 関係節優先処理
        # 関係節がある場合は、まず関係節ハンドラーが協力者を使って境界認識
        
        if 'relative_clause' in grammar_patterns:
            # Step 1: 関係節ハンドラー（協力者と連携して境界認識）
            rel_handler = self.handlers['relative_clause']
            rel_result = rel_handler.process(text)
            
            if rel_result['success']:
                # 関係節処理結果を保存
                final_result.update(rel_result)
                
                # 関係節を除去した簡略文を作成
                simplified_text = self._create_simplified_text(text, rel_result)
                print(f"🔄 Phase 2 処理: 関係節検出 → 簡略文: '{simplified_text}'")
                
                # Step 2: 主節に対してのみ副詞ハンドラーを適用
                adverb_handler = self.handlers['adverb']
                adverb_result = adverb_handler.process(simplified_text)
                
                modifier_slots = {}
                if adverb_result['success']:
                    modifier_slots = adverb_result.get('modifier_slots', {})
                    final_simplified_text = adverb_result['separated_text']
                    for slot, value in modifier_slots.items():
                        print(f"📍 主節修飾語: {slot} = '{value}'")
                else:
                    final_simplified_text = simplified_text
                
                # Step 3: 受動態処理（主節）
                passive_handler = self.handlers['passive_voice']
                passive_result = passive_handler.process(final_simplified_text)
                
                # Step 4: 5文型処理（主節のみ）
                if 'basic_five_pattern' in grammar_patterns:
                    five_handler = self.handlers['basic_five_pattern']
                    five_result = five_handler.process(final_simplified_text)
                    
                    if five_result['success']:
                        return self._merge_results_with_passive(text, final_result, five_result, modifier_slots, passive_result)
                    else:
                        return self._create_error_result(text, five_result['error'])
                        
            else:
                print(f"⚠️ 関係節処理失敗、通常の処理フローに移行")
        
        # 関係節がない場合の通常処理フロー
        processing_text = text  # 段階的に処理されるテキスト
        
        # Step 0: 修飾語処理（最初に実施）
        adverb_handler = self.handlers['adverb']
        adverb_result = adverb_handler.process(processing_text)
        
        modifier_slots = {}  # 副詞ハンドラーから受け取る
        
        if adverb_result['success']:
            # 修飾語分離結果を保存
            final_result['modifier_info'] = adverb_result
            processing_text = adverb_result['separated_text']
            
            # 🎯 責任分担原則: 副詞ハンドラーが配置済みのMスロットを受け取る
            modifier_slots = adverb_result.get('modifier_slots', {})
            for slot, value in modifier_slots.items():
                print(f"📍 修飾語受信: {slot} = '{value}'")
            
            print(f"🔧 修飾語分離: '{text}' → '{processing_text}'")
        else:
            print(f"ℹ️ 修飾語なし、元の文を継続使用")
            
        # Step 1: 受動態処理（通常フロー）
        passive_handler = self.handlers['passive_voice']
        passive_result = passive_handler.process(processing_text)
        
        # Step 2: 5文型処理（関係節がない場合）
        if 'basic_five_pattern' in grammar_patterns:
            five_handler = self.handlers['basic_five_pattern']
            five_result = five_handler.process(processing_text)
            
            if five_result['success']:
                # 受動態対応版の結果作成
                return self._format_result_with_passive(text, five_result['slots'], modifier_slots, passive_result)
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
    
    def _merge_results(self, text: str, relative_result: Dict, five_result: Dict, modifier_slots: Dict = None) -> Dict[str, Any]:
        """
        関係節結果と5文型結果の統合（設計仕様書準拠）
        
        設計仕様: → 中央管理システム: サブ要素がある上位Sを""に設定
        
        Args:
            text: 元の文
            relative_result: 関係節処理結果
            five_result: 5文型処理結果
            modifier_slots: 修飾語スロット（Central Controllerが配置）
            
        Returns:
            Dict: 統合済み結果
        """
        # メインスロット: 5文型結果をベースに
        main_slots = five_result['slots'].copy()
        
        # 🎯 Central Controller責任: 修飾語スロットを統合
        # 関係節ケースでは、関係節内修飾語は除外
        if modifier_slots:
            # 関係節内修飾語をチェック
            sub_slots = relative_result.get('sub_slots', {})
            filtered_modifiers = {}
            
            for slot_key, modifier_value in modifier_slots.items():
                # 関係節内修飾語は主節に統合しない
                sub_modifier_found = False
                for sub_key, sub_value in sub_slots.items():
                    if sub_key.startswith('sub-m') and sub_value == modifier_value:
                        sub_modifier_found = True
                        print(f"🔍 関係節内修飾語 '{modifier_value}' を主節から除外")
                        break
                
                if not sub_modifier_found:
                    filtered_modifiers[slot_key] = modifier_value
            
            main_slots.update(filtered_modifiers)
        
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
    
    def _format_result(self, text: str, slots: Dict[str, str], modifier_slots: Dict = None) -> Dict[str, Any]:
        """
        結果フォーマット: Rephraseスロット形式に整形
        
        Args:
            text: 元の文
            slots: ハンドラーからの結果
            modifier_slots: 修飾語スロット（Central Controllerが配置）
            
        Returns:
            Dict: 整形済み結果
        """
        # メインスロットに修飾語スロットを統合
        final_slots = slots.copy()
        if modifier_slots:
            final_slots.update(modifier_slots)
            
        return {
            'original_text': text,
            'success': True,
            'main_slots': final_slots,  # 修正: main_slotsキーを追加
            'slots': final_slots,
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

    def _format_result_with_passive(self, text: str, slots: Dict[str, str], modifier_slots: Dict = None, 
                                   passive_result: Optional[Dict] = None) -> Dict[str, Any]:
        """
        結果フォーマット: 受動態対応版
        
        Args:
            text: 元の文
            slots: ハンドラーからの結果
            modifier_slots: 修飾語スロット
            passive_result: 受動態処理結果
            
        Returns:
            Dict: 整形済み結果（受動態対応）
        """
        # 基本スロットをコピー
        final_slots = slots.copy()
        
        # 受動態の場合、VをAux+Vに分離
        if passive_result and passive_result.get('is_passive'):
            # 元のVを削除してAux+Vに分離
            if 'V' in final_slots:
                del final_slots['V']
            final_slots['Aux'] = passive_result.get('aux', '')
            final_slots['V'] = passive_result.get('verb', '')
            print(f"🎯 通常フロー受動態処理: Aux='{final_slots['Aux']}', V='{final_slots['V']}'")
        
        # 修飾語スロット統合
        if modifier_slots:
            final_slots.update(modifier_slots)
        
        return {
            'original_text': text,
            'success': True,
            'slots': final_slots,
            'grammar_pattern': 'basic_five_pattern + passive_voice',
            'phase': 1  # 基本処理 + 受動態
        }
    
    def _extract_modifier_list(self, adverb_result: Dict) -> List[str]:
        """
        AdverbHandlerの複雑な結果から修飾語のリストを抽出
        （廃止予定: 副詞ハンドラーが直接スロット配置を行うため不要）
        
        Args:
            adverb_result: AdverbHandlerの結果
            
        Returns:
            List[str]: 修飾語のテキストリスト
        """
        # この機能は副詞ハンドラーに移行済み
        return []
    
    def _assign_modifier_slots(self, modifiers: List[str]) -> Dict[str, str]:
        """
        REPHRASE仕様に基づく修飾語スロット配置
        
        ルール（REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md準拠）:
        - 1個のみ → M2
        - 2個 → M2, M3 
        - 3個 → M1, M2, M3
        
        Args:
            modifiers: 修飾語のリスト
            
        Returns:
            Dict[str, str]: スロット名と修飾語のマッピング
        """
        slots = {}
        
        if len(modifiers) == 1:
            # 1個のみ → M2
            slots['M2'] = modifiers[0]
        elif len(modifiers) == 2:
            # 2個 → M2, M3
            slots['M2'] = modifiers[0]
            slots['M3'] = modifiers[1]
        elif len(modifiers) == 3:
            # 3個 → M1, M2, M3
            slots['M1'] = modifiers[0]
            slots['M2'] = modifiers[1]
            slots['M3'] = modifiers[2]
        elif len(modifiers) > 3:
            # 4個以上は最初の3個のみ使用
            slots['M1'] = modifiers[0]
            slots['M2'] = modifiers[1]
            slots['M3'] = modifiers[2]
            print(f"⚠️ 修飾語が3個を超過: {len(modifiers)}個 → 最初の3個のみ使用")
        
        return slots

    def _merge_results_with_passive(self, text: str, rel_result: Dict, five_result: Dict, 
                                  modifier_slots: Dict, passive_result: Optional[Dict]) -> Dict[str, Any]:
        """関係節、5文型、修飾語、受動態の結果を統合（受動態対応版）"""
        # 基本の5文型結果を取得
        slots = five_result.get('slots', {})
        
        # 受動態の場合、VをAux+Vに分離
        if passive_result and passive_result.get('is_passive'):
            # 元のVを削除してAux+Vに分離
            if 'V' in slots:
                del slots['V']
            slots['Aux'] = passive_result.get('aux', '')
            slots['V'] = passive_result.get('verb', '')
            print(f"🎯 受動態処理: Aux='{slots['Aux']}', V='{slots['V']}'")
        
        # 修飾語スロットを統合
        final_slots = slots.copy()
        if modifier_slots:
            final_slots.update(modifier_slots)
            
        return {
            'original_text': text,
            'success': True,
            'main_slots': final_slots,
            'slots': final_slots,
            'sub_slots': rel_result.get('sub_slots', {}),
            'grammar_pattern': 'relative_clause + basic_five_pattern + passive_voice',
            'phase': 3  # Phase 3（受動態対応）
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
