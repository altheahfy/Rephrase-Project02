# Training Data Directory Structure

## 📁 Directory Organization

### Core Files
- `grammar_master_controller.py` - メインコントローラー（従来版）
- `grammar_master_controller_v2.py` - 統合コントローラー（最新版）
- `preset_config.json` - 設定ファイル
- `rephrase_rules_v2.0.json` - リフレーズルール
- `slot_order_data.json` - スロット順序データ
- `ultimate_grammar_engine.log` - システムログ

### 📁 engines/
文法エンジンコアモジュール
- `modal_engine.py` - 助動詞エンジン（11番目の統合エンジン）
- その他の統合済み文法エンジン

### 📁 tests/
全テストファイル（18個）
- `test_modal_*` - Modal Engine テスト
- `test_passive_*` - 受動態テスト  
- `test_perfect_progressive_*` - 完了進行形テスト
- `test_comparative_*` - 比較級・最上級テスト
- `test_*_unified.py` - 統合テスト
- `test_all_unified.py` - 全エンジン統合テスト

### 📁 analysis/
分析・デモファイル（4個）
- `analyze_*.py` - 各文法パターン分析
- `demo_*.py` - デモンストレーション

### 📁 monitoring/
システム監視・最適化（5個）
- `ultimate_grammar_system.py` - Ultimate Grammar System v1.0
- `auto_optimization_system.py` - 自動最適化
- `resilience_system.py` - 復旧システム
- `grammar_performance_dashboard.py` - パフォーマンスダッシュボード
- `simple_grammar_monitor.py` - 簡易監視

### 📁 specifications/
設計仕様書（1ファイル - 最新統合版）
- `文要素分解システム設計仕様書_v2.0_Ultimate.md` - **Ultimate Grammar System v1.0完全仕様書**

### 📁 development_archive/
開発履歴アーカイブ

### 📁 docs/
ドキュメント

### 📊 Data Files
- `V自動詞第1文型.json` - 自動詞データ
- `第3,4文型.json` - 第3,4文型データ
- `例文入力元.xlsx` - 例文データベース
- `絶対順序考察.xlsx` - スロット順序分析

## 🎯 Current Status (2025年8月12日)
- ✅ Modal Engine: 100% accuracy achieved
- ✅ 11 Unified Grammar Engines integrated
- ✅ Ultimate Grammar System v1.0 operational
- ✅ Enterprise monitoring & optimization active

## 🚀 Next Steps
1. Question Formation Engine (12th engine)
2. Conditional Sentence Engine (13th engine)  
3. Complex Sentence Structure Engine (14th engine)
4. Performance optimization and scaling
