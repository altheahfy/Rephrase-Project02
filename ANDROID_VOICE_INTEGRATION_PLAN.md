# Android音声システム統合計画 - 詳細設計書
作成日: 2025年7月29日
目的: 現行システムを基盤とし、Android専用機能を段階的に追加

## 🎯 基本方針
- 現行システム（PC・スマホ対応）は100%保持
- Android検出時のみ、専用パネルに切り替え
- 既存機能の動作は一切変更しない
- コピー&ペーストベースで安全に実装

## 📋 実装手順

### ①Android専用パネル作成（コピー&ペースト方式）
**目標**: Android検出時に専用パネルを表示

**実装方法**:
1. 現行の`voice-control-panel`（line 802-）を完全コピー
2. 新ID `android-voice-control-panel` で作成
3. Android検出条件分岐を追加:
   ```javascript
   if (/Android/i.test(navigator.userAgent)) {
       // Android専用パネル表示
       document.getElementById('android-voice-control-panel').style.display = 'block';
   } else {
       // 現行パネル表示（PC・その他）
       document.getElementById('voice-control-panel').style.display = 'block';
   }
   ```

**利点**: 読み上げ機構（TTS）は現行のものをそのまま利用可能

### ②録音機構の分離（Android対応）
**問題**: 現行は録音+音声認識が同時処理
**解決**: Android専用パネルでは録音のみに変更

**移植元**: `backup/voice_system_backup_20250727/voice_system_original.js`
**対象機能**: 
- `androidRetryRecognition` (line 4145)
- Android専用録音メソッド

**実装箇所**: Android専用パネルの録音ボタン
```html
<button id="android-voice-record-btn" onclick="androidRecordOnly()">🎤 録音</button>
```

### ③再生機構の移植
**移植元**: 同上バックアップファイル
**対象**: Android対応の再生メソッド
**実装**: Android専用の再生ボタン機能

### ④分析ボタン追加
**新機能**: 音声分析テスト機構を移植
**移植元**: バックアップの音声分析機能
**統合**: 現行パネルの例文比較・採点機構と連携

## 🗂️ ファイル構成

### 現行ファイル（保持）
- `training/index.html` - メインHTML（現行パネル保持）
- `training/js/voice_system.js` - 現行音声システム（保持）

### バックアップファイル（移植元）
- `backup/voice_system_backup_20250727/voice_system_original.js`

### 新規作成予定
- Android専用パネルHTML（既存のコピー＋修正）
- Android専用メソッド（バックアップから移植）

## 🔧 技術的詳細

### Android検出コード
```javascript
const isAndroid = /Android/i.test(navigator.userAgent);
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
```

### パネル切り替えロジック
```javascript
function initializeVoicePanel() {
    if (isAndroid) {
        showAndroidPanel();
    } else {
        showStandardPanel();
    }
}
```

## 📊 現在の状況（2025年7月29日時点）

### 正常動作確認済み
- ✅ PC版音声パネル: `voice-control-panel`
- ✅ スマホ版音声パネル: `voice-debug-panel`  
- ✅ 録音ボタン: 緑色で正常動作
- ✅ Git管理: 正常同期

### 準備完了
- ✅ バックアップファイル特定済み
- ✅ 現行システム安定化済み
- ✅ 段階的実装計画策定済み

## ⚠️ 重要な注意事項

### 絶対に守るルール
1. **現行システムを一切変更しない**
2. **コピー&ペーストベースで実装**
3. **段階的テスト（一つずつ確認）**
4. **問題発生時は即座に復旧**

### 作業前の必須チェック
1. 現行パネルが正常動作することを確認
2. バックアップファイルの存在確認
3. Git状態の確認（clean working tree）

## 🚀 次回作業開始時の手順

1. **この設計書を熟読**
2. **現行システムの動作確認**
3. **①から順番に実装開始**
4. **各段階でコミット・テスト**

---
この設計書により、記憶リセット後も確実に継続可能
