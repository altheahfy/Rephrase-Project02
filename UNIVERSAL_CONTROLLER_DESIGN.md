# 🎯 Universal Grammar Controller 設計図
## 次フェーズ実装のための詳細設計仕様

**目標**: migration_cleanライブラリを基盤とした真の汎用的中央管理システム

---

## 🏗️ システム全体アーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│                Universal Grammar Controller                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Text Router    │  │  Handler Pool   │  │ Result Merger   │ │
│  │  (パターン判定)  │  │  (並列処理)     │  │  (競合解決)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Handler Registry│  │ Config Manager  │  │ Performance Mon │ │
│  │ (動的登録)      │  │ (統一設定)      │  │ (性能監視)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    migration_clean Library                  │
│  BasicFive │ Question │ Relative │ Passive │ Modal │ ...     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 コアコンポーネント設計

### 1. UniversalGrammarController (統一コントローラー)

```python
class UniversalGrammarController:
    """
    汎用文法解析統一コントローラー
    
    責任範囲:
    - テキスト入力の受付
    - 適切なハンドラーの選択・実行
    - 結果の統合・競合解決
    - 最終出力の生成
    """
    
    def __init__(self, config_path: str = "universal_config.json"):
        self.config = self._load_universal_config(config_path)
        self.registry = HandlerRegistry()
        self.router = TextAnalysisRouter()
        self.merger = ResultMerger()
        self.performance_monitor = PerformanceMonitor()
        
        # migration_cleanハンドラーの自動登録
        self._register_migration_clean_handlers()
    
    def analyze(self, text: str, analysis_mode: str = "comprehensive") -> Dict[str, Any]:
        """
        統一解析インターフェース
        
        Args:
            text: 解析対象テキスト
            analysis_mode: "comprehensive" | "fast" | "specialized"
            
        Returns:
            統合解析結果
        """
        # 1. テキスト前処理・特徴抽出
        text_features = self._extract_text_features(text)
        
        # 2. 適切なハンドラーの選択
        selected_handlers = self.router.route(text_features, analysis_mode)
        
        # 3. 並列解析実行
        analysis_results = self._execute_parallel_analysis(text, selected_handlers)
        
        # 4. 結果統合・競合解決
        merged_result = self.merger.merge(analysis_results)
        
        # 5. 性能記録・最適化
        self.performance_monitor.record(text, selected_handlers, merged_result)
        
        return merged_result
    
    def _extract_text_features(self, text: str) -> Dict[str, Any]:
        """テキスト特徴の高速抽出"""
        features = {
            'has_question_mark': '?' in text,
            'starts_with_wh': text.lower().split()[0] in ['what', 'who', 'where', 'when', 'why', 'how'] if text.split() else False,
            'has_relative_pronouns': any(word in text.lower() for word in ['who', 'which', 'that']),
            'has_auxiliary_inversion': self._detect_auxiliary_inversion(text),
            'has_passive_markers': 'by' in text.lower() or any(word in text.lower() for word in ['was', 'were', 'is', 'are']),
            'has_modal_verbs': any(word in text.lower().split() for word in ['can', 'will', 'should', 'must', 'may', 'might']),
            'has_conditional_markers': any(word in text.lower() for word in ['if', 'unless', 'provided', 'assuming']),
            'text_length': len(text),
            'word_count': len(text.split()),
            'complexity_score': self._calculate_complexity_score(text)
        }
        return features
    
    def _execute_parallel_analysis(self, text: str, handler_names: List[str]) -> Dict[str, Any]:
        """並列解析実行（将来的にmultiprocessing対応）"""
        results = {}
        
        for handler_name in handler_names:
            try:
                handler = self.registry.get_handler(handler_name)
                result = handler.process(text)
                results[handler_name] = result
            except Exception as e:
                results[handler_name] = {
                    'success': False,
                    'error': str(e),
                    'handler': handler_name
                }
        
        return results
```

### 2. HandlerRegistry (ハンドラー登録システム)

