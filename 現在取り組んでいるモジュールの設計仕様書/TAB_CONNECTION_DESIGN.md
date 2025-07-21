# エクセル風タブ連結システム 設計仕様書

## 🎯 設計目標
- 上位スロットとサブスロットの視覚的一体感を向上
- どの上位スロットのサブスロットが展開中かを明確化
- サブスロットの位置を上位スロット直下に近づける
- エクセルのようなタブ連結UI/UXを実現

## 🔗 統一設計方針

### 1. タブ連結の視覚的表現
- **親スロット**: 薄い黄色背景 (`rgba(254, 243, 199, 0.6)`) + 黄色系境界線 (`#f59e0b`)
- **サブスロットエリア**: より薄い黄色背景 (`rgba(254, 243, 199, 0.4)`) + 連結境界線
- **境界線の連結**: 親の下部境界線とサブエリアの上部境界線を除去して視覚的統合

### 2. タブ風ラベル
- **背景**: 薄い黄色のグラデーション (`#fffbeb` → `#fef3c7`)
- **テキスト色**: 温かみのあるブラウン (`#78716c`)
- **形状**: 上部角丸 (`border-radius: 8px 8px 0 0`)
- **アイコン**: 📂 フォルダアイコン + スロット名

### 3. 位置調整システム
- サブスロットエリアを親スロットの水平位置に合わせる
- `margin-left` と `max-width` でレスポンシブ調整
- ウィンドウリサイズ時の自動再調整

### 4. 制御パネル連携
- サブスロット制御パネルもタブ連結スタイルを適用
- 黄色系グラデーション背景 (`rgba(254, 243, 199, 0.5)` → `rgba(251, 191, 36, 0.3)`)
- 黄色系境界線とシャドウで統一感を演出

## 📋 実装ファイル

### JavaScript
- **`js/subslot_toggle.js`**: メイン制御ロジック
  - `applyTabConnection(slotId, isActive)`: タブ連結適用/解除
  - `adjustSubslotPosition(slotId)`: 位置調整
  - `clearAllTabConnections()`: 全てのタブ連結クリア

### CSS
- **`style.css`**: 視覚スタイル定義
  - `.active-parent-slot`: 親スロットのタブ連結スタイル
  - `.active-subslot-area`: サブスロットエリアのタブ連結スタイル
  - `.tab-style`: タブ風ラベルスタイル
  - `.tab-connected`: 制御パネル連結スタイル

## 🔄 動作フロー

1. **サブスロット展開時**:
   - 他の全タブ連結をクリア (`clearAllTabConnections()`)
   - 親スロットに `.active-parent-slot` 追加
   - サブエリアに `.active-subslot-area` 追加
   - ラベルに `.tab-style` 追加とテキスト更新
   - 位置調整実行 (`adjustSubslotPosition()`)
   - 制御パネルに `.tab-connected` 追加

2. **サブスロット閉じる時**:
   - 全タブ連結スタイルクリア
   - 位置調整スタイルリセット
   - 制御パネル削除

3. **ウィンドウリサイズ時**:
   - 展開中のサブスロットの位置を再調整

## 🎨 視覚的統一要素

### カラーパレット（2025年7月21日 最新実装）
- **メイン黄色**: `#f59e0b` (アンバーオレンジ)
- **背景黄色**: `rgba(254, 243, 199, 0.6)` (親) / `rgba(254, 243, 199, 0.4)` (子)
- **タブ黄色**: `#fffbeb` → `#fef3c7` (薄い黄色グラデーション)
- **テキスト色**: `#78716c` (温かみのあるブラウン)
- **境界線**: `#f59e0b` (2px solid)

### エフェクト
- **アニメーション**: `tabConnect` (0.3s ease-out)
- **シャドウ**: 黄色系で連結感を演出する多層シャドウ (`rgba(245, 158, 11, 0.3)`)
- **ホバー効果**: 親スロットのリフトアップ効果

## 💻 コード制御箇所

