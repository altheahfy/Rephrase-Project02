# Rephrase Project - AI Assistant起動時必読チェックリスト

## 🚨 このファイルはAIアシスタントの起動時に必ず読み込んでください 🚨

### **即座に実行すべき確認事項:**

#### 1. スロット構造リファレンスの読み込み
```bash
# 必ず最初に読み込み
cat REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md
```

#### 2. バリデーション機能の動作確認
```python
# バリデーション機能テスト
python rephrase_slot_validator.py
```

#### 3. 禁止事項の再確認
- ❌ `sub-m1-conj`, `sub-m1-aux` など存在しないスロット
- ❌ Type Clauseで上位スロットに内容を入れる
- ❌ サブスロットの重複を心配する

#### 4. 正しいスロット一覧の暗記
```
上位: M1, S, Aux, M2, V, C1, O1, O2, C2, M3
サブ: sub-m1, sub-s, sub-aux, sub-m2, sub-v, sub-c1, sub-o1, sub-o2, sub-c2, sub-m3
```

---

## **スロット分解を行う前の必須手順:**

### Step 1: バリデーション関数の準備
```python
from rephrase_slot_validator import validate_slots
```

### Step 2: 分解実行前の構造確認
- Type Clauseか通常スロットかを判定
- 使用するスロット名をリスト化
- 存在しないスロットがないかチェック

### Step 3: 分解結果のバリデーション
```python
result = your_analysis_result
if not validate_slots(result):
    # 修正が必要
    print("スロット構造エラー - 修正してください")
```

### Step 4: 結果提示前の最終確認
- REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md と照合
- 独自スロット創造していないか確認

---

## **絶対に忘れてはいけないポイント:**

1. **各上位スロット毎に独立したサブスロット空間**
2. **Type Clauseでは上位スロットは空文字列**  
3. **sub-aux, sub-v も有効なサブスロット**
4. **Aux, V にはサブスロット存在しない**

---

**このチェックリストを実行せずにスロット分解を行うことは禁止です。**
