# Rule Dictionary v2.0 サブスロット生成システム設計仕様書

## 📋 概要

本仕様書は、Rephraseプロジェクトの新しいサブスロット生成システム（Rule Dictionary v2.0）の設計と実装を定義する。従来のパターンマッチング手法から完全に脱却し、spaCy依存構造解析を基盤とした構造的アプローチを採用する。

## 🎯 設計目標

### 1. **パターンマッチングからの完全脱却**
- ハードコードされた文字列パターンの完全排除
- spaCy依存解析（token.dep_, token.pos_, token.head, token.children）による構造的判定
- 柔軟で拡張可能な言語処理基盤の構築

### 2. **100%単語カバレッジの保証**
- 入力テキストのすべてのトークンが必ずいずれかのサブスロットに配置される
- カバレッジ検証機能による品質保証
- 未配置トークンの検出とアラート機能

### 3. **正確なRephraseルール準拠**
- 受動態処理：be動詞→sub-aux、過去分詞→sub-v
- 不定詞統合：「to + 動詞」→単一のsub-v
- サブスロット範囲：S, O1, O2, C1, C2, M1, M2, M3のみ（AuxとVは除外）

## 🏗️ システム構造

### サブスロットタイプ定義

```
9つのサブスロットタイプ:
├── sub-s    (主語サブスロット)
├── sub-aux  (助動詞サブスロット) ※Auxスロット自体には適用されない
├── sub-v    (動詞サブスロット)   ※Vスロット自体には適用されない
├── sub-o1   (目的語1サブスロット)
├── sub-o2   (目的語2サブスロット)
├── sub-c1   (補語1サブスロット)
├── sub-c2   (補語2サブスロット)
├── sub-m1   (修飾語1サブスロット)
├── sub-m2   (修飾語2サブスロット)
└── sub-m3   (修飾語3サブスロット)
```

### 適用範囲
- **サブスロット生成対象**: S, O1, O2, C1, C2, M1, M2, M3スロット
- **サブスロット生成対象外**: Aux, Vスロット（構造が単純なため）

## 🔧 実装済みサブスロットタイプ

### 1. O2サブスロット（step9_o2_subslot.py）

**目的**: 間接目的語スロット内の複雑構造分解

#### 核心技術：関係代名詞役割判定
```python
# 関係代名詞の文法的役割による分岐処理
if rel_pronoun_role == "nsubj":    # 主語役割
    # "anyone who wants to learn" → sub-s: 'anyone who'
    
elif rel_pronoun_role == "dobj":   # 目的語役割  
    # "the person that I met" → sub-o1: 'the person that'
```

#### テスト結果例
```
"anyone who wants to learn"
├── sub-s: 'anyone who'
├── sub-v: 'wants' 
└── sub-o1: 'to learn'
カバレッジ: 100.0% (5/5)

"the person that I met yesterday"
├── sub-o1: 'the person that'
├── sub-s: 'I'
├── sub-v: 'met'
└── sub-m1: 'yesterday'
カバレッジ: 100.0% (6/6)
```

#### 技術的特徴
- **依存関係ラベル活用**: nsubj, dobj, relclによる構造判定
- **相対節解析**: 関係代名詞の文法的機能の正確な特定
- **完全カバレッジ**: すべてのトークンの適切な配置

### 2. C1サブスロット（step10_c1_subslot.py）

**目的**: 補語1スロット内の複雑構造分解（第2文型SVC・第5文型SVOCの補語処理）

#### 核心技術1：受動態処理
```python
# Rephraseルール: 受動態のbe動詞は助動詞扱い
"the leader who is very experienced"
├── sub-s: 'the leader who'      # 関係代名詞付き主語
├── sub-aux: 'is'                # be動詞→助動詞として処理
├── sub-v: 'experienced'         # 過去分詞→実質動詞として処理
└── sub-m2: 'very'               # 副詞修飾語
```

#### 核心技術2：不定詞統合処理
```python
# Rephraseルール: 「to + 動詞」は一つのsub-vとして統合
"to be successful"
├── sub-v: 'to be'               # 不定詞統合
└── sub-c1: 'successful'         # 補語
```

#### 核心技術3：前置詞句分離処理
```python
# 補語の核と修飾語の適切な分離
"to be successful in business"
├── sub-v: 'to be'
├── sub-c1: 'successful'         # 補語の核のみ
└── sub-m3: 'in business'        # 前置詞句は別途修飾語として
```

#### 核心技術4：what節特殊処理
```python
# サブスロットのサブスロット回避のための便宜的分離
"what I want to become"
├── sub-o2: 'what'               # 本来はbecomeの目的語だが便宜的にo2
├── sub-s: 'I'
├── sub-v: 'want'
└── sub-o1: 'to become'          # 便宜的にo1として分離
```

## 🚨 サブスロット分離・サブサブ構造回避方法

### 問題：Rephraseではサブスロットのサブスロットは存在しない

Rephraseシステムの制約により、サブスロット内でさらに細分化されたサブスロット（サブサブスロット）は作成できない。このため、複雑な構造を便宜的に分離する手法が必要となる。

### 解決策1：便宜的なo1/o2分離

#### 例：what節の処理
```
元の文法構造: "what I want to become"
├── what: becomeの本来の目的語（文法的に正確）
├── I want to become: 関係節

Rephraseでの処理（便宜的分離）:
├── sub-o2: 'what'          # 本来の文法関係を保持しつつo2に配置
├── sub-s: 'I'              
├── sub-v: 'want'
└── sub-o1: 'to become'     # 便宜的にo1として分離
```

