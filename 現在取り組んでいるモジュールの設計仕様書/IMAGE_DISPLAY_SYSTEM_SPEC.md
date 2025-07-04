# イラスト自動表示機構 設計仕様書

## 概要

Rephraseプロジェクトにおいて、スロット内のテキストに基づいて自動的に関連するイラストを表示する機能です。上位スロット・サブスロット問わず、単語の意味に応じた画像を動的に適用し、個別ランダマイズ時の画像更新にも対応します。

## システム構成

### ファイル構成

```
project-root/
├── image_meta_tags.json          # メタタグデータベース
├── js/image_meta_tag_system.js   # 画像表示制御ロジック
├── slot_images/                  # 画像ファイル格納ディレクトリ
│   ├── common/
│   │   └── placeholder.png       # デフォルト画像
│   ├── people/                   # 人物関連画像
│   ├── actions/                  # 動作関連画像
│   ├── objects/                  # 物体関連画像
│   └── [その他カテゴリ]/
└── index.html                    # メインUI
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

### `js/image_meta_tag_system.js` アーキテクチャ

#### 主要関数

##### 1. `loadImageMetaTagsOnStartup()`
- **目的**: メタタグデータの初期読み込み
- **戻り値**: `Promise<boolean>`
- **特徴**: キャッシュ無効化クエリパラメータ付きfetch

##### 2. `extractWordsWithStemming(text)`
- **目的**: テキストから検索対象単語を抽出
- **処理内容**:
  - 2文字以上の単語を対象（短い重要語に対応）
  - 最小限の語幹抽出（-s, -ed, -ing）
  - 元単語 + 語幹の両方を検索対象に含める

##### 3. `findImageByMetaTag(text)`
- **目的**: テキストにマッチする画像を検索
- **マッチング方式**: 厳密一致のみ（部分マッチ無し）
- **優先度制御**: `priority`フィールドに基づく最適マッチ選択

##### 4. `applyImageToSlot(slotElement, phraseText, forceRefresh)`
- **目的**: 単一スロットへの画像適用
- **居座り防止**: 同一画像の重複適用回避
- **表示制御**: visibility/opacity/display の正規化

##### 5. `clearSlotImage(slotElement)`
- **目的**: スロット画像のクリア
- **安全性**: メタタグ画像・プレースホルダーのみ対象

##### 6. `applyMetaTagImagesToAllSlots(forceRefresh)`
- **目的**: 全スロット一括画像適用
- **対象**: `.slot-container` + `.subslot-container`

##### 7. `handleSlotTextChange(slotElement)`
- **目的**: テキスト変更時の画像更新
- **処理フロー**: クリア → 新規適用（居座り防止）

##### 8. `setupIndividualRandomizeObserver()`
- **目的**: DOM変更監視・自動画像更新
- **監視方式**: MutationObserver
- **対象**: `#training-container` 内の `characterData` + `childList`

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

## 既知の制限・課題

### 現在の制限事項

1. **単語レベルマッチング**: フレーズ全体での意味理解は未対応
2. **文脈依存性**: 同一単語の複数意味への対応限定的
3. **大文字小文字**: 小文字変換後のマッチングのみ
4. **特殊文字**: ハイフン以外の記号は除去される

### 今後の改善候補

1. **フレーズマッチング**: 複数単語での検索対応
2. **曖昧マッチング**: 編集距離ベースの近似マッチ
3. **学習機能**: ユーザー選択に基づく優先度自動調整
4. **パフォーマンス**: 大量データでの検索最適化

## 運用・保守

### メタタグデータ更新手順

1. `image_meta_tags.json` 編集
2. 画像ファイルを適切なディレクトリに配置
3. ブラウザキャッシュクリア（自動クエリパラメータで対応済み）
4. ページリロード

### トラブルシューティング

#### 画像が表示されない場合

1. **ブラウザコンソール確認**
   ```javascript
   window.debugStrictMatching()
   ```

2. **メタタグデータ読み込み状況確認**
   ```javascript
   console.log(window.imageMetaTagsLoaded, window.imageMetaTagsData?.length)
   ```

3. **DOM構造確認**
   - `.slot-container` / `.subslot-container` の存在
   - `.slot-phrase` 要素の存在
   - `.slot-image` 要素の存在

#### 画像が更新されない場合

1. **MutationObserver 動作確認**
2. **テキスト変更イベント発生確認**
3. **同一画像スキップロジック確認**

## バージョン履歴

### v1.0 (実装完了版)
- メタタグベース画像表示機能
- 上位・サブスロット対応
- 個別ランダマイズ監視
- 居座り防止機構
- 短い単語対応（2文字以上）
- 厳密マッチング方式
- 語幹抽出による活用形対応

---

**最終更新**: 2025年7月3日  
**対応バージョン**: Rephraseプロジェクト完全トレーニングUI完成フェーズ３
