# Unified Stanza-Rephrase Mapper 設計仕様書・開発工程表 (修正版)
**作成日**: 2025年8月15日  
**最終更新**: 2025年8月15日 - 統一修飾語句処理システム対応版  
**プロジェクト**: Rephrase英語学習システム - 統合型文法分解エンジン  
**アプローチ**: ハイブリッド方式（個別エンジン知識の統合 + 統一修飾語句処理）

---

## 📋 1. プロジェクト概要

### 1.1 目的
既存の個別エンジンの優秀なマッピング知識を、選択不要の統合システムに再編成し、「文法検出→エンジン選択→分解」の問題を「同時並行処理」で解決する。

### 1.2 核心思想
- **Stanza解析結果 → Rephrase形式スロットの体系的マッピング**
- **選択問題の排除**: 全ハンドラーが同時実行
- **統一修飾語句処理**: det, amod, nummod, nmod:poss, compound の一元管理
- **個別エンジン不要**: 冠詞・形容詞・数詞・所有格エンジンは統合システムで処理

### 1.3 革新的アーキテクチャ
```python
class UnifiedStanzaRephraseMapper:
    def _build_phrase_with_modifiers(self, sentence, main_word):
        """統一修飾語句処理システム - 全文法要素対応"""
        # det: 冠詞・限定詞 (a, an, the, this, that, my, your)
        # amod: 形容詞 (red, beautiful, smart)  
        # nummod: 数詞 (one, two, first, second)
        # nmod:poss: 所有格 (John's, Mary's)
        # compound: 複合名詞 (car door, school bus)
    
    def process(self, sentence):
        # 全ハンドラーが同時実行 + 統一修飾語句処理
        for handler in self.active_handlers:
            handler_result = handler(sentence)
            # 全スロットに統一修飾語句処理を適用
            self._apply_unified_modifier_system(handler_result)
```

---

## 🚀 2. 開発工程表 (実績反映版)

### Phase 0: 基盤構築 ✅ **完了**
```
✅ 成果物:
- unified_stanza_rephrase_mapper.py (基盤クラス + 統一修飾語句システム)
- 並列ハンドラー処理アーキテクチャ
- Rephrase仕様準拠ロジック (複文での正しいスロット配置)
```

### Phase 1: 関係節処理 ✅ **完了**  
```
✅ 実装済み機能:
- _handle_relative_clause() メソッド完全実装
- 全関係代名詞・関係副詞対応 (who, which, that, whose, where, when, why, how)
- 省略関係代名詞対応 (能動態・受動態・現在分詞)
- 所有格関係代名詞の文脈判定 (主語位置/目的語位置)

✅ テスト結果: 関係節テスト7/7成功
```

### Phase 2: 受動態処理 ✅ **完了**
```
✅ 実装済み機能:  
- _handle_passive_voice() メソッド実装
- 'nsubj:pass', 'aux:pass', 'obl:agent' 完全対応
- by句の適切なスロット配置

✅ テスト結果: 受動態テスト4/4成功
```

### Phase 2.5: 基本5文型処理 ✅ **完了**
```
✅ 実装済み機能:
- _handle_basic_five_pattern() メソッド実装
- 統一修飾語句処理システム (_build_phrase_with_modifiers)
- 全スロットタイプ対応 (S, V, O1, O2, C1, C2, Aux, M1, M2, M3)

✅ 革新的成果: 
- 冠詞エンジン不要化 (det処理で統合)
- 形容詞エンジン不要化 (amod処理で統合) 
- 数詞エンジン不要化 (nummod処理で統合)
- 所有格エンジン不要化 (nmod:poss処理で統合)
- 複合名詞エンジン不要化 (compound処理で統合)
```

### Phase 3: 複合文法統合テスト ✅ **完了**
```
✅ 実装済み機能:
- 複数ハンドラー同時実行
- 競合解決機能 (_merge_handler_results)
- Rephrase仕様準拠 (sub-slotsがある場合のmain slots空文字化)

✅ テスト結果: 複合文処理54/54成功 (成功率100%)
```

### Phase 4-10: 追加文法処理 🔄 **計画中**
```
🎯 実装予定 (優先順位順):
Phase 4:  接続詞処理        (advcl, mark依存関係)
Phase 5:  前置詞句処理      (obl, nmod依存関係) 
Phase 6:  進行形処理        (aux + Verb-ing パターン)
Phase 7:  完了時制処理      (aux + past_participle パターン)
Phase 8:  疑問文処理        (疑問詞 + 語順変化)
Phase 9:  不定詞処理        (to + Verb パターン)
Phase 10: 動名詞処理        (Verb-ing 主語・目的語パターン)

❌ 実装不要 (統一修飾語句システムで処理):
- 冠詞・定冠詞エンジン → det処理で統合済み
- 形容詞エンジン → amod処理で統合済み  
- 数詞エンジン → nummod処理で統合済み
- 所有格エンジン → nmod:poss処理で統合済み
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
