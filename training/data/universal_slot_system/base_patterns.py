"""
Base Pattern Classes
統一文法パターンの基底クラス定義

全ての文法パターン（whose, passive, etc.）が継承する基底クラス
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any
import logging


class BasePattern(ABC):
    """
    全文法パターンの基底クラス
    
    統一インターフェースにより、個別ハンドラーアプローチから
    統一システムアプローチへの移行を実現
    """
    
    def __init__(self, pattern_name: str, confidence_threshold: float = 0.8):
        self.pattern_name = pattern_name
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(f"Pattern.{pattern_name}")
        
    @abstractmethod
    def detect(self, words: List, sentence: str) -> Dict[str, Any]:
        """
        パターン検出の統一インターフェース
        
        Args:
            words: Stanza解析後の単語リスト
            sentence: 原文
            
        Returns:
            Dict containing:
            - found: bool (パターン発見フラグ)
            - confidence: float (信頼度)
            - target_words: List (対象単語)
            - correction_data: Dict (修正情報)
        """
        pass
        
    @abstractmethod  
    def correct(self, doc, detection_result: Dict) -> Tuple[Any, Dict]:
        """
        修正処理の統一インターフェース
        
        Args:
            doc: Stanza document
            detection_result: detect()の結果
            
        Returns:
            Tuple of:
            - corrected_doc: 修正後のdocument
            - correction_metadata: 修正メタデータ
        """
        pass
        
    def calculate_confidence(self, detection_result: Dict) -> float:
        """
        confidence計算の統一インターフェース
        
        基本実装：detection_resultのconfidenceを返す
        子クラスでオーバーライド可能
        """
        return detection_result.get('confidence', self.confidence_threshold)
        
    def is_applicable(self, sentence: str) -> bool:
        """
        文にパターンが適用可能かチェック
        
        基本実装：pattern_nameが文に含まれるかチェック
        子クラスでオーバーライド推奨
        """
        return self.pattern_name.lower() in sentence.lower()
        
    def log_detection(self, detection_result: Dict, sentence: str):
        """統一ログ出力"""
        if detection_result.get('found', False):
            confidence = detection_result.get('confidence', 0.0)
            target_words = detection_result.get('target_words', [])
            self.logger.debug(
                f"🧠 {self.pattern_name}パターン検出: "
                f"信頼度={confidence:.3f}, "
                f"対象語={target_words}, "
                f"文='{sentence[:50]}...'"
            )
        else:
            self.logger.debug(f"❌ {self.pattern_name}パターン未検出: '{sentence[:50]}...'")
            
    def log_correction(self, correction_metadata: Dict, sentence: str):
        """統一修正ログ出力"""
        if correction_metadata:
            self.logger.debug(
                f"✅ {self.pattern_name}修正完了: "
                f"修正内容={correction_metadata}, "
                f"文='{sentence[:50]}...'"
            )


class GrammarPattern(BasePattern):
    """
    文法パターン専用の基底クラス
    
    POS tag修正、dependency relation修正など
    文法的な修正を行うパターン用
    """
    
    def __init__(self, pattern_name: str, confidence_threshold: float = 0.8):
        super().__init__(pattern_name, confidence_threshold)
        self.correction_types = [
            'upos_correction',      # POS tag修正
            'deprel_correction',    # dependency relation修正
            'head_correction',      # head語修正
            'features_correction'   # morphological features修正
        ]
        
    def create_correction_metadata(self, word, original_attrs: Dict, corrected_attrs: Dict) -> Dict:
        """
        統一修正メタデータ作成
        
        Args:
            word: 対象単語
            original_attrs: 修正前属性
            corrected_attrs: 修正後属性
            
        Returns:
            統一形式の修正メタデータ
        """
        return {
            'word_id': getattr(word, 'id', None),
            'word_text': getattr(word, 'text', ''),
            'original_upos': original_attrs.get('upos', getattr(word, 'upos', '')),
            'corrected_upos': corrected_attrs.get('upos', getattr(word, 'upos', '')),
            'original_deprel': original_attrs.get('deprel', getattr(word, 'deprel', '')),
            'corrected_deprel': corrected_attrs.get('deprel', getattr(word, 'deprel', '')),
            'correction_type': self.pattern_name,
            'confidence': corrected_attrs.get('confidence', self.confidence_threshold),
            'timestamp': self._get_timestamp()
        }
        
    def _get_timestamp(self) -> str:
        """タイムスタンプ取得"""
        from datetime import datetime
        return datetime.now().isoformat()


class PositionPattern(BasePattern):
    """
    位置パターン専用の基底クラス
    
    slot position修正、語順変更など
    位置的な修正を行うパターン用
    """
    
    def __init__(self, pattern_name: str, confidence_threshold: float = 0.8):
        super().__init__(pattern_name, confidence_threshold)
        self.position_types = [
            'slot_position',        # スロット位置修正
            'word_order',          # 語順修正
            'phrase_position',     # 句位置修正
            'clause_position'      # 節位置修正
        ]
        
    def create_position_metadata(self, position_changes: List[Dict]) -> Dict:
        """
        統一位置修正メタデータ作成
        
        Args:
            position_changes: 位置変更のリスト
            
        Returns:
            統一形式の位置修正メタデータ
        """
        return {
            'pattern_type': self.pattern_name,
            'position_changes': position_changes,
            'total_changes': len(position_changes),
            'confidence': self.confidence_threshold,
            'timestamp': self._get_timestamp()
        }
        
    def _get_timestamp(self) -> str:
        """タイムスタンプ取得"""
        from datetime import datetime
        return datetime.now().isoformat()
