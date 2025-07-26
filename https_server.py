#!/usr/bin/env python3
import http.server
import ssl
import socketserver
import os
from pathlib import Path

# ポート設定
PORT = 3000
HOST = '0.0.0.0'

# 現在のディレクトリを取得
current_dir = Path(__file__).parent

# HTTPSサーバークラス
class HTTPSServer:
    def __init__(self, port=PORT, host=HOST):
        self.port = port
        self.host = host
        
    def create_self_signed_cert(self):
        """自己署名証明書を作成"""
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization
            import datetime
            import ipaddress
            
            # 秘密鍵を生成
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # 証明書の基本情報
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "JP"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Tokyo"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Rephrase Dev"),
                x509.NameAttribute(NameOID.COMMON_NAME, "192.168.0.154"),
            ])
            
            # 証明書を作成
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.DNSName("192.168.0.154"),
                    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                    x509.IPAddress(ipaddress.IPv4Address("192.168.0.154")),
                ]),
                critical=False,
            ).sign(key, hashes.SHA256())
            
            # PEMファイルに保存
            with open("cert.pem", "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            with open("key.pem", "wb") as f:
                f.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            print("SSL証明書を作成しました: cert.pem, key.pem")
            return True
            
        except ImportError:
            print("cryptographyライブラリが見つかりません。pip install cryptographyでインストールしてください。")
            return False
        except Exception as e:
            print(f"証明書作成エラー: {e}")
            return False
    
    def start_server(self):
        """HTTPSサーバーを開始"""
        # 証明書ファイルをチェック
        if not (Path('cert.pem').exists() and Path('key.pem').exists()):
            print("SSL証明書が見つかりません。作成を試みます...")
            if not self.create_self_signed_cert():
                print("HTTPサーバーとして起動します（音声録音機能は無効）")
                self.start_http_server()
                return
        
        try:
            # HTTPSサーバーを作成
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer((self.host, self.port), handler)
            
            # SSL設定
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain('cert.pem', 'key.pem')
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"HTTPSサーバーが起動しました: https://{self.host}:{self.port}")
            print("Ctrl+C で停止します")
            httpd.serve_forever()
            
        except Exception as e:
            print(f"HTTPSサーバー起動エラー: {e}")
            print("HTTPサーバーとして起動します")
            self.start_http_server()
    
    def start_http_server(self):
        """HTTPサーバーを開始（フォールバック）"""
        try:
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer((self.host, self.port), handler)
            print(f"HTTPサーバーが起動しました: http://{self.host}:{self.port}")
            print("Ctrl+C で停止します")
            httpd.serve_forever()
        except Exception as e:
            print(f"サーバー起動エラー: {e}")

if __name__ == "__main__":
    server = HTTPSServer()
    server.start_server()
