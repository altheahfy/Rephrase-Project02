# イラスト自動表示機構 設計仕様書

## 概要

Rephraseプロジェクトにおいて、スロット内のテキストに基づいて自動的に関連するイラストを表示する汎用システムです。上位スロット全体に対応し、単語の意味に応じた画像を動的に適用、複数画像の横並び表示、メタタグ自動生成、Type判定による表示制御、責務分離設計を実現しています。

---

## 🖼️ 視覚学習革命：母国語非介入システム

### 直接想起学習の実現
- **視覚→英語直結**: イラストから英語への直接的想起回路構築
- **翻訳思考排除**: 日本語を介さない自然な英語理解の促進
- **概念レベル学習**: 単語ではなく概念・イメージでの英語習得

### 認知科学に基づく視覚学習効果
- **二重符号化理論**: 言語情報と視覚情報の統合による強力な記憶定着
- **具体性効果**: 抽象的な文法概念の具体的イメージ化
- **図示効果**: 視覚的手がかりによる理解促進と記憶向上

### 多感覚統合学習環境
- **複数画像表示**: 複雑な概念の多角的理解促進
- **文脈適応**: 文の内容に応じた最適な視覚的手がかり提供
- **段階的支援**: テキスト非表示時の代替情報源として機能

### 学習動機・継続性の向上
- **視覚的魅力**: カラフルで魅力的な学習環境の提供
- **成功体験**: 視覚手がかりによる理解成功の積み重ね
- **個別最適化**: 学習者の理解度に応じた視覚的支援レベル調整

---

## システム構成

### ファイル構成

```
project-root/
├── image_meta_tags.json                # メタタグデータベース（自動生成対応）
├── js/universal_image_system.js        # 汎用画像表示制御システム（メインエンジン）
├── js/insert_test_data_clean.js        # 静的データ制御・button.png制御ロジック
├── js/generate_meta_tags.js            # メタタグ自動生成スクリプト
├── slot_images/                        # 画像ファイル格納ディレクトリ
│   ├── common/
│   │   ├── placeholder.png             # デフォルト画像
│   │   └── button.png                  # サブスロット展開ボタン画像
│   ├── people/                         # 人物関連画像
│   ├── actions/                        # 動作関連画像
│   ├── objects/                        # 物体関連画像
│   └── [その他カテゴリ]/
├── test_universal_image_system.html    # テスト用HTML
├── test_multiple_images.html           # 複数画像表示テスト
└── index.html                          # メインUI
```

## メタタグデータベース仕様

### `image_meta_tags.json` 構造

```json
[
  {
    "image_file": "manager.png",
    "folder": "people",
    "meta_tags": ["manager", "managers", "boss", "supervisor", "executive"],
    "priority": 3,
    "description": "マネージャー、管理職"
  }
]
```

#### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|------------|----|----- |------|
| `image_file` | string | ✓ | 画像ファイル名 |
| `folder` | string | ✓ | `slot_images/` 内のサブディレクトリ名 |
| `meta_tags` | string[] | ✓ | マッチング対象の単語・フレーズ配列 |
| `priority` | number | - | 優先度（高いほど優先、デフォルト: 1） |
| `description` | string | - | 画像の説明（管理用） |

#### メタタグ設計方針

1. **基本形 + 活用形の網羅**
   - 単数形・複数形：`offer` / `offers`
   - 動詞活用：`offer` / `offered` / `offering`
   - 三単現：`meet` / `meets`

2. **同義語・類似語の包含**
   - `manager` / `boss` / `supervisor`
   - `meeting` / `conference` / `session`

3. **短い単語への対応**
   - `she` / `he` / `we` / `go` など2文字以上の重要語も含める

## JavaScript制御システム仕様

### アーキテクチャ設計原則

#### 1. **責務分離（Separation of Concerns）**
- **`universal_image_system.js`**: 汎用画像表示エンジン（メタタグマッチング、複数画像表示）
- **`insert_test_data_clean.js`**: 静的データ制御、Type判定、button.png制御
- **明確な境界**: 空テキスト時の処理は静的制御側に完全委譲

#### 2. **全スロット対応**
- **対象スロット**: `['slot-m1', 'slot-s', 'slot-aux', 'slot-m2', 'slot-v', 'slot-c1', 'slot-o1', 'slot-o2', 'slot-c2', 'slot-m3']`
- **統一インターフェース**: 全スロットで同一の画像制御API

#### 3. **複数画像対応システム**
- **横並び表示**: 同一テキストから複数単語を抽出し、それぞれの画像を横並び表示
- **動的サイズ調整**: 画像枚数に応じてスロット幅・画像サイズを自動調整
- **重複排除**: 同一画像の重複表示を防止

### `js/universal_image_system.js` 主要関数

#### 核心関数

##### 1. `loadImageMetaTags()`
- **目的**: メタタグデータの非同期読み込み
- **戻り値**: `Promise<boolean>`
- **特徴**: キャッシュ無効化、エラーハンドリング、グローバル公開

##### 2. `findAllImagesByMetaTag(text)`
- **目的**: 複数画像検索（新機能）
- **処理**: 各単語ごとに最適マッチを検索、重複排除
- **戻り値**: `Array<ImageData>`

##### 3. `applyMultipleImagesToSlot(slotId, phraseText, forceRefresh)`
- **目的**: 複数画像表示制御（新機能）
- **処理フロー**:
  - 空テキスト時: 複数画像コンテナ削除→従来制御に委譲
  - マッチ0件: 複数画像コンテナ削除→単一画像制御
  - マッチ1件: 複数画像コンテナ削除→単一画像制御
  - マッチ2件以上: 複数画像コンテナ作成・表示

##### 4. `clearMultiImageContainer(slotId)`
- **目的**: 複数画像コンテナの完全クリア（外部制御用）
- **効果**: 単一画像表示への安全な復帰

##### 5. `updateSlotImage(slotId, forceRefresh)`
- **目的**: 個別スロット画像更新（外部API）
- **重要な設計**: 空テキスト時は複数画像クリアのみ実行、静的制御に委譲

