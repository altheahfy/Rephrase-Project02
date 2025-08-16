# 🎯 例文セットDB作成システム専用注意書き

**🚨 このドキュメントは例文セット作成・テスト時の必読事項です**

---

## 📋 **例文テスト時の重要原則**

### **❌ 典型的な誤解パターン**

```
誤解例 1: "前置詞句エンジンのテスト"
❌ 間違い: "The book is on the table" → Prepositional Engine単体でテスト
✅ 正解: Grammar Master Controller経由でマルチエンジン協調テスト

誤解例 2: "進行形エンジンの不完全な結果"
❌ 間違い: "She was running to the store" → M2:"to" だけで「失敗」判定
✅ 正解: 協調システムで M2:"to the store" に補完されることを想定

誤解例 3: "単体エンジンの完璧性要求"
❌ 間違い: 個別エンジンが全ての要素を完璧に処理すべき
✅ 正解: 専門領域のみ処理、他はマルチエンジン協調に委ねる
```

---

## 🧪 **正しいテスト手順**

### **Phase 1: 単体エンジンテスト (参考用)**
```python
# 目的: エンジンの専門領域動作確認のみ
engine = ProgressiveTensesEngine()
result = engine.process("She was running to the store")
# 期待: S:She, Aux:was, V:running, M1:quickly, M2:"to" 
# 注意: M2:"to"の不完全さは正常動作
```

### **Phase 2: 協調システムテスト (本番)**
```python
# 目的: 実際の運用状況での動作確認
controller = GrammarMasterControllerV2()
result = controller.process("She was running to the store", debug=True)
# 期待: 完全な統合結果 (M2:"to the store"等)
```

### **Phase 3: 複雑文テスト**
```python
# 目的: Multi Cooperative動作確認
complex_sentence = "The students who were studying in the library have been working"
result = controller.process(complex_sentence, debug=True)
# 期待: 複数エンジンの協調による完璧な分解
```

---

## 📊 **例文分類システム**

### **難易度別カテゴリ**

```
Level 1: Single Optimal適用例文
├─ "I am eating." (進行形エンジン単独)
├─ "The cat sits." (基本5文型単独)
└─ "Can you help me?" (疑問文エンジン単独)

Level 2: Foundation Plus Specialist適用例文
├─ "She was running quickly." (基本5文型 + 進行形)
├─ "The book was written by him." (基本5文型 + 受動態)
└─ "I can see the mountain." (基本5文型 + 助動詞)

Level 3: Multi Cooperative適用例文
├─ "The students who were studying have been working."
├─ "Because she was tired, she went to bed early."
└─ "The book that I bought was written by a famous author."
```

### **エンジン特化テストセット**

```
進行形エンジン専用:
├─ "I am eating." → S:I, Aux:am, V:eating
├─ "She was running fast." → S:She, Aux:was, V:running, M1:fast
└─ "They are playing in the park." → M2:"in" (協調で補完予定)

前置詞句エンジン専用:
├─ "The book is on the table." → 場所前置詞句
├─ "We met at 3 o'clock." → 時間前置詞句  
└─ "She went to the store with her friend." → 複数前置詞句
```

---

## 🎯 **テスト結果評価基準**

### **正しい評価方法**

```
✅ 正常判定基準:
1. 専門エンジン: 専門領域を正確に処理
2. 協調システム: 統合結果が完璧
3. 複雑度判定: 適切な協調戦略を選択
4. 性能: 78.7%以上の成功率維持

❌ 間違った評価基準:
1. 単体エンジンの完璧性要求
2. 表面的な「不完全」による失敗判定
3. 協調システムを無視したテスト
4. 専門外領域の処理要求
```

### **トラブルシューティング指針**

```
問題: "前置詞句処理が不完全"
→ 確認: 単体テストか協調テストか？
→ 解決: 協調テストで再評価

問題: "エンジンが他の構造を見落とし"
→ 確認: そのエンジンの専門領域か？
→ 解決: 専門外なら協調システムで処理

問題: "複雑文で失敗"
→ 確認: Multi Cooperative戦略が選択されているか？
→ 解決: 複雑度判定ロジックを確認
```

---

## 💡 **例文セット作成ガイドライン**

### **良い例文の条件**
```
1. 明確な文法構造を持つ
2. 該当エンジンの専門領域を適切にテスト
3. 協調システムの動作を確認可能
4. 現実的な英語表現を使用
```

### **避けるべき例文**
```
1. 文法的に曖昧な文
2. 複数の解釈が可能な文
3. 専門領域外の要素が主体の文
4. 人工的で不自然な文
```

---

## 🔄 **継続改善プロセス**

### **例文セットメンテナンス**
1. 月1回の例文セット評価
2. 新しい文法パターンの追加
3. 失敗例文の原因分析
4. 協調システム最適化

### **AI Assistant向け学習材料**
- 成功例文の蓄積
- 失敗パターンの分析
- 協調システム理解の深化
- 設計思想の内在化

---

**Remember: "Test the symphony, not just individual instruments"**
