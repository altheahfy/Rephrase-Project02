# 新規文法分解システム 設計仕様書 v1.0

**作成日**: 2025年8月26日  
**対象**: Rephrase文法分解システム 完全新規実装  
**目標精度**: 段階的100%達成（5文型→関係節→受動態の順）

---

## 🚨 【重要】新規開発者への注意事項

### ⚠️ 必読事項
本仕様書に基づく開発を開始する前に、以下を必ず理解してください：

1. **🔥 完全新規実装**: 既存システム（dynamic_grammar_mapper.py等）のコード継承・依存は**絶対禁止**
2. **🎯 専門分担型ハイブリッド解析**: 品詞分析と依存関係を得意分野に応じて専門分担使用
3. **🧠 Human Grammar Pattern**: 人間文法認識ベースの設計思想を理解することが**必須**
4. **📊 段階的100%精度**: 86.1%維持ではなく段階的100%達成が**絶対目標**
5. **🏗️ Central Controller**: 文法処理は各ハンドラーに委任、直接処理は**禁止**

### 🎯 開発目標の明確化
- **❌ 間違った目標**: 既存システムの修正・改良・86.1%精度維持
- **✅ 正しい目標**: 完全新規システムで段階的100%精度達成

### 📚 技術方針の確認（専門分担型ハイブリッド解析）

#### ✅ **品詞分析専門分野**
- **副詞検出**: `token.pos_ == 'ADV'`で100%精度達成
- **受動態パターン**: be動詞 + `token.tag_ == 'VBN'`で確実な検出
- **単純文動詞**: 関係節のない文での主動詞特定
- **完了形助動詞**: has/have + 過去分詞の判定

#### ✅ **依存関係専門分野**  
- **複文主動詞**: `token.dep_ == 'ROOT'`での確実な検出
- **関係節構造**: `token.dep_ == 'relcl'`での関係節動詞識別
- **文構造理解**: 主節と従属節の区別

#### ⚠️ **透明性確保原則**
- 使用箇所と理由を明示的に文書化
- どの手法をなぜ使うかコメントで明記
- デバッグ時の追跡可能性を保証

#### ❌ **使用禁止技術**
- Stanza、既存コードの流用、過度なハードコーディング

### 🔧 実装アプローチ
- **Phase 1**: Central Controller + BasicFivePatternHandler（5文型のみ、100%精度）
- **Phase 2**: RelativeClauseHandler追加（関係節対応）
- **Phase 3**: PassiveVoiceHandler追加（受動態対応）

---

## 1. 開発思想・方針

### 1.1 核心思想
**「中央管理システム + 個別文法ハンドラー」による効率的Rephrase文法分解システム**

- **Central Controller**: 文法解析実施→使用文法項目特定→各ハンドラーに順次分解指示→結果統合・order管理
- **Specialized Handlers**: 各文法要素の専門分解のみ担当（中央管理システムとのみ接続）
- **Human Grammar Recognition**: spaCyの品詞分析結果を情報源に、人間がパターン認識で文法体系を構築しそれに沿って言語を理解するように、文の全体構造からパターンと照合して分解する汎用的機能の集合体

（具体例）
「文法解析を実施し、使われている文法項目を特定、それぞれのハンドラーに順次分解を指示。まずは関係節ハンドラーに指示して節構造を分ける」「関係節ハンドラーが分解したサブスロット（代表語句以外にマスク）と上位スロットの対応構造を整理・保存」「order管理」「5文型ハンドラーにそれぞれをフラットに処理させ、上位とサブの配置、サブ要素がある上位を””にする、などの整理」「各個別ハンドラーは中央管理システムとのみ接続し、情報は中央管理システムのみから取得、処理結果も中央管理システムに渡す」

### 1.2 設計原則（修正版 - 協力アプローチ採用）
1. **Single Responsibility Principle**: 各コンポーネントは単一の責任のみ（協力は例外として許可）
2. **Controlled Cooperation**: 必要時のみハンドラー間協力、完了後は中央報告
3. **Information Centralization**: 最終的に全情報はCentralControllerが管理
4. **Dependency Injection**: 協力者はコンストラクタで注入、疎結合を維持
5. **Human Grammar Pattern**: spaCy品詞分析を情報源とし、人間が文法体系を構築するように全体構造からパターン照合
6. **Generic Design**: 個別事例対応ではなく同種ケース全てに機能する汎用設計
7. **Hard-coding Prohibition**: どうしても他に方法がない場合以外はハードコーディング禁止
8. **Zero Technical Debt**: 技術負債を発生させない

---

## 1.3 実際の進捗状況（2025年8月26日時点）

### 📊 開発実績サマリー
- **開発期間**: 2025年8月26日開始
- **現在フェーズ**: Phase 2（関係節処理）
- **到達精度**: 41.7%（関係節テスト12ケース中5ケース成功）
- **実装済み**: Central Controller + BasicFivePatternHandler + RelativeClauseHandler（基本）

### ✅ Phase 1完了実績（8月26日）
**Central Controller + BasicFivePatternHandler**
- ✅ **spaCy文脈解析基盤**: `en_core_web_sm`による文全体解析
- ✅ **5文型判定システム**: SV/SVC/SVO/SVOO/SVOC の完全対応
- ✅ **設計仕様書準拠**: マスク処理・簡略文作成・S空文字列化戦略
- ✅ **統合制御アーキテクチャ**: 各ハンドラーとの適切な連携
- ✅ **責任分担の実現**: 中央制御 vs 専門ハンドラーの明確な分離

### 🔧 Phase 2進行中実績（8月26日）
**RelativeClauseHandler 開発**

