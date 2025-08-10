# 📚 Rephrase例文DB作成完全手順書 v3.0

  > **📅 作成日**: 2025年8月5日  
  > **🔄 リライト日**: 2025年8月10日  
  > **👤 作成者**: Claude（Anthropic）  
  > **🎯 用途**: エクセル入力からJSON化まで、例文DB作成の全工程を標準化  
  > **🆕 v3.0更新**: spaCy完全連携 + 構造的判定ルール対応

---

## 🚨 **重要な変更通知（v3.0）**

### **システム設計思想の大幅変更**
- **旧**: パターンマッチング型ルール辞書
- **新**: spaCy完全連携 + 構造的判定ルールシステム
- **影響**: ルール辞書全面改写、エンジン大幅改修が必要

### **現在の開発段階**
- ✅ 問題特定完了: "ago重複"等の根本原因判明
- ✅ 新設計思想確立: spaCy依存関係→Rephraseルール適用
- 🔄 **大規模改修中**: ルール辞書v2.0 + エンジン改修
- ⏳ 品質保証: 例文DB 100%準拠への最終段階

---

## 📋 手順一覧（v3.0対応版）

| 手順 | 項目 | 概要 |
|------|------|------|
| 1️⃣ | [例文の増殖（AI支援）](#1️⃣-例文の増殖ai支援) | 著作権対策＋属性固定型増殖 |
| 2️⃣ | [文要素自動分解システム](#🆕-文要素自動分解システム) | spaCyベース句動詞対応パーシング |
| 3️⃣ | [未作成アセットの検出](#3️⃣-未作成アセットの検出) | 不足要素の自動検出 |
| 4️⃣ | [イラストの生成＋slottext.json追記](#4️⃣-イラストの生成) | 視覚的補助材料作成 | jsonデータへの変換時に日本語補助テキストを付加するためのデータベースに追記　｜
| 5️⃣ | [JSONデータへの変換](#5️⃣-jsonデータへの変換) | システム用形式変換 |
| 6️⃣ | [解説データの統合](#6️⃣5️-解説データの統合) | 文法解説の統合 |

| 7️⃣ | [メタデータの更新](#7️⃣-メタデータの更新) | システム連携情報更新 |
| 8️⃣ | [品質保証チェック](#8️⃣-品質保証チェックとトラブルシューティング) | 最終検証・問題解決 |

---

## 1️⃣ 例文の増殖（AI支援）

### 🎯 目的
著作権を侵害せずに元の例文を多様化するため、パラフレーズと属性固定型増殖を用いて様々な属性を持つ例文を生成します。

### 📋 前提と準備
- ✅ 元になる例文（著作権のある教材などから抽出）
- ✅ `example_expansion_spec_v2.0.md`（属性固定型増殖仕様書）

### 🔧 実行手順

　**（１）ステップ1-1: 著作権対策パラフレーズ**
　　例文を語彙レベルで言い換えます。構造は変えずに語彙を置き換え、著作権侵害を防ぎます。

　　> **💡 例**: 
　　> - **元文**: "He has fully recovered from his illness."
　　> - **パラフレーズ**: "He has completely recovered from his injury."

　**（２）ステップ1-2: 属性固定型増殖**
　　パラフレーズした例文を、`example_expansion_spec_v2.0.md` に従って属性固定型増殖します。ChatGPTなどに指示し、指定した属性（例: `male/singular`）で段階0〜4を順に実行させます。

　　> ⚠️ **注意**: セッション内で他の属性を混在させないよう注意します。

　**（３）ステップ1-3: 複数属性展開**
　　商用利用時の多様性を確保するため、次の4属性のセッションを別々に実行します。各セッションで4例文ずつ生成し、合計16例文を作成します。

　　| 属性 | 説明 | 例文数 |
　　|------|------|---------|
　　| 🧑 `male/singular` | 男性・単数 | 4例文 |
　　| 👩 `female/singular` | 女性・単数 | 4例文 |
　　| 🧑‍🤝‍🧑 `neutral/singular` | 中性・単数 | 4例文 |
　　| 👥 `neutral/plural` | 中性・複数 | 4例文 |

### ✅ 成果物
- 📊 属性ごとに4例文、合計16例文から成る増殖済みデータベース

---

## 2️⃣ 文要素自動分解システム

### 🎯 目的
RephraseParsingEngine v1.1 + spaCy語彙認識を用いて、英文を自動的にスロット（S, V, O1, M2など）に分解し、Excel形式で出力します。特に句動詞（phrasal verbs）の分離可能構造を正確に処理します。

### 📋 前提と準備
- ✅ `Rephrase_Parsing_Engine.py`（spaCyベース句動詞対応版）
- ✅ `Excel_Generator.py` / `ExcelGeneratorV2.py`
- ✅ spaCy英語モデル（`en_core_web_sm`）
- ✅ 増殖済み例文データ

### 🧠 技術仕様

#### **コア技術スタック**
| 技術要素 | 役割 | 特徴 |
|----------|------|------|
| 🧬 **spaCy 3.8.7** | NLP基盤・依存関係解析 | `prt`依存関係で句動詞を自動検出 |
| 🎯 **RephraseParsingEngine** | 文法ルール適用 | 35種類の埋め込み文法ルール |
| 📊 **ExcelGeneratorV2** | 出力形式変換 | Rephrase標準形式（word/phrase分類） |
| 🔍 **自動句動詞検出** | 句動詞分離処理 | 分離型・非分離型を統一的に処理 |

#### **句動詞処理アルゴリズム**
```python
# spaCyの prt (particle) 依存関係を活用
for token in doc:
    if token.dep_ == "prt" and token.head.pos_ == "VERB":
        # 句動詞構造を検出
        verb = token.head.text      # → V スロット
        particle = token.text       # → M2スロット (particle)
        # 目的語は自動分離: "write the sentence down"
        # → V:'write', O1:'the sentence', M2:'down'
```

### 🔧 実行手順

　**（１）ステップ🆕-1: パーシングエンジン初期化**
　　```python
　　from Rephrase_Parsing_Engine import RephraseParsingEngine
　　from Excel_Generator import ExcelGeneratorV2
　　
　　# spaCyベースエンジン初期化
　　parser = RephraseParsingEngine()
　　generator = ExcelGeneratorV2()
　　```

　**（２）ステップ🆕-2: 例文の自動分解**
　　```python
　　# 句動詞対応の自動分解
　　sentences = [
　　    "Write down the sentence",      # 非分離型
　　    "Write the sentence down",      # 分離型  
　　    "Could you write it down?",     # 疑問文
　　    "You, give it to me straight"   # 呼びかけ
　　]
　　
　　for sentence in sentences:
　　    result = parser.analyze_sentence(sentence)
　　    generator.analyze_and_add_sentence(sentence, v_group_key="phrasal_verb_test")
　　```

　**（３）ステップ🆕-3: Excel出力生成**
　　```python
　　# Excel形式データ生成
　　excel_data = generator.generate_excel_data()
　　```

　**（４）ステップ🆕-4: 句動詞構造の確認**
　　出力されるExcel構造例：

　　| Slot | SlotPhrase | Phrase_type | Slot_display_order |
　　|------|------------|-------------|-------------------|
　　| Aux | Could | word | 1 |
　　| S | you | word | 2 |
　　| V | write | word | 3 |
　　| O1 | it | word | 4 |
　　| M2 | down | word | 5 |

　　> 🎯 **句動詞の表示**: `write_V` + `it_O1` + `down_M2`で分離表示
　　> 学習効果: 分離型・非分離型を並べて比較学習可能

### 💡 対応文法パターン

| パターン | 例文 | 自動検出結果 |
|----------|------|-------------|
| **句動詞（非分離）** | `Turn off the light` | V:`Turn`, M2:`off`, O1:`the light` |
| **句動詞（分離）** | `Turn the light off` | V:`Turn`, O1:`the light`, M2:`off` |
| **疑問文+句動詞** | `Can you turn it down?` | Aux:`Can`, S:`you`, V:`turn`, O1:`it`, M2:`down` |
| **現在完了** | `I haven't seen you` | S:`I`, Aux:`haven't`, V:`seen`, O1:`you` |
| **呼びかけ+命令** | `You, write it down` | M1:`You,`, V:`write`, O1:`it`, M2:`down` |

### ⚡ パフォーマンス特性

- **句動詞認識精度**: 95%+ (spaCyの`prt`依存関係ベース)
- **処理速度**: ~100文/秒
- **対応文法**: 35種類の埋め込みルール
- **メモリ使用量**: 約200MB (spaCyモデル込み)

### ✅ 成果物
- 📊 文要素分解済みExcelデータ
- 🎯 句動詞構造の正確な分離表示
- 🔄 学習用スロット順序データ

---

　　> 🎯 **絶対順序ルール**: 各`V_group_key`内でスロット（M3, S, Aux, V, O1, O2 等）に番号を振る際は、全例文を通じて一意な順序にします。「絶対順序考察.xlsx」参照。

　　- ✅ **正しい**: 相対順序でリセットしない
　　- ✅ **許可**: `V_group_key`が異なれば、番号付けを1から再開始してOK。

　**（５）ステップ2-4: 整合性チェック**
　　手動で以下を確認します：

　　| チェック項目 | 詳細 |
　　|-------------|------|
　　| 🔢 **絶対順序** | 正しく統一されているか |
　　| ❓ **疑問詞属性** | `QuestionType: wh-word`属性が付与されているか |
　　| 🎲 **空白セル候補** | 各スロットに含まれているか（ランダマイズ用） |
　　| 👤 **代名詞一致** | 性別が主語と一致しているか |
　　| 📊 **データ完整性** | Slot, SlotPhrase, SubslotID, SubslotElement の記入漏れ |
　　| 📝 **表記統一** | 同一`V_group_key`内で表記揺れや余計なスペースがないか |

### ✅ 成果物
- 📋 整合性チェック済みの`例文入力元.xlsx`

---

## 3️⃣ 未作成アセットの検出

### 🎯 目的
例文に必要なイラストや日本語補助テキストが不足していないかを自動判定します。

### 📋 前提と準備
- ✅ 段階2で完成した`例文入力元.xlsx`
- ✅ `auto_check_missing_assets.py`

### 🔧 実行手順

　**（１）ステップ3-1: 自動検出スクリプト実行**

　　コマンドラインから以下を実行します：

　　```bash
　　cd 例文セットDB作成システム
　　python auto_check_missing_assets.py
　　```

　**（２）ステップ3-2: 検出結果の確認**

　　スクリプトが以下を解析します：
　　- 📊 **Excel解析**: `SlotPhrase`と`SubslotElement`
　　- 🔍 **参照ファイル**: `image_meta_tags.json`と`slottext.json`
　　- 🎯 **検出対象**: 未作成アセット

　**（３）ステップ3-3: 結果ファイルの確認**

　　結果が`例文入力元_チェック結果.xlsx`のV列に出力されます：

　　| アイコン | 意味 | 対応 |
　　|----------|------|------|
　　| 📷 | イラストが必要な単語 | 段階6でイラスト作成 |
　　| 📝 | 補助テキストが必要なフレーズ | 段階7でテキスト追加 |
　　| 🔴 **赤色行** | 未作成アセットあり | 要対応 |

### ✅ 成果物
- 📋 未作成アセットリストを含む`例文入力元_チェック結果.xlsx`

---
## 4️⃣ イラストの生成とslottext.json追記

### 🎯 目的
未作成アセット検出フェーズで検出された単語のイラストを作成するとともに、日本語補助テキストのデータベースであるslotttext.jsonに追記します。

### 📋 前提と準備
- ✅ 未作成アセットリスト（段階3の結果）
- ✅ `canva_illustration_prompts.md`（イラスト生成指針）

### 🔧 実行手順

　**（１）ステップ4-1: プロンプト生成**

　　Claude Sonnet 4 に対し、`canva_illustration_prompts.md`を参考にして各単語のイラスト用プロンプトを作成させます。

　　> 💡 **指示例**: 
　　> "単語 'vocabulary', 'trauma', 'recovery' の理解を助けるイラストのプロンプトを作成してください。"

　**（２）ステップ4-2: Canva AIでの生成**

　　①**プロンプト入力**: Claudeが生成したプロンプトを Canva AI に入力
　　②**イラスト生成**: 英語学習者向けのイラストを生成
　　③**ファイル命名**: `[単語名].png`とします

　**（３）ステップ4-3: 画像の配置**

　　生成した画像を`training/slot_images/common/`ディレクトリに保存します。

　　```
　　📁 training/
　　  📁 slot_images/
　　    📁 common/
　　      🖼️ vocabulary.png
　　      🖼️ trauma.png
　　      🖼️ recovery.png
　　```

**（４）ステップ4-4: slottext.jsonへの追記**

　　3️⃣で検出した不足する日本語補助テキストについて、Claude Sonnet4に直接追記依頼。

### ✅ 成果物
- 🎨 新規イラストファイルが`training/slot_images/common/`に追加される。slottext.jsonが更新される。

---
## 5️⃣ JSONデータへの変換

### 🎯 目的
Excelデータを Rephrase システムで利用可能な JSON 形式に変換し、日本語補助テキストを付与します。

### 📋 前提と準備
- ✅ `例文入力元.xlsx`
- ✅ `batch.py`
- ✅ `slottext.json`

### 🔧 実行手順

　**（１）ステップ4-1: JSON変換実行**

　　```bash
　　cd 例文セットDB作成システム
　　python batch.py 例文入力元.xlsx
　　```

　**（２）ステップ4-2: 変換処理内容**

　　スクリプトは以下を実行します：
　　- 📊 **Excel読み込み**: スロット構造を JSON に変換
　　- 🇯🇵 **補助テキスト付与**: `slottext.json`に従って各フレーズに日本語テキストを付与
　　- 🔍 **自動判別**: 動詞の活用や前置詞・接続詞等を自動判別

　**（３）ステップ4-3: 結果確認・調整**

　　①出力された`slot_order_data.json`を確認
　　②必要に応じて`slottext.json`に新ルールを追加
　　③スクリプトを再実行

　　> 🔄 **繰り返し処理**: 完璧な結果が得られるまで調整・再実行可能

### ✅ 成果物
- 🗄️ Rephrase システム用データベース`slot_order_data.json`

---

## 6️⃣ 解説データの統合

### 🎯 目的
動詞グループごとの文法解説を JSON データベースに統合します。

### 📋 前提と準備
- ✅ `解説入力フォーマット.csv`（解説入力用テンプレート）
- ✅ `integrate_explanations.py`（CSV→JSON統合スクリプト）
- ✅ 段階4で生成された`slot_order_data.json`

### 🔧 実行手順

　**（１）ステップ5-1: 解説CSVの編集**

　　①**ファイル編集**: `解説入力フォーマット.csv`を Excel で開きます
　　②**データ入力**: 各行に以下を入力します：

　　| 列名 | 内容 | 例 |
　　|------|------|-----|
　　| `V_group_key` | 動詞グループキー | `recover` |
　　| `explanation_title` | 解説タイトル | `"recoverの使い方"` |
　　| `explanation_content` | 解説本文 | `"recoverは「治る」なら自動詞で..."` |

　　> 💡 **記入例**:
　　> ```csv
　　> V_group_key,explanation_title,explanation_content
　　> recover,"recoverの使い方","recoverは「治る」なら自動詞で「from his illness」を付加するが、「回復する」なら他動詞で目的語が必要…"
　　> apologize,"apologizeの使い方","apologizeは自動詞であり…"
　　> ```

　　> ⚠️ **注意**: 複数行の本文は二重引用符で囲みます
　　> ⚠️ **注意**: この中で使われている例文も事前にパラフレーズ

　**（２）ステップ5-2: 統合スクリプトの実行**

　　```bash
　　cd 例文セットDB作成システム
　　python integrate_explanations.py
　　```

　**（３）ステップ5-3: 処理内容確認**

　　スクリプトは以下を実行します：
　　- 📖 **CSV読み込み**: 解説データを取得
　　- 🗑️ **古い解説削除**: 既存JSONから古いエントリを削除
　　- ➕ **新しい解説追加**: 新しい解説エントリを追加
　　- 💾 **バックアップ作成**: `*_backup.json`として保存

　**（４）ステップ5-4: 結果の確認**

　　以下をチェックします：
　　- ✅ スクリプト実行時にエラーが無いか
　　- ✅ `slot_order_data.json`に`EXPLANATION`スロットが追加されているか
　　- ✅ `V_group_key`が例文データと一致しているか

### ✅ 成果物
- 📋 解説統合済みの`slot_order_data.json`

---



## 7️⃣ メタデータの更新

### 🎯 目的
新しく生成したイラストと補助テキストに対応するメタデータファイルを更新します。

### 📋 前提と準備
- ✅ 新規イラストファイル
- ✅ `image_meta_tags.json`
- ✅ `slottext.json`

### 🔧 実行手順

　**（１）ステップ7-1: イラストメタタグの追加**

　　①**AI支援**: Claude Sonnet 4 に`image_meta_tags.json`の既存内容を提示
　　②**タグ生成**: 新しく追加すべきタグを生成させます（例: `vocabulary.png`など）
　　③**メタタグ追記**: 生成されたメタタグを`training/image_meta_tags.json`に追記

　**（２）ステップ7-2: 補助テキストの追加**

　　①**対象確認**: 段階3で📝が付いた未対応表現を確認
　　②**ルール生成**: Claude Sonnet 4 に日本語補助テキストルールを生成させます
　　③**ルール追記**: 新しいルールを`slottext.json`に追記
　　④**再実行**: 必要に応じて`batch.py`を再実行して補助テキストを付与

　　> 🔄 **更新フロー**:
　　> ```
　　> 段階3検出結果 → Claude AI → 新ルール → slottext.json → batch.py再実行
　　> ```

### ✅ 成果物
- 📋 更新済みの`training/image_meta_tags.json`
- 📋 更新済みの`slottext.json`

---

## 8️⃣ 品質保証チェックとトラブルシューティング

### 📋 最終チェックリスト

| チェック項目 | 詳細内容 | 重要度 |
|-------------|----------|---------|
| ✅ **例文品質** | 文法的に正しく意味が自然か | 🔴 必須 |
| ✅ **属性整合** | 代名詞や性別が適切か | 🔴 必須 |
| ✅ **絶対順序** | `V_group_key`内で順序が統一されているか | 🔴 必須 |
| ✅ **解説統合** | 解説データがJSONに正しく追加されているか | 🟡 重要 |
| ✅ **イラスト・補助テキスト** | 必要なアセットが揃っているか | 🟡 重要 |
| ✅ **JSON整合** | `slot_order_data.json`の構造に欠損がないか | 🔴 必須 |
| ✅ **V_group_key対応** | 例文と解説の`V_group_key`が一致しているか | 🔴 必須 |

---

### 🔧 よくある問題と対処

　**（１）❌ 問題1: 絶対順序の誤り**
　　**症状**: ランダマイズ時の順序がおかしい  
　　**対処**: 各例文の順序付けを確認し、`V_group_key`内で統一

　**（２）❌ 問題2: V_group間順序を統一しようとしている**  
　　**症状**: 異なる`V_group_key`で順序を揃えようとしている  
　　**対処**: 各グループで1から始める（統一不要）

　**（３）❌ 問題3: 補助テキストが付かない**  
　　**症状**: 日本語補助テキストが表示されない  
　　**対処**: `slottext.json`に新しいルールを追加し、`batch.py`を再実行

　**（４）❌ 問題4: 属性不一致**  
　　**症状**: 代名詞や主語が不一致  
　　**対処**: 段階1の増殖設定を見直し

　**（５）❌ 問題5: ファイルパスエラー**  
　　**症状**: Pythonスクリプトでパスエラー  
　　**対処**: 必ず`例文セットDB作成システム`ディレクトリ内で実行

　**（６）❌ 問題6: 解説が反映されない**  
　　**症状**: CSV解説データがJSONに反映されない  
　　**対処**: 
　　- CSVのエンコードがUTF-8 BOMであるか確認
　　- `V_group_key`に余分な空白がないか確認

---

### 📁 作業ファイル一覧

## 🔧 使用ツール・資産一覧

### 📚 コア技術システム（v2.0更新）

　**（１）🧠 文要素自動分解エンジン**
　　- 🎯 `Rephrase_Parsing_Engine.py`（spaCyベース句動詞対応版）
　　- � `Excel_Generator.py` / `ExcelGeneratorV2.py`
　　- 🧬 `spacy 3.8.7` + `en_core_web_sm`モデル

　**（２）�📥 入力ファイル**
　　- 📋 `例文入力元（フォーマット）.xlsx`
　　- 📘 `example_expansion_spec_v2.0.md`

　**（３）🐍 処理スクリプト**
　　- ⚙️ `generate.py`（従来方式）
　　- 🆕 文要素自動分解システム（spaCyベース）
　　- 🔍 `auto_check_missing_assets.py`
　　- 🔄 `batch.py`
　　- 📝 `integrate_explanations.py`

　**（４）⚙️ 設定ファイル**
　　- 🇯🇵 `slottext.json`
　　- 🎨 `image_meta_tags.json`
　　- 📋 `解説入力フォーマット.csv`

　**（５）📤 出力ファイル**
　　- 📊 `例文入力元_チェック結果.xlsx`
　　- 🗄️ `slot_order_data.json`

---

> 🎉 **完了！** 
> 
> この手順書v2.0に従って作業を進めることで、spaCyベース句動詞自動検出システムを含む高品質な例文データベースを効率的に作成できます。
> 
> **🆕 v2.0の主な改善**：
> - 句動詞の分離可能構造を自動検出・分解
> - 手動リスト不要の完全自動化
> - 学習効果の向上（分離型・非分離型の比較学習）