##### 6. `updateAllSlotImages(forceRefresh)`
- **目的**: 全スロット一括画像更新（外部API）

#### 複数画像表示システム

##### 画像コンテナDOM構造
```html
<div class="multi-image-container" style="display: flex; gap: 6px;">
  <img class="slot-multi-image" src="slot_images/people/manager.png" style="height: 160px; width: 80px;">
  <img class="slot-multi-image" src="slot_images/actions/analyze.png" style="height: 160px; width: 80px;">
  <img class="slot-multi-image" src="slot_images/objects/data.png" style="height: 160px; width: 80px;">
</div>
```

##### 動的サイズ調整ロジック
```javascript
// 基本設定
const baseContainerWidth = 390;  // 1枚用基本幅
const minImageWidth = 50;        // 最小画像幅
const maxImageWidth = 120;       // 最大画像幅
const gap = 6;                   // 画像間隙間

// スロット拡大計算
const expandedContainerWidth = baseContainerWidth + (imageCount - 1) * 80;
const dynamicWidth = Math.min(maxImageWidth, Math.max(minImageWidth, Math.floor(availableWidth / imageCount)));

// スロット全体の横幅制御
slot.style.maxWidth = `${expandedContainerWidth}px`;
```

## HTML構造仕様

### スロット要素構造

#### 上位スロット
```html
<div class="slot-container" id="slot-v">
  <label>V</label>
  <img class="slot-image" src="slot_images/common/placeholder.png" alt="image for V">
  <div class="slot-text"></div>
  <div class="slot-phrase">offered</div>
</div>
```

#### サブスロット
```html
<div class="subslot-container" id="slot-o1-sub-s">
  <label>S</label>
  <img class="slot-image" src="slot_images/common/placeholder.png" alt="image for S">
  <div class="slot-text"></div>
  <div class="slot-phrase">she</div>
</div>
```

### 重要なクラス名

| クラス名 | 用途 |
|----------|------|
| `.slot-container` | 上位スロットコンテナ |
| `.subslot-container` | サブスロットコンテナ |
| `.slot-image` | 画像要素 |
| `.slot-phrase` | テキスト内容（マッチング対象） |

## 画像適用ロジック

### マッチングアルゴリズム

1. **テキスト正規化**
   ```javascript
   text.toLowerCase()
     .replace(/[^a-z0-9\s-]/g, ' ')
     .split(/\s+/)
     .filter(word => word.length > 1)
   ```

2. **語幹抽出**
   - `-s` 除去（3文字超、例外: -ss, -us, -is）
   - `-ed` 除去（4文字超）
   - `-ing` 除去（5文字超）

3. **厳密マッチング**
   ```javascript
   textWords.includes(tag.toLowerCase())
   ```

4. **優先度ソート**
   ```javascript
   matches.sort((a, b) => b.priority - a.priority)
   ```

### 画像パス生成

```javascript
imagePath = `slot_images/${imageData.folder}/${imageData.image_file}`
```

## 初期化・監視システム

### 初期化フロー

1. **DOMContentLoaded 待機**
2. **メタタグデータ読み込み**
3. **500ms 遅延後に初回画像適用**
4. **MutationObserver 開始**

### DOM変更監視

- **監視対象**: `#training-container`
- **監視タイプ**: `childList`, `subtree`, `characterData`
- **除外対象**: `#debug-console` 関連変更
- **重複防止**: 同一スロットへの連続処理回避

## データ属性管理

### 画像要素の状態管理

```javascript
// 適用時
imageElement.setAttribute('data-meta-tag', 'true');
imageElement.setAttribute('data-meta-tag-applied', matchedTag);
imageElement.setAttribute('data-applied-text', phraseText);

// クリア時
imageElement.removeAttribute('data-meta-tag');
imageElement.removeAttribute('data-meta-tag-applied');
imageElement.removeAttribute('data-applied-text');
```

## デバッグ機能

### `window.debugStrictMatching()`

コンソールから実行可能なデバッグ関数：

```javascript
window.debugStrictMatching()
```

**出力内容**:
- 利用可能メタタグデータ件数
- マッチングルール表示
- 全スロットのマッチング結果
- マッチング統計（成功率）

## 設定・カスタマイズ

### 調整可能パラメータ

| パラメータ | 場所 | デフォルト値 | 説明 |
|------------|------|-------------|------|
| 初期化遅延 | `initializeMetaTagSystem()` | 500ms | DOM安定化待機時間 |
| 最小単語長 | `extractWordsWithStemming()` | 2文字 | マッチング対象最小長 |
| 監視対象 | `setupIndividualRandomizeObserver()` | `#training-container` | DOM変更監視範囲 |

### 画像ディレクトリ拡張

新しいカテゴリ追加時：
1. `slot_images/` 内に新ディレクトリ作成
2. `image_meta_tags.json` に対応エントリ追加
3. `folder` フィールドにディレクトリ名指定

## 重要なトラブルシューティング事例

### 🚨 責務分離違反による表示不具合

#### 問題症状
- 複数画像表示後に「全クリア」すると404エラーや空白表示
- `button.png`が表示されるべき場面で表示されない

#### 根本原因
```javascript
// ❌ 問題のあった実装（修正前）
if (!currentText) {
  // 空テキスト時に汎用システムが介入
  applyMultipleImagesToSlot(slotId, currentText, forceRefresh);
  return; // ← これにより静的制御が実行されない
}
```

#### 正しい解決方法
```javascript
// ✅ 修正後の実装
if (!currentText) {
  // 複数画像クリアのみ実行
  const existingContainer = slot.querySelector('.multi-image-container');
  if (existingContainer) {
    existingContainer.remove();
  }
  // 静的制御（button.png制御）に委譲
  return;
}
```

#### 教訓
1. **空テキスト時は汎用システムが介入しない**
2. **button.png制御は静的システムの専門領域**
3. **責務の明確な分離が安定性を保証**

### 🚨 句読点による複数画像表示不具合【2025年7月15日修正】

#### 問題症状
- 文末に句読点（. ? ! , 等）が付くスロットで複数画像が期待通りに表示されない
- 例：「important message.」→ message.png のみ表示（important.png が表示されない）
- 例：「funny story?」→ story.png のみ表示（funny.png が表示されない）