#### 重要な設計改善
- **❌ 問題発見**: Legacy参考時のハードコーディング動詞リスト
- **✅ 改善実施**: spaCy単語単位判定 → spaCy文脈解析に完全移行
- **✅ 品詞分析最適化**: `_is_likely_verb(word)` → `_analyze_relative_clause(text)`

#### 実装完了項目
- ✅ **spaCy文脈解析ベース**: 文全体解析による関係節特定
- ✅ **関係代名詞対応**: who/which/that/whom/whose の基本処理
- ✅ **sub-slots生成**: 関係節構造の適切な分離
- ✅ **設計仕様書準拠**: `_parent_slot`等の必須フィールド実装

#### テスト結果詳細
**成功ケース（5/12 = 41.7%）:**
1. ✅ ケース3: "The man who runs fast is strong."
2. ✅ ケース5: "The person that works here is kind."
3. ✅ ケース6: "The book which I bought is expensive."
4. ✅ ケース7: "The man whom I met is tall."
5. ✅ ケース8: "The car that he drives is new."

**失敗ケース分析:**
- **受動態問題**: ケース9,10,11（`was crashed` → PassiveVoiceHandlerの責任）
- **修飾語分離**: ケース4（`lies there` → AdverbHandlerの責任）
- **whose複雑構文**: ケース12,13,14（構造理解の改善必要）

### 🎯 次期開発方針（責任分担原則の徹底）
**重要な設計判断**: 関係節ハンドラー内での修飾語処理実装を**責任分団原則違反**として却下

#### 🤝 ハンドラー協力アプローチの正式採用（設計方針確定）
**実装検証の結果**: 関係節の正確な境界決定には関係節内部の完全な5文型理解と受動態処理が必要

**確定設計: ハンドラー協力パターン + 中央報告**
```python
class RelativeClauseHandler:
    def __init__(self, collaborators=None):
        # 協力者への参照（Dependency Injection）
        self.five_pattern_handler = collaborators.get('five_pattern')
        self.adverb_handler = collaborators.get('adverb')
        self.passive_handler = collaborators.get('passive')  # 追加
        
    def process(self, text):
        # 協力者と連携して複雑な文法構造を処理
        # ...協力処理...
        
        # 重要: 全情報をCentralControllerに報告
        return {
            'success': True,
            'main_slots': {...},
            'sub_slots': {...},
            'cooperation_details': {
                'adverb_analysis': {...},
                'passive_analysis': {...},
                'structure_analysis': {...}
            }
        }
```

**協力アプローチの利点（実証済み）:**
- ✅ **Dependency Injection**: 依存性注入による疎結合設計
- ✅ **情報統合**: 協力結果の完全な中央報告
- ✅ **責任分担維持**: 各ハンドラーの専門性を保持
- ✅ **効率性**: 自然言語処理の並行処理に適合
- ✅ **拡張性**: 新しい協力関係の容易な追加

**従来の「内包」アプローチとの比較:**
- ❌ 内包: `self.five_pattern = BasicFivePatternHandler()` → 重複インスタンス
- ✅ 協力: `self.five_pattern_handler = five_pattern_handler` → 参照渡し

#### 即時実施予定
1. **AdverbHandler/ModifierHandler 優先開発** ✅ **完了**
   - 目的: `runs fast`/`lies there`/`works here` の適切な分離
   - 効果: 関係節ハンドラーが修飾語の正確な分離結果を利用可能

2. **ハンドラー協力アプローチの実装** 🔄 **実施中**
   - **設計思想**: Dependency Injection による協力関係構築
   - **実装方針**: 内包ではなく参照渡しによる疎結合設計
   
   **関係節ハンドラーの協力関係:**
   ```python
   class RelativeClauseHandler:
       def __init__(self, collaborators=None):
           self.adverb_handler = collaborators.get('adverb')      # 修飾語分離協力
           self.five_pattern_handler = collaborators.get('five_pattern')  # 5文型分析協力
           self.passive_handler = collaborators.get('passive')    # 受動態理解協力
           
       def _analyze_relative_clause_structure(self, clause_text):
           # 1. 副詞ハンドラーと協力：修飾語分離
           if self.adverb_handler:
               adverb_result = self.adverb_handler.process(clause_text)
           
           # 2. 5文型ハンドラーと協力：構造分析
           if self.five_pattern_handler:
               structure = self.five_pattern_handler.process(cleaned_clause)
           
           # 3. 統合された完全な関係節理解を構築
           return self._integrate_analysis_results(adverb_result, structure)
   ```

   **CentralController での協力者注入:**
   ```python
   class CentralController:
       def __init__(self):
           self.adverb_handler = AdverbHandler()
           self.five_pattern_handler = BasicFivePatternHandler()
           
           collaborators = {
               'adverb': self.adverb_handler,
               'five_pattern': self.five_pattern_handler
           }
           self.relative_handler = RelativeClauseHandler(collaborators)
   ```

3. **修正された実装順序** 🔄 **設計検討中**
   - **従来順序**: `関係節 → 5文型 → 受動態 → 修飾語`
   - **改善提案**: `修飾語 → 関係節 → 5文型 → 受動態` (依存関係順)
   - **協力アプローチ**: 順序に依存せず、必要時に協力者を呼び出し
   
### 📋 技術的成果・教訓
1. **spaCy活用方針の確立**: 単語単位→文脈解析への移行成功
2. **責任分担原則の重要性**: 機能バッティング回避のための厳格な原則適用
3. **設計仕様書の価値**: 関係節処理例の詳細記述が実装指針として有効
4. **段階的開発の効果**: Phase別実装によるエラー局所化・品質向上

---

## 2. システム要件（既存システム分析結果）

