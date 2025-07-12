# Rephraseプロジェクト 音声機構システム 設計仕様書

## 🎯 概要

Rephraseプロジェクトにおける音声学習機能の統合設計仕様書です。学習者の発話練習、録音・再生、模範音声の提供、発音評価、進捗追跡、全国比較機能を実現する包括的な音声システムを定義します。

## 📋 要求仕様（再定義）

### ①発話練習モード
- **目的**: 選択したスロットのテキストを非表示にして、イラストをヒントに発話練習
- **対象**: 個別スロット（M1, S, AUX, V, O1等）または全文
- **習熟度連動**: 初心者〜達人レベルに応じた非表示範囲の調整

### ②録音・再生機能
- **録音**: 学習者の発話を高品質で録音
- **再生**: 録音内容の確認・検証
- **フォーマット**: WebM/MP3対応、ブラウザネイティブ

### ③模範音声システム
- **自動生成**: 完成例文に対するワンクリック模範読み上げ
- **音声合成**: Web Speech API（TTS）使用
- **カスタマイズ**: 速度・声質・アクセント調整可能

### ④発音評価機能
- **音声比較**: 学習者録音vs模範音声の基本比較
- **評価指標**: 音声長、音量レベル、基本的な音響特徴
- **精度方針**: 厳密性よりユーザビリティ重視

### ⑤発話速度評価
- **基準設定**: レベル別目標速度（初心者1秒/語 → 達人0.3秒/語）
- **時間計測**: 発話開始〜終了の正確な時間測定
- **達成度表示**: 目標時間vs実際時間の比較

### ⑥学習進捗管理
- **データ蓄積**: ローカルストレージ + オプションでサーバー同期
- **期間別統計**: 1週間、1ヶ月、3ヶ月単位の上達傾向
- **視覚化**: グラフ・チャートによる進捗表示

### ⑦全国比較機能（将来実装）
- **サーバーサイド**: ユーザーデータの匿名化集計
- **比較指標**: 発話速度、練習時間、達成率等
- **フィードバック**: 全国平均との位置づけ表示

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
