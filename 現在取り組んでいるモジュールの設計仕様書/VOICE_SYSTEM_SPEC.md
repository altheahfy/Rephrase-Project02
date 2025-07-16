# Rephraseプロジェクト 音声機構システム 設計仕様書

## 🎯 概要

Rephraseプロジェクトにおける音声学習機能の統合設計仕様書です。学習者の発話練習、録音・再生、模範音声の提供、発音評価、進捗追跡機能を実現する包括的な音声システムを定義します。

## ✅ 実装完了ステータス（2025年7月）

**実装完了済み機能：**
- ✅ 発話練習モード（完全実装）
- ✅ 録音・再生機能（完全実装）
- ✅ 模範音声システム（完全実装）
- ✅ 発音評価機能（完全実装）
- ✅ 発話速度評価（完全実装）
- ✅ 学習進捗管理（完全実装）
- ✅ 進捗表示UI（完全実装）

**将来実装予定：**
- 🔄 全国比較機能（サーバーサイド実装待ち）

## 📋 実装完了機能詳細

### ✅ 発話練習モード
- **実装状況**: 完全実装済み
- **機能**: 例文全体の録音・再生による発話練習
- **対応レベル**: 4段階の習熟度レベル（初心者〜達人）
- **実装ファイル**: `voice_system.js`

### ✅ 録音・再生機能
- **実装状況**: 完全実装済み
- **機能**: MediaRecorder APIによる高品質録音、Audio APIによる再生
- **対応フォーマット**: WebM/MP3、ブラウザネイティブ
- **実装ファイル**: `voice_system.js`

### ✅ 模範音声システム
- **実装状況**: 完全実装済み
- **機能**: Web Speech API（TTS）による自動読み上げ
- **カスタマイズ**: 速度・声質・アクセント調整対応
- **実装ファイル**: `voice_system.js`

### ✅ 発音評価機能
- **実装状況**: 完全実装済み
- **機能**: Web Speech API（STT）による音声認識と内容マッチング
- **評価方式**: 4段階レベル判定（達人レベル、上級者レベル、中級者レベル、初心者レベル）
- **実装ファイル**: `voice_system.js`

### ✅ 発話速度評価
- **実装状況**: 完全実装済み
- **機能**: 録音時間と文字数による速度計測
- **基準**: レベル別目標速度設定済み
- **実装ファイル**: `voice_system.js`

### ✅ 学習進捗管理
- **実装状況**: 完全実装済み
- **機能**: IndexedDBによる学習データ永続化
- **データ**: 期間別統計、レベル別進捗、練習回数等
- **実装ファイル**: `voice_progress_tracker.js`

### ✅ 進捗表示UI
- **実装状況**: 完全実装済み
- **機能**: グラフィカルな進捗表示パネル
- **期間**: 1週間、1ヶ月、3ヶ月、1年単位
- **実装ファイル**: `voice_progress_ui.js`, `voice_progress.css`

### 🔄 全国比較機能（将来実装）
- **実装状況**: 設計完了、サーバーサイド実装待ち
- **機能**: ユーザーデータの匿名化集計と全国平均比較
- **必要技術**: サーバーサイドAPI、データベース

---

## 🔧 技術実現可能性分析

### ✅ 実現可能な技術

#### 1. Web Audio API + MediaRecorder API
```javascript
// 高品質録音の実現
const audioContext = new AudioContext();
const mediaRecorder = new MediaRecorder(stream, {
  mimeType: 'audio/webm;codecs=opus',
  audioBitsPerSecond: 128000
});
```

#### 2. Web Speech API (SpeechSynthesis)
```javascript
// 模範音声の自動生成
const utterance = new SpeechSynthesisUtterance(text);
utterance.rate = 0.8; // 速度調整
utterance.voice = voices.find(v => v.lang === 'en-US');
speechSynthesis.speak(utterance);
```

#### 3. 音響分析（Web Audio API）
```javascript
// 基本的な音響特徴抽出
const analyser = audioContext.createAnalyser();
const frequencyData = new Uint8Array(analyser.frequencyBinCount);
analyser.getByteFrequencyData(frequencyData);
```

#### 4. ローカルストレージ + IndexedDB
```javascript
// 進捗データの永続化
const voiceProgressDB = new Dexie('VoiceProgressDB');
voiceProgressDB.version(1).stores({
  sessions: '++id, timestamp, slotId, score, duration'
});
```

### ⚠️ 制限事項

#### 1. **精密な発音評価の限界**
- ブラウザネイティブでは音素レベルの詳細分析は困難
- **対策**: 基本的な指標（時間、音量、エネルギー）に焦点

#### 2. **音声認識の精度限界**
- Web Speech API（STT）は環境・アクセントに依存
- **対策**: 音声認識は補助機能として位置づけ

#### 3. **リアルタイム処理の負荷**
- 高度な音響分析はパフォーマンスに影響
- **対策**: 軽量なアルゴリズムと適切なサンプリング

---

## 🏗️ システム設計

### アーキテクチャ概要

```
┌─────────────────────────────────────────────────────┐
│                 音声UI制御層                          │
├─────────────────────────────────────────────────────┤
│           音声録音モジュール   │   模範音声モジュール    │
├─────────────────────────────────────────────────────┤
│     発音評価エンジン          │   発話速度計測エンジン   │
├─────────────────────────────────────────────────────┤
│               進捗データ管理層                         │
├─────────────────────────────────────────────────────┤
│    ローカルDB (IndexedDB)     │   サーバー同期API      │
└─────────────────────────────────────────────────────┘
```

### ファイル構成

```
voice_system/
├── js/
│   ├── voice_recorder.js           # 録音・再生制御
│   ├── voice_synthesis.js          # 模範音声生成
│   ├── voice_analysis.js           # 音響分析・評価
│   ├── voice_speed_analyzer.js     # 発話速度計測
│   ├── voice_progress_manager.js   # 進捗データ管理
│   ├── voice_ui_controller.js      # UI統合制御
│   └── voice_comparison_engine.js  # 全国比較機能
├── css/
│   └── voice_system.css            # 音声UI専用スタイル
├── audio/
│   ├── recorded/                   # 録音データ保存
│   └── reference/                  # 模範音声キャッシュ
└── data/
    └── voice_settings.json         # 音声設定データ
```

### データベース設計

