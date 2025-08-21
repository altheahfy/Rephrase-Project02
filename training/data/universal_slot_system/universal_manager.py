"""
Universal Slot Position Manager
統一スロット位置管理システムのメインクラス

個別ハンドラーアプローチから統一システムアプローチへの移行を実現する
中核システム
"""

from typing import Dict, List, Tuple, Any, Optional
import logging
from .base_patterns import BasePattern
from .pattern_registry import PatternRegistry
from .confidence_calculator import ConfidenceCalculator


class UniversalSlotPositionManager:
    """
    統一スロット位置管理システム
    
    Phase 1の中核システム：
    - 個別ハンドラーの統一
    - パターンの動的管理
    - 統一品質保証
    """
    
    def __init__(self):
        self.logger = logging.getLogger("UniversalSlotPositionManager")
        
        # コンポーネント初期化
        self.pattern_registry = PatternRegistry()
        self.confidence_calculator = ConfidenceCalculator()
        
        # 処理統計
        self.processing_stats = {
            'total_processed': 0,
            'total_corrections': 0,
            'pattern_usage': {},
            'error_count': 0
        }
        
        # 品質監視
        self.quality_monitor = {
            'accuracy_history': [],
            'performance_history': [],
            'error_history': []
        }
        
        self.logger.info("🚀 Universal Slot Position Manager 初期化完了")
        
    def process_all_patterns(self, doc, sentence: str) -> Tuple[Any, Dict]:
        """
        統一パターン処理のメインエントリーポイント
        
        Args:
            doc: Stanza document
            sentence: 原文
            
        Returns:
            Tuple of:
            - processed_doc: 処理後のdocument
            - processing_metadata: 処理メタデータ
        """
        start_time = self._get_timestamp_ms()
        self.processing_stats['total_processed'] += 1
        
        try:
            # 適用可能パターンを取得
            applicable_patterns = self.pattern_registry.get_applicable_patterns(sentence)
            
            if not applicable_patterns:
                self.logger.debug(f"📝 適用パターンなし: '{sentence[:50]}...'")
                return doc, {'patterns_applied': [], 'processing_time': 0}
                
            # パターンを順次適用
            processed_doc = doc
            applied_patterns = []
            correction_metadata = {}
            
            for pattern in applicable_patterns:
                pattern_result = self._apply_single_pattern(
                    pattern, processed_doc, sentence
                )
                
                if pattern_result['success']:
                    processed_doc = pattern_result['doc']
                    applied_patterns.append(pattern.pattern_name)
                    correction_metadata[pattern.pattern_name] = pattern_result['metadata']
                    
                    # 統計更新
                    self._update_pattern_usage(pattern.pattern_name, True)
                    self.processing_stats['total_corrections'] += 1
                else:
                    self._update_pattern_usage(pattern.pattern_name, False)
                    
            # メタデータ構築
            processing_time = self._get_timestamp_ms() - start_time
            metadata = {
                'patterns_applied': applied_patterns,
                'correction_metadata': correction_metadata,
                'processing_time': processing_time,
                'total_patterns_checked': len(applicable_patterns),
                'sentence_length': len(sentence),
                'timestamp': self._get_timestamp()
            }
            
            # 品質監視更新
            self._update_quality_monitor(metadata)
            
            self.logger.debug(
                f"✅ パターン処理完了: 適用={len(applied_patterns)}, "
                f"時間={processing_time}ms, 文='{sentence[:30]}...'"
            )
            
            return processed_doc, metadata
            
        except Exception as e:
            self.processing_stats['error_count'] += 1
            self.logger.error(f"❌ パターン処理エラー: {str(e)}")
            return doc, {'error': str(e), 'patterns_applied': []}
            
    def _apply_single_pattern(self, pattern: BasePattern, doc, sentence: str) -> Dict:
        """
        単一パターンの適用
        
        Args:
            pattern: 適用するパターン
            doc: 対象document
            sentence: 原文
            
        Returns:
            適用結果辞書
        """
        pattern_name = pattern.pattern_name
        
        try:
            # パターン検出
            words = doc.sentences[0].words if doc.sentences else []
            detection_result = pattern.detect(words, sentence)
            
            pattern.log_detection(detection_result, sentence)
            
            if not detection_result.get('found', False):
                return {
                    'success': False,
                    'reason': 'pattern_not_detected',
                    'doc': doc,
                    'metadata': {}
                }
                
            # 信頼度計算
            confidence = self.confidence_calculator.calculate_pattern_confidence(
                pattern_name, detection_result
            )
            
            # 信頼度チェック
            if not self.confidence_calculator.validate_confidence_threshold(
                confidence, pattern.confidence_threshold
            ):
                return {
                    'success': False,
                    'reason': 'confidence_too_low',
                    'confidence': confidence,
                    'threshold': pattern.confidence_threshold,
                    'doc': doc,
                    'metadata': {}
                }
                
            # パターン修正適用
            corrected_doc, correction_metadata = pattern.correct(doc, detection_result)
            
            # 修正メタデータに信頼度追加
            correction_metadata['confidence'] = confidence
            correction_metadata['pattern_name'] = pattern_name
            
            pattern.log_correction(correction_metadata, sentence)
            
            return {
                'success': True,
                'doc': corrected_doc,
                'metadata': correction_metadata,
                'confidence': confidence
            }
            
        except Exception as e:
            self.logger.error(f"❌ パターン適用エラー [{pattern_name}]: {str(e)}")
            return {
                'success': False,
                'reason': 'pattern_application_error',
                'error': str(e),
                'doc': doc,
                'metadata': {}
            }
            
    def register_pattern(self, pattern_name: str, pattern_instance: BasePattern,
                        priority: int = 50, dependencies: List[str] = None) -> bool:
        """
        新しいパターンを登録
        
        Args:
            pattern_name: パターン名
            pattern_instance: パターンインスタンス
            priority: 優先順位
            dependencies: 依存パターン
            
        Returns:
            登録成功フラグ
        """
        return self.pattern_registry.register_pattern(
            pattern_name, pattern_instance, priority, dependencies
        )
        
    def unregister_pattern(self, pattern_name: str) -> bool:
        """パターンの登録解除"""
        return self.pattern_registry.unregister_pattern(pattern_name)
        
    def get_registered_patterns(self) -> List[str]:
        """登録済みパターン一覧"""
        return self.pattern_registry.list_registered_patterns()
        
    def get_processing_stats(self) -> Dict:
        """処理統計取得"""
        stats = self.processing_stats.copy()
        
        # 成功率計算
        if stats['total_processed'] > 0:
            stats['correction_rate'] = stats['total_corrections'] / stats['total_processed']
            stats['error_rate'] = stats['error_count'] / stats['total_processed']
        else:
            stats['correction_rate'] = 0.0
            stats['error_rate'] = 0.0
            
        # パターン別統計
        stats['pattern_stats'] = self.pattern_registry.get_pattern_stats()
        
        return stats
        
    def get_quality_metrics(self) -> Dict:
        """品質メトリクス取得"""
        return {
            'processing_stats': self.get_processing_stats(),
            'quality_monitor': self.quality_monitor.copy(),
            'recent_performance': self._calculate_recent_performance(),
            'system_health': self._assess_system_health()
        }
        
    def reset_stats(self):
        """統計リセット"""
        self.processing_stats = {
            'total_processed': 0,
            'total_corrections': 0,
            'pattern_usage': {},
            'error_count': 0
        }
        self.quality_monitor = {
            'accuracy_history': [],
            'performance_history': [],
            'error_history': []
        }
        self.logger.info("📊 統計リセット完了")
        
    def _update_pattern_usage(self, pattern_name: str, success: bool):
        """パターン使用統計更新"""
        if pattern_name not in self.processing_stats['pattern_usage']:
            self.processing_stats['pattern_usage'][pattern_name] = {
                'usage_count': 0,
                'success_count': 0
            }
            
        usage = self.processing_stats['pattern_usage'][pattern_name]
        usage['usage_count'] += 1
        if success:
            usage['success_count'] += 1
            
        # パターンレジストリの統計も更新
        self.pattern_registry.update_pattern_stats(pattern_name, success)
        
    def _update_quality_monitor(self, metadata: Dict):
        """品質監視更新"""
        # パフォーマンス履歴
        processing_time = metadata.get('processing_time', 0)
        self.quality_monitor['performance_history'].append(processing_time)
        
        # 履歴サイズ制限
        max_history = 1000
        if len(self.quality_monitor['performance_history']) > max_history:
            self.quality_monitor['performance_history'] = \
                self.quality_monitor['performance_history'][-max_history:]
                
    def _calculate_recent_performance(self) -> Dict:
        """最近のパフォーマンス計算"""
        perf_history = self.quality_monitor['performance_history']
        
        if not perf_history:
            return {'avg_processing_time': 0, 'samples': 0}
            
        recent_samples = perf_history[-100:]  # 最新100サンプル
        avg_time = sum(recent_samples) / len(recent_samples)
        
        return {
            'avg_processing_time': avg_time,
            'samples': len(recent_samples),
            'min_time': min(recent_samples),
            'max_time': max(recent_samples)
        }
        
    def _assess_system_health(self) -> Dict:
        """システム健全性評価"""
        stats = self.processing_stats
        
        # エラー率チェック
        error_rate = stats['error_count'] / max(stats['total_processed'], 1)
        error_status = 'healthy' if error_rate < 0.01 else 'warning' if error_rate < 0.05 else 'critical'
        
        # パフォーマンスチェック
        recent_perf = self._calculate_recent_performance()
        perf_status = 'healthy' if recent_perf['avg_processing_time'] < 100 else 'warning'
        
        # 全体評価
        overall_status = 'healthy'
        if error_status == 'critical' or perf_status == 'critical':
            overall_status = 'critical'
        elif error_status == 'warning' or perf_status == 'warning':
            overall_status = 'warning'
            
        return {
            'overall_status': overall_status,
            'error_status': error_status,
            'performance_status': perf_status,
            'error_rate': error_rate,
            'avg_processing_time': recent_perf['avg_processing_time']
        }
        
    def _get_timestamp(self) -> str:
        """タイムスタンプ取得"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def _get_timestamp_ms(self) -> int:
        """ミリ秒タイムスタンプ取得"""
        import time
        return int(time.time() * 1000)
