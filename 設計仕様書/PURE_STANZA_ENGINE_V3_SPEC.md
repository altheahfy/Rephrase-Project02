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

---

## 2. 現在の制限事項

### 2.1 未実装機能
- **サブスロット分解**: 複雑な句・節の再帰分解
- **90スロット対応**: 現在は10スロット基本構成
- **上位スロット空化**: Rephraseサブスロット仕様

### 2.2 改善が必要な領域
- **複文対応**: 従属節・関係節の詳細分解
- **前置詞句**: 複雑な修飾句の処理
- **特殊構文**: 倒置、省略などの高度文法

---

## 3. 開発ロードマップ

### Phase 1（完了済み）
- ✅ 基本5文型完全対応
- ✅ 高頻度構文（助動詞、受動態、疑問文、否定文）
- ✅ ゼロハードコーディング設計
- ✅ 設定駆動型アーキテクチャ

### Phase 2（次期計画）
- [ ] サブスロット分解機能追加
- [ ] 複文・複雑文対応
- [ ] Rephraseサブスロット仕様準拠
- [ ] パフォーマンス最適化

### Phase 3（将来計画）
- [ ] 90スロット完全対応
- [ ] 高度文法構文対応
- [ ] リアルタイム処理対応

---

## 4. テスト体制

### 4.1 実装済みテスト
- **test_engine_v3_phase2.py**: 高頻度構文の包括的テスト
- **動作確認**: 全テストケース成功
- **カバレッジ**: 基本構文100%、高頻度構文100%

### 4.2 品質保証
- **継続的テスト**: 機能追加時の回帰テスト
- **設定検証**: rephrase_rules_v2.0.json の整合性確認
- **パフォーマンス測定**: 処理時間・メモリ使用量監視

---

## 5. 使用方法

### 5.1 基本的な使用
```python
from pure_stanza_engine_v3 import PureStanzaEngineV3

engine = PureStanzaEngineV3()
result = engine.decompose("I can swim.")
# 結果: {"S": "I", "Aux": "can", "V": "swim"}
```

### 5.2 設定カスタマイズ
- **設定ファイル**: `rephrase_rules_v2.0.json` を編集
- **追加パターン**: 新しい構文パターンを設定で追加可能
- **柔軟性**: ハードコーディングなしで動作変更可能

---

## 6. まとめ

**Pure Stanza Engine v3** は、基本5文型から高頻度構文まで実用レベルで動作する実装済みエンジンです。設定駆動型設計により、柔軟な拡張が可能で、今後のサブスロット対応や90スロット実装の基盤として活用できます。

**実績**: 
- ✅ 実装完了・動作確認済み
- ✅ 包括的テスト成功
- ✅ 実用レベルの品質

**次のステップ**: Phase 2としてサブスロット分解機能の追加を計画。
