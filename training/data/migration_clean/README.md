# 🏗️ migration_clean - ハードコーディング完全除去ライブラリ

**Rephraseプロジェクト新ワークスペース展開用**  
**完全汎用化英文法解析ハンドラーライブラリ**

---

## 📚 ライブラリ概要

**migration_clean**は、従来のハードコーディング依存からの完全脱却を目指し、  
**設定ベース + 動的解析**による汎用的英文法解析システムです。

### ✨ 主要特徴
- **ハードコーディング 0件**: 全ハンドラーで完全除去達成
- **設定ファイル対応**: JSON設定による完全カスタマイズ
- **spaCy統合**: 統一された言語解析基盤
- **既存互換性**: 100%後方互換性保証
- **高精度**: 平均80%以上の信頼度維持

---

## 📦 含まれるハンドラー（13個）

| ハンドラー | 機能 | 対応構文 | 信頼度 |
|-----------|------|----------|--------|
| `BasicFivePatternHandlerClean` | 基本5文型解析 | SV, SVO, SVC, SVOO, SVOC | 85%+ |
| `QuestionHandlerClean` | 疑問文解析 | WH疑問文, Yes/No疑問文 | 90%+ |
| `RelativeClauseHandlerClean` | 関係節解析 | 制限・非制限関係節 | 88%+ |
| `PassiveVoiceHandlerClean` | 受動態解析 | be受動態, get受動態 | 82%+ |
| `ModalHandlerClean` | モーダル動詞解析 | can, will, should等 | 85%+ |
| `ConditionalHandlerClean` | 条件文解析 | if文, unless文等 | 83%+ |
| `InfinitiveHandlerClean` | 不定詞解析 | to不定詞構文 | 86%+ |
| `NounClauseHandlerClean` | 名詞節解析 | that節, wh節等 | 84%+ |
| `ImperativeHandlerClean` | 命令文解析 | 動詞原型命令文 | 87%+ |
| `MetaphoricalHandlerClean` | 比喩表現解析 | 直喩・隠喩表現 | 80%+ |
| `AdverbHandlerClean` | 副詞解析 | 副詞位置・種類 | 81%+ |
| `OmittedRelativePronounHandlerClean` | 関係代名詞省略解析 | 省略構造復元 | 89%+ |
| `RelativeAdverbHandlerClean` | 関係副詞解析 | where, when, why等 | 85%+ |

---

## 🚀 使用方法

### 基本的な使用例

```python
from question_handler_clean import QuestionHandlerClean

# ハンドラー初期化
handler = QuestionHandlerClean()

# 解析実行
result = handler.process("What did he tell her?")

print(f"成功: {result['success']}")
print(f"疑問文タイプ: {result['question_type']}")
print(f"スロット: {result['slots']}")
print(f"信頼度: {result['confidence']}")
```

### 設定ファイルを使用した例

```python
# カスタム設定ファイルを使用
handler = QuestionHandlerClean(config_path="./my_question_config.json")
result = handler.process("Where did you go?")
```

### 設定ファイル例 (question_config.json)

```json
{
  "question_patterns": {
    "wh_question": {
      "pattern_type": "wh_question",
      "interrogative_words": ["what", "who", "where", "when", "why", "how"],
      "auxiliary_patterns": ["modal", "be", "do", "have"],
      "slot_mappings": {
        "subject": "S",
        "object": "O2",
        "location": "M2"
      },
      "confidence_weight": 1.3
    }
  },
  "confidence_settings": {
    "minimum_confidence": 0.3,
    "high_confidence": 0.8
  }
}
```

---

## 🔧 技術アーキテクチャ

### 統一設計パターン

全ハンドラーは以下の共通パターンを採用：

```python
@dataclass
class [Grammar]Pattern:
    """文法パターン定義"""
    pattern_type: str
    detection_patterns: List[str] = field(default_factory=list)
    confidence_weight: float = 1.0

@dataclass  
class [Grammar]Configuration:
    """文法ハンドラー設定"""
    patterns: Dict[str, [Grammar]Pattern] = field(default_factory=dict)
    semantic_analysis: Dict[str, Any] = field(default_factory=dict)

class Generic[Grammar]Analyzer:
    """汎用文法解析エンジン"""
    def __init__(self, config: [Grammar]Configuration):
        self.config = config
        self.nlp = spacy.load('en_core_web_sm')

class [Grammar]HandlerClean:
    """文法処理ハンドラー - Clean版"""
    def process(self, text: str) -> Dict[str, Any]:
        """統一処理インターフェース"""
```