#### 根本原因
**複数画像検索と単一画像検索で異なる正規化処理**

1. **複数画像検索**（`findAllImagesByMetaTag`）：
   ```javascript
   // 修正前：句読点が残る
   const individualWords = text.toLowerCase().split(/\s+/).filter(word => word.length >= 2);
   // 結果：["important", "message."] → "message." がマッチしない
   ```

2. **単一画像検索**（`findImageByMetaTag`）：
   ```javascript
   // 正常：句読点が除去される
   const searchWords = extractWordsWithStemming(text);
   // 結果：["important", "message"] → "message" がマッチする
   ```

#### 修正内容
**`findAllImagesByMetaTag`関数の個別単語処理を正規化**

```javascript
// ✅ 修正後の実装
const individualWords = text.toLowerCase()
  .replace(/[^\w\s-]/g, ' ')  // 句読点を除去
  .split(/\s+/)
  .filter(word => word.length >= 2);
```

#### 影響範囲
- **全ての上位スロット**：文末に来る可能性（O2, C1, C2, M3等）
- **全てのサブスロット**：親スロットの内容次第で句読点が付く可能性
- **対象句読点**：`. ? ! , ; : " ' ( ) [ ]` など

#### 解決効果
- 「important message.」→ [important.png, message.png] の2枚表示
- 「funny story?」→ [funny.png, story.png] の2枚表示
- 「What do you think?」→ [what.png, think.png] の2枚表示

#### 技術的詳細
**正規表現 `[^\w\s-]` の効果**：
- `\w`：英数字とアンダースコア
- `\s`：空白文字
- `-`：ハイフン（単語の一部として保持）
- `[^...]`：上記以外の文字（句読点）を空白に置換

#### 予防策
**新機能実装時の注意点**：
1. **統一された正規化処理**：全ての画像検索関数で同じ処理を使用
2. **句読点テスト**：文末テキストでの動作確認を必須とする
3. **デバッグ用関数**：句読点問題の早期発見用テスト関数の活用

#### デバッグ用テストケース
```javascript
// 句読点問題のテスト用関数
function testPunctuationHandling() {
  const testCases = [
    "important message.",
    "funny story?",
    "What do you think!",
    "Hello, world;",
    "Let's go:",
    "She said \"Hello\"",
    "Number (1)",
    "Item [A]"
  ];
  
  testCases.forEach(text => {
    console.log(`テスト: "${text}"`);
    const results = window.findAllImagesByMetaTag(text);
    console.log(`結果: ${results.map(r => r.image_file).join(', ')}`);
  });
}
```

#### 修正履歴
- **2025年7月15日**: 句読点による複数画像表示不具合を修正
- **対象関数**: `findAllImagesByMetaTag`の個別単語処理ロジック
- **修正方法**: 句読点除去の正規化処理を追加

## 外部API・グローバル関数

### 汎用画像システム公開関数

```javascript
// 基本制御API
window.updateAllSlotImages(forceRefresh = false)     // 全スロット更新
window.updateSlotImage(slotId, forceRefresh = false) // 個別スロット更新
window.initializeUniversalImageSystem()             // システム初期化

// 複数画像制御API
window.applyMultipleImagesToSlot(slotId, text, forceRefresh)  // 複数画像適用
window.clearMultiImageContainer(slotId)                      // 複数画像クリア
window.findAllImagesByMetaTag(text)                          // 複数画像検索

// データ更新API
window.updateAllSlotImagesAfterDataChange()         // データ変更後の全更新

// テスト・デバッグAPI
window.testUniversalImageSystem()                   // 手動テスト実行
```

### 使用例

```javascript
// 全スロットの画像を強制更新
updateAllSlotImages(true);

// 特定スロットの複数画像をクリア
clearMultiImageContainer('slot-v');

// データ更新後の再同期
updateAllSlotImagesAfterDataChange();
```

## 既知の制限・今後の改善

### 現在の制限事項

1. **単語レベルマッチング**: フレーズ全体での意味理解は未対応
2. **文脈依存性**: 同一単語の複数意味への対応限定的
3. **複数画像の意味的関連**: 単語レベルの独立マッチング
4. **特殊文字**: ハイフン以外の記号は除去される

### 技術的改善候補

1. **セマンティック検索**: 意味ベースのマッチング
2. **画像品質管理**: 自動リサイズ・最適化
3. **キャッシング戦略**: 画像・メタデータの効率的キャッシュ
4. **A/Bテスト**: マッチング精度の定量評価

### 🔧 メンテナンス時の重要な確認事項

#### 新機能実装時の必須チェック
1. **句読点テスト**: 文末に句読点が付くテキストでの動作確認
2. **複数画像検索**: 2語以上の組み合わせで期待通りの結果が得られるか
3. **単一画像検索**: 1語のみの場合の動作確認
4. **空テキスト処理**: 空文字列やスペースのみの場合の動作確認

#### 画像検索関数の修正時の注意点
```javascript
// ✅ 必須：句読点除去の正規化処理
const normalizedText = text.toLowerCase()
  .replace(/[^\w\s-]/g, ' ')  // 句読点を除去
  .split(/\s+/)
  .filter(word => word.length >= 2);

// ❌ 禁止：生の split のみ
const words = text.toLowerCase().split(/\s+/);
```

#### 新しい句読点・記号への対応
現在の正規表現 `[^\w\s-]` でカバーされていない文字が問題になる場合：

1. **`extractWordsWithStemming`関数を修正**（全関数に適用）
2. **`findAllImagesByMetaTag`関数を修正**（個別単語処理のみ）
3. **両方の修正を推奨**（統一性のため）

#### テスト用デバッグ関数
```javascript
// 句読点問題の早期発見用
function validatePunctuationHandling() {
  const punctuationCases = [
    "word.", "word?", "word!", "word,", "word;", "word:",
    "word'", "word\"", "word(", "word)", "word[", "word]",
    "two words.", "three word test!"
  ];
  
  punctuationCases.forEach(testCase => {
    const multiResults = window.findAllImagesByMetaTag(testCase);
    const singleResult = window.findImageByMetaTag(testCase);
    console.log(`"${testCase}": 複数=${multiResults.length}, 単一=${singleResult ? '有' : '無'}`);
  });
}
```