#### 理由と効果
- **文法的正確性**: whatは本来becomeの目的語だが、サブサブスロット禁止により分離
- **学習者理解**: 各要素が独立して認識可能
- **システム制約対応**: Rephraseの技術的制限内で最適解を提供

### 解決策2：修飾語階層分離（m2/m3分離）

#### 例：形容詞的用法での複雑分離
```
"material to make examination out of"

文法的構造:
├── material: 修飾される名詞
├── to make examination out of material: 形容詞節（本来は一体）

Rephraseでの処理（便宜的階層分離）:
├── sub-m2: 'material'       # 便宜的にm2配置
├── sub-v: 'to make'
├── sub-o1: 'examination'
└── sub-m3: 'out of'         # 本来は"out of material"だが分離
```

#### 例：副詞的用法での分離
```
"vocabulary to memorize for the test"

Rephraseでの処理:
├── sub-o1: 'vocabulary'     
├── sub-v: 'to memorize'
└── sub-m3: 'for the test'   # 目的を表す前置詞句
```


### 分離判定基準

#### 1. 文法的依存関係の優先
- spaCyの依存解析結果（token.dep_）を基準とする
- 主要な文法関係（nsubj, dobj, acomp, prep等）に基づく分類

#### 2. Rephraseシステム制約の考慮
- サブサブスロット禁止制約
- 学習者の理解可能性
- システムの技術的制限

#### 3. 便宜的分離の優先順位
```
優先順位1: 文法的核の保持（主語、動詞、目的語、補語の核）
優先順位2: 修飾関係の階層化（m1 < m2 < m3）
優先順位3: 学習者理解の最適化（意味単位での分離）
```

## 🔍 品質保証システム

### カバレッジ検証機能
```python
def _check_complete_coverage(self, original_text, subslots):
    """全単語カバレッジ検証"""
    doc = self.nlp(original_text)
    all_tokens = [(token.text, token.i) for token in doc]
    
    covered_indices = set()
    for subslot_data in subslots.values():
        if 'token_indices' in subslot_data:
            covered_indices.update(subslot_data['token_indices'])
    
    missing_tokens = [(text, idx) for text, idx in all_tokens if idx not in covered_indices]
    
    return {
        'total_tokens': len(all_tokens),
        'covered_tokens': len(covered_indices),
        'missing_tokens': missing_tokens,
        'coverage_rate': len(covered_indices) / len(all_tokens) if all_tokens else 0,
        'is_complete': len(missing_tokens) == 0
    }
```

### 品質指標
- **完全カバレッジ率**: 100.0%必須
- **未配置トークン検出**: missing_tokensによるアラート
- **構造整合性**: spaCy依存解析との一致性検証

## 🎯 実装状況

### ✅ 完了済み
- **O2サブスロット**: 関係代名詞役割判定、完全カバレッジ対応
- **C1サブスロット**: 受動態処理、不定詞統合、前置詞句分離、what節特殊処理

### 🔄 実装予定
- **C2サブスロット**: 第5文型補語2の特殊処理
- **M2サブスロット**: 副詞修飾語の階層処理  
- **M3サブスロット**: 前置詞句修飾語の構造処理

### 📅 統合予定
- 既存JSONデータとの統合
- 語順制御システムとの連携
- 大規模テストとパフォーマンス最適化

## 🛠️ 技術基盤

### 依存ライブラリ
- **spaCy**: 英語依存構造解析 (`en_core_web_sm`)
- **Python 3.10+**: 型ヒントとモダンシンタックス対応

### 核心技術
- **依存構造解析**: token.dep_, token.pos_, token.head, token.children
- **構造トラバース**: token.subtreeによる部分木探索
- **トークンインデックス管理**: 完全カバレッジ検証のための位置追跡

## 📝 変更履歴

### v2.0.1 (2025-08-10)
- **受動態処理ルール確定**: be動詞→sub-aux、過去分詞→sub-v
- **不定詞統合処理**: 「to + 動詞」の単一sub-v化
- **前置詞句分離**: 補語核とmodifier分離によるsub-c1/sub-m3適切配置
- **what節便宜的分離**: サブサブスロット制約回避のためのo1/o2分離

### v2.0.0 (2025-08-10)
- **パターンマッチング完全廃止**: 全ロジックをspaCy依存解析ベースに変更
- **100%カバレッジシステム**: 未配置トークン検出機能実装
- **サブスロット範囲確定**: Aux/V除外、8スロットタイプのみ適用

## 🎯 今後の展開

### 短期目標
1. **残りサブスロット実装**: C2, M2, M3の完成
2. **統合テスト**: 全サブスロットタイプの協調動作確認
3. **パフォーマンス最適化**: 大規模データでの処理速度向上

### 中期目標
1. **既存システム統合**: JSON構造との完全互換性確保
2. **語順制御統合**: slot_order_data.jsonとの連携
3. **本番環境デプロイ**: プロダクション品質の保証

### 長期目標
1. **多言語対応**: 他言語spaCyモデルとの統合
2. **AI学習データ生成**: 高品質な訓練データ自動生成
3. **リアルタイム処理**: WebアプリケーションでのAPI提供

---

*本仕様書は実装の進捗に合わせて継続的に更新される。*
