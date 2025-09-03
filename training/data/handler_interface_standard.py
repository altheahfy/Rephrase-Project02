"""
標準化ハンドラーインターフェース
Standardized Handler Interface for Generic Central Management

このファイルは新しいワークスペースでハードコーディングを完全に排除した
中央管理システムを構築するための基礎インターフェースを提供します。

設計原則:
- 完全汎用性: 特定のハンドラー実装に依存しない
- 標準化: 全ハンドラーが同一インターフェースを実装
- 拡張性: 新しいハンドラーの動的追加をサポート
- 品質保証: 統一された品質指標による評価
"""

from typing import Dict, List, Any, Optional, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import time


class ProcessingResult:
    """標準化された処理結果"""
    
    def __init__(self):
        self.success: bool = False
        self.confidence: float = 0.0
        self.main_data: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.quality_indicators: Dict[str, float] = {}
        self.cooperation_requests: List[str] = []
    
    def set_success(self, success: bool, confidence: float = 0.0):
        """成功状態と信頼度を設定"""
        self.success = success
        self.confidence = max(0.0, min(1.0, confidence))
    
    def add_data(self, key: str, value: Any):
        """メインデータを追加"""
        self.main_data[key] = value
    
    def add_metadata(self, key: str, value: Any):
        """メタデータを追加"""
        self.metadata[key] = value
    
    def add_quality_indicator(self, indicator: str, score: float):
        """品質指標を追加"""
        self.quality_indicators[indicator] = max(0.0, min(1.0, score))
    
    def request_cooperation(self, handler_type: str):
        """協力要請を追加"""
        if handler_type not in self.cooperation_requests:
            self.cooperation_requests.append(handler_type)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'success': self.success,
            'confidence': self.confidence,
            'main_data': self.main_data,
            'metadata': self.metadata,
            'quality_indicators': self.quality_indicators,
            'cooperation_requests': self.cooperation_requests
        }


class HandlerCapability(Enum):
    """ハンドラー能力の分類"""
    STRUCTURAL_ANALYSIS = "structural_analysis"
    PATTERN_DETECTION = "pattern_detection"
    MODIFICATION_PROCESSING = "modification_processing"
    TRANSFORMATION = "transformation"
    BOUNDARY_DETECTION = "boundary_detection"
    SEMANTIC_ANALYSIS = "semantic_analysis"


@dataclass
class HandlerConfiguration:
    """ハンドラー設定情報"""
    handler_id: str
    capabilities: List[HandlerCapability]
    supported_patterns: List[str]
    processing_priority: int = 5  # 1=最高優先度, 10=最低優先度
    requires_preprocessing: bool = False
    cooperation_preferences: List[str] = field(default_factory=list)
    quality_thresholds: Dict[str, float] = field(default_factory=dict)


class StandardHandlerInterface(Protocol):
    """標準化されたハンドラーインターフェース"""
    
    @abstractmethod
    def get_configuration(self) -> HandlerConfiguration:
        """ハンドラー設定情報を返す"""
        pass
    
    @abstractmethod
    def analyze_input(self, input_text: str) -> ProcessingResult:
        """入力テキストを分析し、標準化された結果を返す"""
        pass
    
    @abstractmethod
    def get_processing_confidence(self, input_text: str) -> float:
        """入力テキストに対する処理信頼度を返す（0.0-1.0）"""
        pass
    
    @abstractmethod
    def can_cooperate_with(self, other_handler_id: str) -> bool:
        """他のハンドラーとの協力可能性を判定"""
        pass
    
    def validate_input(self, input_text: str) -> bool:
        """入力の妥当性を検証"""
        return isinstance(input_text, str) and len(input_text.strip()) > 0
    
    def get_handler_type(self) -> str:
        """ハンドラータイプを返す（協力要請で使用）"""
        config = self.get_configuration()
        return config.handler_id.split('_')[0] if '_' in config.handler_id else config.handler_id


class BaseHandler(ABC):
    """基底ハンドラークラス"""
    
    def __init__(self, configuration: HandlerConfiguration):
        self.config = configuration
        self.processing_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, float] = {}
    
    def get_configuration(self) -> HandlerConfiguration:
        """設定情報を返す"""
        return self.config
    
    def can_cooperate_with(self, other_handler_id: str) -> bool:
        """協力可能性の基本判定"""
        return other_handler_id in self.config.cooperation_preferences
    
    def record_processing(self, input_text: str, result: ProcessingResult):
        """処理履歴を記録"""
        self.processing_history.append({
            'timestamp': time.time(),
            'input_length': len(input_text),
            'success': result.success,
            'confidence': result.confidence,
            'quality_score': sum(result.quality_indicators.values()) / len(result.quality_indicators) if result.quality_indicators else 0.0
        })
        
        # パフォーマンス指標を更新
        self._update_performance_metrics()
    
    def _update_performance_metrics(self):
        """パフォーマンス指標の更新"""
        if not self.processing_history:
            return
        
        recent_history = self.processing_history[-100:]  # 直近100件
        
        self.performance_metrics.update({
            'success_rate': sum(1 for h in recent_history if h['success']) / len(recent_history),
            'average_confidence': sum(h['confidence'] for h in recent_history) / len(recent_history),
            'average_quality': sum(h['quality_score'] for h in recent_history) / len(recent_history)
        })
    
    @abstractmethod
    def analyze_input(self, input_text: str) -> ProcessingResult:
        """具象クラスで実装する分析メソッド"""
        pass
    
    @abstractmethod
    def get_processing_confidence(self, input_text: str) -> float:
        """具象クラスで実装する信頼度計算メソッド"""
        pass