### 🎯 将来の拡張方向

1. **多言語対応**: 日本語・中国語等の句読点に対応
2. **文脈理解**: 前後の文脈を考慮したマッチング
3. **学習機能**: ユーザーの選択から最適な画像を学習
4. **画像生成**: 存在しない画像を自動生成

## バージョン履歴

### v2.1 (句読点対応版) - 2025年7月15日
#### 🚨 重要な修正
- **句読点による複数画像表示不具合を修正**
- **対象関数**: `findAllImagesByMetaTag`の個別単語処理ロジック
- **修正内容**: 句読点除去の正規化処理を追加
- **影響範囲**: 全スロット（上位・サブスロット）の文末句読点処理

#### 🔧 技術的改善
- **正規化処理の統一**: 複数画像検索と単一画像検索で同じ句読点処理
- **デバッグ機能の強化**: 句読点問題の早期発見用テスト関数
- **メンテナンス性向上**: 設計仕様書にトラブルシューティング事例を追加

#### 📝 修正詳細
```javascript
// 修正前（問題のあった実装）
const individualWords = text.toLowerCase().split(/\s+/).filter(word => word.length >= 2);

// 修正後（句読点対応）
const individualWords = text.toLowerCase()
  .replace(/[^\w\s-]/g, ' ')  // 句読点を除去
  .split(/\s+/)
  .filter(word => word.length >= 2);
```

#### 🎯 解決した問題
- 「important message.」→ [important.png, message.png] の2枚表示
- 「funny story?」→ [funny.png, story.png] の2枚表示
- 「What do you think!」→ [what.png, think.png] の2枚表示

### v2.0 (汎用システム完成版) - 2025年7月7日
#### 🎯 主要新機能
- **汎用画像システム**: 全上位スロット対応（10スロット統一制御）
- **複数画像横並び表示**: 動的サイズ調整・重複排除・ホバー効果
- **メタタグ自動生成**: ファイル一覧からの自動メタデータ作成
- **責務分離設計**: 汎用制御vs静的制御の明確な境界
- **Type判定連携**: button.png制御との完全統合

#### 🛠️ 技術仕様
- **複数画像対応**: 2枚以上の場合のみコンテナ作成
- **動的レイアウト**: 画像枚数×80px のスロット拡大
- **キャッシュバスター**: タイムスタンプ付きURL生成
- **エラーハンドリング**: 404時の自動placeholder.png適用

#### 🐛 重要な修正
- **空テキスト時の責務分離**: 汎用システムは複数画像クリアのみ実行
- **button.png制御の保護**: 静的システムの専門領域を侵害しない設計
- **DOM競合の解消**: 複数画像↔単一画像の安全な切り替え

### v1.0 (基本実装版) - 2025年7月3日
- メタタグベース画像表示機能
- 上位・サブスロット対応
- 個別ランダマイズ監視
- 居座り防止機構
- 短い単語対応（2文字以上）
- 厳密マッチング方式
- 語幹抽出による活用形対応

---

**最終更新**: 2025年7月15日  
**対応バージョン**: Rephraseプロジェクト完全トレーニングUI完成フェーズ３  
**システム状態**: 汎用イラスト表示システム完全実装完了（句読点対応済み）

## サブスロット画像表示システム 🆕

### 概要

**重要課題**: C1サブスロットの詳細ボタン展開時に、画像が一瞬表示されて消える問題の完全解決

このシステムは、上位スロットと同様にサブスロット（特にC1サブスロット）に自動画像表示機能を提供します。`image_auto_hide.js`との兼ね合いを慎重に考慮し、画像の安定表示を実現しています。

### 核心的な技術的課題と解決方法

#### 🚨 根本的問題: image_auto_hide.js との競合

**問題の詳細**:
1. C1サブスロット画像にキャッシュバスター（`?t=timestamp`）付きURLが使用される
2. `image_auto_hide.js`のHIDDEN_IMAGE_PATTERNSに`'?'`が含まれていた
3. キャッシュバスター付き画像が「？画像（プレースホルダー）」として誤判定され自動非表示になる
4. 結果：画像が一瞬表示されて即座に消える現象

#### ✅ 解決策: 3段階の保護システム

##### 1. HIDDEN_IMAGE_PATTERNSの修正
```javascript
// 🚫 修正前（問題のあった実装）
const HIDDEN_IMAGE_PATTERNS = [
  'placeholder.png',
  '?',  // ← この行がキャッシュバスターと誤判定を引き起こしていた
  'question',
  // ...
];

// ✅ 修正後（安全な実装）
const HIDDEN_IMAGE_PATTERNS = [
  'placeholder.png',
  // '?',  // ← コメントアウト：キャッシュバスターと誤判定するため
  'question',
  // ...
];
```

##### 2. data-meta-tag属性による保護
```javascript
// universal_image_system.js内でC1サブスロット画像に必須属性を設定
imgElement.setAttribute('data-meta-tag', 'true');

// image_auto_hide.js内で保護ロジックを実装
function shouldHideImage(imgElement) {
  // メタタグを持つ画像は常に表示（意図したイラスト）
  if (imgElement.hasAttribute('data-meta-tag')) {
    console.log(`✅ メタタグ付き画像は表示: ${src}`);
    return false; // 非表示にしない
  }
  // ...other logic
}
```

##### 3. 強制表示監視システム
```javascript
// applyImageToSubslot関数内で画像の強制表示を維持
function applyImageToSubslot(slotId, imageData, phraseText) {
  // ...画像設定処理...
  
  // 強制的に表示状態にする
  imgElement.style.display = 'block';
  imgElement.style.visibility = 'visible';
  imgElement.style.opacity = '1';
  imgElement.classList.remove('auto-hidden-image');
  
  // 競合対策：3秒間監視して表示状態を維持
  const forceShowInterval = setInterval(() => {
    if (imgElement.style.display === 'none' || 
        imgElement.classList.contains('auto-hidden-image')) {
      imgElement.style.display = 'block';
      imgElement.classList.remove('auto-hidden-image');
      console.log(`🔧 C1サブスロット画像の表示を強制維持: ${slotId}`);
    }
  }, 100);
  
  // 3秒後に監視終了
  setTimeout(() => clearInterval(forceShowInterval), 3000);
}
```