### 2.1 機能要件
- **入力**: 英語文（文字列）
- **出力**: Rephraseスロット形式のJSONオブジェクト（slot_order_data.json準拠）
  ```json
  {
    "main_slots": {"S": "主語", "V": "動詞", "O1": "目的語", "M2": "修飾語"},
    "sub_slots": {"sub-s": "関係節主語", "sub-v": "関係節動詞", "_parent_slot": "S"}
  }

  （最終成果物具体例）
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M1",
    "SlotPhrase": "that afternoon at the crucial point in the presentation",
    "SlotText": "あの、～の時点・地点で、～の中に、～の中で",
    "PhraseType": "word",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 1,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "S",
    "SlotPhrase": "the manager who had recently taken charge of the project",
    "SlotText": "最近",
    "PhraseType": "clause",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 2,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "S",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-s",
    "SubslotElement": "the manager who",
    "SubslotText": "",
    "Slot_display_order": 2,
    "display_order": 1,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "S",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-aux",
    "SubslotElement": "had",
    "SubslotText": "過去完了",
    "Slot_display_order": 2,
    "display_order": 2,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "S",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-m2",
    "SubslotElement": "recently",
    "SubslotText": "最近",
    "Slot_display_order": 2,
    "display_order": 3,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "S",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-v",
    "SubslotElement": "taken",
    "SubslotText": "",
    "Slot_display_order": 2,
    "display_order": 4,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "S",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-o1",
    "SubslotElement": "charge of the project",
    "SubslotText": "",
    "Slot_display_order": 2,
    "display_order": 5,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "Aux",
    "SlotPhrase": "had to",
    "SlotText": "～しなければならなかった",
    "PhraseType": "word",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 3,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "V",
    "SlotPhrase": "make",
    "SlotText": "",
    "PhraseType": "word",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 4,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "O1",
    "SlotPhrase": "the committee responsible for implementation",
    "SlotText": "～のために",
    "PhraseType": "word",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 6,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "C2",
    "SlotPhrase": "deliver the final proposal flawlessly",
    "SlotText": "",
    "PhraseType": "phrase",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 7,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "C2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-v",
    "SubslotElement": "deliver",
    "SubslotText": "",
    "Slot_display_order": 7,
    "display_order": 1,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "C2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-o1",
    "SubslotElement": "the final proposal",
    "SubslotText": "",
    "Slot_display_order": 7,
    "display_order": 2,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "C2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-m3",
    "SubslotElement": "flawlessly",
    "SubslotText": "",
    "Slot_display_order": 7,
    "display_order": 3,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M2",
    "SlotPhrase": "even though he was under intense pressure",
    "SlotText": "たとえ～でも、～の下・元で",
    "PhraseType": "clause",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 5,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-m1",
    "SubslotElement": "even though",
    "SubslotText": "たとえ～でも",
    "Slot_display_order": 5,
    "display_order": 1,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-s",
    "SubslotElement": "he",
    "SubslotText": "",
    "Slot_display_order": 5,
    "display_order": 2,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-v",
    "SubslotElement": "was",
    "SubslotText": "be動詞過去、進行形のbe動詞",
    "Slot_display_order": 5,
    "display_order": 3,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M2",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-m2",
    "SubslotElement": "under intense pressure",
    "SubslotText": "～の下・元で",
    "Slot_display_order": 5,
    "display_order": 4,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M3",
    "SlotPhrase": "so the outcome would reflect their full potential",
    "SlotText": "だから、過去から未来を推量、彼らの",
    "PhraseType": "clause",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 8,
    "display_order": 0,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M3",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-m1",
    "SubslotElement": "so",
    "SubslotText": "だから",
    "Slot_display_order": 8,
    "display_order": 1,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M3",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-s",
    "SubslotElement": "the outcome",
    "SubslotText": "",
    "Slot_display_order": 8,
    "display_order": 2,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M3",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-aux",
    "SubslotElement": "would",
    "SubslotText": "過去から未来を推量",
    "Slot_display_order": 8,
    "display_order": 3,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M3",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-v",
    "SubslotElement": "reflect",
    "SubslotText": "",
    "Slot_display_order": 8,
    "display_order": 4,
    "QuestionType": ""
  },
  {
    "構文ID": "",
    "V_group_key": "make",
    "例文ID": "ex007",
    "Slot": "M3",
    "SlotPhrase": "",
    "SlotText": "",
    "PhraseType": "",
    "SubslotID": "sub-o1",
    "SubslotElement": "the full potential",
    "SubslotText": "",
    "Slot_display_order": 8,
    "display_order": 5,
    "QuestionType": ""
  },
  ```

### 2.2 Rephrase的スロット構造（絶対遵守）
#### 上位スロット（固定10スロット）
【S位置のサブスロット群】
S-sub-m1, S-sub-s, S-sub-aux, S-sub-m2, S-sub-v, S-sub-c1, S-sub-o1, S-sub-o2, S-sub-c2, S-sub-m3

【M1位置のサブスロット群】  
M1-sub-m1, M1-sub-s, M1-sub-aux, M1-sub-m2, M1-sub-v, M1-sub-c1, M1-sub-o1, M1-sub-o2, M1-sub-c2, M1-sub-m3

【M2位置のサブスロット群】
M2-sub-m1, M2-sub-s, M2-sub-aux, M2-sub-m2, M2-sub-v, M2-sub-c1, M2-sub-o1, M2-sub-o2, M2-sub-c2, M2-sub-m3