class HandlerAdapter:
    """既存ハンドラーを標準インターフェースに適応させるアダプター"""
    
    def __init__(self, legacy_handler: Any, adapter_config: HandlerConfiguration):
        self.legacy_handler = legacy_handler
        self.config = adapter_config
        self.processing_history: List[Dict[str, Any]] = []
    
    def get_configuration(self) -> HandlerConfiguration:
        return self.config
    
    def analyze_input(self, input_text: str) -> ProcessingResult:
        """レガシーハンドラーの結果を標準形式に変換"""
        result = ProcessingResult()
        
        try:
            # レガシーハンドラーの処理実行
            if hasattr(self.legacy_handler, 'process'):
                legacy_result = self.legacy_handler.process(input_text)
            else:
                legacy_result = None
            
            if legacy_result:
                # 標準形式に変換
                success = legacy_result.get('success', False)
                confidence = self._extract_confidence(legacy_result)
                
                result.set_success(success, confidence)
                
                # データの変換
                if 'slots' in legacy_result:
                    result.add_data('slots', legacy_result['slots'])
                if 'sub_slots' in legacy_result:
                    result.add_data('sub_slots', legacy_result['sub_slots'])
                if 'modifiers' in legacy_result:
                    result.add_data('modifiers', legacy_result['modifiers'])
                
                # メタデータの変換
                for key, value in legacy_result.items():
                    if key not in ['success', 'slots', 'sub_slots', 'modifiers']:
                        result.add_metadata(key, value)
                
                # 品質指標の推定
                result.add_quality_indicator('data_completeness', 
                    self._calculate_data_completeness(legacy_result))
                
        except Exception as e:
            result.add_metadata('adapter_error', str(e))
        
        return result
    
    def get_processing_confidence(self, input_text: str) -> float:
        """レガシーハンドラーから信頼度を推定"""
        try:
            if hasattr(self.legacy_handler, 'get_confidence'):
                return self.legacy_handler.get_confidence(input_text)
            elif hasattr(self.legacy_handler, 'process'):
                # 簡易処理で信頼度を推定
                result = self.legacy_handler.process(input_text)
                return self._extract_confidence(result)
            else:
                return 0.5  # デフォルト信頼度
        except:
            return 0.0
    
    def can_cooperate_with(self, other_handler_id: str) -> bool:
        return other_handler_id in self.config.cooperation_preferences
    
    def _extract_confidence(self, legacy_result: Dict[str, Any]) -> float:
        """レガシー結果から信頼度を抽出"""
        if 'confidence' in legacy_result:
            return float(legacy_result['confidence'])
        elif legacy_result.get('success', False):
            # 成功時は中程度の信頼度
            return 0.7
        else:
            return 0.0
    
    def _calculate_data_completeness(self, legacy_result: Dict[str, Any]) -> float:
        """データ完全性スコアを計算"""
        completeness = 0.0
        
        if legacy_result.get('slots'):
            completeness += 0.4
        if legacy_result.get('sub_slots'):
            completeness += 0.3
        if legacy_result.get('modifiers'):
            completeness += 0.3
        
        return completeness


# 使用例：既存ハンドラーのアダプター作成
def create_adapter_for_legacy_handler(legacy_handler: Any, 
                                    handler_id: str,
                                    capabilities: List[HandlerCapability],
                                    supported_patterns: List[str]) -> HandlerAdapter:
    """レガシーハンドラー用アダプターを作成"""
    config = HandlerConfiguration(
        handler_id=handler_id,
        capabilities=capabilities,
        supported_patterns=supported_patterns,
        processing_priority=5,
        cooperation_preferences=[]
    )
    
    return HandlerAdapter(legacy_handler, config)


if __name__ == "__main__":
    print("📋 標準化ハンドラーインターフェース")
    print("このモジュールは汎用的な中央管理システムの基礎を提供します")
    print("主要コンポーネント:")
    print("- StandardHandlerInterface: 統一されたハンドラーインターフェース")
    print("- ProcessingResult: 標準化された処理結果")
    print("- BaseHandler: 基底ハンドラークラス")
    print("- HandlerAdapter: レガシーハンドラー適応アダプター")