### ファイル間の連携仕様

#### 関連ファイルと責務

| ファイル | 責務 | 重要な実装 |
|----------|------|-----------|
| `universal_image_system.js` | C1サブスロット画像の自動適用 | `c1SubslotImageSystem`、`applyImageToSubslot` |
| `subslot_renderer.js` | C1サブスロットのDOM制御 | `slotIds`配列への追加、画像保護ロジック |
| `subslot_toggle.js` | 詳細ボタンによる展開制御 | C1サブスロット画像の遅延再適用 |
| `image_auto_hide.js` | 不要画像の自動非表示 | HIDDEN_IMAGE_PATTERNS修正、data-meta-tag保護 |

#### universal_image_system.js の C1サブスロット対応

##### c1SubslotImageSystem オブジェクト
```javascript
const c1SubslotImageSystem = {
  // C1サブスロット用の画像データキャッシュ
  imageCache: new Map(),
  
  // 初期化処理
  initialize() {
    console.log('🎯 C1サブスロット画像システム初期化中...');
    this.applyImagesToAllC1Subslots();
    this.setupC1SubslotObserver();
  },
  
  // 全C1サブスロットに画像を適用
  applyImagesToAllC1Subslots() {
    const c1Subslots = document.querySelectorAll('[id^="slot-c1-sub-"]');
    c1Subslots.forEach(subslot => {
      const slotId = subslot.id;
      const phraseElement = subslot.querySelector('.slot-phrase');
      if (phraseElement) {
        const phraseText = phraseElement.textContent.trim();
        if (phraseText) {
          this.applyImageToC1Subslot(slotId, phraseText);
        }
      }
    });
  },
  
  // 個別C1サブスロットに画像適用
  applyImageToC1Subslot(slotId, phraseText) {
    if (window.imageMetaData && window.imageMetaData.length > 0) {
      const imageData = findImageByMetaTag(phraseText);
      if (imageData) {
        applyImageToSubslot(slotId, imageData, phraseText);
      }
    }
  }
};
```

#### subslot_renderer.js の修正点

##### slotIds配列への追加
```javascript
// C1サブスロットIDの動的追加
function addC1SubslotToSlotIds() {
  const c1Subslots = document.querySelectorAll('[id^="slot-c1-sub-"]');
  c1Subslots.forEach(subslot => {
    const slotId = subslot.id;
    if (!slotIds.includes(slotId)) {
      slotIds.push(slotId);
      console.log(`📝 SlotIds配列にC1サブスロット追加: ${slotId}`);
    }
  });
}
```

##### 画像保護ロジック
```javascript
function renderSubslotData(/* parameters */) {
  // ...既存のレンダリング処理...
  
  // C1サブスロット画像の保護ロジック
  if (slotId.startsWith('slot-c1-sub-') && imageElement) {
    // data-meta-tag属性を持つ画像は上書きしない
    if (imageElement.hasAttribute('data-meta-tag')) {
      console.log(`🛡️ C1サブスロット画像を保護（上書きスキップ）: ${slotId}`);
      return; // 画像の上書きを防止
    }
  }
  
  // ...残りの処理...
}
```

#### subslot_toggle.js の拡張

##### 詳細ボタン展開時の画像再適用
```javascript
function toggleSubslots(mainSlotId, isCollapsing = false) {
  // ...既存の展開処理...
  
  // C1サブスロット画像の遅延再適用
  if (mainSlotId === 'slot-c1') {
    setTimeout(() => {
      if (typeof window.c1SubslotImageSystem !== 'undefined' && 
          window.c1SubslotImageSystem.applyImagesToAllC1Subslots) {
        window.c1SubslotImageSystem.applyImagesToAllC1Subslots();
        console.log('🔄 C1サブスロット展開後の画像再適用完了');
      }
    }, 200); // DOM更新待機
  }
}
```

### 重要な注意事項とトラブルシューティング

#### ⚠️ 必須の実装順序

1. **image_auto_hide.js の修正が最優先**
   ```javascript
   // この修正なしでは他の対策も無効
   // '?' → // '?' にコメントアウト必須
   ```

2. **data-meta-tag 属性の確実な設定**
   ```javascript
   // universal_image_system.js内で必須
   imgElement.setAttribute('data-meta-tag', 'true');
   ```

3. **DOM更新タイミングの調整**
   ```javascript
   // subslot_toggle.js で適切な遅延設定
   setTimeout(() => { /* 画像再適用 */ }, 200);
   ```

#### 🔍 デバッグ方法

##### 画像消失の監視関数
```javascript
// ブラウザコンソールで実行
function watchImageChanges() {
  const c1Images = document.querySelectorAll('[id^="slot-c1-sub-"] .slot-image');
  c1Images.forEach(img => {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach(mutation => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'src') {
          console.log(`🔄 画像src変更: ${img.closest('[id^="slot-c1-sub-"]').id}`);
          console.log(`旧: ${mutation.oldValue}`);
          console.log(`新: ${img.src}`);
        }
      });
    });
    observer.observe(img, { 
      attributes: true, 
      attributeOldValue: true, 
      attributeFilter: ['src'] 
    });
  });
}
```

##### 画像状態の確認
```javascript
// 現在のC1サブスロット画像状態を確認
function checkC1SubslotImages() {
  const c1Images = document.querySelectorAll('[id^="slot-c1-sub-"] .slot-image');
  c1Images.forEach(img => {
    console.log(`🖼️ ${img.closest('[id^="slot-c1-sub-"]').id}:`);
    console.log(`  src: ${img.src}`);
    console.log(`  data-meta-tag: ${img.getAttribute('data-meta-tag')}`);
    console.log(`  display: ${img.style.display}`);
    console.log(`  visibility: ${img.style.visibility}`);
  });
}
```

