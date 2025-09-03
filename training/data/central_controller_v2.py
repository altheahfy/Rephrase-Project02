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
from omitted_relative_pronoun_handler import OmittedRelativePronounHandler


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
            # RelativeClauseHandlerは空辞書を引数に取る
            handlers['relative_clause'] = OmittedRelativePronounHandler({})
            print("✅ RelativeClauseHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ RelativeClauseHandler 初期化エラー: {e}")
            
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
                'detected_grammar': [primary_handler] if primary_handler else [],
                'confidence': handler_reports.get(primary_handler, {}).get('confidence', 0.0),
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
                report = self._get_handler_report(handler_name, handler, sentence)
                reports[handler_name] = {
                    'confidence': report.confidence,
                    'patterns': report.detected_patterns,
                    'metadata': report.metadata
                }
            except Exception as e:
                print(f"⚠️ {handler_name} レポート取得エラー: {e}")
                reports[handler_name] = {
                    'confidence': 0.0,
                    'patterns': [],
                    'metadata': {'error': str(e)}
                }
        
        return reports
    
    def _make_integration_decision(self, handler_reports):
        """統合判断（新メソッド）"""
        if not handler_reports:
            return None, {}
        
        # 最も信頼度の高いハンドラーを選択
        best_handler = max(handler_reports.keys(), 
                          key=lambda h: handler_reports[h]['confidence'])
        
        cooperation_plan = {
            'primary': best_handler,
            'strategy': 'single_handler'
        }
        
        return best_handler, cooperation_plan
    
    def _execute_slot_decomposition(self, sentence, primary_handler, handler_reports):
        """スロット分解実行（Rephraseルール準拠）"""
        if not primary_handler or primary_handler not in self.active_handlers:
            return {'main_slots': {}, 'sub_slots': {}}
        
        handler = self.active_handlers[primary_handler]
        
        try:
            if primary_handler == 'basic_five_pattern':
                # BasicFivePatternHandlerを使用してRephraseスロット分解実行
                # 正しいメソッド名は'process'
                result = handler.process(sentence)
                if result and result.get('success', False):
                    # 既存ハンドラーの結果をV2形式に変換
                    # BasicFivePatternHandlerは'slots'キーに結果を格納
                    all_slots = result.get('slots', {})
                    
                    # main_slotsとsub_slotsを分離
                    main_slots = {}
                    sub_slots = {}
                    
                    for key, value in all_slots.items():
                        if key.startswith('sub-'):
                            sub_slots[key] = value
                        else:
                            main_slots[key] = value
                    
                    print(f"🔍 BasicFivePattern結果変換: main_slots={main_slots}, sub_slots={sub_slots}")
                    
                    return {
                        'main_slots': main_slots,
                        'sub_slots': sub_slots
                    }
                else:
                    print(f"⚠️ BasicFivePatternHandler結果: {result}")
                    # 失敗時はフォールバック処理
                    return self._basic_slot_decomposition(sentence)
            
            # 他のハンドラーの場合（後で実装）
            elif primary_handler == 'modal':
                # ModalHandlerも基本的にはBasicFivePatternと同様の処理
                # 現在はPOCなので簡易実装
                return self._basic_slot_decomposition(sentence)
            
            elif primary_handler == 'relative_clause':
                # 関係節の場合はサブスロット処理が重要
                # 現在はPOCなので簡易実装
                return self._basic_slot_decomposition(sentence)
            
            # フォールバック: 基本的なスロット分解
            return self._basic_slot_decomposition(sentence)
            
        except Exception as e:
            print(f"⚠️ スロット分解エラー ({primary_handler}): {e}")
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
        return {
            'has_primary_grammar': bool(primary_handler),
            'confidence_acceptable': handler_reports.get(primary_handler, {}).get('confidence', 0) > 0.3,
            'no_critical_conflicts': True,
            'text_coverage_adequate': True
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
    
    def _get_handler_report(self, handler_name: str, handler: Any, text: str) -> HandlerReport:
        """個別ハンドラーから情報レポート取得"""
        
        # 既存ハンドラーの情報を新形式に変換
        if handler_name == 'basic_five_pattern':
            # BasicFivePatternHandlerの場合
            confidence = 0.8 if self._has_basic_structure(text) else 0.3
            patterns = ['five_pattern'] if confidence > 0.5 else []
            
        elif handler_name == 'modal':
            # ModalHandlerの場合
            modal_info = handler.detect_modal_structure(text)
            confidence = 0.9 if modal_info.get('has_modal', False) else 0.1
            patterns = ['modal'] if modal_info.get('has_modal', False) else []
            
        elif handler_name == 'relative_clause':
            # RelativeClauseHandlerの場合
            doc = self.nlp(text)
            has_relative = any(token.text.lower() in ['who', 'which', 'that', 'whose', 'whom'] 
                             for token in doc)
            confidence = 0.7 if has_relative else 0.2
            patterns = ['relative_clause'] if has_relative else []
            
        else:
            # 未知のハンドラー
            confidence = 0.0
            patterns = []
        
        return HandlerReport(
            handler_name=handler_name,
            confidence=confidence,
            detected_patterns=patterns,
            metadata={'text_length': len(text)}
        )
    
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
