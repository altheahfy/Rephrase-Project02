# auto_check_missing_assets.py 使い方マニュアル

## 概要
`auto_check_missing_assets.py`は、例文データベース作成システムにおいて、**イラスト**や**日本語補助テキスト（slottext）**がまだ存在しない表現を自動的に識別し、Excelファイルに結果を書き込むアプリケーションです。

## 機能
- 📊 例文入力元.xlsxの内容を解析
- 🔍 イラストが未作成の英単語を検出
- 📝 slottext.jsonに未登録の表現を検出
- ✅ 結果をExcelファイルの右側列に自動記入
- 🎨 未作成項目を赤色ハイライトで視覚化

## 必要なファイル構成
実行前に以下のファイルが同じディレクトリまたは指定パスに存在する必要があります：

### 必須ファイル
1. **例文入力元.xlsx** - 分析対象のExcelファイル
2. **slottext.json** - 日本語補助テキストのルール定義
3. **image_meta_tags.json** - イラストメタデータ（相対パス: `../完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/image_meta_tags.json`）
4. **slot_images/common/** - イラストファイル格納フォルダ（相対パス: `../完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/slot_images/common`）

### 分析対象列
- **SlotPhrase** - スロット表現
- **SubslotElement** - サブスロット要素

## 使用方法

### 1. 実行準備
```bash
# Pythonライブラリが必要な場合はインストール
pip install pandas openpyxl
```

### 2. 実行
```bash
python auto_check_missing_assets.py
```

### 3. 実行結果
- **例文入力元_チェック結果.xlsx** が生成されます
- 元のファイルは変更されません

## 出力結果の見方

### Excelファイル
- **V列（22列目）**：「未作成アセット」列が追加
- **赤色ハイライト**：未作成アセットがある行
- **カンマ区切り**：複数の未作成アセットがある場合

### コンソール出力
```
🚀 例文入力元.xlsx 自動チェック開始
📊 データ読み込み中...
✅ Excel読み込み完了: 1000行
✅ slottext.json読み込み完了: 250ルール
✅ image_meta_tags.json読み込み完了: 500項目
✅ 画像ファイル読み込み完了: 300ファイル
🔍 未作成アセット分析中...
🔍 未作成アセット合計: 45項目

📊 未作成アセット分析結果
🔍 未作成アセット (45個):
  1. vocabulary
  2. exercise
  3. grammar
  ...

✅ 処理完了！結果ファイル: 例文入力元_チェック結果.xlsx
```

## アルゴリズム詳細

### 単語抽出ロジック
- **対象**：英単語のみ（2文字以上のアルファベット）
- **除外**：一般的な機能語（the, a, is, have等）
- **処理**：小文字に正規化

### 複数形対応
自動的に単数形に変換してチェック：
- `cities` → `city`
- `boxes` → `box` 
- `watches` → `watch`
- `cats` → `cat`

### 判定基準
単語が以下の**両方に存在しない**場合のみ「未作成アセット」として識別：
1. **イラストチェック**
   - image_meta_tags.jsonのmeta_tags
   - slot_images/common/*.pngファイル名
2. **slottextチェック**
   - slottext.jsonの正規表現条件

## エラー対処

### よくあるエラー
1. **ファイルが見つからない**
   ```
   ❌ Excel файл не найден: 例文入力元.xlsx
   ```
   → ファイルパスと名前を確認

2. **画像フォルダが見つからない**
   ```
   ❌ 画像フォルダが見つかりません
   ```
   → 相対パス構造を確認

3. **JSON形式エラー**
   → slottext.jsonまたはimage_meta_tags.jsonの形式を確認

### ファイルパス設定
必要に応じて、`MissingAssetsChecker`クラスの`__init__`メソッド内のパスを環境に合わせて変更してください：

```python
self.excel_file = "例文入力元.xlsx"
self.slottext_file = "slottext.json"
self.image_meta_file = "../完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/image_meta_tags.json"
self.image_folder = "../完全トレーニングUI完成フェーズ３/project-root/Rephrase-Project/training/slot_images/common"
```

## 次のステップ
1. **結果ファイルを開く**：例文入力元_チェック結果.xlsx
2. **赤色項目を確認**：V列の未作成アセット
3. **手作業判断**：実際にイラストが必要か、slottextが必要かを内容に応じて判断
4. **アセット作成**：必要に応じてイラスト作成またはslottext.json更新

## 作成情報
- **作成者**：GitHub Copilot
- **作成日**：2025年7月20日
- **対象ファイル**：auto_check_missing_assets.py