#### VoiceSession テーブル
```javascript
{
  id: "自動採番",
  timestamp: "2025-07-12T14:30:00Z",
  userId: "学習者ID（匿名化）",
  slotId: "s", // 対象スロット
  exampleText: "She is a software engineer",
  exerciseType: "individual_slot", // "full_sentence"
  recordingData: {
    audioBlob: "音声データ（Base64）",
    duration: 2.3, // 秒
    averageVolume: 0.7,
    frequencyProfile: [...]
  },
  referenceData: {
    expectedDuration: 2.0,
    targetSpeed: "intermediate"
  },
  evaluation: {
    speedScore: 85, // 0-100
    pronunciationScore: 78,
    overallScore: 82
  },
  userLevel: "intermediate"
}
```

#### VoiceProgress テーブル
```javascript
{
  id: "自動採番",
  userId: "学習者ID",
  periodType: "weekly", // "daily", "monthly"
  startDate: "2025-07-05",
  endDate: "2025-07-12",
  metrics: {
    totalSessions: 15,
    averageScore: 78.5,
    improvementRate: 12.3, // %
    practiceTime: 45.2, // 分
    slotsCompleted: ["s", "v", "o1"]
  }
}
```

---

## 🎨 UI/UX設計

### スロット統合デザイン

#### 各スロットへの音声ボタン追加
```html
<div class="slot-container" id="slot-s">
  <label>S</label>
  <img class="slot-image" src="..." alt="...">
  <div class="slot-text">She</div>
  <div class="slot-phrase">software engineer</div>
  
  <!-- 🔊 音声機能ボタン群（新規追加） -->
  <div class="voice-control-panel">
    <button class="voice-btn record-btn" data-slot="s">🎙️</button>
    <button class="voice-btn play-btn" data-slot="s" disabled>▶️</button>
    <button class="voice-btn tts-btn" data-slot="s">🔊</button>
    <button class="voice-btn hide-text-btn" data-slot="s">👁️‍🗨️</button>
  </div>
  
  <!-- 音声評価結果表示 -->
  <div class="voice-evaluation" data-slot="s" style="display: none;">
    <div class="speed-score">速度: <span class="score">85</span>%</div>
    <div class="pronunciation-score">発音: <span class="score">78</span>%</div>
  </div>
</div>
```

#### グローバル音声制御パネル
```html
<div id="global-voice-panel" class="voice-panel">
  <div class="voice-level-selector">
    <label>学習レベル:</label>
    <select id="voice-learning-level">
      <option value="beginner">初心者 (1.0秒/語)</option>
      <option value="intermediate">中級者 (0.7秒/語)</option>
      <option value="advanced">上級者 (0.5秒/語)</option>
      <option value="expert">達人 (0.3秒/語)</option>
    </select>
  </div>
  
  <div class="voice-mode-selector">
    <label>練習モード:</label>
    <button class="mode-btn" data-mode="individual">個別スロット</button>
    <button class="mode-btn" data-mode="full-sentence">全文練習</button>
  </div>
  
  <div class="voice-progress-summary">
    <div class="today-stats">今日: 5回練習、平均82点</div>
    <div class="weekly-stats">今週: 23回練習、12%向上</div>
  </div>
</div>
```

### 音声評価フィードバックUI

#### リアルタイム録音インジケーター
```html
<div class="recording-indicator" style="display: none;">
  <div class="recording-wave">🎤</div>
  <div class="recording-timer">00:03</div>
  <div class="recording-level">
    <div class="level-bar" style="width: 70%"></div>
  </div>
</div>
```

#### 評価結果モーダル
```html
<div id="voice-evaluation-modal" class="modal">
  <div class="modal-content">
    <h3>🎯 発話評価結果</h3>
    <div class="score-display">
      <div class="score-item">
        <label>発話速度</label>
        <div class="score-bar">
          <div class="score-fill" style="width: 85%"></div>
        </div>
        <span class="score-text">85% (目標: 2.0秒、実際: 2.3秒)</span>
      </div>
      <div class="score-item">
        <label>音量レベル</label>
        <div class="score-bar">
          <div class="score-fill" style="width: 92%"></div>
        </div>
        <span class="score-text">92% (適切な音量)</span>
      </div>
    </div>
    <div class="playback-controls">
      <button class="play-recording">録音再生</button>
      <button class="play-reference">模範音声</button>
    </div>
  </div>
</div>
```

---

## 🔄 処理フロー設計

### 1. 音声録音フロー

```javascript
// voice_recorder.js
class VoiceRecorder {
  async startRecording(slotId) {
    // 1. マイクアクセス許可取得
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 44100
      }
    });
    
    // 2. MediaRecorder初期化
    this.mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm;codecs=opus'
    });
    
    // 3. 録音開始 + UI更新
    this.startTime = performance.now();
    this.mediaRecorder.start();
    this.updateRecordingUI(true);
    
    // 4. 音量レベルモニタリング
    this.setupVolumeMonitoring(stream);
  }
  
  stopRecording() {
    this.endTime = performance.now();
    this.mediaRecorder.stop();
    this.updateRecordingUI(false);
    
    return {
      audioBlob: this.recordedBlob,
      duration: (this.endTime - this.startTime) / 1000
    };
  }
}
```

### 2. 音声評価フロー

```javascript
// voice_analysis.js
class VoiceAnalyzer {
  async analyzeRecording(audioBlob, referenceText, targetLevel) {
    // 1. 音声データをAudioContextに変換
    const audioBuffer = await this.blobToAudioBuffer(audioBlob);
    
    // 2. 基本的な音響特徴抽出
    const features = this.extractAcousticFeatures(audioBuffer);
    
    // 3. 発話速度計算
    const wordCount = referenceText.split(' ').length;
    const wordsPerSecond = wordCount / features.duration;
    const speedScore = this.calculateSpeedScore(wordsPerSecond, targetLevel);
    
    // 4. 音量・品質評価
    const qualityScore = this.calculateQualityScore(features);
    
    // 5. 総合評価
    const overallScore = (speedScore + qualityScore) / 2;
    
    return {
      speedScore,
      qualityScore,
      overallScore,
      duration: features.duration,
      recommendedImprovements: this.generateRecommendations(speedScore, qualityScore)
    };
  }
}
```

### 3. 模範音声生成フロー

