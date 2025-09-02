"""
True Central Management System - Phase A Implementation
設計仕様書準拠の真の中央管理システム

設計原則:
- 各ハンドラーは中央管理システムとのみ接続
- 情報は中央管理システムのみから取得
- 処理結果も中央管理システムに渡す
- 並列ハンドラー処理（順次if/elif禁止）
- 純粋管理・調整のみ（分解作業一切なし）
"""

import spacy
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from basic_five_pattern_handler import BasicFivePatternHandler
from relative_clause_handler import RelativeClauseHandler
from relative_adverb_handler import RelativeAdverbHandler
from adverb_handler import AdverbHandler
from passive_voice_handler import PassiveVoiceHandler
from question_handler import QuestionHandler
from modal_handler import ModalHandler
from noun_clause_handler import NounClauseHandler
from omitted_relative_pronoun_handler import OmittedRelativePronounHandler
from conditional_handler import ConditionalHandler
from imperative_handler import ImperativeHandler
from metaphorical_handler import MetaphoricalHandler
from infinitive_handler import InfinitiveHandler
from pure_data_driven_order_manager import PureDataDrivenOrderManager


@dataclass
class ProcessingContext:
    """処理コンテキスト - 全ハンドラー間で共有される情報"""
    sentence: str
    tokens: Any  # spaCy Doc object
    main_slots: Dict[str, str] = None
    sub_slots: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    current_stage: str = 'initialization'
    completed_handlers: List[str] = None
    
    def __post_init__(self):
        if self.main_slots is None:
            self.main_slots = {}
        if self.sub_slots is None:
            self.sub_slots = {}
        if self.metadata is None:
            self.metadata = {}
        if self.completed_handlers is None:
            self.completed_handlers = []


