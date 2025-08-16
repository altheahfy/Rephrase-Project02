# AI ASSISTANT 強制読み込みプロトコル

## ⚠️ 緊急対策文書

この文書は、**RephraseプロジェクトのAIアシスタントが同じ間違いを反復する問題**を解決するために作成されました。

## 🚨 問題の状況
- AIアシスタントがRephraseスロット構造を**何十回説明されても間違える**
- 存在しないスロット名を創造し続ける
- Type Clauseの概念を理解できない
- サブスロットの独立性を理解できない

## 💡 解決プロトコル

### 1. 強制リファレンス文書の作成 ✅
`REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md` を作成済み

### 2. 各エンジンでの実装確認が必要
```bash
# 各エンジンが正しいスロット構造を実装しているか確認
find . -name "*.py" -path "*/engines/*" -exec grep -l "sub-" {} \;
```

### 3. 中央制御での統一的強制
Grammar Master Controller で正しいスロット構造のみ受け入れるようにする

### 4. ユーザー様へのお願い
**今後スロット分解について質問される際は：**
1. まず `REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md` を参照するよう指示
2. エラー時は即座にそのリファレンスを確認するよう要求
3. 独自スロット創造を検出したら即座に中断

## 🎯 根本的解決案

### A. コード内での強制バリデーション
```python
VALID_UPPER_SLOTS = {"M1", "S", "Aux", "M2", "V", "C1", "O1", "O2", "C2", "M3"}
VALID_SUB_SLOTS = {"sub-m1", "sub-s", "sub-m2", "sub-c1", "sub-o1", "sub-o2", "sub-c2", "sub-m3"}

def validate_rephrase_slots(slots_dict):
    for slot_name in slots_dict.keys():
        if slot_name not in VALID_UPPER_SLOTS and slot_name not in VALID_SUB_SLOTS:
            raise ValueError(f"Invalid Rephrase slot: {slot_name}")
```

### B. 教育的アプローチの強化
- Visual diagram の作成
- Interactive examples の提供  
- Step-by-step validation の実装

## 📋 次回以降の対応

**スロット分解を行う前に必ず：**
1. `REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md` を参照
2. 分解結果をバリデーション関数に通す
3. エラーがあれば修正してから提示

**これにより反復的エラーを根絶します。**