```javascript
// voice_synthesis.js
class VoiceSynthesis {
  generateReferenceAudio(text, level = 'intermediate') {
    const utterance = new SpeechSynthesisUtterance(text);
    
    // レベル別パラメータ設定
    const levelSettings = {
      beginner: { rate: 0.6, pitch: 1.0 },
      intermediate: { rate: 0.8, pitch: 1.0 },
      advanced: { rate: 1.0, pitch: 1.0 },
      expert: { rate: 1.2, pitch: 1.0 }
    };
    
    Object.assign(utterance, levelSettings[level]);
    
    // 高品質な英語音声選択
    const voices = speechSynthesis.getVoices();
    utterance.voice = voices.find(v => 
      v.lang.startsWith('en-') && v.name.includes('Google')
    ) || voices.find(v => v.lang.startsWith('en-'));
    
    return new Promise((resolve) => {
      utterance.onend = () => resolve();
      speechSynthesis.speak(utterance);
    });
  }
}
```

---

## 📊 学習進捗追跡システム

### データ蓄積戦略

#### 1. ローカルファースト + クラウド同期
```javascript
// voice_progress_manager.js
class VoiceProgressManager {
  async saveSession(sessionData) {
    // 1. ローカルDB保存（即座）
    await this.localDB.sessions.add(sessionData);
    
    // 2. クラウド同期（バックグラウンド）
    this.queueForCloudSync(sessionData);
  }
  
  async getWeeklyProgress(userId) {
    const sessions = await this.localDB.sessions
      .where('timestamp')
      .between(startOfWeek, endOfWeek)
      .toArray();
      
    return this.calculateWeeklyMetrics(sessions);
  }
}
```

#### 2. 匿名化データ収集
```javascript
class AnonymizedDataCollector {
  anonymizeSession(session) {
    return {
      id: generateAnonymousId(session.userId),
      level: session.userLevel,
      score: session.evaluation.overallScore,
      practiceTime: session.recordingData.duration,
      timestamp: session.timestamp,
      // 個人識別情報は除外
    };
  }
}
```

### 進捗可視化

#### 1. 個人ダッシュボード
```html
<div class="voice-progress-dashboard">
  <div class="progress-chart">
    <canvas id="weekly-progress-chart"></canvas>
  </div>
  <div class="achievement-badges">
    <div class="badge earned">🎯 1週間連続練習</div>
    <div class="badge earned">⚡ 発話速度向上</div>
    <div class="badge pending">🏆 全国上位20%</div>
  </div>
</div>
```

#### 2. 全国比較レポート
```html
<div class="national-comparison">
  <h4>🇯🇵 全国比較 (あなたの位置)</h4>
  <div class="percentile-display">
    <div class="percentile-bar">
      <div class="your-position" style="left: 65%">あなた</div>
    </div>
    <div class="percentile-labels">
      <span>下位</span>
      <span>上位</span>
    </div>
  </div>
  <div class="comparison-stats">
    <div>平均練習時間: 週32分 (全国平均: 28分)</div>
    <div>平均達成スコア: 78点 (全国平均: 72点)</div>
  </div>
</div>
```
## 5. リアルタイム例文発話品質判定システム

### 5.1 システム概要
学習者の発話をリアルタイムで分析し、内容の正確性・発話速度・音質を総合的に評価して、4段階のレベル判定を行うシステム。

### 5.2 判定フロー
```
音声録音 → 音質チェック → 音声認識 → 内容評価 → 速度評価 → レベル判定
```

### 5.3 技術仕様

#### 5.3.1 音質品質チェック
- **最低録音時間**: 0.3秒以上
- **最低音量レベル**: 0.1以上
- **最低振幅**: 0.001以上
- **品質スコア計算**: 音量(50%) + 録音時間(30%) + 動的範囲(20%)

#### 5.3.2 音声認識
- **技術**: Web Speech API (SpeechRecognition)
- **言語設定**: 英語 (en-US)
- **リアルタイム処理**: 継続的認識モード
- **結果処理**: 最終認識結果を使用

#### 5.3.3 内容正確性評価
複数指標による類似度計算:

1. **Jaccard係数** (重み: 30%)
   ```javascript
   jaccardSimilarity = intersection.size / union.size
   ```

2. **最長共通部分列 (LCS)** (重み: 25%)
   ```javascript
   lcsSimilarity = lcsLength / Math.max(expected.length, actual.length)
   ```

3. **編集距離類似度** (重み: 25%)
   ```javascript
   editSimilarity = 1 - (editDistance / maxLength)
   ```

4. **部分文字列一致** (重み: 20%)
   ```javascript
   substringScore = matchedSubstrings / totalSubstrings
   ```

#### 5.3.4 発話速度計算
- **基準単位**: 語数/分 (WPM: Words Per Minute)
- **計算方式**: `(実際の語数 / 録音時間) × 60`
- **語数カウント**: 空白区切りによる単語数

#### 5.3.5 レベル判定基準

| 内容正確性 | 発話速度 (WPM) | 判定レベル |
|-----------|---------------|-----------|
| < 0.3 | - | ❌ 内容不一致 |
| 0.3-0.6 | - | ⚠️ 内容要改善 |
| ≥ 0.6 | < 80 | 🐌 初心者レベル |
| ≥ 0.6 | 80-130 | 📈 中級者レベル |
| ≥ 0.6 | 130-150 | 🚀 上級者レベル |
| ≥ 0.6 | > 150 | ⚡ 達人レベル |

### 5.4 出力データ構造
```javascript
{
    level: "📈 中級者レベル",
    contentAccuracy: 0.85,
    wordsPerMinute: 120,
    duration: 2.5,
    qualityScore: 0.9,
    expectedSentence: "原文テキスト",
    recognizedText: "認識されたテキスト",
    timestamp: "2025-07-13T10:30:00Z"
}
```

## 6. 学習進捗計測システム

### 6.1 システム概要
学習者の発話品質判定結果を時系列で保存・集計し、期間別の上達度を可視化するシステム。

### 6.2 データ保存仕様

#### 6.2.1 データベース設計
- **技術**: IndexedDB
- **データベース名**: VoiceProgressDB
- **バージョン**: 1
- **オブジェクトストア**: voiceProgress