```python
class HandlerRegistry:
    """
    ハンドラー動的登録・管理システム
    
    機能:
    - migration_cleanハンドラーの自動登録
    - カスタムハンドラーの動的追加
    - ハンドラー能力の管理
    - 負荷分散・フェイルオーバー
    """
    
    def __init__(self):
        self.handlers = {}  # handler_name -> handler_instance
        self.capabilities = {}  # handler_name -> capabilities
        self.performance_stats = {}  # handler_name -> performance_data
        self.fallback_handlers = {}  # primary -> fallback mapping
    
    def register_handler(self, 
                        name: str, 
                        handler_class: type, 
                        capabilities: List[str],
                        priority: int = 1,
                        config_path: str = None):
        """ハンドラーの動的登録"""
        
        # ハンドラーインスタンス作成
        if config_path:
            handler_instance = handler_class(config_path=config_path)
        else:
            handler_instance = handler_class()
        
        # 登録
        self.handlers[name] = handler_instance
        self.capabilities[name] = {
            'features': capabilities,
            'priority': priority,
            'performance': {'avg_confidence': 0.0, 'avg_time': 0.0},
            'status': 'active'
        }
        
        print(f"✅ ハンドラー登録完了: {name} (機能: {capabilities})")
    
    def auto_register_migration_clean(self):
        """migration_cleanハンドラーの自動登録"""
        migration_clean_handlers = [
            ('question', QuestionHandlerClean, ['interrogative', 'wh_question', 'yes_no_question'], 1),
            ('relative_clause', RelativeClauseHandlerClean, ['relative_pronouns', 'subordination'], 2),
            ('passive_voice', PassiveVoiceHandlerClean, ['passive_transformation', 'by_phrase'], 2),
            ('modal', ModalHandlerClean, ['modal_verbs', 'possibility', 'obligation'], 2),
            ('conditional', ConditionalHandlerClean, ['if_clauses', 'conditional_logic'], 2),
            ('basic_five', BasicFivePatternHandlerClean, ['sentence_patterns', 'core_grammar'], 3),
            ('infinitive', InfinitiveHandlerClean, ['to_infinitive', 'complement'], 3),
            ('noun_clause', NounClauseHandlerClean, ['that_clauses', 'embedded_clauses'], 3),
            ('imperative', ImperativeHandlerClean, ['commands', 'directives'], 3),
            ('metaphorical', MetaphoricalHandlerClean, ['figurative_language', 'comparisons'], 4),
            ('adverb', AdverbHandlerClean, ['adverbial_phrases', 'modification'], 4),
            ('omitted_relative', OmittedRelativePronounHandlerClean, ['ellipsis', 'zero_relatives'], 4),
            ('relative_adverb', RelativeAdverbHandlerClean, ['where_when_why', 'adverbial_relatives'], 4)
        ]
        
        for name, handler_class, capabilities, priority in migration_clean_handlers:
            self.register_handler(name, handler_class, capabilities, priority)
    
    def get_suitable_handlers(self, text_features: Dict[str, Any]) -> List[str]:
        """テキスト特徴に基づく適切なハンドラー選択"""
        suitable = []
        
        # 機能マッチングロジック
        if text_features.get('has_question_mark') or text_features.get('starts_with_wh'):
            suitable.append('question')
        
        if text_features.get('has_relative_pronouns'):
            suitable.extend(['relative_clause', 'omitted_relative'])
        
        if text_features.get('has_passive_markers'):
            suitable.append('passive_voice')
        
        if text_features.get('has_modal_verbs'):
            suitable.append('modal')
        
        if text_features.get('has_conditional_markers'):
            suitable.append('conditional')
        
        # 常に実行される基本ハンドラー
        suitable.extend(['basic_five', 'adverb'])
        
        # 優先度でソート
        suitable.sort(key=lambda x: self.capabilities.get(x, {}).get('priority', 99))
        
        return suitable
```

### 3. TextAnalysisRouter (テキスト解析ルーター)

```python
class TextAnalysisRouter:
    """
    テキスト解析ルーティングシステム
    
    機能:
    - テキスト特徴に基づくハンドラー選択
    - 解析モードに応じた最適化
    - 動的優先度調整
    """
    
    def __init__(self):
        self.routing_rules = self._load_routing_rules()
        self.performance_history = {}
    
    def route(self, text_features: Dict[str, Any], analysis_mode: str = "comprehensive") -> List[str]:
        """
        ルーティング実行
        
        Args:
            text_features: テキスト特徴辞書
            analysis_mode: "comprehensive" | "fast" | "specialized"
            
        Returns:
            実行すべきハンドラー名のリスト
        """
        if analysis_mode == "fast":
            return self._fast_route(text_features)
        elif analysis_mode == "specialized":
            return self._specialized_route(text_features)
        else:  # comprehensive
            return self._comprehensive_route(text_features)
    
    def _comprehensive_route(self, text_features: Dict[str, Any]) -> List[str]:
        """包括的解析モード - 全ての関連ハンドラーを実行"""
        selected = []
        
        # 高優先度ハンドラー（確実に実行）
        if text_features.get('has_question_mark') or text_features.get('starts_with_wh'):
            selected.append('question')
        
        # 中優先度ハンドラー（条件付き実行）
        if text_features.get('has_relative_pronouns'):
            selected.extend(['relative_clause', 'omitted_relative'])
        
        if text_features.get('has_passive_markers'):
            selected.append('passive_voice')
        
        # 基本ハンドラー（常時実行）
        selected.extend(['basic_five', 'adverb'])
        
        # 文の複雑さに応じて追加
        if text_features.get('complexity_score', 0) > 3:
            selected.extend(['noun_clause', 'infinitive', 'metaphorical'])
        
        return list(set(selected))  # 重複除去
    
    def _fast_route(self, text_features: Dict[str, Any]) -> List[str]:
        """高速解析モード - 最小限のハンドラーのみ"""
        if text_features.get('has_question_mark'):
            return ['question']
        elif text_features.get('has_relative_pronouns'):
            return ['relative_clause']
        else:
            return ['basic_five']
    
    def _specialized_route(self, text_features: Dict[str, Any]) -> List[str]:
        """専門解析モード - 特定分野に特化"""
        specialized = []
        
        # 疑問文特化
        if text_features.get('has_question_mark') or text_features.get('starts_with_wh'):
            specialized.extend(['question', 'relative_adverb'])
        
        # 関係節特化
        if text_features.get('has_relative_pronouns'):
            specialized.extend(['relative_clause', 'omitted_relative', 'relative_adverb'])
        
        # フォールバック
        if not specialized:
            specialized = ['basic_five']
        
        return specialized
```