... (O1, O2, C1, C2, M3も同様)
```

**❌ 絶対に間違った理解：**
- `sub-m2` がM2のサブスロット ← **大間違い！**
- `sub-v` がVのサブスロット ← **大間違い！**
- 全スロットで共通のサブスロット群 ← **大間違い！**

**✅ 正しい理解：**
- `S-sub-m2` はSスロットのサブスロット
- `M2-sub-v` はM2スロットのサブスロット  
- `O1-sub-s` はO1スロットのサブスロット
- **各上位スロットが独立した10個のサブスロットを持つ**

#### 重要なRephrase的ルール
1. **関係詞処理**: 先行詞と関係代名詞をセットでsub-sに格納
   - ❌ 間違い: `S: "The man", sub-s: "who"`
   - ✅ 正解: `S: "", sub-s: "The man who"`

2. **重複排除**: サブスロット要素がある上位スロットは`""`とする（Rephraseではスロットに入れた要素を並べて例文を表示するので、重複や抜けがあると成立しない）
   - 例: `"The man who runs"` → `S: "", sub-s: "The man who", sub-v: "runs"`

3. **Mスロット配置**: 個数ベース超シンプルルール
   - 1個のみ → M2
   - 2個 → 動詞前後で M1+M2 または M2+M3
   - 3個 → M1, M2, M3

### 2.3 性能要件
- **精度**: 段階的100%達成
  - Phase 1: 5文型のみで100%
  - Phase 2: 5文型+関係節で100%  
  - Phase 3: 5文型+関係節+受動態で100%
- **処理時間**: 文あたり1秒以内
- **メモリ使用量**: 1GB以内

### 2.4 対応文法要素（全文法対応）

#### Phase 1実装（参考設計有り）
1. **基本5文型**: SV, SVC, SVO, SVOO, SVOC
2. **関係節**: who/which/that節  
3. **受動態**: be + 過去分詞構造
4. **修飾語**: 副詞・前置詞句の適切な配置

#### 既存エンジン参考可能（dynamic_grammar_mapper.py未実装だがunified_stanza_rephrase_mapper.pyには実装していた）
5. **接続詞**: stanza_based_conjunction_engine
6. **前置詞句**: prepositional_phrase_engine  
7. **不定詞**: infinitive_engine
8. **動名詞**: gerund_engine
9. **分詞**: participle_engine
10. **完了進行**: perfect_progressive_engine
11. **モーダル**: modal_engine
12. **比較級**: comparative_superlative_engine
13. **倒置**: inversion_engine
14. **疑問文**: question_formation_engine
15. **命令文**: imperative_engine
16. **仮定法**: subjunctive_conditional_engine
17. **存在文**: existential_there_engine

---

## 3. アーキテクチャ設計

### 3.1 Central Controller詳細責任
1. **文法解析実施**: spaCy解析で使用文法項目を特定
2. **順次分解指示**: まず関係節ハンドラーで節構造分離
3. **構造整理保存**: 関係節分解結果（サブスロット+代表語句マスク）保存
4. **order管理**: スロット表示順序の管理
5. **5文型処理**: 各文をフラットに5文型ハンドラーに処理指示
6. **結果統合**: サブ要素がある上位スロットを`""`に設定等の最終整理

### 3.2 データフロー
```
Input → spaCy Parse → 文法項目特定 → 関係節Handler → 構造保存 → 
5文型Handler → 受動態Handler → 修飾語Handler → 結果統合 → Output
```

### 3.3 ハンドラー接続原則
- **各ハンドラーは中央管理システムとのみ接続**
- **情報は中央管理システムのみから取得**
- **処理結果も中央管理システムに渡す**
- **ハンドラー間の直接通信は禁止**

---

## 4. 人間文法認識の具体的実装思想

### 4.1 人間的パターン認識例
#### 例1: 関係節境界認識
```
"The man who has a red car lives here."

→ spaCy解析: who_sub-s → has_sub-v → a red car_sub-o1 → lives

→ 人間的判断: またVが出現 → その一つ前のcarで関係節終了 → 主部動詞に復帰
```

#### 例2: 曖昧語句解決
```
"The man whose car is red lives here."

→ spaCy誤判定: livesを名詞life複数形と判定
→ システム警戒: 曖昧語句として2選択肢を準備
→ 第1候補: lives_名詞 → 上位スロットゼロで文法破綻
→ 第2候補: lives_動詞 → redで関係節終了 → lives_V, here_M2で文成立
→ 判断: 第2候補が正しい
```

#### 例3: マスク処理による5文型ハンドラー支援
```
"The man who runs fast lives here."

