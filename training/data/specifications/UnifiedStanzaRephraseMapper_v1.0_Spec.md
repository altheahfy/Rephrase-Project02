# UnifiedStanzaRephraseMapper v1.4 設計仕様書

**作成日**: 2025年8月16日  
**最終更新**: 2025年8月22日  
**バージョン**: v1.4+  
**ステータス**: 人間文法認識システム実装完了、100%精度達成、"lives"誤認識問題解決済み  
**新機能**: Order機能統合設計追加 *(2025年8月22日)*

---

## 📋 **主要セクション**

1. **🏗️ システム設計思想** - プラグイン型同時処理方式 + 段階的ハイブリッド戦略
2. **🧠 人間文法認識システム詳細** - 構造パターン認識による高精度解析
3. **📊 ハンドラー系統別処理方式** - 15の専門ハンドラーによる協調処理
4. **🔄 段階的移行実装戦略** - リスク最小化による段階的実装
5. **🔢 Order機能統合設計** - *NEW* 絶対順序システムによるランダマイゼーション実現
6. **⚡ パフォーマンス最適化** - 処理効率とメモリ使用量の最適化
7. **🧪 テスト・検証システム** - 品質保証と回帰テスト
8. **🚀 本番展開計画** - 段階的リリースとリスク管理  

---

## 🏗️ **システム設計思想**

### **核心概念: プラグイン型同時処理方式 + 段階的ハイブリッド戦略**

```
🎯 設計原理:
全ての専門シェフが同時に厨房に入り、
各自の専門領域を見極めて同時並行処理を行う

🔄 v1.4新戦略: 段階的ハイブリッド実装
各ハンドラーの内部実装を、Stanza依存から人間文法認識へ段階的移行
アーキテクチャは完全維持、内部実装のみ改善

🏢 従来方式との差異:
❌ 旧方式: 順次選択型（15個の個別エンジンから1つを選択）
✅ 新方式: 協調処理型（全ハンドラーが並行動作して協調）
🆕 v1.4: ハイブリッド型（確実パターンは人間文法、複雑パターンはStanza補完）
```
✅ 新方式: 同時処理型（全ハンドラーが並行動作して協調）
```

### **アーキテクチャ構造**

```
┌─────────────────────────────────────────────┐
│ UnifiedStanzaRephraseMapper v1.4            │
├─────────────────────────────────────────────┤
│ 🔄 段階的ハイブリッド解析システム             │
│ ┌─────────────────────────────────────────┐ │
│ │ 人間文法認識 (確実パターン)             │ │
│ │ ├─ whose構文パターン ✅                │ │
│ │ ├─ 基本5文型パターン (予定)             │ │
│ │ └─ 受動態パターン (予定)               │ │
│ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────┐ │
│ │ Stanza + spaCy補完 (複雑パターン)       │ │
│ │ ├─ 複合関係節                          │ │
│ │ ├─ 入れ子構造                          │ │
│ │ └─ 不明パターン                        │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 🆕 ハンドラー間連携システム (基本実装完了)     │
│ ┌─────────────────────────────────────────┐ │
│ │ handler_shared_context                  │ │
│ │ ├─ predefined_slots (実装済み)          │ │
│ │ ├─ remaining_elements (設計中)          │ │
│ │ ├─ handler_metadata (部分実装)         │ │
│ │ └─ control_flags (実装済み)             │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ �️ プラグイン型協調ハンドラーシステム         │
│ ┌─────────────────────────────────────────┐ │
│ │ アーキテクチャ: 完全維持               │ │
│ │ 内部実装: 段階的人間文法認識化          │ │
│ │ ✅ _handle_participle_construction      │ │
│ │ 🔄 _handle_relative_clause (移行中)     │ │
│ │ 🔄 _handle_basic_five_pattern (移行中)  │ │
│ │ 🔄 _handle_passive_voice (移行予定)     │ │
│ │ ✅ _handle_adverbial_modifier           │ │
│ │ ✅ _handle_auxiliary_complex            │ │
│ │ ✅ _handle_conjunction                  │ │
│ └─────────────────────────────────────────┘ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 🆕 分詞構文保護システム (実装完了)           │
│ ├─ participle_detected フラグ制御          │
│ ├─ 受動態ハンドラー保護機能                │
│ └─ 主スロット競合回避                      │
├─────────────────────────────────────────────┤
│ 🚧 位置別サブスロット管理システム (部分実装) │
├─────────────────────────────────────────────┤
│ 結果統合・重複解決・優先度処理               │
└─────────────────────────────────────────────┘
├─────────────────────────────────────────────┤
│ 結果統合・重複解決・優先度処理               │
└─────────────────────────────────────────────┘
```

---

## 🧠 **人間文法認識システム詳細 (v1.4新機能)**

### **基本設計思想**

```
従来: Stanza統計解析 → 修正 → スロット変換
新方式: 構造パターン認識 → 文法ルール適用 → 直接スロット生成
```

### **Stanza vs 人間文法認識の比較**

| 観点 | Stanza/spaCy | 人間文法認識システム |
|------|--------------|------------------|
| **認識方法** | 統計的パターンマッチング | 構造的文法ルール |
| **判定根拠** | 「よく一緒に現れる組み合わせ」 | 「文法的に必然の関係」 |
| **処理順序** | 語→文（ボトムアップ） | 文→語（トップダウン） |
| **エラーの原因** | 統計の偏り | ルールの不完全性 |
| **デバッグ性** | 困難（ブラックボックス） | 容易（透明なルール） |

### **段階的ハイブリッド戦略**

#### **設計原則: 100%精度保護最優先**
```
🛡️ 基本方針:
既存の100%精度システムを絶対に壊さない
段階的ラッパー方式による最小リスク移行
各ステップでの完全品質保証

⚠️ 移行の複雑さ認識:
現在のシステムはStanzaに深度依存
データ構造・処理フローの根本的違い
完全移行は数週間の高リスク作業
```

#### **現実的移行戦略: 段階的ラッパー方式**

**Phase 1: リスク最小化ラッパー実装**
```python
class HybridTransitionHandler:
    def __init__(self):
        # 既存Stanza実装を完全保護
        self.stanza_backup = copy.deepcopy(existing_stanza_handler)
        
        # 人間文法認識パターンを段階的追加
        self.human_patterns = {
            'whose_clause': WhosePattern(),     # ✅ 実装済み（成功実績）
            'basic_svo': None,                  # 🔄 次の移行対象
            'passive_voice': None,              # 🔄 その後の対象
        }
        
        # 品質保証フラグ
        self.enable_human_grammar = True
        self.fallback_mode = 'immediate'  # 問題時即座復旧
    
    def process(self, sentence, result):
        if self.enable_human_grammar:
            # 1. 人間文法認識で処理可能かチェック
            for pattern_name, pattern in self.human_patterns.items():
                if pattern and pattern.can_handle(sentence):
                    human_result = pattern.process(sentence)
                    
                    # 2. 結果の妥当性チェック
                    if self._validate_human_result(human_result, sentence):
                        return human_result
                    
                    # 3. 問題時の即座フォールバック
                    self._log_fallback(pattern_name, sentence)
        
        # 4. 既存Stanza実装（完全無改変）
        return self.stanza_backup.process(sentence, result)
```

**Phase 2: 段階的パターン移行**
```python
# 最小単位での移行（各1-2日）
def migrate_single_pattern(pattern_name, test_sentences):
    """単一パターンの慎重な移行"""
    
    # 1. 新パターン実装
    new_pattern = implement_human_pattern(pattern_name)
    
    # 2. 限定テスト（該当例文のみ）
    test_results = run_limited_test(new_pattern, test_sentences)
    
    # 3. 品質保証チェック
    if test_results.success_rate < 100%:
        rollback_immediately()
        return False
    
    # 4. 全例文テスト
    full_results = run_full_test_suite()
    
    # 5. 最終判定
    if full_results.success_rate == 100%:
        commit_pattern_migration(pattern_name)
        return True
    else:
        rollback_immediately()
        return False
```

**Phase 3: 段階的置換スケジュール**
```python
migration_schedule = {
    'v2.0.1': {
        'target': 'basic_svo_simple',
        'scope': 'I love you形式のみ',
        'risk': 'LOW',
        'fallback': 'immediate_available'
    },
    'v2.0.2': {
        'target': 'basic_svo_complex', 
        'scope': '修飾語付きSVO',
        'risk': 'MEDIUM',
        'fallback': 'immediate_available'
    },
    'v2.0.3': {
        'target': 'passive_voice_simple',
        'scope': '基本受動態のみ',
        'risk': 'MEDIUM', 
        'fallback': 'immediate_available'
    }
}
```

#### **品質保証・リスク管理システム**

**絶対保護原則**
- **100%精度は絶対維持**: 一時的な品質低下も許可しない
- **即座復旧機能**: 問題発生時0.1秒以内でStanzaにフォールバック  
- **完全ロールバック**: 任意の時点への完全復旧が可能

**1. 完全バックアップシステム**
```python
class StanzaSystemBackup:
    """現在の100%精度システムの完全保護"""
    
    def __init__(self):
        # 既存システムの完全複製保存
        self.original_handlers = self._deep_copy_all_handlers()
        self.original_test_results = self._backup_current_results()
        self.checkpoint_timestamps = []
        
        # 緊急復旧機構の事前テスト
        self._verify_emergency_restoration()
    
    def immediate_rollback(self, component_name):
        """問題発生時の即座復旧（0.1秒以内）"""
        start_time = time.time()
        
        # 1. 問題コンポーネント無効化
        disable_component(component_name)
        
        # 2. Stanzaバックアップ有効化
        activate_stanza_backup(component_name)
        
        # 3. 復旧検証
        verify_restoration_success()
        
        recovery_time = time.time() - start_time
        assert recovery_time < 0.1  # 0.1秒以内保証
        
    def validate_system_integrity(self):
        """システム整合性の継続検証"""
        current_results = run_full_test_suite()
        
        # 完全一致確認（100%基準）
        if current_results != self.original_test_results:
            self.emergency_full_restoration()
            return False
        
        return True
    
    def emergency_full_restoration(self):
        """緊急時完全復旧プロトコル"""
        # システム全体を既知安定状態に復旧
        self._restore_all_components()
        self._verify_complete_restoration()
        self._log_emergency_restoration()
