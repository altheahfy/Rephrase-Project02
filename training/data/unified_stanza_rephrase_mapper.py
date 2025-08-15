#!/usr/bin/env python3
"""
Unified Stanza-Rephrase Mapper v1.0
===================================

統合型文法分解エンジン - ハイブリッド方式
- 15個別エンジンの知識を統合
- 選択問題を排除（全ハンドラー同時実行）
- Stanza dependency parsing → Rephrase slot mapping

作成日: 2025年8月15日
Phase 0: 基盤構築
"""

import stanza
from typing import Dict, List, Optional, Any, Tuple
import json
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RephraseSlot:
    """Rephraseスロット表現"""
    slot_name: str
    content: str
    sub_slots: Dict[str, Any] = None
    confidence: float = 1.0
    source_handler: str = ""

class UnifiedStanzaRephraseMapper:
    """
    統合型Stanza→Rephraseマッパー
    
    核心思想:
    - 全文法ハンドラーが同時実行（選択問題排除）
    - 単一Stanza解析結果の多角的分析
    - 個別エンジンの実装知識継承
    """
    
    def __init__(self, 
                 language='en', 
                 enable_gpu=False,
                 log_level='INFO'):
        """
        統合マッパー初期化
        
        Args:
            language: 処理言語（デフォルト: 'en'）
            enable_gpu: GPU使用フラグ
            log_level: ログレベル
        """
        self.language = language
        self.enable_gpu = enable_gpu
        
        # ログ設定
        self._setup_logging(log_level)
        
        # Stanzaパイプライン初期化
        self.nlp = None
        self._initialize_stanza_pipeline()
        
        # 統計情報
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.handler_success_count = {}
        
        # 段階的ハンドラー管理（Phase別追加）
        self.active_handlers = []
        
        self.logger.info("🚀 Unified Stanza-Rephrase Mapper v1.0 初期化完了")
    
    def _setup_logging(self, level: str):
        """ログ設定"""
        self.logger = logging.getLogger(f"{__name__}.UnifiedMapper")
        self.logger.setLevel(getattr(logging, level.upper()))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _initialize_stanza_pipeline(self):
        """Stanza NLPパイプライン初期化"""
        try:
            self.logger.info("🔧 Stanza pipeline 初期化中...")
            
            # 基本的なパイプライン構成
            processors = 'tokenize,pos,lemma,depparse'
            
            self.nlp = stanza.Pipeline(
                lang=self.language,
                processors=processors,
                download_method=None,  # 事前ダウンロード済みを想定
                use_gpu=self.enable_gpu,
                verbose=False
            )
            
            self.logger.info("✅ Stanza pipeline 初期化成功")
            
            # 動作確認
            test_result = self.nlp("Hello world.")
            self.logger.info(f"🧪 Pipeline 動作確認: {len(test_result.sentences)} sentences processed")
            
        except Exception as e:
            self.logger.error(f"❌ Stanza pipeline 初期化失敗: {e}")
            self.logger.error("💡 解決方法: python -c 'import stanza; stanza.download(\"en\")'")
            raise RuntimeError(f"Stanza initialization failed: {e}")
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        統合処理メインエントリポイント
        
        Args:
            sentence: 処理対象文
            
        Returns:
            Dict: Rephrase形式処理結果
        """
        start_time = datetime.now()
        self.processing_count += 1
        
        try:
            self.logger.debug(f"🔍 Processing: {sentence}")
            
            # Phase 1: Stanza解析
            doc = self._analyze_with_stanza(sentence)
            if not doc or not doc.sentences:
                self.logger.warning(f"⚠️ Stanza解析失敗: {sentence}")
                return self._create_empty_result(sentence)
            
            # Phase 2: 統合処理（全ハンドラー同時実行）
            result = self._unified_mapping(sentence, doc)
            
            # Phase 3: 後処理・検証
            result = self._post_process_result(result, sentence)
            
            # 処理時間記録
            processing_time = (datetime.now() - start_time).total_seconds()
            self.total_processing_time += processing_time
            
            result['meta'] = {
                'processing_time': processing_time,
                'sentence_id': self.processing_count,
                'active_handlers': len(self.active_handlers),
                'stanza_info': {
                    'sentences': len(doc.sentences),
                    'tokens': len(doc.sentences[0].words) if doc.sentences else 0
                }
            }
            
            self.logger.info(f"✅ Processing完了 ({processing_time:.3f}s): {len(result.get('slots', {}))} slots detected")
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"❌ Processing error: {e}")
            
            return {
                'sentence': sentence,
                'slots': {},
                'error': str(e),
                'meta': {
                    'processing_time': processing_time,
                    'sentence_id': self.processing_count,
                    'error_occurred': True
                }
            }
    
    def _analyze_with_stanza(self, sentence: str):
        """Stanza解析実行"""
        try:
            doc = self.nlp(sentence)
            return doc
        except Exception as e:
            self.logger.error(f"❌ Stanza analysis failed: {e}")
            return None
    
    def _unified_mapping(self, sentence: str, doc) -> Dict[str, Any]:
        """
        統合マッピング処理
        
        全アクティブハンドラーが同時実行
        各ハンドラーは独立してStanza解析結果を処理
        """
        result = {
            'sentence': sentence,
            'slots': {},
            'sub_slots': {},
            'grammar_info': {
                'detected_patterns': [],
                'handler_contributions': {}
            }
        }
        
        # メイン文（最初のsentence）を対象とする
        main_sentence = doc.sentences[0] if doc.sentences else None
        if not main_sentence:
            return result
        
        self.logger.debug(f"🔧 Unified mapping開始: {len(self.active_handlers)} handlers active")
        
        # 全アクティブハンドラーの同時実行
        for handler_name in self.active_handlers:
            try:
                self.logger.debug(f"🎯 Handler実行: {handler_name}")
                handler_method = getattr(self, f'_handle_{handler_name}')
                handler_result = handler_method(main_sentence, result.copy())
                
                # ハンドラー結果をマージ
                if handler_result:
                    result = self._merge_handler_results(result, handler_result, handler_name)
                    
                    # 成功カウント
                    self.handler_success_count[handler_name] = \
                        self.handler_success_count.get(handler_name, 0) + 1
                        
            except Exception as e:
                self.logger.warning(f"⚠️ Handler error ({handler_name}): {e}")
                continue
        
        return result
    
    def _merge_handler_results(self, base_result: Dict, handler_result: Dict, handler_name: str) -> Dict:
        """
        ハンドラー結果をベース結果にマージ
        
        Args:
            base_result: ベース結果
            handler_result: ハンドラー処理結果  
            handler_name: ハンドラー名
        """
        # スロット情報マージ
        if 'slots' in handler_result:
            for slot_name, slot_data in handler_result['slots'].items():
                if slot_name not in base_result['slots']:
                    base_result['slots'][slot_name] = slot_data
                else:
                    # 競合解決（単純上書き - 文字列の場合も対応）
                    base_result['slots'][slot_name] = slot_data
        
        # サブスロット情報マージ
        if 'sub_slots' in handler_result:
            for sub_slot_name, sub_slot_data in handler_result['sub_slots'].items():
                base_result['sub_slots'][sub_slot_name] = sub_slot_data
        
        # 文法情報記録
        if 'grammar_info' in handler_result:
            grammar_info = handler_result['grammar_info']
            base_result['grammar_info']['handler_contributions'][handler_name] = grammar_info
            
            # 検出パターン追加
            if 'patterns' in grammar_info:
                base_result['grammar_info']['detected_patterns'].extend(grammar_info['patterns'])
        
        return base_result
    
    def _post_process_result(self, result: Dict, sentence: str) -> Dict:
        """後処理・結果検証"""
        # 重複パターン除去
        if 'detected_patterns' in result.get('grammar_info', {}):
            result['grammar_info']['detected_patterns'] = \
                list(set(result['grammar_info']['detected_patterns']))
        
        # スロット整合性チェック（今後実装）
        # TODO: rephrase_slot_validator.py との連携
        
        return result
    
    def _create_empty_result(self, sentence: str) -> Dict[str, Any]:
        """空結果の作成"""
        return {
            'sentence': sentence,
            'slots': {},
            'sub_slots': {},
            'grammar_info': {
                'detected_patterns': [],
                'handler_contributions': {}
            },
            'meta': {
                'processing_time': 0.0,
                'sentence_id': self.processing_count,
                'empty_result': True
            }
        }
    
    # =============================================================================
    # ハンドラー管理（Phase別機能追加用）
    # =============================================================================
    
    def add_handler(self, handler_name: str):
        """ハンドラーを追加（Phase別開発用）"""
        if handler_name not in self.active_handlers:
            self.active_handlers.append(handler_name)
            self.logger.info(f"➕ Handler追加: {handler_name}")
        else:
            self.logger.warning(f"⚠️ Handler already active: {handler_name}")
    
    def remove_handler(self, handler_name: str):
        """ハンドラーを削除"""
        if handler_name in self.active_handlers:
            self.active_handlers.remove(handler_name)
            self.logger.info(f"➖ Handler削除: {handler_name}")
    
    def list_active_handlers(self) -> List[str]:
        """アクティブハンドラー一覧"""
        return self.active_handlers.copy()
    
    # =============================================================================
    # 統計・デバッグ情報
    # =============================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """処理統計情報取得"""
        avg_processing_time = (
            self.total_processing_time / self.processing_count 
            if self.processing_count > 0 else 0.0
        )
        
        return {
            'processing_count': self.processing_count,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': avg_processing_time,
            'active_handlers': self.active_handlers.copy(),
            'handler_success_count': self.handler_success_count.copy(),
            'stanza_pipeline_status': 'active' if self.nlp else 'inactive'
        }
    
    def reset_stats(self):
        """統計情報リセット"""
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.handler_success_count.clear()
        self.logger.info("📊 Statistics reset")
    
    # =============================================================================
    # 文法ハンドラー実装（Phase 1+: 段階的追加）
    # =============================================================================
    
    def _handle_relative_clause(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        関係節ハンドラー（Phase 1実装）
        
        simple_relative_engine.py の機能を統合システムに移植
        Stanza dependency parsing による直接的な関係節検出・分解
        
        Args:
            sentence: Stanza解析済みsentence object
            base_result: ベース結果（コピー）
            
        Returns:
            Dict: 関係節分解結果 or None
        """
        try:
            self.logger.debug("🔍 関係節ハンドラー実行中...")
            
            # 関係節存在チェック
            if not self._has_relative_clause(sentence):
                self.logger.debug("  関係節なし - スキップ")
                return None
            
            self.logger.debug("  ✅ 関係節検出")
            return self._process_relative_clause_structure(sentence, base_result)
            
        except Exception as e:
            self.logger.warning(f"⚠️ 関係節ハンドラーエラー: {e}")
            return None
    
    def _has_relative_clause(self, sentence) -> bool:
        """関係節を含むかチェック"""
        return any(w.deprel in ['acl:relcl', 'acl'] for w in sentence.words)
    
    def _process_relative_clause_structure(self, sentence, base_result: Dict) -> Dict:
        """関係節構造の分解処理"""
        
        # === 1. 要素特定 ===
        # 関係節動詞（関係節の核）
        rel_verb = self._find_word_by_deprel(sentence, 'acl:relcl')
        if not rel_verb:
            rel_verb = self._find_word_by_deprel(sentence, 'acl')
        if not rel_verb:
            return base_result
        
        # 先行詞（関係節動詞の頭）
        antecedent = self._find_word_by_id(sentence, rel_verb.head)
        if not antecedent:
            return base_result
        
        self.logger.debug(f"  先行詞: {antecedent.text}, 関係動詞: {rel_verb.text}")
        
        # === 2. 関係代名詞/関係副詞特定 ===
        rel_pronoun, rel_type = self._identify_relative_pronoun(sentence, rel_verb)
        
        # === 3. 関係節内要素特定 ===
        rel_subject = None
        if rel_type in ['obj', 'advmod']:  # 目的語・関係副詞の場合は別途主語検索
            rel_subject = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
        
        # 所有格関係代名詞の特別処理
        possessed_noun = None
        if rel_type == 'poss':
            possessed_noun = self._find_word_by_id(sentence, rel_pronoun.head)
        
        self.logger.debug(f"  関係代名詞: {rel_pronoun.text if rel_pronoun else 'None'} ({rel_type})")
        if rel_subject:
            self.logger.debug(f"  関係節主語: {rel_subject.text}")
        if possessed_noun:
            self.logger.debug(f"  所有される名詞: {possessed_noun.text}")
        
        # === 4. 先行詞句構築 ===
        noun_phrase = self._build_antecedent_phrase(sentence, antecedent, rel_pronoun, possessed_noun)
        self.logger.debug(f"  構築先行詞句: '{noun_phrase}'")
        
        # === 5. Rephraseスロット分解 ===
        result = base_result.copy()
        rephrase_slots = self._generate_relative_clause_slots(
            rel_type, noun_phrase, rel_subject, rel_verb, sentence
        )
        
        # 結果マージ
        if 'slots' not in result:
            result['slots'] = {}
        if 'sub_slots' not in result:
            result['sub_slots'] = {}
        
        result['slots'].update(rephrase_slots.get('slots', {}))
        result['sub_slots'].update(rephrase_slots.get('sub_slots', {}))
        
        # 文法情報記録
        result['grammar_info'] = {
            'patterns': ['relative_clause'],
            'rel_type': rel_type,
            'antecedent': antecedent.text,
            'rel_pronoun': rel_pronoun.text if rel_pronoun else None,
            'rel_verb': rel_verb.text
        }
        
        self.logger.debug(f"  ✅ 関係節処理完了: {len(rephrase_slots.get('slots', {}))} main slots, {len(rephrase_slots.get('sub_slots', {}))} sub slots")
        return result
    
    def _identify_relative_pronoun(self, sentence, rel_verb) -> Tuple[Optional[Any], str]:
        """関係代名詞/関係副詞の特定と分類"""
        
        # 1. 関係副詞検出（最優先）
        advmod_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'advmod')
        if advmod_word and advmod_word.text.lower() in ['where', 'when', 'why', 'how']:
            return advmod_word, 'advmod'
        
        # 2. 所有格関係代名詞検出
        for word in sentence.words:
            if word.text.lower() == 'whose' and word.deprel == 'nmod:poss':
                return word, 'poss'
        
        # 3. 目的語関係代名詞
        obj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obj')
        if obj_pronoun:
            return obj_pronoun, 'obj'
        
        # 4. 主語関係代名詞
        subj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
        if subj_pronoun:
            return subj_pronoun, 'nsubj'
        
        return None, 'unknown'
    
    def _build_antecedent_phrase(self, sentence, antecedent, rel_pronoun, possessed_noun=None) -> str:
        """先行詞句構築（修飾語含む）- 関係節全体を含む完全な句を構築"""
        if not antecedent:
            return rel_pronoun.text if rel_pronoun else ""
        
        # 先行詞の修飾語収集
        modifiers = []
        for word in sentence.words:
            if word.head == antecedent.id and word.deprel in ['det', 'amod', 'compound']:
                modifiers.append(word)
        
        # 関係節内の全単語を収集（関係節動詞とその依存語）
        rel_clause_words = []
        if rel_pronoun:
            # 関係代名詞を追加
            rel_clause_words.append(rel_pronoun)
            
            # 関係節動詞を特定
            rel_verb = None
            for word in sentence.words:
                if (word.deprel in ['acl:relcl', 'acl'] and 
                    word.head == antecedent.id):
                    rel_verb = word
                    break
            
            if rel_verb:
                # 関係節動詞を追加
                rel_clause_words.append(rel_verb)
                
                # 関係節動詞の依存語を追加
                for word in sentence.words:
                    if (word.head == rel_verb.id and 
                        word.id != rel_pronoun.id):  # 関係代名詞は既に追加済み
                        rel_clause_words.append(word)
        
        # 語順構築
        phrase_words = modifiers + [antecedent] + rel_clause_words
        
        # 所有格の特別処理
        if possessed_noun and rel_pronoun:
            if possessed_noun not in phrase_words:
                phrase_words.append(possessed_noun)
        
        # ID順ソート（語順保持）
        phrase_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _generate_relative_clause_slots(self, rel_type: str, noun_phrase: str, rel_subject, rel_verb, sentence) -> Dict:
        """関係節タイプ別スロット生成"""
        
        slots = {}
        sub_slots = {}
        
        if rel_type == 'obj':
            # 目的語関係代名詞: "The book that he bought"
            slots["O1"] = ""  # 上位スロット空
            sub_slots["sub-o1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj':
            # 主語関係代名詞: "The man who runs"
            slots["S"] = ""  # 上位スロット空
            sub_slots["sub-s"] = noun_phrase
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'poss':
            # 所有格関係代名詞: "The man whose car is red"
            slots["S"] = ""  # 上位スロット空
            sub_slots["sub-s"] = noun_phrase
            
            # be動詞確認
            cop_verb = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'cop')
            if cop_verb:
                if rel_verb.pos == 'ADJ':
                    sub_slots["sub-aux"] = cop_verb.text
                    sub_slots["sub-c1"] = rel_verb.text
                else:
                    sub_slots["sub-aux"] = cop_verb.text
                    sub_slots["sub-v"] = rel_verb.text
            else:
                sub_slots["sub-v"] = rel_verb.text
                
        elif rel_type == 'advmod':
            # 関係副詞: "The place where he lives"
            slots["M3"] = ""  # 上位スロット空（副詞句扱い）
            sub_slots["sub-m3"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
        else:
            # デフォルト（目的語扱い）
            slots["O1"] = ""
            sub_slots["sub-o1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
        
        return {'slots': slots, 'sub_slots': sub_slots}
    
    # === Stanza解析ヘルパーメソッド ===
    
    def _find_word_by_deprel(self, sentence, deprel: str):
        """依存関係で語を検索"""
        return next((w for w in sentence.words if w.deprel == deprel), None)
    
    def _find_word_by_id(self, sentence, word_id: int):
        """IDで語を検索"""
        return next((w for w in sentence.words if w.id == word_id), None)
    
    def _find_word_by_head_and_deprel(self, sentence, head_id: int, deprel: str):
        """頭IDと依存関係で語を検索"""
        return next((w for w in sentence.words if w.head == head_id and w.deprel == deprel), None)

# =============================================================================
# Phase 0 テスト用 基本テストハーネス
# =============================================================================

def test_phase0_basic():
    """Phase 0 基本動作確認テスト"""
    print("🧪 Phase 0 基本テスト開始...")
    
    try:
        # 初期化テスト
        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        print("✅ 初期化成功")
        
        # 基本処理テスト
        test_sentence = "The car is red."
        result = mapper.process(test_sentence)
        
        print(f"✅ 基本処理成功: {result['sentence']}")
        print(f"📊 処理時間: {result['meta']['processing_time']:.3f}s")
        print(f"🔧 Stanza情報: {result['meta']['stanza_info']}")
        
        # 統計確認
        stats = mapper.get_stats()
        print(f"📈 処理統計: {stats}")
        
        print("🎉 Phase 0 基本テスト完了！")
        return True
        
    except Exception as e:
        print(f"❌ Phase 0 テスト失敗: {e}")
        return False

# =============================================================================
# Phase 1 テスト用 関係節テストハーネス
# =============================================================================

def test_phase1_relative_clause():
    """Phase 1 関係節ハンドラーテスト"""
    print("🧪 Phase 1 関係節テスト開始...")
    
    try:
        # 初期化
        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        
        # Phase 1 ハンドラー追加
        mapper.add_handler('relative_clause')
        print("✅ 関係節ハンドラー追加完了")
        
        # 重要テストケース
        test_cases = [
            ("The car which we saw was red.", "目的語関係代名詞"),
            ("The man who runs fast is strong.", "主語関係代名詞"),
            ("The man whose car is red lives here.", "所有格関係代名詞"),
            ("The place where he lives is nice.", "関係副詞where")
        ]
        
        success_count = 0
        for i, (test_sentence, pattern_type) in enumerate(test_cases, 1):
            print(f"\n📖 テスト{i}: '{test_sentence}' ({pattern_type})")
            print("-" * 60)
            
            try:
                result = mapper.process(test_sentence)
                
                print("📊 処理結果:")
                print(f"  メインスロット: {result.get('slots', {})}")
                print(f"  サブスロット: {result.get('sub_slots', {})}")
                print(f"  文法情報: {result.get('grammar_info', {})}")
                print(f"  処理時間: {result['meta']['processing_time']:.3f}s")
                
                # 第1テストケースの特別チェック
                if i == 1:  # "The car which we saw was red."
                    slots = result.get('slots', {})
                    sub_slots = result.get('sub_slots', {})
                    
                    print(f"\n🎯 重要チェック:")
                    expected_sub_o1 = "The car which we saw"
                    actual_sub_o1 = sub_slots.get('sub-o1', '')
                    print(f"  期待 sub-o1: '{expected_sub_o1}'")
                    print(f"  実際 sub-o1: '{actual_sub_o1}'")
                    
                    if expected_sub_o1.lower() in actual_sub_o1.lower():
                        print("  ✅ 基本要求達成！")
                        success_count += 1
                    else:
                        print("  ❌ 基本要求未達成")
                else:
                    success_count += 1
                    
            except Exception as e:
                print(f"❌ テスト{i}エラー: {e}")
        
        # 統計確認
        stats = mapper.get_stats()
        print(f"\n📈 Phase 1 統計:")
        print(f"  処理数: {stats['processing_count']}")
        print(f"  平均処理時間: {stats['average_processing_time']:.3f}s")
        print(f"  ハンドラー成功数: {stats['handler_success_count']}")
        
        print(f"\n🎉 Phase 1 テスト完了! 成功: {success_count}/{len(test_cases)}")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"❌ Phase 1 テスト失敗: {e}")
        return False

if __name__ == "__main__":
    # Phase 0 基本テスト
    if test_phase0_basic():
        print("\n" + "="*60)
        # Phase 1 関係節テスト
        test_phase1_relative_clause()
    else:
        print("❌ Phase 0失敗のため Phase 1をスキップ")