→ 関係節ハンドラー処理: 代表語句"The man"選定 → 他をマスク
→ 中央管理システム: "The man lives here."を5文型ハンドラーに渡す
→ 5文型ハンドラー: 混乱なく S="The man", V="lives", M2="here"と分解
→ 中央管理システム: サブ要素がある上位Sを""に設定
```

### 4.2 有用な手法抽出（コードではなく考え方）

#### 従来システムから学ぶ手法
1. **段階的処理順序**: 関係節除外→コア要素特定→修飾語配置
2. **テストケース網羅性**: 基本文型・関係節・受動態の組み合わせ
3. **エラーハンドリング**: 個別ハンドラー失敗が全体に影響しない設計
4. **結果形式**: main_slots + sub_slotsの分離構造

#### 回避すべき問題
- **依存関係解析の使用**: spaCy dep_関係はRephrase翻訳が困難なため使用禁止
- **二重処理**: 同一処理を複数箇所で実行
- **責任境界の曖昧さ**: Central Controllerでの直接文法処理
- **ハードコーディング**: 個別事例対応の固定値

---

## 5. 実装工程計画

### Phase 1: 基盤構築（2日）
- [ ] spaCy統合・基本クラス設計
- [ ] CentralController基本フレームワーク
- [ ] テストハーネス構築
- [ ] 既存テストケース移行

### Phase 2: コアハンドラー実装（4日）
- [ ] BasicFivePatternHandler実装
- [ ] 基本5文型テストケース検証
- [ ] 精度測定システム構築

### Phase 3: 拡張ハンドラー実装（3日）
- [ ] RelativeClauseHandler実装
- [ ] PassiveVoiceHandler実装
- [ ] 関係節・受動態テストケース検証

### Phase 4: 統合・最適化（2日）
- [ ] ModifierHandler実装
- [ ] ResultIntegrator完成
- [ ] 全テストケース検証
- [ ] 100%精度達成確認

### Phase 5: 品質保証（1日）
- [ ] コードレビュー
- [ ] パフォーマンステスト
- [ ] ドキュメント整備

**総開発期間: 12日**

## 5. 既存エンジンの設計コンセプト参考（技術実装ではなく発想のみ）

### 5.1 Basic Five Pattern Engine のコンセプト
**核心アイデア**: 
- **統一境界拡張の概念**: 単語レベル検出から適切な句レベルへの拡張処理
- **スロット別最適化**: S、V、O、Cごとに異なる拡張ルール適用
- **知識ベース継承方式**: 過去エンジンの成功パターンを体系的に集約

**新システムへの応用価値**:
- 単語→句への2段階拡張処理の考え方
- スロット特性に応じた処理分岐設計
- 成功パターンの体系的蓄積・活用手法

### 5.2 Simple Relative Engine のコンセプト
**核心アイデア**:
- **先行詞+関係代名詞結合原則**: 分離せずセットで管理
- **余計な再帰処理排除**: シンプルな直接処理による複雑性回避
- **段階的処理**: 関係節検出→要素特定→結合の明確な処理段階

**新システムへの応用価値**:
- 関係節境界の明確な特定手法の考え方
- 先行詞保持とマスキング処理の概念
- 段階的処理による複雑性管理手法

### 5.3 Passive Voice Engine のコンセプト  
**核心アイデア**:
- **統合処理方式**: 上位スロット配置+サブスロット分解を単一処理で実行
- **受動態タイプ別分岐**: 単純受動態 vs by句付きで処理方法変更
- **Auxスロット活用**: 助動詞の独立スロット管理による明確な構造化

**新システムへの応用価値**:
- 文法タイプ別の処理分岐設計思想
- 助動詞の独立管理による構造明確化
- 統合処理による情報保持とデバッグ効率両立

### 5.4 Modal Engine のコンセプト
**核心アイデア**:
- **段階的モーダル処理**: 検出→分類→配置の3段階
- **意味カテゴリ別分類**: possibility, necessity, permission等での体系化
- **複合モーダル対応**: 複数モーダルの組み合わせへの対応

**新システムへの応用価値**:
- 意味的分類による処理分岐の考え方
- 複合構造への段階的アプローチ
- 文脈依存処理の体系化手法

### 5.5 Question Formation Engine のコンセプト
**核心アイデア**:
- **疑問文タイプ体系化**: Wh疑問文、Yes/No疑問文等の明確な分類
- **倒置構造正規化**: 語順変更された構造の標準形への変換
- **疑問詞スロット配置**: 疑問詞の適切な位置への体系的配置

**新システムへの応用価値**:
- 構造変化への対応方式の考え方
- 語順変更の系統的処理手法
- 特殊構造の正規化アプローチ

---

## 6. 専門分担型ハイブリッド解析の詳細設計

### 6.1 設計決定の経緯と根拠

#### 🔍 **技術検証結果**（2025年8月28日決定）
実証テストにより以下が判明：

1. **品詞のみアプローチ**: 80%精度（4/5ケース成功）
   - ✅ 単純文、受動態、副詞検出で100%精度
   - ❌ 関係節含む複文で33%精度（1/3ケース失敗）

2. **依存関係のみアプローチ**: 100%精度（5/5ケース成功）
   - ✅ 複文構造の正確な理解
   - ❌ ブラックボックス性、保守困難

3. **専門分担型ハイブリッド**: 100%精度 + 透明性確保
   - ✅ 各手法を得意分野で活用
   - ✅ 判定過程の完全な追跡可能性

#### 📊 **精度比較実証データ**
```
テストケース分析結果:
- 'The book which lies there is mine.' → 両手法で正解
- 'The man who runs fast is strong.' → 品詞のみ失敗、依存関係成功
- 'Tomorrow I study.' → 両手法で正解
- 'He has finished his homework.' → 両手法で正解
- 'The teacher whose class runs efficiently is respected greatly.' → 両手法で正解

結論: 複文における主動詞検出で依存関係の優位性が実証
```

### 6.2 専門分担マップ（確定版）

#### ✅ **品詞分析専門分野**

| **処理タスク** | **使用技術** | **精度** | **理由** |
|---|---|---|---|
| 副詞検出 | `token.pos_ == 'ADV'` | 100% | パターンが明確 |
| 受動態パターン | be動詞 + `token.tag_ == 'VBN'` | 100% | 構造が単純 |
| 単純文動詞 | `token.pos_ == 'VERB'` | 100% | 複雑性なし |
| 完了形助動詞 | `token.pos_ == 'AUX'` + 位置 | 100% | 語順固定 |

#### ✅ **依存関係専門分野**

| **処理タスク** | **使用技術** | **精度** | **理由** |
|---|---|---|---|
| 複文主動詞 | `token.dep_ == 'ROOT'` | 100% | 構造理解必須 |
| 関係節識別 | `token.dep_ == 'relcl'` | 100% | 節境界確定 |
| 主語特定 | `token.dep_ in ['nsubj', 'nsubjpass']` | 95% | 修飾語範囲制限 |

### 6.3 透明性確保実装ガイドライン

#### 🔍 **必須ログ出力**
```python
# 良い例: 透明性を確保した実装
def find_main_verb_transparent(doc, sentence):
    """主動詞検出 - 透明性確保版"""
    
    # Step 1: 文の複雑性判定
    rel_pronouns = ['who', 'which', 'that', 'whose']
    has_relative = any(token.text.lower() in rel_pronouns for token in doc)
    
    if has_relative:
        # 複文: 依存関係使用（理由をログ出力）
        for token in doc:
            if token.dep_ == 'ROOT':
                print(f"🔍 複文主動詞: '{sentence}' → '{token.text}' (依存関係使用: 関係節構造のため)")
                return token.i
    else:
        # 単純文: 品詞使用（理由をログ出力）
        verbs = [token for token in doc if token.pos_ == 'VERB']
        if verbs:
            main_verb = verbs[-1]
            print(f"🔍 単純文主動詞: '{sentence}' → '{main_verb.text}' (品詞使用: 単純構造のため)")
            return main_verb.i
    
    return None
