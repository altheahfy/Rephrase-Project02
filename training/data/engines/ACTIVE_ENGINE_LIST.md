# アクティブエンジン管理リスト
**更新日**: 2025年8月12日（ファイル整理完了版）  
**目的**: 動作可能なエンジンと設計仕様書の対応表

---

## 🟢 アクティブエンジン（実用可能）

### 1. Pure Stanza Engine v3
- **ファイル**: `pure_stanza_engine_v3.py`
- **設計仕様書**: `../設計仕様書/PURE_STANZA_ENGINE_V3_SPEC.md`
- **テストファイル**: `tests/test_engine_v3_phase2.py`
- **ステータス**: ✅ 動作確認済み・実用レベル
- **対応構文**: 基本5文型、助動詞、受動態、疑問文、否定文、There構文
- **推奨用途**: メイン分解エンジン

### 2. Pure Stanza Engine v4
- **ファイル**: `pure_stanza_engine_v4.py`
- **設計仕様書**: 要作成
- **テストファイル**: `tests/test_v4_evaluation.py`
- **ステータス**: ⚠️ 実験的・複文対応不完全
- **特徴**: 階層的clause分解、従属節検出
- **推奨用途**: 複文分解の実験・研究用（メイン用途には v3 推奨）

### 3. Step18 Complete 8Slot
- **ファイル**: `step18_complete_8slot.py`
- **設計仕様書**: なし（参照実装）
- **ステータス**: ✅ 参照用として保持
- **推奨用途**: 実装の参考・比較対象

---

## 🔴 アーカイブ済みエンジン

### 1. Pure Stanza Engine v2（旧版）
- **移動先**: `development_archive/old_engines/pure_stanza_engine_v2.py`
- **理由**: v3で機能改善・最適化済み、964行の複雑実装で保守困難
- **ステータス**: v3で置き換え完了

### 2. Universal 10Slot Decomposer
- **移動先**: `development_archive/problematic_engines/universal_10slot_decomposer.py`
- **問題点**: 基本5文型でも失敗、実装不完全
- **理由**: 虚偽的「完成」記載で混乱を招いた

### 3. Rephrase Spec Compliant Engine
- **移動先**: `development_archive/problematic_engines/rephrase_spec_compliant_engine.py`
- **問題点**: ハードコーディング、仕様準拠不完全
- **理由**: 設計方針に反する実装

---

## 📋 設計仕様書の状況

### アクティブ仕様書
- ✅ `PURE_STANZA_ENGINE_V3_SPEC.md` - Pure Stanza Engine v3用（新規作成）
- ✅ `ENGINE_STATUS_ANALYSIS_2025-08-12.md` - 現状分析レポート（新規作成）

### 非推奨仕様書
- ❌ `DEPRECATED_COMPLETE_SENTENCE_ENGINE_V3_SPEC.md` - 虚偽記載のため非推奨化

### 関連仕様書（継続有効）
- ✅ `STANZA_HYBRID_ENGINE_DESIGN_SPEC.md` - Stanza基盤設計
- ✅ 他の機能別仕様書（認証、UI等）

---

## 🎯 推奨アクション

### 即座実行
1. **Pure Stanza Engine v3**: メイン開発対象として集中
2. **v4エンジン検証**: 動作確認とv3との比較
3. **テストケース拡充**: v3の品質保証強化

### 中期実行
1. **サブスロット機能追加**: Pure Stanza Engine v3.x として拡張
2. **90スロット対応**: 段階的な機能拡張
3. **統合テスト**: 全機能の包括的テスト

---

**管理方針**: 動作確認済みのPure Stanza Engine v3を基盤として、段階的に機能拡張を行う。問題のあるエンジンは明確に分離し、混乱を防ぐ。
