# イラスト自動表示機構 設計仕様書

## 概要

Rephraseプロジェクトにおいて、スロット内のテキストに基づいて自動的に関連するイラストを表示する汎用システムです。上位スロット全体に対応し、単語の意味に応じた画像を動的に適用、複数画像の横並び表示、メタタグ自動生成、Type判定による表示制御、責務分離設計を実現しています。

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

## バージョン履歴

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

**最終更新**: 2025年7月7日  
**対応バージョン**: Rephraseプロジェクト完全トレーニングUI完成フェーズ３  
**システム状態**: 汎用イラスト表示システム完全実装完了