```

#### ❌ **悪い例: 不透明な実装**
```python
def find_main_verb_opaque(doc):
    """透明性に欠ける実装例"""
    for token in doc:
        if token.dep_ == 'ROOT':  # なぜ依存関係を使うか不明
            return token.i
    return None
```

### 6.4 ハンドラー別実装方針

#### **AdverbHandler**
- **専門分野**: 副詞検出・分離
- **使用技術**: 品詞分析のみ（`token.pos_ == 'ADV'`）
- **理由**: 副詞の品詞判定は100%精度で信頼性高い

#### **PassiveVoiceHandler**  
- **専門分野**: 受動態パターン検出
- **使用技術**: 品詞分析のみ（be動詞 + `VBN`タグ）
- **理由**: パターンが明確で品詞だけで十分

#### **RelativeClauseHandler**
- **専門分野**: 関係節構造解析
- **使用技術**: 依存関係 + 品詞分析の協調
- **使用箇所**:
  - 主動詞検出: `token.dep_ == 'ROOT'`（複文構造のため）
  - 関係節動詞: `token.dep_ == 'relcl'`（節境界のため）
  - 副詞検出: `token.pos_ == 'ADV'`（パターン明確のため）

#### **BasicFivePatternHandler**
- **専門分野**: 5文型分析
- **使用技術**: 品詞分析メイン
- **理由**: 単純化された文での処理がメイン

### 6.5 設計方針の改定

#### **旧方針（2025年8月28日以前）**
```
❌ spaCy依存関係解析（dep_関係）の使用は厳格に禁止
```

#### **新方針（2025年8月28日以降）**
```
✅ 専門分担型ハイブリッド解析
- 品詞分析: 副詞、受動態、単純文での使用
- 依存関係: 複文、関係節構造での限定使用
- 透明性: 使用理由の明示的ログ出力
```

### 6.6 実装時の注意事項

#### ⚠️ **必須チェックリスト**
1. [ ] 使用する解析手法（品詞/依存関係）の明示
2. [ ] 使用理由のコメント記載
3. [ ] デバッグ用ログ出力の実装
4. [ ] fallback処理の実装
5. [ ] テストケースでの精度検証

#### 🚨 **避けるべき実装**
- 理由なく依存関係を使用
- ログ出力なしの判定処理
- どちらの手法を使ったか不明な実装
- ハイブリッド部分の過度な複雑化

---

## 7. 厳格な禁止事項

### 7.1 技術的禁止事項
❌ **既存システムからのコード直接コピペ**
❌ **既存クラス・メソッドの継承・依存**
❌ **spaCy依存関係解析（dep_関係）の使用**
❌ **Phase A2等の設計違反概念の導入**
❌ **Central Controllerでの直接文法処理**
❌ **ハードコーディング（個別事例対応の固定値）**
❌ **テストケース・期待値の変更**

### 6.2 プロセス禁止事項
### 7.1 技術的禁止事項

❌ **無目的な依存関係解析の使用**
- 理由なく`token.dep_`を使用することは禁止
- 専門分担マップに従った使用のみ許可

❌ **透明性を欠く実装**
- 使用理由のコメントなし
- ログ出力なしの判定処理

❌ **過度なハイブリッド化**
- 複雑な条件分岐での両手法混在
- 判定基準の不明確な実装

### 7.2 設計禁止事項
❌ **設計仕様書の無承認変更**
❌ **責任分離原則の違反**
❌ **技術負債の導入**
❌ **一時的な「Phase」概念の導入**
❌ **ハンドラー間の直接通信は禁止**

### 7.3 テスト禁止事項
❌ **compare_results.pyの変更**
❌ **テスト条件・期待値の調整**
❌ **新規テストスクリプトの作成**

---

## 7. 成功基準

### 7.1 機能基準
✅ **段階的100%精度達成**
  - Phase 1: 基本5文型のみで100%
  - Phase 2: 5文型+関係節で100%  
  - Phase 3: 5文型+関係節+受動態で100%
✅ **全テストケースの自動実行**
✅ **既存compare_results.pyでの検証パス**
✅ **Rephraseスロット構造の完全遵守**

### 7.2 設計基準
✅ **責任分離原則の完全遵守**
✅ **各コンポーネントの単体テスト可能性**
✅ **技術負債ゼロ**
✅ **拡張性の確保**

### 7.3 保守性基準
✅ **コード行数500行以内**（既存7707行の大幅削減）
✅ **循環的複雑度10以下**
✅ **依存関係の最小化**

---

## 8. 既存エンジン・ハンドラーの参考構造詳細

### 8.1 BasicFivePatternEngine（基本5文型）
#### 核心アーキテクチャ
```python
class BasicFivePatternEngine:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.boundary_lib = BoundaryExpansionLib()  # 境界拡張
        self.sentence_patterns = self._load_sentence_patterns()
        
    def process(self, text: str) -> Dict[str, str]:
        # 1. spaCy POS解析（情報源のみ）
        # 2. 人間文法パターンマッチング（優先度順）
        # 3. スロット配置
        # 4. 境界拡張
        # 5. 100%精度検証
