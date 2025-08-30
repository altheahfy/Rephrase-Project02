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
from relative_adverb_handler import RelativeAdverbHandler
from adverb_handler import AdverbHandler
from passive_voice_handler import PassiveVoiceHandler
from question_handler import QuestionHandler
from modal_handler import ModalHandler
from pure_data_driven_order_manager import PureDataDrivenOrderManager
# from dynamic_absolute_order_manager import DynamicAbsoluteOrderManager  # 破棄済み


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
        
        # 動的分析用のグループマッピングを初期化
        self._initialize_group_mappings()
        
        # Phase 6: 基本ハンドラーたちを先に初期化
        basic_five_pattern_handler = BasicFivePatternHandler()
        adverb_handler = AdverbHandler()
        passive_voice_handler = PassiveVoiceHandler()
        question_handler = QuestionHandler()
        modal_handler = ModalHandler(self.nlp)  # Phase 6: ModalHandler追加
        
        # Pure Data-Driven Order Manager を初期化
        self.order_manager = PureDataDrivenOrderManager()
        
        # 関係節ハンドラーに協力者を注入（Dependency Injection）
        collaborators = {
            'adverb': adverb_handler,
            'five_pattern': basic_five_pattern_handler,
            'passive': passive_voice_handler,
            'modal': modal_handler
        }
        relative_clause_handler = RelativeClauseHandler(collaborators)
        relative_adverb_handler = RelativeAdverbHandler(collaborators)
        
        # ハンドラー辞書に登録
        self.handlers = {
            'basic_five_pattern': basic_five_pattern_handler,
            'relative_clause': relative_clause_handler,
            'relative_adverb': relative_adverb_handler,
            'adverb': adverb_handler,
            'passive_voice': passive_voice_handler,
            'question': question_handler,
            'modal': modal_handler  # Phase 6: ModalHandler追加
        }
        
        # Rephraseスロット定義読み込み
        self.slot_structure = self._load_slot_structure()
    
    def _apply_order_to_result(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        処理結果に順序情報を追加
        """
        if not result_dict.get('success', False):
            return result_dict
        
        main_slots = result_dict.get('main_slots', {})
        text = result_dict.get('text', '') or result_dict.get('original_text', '')
        
        if not main_slots or not text:
            print(f"⚠️ 順序付与スキップ: main_slots={bool(main_slots)}, text='{text}'")
            return result_dict
        
        try:
            # V_group_keyを推定（簡単な実装）
            v_group_key = self._determine_v_group_key(main_slots, text)
            print(f"🔍 推定V_group_key: {v_group_key}")
            
            # 例文データ構造を作成
            sentence_data = [{
                'sentence': text,
                'slots': main_slots
            }]
            
            # Pure Data-Driven Order Manager で順序を取得
            order_results = self.order_manager.process_adverb_group(v_group_key, sentence_data)
            
            if order_results and len(order_results) > 0:
                ordered_slots = order_results[0].get('ordered_slots', {})
                result_dict['ordered_slots'] = ordered_slots
                print(f"✅ 順序付与成功: {ordered_slots}")
            else:
                print(f"⚠️ 順序付与結果が空です")
            
        except Exception as e:
            print(f"⚠️ 順序付与エラー: {e}")
            # エラーでも基本結果は返す
        
        return result_dict
    
    def _determine_v_group_key(self, main_slots: Dict, text: str) -> str:
        """
        V_group_keyを推定（簡単な実装）
        """
        verb = main_slots.get('V', '').lower()
        if 'tell' in verb:
            return 'tell'
        elif 'give' in verb or 'gave' in verb:
            return 'give'
        else:
            return 'action'  # デフォルト
        
    def _initialize_group_mappings(self):
        """動的分析用のグループマッピングを初期化 - 実際のデータから読み込み"""
        
        # 実際のデータファイルからtellグループを抽出
        tell_examples = self._extract_real_group_data("tell")
        gave_examples = self._extract_real_group_data("gave")
        
        if not tell_examples:
            print("⚠️ tellグループのデータが見つかりません。スキップします。")
            return
            
        print(f"📚 実際のtellグループ例文 ({len(tell_examples)}件):")
        for i, example in enumerate(tell_examples, 1):
            print(f"  {i}. {example}")
        
        # 注意: 動的分析は現在PureDataDrivenOrderManagerで処理
        print("✅ グループマッピングの初期化完了（PureDataDrivenOrderManager使用）")
    
    def _extract_real_group_data(self, group_key: str) -> List[str]:
        """実際のデータファイルから指定グループの例文を抽出"""
        try:
            with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            examples = []
            for key, item in data['data'].items():
                if item.get('V_group_key') == group_key:
                    # basic_5_patternsカテゴリのみを使用（テスト用は除外）
                    category = item.get('grammar_category', 'unknown')
                    if category == 'basic_5_patterns':
                        examples.append(item['sentence'])
            
            return examples
        except Exception as e:
            print(f"⚠️ {group_key}グループデータ抽出エラー: {e}")
            return []
        
    def _load_slot_structure(self) -> Dict[str, Any]:
        """slot_order_data.jsonからRephraseスロット構造を読み込み"""
        try:
            with open('slot_order_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("slot_order_data.json が見つかりません")
    
    def _determine_group_key(self, slots: Dict[str, str], text: str) -> str:
        """スロットと文章から動詞グループキーを決定"""
        if 'V' in slots:
            verb = slots['V'].lower()
            if 'tell' in verb:
                return 'tell'
            elif 'gave' in verb or 'give' in verb:
                return 'gave'
        
        # 文章からも動詞を検出
        text_lower = text.lower()
        if 'tell' in text_lower or 'told' in text_lower:
            return 'tell'
        elif 'gave' in text_lower or 'give' in text_lower:
            return 'gave'
        
        # デフォルト
        return 'basic'
    
    def analyze_grammar_structure(self, text: str) -> List[str]:
        """
        文法構造分析: 使用されている文法項目を特定
        
        Args:
            text: 分析対象の英語文
            
        Returns:
            List[str]: 検出された文法項目リスト（優先度順）
        """
        doc = self.nlp(text)
        
        # Phase 6: 疑問文 + 助動詞 + 関係節 + 5文型の検出
        detected_patterns = []
        
        # 疑問文検出（最優先）
        if self.handlers['question'].is_question(text):
            detected_patterns.append('question')
        
        # 助動詞検出（高優先度）
        modal_info = self.handlers['modal'].detect_modal_structure(text)
        if modal_info.get('has_modal', False):
            detected_patterns.append('modal')
        
        # 関係節検出（優先度高）
        has_relative = any(token.text.lower() in ['who', 'which', 'that', 'whose', 'whom'] 
                          for token in doc)
        # 関係副詞検出（関係節より優先）
        import re
        relative_adverb_patterns = [
            r'\bthe\s+\w+\s+where\b',
            r'\bthe\s+\w+\s+when\b', 
            r'\bthe\s+\w+\s+why\b',
            r'\bthe\s+\w+\s+how\b'
        ]
        has_relative_adverb = any(re.search(pattern, text.lower()) for pattern in relative_adverb_patterns)
        
        if has_relative_adverb:
            detected_patterns.append('relative_adverb')
        elif has_relative:
            detected_patterns.append('relative_clause')
        
        # 基本5文型の存在確認（POS解析ベース）
        has_verb = any(token.pos_ in ['VERB', 'AUX'] for token in doc)
        has_noun = any(token.pos_ in ['NOUN', 'PRON', 'PROPN'] for token in doc)
        
        if has_verb and has_noun:
            detected_patterns.append('basic_five_pattern')
            
        return detected_patterns
    
    def _normalize_question_to_statement(self, question_text: str, question_result: Dict) -> str:
        """
        疑問文を平叙文に正規化してBasicFivePatternHandlerで処理可能にする
        
        Args:
            question_text: 疑問文テキスト
            question_result: QuestionHandlerの処理結果
            
        Returns:
            str: 正規化された平叙文
        """
        if not question_result.get('success'):
            return question_text
        
        question_type = question_result.get('question_type')
        slots = question_result.get('slots', {})
        
        # Yes/No疑問文の正規化: "Did he tell her a secret ?" → "He tell her a secret"
        if question_type == 'yes_no_question':
            text = question_text.strip()
            if text.endswith('?'):
                text = text[:-1].strip()
            
            # 助動詞を除去して語順を調整
            if 'Aux' in slots and 'S' in slots:
                aux = slots['Aux'].lower()
                subject = slots['S']
                
                # "Did/Do/Does" + 主語 → 主語のみ
                if aux in ['did', 'do', 'does']:
                    # "Did he tell" → "He tell"
                    pattern = f"{slots['Aux']} {subject}"
                    if pattern in text:
                        normalized = text.replace(pattern, subject, 1)
                        return normalized.strip()
                
                # その他の助動詞も同様に処理
                pattern = f"{slots['Aux']} {subject}"
                if pattern in text:
                    normalized = text.replace(pattern, subject, 1) 
                    return normalized.strip()
        
        # WH疑問文の正規化: "What did he tell her ?" → "He tell her what"
        elif question_type == 'wh_question':
            text = question_text.strip()
            if text.endswith('?'):
                text = text[:-1].strip()
            
            # WH語と助動詞を除去して語順調整
            wh_word = None
            for slot, value in slots.items():
                if slot in ['O2', 'M2'] and value.lower() in self.handlers['question'].WH_WORDS:
                    wh_word = value
                    break
            
            if wh_word and 'Aux' in slots and 'S' in slots:
                # "What did he tell" → "He tell"
                pattern = f"{wh_word} {slots['Aux']} {slots['S']}"
                if pattern in text:
                    remaining = text.replace(pattern, slots['S'], 1)
                    return remaining.strip()
        
        return question_text
    
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
        
        # 2. Phase 3順次処理: 疑問文優先→関係節→主節処理の順
        final_result = {}
        
        # 🎯 疑問文処理（最優先 + AdverbHandler + BasicFivePatternHandlerとの協力）
        if 'question' in grammar_patterns:
            # Step 1: AdverbHandlerで修飾語分離
            adverb_handler = self.handlers['adverb']
            adverb_result = adverb_handler.process(text)
            
            modifier_slots = {}
            processing_text = text
            
            if adverb_result['success']:
                modifier_slots = adverb_result.get('modifier_slots', {})
                processing_text = adverb_result['separated_text']
                print(f"🔧 疑問文修飾語分離: '{text}' → '{processing_text}'")
                for slot, value in modifier_slots.items():
                    print(f"📍 修飾語検出: {slot} = '{value}'")
            
            # Step 2: QuestionHandlerで疑問文構造処理
            question_handler = self.handlers['question']
            question_result = question_handler.process(processing_text)
            
            # Step 3: BasicFivePatternHandlerで5文型構造処理
            # 疑問文を平叙文に正規化してから処理
            normalized_text = self._normalize_question_to_statement(processing_text, question_result)
            print(f"🔄 疑問文正規化: '{processing_text}' → '{normalized_text}'")
            
            five_pattern_handler = self.handlers['basic_five_pattern']
            five_pattern_result = five_pattern_handler.process(normalized_text)
            
            if question_result['success'] and five_pattern_result['success']:
                # 疑問文+5文型+修飾語統合
                question_slots = question_result['slots']
                five_pattern_slots = five_pattern_result['slots']
                
                # スロット統合（疑問詞優先、5文型で補完）
                final_slots = {}
                
                # 疑問詞スロット（QuestionHandlerから優先取得）
                wh_slots = {}
                for slot, value in question_slots.items():
                    if slot in ['O2', 'M2'] and value.lower() in question_handler.WH_WORDS:
                        wh_slots[slot] = value  # WH語は疑問文ハンドラー優先
                        final_slots[slot] = value
                
                # 助動詞はQuestionHandlerから
                if 'Aux' in question_slots:
                    final_slots['Aux'] = question_slots['Aux']
                
                # 5文型スロット（疑問詞と競合しない場合のみ）
                for slot, value in five_pattern_slots.items():
                    if slot not in final_slots:  # 疑問詞・助動詞と重複しない場合のみ
                        # WH語が主語位置の場合の特別処理
                        if slot == 'S' and any(wh_slot == 'S' for wh_slot in wh_slots):
                            continue  # WH語が主語の場合は5文型の主語をスキップ
                        final_slots[slot] = value
                
                # 修飾語スロットを統合（WH語でない修飾語のみ）
                for slot, value in modifier_slots.items():
                    if slot not in final_slots:
                        final_slots[slot] = value
                
                print(f"✅ 疑問文+5文型+修飾語統合成功: {final_slots}")
                
                # 🎯 Pure Data-Driven Order Manager統合: 順序付与
                result = {
                    'success': True,
                    'text': text,
                    'main_slots': final_slots,
                    'sub_slots': {},
                    'metadata': {
                        'controller': 'central',
                        'primary_handler': 'question',
                        'collaboration': ['adverb', 'basic_five_pattern'],
                        'question_type': question_result.get('question_type'),
                        'sentence_pattern': five_pattern_result.get('pattern'),
                        'confidence': (question_result['metadata']['confidence'] + 
                                     five_pattern_result.get('confidence', 0.5)) / 2
                    }
                }
                
                # 順序情報を追加
                return self._apply_order_to_result(result)
            else:
                print(f"⚠️ 疑問文または5文型処理失敗、通常の処理フローに移行")
                if not question_result['success']:
                    print(f"  QuestionHandler error: {question_result.get('error')}")
                if not five_pattern_result['success']:
                    print(f"  BasicFivePatternHandler error: {five_pattern_result.get('error')}")
        
        # 🎯 Phase 6: 助動詞処理（疑問文でない場合に適用）
        if 'modal' in grammar_patterns and 'question' not in grammar_patterns:
            # Step 1: AdverbHandlerで修飾語分離
            adverb_handler = self.handlers['adverb']
            adverb_result = adverb_handler.process(text)
            
            modifier_slots = {}
            processing_text = text
            
            if adverb_result['success']:
                modifier_slots = adverb_result.get('modifier_slots', {})
                processing_text = adverb_result['separated_text']
                print(f"🔧 助動詞文修飾語分離: '{text}' → '{processing_text}'")
                for slot, value in modifier_slots.items():
                    print(f"📍 修飾語検出: {slot} = '{value}'")
            
            # Step 2: ModalHandlerで助動詞構造処理
            modal_handler = self.handlers['modal']
            modal_result = modal_handler.process(processing_text)
            
            if modal_result['success']:
                # 助動詞+修飾語統合
                modal_slots = modal_result['main_slots']
                
                # 修飾語スロットを統合
                final_slots = modal_slots.copy()
                for slot, value in modifier_slots.items():
                    if slot not in final_slots:
                        final_slots[slot] = value
                
                print(f"✅ 助動詞+修飾語統合成功: {final_slots}")
                
                # 順序情報を追加
                result = {
                    'success': True,
                    'text': text,
                    'main_slots': final_slots,
                    'sub_slots': modal_result.get('sub_slots', {}),
                    'metadata': {
                        'controller': 'central',
                        'primary_handler': 'modal',
                        'collaboration': ['adverb'],
                        'modal_info': modal_result.get('modal_info', {}),
                        'confidence': 0.9
                    }
                }
                
                return self._apply_order_to_result(result)
            else:
                print(f"⚠️ 助動詞処理失敗、通常の処理フローに移行")
                print(f"  ModalHandler error: {modal_result.get('error')}")
        
        # 🎯 関係副詞処理（関係節より優先）
        if 'relative_adverb' in grammar_patterns:
            # Step 1: 関係副詞ハンドラー
            rel_adv_handler = self.handlers['relative_adverb']
            rel_adv_result = rel_adv_handler.process(text)
            
            if rel_adv_result['success']:
                print(f"✅ 関係副詞処理成功: {rel_adv_result['relative_adverb']}")
                
                # 順序情報を追加
                result = {
                    'success': True,
                    'text': text,
                    'main_slots': rel_adv_result['main_slots'],
                    'sub_slots': rel_adv_result['sub_slots'],
                    'metadata': {
                        'controller': 'central',
                        'primary_handler': 'relative_adverb',
                        'relative_adverb': rel_adv_result['relative_adverb'],
                        'confidence': 0.9
                    }
                }
                
                return self._apply_order_to_result(result)
            else:
                print(f"⚠️ 関係副詞処理失敗、通常の処理フローに移行")
                print(f"  RelativeAdverbHandler error: {rel_adv_result.get('reason')}")
        
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
        
        # 🎯 Pure Data-Driven Order Manager統合: 順序付与
        result = {
            'original_text': text,
            'success': True,
            'main_slots': final_slots,  # main_slotsを追加
            'slots': final_slots,
            'grammar_pattern': 'basic_five_pattern + passive_voice',
            'phase': 1  # 基本処理 + 受動態
        }
        
        # 順序情報を追加
        return self._apply_order_to_result(result)
    
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
        """
        関係節+5文型+受動態の結果統合（受動態対応版）
        
        Args:
            text: 元の文
            rel_result: 関係節処理結果
            five_result: 5文型処理結果
            modifier_slots: 修飾語スロット
            passive_result: 受動態処理結果
            
        Returns:
            Dict: 統合済み結果
        """
        # メインスロット: 5文型結果をベースにして、関係節のmain_slotsも統合
        main_slots = five_result['slots'].copy()
        
        # 🎯 関係節処理結果のmain_slotsを統合（主節修飾語含む）
        rel_main_slots = rel_result.get('main_slots', {})
        if rel_main_slots:
            # 関係節から取得した主節修飾語を統合
            for slot, value in rel_main_slots.items():
                if slot != 'S' and value:  # S以外の非空スロットを統合
                    main_slots[slot] = value
                    print(f"🎯 関係節main_slotsから統合: {slot} = '{value}'")
        
        # 🎯 受動態処理結果を統合
        if passive_result and passive_result.get('is_passive', False):
            print(f"🎯 受動態処理: Aux='{passive_result.get('aux')}', V='{passive_result.get('verb')}'")
            main_slots['Aux'] = passive_result.get('aux', '')
            main_slots['V'] = passive_result.get('verb', '')
        
        # 🎯 Central Controller責任: 修飾語スロットを統合
        if modifier_slots:
            # 関係節内修飾語をチェック
            sub_slots = rel_result.get('sub_slots', {})
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
        sub_slots = rel_result.get('sub_slots', {})
        
        # 🎯 設計仕様書ルール: 「サブ要素がある上位Sを""に設定」
        if sub_slots:
            # サブスロットがある場合、対応するメインスロットを空文字列に
            if any(slot.startswith('sub-') for slot in sub_slots.keys()):
                # 関係節の場合、主にSスロットが影響を受ける
                if 'sub-s' in sub_slots or 'sub-o1' in sub_slots:
                    main_slots['S'] = ''
                    print(f"🎯 Rephrase空化ルール適用: S → '' (サブスロット存在)")
        
        # 結果フォーマット
        result = {
            'success': True,
            'text': text,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'pattern_type': rel_result.get('pattern_type', 'unknown'),
            'grammar_analysis': {
                'relative_clause': True,
                'passive_voice': passive_result.get('is_passive', False) if passive_result else False,
                'detected_patterns': ['relative_clause', 'basic_five_pattern']
            }
        }
        
        # 順序情報を追加
        return self._apply_order_to_result(result)


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
