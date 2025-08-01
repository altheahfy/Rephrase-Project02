# JavaScript Architecture Document
**Rephrase English Learning System v2025.07.27-1**  
**Generated:** 2025年8月1日  
**Status:** Production Environment

## 📋 概要

このドキュメントは、Rephraseシステムの本番環境で使用されているJavaScriptファイルの役割と依存関係を記録しています。開発過程で作成された未使用ファイルは全て保管庫に移動済みです。

## 🏗️ アーキテクチャ構成

### ESModule システム（ES6 import/export）
モジュール間の依存関係を管理し、名前空間の衝突を防ぐ現代的なアーキテクチャ。

### Script Tag システム（従来型）
グローバルスコープで動作し、DOMイベントやユーザーインタラクションを直接処理。

## 📁 ファイル一覧と役割

### 🔒 セキュリティ・認証システム
#### `security.js` ★ESModule
- **役割**: セキュリティ機能の中核
- **機能**: ファイルアップロード検証、HTMLエスケープ、XSS防止
- **Export**: `initSecurity()`, `validateFileUpload()`, `escapeHtml()`
- **使用場所**: `training/index.html` (最優先で読み込み)
- **依存関係**: なし

#### `auth.js`
- **役割**: 認証システム
- **機能**: ユーザー認証、セッション管理
- **使用場所**: `training/index.html`
- **依存関係**: 
  - `window.rateLimiter` (rate-limiter.js)
  - `window.errorHandler` (error-handler.js) 
  - `window.securityUtils` (training/index.html内定義)

#### `rate-limiter.js`
- **役割**: レート制限機能
- **機能**: API呼び出し頻度制限、DoS攻撃防止
- **使用場所**: `training/index.html`
- **依存関係**: なし
- **提供**: `window.rateLimiter` (グローバルオブジェクト)

#### `error-handler.js`
- **役割**: エラーハンドリングシステム
- **機能**: エラー表示、ログ管理、ユーザー通知
- **使用場所**: `training/index.html`
- **依存関係**: なし
- **提供**: `window.errorHandler` (グローバルオブジェクト)

### 🎯 コア機能システム
#### `structure_builder.js` ★ESModule
- **役割**: DOM構造構築
- **機能**: スロット構造の動的生成、HTMLテンプレート管理
- **Export**: `buildStructure()`
- **使用場所**: `training/index.html` (ESModule import)
- **依存関係**: なし

#### `randomizer_all.js` ★ESModule
- **役割**: 全体ランダマイザー機能
- **機能**: 全スロットの一括ランダム化、状態管理
- **Export**: `randomizeAll()`, `randomizeAllWithStateManagement()`
- **使用場所**: `training/index.html` (ESModule import)
- **依存関係**: なし

#### `randomizer_individual.js`
- **役割**: 個別スロットランダマイザー
- **機能**: 単一スロットのランダム化、個別制御
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `insert_test_data_clean.js`
- **役割**: 動的記載エリア監視・同期システム
- **機能**: 
  - `dynamic-slot-area`の変更監視（MutationObserver使用）
  - `window.loadedJsonData`から例文データを読み取り
  - 動的記載エリアから静的DOMへのデータ同期
  - サブスロット順序制御、DisplayAtTop処理
- **使用場所**: `training/index.html`
- **依存関係**: `window.loadedJsonData` (グローバル変数)
- **提供**: 処理完了シグナル (image_auto_hide.jsが待機)

### 🎛️ UI制御システム
#### `control_panel_manager.js`
- **役割**: コントロールパネル管理
- **機能**: 設定パネル、ユーザーインターフェース制御
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `visibility_control.js`
- **役割**: 要素表示制御
- **機能**: スロット・要素の表示/非表示切り替え、`questionWordVisibilityState`宣言
- **使用場所**: `training/index.html`
- **依存関係**: なし
- **提供**: `questionWordVisibilityState` (グローバル変数)

#### `subslot_visibility_control.js`
- **役割**: サブスロット表示制御
- **機能**: 詳細レベルのサブスロット表示管理
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `subslot_toggle.js`
- **役割**: サブスロット切り替え機能
- **機能**: サブスロットの開閉、アニメーション制御
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `zoom_controller.js`
- **役割**: ズーム機能制御
- **機能**: 画面拡大縮小、モバイル対応ズーム
- **使用場所**: `training/index.html`
- **依存関係**: なし

### 🖼️ 画像・メディア系システム
#### `universal_image_system.js`
- **役割**: 汎用画像管理システム
- **機能**: 画像表示、遅延読み込み、エラーハンドリング
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `image_auto_hide.js`
- **役割**: 画像自動非表示機能
- **機能**: 不要画像の自動非表示、パフォーマンス最適化
- **使用場所**: `training/index.html`
- **依存関係**: `insert_test_data_clean.js`の処理完了を待機

### 🔊 音声システム
#### `voice_system.js`
- **役割**: 音声認識・再生システム
- **機能**: 音声入力、TTS、プラットフォーム別対応
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `voice_progress_tracker.js`
- **役割**: 音声進捗追跡
- **機能**: 学習進捗記録、音声データ管理
- **使用場所**: `training/index.html` (重複読み込みあり)
- **依存関係**: なし

