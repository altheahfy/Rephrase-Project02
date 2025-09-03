# Phase 5: 最終設定化プラン

## 🎯 残存ハードコーディング分析

### 発見された設定化可能な部分

#### 1. 文法パターン検出順序 (lines 676-680)
```python
# 現在のハードコーディング
if self.handlers['metaphorical'].can_handle(text):
    detected_patterns.append('metaphorical')
elif self.handlers['question'].is_question(text):
    detected_patterns.append('question')
```

**設定化案**: `grammar_detection_priority` 配列

#### 2. 助動詞正規化パターン (lines 770-780)
```python
# 現在のハードコーディング
if aux in ['did', 'do', 'does']:
    pattern = f"{slots['Aux']} {subject}"
```

**設定化案**: `auxiliary_normalization_patterns` テーブル

#### 3. 疑問文判定ロジック (line 762)
```python
# 現在のハードコーディング
if text.endswith('?'):
    text = text[:-1].strip()
```

**設定化案**: `question_markers` 配列

#### 4. ハンドラー選択ロジック (lines 695-700)
```python
# 現在のハードコーディング
if gerund_handler.can_handle(text):
    # 処理
if infinitive_handler.can_handle(text):
    # 処理
```

**設定化案**: `handler_priority_chain` 設定

## 📊 設定化の価値分析

### 高価値（実施推奨）
1. **文法パターン検出順序** - 新しい文法パターン追加時の柔軟性
2. **助動詞正規化パターン** - 多言語対応・新しい助動詞追加

### 中価値（検討要）
3. **疑問文判定ロジック** - 多言語対応時に有用
4. **ハンドラー選択ロジック** - プラグインアーキテクチャ向け

### 低価値（現状維持でOK）
- 基本的なPython構文（if文、for文等）
- ライブラリAPI呼び出し（self.nlp等）

## 🎯 Phase 5 実施方針

### 優先度A: 文法パターン検出順序の設定化
- 最も高い拡張性効果
- 新しい文法機能追加時の影響大

### 優先度B: 助動詞正規化の設定化  
- 国際化対応に重要
- テストしやすくなる

### 判断基準
- **設定化効果 > 複雑性コスト** の場合のみ実施
- 将来の拡張可能性を重視

## 💎 最終目標

**完全設定駆動型システム**: 新機能追加がすべて設定変更のみで対応可能