#### 6.2.2 データ構造
```javascript
{
    id: "auto-generated-key",
    timestamp: "2025-07-13T10:30:00Z",
    level: "📈 中級者レベル",
    levelScore: 2,                    // 数値化: 0-4
    contentAccuracy: 0.85,
    wordsPerMinute: 120,
    duration: 2.5,
    qualityScore: 0.9,
    expectedSentence: "原文テキスト",
    recognizedText: "認識されたテキスト",
    sessionId: "uuid-v4",
    slotId: "slot-1"
}
```

#### 6.2.3 レベル数値化マッピング
```javascript
{
    '達人レベル': 4,
    '上級者レベル': 3,
    '中級者レベル': 2,
    '初心者レベル': 1,
    '内容要改善': 0.5,
    '内容不一致': 0,
    '音質不良': 0,
    '音声未検出': 0
}
```

### 6.3 進捗集計システム

#### 6.3.1 集計期間
- **1週間**: 過去7日間
- **1ヶ月**: 過去30日間
- **3ヶ月**: 過去90日間
- **1年**: 過去365日間

#### 6.3.2 集計指標
```javascript
{
    period: "1週間",
    sessionCount: 15,              // セッション数
    averageLevel: 2.3,             // 平均レベル
    maxWordsPerMinute: 145,        // 最高速度
    averageAccuracy: 0.82,         // 平均正確性
    improvementRate: 0.15,         // 改善度
    levelDistribution: {           // レベル分布
        '達人レベル': 2,
        '上級者レベル': 5,
        '中級者レベル': 6,
        '初心者レベル': 2
    }
}
```

### 6.4 可視化仕様

#### 6.4.1 UI コンポーネント
- **進捗パネル**: モーダル形式で表示
- **期間タブ**: 1週間・1ヶ月・3ヶ月・1年の切り替え
- **グラフ表示**: Canvas APIによる描画

#### 6.4.2 グラフ種類
1. **レベル分布グラフ**: 棒グラフ形式
2. **進捗推移チャート**: 折れ線グラフ形式
3. **統計サマリー**: 数値表示

#### 6.4.3 色分け設定
```javascript
{
    '達人レベル': '#FF6B6B',      // 赤
    '上級者レベル': '#4ECDC4',    // 青緑
    '中級者レベル': '#45B7D1',    // 青
    '初心者レベル': '#96CEB4',    // 緑
    'その他': '#FFEAA7'           // 黄
}
```

### 6.5 データ連携仕様

#### 6.5.1 自動保存
- **トリガー**: 音声分析完了時
- **保存タイミング**: 分析結果表示と同時
- **エラーハンドリング**: 保存失敗時の再試行機能

#### 6.5.2 データ取得
- **非同期処理**: Promise/async-await
- **フィルタリング**: 期間指定による絞り込み
- **ソート**: タイムスタンプ昇順

### 6.6 パフォーマンス仕様
- **データ保存**: 100ms以内
- **進捗表示**: 500ms以内
- **グラフ描画**: 200ms以内
- **メモリ使用量**: 最大10MB

### 6.7 セキュリティ仕様
- **データ保存**: ブラウザローカルのみ
- **個人情報**: 音声データは保存しない
- **匿名化**: 将来的な統計利用時は完全匿名化

## 7. 商用展開時の拡張仕様：ユーザー平均比較システム

### 7.1 システム概要
現在の個人進捗追跡システムを拡張し、匿名化された全ユーザーデータとの比較機能を提供するシステム。個人の学習進捗を全国平均・同世代平均・地域平均と比較し、客観的な学習位置を把握できる。

### 7.2 現在の設計の拡張対応状況

#### 7.2.1 拡張準備完了項目
- ✅ **データ構造の標準化**: levelScore（0-4）、WPM、contentAccuracy等の定量化済み
- ✅ **時系列データ蓄積**: タイムスタンプ付きセッションデータの保存
- ✅ **期間別集計機能**: 1週間・1ヶ月・3ヶ月・1年の進捗分析
- ✅ **モジュラー設計**: 新機能を独立クラスとして追加可能
- ✅ **プライバシー配慮**: ローカルファースト設計

#### 7.2.2 拡張時追加項目
- 🔄 **クラウドデータベース連携**: 匿名化データの収集・配信
- 🔄 **比較UI コンポーネント**: 全国平均との比較表示
- 🔄 **ユーザー同意管理**: データ利用に関する同意システム
- 🔄 **統計処理エンジン**: リアルタイム統計分析

### 7.3 技術アーキテクチャ拡張

#### 7.3.1 データ収集・匿名化レイヤー
```javascript
class AnonymousDataCollector {
    constructor(localTracker) {
        this.localTracker = localTracker;
        this.userConsent = false;
        this.anonymizationEngine = new DataAnonymizer();
    }
    
    async submitAnonymousData(sessionData) {
        if (!this.userConsent) return;
        
        const anonymizedData = this.anonymizationEngine.anonymize(sessionData);
        return await this.sendToCloud(anonymizedData);
    }
    
    anonymize(sessionData) {
        return {
            levelScore: sessionData.levelScore,
            contentAccuracy: Math.round(sessionData.contentAccuracy * 100) / 100,
            wordsPerMinute: Math.round(sessionData.wordsPerMinute),
            duration: Math.round(sessionData.duration * 10) / 10,
            timestamp: this.roundToHour(sessionData.timestamp),
            region: this.getRegionCode(), // 都道府県レベル
            userSegment: this.calculateUserSegment(sessionData),
            sessionCount: await this.getAnonymizedSessionCount()
        };
    }
}
```

#### 7.3.2 比較システム統合
```javascript
class VoiceProgressComparison extends VoiceProgressTracker {
    constructor() {
        super();
        this.dataCollector = new AnonymousDataCollector(this);
        this.benchmarkEngine = new BenchmarkEngine();
        this.comparisonUI = new ComparisonUI();
    }
    
    async getComparisonData(period) {
        const personalData = await this.getProgressData(period);
        const benchmarkData = await this.benchmarkEngine.getBenchmarkData(period);
        
        return {
            personal: personalData,
            benchmark: benchmarkData,
            comparison: this.calculateComparison(personalData, benchmarkData)
        };
    }
    
    calculateComparison(personal, benchmark) {
        return {
            levelPercentile: this.calculatePercentile(personal.averageLevel, benchmark.levelDistribution),
            speedPercentile: this.calculatePercentile(personal.averageSpeed, benchmark.speedDistribution),
            accuracyPercentile: this.calculatePercentile(personal.averageAccuracy, benchmark.accuracyDistribution),
            improvementRate: this.calculateImprovementComparison(personal, benchmark),
            ranking: this.calculateRanking(personal, benchmark)
        };
    }
}
```

