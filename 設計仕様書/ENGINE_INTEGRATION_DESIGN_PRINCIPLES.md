# Unified Stanza-Rephrase Mapper エンジン設計原則仕様書 v1.0

**作成日**: 2025年8月15日  
**対象**: 全エンジン開発・統合  
**重要度**: ★★★ 必須遵守

## 1. 並列処理の基本原則

### 1.1 「全シェフが例文を見る」方式
```python
# 各エンジンは独立して全文を解析
for handler_name in self.active_handlers:
    handler_result = handler_method(main_sentence, result.copy())
    # ↑ 全エンジンが同一の入力文を受け取る
```

**原則:**
- ✅ 各エンジンは**全文を独立解析**
- ✅ エンジン間で**依存関係を持たない**
- ❌ エンジンAがエンジンBを内部呼び出ししない

### 1.2 責任分離の明確化

| エンジン種類 | 処理対象 | 出力責任 | 上位スロット | サブスロット |
|------------|---------|---------|------------|-------------|
| **5文型エンジン** | 主文構造 | S, V, O1, O2, C1, C2 | ✅設定 | ❌設定禁止 |
| **関係節エンジン** | 関係節構造 | sub-s, sub-v, sub-o1等 | ❌設定禁止 | ✅設定 |
| **受動態エンジン** | 受動態構造 | Aux, by句処理 | ✅設定 | ✅設定 |
| **副詞エンジン** | 修飾語処理 | M1, M2, M3 | ✅設定 | ✅設定 |

## 2. 競合回避メカニズム

### 2.1 スロット競合解決ルール

```python
# 修正後の競合解決ロジック
if slot_name not in base_result['slots']:
    base_result['slots'][slot_name] = slot_data
else:
    existing_value = base_result['slots'][slot_name]
    
    # 【重要】空文字・空値での有効値上書きを防止
    if existing_value and not slot_data:
        pass  # 既存の有効値を保持
    elif not existing_value and slot_data:
        base_result['slots'][slot_name] = slot_data  # 空→有効値で更新
    else:
        base_result['slots'][slot_name] = slot_data  # 後勝ち
```

### 2.2 禁止事項

#### ❌ エンジン内での他エンジン呼び出し
```python
# 悪い例：関係節エンジンが5文型エンジンを呼び出し
def _handle_relative_clause(self, sentence, base_result):
    # ... 関係節処理 ...
    main_result = self._handle_basic_five_pattern(...)  # ❌ 禁止
    return result
```

#### ❌ 空値での有効値上書き
```python
# 悪い例：関係節エンジンが主語を空文字で設定
def _generate_relative_clause_slots(self, ...):
    slots = {}
    slots["S"] = ""  # ❌ 5文型エンジンの有効値を消去
    return {"slots": slots, "sub_slots": sub_slots}
```

#### ❌ 責任範囲外への干渉
```python
# 悪い例：関係節エンジンが主文の動詞を設定
def _generate_relative_clause_slots(self, ...):
    slots = {}
    slots["V"] = "is"  # ❌ 5文型エンジンの責任範囲
    return {"slots": slots, "sub_slots": sub_slots}
```

### 2.3 推奨実装パターン

#### ✅ 責任範囲の純化
```python
# 良い例：関係節エンジンはサブスロットのみ設定
def _generate_relative_clause_slots(self, ...):
    slots = {}  # 上位スロットは設定しない
    sub_slots = {
        "sub-s": noun_phrase,
        "sub-v": rel_verb.text
    }
    return {"slots": slots, "sub_slots": sub_slots}
```

#### ✅ 条件付き処理
```python
# 良い例：該当しない場合は何もしない
def _handle_passive_voice(self, sentence, base_result):
    if not self._is_passive_voice(sentence):
        return None  # 受動態でなければ処理しない
    # ... 受動態処理のみ実行 ...
```

## 3. エンジン実装チェックリスト

### 3.1 新エンジン開発時の必須確認項目

- [ ] **独立性確保**: 他エンジンを内部呼び出ししていないか？
- [ ] **責任明確化**: 処理対象が明確に定義されているか？
- [ ] **競合回避**: 他エンジンと同じスロットに異なる値を設定していないか？
- [ ] **条件処理**: 該当しない文には何もしないか？
- [ ] **空値設定禁止**: 意味のない空文字でスロットを埋めていないか？

### 3.2 統合テスト必須項目

- [ ] **単体動作**: エンジン単体で正常動作するか？
- [ ] **並列動作**: 他エンジンと同時実行で競合しないか？
- [ ] **順序独立**: エンジン実行順序に依存しないか？
- [ ] **結果統合**: マージ後の結果が論理的に正しいか？

## 4. 実装例：修正前後の比較

### 4.1 修正前（問題のあるコード）

```python
# 関係節エンジンの問題実装
def _generate_relative_clause_slots(self, ...):
    slots = {
        "S": "",  # ❌ 5文型エンジンの結果を上書き
        "O1": ""  # ❌ 空文字で他エンジンの有効値を消去
    }
    sub_slots = {"sub-s": noun_phrase, "sub-v": rel_verb.text}
    return {"slots": slots, "sub_slots": sub_slots}

# 関係節エンジン内での重複処理
def _process_relative_clause_structure(self, ...):
    # ... 関係節処理 ...
    main_result = self._process_main_clause_after_relative(...)  # ❌ 重複
    return result
```

### 4.2 修正後（推奨実装）

```python
# 関係節エンジンの正しい実装
def _generate_relative_clause_slots(self, ...):
    slots = {}  # ✅ 上位スロットは設定しない
    sub_slots = {
        "sub-s": noun_phrase, 
        "sub-v": rel_verb.text
    }
    return {"slots": slots, "sub_slots": sub_slots}

# 5文型エンジンが独立して主文処理
def _handle_basic_five_pattern(self, sentence, base_result):
    # ✅ 全文を解析して主文構造を抽出
    return {"slots": {"S": "book", "V": "is", "C1": "mine"}, "sub_slots": {}}
```

## 5. Phase 3以降への適用

### 5.1 冠詞エンジン設計方針
- **処理対象**: det依存関係のみ
- **出力責任**: 既存スロット値の拡張（"car" → "The car"）
- **競合回避**: 既存値を完全置換ではなく拡張

### 5.2 副詞エンジン設計方針
- **処理対象**: advmod依存関係
- **出力責任**: M1, M2, M3スロット、sub-m1, sub-m2等
- **競合回避**: 既存の修飾語と階層的に整理

### 5.3 将来エンジンへの適用
- **前置詞句エンジン**: 前置詞句構造のみ処理
- **比較構文エンジン**: 比較構造のみ処理  
- **接続詞エンジン**: 等位・従位接続のみ処理

## 6. 保守・拡張ガイドライン

### 6.1 既存エンジン修正時
1. **影響範囲確認**: 他エンジンとの競合が発生しないか検証
2. **統合テスト**: 全エンジン組み合わせでの動作確認
3. **責任範囲維持**: 修正により責任範囲が曖昧にならないか確認

### 6.2 新規エンジン追加時
1. **責任定義**: 処理対象と出力責任の明確化
2. **競合分析**: 既存エンジンとのスロット競合可能性の調査
3. **設計レビュー**: この仕様書への準拠確認

---

**この設計原則により、スケーラブルで保守性の高いエンジン統合システムを実現します。**