```

**2. 段階的品質保証（多層防護）**
```python
class MultiLayerQualityAssurance:
    """多層防護による品質保証システム"""
    
    def __init__(self):
        self.quality_gates = [
            PreImplementationGate(),
            ImplementationGate(), 
            PostImplementationGate(),
            ContinuousMonitoringGate()
        ]
    
    def migration_quality_gate(self, pattern_name):
        """各移行段階での厳格な品質チェック"""
        
        # ゲート1: 実装前検証
        pre_check = self._pre_implementation_validation(pattern_name)
        if not pre_check.passed:
            return self._reject_migration("Pre-implementation failed", pre_check.details)
        
        # ゲート2: 実装中監視
        impl_monitor = self._implementation_monitoring(pattern_name)
        if not impl_monitor.stable:
            return self._abort_implementation("Implementation unstable", impl_monitor.issues)
        
        # ゲート3: 実装後完全検証
        post_validation = self._post_implementation_validation(pattern_name)
        if not post_validation.perfect():
            return self._reject_migration("Post-implementation failed", post_validation.failures)
        
        # ゲート4: 継続監視開始
        self._start_continuous_monitoring(pattern_name)
        
        return self._approve_migration(pattern_name)
    
    def _post_implementation_validation(self, pattern_name):
        """実装後の包括的検証"""
        
        validation_results = {}
        
        # テスト1: 該当パターンの完全性
        pattern_test = test_specific_pattern(pattern_name)
        validation_results['pattern_specific'] = pattern_test.perfect()
        
        # テスト2: 全例文での品質維持（最重要）
        full_test = run_complete_test_suite()
        validation_results['overall_quality'] = (full_test.success_rate == 100%)
        
        # テスト3: パフォーマンス確認
        performance_test = measure_processing_speed()
        validation_results['performance'] = (performance_test.degradation < 5%)
        
        # テスト4: メモリ・リソース確認
        resource_test = check_resource_usage()
        validation_results['resources'] = resource_test.within_limits()
        
        # テスト5: エラーハンドリング確認
        error_handling_test = test_error_scenarios()
        validation_results['error_handling'] = error_handling_test.robust()
        
        # 全てのテストが完璧でなければ不合格
        return ValidationResult(
            perfect=all(validation_results.values()),
            details=validation_results
        )
```

**3. 継続的監視システム**
```python
class ContinuousQualityMonitoring:
    """リアルタイム品質監視"""
    
    def __init__(self):
        self.quality_threshold = 100%  # 絶対基準
        self.performance_threshold = 95%  # 許容範囲
        self.monitoring_interval = 0.1  # 0.1秒間隔
        self.alert_system = AlertSystem()
    
    def start_monitoring(self):
        """継続的品質監視開始"""
        while system_running:
            try:
                # 品質チェック
                current_quality = self._measure_current_quality()
                if current_quality < self.quality_threshold:
                    self._trigger_immediate_fallback("Quality degraded")
                
                # パフォーマンスチェック
                current_performance = self._measure_performance()
                if current_performance < self.performance_threshold:
                    self._trigger_performance_alert()
                
                # システム整合性チェック
                integrity_ok = self._check_system_integrity()
                if not integrity_ok:
                    self._trigger_emergency_restoration()
                
            except Exception as e:
                # 監視システム自体の異常
                self._emergency_fallback_all_systems(e)
            
            sleep(self.monitoring_interval)
    
    def _trigger_immediate_fallback(self, reason):
        """即座フォールバック実行"""
        self.alert_system.emergency_alert(f"IMMEDIATE FALLBACK: {reason}")
        self.backup_system.immediate_rollback("all_components")
        self._verify_fallback_success()
```

**4. 緊急時対応プロトコル**

**レベル1: 品質低下検出**
```python
def handle_quality_degradation(detection_details):
    """品質低下時の自動対応"""
    
    # 1. 即座にStanzaフォールバック（0.1秒以内）
    emergency_timestamp = time.time()
    activate_stanza_fallback_all()
    
    # 2. 問題箇所の特定・隔離
    problematic_component = isolate_problematic_component(detection_details)
    disable_component(problematic_component)
    
    # 3. システム状態のログ保存
    save_system_state_for_analysis({
        'timestamp': emergency_timestamp,
        'detection_details': detection_details,
        'affected_component': problematic_component,
        'system_snapshot': capture_system_snapshot()
    })
    
    # 4. 自動復旧実行・検証
    execute_automatic_recovery()
    verify_recovery_success()
    
    # 5. 品質確認・報告
    quality_check = run_complete_test_suite()
    assert quality_check.success_rate == 100%
```

**レベル2: システム異常検出**
```python
def handle_system_anomaly(anomaly_type, anomaly_data):
    """システム異常時の緊急対応"""
    
    # 1. 完全システム停止（安全確保）
    emergency_system_halt()
    
    # 2. 最新安定版への完全復旧
    restore_to_last_known_good_checkpoint()
    
    # 3. 完全整合性チェック実行
    integrity_verification = verify_complete_system_integrity()
    if not integrity_verification.perfect():
        # 更に前のチェックポイントに復旧
        restore_to_previous_checkpoint()
    
    # 4. 段階的サービス復旧
    gradual_service_restoration_protocol()
    
    # 5. 異常原因分析・再発防止
    anomaly_analysis = analyze_anomaly_root_cause(anomaly_type, anomaly_data)
    implement_prevention_measures(anomaly_analysis)
```

#### **実装タイムライン（現実的スケジュール）**

**完全リスク管理下での段階的実装**

| 期間 | 作業内容 | リスク | 成功基準 | 失敗時対応 |
|------|----------|--------|----------|------------|
| **8/22-23** | 安全基盤構築・バックアップ | **極低** | システム動作継続、バックアップ機能テスト完了 | なし（準備作業のため） |
| **8/24-25** | basic_svo_simple移行実験 | **低** | 100%精度維持、対象例文正確処理 | 即座Stanzaフォールバック |
| **8/26-27** | 品質検証・判定フェーズ | **中** | 全54例文100%正確、性能維持 | 完全ロールバック実行 |
| **8/28-29** | 拡張 or 戦略見直し | **中** | 品質保証継続 | 移行戦略の根本的見直し |

**詳細実装プロトコル**

**8/22-23: 安全基盤構築（リスク0%）**
```python
# Phase 0 準備作業 - システムに影響を与えない作業のみ
day_1_tasks = {
    "morning": [
        "現在システム完全バックアップ作成",
        "復旧機能の動作テスト",
        "品質監視システム準備"
    ],
    "afternoon": [
        "ラッパーシステム設計・実装（未接続状態）", 
        "テスト環境構築",
        "エラーハンドリング機構実装"
    ],
    "evening": [
        "緊急時対応手順確認",
        "翌日実験の最終準備",
        "システム整合性確認"
    ]
}

success_criteria_day1 = {
    "backup_system": "完全バックアップ作成完了",
    "rollback_test": "復旧機能正常動作確認",
    "monitoring": "品質監視システム稼働",
    "no_impact": "既存システム無改変・100%精度維持"
}
```

**8/24-25: 最小リスク移行実験（慎重実装）**
```python
# 最も安全なパターンから開始
day_2_experiment = {
    "target_pattern": "basic_svo_simple",
    "target_sentences": [
        "I love you.",           # 最も基本的
        "She works hard.",       # 副詞あり
        "We study English."      # 複数主語
    ],
    "safety_measures": {
        "scope_limitation": "対象3例文のみ",
        "fallback_immediate": "問題発生時0.1秒以内復旧",
        "continuous_monitoring": "0.1秒間隔品質チェック"
    }
}

experiment_protocol = {
    "step1": "ラッパーシステム有効化（対象例文のみ）",
    "step2": "対象例文での人間文法認識テスト",
    "step3": "全例文での品質確認（54例文100%必須）",
    "step4": "パフォーマンス測定",
    "step5": "24時間継続監視"
}

quality_gates = {
    "gate1": "対象例文100%正確",
    "gate2": "全体品質100%維持", 
    "gate3": "パフォーマンス劣化5%以内",
    "gate4": "24時間安定動作"
}
```

**8/26-27: 品質検証・判定フェーズ（厳格評価）**
```python
# 移行継続の可否を決定する重要フェーズ
evaluation_protocol = {
    "comprehensive_testing": {
        "full_suite": "54例文完全テストスイート",
        "stress_testing": "高負荷での品質確認",
        "edge_cases": "境界条件での動作確認"
    },
    
    "performance_analysis": {
        "speed_check": "処理速度測定・比較",
        "memory_usage": "メモリ使用量確認",
        "resource_efficiency": "リソース効率性評価"
    },
    
    "stability_verification": {
        "long_running": "長時間運用での安定性",
        "error_handling": "エラー状況での復旧能力",
        "integration": "システム全体との統合性"
    }
}

decision_criteria = {
    "continue_migration": {
        "quality": "100%精度完全維持",
        "performance": "劣化5%以内",
        "stability": "24時間安定動作",
        "confidence": "今後の移行計画への確信"
    },
    
    "rollback_decision": {
        "quality_issue": "精度100%未満",
        "performance_issue": "劣化5%超過",
        "stability_issue": "不安定動作検出",
        "complexity_concern": "実装複雑性が高すぎる"
    }
}
```

**8/28-29: 拡張 or 戦略見直し（結果に基づく判断）**
```python
# 前フェーズの結果に基づく分岐処理
outcome_scenarios = {
    "success_scenario": {
        "condition": "全ての品質ゲートクリア",
        "action": "次パターン（basic_svo_complex）への移行準備",
        "timeline": "同様の慎重なプロトコルで実施",
        "risk_level": "低（成功実績に基づく）"
    },
    
    "partial_success_scenario": {
        "condition": "品質維持だが課題発見",
        "action": "問題分析・改善策検討",
        "timeline": "課題解決後の再実験計画",
        "risk_level": "中（要改善点あり）"
    },
    
    "failure_scenario": {
        "condition": "品質劣化またはシステム不安定",
        "action": "完全ロールバック・戦略根本見直し",
        "timeline": "代替アプローチの検討期間",
        "risk_level": "高（アプローチ変更必要）"
    }
}

strategy_review_options = {
    "approach_1": "より段階的な移行（例文単位での移行）",
    "approach_2": "異なる技術アプローチ（AIアシスト人間認識等）",
    "approach_3": "現行システム最適化（Stanza精度向上に集中）",
    "approach_4": "長期計画への変更（数ヶ月スパンでの移行）"
}
```

**成功の定義（絶対基準）**
```python
absolute_success_criteria = {
    "quality": {
        "metric": "全54例文での正確性",
        "threshold": "100%（例外なし）",
        "measurement": "完全一致による検証"
    },
    
    "stability": {
        "metric": "システム安定性",
        "threshold": "24時間連続安定動作",
        "measurement": "継続監視による確認"
    },
    
    "performance": {
        "metric": "処理速度・リソース使用量",
        "threshold": "劣化5%以内",
        "measurement": "ベンチマーク比較"
    },
    
    "maintainability": {
        "metric": "コード品質・可読性",
        "threshold": "既存レベル維持",
        "measurement": "レビュー・テストカバレッジ"
    }
}
```
```python
# 実装済み例: whose構文
def _handle_relative_clause(self, sentence, result):
    if self._detect_whose_pattern(sentence):
        return self._human_grammar_whose_clause(sentence)  # 人間文法認識
    else:
        return self._stanza_relative_clause(sentence)      # Stanzaフォールバック

