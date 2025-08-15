# Unified Stanza-Rephrase Mapper 設計仕様書・開発工程表
**作成日**: 2025年8月15日  
**プロジェクト**: Rephrase英語学習システム - 統合型文法分解エンジン  
**アプローチ**: ハイブリッド方式（個別エンジン知識の統合）

---

## 📋 1. プロジェクト概要

### 1.1 目的
既存の15個別エンジンの優秀なマッピング知識を、選択不要の統合システムに再編成し、「文法検出→エンジン選択→分解」の問題を「同時並行処理」で解決する。

### 1.2 核心思想
- **Stanza解析結果 → Rephrase形式スロットの体系的マッピング**
- **選択問題の排除**: 全ハンドラーが同時実行
- **既存資産活用**: 15個別エンジンの実装知識を継承

### 1.3 アーキテクチャ
```python
class UnifiedStanzaRephraseMapper:
    def process(self, sentence):
        doc = stanza.nlp(sentence)
        result = {}
        
        # 全ハンドラーが同時実行（選択不要）
        for token in doc.sentences[0].words:
            self._handle_relative_clause(token, result)
            self._handle_passive_voice(token, result)
            self._handle_conjunction(token, result)
            # ... 全文法ハンドラー
            
        return result
```

---

## 🚀 2. 開発工程表

### Phase 0: 基盤構築 (1-2日)
```
✅ 目標: 統合ファイルの基盤とテスト環境構築
📄 成果物:
- unified_stanza_rephrase_mapper.py (基盤クラス)
- test_unified_mapper.py (段階的テストシステム)
- migration_source/ (移植元ファイル集約)

🧪 テスト項目:
- Stanzaパイプライン初期化
- 基本的な構造解析動作確認
```

### Phase 1: 関係節処理 (2-3日)  
```
✅ 目標: simple_relative_engine.py の機能移植
📄 機能:
- _handle_relative_clause() メソッド実装
- 'acl:relcl', 'nsubj', 'obj', 'nmod:poss', 'advmod' 処理
- 先行詞抽出、関係代名詞・関係副詞対応

🧪 テスト例文:
- "The car which we saw was red."
- "The man who runs is fast."  
- "The man whose car is red lives here."
- "The place where I live is Tokyo."

✅ 成功基準: 4例文すべてで正確なスロット分解
```

### Phase 2: 受動態処理 (2-3日)
```
✅ 目標: passive_voice_engine.py の機能追加
📄 機能:
- _handle_passive_voice() メソッド追加
- 'nsubj:pass', 'aux:pass', 'obl:agent' 処理
- by句の適切な配置

🧪 テスト例文:
- "The car was bought."
- "The car was bought by him."
- "The book which was read was interesting."

✅ 成功基準: 受動態単独 + 関係節との複合処理
```

### Phase 3: 接続詞処理 (2-3日)
```
✅ 目標: stanza_based_conjunction_engine.py の機能追加
📄 機能:
- _handle_conjunction() メソッド追加
- 'mark', 'advcl' 処理、意味分類(M1/M2/M3)
- 従属節と主節の適切な分離

🧪 テスト例文:
- "I came because it rained."
- "Although he is tired, he works."
- "When she arrived, I left."

✅ 成功基準: 接続詞単独 + 既存機能との複合処理
```

### Phase 4-15: 段階的機能拡張 (各2-3日)
```
Phase 4:  進行形処理      (progressive_tenses_engine.py)
Phase 5:  前置詞句処理    (prepositional_phrase_engine.py)
Phase 6:  完了進行形処理  (perfect_progressive_engine.py)
Phase 7:  分詞処理        (participle_engine.py)
Phase 8:  動名詞処理      (gerund_engine.py)
Phase 9:  不定詞処理      (infinitive_engine.py)
Phase 10: 疑問文処理      (question_formation_engine.py)
Phase 11: 仮定法処理      (subjunctive_conditional_engine.py)
Phase 12: 倒置処理        (inversion_engine.py)
Phase 13: 比較構文処理    (comparative_superlative_engine.py)
Phase 14: 基本5文型処理   (basic_five_pattern_engine.py)
Phase 15: 統合テスト・最適化
```

### Phase 16: 完成・統合 (3-5日)
```
✅ 目標: 全機能統合テスト・文書化・本番適用
📄 成果物:
- 包括的テストスイート
- パフォーマンス最適化
- 既存システムとの統合
- 運用ドキュメント

🧪 テスト項目:
- 超複雑文処理テスト
- パフォーマンステスト  
- エッジケーステスト
- 既存UI連携テスト
```

---

## 📁 3. ファイル構成

### 新規作成ファイル
```
unified_stanza_rephrase_mapper.py    # メイン統合エンジン (2000-3000行予定)
test_unified_mapper.py               # 段階的テストシステム
migration_checklist.md               # 移植チェックリスト
performance_benchmark.py             # パフォーマンス測定
```

### 移植元参照ファイル
```
migration_source/                    # 移植元ファイル集約フォルダ
├── simple_relative_engine.py
├── passive_voice_engine.py  
├── stanza_based_conjunction_engine.py
├── progressive_tenses_engine.py
├── prepositional_phrase_engine.py
└── ... (全15個別エンジン)
```

---

## ⚡ 4. 技術仕様

### 4.1 依存関係
- **Stanza**: 主要NLP解析エンジン
- **Python 3.8+**: 開発環境

### 4.2 入出力仕様
```python
# 入力
sentence: str = "The car which we saw was red."

# 出力  
result: Dict[str, str] = {
    "S": "The car",
    "V": "was", 
    "C1": "red",
    "sub-s": "we",
    "sub-v": "saw", 
    "sub-o1": "which"  # 関係代名詞情報
}
```

### 4.3 パフォーマンス目標
- **処理速度**: 1文あたり0.1-0.3秒以内
- **精度**: 基本構文95%以上、複合構文85%以上
- **メモリ使用**: 50MB以下

---

## 🎯 5. 品質保証

### 5.1 段階的テスト戦略
各Phase完了時に必須：
1. **単体テスト**: 該当文法パターンの完全動作確認
2. **統合テスト**: 既存機能との組み合わせ確認  
3. **回帰テスト**: 既存機能の劣化なし確認

### 5.2 テスト例文セット
- **基本例文**: 各文法5-10例文
- **複合例文**: 文法組み合わせ例文
- **エッジケース**: 特殊・例外的構文

---

## 🔄 6. 移行戦略

### 6.1 既存システムとの併用
開発期間中は既存システムと並行運用し、段階的に置き換え

### 6.2 フォールバック機能
統合エンジンで処理できない場合の既存システム呼び出し

---

## 📈 7. 成功指標

- ✅ **機能完全性**: 15個別エンジンの全機能移植完了
- ✅ **精度向上**: 現在のsimple_unified_integrator比20%以上向上
- ✅ **処理速度**: 現在システム同等以上
- ✅ **保守性**: 単一ファイルでの管理実現

---

**備考**: この仕様書は開発進行に応じて随時更新されます。
