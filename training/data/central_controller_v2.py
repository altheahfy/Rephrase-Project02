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
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# 既存ハンドラーをインポート（段階的移行のため）
from basic_five_pattern_handler import BasicFivePatternHandler
from modal_handler import ModalHandler
from relative_clause_handler import RelativeClauseHandler


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
            handlers['relative_clause'] = RelativeClauseHandler({})
            print("✅ RelativeClauseHandler 初期化完了")
        except Exception as e:
            print(f"⚠️ RelativeClauseHandler 初期化エラー: {e}")
            
        print(f"✅ POC ハンドラー初期化完了: {len(handlers)}個")
        return handlers

    def analyze_grammar_structure_v2(self, text: str) -> Dict[str, Any]:
        """
        新中央管理システムによる文法解析
        
        Returns:
            分析結果 + 比較用メタデータ
        """
        print(f"\n🔬 新システム分析開始: '{text}'")
        
        # Step 1: 全ハンドラーから情報収集
        handler_reports = self._collect_all_handler_reports(text)
        
        # Step 2: 中央での統合判断
        integrated_analysis = self._integrate_handler_reports(handler_reports, text)
        
        # Step 3: 協力調整（必要時）
        if self._requires_collaboration(integrated_analysis):
            collaborative_result = self._coordinate_handlers(integrated_analysis, text)
            integrated_analysis = collaborative_result
        
        # Step 4: 品質保証チェック
        validated_result = self._validate_final_result(integrated_analysis, text)
        
        # Step 5: 既存システム互換形式に変換
        legacy_format_result = self._convert_to_legacy_format(validated_result)
        
        return {
            'v2_result': validated_result,
            'legacy_format': legacy_format_result,
            'analysis_metadata': {
                'system_version': 'v2',
                'handler_count': len(handler_reports),
                'confidence_score': validated_result.confidence_score,
                'processing_time': None  # 後で実装
            }
        }
    
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