def _human_grammar_whose_clause(self, sentence):
    # 1. 構造パターン認識
    whose_pos = sentence.find("whose")
    antecedent = self._extract_noun_before_whose(sentence, whose_pos)
    
    # 2. 構造的分析
    relative_clause = self._extract_clause_after_whose(sentence, whose_pos)
    main_clause = self._extract_remaining_clause(sentence, relative_clause)
    
    # 3. 構造から語の役割を確定
    main_verb = self._find_main_verb_in_clause(main_clause)  # 構造的に動詞確定
    
    return self._build_slots_from_structure(antecedent, main_verb, relative_clause)
```

#### **Phase 2: 基本パターンの段階的移行**
- **優先度高**: SVO, SVC等の基本5文型
- **優先度中**: 受動態、完了形
- **優先度低**: 複合構造、入れ子構造

#### **Phase 3: Stanzaフォールバックの最小化**
- 人間文法認識カバー率90%以上を目標
- Stanzaは真に複雑な構文のみ担当

### **実装パターンテンプレート**

```python
class HumanGrammarPattern:
    def can_handle(self, sentence) -> bool:
        """このパターンで処理可能かを判定"""
        pass
    
    def analyze_structure(self, sentence) -> dict:
        """文構造を分析"""
        pass
    
    def determine_word_roles(self, structure) -> dict:
        """構造から語の役割を確定"""
        pass
    
    def build_slots(self, word_roles) -> dict:
        """スロット構造を構築"""
        pass

# 具体例: whose構文パターン
class WhoseClausePattern(HumanGrammarPattern):
    def can_handle(self, sentence):
        return "whose" in sentence.lower()
    
    def analyze_structure(self, sentence):
        # 構造的分析ロジック
        return {
            'antecedent': antecedent,
            'relative_clause': relative_clause,
            'main_clause': main_clause
        }
```

---

## 🎯 **実装完了ハンドラー詳細**

### **🆕 0. participle_construction (分詞構文) - v1.3新規追加**
- **責任範囲**: 現在分詞、過去分詞、being+過去分詞の分詞構文処理
- **対応例文**: 修飾分詞、分詞構文、being構文
- **実装状況**: ✅ 完了 (v1.3)
- **保護機能**: `participle_detected`フラグによる他ハンドラー制御
- **例**: "The children playing..." → S:'', sub-v:'the children playing'

### **1. basic_five_pattern (基本5文型)**
- **責任範囲**: S, V, O1, O2, C1, C2, Aux の基本構造認識
- **対応例文**: 第1-5文型、助動詞、時制の基本形
- **実装状況**: ✅ 完了
- **🆕 v1.3強化**: 分詞構文保護機能、共有コンテキスト対応
- **例**: "I love you." → S:I, V:love, O1:you

### **2. relative_clause (関係節)**
- **責任範囲**: who, which, that, whose, where, when, why, how の関係節処理
- **対応例文**: 関係代名詞、関係副詞、省略関係代名詞
- **実装状況**: ✅ 完了
- **🆕 v1.3強化**: 主スロット占有情報の共有コンテキスト伝達
- **例**: "The man who runs is fast." → S:"", V:is, C1:fast + sub-slots

### **3. passive_voice (受動態)**
- **責任範囲**: be動詞 + 過去分詞の受動態構造認識
- **対応例文**: 能動態↔受動態変換、by句処理
- **実装状況**: ✅ 完了
- **🆕 v1.3強化**: 分詞構文保護機能実装
- **例**: "The letter was written by John." → S:The letter, Aux:was, V:written, M1:by John

### **4. adverbial_modifier (副詞修飾)**
- **責任範囲**: 副詞、副詞句、時間・場所・方法表現
- **対応例文**: M1, M2, M3 修飾要素の適切な分類
- **実装状況**: ✅ 完了
- **例**: "She sings beautifully." → S:She, V:sings, M1:beautifully

### **5. auxiliary_complex (複合助動詞)**
- **責任範囲**: 複数助動詞の組み合わせ、完了形、受動態助動詞
- **対応例文**: have been, will have, might have been等の複合構造
- **実装状況**: ✅ 完了
- **🆕 v1.3強化**: 分詞構文sub-aux保護機能
- **例**: "He has been working." → S:He, Aux:has been, V:working

### **🆕 6. conjunction (接続詞) - v1.3新規追加**
- **責任範囲**: and, but, or等の接続詞処理
- **対応例文**: 等位接続、従属接続
- **実装状況**: ✅ 完了 (v1.3)
- **例**: 基本的な接続詞構文対応

---

## � **ハンドラー間連携システム詳細 (v1.3新機能)**

### **🏗️ ハンドラー間連携システム (occupied_main_slots)**

#### **handler_shared_context 構造 (実装済み)**
```python
handler_shared_context = {
    'occupied_main_slots': set(),        # ✅ 占有された主スロット管理
    'handler_metadata': {               # ✅ 関係節情報のみ実装
        'relative_clause': {
            'occupied_slot': str,        # 占有スロット名
            'antecedent': str,          # 先行詞
            'processed_sub_slots': list  # 処理済みサブスロット
        }
    }
}
```

#### **占有管理システム (実装済み)**
```python
# 関係節ハンドラーによる主スロット占有宣言
shared_context['occupied_main_slots'].add(antecedent_position)

# 5文型ハンドラーでの占有チェック
occupied_slots = shared_context.get('occupied_main_slots', set())
if occupied_slots:
    # 部分的パターン検出を実行
    perform_partial_pattern_detection()
```

### **🛡️ ハンドラー間連携システム詳細**

#### **🎯 設計理念 (あるべき姿)**
```
汎用上位サブ連結システム:
全てのハンドラーが句・節情報を統一プロトコルで交換し、
動的に実行順序を最適化する完全協調型システム
```

#### **🔍 現在の実装状況**

**✅ 実装完了機能:**
```python
# 基本的な共有コンテキスト
handler_shared_context = {
    'occupied_main_slots': set(),  # 占有済み上位スロット (基本実装)
    'remaining_elements': {},      # 残り要素情報 (構造のみ)
    'handler_metadata': {}         # ハンドラー別メタデータ (限定実装)
}

# 関係節→5文型への情報伝達 (成功例)
shared_context['occupied_main_slots'].add(antecedent_position)
occupied_slots = shared_context.get('occupied_main_slots', set())
```

**� 部分実装機能:**
```python
# 分詞構文保護システム (フラグベース)
control_flags['participle_detected'] = True

# ハンドラー実行順序 (固定順序)
ordered_handlers = [
    'participle_construction',  # 最優先
    'relative_clause',         # 占有情報設定
    'basic_five_pattern',      # 占有情報参照
    # ... 残りは固定順序
]
```

**❌ 未実装・設計中機能:**
```python
# 理想的な汎用連携システム (未実装)
class HandlerProtocol:
    def declare_dependencies(self) -> List[str]
    def provide_information(self, context) -> HandlerInfo
    def consume_information(self, available_info) -> ProcessingDecision

# 動的実行順序制御 (未実装)
def optimize_handler_execution_order(dependencies, available_handlers)

# whose構文の「処理委託」先システム (コメントのみ、実装なし)
# 現実: basic_five_pattern の通常処理に依存
def generic_upper_sub_connection_system(clause_info, main_structure)
```

**🔍 現状の技術的負債:**
- whose構文: "汎用システムに委託"のコメントあり、実際は5文型ハンドラーが処理
- 情報伝達: 関係節→5文型のみ実装、他ハンドラー間は未対応
- 実行順序: 固定順序、依存関係による動的制御なし

#### **� 今後の実装方針**

**Phase 2.1: プロトコル統一**
- 全ハンドラー間の情報交換インターフェース統一
- whose構文処理の実際の汎用システム移行
- メタデータ共有の完全実装

**Phase 2.2: 動的制御**
- ハンドラー依存関係の自動解決
- 実行順序の動的最適化
- 句・節境界の自動認識

---

## �🔄 **処理フロー**

### **Phase 1: 統合解析**
1. **Stanza解析**: 基本的な品詞・依存関係分析
2. **spaCyハイブリッド補正**: 特定パターンの解析修正
3. **統一doc生成**: 全ハンドラー共通の解析結果

### **Phase 2: 並行ハンドラー処理**
```python
# 全アクティブハンドラーの同時実行
for handler_name in self.active_handlers:
    handler_method = getattr(self, f'_handle_{handler_name}')
    handler_result = handler_method(main_sentence, result.copy())
    
    if handler_result:
        result = self._merge_handler_results(result, handler_result, handler_name)
```

### **Phase 3: 結果統合**
1. **重複解決**: 複数ハンドラーからの競合結果を調整
2. **優先度適用**: ハンドラー固有の優先度ルール
3. **サブスロット統合**: 位置別サブスロット管理システムによる整理

---

## 📊 **現在の対応範囲**

### **✅ 実装済み機能 (54例文100%対応)**
- **基本5文型**: 20例文 (37%)
- **関係節**: 18例文 (33%)
- **受動態**: 11例文 (20%)
- **副詞修飾**: 5例文 (9%)

---

## 📊 **実装済みハンドラーパフォーマンス (2025年8月19日更新)**

### **実証済み精度（53例文標準検証）**
| ハンドラー | 適用例文数 | 貢献度 | 主な成功パターン |
|-----------|------------|---------|------------------|
| basic_five_pattern | 53/53 | 100% | SV, SVC, SVO, SVOO, SVOC |
| relative_clause | 19/53 | 36% | who, which, that, whose節 |
| passive_voice | 13/53 | 25% | be + 過去分詞構造 |
| adverbial_modifier | 40/53 | 75% | 副詞、前置詞句、時間・場所表現 |
| auxiliary_complex | 19/53 | 36% | have been, will have等複合助動詞 |

### **全体精度実績 (標準検証v4.0 - 人間文法認識システム完成後)**
- **完全一致率**: **100%** (54/54例文) 🏆 **完全精度達成！**
- **部分一致率**: 0% (0/54例文) - 全ケース完全一致
- **処理成功率**: 100% (54/54例文)
- **平均処理時間**: 0.32秒/例文
- **重要修正**: "The man whose car is red lives here"のStanza誤認識解決

### **スロット別精度詳細 (v1.4最新実績)**
- **S (主語)**: 100.0% (54/54) ✅ PERFECT
- **V (動詞)**: 100.0% (54/54) ✅ PERFECT  
- **Aux (助動詞)**: 100.0% (19/19) ✅ PERFECT
- **O1 (目的語)**: 100.0% (7/7) ✅ PERFECT
- **M1 (修飾語1)**: 100.0% (1/1) ✅ PERFECT
- **M2 (修飾語2)**: 100.0% (30/30) ✅ PERFECT
- **M3 (修飾語3)**: 100.0% (10/10) ✅ PERFECT
- **C1 (補語)**: 100.0% (20/20) ✅ PERFECT

### **� 100%精度達成の技術的要因**
- **人間文法認識システム**: Stanzaの"lives"誤認識(NOUN→VERB)を修正
- **whose構文修正パターン**: `_correct_whose_ambiguous_verb_pattern`実装
- **ハイブリッド修正システム**: 文書レベル→文レベルの修正情報伝達

### **✅ 実装済み機能 (v1.4完成版)**
- **🆕 人間文法認識システム**: Stanza誤認識の修正機能  
- **ハンドラー間連携システム**: 占有スロット情報の動的共有
- **分詞構文保護機能**: participle_detected フラグ制御
- **超シンプルルール**: 1個→M2, 2個→M2,M3, 3個→M1,M2,M3
- **Rephraseルール**: 全単語スロット配置、サブスロット時の上位空化
- **助動詞系**: will, can, must, should等の詳細分類
- **関係節処理**: whose, which, that等の高精度処理
- **時制系**: 完了形、進行形、受動態の完全対応
- **準動詞系**: 不定詞、動名詞、分詞の処理
- **関係詞節**: whose, which, that等の高精度処理

---

## 🧪 **テスト・検証システム (v1.2更新)**

### **🔒 標準検証方法 (必須準拠)**
**⚠️ 重要**: 都度作成のテストスクリプトは禁止。以下の標準方法のみ使用すること。

#### **Step 1: CLIバッチ処理**
```bash
# 標準テストセット処理 (53例文)
python unified_stanza_rephrase_mapper.py --input final_test_system/final_54_test_data.json

