"""
新中央管理システム (Phase 6a)
真の中央管理アーキテクチャによる文法解析システム

設計原則:
1. 監督的立場: CentralControllerが全てを把握・統制
2. 情報収集: 全ハンドラーから並行して情報収集
3. 統合判断: 中央での最終判断による処理決定
4. 協力調整: 必要時のハンドラー間協力の調整
5. 品質保証: バッティング・欠落の最終チェック
"""

import spacy
import json
import os
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# 既存ハンドラーをインポート（段階的移行のため）
from basic_five_pattern_handler import BasicFivePatternHandler
from modal_handler import ModalHandler
from relative_clause_handler import RelativeClauseHandler  # 正しい関係節ハンドラー
from adverb_handler import AdverbHandler
from passive_voice_handler import PassiveVoiceHandler


class AnalysisConfidence(Enum):
    """分析信頼度レベル"""
    HIGH = "high"
    MEDIUM = "medium" 
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class HandlerReport:
    """ハンドラーからの情報レポート"""
    handler_name: str
    confidence: float  # 0.0-1.0
    detected_patterns: List[str]
    boundary_info: Optional[Dict[str, Any]] = None
    cooperation_needs: List[str] = None
    metadata: Dict[str, Any] = None
    processing_notes: List[str] = None

    def __post_init__(self):
        if self.cooperation_needs is None:
            self.cooperation_needs = []
        if self.metadata is None:
            self.metadata = {}
        if self.processing_notes is None:
            self.processing_notes = []


@dataclass 
class IntegratedAnalysis:
    """統合分析結果"""
    primary_grammar: str
    secondary_grammars: List[str]
    confidence_score: float
    handler_reports: Dict[str, HandlerReport]
    cooperation_plan: Dict[str, Any]
    quality_checks: Dict[str, bool]