```

#### 文型パターン構造（優先度順）
```python
patterns = {
    "SVOO": {  # 最高優先度（最も具体的）
        "required_relations": ["nsubj", "iobj", "obj", "root"],
        "mapping": {"nsubj": "S", "iobj": "O1", "obj": "O2", "root": "V"},
        "priority": 1
    },
    "SVOC": {
        "required_relations": ["nsubj", "obj", "xcomp", "root"],
        "mapping": {"nsubj": "S", "obj": "O1", "xcomp": "C2", "root": "V"},
        "priority": 2
    },
    "SVO": {"priority": 3},
    "SVC": {"priority": 4},
    "SV": {"priority": 5}  # 最も汎用的なので最低優先度
}
```

#### 参考にすべき手法
- **優先度ベースパターンマッチング**: 具体的な文型から汎用的な文型へ
- **境界拡張技術**: 単語レベルから句レベルへの自動拡張
- **人間文法認識**: POSタグを情報源とした文法パターン識別

### 8.2 SimpleRelativeEngine（関係節）
#### 核心アーキテクチャ
```python
class SimpleRelativeEngine:
    def process(self, text: str) -> Dict[str, str]:
        # 1. 関係節検出（acl:relcl, acl）
        # 2. 先行詞特定（関係動詞の頭）
        # 3. 関係代名詞特定（obj, nsubj, advmod, nmod:poss）
        # 4. 先行詞+関係代名詞結合
        # 5. サブスロット生成
```

#### 関係詞検出ロジック
```python
def _detect_relative_pronoun(self, sent, rel_verb):
    # 1. 関係副詞優先（where, when, why, how）
    advmod = find_by_deprel(rel_verb, 'advmod')
    
    # 2. 目的格関係代名詞（that, which）
    if not advmod:
        obj_rel = find_by_deprel(rel_verb, 'obj')
    
    # 3. 主格関係代名詞（who, which）
    if not obj_rel:
        subj_rel = find_by_deprel(rel_verb, 'nsubj')
    
    # 4. 所有格関係代名詞（whose）
    if whose_word and whose_word.deprel == 'nmod:poss':
        possessed_noun = find_by_id(whose_word.head)
```

#### 参考にすべき手法
- **段階的関係詞検出**: 関係副詞 → 目的格 → 主格 → 所有格の順
- **先行詞+関係詞結合**: "The man who", "The book which"形式
- **所有格特別処理**: "whose car" → sub-s含有、possessed_noun管理

### 8.3 PassiveVoiceEngine（受動態）
#### 核心アーキテクチャ
```python
class PassiveVoiceEngine:
    def process(self, text: str) -> Dict[str, str]:
        # 1. 受動態構造検出（aux + past_participle）
        # 2. 要素特定（subject, auxiliary, main_verb, agent）
        # 3. スロット配置（S, Aux, V, M1-by句）
        # 4. サブスロット対応
```

#### 受動態検出パターン
```python
def _analyze_passive_structure(self, sent):
    # be動詞 + 過去分詞の検出
    for word in sent.words:
        if word.deprel == 'aux:pass':  # 受動態助動詞
            main_verb = find_by_id(word.head)  # 過去分詞
            if main_verb.xpos in ['VBN']:  # 過去分詞確認
                return {
                    'auxiliary': word,      # "was", "is", "been"
                    'main_verb': main_verb, # "written", "built"
                    'subject': find_subject(main_verb),
                    'agent': find_agent(main_verb)  # by句
                }
```

#### 参考にすべき手法
- **受動態パターン認識**: POS_TAG=VBN + 助動詞パターンの検出
- **by句処理**: agent検出とM1スロット配置
- **サブスロット対応**: sub-aux, sub-v分離

### 8.4 ModifierEngine（修飾語）
#### 参考パターン（複数エンジンから抽出）
```python
# 前置詞句エンジンから
class PrepositionalPhraseEngine:
    def _detect_prep_phrases(self, sent):
        # nmod, obl, advmod関係の前置詞句検出
        # 位置ベース配置（動詞前後でM1/M2/M3判定）
        
# 副詞エンジンから  
class AdverbEngine:
    def _classify_adverbs(self, sent):
        # 頻度副詞、様態副詞、時間副詞の分類
        # 個数ベース配置ルール適用
```

#### 参考にすべき手法
- **個数ベース配置**: 1個→M2、2個→M1+M2またはM2+M3、3個→M1+M2+M3
- **前置詞句検出**: POS_TAG=IN + 名詞句パターンの識別
- **動詞中心配置**: 動詞を基準とした前後判定

### 8.5 NewSystemIntegratedMapper（新統合システム）
#### 統合アーキテクチャ
```python
class NewSystemIntegratedMapper:
    def __init__(self):
        self.handlers = [
            'relative_clause',    # 最優先
            'passive_voice', 
            'basic_five_pattern',
            'modifier_handler'    # 最後
        ]
        
    def process(self, text: str):
        # 1. 全ハンドラー同時実行
        # 2. 結果統合・優先度管理
        # 3. スロット重複解決
        # 4. 最終フォーマット生成