# 結果ファイル: batch_results_YYYYMMDD_HHMMSS.json が生成される
```

#### **Step 2: 精度分析**
```bash
# 生成された結果ファイルを分析
python compare_results.py --results batch_results_YYYYMMDD_HHMMSS.json

# 出力: 完全一致率、部分一致率、スロット別精度詳細
```

#### **Step 3: 結果検証**
- **完全一致率**: 期待値との100%一致ケース数
- **部分一致率**: 一部スロットが一致するケース数  
- **スロット別精度**: 各スロット(S,V,C1,O1,Aux,M1,M2,M3)の精度

### **🚫 禁止事項**
- ❌ 都度作成のテストスクリプト使用
- ❌ 個別例文での単発テスト
- ❌ 不完全な検証方法による精度報告
- ❌ compare_results.py以外の精度計算ツール

### **📊 現在の実証済み精度 (2025年8月21日) - v1.3最終更新**
- **完全一致率**: **98.1%** (52/53例文) [v1.2: 67.9% → +30.2pt 大幅向上]
- **部分一致率**: 1.9% (1/53例文) 
- **処理成功率**: 100% (53/53例文)
- **🎯 主要スロット**: **完全100%精度達成** (S,V,Aux,O1,M1,M2,M3)
- **残課題**: C1スロット 1ケース (95.0% → 100%が最終目標)
- **検証方法**: CLI + compare_results.py (標準準拠)

### **v1.3 精度向上実績 - 歴代最高達成**
- **解決済みエラー**: 全分詞構文エラー、ハンドラー間連携問題、占有スロット競合
- **システム安定性**: 7ハンドラー完全連携、占有情報共有機能実装
- **ハンドラー別精度**: 
  - S,V,Aux,O1,M1,M2,M3: **100.0%** ✅ PERFECT
  - C1: 95.0% (残り1ケースのみ)
  - M2: 96.7%, M3: 100.0%（大幅改善）

### **カスタムテスト環境**
- **高精度テスト**: カスタム5例文で100%精度達成
- **構成**: 実装済み5ハンドラー完全対応版
- **継続監視**: バッチ処理による定量的精度測定

---

## 🔧 **技術仕様**

### **依存関係**
```python
# 必須ライブラリ
import stanza              # 核心NLP解析
import spacy              # ハイブリッド補正（オプション）
import logging            # デバッグ・モニタリング
```

### **初期化パラメータ**
```python
UnifiedStanzaRephraseMapper(
    language='en',           # 処理言語
    enable_gpu=False,        # GPU使用フラグ
    log_level='INFO',        # ログレベル
    use_spacy_hybrid=True    # spaCyハイブリッド使用
)
```

### **ハンドラー管理API**
```python
# ハンドラー追加
mapper.add_handler('basic_five_pattern')
mapper.add_handler('relative_clause')
mapper.add_handler('passive_voice') 
mapper.add_handler('adverbial_modifier')

# ハンドラー状態確認
active_handlers = mapper.list_active_handlers()
stats = mapper.get_stats()
```

---

## 🚀 **開発ロードマップ（95%精度達成戦略）**

### **🧠 基本戦略: ハイブリッド解析システム**

#### **レイヤー1: Stanza/spaCy基盤解析**
- **役割**: 基本的な依存関係分析、品詞タグ付け、構文解析
- **得意領域**: 明確な文法構造、一般的な文型パターン
- **制約**: 曖昧性解決、文脈依存構造に限界

#### **レイヤー2: 人間文法ロジック**
- **役割**: NLP解析の曖昧性を文脈・位置・後続語で解決
- **核心技術**: パターンマッチング + 文法的推論
- **Rephraseの利点**: 3重入れ子なしで複雑度大幅軽減

### **🎯 段階別精度目標**

#### **Phase 2-5: 基本文法完全対応 (45.3% → 75%)**
```
現在の弱点を集中攻略:
• M1/M2副詞配置精度向上: 62.5% → 85%
• 接続詞・前置詞句の適切な分類
• 複合時制の正確な認識
• 不定詞・動名詞の文脈判断
```

#### **Phase 6-10: 曖昧性解決システム (75% → 90%)**
```
人間文法ロジック本格導入:
• Flying planes問題: 後続語分析で解決
• 動名詞vs現在分詞: 文中位置で判断
• 関係節省略: 文脈パターンで補完
• 比較級・最上級: 構造的特徴抽出
```

#### **Phase 11-15: エッジケース特化 (90% → 95%)**
```
残り5%の難解ケース:
• 慣用表現・固定句の辞書ベース処理
• 口語・省略形の正規化
• 倒置・強調構文の変換
• セマンティック妥当性チェック
```

### **🔧 ハイブリッド文法解析戦略**

#### **NLP + 人間文法ロジック統合システム**
```python
class HybridGrammarEngine:
    """NLPエンジンと人間文法ロジックを統合した解析システム"""
    
    def __init__(self):
        self.nlp_engines = {
            'stanza': StanzaPipeline(),
            'spacy': SpacyPipeline()
        }
        self.grammar_logic = StructuralGrammarAnalyzer()
        self.confidence_evaluator = ConfidenceBasedSelector()
    
    def analyze_with_verification(self, sentence):
        """NLP結果を文法ロジックで検証・修正"""
        
        # Step 1: NLP基本解析
        nlp_result = self.nlp_engines['stanza'].analyze(sentence)
        
        # Step 2: 構造的検証
        verification_result = self.grammar_logic.verify_structure(nlp_result)
        
        # Step 3: 信頼度評価による最終判定
        if verification_result.confidence > 0.8:
            return verification_result.corrected_result
        else:
            return self.hybrid_resolution(nlp_result, verification_result)
    
    def identify_problematic_patterns(self, sentence):
        """NLPが苦手とするパターンを事前検出"""
        patterns = [
            self._detect_relative_clause_complexity(sentence),
            self._detect_compound_subject_ambiguity(sentence),
            self._detect_modifier_attachment_issues(sentence)
        ]
        return [p for p in patterns if p.requires_correction]
```

#### **Stanza/spaCy誤判定対処の設計方針**

**⚠️ 重要**: 以下は具体的な実装コードではなく、Stanza/spaCyの誤判定に対処する際の**設計思想と方法論**を示したものです。

##### **基本的なアプローチ**
1. **依存関係に頼らない汎用ルール**: Stanza/spaCyの依存解析結果が間違っている場合、文法的位置関係に基づく汎用ルールで補正
2. **人間の文法認識プロセスの実装**: 人間が文法パターンで英語を理解する認知プロセスをコード化。統計的判定ではなく、文法的パターン認識による判定
3. **汎用的文法パターン検出**: 正規表現による安易なハードコーディングではなく、構造的パターン認識による汎用的実装

##### **人間文法認識の具体例**
- **受動態判定**: "be + 過去分詞" パターン → 人間は無意識に受動態と認識 → `unexpected`は動詞
- **分詞構文判定**: "Working overtime, the team completed..." → 人間は後続の本動詞`completed`を見て`Working`を副詞的分詞構文と認識
- **動名詞判定**: "Swimming is fun" → 人間は文構造から`Swimming`を主語の動名詞と認識

##### **具体的な対処パターン例**

**パターン1: 副詞の修飾先誤判定**
- **問題**: "badly damaged" → Stanzaが"badly"を主文動詞の修飾と誤判定
- **対処法**: 関係詞節境界を文字列パターンで判定し、位置ベースで正しいスロットに配置
- **実装方針**: 依存関係ではなく、文中の相対位置と文法パターンで判定

**パターン2: 受動態での補語誤検出**
- **問題**: "was unexpected" → システムがV:"unexpected" + C1:"unexpected"と重複出力
- **対処法**: 受動態パターン検出時は補語スロットを生成しないルール
- **実装方針**: be動詞 + 過去分詞パターンの明示的判定

**パターン3: 分詞構文のスロット誤配置**
- **問題**: "documents being reviewed" → サブスロット構造の誤解析
- **対処法**: 分詞パターンの文法的解析による正しいスロット構造生成
- **実装方針**: 分詞の種類（現在分詞/過去分詞）による構造決定ルール

##### **実装時の指針**
```python
# ❌ 避けるべき複雑な実装例
def complex_structural_analysis():
    # 複雑な距離計算、信頼度ベース判定、機械学習的アプローチ
    pass

# ✅ 推奨する明確な実装例  
def simple_grammar_rule():
    # 明確な文法パターンマッチング
    # 理解しやすいif-else文での判定
    # 人間が読んで理解できるロジック
    pass
```

この方針に基づき、残り3ケースの問題を個別に解決していく。

#### **動的パターン学習システム**
```python
class AdaptivePatternLearner:
    """失敗ケースから学習する自己改善システム"""
    
    def __init__(self):
        self.error_patterns = ErrorPatternDatabase()
        self.correction_strategies = CorrectionStrategyLibrary()
    
    def learn_from_test_failures(self, test_results):
        """テスト結果から新しいパターンを学習"""
        
        for failure in test_results.failures:
            # パターン抽出
            error_pattern = self._extract_error_pattern(
                failure.sentence, 
                failure.system_output, 
                failure.expected_output
            )
            
            # 修正戦略の導出
            correction_strategy = self._derive_correction_strategy(error_pattern)
            
            # パターンライブラリに追加
            self.correction_strategies.add_strategy(
                pattern=error_pattern,
                strategy=correction_strategy,
                confidence=self._calculate_pattern_confidence(error_pattern)
            )
    
    def apply_learned_corrections(self, sentence, nlp_result):
        """学習した修正戦略を適用"""
        
        applicable_strategies = self.correction_strategies.find_applicable(sentence)
        
        for strategy in applicable_strategies:
            if strategy.confidence > 0.75:
                nlp_result = strategy.apply_correction(nlp_result)
        
        return nlp_result
