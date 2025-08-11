# Pure Stanza Engine v3 仕様書
**バージョン**: v3.2  
**作成日**: 2025年8月12日  
**目的**: 実用レベル英文分解エンジン仕様  
**基盤**: Pure Stanza v3 - 実装済み・動作確認済み

---

## 1. 実装済み機能（動作確認済み）

### 1.1 基本5文型対応 ✅
- **第1文型**: SV - "I sleep." → S:I, V:sleep
- **第2文型**: SVC - "She is happy." → S:She, V:is, C1:happy
- **第3文型**: SVO - "He plays tennis." → S:He, V:plays, O1:tennis
- **第4文型**: SVOO - "I gave him a book." → S:I, V:gave, O1:him, O2:book
- **第5文型**: SVOC - "They made him captain." → S:They, V:made, O1:him, C2:captain

### 1.2 高頻度構文対応 ✅
- **助動詞構文**: "I can swim" → S:I, Aux:can, V:swim
- **複数助動詞**: "We will have done it" → S:We, Aux:will have, V:done, O1:it
- **受動態**: "The book was read" → S:The book, Aux:was, V:read
- **進行受動**: "It is being built" → S:It, Aux:is being, V:built
- **疑問文**: "What is this?" → O1:What, V:is, S:this
- **否定文**: "I don't know" → S:I, Aux:do, V:know, M2:n't
- **There構文**: "There is a book" → M1:There, V:is, O1:a book

### 1.3 技術仕様
- **NLP基盤**: Stanza（Stanford NLP）
- **設定駆動**: rephrase_rules_v2.0.json による柔軟な設定
- **ハードコーディング**: ゼロ（設定ファイルで全制御）
- **処理方式**: 依存構文解析ベース

## 2. 現在の開発位置（2025年8月12日時点）

### 2.1 完了基盤 ✅
- **統一分解エンジンコア**: Pure Stanza Engine v3 実装完了
- **基本10スロット**: M1,S,Aux,V,O1,O2,C1,C2,M2,M3 対応
- **設定駆動アーキテクチャ**: ハードコーディングゼロ実現
- **包括的テスト**: 基本5文型〜高頻度構文の動作確認済み

### 2.2 現在の立ち位置 🎯
**「Rephraseの統一入れ子構造実装の直前」**

Rephraseの核心仕様：
- **Aux, V以外の8スロット**（M1,S,O1,O2,C1,C2,M2,M3）は再帰構造
- **各スロットが同じ10スロット構造**を内包
- **統一アルゴリズム**で全階層に対応可能
- **上位スロット空化**：phrase/clause時に上位を空にしてサブスロット展開

### 2.3 実装直前の技術的準備状況
```python
# 現在のv3エンジンで認識済み（実装待ち）
def _extract_all_subslots(self, sent, slots):
    """サブスロット処理枠組み - 統一入れ子構造実装予定地点"""
    # TODO: Rephraseの8スロット再帰構造をここに実装
```

**統一分解の核心概念は理解済み、実装基盤は整備完了**

---

## 3. 現在の制限事項

### 3.1 未実装機能（実装直前）
- **🎯 統一入れ子構造**: Rephraseの8スロット再帰分解（実装基盤完成済み）
- **🎯 上位スロット空化**: phrase/clause時の上位クリア（アルゴリズム設計済み）
- **🎯 無限階層対応**: 同一アルゴリズムによる深度制限なし分解（理論確立済み）

### 3.2 将来拡張項目
- **90スロット完全対応**: 無限入れ子による自動到達
- **高度文法構文**: 統一エンジンで包括対応
- **パフォーマンス最適化**: 再帰処理の効率化

---

## 4. 開発ロードマップ（更新版）

### Phase 2A（次の一歩・実装直前） 🎯 **現在位置**
**「統一入れ子構造の実装」**
- [ ] Rephraseの8スロット再帰構造実装
- [ ] 上位スロット空化ルール適用  
- [ ] 統一アルゴリズムによる深度無制限分解
- [ ] **Expected: Pure Stanza Engine v3.1 (Unified Recursive Engine)**

### Phase 2B（直後）
- [ ] 複雑文・複文の実証テスト
- [ ] 階層分解品質保証
- [ ] パフォーマンス測定・最適化

### Phase 3（中期）
- [ ] 90スロット自動到達検証
- [ ] 高度文法構文対応
- [ ] リアルタイム処理対応

---

## 5. テスト体制

### 5.1 実装済みテスト
- **test_engine_v3_phase2.py**: 高頻度構文の包括的テスト
- **動作確認**: 全テストケース成功
- **カバレッジ**: 基本構文100%、高頻度構文100%

### 5.2 品質保証
- **継続的テスト**: 機能追加時の回帰テスト
- **設定検証**: rephrase_rules_v2.0.json の整合性確認
- **パフォーマンス測定**: 処理時間・メモリ使用量監視

---

## 6. 使用方法

### 6.1 基本的な使用
```python
from pure_stanza_engine_v3 import PureStanzaEngineV3

engine = PureStanzaEngineV3()
result = engine.decompose("I can swim.")
# 結果: {"S": "I", "Aux": "can", "V": "swim"}
```

### 6.2 設定カスタマイズ
- **設定ファイル**: `rephrase_rules_v2.0.json` を編集
- **追加パターン**: 新しい構文パターンを設定で追加可能
- **柔軟性**: ハードコーディングなしで動作変更可能

---

## 6. まとめ

---

## 7. まとめ

**Pure Stanza Engine v3** は、基本5文型から高頻度構文まで実用レベルで動作する実装済みエンジンです。設定駆動型設計により、柔軟な拡張が可能で、**現在はRephraseの統一入れ子構造実装の直前段階**にあります。

**現在の立ち位置**: 
- ✅ 統一分解エンジンの基盤完成
- 🎯 **Rephraseの8スロット再帰構造実装直前**
- 🎯 統一アルゴリズムによる無限階層対応準備完了

**次のマイルストーン**: 
Pure Stanza Engine v3.1 (Unified Recursive Engine) として、Rephraseの真の統一入れ子構造を実装し、90スロット対応への扉を開く。

**重要な認識**: 
現在は「統一分解エンジンで全てに同じように対応」を実現する一歩手前の重要な地点にある。基盤技術は確立済み。