```

#### 参考にすべき手法
- **順次ハンドラー実行**: 関係節 → 受動態 → 5文型 → 修飾語
- **結果統合技術**: 複数ハンドラー結果のマージ処理
- **優先度管理**: ハンドラー間のスロット競合解決

---

## 9. 承認・変更管理

### 9.1 仕様変更プロセス
1. **変更提案**: 具体的な理由と影響範囲を明記
2. **ユーザー承認**: 明示的な承認なしに変更不可
3. **影響評価**: 精度・性能・保守性への影響評価
4. **文書更新**: 承認後の仕様書更新

### 9.2 実装原則
- **この仕様書に基づく実装のみ許可**
- **仕様書に記載のない機能追加は禁止**
- **問題発生時は仕様書の見直しを優先**

---

## 10. 実装済み機能テストケース管理

### 10.1 目的・重要性
新ハンドラー実装時には、既存実装済み機能への悪影響（デグレード）を確認する必要がある。
そのため、実装済み機能のテストケースを常に把握し、新機能追加後に必ずリグレッションテストを実施する。

### 10.2 実装済み機能対応テストケース（final_54_test_data.json）

#### 10.2.1 基本5文型（単文）
**対象ケース**: `1, 2, 55-69`
- **ケース1**: `"The car is red."` - 第2文型（SVC）
- **ケース2**: `"I love you."` - 第3文型（SVO）
- **ケース55**: `"Birds fly."` - 第1文型（SV）
- **ケース58**: `"She looks happy."` - 第2文型（SVC）
- **ケース61**: `"I read books."` - 第3文型（SVO）
- **ケース64**: `"I gave him a book."` - 第4文型（SVOO）
- **ケース67**: `"We call him Tom."` - 第5文型（SVOC）
- **ケース55-69**: その他基本5文型バリエーション

#### 10.2.2 関係節（who, which, that, whose）
**対象ケース**: `3-14`
- **ケース3**: `"The man who runs fast is strong."` - who主語関係節 + 副詞
- **ケース4**: `"The book which lies there is mine."` - which主語関係節 + 副詞
- **ケース5**: `"The person that works here is kind."` - that主語関係節 + 副詞
- **ケース6**: `"The book which I bought is expensive."` - which目的語関係節
- **ケース7**: `"The man whom I met is tall."` - whom目的語関係節
- **ケース8**: `"The car that he drives is new."` - that目的語関係節
- **ケース12**: `"The man whose car is red lives here."` - whose所有格関係節 + 副詞
- **ケース13**: `"The student whose book I borrowed is smart."` - whose目的語関係節
- **ケース14**: `"The woman whose dog barks is my neighbor."` - whose主語関係節

#### 10.2.3 受動態（単文）
**対象ケース**: `20-22, 35`
- **ケース20**: `"He has finished his homework."` - 完了時制（has + 過去分詞）
- **ケース21**: `"The letter was written by John."` - 基本受動態
- **ケース22**: `"The house was built in 1990."` - 基本受動態
- **ケース35**: `"The teacher whose class runs efficiently is respected greatly."` - 主節受動態 + whose関係節

#### 10.2.4 関係節内受動態
**対象ケース**: `9-11, 46-47`
- **ケース9**: `"The car which was crashed is red."` - 関係節内受動態
- **ケース10**: `"The book that was written is famous."` - 関係節内受動態
- **ケース11**: `"The letter which was sent arrived."` - 関係節内受動態
- **ケース46**: `"The report which was thoroughly reviewed by experts was published successfully."` - 複合受動態
- **ケース47**: `"The student whose essay was carefully corrected improved dramatically."` - whose + 受動態

#### 10.2.5 副詞修飾語（単文）
**対象ケース**: `70-79`
- **ケース70**: `"She sings beautifully."` - 様態副詞
- **ケース71**: `"Tomorrow I study."` - 時副詞
- **ケース72**: `"He slowly opened the door."` - 様態副詞
- **ケース73**: `"We always eat breakfast together."` - 頻度副詞
- **ケース74**: `"The cat quietly sat on the mat."` - 様態副詞
- **ケース75**: `"Students often study here."` - 頻度副詞
- **ケース76**: `"She carefully reads books."` - 様態副詞
- **ケース77**: `"Yesterday he became tired."` - 時副詞
- **ケース78**: `"They run fast."` - 様態副詞
- **ケース79**: `"I gave him the book yesterday."` - 時副詞

### 10.3 リグレッションテスト実行方法

#### 10.3.1 実装済み全機能テスト
```bash
# 実装済み全機能（基本5文型 + 関係節 + 受動態 + 副詞）
python fast_test.py 1 2 3 4 5 6 7 8 9 10 11 12 13 14 20 21 22 35 46 47 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79
```

#### 10.3.2 機能別テスト
```bash
# 基本5文型のみ
python fast_test.py 1 2 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69

# 関係節のみ
python fast_test.py 3 4 5 6 7 8 12 13 14

# 受動態のみ（単文 + 関係節内）
python fast_test.py 9 10 11 20 21 22 35 46 47

# 副詞修飾語のみ
python fast_test.py 70 71 72 73 74 75 76 77 78 79
```

### 10.4 新ハンドラー開発時の必須手順

#### 10.4.1 実装前確認
1. **現在の実装済み機能リスト確認**
2. **既存テストケースの実行・成功率確認**
3. **新機能のテストケース追加計画**

#### 10.4.2 実装中確認
1. **段階的実装とテスト実行**
2. **既存機能への影響確認**
3. **デグレード発生時の即座対応**

#### 10.4.3 実装後確認
1. **全実装済み機能のリグレッションテスト**
2. **成功率の維持確認**
3. **本設計仕様書への新テストケース追加**

### 10.5 テストケース拡張ルール

#### 10.5.1 新機能実装時
新ハンドラー実装時は、対応する例文を上記リストに追加し、以降のリグレッションテストに含める。

#### 10.5.2 例文追加基準
- **実装済み機能**: 100%成功が期待されるケース
- **未実装機能**: 将来実装予定のケース（現在はテスト対象外）
- **複合機能**: 複数ハンドラーが連携するケース

### 10.6 品質保証
- **新機能実装**: 既存機能への悪影響ゼロが必須条件
- **リグレッション**: 実装済み機能の成功率低下は即座修正対象
- **継続改善**: 新例文追加により品質向上を図る

---

**本仕様書は開発の絶対基準であり、これに反する実装は一切認められない。**
**段階的100%精度達成と継続的品質保証が本プロジェクトの成功条件である。**