```
##### **判定優先順位の設計方針**

Stanza/spaCyと独自文法ルールが競合する場合の判定順序：

1. **明確な文法パターン優先**: 受動態、関係詞節など明確なパターンは独自ルール適用
2. **超シンプルルール適用**: 修飾語配置は個数ベースルール優先
3. **Rephraseルール遵守**: 全単語スロット配置、サブスロット時上位空化ルール
4. **NLP結果補完**: 上記で解決できない部分のみStanza/spaCy結果使用

##### **エラーパターン対処方針**

**よくある誤判定パターンと対処指針**:

- `relative_clause_modifier_leak`: 関係詞節内の修飾語が主文に流出 → 節境界判定ルール
- `passive_voice_complement_duplication`: 受動態での補語重複 → 受動態パターン検出
- `participle_structure_misparse`: 分詞構文の誤解析 → 分詞パターン特定ルール
- `modal_auxiliary_confusion`: 助動詞の誤分類 → 助動詞リスト照合

これらの対処は、複雑なアルゴリズムではなく「人間が読んで理解できる明確なif-else文」で実装する。
        "correction_strategy": "structural_main_verb_identification",
        "examples": [
            "The man whose car is red lives here.",
            "The book which was written yesterday arrived."
        ],
        "success_rate": 0.92
    },
    
    "compound_subject_verb_attachment": {
        "description": "複合主語での動詞付け先曖昧性",
        "detection_logic": lambda s: detect_compound_subject_pattern(s),
        "correction_strategy": "subject_boundary_analysis", 
        "examples": [
            "Flying planes can be dangerous.",
            "The students working hard succeed."
        ],
        "success_rate": 0.87
    },
    
    "modifier_scope_ambiguity": {
        "description": "修飾語のスコープ曖昧性",
        "detection_logic": lambda s: detect_modifier_ambiguity(s),
        "correction_strategy": "distance_based_attachment",
        "examples": [
            "I saw the man with binoculars.",
            "She works carefully at home daily."
        ],
        "success_rate": 0.84
    }
}
```

---

### **🎯 100%完成への最終段階**

#### **現在の状況 (2025年8月19日)**
- **達成済み精度**: 94.3% (50/53)
- **残り課題**: 3ケースのシステム修正のみ
- **実装完了度**: 95%以上

#### **最終修正対象**
1. **Test 40**: 関係詞節内副詞の主文流出 → 節境界判定ルール追加
2. **Test 42**: 受動態での補語重複出力 → 受動態パターン修正
3. **Test 52**: 分詞構文スロット誤配置 → 分詞構文ルール調整

#### **100%達成後の運用計画**
- **品質保証**: 53例文標準テストでの継続的精度確認
- **新規パターン**: 追加例文での精度維持確認
- **商用展開**: 本番環境での性能モニタリング

---

### **🔄 現在の開発サイクル**

```
簡潔な改善プロセス:
1. 特定問題の分析 → 原因特定
2. 最小限の修正実装 → 超シンプルルール準拠
3. 標準テストでの検証 → 精度確認
4. 副作用の確認 → 他ケースへの影響チェック
5. 次の問題へ移行
```

### **📊 超シンプルルールアプローチの成果**

- **明確性**: 複雑なアルゴリズム不要、理解しやすいルール
- **精度**: 67.9% → 94.3%の大幅改善
- **保守性**: 人間が読んで理解できるコード
- **拡張性**: 新しいパターンへの対応が容易
- **実用性**: 段階的改善で確実な精度向上を実現
  - エラーケース分析・対策

#### **Phase 11-15: 完成度向上**
- **期間**: 6-8週間
- **目標精度**: 90% → 95%
- **実装内容**:
  - 残存エッジケース特化対策
  - パフォーマンス最適化
  - 包括的テストスイート
  - 商用レベル品質保証

### **🔄 継続改善サイクル**

```
各フェーズで実行:
1. 新ハンドラー実装
2. バッチテストによる精度測定
3. 失敗ケース分析・パターン抽出  
4. 文脈判断ロジック強化
5. 回帰テスト・品質確認
6. 次フェーズ計画調整
```

### **📊 成功要因**

- **基盤の堅牢性**: 現在のプラグイン型アーキテクチャが優秀
- **測定可能性**: CLIバッチ処理による定量的評価システム
- **Rephraseの制約**: 3重入れ子なしで複雑度管理可能
- **ハイブリッド手法**: NLP + 人間文法ロジックの相乗効果

---

## 🚀 **拡張計画**

### **Phase 5: 助動詞ハンドラー**
- **優先度**: 高
- **対象**: will, can, must, should, may, might等
- **期待効果**: 未来形、可能性表現の完全対応

### **Phase 6: 時制ハンドラー**
- **優先度**: 高
- **対象**: have/has/had + 過去分詞、be + ~ing
- **期待効果**: 完了形、進行形の完全対応

### **Phase 7: 準動詞ハンドラー**
- **優先度**: 中
- **対象**: to不定詞、動名詞、分詞構文
- **期待効果**: 複雑な準動詞構造への対応

---

## 🛡️ **運用・保守**

### **品質保証**
- **テスト駆動**: 正解想定チェックによる継続的品質確認
- **段階的拡張**: 1ハンドラーずつの慎重な機能追加
- **後方互換**: 既存ハンドラーへの影響最小化

### **パフォーマンス**
- **並行処理**: 全ハンドラー同時実行による高速化
- **キャッシュ**: Stanza解析結果の再利用
- **最適化**: spaCyハイブリッドの選択的使用

### **デバッグ・監視**
- **詳細ログ**: ハンドラー個別の成功・失敗追跡
- **統計情報**: 処理時間、成功率の継続的監視
- **エラー処理**: 個別ハンドラー失敗時の全体影響回避

---

## �️ **CLIインターフェース使用方法**

### **基本コマンド構文**

```bash
# 基本的な一括処理
python unified_stanza_rephrase_mapper.py --input [入力ファイル] --output [出力ファイル]

# 出力ファイル省略（自動生成）
python unified_stanza_rephrase_mapper.py --input [入力ファイル]

# テストモード（従来のPhase 0-2実行）
python unified_stanza_rephrase_mapper.py --test-mode

# ヘルプ表示
python unified_stanza_rephrase_mapper.py --help
```

### **結果分析コマンド**

```bash
# 基本的な精度分析
python compare_results.py --results [結果ファイル]

# 詳細分析（失敗ケース表示）
python compare_results.py --results [結果ファイル] --detail

# 分析レポート保存
python compare_results.py --results [結果ファイル] --save-report [レポートファイル]
```

### **入力データ形式**

#### **詳細形式（期待値付き）**
```json
{
  "meta": {
    "total_count": 5,
    "description": "カスタム例文テスト"
  },
  "data": {
    "1": {
      "sentence": "She works carefully.",
      "expected": {
        "main_slots": {
          "S": "She",
          "V": "works",
          "M2": "carefully"
        },
        "sub_slots": {}
      }
    },
    "2": {
      "sentence": "The book is interesting.",
      "expected": {
        "main_slots": {
          "S": "The book",
          "V": "is",
          "C1": "interesting"
        },
        "sub_slots": {}
      }
    }
  }
}
```

#### **シンプル形式（期待値なし）**
```json
[
  "She works carefully.",
  "The book is interesting.", 
  "I give him a book.",
  "He has finished his homework.",
  "The letter was written by John."
]
```

### **実用的な使用例**

#### **例1: 既存の53例文テストセットを使用**
```bash
# 53例文一括処理
cd training/data
python unified_stanza_rephrase_mapper.py --input final_test_system/final_54_test_data.json

# 結果確認
python compare_results.py --results batch_results_[タイムスタンプ].json
```

#### **例2: カスタム例文テスト**
```bash
# カスタム例文ファイル作成（上記JSON形式）
# my_test_sentences.json

# 処理実行
python unified_stanza_rephrase_mapper.py --input my_test_sentences.json --output my_results.json

# 結果分析
python compare_results.py --results my_results.json --detail
```

#### **例3: 簡単な文法チェック**
```bash
# シンプルな例文リスト作成
# simple_sentences.json: ["She works carefully.", "The book is red."]

# 処理実行
python unified_stanza_rephrase_mapper.py --input simple_sentences.json

# 結果確認（期待値なしのため、分析結果のみ）
python compare_results.py --results batch_results_[タイムスタンプ].json
```

### **出力ファイル構造**

#### **バッチ処理結果ファイル**
```json
{
  "meta": {
    "input_file": "my_test_sentences.json",
    "processed_at": "2025-08-17T14:50:00.000000",
    "total_sentences": 5,
    "success_count": 5,
    "error_count": 0
  },
  "results": {
    "1": {
      "sentence": "She works carefully.",
      "analysis_result": {
        "sentence": "She works carefully.",
        "slots": {
          "S": "She",
          "V": "works",
          "M2": "carefully"
        },
        "sub_slots": {},
        "grammar_info": {
          "detected_patterns": ["basic_five_pattern"],
          "handler_contributions": {...}
        },
        "meta": {
          "processing_time": 0.129,
          "sentence_id": 1,
          "active_handlers": 5
        }
      },
      "expected": {...},
      "status": "success"
    }
  }
}
```

#### **精度分析レポート**
```
📊 精度分析レポート
============================================================
📁 対象ファイル: my_results.json
⏰ 分析時刻: 2025-08-17T14:50:10.616823

📈 全体統計:
   総ケース数: 5
   完全一致: 5
   部分一致: 0
   失敗: 0
   🎯 完全一致率: 100.0%

🔍 スロット別精度:
   S: 100.0% (5/5)
   V: 100.0% (5/5)
   M2: 100.0% (1/1)
   O1: 100.0% (2/2)
   Aux: 100.0% (2/2)
```

### **実証済みパフォーマンス**

| テストセット | 完全一致率 | 処理成功率 | 主要スロット精度 |
|------------|------------|------------|----------------|
| カスタム5例文 | 100.0% | 100.0% | S:100%, V:100%, M2:100% |
| 標準53例文 | 45.3% | 100.0% | S:88.7%, V:96.2%, C1:95.2% |

### **開発・デバッグ用途**

```bash
# 詳細ログ出力で実行
python unified_stanza_rephrase_mapper.py --input test.json 2>&1 | tee debug.log

# 特定例文のみテスト
echo '["She works carefully."]' > quick_test.json
python unified_stanza_rephrase_mapper.py --input quick_test.json

# 従来のテストモードとの比較
python unified_stanza_rephrase_mapper.py --test-mode
```

---

---

## 🚀 **次期開発計画 (v2.0系 段階的ハイブリッド戦略)**