### 動作確認手順

1. **ブラウザでindex.htmlを開く**
2. **C1スロットの詳細ボタンをクリック**
3. **C1サブスロットが展開されることを確認**
4. **C1サブスロット内の画像が安定して表示されることを確認**
5. **画像が消えないことを確認（重要）**

### 成功指標

- ✅ C1サブスロット画像が詳細ボタン展開時に即座に表示される
- ✅ 画像が表示後に消えることがない
- ✅ 上位スロットの画像システムに影響を与えない
- ✅ 語順や他の機能に齟齬が生じない

---

**🎯 この仕様により、ロールバック後でも新たな担当者が簡単にC1サブスロット画像システムを再実装できます。**

---

## 【2025年7月8日完成】サブスロット複数画像表示システム 🎉

**状況**: 上位スロットの複数画像表示システムと同等の機能をサブスロット（特にC1サブスロット）に完全実装済み

### 完成機能一覧

#### ✅ 複数画像横並び表示
- **機能**: 1つのサブスロットに複数の関連画像を自動検索・横並び表示
- **動作**: テキストから複数キーワードを抽出し、各キーワードにマッチする画像を並列表示
- **サイズ調整**: 画像枚数に応じてサブスロット全体の横幅を自動拡大（上位スロットと同じロジック）
- **表示方式**: `object-fit: fill` による縦横比を維持しない全体表示（切り取りなし）

#### ✅ 単一画像適切表示
- **サイズ**: 150px × 150px（複数画像時と統一）
- **表示方式**: `object-fit: fill !important` による伸縮表示（切り取りではなく全体表示）
- **スタイル**: 上位スロットと同じ緑系ボーダー、角丸5px

#### ✅ 自動フォールバック機能
- **複数マッチ**: 複数画像コンテナで横並び表示
- **単一マッチ**: 単一画像表示（複数画像コンテナは自動削除）
- **マッチなし**: プレースホルダー画像表示
- **空テキスト**: 全ての画像コンテナを削除し、従来処理に移行

#### ✅ 個別ランダマイズ対応
- **問題**: 個別ランダマイズ実行後にサブスロット画像が消失
- **解決**: `randomizer_individual.js`の各個別ランダマイズ関数に`updateSubslotImages()`呼び出しを追加
- **タイミング**: 上位スロット更新(100ms)→サブスロット更新(200ms)の段階的実行

### 実装済み関数一覧

#### `universal_image_system.js` 新規追加関数

```javascript
// サブスロット専用複数画像適用関数
function applyMultipleImagesToSubslot(subslotId, phraseText, forceRefresh = false)

// サブスロット専用単一画像適用関数（フォールバック用）
function applyImageToSubslot(subslotId, phraseText, forceRefresh = false)

// サブスロット画像更新システム（C1専用）
function updateSubslotImages(parentSlotId)

// デバッグ・監視関数群
function monitorSubslotImageState(subslotId, duration = 5000)
function forceUpdateSubslotImages()
function debugImageDisappearance()
```

#### グローバル公開関数

```javascript
// 新規追加されたグローバル関数
window.applyMultipleImagesToSubslot = applyMultipleImagesToSubslot;
window.applyImageToSubslot = applyImageToSubslot;
window.updateSubslotImages = updateSubslotImages;
window.monitorSubslotImageState = monitorSubslotImageState;
window.forceUpdateSubslotImages = forceUpdateSubslotImages;
window.debugImageDisappearance = debugImageDisappearance;
```

### サイズ仕様（上位スロットと統一）

#### 複数画像表示時

| 設定項目 | 値 | 説明 |
|----------|-------|------|
| **基本コンテナ幅** | 390px | 上位スロットと同じ |
| **画像1枚あたり最小幅** | 50px | 上位スロットと同じ |
| **画像1枚あたり最大幅** | 120px | 上位スロットと同じ |
| **画像間隙間** | 6px | 上位スロットと同じ |
| **拡大率** | +80px/枚 | 1枚増えるごとに+80px |
| **画像高さ** | 150px | 縦方向めいっぱい |
| **コンテナ高さ** | 160px | 上位スロットと同じ |

#### 単一画像表示時

| 設定項目 | 値 | 説明 |
|----------|-------|------|
| **画像サイズ** | 150px × 150px | 複数画像時と統一 |
| **表示方式** | `object-fit: fill !important` | 伸縮表示（切り取りなし） |
| **ボーダー** | 1px solid rgba(40, 167, 69, 0.6) | 緑系統一 |
| **角丸** | 5px | 複数画像時と統一 |

### 個別ランダマイズ修正例

#### C1スロット個別ランダマイズ (`randomizer_individual.js`)

```javascript
// 修正前（画像更新不足）
if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
  setTimeout(() => {
    window.updateAllSlotImagesAfterDataChange();
    console.log("🎨 全スロット画像更新完了");
  }, 100);
}

// 修正後（サブスロット画像更新追加）✅
if (typeof window.updateAllSlotImagesAfterDataChange === "function") {
  setTimeout(() => {
    window.updateAllSlotImagesAfterDataChange();
    console.log("🎨 全スロット画像更新完了");
  }, 100);
}

// 🆕 サブスロット画像更新（C1専用）
if (typeof window.updateSubslotImages === "function") {
  setTimeout(() => {
    window.updateSubslotImages('c1');
    console.log("🎨 C1サブスロット画像更新完了");
  }, 200);
}
```

### 水平展開準備完了

#### 他スロット対応のパターン

**S、M1、AUX、V、M2、O1、O2、C2、M3**スロットの個別ランダマイズ関数にも同様の修正を適用可能：

```javascript
// 各スロットの個別ランダマイズ関数末尾に追加
if (typeof window.updateSubslotImages === "function") {
  setTimeout(() => {
    window.updateSubslotImages('[スロット名小文字]'); // 例: 's', 'm1', 'aux'等
    console.log("🎨 [スロット名]サブスロット画像更新完了");
  }, 200);
}
```

#### `updateSubslotImages()` 関数の対応スロット拡張

