# CLIインターフェース開発アーカイブ (2025年8月17日)

## 📁 **アーカイブ内容**

このフォルダには、UnifiedStanzaRephraseMapperのCLIインターフェース開発過程で作成された一時ファイルや開発用スクリプトを保存しています。

### **🗂️ フォルダ構成**

#### **📊 batch_results/**
CLI開発過程で生成されたバッチ処理結果ファイル
- `batch_results_20250817_143730.json` - 最初のCLI実行結果
- `batch_results_53_examples.json` - 53例文テスト結果
- `batch_results_working.json` - 作業中の中間結果
- `batch_results_final.json` - 最終テスト結果
- `my_results.json` - カスタム例文テスト結果

#### **🔧 debug_scripts/**
開発・デバッグ用のスクリプトファイル
- `debug_auxiliary_clauses.py` - 助動詞句解析デバッグ
- `debug_hard_example.py` - 困難例文専用デバッグ
- `test_adverb_fixes.py` - 副詞配置修正テスト
- `test_system_debug.py` - システム全体デバッグ
- `compare_sentences.py` - 旧比較スクリプト（compare_results.pyに統合済み）

#### **📝 test_examples/**
CLI機能テスト用の例文ファイル
- `my_test_sentences.json` - カスタム5例文テストセット（100%精度達成）
- `simple_sentences.json` - シンプル形式の例文テスト

## 📈 **開発成果**

### **達成された精度**
- カスタム5例文: **100.0%** 完全一致
- 標準53例文: **45.3%** 完全一致
- 主要スロット精度: S:88.7%, V:96.2%, C1:95.2%

### **実装された機能**
- ✅ CLIインターフェース（--input, --output オプション）
- ✅ バッチ処理機能
- ✅ 結果照合システム分離
- ✅ JSON循環参照エラー解決
- ✅ 5つのハンドラー同時実行

### **技術仕様**
- **コアファイル**: `unified_stanza_rephrase_mapper.py`
- **照合ツール**: `compare_results.py`
- **仕様書**: `specifications/UnifiedStanzaRephraseMapper_v1.0_Spec.md`

## 🔄 **移行理由**

CLI実装が完了し、本番使用可能な状態になったため、開発過程の一時ファイルを整理。
今後は `batch_results_complete.json` を基準ファイルとして使用。

## 📚 **参照文献**

- メイン仕様書: `../specifications/UnifiedStanzaRephraseMapper_v1.0_Spec.md`
- システム現状: `../CURRENT_SYSTEM_STATUS.md`
- 最新結果: `../batch_results_complete.json`

---

**アーカイブ作成日**: 2025年8月17日  
**開発フェーズ**: CLI実装完了 → 精度向上フェーズ移行
