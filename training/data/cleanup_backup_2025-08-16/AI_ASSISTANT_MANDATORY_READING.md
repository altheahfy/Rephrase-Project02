# 🚨 AI Assistant 必読事項 - システム破壊防止ガイド

**⚠️ WARNING: この文書を読まずに修正作業を行うことは絶対禁止 ⚠️**

---

## 📋 **チャット開始時の必須確認事項**

### **🔴 STOP! まずこれを読め！**

```
❌ 絶対にやってはいけないこと:
・個別エンジンファイルだけを見て「不完全だから修正しよう」と判断
・マルチエンジン協調システムを忘れて単体動作を求める
・設計仕様書を読まずに修正作業を開始
・「前置詞句の処理が不十分」などの表面的問題に飛びつく

✅ 必ずやるべきこと:
・文要素分解システム設計仕様書_v2.0_Ultimate.md を最初に読む
・マルチエンジン協調システムの理解を確認
・Grammar Master Controller v2 の協調戦略を把握
・個別エンジンの役割分担を理解してから作業開始
```

---

## 🎯 **Rephrase システム設計思想 - 絶対原則**

### **核心概念: マルチエンジン協調システム**

```
🏗️ システム構造:
┌─────────────────────────────────────┐
│ Grammar Master Controller v2        │ ← 🎯 協調制御の司令塔
├─────────────────────────────────────┤
│ 15個の専門エンジン (Priority 0-14)  │ ← 🔧 専門特化エンジン群
│ ・各エンジンは専門領域のみ担当      │
│ ・単体の完璧性は求めない           │
│ ・協調により全体として完璧になる    │
└─────────────────────────────────────┘

🚨 重要: 個別エンジンの「不完全さ」は設計上意図的！
```

### **協調処理の3戦略**
1. **Single Optimal**: シンプル文 → 最適1エンジン
2. **Foundation Plus Specialist**: 中程度 → 基盤+専門の協調
3. **Multi Cooperative**: 複雑文 → 複数エンジンの協調

### **エンジン役割分担の真実**
```
進行形エンジン: "She was running to the store"
├─ 担当: S:She, Aux:was, V:running の識別
├─ 非担当: "to the store" の詳細分析
└─ 結果: M2:"to" (不完全に見えるが正常)

前置詞句エンジン: 別の文脈または協調時に動作
├─ 担当: 前置詞句の完全な境界認識と詳細分析
└─ 協調: 進行形エンジンの M2:"to" を M2:"to the store" に補完

最終結果: 協調により完璧な統合分析を実現 ✅
```

---

## 🛑 **修正作業前の強制チェックリスト**

### **Phase 1: 設計理解確認**
- [ ] 文要素分解システム設計仕様書_v2.0_Ultimate.md を読んだ
- [ ] マルチエンジン協調システムの3戦略を理解した
- [ ] 該当エンジンの専門領域と非担当領域を把握した
- [ ] Grammar Master Controller の協調戦略を確認した

### **Phase 2: 問題分析**
- [ ] 発見した「問題」は本当に問題なのか？
- [ ] 協調システムで解決される設計上の意図的不完全さではないか？
- [ ] 修正により協調システム全体が破壊される可能性はないか？
- [ ] 単体エンジンに完璧性を求める間違った修正ではないか？

### **Phase 3: 修正実行許可**
- [ ] 上記すべてをクリアした場合のみ修正実行可能
- [ ] 修正内容が設計思想に合致していることを再確認
- [ ] 協調システムへの影響を最小限に抑える修正であることを確認

---

## 🔄 **復旧作業時の特別注意事項**

### **エンジン復旧のPriority順序 (設計仕様書準拠)**
```
Priority 0: Basic Five Pattern Engine (基盤)
Priority 1: Modal Engine (助動詞)
Priority 2: Conjunction Engine (接続詞)
Priority 3: Relative Engine (関係節) 
Priority 4: Passive Engine (受動態)
Priority 5: Progressive Engine (進行形) ← ✅ 完了
Priority 6: Prepositional Engine (前置詞句) ← 🎯 次のターゲット
...以下Priority 14まで
```

### **復旧作業の鉄則**
```
1. GitHubから正確なコードを取得
2. Rephrase的スロット分解原則に従う
3. マルチエンジン協調を前提とした実装
4. 単体の完璧性より協調適合性を優先
```

---

## 📚 **参照必須ドキュメント**

### **必読順序**
1. **文要素分解システム設計仕様書_v2.0_Ultimate.md** (最重要)
2. **Grammar Master Controller v2 のコメント** (協調システム理解)
3. **個別エンジンの実装** (専門領域把握のみ)

### **禁止行動**
- 設計仕様書を読まずに修正開始
- 個別エンジンファイルから作業を開始
- 表面的な「不完全さ」に惑されて修正
- 協調システムを無視した単独動作の強制

---

## 💡 **AI Assistant 向け行動指針**

### **会話開始時の必須ルーチン**
```python
def start_rephrase_work():
    # 1. 設計仕様書を読む
    read("文要素分解システム設計仕様書_v2.0_Ultimate.md")
    
    # 2. 協調システムを理解
    understand_multi_engine_coordination()
    
    # 3. 修正対象の役割分担を把握
    check_engine_responsibilities()
    
    # 4. この理解をユーザーに確認してもらう
    confirm_understanding_with_user()
    
    # 5. 確認後のみ作業開始
    if confirmed:
        start_actual_work()
    else:
        re_read_specifications()
```

### **修正作業時の必須確認**
```python
def before_modification():
    if not design_spec_understood:
        raise Error("設計仕様書を読め！")
    
    if not multi_engine_coordination_understood:
        raise Error("協調システムを理解しろ！")
    
    if surface_level_fix:
        raise Error("表面的修正は禁止！")
    
    if single_engine_perfectionism:
        raise Error("単体完璧主義は設計違反！")
```

---

## 🎯 **成功の鍵**

**"個別エンジンの不完全さは、協調システムの完璧性の証拠"**

この理念を忘れずに作業することで、システム破壊を防げます。

**Remember: "Rephrase is a symphony, not a solo performance"**
