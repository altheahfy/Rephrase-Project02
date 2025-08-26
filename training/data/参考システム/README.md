# 参考システム - 旧実装群

**⚠️ 重要警告**: このフォルダ内のコードは**参考のみ**です。**絶対に直接使用・継承・コピペしないでください。**

## 📁 フォルダ構成

### 🗂️ 旧エンジン群/
- engines/ - 最新の個別文法処理エンジン
- migration_source/ - マイグレーション用エンジン群
- **用途**: 設計コンセプトの参考のみ
- **禁止**: コード流用、クラス継承、メソッド継承

### 🧪 テストスクリプト/
- 既存のテスト・検証スクリプト
- **用途**: テスト手法の参考のみ  
- **禁止**: スクリプトの直接実行、期待値の変更

### 🏗️ 旧システム群/
- archive/ - アーカイブシステム
- backup/ - バックアップファイル
- development_archive/ - 開発履歴
- final_test_system/ - 旧テストシステム
- monitoring/ - モニタリングシステム
- safety_infrastructure/ - 安全性インフラ
- universal_slot_system/ - 旧スロットシステム

### 📄 主要システムファイル
- `dynamic_grammar_mapper.py`: メインシステム（Phase A2違反あり）
- `boundary_expansion_lib.py`: 境界拡張ライブラリ
- `grammar_handler_fix_priorities.py`: 優先度管理
- `CURRENT_SYSTEM_STATUS.md`: 旧システム状況記録
- `Excel_Generator.py`: Excelファイル生成ツール

## 🚫 絶対禁止事項

1. **❌ コード直接使用**: 既存コードのコピー&ペースト
2. **❌ クラス継承**: 既存クラスからの継承
3. **❌ 依存関係**: 既存ファイルへのimport
4. **❌ テスト変更**: 期待値・テストケースの変更
5. **❌ Phase A2概念**: 既存の設計違反概念の導入

## ✅ 許可される参考方法

1. **🔍 設計コンセプト**: アルゴリズムの基本思想
2. **📋 処理パターン**: 文法認識のアプローチ
3. **🎯 テスト手法**: 検証方法の考え方
4. **📊 データ構造**: スロット設計の参考

## 📖 NEW_SYSTEM_DESIGN_SPECIFICATION.md を必読

新規システムの開発は、`NEW_SYSTEM_DESIGN_SPECIFICATION.md`の設計仕様に**厳密に従って**実装してください。

**完全新規実装 = Zero Technical Debt**
