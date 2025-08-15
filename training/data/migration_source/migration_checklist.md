# 移植チェックリスト - Individual Engine to Unified Mapper

## 📋 移植対象エンジン一覧

### ✅ 優先度1 (Phase 1-3: 基礎構文)
- [ ] **simple_relative_engine.py** (256行)
  - 機能: 関係節処理 (acl:relcl, nsubj, obj, nmod:poss, advmod)  
  - 移植先メソッド: `_handle_relative_clause()`
  - テスト例文: "The car which we saw was red."

- [ ] **passive_voice_engine.py** (281行)
  - 機能: 受動態処理 (nsubj:pass, aux:pass, obl:agent)
  - 移植先メソッド: `_handle_passive_voice()`  
  - テスト例文: "The car was bought by him."

- [ ] **stanza_based_conjunction_engine.py** (218行)
  - 機能: 従属接続詞処理 (mark, advcl, 意味分類)
  - 移植先メソッド: `_handle_conjunction()`
  - テスト例文: "I came because it rained."

### ⚡ 優先度2 (Phase 4-6: 時制・句構造)
- [ ] **progressive_tenses_engine.py** 
  - 機能: 進行形処理
  - 移植先メソッド: `_handle_progressive()`

- [ ] **prepositional_phrase_engine.py**
  - 機能: 前置詞句処理  
  - 移植先メソッド: `_handle_prepositional_phrase()`

- [ ] **perfect_progressive_engine.py**
  - 機能: 完了進行形処理
  - 移植先メソッド: `_handle_perfect_progressive()`

### 🔧 優先度3 (Phase 7-9: 準動詞)
- [ ] **participle_engine.py**
  - 機能: 分詞処理
  - 移植先メソッド: `_handle_participle()`

- [ ] **gerund_engine.py** 
  - 機能: 動名詞処理
  - 移植先メソッド: `_handle_gerund()`

- [ ] **infinitive_engine.py**
  - 機能: 不定詞処理
  - 移植先メソッド: `_handle_infinitive()`

### 🎯 優先度4 (Phase 10-12: 特殊構文)
- [ ] **question_formation_engine.py**
  - 機能: 疑問文処理
  - 移植先メソッド: `_handle_question()`

- [ ] **subjunctive_conditional_engine.py**
  - 機能: 仮定法・条件法処理  
  - 移植先メソッド: `_handle_subjunctive_conditional()`

- [ ] **inversion_engine.py**
  - 機能: 倒置構文処理
  - 移植先メソッド: `_handle_inversion()`

### 📊 優先度5 (Phase 13-15: その他・基礎)
- [ ] **comparative_superlative_engine.py**
  - 機能: 比較・最上級処理
  - 移植先メソッド: `_handle_comparative()`

- [ ] **basic_five_pattern_engine.py**
  - 機能: 基本5文型処理
  - 移植先メソッド: `_handle_basic_five_pattern()`

- [ ] **modal_engine.py**
  - 機能: 法助動詞処理
  - 移植先メソッド: `_handle_modal()`

---

## 📝 移植作業手順

### 各エンジンの移植ステップ
1. **コード解析**: 移植元エンジンの主要メソッドを特定
2. **依存関係確認**: Stanza解析、ヘルパーメソッドなど
3. **メソッド抽出**: 核心ロジックを統合ファイル用に調整
4. **統合実装**: `_handle_xxx()` メソッドとしてUnifiedMapperに追加
5. **単体テスト**: 該当文法の動作確認
6. **統合テスト**: 既存機能との複合動作確認
7. **回帰テスト**: 既存機能の劣化がないことを確認

### 移植時の注意事項
- **Stanzaパイプライン**: 既存の`self.nlp`を活用
- **スロット命名**: Rephrase規約に準拠 (S, V, O1, sub-s, sub-v, etc.)
- **エラーハンドリング**: 統合システム用に調整
- **デバッグ出力**: 統合システムのログレベルに合わせる

---

## 🧪 テスト戦略

### 段階的テスト
```python
# test_unified_mapper.py での検証項目

Phase 1: 関係節のみ
✅ "The car which we saw was red."
✅ "The man who runs is fast."
✅ "The place where I live is Tokyo."

Phase 2: 関係節 + 受動態
✅ "The car was bought."  
✅ "The car which was bought was red."
✅ "The book which was read by him is interesting."

Phase 3: 関係節 + 受動態 + 接続詞
✅ "Because the car which was bought was red, he liked it."
```

### パフォーマンステスト
- 処理時間測定 (1文あたり0.1-0.3秒目標)
- メモリ使用量監視 (50MB以下)
- 複雑文での安定性確認

---

## 📊 進捗管理

### 完了チェック
- [ ] Phase 0: 基盤構築
- [ ] Phase 1: 関係節移植
- [ ] Phase 2: 受動態移植  
- [ ] Phase 3: 接続詞移植
- [ ] Phase 4-15: 段階的拡張
- [ ] Phase 16: 統合・最適化

### 品質基準
各Phase完了時に以下をクリア:
- ✅ 単体テスト100%成功
- ✅ 統合テスト95%以上成功  
- ✅ パフォーマンス基準内
- ✅ 既存機能劣化なし

---

## 🔗 参考ファイル

### 移植元ディレクトリ
```
migration_source/
├── simple_relative_engine.py           # 関係節処理の参考実装
├── passive_voice_engine.py             # 受動態処理の参考実装
├── stanza_based_conjunction_engine.py  # 接続詞処理の参考実装
├── ...
└── (全15個別エンジン)
```

### 開発ファイル
- `unified_stanza_rephrase_mapper.py` - 統合メインファイル
- `test_unified_mapper.py` - テストシステム
- `Unified_Mapper_Design_Spec.md` - 設計仕様書

---

**更新履歴**:
- 2025/08/15: 初版作成
- (進行に応じて更新予定)