### **📋 4大開発課題と段階的実装工程**

**基本方針**: 段階的ハイブリッド戦略
- **アーキテクチャ**: プラグイン型協調システム完全維持
- **内部実装**: 各ハンドラーをStanza依存から人間文法認識へ段階移行
- **品質保証**: 100%精度維持しながら安全な移行

**実装優先順位**: 
- Phase 2.0: ハンドラー内部実装移行 + 基盤システム強化
- Phase 2.1: 位置システム実装  
- Phase 2.2: 新ハンドラー追加（人間文法認識で実装）

---

### **🔧 Phase 2.0: ハンドラー内部移行 + 基盤強化 (v2.0-v2.1)**

#### **課題⓪: ハンドラー内部実装の段階的移行 (新規追加)**
**目標期間**: 2025年8月22日-29日  
**実装範囲**: 既存ハンドラーの内部実装を段階的ラッパー方式で移行

**⚠️ 重要原則**: 既存100%精度システムの完全保護

**技術仕様**:
```python
# 段階的ラッパー方式（最小リスク移行）
class RiskManagedHybridHandler:
    def __init__(self):
        # 既存実装の完全バックアップ
        self.stanza_backup = self._backup_original_implementation()
        
        # 段階的移行管理
        self.migration_status = {
            'whose_clause': 'COMPLETED',       # ✅ 実装済み（成功実績）
            'basic_svo_simple': 'PLANNED',     # 🔄 次の移行対象
            'basic_svo_complex': 'FUTURE',     # 🔄 その後
            'passive_simple': 'FUTURE',        # 🔄 最後
        }
        
        # 品質保証設定
        self.quality_gate_enabled = True
        self.immediate_fallback = True
        self.backup_restoration_tested = True
    
    def process_with_quality_protection(self, sentence):
        """100%精度保護付き処理"""
        
        # 1. 人間文法認識試行
        if self._can_attempt_human_processing(sentence):
            try:
                human_result = self._attempt_human_processing(sentence)
                
                # 2. 結果検証（厳格）
                if self._validate_result_quality(human_result, sentence):
                    return human_result
                
            except Exception as e:
                # 3. 例外時の即座復旧
                self._log_fallback_incident(sentence, e)
        
        # 4. 既存Stanza処理（完全無改変）
        return self.stanza_backup.process(sentence)
    
    def _validate_result_quality(self, result, sentence):
        """厳格な品質検証"""
        
        # 基本構造チェック
        if not self._validate_slot_structure(result):
            return False
        
        # 既知正解との照合
        if sentence in self.known_correct_results:
            return result == self.known_correct_results[sentence]
        
        # 文法的妥当性チェック
        return self._validate_grammatical_consistency(result)
```

**段階的移行スケジュール**:

**8/22-23: 安全基盤構築**
```python
# リスク0の準備作業
1. バックアップシステム構築
2. 品質検証システム準備  
3. フォールバック機構テスト
4. 復旧手順確認

# 成功基準: システム動作継続、全テストパス維持
```

**8/24-25: 最小リスク移行実験**
```python
# 最も安全なパターンから開始
target_pattern = 'basic_svo_simple'
target_sentences = ['I love you.', 'She works hard.']

# 限定的実装・テスト
implement_minimal_human_pattern(target_pattern)
test_only_target_sentences(target_sentences)

# 成功基準: 対象例文100%正確、全体品質維持
```

**8/26-27: 品質検証・判定**
```python
# 厳格な品質保証
full_test_results = run_complete_test_suite()
performance_check = measure_system_performance()

if full_test_results.success_rate == 100%:
    approve_pattern_migration()
    plan_next_migration()
else:
    immediate_rollback_to_stanza()
    analyze_failure_causes()
```

**移行対象ハンドラー（優先順位付き）**:
- � **LOW RISK**: basic_five_pattern simple patterns (SVO基本形)
- � **MEDIUM RISK**: relative_clause remaining patterns (which, that)  
- � **HIGH RISK**: passive_voice structural recognition (受動態構造認識)

**品質保証システム**:
```python
class QualityAssuranceSystem:
    def __init__(self):
        self.original_test_results = self._backup_current_100percent_results()
        self.rollback_capability = self._verify_rollback_system()
    
    def migration_quality_gate(self, migration_name):
        """各移行の厳格な品質チェック"""
        
        # チェック1: 完全テストスイート
        current_results = run_all_54_test_cases()
        if current_results.success_rate < 100%:
            return self._reject_migration("Quality degraded")
        
        # チェック2: パフォーマンス確認
        perf_check = measure_processing_speed()
        if perf_check.degradation > 15%:
            return self._reject_migration("Performance degraded")
        
        # チェック3: システム整合性
        integrity_check = verify_system_integrity()
        if not integrity_check.passed:
            return self._reject_migration("System integrity compromised")
        
        return self._approve_migration()
```

#### **課題②: ハンドラー間情報伝達システム全面拡充**
**目標期間**: 2025年8月26日-29日  
**実装範囲**: 全ハンドラー間での句・節情報の統一プロトコル化

**技術仕様**:
```python
# 統一情報交換プロトコル（アーキテクチャ維持）
class HandlerProtocol:
    def declare_phrase_clause_info(self, context) -> HandlerInfo:
        """句・節情報の宣言（既存shared_context拡張）"""
        return {
            'element_type': 'phrase' | 'clause',
            'target_slots': ['S', 'O1', 'M2'],
            'processing_priority': int,
            'dependency_handlers': ['relative_clause']
        }
```

**実装対象ハンドラー**:
- ✅ relative_clause → basic_five_pattern (実装済み)
- 🔄 participle_construction → passive_voice  
- 🔄 noun_clause → basic_five_pattern (新規)
- 🔄 auxiliary_complex → basic_five_pattern
- 🔄 adverbial_modifier → 全ハンドラー

#### **課題①: 上位サブ連結汎用システム全面適用**  
**目標期間**: 2025年8月26日-29日  
**実装範囲**: 全ハンドラーでの位置情報統一管理

**技術仕様**:
```python
# 汎用上位サブ連結システム
class UniversalSlotPositionSystem:
    def __init__(self):
        self.slot_positions = {}  # {sub_slot: main_slot}
        self.position_metadata = {}  # 位置決定の根拠情報
    
    def register_sub_slot_position(self, sub_slot, main_position, rationale):
        """サブスロットの位置登録"""
        self.slot_positions[sub_slot] = main_position
        self.position_metadata[sub_slot] = {
            'handler': rationale.handler_name,
            'grammatical_role': rationale.deprel,
            'confidence': rationale.confidence
        }
    
    def apply_position_based_emptying(self, slots, sub_slots):
        """位置情報に基づく上位スロット空化"""
        for sub_slot, main_pos in self.slot_positions.items():
            if sub_slot in sub_slots and main_pos in slots:
                slots[main_pos] = ''
        return slots
```

**実装対象ハンドラー**:
- ✅ relative_clause (実装済み: sub-s→S, sub-aux→S, sub-v→S)
- 🔄 participle_construction (sub-v→S, sub-m2→S)  
- 🆕 noun_clause (sub-s→S/O1, sub-v→内部, sub-o1→内部)
- 🆕 adverbial_clause (sub-m2→M1/M2/M3)
- 🔄 passive_voice (位置情報考慮)
- 🔄 auxiliary_complex (sub-aux位置情報)

---

### **📍 Phase 2.1: 位置システム実装 (v2.2-v2.3)**

#### **課題③: orderシステム導入**
**目標期間**: 2025年8月30日-9月2日  
**実装範囲**: 全スロットの語順データ付与

**技術仕様**:
```python
# 語順情報付きスロットシステム
class OrderedSlotSystem:
    def __init__(self):
        self.slot_orders = {}  # スロット名 → 語順番号
        self.sub_slot_orders = {}  # サブスロット名 → 語順番号
    
    def analyze_word_order(self, sentence_tokens):
        """文中の語順を分析してスロットに番号付与"""
        order_mapping = {}
        
        # 例: "Yesterday I worked quickly"
        # → M1_1:"yesterday", S_2:"I", V_3:"worked", M2_4:"quickly"
        
        for i, token in enumerate(sentence_tokens, 1):
            slot_assignment = self._determine_slot_assignment(token)
            if slot_assignment:
                order_mapping[f"{slot_assignment}_{i}"] = token.text
        
        return order_mapping
    
    def generate_ordered_output(self, slots, sub_slots):
        """語順情報付き出力の生成"""
        ordered_slots = {}
        
        # メインスロット語順付与
        for slot_name, content in slots.items():
            order_num = self._get_word_position(content)
            ordered_slots[f"{slot_name}_{order_num}"] = content
        
        # サブスロット語順付与  
        for sub_slot, content in sub_slots.items():
            parent_slot = self._get_parent_slot(sub_slot)
            sub_order = self._get_sub_word_position(content, parent_slot)
            ordered_slots[f"{parent_slot}-{sub_slot}_{sub_order}"] = content
        
        return ordered_slots
```

**実装内容**:
1. **メインスロット語順**: M1_1, S_2, Aux_3, V_4, O1_5, M2_6
2. **サブスロット語順**: S-sub-s_1, S-sub-v_2, S-sub-o1_3  
3. **出力形式制御**: 設定による表示ON/OFF
4. **UI連携**: フロントエンドでの語順表示対応

---

### **🆕 Phase 2.2: 新ハンドラー追加 (v2.4-v2.6)**

#### **課題④: 人間文法認識ベース新ハンドラー実装**
**目標期間**: 2025年9月3日-15日  
**実装範囲**: 新ハンドラー5種類を最初から人間文法認識で実装

**実装方針**: 
- **全て人間文法認識で実装**: Stanza依存なしの純粋ルールベース
- **プラグイン型協調**: 既存アーキテクチャに完全統合
- **段階的追加**: 各ハンドラーを個別にテストして品質確保

**新規ハンドラー一覧**:

**1. noun_clause (名詞節) - v2.4**
```python
def _handle_noun_clause(self, sentence, result):
    """名詞節処理: 人間文法認識ベース"""
    
    # 1. 構造パターン認識
    if self._detect_that_clause(sentence):
        return self._process_that_clause_structure(sentence)
    elif self._detect_what_clause(sentence):
        return self._process_what_clause_structure(sentence)
    
    # 対応例文: "I know that he is kind."
    # 人間文法認識: that句は名詞節 → O1位置を占有
    # → S:I, V:know, O1:"", sub-s:he, sub-v:is, sub-c1:kind
```

**2. adverbial_clause (副詞節) - v2.4**  
```python
def _handle_adverbial_clause(self, sentence, result):
    """副詞節処理: 人間文法認識ベース"""
    
    # 1. 副詞節マーカー検出
    adv_markers = ['when', 'where', 'because', 'if', 'while', 'since']
    detected_marker = self._find_adverbial_marker(sentence, adv_markers)
    
    # 2. 構造的分析
    if detected_marker:
        return self._process_adverbial_structure(sentence, detected_marker)
    
    # 対応例文: "I study when I have time."
    # 人間文法認識: when句は時間副詞 → M2位置を占有
    # → S:I, V:study, M2:"", sub-s:I, sub-v:have, sub-o1:time
```