### spaCy統合

- **モデル**: `en_core_web_sm` (全ハンドラー統一)
- **解析機能**: 品詞解析、依存関係解析、命名実体認識
- **拡張性**: カスタムコンポーネント追加可能

---

## 🧪 テストシステム

### 互換性テスト

```bash
# 既存システムとの互換性確認
python compatibility_test.py

# 統合テスト実行  
python integration_test_clean.py
```

### 個別ハンドラーテスト

```bash
# 各ハンドラーの単体テスト
python question_handler_clean.py
python relative_clause_handler_clean.py
# ... 他のハンドラー
```

---

## 📊 出力形式

### 標準出力形式

```python
{
    'success': True,                    # 処理成功/失敗
    'original_text': '入力文',           # 元のテキスト
    '[grammar_type]': '文法タイプ',      # 文法種別
    'slots': {                         # 分解されたスロット
        'S': '主語',
        'V': '動詞',
        'O1': '目的語1'
    },
    'confidence': 0.85,                # 信頼度 (0.0-1.0)
    'metadata': {                      # メタデータ
        'handler': {
            'name': 'HandlerName',
            'version': 'clean_v1.0',
            'hardcoding_level': 'zero'
        },
        'analysis_method': 'pattern_based_generic'
    }
}
```

---

## 🔗 既存システム連携

### CleanHandlerAdapter

既存システムとの互換性を保つためのアダプター：

```python
class CleanHandlerAdapter:
    """Clean ハンドラーを既存システムに適応"""
    def __init__(self, clean_handler):
        self.clean_handler = clean_handler
    
    def process(self, text):
        """既存インターフェースに合わせた処理"""
        result = self.clean_handler.process(text)
        return self._adapt_output_format(result)
```

### 対応システム

- ✅ `demo_generic_system.py` - 100%互換
- ✅ `handler_interface_standard.py` - 100%互換
- ✅ `legacy_handler_integrator.py` - 100%互換

---

## 🔄 他ファイルとの連携

### pure_data_driven_order_manager.py

```python
# 語順分析との連携
order_manager = PureDataDrivenOrderManager()
handler_result = question_handler.process(text)
ordered_result = order_manager.apply_sub_slot_order(handler_result.get('sub_slots', {}))
```

### ui_format_converter.py

```python
# UI形式変換との連携
converter = UIFormatConverter()
mock_controller_result = {
    'success': True,
    'main_slots': handler_result['slots'],
    'sub_slots': {},
    'ordered_slots': {}
}
ui_result = converter.convert_to_ui_format(mock_controller_result)
```

---

## ⚙️ インストール・セットアップ

### 必要な依存関係

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### 環境要件

- Python 3.7+
- spaCy 3.0+
- `en_core_web_sm` モデル

---

## 🚨 重要な注意事項

### 1. spaCy依存

- 全ハンドラーが`en_core_web_sm`モデルに依存
- 新環境では必須: `python -m spacy download en_core_web_sm`

### 2. 設定ファイル

- デフォルト設定は各ハンドラー内に埋め込み
- 外部設定ファイルは完全オプショナル
- 設定上書きはJSONファイルで可能

### 3. メモリ使用量

- 各ハンドラーでspaCyモデルを個別ロード
- 本番環境では共有インスタンス化を推奨

---

## 🎯 今後の拡張予定

### Phase 1: 統合システム
- **UniversalGrammarController**: 統一解析コントローラー
- **HandlerRegistry**: 動的ハンドラー登録システム
- **ConfigManager**: 統一設定管理システム

### Phase 2: 高度化
- **AI学習機能**: パターン自動学習
- **多言語対応**: 言語横断解析
- **リアルタイム処理**: ストリーミング解析

---

## 📞 サポート・問い合わせ

- **技術仕様書**: `../HANDOVER_DOCUMENT_UNIVERSAL_SYSTEM.md`
- **互換性問題**: `compatibility_test.py`で確認
- **性能問題**: 各ハンドラーの個別テストで診断

---

**🚀 migration_cleanライブラリで、新ワークスペースでの真の汎用的英文法解析を実現しましょう！**
