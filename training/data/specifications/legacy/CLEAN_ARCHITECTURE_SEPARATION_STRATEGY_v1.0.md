# Clean Architecture + Reality Controller Strategy
## 三段階分離による理想と現実の完全分離戦略

**作成日**: 2025年9月3日  
**戦略**: Clean Architecture保護 + 現実対処分離

---

## 🎯 **三段階分離戦略**

### **基本理念: 理想の保護と現実の隔離**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  ① 不適切部分   │───▶│  ② 汎用的改善   │───▶│ ③ エッジ分離    │
│     完全把握     │    │     徹底模索     │    │   最終隔離      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
      現状分析              理想化努力           現実対処分離
```

### **アーキテクチャ分離**
- **Core System**: `true_central_controller.py` + **Clean Handlers** (理想設計保護)
- **Edge Controller**: 現実対処専用システム (泥臭い部分隔離)
- **Reality Bridge**: 必要時のみEdgeに委譲

---

## 📋 **Phase 1: 不適切部分の完全把握** (推定工数: 3-4時間)

### **Task 1.1: 現行システム問題の全数調査**

#### **ハードコーディング箇所の完全リストアップ**
```python
hardcoding_audit = {
    "case_specific": [
        "Case 151: Imagine構文",
        "Case 152: Provided構文", 
        "Case 153: As long as構文",
        "Case 154: If過去完了仮定法",
        "Case 155: Even if構文"
    ],
    "pattern_specific": [
        "WH語主語位置の特別処理",
        "wish文等の特別処理",
        "逆転構造の特別処理",
        "Without/But for構文"
    ],
    "spacy_workarounds": [
        "依存関係解析の補正",
        "品詞判定の上書き",
        "構文構造の強制修正"
    ]
}
```

#### **失敗ケース詳細分析**
```python
def analyze_failure_cases():
    """現在の24失敗ケースを分類"""
    failure_analysis = {
        "spacy_limitation": [],      # spaCy解析能力の限界
        "design_gap": [],            # 設計理念と現実の乖離
        "edge_grammar": [],          # 極端な文法構造
        "complex_nesting": [],       # 複雑な入れ子構造
        "ambiguous_structure": []    # 構造的曖昧性
    }
    
    # 各失敗ケースを上記5カテゴリに分類
    for case in get_failed_cases():
        category = classify_failure_reason(case)
        failure_analysis[category].append(case)
    
    return failure_analysis
```

### **Task 1.2: ハンドラー品質監査**
```python
def audit_handler_quality():
    """各ハンドラーの理想度測定"""
    handlers = [
        "basic_five_pattern_handler.py",
        "conditional_handler.py", 
        "infinitive_handler.py",
        "gerund_handler.py",
        # ... 全ハンドラー
    ]
    
    quality_report = {}
    for handler in handlers:
        quality_report[handler] = {
            "spacy_dependency": assess_spacy_usage(handler),
            "hardcoding_level": detect_hardcoding(handler),
            "principle_adherence": check_grammatical_principles(handler),
            "edge_case_handling": count_special_cases(handler)
        }
    
    return quality_report
```

---

## 🔧 **Phase 2: 汎用的改善の徹底模索** (推定工数: 6-8時間)

### **Task 2.1: 原理的解決可能性の検証**

#### **各問題に対する汎用化アプローチ**
```python
class PrincipleBasedSolver:
    """原理的解決の可能性を検証"""
    
    def analyze_imagine_constructions(self):
        """Case 151: Imagine構文の汎用化"""
        # 1. 文法的特徴の抽出
        features = {
            "trigger_words": ["imagine", "suppose", "consider"],
            "syntactic_pattern": "subjunctive_mood_marker",
            "semantic_role": "hypothetical_condition"
        }
        
        # 2. spaCy解析での検出可能性
        spacy_feasibility = self.test_spacy_detection(features)
        
        # 3. ConditionalHandlerでの処理可能性
        handler_feasibility = self.test_handler_coverage(features)
        
        return {
            "generalizable": spacy_feasibility and handler_feasibility,
            "required_enhancements": self.suggest_improvements(features)
        }
    
    def analyze_provided_constructions(self):
        """Case 152: Provided構文の汎用化"""
        # 同様の分析...
        pass
