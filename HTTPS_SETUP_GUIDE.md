# 📱 Rephrase HTTPS開発サーバー起動スクリプト

## 📋 必要な準備

### 1. Node.js http-server のインストール
```bash
npm install -g http-server
```

### 2. OpenSSL で自己署名証明書を作成（Windows）
```bash
# 秘密鍵を作成
openssl genrsa -out server.key 2048

# 証明書署名要求（CSR）を作成
openssl req -new -key server.key -out server.csr -config ssl.conf

# 自己署名証明書を作成（1年間有効）
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt -extensions v3_req -extfile ssl.conf
```

### 3. SSL設定ファイル（ssl.conf）
```ini
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = JP
ST = Tokyo
L = Tokyo
O = Rephrase Development
OU = Development Team
CN = 192.168.1.100

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = 192.168.1.100
```

## 🚀 サーバー起動コマンド

### HTTPS対応サーバー起動
```bash
# プロジェクトフォルダで実行
http-server -p 8443 -S -C server.crt -K server.key -a 0.0.0.0 --cors

# または、より簡単な方法（自動証明書生成）
http-server -p 8443 -S -a 0.0.0.0 --cors
```

### アクセス方法
```
PC: https://localhost:8443
スマホ: https://192.168.1.100:8443 （PCのIPアドレス）
```

## ⚠️ 重要な注意事項

### ブラウザの証明書警告
1. **PC Chrome**: 「詳細設定」→「安全でないサイトにアクセス」
2. **Android Chrome**: 「詳細」→「192.168.1.100にアクセス（安全でない）」
3. **iPhone Safari**: 「詳細」→「Webサイトにアクセス」

### 証明書の永続的信頼設定
**Android Chrome:**
1. 設定 → プライバシーとセキュリティ → セキュリティ
2. 詳細設定 → 証明書の管理
3. server.crt ファイルをインポート

**iPhone:**
1. 設定 → 一般 → VPNとデバイス管理
2. 証明書をインストール
3. 設定 → 一般 → 情報 → 証明書信頼設定

## 🔧 トラブルシューティング

### よくある問題と解決策

#### 1. ERR_CERT_AUTHORITY_INVALID
**原因**: 自己署名証明書による警告
**解決**: ブラウザで「安全でないサイトにアクセス」を選択

#### 2. マイクアクセス拒否
**原因**: HTTPSでもマイク許可が必要
**解決**: アドレスバーのアイコンから「マイク許可」

#### 3. 接続できない
**原因**: ファイアウォールによるブロック
**解決**: Windows Defender でポート8443を許可

### 診断コマンド
```bash
# PCのIPアドレス確認
ipconfig

# ポート開放確認
netstat -an | findstr 8443

# ファイアウォール確認
netsh advfirewall firewall show rule name="Node.js"
```

## 🎯 最終確認

### 成功パターン
```
✅ https://192.168.1.100:8443 でアクセス
✅ 証明書警告を承認
✅ マイクアクセスを許可
✅ 「✅ マイクアクセス許可取得済み」がコンソールに表示
✅ 録音ボタンが正常動作
```

### 代替確認方法
diagnostic tool: `https://192.168.1.100:8443/microphone-diagnosis.html`