### 7.4 データ構造拡張

#### 7.4.1 匿名化データ構造
```javascript
// 商用サーバーに送信される匿名化データ
{
    sessionId: "anonymous-uuid",
    timestamp: "2025-07-13T10:00:00Z", // 時間を時間単位に丸める
    levelScore: 2,                      // 0-4の評価レベル
    contentAccuracy: 0.85,              // 内容正確性
    wordsPerMinute: 120,                // 発話速度
    duration: 2.5,                      // 録音時間
    region: "JP-13",                    // 都道府県コード（任意）
    userSegment: "intermediate",         // 学習者レベル分類
    sessionCount: 15,                   // 学習回数（匿名化）
    deviceType: "desktop",              // 端末種別
    timestamp_created: "2025-07-13T10:30:00Z"
}
```

#### 7.4.2 比較結果データ構造
```javascript
{
    period: "1ヶ月",
    personal: {
        sessionCount: 25,
        averageLevel: 2.3,
        averageSpeed: 115,
        averageAccuracy: 0.78,
        improvementRate: 0.15
    },
    benchmark: {
        totalUsers: 12500,
        averageLevel: 2.1,
        averageSpeed: 95,
        averageAccuracy: 0.72,
        levelDistribution: {
            "達人レベル": 0.05,
            "上級者レベル": 0.20,
            "中級者レベル": 0.45,
            "初心者レベル": 0.30
        }
    },
    comparison: {
        levelPercentile: 68,        // 上位32%
        speedPercentile: 75,        // 上位25%
        accuracyPercentile: 62,     // 上位38%
        overallRanking: 70,         // 総合順位パーセンタイル
        improvementRanking: 45      // 改善度ランキング
    }
}
```

### 7.5 UI拡張設計

#### 7.5.1 比較ダッシュボード
```html
<!-- 拡張後の進捗表示UI -->
<div class="voice-progress-panel-extended">
    <div class="progress-tabs">
        <button class="tab active" data-tab="personal">個人進捗</button>
        <button class="tab" data-tab="comparison">全国比較</button>
        <button class="tab" data-tab="ranking">ランキング</button>
        <button class="tab" data-tab="insights">学習インサイト</button>
    </div>
    
    <div class="comparison-dashboard">
        <!-- 個人 vs 全国平均比較 -->
        <div class="comparison-metrics">
            <div class="metric-card">
                <h5>発話速度</h5>
                <div class="metric-comparison">
                    <div class="personal-metric">あなた: 120 WPM</div>
                    <div class="benchmark-metric">全国平均: 95 WPM</div>
                    <div class="percentile-badge">上位25%</div>
                </div>
            </div>
            
            <div class="metric-card">
                <h5>内容正確性</h5>
                <div class="metric-comparison">
                    <div class="personal-metric">あなた: 78%</div>
                    <div class="benchmark-metric">全国平均: 72%</div>
                    <div class="percentile-badge">上位38%</div>
                </div>
            </div>
        </div>
        
        <!-- 視覚的比較チャート -->
        <div class="comparison-charts">
            <canvas id="comparison-radar-chart"></canvas>
            <canvas id="percentile-distribution-chart"></canvas>
        </div>
    </div>
</div>
```

#### 7.5.2 ランキング表示
```javascript
class RankingDisplay {
    displayRanking(comparisonData) {
        return `
            <div class="ranking-display">
                <h4>🏆 あなたの順位</h4>
                <div class="ranking-cards">
                    <div class="ranking-card">
                        <div class="rank-number">${comparisonData.comparison.overallRanking}</div>
                        <div class="rank-label">総合順位</div>
                        <div class="rank-description">上位${100 - comparisonData.comparison.overallRanking}%</div>
                    </div>
                    
                    <div class="ranking-card">
                        <div class="rank-number">${comparisonData.comparison.speedPercentile}</div>
                        <div class="rank-label">発話速度</div>
                        <div class="rank-description">上位${100 - comparisonData.comparison.speedPercentile}%</div>
                    </div>
                    
                    <div class="ranking-card">
                        <div class="rank-number">${comparisonData.comparison.accuracyPercentile}</div>
                        <div class="rank-label">正確性</div>
                        <div class="rank-description">上位${100 - comparisonData.comparison.accuracyPercentile}%</div>
                    </div>
                </div>
            </div>
        `;
    }
}
```

### 7.6 段階的実装計画

#### Phase 1: データ収集基盤（商用ローンチ時）
- **期間**: 2-3週間
- **実装内容**:
  - 匿名化データ収集システム
  - ユーザー同意管理
  - 基本統計処理
  - クラウドストレージ連携

#### Phase 2: 比較機能（ローンチ後1-2ヶ月）
- **期間**: 3-4週間
- **実装内容**:
  - 全国平均比較機能
  - 比較UI コンポーネント
  - パーセンタイル計算
  - 基本ランキング表示

#### Phase 3: 高度な分析（ローンチ後3-6ヶ月）
- **期間**: 4-6週間
- **実装内容**:
  - 同世代・地域別比較
  - 学習推奨システム
  - 詳細インサイト機能
  - 予測分析

### 7.7 プライバシー・セキュリティ仕様

#### 7.7.1 データ匿名化プロセス
```javascript
class DataAnonymizer {
    anonymize(sessionData) {
        // 1. 個人特定情報の完全除去
        const anonymized = {
            levelScore: sessionData.levelScore,
            accuracy: this.roundToDecimal(sessionData.contentAccuracy, 2),
            wpm: this.roundToInteger(sessionData.wordsPerMinute),
            duration: this.roundToDecimal(sessionData.duration, 1)
        };
        
        // 2. 時間情報の粗化
        anonymized.timestamp = this.roundToHour(sessionData.timestamp);
        
        // 3. 地域情報の一般化（都道府県レベル）
        anonymized.region = this.getRegionCode(); // 任意設定
        
        // 4. セッション数の範囲化
        anonymized.sessionRange = this.getSessionRange(sessionData.sessionCount);
        
        // 5. 一意識別子の生成（セッション単位）
        anonymized.sessionId = this.generateAnonymousId();
        
        return anonymized;
    }
    
    getSessionRange(count) {
        if (count < 10) return "beginner";
        if (count < 50) return "intermediate";
        if (count < 100) return "advanced";
        return "expert";
    }
}
```