```

#### **spaCy解析能力の拡張**
```python
class EnhancedSpacyAnalyzer:
    """spaCy解析の限界を補う拡張システム"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.custom_patterns = self.load_custom_patterns()
    
    def enhanced_dependency_analysis(self, sentence):
        """依存関係解析の補強"""
        doc = self.nlp(sentence)
        
        # 1. 標準解析の品質評価
        quality_score = self.assess_parse_quality(doc)
        
        # 2. 品質が低い場合の補強
        if quality_score < 0.8:
            doc = self.apply_custom_patterns(doc, sentence)
            doc = self.structural_heuristics(doc, sentence)
        
        return doc
    
    def load_custom_patterns(self):
        """文法的パターンマッチングルール"""
        return {
            "conditional_markers": [
                {"pattern": "imagine if", "type": "subjunctive"},
                {"pattern": "provided that", "type": "conditional"},
                {"pattern": "as long as", "type": "conditional"}
            ],
            "complex_structures": [
                # 複雑な構造のパターン定義
            ]
        }
```

### **Task 2.2: ハンドラー連携強化**
```python
class HandlerCooperationEngine:
    """ハンドラー間の高度な連携システム"""
    
    def resolve_complex_structures(self, sentence, handler_results):
        """複数ハンドラー結果の賢い統合"""
        
        # 1. 結果の妥当性検証
        validated_results = []
        for result in handler_results:
            if self.validate_grammatical_consistency(result):
                validated_results.append(result)
        
        # 2. 競合解決
        if len(validated_results) > 1:
            return self.resolve_conflicts(validated_results)
        elif len(validated_results) == 1:
            return validated_results[0]
        else:
            return self.fallback_analysis(sentence)
    
    def validate_grammatical_consistency(self, result):
        """文法的妥当性の検証"""
        # スロット構造の論理的整合性チェック
        # 文法原理に基づく妥当性検証
        pass
```

---

## 🚨 **Phase 3: エッジコントローラーへの分離** (推定工数: 4-5時間)

### **Task 3.1: Edge Controller設計**

#### **現実対処専用システム**
```python
class EdgeController:
    """
    Clean Architectureで解決困難な現実問題の専用処理
    - spaCy解析限界の補完
    - 極端なエッジケースの処理
    - 構造的曖昧性の実用的解決
    """
    
    def __init__(self):
        self.spacy_limitations = self.load_spacy_workarounds()
        self.edge_patterns = self.load_edge_patterns()
        self.ambiguity_resolvers = self.load_ambiguity_rules()
    
    def handle_spacy_limitations(self, sentence):
        """spaCy解析限界の補完"""
        # 特定の構造でspaCyが誤解析する既知パターンの修正
        for limitation in self.spacy_limitations:
            if limitation.matches(sentence):
                return limitation.correct_analysis(sentence)
        return None
    
    def handle_edge_grammar(self, sentence):
        """極端な文法構造の処理"""
        # 理論的には正しいが実用的に困難な文法の特別処理
        for pattern in self.edge_patterns:
            if pattern.matches(sentence):
                return pattern.special_processing(sentence)
        return None
    
    def resolve_structural_ambiguity(self, sentence, multiple_results):
        """構造的曖昧性の実用的解決"""
        # 複数の解釈が可能な場合の実用的判定
        for resolver in self.ambiguity_resolvers:
            if resolver.applicable(sentence, multiple_results):
                return resolver.decide(multiple_results)
        return multiple_results[0]  # デフォルト選択
```

#### **Edge Pattern Database**
```json
{
  "spacy_workarounds": [
    {
      "pattern": "imagine if.*would",
      "issue": "subjunctive_mood_misparse", 
      "correction": "force_conditional_analysis",
      "confidence": 0.95
    },
    {
      "pattern": "provided.*that",
      "issue": "passive_voice_confusion",
      "correction": "conditional_marker_detection",
      "confidence": 0.90
    }
  ],
  "edge_grammar": [
    {
      "pattern": "倒置強調構文",
      "structure": "rarely/seldom/never + auxiliary + subject",
      "special_processing": "inversion_handler",
      "frequency": "rare"
    }
  ],
  "ambiguity_resolution": [
    {
      "context": "multiple_clause_attachment",
      "heuristic": "proximity_preference",
      "accuracy": 0.85
    }
  ]
}
```

### **Task 3.2: Reality Bridge設計**
```python
class RealityBridge:
    """Clean SystemとEdge Controllerの橋渡し"""
    
    def __init__(self, clean_controller, edge_controller):
        self.clean = clean_controller
        self.edge = edge_controller
        self.delegation_rules = self.load_delegation_rules()
    
    def process_sentence(self, sentence):
        """統合処理: Clean優先 → Edge委譲"""
        
        # 1. Clean Systemで処理
        clean_result = self.clean.process_sentence(sentence)
        
        # 2. 品質評価
        quality = self.assess_result_quality(clean_result, sentence)
        
        # 3. 品質が低い場合はEdge Controllerに委譲
        if quality < 0.8:
            edge_result = self.edge.process_sentence(sentence)
            
            # 4. 結果の統合
            return self.merge_results(clean_result, edge_result)
        
        return clean_result
    
    def assess_result_quality(self, result, sentence):
        """結果品質の自動評価"""
        quality_score = 0.0
        
        # スロット充填率
        slot_completeness = self.calculate_slot_completeness(result)
        quality_score += slot_completeness * 0.4
        
        # 文法的妥当性
        grammatical_validity = self.validate_grammar(result)
        quality_score += grammatical_validity * 0.4
        
        # spaCy解析との整合性
        spacy_consistency = self.check_spacy_consistency(result, sentence)
        quality_score += spacy_consistency * 0.2
        
        return quality_score
```

---

## 🏗 **最終アーキテクチャ**

### **システム構成**
```
┌─────────────────────────────────────────────────────────┐
│                  Reality Bridge                         │
│              (品質評価・委譲制御)                          │
└─────────────────┬───────────────────┬─────────────────────┘
                  │                   │
    ┌─────────────▼─────────────┐   ┌─▼─────────────────────┐
    │    Clean System           │   │   Edge Controller     │
    │                           │   │                       │
    │ • true_central_controller │   │ • spaCy限界補完        │
    │ • Clean Handlers          │   │ • エッジケース処理      │
    │ • 理想的設計保護           │   │ • 構造的曖昧性解決      │
    │                           │   │ • 現実対処隔離          │
    └───────────────────────────┘   └───────────────────────┘
             95%ケース                    5%ケース
```

### **品質保証**
- **Clean System**: 文法的原理に基づく美しい設計を維持
- **Edge Controller**: 現実的制約への実用的対処を分離
- **Reality Bridge**: 自動品質評価による適切な委譲

---

## 📅 **実装工程表**

### **Phase 1: 分析フェーズ** (3-4時間)
- [ ] 現行システム問題の完全調査
- [ ] 失敗ケース24件の詳細分析
- [ ] ハンドラー品質監査

### **Phase 2: 改善フェーズ** (6-8時間)  
- [ ] 各問題の原理的解決可能性検証
- [ ] spaCy解析能力拡張
- [ ] ハンドラー連携強化

### **Phase 3: 分離フェーズ** (4-5時間)
- [ ] Edge Controller実装
- [ ] Reality Bridge設計
- [ ] 統合テスト

### **Phase 4: 検証フェーズ** (2-3時間)
- [ ] 品質評価システム検証
- [ ] 委譲ルール調整
- [ ] 最終統合テスト

**総工数見積もり**: 15-20時間

---

## 🎯 **成功基準**

### **技術的目標**
- **Clean System**: 90%以上のケースで理想的処理
- **Edge Controller**: 残り10%の現実的解決
- **統合品質**: 現行88% → 95%以上の成功率

### **設計品質目標**
- **保守性**: Clean Systemの美しい設計維持
- **拡張性**: 新機能追加時のClean System優先
- **分離性**: 現実対処のEdge Controller完全隔離

**最終成果**: 理想と現実の完全分離による持続可能なアーキテクチャ