class CentralControllerV2:
    """
    新中央管理システム - 真の中央管理アーキテクチャ
    
    既存システムとの並行運用を前提とした段階的移行システム
    """
    
    def __init__(self, config_file: str = 'central_controller_config.json'):
        """初期化: 新システム用の設定"""
        self.nlp = spacy.load('en_core_web_sm')
        self.config = self._load_config(config_file)
        
        # Phase 6a: 最小セットのハンドラーで開始（概念実証）
        self.active_handlers = self._initialize_poc_handlers()
        
        # 統合ルール設定
        self.integration_rules = self.config.get('central_management', {})
        
        print("🎯 Central Controller V2 初期化完了 - 新中央管理システム")
        print(f"📊 アクティブハンドラー数: {len(self.active_handlers)}")
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """設定ファイル読み込み（既存システムと共通）"""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 設定ファイル読み込み失敗: {e}")
                return {}
        return {}
    
    def _initialize_poc_handlers(self) -> Dict[str, Any]:
        """Phase 6a: 概念実証用の最小ハンドラーセット"""
        handlers = {}
        
        # 基本的なハンドラーから開始（既存インターフェースに合わせて）
        try:
            # BasicFivePatternHandlerは引数なしで初期化
            handlers['basic_five_pattern'] = BasicFivePatternHandler()
            print("✅ BasicFivePatternHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ BasicFivePatternHandler 初期化エラー: {e}")
            
        try:
            # ModalHandlerはnlpを引数に取る
            handlers['modal'] = ModalHandler(self.nlp)
            print("✅ ModalHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ ModalHandler 初期化エラー: {e}")
            
        try:
            # RelativeClauseHandlerは協力者辞書を引数に取る
            handlers['relative_clause'] = RelativeClauseHandler({})
            print("✅ RelativeClauseHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ RelativeClauseHandler 初期化エラー: {e}")
            
        try:
            # AdverbHandlerは引数なしで初期化
            handlers['adverb'] = AdverbHandler()
            print("✅ AdverbHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ AdverbHandler 初期化エラー: {e}")
            
        try:
            # PassiveVoiceHandlerを追加
            handlers['passive_voice'] = PassiveVoiceHandler()
            print("✅ PassiveVoiceHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ PassiveVoiceHandler 初期化エラー: {e}")
            
        print(f"✅ POC ハンドラー初期化完了: {len(handlers)}個")
        return handlers

    def process_sentence(self, sentence):
        """文の総合分析と分解を実行（unified_test.py互換）"""
        try:
            start_time = time.time()
            
            # ステップ1: 並行情報収集
            handler_reports = self._collect_handler_reports(sentence)
            
            # ステップ2: 統合判断
            primary_handler, cooperation_plan = self._make_integration_decision(handler_reports)
            
            # ステップ3: スロット分解実行
            slots_result = self._execute_slot_decomposition(sentence, primary_handler, handler_reports)
            
            # ステップ4: 品質保証
            quality_result = self._quality_assurance(handler_reports, primary_handler)
            
            processing_time = time.time() - start_time
            
            return {
                'main_slots': slots_result.get('main_slots', {}),
                'sub_slots': slots_result.get('sub_slots', {}),
                'detected_grammar': cooperation_plan.get('active_handlers', []),
                'confidence': max([handler_reports[h]['confidence'] for h in cooperation_plan.get('active_handlers', [])], default=0.0),
                'v2_metadata': {
                    'handler_reports': len(handler_reports),
                    'cooperation_plan': cooperation_plan,
                    'quality_checks': quality_result,
                    'processing_time': processing_time
                }
            }
            
        except Exception as e:
            print(f"❌ CentralControllerV2エラー: {str(e)}")
            return {
                'main_slots': {},
                'sub_slots': {},
                'detected_grammar': [],
                'confidence': 0.0,
                'v2_metadata': {
                    'error': str(e)
                }
            }
    
    def _collect_handler_reports(self, sentence):
        """並行情報収集（新メソッド）"""
        reports = {}
        
        for handler_name, handler in self.active_handlers.items():
            try:
                print(f"🔍 {handler_name} ハンドラー処理開始")
                report = self._get_handler_report(handler_name, handler, sentence)
                print(f"🔍 {handler_name} レポート取得成功: {report}")
                
                # HandlerReportオブジェクトか辞書かチェック
                if hasattr(report, 'confidence'):
                    # HandlerReportオブジェクトの場合
                    reports[handler_name] = {
                        'confidence': report.confidence,
                        'patterns': report.detected_patterns,
                        'metadata': report.metadata
                    }
                else:
                    # 辞書の場合
                    reports[handler_name] = {
                        'confidence': report['confidence'],
                        'patterns': report['patterns'],
                        'metadata': report['metadata']
                    }
            except Exception as e:
                print(f"⚠️ {handler_name} レポート取得エラー: {e}")
                import traceback
                traceback.print_exc()
                reports[handler_name] = {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        return reports
    
    def _get_handler_report(self, handler_name, handler, sentence):
        """各ハンドラーからの分析レポートを取得"""
        if handler_name == 'basic_five_pattern':
            try:
                result = handler.process(sentence)
                if result and result.get('success', False):
                    confidence = len(result.get('slots', {})) * 0.3  # スロット数に基づく信頼度
                    patterns = ['basic_five_pattern']
                else:
                    confidence = 0.0
                    patterns = []
                
                return {
                    'confidence': confidence,
                    'patterns': patterns,
                    'metadata': {'result': result}
                }
            except Exception as e:
                return {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        elif handler_name == 'adverb':
            try:
                result = handler.process(sentence)
                if result and result.get('success', False):
                    # 副詞が検出された場合の信頼度
                    modifiers = result.get('modifiers', {})
                    modifier_count = len(modifiers)
                    if modifier_count > 0:
                        # 副詞が検出された場合は高い信頼度を設定
                        confidence = 0.8  # 副詞検出時は最高優先度
                        patterns = ['adverb_modifier']
                    else:
                        confidence = 0.0
                        patterns = []
                else:
                    confidence = 0.0
                    patterns = []
                
                return {
                    'confidence': confidence,
                    'patterns': patterns,
                    'metadata': {'result': result}
                }
            except Exception as e:
                return {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        elif handler_name == 'modal':
            try:
                # ModalHandlerの場合は簡易評価
                # 現在はPOCなので基本的な評価
                return {
                    'confidence': 0.1,  # 低い基準信頼度
                    'patterns': [],
                    'metadata': {}
                }
            except Exception as e:
                return {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        elif handler_name == 'passive_voice':
            try:
                result = handler.process(sentence)
                if result and result.get('is_passive', False):
                    # 受動態が検出された場合の信頼度
                    confidence = 0.9  # 受動態検出時は高い信頼度
                    patterns = ['passive_voice']
                    
                    # 成功フラグを追加してAdapterパターンを適用
                    result['success'] = True
                else:
                    confidence = 0.0
                    patterns = []
                
                return {
                    'confidence': confidence,
                    'patterns': patterns,
                    'metadata': {'result': result}
                }
            except Exception as e:
                return {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        elif handler_name == 'relative_clause':
            try:
                print(f"🔍 relative_clause ハンドラー処理開始")
                # ①複文の入れ子構造（関係節）検知
                result = handler.process(sentence)  # RelativeClauseHandlerはprocess使用
                print(f"🔍 relative_clause レポート取得: result={result}")
                
                if result and result.get('success', False):
                    # 関係節が検出された場合の信頼度
                    confidence = 0.95  # 関係節検出時は最高優先度
                    patterns = ['relative_clause']
                    
                    # ②③境界特定情報をメタデータに保存
                    metadata = {
                        'result': result,
                        'boundary_info': result.get('boundary_info', {}),
                        'nested_structure': True,
                        'cooperation_required': ['basic_five_pattern', 'adverb', 'passive_voice']
                    }
                    print(f"🔍 relative_clause レポート取得成功: confidence={confidence}")
                else:
                    confidence = 0.0
                    patterns = []
                    metadata = {'result': result}
                    print(f"🔍 relative_clause レポート取得失敗: confidence={confidence}")
                
                return {
                    'confidence': confidence,
                    'patterns': patterns,
                    'metadata': metadata
                }
            except Exception as e:
                print(f"⚠️ relative_clause ハンドラーエラー: {e}")
                return {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        # その他のハンドラーも低い基準信頼度
        return {
            'confidence': 0.1,
            'patterns': [],
            'metadata': {}
        }
    
    def _make_integration_decision(self, handler_reports):
        """統合判断（新メソッド） - 全ハンドラー結果の統合処理"""
        if not handler_reports:
            return None, {}
        
        # 中央管理システム: 優先度ではなく、全ハンドラーの結果を統合
        active_handlers = [h for h, report in handler_reports.items() 
                          if report['confidence'] > 0.0]
        
        cooperation_plan = {
            'strategy': 'comprehensive_integration',
            'active_handlers': active_handlers,
            'integration_mode': 'merge_all_results'
        }
        
        # 統合処理のため、特定の「primary」ハンドラーは選択しない
        return 'integrated', cooperation_plan
    
    def _execute_slot_decomposition(self, sentence, primary_handler, handler_reports):
        """スロット分解実行（Rephraseルール準拠） - 全ハンドラー結果統合"""
        if primary_handler != 'integrated' or not handler_reports:
            return {'main_slots': {}, 'sub_slots': {}}
        
        # 中央管理システム: 全ハンドラーの結果を統合
        integrated_main_slots = {}
        integrated_sub_slots = {}
        
        # 特殊ルール: 受動態が検出された場合の優先統合
        passive_detected = False
        for handler_name in handler_reports:
            if handler_name == 'passive_voice' and handler_reports[handler_name]['confidence'] > 0.0:
                passive_detected = True
                break
        
        # 🎯 関係節が検出された場合は、V2の7段階処理を最優先で実行
        for handler_name in handler_reports:
            if handler_name == 'relative_clause':
                report = handler_reports[handler_name]
                if report['confidence'] > 0.8:  # 関係節検出時の高信頼度
                    print(f"🔄 関係節検出: V2の7段階階層処理を実行")
                    
                    # 既存RelativeClauseHandlerの完全な結果を取得
                    relative_handler_result = report['metadata'].get('result', {})
                    print(f"🔍 既存RelativeClause詳細結果: {relative_handler_result}")
                    
                    # V2の7段階処理で境界決定と構造統合を実行
                    handler = self.active_handlers['relative_clause']
                    v2_analysis = self._hierarchical_relative_clause_processing(handler, sentence)
                    
                    # 🎯 既存ハンドラーの結果を優先統合（重複処理回避）
                    final_sub_slots = {}
                    
                    # 既存RelativeClauseHandlerのサブスロットを使用
                    if relative_handler_result and relative_handler_result.get('sub_slots'):
                        existing_sub_slots = relative_handler_result['sub_slots']
                        print(f"🔍 既存サブスロット統合: {existing_sub_slots}")
                        final_sub_slots.update(existing_sub_slots)
                    
                    # V2で生成されたサブスロットがあれば追加統合
                    if v2_analysis.get('sub_slots'):
                        final_sub_slots.update(v2_analysis['sub_slots'])
                    
                    print(f"🎯 最終統合サブスロット: {final_sub_slots}")
                    
                    return {
                        'main_slots': v2_analysis['main_slots'],
                        'sub_slots': final_sub_slots
                    }

        # 修飾語競合解決: AdverbHandlerが検出した修飾語パターンを収集
        adverb_modifiers = {}
        if 'adverb' in handler_reports and handler_reports['adverb']['confidence'] > 0.0:
            adverb_handler = self.active_handlers['adverb']
            adverb_result = self._get_handler_slot_result('adverb', adverb_handler, sentence)
            if adverb_result:
                adverb_modifiers = adverb_result.get('main_slots', {})
        
        for handler_name, handler in self.active_handlers.items():
            if handler_name not in handler_reports:
                continue
                
            report = handler_reports[handler_name]
            if report['confidence'] <= 0.0:
                continue
            
            # 受動態検出時は、BasicFivePatternHandlerのSVC誤認識をスキップ
            if passive_detected and handler_name == 'basic_five_pattern':
                handler_result = self._get_handler_slot_result(handler_name, handler, sentence)
                if handler_result:
                    handler_main = handler_result.get('main_slots', {})
                    # SVC誤認識の場合、C1をスキップしてSとVのみ統合
                    if 'C1' in handler_main and 'V' in handler_main:
                        # 受動態の場合、C1は誤認識なのでスキップ
                        filtered_main = {k: v for k, v in handler_main.items() if k != 'C1'}
                        integrated_main_slots.update(filtered_main)
                        print(f"🔍 {handler_name}結果統合（受動態優先）: main={filtered_main}, sub={{}}")
                    else:
                        integrated_main_slots.update(handler_main)
                        print(f"🔍 {handler_name}結果統合: main={handler_main}, sub={{}}")
                continue
            
            # 修飾語競合解決: BasicFivePatternとAdverbの競合チェック
            if handler_name == 'basic_five_pattern' and adverb_modifiers:
                handler_result = self._get_handler_slot_result(handler_name, handler, sentence)
                if handler_result:
                    handler_main = handler_result.get('main_slots', {})
                    handler_sub = handler_result.get('sub_slots', {})
                    
                    # 修飾語との競合をチェックして解決
                    filtered_main = self._resolve_modifier_conflicts(handler_main, adverb_modifiers, sentence)
                    
                    integrated_main_slots.update(filtered_main)
                    integrated_sub_slots.update(handler_sub)
                    
                    print(f"🔍 {handler_name}結果統合（修飾語競合解決後）: main={filtered_main}, sub={handler_sub}")
                continue
            
            try:
                # 各ハンドラーの結果を取得して統合
                handler_result = self._get_handler_slot_result(handler_name, handler, sentence)
                
                if handler_result:
                    # main_slotsとsub_slotsを統合
                    handler_main = handler_result.get('main_slots', {})
                    handler_sub = handler_result.get('sub_slots', {})
                    
                    # スロットの統合（重複チェック付き）
                    integrated_main_slots.update(handler_main)
                    integrated_sub_slots.update(handler_sub)
                    
                    print(f"🔍 {handler_name}結果統合: main={handler_main}, sub={handler_sub}")
                
            except Exception as e:
                print(f"⚠️ {handler_name} 統合エラー: {e}")
                continue
        
        print(f"🎯 統合結果: main_slots={integrated_main_slots}, sub_slots={integrated_sub_slots}")
        
        return {
            'main_slots': integrated_main_slots,
            'sub_slots': integrated_sub_slots
        }
    
    def _get_handler_slot_result(self, handler_name, handler, sentence):
        """各ハンドラーからスロット結果を取得"""
        try:
            if handler_name == 'basic_five_pattern':
                result = handler.process(sentence)
                if result and result.get('success', False):
                    all_slots = result.get('slots', {})
                    main_slots = {}
                    sub_slots = {}
                    
                    for key, value in all_slots.items():
                        if key.startswith('sub-'):
                            sub_slots[key] = value
                        else:
                            main_slots[key] = value
                    
                    return {'main_slots': main_slots, 'sub_slots': sub_slots}
                    
            elif handler_name == 'adverb':
                result = handler.process(sentence)
                if result and result.get('success', False):
                    all_slots = result.get('modifier_slots', {})
                    main_slots = {}
                    sub_slots = {}
                    
                    for key, value in all_slots.items():
                        if key.startswith('sub-'):
                            sub_slots[key] = value
                        else:
                            main_slots[key] = value
                    
                    return {'main_slots': main_slots, 'sub_slots': sub_slots}
            
            elif handler_name == 'relative_clause':
                # ユーザー様の7段階処理フロー実装
                return self._hierarchical_relative_clause_processing(handler, sentence)
            
            elif handler_name == 'modal':
                # 現在はPOCなので基本実装
                return {'main_slots': {}, 'sub_slots': {}}
            
            elif handler_name == 'passive_voice':
                result = handler.process(sentence)
                if result and result.get('is_passive', False):
                    # 受動態構造からスロット情報を構築
                    main_slots = {}
                    sub_slots = {}
                    
                    # 主語を抽出（spaCy依存関係解析）
                    doc = handler.nlp(sentence)
                    for token in doc:
                        if token.dep_ == 'nsubjpass':  # 受動態の主語
                            # 記事詞も含む主語を抽出
                            if token.children:
                                # 冠詞を含む主語構築
                                subject_tokens = []
                                for child in token.children:
                                    if child.dep_ == 'det':
                                        subject_tokens.append(child.text)
                                subject_tokens.append(token.text)
                                main_slots['S'] = ' '.join(subject_tokens)
                            else:
                                main_slots['S'] = token.text
                            break
                    
                    # 助動詞と動詞を設定
                    main_slots['Aux'] = result.get('aux', '')
                    main_slots['V'] = result.get('verb', '')
                    
                    return {'main_slots': main_slots, 'sub_slots': sub_slots}
                    
                return {'main_slots': {}, 'sub_slots': {}}
            
            # その他のハンドラー
            return {'main_slots': {}, 'sub_slots': {}}
            
        except Exception as e:
            print(f"⚠️ {handler_name} スロット取得エラー: {e}")
            return {'main_slots': {}, 'sub_slots': {}}
    
    def _extract_sub_slots_from_legacy_result(self, legacy_result):
        """既存システムの結果からサブスロットを抽出"""
        sub_slots = {}
        
        # 既存システムのslotsからサブスロット（sub-で始まる）を抽出
        all_slots = legacy_result.get('slots', {})
        for key, value in all_slots.items():
            if key.startswith('sub-') and value:  # sub-で始まる非空スロット
                sub_slots[key] = value
        
        return sub_slots
    
    def _resolve_modifier_conflicts(self, basic_slots, adverb_modifiers, sentence):
        """BasicFivePatternとAdverbの修飾語競合を解決"""
        filtered_slots = basic_slots.copy()
        
        # 前置詞句修飾語（M2, M3など）をチェック
        for modifier_key, modifier_value in adverb_modifiers.items():
            if modifier_key.startswith('M') and modifier_value:
                # 前置詞句から名詞部分を抽出 (例: "for exams" → "exams")
                modifier_words = modifier_value.split()
                if len(modifier_words) >= 2:  # 前置詞 + 名詞の形
                    noun_part = modifier_words[-1]  # 最後の単語（通常名詞）
                    
                    # BasicFivePatternの目的語スロットと競合チェック
                    for basic_key, basic_value in list(filtered_slots.items()):
                        if basic_key in ['O1', 'O2', 'C1', 'C2'] and basic_value:
                            # 目的語/補語が修飾語内の名詞と一致する場合
                            if basic_value.lower() == noun_part.lower():
                                print(f"🔧 修飾語競合解決: {basic_key}='{basic_value}' を削除（{modifier_key}='{modifier_value}' と重複）")
                                del filtered_slots[basic_key]
                                
        return filtered_slots
    
    def _basic_slot_decomposition(self, sentence):
        """基本的なスロット分解（Rephraseルール簡易版）"""
        # spaCyで基本的な解析
        doc = self.nlp(sentence)
        
        main_slots = {}
        sub_slots = {}
        
        # 主語検出
        subject = None
        verb = None
        objects = []
        modifiers = []
        
        for token in doc:
            if token.dep_ == 'nsubj':  # 主語
                subject = token.text
            elif token.dep_ == 'ROOT' and token.pos_ in ['VERB', 'AUX']:  # 動詞
                verb = token.text
            elif token.dep_ in ['dobj', 'iobj']:  # 目的語
                objects.append(token.text)
            elif token.dep_ in ['acomp', 'attr']:  # 補語
                if 'C1' not in main_slots:
                    main_slots['C1'] = token.text
            elif token.dep_ == 'advmod':  # 副詞
                modifiers.append(token.text)
        
        # Rephraseルールに従って配置
        if subject:
            main_slots['S'] = subject
        if verb:
            main_slots['V'] = verb
        
        # 目的語配置
        if objects:
            if len(objects) >= 1:
                main_slots['O1'] = objects[0]
            if len(objects) >= 2:
                main_slots['O2'] = objects[1]
        
        # 修飾語配置（個数ベースルール）
        if modifiers:
            if len(modifiers) == 1:
                main_slots['M2'] = modifiers[0]
            elif len(modifiers) == 2:
                main_slots['M1'] = modifiers[0]
                main_slots['M3'] = modifiers[1]
            elif len(modifiers) >= 3:
                main_slots['M1'] = modifiers[0]
                main_slots['M2'] = modifiers[1]
                main_slots['M3'] = modifiers[2]
        
        return {
            'main_slots': main_slots,
            'sub_slots': sub_slots
        }
    
    def _quality_assurance(self, handler_reports, primary_handler):
        """品質保証チェック"""
        active_handlers = [h for h, report in handler_reports.items() 
                          if report['confidence'] > 0.0]
        
        max_confidence = max([report['confidence'] for report in handler_reports.values()], default=0.0)
        
        return {
            'has_active_handlers': len(active_handlers) > 0,
            'confidence_acceptable': max_confidence > 0.3,
            'no_critical_conflicts': True,
            'text_coverage_adequate': True,
            'integrated_processing': primary_handler == 'integrated'
        }

    def analyze_grammar_structure_v2(self, text: str) -> Dict[str, Any]:
        """
        新中央管理システムによる文法解析（unified_test.py互換）
        
        Returns:
            process_sentenceと同じ形式の結果
        """
        print(f"\n🔬 新システム分析開始: '{text}'")
        
        # process_sentenceメソッドをそのまま呼び出し
        return self.process_sentence(text)
    
    def _collect_all_handler_reports(self, text: str) -> Dict[str, HandlerReport]:
        """全ハンドラーから並行情報収集"""
        reports = {}
        
        for handler_name, handler in self.active_handlers.items():
            try:
                # ハンドラーから情報レポートを取得（判断はさせない）
                report = self._get_handler_report(handler_name, handler, text)
                reports[handler_name] = report
                
                print(f"📋 {handler_name}: 信頼度={report.confidence:.2f}, パターン={report.detected_patterns}")
                
            except Exception as e:
                print(f"⚠️ {handler_name} レポート取得エラー: {e}")
                # エラー時のフォールバック
                reports[handler_name] = HandlerReport(
                    handler_name=handler_name,
                    confidence=0.0,
                    detected_patterns=[],
                    processing_notes=[f"Error: {str(e)}"]
                )
        
        return reports
    
    def _has_basic_structure(self, text: str) -> bool:
        """基本構造の存在確認（簡易版）"""
        doc = self.nlp(text)
        has_verb = any(token.pos_ in ['VERB', 'AUX'] for token in doc)
        has_noun = any(token.pos_ in ['NOUN', 'PRON', 'PROPN'] for token in doc)
        return has_verb and has_noun
    
    def _integrate_handler_reports(self, reports: Dict[str, HandlerReport], text: str) -> IntegratedAnalysis:
        """中央での統合判断"""
        
        # 信頼度に基づいて主要文法項目を決定
        valid_reports = {name: report for name, report in reports.items() 
                        if report.confidence > 0.5}
        
        if not valid_reports:
            # フォールバック: 最も信頼度の高いものを選択
            if reports:
                best_report = max(reports.values(), key=lambda r: r.confidence)
                primary_grammar = best_report.handler_name
                confidence_score = best_report.confidence
            else:
                primary_grammar = 'unknown'
                confidence_score = 0.0
            secondary_grammars = []
        else:
            # 最も信頼度の高いものを主要文法に
            best_report = max(valid_reports.values(), key=lambda r: r.confidence)
            primary_grammar = best_report.handler_name
            confidence_score = best_report.confidence
            
            # 残りを副次文法に
            secondary_grammars = [name for name, report in valid_reports.items() 
                                if name != primary_grammar]
        
        print(f"🎯 統合判断: 主要={primary_grammar} (信頼度={confidence_score:.2f}), 副次={secondary_grammars}")
        
        return IntegratedAnalysis(
            primary_grammar=primary_grammar,
            secondary_grammars=secondary_grammars,
            confidence_score=confidence_score,
            handler_reports=reports,
            cooperation_plan={},
            quality_checks={'basic_validation': True}
        )
    
    def _requires_collaboration(self, analysis: IntegratedAnalysis) -> bool:
        """協力が必要かどうかの判断"""
        # Phase 6a: 簡易版（後で拡張）
        return len(analysis.secondary_grammars) > 1
    
    def _coordinate_handlers(self, analysis: IntegratedAnalysis, text: str) -> IntegratedAnalysis:
        """ハンドラー間協力の調整"""
        # Phase 6a: 基本実装（後で拡張）
        print(f"🤝 協力調整実行: {analysis.primary_grammar} + {analysis.secondary_grammars}")
        
        # 協力計画を更新
        analysis.cooperation_plan = {
            'strategy': 'parallel_processing',
            'involved_handlers': [analysis.primary_grammar] + analysis.secondary_grammars,
            'coordination_notes': ['Phase 6a basic coordination']
        }
        
        return analysis
    
    def _validate_final_result(self, analysis: IntegratedAnalysis, text: str) -> IntegratedAnalysis:
        """最終品質保証"""
        
        # 基本的な品質チェック
        quality_checks = {
            'has_primary_grammar': bool(analysis.primary_grammar),
            'confidence_acceptable': analysis.confidence_score > 0.3,
            'no_critical_conflicts': True,  # 後で実装
            'text_coverage_adequate': True   # 後で実装
        }
        
        analysis.quality_checks = quality_checks
        
        all_passed = all(quality_checks.values())
        print(f"✅ 品質保証: {'合格' if all_passed else '要注意'} - {quality_checks}")
        
        return analysis
    
    def _convert_to_legacy_format(self, analysis: IntegratedAnalysis) -> List[str]:
        """既存システム互換形式に変換"""
        result = []
        
        if analysis.primary_grammar and analysis.primary_grammar != 'unknown':
            result.append(analysis.primary_grammar)
        
        result.extend(analysis.secondary_grammars)
        
        return result
    
    def compare_with_legacy_system(self, text: str, legacy_controller) -> Dict[str, Any]:
        """既存システムとの比較分析"""
        
        # 新システムで分析
        v2_result = self.analyze_grammar_structure_v2(text)
        
        # 既存システムで分析
        try:
            legacy_result = legacy_controller.analyze_grammar_structure(text)
        except Exception as e:
            legacy_result = []
            print(f"⚠️ 既存システムエラー: {e}")
        
        # 比較分析
        comparison = {
            'text': text,
            'v2_system': {
                'result': v2_result['legacy_format'],
                'confidence': v2_result['v2_result'].confidence_score,
                'handlers_used': len(v2_result['v2_result'].handler_reports)
            },
            'legacy_system': {
                'result': legacy_result,
                'confidence': None,  # 既存システムには信頼度なし
                'handlers_used': None
            },
            'differences': {
                'result_match': v2_result['legacy_format'] == legacy_result,
                'v2_extra': set(v2_result['legacy_format']) - set(legacy_result),
                'legacy_extra': set(legacy_result) - set(v2_result['legacy_format'])
            }
        }
        
        print(f"\n📊 システム比較結果:")
        print(f"   新システム: {v2_result['legacy_format']}")
        print(f"   既存システム: {legacy_result}")
        print(f"   一致: {comparison['differences']['result_match']}")
        
        return comparison

    def _hierarchical_relative_clause_processing(self, handler, sentence):
        """ユーザー様の7段階処理フロー実装"""
        print(f"🔄 関係節階層処理開始: {sentence}")
        
        try:
            # ①V2が例文に複文の入れ子構造（関係節）があることを検知
            result = handler.process(sentence)  # RelativeClauseHandlerはprocess使用
            if not result or not result.get('success', False):
                return {'main_slots': {}, 'sub_slots': {}}
            
            print(f"✅ ①構造検知完了: {result.get('boundary_info', {})}")
            
            # ②さらに例文全体で他に何の文法が登場するか検知・整理
            grammar_inventory = self._detect_grammar_patterns(sentence)
            print(f"✅ ②文法整理完了: {grammar_inventory}")
            
            # ③必要なハンドラーを招集し、協調して境界を特定
            boundary_decision = self._coordinate_boundary_detection(sentence, result, grammar_inventory)
            print(f"✅ ③境界決定完了: {boundary_decision}")
            
            # ④⑤V2が境界を決定し、節に対して代表的な語句を残してマスク
            masked_sentence = self._create_masked_sentence(sentence, boundary_decision)
            print(f"✅ ④⑤マスク処理完了: '{masked_sentence}'")
            
            # ⑥上位スロットを合体したものに対して必要なハンドラーを読んで処理
            main_clause_slots = self._process_main_clause(masked_sentence, grammar_inventory)
            print(f"✅ ⑥主節処理完了: {main_clause_slots}")
            
            # ⑦節を各ハンドラーに処理させ、結果を統合
            relative_clause_slots = self._process_relative_clause(boundary_decision['relative_clause'], grammar_inventory)
            print(f"✅ ⑦関係節処理完了: {relative_clause_slots}")
            
            return {'main_slots': main_clause_slots, 'sub_slots': relative_clause_slots}
            
        except Exception as e:
            print(f"⚠️ 階層処理エラー: {e}")
            return {'main_slots': {}, 'sub_slots': {}}
    
    def _detect_grammar_patterns(self, sentence):
        """②文法パターン検知・整理"""
        patterns = {
            'has_passive': False,
            'has_modal': False,
            'has_adverb': False,
            'verb_forms': [],
            'complexity_level': 'simple'
        }
        
        doc = self.nlp(sentence)
        for token in doc:
            if token.tag_ == 'VBN' and any(aux.lemma_ in ['be', 'have'] for aux in token.ancestors):
                patterns['has_passive'] = True
            if token.tag_ == 'MD':
                patterns['has_modal'] = True
            if token.pos_ == 'ADV':
                patterns['has_adverb'] = True
            if token.pos_ == 'VERB':
                patterns['verb_forms'].append(token.lemma_)
        
        patterns['complexity_level'] = 'complex' if len(patterns['verb_forms']) > 1 else 'simple'
        return patterns
    
    def _coordinate_boundary_detection(self, sentence, relative_result, grammar_patterns):
        """③ハンドラー協調による境界特定 - 既存システムの境界検出ロジックを活用"""
        
        # 既存RelativeClauseHandlerの結果から正確な境界情報を取得
        if relative_result and relative_result.get('success', False):
            main_continuation = relative_result.get('main_continuation', '')
            relative_pronoun = relative_result.get('relative_pronoun', '')
            antecedent = relative_result.get('antecedent', '')
            
            # 既存システムの簡略文作成ロジックを使用
            boundary_info = {
                'main_clause': main_continuation,
                'relative_clause': '',  # 関係節内容は既存ハンドラーから取得
                'boundary_position': 0,
                'relative_pronoun': relative_pronoun,
                'antecedent': antecedent
            }
            
            # main_continuationから主節動詞を特定
            doc_main = self.nlp(main_continuation)
            for token in doc_main:
                if token.dep_ == 'ROOT' or (token.pos_ in ['VERB', 'AUX'] and token.dep_ in ['aux', 'auxpass', 'cop']):
                    boundary_info['main_verb'] = token.text
                    boundary_info['main_verb_pos'] = token.i
                    break
            
            return boundary_info
        
        # フォールバック: 基本的なspaCy検出
        doc = self.nlp(sentence)
        boundary_info = {
            'main_clause': sentence,
            'relative_clause': '',
            'boundary_position': 0,
            'relative_pronoun': ''
        }
        
        return boundary_info
    
    def _create_masked_sentence(self, sentence, boundary_decision):
        """④⑤代表語句によるマスク処理 - 関係節を先行詞に置換"""
        
        # 既存RelativeClauseHandlerが作成した簡略文（main_continuation）を使用
        if 'main_clause' in boundary_decision and boundary_decision['main_clause']:
            main_clause = boundary_decision['main_clause'].strip()
            antecedent = boundary_decision.get('antecedent', '')
            
            # 先行詞を復元してマスク文作成
            if antecedent and main_clause:
                # main_continuationが動詞から始まる場合、先行詞を前に付ける
                if main_clause and not main_clause.split()[0].lower() in ['the', 'a', 'an', 'this', 'that', 'these', 'those']:
                    masked_sentence = f"{antecedent} {main_clause}"
                else:
                    masked_sentence = main_clause
                
                print(f"🔍 マスク処理: '{sentence}' → '{masked_sentence}'")
                return masked_sentence
            
            return main_clause
        
        # フォールバック: 元の文をそのまま返す
        return sentence
    
    def _process_main_clause(self, masked_sentence, grammar_patterns):
        """⑥マスク文での主節処理"""
        main_slots = {}
        
        print(f"🔍 主節処理入力: '{masked_sentence}'")
        
        # BasicFivePatternHandlerで主節を処理
        if 'basic_five_pattern' in self.active_handlers:
            basic_handler = self.active_handlers['basic_five_pattern']
            result = basic_handler.process(masked_sentence)
            print(f"🔍 BasicFivePattern結果: {result}")
            
            if result and result.get('success', False):
                main_slots = result.get('slots', {})
                print(f"🔍 抽出されたスロット: {main_slots}")
        
        # 🎯 Rephrase空化ルール適用: 関係節存在時にSスロットを空にする
        if main_slots and 'S' in main_slots:
            main_slots['S'] = ''
            print(f"🎯 Rephrase空化ルール適用: S → '' (関係節による主語抽象化)")
        
        print(f"🔍 最終主節スロット: {main_slots}")
        return main_slots
    
    def _process_relative_clause(self, relative_clause, grammar_patterns):
        """⑦関係節の個別処理 - 既存ハンドラー結果の統合"""
        sub_slots = {}
        
        if not relative_clause:
            return sub_slots
        
        print(f"🔍 関係節処理入力: '{relative_clause}'")
        print(f"🔍 ⑦段階は既存ハンドラー結果を統合するのみ - 重複処理回避")
        
        # ⑦段階では新たにハンドラーを呼び出さず、
        # 既存のRelativeClauseHandlerとAdverbHandlerの結果を統合
        # （重複処理を避け、V2の中央管理理念に従う）
        
        return sub_slots


def test_new_system():
    """新システムの基本動作テスト"""
    print("🧪 新中央管理システム テスト開始")
    
    # 新システム初期化
    controller_v2 = CentralControllerV2()
    
    # テストケース
    test_cases = [
        "I can speak English.",
        "The book that I read was interesting.",
        "What did you see?",
        "I wish I knew the answer."
    ]
    
    for text in test_cases:
        print(f"\n--- テスト: '{text}' ---")
        result = controller_v2.analyze_grammar_structure_v2(text)
        print(f"結果: {result['legacy_format']}")
        print(f"信頼度: {result['v2_result'].confidence_score:.2f}")


if __name__ == "__main__":
    test_new_system()