#### 7.7.2 同意管理システム
```javascript
class ConsentManager {
    async requestDataSharingConsent() {
        const consent = await this.showConsentDialog({
            title: "学習データの統計利用について",
            description: `
                あなたの学習データを以下の目的で利用させていただきます：
                • 全国平均との比較機能の提供
                • 学習効果の統計分析
                • サービス改善のための研究
                
                個人を特定できる情報は一切収集・保存されません。
                いつでも同意を取り消すことができます。
            `,
            benefits: [
                "📊 全国平均との詳細比較",
                "🏆 ランキング機能の利用",
                "📈 学習効果の客観的評価",
                "🎯 個別学習推奨の提供"
            ],
            options: ["同意する", "同意しない", "詳細を見る"]
        });
        
        if (consent === "同意する") {
            this.saveConsent(true);
            return true;
        }
        
        return false;
    }
    
    saveConsent(consent) {
        localStorage.setItem('voiceDataSharingConsent', JSON.stringify({
            consent: consent,
            timestamp: new Date().toISOString(),
            version: "1.0"
        }));
    }
}
```

### 7.8 統計処理エンジン

#### 7.8.1 パーセンタイル計算
```javascript
class BenchmarkEngine {
    calculatePercentile(personalValue, distributionData) {
        // 累積分布関数を使用してパーセンタイルを計算
        const sortedValues = distributionData.sort((a, b) => a - b);
        const position = sortedValues.findIndex(value => value >= personalValue);
        
        if (position === -1) return 100; // 最高値
        
        const percentile = (position / sortedValues.length) * 100;
        return Math.round(percentile);
    }
    
    async getBenchmarkData(period) {
        // 商用サーバーから統計データを取得
        const response = await fetch(`/api/benchmark/${period}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return await response.json();
    }
    
    calculateTrends(historicalData) {
        // 時系列データから傾向を分析
        const trends = {
            levelTrend: this.calculateLinearTrend(historicalData.levels),
            speedTrend: this.calculateLinearTrend(historicalData.speeds),
            accuracyTrend: this.calculateLinearTrend(historicalData.accuracies)
        };
        
        return trends;
    }
}
```

### 7.9 モチベーション機能

#### 7.9.1 バッジシステム
```javascript
class BadgeSystem {
    checkBadgeEligibility(comparisonData) {
        const badges = [];
        
        // 速度バッジ
        if (comparisonData.comparison.speedPercentile >= 90) {
            badges.push({
                id: 'speed_master',
                name: '⚡ スピードマスター',
                description: '発話速度が全国上位10%に到達'
            });
        }
        
        // 正確性バッジ
        if (comparisonData.comparison.accuracyPercentile >= 85) {
            badges.push({
                id: 'accuracy_expert',
                name: '🎯 正確性エキスパート',
                description: '内容正確性が全国上位15%に到達'
            });
        }
        
        // 継続学習バッジ
        if (comparisonData.personal.sessionCount >= 100) {
            badges.push({
                id: 'consistency_champion',
                name: '🏆 継続学習チャンピオン',
                description: '100セッション以上の継続学習を達成'
            });
        }
        
        return badges;
    }
}
```

#### 7.10 学習推奨システム

##### 7.10.1 AIによる個別推奨
```javascript
class LearningRecommendationEngine {
    generateRecommendations(comparisonData) {
        const recommendations = [];
        
        // 弱点分析に基づく推奨
        if (comparisonData.comparison.speedPercentile < 50) {
            recommendations.push({
                type: 'speed_improvement',
                title: '発話速度の向上',
                description: '毎日10分の発話練習で速度を向上させましょう',
                target: '1ヶ月で20WPM向上',
                methods: ['短文の反復練習', '音読練習', '発話速度意識トレーニング']
            });
        }
        
        if (comparisonData.comparison.accuracyPercentile < 50) {
            recommendations.push({
                type: 'accuracy_improvement',
                title: '内容正確性の向上',
                description: '発音とイントネーションを重点的に練習しましょう',
                target: '1ヶ月で正確性10%向上',
                methods: ['音声認識練習', '発音矯正', 'シャドーイング']
            });
        }
        
        return recommendations;
    }
}
```

### 7.11 API設計

#### 7.11.1 データ収集API
```javascript
// POST /api/voice-sessions
{
    "sessions": [
        {
            "sessionId": "anonymous-uuid",
            "timestamp": "2025-07-13T10:00:00Z",
            "levelScore": 2,
            "contentAccuracy": 0.85,
            "wordsPerMinute": 120,
            "duration": 2.5,
            "region": "JP-13",
            "userSegment": "intermediate"
        }
    ]
}
```

#### 7.11.2 比較データAPI
```javascript
// GET /api/benchmark/1month
{
    "period": "1month",
    "totalUsers": 12500,
    "averageLevel": 2.1,
    "averageSpeed": 95,
    "averageAccuracy": 0.72,
    "levelDistribution": {
        "4": 0.05,
        "3": 0.20,
        "2": 0.45,
        "1": 0.30
    },
    "speedDistribution": [65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150],
    "accuracyDistribution": [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95],
    "timestamp": "2025-07-13T10:00:00Z"
}
```

### 7.12 成功指標（KPI）

#### 7.12.1 機能利用率
- **比較機能利用率**: 月間アクティブユーザーの60%以上
- **データ共有同意率**: 新規ユーザーの70%以上
- **継続利用率**: 比較機能利用者の月間リテンション80%以上

#### 7.12.2 学習効果
- **学習モチベーション**: 比較機能利用者の学習継続率20%向上
- **学習成果**: 全国平均との比較による学習効果10%向上
- **ユーザーエンゲージメント**: セッション数15%増加

### 7.13 今後の発展可能性
#### 7.13.1 グローバル展開
- 多言語対応（中国語、韓国語、フランス語等）
- 国際比較機能
- 文化的差異を考慮した評価基準

#### 7.13.2 AI高度化
- 個人学習パターンの深度分析
- 最適学習経路の自動生成
- 音声認識精度のパーソナライズ化

#### 7.13.3 コミュニティ機能
- 学習グループの形成
- 地域別学習コミュニティ
- 学習成果の共有プラットフォーム

---

**更新日**: 2025年7月13日  
**バージョン**: 2.1  
**実装状況**: 拡張仕様設計完了  
**商用展開対応**: 完全準備完了
---

## 🚀 実装フェーズ計画

### Phase 1: 基本音声機能 (2週間)
- [x] 要件分析・設計完了
- [ ] 音声録音・再生機能
- [ ] 基本的なUI統合
- [ ] ローカルデータ保存

### Phase 2: 評価・分析機能 (2週間)
- [ ] 発話速度計測
- [ ] 基本音響分析
- [ ] 評価アルゴリズム実装
- [ ] フィードバックUI完成

### Phase 3: 進捗管理機能 (1週間)
- [ ] 進捗データベース設計
- [ ] 統計・可視化機能
- [ ] 達成度システム

### Phase 4: 高度機能 (2週間)
- [ ] 模範音声自動生成
- [ ] レベル別適応機能
- [ ] 音声品質最適化

### Phase 5: サーバー連携 (将来)
- [ ] クラウド同期API
- [ ] 全国比較機能
- [ ] 匿名化データ収集

---

## ⚡ パフォーマンス考慮事項

### 1. 音声データ最適化
- **圧縮**: WebM Opus codec使用（高圧縮率）
- **サンプリング**: 16kHz以下で十分（音声認識用途）
- **分割保存**: 長時間録音時の分割処理

### 2. リアルタイム処理
- **Web Workers**: 音響分析をメインスレッドから分離
- **RequestAnimationFrame**: UI更新の最適化
- **デバウンス**: 連続操作時の処理制限

### 3. メモリ管理
- **AudioBuffer解放**: 分析完了後の即座なクリーンアップ
- **Blob URL管理**: 一時URLの適切な解放
- **キャッシュ戦略**: 模範音声の効率的なキャッシュ

---

## 🔒 セキュリティ・プライバシー

### 1. 音声データ保護
- **ローカル優先**: 音声データの外部送信最小化
- **暗号化**: 保存時の音声データ暗号化
- **自動削除**: 古い練習データの定期削除

### 2. 匿名化
- **ID生成**: 復元不可能な匿名IDシステム
- **データ最小化**: 統計に必要な最小限のデータのみ収集
- **オプトアウト**: ユーザーによるデータ共有拒否オプション

---

## 📋 今後の拡張可能性

### 1. AI音声認識統合
- **OpenAI Whisper API**: より精密な音声認識
- **音素レベル分析**: 詳細な発音矯正指導
- **リアルタイムフィードバック**: 発話中のリアルタイム評価

### 2. ソーシャル機能
- **学習グループ**: 友達との進捗共有
- **チャレンジ**: 月間チャレンジイベント
- **ランキング**: 匿名化された実力ランキング

### 3. 適応学習
- **弱点分析**: 個人の苦手パターン特定
- **カスタムプラン**: AI生成の個別学習計画
- **予測モデル**: 上達予測とモチベーション維持

---

## 📝 まとめ

この音声機構システムは、現在のRephraseプロジェクトのスロットベース学習UIと完全に統合し、段階的な実装により確実に機能を追加していく設計となっています。

**重要なポイント:**
1. **ブラウザネイティブ技術**を活用した実装可能性100%
2. **既存UI への最小限の影響**での統合
3. **段階的実装**による安全な機能追加
4. **将来拡張性**を考慮した柔軟な設計

この仕様書に基づいて、Phase 1から順次実装を開始できます。

---

## 🎯 2025年7月 実装完了機能

### ✅ 高度な例文読み上げシステム（完全実装済み）

#### 1. 複合データソース対応読み上げ機能
```javascript
buildSentenceFromOrderedData() {
    // 🎯 混合アプローチ：各スロットの表示順序ごとに処理
    const slotOrderGroups = {};
    
    // 上位スロットをグループ化（window.loadedJsonDataから）
    upperSlotData.forEach(item => {
        const order = item.Slot_display_order;
        if (!slotOrderGroups[order]) {
            slotOrderGroups[order] = { upperSlot: null, subSlots: [] };
        }
        
        if (!item.SubslotID) {
            slotOrderGroups[order].upperSlot = item;
        }
    });
    
    // サブスロットをグループ化（window.lastSelectedSlotsから）
    subSlotData.forEach(item => {
        const order = item.Slot_display_order;
        if (!slotOrderGroups[order]) {
            slotOrderGroups[order] = { upperSlot: null, subSlots: [] };
        }
        
        if (item.SubslotID) {
            slotOrderGroups[order].subSlots.push(item);
        }
    });
}
```

**実現された機能:**
- 上位スロット（window.loadedJsonData）とサブスロット（window.lastSelectedSlots）の混合データソース対応
- Slot_display_order（上位スロット）とdisplay_order（サブスロット内順序）による正確な順序制御
- 上位スロットとサブスロットの重複回避ロジック（either/or選択）

#### 2. スロット選択優先度システム
```javascript
// 🎯 判定：上位スロットにテキストがあるかどうか
if (upperSlot && upperSlot.SlotPhrase && upperSlot.SlotPhrase.trim()) {
    // 上位スロットにテキストがある場合：上位スロットを使用
    console.log(`✅ 上位スロット使用 ${upperSlot.Slot}(order:${order}): "${upperSlot.SlotPhrase}"`);
    sentenceParts.push({
        order: parseInt(order),
        text: upperSlot.SlotPhrase,
        slot: upperSlot.Slot,
        type: 'upper'
    });
} else if (subSlots.length > 0) {
    // 上位スロットが空でサブスロットがある場合：サブスロットを使用
    console.log(`✅ サブスロット使用 (order:${order})`);
    subSlots
        .filter(sub => sub.SubslotElement && sub.SubslotElement.trim())
        .sort((a, b) => (a.display_order || 0) - (b.display_order || 0))
        .forEach(subSlot => {
            const totalOrder = parseInt(order) * 1000 + (subSlot.display_order || 0);
            sentenceParts.push({
                order: totalOrder,
                text: subSlot.SubslotElement,
                slot: subSlot.SubslotID,
                type: 'sub',
                parent: subSlot.Slot
            });
        });
}
```

**実現された機能:**
- 上位スロットに内容がある場合は上位スロットを優先
- 上位スロットが空の場合のみサブスロットを使用
- サブスロット重複読み上げの完全回避
- サブスロット内での正確な順序制御（display_order準拠）

#### 3. ランダマイズ結果対応読み上げ
**全体ランダマイズ対応:**
- `randomizer.js`による全スロット一括ランダマイズ後も正確な読み上げ
- 新しく選択されたスロット内容を即座に反映
- window.loadedJsonDataの更新を自動検知

**個別ランダマイズ対応:**
- `randomizer_individual.js`による個別スロットランダマイズ対応
- `randomizer_slot.js`による単一スロットランダマイズ対応
- ランダマイズ後のwindow.lastSelectedSlots更新を即座に反映

#### 4. 疑問詞特別処理システム
```javascript
// 疑問詞をチェック（上位スロットデータから）
const questionWordData = upperSlotData.find(item => 
    item.DisplayAtTop === true && item.DisplayText
);
if (questionWordData) {
    console.log('✅ 疑問詞:', questionWordData.DisplayText);
    sentenceParts.push({
        order: -1,
        text: questionWordData.DisplayText,
        slot: 'question-word'
    });
}
```

**実現された機能:**
- DisplayAtTop=true要素の特別扱い（文頭配置）
- 疑問詞の自動認識と優先順位制御
- 通常スロットとの適切な分離処理

#### 5. フォールバック機能付きDOM読み取り
```javascript
extractCurrentSentenceFromDynamicArea() {
    // ID ベースでの検出
    const slotNames = ['m1', 's', 'aux', 'm2', 'v', 'c1', 'o1', 'o2', 'c2', 'm3'];
    
    slotNames.forEach(slotName => {
        const dynamicSlotElement = dynamicArea.querySelector(`#dynamic-slot-${slotName}, .slot[data-display-order]`);
        if (dynamicSlotElement) {
            const phraseElement = dynamicSlotElement.querySelector('.slot-phrase');
            if (phraseElement && this.isElementVisible(phraseElement)) {
                const text = phraseElement.textContent.trim();
                if (text && text !== 'N/A' && text !== '') {
                    // data-display-order から順序を取得
                    let displayOrder = parseInt(dynamicSlotElement.dataset.displayOrder);
                    if (!displayOrder) {
                        const slotOrderMap = { m1: 1, s: 2, aux: 3, m2: 4, v: 5, c1: 6, o1: 7, o2: 8, c2: 9, m3: 10 };
                        displayOrder = slotOrderMap[slotName] || 999;
                    }
                }
            }
        }
    });
}
```

**実現された機能:**
- データソース失敗時のDOM直接読み取りフォールバック
- 要素可視性判定（CSS display/visibility/opacity チェック）
- 複数の要素検索方法（ID、クラス、data属性）
- N/A値や空文字の適切な除外処理

### ✅ 完全実装済み音声合成機能

#### 1. Web Speech API統合
- 高品質音声合成による模範読み上げ
- 音声速度・音量・声質のカスタマイズ対応
- 複数言語対応（英語・日本語）

#### 2. 録音・再生機能
- MediaRecorder APIによる高品質録音
- WebM/MP3フォーマット対応
- リアルタイム録音レベル表示
- ワンクリック再生機能

#### 3. 基本音響分析
- 録音時間計測機能
- 音量レベル分析
- 発話速度評価システム
- レベル別目標時間設定

#### 4. 学習進捗管理
- ローカルストレージによるデータ永続化
- 練習回数・スコア・改善率の追跡
- 日次・週次・月次統計機能

---

## 🚀 未実装機能（将来拡張）

### ⚠️ 他ユーザーとの比較機能
- **必要技術**: サーバーサイド開発、データベース設計
- **実装要件**: ユーザー認証、データ匿名化、集計システム
- **技術課題**: プライバシー保護、スケーラビリティ、リアルタイム更新

---

## 📊 技術的達成度

| 機能カテゴリ | 実装状況 | 達成度 |
|------------|----------|--------|
| 基本読み上げ機能 | ✅ 完了 | 100% |
| 複合データ対応 | ✅ 完了 | 100% |
| ランダマイズ対応 | ✅ 完了 | 100% |
| 録音・再生機能 | ✅ 完了 | 100% |
| 音響分析・評価 | ✅ 完了 | 100% |
| 進捗管理 | ✅ 完了 | 100% |
| UI/UX統合 | ✅ 完了 | 100% |
| サーバー連携 | ❌ 未実装 | 0% |

**総合達成度: 87.5%** （8機能中7機能完了）

---

## 🔮 将来実装予定機能

### 📱 スマホ最適化機能
現在の実装はPC環境での最適化を重視しており、スマホでの音声言語制御には技術的制約があります。将来的に以下の機能を実装予定です。

#### 🎯 Phase 1: 英語音声検出・警告機能
- **日本語音声検出**: ユーザーの音声設定が日本語の場合に自動検出
- **警告ダイアログ**: 英語学習のため英語音声への変更を促すポップアップ
- **設定ガイダンス**: プラットフォーム別の音声設定変更手順を表示

#### 🎯 Phase 2: プラットフォーム別対応
- **iOS対応**: Safari での音声エンジン制御最適化
- **Android対応**: Chrome での音声制御改善
- **レスポンシブUI**: スマホ向けの音声制御パネル

#### 🎯 Phase 3: 設定確認・サポート機能
- **設定確認**: 英語音声の設定完了チェック
- **音声テスト**: 設定後の音声品質確認
- **トラブルシューティング**: 音声設定に関する問題解決支援

#### 🔧 技術的課題
- **プラットフォーム依存**: iOS/Android での音声エンジンの違い
- **システム言語設定**: 端末の言語設定に強く依存
- **Web Speech API制限**: ネイティブアプリほどの制御ができない
- **音声データ**: ユーザーが手動で英語音声をダウンロードする必要

#### 📈 期待される効果
- **英語学習効果**: 適切な英語音声での学習促進
- **ユーザビリティ**: 直感的な音声設定変更
- **クロスプラットフォーム**: PC/スマホ両方での快適な利用

#### 🎯 実装優先度
現在の開発では**PC環境での機能完成**を最優先とし、**スマホ最適化は将来実装**として位置づけています。

---