**3. infinitive_construction (不定詞構文) - v2.5**
```python  
def _handle_infinitive_construction(self, sentence, result):
    """不定詞処理: 人間文法認識ベース"""
    
    # 1. to + 動詞原形パターン検出
    infinitive_pattern = self._detect_to_infinitive(sentence)
    
    # 2. 用法判定（名詞的・形容詞的・副詞的）
    usage_type = self._determine_infinitive_usage(sentence, infinitive_pattern)
    
    # 3. 構造的処理
    return self._process_infinitive_structure(sentence, usage_type)
    
    # 対応例文: "I want to study English."
    # 人間文法認識: to study = 名詞的用法（目的語）
    # → S:I, V:want, O1:"", sub-v:study, sub-o1:English
```

**4. gerund_construction (動名詞構文) - v2.5**
```python
def _handle_gerund_construction(self, sentence, result):  
    """動名詞処理: 人間文法認識ベース"""
    
    # 1. -ing形の名詞的用法検出
    gerund_pattern = self._detect_gerund_usage(sentence)
    
    # 2. 文法的役割判定（主語・目的語・補語）
    grammatical_role = self._determine_gerund_role(sentence, gerund_pattern)
    
    # 3. 構造的処理
    return self._process_gerund_structure(sentence, grammatical_role)
    
    # 対応例文: "Swimming is fun."
    # 人間文法認識: Swimming = 動名詞主語
    # → S:"", V:is, C1:fun, sub-v:Swimming
```

**5. comparative_construction (比較構文) - v2.6**
```python
def _handle_comparative_construction(self, sentence, result):
    """比較級・最上級処理"""
    # 対応例文: "She is taller than me."
    # → S:She, V:is, C1:taller, M2:"than me"
    pass
```

---

### **📊 段階的ハイブリッド実装マイルストーン**

| Phase | バージョン | 期間 | 主要機能 | 対応例文数目標 | 人間文法認識率 |
|-------|-----------|------|----------|--------------|---------------|
| 2.0 | v2.0 | 8/22-25 | 既存ハンドラー内部移行 | 54→65 | 30%→50% |
| 2.0 | v2.1 | 8/26-29 | ハンドラー間情報伝達統一 | 65→75 | 50%→60% |  
| 2.1 | v2.2 | 8/30-9/2 | order系統実装 | 75→75 | 60%→60% |
| 2.2 | v2.4 | 9/3-6 | 名詞節・副詞節(人間文法) | 75→95 | 60%→75% |
| 2.2 | v2.5 | 9/7-11 | 不定詞・動名詞(人間文法) | 95→120 | 75%→85% |
| 2.2 | v2.6 | 9/12-15 | 比較構文(人間文法) | 120→150 | 85%→90% |

**最終目標**: 
- **v2.6で150例文対応、完全精度100%維持**
- **人間文法認識率90%以上（Stanzaフォールバック10%以下）**

**ハンドラー移行スケジュール**:
```
v2.0: basic_five_pattern主要パターン移行
v2.1: relative_clause残りパターン移行  
v2.2: passive_voice構造認識化
v2.4+: 新ハンドラーは全て人間文法認識で実装
```

---

## 🎯 **次期開発計画 (v1.4予定)**

### **副詞ハンドラー精密化**
- **関係副詞配置ルール修正**: sub-m1 → sub-m2 の適切な配置
- **副詞重複処理改善**: M1とM2の重複防止システム
- **目標精度**: 77.4% → 85% (残る12例文のエラー解決)

### **追加ハンドラー実装**
- **不定詞構文**: to + 動詞原形の処理
- **動名詞構文**: -ing形の名詞的用法
- **比較構文**: 比較級・最上級の処理

---

## 🚀 **今後の実装予定 (Phase 4: 位置情報表示システム)**

### **📍 上位サブ連結位置情報表示機能**

**実装予定**: v1.4 (2025年8月下旬)  
**実装ステータス**: 📋 設計段階

#### **実装背景**
- **現在の状況**: 位置情報システムは関係節ハンドラーのみに実装済み
- **内部処理**: `slot_positions`で位置情報を記録・管理中
- **出力制限**: 位置情報は内部制御用のみ、ユーザー向け表示なし

#### **実装計画**

**Phase 1: 全ハンドラーへの位置情報システム拡張**
```python
# 拡張対象ハンドラー
✅ relative_clause        # 実装済み (sub-s:S, sub-aux:S, sub-v:S)
🔄 participle_construction # 拡張予定
🔄 noun_clause            # 新規実装予定  
🔄 adverbial_clause       # 新規実装予定
🔄 passive_voice          # 位置情報対応予定
🔄 auxiliary_complex      # 位置情報対応予定
```

**Phase 2: 位置情報付き出力フォーマット設計**
```python
# 従来フォーマット
'sub_slots': {
    'sub-s': 'The artist whose paintings',
    'sub-aux': 'were', 
    'sub-v': 'exhibited'
}

# 新フォーマット (位置情報付き)
'sub_slots': {
    'sub-s:S': 'The artist whose paintings',    # S位置の従属節
    'sub-aux:S': 'were',                        # S位置の助動詞
    'sub-v:S': 'exhibited',                     # S位置の動詞
    'sub-m2:O1': 'quickly'                      # O1位置の修飾語
}
```

**Phase 3: UI表示機能対応**
```html
<!-- 位置情報ベース表示 -->
<div class="slot-position-s">
    <span class="sub-slot">sub-s:S</span>
    <span class="content">The artist whose paintings</span>
</div>
```

#### **技術仕様**

**位置特定アルゴリズム**
```python
def _determine_element_position(self, sentence, element):
    """要素の位置を文法的役割から特定"""
    if element.deprel in ['nsubj', 'nsubj:pass']:
        return 'S'
    elif element.deprel in ['obj', 'dobj']:
        return 'O1'
    elif element.deprel in ['iobj']:
        return 'O2'
    elif element.deprel in ['xcomp', 'ccomp']:
        return 'C1'
    # 継続実装...
```

**出力形式制御**
```python
# 設定による出力制御
output_format = {
    'show_position_info': True,     # 位置情報表示ON/OFF
    'position_delimiter': ':',      # 区切り文字
    'legacy_compatibility': False   # 従来形式との互換性
}
```

#### **実装優先度**
1. **高**: 関係節以外のハンドラーへの位置情報システム拡張
2. **中**: 出力フォーマット変更とUI対応
3. **低**: 設定による表示制御機能

---

**実装完了確認**: 2025年8月21日時点で、人間文法認識システムの実装が成功し、54例文全てで100%精度を達成しました。これにより基盤システムが確立され、次期v2.0系開発の準備が整いました。

### **v1.4 (2025年8月21日)**
- 🏆 **100%精度達成** (54/54例文完全一致)
- 人間文法認識システム実装完了
- "The man whose car is red lives here"のStanza誤認識問題解決
- whose構文での動詞修正パターン実装
- ハイブリッド修正システム(文書→文レベル情報伝達)完成
- **Phase 2.0系開発工程策定完了**

### **v1.3 (2025年8月21日)**
- Phase1/test-mode機能削除完了
- 94.3%精度達成 (50/53完全一致)
- エラーケース特定: Cases 13,14,52
- 位置情報表示システム設計策定

### **v1.2 (2025年8月20日)**
- 上位サブ連結汎用システム実装完了
- 分詞構文保護システム強化
- 77.4%精度達成

### **v1.1 (2025年8月17日)**
- CLIインターフェース実装完了
- バッチ処理機能追加
- 結果照合システム分離
- 53例文一括処理対応
- カスタム例文テスト機能

### **v1.0 (2025年8月16日)**
- 初版リリース
- 4ハンドラー実装完了
- 54例文対応版構築
- プラグイン型同時処理方式確立

---

**次期更新予定**: v2.0 (ハンドラー間情報伝達システム統一実装版)

---

## **Phase 2.0 実装開始の判断基準**

### **実装開始の前提条件**

**絶対条件（これらが満たされない限り実装開始しない）**:
1. ✅ **100%精度の完全実現**: 現在54例文で100%精度達成済み
2. ✅ **システム安定性確認**: 長期間安定動作実績あり
3. 🔄 **完全バックアップシステム**: 即座復旧機能の動作確認必要
4. 🔄 **リスク管理体制**: 緊急時対応プロトコルの整備必要

### **実装可否判定フローチャート**

```python
def assess_implementation_readiness():
    """Phase 2.0実装可否の総合判定"""
    
    # ステップ1: 基盤技術の準備状況確認
    foundation_ready = check_foundation_readiness()
    if not foundation_ready.perfect():
        return postpone_implementation("Foundation not ready", foundation_ready.gaps)
    
    # ステップ2: リスク管理体制の完成度確認  
    risk_management_ready = verify_risk_management_systems()
    if not risk_management_ready.operational():
        return postpone_implementation("Risk management incomplete", risk_management_ready.issues)
    
    # ステップ3: チーム準備・リソース確認
    team_ready = assess_team_and_resources()
    if not team_ready.sufficient():
        return postpone_implementation("Insufficient resources", team_ready.limitations)
    
    # ステップ4: 最終総合判定
    return make_final_go_no_go_decision()

def check_foundation_readiness():
    """技術基盤の準備状況評価"""
    checklist = {
        "backup_system": verify_complete_backup_capability(),
        "rollback_mechanism": test_immediate_rollback_function(),
        "monitoring_system": validate_continuous_monitoring(),
        "quality_gates": verify_quality_assurance_gates(),
        "emergency_protocols": test_emergency_response_procedures()
    }
    
    return FoundationReadiness(
        perfect=all(checklist.values()),
        gaps=[key for key, value in checklist.items() if not value]
    )
```

### **現在の準備状況評価**

**✅ 完了済み項目**:
- UnifiedStanzaRephraseMapper v1.4: 100%精度実現
- 詳細設計仕様書: ハイブリッド移行戦略文書化
- 技術的実現可能性: whose構文実装で実証済み

**🔄 準備中・要確認項目**:
- 完全バックアップシステムの実装・テスト
- 緊急時復旧プロトコルの動作確認
- 継続的品質監視システムの構築
- エラーハンドリング機構の実装

**❌ 未着手項目**:
- 実際のラッパーシステム実装
- 段階的移行テスト環境構築
- 長時間運用での安定性実証

### **実装開始推奨タイミング**

**即座開始可能シナリオ**:
```python
immediate_start_conditions = {
    "confidence_level": "HIGH",
    "prerequisites": [
        "バックアップシステム1日で実装可能",
        "品質監視機構既存技術で構築可能", 
        "リスク最小化戦略確立済み"
    ],
    "timeline": "8/22開始、8/29までPhase 0完了"
}
```