### 1. 親スロット（展開時）の配色制御
**ファイル**: `style.css`  
**セレクタ**: `.slot-container.active-parent-slot`  
**行数**: 約1319行目

```css
.slot-container.active-parent-slot {
  background: rgba(254, 243, 199, 0.6) !important; /* 🌻 薄い黄色背景 */
  border: 2px solid #f59e0b !important; /* 🌻 黄色系境界線 */
  box-shadow: 0 -2px 8px rgba(245, 158, 11, 0.3) !important; /* 🌻 黄色系シャドウ */
}
```

### 2. サブスロットエリアの配色制御
**ファイル**: `style.css`  
**セレクタ**: `.slot-wrapper.active-subslot-area`  
**行数**: 約1348行目

```css
.slot-wrapper.active-subslot-area {
  background: rgba(254, 243, 199, 0.4) !important; /* 🌻 親より薄い黄色 */
  border: 2px solid #f59e0b !important; /* 🌻 黄色系境界線 */
  box-shadow: 0 -2px 4px rgba(245, 158, 11, 0.3) !important; /* 🌻 黄色系シャドウ */
}
```

### 3. タブラベルの配色制御
**ファイル**: `style.css`  
**セレクタ**: `.subslot-label.tab-style`  
**行数**: 約1380行目

```css
.subslot-label.tab-style {
  background: linear-gradient(135deg, #fffbeb, #fef3c7) !important; /* 🌻 薄い黄色グラデーション */
  color: #78716c !important; /* 🌻 黄色背景に温かみのあるブラウン文字 */
  border-radius: 8px 8px 0 0 !important;
}
```

### 4. 制御パネル連結時の配色制御
**ファイル**: `style.css`  
**セレクタ**: `.subslot-control-panel.tab-connected`  
**行数**: 約1422行目

```css
.subslot-control-panel.tab-connected {
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.5), rgba(251, 191, 36, 0.3)) !important;
  border: 1px solid #f59e0b !important;
  box-shadow: 0 2px 6px rgba(245, 158, 11, 0.2) !important;
}
```

### 5. JavaScript制御箇所
**ファイル**: `js/subslot_toggle.js`  
**関数**: `applyTabConnection(slotId, isActive)`

```javascript
// タブ連結適用時にクラス追加
parentSlot.classList.add('active-parent-slot');
subslotArea.classList.add('active-subslot-area');
tabLabel.classList.add('tab-style');
controlPanel.classList.add('tab-connected');
```

## 🚀 今後の拡張予定
- タブの順序変更機能
- 複数サブスロット同時展開対応
- タブアニメーションの改善
- アクセシビリティ対応

## 📝 注意事項
- 一度に1つのサブスロットのみ展開可能
- 位置調整はCSSカスタムプロパティとinlineスタイルの併用
- ブラウザウィンドウサイズに応じた動的調整

## 🔧 配色変更時の手順

### 1. 基本色の変更
主要な黄色系を変更する場合は、以下の箇所を統一して修正：

1. **親スロット背景**: `style.css` 1319行目 `rgba(254, 243, 199, 0.6)`
2. **サブエリア背景**: `style.css` 1348行目 `rgba(254, 243, 199, 0.4)`
3. **境界線色**: 全箇所の `#f59e0b`
4. **シャドウ色**: 全箇所の `rgba(245, 158, 11, 0.3)`

### 2. タブラベル専用色の変更
タブラベルのみ変更する場合：

1. **背景グラデーション**: `style.css` 1380行目 `#fffbeb` → `#fef3c7`
2. **テキスト色**: `style.css` 1380行目 `#78716c`

### 3. 変更時の確認ポイント
- [ ] 親スロットとサブエリアの色階調が適切か
- [ ] テキストのコントラスト比が十分か（WCAG AA基準）
- [ ] 他のUI要素との調和が取れているか
- [ ] 全ブラウザでの表示確認

---

**最終更新**: 2025年7月21日  
**更新理由**: 黄色系配色実装に伴う仕様書修正  
**確認済みブラウザ**: Chrome, Firefox, Safari, Edge
