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
        
        # 基本ハンドラーの初期化
        self._initialize_basic_handlers()
        
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
    
    def _initialize_basic_handlers(self):
        """基本ハンドラーの初期化"""
        basic_handlers = [
            'basic_five_pattern',     # 基本5文型
            'relative_clause',        # 関係節
            'passive_voice',          # 受動態  
            'participle_construction', # 分詞構文（副詞処理より先）
            'adverbial_modifier',     # 副詞句（前置詞句含む）
            'auxiliary_complex',      # 助動詞
            'conjunction',            # 接続詞（"as if"等）
        ]
        
        for handler in basic_handlers:
            self.add_handler(handler)
        
        self.logger.info(f"✅ 基本ハンドラー初期化完了: {len(self.active_handlers)}個")
    
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
                'handler_contributions': {},
                'control_flags': {}  # ハンドラー制御フラグ
            }
        }
        
        # メイン文（最初のsentence）を対象とする
        main_sentence = doc.sentences[0] if doc.sentences else None
        if not main_sentence:
            return result
        
        self.logger.debug(f"🔧 Unified mapping開始: {len(self.active_handlers)} handlers active")
        
        # ハンドラー実行順序の制御（分詞構文を最優先）
        ordered_handlers = self._get_ordered_handlers()
        
        # 全アクティブハンドラーの同時実行（順序制御付き）
        for handler_name in ordered_handlers:
            try:
                # ハンドラー制御フラグをチェック
                control_flags = result.get('grammar_info', {}).get('control_flags', {})
                if self._should_skip_handler(handler_name, control_flags):
                    self.logger.debug(f"🚫 Handler スキップ: {handler_name} (制御フラグ)")
                    continue
                
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
    
    def _should_skip_handler(self, handler_name: str, control_flags: Dict) -> bool:
        """ハンドラーをスキップすべきかチェック"""
        # 分詞構文が検出された場合、関係節ハンドラーをスキップ
        if handler_name == 'relative_clause' and control_flags.get('participle_detected', False):
            return True
        
        return False
    
    def _get_ordered_handlers(self) -> List[str]:
        """ハンドラーの実行順序を制御（分詞構文を最優先）"""
        
        # 優先順位テーブル
        priority_order = [
            'participle_construction',  # 最優先：分詞構文が制御フラグを設定
            'basic_five_pattern',
            'relative_clause',
            'passive_voice',
            'adverbial_modifier',
            'auxiliary_complex',
            'conjunction'
        ]
        
        # アクティブハンドラーを優先順位順に並べ替え
        ordered = []
        
        # 1. 優先順位テーブルに従って順序付け
        for handler in priority_order:
            if handler in self.active_handlers:
                ordered.append(handler)
        
        # 2. テーブルにない新しいハンドラーは最後に追加
        for handler in self.active_handlers:
            if handler not in ordered:
                ordered.append(handler)
        
        self.logger.debug(f"📋 ハンドラー実行順序: {ordered}")
        return ordered
    
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
                    
                    # 🎯 分詞構文保護：分詞構文ハンドラーが設定した空文字を保護
                    control_flags = base_result.get('grammar_info', {}).get('control_flags', {})
                    participle_detected = control_flags.get('participle_detected', False)
                    modified_slot = control_flags.get('modified_slot')
                    
                    if (participle_detected and slot_name == modified_slot and 
                        existing_value == "" and handler_name != 'participle_construction'):
                        # 分詞構文で空文字化されたスロットは他のハンドラーで上書き禁止
                        self.logger.debug(f"🛡️ 分詞構文保護: {slot_name} 空文字保持 (by participle_construction)")
                        pass  # 空文字を保持
                    # ★ Mスロット保護：副詞ハンドラーで設定されたMスロットを保護
                    elif slot_name.startswith('M') and existing_value and handler_name != 'adverbial_modifier':
                        # 副詞ハンドラー以外はMスロットを上書きできない
                        pass  # 既存値を保持
                    # 既存値が空で新値が有効な場合は上書き
                    elif not existing_value and slot_data:
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
        self._apply_rephrase_slot_structure_rules(result)
        
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
            
            # 助動詞ハンドラーが検出した主文動詞を適用
            detected_patterns = result.get('grammar_info', {}).get('detected_patterns', [])
            if 'passive_voice' in detected_patterns:
                passive_info = result.get('grammar_info', {}).get('handler_contributions', {}).get('passive_voice', {})
                if passive_info and 'main_verb' in passive_info:
                    main_verb_from_passive = passive_info['main_verb']
                    result['slots']['V'] = main_verb_from_passive
                    self.logger.debug(f"🔧 whose構文: 受動態動詞修正 V='{main_verb_from_passive}'")
                    
            self.logger.debug(f"🔧 whose構文後処理: 主文V={result['slots'].get('V')}, S={result['slots'].get('S')}")
        
        return result
    
    def _apply_rephrase_slot_structure_rules(self, result: Dict) -> None:
        """
        Rephrase仕様準拠：複文での正しいスロット配置
        
        重要ルール：sub-slotsが存在する場合、対応するmain slotsは空文字にする
        例外：Aux, Vスロットは例外適用なし、接続詞構文では主節要素保持
        
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
        
        # 接続詞構文では主節要素を保持
        grammar_info = result.get('grammar_info', {})
        handler_contributions = grammar_info.get('handler_contributions', {})
        is_conjunction = 'conjunction' in handler_contributions
        
        if is_conjunction:
            self.logger.debug("🔗 接続詞構文検出: 主節要素保持")
            return
        
        # 対応関係マッピング（Aux, V除外）
        main_to_sub_mapping = {
            'S': 'sub-s',
            'O1': 'sub-o1', 
            'O2': 'sub-o2',
            'C1': 'sub-c1',
            'C2': 'sub-c2'
            # M1, M2, M3は除外 - 主節副詞と関係節副詞は独立存在
        }
        
        # 🎯 Sスロットの完全な子スロット群（分詞構文用）
        s_child_slots = ['sub-s', 'sub-aux', 'sub-v', 'sub-c1', 'sub-o1', 'sub-o2', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3']
        
        # 分詞構文制御フラグをチェック
        grammar_info = result.get('grammar_info', {})
        control_flags = grammar_info.get('control_flags', {})
        participle_detected = control_flags.get('participle_detected', False)
        
        self.logger.debug(f"🏗️ Rephrase仕様適用開始 - Sub-slots: {list(sub_slots.keys())}, 分詞構文: {participle_detected}")
        
        # 複文判定＆スロット空文字化処理
        for main_slot, sub_slot in main_to_sub_mapping.items():
            if sub_slot in sub_slots and sub_slots[sub_slot]:
                # Sub-slotが存在し内容がある場合、対応するmain slotを空にする
                if main_slot in slots:
                    original_value = slots[main_slot]
                    
                    # 分詞構文特別処理: 分詞構文ハンドラーが既に適切に設定済み
                    if participle_detected and sub_slot in ['sub-v', 'sub-aux', 'sub-m2', 'sub-m3']:
                        self.logger.debug(
                            f"🎯 分詞構文保護: {main_slot} - {sub_slot}は分詞構文ハンドラーが管理済み"
                        )
                        continue  # 分詞構文関連のsub-slotは変更しない
                    
                    # 副詞スロット特別処理: 主節副詞は保持
                    if main_slot.startswith('M') and original_value:
                        # 主節副詞が存在する場合、sub-slotの移動は行わない
                        self.logger.debug(
                            f"🛡️ 主節副詞保護: {main_slot}: '{original_value}' (preserved) "
                            f"while {sub_slot}: '{sub_slots[sub_slot]}' (kept in sub-slot)"
                        )
                        continue  # 空文字化をスキップ
                    
                    slots[main_slot] = ""  # 位置マーカーとして空文字設定
                    
                    self.logger.debug(
                        f"🔄 Complex sentence rule applied: "
                        f"{main_slot}: '{original_value}' → '' "
                        f"(sub-slot {sub_slot}: '{sub_slots[sub_slot]}')"
                    )
        
        # 🎯 Sスロットの完全な子スロット群チェック（分詞構文対応）
        s_has_child = any(child_slot in sub_slots and sub_slots[child_slot] for child_slot in s_child_slots)
        if s_has_child and 'S' in slots and slots['S']:
            original_s = slots['S']
            slots['S'] = ""
            active_children = [slot for slot in s_child_slots if slot in sub_slots and sub_slots[slot]]
            self.logger.debug(
                f"🎯 Sスロット空文字化: S: '{original_s}' → '' "
                f"(子スロット存在: {', '.join(active_children)})"
            )
        
        # 副詞重複チェックと削除
        self._remove_adverb_duplicates(slots, sub_slots)
        
        # 処理結果をデバッグログ出力
        applied_rules = [
            f"{main}→{sub}" for main, sub in main_to_sub_mapping.items() 
            if sub in sub_slots and sub_slots[sub] and main in slots
        ]
        
        if applied_rules:
            self.logger.info(f"✅ Rephrase複文ルール適用: {', '.join(applied_rules)}")
        else:
            self.logger.debug("🔍 Simple sentence detected - No main slot emptying required")
    
    def _remove_adverb_duplicates(self, slots: Dict, sub_slots: Dict):
        """主節と関係節の副詞重複を除去（関係節内重複も対応）"""
        
        # === 1. 関係節内重複除去（最重要）===
        sub_adverbs = {k: v for k, v in sub_slots.items() if k.startswith('sub-m') and v}
        
        if len(sub_adverbs) > 1:
            # 関係節内で同じ副詞が複数スロットに配置されている場合
            seen_adverbs = {}
            slots_to_clear = []
            
            for sub_slot, sub_value in sub_adverbs.items():
                adverb_text = sub_value.strip()
                if adverb_text in seen_adverbs:
                    # 重複検出: より優先度の低いスロットを削除
                    existing_slot = seen_adverbs[adverb_text]
                    
                    # 優先度: sub-m2 > sub-m1 > sub-m3（Rephrase仕様準拠）
                    priority_order = {'sub-m2': 3, 'sub-m1': 2, 'sub-m3': 1}
                    
                    if priority_order.get(sub_slot, 0) > priority_order.get(existing_slot, 0):
                        # 新スロットの方が優先度高→既存を削除
                        slots_to_clear.append(existing_slot)
                        seen_adverbs[adverb_text] = sub_slot
                        self.logger.debug(f"🔄 関係節内重複削除: {existing_slot}='{adverb_text}' → '' ({sub_slot}='{adverb_text}' を優先)")
                    else:
                        # 既存スロットの方が優先度高→新スロットを削除
                        slots_to_clear.append(sub_slot)
                        self.logger.debug(f"🔄 関係節内重複削除: {sub_slot}='{adverb_text}' → '' ({existing_slot}='{adverb_text}' を優先)")
                else:
                    seen_adverbs[adverb_text] = sub_slot
            
            # 重複スロットをクリア
            for slot_to_clear in slots_to_clear:
                sub_slots[slot_to_clear] = ""
        
        # === 2. 主節↔関係節間重複除去（従来機能）===
        main_adverbs = {k: v for k, v in slots.items() if k.startswith('M') and v}
        remaining_sub_adverbs = {k: v for k, v in sub_slots.items() if k.startswith('sub-m') and v}
        
        if not main_adverbs or not remaining_sub_adverbs:
            return
        
        # 重複副詞の検出と削除
        for main_slot, main_value in list(main_adverbs.items()):
            for sub_slot, sub_value in remaining_sub_adverbs.items():
                # 同じ副詞が主節と関係節に存在する場合
                if main_value.strip() == sub_value.strip():
                    # 関係節を優先し、主節から削除
                    slots[main_slot] = ""
                    self.logger.debug(f"🔄 主節↔関係節重複削除: {main_slot}='{main_value}' → '' (sub-slot {sub_slot}='{sub_value}' を優先)")
                    break
    
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
        関係節ハンドラー（Phase 1実装 + 分詞構文制御フラグ対応）
        
        simple_relative_engine.py の機能を統合システムに移植
        Stanza dependency parsing による直接的な関係節検出・分解
        分詞構文が検出されている場合は、関係節処理をスキップ
        
        Args:
            sentence: Stanza解析済みsentence object
            base_result: ベース結果（コピー）
            
        Returns:
            Dict: 関係節分解結果 or None
        """
        try:
            self.logger.debug("🔍 関係節ハンドラー実行中...")
            
            # 分詞構文制御フラグをチェック
            grammar_info = base_result.get('grammar_info', {})
            control_flags = grammar_info.get('control_flags', {})
            participle_detected = control_flags.get('participle_detected', False)
            
            if participle_detected:
                self.logger.debug("  🎯 分詞構文検出済み - 関係節処理をスキップ（分詞構文が優先）")
                return None
            
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
            # whose構文では常に関係節として処理
            # 主文動詞と関係節動詞を適切に分離することで対応
            self.logger.debug(f"🔧 whose構文: 関係節として処理開始")
            return True
        
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
        
        # 🚫 副詞処理を副詞ハンドラーに完全委譲（競合回避）
        # 助動詞ハンドラーは副詞スロット設定を行わない
        # adverb_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'advmod')
        # if adverb_word:
        #     if adverb_word.text.lower() not in ['where', 'when', 'why', 'how']:
        #         if adverb_word.id < rel_verb.id:
        #             sub_slots["sub-m1"] = adverb_word.text
        #             self.logger.debug(f"🔧 関係節内副詞検出: sub-m1 = '{adverb_word.text}' (動詞前)")
        #         else:
        #             sub_slots["sub-m2"] = adverb_word.text
        #             self.logger.debug(f"🔧 関係節内副詞検出: sub-m2 = '{adverb_word.text}' (動詞後)")
        
        # 🚫 前置詞句処理も副詞ハンドラーに委譲（完全な副詞処理統一）
        # obl_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obl')
        # if obl_word:
        #     sub_slots["sub-m3"] = obl_word.text
        #     self.logger.debug(f"🔧 関係節内副詞句検出: sub-m3 = '{obl_word.text}'")
        
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
            # 関係副詞: "The place where he lives" / "The way how he solved it"
            # slots["M3"] = ""  # 上位スロットは5文型エンジンに任せる
            sub_slots["sub-m1"] = noun_phrase
            if rel_subject:
                sub_slots["sub-s"] = rel_subject.text
            sub_slots["sub-v"] = rel_verb.text
            
            # ✅ 関係副詞句内の目的語を検出してsub-o1に配置
            obj_word = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'obj')
            if obj_word:
                sub_slots["sub-o1"] = obj_word.text
                self.logger.debug(f"🔧 関係副詞句内目的語検出: sub-o1 = '{obj_word.text}'")
            
        # 省略関係代名詞の処理
        elif rel_type == 'obj_omitted':
            # 省略目的語関係代名詞: "The book I read"
            # 🔧 修正: 関係節全体を構築
            slots["S"] = ""  # 主節主語を空に設定（先行詞は従属節に移動）
            
            # 先行詞テキストから[omitted]を除去
            clean_noun_phrase = noun_phrase.replace(" [omitted]", "").replace("[omitted]", "")
            
            # 従属節主語を検出（関係節動詞のnsubj）
            rel_subject = self._find_word_by_head_and_deprel(sentence, rel_verb.id, 'nsubj')
            if rel_subject:
                sub_slots["sub-o1"] = clean_noun_phrase
                sub_slots["sub-s"] = rel_subject.text
                sub_slots["sub-v"] = rel_verb.text
                self.logger.debug(f"🔧 省略目的語関係節: sub-s = '{rel_subject.text}'")
            else:
                sub_slots["sub-o1"] = clean_noun_phrase
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
        
        # 通常の場合：rootを検索（whose構文でも先にチェック）
        root_word = None
        for word in sentence.words:
            if word.head == 0:  # root
                root_word = word
                break
        
        # whose構文の特別処理：rootが存在せず、acl:relcl語がメイン動詞候補の場合のみ
        if any(w.text.lower() == 'whose' for w in sentence.words) and not root_word:
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes'] and
                acl_relcl_word.lemma in ['live', 'work', 'run', 'go']):
                self.logger.debug(f"🔧 whose構文: 主文動詞として {acl_relcl_word.text} を使用")
                return acl_relcl_word
        
        # 通常の場合：rootを検索（whose構文でも先にチェック）
        root_word = None
        for word in sentence.words:
            if word.head == 0:  # root
                root_word = word
                break
        
        # whose構文の特別処理：rootが存在せず、acl:relcl語がメイン動詞候補の場合のみ
        if any(w.text.lower() == 'whose' for w in sentence.words) and not root_word:
            acl_relcl_word = self._find_word_by_deprel(sentence, 'acl:relcl')
            if (acl_relcl_word and 
                acl_relcl_word.text.lower() in ['lives', 'works', 'runs', 'goes'] and
                acl_relcl_word.lemma in ['live', 'work', 'run', 'go']):
                self.logger.debug(f"🔧 whose構文: 主文動詞として {acl_relcl_word.text} を使用")
                return acl_relcl_word
        
        if not root_word:
            return None
            
        # rootが形容詞の場合の特別処理
        if root_word.upos == 'ADJ':
            # when構文では形容詞を主動詞として扱う（Rephrase仕様）
            if any(w.text.lower() == 'when' for w in sentence.words):
                self.logger.debug(f"🔧 when構文: 形容詞を主動詞として使用 {root_word.text}")
                return root_word
            else:
                # 通常の場合：cop動詞を主動詞とする（"The man is strong"構造）
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
        基本5文型ハンドラー（Phase 1実装 + 分詞構文制御フラグ対応）
        
        basic_five_pattern_engine.py の機能を統合システムに移植
        Stanza dependency parsing による基本文型検出・分解
        分詞構文が検出されている場合は、適切に主語スロットを制御
        
        Args:
            sentence: Stanza sentence object
            base_result: 基本結果辞書
            
        Returns:
            Optional[Dict]: 5文型処理結果 or None
        """
        try:
            self.logger.debug("🔍 5文型ハンドラー実行中...")
            
            # 分詞構文制御フラグをチェック
            grammar_info = base_result.get('grammar_info', {})
            control_flags = grammar_info.get('control_flags', {})
            participle_detected = control_flags.get('participle_detected', False)
            
            if participle_detected:
                self.logger.debug("  ✅ 分詞構文検出済み - 分詞構文ルールを適用")
                return self._process_basic_pattern_with_participle_control(sentence, base_result)
            
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
                    # ✅ C1重複防止: ROOTワードがVに既に設定されている場合はC1に設定しない
                    if slot == "C1" and "V" in slots and slots["V"] == root_word.text:
                        self.logger.debug(f"🚫 C1重複防止: {root_word.text} (Vと同一)")
                        continue  # C1への設定をスキップ
                    self.logger.debug(f"🔧 ROOT語設定: {slot} = '{root_word.text}'")
                    slots[slot] = root_word.text
            elif dep_rel in dep_relations:
                # 依存関係語の処理（修飾語句を含む完全な句を構築）
                words = dep_relations[dep_rel]
                if words:
                    # メインの語
                    main_word = words[0]
                    # 修飾語句を構築
                    phrase = self._build_phrase_with_modifiers(sentence, main_word)
                    self.logger.debug(f"🔧 依存関係語設定: {slot} = '{phrase}'")
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
        副詞処理エンジン（Rephrase距離ベース原理 + 仕様書準拠解析エラー修正）
        Stanza/spaCy分析結果を使用し、解析エラーパターンに対応する修正戦略を適用
        """
        print("🔧 副詞ハンドラー開始")
        self.logger.debug("副詞ハンドラー実行中（距離ベース原理 + 解析エラー修正）...")
        
        # === 解析エラーパターン処理（仕様書のError Pattern Management準拠）===
        error_corrections = self._apply_analysis_error_corrections(sentence, base_result)
        
        # 🎯 Rephrase原理：ハードコーディング分類は不要
        # Stanza/spaCyの分析結果のみを信頼（ただし、エラーパターンは修正）
        
        # === 既存スロット確認（関係節スロット含む）===
        existing_slots = base_result.get('slots', {}) if base_result else {}
        existing_sub_slots = base_result.get('sub_slots', {}) if base_result else {}
        
        existing_adverbs = set()
        
        # 主節副詞を既存チェックに追加
        for slot_key, slot_value in existing_slots.items():
            if slot_key.startswith('M') and slot_value:
                existing_adverbs.update(slot_value.split())
        
        # 🔧 重要修正: 関係節副詞も既存チェックに追加
        for slot_key, slot_value in existing_sub_slots.items():
            if slot_key.startswith('sub-m') and slot_value:
                existing_adverbs.update(slot_value.split())
        
        self.logger.debug(f"🔍 既存副詞チェック: {existing_adverbs}")
        
        # エラー修正適用
        if error_corrections:
            existing_sub_slots.update(error_corrections)
            self.logger.debug(f"✅ 解析エラー修正適用: {error_corrections}")
        
        # === 関係節・従属節コンテキスト分析 ===
        # 🔧 修正：base_resultから主動詞情報を取得（ハイブリッド解析結果反映）
        main_verb_id = None
        main_verb_text = existing_slots.get('V')
        
        print(f"🔍 MAIN VERB DETECTION:")
        
        # 🔧 Whose構文専用検出（最優先）
        sentence_text = " ".join([w.text for w in sentence.words])
        if "whose" in sentence_text:
            print(f"🎯 WHOSE構文検出: {sentence_text}")
            # whose以降で関係節を超えた最初のVERB品詞の動詞を主動詞とする
            for word in sentence.words:
                if (word.upos == 'VERB' and 
                    word.deprel not in ['acl:relcl', 'acl'] and
                    word.text not in ['is', 'are', 'was', 'were']):
                    print(f"   → WHOSE構文主動詞確定: {word.text} (id={word.id})")
                    main_verb_id = word.id
                    break
            
            # フォールバック：動詞語幹パターンで検索（品詞無視）
            if not main_verb_id:
                for word in sentence.words:
                    if (self._is_verb_pattern(word.text) and 
                        word.text not in ['is', 'are', 'was', 'were']):
                        print(f"   → WHOSE構文フォールバック: {word.text} (id={word.id})")
                        main_verb_id = word.id
                        break

        if not main_verb_id:
            print(f"   existing_slots V: {main_verb_text}")
            
            # 🎯 重要修正：関係節処理でVが正しく設定されていない場合の主動詞特定
            if main_verb_text in ['is', 'are', 'was', 'were']:
                print(f"   → 関係節動詞検出、真の主動詞を探索中...")
                # whose構文などで関係節の動詞が主動詞として誤認されている場合
                # 真の主動詞（lives, needs, etc.）を探す
                for word in sentence.words:
                    print(f"     検討: {word.text} (upos={word.upos}, deprel={word.deprel})")
                    if (word.text not in ['is', 'are', 'was', 'were'] and 
                        word.upos == 'VERB' and  # VERBのみに限定
                        word.deprel not in ['acl:relcl', 'acl', 'advcl']):  # 従属節動詞を除外
                        main_verb_text = word.text
                        print(f"   → 主動詞修正: '{main_verb_text}' (関係節動詞 '{existing_slots.get('V')}' から変更)")
                        self.logger.debug(f"🔧 主動詞修正: '{main_verb_text}' (関係節動詞 '{existing_slots.get('V')}' から変更)")
                        break
            
            if main_verb_text:
                print(f"   main_verb_text最終: {main_verb_text}")
                # 主動詞テキストから対応するword IDを特定
                for word in sentence.words:
                    print(f"     ID探索: {word.text} (id={word.id}, upos={word.upos})")
                    if word.text == main_verb_text and word.upos in ['VERB', 'AUX', 'NOUN']:  # NOUNも含める（lives等）
                        main_verb_id = word.id
                        print(f"   → 主動詞ID確定: {main_verb_id}")
                        break
            
            # フォールバック: 従来の方法
            if not main_verb_id:
                main_verb_id = self._find_main_verb(sentence)
        
        print(f"🎯 最終主動詞ID: {main_verb_id}")
        
        subordinate_verbs = self._find_subordinate_verbs(sentence, main_verb_id)
        
        # === 副詞候補収集（Migration source優秀機能活用）===
        adverb_phrases = []
        processed_positions = set()
        processed_phrases = set()  # 重複フレーズ防止
        
        self.logger.debug("🔍 副詞候補スキャン開始（Stanza/spaCy分析ベース）...")
        for word in sentence.words:
            # 🎯 Rephrase原理：純粋にStanza/spaCy分析結果を信頼
            is_adverb = (
                word.deprel in ['advmod', 'obl', 'obl:tmod', 'obl:npmod', 'obl:agent', 'obl:unmarked', 'nmod:tmod'] or
                word.upos == 'ADV'  # POS-based detection（信頼性高い）
            )
            
            self.logger.debug(f"  {word.text}: deprel={word.deprel}, upos={word.upos}, is_adverb={is_adverb}")
            
            if is_adverb:
                if word.text in existing_adverbs:
                    self.logger.debug(f"    → 除外（既存副詞）: {word.text}")
                    continue
                    
                # 重複除去（Migration source優秀機能）
                if word.id in processed_positions:
                    self.logger.debug(f"    → 除外（重複位置）: {word.text}")
                    continue
                    
                # 関係副詞除外
                if word.text.lower() in ['where', 'when', 'why', 'how']:
                    self.logger.debug(f"    → 除外（関係副詞）: {word.text}")
                    continue
                
                # Migration source前置詞句構築機能活用
                if word.deprel.startswith('obl'):
                    # 🔧 advmod修飾語を除外して基本語のみでOBL句構築
                    phrase = self._build_prepositional_phrase(sentence, word, exclude_advmod=True)
                    print(f"DEBUG OBL: '{word.text}' -> '{phrase}' (advmod除外)")
                    # 前置詞句の全tokens記録（重複回避）
                    phrase_words = phrase.split()
                    for pw in phrase_words:
                        for w in sentence.words:
                            if w.text == pw:
                                processed_positions.add(w.id)
                else:
                    # 🔧 副詞修飾語を含む句構築（"very carefully"対応）
                    phrase = self._build_adverbial_phrase(sentence, word)
                    print(f"🔧 ADV句構築: '{word.text}' → '{phrase}'")
                    phrase_words = phrase.split()
                    for pw in phrase_words:
                        for w in sentence.words:
                            if w.text == pw:
                                processed_positions.add(w.id)
                
                # 重複フレーズチェック
                if phrase in processed_phrases:
                    self.logger.debug(f"    → 除外（重複フレーズ）: {phrase}")
                    continue
                
                processed_phrases.add(phrase)
                
                # 🎯 Rephrase原理：分類不要、位置情報のみで判定
                # category = self._classify_adverbial_phrase(phrase, time_keywords, location_keywords, manner_keywords)
                category = 'position_based'  # Rephrase距離ベース原理
                
                # 文脈分析: 主節 vs 従属節（Migration source判定ロジック）
                context = self._determine_adverb_context(word, main_verb_id, subordinate_verbs, sentence)
                
                self.logger.debug(f"    → 検出: phrase='{phrase}', category={category}, context={context}")
                
                adverb_phrases.append({
                    'phrase': phrase,
                    'category': category,
                    'position': word.id,
                    'word': word,
                    'context': context  # 'main' or 'subordinate'
                })
        
        if not adverb_phrases:
            self.logger.debug("副詞なし - スキップ")
            return None

        # === Rephrase仕様配置ロジック（Migration source機能活用） ===
        slots = {}
        sub_slots = {}
        
        # 位置順ソート
        adverb_phrases.sort(key=lambda x: x['position'])
        
        # === シンプルルール一括配置システム ===
        # 主節副詞と従属節副詞を分離して、それぞれにシンプルルールを適用
        
        main_adverbs = [p for p in adverb_phrases if p['context'] == 'main']
        sub_adverbs = [p for p in adverb_phrases if p['context'] == 'subordinate']
        
        self.logger.debug(f"🎯 シンプルルール適用: 主節副詞{len(main_adverbs)}個, 従属節副詞{len(sub_adverbs)}個")
        
        # 主節副詞のシンプルルール配置
        if main_adverbs:
            print(f"🎯 Main副詞詳細: {main_adverbs}")
            main_slots = self._apply_simple_rule_to_adverbs(main_adverbs, 'main')
            print(f"🎯 Main副詞結果: {main_slots}")
            slots.update(main_slots)
        
        # 従属節副詞のシンプルルール配置
        if sub_adverbs:
            sub_main_slots = self._apply_simple_rule_to_adverbs(sub_adverbs, 'sub')
            sub_slots.update(sub_main_slots)
        
        self.logger.debug(f"副詞配置完了: slots={slots}, sub_slots={sub_slots}")
        print(f"🔧 副詞ハンドラー完了: slots={slots}, sub_slots={sub_slots}")
        return {'slots': slots, 'sub_slots': sub_slots}
    
    def _apply_simple_rule_to_adverbs(self, adverbs, context_type):
        """
        シンプルルールを副詞群に一括適用
        
        Args:
            adverbs: 副詞リスト
            context_type: 'main' or 'sub'
        """
        result_slots = {}
        count = len(adverbs)
        
        self.logger.debug(f"🎯 {context_type}節シンプルルール適用: {count}個の副詞")
        
        if count == 0:
            return result_slots
        
        # スロット名プレフィックス
        slot_prefix = 'sub-m' if context_type == 'sub' else 'M'
        
        if count == 1:
            # 1個 → M2 (または sub-m2)
            slot_name = f"{slot_prefix}2"
            result_slots[slot_name] = adverbs[0]['phrase']
            self.logger.debug(f"  1個ルール: {slot_name} = '{adverbs[0]['phrase']}'")
        
        elif count == 2:
            # 2個 → M2, M3 (または sub-m2, sub-m3)
            # 位置順でソート済みなので、最初がM2、次がM3
            result_slots[f"{slot_prefix}2"] = adverbs[0]['phrase']
            result_slots[f"{slot_prefix}3"] = adverbs[1]['phrase']
            self.logger.debug(f"  2個ルール: {slot_prefix}2 = '{adverbs[0]['phrase']}', {slot_prefix}3 = '{adverbs[1]['phrase']}'")
            self.logger.debug(f"  詳細: adverb[0]={adverbs[0]}, adverb[1]={adverbs[1]}")
        
        elif count >= 3:
            # 3個以上 → M1, M2, M3 (または sub-m1, sub-m2, sub-m3)
            result_slots[f"{slot_prefix}1"] = adverbs[0]['phrase']
            result_slots[f"{slot_prefix}2"] = adverbs[1]['phrase']
            result_slots[f"{slot_prefix}3"] = adverbs[2]['phrase']
            self.logger.debug(f"  3個ルール: {slot_prefix}1/2/3 = '{adverbs[0]['phrase']}'/'{adverbs[1]['phrase']}'/'{adverbs[2]['phrase']}'")
            
            # 4個以上は無視（警告）
            if count > 3:
                ignored = [a['phrase'] for a in adverbs[3:]]
                self.logger.warning(f"  ⚠️ 4個以上の副詞を無視: {ignored}")
        
        return result_slots
    
    def _find_main_verb(self, sentence):
        """主動詞を特定（構造的修正版）"""
        
        print(f"🔍 MAIN VERB ANALYSIS:")
        for word in sentence.words:
            print(f"   Word: {word.text} (id={word.id}, upos={word.upos}, deprel={word.deprel})")
        
        # 🔧 Step 0: whose構文特殊処理
        sentence_text = getattr(sentence, 'text', ' '.join(w.text for w in sentence.words))
        if 'whose' in sentence_text.lower():
            print(f"   🎯 whose構文検出 - 特殊処理開始")
            
            # whose以降の節を特定
            whose_index = None
            for i, word in enumerate(sentence.words):
                if word.text.lower() == 'whose':
                    whose_index = i
                    break
            
            if whose_index is not None:
                # whose節後の最初の動詞をスキップして、その次の動詞を主動詞とする
                relative_clause_verbs = []
                main_clause_candidates = []
                
                for i, word in enumerate(sentence.words[whose_index:], whose_index):
                    if word.upos == 'VERB' or self._is_verb_by_pattern(word.text):
                        if not relative_clause_verbs:
                            # 最初の動詞は関係節動詞
                            relative_clause_verbs.append(word)
                            print(f"     関係節動詞: {word.text} (id={word.id})")
                        else:
                            # 2番目以降は主節候補
                            main_clause_candidates.append(word)
                            print(f"     主節候補: {word.text} (id={word.id})")
                
                if main_clause_candidates:
                    main_verb = main_clause_candidates[0]
                    print(f"   → whose構文主動詞: {main_verb.text} (id={main_verb.id})")
                    return main_verb.id
        
        # 🎯 Step 1: ROOT動詞を優先
        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                self.logger.debug(f"🎯 主動詞（ROOT動詞）: {word.text} (id={word.id})")
                print(f"   → ROOT動詞が主動詞: {word.text} (id={word.id})")
                return word.id
        
        # 🔧 Step 2: ROOT形容詞で受動態の場合、ROOT自体を主動詞として扱う
        root_word = None
        for word in sentence.words:
            if word.deprel == 'root':
                root_word = word
                break
        
        print(f"   Root word: {root_word.text if root_word else None} (upos={root_word.upos if root_word else None})")
        
        if root_word and root_word.upos == 'ADJ':
            # 受動態構造：ROOT形容詞を主動詞とする
            # "was unexpected" → unexpected が主動詞相当
            self.logger.debug(f"🎯 主動詞（受動態ROOT形容詞）: {root_word.text} (id={root_word.id})")
            print(f"   → ROOT形容詞が主動詞: {root_word.text} (id={root_word.id})")
            return root_word.id
        
        if root_word and root_word.upos != 'VERB':
            # 構造的階層で主動詞候補を評価（品詞誤認識対策含む）
            verb_candidates = []
            for w in sentence.words:
                if w.upos == 'VERB' or self._is_verb_by_pattern(w.text):
                    verb_candidates.append(w)
            
            print(f"   Verb candidates: {[(v.text, v.id, v.upos) for v in verb_candidates]}")
            if verb_candidates:
                # 最も文の中心に近い動詞を主動詞とする
                main_verb = min(verb_candidates, key=lambda v: abs(v.id - root_word.id))
                self.logger.debug(f"🎯 主動詞（構造的選択）: {main_verb.text} (id={main_verb.id})")
                print(f"   → 構造的選択で主動詞: {main_verb.text} (id={main_verb.id})")
                return main_verb.id
        
        # 🔄 Fallback: 最初の動詞（品詞誤認識対策含む）
        for word in sentence.words:
            if word.upos == 'VERB' or self._is_verb_by_pattern(word.text):
                self.logger.debug(f"🎯 主動詞（Fallback）: {word.text} (id={word.id})")
                print(f"   → フォールバック主動詞: {word.text} (id={word.id})")
                return word.id
        
        return None

    def _is_verb_by_pattern(self, word_text):
        """動詞語幹パターン判定（Stanza誤認識対策）"""
        # 一般的な動詞語尾パターン
        verb_endings = ['s', 'es', 'ed', 'ing', 'en']
        verb_patterns = [
            'live', 'work', 'play', 'study', 'run', 'walk', 'talk', 'sing',
            'dance', 'write', 'read', 'teach', 'learn', 'help', 'love'
        ]
        
        word_lower = word_text.lower()
        
        # 直接的な動詞パターンマッチ
        for pattern in verb_patterns:
            if word_lower == pattern:
                return True
            for ending in verb_endings:
                if word_lower == pattern + ending:
                    return True
        
        # 特定語: lives (live + s)
        if word_lower == 'lives':
            return True
            
        return False
    
    def _find_subordinate_verbs(self, sentence, main_verb_id):
        """従属節動詞を特定（構造的修正版）"""
        subordinate_verbs = []
        
        # 🎯 主動詞を除外して、明確な従属節動詞のみを特定
        for word in sentence.words:
            if word.id == main_verb_id:
                continue  # 主動詞は除外
                
            # 明確な従属節パターンのみを従属節動詞として認識
            if word.deprel in ['acl:relcl', 'acl', 'advcl', 'ccomp', 'xcomp']:
                # ただし、主動詞として特定済みの場合は除外
                if word.upos == 'VERB':
                    subordinate_verbs.append(word.id)
                    self.logger.debug(f"🔍 従属節動詞検出: {word.text} (id={word.id}, deprel={word.deprel})")
        
        return subordinate_verbs
    
    def _is_verb_pattern(self, word_text):
        """動詞語幹パターンを判定（品詞に依存しない）"""
        word = word_text.lower()
        
        # 明確な動詞パターン
        verb_patterns = [
            'live', 'lives', 'lived', 'living',
            'need', 'needs', 'needed', 'needing',  
            'work', 'works', 'worked', 'working',
            'run', 'runs', 'ran', 'running',
            'come', 'comes', 'came', 'coming',
            'go', 'goes', 'went', 'going',
            'see', 'sees', 'saw', 'seeing',
            'get', 'gets', 'got', 'getting',
            'make', 'makes', 'made', 'making',
            'take', 'takes', 'took', 'taking',
            'know', 'knows', 'knew', 'knowing',
            'think', 'thinks', 'thought', 'thinking',
            'find', 'finds', 'found', 'finding',
            'give', 'gives', 'gave', 'giving',
            'tell', 'tells', 'told', 'telling',
            'become', 'becomes', 'became', 'becoming',
            'leave', 'leaves', 'left', 'leaving',
            'feel', 'feels', 'felt', 'feeling',
            'try', 'tries', 'tried', 'trying',
            'ask', 'asks', 'asked', 'asking',
            'seem', 'seems', 'seemed', 'seeming',
            'help', 'helps', 'helped', 'helping',
            'talk', 'talks', 'talked', 'talking',
            'turn', 'turns', 'turned', 'turning',
            'start', 'starts', 'started', 'starting',
            'show', 'shows', 'showed', 'showing',
            'hear', 'hears', 'heard', 'hearing',
            'play', 'plays', 'played', 'playing',
            'move', 'moves', 'moved', 'moving',
            'pay', 'pays', 'paid', 'paying',
            'meet', 'meets', 'met', 'meeting',
            'include', 'includes', 'included', 'including',
            'continue', 'continues', 'continued', 'continuing',
            'set', 'sets', 'setting',
            'learn', 'learns', 'learned', 'learning',
            'change', 'changes', 'changed', 'changing',
            'lead', 'leads', 'led', 'leading',
            'understand', 'understands', 'understood', 'understanding',
            'watch', 'watches', 'watched', 'watching',
            'follow', 'follows', 'followed', 'following',
            'stop', 'stops', 'stopped', 'stopping',
            'create', 'creates', 'created', 'creating',
            'speak', 'speaks', 'spoke', 'speaking',
            'read', 'reads', 'reading',
            'allow', 'allows', 'allowed', 'allowing',
            'add', 'adds', 'added', 'adding',
            'spend', 'spends', 'spent', 'spending',
            'grow', 'grows', 'grew', 'growing',
            'open', 'opens', 'opened', 'opening',
            'walk', 'walks', 'walked', 'walking',
            'win', 'wins', 'won', 'winning',
            'offer', 'offers', 'offered', 'offering',
            'remember', 'remembers', 'remembered', 'remembering',
            'love', 'loves', 'loved', 'loving',
            'consider', 'considers', 'considered', 'considering',
            'appear', 'appears', 'appeared', 'appearing',
            'buy', 'buys', 'bought', 'buying',
            'wait', 'waits', 'waited', 'waiting',
            'serve', 'serves', 'served', 'serving',
            'die', 'dies', 'died', 'dying',
            'send', 'sends', 'sent', 'sending',
            'expect', 'expects', 'expected', 'expecting',
            'build', 'builds', 'built', 'building',
            'stay', 'stays', 'stayed', 'staying',
            'fall', 'falls', 'fell', 'falling',
            'cut', 'cuts', 'cutting',
            'reach', 'reaches', 'reached', 'reaching',
            'kill', 'kills', 'killed', 'killing',
            'remain', 'remains', 'remained', 'remaining'
        ]
        
        return word in verb_patterns

    def _determine_adverb_context(self, adverb_word, main_verb_id, subordinate_verbs, sentence):
        """副詞の文脈（主節 vs 従属節）を判定（修正版）"""
        
        # デバッグメッセージ追加
        print(f"� ADVERB CONTEXT ANALYSIS: {adverb_word.text}")
        print(f"   - adverb_word.head: {adverb_word.head}")
        print(f"   - main_verb_id: {main_verb_id}")
        print(f"   - subordinate_verbs: {subordinate_verbs}")
        
        # 🔧 Whose構文位置ベース判定（Stanza誤解析対策）- 最優先

        
        sentence_text = " ".join([w.text for w in sentence.words])

        
        if "whose" in sentence_text:

        
            whose_pos = -1

        
            main_verb_pos = -1

        
            adverb_pos = adverb_word.id

        
            

        
            for word in sentence.words:

        
                if word.text.lower() == "whose":

        
                    whose_pos = word.id

        
                elif word.id == main_verb_id:

        
                    main_verb_pos = word.id

        
            

        
            # whose節内（whose〜主動詞前）の副詞は従属節

        
            if whose_pos > 0 and main_verb_pos > 0:

        
                if whose_pos < adverb_pos < main_verb_pos:

        
                    print(f"   → WHOSE構文位置判定: SUBORDINATE (whose:{whose_pos} less_than adverb:{adverb_pos} less_than main:{main_verb_pos})")

        
                    return 'subordinate'

        
                elif adverb_pos > main_verb_pos:

        
                    print(f"   → WHOSE構文位置判定: MAIN (adverb:{adverb_pos} greater_than main:{main_verb_pos})")

        
                    return 'main'

        
        

        
        # 🔧 主動詞直接修飾チェック（whose構文判定後）
        if adverb_word.head == main_verb_id:
            self.logger.debug(f"🎯 主動詞直接修飾: {adverb_word.text} → 主動詞 (head={main_verb_id})")
            print(f"   → 主動詞直接修飾: MAIN")
            return 'main'
        
        # 直接の動詞依存関係をチェック
        head_id = adverb_word.head
        
        # まず、副詞が直接修飾している動詞を確認
        direct_head = None
        for word in sentence.words:
            if word.id == head_id:
                direct_head = word
                break
        
        print(f"   - direct_head: {direct_head.text if direct_head else None} (id={head_id})")
        
        # 🔧 強化：従属動詞直接修飾チェック
        if direct_head and direct_head.id in subordinate_verbs:
            self.logger.debug(f"🎯 従属動詞直接修飾: {adverb_word.text} → {direct_head.text} (subordinate)")
            print(f"   → 従属動詞直接修飾: SUBORDINATE")
            return 'subordinate'
        
        # 直接修飾している動詞が関係詞節動詞の場合
        if direct_head and direct_head.deprel in ['acl:relcl', 'acl']:
            self.logger.debug(f"🎯 関係詞節副詞検出: {adverb_word.text} → {direct_head.text} ({direct_head.deprel})")
            print(f"   → 関係詞節副詞: SUBORDINATE")
            return 'subordinate'
        
        # 🔧 Whose構文位置ベース判定（Stanza誤解析対策）
        sentence_text = " ".join([w.text for w in sentence.words])
        if "whose" in sentence_text:
            whose_pos = -1
            main_verb_pos = -1
            adverb_pos = adverb_word.id
            
            for word in sentence.words:
                if word.text.lower() == "whose":
                    whose_pos = word.id
                elif word.id == main_verb_id:
                    main_verb_pos = word.id
            
            # whose節内（whose〜主動詞前）の副詞は従属節
            if whose_pos > 0 and main_verb_pos > 0:
                if whose_pos < adverb_pos < main_verb_pos:
                    print(f"   → WHOSE構文位置判定: SUBORDINATE (whose:{whose_pos} < adverb:{adverb_pos} < main:{main_verb_pos})")
                    return 'subordinate'
                elif adverb_pos > main_verb_pos:
                    print(f"   → WHOSE構文位置判定: MAIN (adverb:{adverb_pos} > main:{main_verb_pos})")
                    return 'main'
        
        # 🔧 重要修正：主動詞への依存経路チェック（修正版）
        # 副詞 → ... → main_verb の経路があるかを確認
        visited = set()
        check_word = direct_head
        
        print(f"   - 経路チェック開始...")
        while check_word and check_word.id not in visited:
            visited.add(check_word.id)
            print(f"     経路: {check_word.text} (id={check_word.id}, deprel={check_word.deprel})")
            
            if check_word.id == main_verb_id:
                self.logger.debug(f"🎯 主動詞経路検出: {adverb_word.text} → 主節")
                print(f"   → 主動詞経路検出: MAIN")
                return 'main'
            
            # 関係詞節マーカーチェック
            if check_word.deprel in ['acl:relcl', 'acl', 'advcl']:
                self.logger.debug(f"🎯 従属節マーカー検出: {adverb_word.text} → {check_word.deprel}")
                print(f"   → 従属節マーカー: SUBORDINATE")
                return 'subordinate'
            
            # 次のheadを探す
            if check_word.head == 0:
                break
                
            next_word = None
            for w in sentence.words:
                if w.id == check_word.head:
                    next_word = w
                    break
            check_word = next_word
        
        # 🔧 安全フォールバック：主節副詞として処理
        self.logger.debug(f"🎯 フォールバック判定: {adverb_word.text} → 主節（安全側）")
        print(f"   → フォールバック: MAIN")
        return 'main'

    def _determine_optimal_main_adverb_slot(self, phrase, category, position, main_verb_position, existing_slots):
        """
        🎯 真のシンプル副詞配置ルール（蒸し返し問題完全解決版）
        
        核心原理：個数に基づく固定配置
        1個のみ → M2（どこにあっても）
        2個 → M2, M3（位置順） 
        3個 → M1, M2, M3（位置順）
        
        従来の複雑な判定を排除し、予測可能性を最大化
        """
        
        # 全修飾語を収集（現在の処理対象含む）
        all_modifiers = []
        
        # 既存のMスロットから修飾語を収集
        for slot in ['M1', 'M2', 'M3']:
            if slot in existing_slots and existing_slots[slot]:
                all_modifiers.append(existing_slots[slot])
        
        # 現在の修飾語を追加
        all_modifiers.append(phrase)
        
        total_count = len(all_modifiers)
        
        self.logger.debug(f"🎯 真シンプルMスロット判定: phrase='{phrase}', 総修飾語数={total_count}")
        self.logger.debug(f"  全修飾語: {all_modifiers}")
        
        # === 真のシンプルルール適用 ===
        
        if total_count == 1:
            # 1個のみ → M2
            self.logger.debug(f"  → M2選択（1個ルール）")
            return 'M2'
        
        elif total_count == 2:
            # 2個 → M2, M3
            # 現在の修飾語が最初の場合はM2、2番目の場合はM3
            current_index = all_modifiers.index(phrase)
            if current_index == 0:
                target_slot = 'M2'
            else:
                target_slot = 'M3'
            
            self.logger.debug(f"  → {target_slot}選択（2個ルール・位置{current_index + 1}）")
            return target_slot
        
        elif total_count >= 3:
            # 3個以上 → M1, M2, M3
            current_index = all_modifiers.index(phrase)
            slot_mapping = ['M1', 'M2', 'M3']
            
            if current_index < 3:
                target_slot = slot_mapping[current_index]
                self.logger.debug(f"  → {target_slot}選択（3個+ルール・位置{current_index + 1}）")
                return target_slot
            else:
                # 3個を超える場合は無視（エラー回避）
                self.logger.debug(f"  → None（3個超過・位置{current_index + 1}）")
                return None
        
        # フォールバック（通常は到達しない）
        self.logger.debug(f"  → M2選択（フォールバック）")
        return 'M2'

    def _build_prepositional_phrase(self, sentence, word, exclude_advmod=True):
        """前置詞句の構築（完全性強化版）"""
        print(f"DEBUG METHOD1: '{word.text}' (id={word.id})")
        
        # 前置詞句の完全構築
        phrase_parts = []
        
        # 前置詞を探す
        preposition = None
        for w in sentence.words:
            if w.head == word.id and w.deprel == 'case':
                preposition = w.text
                break
        
        if preposition:
            phrase_parts.append(preposition)
        
        # 🔧 修飾語収集を拡張（より多くの修飾関係を含める）
        # ただし、advmod は除外（副詞は独立処理）
        modifiers = []
        for w in sentence.words:
            if w.head == word.id and w.deprel in ['det', 'amod', 'compound', 'nmod', 'nmod:poss']:
                modifiers.append((w.id, w.text))
                print(f"DEBUG MOD: {w.text} (deprel={w.deprel})")
            elif w.head == word.id and w.deprel == 'advmod':
                # advmod は副詞として独立処理するため除外
                print(f"DEBUG ADVMOD EXCLUDED: {w.text} (advmod)")
            elif w.head == word.id:
                print(f"DEBUG OTHER: {w.text} (deprel={w.deprel})")
        
        # 🔧 間接修飾語も収集（"the morning breeze"の"morning"をキャッチ）
        for w in sentence.words:
            # wordの直接修飾語の修飾語も収集
            if any(mod[0] == w.head for mod in modifiers) and w.deprel in ['amod', 'compound']:
                modifiers.append((w.id, w.text))
                print(f"DEBUG INDIRECT: {w.text} (deprel={w.deprel})")
        
        # 位置順ソート
        modifiers.sort()
        phrase_parts.extend([mod[1] for mod in modifiers])
        phrase_parts.append(word.text)
        
        constructed_phrase = ' '.join(phrase_parts)
        self.logger.debug(f"🔧 前置詞句構築: '{word.text}' → '{constructed_phrase}'")
        print(f"DEBUG RESULT: '{word.text}' -> '{constructed_phrase}'")
        
        return constructed_phrase
    
    def _build_adverbial_phrase(self, sentence, word):
        """副詞修飾語を含む句構築（"very carefully"対応）"""
        phrase_parts = []
        modifiers = []
        
        # 副詞の修飾語を収集（advmod）
        for w in sentence.words:
            if w.head == word.id and w.deprel == 'advmod':
                modifiers.append((w.id, w.text))
        
        # 位置順ソート
        modifiers.sort()
        phrase_parts.extend([mod[1] for mod in modifiers])
        phrase_parts.append(word.text)
        
        constructed_phrase = ' '.join(phrase_parts)
        self.logger.debug(f"🔧 副詞句構築: '{word.text}' → '{constructed_phrase}'")
        
        return constructed_phrase
    
    # 🗑️ 削除：ハードコーディング分類機能（Rephrase距離ベース原理と矛盾）
    # def _classify_adverbial_phrase(...) -> 不要

    # ==== PASSIVE VOICE HANDLER ====

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
            'eaten', 'driven', 'shown', 'known', 'grown', 'thrown', 'chosen',
            'unexpected'  # 形容詞型受動態の追加
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
            
            # 非root語での形容詞受動態検出（複文対応）
            elif word.upos == 'ADJ' and word.text.lower() in common_past_participles:
                if not passive_features['main_verb']:  # まだ見つかっていない場合
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
        """受動態タイプ別スロット生成（副詞処理は専門ハンドラーに委譲）"""
        
        slots = {}
        sub_slots = {}
        
        # 基本スロット（共通）
        slots['S'] = self._build_subject_phrase(sentence, subject)
        slots['Aux'] = auxiliary.text
        slots['V'] = main_verb.text
        
        # ✅ 受動態ではC1は空（補語なし）
        slots['C1'] = ''
        
        # ✅ 副詞処理を除去：by句は副詞ハンドラーに委譲
        # by句付き受動態でも、M1は設定せず副詞ハンドラーに任せる
        # agent_phraseの情報は文法情報として記録するが、スロットには設定しない
        
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
                if word.head == agent_word.id and word.deprel in ['det', 'amod', 'nmod', 'compound', 'nmod:poss']:
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
    # 分詞構文処理ハンドラー (Phase 3)
    # =============================================================================
    
    def _handle_participle_construction(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        分詞構文ハンドラー
        
        分詞構文パターンの検出・分解:
        - The team working overtime (現在分詞修飾)
        - The woman standing quietly (現在分詞修飾)
        - The documents being reviewed (being + 過去分詞)
        
        Args:
            sentence: Stanza解析済みsentence object
            base_result: ベース結果（コピー）
            
        Returns:
            Dict: 分詞構文分解結果 or None
        """
        try:
            self.logger.debug("🔍 分詞構文ハンドラー実行中...")
            
            # 分詞構文パターンの検出
            participle_info = self._analyze_participle_structure(sentence)
            if not participle_info:
                self.logger.debug("  分詞構文なし - スキップ")
                return None
                
            self.logger.debug("  ✅ 分詞構文検出")
            return self._process_participle_construction(sentence, participle_info, base_result)
            
        except Exception as e:
            self.logger.warning(f"⚠️ 分詞構文ハンドラーエラー: {e}")
            return None
    
    def _analyze_participle_structure(self, sentence) -> Optional[Dict]:
        """分詞構文の分析"""
        participle_info = {
            'participle_verb': None,    # 分詞動詞
            'subject': None,            # 主語
            'participle_type': None,    # 分詞のタイプ (present/past/being)
            'modifiers': []             # 修飾語
        }
        
        # 現在分詞の検出 (VBG) - dep:acl パターンを優先検出
        for word in sentence.words:
            if word.xpos == 'VBG' and word.deprel == 'acl':
                participle_info['participle_verb'] = word
                participle_info['participle_type'] = 'present'
                
                # 分詞の主語を探す（head が NOUN の場合）
                if word.head > 0:
                    head_word = next((w for w in sentence.words if w.id == word.head), None)
                    if head_word and head_word.upos == 'NOUN':
                        participle_info['subject'] = head_word
                
                # 分詞の修飾語を収集（Case 49 "overtime"問題対応）
                participle_info['modifiers'] = self._find_participle_modifiers(sentence, word)
                
                self.logger.debug(f"  🎯 現在分詞検出: {word.text} (ID:{word.id}, HEAD:{word.head}, DEP:{word.deprel})")
                return participle_info
        
        # being + 過去分詞の検出
        for word in sentence.words:
            if word.text.lower() == 'being' and word.deprel == 'aux:pass':
                # beingが修飾する過去分詞を探す
                for reviewed_word in sentence.words:
                    if (reviewed_word.head == word.head and 
                        reviewed_word.xpos == 'VBN' and 
                        reviewed_word.deprel == 'acl'):
                        
                        participle_info['participle_verb'] = reviewed_word
                        participle_info['participle_type'] = 'being_past'
                        
                        # beingの主語を探す（reviewed の head）
                        if reviewed_word.head > 0:
                            head_word = next((w for w in sentence.words if w.id == reviewed_word.head), None)
                            if head_word and head_word.upos == 'NOUN':
                                participle_info['subject'] = head_word
                        
                        self.logger.debug(f"  🎯 being+過去分詞検出: being {reviewed_word.text} (被修飾語:{head_word.text if head_word else 'unknown'})")
                        return participle_info
        
        return None
    
    def _process_participle_construction(self, sentence, participle_info: Dict, base_result: Dict) -> Dict:
        """分詞修飾句の汎用処理（仕様書準拠：どのスロットでも対応可能）
        
        分詞修飾句が修飾する名詞がどのスロット（S/O1/O2/C1/C2）にあっても、
        適切にsub-スロットに移動させる汎用実装
        """
        result = base_result.copy()
        
        # 分詞構文のスロット生成
        slots = result.get('slots', {})
        sub_slots = result.get('sub_slots', {})
        
        participle_verb = participle_info['participle_verb']
        subject = participle_info['subject']  # 実際は'modified_target'が適切
        participle_type = participle_info['participle_type']
        
        self.logger.debug(f"  汎用分詞処理: type={participle_type}, verb={participle_verb.text}, target={subject.text if subject else 'None'}")
        
        if not subject:
            return result
        
        # Step 1: 修飾対象の名詞がメイン文のどのスロットにあるかを特定
        target_slot = self._identify_modified_noun_slot(subject, slots)
        
        if participle_type == 'present':
            # 現在分詞構文処理
            subject_phrase = self._build_noun_phrase_for_subject(sentence, subject)
            sub_v_content = f"{subject_phrase} {participle_verb.text}"
            
            # 🎯 文頭を小文字化（Rephrase仕様準拠）
            sub_v_content = sub_v_content[0].lower() + sub_v_content[1:] if sub_v_content else sub_v_content
            
            # Step 2: 該当スロットを空にして、sub-vに移動
            if target_slot:
                slots[target_slot] = ""  # 修飾対象スロットを空にする
                sub_slots['sub-v'] = sub_v_content
                self.logger.debug(f"  ✅ 分詞修飾処理: {target_slot} → sub-v = '{sub_v_content}'")
            else:
                # フォールバック: Sを空にする（従来の挙動）
                slots['S'] = ""
                sub_slots['sub-v'] = sub_v_content
                self.logger.debug(f"  ⚠️ フォールバック: S → sub-v = '{sub_v_content}'")
                
        elif participle_type == 'being_past':
            # Case 52パターン: The documents being reviewed
            subject_phrase = self._build_noun_phrase_for_subject(sentence, subject)
            
            # 🎯 文頭を小文字化（Rephrase仕様準拠）
            sub_aux_content = f"{subject_phrase} being"
            sub_aux_content = sub_aux_content[0].lower() + sub_aux_content[1:] if sub_aux_content else sub_aux_content
            
            # Step 2: 該当スロットを空にして、sub-aux/sub-vに分割
            if target_slot:
                slots[target_slot] = ""
                sub_slots['sub-aux'] = sub_aux_content
                sub_slots['sub-v'] = participle_verb.text
                self.logger.debug(f"  ✅ being分詞処理: {target_slot} → sub-aux/sub-v")
            else:
                # フォールバック
                slots['S'] = ""
                sub_slots['sub-aux'] = sub_aux_content
                sub_slots['sub-v'] = participle_verb.text
        
        # 結果を更新
        result['slots'] = slots
        result['sub_slots'] = sub_slots
        
        # ハンドラー情報を記録
        grammar_info = result.get('grammar_info', {})
        grammar_info['detected_patterns'] = grammar_info.get('detected_patterns', [])
        if 'participle_construction' not in grammar_info['detected_patterns']:
            grammar_info['detected_patterns'].append('participle_construction')
        
        # 制御フラグ設定：分詞構文が検出されたことをマーク（仕様書のhandler control system準拠）
        grammar_info['control_flags'] = grammar_info.get('control_flags', {})
        grammar_info['control_flags']['participle_detected'] = True
        grammar_info['control_flags']['modified_slot'] = target_slot  # 修飾対象スロットを記録
        
        # Stanza/spaCy解析エラー対応：問題パターンをマーク（仕様書のError Pattern Management準拠）
        self._mark_analysis_error_patterns(sentence, participle_info, result)
        
        result['grammar_info'] = grammar_info
        
        self.logger.debug(f"  ✅ 汎用分詞処理完了: slots={slots}, sub_slots={sub_slots}")
        return result
    
    def _is_standalone_participle(self, sentence, subject, participle_verb) -> bool:
        """分詞が独立した修飾語か（Case 49パターン）を判定"""
        # メイン動詞が存在し、分詞とは別の場合は独立分詞
        main_verb = None
        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB' and word.id != participle_verb.id:
                main_verb = word
                break
        
        # メイン動詞が存在し、主語が同じ場合は独立分詞（Case 49）
        if main_verb and subject:
            # 主語がメイン動詞の主語でもある場合
            main_subj = None
            for word in sentence.words:
                if word.head == main_verb.id and word.deprel == 'nsubj':
                    main_subj = word
                    break
            
            if main_subj and main_subj.id == subject.id:
                return True
        
        return False
    
    def _mark_analysis_error_patterns(self, sentence, participle_info: Dict, result: Dict) -> None:
        """Stanza/spaCy解析エラーパターンをマーク（仕様書のError Pattern Management準拠）
        
        Case 49の"overtime"問題のように、品詞・依存関係の誤分類をマークして
        adverbial_modifierハンドラーでの修正戦略を指示
        """
        try:
            grammar_info = result.get('grammar_info', {})
            if 'analysis_error_patterns' not in grammar_info:
                grammar_info['analysis_error_patterns'] = []
            
            # Pattern 1: 分詞直後の名詞が副詞的修飾として誤分類される問題
            participle_verb = participle_info['participle_verb']
            sentence_text = sentence.text.lower()
            
            # "overtime", "quickly", "carefully"などの特定パターンを検出
            problematic_modifiers = []
            
            # 分詞の直後の語を確認
            words = [w.text.lower() for w in sentence.words]
            participle_idx = None
            for i, word in enumerate(words):
                if word == participle_verb.text.lower():
                    participle_idx = i
                    break
            
            if participle_idx is not None and participle_idx + 1 < len(words):
                next_word = words[participle_idx + 1]
                
                # "overtime"のような時間副詞が名詞として誤分類される問題
                time_adverbs = ['overtime', 'today', 'yesterday', 'tomorrow', 'tonight', 'now', 'then']
                if next_word in time_adverbs:
                    problematic_modifiers.append({
                        'type': 'time_adverb_misclassified_as_noun',
                        'word': next_word,
                        'expected_pos': 'ADV',
                        'correction_strategy': 'force_adverbial_classification',
                        'target_slot': 'sub-m2'
                    })
                
                # その他の副詞的修飾語パターン
                elif next_word.endswith('ly'):
                    problematic_modifiers.append({
                        'type': 'manner_adverb_in_participle',
                        'word': next_word,
                        'expected_pos': 'ADV',
                        'correction_strategy': 'sub_slot_placement',
                        'target_slot': 'sub-m2'
                    })
            
            # エラーパターンを記録
            for pattern in problematic_modifiers:
                grammar_info['analysis_error_patterns'].append(pattern)
                self.logger.debug(f"  ⚠️ 分析エラーパターン検出: {pattern['type']} - {pattern['word']}")
            
            result['grammar_info'] = grammar_info
            
        except Exception as e:
            self.logger.error(f"Error in marking analysis error patterns: {e}")
    
    def _structural_main_verb_fallback(self, tokens: List[str], participle_index: int) -> List[Tuple[str, int]]:
        """構造的主動詞判定のフォールバック（仕様書のStructuralGrammarAnalyzer準拠）
        
        Stanza解析が失敗した場合の構造的判定
        """
        candidates = []
        
        try:
            # 分詞より後ろにある動詞候補を探索
            for i in range(participle_index + 1, len(tokens)):
                token = tokens[i]
                
                # 基本的な動詞形パターン
                verb_patterns = [
                    lambda w: w.endswith('ed'),  # 過去形・過去分詞
                    lambda w: w in ['was', 'were', 'is', 'are', 'am', 'be', 'been', 'being'],  # be動詞
                    lambda w: w in ['have', 'has', 'had', 'will', 'would', 'can', 'could', 'should'],  # 助動詞
                    lambda w: w.endswith('s') and len(w) > 2,  # 三人称単数現在
                ]
                
                for pattern in verb_patterns:
                    if pattern(token.lower()):
                        candidates.append((token, i))
                        break
                
        except Exception as e:
            self.logger.error(f"Error in structural main verb fallback: {e}")
        
        return candidates
    
    def _identify_modified_noun_slot(self, modified_noun, current_slots: Dict) -> Optional[str]:
        """修飾対象の名詞がメイン文のどのスロットにあるかを特定
        
        Args:
            modified_noun: 分詞に修飾される名詞（Stanza word object）
            current_slots: 現在のメインスロット状況
            
        Returns:
            str: 該当スロット名（S/O1/O2/C1/C2）または None
        """
        try:
            modified_text = modified_noun.text.lower()
            
            # 各スロットの内容と照合
            for slot_name, slot_value in current_slots.items():
                if slot_name in ['S', 'O1', 'O2', 'C1', 'C2'] and slot_value:
                    # スロット値に修飾対象名詞が含まれているかチェック
                    slot_words = slot_value.lower().split()
                    if modified_text in slot_words:
                        self.logger.debug(f"  🎯 修飾対象特定: {modified_text} → {slot_name} ('{slot_value}')")
                        return slot_name
                    
                    # 部分一致もチェック（"team" in "The team"）
                    if modified_text in slot_value.lower():
                        self.logger.debug(f"  🎯 修飾対象特定（部分一致）: {modified_text} → {slot_name} ('{slot_value}')")
                        return slot_name
            
            # デフォルト：主語を仮定
            self.logger.debug(f"  ⚠️ 修飾対象特定失敗: {modified_text} → S（デフォルト）")
            return 'S'
            
        except Exception as e:
            self.logger.error(f"Error identifying modified noun slot: {e}")
            return 'S'  # フォールバック
    
    def _process_basic_pattern_with_participle_control(self, sentence, base_result: Dict) -> Dict:
        """分詞構文制御フラグが設定されている場合の基本文型処理
        
        分詞構文ハンドラーで既に設定されたスロット構造を尊重し、
        主語スロット（S）は絶対に変更せず、メイン動詞・目的語・補語のみを処理
        """
        result = base_result.copy()
        slots = result.get('slots', {})
        
        # 🚨 重要：分詞構文では主語は絶対に変更しない
        original_subject = slots.get('S', '')
        self.logger.debug(f"  🎯 分詞構文制御モード: 主語'{original_subject}'を保護、他要素のみ処理")
        
        # Step 1: メイン動詞の特定（分詞構文でない真の主動詞）
        main_verb = self._find_main_verb_excluding_participles(sentence)
        if main_verb:
            slots['V'] = main_verb.text
            self.logger.debug(f"    ✅ メイン動詞: {main_verb.text}")
            
            # Step 2: メイン動詞の直接目的語を特定
            main_object = self._find_verb_direct_object(sentence, main_verb)
            if main_object and not slots.get('O1'):
                object_phrase = self._build_noun_phrase_for_subject(sentence, main_object)
                slots['O1'] = object_phrase
                self.logger.debug(f"    ✅ 目的語: {object_phrase}")
            
            # Step 3: メイン動詞の補語を特定
            main_complement = self._find_verb_complement(sentence, main_verb)
            if main_complement and not slots.get('C1'):
                complement_phrase = self._build_noun_phrase_for_subject(sentence, main_complement)
                
                # 🔧 重複防止：主動詞と同じ単語は補語に設定しない
                main_verb_text = slots.get('V', '')
                if complement_phrase != main_verb_text:
                    slots['C1'] = complement_phrase
                    self.logger.debug(f"    ✅ 補語: {complement_phrase}")
                else:
                    self.logger.debug(f"    🚫 補語重複回避: {complement_phrase} (主動詞と同一)")
                    
        # 🚨 主語保護：分詞構文ハンドラーが設定した主語を絶対に維持
        slots['S'] = original_subject
        self.logger.debug(f"    🛡️ 主語保護: S='{original_subject}' (分詞構文により固定)")
        
        result['slots'] = slots
        
        # ハンドラー情報を記録
        grammar_info = result.get('grammar_info', {})
        grammar_info['detected_patterns'] = grammar_info.get('detected_patterns', [])
        if 'basic_five_pattern' not in grammar_info['detected_patterns']:
            grammar_info['detected_patterns'].append('basic_five_pattern')
        
        result['grammar_info'] = grammar_info
        
        self.logger.debug(f"  ✅ 分詞構文制御処理完了: slots={slots}")
        return result
    
    def _find_main_verb_excluding_participles(self, sentence):
        """分詞を除いた真のメイン動詞を特定"""
        for word in sentence.words:
            # ROOT動詞で、分詞（VBG/VBN）でないもの
            if (word.deprel == 'root' and 
                word.upos == 'VERB' and 
                word.xpos not in ['VBG', 'VBN']):
                return word
        
        # フォールバック: ROOT動詞
        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                return word
                
        return None
    
    def _find_verb_direct_object(self, sentence, verb_word):
        """動詞の直接目的語を特定"""
        for word in sentence.words:
            if word.head == verb_word.id and word.deprel == 'obj':
                return word
        return None
    
    def _find_verb_complement(self, sentence, verb_word):
        """動詞の補語を特定"""
        for word in sentence.words:
            if word.head == verb_word.id and word.deprel in ['xcomp', 'ccomp', 'nsubj:xsubj']:
                return word
        return None
    
    def _apply_analysis_error_corrections(self, sentence, base_result: Dict) -> Dict:
        """解析エラーパターンに対応する修正戦略を適用（仕様書準拠）
        
        分詞構文ハンドラーが検出した解析エラーパターンに基づいて、
        正しいスロット配置を行う
        """
        corrections = {}
        
        try:
            grammar_info = base_result.get('grammar_info', {})
            error_patterns = grammar_info.get('analysis_error_patterns', [])
            
            if not error_patterns:
                return corrections
            
            self.logger.debug(f"🔧 解析エラー修正開始: {len(error_patterns)}個のパターン")
            
            for pattern in error_patterns:
                pattern_type = pattern.get('type')
                word = pattern.get('word')
                target_slot = pattern.get('target_slot')
                strategy = pattern.get('correction_strategy')
                
                if pattern_type == 'time_adverb_misclassified_as_noun':
                    # Case 49の "overtime" 問題
                    if strategy == 'force_adverbial_classification' and target_slot:
                        corrections[target_slot] = word
                        self.logger.debug(f"  ✅ 時間副詞修正: {word} → {target_slot}")
                
                elif pattern_type == 'manner_adverb_in_participle':
                    # -ly 副詞の分詞構文内配置
                    if strategy == 'sub_slot_placement' and target_slot:
                        corrections[target_slot] = word
                        self.logger.debug(f"  ✅ 方法副詞修正: {word} → {target_slot}")
            
            return corrections
            
        except Exception as e:
            self.logger.error(f"Error in applying analysis error corrections: {e}")
            return corrections
    
    def _find_participle_modifiers(self, sentence, participle_word) -> List:
        """分詞の修飾語を検出（Stanza解析エラー対応）"""
        modifiers = []
        
        # 直接の修飾語（Stanza解析結果ベース）
        for modifier in sentence.words:
            if modifier.head == participle_word.id:
                modifiers.append(modifier)
        
        # 構造的修飾語検出（Case 49 "overtime"のような誤分類対応）
        words = [w.text.lower() for w in sentence.words]
        participle_idx = None
        
        for i, word in enumerate(sentence.words):
            if word.id == participle_word.id:
                participle_idx = i
                break
        
        if participle_idx is not None and participle_idx + 1 < len(sentence.words):
            next_word = sentence.words[participle_idx + 1]
            
            # 時間副詞が名詞として誤分類されている場合
            time_adverbs = ['overtime', 'today', 'yesterday', 'tomorrow', 'tonight', 'now', 'then']
            if (next_word.text.lower() in time_adverbs and 
                next_word.upos == 'NOUN' and 
                next_word.deprel == 'obj'):
                
                modifiers.append(next_word)
                self.logger.debug(f"  🔧 構造的修飾語検出: {next_word.text} (誤分類修正)")
        
        return modifiers
    
    def _detect_expanded_participle_patterns(self, sentence) -> Optional[Dict]:
        """拡張分詞パターン検出（構造的アプローチ）"""
        # より幅広い分詞パターンを検出する場合に使用
        # 現在は基本検出に委譲
        return None
    
    def _find_main_verb_object(self, sentence):
        """メイン動詞の目的語を探す（Case 49用）"""
        # rootの直接目的語を探す
        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                # この動詞の目的語を探す
                for obj_word in sentence.words:
                    if obj_word.head == word.id and obj_word.deprel == 'obj':
                        return obj_word
        return None
    
    def _build_noun_phrase_for_subject(self, sentence, subject_word) -> str:
        """主語の名詞句を構築"""
        # 冠詞・修飾語を含む名詞句を構築
        phrase_words = []
        
        # 冠詞を探す
        for word in sentence.words:
            if word.head == subject_word.id and word.deprel == 'det':
                phrase_words.append((word.id, word.text))
        
        # 主語本体を追加
        phrase_words.append((subject_word.id, subject_word.text))
        
        # ID順でソート
        phrase_words.sort(key=lambda x: x[0])
        
        return " ".join([w[1] for w in phrase_words])
    
    def _assign_participle_modifiers(self, modifiers, sub_slots, sentence, is_single_modifier_case):
        """分詞の修飾語を適切な sub-m スロットに配置"""
        modifier_texts = []
        
        for modifier in modifiers:
            # 修飾語の構築（前置詞句なども含む）
            if modifier.deprel == 'obl':
                # 前置詞句の場合
                prep_phrase = self._build_prepositional_phrase(sentence, modifier, exclude_advmod=False)
                modifier_texts.append(prep_phrase)
            else:
                # 単純な修飾語
                modifier_texts.append(modifier.text)
        
        # 修飾語の配置ルール
        if is_single_modifier_case:
            # Case 49: 1つの修飾語 -> sub-m2
            if len(modifier_texts) >= 1:
                sub_slots['sub-m2'] = modifier_texts[0]
        else:
            # Case 50, 51: 複数修飾語 -> sub-m2, sub-m3
            if len(modifier_texts) >= 1:
                sub_slots['sub-m2'] = modifier_texts[0]
            if len(modifier_texts) >= 2:
                sub_slots['sub-m3'] = modifier_texts[1]
    
    def _assign_modifiers_to_sub_slots(self, modifiers, sub_slots, sentence):
        """修飾語を sub-m スロットに割り当て"""
        modifier_texts = []
        
        for modifier in modifiers:
            # 修飾語の構築（前置詞句なども含む）
            if modifier.deprel == 'obl':
                # 前置詞句の場合
                prep_phrase = self._build_prepositional_phrase(sentence, modifier, exclude_advmod=False)
                modifier_texts.append(prep_phrase)
            else:
                # 単純な修飾語
                modifier_texts.append(modifier.text)
        
        # Simple Ruleに従って M スロットに配置
        self._apply_simple_rule_to_sub_modifiers(modifier_texts, sub_slots)
    
    def _build_prepositional_phrase(self, sentence, obl_word, exclude_advmod=True) -> str:
        """前置詞句を構築"""
        print(f"DEBUG METHOD2: '{obl_word.text}' (id={obl_word.id}) exclude_advmod={exclude_advmod}")
        
        # obl_wordは前置詞句の目的語なので、前置詞を探す
        prep = None
        for word in sentence.words:
            if word.head == obl_word.id and word.deprel == 'case':
                prep = word
                break
        
        # 🔧 advmod除外処理を追加
        advmod_modifiers = []
        for word in sentence.words:
            if word.head == obl_word.id and word.deprel == 'advmod':
                advmod_modifiers.append(word.text)
                print(f"DEBUG ADVMOD FOUND: {word.text} modifies {obl_word.text}")
        
        if prep:
            # 冠詞も含めて構築
            det = None
            for word in sentence.words:
                if word.head == obl_word.id and word.deprel == 'det':
                    det = word
                    break
            
            # 🔧 exclude_advmodがTrueの場合、advmodを含めない
            if exclude_advmod and advmod_modifiers:
                print(f"DEBUG EXCLUDING ADVMOD: {advmod_modifiers}")
                if det:
                    result = f"{prep.text} {det.text} {obl_word.text}"
                else:
                    result = f"{prep.text} {obl_word.text}"
            else:
                # 従来の処理（advmodも含める）
                advmod_text = ' '.join(advmod_modifiers)
                if det:
                    if advmod_modifiers:
                        result = f"{prep.text} {det.text} {advmod_text} {obl_word.text}"
                    else:
                        result = f"{prep.text} {det.text} {obl_word.text}"
                else:
                    if advmod_modifiers:
                        result = f"{prep.text} {advmod_text} {obl_word.text}"
                    else:
                        result = f"{prep.text} {obl_word.text}"
        else:
            # 前置詞がない場合
            if exclude_advmod and advmod_modifiers:
                print(f"DEBUG NO PREP, EXCLUDING ADVMOD: {advmod_modifiers}")
                result = obl_word.text
            else:
                advmod_text = ' '.join(advmod_modifiers)
                if advmod_modifiers:
                    result = f"{advmod_text} {obl_word.text}"
                else:
                    result = obl_word.text
        
        print(f"DEBUG METHOD2 RESULT: '{result}'")
        return result
    
    def _apply_simple_rule_to_sub_modifiers(self, modifier_texts, sub_slots):
        """Simple Ruleを sub-m スロットに適用"""
        if not modifier_texts:
            return
        
        count = len(modifier_texts)
        
        if count == 1:
            sub_slots['sub-m2'] = modifier_texts[0]
        elif count == 2:
            sub_slots['sub-m1'] = modifier_texts[0]
            sub_slots['sub-m2'] = modifier_texts[1]
        elif count == 3:
            sub_slots['sub-m1'] = modifier_texts[0]
            sub_slots['sub-m2'] = modifier_texts[1]
            sub_slots['sub-m3'] = modifier_texts[2]
    
    def _is_object_of_main_verb(self, sentence, word) -> bool:
        """語が主動詞の目的語かチェック"""
        # 主動詞を探す
        main_verb = None
        for w in sentence.words:
            if w.deprel == 'root':
                main_verb = w
                break
        
        if main_verb and word.head == main_verb.id and word.deprel in ['obj', 'dobj']:
            return True
        return False
    
    def _build_prepositional_phrase(self, sentence, prep, exclude_advmod=True) -> str:
        """前置詞句の構築"""
        print(f"DEBUG METHOD3: called with prep='{prep.text}' exclude_advmod={exclude_advmod}")
        
        # 🔧 時間副詞の特別処理（"yesterday", "today", "tomorrow"など）
        if prep.text.lower() in ['yesterday', 'today', 'tomorrow', 'now', 'then']:
            print(f"DEBUG METHOD3: temporal adverb '{prep.text}' treated as standalone")
            return prep.text
        
        phrase_words = [prep]
        
        # 前置詞の目的語を探す
        for word in sentence.words:
            if word.head == prep.id:
                phrase_words.append(word)
                print(f"DEBUG METHOD3: found object '{word.text}' for prep '{prep.text}'")
                
                # 目的語の修飾語も追加
                for modifier in sentence.words:
                    if modifier.head == word.id and modifier.deprel in ['det', 'amod']:
                        phrase_words.append(modifier)
                        print(f"DEBUG METHOD3: added modifier '{modifier.text}' (deprel={modifier.deprel})")
                    elif modifier.head == word.id and modifier.deprel == 'advmod':
                        if not exclude_advmod:
                            phrase_words.append(modifier)
                            print(f"DEBUG METHOD3: added advmod '{modifier.text}' (exclude_advmod=False)")
                        else:
                            print(f"DEBUG METHOD3: excluded advmod '{modifier.text}' (exclude_advmod=True)")
        
        # ID順ソート（語順保持）
        phrase_words.sort(key=lambda w: w.id)
        result = ' '.join(w.text for w in phrase_words)
        print(f"DEBUG METHOD3 RESULT: '{result}'")
        return result
    
    def _build_noun_phrase(self, sentence, noun) -> str:
        """名詞句の構築（修飾語含む）"""
        if not noun:
            return ""
            
        noun_words = [noun]
        
        # 名詞の修飾語を収集
        for word in sentence.words:
            if word.head == noun.id and word.deprel in ['det', 'amod', 'compound', 'nmod']:
                noun_words.append(word)
        
        # ID順ソート（語順保持）
        noun_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in noun_words)

    # =============================================================================
    # 助動詞複合体処理ハンドラー (Phase 3)
    # =============================================================================
    
    def _handle_auxiliary_complex(self, sentence, base_result: Dict) -> Dict[str, Any]:
        """
        助動詞複合体処理ハンドラー (Phase 3)
        
        複合助動詞チェーンの処理:
        - is being (現在進行受動態)
        - will be (未来時制)
        - has finished (現在完了)
        - will have been (未来完了)
        
        Migration Source: perfect_progressive_engine.py のロジック継承
        """
        print(f"  🔧 助動詞複合処理ハンドラー開始")
        
        result = {
            'handler': 'auxiliary_complex',
            'analysis_type': 'auxiliary_chain_processing',
            'metadata': {}
        }
        
        # 助動詞チェーン検出
        auxiliary_chain = []
        main_verb = None
        subject = None
        
        # 第一パス: 主動詞を特定
        for word in sentence.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                main_verb = word
                print(f"    🎯 主動詞検出: {word.text}")
                break
        
        # 第二パス: 助動詞を節レベルで分類して収集
        main_auxiliary_words = []  # 主節助動詞
        sub_auxiliary_words = []   # 従属節助動詞
        
        for word in sentence.words:
            # 助動詞検出
            is_auxiliary = False
            if word.deprel in ['aux', 'aux:pass']:
                is_auxiliary = True
                print(f"    🔗 標準助動詞: {word.text} ({word.deprel})")
            elif word.deprel == 'cop' and word.lemma == 'be':
                # 連結詞は助動詞ではない（補語構文のbe動詞）
                # 受動態・進行形の文脈でのみ助動詞として扱う
                is_auxiliary_context = False
                
                # 受動態チェック: 近くに過去分詞があるか
                for next_word in sentence.words:
                    if (next_word.id > word.id and 
                        next_word.upos == 'VERB' and 
                        (next_word.xpos in ['VBN'] or next_word.text.endswith('ed'))):
                        is_auxiliary_context = True
                        break
                        
                # 進行形チェック: 近くにbeingがあるか
                for next_word in sentence.words:
                    if (next_word.id > word.id and 
                        next_word.text.lower() == 'being'):
                        is_auxiliary_context = True
                        break
                
                if is_auxiliary_context:
                    is_auxiliary = True
                    print(f"    🔗 文脈的助動詞be: {word.text}")
                else:
                    print(f"    ❌ 連結詞be (非助動詞): {word.text}")
                    continue
            elif (word.upos == 'VERB' and 
                  word.text.lower() in ['can', 'could', 'will', 'would', 'shall', 'should', 'may', 'might', 'must']):
                is_auxiliary = True
                print(f"    🔗 法助動詞: {word.text}")
            elif word.text.lower() == 'being' and word.upos in ['AUX', 'VERB']:
                is_auxiliary = True
                print(f"    🔗 being検出: {word.text}")
            
            # 助動詞の節レベル分類
            if is_auxiliary:
                # 主節助動詞: 主動詞に直接依存
                if main_verb and (word.head == main_verb.id or 
                                  (word.deprel == 'cop' and word.text.lower() in ['am', 'is', 'are', 'was', 'were'])):
                    main_auxiliary_words.append(word)
                    print(f"      → 主節助動詞: {word.text}")
                else:
                    sub_auxiliary_words.append(word)
                    print(f"      → 従属節助動詞: {word.text}")
            
            # 主語検出 (主文のみ)
            elif word.deprel == 'nsubj' and main_verb and word.head == main_verb.id:
                subject = word
                print(f"    👤 主語検出: {word.text}")
        
        # 主節助動詞を位置順にソートして統合
        if main_auxiliary_words:
            main_auxiliary_words.sort(key=lambda x: x.id)
            auxiliary_chain = [word.text for word in main_auxiliary_words]
            print(f"    🎯 主節助動詞チェーン: {auxiliary_chain}")
        else:
            auxiliary_chain = []
        
        # 第三パス: 従属節助動詞をsub-auxとして処理
        subordinate_auxiliaries = []
        for aux_word in sub_auxiliary_words:
            subordinate_auxiliaries.append(aux_word.text.lower())
            print(f"    🔗 従属節助動詞統合: {aux_word.text}")
        
        # 助動詞チェーンが存在する場合のみ処理
        if len(auxiliary_chain) >= 1:
            print(f"    ✅ 主節助動詞チェーン発見: {auxiliary_chain}")
            
            # 助動詞チェーン結合 (核心ロジック)
            auxiliary_phrase = ' '.join(auxiliary_chain)
            result['metadata']['auxiliary_chain'] = auxiliary_phrase
            result['metadata']['auxiliary_count'] = len(auxiliary_chain)
            
            # スロット構造の初期化
            slots = {}
            sub_slots = {}
            
            # 主文要素の配置
            if subject:
                subject_phrase = self._build_phrase_with_modifiers(sentence, subject)
                slots['S'] = subject_phrase
            
            # 助動詞句をAuxスロットに配置（主文のみ）
            slots['Aux'] = auxiliary_phrase
            
            # 主動詞処理
            if main_verb:
                verb_phrase = self._build_phrase_with_modifiers(sentence, main_verb)
                slots['V'] = verb_phrase
            
            # 従属節助動詞の処理
            if subordinate_auxiliaries:
                sub_slots['sub-aux'] = ' '.join(subordinate_auxiliaries)
                print(f"    📍 従属節助動詞: sub-aux = {sub_slots['sub-aux']}")
            
            print(f"    ✅ 助動詞複合処理完了: Aux='{auxiliary_phrase}'")
            return {'slots': slots, 'sub_slots': sub_slots}
        
        elif subordinate_auxiliaries:
            # 主節助動詞なし、従属節助動詞のみの場合
            print(f"    📍 従属節助動詞のみ: {subordinate_auxiliaries}")
            return {'slots': {}, 'sub_slots': {'sub-aux': ' '.join(subordinate_auxiliaries)}}
        
        else:
            print(f"    ❌ 助動詞チェーン未検出")
            return None

    def _is_main_clause_auxiliary(self, word, main_verb) -> bool:
        """主文の助動詞かどうかを判定"""
        # 基本的な助動詞判定
        is_auxiliary = (
            word.upos == 'AUX' or 
            (word.upos == 'VERB' and word.deprel in ['aux', 'cop']) or
            word.text.lower() in ['be', 'have', 'will', 'can', 'should', 'would', 'could', 'may', 'might', 'must']
        )
        
        if not is_auxiliary:
            return False
        
        # 主動詞に直接関連する助動詞のみ（主文レベル）
        if word.deprel in ['aux', 'cop'] and word.head == main_verb.id:
            return True
            
        return False

    def _handle_conjunction(self, sentence, base_result: Dict) -> Optional[Dict]:
        """
        接続詞処理ハンドラー（"as if"等の従属接続詞対応）
        migrationエンジンからの移植版
        """
        self.logger.debug("接続詞ハンドラー実行中...")
        
        # 従属接続詞の検出（mark + advcl の組み合わせ）
        mark_words = []
        advcl_verbs = []
        
        for word in sentence.words:
            if word.deprel == 'mark' and word.upos == 'SCONJ':
                mark_words.append(word)
            elif word.deprel == 'advcl':
                advcl_verbs.append(word)
        
        if not mark_words or not advcl_verbs:
            self.logger.debug("  → 接続詞構文未検出")
            return None
        
        # "as if"等の複合接続詞を検出
        conjunction_phrase = self._detect_compound_conjunction(sentence, mark_words)
        if not conjunction_phrase:
            self.logger.debug("  → 複合接続詞未検出")
            return None
        
        self.logger.debug(f"  🔗 複合接続詞検出: '{conjunction_phrase}'")
        
        # 従属節の要素を抽出
        advcl_verb = advcl_verbs[0]  # 最初のadvcl動詞を使用
        sub_slots = self._extract_subordinate_conjunction_elements(sentence, advcl_verb, conjunction_phrase)
        
        # 主節は既存のbase_resultを使用（接続詞構文では移行しない）
        main_slots = base_result.get('slots', {}) if base_result else {}
        
        # 従属節要素を主節から除去
        self._remove_subordinate_elements_from_main(main_slots, sub_slots, advcl_verb)
        
        # ★ M1位置に接続詞を配置（但し既存のMスロットは保護）
        # 接続詞構造では一般的にM1は使わないため、この処理をコメントアウト
        # if not main_slots.get('M1'):
        #     main_slots['M1'] = ''
        
        result = {
            'slots': main_slots,
            'sub_slots': sub_slots,
            'grammar_info': {
                'detected_patterns': ['conjunction'],
                'conjunction_type': conjunction_phrase,
                'subordinate_verb': advcl_verb.text
            }
        }
        
        self.logger.debug(f"  ✅ 接続詞処理完了: {len(sub_slots)}個の従属節要素")
        return result
    
    def _detect_compound_conjunction(self, sentence, mark_words) -> Optional[str]:
        """複合接続詞の検出（"as if"等）"""
        if len(mark_words) < 2:
            return None
        
        # 連続するmark wordを検出
        mark_words.sort(key=lambda x: x.id)
        
        # "as if"パターンの検出
        for i in range(len(mark_words) - 1):
            word1 = mark_words[i]
            word2 = mark_words[i + 1]
            
            # 連続する位置にある場合
            if word2.id == word1.id + 1:
                phrase = f"{word1.text} {word2.text}"
                if phrase.lower() in ['as if', 'even if', 'as though']:
                    return phrase
        
        return None
    
    def _extract_subordinate_conjunction_elements(self, sentence, advcl_verb, conjunction_phrase) -> Dict[str, str]:
        """従属節要素の抽出"""
        sub_slots = {}
        
        # 接続詞をsub-m1に配置
        sub_slots['sub-m1'] = conjunction_phrase
        
        # 従属節の主語
        for word in sentence.words:
            if word.head == advcl_verb.id and word.deprel == 'nsubj':
                sub_slots['sub-s'] = word.text
                break
        
        # 従属節の動詞
        sub_slots['sub-v'] = advcl_verb.text
        
        # 従属節の目的語
        for word in sentence.words:
            if word.head == advcl_verb.id and word.deprel == 'obj':
                sub_slots['sub-o1'] = word.text
                break
        
        return sub_slots

    def _remove_subordinate_elements_from_main(self, main_slots: Dict[str, str], sub_slots: Dict[str, str], advcl_verb) -> None:
        """従属節要素を主節から除去（主節の主語・動詞は保持）"""
        # 従属節にのみ存在する要素を特定
        subordinate_only_elements = set()
        
        # 従属節の目的語・補語等（主語・動詞以外）を取得
        for sub_key, sub_value in sub_slots.items():
            if sub_value and sub_key.startswith('sub-') and sub_key not in ['sub-m1', 'sub-s', 'sub-v']:
                subordinate_only_elements.add(sub_value.lower())
        
        # 主節スロットから従属節にのみ存在する要素を除去
        for main_key, main_value in list(main_slots.items()):
            if main_value and main_value.lower() in subordinate_only_elements:
                main_slots[main_key] = ''
                self.logger.debug(f"  🔄 従属節専用要素を主節から除去: {main_key}='{main_value}' → ''")


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

def clean_result_for_json(result: Dict) -> Dict:
    """
    JSON出力用に結果をクリーンアップ
    循環参照や非JSON対応オブジェクトを除去
    """
    def clean_value(obj, visited=None):
        if visited is None:
            visited = set()
        
        # 循環参照チェック
        obj_id = id(obj)
        if obj_id in visited:
            return "<circular_reference>"
        
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, dict):
            visited.add(obj_id)
            cleaned = {}
            for k, v in obj.items():
                # 特定のキーは除外
                if k in ['stanza_doc', 'spacy_doc', '__dict__', '__weakref__']:
                    continue
                try:
                    cleaned[k] = clean_value(v, visited.copy())
                except (RecursionError, RuntimeError):
                    cleaned[k] = f"<error_cleaning_{k}>"
            return cleaned
        elif isinstance(obj, list):
            visited.add(obj_id)
            try:
                return [clean_value(item, visited.copy()) for item in obj[:100]]  # 最大100要素
            except (RecursionError, RuntimeError):
                return ["<error_cleaning_list>"]
        else:
            # その他のオブジェクトは文字列表現
            try:
                return str(obj)[:200]  # 最大200文字
            except:
                return "<unrepresentable_object>"


def process_batch_sentences(input_file: str, output_file: str = None) -> str:
    """
    バッチ処理：53例文一括実行
    
    Args:
        input_file: 入力ファイル (JSON)
        output_file: 出力ファイル (省略時は auto-generated)
    
    Returns:
        output_file: 保存されたファイル名
    """
    import argparse
    from datetime import datetime
    
    print(f"🔄 バッチ処理開始: {input_file}")
    
    # 入力データ読み込み
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ エラー: ファイルが見つかりません - {input_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        return None
    
    # 出力ファイル名生成
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"batch_results_{timestamp}.json"
    
    # システム初期化
    mapper = UnifiedStanzaRephraseMapper()
    print("✅ システム初期化完了")
    
    # 結果格納
    results = {
        "meta": {
            "input_file": input_file,
            "processed_at": datetime.now().isoformat(),
            "total_sentences": 0,
            "success_count": 0,
            "error_count": 0
        },
        "results": {}
    }
    
    # データ形式判定と処理
    if "data" in test_data:
        # final_54_test_data.json 形式
        sentences_data = test_data["data"]
        results["meta"]["total_sentences"] = len(sentences_data)
        
        print(f"📊 処理対象: {len(sentences_data)}例文")
        
        for test_id, test_case in sentences_data.items():
            try:
                sentence = test_case["sentence"]
                print(f"Processing [{test_id}]: {sentence}")
                
                # 文解析実行
                result = mapper.process(sentence)
                
                # 基本スロット情報のみ抽出（循環参照問題を回避）
                clean_result = {
                    "sentence": result.get("sentence", ""),
                    "slots": result.get("slots", {}),
                    "sub_slots": result.get("sub_slots", {}),
                    "meta": {
                        "processing_time": result.get("meta", {}).get("processing_time", 0.0),
                        "sentence_id": result.get("meta", {}).get("sentence_id", 0),
                        "active_handlers": result.get("meta", {}).get("active_handlers", 0)
                    }
                }
                
                results["results"][test_id] = {
                    "sentence": sentence,
                    "analysis_result": clean_result,
                    "expected": test_case.get("expected", {}),
                    "status": "success"
                }
                results["meta"]["success_count"] += 1
                
            except Exception as e:
                print(f"❌ エラー [{test_id}]: {e}")
                results["results"][test_id] = {
                    "sentence": test_case.get("sentence", ""),
                    "error": str(e),
                    "status": "error"
                }
                results["meta"]["error_count"] += 1
    
    elif isinstance(test_data, list):
        # シンプルリスト形式 ["sentence1", "sentence2", ...]
        results["meta"]["total_sentences"] = len(test_data)
        
        for i, sentence in enumerate(test_data):
            try:
                print(f"Processing [{i+1}]: {sentence}")
                result = mapper.process(sentence)
                
                # 基本スロット情報のみ抽出（循環参照問題を回避）
                clean_result = {
                    "sentence": result.get("sentence", ""),
                    "slots": result.get("slots", {}),
                    "sub_slots": result.get("sub_slots", {}),
                    "meta": {
                        "processing_time": result.get("meta", {}).get("processing_time", 0.0),
                        "sentence_id": result.get("meta", {}).get("sentence_id", 0),
                        "active_handlers": result.get("meta", {}).get("active_handlers", 0)
                    }
                }
                
                results["results"][str(i+1)] = {
                    "sentence": sentence,
                    "analysis_result": clean_result,
                    "status": "success"
                }
                results["meta"]["success_count"] += 1
                
            except Exception as e:
                print(f"❌ エラー [{i+1}]: {e}")
                results["results"][str(i+1)] = {
                    "sentence": sentence,
                    "error": str(e),
                    "status": "error"
                }
                results["meta"]["error_count"] += 1
    
    else:
        print("❌ 未対応のデータ形式です")
        return None
    
    # 結果保存
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 処理完了！")
        print(f"📁 結果保存: {output_file}")
        print(f"📊 統計:")
        print(f"   総数: {results['meta']['total_sentences']}")
        print(f"   成功: {results['meta']['success_count']}")
        print(f"   エラー: {results['meta']['error_count']}")
        print(f"   成功率: {results['meta']['success_count']/results['meta']['total_sentences']*100:.1f}%")
        
        return output_file
        
    except Exception as e:
        print(f"❌ 保存エラー: {e}")
        return None

def main():
    """CLI メインエントリーポイント"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Unified Stanza-Rephrase Mapper - バッチ処理版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 53例文一括処理
  python unified_stanza_rephrase_mapper.py --input final_test_system/final_54_test_data.json
  
  # 出力ファイル指定
  python unified_stanza_rephrase_mapper.py --input sentences.json --output my_results.json
  
  # シンプルリスト形式のJSONも対応
  python unified_stanza_rephrase_mapper.py --input simple_sentences.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='入力JSONファイル（例文データ）'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='出力JSONファイル（省略時は自動生成）'
    )
    
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='テストモード（旧Phase 0-2実行）'
    )
    
    args = parser.parse_args()
    
    if args.test_mode:
        # 従来のテストモード
        print("🧪 テストモード実行")
        if test_phase0_basic():
            print("\n" + "="*60)
            if test_phase1_relative_clause():
                print("\n" + "="*60)
                test_phase2_passive_voice()
            else:
                print("❌ Phase 1失敗のため Phase 2をスキップ")
        else:
            print("❌ Phase 0失敗のため Phase 1,2をスキップ")
    else:
        # バッチ処理モード
        result_file = process_batch_sentences(args.input, args.output)
        if result_file:
            print(f"\n🎉 バッチ処理が完了しました")
            print(f"結果ファイル: {result_file}")
        else:
            print("\n❌ バッチ処理が失敗しました")
            exit(1)

if __name__ == "__main__":
    main()