### 4. ResultMerger (結果統合システム)

```python
class ResultMerger:
    """
    複数ハンドラー結果の統合・競合解決システム
    
    機能:
    - 重複スロットの競合解決
    - 信頼度に基づく結果選択
    - 補完的情報の統合
    """
    
    def merge(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """結果統合処理"""
        if not analysis_results:
            return {'success': False, 'error': 'No analysis results'}
        
        # 成功した解析結果のみ抽出
        successful_results = {
            name: result for name, result in analysis_results.items() 
            if result.get('success', False)
        }
        
        if not successful_results:
            return {'success': False, 'error': 'All analyses failed'}
        
        # 統合結果の初期化
        merged = {
            'success': True,
            'original_text': '',
            'merged_slots': {},
            'sub_slots': {},
            'confidence_scores': {},
            'handler_contributions': {},
            'overall_confidence': 0.0,
            'analysis_summary': {}
        }
        
        # 1. 基本情報の統合
        merged['original_text'] = list(successful_results.values())[0].get('original_text', '')
        
        # 2. スロット統合（競合解決付き）
        merged['merged_slots'] = self._merge_slots(successful_results)
        
        # 3. サブスロット統合
        merged['sub_slots'] = self._merge_sub_slots(successful_results)
        
        # 4. 信頼度統合
        merged['confidence_scores'] = self._merge_confidences(successful_results)
        merged['overall_confidence'] = self._calculate_overall_confidence(successful_results)
        
        # 5. 解析サマリー生成
        merged['analysis_summary'] = self._generate_analysis_summary(successful_results)
        
        return merged
    
    def _merge_slots(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """スロット統合（競合解決付き）"""
        all_slots = {}
        slot_sources = {}  # どのハンドラーからのスロットか記録
        
        # 全ハンドラーからスロットを収集
        for handler_name, result in results.items():
            slots = result.get('slots', {})
            confidence = result.get('confidence', 0.0)
            
            for slot_key, slot_value in slots.items():
                if slot_key not in all_slots:
                    all_slots[slot_key] = slot_value
                    slot_sources[slot_key] = [(handler_name, confidence)]
                else:
                    # 競合が発生した場合
                    slot_sources[slot_key].append((handler_name, confidence))
                    
                    # 信頼度による競合解決
                    current_confidence = max(source[1] for source in slot_sources[slot_key][:-1])
                    if confidence > current_confidence:
                        all_slots[slot_key] = slot_value
        
        return all_slots
    
    def _calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """全体信頼度の計算"""
        confidences = [result.get('confidence', 0.0) for result in results.values()]
        if not confidences:
            return 0.0
        
        # 重み付き平均（ハンドラー数で正規化）
        weighted_sum = sum(confidences)
        return weighted_sum / len(confidences)
```

---

## 📋 実装優先順位

### Phase 1: 基盤構築 (即座に実装)
1. **UniversalGrammarController骨格**
2. **HandlerRegistry自動登録機能**
3. **基本的なTextAnalysisRouter**
4. **簡単なResultMerger**

### Phase 2: 機能強化 (短期)
1. **並列処理対応**
2. **高度な競合解決**
3. **性能監視機能**
4. **設定ファイル統一**

### Phase 3: 高度化 (中期)
1. **AI学習機能統合**
2. **動的最適化**
3. **多言語対応基盤**
4. **クラウド対応**

---

## 🎯 次回チャット開始時の実装手順

1. **UniversalGrammarController.py作成**
2. **migration_cleanハンドラーのインポート統合**
3. **基本的な統一解析機能の実装**
4. **簡単なテストケースでの動作確認**

**🚀 この設計図に従って、次回チャットで即座に真の汎用的中央管理システムの実装に着手可能です！**