```javascript
// 現在: C1のみ対応
if (parentSlotId !== 'c1') {
  console.log(`⏭️ テスト段階のため ${parentSlotId} はスキップします（C1スロットのみ対象）`);
  return;
}

// 拡張時: 全スロット対応に変更
const supportedSlots = ['c1', 's', 'm1', 'aux', 'v', 'm2', 'o1', 'o2', 'c2', 'm3'];
if (!supportedSlots.includes(parentSlotId)) {
  console.log(`⏭️ 未対応スロット: ${parentSlotId}`);
  return;
}
```

### テスト・デバッグ機能

#### コンソールテスト関数

```javascript
// C1サブスロットの強制画像更新テスト
forceUpdateSubslotImages();

// 特定サブスロットの画像状態監視（5秒間）
monitorSubslotImageState('slot-c1-sub-c1', 5000);

// 画像消失問題の詳細デバッグ
debugImageDisappearance();
```

### 成功実績

#### ✅ 達成項目
- **複数画像横並び表示**: 2枚以上の関連画像を自動検索・横並び表示
- **適切なサイズ調整**: 画像枚数に応じた動的幅調整
- **縦横比の適切な処理**: 切り取りではなく伸縮による全体表示
- **個別ランダマイズ対応**: ランダマイズ後も画像が正常表示継続
- **既存システム非破壊**: 上位スロットの機能に一切影響なし
- **統一されたUI**: 上位スロットと同じスタイル・動作

#### 🎯 完成度
- **C1サブスロット**: 100%完成
- **他サブスロット**: 水平展開準備完了（設計完成、実装パターン確立）

### 今後の拡張作業

1. **他スロットへの水平展開**: `updateSubslotImages()`の対応スロット追加
2. **個別ランダマイズ全対応**: 全スロットの個別ランダマイズ関数修正
3. **パフォーマンス最適化**: 必要に応じてキャッシュ機構の強化

---

## 【2025年7月25日完成】個別ランダマイズ対応・サブスロット幅調整システム 🎯

**実装背景**: 個別ランダマイズ実行時にサブスロットの複数画像表示でスロット幅が適切に調整されない問題が発生。初回サブスロット展開時は正常に機能するが、個別ランダマイズによる「動的生成」時に幅調整機能が失われる現象を完全解決。

### 問題の詳細分析

#### 🚨 根本的課題
1. **動的生成による初期化問題**: 個別ランダマイズ時はサブスロットが再生成され、初期状態にリセット
2. **タイミング制御不足**: `applyMultipleImagesToSubslot`内の幅調整が確実に実行されない
3. **専用機構の不在**: 個別ランダマイズ後の強制的な幅調整システムが未実装

#### 📋 症状
- **初回展開**: ✅ 複数画像時にスロット幅が適切に拡大
- **個別ランダマイズ後**: ❌ 複数画像が表示されるがスロット幅が狭いまま
- **結果**: 画像が重なったり、見切れたりして視認性が悪化

### 実装した解決策

#### 🔧 新規実装: `ensureSubslotWidthForMultipleImages`関数

**場所**: `universal_image_system.js`（2025年7月25日追加）

```javascript
// 🎯 個別ランダマイズ専用：サブスロット幅調整強制実行関数
function ensureSubslotWidthForMultipleImages(parentSlotId) {
  // サブスロットコンテナ検証
  const subslotContainer = document.getElementById(`slot-${parentSlotId}-sub`);
  
  // 表示中のサブスロット検索
  const visibleSubslots = Array.from(subslotContainer.children).filter(child => {
    return child.id && child.id.includes('sub') && 
           window.getComputedStyle(child).display !== 'none';
  });
  
  visibleSubslots.forEach(subslot => {
    const multiImageContainer = subslot.querySelector('.multi-image-container');
    if (!multiImageContainer) return;
    
    const images = multiImageContainer.querySelectorAll('.slot-multi-image');
    if (images.length <= 1) return;
    
    // 🎯 強制的なスロット幅調整（上位スロットと同じロジック）
    const imageCount = images.length;
    const largerOptimalImageWidth = 120;
    const gap = 6;
    const requiredImageWidth = imageCount * largerOptimalImageWidth + (imageCount - 1) * gap + 60;
    
    const currentWidth = subslot.offsetWidth || 200;
    const finalWidth = Math.max(currentWidth, requiredImageWidth);
    
    // 強制的にスタイル適用
    subslot.style.width = finalWidth + 'px';
    subslot.style.minWidth = finalWidth + 'px';
    subslot.style.maxWidth = finalWidth + 'px';
    
    // 各画像のサイズも再調整
    const availableWidth = finalWidth - (imageCount - 1) * gap - 40;
    const dynamicWidth = Math.min(120, Math.max(80, Math.floor(availableWidth / imageCount)));
    
    images.forEach(img => {
      img.style.width = dynamicWidth + 'px';
      img.style.maxWidth = dynamicWidth + 'px';
      img.style.minWidth = '80px';
    });
  });
}
```

#### 🔄 個別ランダマイズ関数の統合修正

**対象**: 全8つの個別ランダマイズ関数（S, M1, M2, C1, O1, O2, C2, M3）

**修正パターン**:
```javascript
// 150ms: サブスロット画像更新
if (typeof window.updateSubslotImages === "function") {
  setTimeout(() => {
    window.updateSubslotImages('[スロット名]');
    console.log("🎨 [スロット名]サブスロット画像更新完了");
  }, 150);
}

// 🆕 250ms: サブスロット幅調整強制実行
if (typeof window.ensureSubslotWidthForMultipleImages === "function") {
  setTimeout(() => {
    window.ensureSubslotWidthForMultipleImages('[スロット名]');
    console.log("📏 [スロット名]サブスロット幅調整完了");
  }, 250);
}

// 300ms: 複数画像システム更新
if (typeof window.refreshAllMultipleImages === "function") {
  setTimeout(() => {
    window.refreshAllMultipleImages();
    console.log("🎨 [スロット名]複数画像システム更新完了");
  }, 300);
}
```

### 技術的特徴

