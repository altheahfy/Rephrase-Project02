"""
Universal Slot Position System
統一スロット位置管理システム

Phase 1: 個別ハンドラーアプローチから統一システムへの移行
"""

from .universal_manager import UniversalSlotPositionManager
from .pattern_registry import PatternRegistry
from .base_patterns import BasePattern
from .confidence_calculator import ConfidenceCalculator

__version__ = "1.0.0"
__author__ = "Rephrase Project Team"
__description__ = "Unified slot position management system for grammar pattern handling"

__all__ = [
    'UniversalSlotPositionManager',
    'PatternRegistry', 
    'BasePattern',
    'ConfidenceCalculator'
]
