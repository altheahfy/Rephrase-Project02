# 🌐 ngrok を使用したHTTPS接続設定

## 📥 ngrok のダウンロード・インストール
1. https://ngrok.com/ にアクセス
2. アカウント作成（無料）
3. ngrok をダウンロード
4. authtoken を設定

## 🚀 使用方法

### 1. Live Server を通常通り起動
VS Code で Live Server を起動（HTTP、ポート5500）

### 2. ngrok でHTTPSトンネル作成
```bash
# コマンドプロンプトで実行
ngrok http 5500
```

### 3. 出力されるHTTPS URLを使用
```
Session Status                online
Account                       your_account
Version                       3.x.x
Region                        Japan (jp)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:5500

# ↑ この https://abc123.ngrok.io をスマホで開く
```

## ✅ メリット
- 証明書設定不要
- 外部からもアクセス可能
- 設定が最も簡単

## ⚠️ 注意点
- インターネット経由（若干遅延あり）
- 無料版は8時間制限
- URLが毎回変わる