#### 🎯 確実性の担保
- **存在確認**: サブスロットコンテナ、複数画像コンテナの存在を段階的に確認
- **条件判定**: 複数画像（2枚以上）の場合のみ処理実行
- **強制適用**: `style`プロパティによる直接的なスタイル適用

#### ⚡ 効率性の追求
- **必要時のみ実行**: 複数画像表示時のみ幅調整を実行
- **処理分散**: タイミング制御による負荷分散
- **統一ロジック**: 上位スロットと同じ計算式で一貫性確保

#### 🛡️ 安全性の確保
- **エラーハンドリング**: 各段階での適切な検証
- **既存機能保護**: 単一画像表示、通常動作に影響なし
- **デバッグ支援**: 詳細なログ出力で動作状況を可視化

### 対応完了スロット

| スロット | 名称 | 個別ランダマイズ関数 | サブスロット幅調整 |
|----------|------|-------------------|------------------|
| **S** | 主語 | `randomizeSlotSIndividual` | ✅ 完了 |
| **M1** | 修飾語1 | `randomizeSlotM1Individual` | ✅ 完了 |
| **M2** | 修飾語2 | `randomizeSlotM2Individual` | ✅ 完了 |
| **C1** | 補語1 | `randomizeSlotC1Individual` | ✅ 完了 |
| **O1** | 目的語1 | `randomizeSlotO1Individual` | ✅ 完了 |
| **O2** | 目的語2 | `randomizeSlotO2Individual` | ✅ 完了 |
| **C2** | 補語2 | `randomizeSlotC2Individual` | ✅ 完了 |
| **M3** | 修飾語3 | `randomizeSlotM3Individual` | ✅ 完了 |

### 動作確認手順

1. **初回サブスロット展開**: 複数画像が適切な幅で表示されることを確認
2. **個別ランダマイズ実行**: 新しい複数画像表示でも適切な幅が維持されることを確認
3. **コンソールログ確認**: `📏 [スロット名]サブスロット幅調整完了` の表示を確認
4. **視覚確認**: 画像の重なりや見切れがないことを確認

### 学習効果への貢献

#### 🎯 視覚的学習体験の向上
- **見やすさ向上**: 複数画像が適切に配置され、学習者の理解を促進
- **操作性向上**: 個別ランダマイズ後も一貫した表示品質を維持
- **集中力維持**: UI不具合による学習阻害要因を完全排除

#### 🚀 システム信頼性の向上
- **操作予測性**: ランダマイズ機能が常に期待通りの結果を提供
- **UI一貫性**: 初回展開と個別ランダマイズ後で同じ表示品質
- **バグ回避**: 視覚的不具合による学習中断を防止

### デバッグ・メンテナンス

#### 🔍 トラブルシューティング
```javascript
// ブラウザコンソールでの確認コマンド
window.ensureSubslotWidthForMultipleImages('c1'); // C1サブスロットの強制幅調整
```

#### 📊 状態確認方法
- **コンソールログ**: 各段階の処理状況を詳細に出力
- **DOM検査**: 開発者ツールでスタイル適用状況を確認
- **関数テスト**: 個別関数の手動実行による動作確認

---

**🏆 サブスロット画像表示システムは上位スロットと同等の機能を持つ完全なシステムとして完成しました。**

---

## 📐 スロット幅制御システム詳細仕様

### 2025-08-01 重要修正：M1スロット幅問題解決

#### 問題概要
M1スロットが画像枚数に関係なく異常に幅広になる問題が発生。特にモバイル環境で顕著に現れ、2枚時は正常だが4枚時に507px幅になる現象。

#### 根本原因分析
1. **モバイル判定失敗**: `mobile-device`クラスベースの判定が開発環境で機能せず
2. **変数スコープエラー**: `isMobile`変数が条件分岐内でのみ定義され、後続処理でエラー発生
3. **テキスト幅上限不適切**: PC版600px上限が高すぎて2枚時にアンバランス

#### 解決策実装

##### 1. 堅牢なモバイル判定システム
```javascript
// 3重判定による確実なモバイル検出
const isMobile = document.body.classList.contains('mobile-device') || 
                /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                window.innerWidth <= 768;
```

##### 2. デバイス別幅制御パラメータ
```javascript
// テキスト幅上限
const maxTextWidth = isMobile ? 350 : 400; // モバイル350px、PC400px

// 画像サイズ
const largerOptimalImageWidth = isMobile ? 80 : 120; // モバイル80px、PC120px
```

##### 3. スロット幅計算ロジック
```javascript
// 最終幅決定式
const finalSlotWidth = Math.max(textBasedWidth, requiredImageWidth);

// 画像必要幅計算
const requiredImageWidth = imageCount * largerOptimalImageWidth + (imageCount - 1) * gap + 60;
```

#### 最終仕様
- **モバイル環境**
  - テキスト幅上限: 350px
  - 画像幅: 80px
  - 2枚時想定幅: max(350px, 228px) = 350px
  - 4枚時想定幅: max(350px, 404px) = 404px

- **PC環境**
  - テキスト幅上限: 400px  
  - 画像幅: 120px
  - 2枚時想定幅: max(400px, 308px) = 400px
  - 4枚時想定幅: max(400px, 564px) = 564px

#### 重要な実装上の注意点
1. **変数スコープ**: `isMobile`は必ず関数上位スコープで定義する
2. **モバイル判定**: 単一条件ではなく3条件のOR結合で実装する
3. **デバッグ時**: 画面サイズ変更後は必ずページリロードで確認する
4. **将来の調整**: 上限値変更時は画像枚数との関係を考慮する

#### トラブルシューティング
```javascript
// デバッグ用確認コマンド
const isMobile = document.body.classList.contains('mobile-device') || 
                /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                window.innerWidth <= 768;
console.log('モバイル判定:', isMobile);
console.log('画面幅:', window.innerWidth);

// M1スロット状態確認
const m1 = document.getElementById('slot-m1');
console.log('M1幅:', m1.offsetWidth, 'px');
console.log('M1画像数:', m1.querySelectorAll('img').length);
```

この修正により、M1スロットを含む全スロットで画像枚数に応じた適切な幅制御が実現されました。
