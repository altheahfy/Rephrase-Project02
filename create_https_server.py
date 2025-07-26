#!/usr/bin/env python3
"""
ローカルHTTPSサーバー - 音声録音テスト用
自己署名証明書を自動生成してHTTPSサーバーを起動
"""

import http.server
import ssl
import os
import subprocess
import sys
from pathlib import Path

def create_self_signed_cert():
    """自己署名証明書を作成"""
    cert_file = "localhost.crt"
    key_file = "localhost.key"
    
    # 既存の証明書ファイルをチェック
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"✅ 既存の証明書を使用: {cert_file}, {key_file}")
        return cert_file, key_file
    
    print("🔐 自己署名証明書を作成中...")
    
    try:
        # OpenSSLコマンドで証明書を作成
        cmd = [
            "openssl", "req", "-x509", "-newkey", "rsa:4096", 
            "-keyout", key_file, "-out", cert_file, "-days", "365", "-nodes",
            "-subj", "/C=JP/ST=Tokyo/L=Tokyo/O=Local/OU=Development/CN=localhost"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ 自己署名証明書作成完了")
        return cert_file, key_file
        
    except subprocess.CalledProcessError as e:
        print(f"❌ OpenSSLエラー: {e}")
        print("💡 OpenSSLがインストールされていない可能性があります")
        return create_python_cert()
    except FileNotFoundError:
        print("⚠️ OpenSSLが見つかりません。Pythonで代替証明書を作成します...")
        return create_python_cert()

def create_python_cert():
    """PythonのcryptographyライブラリでSSL証明書を作成"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        print("🐍 Pythonで自己署名証明書を作成中...")
        
        # 秘密鍵を生成
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # 証明書の詳細を設定
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "JP"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Tokyo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Local Development"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        # 証明書を作成
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # ファイルに保存
        cert_file = "localhost.crt"
        key_file = "localhost.key"
        
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Python証明書作成完了")
        return cert_file, key_file
        
    except ImportError:
        print("❌ cryptographyライブラリがインストールされていません")
        print("💻 インストール: pip install cryptography")
        return None, None

def start_https_server(port=8443):
    """HTTPSサーバーを開始"""
    cert_file, key_file = create_self_signed_cert()
    
    if not cert_file or not key_file:
        print("❌ SSL証明書の作成に失敗しました")
        return
    
    # カスタムHTTPRequestHandlerクラス
    class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    # HTTPSサーバーを設定
    httpd = http.server.HTTPServer(('localhost', port), CORSHTTPRequestHandler)
    
    # SSL設定
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"🚀 HTTPSサーバーを開始しました")
    print(f"📡 URL: https://localhost:{port}")
    print(f"📱 モバイル音声録音テストが可能です")
    print(f"⚠️ ブラウザで「安全でない」警告が表示されますが、「詳細設定」→「localhost にアクセスする（安全ではありません）」で続行してください")
    print(f"🛑 停止するには Ctrl+C を押してください")
    print(f"")
    print(f"📋 テスト手順:")
    print(f"1. ブラウザで https://localhost:{port} にアクセス")
    print(f"2. セキュリティ警告を無視して続行")
    print(f"3. training/matrix/ にアクセス")
    print(f"4. 音声録音をテスト")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 サーバーを停止しました")
        httpd.shutdown()

if __name__ == "__main__":
    port = 8443
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ 無効なポート番号です。デフォルトの8443を使用します。")
    
    start_https_server(port)