**準備期間必要シナリオ**:
```python
preparation_needed_scenario = {
    "confidence_level": "MEDIUM",
    "additional_prep_time": "3-5日間",
    "focus_areas": [
        "バックアップシステム実装・テスト",
        "品質監視システム構築",
        "緊急時対応手順の実証"
    ],
    "revised_timeline": "8/25開始、9/1までPhase 0完了"
}
```

### **推奨実装判定**

**現在の総合評価**: **🟡 READY WITH PREPARATION**

**判定理由**:
- ✅ **技術的実現可能性**: 実証済み（whose構文成功）
- ✅ **設計完成度**: 詳細戦略文書化済み  
- ✅ **リスク管理戦略**: 包括的プロトコル設計済み
- 🔄 **実装基盤**: 2-3日で準備完了可能
- 🔄 **安全保証システム**: 構築・テスト必要

**推奨アクション**:
1. **即座開始**: 安全基盤構築作業（8/22-23）
2. **並行準備**: バックアップ・監視システム実装
3. **慎重実験**: 8/24-25の最小リスク移行実験
4. **結果判定**: 8/26-27の包括的評価

**最終判断**: 
```
Phase 2.0ハンドラー内部移行は技術的に実現可能であり、
適切なリスク管理下での実装開始を推奨する。

開始条件: 安全基盤構築の完了
開始時期: 準備完了次第（最早8/22、遅くとも8/25）
成功確度: 中～高（適切な準備とリスク管理による）
```

---

## 🔢 **Order機能統合設計** *(2025年8月22日追加)*

### **設計思想: 段階的Order機能統合戦略**

```
🎯 Order機能の核心概念:
絶対順序システムによる文法要素のランダマイゼーション実現
- V_group_key内での固定順序管理
- 2階層Order構造（Slot_display_order + display_order）
- 空白スロット・wh-word排他制御による文型バリエーション

🔄 統合戦略: 現行システム保持＋機能拡張
現在の69.7%認識精度の動的文法認識システムを基盤とし、
order機能を段階的に統合してランダマイゼーション機能を実現
```

### **Order機能アーキテクチャ**

```
┌─────────────────────────────────────────────┐
│ 動的文法認識システム + Order機能統合         │
├─────────────────────────────────────────────┤
│ 🏗️ Phase 1: 基盤整備 (必須実装)            │
│ ┌─────────────────────────────────────────┐ │
│ │ GrammarElement拡張                     │ │
│ │ ├─ slot_display_order フィールド       │ │
│ │ ├─ display_order フィールド            │ │
│ │ ├─ v_group_key フィールド              │ │
│ │ └─ is_subslot フラグ                   │ │
│ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────┐ │
│ │ V_group_key管理システム                │ │
│ │ ├─ 動詞ベースグループ分類              │ │
│ │ ├─ グループ別絶対順序テーブル          │ │
│ │ └─ 順序マッピング機能                  │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 🔧 Phase 2: コア機能実装 (強く推奨)         │
│ ┌─────────────────────────────────────────┐ │
│ │ サブスロット認識エンジン               │ │
│ │ ├─ sub-s, sub-v, sub-aux自動認識       │ │
│ │ ├─ sub-m1, sub-m2, sub-m3修飾語分類    │ │
│ │ ├─ sub-o1, sub-o2, sub-c1分割          │ │
│ │ └─ 品詞・依存関係ベース判定            │ │
│ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────┐ │
│ │ 階層構造データ管理                     │ │
│ │ ├─ 親スロット-子サブスロット関係管理   │ │
│ │ ├─ display_order による細分化順序      │ │
│ │ ├─ JSON出力形式対応                    │ │
│ │ └─ slot_order_data.json互換性          │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ 🚀 Phase 3: 応用機能 (遅延可能)            │
│ ┌─────────────────────────────────────────┐ │
│ │ ランダマイゼーション機能               │ │
│ │ ├─ 空白スロット・選択肢管理            │ │
│ │ ├─ wh-word排他制御                     │ │
│ │ ├─ 文型バリエーション生成              │ │
│ │ └─ 学習データ生成支援                  │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### **Order機能実装工程表**

#### **🏗️ Phase 1: 基盤整備** *(推定工数: 2-3週間, 必須実装)*

**目標**: 基本的なorder情報の管理基盤構築

**実装タスク**:

1. **GrammarElementクラス拡張**
   ```python
   @dataclass
   class GrammarElement:
       text: str
       tokens: List[Dict]
       role: str  # S, V, O1, O2, C1, C2, M1, M2, M3, Aux
       start_idx: int
       end_idx: int
       confidence: float
       # 🆕 Order機能追加フィールド
       slot_display_order: int = 0      # 上位スロット順序
       display_order: int = 0           # サブスロット内順序
       v_group_key: str = ""            # 動詞グループキー
       is_subslot: bool = False         # サブスロットフラグ
       parent_slot: str = ""            # 親スロット (サブスロット用)
       subslot_id: str = ""             # サブスロットID (sub-s, sub-v等)
   ```

2. **V_group_key管理システム**
   ```python
   class VGroupKeyManager:
       """V_group_key管理とorder計算"""
       
       def __init__(self):
           self.absolute_order_tables = self._load_order_tables()
       
       def determine_v_group_key(self, main_verb: str) -> str:
           """メイン動詞からV_group_keyを決定"""
           
       def get_absolute_order_map(self, v_group_key: str) -> Dict[str, int]:
           """絶対順序マップを取得"""
           
       def calculate_slot_display_order(self, slot: str, v_group_key: str) -> int:
           """Slot_display_orderを計算"""
   ```

3. **基本order計算機能**
   - 文中位置からSlot_display_order計算
   - V_group_key別順序ルール適用
   - 順序検証機能

**マイルストーン**:
- [x] 設計仕様策定完了
- [ ] GrammarElement拡張実装
- [ ] V_group_key管理システム実装
- [ ] 基本order計算ロジック実装
- [ ] Phase 1統合テスト

#### **🔧 Phase 2: コア機能実装** *(推定工数: 3-4週間, 強く推奨)*

**目標**: サブスロット認識と階層構造データ管理

**実装タスク**:

1. **サブスロット認識エンジン**
   ```python
   class SubslotRecognitionEngine:
       """サブスロット自動認識システム"""
       
       def recognize_subslots(self, grammar_element: GrammarElement) -> List[GrammarElement]:
           """主要スロットをサブスロットに分割"""
           
       def classify_subslot_type(self, token: Dict, context: List[Dict]) -> str:
           """sub-s, sub-v, sub-aux, sub-m1等の分類"""
           
       def calculate_display_order(self, subslots: List[GrammarElement]) -> List[GrammarElement]:
           """サブスロット内のdisplay_order計算"""
   ```

2. **階層構造データ管理**
   - 親スロット-子サブスロット関係管理
   - display_order による細分化順序
   - slot_order_data.json互換JSON出力

3. **順序計算システム高度化**
   - 複雑な文構造対応
   - 関係詞節・従属節処理
   - 修飾句の適切な分割

**マイルストーン**:
- [ ] サブスロット認識エンジン実装
- [ ] 階層構造データ管理実装
- [ ] JSON出力形式対応
- [ ] slot_order_data.json互換性確認
- [ ] Phase 2統合テスト

#### **🚀 Phase 3: 応用機能** *(推定工数: 2-3週間, 遅延可能)*

**目標**: ランダマイゼーション機能と高度な制御

**実装タスク**:

1. **空白スロット・選択肢管理**
   - 空白要素の母集団管理
   - 選択確率制御
   - 文型バリエーション生成

2. **wh-word排他制御**
   - 疑問詞の排他的選択ロジック
   - yes/no疑問文/肯定文変換
   - 疑問文パターン管理

3. **ランダマイゼーション機能**
   - スロット組み合わせ生成
   - 文意保持チェック
   - 学習データ生成支援

**マイルストーン**:
- [ ] 空白スロット処理実装
- [ ] wh-word排他制御実装
- [ ] ランダマイゼーション機能実装
- [ ] 統合システム最終テスト

### **実装優先度と判断基準**

#### **必須実装** *(Phase 1)*
```
判定理由:
✅ 現在の基本的なorderでは絶対順序が実現不可能
✅ V_group_key管理なしではランダマイゼーション時の文意保持が困難
✅ 後から追加するより、最初から設計した方が大幅に効率的
✅ 現在の69.7%認識精度を活かした順序情報付与が実現可能
```

#### **強く推奨** *(Phase 2)*
```
判定理由:
✅ 基本的な実用性のために重要
✅ slot_order_data.json完全互換には必須
✅ サブスロット認識なしでは詳細な文法分析が不完全
✅ 階層構造管理は将来の機能拡張の基盤
```

#### **遅延可能** *(Phase 3)*
```
判定理由:
⚠️ 高度なランダマイゼーション機能
⚠️ 動的文法認識システムが安定してから検討可
⚠️ 学習データ生成支援は実用段階で必要
✅ ただし、設計時点でPhase 3まで考慮した拡張可能な構造で実装
```

### **実装上の重要な考慮点**

```python
implementation_considerations = {
    "performance_preservation": [
        "現在の69.7%認識精度を下げないよう注意深く実装",
        "Phase 1実装後に既存テストで回帰テスト実施",
        "メモリ使用量とパフォーマンスへの影響監視"
    ],
    "compatibility_maintenance": [
        "slot_order_data.jsonとの互換性確保",
        "既存のDynamicGrammarMapperとの統合性維持",
        "後方互換性を保持した設計"
    ],
    "risk_management": [
        "段階的リリースで問題の早期発見",
        "各Phaseで完全なテスト実施",
        "ロールバック可能な実装戦略"
    ]
}
```

### **Order機能最終判断**

**技術的実現可能性**: **🟢 HIGH**
- 現在の動的文法認識システムの拡張として実装可能
- 既存の69.7%認識精度を基盤とした順序情報付与
- slot_order_data.jsonの構造分析により設計根拠明確化

**実装推奨度**: **🟡 PHASE 1 REQUIRED, PHASE 2 STRONGLY RECOMMENDED**
- Phase 1（基盤整備）: 必須実装 - 絶対順序システムの実現に不可欠
- Phase 2（コア機能）: 強く推奨 - 実用性のために重要
- Phase 3（応用機能）: 遅延可能 - 高度化は安定後に検討

**推奨開始時期**: **即座開始可能**
- 現在のシステムに対する拡張として段階的実装
- 既存の認識精度向上作業と並行実施可能
- リスク管理されたアプローチで安全な実装

**成功確度**: **🟢 HIGH**
```
Order機能統合は技術的に実現可能であり、
現在の動的文法認識システムの価値を大幅に向上させる。

開始条件: Phase 1設計完了（完了済み）
開始時期: 即座開始可能
優先順序: Phase 1 → Phase 2 → （認識精度向上後）Phase 3
```
