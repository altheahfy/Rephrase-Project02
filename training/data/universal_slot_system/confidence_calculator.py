"""
Confidence Calculator
統一信頼度計算システム

全パターンで一貫したconfidence計算を提供
"""

from typing import Dict, List, Any
import logging
import re


class ConfidenceCalculator:
    """
    統一信頼度計算システム
    
    各パターンの信頼度を統一的に計算し、
    システム全体の品質を保証
    """
    
    def __init__(self):
        self.logger = logging.getLogger("ConfidenceCalculator")
        
        # 基本信頼度設定
        self.BASE_CONFIDENCE = {
            'whose_ambiguous_verb': 0.95,
            'passive_voice': 0.90,
            'complex_relative': 0.85,
            'default': 0.80
        }
        
        # 信頼度調整要因
        self.CONFIDENCE_FACTORS = {
            'pattern_match_strength': 0.3,    # パターンマッチ強度
            'context_coherence': 0.25,        # 文脈一貫性
            'grammar_rules': 0.25,            # 文法規則適合性
            'frequency_analysis': 0.20        # 頻度分析
        }
        
    def calculate_pattern_confidence(self, pattern_type: str, detection_data: Dict) -> float:
        """
        パターン信頼度計算
        
        Args:
            pattern_type: パターンタイプ
            detection_data: 検出データ
            
        Returns:
            計算された信頼度 (0.0-1.0)
        """
        base_confidence = self.BASE_CONFIDENCE.get(pattern_type, self.BASE_CONFIDENCE['default'])
        
        # 各要因の計算
        pattern_strength = self._calculate_pattern_match_strength(detection_data)
        context_score = self._calculate_context_coherence(detection_data)
        grammar_score = self._calculate_grammar_rules_score(detection_data)
        frequency_score = self._calculate_frequency_score(detection_data)
        
        # 重み付き平均で最終信頼度計算
        weighted_score = (
            pattern_strength * self.CONFIDENCE_FACTORS['pattern_match_strength'] +
            context_score * self.CONFIDENCE_FACTORS['context_coherence'] +
            grammar_score * self.CONFIDENCE_FACTORS['grammar_rules'] +
            frequency_score * self.CONFIDENCE_FACTORS['frequency_analysis']
        )
        
        # ベース信頼度と調整スコアの結合
        final_confidence = min(1.0, base_confidence + weighted_score * 0.2)
        
        self.logger.debug(
            f"📊 信頼度計算 [{pattern_type}]: "
            f"base={base_confidence:.3f}, "
            f"pattern={pattern_strength:.3f}, "
            f"context={context_score:.3f}, "
            f"grammar={grammar_score:.3f}, "
            f"frequency={frequency_score:.3f}, "
            f"final={final_confidence:.3f}"
        )
        
        return final_confidence
        
    def _calculate_pattern_match_strength(self, detection_data: Dict) -> float:
        """
        パターンマッチ強度計算
        
        正規表現マッチ数、キーワード一致度など
        """
        strength = 0.0
        
        # キーワードマッチ数
        keywords_matched = detection_data.get('keywords_matched', 0)
        total_keywords = detection_data.get('total_keywords', 1)
        keyword_ratio = keywords_matched / total_keywords
        strength += keyword_ratio * 0.4
        
        # 正規表現マッチ精度
        regex_matches = detection_data.get('regex_matches', [])
        if regex_matches:
            match_quality = sum(len(match) for match in regex_matches) / len(regex_matches)
            normalized_quality = min(1.0, match_quality / 10)  # 正規化
            strength += normalized_quality * 0.3
            
        # 文法構造一致度
        structure_match = detection_data.get('structure_match_score', 0.0)
        strength += structure_match * 0.3
        
        return min(1.0, strength)
        
    def _calculate_context_coherence(self, detection_data: Dict) -> float:
        """
        文脈一貫性計算
        
        周辺語との関係、意味的整合性など
        """
        coherence = 0.0
        
        # 周辺語との品詞一貫性
        pos_consistency = detection_data.get('pos_consistency_score', 0.0)
        coherence += pos_consistency * 0.4
        
        # 意味的関連性
        semantic_relatedness = detection_data.get('semantic_score', 0.0)
        coherence += semantic_relatedness * 0.3
        
        # 語順自然性
        word_order_naturalness = detection_data.get('word_order_score', 0.0)
        coherence += word_order_naturalness * 0.3
        
        return min(1.0, coherence)
        
    def _calculate_grammar_rules_score(self, detection_data: Dict) -> float:
        """
        文法規則適合性計算
        
        英語文法規則への適合度
        """
        grammar_score = 0.0
        
        # 基本文法規則チェック
        basic_rules_passed = detection_data.get('basic_grammar_checks', 0)
        total_basic_rules = detection_data.get('total_basic_rules', 1)
        grammar_score += (basic_rules_passed / total_basic_rules) * 0.5
        
        # 高度文法規則チェック
        advanced_rules_passed = detection_data.get('advanced_grammar_checks', 0)
        total_advanced_rules = detection_data.get('total_advanced_rules', 1)
        grammar_score += (advanced_rules_passed / total_advanced_rules) * 0.3
        
        # 例外ケース処理
        exception_handling = detection_data.get('exception_handling_score', 0.0)
        grammar_score += exception_handling * 0.2
        
        return min(1.0, grammar_score)
        
    def _calculate_frequency_score(self, detection_data: Dict) -> float:
        """
        頻度分析スコア計算
        
        類似パターンの過去成功率など
        """
        frequency_score = 0.0
        
        # 過去の成功率
        historical_success_rate = detection_data.get('historical_success_rate', 0.0)
        frequency_score += historical_success_rate * 0.6
        
        # 類似パターン頻度
        similar_pattern_frequency = detection_data.get('similar_pattern_freq', 0.0)
        frequency_score += similar_pattern_frequency * 0.4
        
        return min(1.0, frequency_score)
        
    def combine_pattern_confidences(self, pattern_confidences: List[float]) -> float:
        """
        複数パターンの信頼度結合
        
        Args:
            pattern_confidences: 各パターンの信頼度リスト
            
        Returns:
            結合された信頼度
        """
        if not pattern_confidences:
            return 0.0
            
        if len(pattern_confidences) == 1:
            return pattern_confidences[0]
            
        # 重み付き平均（高い信頼度により大きな重み）
        weights = [conf ** 2 for conf in pattern_confidences]  # 二乗で重み付け
        weighted_sum = sum(conf * weight for conf, weight in zip(pattern_confidences, weights))
        total_weight = sum(weights)
        
        combined_confidence = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        self.logger.debug(
            f"🔗 信頼度結合: "
            f"個別={[f'{c:.3f}' for c in pattern_confidences]}, "
            f"結合後={combined_confidence:.3f}"
        )
        
        return combined_confidence
        
    def validate_confidence_threshold(self, confidence: float, threshold: float) -> bool:
        """
        信頼度閾値検証
        
        Args:
            confidence: 計算された信頼度
            threshold: 最小閾値
            
        Returns:
            閾値を満たすかどうか
        """
        is_valid = confidence >= threshold
        
        if is_valid:
            self.logger.debug(f"✅ 信頼度OK: {confidence:.3f} >= {threshold:.3f}")
        else:
            self.logger.debug(f"❌ 信頼度不足: {confidence:.3f} < {threshold:.3f}")
            
        return is_valid
