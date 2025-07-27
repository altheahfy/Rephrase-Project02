# Rephraseプロジェクト - イラスト作成実行計画書

## 概要
`slot_order_data.json`に登場する単語のうち、イラスト化に適した124個の単語について、5つのAIツールを使用してイラストを作成する計画です。

## 現状
- 既存のイラスト: 65個（`slot_images\common\`に格納済み）
- 追加で必要なイラスト: 124個

## AIツール別分担

### 1. ChatGPT（25個）
- 対象単語: absent, academic, administrator, afternoon, alarm, analyze, appeared, avoid, avoided, became, become, believed, briefing, building, capable, catch, central, challenges, clarity, clouded, completed, complex, composure, confidence, confident
- 特徴: 詳細な説明と具体的な描写が得意
- プロンプト形式: 「A simple black and white line art illustration of...」

### 2. Gemini（25個）
- 対象単語: counting, critical, crucial, cruelty, data, days, decisive, dependable, determined, direct, doubt, earlier, echoed, employee, encourage, engineer, enhance, everyone, exhausting, experiment, facing, fatigue, feared, figured, filled
- 特徴: 構造化された指示に従うのが得意
- プロンプト形式: 「Create a simple black and white line drawing illustration showing...」

### 3. Bing Image Creator（25個）
- 対象単語: final, flawlessly, full, given, growth, hard, help, hesitation, instant, instructor, joined, known, laboratory, lacked, leader, lessons, lingered, long, make, math, mentally, meticulously, mind, missed, moment
- 特徴: シンプルで明確な指示が効果的
- プロンプト形式: 「Simple black and white line art drawing of...」

### 4. Ideogram（25個）
- 対象単語: near, new, notice, occurred, offered, out, outage, outline, people, point, policy, power, prepared, previous, prior, privious, publication, recently, reflect, remarkable, reputation, research, responded, responsible, returned
- 特徴: テキストとイラストの組み合わせが得意
- プロンプト形式: 「Black and white line art illustration:...」

### 5. Playground（24個）
- 対象単語: room, scientist, seemed, severe, shown, silence, spoke, staff, students, suggestions, support, taken, think, thoughts, tom, transferred, trying, uncertainty, unexpected, voice, waiting, wanted, week, working
- 特徴: アーティスティックな表現が得意
- プロンプト形式: 「Line art illustration in black and white showing...」

## 共通スタイル要件
- 白黒の線画
- シンプルで分かりやすい
- 漫画風のスタイル
- 色なし、グラデーションなし
- 明確な黒い線のみ
- 単語の概念を直感的に理解できる

## 実行手順

### Phase 1: プロンプトファイルの確認
- [x] `chatgpt_prompts.md` - ChatGPT用プロンプト（25個）
- [x] `gemini_prompts.md` - Gemini用プロンプト（25個）
- [x] `bing_prompts.md` - Bing Image Creator用プロンプト（25個）
- [x] `ideogram_prompts.md` - Ideogram用プロンプト（25個）
- [x] `playground_prompts.md` - Playground用プロンプト（24個）

### Phase 2: イラスト生成
1. 各AIツールにアクセス
2. 対応するプロンプトファイルを参照
3. 1つずつプロンプトを実行
4. 生成されたイラストをダウンロード

### Phase 3: ファイル管理
1. 生成されたイラストを`slot_images\common\`フォルダに保存
2. ファイル名は単語名（例: `absent.png`）
3. 複数の単語を含む場合はアンダースコア区切り（例: `figure_out.png`）

### Phase 4: 品質確認
1. 各イラストが対応する単語を適切に表現しているか確認
2. スタイルが統一されているか確認
3. 必要に応じて再生成

## 注意事項
- 各AIツールの利用制限に注意
- 生成されたイラストの品質が低い場合は、プロンプトを調整して再生成
- 著作権に配慮し、オリジナルのイラスト生成を心がける

## 完了基準
- 124個すべての単語にイラストが割り当てられている
- イラストの品質が一定水準以上である
- ファイル名が正しく設定されている
- `slot_images\common\`フォルダに適切に格納されている

## 進捗管理
- [ ] ChatGPT: 0/25個完了
- [ ] Gemini: 0/25個完了
- [ ] Bing Image Creator: 0/25個完了
- [ ] Ideogram: 0/25個完了
- [ ] Playground: 0/24個完了

## 総進捗: 0/124個（0%）
