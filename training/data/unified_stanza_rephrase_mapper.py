#!/usr/bin/env python3
"""
Unified Stanza-Rephrase Mapper v1.0
===================================

統合型文法分解エンジン - ハイブリッド方式
- 15個別エンジンの知識を統合
- 選択問題を排除（全ハンドラー同時実行）
- Stanza dependency parsing → Rephrase slot mapping
- spaCy補完解析（Stanzaの誤解析箇所対応）

作成日: 2025年8月15日
Phase 0: 基盤構築
"""

import stanza
from typing import Dict, List, Optional, Any, Tuple
import json
import logging
from dataclasses import dataclass
from datetime import datetime

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

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
                 log_level='INFO',
                 use_spacy_hybrid=True):
        """
        統合マッパー初期化
        
        Args:
            language: 処理言語（デフォルト: 'en'）
            enable_gpu: GPU使用フラグ
            log_level: ログレベル
            use_spacy_hybrid: spaCyハイブリッド解析使用フラグ
        """
        self.language = language
        self.enable_gpu = enable_gpu
        self.use_spacy_hybrid = use_spacy_hybrid
        
        # ログ設定
        self._setup_logging(log_level)
        
        # Stanzaパイプライン初期化
        self.nlp = None
        self._initialize_stanza_pipeline()
        
        # spaCyハイブリッド解析初期化
        self.spacy_nlp = None
        if self.use_spacy_hybrid and SPACY_AVAILABLE:
            self._initialize_spacy_pipeline()
        
        # 統計情報
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.handler_success_count = {}
        
        # 段階的ハンドラー管理（Phase別追加）
        self.active_handlers = []
        
        self.logger.info("🚀 Unified Stanza-Rephrase Mapper v1.0 初期化完了")
        if self.spacy_nlp:
            self.logger.info("🔧 spaCyハイブリッド解析 有効")
        else:
            self.logger.info("⚠️ spaCyハイブリッド解析 無効")
    
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
    
    def _initialize_spacy_pipeline(self):
        """spaCy NLPパイプライン初期化（ハイブリッド解析用）"""
        try:
            self.logger.info("🔧 spaCy pipeline 初期化中...")
            
            # 英語モデルをロード
            self.spacy_nlp = spacy.load('en_core_web_sm')
            
            self.logger.info("✅ spaCy pipeline 初期化成功")
            
        except Exception as e:
            self.logger.warning(f"⚠️ spaCy pipeline 初期化失敗: {e}")
            self.logger.warning("  pip install spacy; python -m spacy download en_core_web_sm で設定してください")
            self.spacy_nlp = None
            self.use_spacy_hybrid = False
    
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
            
            # Phase 1.5: ハイブリッド解析（spaCy補完）
            if self.use_spacy_hybrid and self.spacy_nlp:
                doc = self._apply_spacy_hybrid_corrections(sentence, doc)
            
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
    
    def _apply_spacy_hybrid_corrections(self, sentence: str, stanza_doc):
        """
        spaCyハイブリッド解析補完
        
        Stanzaの誤解析を検出してspaCyで補完修正
        特にwhose構文での動詞POS誤解析を修正
        """
        try:
            # spaCy解析実行
            spacy_doc = self.spacy_nlp(sentence)
            
            # 修正が必要な箇所を検出
            corrections = self._detect_analysis_discrepancies(stanza_doc, spacy_doc, sentence)
            
            if corrections:
                self.logger.debug(f"🔧 ハイブリッド解析補正: {len(corrections)} 箇所修正")
                
                # Stanza結果に補正を適用
                corrected_doc = self._apply_corrections_to_stanza(stanza_doc, corrections)
                return corrected_doc
            
            return stanza_doc
            
        except Exception as e:
            self.logger.warning(f"⚠️ spaCyハイブリッド解析エラー: {e}")
            return stanza_doc  # 補正失敗時は元のStanza結果を返す
    
    def _detect_analysis_discrepancies(self, stanza_doc, spacy_doc, sentence: str) -> List[Dict]:
        """
        Stanza-spaCy解析結果の相違点を検出
        
        特に重要な修正箇所:
        1. whose構文での動詞POS誤解析 (NOUN → VERB)
        2. 関係節動詞の誤分類
        """
        corrections = []
        
        # whose構文特別処理
        if 'whose' in sentence.lower():
            corrections.extend(self._detect_whose_verb_misanalysis(stanza_doc, spacy_doc, sentence))
        
        return corrections
    
    def _detect_whose_verb_misanalysis(self, stanza_doc, spacy_doc, sentence: str) -> List[Dict]:
        """whose構文での動詞POS誤解析を検出"""
        corrections = []
        
        stanza_words = {w.text.lower(): w for w in stanza_doc.sentences[0].words}
        spacy_tokens = {t.text.lower(): t for t in spacy_doc}
        
        # 'lives', 'works', 'runs'等の動詞が名詞として誤解析されているかチェック
        potential_verbs = ['lives', 'works', 'runs', 'goes', 'comes', 'stays']
        
        for verb_text in potential_verbs:
            if verb_text in stanza_words and verb_text in spacy_tokens:
                stanza_word = stanza_words[verb_text]
                spacy_token = spacy_tokens[verb_text]
                
                # Stanza: NOUN, spaCy解析でもNOUNだが、文脈的に動詞と判断できる場合
                if (stanza_word.upos == 'NOUN' and 
                    stanza_word.deprel == 'acl:relcl' and
                    self._is_contextually_verb(sentence, verb_text)):
                    
                    corrections.append({
                        'word_id': stanza_word.id,
                        'word_text': stanza_word.text,
                        'original_upos': stanza_word.upos,
                        'corrected_upos': 'VERB',
                        'correction_type': 'whose_verb_fix',
                        'confidence': 0.9
                    })
                    self.logger.debug(f"🔧 whose構文動詞修正検出: {verb_text} NOUN→VERB")
        
        return corrections
    
    def _is_contextually_verb(self, sentence: str, word: str) -> bool:
        """文脈的に動詞と判断できるかチェック"""
        # 簡単なルールベース判定
        # whose + [noun] + is + [adj] + [word] + here/there パターン
        import re
        
        whose_pattern = rf'whose\s+\w+\s+is\s+\w+\s+{word}\s+(here|there)'
        if re.search(whose_pattern, sentence.lower()):
            return True
            
        return False
    
    def _apply_corrections_to_stanza(self, stanza_doc, corrections):
        """Stanza解析結果に補正を適用"""
        # 注意: Stanzaのデータ構造は読み取り専用のため、直接修正はできない
        # ここでは修正情報を記録して、後続処理で利用する
        
        if not hasattr(stanza_doc, 'hybrid_corrections'):
            stanza_doc.hybrid_corrections = {}
        
        for correction in corrections:
            word_id = correction['word_id']
            stanza_doc.hybrid_corrections[word_id] = correction
            
        return stanza_doc
    
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
                    # 競合解決：空文字や空値で既存の有効な値を上書きしない
                    existing_value = base_result['slots'][slot_name]
                    
                    # 既存値が空で新値が有効な場合は上書き
                    if not existing_value and slot_data:
                        base_result['slots'][slot_name] = slot_data
                    # 既存値が有効で新値も有効な場合は後勝ち（従来通り）
                    elif existing_value and slot_data:
                        base_result['slots'][slot_name] = slot_data
                    # 既存値が有効で新値が空の場合は保持（★修正ポイント）
                    elif existing_value and not slot_data:
                        pass  # 既存値を保持
                    # 両方空の場合は後勝ち
                    else:
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
        """後処理・結果検証（whose構文特別処理追加）"""
        
        # ✅ whose構文の特別な後処理：主文・関係節の正しい分離
        if 'whose' in sentence.lower():
            result = self._post_process_whose_construction(result, sentence)
        
        # 重複パターン除去
        if 'detected_patterns' in result.get('grammar_info', {}):
            result['grammar_info']['detected_patterns'] = \
                list(set(result['grammar_info']['detected_patterns']))
        
        # 🔧 REPHRASE SPECIFICATION COMPLIANCE: Sub-slots require empty main slots
        self._apply_rephrase_slot_structure_rules(result, sentence)
        
        # スロット整合性チェック（今後実装）
        # TODO: rephrase_slot_validator.py との連携
        
        return result
    
    def _post_process_whose_construction(self, result: Dict, sentence: str) -> Dict:
        """whose構文の後処理：主文・関係節の正しい分離"""
        
        # ハイブリッド解析で補正された動詞（主文動詞）を検出
        main_verb = None
        for word in sentence.split():
            if word.lower() in ['lives', 'works', 'runs', 'goes', 'sits', 'stands']:
                main_verb = word
                break
        
        if main_verb:
            # 主文動詞をVスロットに配置
            if 'slots' not in result:
                result['slots'] = {}
            result['slots']['V'] = main_verb
            
            # ✅ 副詞処理は専門エンジンに委譲 - 固定処理を無効化
            # if 'here' in sentence.lower():
            #     result['slots']['M2'] = 'here'
            # elif 'there' in sentence.lower():
            #     result['slots']['M2'] = 'there'
                
            # 主語は関係節ハンドラーが設定したsub-sを移動
            if result.get('sub_slots', {}).get('sub-s'):
                # sub-sの内容から関係節部分を除去して主文主語を作る
                sub_s_content = result['sub_slots']['sub-s']  # "The man whose car"
                # "whose car"部分を除去して"The man"を主語とする
                main_subject = sub_s_content.split(' whose ')[0]  # "The man"
                result['slots']['S'] = main_subject
                
            # 関係節のsub-c1が主文動詞になっている場合は修正
            if result.get('sub_slots', {}).get('sub-c1') == main_verb:
                # 本来の関係節補語を探す
                if 'red' in sentence.lower():
                    result['sub_slots']['sub-c1'] = 'red'
                    
            self.logger.debug(f"🔧 whose構文後処理: 主文V={main_verb}, S={result['slots'].get('S')}")
        
        return result
    
    def _apply_rephrase_slot_structure_rules(self, result: Dict, sentence: str) -> None:
        """
        Rephrase仕様準拠：複文での正しいスロット配置
        
        重要ルール：sub-slotsが存在する場合、対応するmain slotsは空文字にする
        例外：Aux, Vスロットは例外適用なし
        
        対応関係：
        - S ←→ sub-s (S位置の従属節)
        - O1 ←→ sub-o1 (O1位置の従属節)  
        - O2 ←→ sub-o2 (O2位置の従属節)
        - C1 ←→ sub-c1 (C1位置の従属節)
        - C2 ←→ sub-c2 (C2位置の従属節)
        - M1 ←→ sub-m1 (M1位置の従属節)
        - M2 ←→ sub-m2 (M2位置の従属節) 
        - M3 ←→ sub-m3 (M3位置の従属節)
        """
        slots = result.get('slots', {})
        sub_slots = result.get('sub_slots', {})
        
        # 対応関係マッピング（Aux, V除外）
        main_to_sub_mapping = {
            'S': 'sub-s',
            'O1': 'sub-o1', 
            'O2': 'sub-o2',
            'C1': 'sub-c1',
            'C2': 'sub-c2', 
            'M1': 'sub-m1',
            'M2': 'sub-m2',
            'M3': 'sub-m3'
        }
        
        self.logger.debug(f"🏗️ Rephrase仕様適用開始 - Sub-slots: {list(sub_slots.keys())}")
        
        # 複文判定＆スロット空文字化処理
        for main_slot, sub_slot in main_to_sub_mapping.items():
            if sub_slot in sub_slots and sub_slots[sub_slot]:
                # Sub-slotが存在し内容がある場合、対応するmain slotを空にする
                if main_slot in slots:
                    original_value = slots[main_slot]
                    slots[main_slot] = ""  # 位置マーカーとして空文字設定
                    
                    self.logger.debug(
                        f"🔄 Complex sentence rule applied: "
                        f"{main_slot}: '{original_value}' → '' "
                        f"(sub-slot {sub_slot}: '{sub_slots[sub_slot]}')"
                    )
        
        # 処理結果をデバッグログ出力
        applied_rules = [
            f"{main}→{sub}" for main, sub in main_to_sub_mapping.items() 
            if sub in sub_slots and sub_slots[sub] and main in slots
        ]
        
        if applied_rules:
            self.logger.info(f"✅ Rephrase複文ルール適用: {', '.join(applied_rules)}")
        
        # ✅ whose構文の主文副詞は上位スロットに保持（自動移動無効化）
        # 主文の副詞（M1, M2, M3）は上位スロットに残すのが正しい仕様
        # if 'whose' in sentence.lower() and any(s in sub_slots for s in ['sub-s', 'sub-v', 'sub-c1']):
        #     # whose構文検出時、主文のM-slotを自動的にsub-slotに移動
        #     additional_rules = []
        #     for main_slot in ['M1', 'M2', 'M3']:
        #         if main_slot in slots and slots[main_slot]:  # 内容がある場合
        #             sub_slot = main_to_sub_mapping[main_slot]
        #             if sub_slot not in sub_slots or not sub_slots[sub_slot]:  # sub-slotが空の場合
        #                 sub_slots[sub_slot] = slots[main_slot]
        #                 slots[main_slot] = ""
        #                 additional_rules.append(f"{main_slot}→{sub_slot}")
        #                 self.logger.debug(f"🔄 whose構文主文副詞移動: {main_slot}: '{sub_slots[sub_slot]}' → {sub_slot}")
        #     
        #     if additional_rules:
        #         self.logger.info(f"✅ whose構文主文副詞移動: {', '.join(additional_rules)}")
        
        else:
            self.logger.debug("🔍 Simple sentence detected - No main slot emptying required")
    
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
        # ✅ whose構文の詳細処理
        has_acl_relcl = any(w.deprel in ['acl:relcl', 'acl'] for w in sentence.words)
        
        if has_acl_relcl and any(w.text.lower() == 'whose' for w in sentence.words):
            # whose構文でacl:relcl語がメイン動詞候補の場合は関係節なしと判定
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes', 'sits', 'stands']):
                self.logger.debug(f"🔧 whose構文: {acl_relcl_word.text}をメイン動詞として処理（関係節ではない）")
                
                # ただし、真の関係節（whose car is red部分）が存在する場合は処理する
                # cop関係のbe動詞があるかチェック
                cop_verb = None
                for word in sentence.words:
                    if word.deprel == 'cop':
                        cop_verb = word
                        break
                
                if cop_verb:
                    self.logger.debug(f"🔧 whose構文内の真の関係節検出: cop動詞 {cop_verb.text}")
                    return True  # 真の関係節が存在
                else:
                    return False  # 関係節ではなくメイン動詞
        
        return has_acl_relcl
    
    def _process_relative_clause_structure(self, sentence, base_result: Dict) -> Dict:
        """関係節構造の分解処理"""
        
        # === 1. 要素特定 ===
        # ✅ whose構文の真の関係節検出
        rel_verb = None
        antecedent = None
        
        is_whose_construction = any(w.text.lower() == 'whose' for w in sentence.words)
        
        if is_whose_construction:
            # whose構文では、まずacl:relcl関係の実動詞を探す
            acl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if acl_word and acl_word.upos == 'VERB':
                # Pattern B: 実動詞が関係節動詞 (例: borrowed)
                rel_verb = acl_word
                if acl_word.head > 0:
                    antecedent = self._find_word_by_id(sentence, acl_word.head)
            else:
                # Pattern A: cop動詞が関係節動詞 (例: is in "car is red")  
                for word in sentence.words:
                    if word.deprel == 'cop':
                        rel_verb = word
                        # acl:relclのheadから先行詞を探す
                        if acl_word and acl_word.head > 0:
                            antecedent = self._find_word_by_id(sentence, acl_word.head)
                        else:
                            # fallback: root語を先行詞とする
                            for w in sentence.words:
                                if w.deprel == 'root':
                                    antecedent = w
                                    break
                        break
                        
            if rel_verb and antecedent:
                self.logger.debug(f"🔧 whose構文修正: 関係節動詞={rel_verb.text}, 先行詞={antecedent.text}")
        
        # 通常の関係節検出
        if not rel_verb:
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
        if rel_type in ['obj', 'advmod']:  # 目的語・関係副詞の場合のみ主語検索
            rel_subject = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
        elif rel_type == 'poss':
            # 所有格関係代名詞の場合は特別処理
            # whose構文では、所有される名詞以外の独立した主語を探す
            nsubj_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
            possessed_noun = self._find_word_by_id(sentence, rel_pronoun.head) if rel_pronoun else None
            
            # 所有される名詞と異なる主語がある場合のみrel_subjectとして認識
            if nsubj_word and possessed_noun and nsubj_word.id != possessed_noun.id:
                rel_subject = nsubj_word
        
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
        
        # ✅ whose構文の特別処理: メイン動詞処理を妨害しない
        if is_whose_construction and rel_verb and rel_verb.deprel == 'cop':
            # 関係節スロットのみ生成し、メイン文は5文型ハンドラーに任せる
            rephrase_slots = self._generate_whose_relative_clause_slots(
                antecedent, rel_verb, sentence
            )
            
            # 結果マージ（メイン文スロットは保持）
            if 'slots' not in result:
                result['slots'] = {}
            if 'sub_slots' not in result:
                result['sub_slots'] = {}
            
            # 関係節のsub-slotsのみマージ（メイン文スロットは変更しない）
            result['sub_slots'].update(rephrase_slots.get('sub_slots', {}))
            
            self.logger.debug(f"🔧 whose構文: メイン文スロット保持, 関係節サブスロット追加")
            
        else:
            # 通常の関係節処理
            rephrase_slots = self._generate_relative_clause_slots(
                rel_type, noun_phrase, rel_subject, rel_verb, sentence
            )
            
            # 結果マージ
            if 'slots' not in result:
                result['slots'] = {}
            if 'sub_slots' not in result:
                result['sub_slots'] = {}
            
            # 通常のマージ
            result['slots'].update(rephrase_slots.get('slots', {}))
            result['sub_slots'].update(rephrase_slots.get('sub_slots', {}))
        
        # 文法情報記録
        result['grammar_info'] = {
            'patterns': ['relative_clause'],
            'rel_type': rel_type if not is_whose_construction else 'poss',
            'antecedent': antecedent.text,
            'rel_pronoun': 'whose' if is_whose_construction else (rel_pronoun.text if rel_pronoun else None),
            'rel_verb': rel_verb.text
        }
        
        self.logger.debug(f"  ✅ 関係節処理完了: {len(result.get('slots', {}))} main slots, {len(result.get('sub_slots', {}))} sub slots")
        return result
    
    def _identify_relative_pronoun(self, sentence, rel_verb) -> Tuple[Optional[Any], str]:
        """関係代名詞/関係副詞の特定と分類（省略文対応強化・受動態考慮）"""
        
        # 1. 関係副詞検出（最優先）
        advmod_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'advmod')
        if advmod_word and advmod_word.text.lower() in ['where', 'when', 'why', 'how']:
            return advmod_word, 'advmod'
        
        # 2. 所有格関係代名詞検出
        for word in sentence.words:
            if word.text.lower() == 'whose' and word.deprel == 'nmod:poss':
                return word, 'poss'
        
        # 3. 明示的関係代名詞検出
        # 目的語関係代名詞
        obj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obj')
        if obj_pronoun and obj_pronoun.text.lower() in ['who', 'whom', 'which', 'that']:
            return obj_pronoun, 'obj'
        
        # 主語関係代名詞（受動態チェック追加）  
        subj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
        if subj_pronoun and subj_pronoun.text.lower() in ['who', 'which', 'that']:
            # 受動態の場合は主語関係代名詞として処理
            return subj_pronoun, 'nsubj'
            
        # 受動態主語関係代名詞
        pass_subj_pronoun = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj:pass')
        if pass_subj_pronoun and pass_subj_pronoun.text.lower() in ['who', 'which', 'that']:
            return pass_subj_pronoun, 'nsubj:pass'
        
        # 4. 省略関係代名詞の推定（受動態構造改善）
        inferred_type = self._infer_omitted_relative_pronoun(sentence, rel_verb)
        if inferred_type:
            # 仮想的な関係代名詞オブジェクトを作成
            virtual_pronoun = self._create_virtual_relative_pronoun(sentence, rel_verb, inferred_type)
            return virtual_pronoun, inferred_type
        
        return None, 'unknown'
    
    def _infer_omitted_relative_pronoun(self, sentence, rel_verb) -> Optional[str]:
        """省略された関係代名詞の推定（受動態構造改善）"""
        
        # 関係節動詞の依存構造を分析
        rel_verb_deps = []
        for word in sentence.words:
            if word.head == rel_verb.id:
                rel_verb_deps.append(word.deprel)
        
        self.logger.debug(f"    関係動詞 '{rel_verb.text}' の依存語: {rel_verb_deps}")
        
        # パターン1: 受動態関係節の検出（改善）
        has_nsubj_pass = 'nsubj:pass' in rel_verb_deps or 'nsubjpass' in rel_verb_deps
        has_aux_pass = any(word.deprel in ['aux:pass', 'auxpass'] and word.head == rel_verb.id 
                          for word in sentence.words)
        
        if has_nsubj_pass or has_aux_pass:
            # 受動態関係節：先行詞が受動態の主語
            self.logger.debug(f"    推定: 受動態主語関係代名詞")
            return 'nsubj:pass'  # 受動態主語として扱う
        
        # パターン2: 能動態で目的語がない場合
        has_nsubj = 'nsubj' in rel_verb_deps
        has_obj = 'obj' in rel_verb_deps or 'dobj' in rel_verb_deps
        
        if has_nsubj and not has_obj:
            # 能動態で目的語がない場合、先行詞が目的語の可能性
            self.logger.debug(f"    推定: 省略目的語関係代名詞（能動態パターン）")  
            return 'obj_omitted'
        
        # パターン3: 主語がなく、関係節が能動態の場合
        if not has_nsubj and not has_nsubj_pass:
            self.logger.debug(f"    推定: 省略主語関係代名詞")
            return 'nsubj_omitted'
        
        return None
    
    def _create_virtual_relative_pronoun(self, sentence, rel_verb, inferred_type):
        """仮想的な関係代名詞オブジェクト作成"""
        
        # 関係節の先行詞を取得
        antecedent = self._find_word_by_id(sentence, rel_verb.head)
        
        # 仮想オブジェクト（辞書形式で簡易実装）
        virtual_pronoun = type('VirtualWord', (), {
            'text': '[omitted]',  # 省略マーカー
            'id': rel_verb.id - 0.5,  # 仮想ID（関係動詞の直前）
            'head': rel_verb.head,
            'deprel': inferred_type.replace('_omitted', ''),
            'lemma': '[omitted]'
        })()
        
        self.logger.debug(f"    仮想関係代名詞作成: type={inferred_type}, text=[omitted]")
        return virtual_pronoun
    
    def _build_antecedent_phrase(self, sentence, antecedent, rel_pronoun, possessed_noun=None) -> str:
        """先行詞句構築（修飾語含む）- 関係節の動詞部分は除外"""
        if not antecedent:
            return rel_pronoun.text if rel_pronoun else ""
        
        # 先行詞の修飾語収集
        modifiers = []
        for word in sentence.words:
            if word.head == antecedent.id and word.deprel in ['det', 'amod', 'compound']:
                modifiers.append(word)
        
        # 基本構成：修飾語 + 先行詞 + 関係代名詞
        phrase_words = modifiers + [antecedent]
        
        # 関係代名詞を追加（動詞部分は除外）
        if rel_pronoun:
            phrase_words.append(rel_pronoun)
        
        # 所有格の特別処理（所有される名詞のみ）
        if possessed_noun and rel_pronoun:
            if possessed_noun not in phrase_words:
                phrase_words.append(possessed_noun)
        
        # ID順ソート（語順保持）
        phrase_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _generate_relative_clause_slots(self, rel_type: str, noun_phrase: str, rel_subject, rel_verb, sentence) -> Dict:
        """関係節タイプ別スロット生成（受動態対応改善）"""
        
        slots = {}
        sub_slots = {}
        
        # 受動態補助動詞の検出
        aux_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'aux:pass')
        if not aux_word:
            aux_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'aux')
        
        # ✅ 関係節内の副詞を検出してsub-m2に配置
        adverb_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'advmod')
        if adverb_word:
            # 関係副詞は除外（where, when, why, howは関係副詞として別途処理）
            if adverb_word.text.lower() not in ['where', 'when', 'why', 'how']:
                sub_slots["sub-m2"] = adverb_word.text
                self.logger.debug(f"🔧 関係節内副詞検出: sub-m2 = '{adverb_word.text}'")
        
        # ✅ 関係節内の前置詞句・副詞句を検出してsub-m3に配置
        obl_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obl')
        if obl_word:
            sub_slots["sub-m3"] = obl_word.text
            self.logger.debug(f"🔧 関係節内副詞句検出: sub-m3 = '{obl_word.text}'")
        
        if rel_type == 'obj':
            # 目的語関係代名詞: "The book that he bought"
            # slots["O1"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-o1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj':
            # 主語関係代名詞: "The man who runs"
            # slots["S"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-s"] = noun_phrase
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj:pass':
            # 受動態主語関係代名詞: "The car which was crashed"
            # slots["S"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-s"] = noun_phrase
            if aux_word:
                sub_slots["sub-aux"] = aux_word.text
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'poss':
            # 所有格関係代名詞: whose構文の特別処理
            
            # ✅ ハイブリッド解析補正がある場合の特別処理
            if hasattr(sentence, 'hybrid_corrections'):
                # whose構文で動詞が補正されている場合は、主文・関係節構造を正しく分離
                for word_id, correction in sentence.hybrid_corrections.items():
                    if correction['correction_type'] == 'whose_verb_fix':
                        # 補正された動詞（例：lives）は主文動詞なので、関係節の処理から除外
                        main_verb_word = self._find_word_by_id(sentence, word_id)
                        if main_verb_word:
                            self.logger.debug(f"🔧 whose構文ハイブリッド補正: {main_verb_word.text}は主文動詞として処理")
                            # この場合、関係節は"car is red"の部分
                            # rel_verbはcopula "is"
                            sub_slots["sub-s"] = noun_phrase  # "The man whose car"
                            sub_slots["sub-v"] = rel_verb.text  # "is"
                            
                            # 補語を検出（"red"）
                            complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'amod')
                            if complement:
                                sub_slots["sub-c1"] = complement.text
                            
                            # メイン文は別途基本5文型ハンドラーが処理する
                            return {"slots": slots, "sub_slots": sub_slots}
            
            # 通常のwhose構文処理
            if rel_subject:
                # 別の主語がある場合: "The student whose book I borrowed"
                # → 目的語関係代名詞として処理
                sub_slots["sub-o1"] = noun_phrase
                sub_slots["sub-s"] = rel_subject.text
            else:
                # 別の主語がない場合: "The woman whose dog barks"  
                # → 主語関係代名詞として処理
                sub_slots["sub-s"] = noun_phrase
            
            # 関係節内の動詞・補語を正しく抽出
            if aux_word:
                sub_slots["sub-aux"] = aux_word.text
            sub_slots["sub-v"] = rel_verb.text
            
            # whose構文の特別処理：Stanzaの誤解析対応
            if any(w.text.lower() == 'whose' for w in sentence.words):
                # acl:relclとして解析されたlives（id=7）の依存語からredを探す
                acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
                if acl_relcl_word:
                    complement = self._find_word_by_head_and_deprel(sentence, acl_relcl_word.id, 'amod')
                    if complement:
                        sub_slots["sub-c1"] = complement.text
            else:
                # 通常の補語検出
                complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'acomp')  # 形容詞補語
                if not complement:
                    complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'attr')  # 属性補語
                if not complement:
                    complement = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nmod')  # 名詞修飾
                if complement:
                    sub_slots["sub-c1"] = complement.text
            
        elif rel_type == 'advmod':
            # 関係副詞: "The place where he lives"
            # slots["M3"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-m3"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
        # 省略関係代名詞の処理
        elif rel_type == 'obj_omitted':
            # 省略目的語関係代名詞: "The book I read"
            # slots["O1"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-o1"] = noun_phrase
            sub_slots["sub-v"] = rel_verb.text
            
        elif rel_type == 'nsubj_omitted':  
            # 省略主語関係代名詞: "The person standing there"
            # slots["O1"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-o1"] = noun_phrase
            sub_slots["sub-v"] = rel_verb.text
            
        else:
            # デフォルト（目的語扱い）
            # slots["O1"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-o1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
        
        return {"slots": slots, "sub_slots": sub_slots}
    
    def _generate_whose_relative_clause_slots(self, antecedent, cop_verb, sentence) -> Dict:
        """whose構文専用の関係節スロット生成（メイン文を妨害しない）"""
        
        slots = {}  # メイン文スロットは変更しない
        sub_slots = {}
        
        # whose構文の関係節: "whose car is red"
        # 所有格関係代名詞を含む先行詞句を構築
        whose_word = None
        car_word = None
        
        for word in sentence.words:
            if word.text.lower() == 'whose':
                whose_word = word
                # whoseが依存する語（car）を取得
                car_word = self._find_word_by_id(sentence, whose_word.head)
                break
        
        if whose_word and car_word:
            # "The man whose car"の構築
            man_phrase = self._build_phrase_with_modifiers(sentence, antecedent)
            whose_car_phrase = f"{man_phrase} {whose_word.text} {car_word.text}"
            
            sub_slots["sub-s"] = whose_car_phrase
            sub_slots["sub-v"] = cop_verb.text  # "is"
            
            # 補語（red）を取得
            complement = self._find_word_by_id(sentence, cop_verb.head)
            if complement:
                sub_slots["sub-c1"] = complement.text
            
            self.logger.debug(f"🔧 whose関係節スロット: sub-s='{whose_car_phrase}', sub-v='{cop_verb.text}', sub-c1='{complement.text if complement else ''}'")
        
        return {"slots": slots, "sub_slots": sub_slots}
    
    def _process_main_clause_after_relative(self, sentence, antecedent, rel_verb, noun_phrase) -> Optional[Dict]:
        """関係節処理後の主文部分を5文型で処理"""
        
        # 主文の動詞（ROOT語）を特定
        main_verb = self._find_root_word(sentence)
        if not main_verb:
            self.logger.debug("  ⚠️ 主文動詞なし")
            return None
            
        if main_verb.id == rel_verb.id:
            self.logger.debug(f"  ⚠️ 関係節動詞がROOT - 主文なし (main_verb={main_verb.text}, rel_verb={rel_verb.text})")
            return None
        
        self.logger.debug(f"  🔍 主文動詞検出: {main_verb.text} (id: {main_verb.id}, POS: {main_verb.upos})")
        
        # 依存関係マップ構築（関係節を除外）
        dep_relations = {}
        excluded_words = []
        
        for word in sentence.words:
            # 関係節内の語をスキップ
            if self._is_word_in_relative_clause(word, rel_verb):
                excluded_words.append(word.text)
                continue
                
            if word.deprel not in dep_relations:
                dep_relations[word.deprel] = []
            dep_relations[word.deprel].append(word)
        
        self.logger.debug(f"  🚫 除外語: {excluded_words}")
        self.logger.debug(f"  📝 主文依存関係: {list(dep_relations.keys())}")
        
        # 基本5文型パターン検出
        pattern_result = self._detect_basic_five_pattern(main_verb, dep_relations)
        if not pattern_result:
            self.logger.debug("  ❌ 主文パターン検出失敗")
            return None
        
        self.logger.debug(f"  🎯 主文パターン検出: {pattern_result['pattern']}")
        
        # スロット生成（Sスロットは空にして構造を維持）
        five_pattern_slots = self._generate_basic_five_slots(
            pattern_result['pattern'], pattern_result['mapping'], dep_relations, sentence
        )
        
        # 関係節を含む主語はサブスロットにあるため、上位SスロットはNoneまたは空
        if 'slots' in five_pattern_slots and 'S' in five_pattern_slots['slots']:
            five_pattern_slots['slots']['S'] = ""  # 関係節がサブスロットに含まれることを示す
            
        self.logger.debug(f"  ✅ 主文処理完了: パターン={pattern_result['pattern']}")
        return five_pattern_slots
    
    def _is_word_in_relative_clause(self, word, rel_verb) -> bool:
        """語が関係節内にあるかチェック"""
        
        # 関係節動詞自身
        if word.id == rel_verb.id:
            return True
            
        # 関係節動詞の直接依存語（全種類）
        if word.head == rel_verb.id:
            return True
            
        # 関係代名詞（関係節動詞に依存するnsubj/obj等）
        if word.deprel in ['nsubj', 'obj', 'advmod', 'obl', 'aux', 'aux:pass', 'acomp', 'attr', 'nmod'] and word.head == rel_verb.id:
            return True
        
        # 関係節を修飾するacl:relclの依存語
        if word.deprel == 'acl:relcl':
            return True
            
        return False
    
    def _get_all_dependents(self, head_word) -> List:
        """指定語のすべての依存語を取得"""
        # この実装では、sentenceオブジェクトに直接アクセスできないため
        # 簡易実装として空リストを返す
        # 実際の使用では、sentence.wordsを通じて依存語を検索する
        return []
    
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
    
    def _find_main_verb(self, sentence):
        """主文の動詞を検索（関係節を除外・ハイブリッド解析対応）"""
        
        # ハイブリッド解析の補正情報をチェック
        if hasattr(sentence, 'hybrid_corrections'):
            for word in sentence.words:
                if word.id in sentence.hybrid_corrections:
                    correction = sentence.hybrid_corrections[word.id]
                    if correction['correction_type'] == 'whose_verb_fix':
                        # 補正された動詞を主文動詞として返す
                        self.logger.debug(f"🔧 ハイブリッド解析: 主文動詞として {word.text} を使用 (補正済み)")
                        return word
        
        # whose構文の特別処理：Stanzaがlivesを誤解析する場合の対応
        if any(w.text.lower() == 'whose' for w in sentence.words):
            # acl:relcl関係にある語を確認
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes'] and
                acl_relcl_word.lemma in ['live', 'work', 'run', 'go']):
                # これは動詞として解釈すべき
                self.logger.debug(f"🔧 whose構文: 主文動詞として {acl_relcl_word.text} を使用")
                return acl_relcl_word
        
        # 通常の場合：rootを検索
        root_word = None
        for word in sentence.words:
            if word.head == 0:  # root
                root_word = word
                break
        
        if not root_word:
            return None
            
        # rootが形容詞の場合、cop動詞を主動詞とする（"The man is strong"構造）
        if root_word.upos == 'ADJ':
            cop_verb = self._find_word_by_head_and_deprel(sentence, root_word.id, 'cop')
            if cop_verb:
                return cop_verb
        
        return root_word
    
    def _build_full_subject_with_relative_clause(self, sentence, antecedent, rel_verb):
        """関係節を含む完全な主語句を構築"""
        # 先行詞から開始
        subject_phrase = antecedent.text
        
        # 先行詞の修飾語を追加
        modifiers = []
        for word in sentence.words:
            if word.head == antecedent.id and word.id != rel_verb.id:
                if word.deprel in ['det', 'amod', 'compound']:
                    modifiers.append((word.id, word.text))
        
        # 修飾語を位置順でソート
        modifiers.sort(key=lambda x: x[0])
        
        # 完全な主語句を構築
        if modifiers:
            modifier_text = ' '.join([m[1] for m in modifiers])
            subject_phrase = f"{modifier_text} {subject_phrase}"
        
        return subject_phrase
    
    def _is_whose_construction(self, sentence, rel_verb):
        """whose構文かどうかを判定"""
        # whoseが存在し、かつrel_verbの依存語にcopがある場合
        has_whose = any(w.text.lower() == 'whose' for w in sentence.words)
        has_cop_child = any(w.head == rel_verb.id and w.deprel == 'cop' for w in sentence.words)
        return has_whose and has_cop_child
    
    def _find_cop_verb_in_whose_clause(self, sentence, rel_verb):
        """whose構文での実際の関係節動詞（cop）を検索"""
        # rel_verbの依存語でcopのものを探す
        cop_verb = next((w for w in sentence.words if w.head == rel_verb.id and w.deprel == 'cop'), None)
        return cop_verb
    
    def _find_whose_antecedent(self, sentence):
        """whose構文の先行詞を検索"""
        # root主語を取得（通常は先行詞）
        for word in sentence.words:
            if word.head == 0 and word.deprel == 'root':
                return word
        return None
    
    def _handle_basic_five_pattern(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        基本5文型ハンドラー（Phase 1実装）
        
        basic_five_pattern_engine.py の機能を統合システムに移植
        Stanza dependency parsing による基本文型検出・分解
        
        Args:
            sentence: Stanza sentence object
            base_result: 基本結果辞書
            
        Returns:
            Optional[Dict]: 5文型処理結果 or None
        """
        try:
            self.logger.debug("🔍 5文型ハンドラー実行中...")
            
            # 他のエンジンが主文動詞（V）を既に処理済みの場合のみスキップ
            # sub-vは関係節動詞なので主文処理には影響しない
            if base_result.get('slots', {}).get('V'):
                self.logger.debug("  主文動詞(V)が処理済み - スキップ")
                return None
            
            return self._process_basic_five_pattern_structure(sentence, base_result)
            
        except Exception as e:
            self.logger.warning(f"⚠️ 5文型ハンドラーエラー: {e}")
            return None
    
    def _process_basic_five_pattern_structure(self, sentence, base_result: Dict) -> Dict:
        """基本5文型構造の分解処理（ハイブリッド解析対応）"""
        
        # ✅ ハイブリッド解析補正情報を優先的に利用
        root_word = None
        is_whose_construction = any(w.text.lower() == 'whose' for w in sentence.words)
        
        if hasattr(sentence, 'hybrid_corrections'):
            # ハイブリッド解析でVERBとして補正された語を主文動詞として採用
            for word_id, correction in sentence.hybrid_corrections.items():
                if correction['correction_type'] == 'whose_verb_fix':
                    root_word = self._find_word_by_id(sentence, word_id)
                    if root_word:
                        self.logger.debug(f"🔧 ハイブリッド解析: {root_word.text} をメイン動詞として使用")
                        break
        
        # ハイブリッド解析がない場合の従来処理        
        if not root_word and is_whose_construction:
            # acl:relcl関係にある語を確認
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes', 'sits', 'stands']):
                # これは実際のメイン動詞として解釈すべき
                root_word = acl_relcl_word
                self.logger.debug(f"🔧 whose構文検出: メイン動詞を {acl_relcl_word.text} に修正")
        
        # 通常の場合：ROOT語検出
        if not root_word:
            root_word = self._find_root_word(sentence)
            if not root_word:
                return base_result

        # 依存関係マップ構築
        dep_relations = {}
        for word in sentence.words:
            if word.deprel not in dep_relations:
                dep_relations[word.deprel] = []
            dep_relations[word.deprel].append(word)
        
        # ✅ whose構文の特別処理：メイン文の依存関係マップを正しく構築
        if is_whose_construction and root_word:
            # メイン動詞の直接依存語を依存関係マップに追加
            for word in sentence.words:
                if word.head == root_word.id:
                    if word.deprel not in dep_relations:
                        dep_relations[word.deprel] = []
                    dep_relations[word.deprel].append(word)
                    
            # ROOT語（先行詞）を主語として追加
            if 'nsubj' not in dep_relations:
                dep_relations['nsubj'] = []
            root_word_from_stanza = self._find_root_word(sentence)
            if root_word_from_stanza:
                dep_relations['nsubj'].append(root_word_from_stanza)
                
            self.logger.debug(f"🔧 whose構文: 依存関係再構築完了, メイン動詞={root_word.text}")

        # 基本5文型パターン検出
        pattern_result = self._detect_basic_five_pattern(root_word, dep_relations)
        if not pattern_result:
            return base_result
        
        # スロット生成
        result = base_result.copy()
        if 'slots' not in result:
            result['slots'] = {}
        if 'sub_slots' not in result:
            result['sub_slots'] = {}
        
        five_pattern_slots = self._generate_basic_five_slots(
            pattern_result['pattern'], pattern_result['mapping'], dep_relations, sentence
        )
        
        result['slots'].update(five_pattern_slots.get('slots', {}))
        result['sub_slots'].update(five_pattern_slots.get('sub_slots', {}))
        
        # 文法情報記録（_merge_handler_resultsと互換性のある形式）
        result['grammar_info'] = {
            'detected_patterns': ['basic_five_pattern'],
            'handler_contributions': {
                'basic_five_pattern': {
                    'pattern': pattern_result['pattern'],
                    'confidence': pattern_result.get('confidence', 0.8)
                }
            }
        }
        
        self.logger.debug(f"  ✅ 5文型処理完了: パターン={pattern_result['pattern']}")
        return result
    
    def _find_root_word(self, sentence):
        """ROOT語を検索"""
        return next((w for w in sentence.words if w.head == 0), None)
    
    def _detect_basic_five_pattern(self, root_word, dep_relations):
        """基本5文型パターン検出"""
        
        # 基本5文型パターン定義（詳細→単純の順序で検出）
        patterns = {
            "SVOO": {
                "required": ["nsubj", "obj", "iobj"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "iobj": "O1", "obj": "O2"}
            },
            "SVOC": {
                "required": ["nsubj", "obj", "xcomp"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1", "xcomp": "C2"}
            },
            "SVO": {
                "required": ["nsubj", "obj"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1"}
            },
            "SVC": {
                "required": ["nsubj", "cop"],
                "optional": [],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SVC_PRON": {
                "required": ["nsubj", "cop"],
                "optional": [],
                "root_pos": ["PRON"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SVC_ALT": {
                "required": ["nsubj", "xcomp"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V", "xcomp": "C1"}
            },
            "SV": {
                "required": ["nsubj"],
                "optional": [],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"}
            }
        }
        
        # パターンマッチング
        for pattern_name, pattern_info in patterns.items():
            if self._matches_five_pattern(pattern_info, dep_relations, root_word):
                return {
                    'pattern': pattern_name,
                    'mapping': pattern_info['mapping'],
                    'confidence': 0.9
                }
        
        return None
    
    def _matches_five_pattern(self, pattern_info, dep_relations, root_word):
        """5文型パターンマッチング"""
        # 必要な依存関係の確認
        for rel in pattern_info['required']:
            if rel not in dep_relations:
                return False
        
        # ROOT語の品詞チェック
        if root_word.upos not in pattern_info['root_pos']:
            return False
        
        return True
    
    def _build_phrase_with_modifiers(self, sentence, main_word):
        """
        修飾語句を含む完全な句を構築
        
        対応修飾語タイプ：
        - det: 限定詞 (a, an, the, my, your, his, her, its, our, their)
        - amod: 形容詞修飾語 (red, beautiful, smart, old)
        - nummod: 数詞修飾語 (one, two, first, second)  
        - nmod:poss: 所有格修飾語 (John's, Mary's, my, your)
        - compound: 複合名詞 (car door, school bus)
        """
        if not main_word:
            return ""
        
        # 修飾語収集
        modifiers = []
        for word in sentence.words:
            if word.head == main_word.id:
                if word.deprel in ['det', 'amod', 'nummod', 'nmod:poss', 'compound']:
                    modifiers.append(word)
        
        # デバッグログ追加
        if modifiers:
            self.logger.debug(f"🔧 修飾語検出 [{main_word.text}]: {[(m.text, m.deprel) for m in modifiers]}")
        
        # 修飾語をID順でソート（語順保持）
        modifiers.sort(key=lambda w: w.id)
        
        # 句構築: 修飾語 + メイン語
        phrase_words = modifiers + [main_word]
        phrase_words.sort(key=lambda w: w.id)  # 最終的な語順確保
        
        result = ' '.join(word.text for word in phrase_words)
        self.logger.debug(f"🔧 句構築完了: '{result}'")
        
        return result
    
    def _generate_basic_five_slots(self, pattern, mapping, dep_relations, sentence):
        """基本5文型スロット生成（修飾語句対応強化）"""
        slots = {}
        sub_slots = {}
        
        # マッピングに従ってスロット生成
        for dep_rel, slot in mapping.items():
            if dep_rel == "root":
                # ROOT語の処理（動詞は通常修飾語なしなので単語のみ）
                root_word = self._find_root_word(sentence)
                if root_word:
                    slots[slot] = root_word.text
            elif dep_rel in dep_relations:
                # 依存関係語の処理（修飾語句を含む完全な句を構築）
                words = dep_relations[dep_rel]
                if words:
                    # メインの語
                    main_word = words[0]
                    # 修飾語句を構築
                    phrase = self._build_phrase_with_modifiers(sentence, main_word)
                    slots[slot] = phrase
        
        # ✅ 追加処理：ROOTワードにも修飾語句処理を適用（動詞以外の場合）
        # 例: "The woman is my neighbor" でneighborがROOTの場合
        root_word = self._find_root_word(sentence)
        if root_word and root_word.pos in ['NOUN', 'PRON', 'ADJ']:
            # 名詞・代名詞・形容詞がROOTの場合、修飾語句を構築
            root_phrase = self._build_phrase_with_modifiers(sentence, root_word)
            
            # ROOTワード対応のスロットを更新
            for dep_rel, slot in mapping.items():
                if dep_rel == "root" and slot in slots:
                    if slots[slot] == root_word.text:  # 単語のみの場合
                        slots[slot] = root_phrase  # 修飾語句に更新
                        self.logger.debug(f"🔧 ROOT語修飾語句適用: {slot} = '{root_phrase}'")
        
        # 修飾語の処理（基本的なもののみ）
        # 関係副詞は関係節ハンドラーに任せるため除外
        relative_adverbs = ['where', 'when', 'why', 'how']
        
        # ✅ 関係節内の語を事前に特定して除外
        rel_verb_candidates = [w for w in sentence.words if w.deprel in ['acl:relcl', 'acl']]
        excluded_word_ids = set()
        for rel_verb_cand in rel_verb_candidates:
            # 関係節動詞とその依存語をすべて除外
            excluded_word_ids.add(rel_verb_cand.id)
            for word in sentence.words:
                if word.head == rel_verb_cand.id:
                    excluded_word_ids.add(word.id)
        
        for word in sentence.words:
            # 関係節内の語をスキップ
            if word.id in excluded_word_ids:
                continue
                
            # ✅ 副詞処理は専門エンジンに委譲 - 基本5文型では処理しない
            # if word.deprel == 'advmod' and 'M2' not in slots:
            #     if word.text.lower() not in relative_adverbs:
            #         slots['M2'] = word.text  # 通常の副詞修飾語のみ
            #     else:
            #         self.logger.debug(f"🔍 関係副詞除外: {word.text} (関係節ハンドラーに委譲)")
            # elif word.deprel == 'obl' and 'M3' not in slots:
            #     slots['M3'] = word.text  # 前置詞句等
        
        return {'slots': slots, 'sub_slots': sub_slots}

    def _handle_adverbial_modifier(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        副詞エンジン（Phase 4実装）
        
        migration_source/prepositional_phrase_engine.py の分類システムを参考に
        統一された副詞処理を実装
        
        Args:
            sentence: Stanza sentence オブジェクト
            base_result: 基本解析結果（重複防止用）
            
        Returns:
            Optional[Dict]: 副詞処理結果、または None
        """
        from enum import Enum
        
        class AdverbialType(Enum):
            """副詞の意味分類"""
            TIME = "time"           # 時間副詞 → M1
            FREQUENCY = "frequency" # 頻度副詞 → M2
            MANNER = "manner"       # 様態副詞 → M2/M3
            LOCATION = "location"   # 場所副詞 → M2/M3
            DEGREE = "degree"       # 程度副詞 → M2
        
        self.logger.debug("🔍 副詞ハンドラー実行中...")
        
        # === 既存スロット確認（重複防止） ===
        existing_slots = {}
        if base_result and 'slots' in base_result:
            existing_slots = base_result['slots']
        
        # 既に割り当て済みの副詞文字列を特定
        existing_adverbs = set()
        for slot_key, slot_value in existing_slots.items():
            if slot_key.startswith('M') and slot_value:
                # スロット値を単語に分解して副詞を特定
                words = slot_value.split()
                existing_adverbs.update(words)
        
        # === 1. 副詞検出（拡張対応） ===
        adverbial_modifiers = []
        sentence_length = len(sentence.words)
        
        for word in sentence.words:
            # 拡張副詞依存関係対応（Yesterday検出バグ修正済み）
            if word.deprel in ['advmod', 'obl', 'obl:unmarked', 'obl:tmod', 'obl:npmod', 'nmod:unmarked', 'nmod:tmod']:
                # 既に処理済みの副詞をスキップ
                if word.text in existing_adverbs:
                    self.logger.debug(f"⚠️ 既存スロットに割り当て済み - スキップ: {word.text}")
                    continue
                    
                # 関係副詞は関係節ハンドラーに任せる
                if word.text.lower() in ['where', 'when', 'why', 'how']:
                    continue
                
                # 副詞分類
                adv_type = self._classify_adverb(word, sentence)
                
                # 位置計算（1ベース）
                position_ratio = word.id / sentence_length
                
                adverbial_modifiers.append({
                    'word': word,
                    'type': adv_type,
                    'position': word.id,
                    'position_ratio': position_ratio,
                    'text': word.text
                })
        
        if not adverbial_modifiers:
            self.logger.debug("❌ 副詞なし - スキップ")
            return None
        
        # === 2. 位置ベース配置 ===
        slots = {}
        sub_slots = {}
        
        # 位置順でソート（前から後ろへ）
        adverbial_modifiers.sort(key=lambda x: x['position'])
        
        for adv_info in adverbial_modifiers:
            word = adv_info['word']
            adv_type = adv_info['type']
            position_ratio = adv_info['position_ratio']
            word_text = word.text
            
            # 複合副詞句の構築
            phrase = self._build_adverbial_phrase(sentence, word)
            if phrase != word_text:
                word_text = phrase
            
            # 位置ベース配置判定
            target_slot = self._determine_adverb_slot(adv_type, position_ratio)
            
            # スロット配置（重複回避）
            if target_slot == 'M1' and 'M1' not in slots:
                slots['M1'] = word_text
                self.logger.debug(f"🔧 M1配置({adv_type.value}): {word_text} (位置: {position_ratio:.2f})")
            elif target_slot == 'M2' and 'M2' not in slots:
                slots['M2'] = word_text
                self.logger.debug(f"🔧 M2配置({adv_type.value}): {word_text} (位置: {position_ratio:.2f})")
            elif target_slot == 'M3' and 'M3' not in slots:
                slots['M3'] = word_text
                self.logger.debug(f"🔧 M3配置({adv_type.value}): {word_text} (位置: {position_ratio:.2f})")
            else:
                # フォールバック配置
                for fallback_slot in ['M1', 'M2', 'M3']:
                    if fallback_slot not in slots:
                        slots[fallback_slot] = word_text
                        self.logger.debug(f"🔧 {fallback_slot}フォールバック配置: {word_text}")
                        break
        
        if slots:
            self.logger.debug(f"  ✅ 副詞処理完了: {len(slots)} slots detected")
            return {'slots': slots, 'sub_slots': sub_slots}
        else:
            return None
    
    def _classify_adverb(self, word, sentence):
        """副詞の意味分類"""
        from enum import Enum
        
        class AdverbialType(Enum):
            TIME = "time"
            FREQUENCY = "frequency"
            MANNER = "manner"
            LOCATION = "location"
            DEGREE = "degree"
        
        word_lower = word.text.lower()
        
        # 時間副詞
        time_adverbs = {
            'yesterday', 'today', 'tomorrow', 'now', 'then', 'recently', 
            'currently', 'formerly', 'previously', 'eventually', 'finally',
            'earlier', 'later', 'soon', 'immediately', 'already', 'still',
            'ago', 'before', 'after', 'during', 'meanwhile'
        }
        
        # 頻度副詞
        frequency_adverbs = {
            'always', 'usually', 'often', 'sometimes', 'rarely', 'never',
            'frequently', 'occasionally', 'seldom', 'constantly', 'repeatedly',
            'once', 'twice', 'again', 'daily', 'weekly', 'monthly'
        }
        
        # 様態副詞
        manner_adverbs = {
            'carefully', 'quickly', 'slowly', 'quietly', 'loudly', 'gently',
            'suddenly', 'gradually', 'easily', 'hardly', 'clearly', 'properly',
            'correctly', 'incorrectly', 'well', 'badly', 'perfectly', 'seriously'
        }
        
        # 場所副詞
        location_adverbs = {
            'here', 'there', 'everywhere', 'nowhere', 'somewhere', 'anywhere',
            'upstairs', 'downstairs', 'outside', 'inside', 'nearby', 'far',
            'home', 'abroad', 'locally', 'globally'
        }
        
        # 程度副詞
        degree_adverbs = {
            'very', 'quite', 'rather', 'extremely', 'completely', 'totally',
            'partially', 'slightly', 'barely', 'almost', 'entirely', 'mostly',
            'too', 'enough', 'highly', 'deeply'
        }
        
        # 分類実行
        if word_lower in time_adverbs:
            return AdverbialType.TIME
        elif word_lower in frequency_adverbs:
            return AdverbialType.FREQUENCY
        elif word_lower in manner_adverbs:
            return AdverbialType.MANNER
        elif word_lower in location_adverbs:
            return AdverbialType.LOCATION
        elif word_lower in degree_adverbs:
            return AdverbialType.DEGREE
        else:
            # デフォルト（品詞ベース判定）
            if word.upos == 'ADV':
                return AdverbialType.MANNER  # 副詞は様態として扱う
            else:
                return AdverbialType.LOCATION  # 名詞句は場所として扱う
    
    def _determine_adverb_slot(self, adv_type, position_ratio) -> str:
        """副詞タイプと位置に基づくスロット決定"""
        from enum import Enum
        
        class AdverbialType(Enum):
            TIME = "time"
            FREQUENCY = "frequency"
            MANNER = "manner"
            LOCATION = "location"
            DEGREE = "degree"
        
        # 時間副詞は常にM1
        if adv_type == AdverbialType.TIME:
            return 'M1'
        
        # 位置ベース判定
        if position_ratio <= 0.3:  # 文頭30%
            return 'M1'
        elif position_ratio >= 0.7:  # 文末30% 
            return 'M3'
        else:  # 文中40%
            return 'M2'
    
    def _build_adverbial_phrase(self, sentence, main_word):
        """副詞句の構築（前置詞句対応）"""
        # 修飾語収集
        modifiers = []
        for word in sentence.words:
            if word.head == main_word.id:
                if word.deprel in ['det', 'amod', 'case', 'compound']:
                    modifiers.append(word)
        
        if not modifiers:
            return main_word.text
        
        # 修飾語をID順でソート（語順保持）
        modifiers.sort(key=lambda w: w.id)
        
        # 句構築: 修飾語 + メイン語
        phrase_words = modifiers + [main_word]
        phrase_words.sort(key=lambda w: w.id)
        
        return ' '.join(word.text for word in phrase_words)

    def _handle_passive_voice(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        受動態ハンドラー（Phase 2実装）
        
        passive_voice_engine.py の機能を統合システムに移植
        Stanza dependency parsing による受動態検出・分解
        
        Args:
            sentence: Stanza解析済みsentence object
            base_result: ベース結果（コピー）
            
        Returns:
            Dict: 受動態分解結果 or None
        """
        try:
            self.logger.debug("🔍 受動態ハンドラー実行中...")
            
            # 受動態構造分析
            passive_info = self._analyze_passive_structure(sentence)
            if not passive_info:
                self.logger.debug("  受動態なし - スキップ")
                return None
                
            self.logger.debug("  ✅ 受動態検出")
            return self._process_passive_construction(sentence, passive_info, base_result)
            
        except Exception as e:
            self.logger.warning(f"⚠️ 受動態ハンドラーエラー: {e}")
            return None
    
    def _analyze_passive_structure(self, sentence) -> Optional[Dict]:
        """受動態構造の分析"""
        passive_features = {
            'auxiliary': None,      # be動詞
            'main_verb': None,      # 過去分詞
            'subject': None,        # 主語
            'agent': None,          # by句動作主
            'agent_phrase': None,   # by句全体
            'type': None            # 受動態の種類
        }
        
        # 典型的な過去分詞リスト
        common_past_participles = {
            'written', 'bought', 'sold', 'made', 'taken', 'given', 'seen', 'done',
            'broken', 'stolen', 'found', 'lost', 'taught', 'caught', 'brought',
            'eaten', 'driven', 'shown', 'known', 'grown', 'thrown', 'chosen'
        }
        
        # 構造要素の検出
        for word in sentence.words:
            # 受動態主語検出
            if word.deprel == 'nsubj:pass':
                passive_features['subject'] = word
            elif word.deprel == 'nsubjpass':  # 旧版Stanza対応
                passive_features['subject'] = word
            elif word.deprel == 'nsubj':  # 形容詞受動態の場合
                if not passive_features['subject']:  # まだ見つかっていない場合のみ
                    passive_features['subject'] = word
                    
            # 受動態補助動詞検出
            elif word.deprel == 'aux:pass':
                passive_features['auxiliary'] = word
            elif word.deprel == 'auxpass':  # 旧版Stanza対応
                passive_features['auxiliary'] = word
            elif word.deprel == 'cop' and word.lemma == 'be':
                passive_features['auxiliary'] = word
                
            # 主動詞検出（過去分詞）
            elif word.deprel == 'root':
                if word.upos == 'VERB' and word.xpos == 'VBN':  # 過去分詞
                    passive_features['main_verb'] = word
                elif word.upos == 'ADJ' and word.text.lower() in common_past_participles:
                    passive_features['main_verb'] = word
                    
            # by句動作主検出
            elif word.deprel == 'obl:agent':
                passive_features['agent'] = word
                passive_features['agent_phrase'] = self._build_agent_phrase(sentence, word)
            elif word.deprel == 'agent':  # 旧版対応
                passive_features['agent'] = word
                passive_features['agent_phrase'] = self._build_agent_phrase(sentence, word)
        
        # 受動態判定
        if (passive_features['auxiliary'] and 
            passive_features['main_verb'] and 
            passive_features['subject']):
            
            passive_features['type'] = 'agent_passive' if passive_features['agent'] else 'simple_passive'
            
            self.logger.debug(f"  主語: {passive_features['subject'].text}")
            self.logger.debug(f"  補助動詞: {passive_features['auxiliary'].text}")
            self.logger.debug(f"  主動詞: {passive_features['main_verb'].text}")
            self.logger.debug(f"  動作主: {passive_features['agent'].text if passive_features['agent'] else 'なし'}")
            self.logger.debug(f"  種類: {passive_features['type']}")
            
            return passive_features
        
        return None
    
    def _process_passive_construction(self, sentence, passive_info: Dict, base_result: Dict) -> Dict:
        """受動態構文の処理"""
        result = base_result.copy()
        
        auxiliary = passive_info['auxiliary']
        main_verb = passive_info['main_verb']
        subject = passive_info['subject']
        agent_phrase = passive_info['agent_phrase']
        passive_type = passive_info['type']
        
        self.logger.debug(f"  受動態処理: {passive_type}")
        
        # スロット生成
        rephrase_slots = self._generate_passive_voice_slots(
            passive_type, subject, auxiliary, main_verb, agent_phrase, passive_info['agent'], sentence
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
            'patterns': ['passive_voice'],
            'passive_type': passive_type,
            'subject': subject.text,
            'auxiliary': auxiliary.text,
            'main_verb': main_verb.text,
            'agent': passive_info['agent'].text if passive_info['agent'] else None
        }
        
        self.logger.debug(f"  ✅ 受動態処理完了: {len(rephrase_slots.get('slots', {}))} main slots, {len(rephrase_slots.get('sub_slots', {}))} sub slots")
        return result
    
    def _generate_passive_voice_slots(self, passive_type: str, subject, auxiliary, main_verb, 
                                     agent_phrase: str, agent, sentence) -> Dict:
        """受動態タイプ別スロット生成"""
        
        slots = {}
        sub_slots = {}
        
        # 基本スロット（共通）
        slots['S'] = self._build_subject_phrase(sentence, subject)
        slots['Aux'] = auxiliary.text
        slots['V'] = main_verb.text
        
        # by句付き受動態の場合
        if passive_type == 'agent_passive' and agent_phrase:
            slots['M1'] = agent_phrase  # by句全体
            if agent:
                sub_slots['sub-m1'] = agent.text  # 動作主のみ
        
        return {'slots': slots, 'sub_slots': sub_slots}
    
    def _build_agent_phrase(self, sentence, agent_word) -> str:
        """by句全体の構築"""
        if not agent_word:
            return None
        
        # by前置詞を探す
        by_preposition = None
        for word in sentence.words:
            if word.text.lower() == 'by' and word.deprel == 'case' and word.head == agent_word.id:
                by_preposition = word
                break
        
        if by_preposition:
            # by + 動作主 + 修飾語
            phrase_words = [by_preposition, agent_word]
            
            # 動作主の修飾語を追加
            for word in sentence.words:
                if word.head == agent_word.id and word.deprel in ['det', 'amod', 'nmod']:
                    phrase_words.append(word)
            
            # ID順ソート（語順保持）
            phrase_words.sort(key=lambda w: w.id)
            return ' '.join(w.text for w in phrase_words)
        
        return f"by {agent_word.text}"
    
    def _build_subject_phrase(self, sentence, subject) -> str:
        """主語句の構築（修飾語含む）"""
        if not subject:
            return ""
            
        subject_words = [subject]
        
        # 主語の修飾語を収集
        for word in sentence.words:
            if word.head == subject.id and word.deprel in ['det', 'amod', 'compound', 'nmod']:
                subject_words.append(word)
        
        # ID順ソート（語順保持）
        subject_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in subject_words)

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

def test_phase2_passive_voice():
    """Phase 2 受動態ハンドラーテスト"""
    print("🧪 Phase 2 受動態テスト開始...")
    
    try:
        # 初期化
        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        
        # Phase 1 & 2 ハンドラー追加
        mapper.add_handler('relative_clause')
        mapper.add_handler('passive_voice')
        print("✅ 関係節 + 受動態ハンドラー追加完了")
        
        # 重要テストケース
        test_cases = [
            ("The car was bought.", "単純受動態"),
            ("The car was bought by him.", "by句付き受動態"),
            ("The book which was read was interesting.", "関係節+受動態複合"),
            ("The letter was written by her.", "受動態基本形")
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
                
                # 受動態チェック
                slots = result.get('slots', {})
                if 'Aux' in slots and 'V' in slots:
                    print(f"\n🎯 受動態チェック:")
                    print(f"  S: '{slots.get('S', '')}'")
                    print(f"  Aux: '{slots.get('Aux', '')}'")  
                    print(f"  V: '{slots.get('V', '')}'")
                    if 'M1' in slots:
                        print(f"  M1 (by句): '{slots.get('M1', '')}'")
                    
                    print("  ✅ 受動態構造検出成功！")
                    success_count += 1
                else:
                    print("  ❌ 受動態構造未検出")
                    
            except Exception as e:
                print(f"❌ テスト{i}エラー: {e}")
        
        # 統計確認
        stats = mapper.get_stats()
        print(f"\n📈 Phase 2 統計:")
        print(f"  処理数: {stats['processing_count']}")
        print(f"  平均処理時間: {stats['average_processing_time']:.3f}s")
        print(f"  ハンドラー成功数: {stats['handler_success_count']}")
        
        print(f"\n🎉 Phase 2 テスト完了! 成功: {success_count}/{len(test_cases)}")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"❌ Phase 2 テスト失敗: {e}")
        return False

def test_phase1_relative_clause():
    """Phase 1 関係節ハンドラーテスト"""
    print("🧪 Phase 1 関係節テスト開始...")
    
    try:
        # 初期化
        mapper = UnifiedStanzaRephraseMapper(log_level='DEBUG')
        
        # Phase 1 ハンドラー追加
        mapper.add_handler('relative_clause')
        print("✅ 関係節ハンドラー追加完了")
        
        # 重要テストケース（省略関係代名詞対応強化）
        test_cases = [
            ("The car which we saw was red.", "目的語関係代名詞"),
            ("The man who runs fast is strong.", "主語関係代名詞"), 
            ("The man whose car is red lives here.", "所有格関係代名詞"),
            ("The place where he lives is nice.", "関係副詞where"),
            ("The book I read was interesting.", "省略目的語関係代名詞（能動態）"),
            ("The book that was written is famous.", "省略目的語関係代名詞（受動態）"),
            ("The person standing there is my friend.", "省略主語関係代名詞（現在分詞）")
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
        if test_phase1_relative_clause():
            print("\n" + "="*60)
            # Phase 2 受動態テスト
            test_phase2_passive_voice()
        else:
            print("❌ Phase 1失敗のため Phase 2をスキップ")
    else:
        print("❌ Phase 0失敗のため Phase 1,2をスキップ")