#### `voice_progress_ui.js`
- **役割**: 音声進捗UI表示
- **機能**: 進捗バー、視覚的フィードバック
- **使用場所**: `training/index.html` (重複読み込みあり)
- **依存関係**: なし

### 📚 学習機能システム
#### `explanation_system.js`
- **役割**: 解説システム
- **機能**: 文法解説表示、ヘルプ機能
- **使用場所**: `training/index.html`
- **依存関係**: なし

#### `question_word_visibility.js`
- **役割**: 疑問詞表示制御
- **機能**: 疑問詞の表示/非表示、学習レベル調整
- **使用場所**: `training/index.html`
- **依存関係**: `questionWordVisibilityState` (visibility_control.js)

## 🔗 依存関係マップ

### ESModule Import Chain
```
training/index.html
├── security.js (最優先読み込み)
├── randomizer_all.js
└── structure_builder.js
```

### Script Tag Load Order & Dependencies
```
training/index.html
├── rate-limiter.js (window.rateLimiter)
├── error-handler.js (window.errorHandler)
├── auth.js → 依存: window.rateLimiter, window.errorHandler, window.securityUtils
├── subslot_toggle.js
├── randomizer_individual.js
├── control_panel_manager.js
├── visibility_control.js (questionWordVisibilityState 宣言)
├── subslot_visibility_control.js
├── image_auto_hide.js → 依存: insert_test_data_clean.js の実行完了
├── universal_image_system.js
├── question_word_visibility.js → 依存: questionWordVisibilityState (visibility_control.js)
├── voice_system.js
├── voice_progress_tracker.js (重複)
├── voice_progress_ui.js (重複)
├── explanation_system.js
├── zoom_controller.js
└── insert_test_data_clean.js (image_auto_hide.js から参照)
```

### Global Variables & Functions Dependencies
```
window.rateLimiter (rate-limiter.js)
├── → auth.js が参照

window.errorHandler (error-handler.js)  
├── → auth.js が参照

window.securityUtils (training/index.html内で定義)
├── → auth.js が参照

window.loadedJsonData (insert_test_data_clean.js)
├── → insert_test_data_clean.js が参照・監視

questionWordVisibilityState (visibility_control.js)
├── → question_word_visibility.js が参照

insert_test_data_clean.js の実行完了
├── → image_auto_hide.js が待機

MutationObserver監視 (insert_test_data_clean.js)
├── → dynamic-slot-area の変更を検出して同期処理を実行
```

## ⚠️ 注意事項

### 重複読み込み
- `voice_progress_tracker.js` と `voice_progress_ui.js` が複数箇所で読み込まれています
- パフォーマンスに影響する可能性があるため、要確認

### セキュリティ優先度
- `security.js` は最優先で読み込まれ、他のスクリプト実行前にセキュリティ初期化を実行
- すべてのファイルアップロード処理でセキュリティ検証が必要

### 読み込み順序の重要性
- **必須**: `rate-limiter.js` → `error-handler.js` → `auth.js` の順序
- **必須**: `visibility_control.js` → `question_word_visibility.js` の順序  
- **必須**: `insert_test_data_clean.js` → `image_auto_hide.js` の実行順序
- グローバル変数への依存により、読み込み順序の変更は危険

### モジュール設計
- ESModuleシステムと従来のスクリプトタグが混在
- グローバル変数を通じた密結合が存在
- 将来的にはESModuleへの統一を検討

## 🗃️ 保管済みファイル

以下のファイルは開発過程保管庫に移動済み：

### 未使用JavaScriptファイル (14件)
- `common.js`
- `image_handler.js`
- `main.js`
- `question_word_controller.js`
- `randomizer.js` (セキュリティ強化版・未使用)
- `randomizer_controller.js` (レンダリング統合版・未使用)
- `randomizer_slot.js`
- `renderer_core.js`
- `responsive_layout.js`
- `rotation-fix.js`
- `simple_recorder.js`
- `slot_data_loader.js`
- `subslot_renderer.js`
- `v_slot_image_system.js`

### 開発用フォルダ (3件)
- `old/` - 旧バージョンファイル
- `optimized/` - 最適化実験ファイル
- `バックアップ/` - バックアップファイル

## 📊 統計情報

- **本番環境ファイル数**: 20ファイル
- **保管庫移動ファイル数**: 14ファイル + 3フォルダ
- **ESModule採用率**: 15% (3/20)
- **セキュリティ関連ファイル**: 4ファイル
- **UI制御ファイル**: 5ファイル
- **音声システムファイル**: 3ファイル

## 🔄 更新履歴

- **2025-08-01**: 初版作成、未使用ファイル整理完了
- **対象バージョン**: Rephrase English Learning System v2025.07.27-1

---
**注意**: このドキュメントは本番環境の現在の状態を反映しています。ファイルの追加・削除・変更時は必ずこのドキュメントを更新してください。