class TrueCentralController:
    """
    真の中央管理システム
    
    責務:
    - ハンドラー実行順序制御のみ
    - ハンドラー間情報共有管理のみ
    - 結果統合・最終調整のみ
    - 管理・調整業務のみ（分解作業一切なし）
    """
    
    def __init__(self):
        """初期化: 純粋中央管理クラス"""
        self.nlp = spacy.load('en_core_web_sm')
        self.order_manager = PureDataDrivenOrderManager()
        
        # ハンドラー管理状態
        self.processing_stages = [
            'structure_analysis',    # Stage 1: 構造分析
            'grammar_analysis',      # Stage 2: 文法分析  
            'basic_pattern',         # Stage 3: 基本パターン
            'finalization'           # Stage 4: 統合・確定
        ]
        
        self._initialize_handlers()
        
    def _initialize_handlers(self):
        """ハンドラー初期化と協力関係構築"""
        # 基本ハンドラー群
        basic_five_pattern_handler = BasicFivePatternHandler()
        adverb_handler = AdverbHandler()
        passive_voice_handler = PassiveVoiceHandler()
        question_handler = QuestionHandler()
        modal_handler = ModalHandler(self.nlp)
        noun_clause_handler = NounClauseHandler(self.nlp)
        omitted_relative_pronoun_handler = OmittedRelativePronounHandler()
        conditional_handler = ConditionalHandler(self.nlp)
        imperative_handler = ImperativeHandler()
        metaphorical_handler = MetaphoricalHandler(self.nlp)
        infinitive_handler = InfinitiveHandler(self.nlp)
        
        # 協力者注入（Dependency Injection）
        collaborators = {
            'adverb': adverb_handler,
            'five_pattern': basic_five_pattern_handler,
            'passive': passive_voice_handler,
            'modal': modal_handler,
            'noun_clause': noun_clause_handler,
            'imperative': imperative_handler,
            'infinitive': infinitive_handler,
            'basic_five_pattern': basic_five_pattern_handler
        }
        
        relative_clause_handler = RelativeClauseHandler(collaborators)
        relative_adverb_handler = RelativeAdverbHandler(collaborators)
        metaphorical_handler.collaborators = collaborators
        
        # ステージ別ハンドラー配置
        self.stage_handlers = {
            'structure_analysis': [
                relative_clause_handler,
                relative_adverb_handler,
                conditional_handler,
                noun_clause_handler,
                omitted_relative_pronoun_handler
            ],
            'grammar_analysis': [
                passive_voice_handler,
                modal_handler,
                question_handler,
                imperative_handler,
                infinitive_handler
            ],
            'basic_pattern': [
                basic_five_pattern_handler,
                adverb_handler
            ],
            'finalization': [
                metaphorical_handler
            ]
        }
        
        # 全ハンドラーの参照も保持
        self.all_handlers = {
            'basic_five_pattern': basic_five_pattern_handler,
            'relative_clause': relative_clause_handler,
            'relative_adverb': relative_adverb_handler,
            'adverb': adverb_handler,
            'passive_voice': passive_voice_handler,
            'question': question_handler,
            'modal': modal_handler,
            'noun_clause': noun_clause_handler,
            'omitted_relative_pronoun': omitted_relative_pronoun_handler,
            'conditional': conditional_handler,
            'imperative': imperative_handler,
            'metaphorical': metaphorical_handler,
            'infinitive': infinitive_handler
        }
        
    def process_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        文章処理メイン処理 - 純粋管理方式
        """
        # 1. 処理コンテキスト初期化
        context = self._initialize_context(sentence)
        
        # 2. 段階的ハンドラー実行制御
        for stage in self.processing_stages:
            context.current_stage = stage
            self._execute_stage(stage, context)
            
        # 3. 最終結果統合
        return self._finalize_results(context)
    
    def _initialize_context(self, sentence: str) -> ProcessingContext:
        """✅ 純粋管理: 処理コンテキスト初期化"""
        tokens = self.nlp(sentence)
        
        return ProcessingContext(
            sentence=sentence,
            tokens=tokens,
            main_slots={},
            sub_slots={},
            metadata={
                'sentence_length': len(tokens),
                'processing_started': True,
                'spacy_analysis': True
            }
        )
    
    def _execute_stage(self, stage: str, context: ProcessingContext):
        """✅ 純粋管理: ステージ別ハンドラー実行制御"""
        stage_handlers = self.stage_handlers.get(stage, [])
        stage_results = []
        
        # 並列処理: 各ハンドラーを独立実行
        for handler in stage_handlers:
            try:
                # ハンドラー実行
                result = self._execute_handler(handler, context)
                
                if result and result.get('success', False):
                    stage_results.append(result)
                    
                    # 成功した場合のみコンテキスト更新
                    self._update_context_from_result(context, result)
                    
            except Exception as e:
                # エラーログ記録（処理継続）
                print(f"Handler error in {stage}: {handler.__class__.__name__}: {e}")
                continue
        
        # ステージ完了記録
        context.metadata[f'{stage}_completed'] = True
        context.metadata[f'{stage}_results_count'] = len(stage_results)
    
    def _execute_handler(self, handler, context: ProcessingContext) -> Optional[Dict[str, Any]]:
        """✅ 純粋管理: ハンドラー実行制御"""
        handler_name = handler.__class__.__name__
        
        # ハンドラー適用判定
        if hasattr(handler, 'can_handle'):
            if not handler.can_handle(context.sentence):
                return None
        
        # ハンドラー実行
        if hasattr(handler, 'process'):
            result = handler.process(context.sentence)
        elif hasattr(handler, 'handle'):
            result = handler.handle(context.sentence)
        else:
            print(f"Handler {handler_name} has no process/handle method")
            return None
            
        # 結果にメタデータ追加
        if isinstance(result, dict):
            result['handler_name'] = handler_name
            result['stage'] = context.current_stage
            
        return result
    
    def _update_context_from_result(self, context: ProcessingContext, result: Dict[str, Any]):
        """✅ 純粋管理: コンテキスト更新業務"""
        handler_name = result.get('handler_name', 'unknown')
        
        # メインスロット統合
        if 'main_slots' in result:
            context.main_slots.update(result['main_slots'])
        
        # サブスロット統合
        if 'sub_slots' in result:
            context.sub_slots.update(result['sub_slots'])
        
        # メタデータ統合
        if 'metadata' in result:
            context.metadata.update(result['metadata'])
        
        # 完了ハンドラー記録
        context.completed_handlers.append(handler_name)
    
    def _finalize_results(self, context: ProcessingContext) -> Dict[str, Any]:
        """✅ 純粋管理: 最終結果統合業務"""
        # 簡単な順序管理（基本順序）
        ordered_slots = self._create_basic_order(context.main_slots)
        ordered_sub_slots = self._order_sub_slots(context.sub_slots)
        
        # 最終結果構築
        final_result = {
            'success': True,
            'main_slots': context.main_slots,
            'sub_slots': context.sub_slots,
            'ordered_slots': ordered_slots,
            'ordered_sub_slots': ordered_sub_slots,
            'metadata': {
                **context.metadata,
                'completed_handlers': context.completed_handlers,
                'total_handlers': len(context.completed_handlers),
                'processing_complete': True
            }
        }
        
        return final_result
    
    def _create_basic_order(self, main_slots: Dict[str, str]) -> Dict[str, Any]:
        """基本的なスロット順序作成"""
        order_mapping = {
            'S': 3, 'Aux': 4, 'V': 5, 'O1': 6, 'O2': 7, 'C1': 8, 'C2': 9,
            'M1': 1, 'M2': 2, 'M3': 10
        }
        
        ordered = {}
        for slot, content in main_slots.items():
            if content and content.strip():
                order_num = order_mapping.get(slot, 99)
                ordered[str(order_num)] = content
        
        return ordered
    
    def _order_sub_slots(self, sub_slots: Dict[str, Any]) -> Dict[str, Any]:
        """サブスロット順序作成"""
        if not sub_slots:
            return {}
            
        ordered_sub = {}
        order = 1
        
        # 基本的なサブスロット順序
        slot_order = ['sub-s', 'sub-aux', 'sub-v', 'sub-o1', 'sub-o2', 'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
        
        for slot_name in slot_order:
            if slot_name in sub_slots and sub_slots[slot_name]:
                ordered_sub[str(order)] = sub_slots[slot_name]
                order += 1
        
        return ordered_sub
    
    def _merge_handler_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """✅ 純粋管理: 結果統合業務"""
        merged_main_slots = {}
        merged_sub_slots = {}
        merged_metadata = {}
        
        for result in results:
            if result.get('success', False):
                # メインスロット統合（非破壊的）
                for slot, value in result.get('main_slots', {}).items():
                    if value and value.strip():  # 空でない値のみ
                        merged_main_slots[slot] = value
                
                # サブスロット統合
                merged_sub_slots.update(result.get('sub_slots', {}))
                
                # メタデータ統合
                merged_metadata.update(result.get('metadata', {}))
        
        return {
            'success': True,
            'main_slots': merged_main_slots,
            'sub_slots': merged_sub_slots,
            'metadata': merged_metadata
        }


if __name__ == "__main__":
    """テスト用メイン"""
    controller = TrueCentralController()
    
    test_sentences = [
        "She is happy.",                           # 基本第2文型
        "The book which I read is interesting.",   # 関係節
        "The letter was written by John.",         # 受動態
        "Can you help me?",                        # 疑問文
        "I want to learn programming."             # 不定詞
    ]
    
    print("🎯 True Central Management System Test")
    print("=" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 Test {i}: {sentence}")
        
        try:
            result = controller.process_sentence(sentence)
            
            print(f"✅ Success: {result.get('success', False)}")
            print(f"📊 Main Slots: {result.get('main_slots', {})}")
            print(f"📋 Sub Slots: {result.get('sub_slots', {})}")
            print(f"🔧 Completed Handlers: {result.get('metadata', {}).get('completed_handlers', [])}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🏆 True Central Management System Test Complete")
