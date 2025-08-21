# Phase 1: Universal Slot Position System 実装仕様書
*作成日: 2025年8月21日*
*Phase 2.0完成後の次期開発フェーズ*

## 📋 Overview

**目的**: 個別ハンドラーで実装されているslot position管理を統一システムに移行
**背景**: 現在各ハンドラー（whose, passive, etc.）が独自の位置管理システムを持っており、重複コードと保守性の問題が発生

## 🏗️ Current System Analysis

### Individual Handler Approach (現状)
```python
# whose構文 - 個別実装
def _correct_whose_ambiguous_verb_pattern(self, doc, sentence: str):
    # 専用パターン検出
    whose_pattern = self._detect_whose_ambiguous_verb_pattern(words, sentence)
    # 専用修正ロジック
    if whose_pattern['found']:
        # 個別confidence設定
        'confidence': 0.95

# passive構文 - 個別実装  
def _correct_passive_voice_pattern(self, doc, sentence):
    # 専用パターン検出
    # 専用修正ロジック
    # 個別confidence設定
```

### Problems with Current Approach
1. **重複コード**: 各ハンドラーが独自のパターン検出・修正システム
2. **保守性**: 新パターン追加時に個別実装が必要
3. **統一性欠如**: confidence値、ログ形式、エラー処理が個別
4. **拡張困難**: Phase 2での人間文法認識拡張が複雑化

## 🎯 Phase 1 Design Goals

### Primary Objectives
1. **統一位置管理システム**: 全ハンドラーが共通のslot position framework使用
2. **パターン登録システム**: 新しい文法パターンの動的登録機能
3. **統一confidence管理**: 全パターンで一貫したconfidence計算
4. **デバッグ統一**: 統一されたログ・監視システム

### Secondary Benefits
- **Phase 2準備**: 人間文法認識の拡張基盤整備
- **コード削減**: 重複実装の統合
- **テスト簡素化**: 統一テストフレームワーク

## 🏛️ Architecture Design

### Core Components

#### 1. UniversalSlotPositionManager
```python
class UniversalSlotPositionManager:
    """統一slot position管理システム"""
    
    def __init__(self):
        self.pattern_registry = {}
        self.confidence_calculator = ConfidenceCalculator()
        self.position_corrector = PositionCorrector()
        
    def register_pattern(self, pattern_type: str, rules: Dict):
        """新しい文法パターンを登録"""
        
    def correct_ambiguous_pattern(self, doc, sentence: str, pattern_type: str):
        """統一されたパターン修正処理"""
        
    def calculate_position_confidence(self, pattern_data: Dict) -> float:
        """統一confidence計算"""
```

#### 2. PatternRegistry
```python
class PatternRegistry:
    """文法パターンの動的登録・管理"""
    
    BUILT_IN_PATTERNS = {
        'whose_ambiguous_verb': WhosePattern(),
        'passive_voice': PassivePattern(), 
        'complex_relative': RelativePattern()
    }
    
    def register_custom_pattern(self, name: str, pattern: Pattern):
        """カスタムパターン登録"""
        
    def get_applicable_patterns(self, sentence: str) -> List[Pattern]:
        """文に適用可能なパターンを検出"""
```

#### 3. Pattern Base Classes
```python
class BasePattern:
    """全パターンの基底クラス"""
    
    def detect(self, words, sentence: str) -> Dict:
        """パターン検出の統一インターフェース"""
        
    def correct(self, doc, detection_result: Dict) -> Tuple[Doc, Dict]:
        """修正処理の統一インターフェース"""
        
    def calculate_confidence(self, detection_result: Dict) -> float:
        """confidence計算の統一インターフェース"""

class WhosePattern(BasePattern):
    """whose構文の統一実装"""
    
class PassivePattern(BasePattern):
    """受動態の統一実装"""
```

## 🔄 Migration Strategy

### Phase 1.1: Core Infrastructure (Week 1)
1. **UniversalSlotPositionManager作成**
   - 基本フレームワーク実装
   - Pattern base classes定義
   - 統一logging system

2. **WhosePattern移行**
   - 既存`_correct_whose_ambiguous_verb_pattern`をWhosePatternクラスに移行
   - 統一confidence計算に変更
   - テスト実行・検証

### Phase 1.2: Pattern Expansion (Week 2)  
1. **PassivePattern移行**
   - `_correct_passive_voice_pattern`を統一システムに移行
   - 既存機能の完全互換性確保

2. **統合テスト**
   - 全パターンで100%精度維持確認
   - パフォーマンステスト

### Phase 1.3: System Optimization (Week 3)
1. **Dynamic Pattern Registration**
   - 実行時パターン追加機能
   - Pattern priority system

2. **Advanced Features**
   - Pattern combination detection
   - Multi-pattern confidence calculation

## 🧪 Implementation Plan

### Step 1: Create Core Infrastructure
```python
# training/data/universal_slot_system/
├── __init__.py
├── universal_manager.py      # UniversalSlotPositionManager
├── pattern_registry.py      # PatternRegistry
├── base_patterns.py         # BasePattern classes
└── confidence_calculator.py # 統一confidence計算
```

### Step 2: Migrate Existing Patterns
```python
# training/data/universal_slot_system/patterns/
├── __init__.py
├── whose_pattern.py         # WhosePattern implementation
├── passive_pattern.py       # PassivePattern implementation  
└── relative_pattern.py      # 将来の拡張用
```

### Step 3: Integration with UnifiedStanzaRephraseMapper
```python
# 既存コードの修正
class UnifiedStanzaRephraseMapper:
    def __init__(self):
        # 新システム統合
        self.universal_slot_manager = UniversalSlotPositionManager()
        
    def _apply_human_grammar_corrections(self, doc, sentence):
        # 統一システム使用
        return self.universal_slot_manager.process_all_patterns(doc, sentence)
```

## 📊 Success Metrics

### Quality Assurance
- **100% 精度維持**: 既存53-54テストケースで完全互換
- **Performance**: 処理時間の維持または改善
- **Memory**: メモリ使用量の最適化

### Development Efficiency  
- **Code Reduction**: 重複コード30%以上削減
- **Extensibility**: 新パターン追加時間50%短縮
- **Maintainability**: テスト作成時間の大幅短縮

## 🚀 Phase 2 Preparation

Phase 1完成により、Phase 2の人間文法認識拡張が大幅に簡素化：

```python
# Phase 2での新パターン追加例
new_pattern = ComplexSVOPattern(
    detection_rules=rules,
    confidence_threshold=0.9
)

universal_manager.register_pattern('complex_svo', new_pattern)
# ← これだけで新パターン追加完了
```

## 📅 Timeline

- **Week 1 (8/21-8/27)**: Core Infrastructure + WhosePattern移行
- **Week 2 (8/28-9/3)**: PassivePattern移行 + 統合テスト  
- **Week 3 (9/4-9/10)**: Optimization + Phase 2準備
- **Week 4 (9/11-9/17)**: Phase 2開始準備完了

---

**次のステップ**: Core Infrastructure実装開始
**実装開始日**: 2025年8月21日
**Phase 1完了予定**: 2025年9月10日
