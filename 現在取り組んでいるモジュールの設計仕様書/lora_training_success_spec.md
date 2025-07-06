
# LoRA学習 成功構成・運用仕様書

## ✅ 成功した構成概要

### 使用ベースモデル（pretrained_model_name_or_path）
- モデル名: `runwayml/stable-diffusion-v1-5`
- フォーマット: Hugging Face diffusers 形式
- 認証: Huggingface トークンによる `huggingface-cli login` に成功済み

huggingface-cli login --token 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

### トークン認証処理
```bash
huggingface-cli login
# プロンプトにトークン (hf_...) を貼り付けてEnter
# 成功すると ~/.cache/huggingface/token に保存される
```

---

## 🗂️ フォルダ構成と学習データ

```
C:\AI\sd-scripts\
├─ dataset\
│   └─ lineart\
│       └─ 1\
│           ├─ 001.png
│           ├─ 001.txt
│           ├─ ...
```

- `.png`と対応する`.txt`キャプションが同フォルダ内に64セット以上存在することを確認

---

## ✅ 成功したコマンド（1行）
C\AI\sd-scriptsでpowershellを起動し、以下のコマンドを貼り付けて実行。


```bash
accelerate launch train_network.py --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" --train_data_dir="dataset/lineart" --output_dir="lora_out" --resolution=512,512 --network_alpha=4 --network_dim=4 --network_module=networks.lora --output_name="lineart_lora" --train_batch_size=1 --max_train_steps=1000 --learning_rate=1e-4 --lr_scheduler="constant" --text_encoder_lr=5e-5 --mixed_precision="fp16" --save_every_n_steps=100 --save_model_as=safetensors --caption_extension=".txt" --enable_bucke --save_state
```


---

## 🚫 主なトラブルと対応策

### ❶ トークン認証失敗
**症状**: `Invalid token passed` や `401 Unauthorized`

**原因**:
- トークンが "..." 表示で途中までしか貼り付けられていない
- Git Credential Manager に古い認証が残っている

**対策**:
- huggingface.co で **フル長のトークンを再コピー**
- PowerShellで以下を実行：
```bash
huggingface-cli login
# トークン貼付け後、Yでgit credentialにも保存
```

---

### ❷ モデルが読み込めない (`v1-5-pruned` など）
**症状**: `is neither a valid local path nor a valid repo id`

**対策**:
- `v1-5-pruned.safetensors` は diffusers 形式ではない
- diffusers 形式を使うには Hugging Face 上の `runwayml/stable-diffusion-v1-5` を使う
- トークン認証必須

---

### ❸ 学習が始まるが途中で止まる（画像サイズエラー）

**症状**:
```
AssertionError: image too large, but cropping and bucketing are disabled
```

**対策**:
- `--enable_bucket` オプションを追加して解決

---

### ❹ 学習途中で tokenizer 関連の AttributeError

**症状**:
```
AttributeError: 'CLIPTokenizer' object has no attribute 'added_tokens_encoder'
```

**対策**:
- transformers / diffusers のバージョン不整合
- 必要なら以下でアップグレード：
```bash
pip install --upgrade transformers diffusers
```

---

## 📝 備考

- モデル保存先：`lora_out/lineart_lora.safetensors`
- SD WebUI で使用する場合は「LoRAモデル」フォルダにコピー
- 実行後に `.ckpt` ではなく `.safetensors` で保存される仕様


🔧 次におすすめのステップ（任意）
プロンプト→画像のタグ表（プロンプト管理台帳）の構築
→ LoRA訓練ログや失敗時のデバッグ効率が劇的に上がります。

絵柄LoRA（線画スタイル）の同時適用
→ 線の太さ・陰影・抜けの表現まで揃え、教材としての一貫性が出せます。

プロンプト分類ルールの整備
→ たとえば「pose + emotion + composition + object detail」など、書式を固定することで拡張性と学習効率を両立できます。

学習用画像セットの精選（ノイズ除去）
→ 手や顔の崩れ、意図と違う構図などを除いて学習精度を高めます。


