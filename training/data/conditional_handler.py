"""
Conditional Handler - 仮定法処理専門ハンドラー
Phase 9: ConditionalHandler実装

設計方針:
- If仮定法: 現在、過去、過去完了、混合型
- 倒置仮定法: Were/Had/Should倒置構造
- Wish仮定法: 願望表現の仮定法
- As if/As though仮定法: 比喩的仮定法
- 仮定法相当語句: without/but for/unless/suppose等
- Rephraseスロット構造完全準拠
- Human Grammar Pattern: spaCy依存関係解析を活用した条件節・主節分離
"""

import spacy
import re
from typing import Dict, List, Any, Optional, Tuple


class ConditionalHandler:
    """
    仮定法処理専門ハンドラー
    
    責任:
    - 条件節と主節の分離・分析
    - 仮定法時制パターンの識別
    - 倒置仮定法の構造解析
    - wish/as if等の特殊仮定法処理
    - 仮定法相当語句の処理
    - Rephraseスロット構造への変換
    
    対象範囲:
    - If conditionals: 現在/過去/過去完了/混合型
    - Inverted conditionals: Were/Had/Should倒置
    - Wish subjunctive: I wish構文
    - As if/though subjunctive: 比喩的仮定法
    - Conditional equivalents: without/but for/unless/suppose/provided等
    """
    
    def __init__(self, nlp=None):
        """初期化: spaCy依存関係解析器と仮定法パターンの設定"""
        self.nlp = nlp if nlp else spacy.load('en_core_web_sm')
        
        # 仮定法パターンの初期化
        self._initialize_conditional_patterns()
        
        print("🎯 ConditionalHandler初期化完了")
    
    def _initialize_conditional_patterns(self):
        """仮定法パターンの初期化"""
        
        # If節パターン
        self.if_patterns = {
            'basic_if': r'\bIf\s+',
            'even_if': r'\bEven\s+if\s+',
            'as_if': r'\bas\s+if\s+',
            'as_though': r'\bas\s+though\s+'
        }
        
        # 倒置仮定法パターン
        self.inversion_patterns = {
            'were': r'^\s*Were\s+\w+',
            'had': r'^\s*Had\s+\w+',
            'should': r'^\s*Should\s+\w+'
        }
        
        # 仮定法相当語句
        self.conditional_equivalents = {
            'unless': r'\bUnless\s+',
            'suppose': r'\bSuppose\s+',
            'imagine': r'\bImagine\s+(?:if\s+)?',
            'provided': r'\bProvided\s+(?:that\s+)?',
            'as_long_as': r'\bAs\s+long\s+as\s+',
            'without': r'\bWithout\s+',
            'but_for': r'\bBut\s+for\s+'
        }
        
        # Wish構文パターン
        self.wish_patterns = {
            'wish': r'\b(?:wish|wishes|wished)\s+'
        }
        
        # 仮定法時制識別パターン
        self.tense_patterns = {
            'present': r'\b(?:study|studies|work|works|am|is|are)\b',
            'past': r'\b(?:were|had|studied|worked|went|came)\b',
            'past_perfect': r'\b(?:had\s+\w+ed|had\s+\w+en|had\s+been)\b',
            'present_perfect': r'\b(?:have|has)\s+\w+(?:ed|en)\b'
        }
        
        print("🔧 仮定法パターン初期化完了")
    
    def detect_conditional_patterns(self, text: str) -> List[str]:
        """
        仮定法パターンの検出
        
        Args:
            text: 分析対象の英文
            
        Returns:
            List[str]: 検出された仮定法パターンのリスト
        """
        detected_patterns = []
        text_lower = text.lower()
        
        # If節パターンの検出
        for pattern_name, pattern in self.if_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(pattern_name)
        
        # 倒置仮定法パターンの検出
        for pattern_name, pattern in self.inversion_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(f"inversion_{pattern_name}")
        
        # 仮定法相当語句の検出
        for pattern_name, pattern in self.conditional_equivalents.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(f"equivalent_{pattern_name}")
        
        # Wish構文の検出
        for pattern_name, pattern in self.wish_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(f"wish_{pattern_name}")
        
        return detected_patterns
    
    def process(self, sentence: str) -> Dict[str, Any]:
        """
        仮定法文の処理メイン関数
        
        Args:
            sentence: 処理対象の英文
            
        Returns:
            処理結果辞書 (success, main_slots, sub_slots, metadata)
        """
        try:
            print(f"🎯 ConditionalHandler処理開始: '{sentence}'")
            
            # spaCy解析
            doc = self.nlp(sentence)
            
            # 前処理: 句読点除去と正規化
            clean_sentence = self._preprocess_sentence(sentence)
            
            # 仮定法パターン識別
            conditional_type = self._identify_conditional_type(clean_sentence)
            
            if not conditional_type:
                return {'success': False, 'error': 'No conditional pattern detected'}
            
            print(f"🔍 仮定法タイプ検出: {conditional_type}")
            
            # タイプ別処理
            if conditional_type.startswith('if_'):
                return self._process_if_conditional(doc, clean_sentence, conditional_type)
            elif conditional_type.startswith('inversion_'):
                return self._process_inversion_conditional(doc, clean_sentence, conditional_type)
            elif conditional_type == 'wish':
                return self._process_wish_conditional(doc, clean_sentence)
            elif conditional_type in ['as_if', 'as_though']:
                return self._process_as_if_conditional(doc, clean_sentence, conditional_type)
            elif conditional_type in ['without', 'but_for']:
                return self._process_without_conditional(doc, clean_sentence, conditional_type)
            else:
                return self._process_other_conditional(doc, clean_sentence, conditional_type)
                
        except Exception as e:
            print(f"❌ ConditionalHandler処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _preprocess_sentence(self, sentence: str) -> str:
        """文の前処理"""
        # 句読点処理
        clean = re.sub(r'[,.]', ' ', sentence).strip()
        # 余分な空白除去
        clean = re.sub(r'\s+', ' ', clean)
        return clean
    
    def _identify_conditional_type(self, sentence: str) -> Optional[str]:
        """仮定法タイプの識別"""
        
        # If節パターンチェック
        for pattern_name, pattern in self.if_patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                return pattern_name
        
        # 倒置仮定法パターンチェック
        for pattern_name, pattern in self.inversion_patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                return f"inversion_{pattern_name}"
        
        # Wish構文チェック
        for pattern_name, pattern in self.wish_patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                return 'wish'
        
        # 仮定法相当語句チェック
        for pattern_name, pattern in self.conditional_equivalents.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                return pattern_name
        
        return None
    
    def _process_if_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """If仮定法の処理"""
        try:
            print(f"🔍 If仮定法処理開始: {conditional_type}")
            
            # If節と主節の分離
            if_clause, main_clause = self._split_if_conditional(sentence)
            
            if not if_clause or not main_clause:
                return {'success': False, 'error': 'Failed to split conditional clauses'}
            
            print(f"📝 If節: '{if_clause}'")
            print(f"📝 主節: '{main_clause}'")
            
            # If節の解析
            sub_slots = self._analyze_if_clause(if_clause)
            
            # 主節の解析
            main_slots = self._analyze_main_clause(main_clause)
            
            # 親スロット決定
            parent_slot = self._determine_parent_slot(conditional_type, main_clause)
            
            # 上位スロットに空マーカー追加
            if parent_slot in main_slots:
                main_slots[parent_slot] = ""
            else:
                main_slots[parent_slot] = ""
            
            # サブスロットに親情報追加
            sub_slots['_parent_slot'] = parent_slot
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'metadata': {
                    'handler': 'conditional',
                    'type': conditional_type,
                    'if_clause': if_clause,
                    'main_clause': main_clause,
                    'confidence': 0.9
                }
            }
            
        except Exception as e:
            print(f"❌ If仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _split_if_conditional(self, sentence: str) -> Tuple[str, str]:
        """If仮定法の条件節と主節を分離"""
        
        # コンマで分割
        parts = sentence.split(',')
        
        if len(parts) == 2:
            # "If clause, main clause" パターン
            if_clause = parts[0].strip()
            main_clause = parts[1].strip()
        elif len(parts) == 1:
            # コンマなしの場合、spaCy依存関係を利用
            doc = self.nlp(sentence)
            if_clause, main_clause = self._split_by_dependency(doc)
        else:
            # 複数コンマの場合は最初の分割点を使用
            if_clause = parts[0].strip()
            main_clause = ','.join(parts[1:]).strip()
        
        return if_clause, main_clause
    
    def _split_by_dependency(self, doc) -> Tuple[str, str]:
        """依存関係解析による節分離"""
        
        if_start = -1
        if_end = -1
        
        # If節の範囲を特定
        for i, token in enumerate(doc):
            if token.text.lower() == 'if':
                if_start = i
            elif if_start != -1 and token.dep_ == 'ROOT':
                if_end = i
                break
        
        if if_start != -1 and if_end != -1:
            if_clause = ' '.join([token.text for token in doc[if_start:if_end]])
            main_clause = ' '.join([token.text for token in doc[if_end:]])
        else:
            # フォールバック: 単純分割
            text = doc.text
            if 'if ' in text.lower():
                parts = text.lower().split('if ', 1)
                if_clause = 'If ' + parts[1]
                main_clause = parts[0].strip() if parts[0].strip() else 'Unknown'
            else:
                if_clause = text
                main_clause = ''
        
        return if_clause, main_clause
    
    def _analyze_if_clause(self, if_clause: str) -> Dict[str, str]:
        """If節の解析"""
        
        sub_slots = {}
        
        # spaCy解析
        doc = self.nlp(if_clause)
        
        # 基本構造抽出
        if_word = ""
        subject = ""
        verb = ""
        auxiliary = ""
        obj = ""
        complement = ""
        modifier = ""
        
        for token in doc:
            if token.text.lower() in ['if', 'even', 'unless', 'suppose', 'imagine', 'provided', 'as']:
                if_word += token.text + " "
            elif token.dep_ == 'nsubj':
                subject = token.text
            elif token.pos_ == 'AUX' and token.dep_ != 'ROOT':
                auxiliary = token.text
            elif token.dep_ == 'ROOT' or (token.pos_ == 'VERB' and not auxiliary):
                verb = token.text
            elif token.dep_ in ['dobj', 'pobj']:
                obj += token.text + " "
            elif token.dep_ in ['acomp', 'attr']:
                complement = token.text
            elif token.dep_ in ['advmod', 'npadvmod']:
                modifier += token.text + " "
        
        # If + 主語の結合
        if_word = if_word.strip()
        if subject:
            sub_slots['sub-s'] = f"{if_word} {subject}".strip()
        else:
            sub_slots['sub-s'] = if_word
        
        # 動詞関連
        if auxiliary:
            sub_slots['sub-aux'] = auxiliary
        if verb:
            sub_slots['sub-v'] = verb
        
        # 目的語・補語
        if obj.strip():
            sub_slots['sub-o1'] = obj.strip()
        if complement:
            sub_slots['sub-c1'] = complement
        
        # 修飾語
        if modifier.strip():
            sub_slots['sub-m2'] = modifier.strip()
        
        return sub_slots
    
    def _analyze_main_clause(self, main_clause: str) -> Dict[str, str]:
        """主節の解析"""
        
        main_slots = {}
        
        # spaCy解析
        doc = self.nlp(main_clause)
        
        # 基本構造抽出
        subject = ""
        verb = ""
        auxiliary = ""
        obj = ""
        complement = ""
        modifier = ""
        
        for token in doc:
            if token.dep_ == 'nsubj':
                subject = token.text
            elif token.pos_ == 'AUX' and token.dep_ != 'ROOT':
                auxiliary += token.text + " "
            elif token.dep_ == 'ROOT' or (token.pos_ == 'VERB' and verb == ""):
                verb = token.text
            elif token.dep_ in ['dobj']:
                obj = token.text + " " + obj if obj else token.text
            elif token.dep_ in ['acomp', 'attr']:
                complement = token.text
            elif token.dep_ in ['advmod', 'npadvmod'] and token.text.lower() not in ['please']:
                modifier += token.text + " "
            elif token.text.lower() == 'please':
                # pleaseは特別扱い
                if 'M2' not in main_slots:
                    main_slots['M2'] = 'please'
        
        # スロット設定
        if subject:
            main_slots['S'] = subject
        if auxiliary.strip():
            main_slots['Aux'] = auxiliary.strip()
        if verb:
            main_slots['V'] = verb
        if obj:
            main_slots['O1'] = obj.strip()
        if complement:
            main_slots['C1'] = complement
        if modifier.strip():
            if 'M2' not in main_slots:
                main_slots['M2'] = modifier.strip()
        
        return main_slots
    
    def _determine_parent_slot(self, conditional_type: str, main_clause: str) -> str:
        """親スロットの決定"""
        
        # 文頭条件の場合はM1
        if conditional_type in ['basic_if'] and any(word in main_clause.lower() for word in ['now', 'today', 'tomorrow']):
            return 'M1'
        
        # その他の多くの場合はM2
        return 'M2'
    
    def _process_inversion_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """倒置仮定法の処理"""
        try:
            print(f"🔍 倒置仮定法処理開始: {conditional_type}")
            
            # 倒置節と主節の分離
            inversion_clause, main_clause = self._split_inversion_conditional(sentence)
            
            print(f"📝 倒置節: '{inversion_clause}'")
            print(f"📝 主節: '{main_clause}'")
            
            # 倒置節の解析
            sub_slots = self._analyze_inversion_clause(inversion_clause, conditional_type)
            
            # 主節の解析
            main_slots = self._analyze_main_clause(main_clause)
            
            # 親スロット決定（倒置仮定法は通常M1またはM2）
            parent_slot = 'M1' if 'had' in conditional_type else 'M2'
            
            # 上位スロットに空マーカー追加
            main_slots[parent_slot] = ""
            
            # サブスロットに親情報追加
            sub_slots['_parent_slot'] = parent_slot
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'metadata': {
                    'handler': 'conditional',
                    'type': conditional_type,
                    'inversion_clause': inversion_clause,
                    'main_clause': main_clause,
                    'confidence': 0.85
                }
            }
            
        except Exception as e:
            print(f"❌ 倒置仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _split_inversion_conditional(self, sentence: str) -> Tuple[str, str]:
        """倒置仮定法の分離"""
        
        parts = sentence.split(',')
        if len(parts) >= 2:
            inversion_clause = parts[0].strip()
            main_clause = ','.join(parts[1:]).strip()
        else:
            # コンマがない場合の処理
            inversion_clause = sentence
            main_clause = ""
        
        return inversion_clause, main_clause
    
    def _analyze_inversion_clause(self, inversion_clause: str, conditional_type: str) -> Dict[str, str]:
        """倒置節の解析"""
        
        sub_slots = {}
        
        # spaCy解析
        doc = self.nlp(inversion_clause)
        tokens = [token.text for token in doc]
        
        if 'were' in conditional_type:
            # "Were I you" パターン
            if len(tokens) >= 3:
                sub_slots['sub-v'] = tokens[0]  # Were
                sub_slots['sub-s'] = tokens[1]  # I
                sub_slots['sub-c1'] = tokens[2]  # you
        
        elif 'had' in conditional_type:
            # "Had she known the truth" パターン
            sub_slots['sub-aux'] = tokens[0]  # Had
            sub_slots['sub-s'] = tokens[1] if len(tokens) > 1 else ""  # she
            
            # 残りの部分を解析
            remaining = ' '.join(tokens[2:]) if len(tokens) > 2 else ""
            doc_remaining = self.nlp(remaining)
            
            verb = ""
            obj = ""
            
            for token in doc_remaining:
                if token.pos_ == 'VERB' and not verb:
                    verb = token.text
                elif token.dep_ in ['dobj', 'pobj']:
                    obj += token.text + " "
            
            if verb:
                sub_slots['sub-v'] = verb
            if obj.strip():
                sub_slots['sub-o1'] = obj.strip()
        
        elif 'should' in conditional_type:
            # "Should you need help" パターン
            sub_slots['sub-aux'] = tokens[0]  # Should
            sub_slots['sub-s'] = tokens[1] if len(tokens) > 1 else ""  # you
            
            # 残りの部分を解析
            remaining = ' '.join(tokens[2:]) if len(tokens) > 2 else ""
            doc_remaining = self.nlp(remaining)
            
            verb = ""
            obj = ""
            
            for token in doc_remaining:
                if token.pos_ == 'VERB' and not verb:
                    verb = token.text
                elif token.dep_ in ['dobj', 'pobj']:
                    obj += token.text + " "
            
            if verb:
                sub_slots['sub-v'] = verb
            if obj.strip():
                sub_slots['sub-o1'] = obj.strip()
        
        return sub_slots
    
    def _process_wish_conditional(self, doc, sentence: str) -> Dict[str, Any]:
        """Wish仮定法の処理"""
        try:
            print(f"🔍 Wish仮定法処理開始")
            
            # wishと目的語節の分離
            wish_part, object_clause = self._split_wish_conditional(sentence)
            
            print(f"📝 Wish部分: '{wish_part}'")
            print(f"📝 目的語節: '{object_clause}'")
            
            # Wish部分の解析（主節）
            main_slots = self._analyze_wish_main(wish_part)
            
            # 目的語節の解析（サブスロット）
            sub_slots = self._analyze_wish_object(object_clause)
            
            # 親スロット設定
            main_slots['O1'] = ""
            sub_slots['_parent_slot'] = 'O1'
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'metadata': {
                    'handler': 'conditional',
                    'type': 'wish',
                    'wish_part': wish_part,
                    'object_clause': object_clause,
                    'confidence': 0.9
                }
            }
            
        except Exception as e:
            print(f"❌ Wish仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _split_wish_conditional(self, sentence: str) -> Tuple[str, str]:
        """Wish構文の分離"""
        
        # "I wish" の後ろを目的語節とする
        wish_match = re.search(r'^(.+?wish)\s+(.+)$', sentence, re.IGNORECASE)
        
        if wish_match:
            wish_part = wish_match.group(1).strip()
            object_clause = wish_match.group(2).strip()
        else:
            wish_part = sentence
            object_clause = ""
        
        return wish_part, object_clause
    
    def _analyze_wish_main(self, wish_part: str) -> Dict[str, str]:
        """Wish主節の解析"""
        
        main_slots = {}
        
        # spaCy解析
        doc = self.nlp(wish_part)
        
        for token in doc:
            if token.dep_ == 'nsubj':
                main_slots['S'] = token.text
            elif token.lemma_ == 'wish':
                main_slots['V'] = token.text
        
        return main_slots
    
    def _analyze_wish_object(self, object_clause: str) -> Dict[str, str]:
        """Wish目的語節の解析"""
        
        sub_slots = {}
        
        # spaCy解析
        doc = self.nlp(object_clause)
        
        subject = ""
        verb = ""
        auxiliary = ""
        obj = ""
        complement = ""
        modifier = ""
        
        for token in doc:
            if token.dep_ == 'nsubj':
                subject = token.text
            elif token.pos_ == 'AUX':
                auxiliary = token.text
            elif token.pos_ == 'VERB':
                verb = token.text
            elif token.dep_ in ['dobj', 'pobj']:
                obj += token.text + " "
            elif token.dep_ in ['acomp', 'attr']:
                complement = token.text
            elif token.dep_ in ['advmod', 'npadvmod']:
                modifier += token.text + " "
        
        # スロット設定
        if subject:
            sub_slots['sub-s'] = subject
        if auxiliary:
            sub_slots['sub-aux'] = auxiliary
        if verb:
            sub_slots['sub-v'] = verb
        if obj.strip():
            sub_slots['sub-o1'] = obj.strip()
        if complement:
            sub_slots['sub-c1'] = complement
        if modifier.strip():
            sub_slots['sub-m2'] = modifier.strip()
        
        return sub_slots
    
    def _process_as_if_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """As if/As though仮定法の処理"""
        try:
            print(f"🔍 As if/though仮定法処理開始: {conditional_type}")
            
            # 主節とas if節の分離
            main_part, as_if_clause = self._split_as_if_conditional(sentence, conditional_type)
            
            print(f"📝 主節: '{main_part}'")
            print(f"📝 As if節: '{as_if_clause}'")
            
            # 主節の解析
            main_slots = self._analyze_main_clause(main_part)
            
            # As if節の解析
            sub_slots = self._analyze_as_if_clause(as_if_clause, conditional_type)
            
            # 親スロット設定
            main_slots['M2'] = ""
            sub_slots['_parent_slot'] = 'M2'
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'metadata': {
                    'handler': 'conditional',
                    'type': conditional_type,
                    'main_part': main_part,
                    'as_if_clause': as_if_clause,
                    'confidence': 0.85
                }
            }
            
        except Exception as e:
            print(f"❌ As if/though仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _split_as_if_conditional(self, sentence: str, conditional_type: str) -> Tuple[str, str]:
        """As if/though構文の分離"""
        
        pattern = r'\bas\s+(?:if|though)\s+' if conditional_type == 'as_if' else r'\bas\s+though\s+'
        
        match = re.search(pattern, sentence, re.IGNORECASE)
        
        if match:
            main_part = sentence[:match.start()].strip()
            as_if_clause = sentence[match.start():].strip()
        else:
            main_part = sentence
            as_if_clause = ""
        
        return main_part, as_if_clause
    
    def _analyze_as_if_clause(self, as_if_clause: str, conditional_type: str) -> Dict[str, str]:
        """As if/though節の解析"""
        
        sub_slots = {}
        
        # spaCy解析
        doc = self.nlp(as_if_clause)
        tokens = [token.text for token in doc]
        
        # "as if he" の形でsub-sを設定
        if len(tokens) >= 3:
            sub_slots['sub-s'] = f"{tokens[0]} {tokens[1]} {tokens[2]}"  # "as if he"
        
        # 残りの部分を解析
        remaining_start = 3 if len(tokens) > 3 else len(tokens)
        remaining = ' '.join(tokens[remaining_start:]) if remaining_start < len(tokens) else ""
        
        if remaining:
            doc_remaining = self.nlp(remaining)
            
            verb = ""
            auxiliary = ""
            obj = ""
            complement = ""
            
            for token in doc_remaining:
                if token.pos_ == 'AUX':
                    auxiliary = token.text
                elif token.pos_ == 'VERB':
                    verb = token.text
                elif token.dep_ in ['dobj', 'pobj']:
                    obj += token.text + " "
                elif token.dep_ in ['acomp', 'attr']:
                    complement = token.text
            
            if auxiliary:
                sub_slots['sub-aux'] = auxiliary
            if verb:
                sub_slots['sub-v'] = verb
            if obj.strip():
                sub_slots['sub-o1'] = obj.strip()
            if complement:
                sub_slots['sub-c1'] = complement
        
        return sub_slots
    
    def _process_without_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """Without/But for仮定法の処理"""
        try:
            print(f"🔍 Without/But for仮定法処理開始: {conditional_type}")
            
            # without/but for句と主節の分離
            prep_phrase, main_clause = self._split_without_conditional(sentence, conditional_type)
            
            print(f"📝 前置詞句: '{prep_phrase}'")
            print(f"📝 主節: '{main_clause}'")
            
            # 主節の解析
            main_slots = self._analyze_main_clause(main_clause)
            
            # 前置詞句をM2に設定
            main_slots['M2'] = prep_phrase
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': {},
                'metadata': {
                    'handler': 'conditional',
                    'type': conditional_type,
                    'prep_phrase': prep_phrase,
                    'main_clause': main_clause,
                    'confidence': 0.9
                }
            }
            
        except Exception as e:
            print(f"❌ Without/But for仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _split_without_conditional(self, sentence: str, conditional_type: str) -> Tuple[str, str]:
        """Without/But for構文の分離"""
        
        if conditional_type == 'without':
            pattern = r'(Without\s+[^,]+),?\s*(.*)'
        else:  # but_for
            pattern = r'(But\s+for\s+[^,]+),?\s*(.*)'
        
        match = re.search(pattern, sentence, re.IGNORECASE)
        
        if match:
            prep_phrase = match.group(1).strip()
            main_clause = match.group(2).strip()
        else:
            prep_phrase = sentence
            main_clause = ""
        
        return prep_phrase, main_clause
    
    def _process_other_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """その他の仮定法の処理"""
        try:
            print(f"🔍 その他仮定法処理開始: {conditional_type}")
            
            # 条件節と主節の分離（汎用）
            condition_clause, main_clause = self._split_generic_conditional(sentence, conditional_type)
            
            print(f"📝 条件節: '{condition_clause}'")
            print(f"📝 主節: '{main_clause}'")
            
            # 条件節の解析
            sub_slots = self._analyze_generic_condition(condition_clause, conditional_type)
            
            # 主節の解析
            main_slots = self._analyze_main_clause(main_clause)
            
            # 親スロット決定
            parent_slot = 'M1' if conditional_type in ['imagine'] else 'M2'
            
            # 上位スロットに空マーカー追加
            main_slots[parent_slot] = ""
            
            # サブスロットに親情報追加
            sub_slots['_parent_slot'] = parent_slot
            
            return {
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slots,
                'metadata': {
                    'handler': 'conditional',
                    'type': conditional_type,
                    'condition_clause': condition_clause,
                    'main_clause': main_clause,
                    'confidence': 0.8
                }
            }
            
        except Exception as e:
            print(f"❌ その他仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _split_generic_conditional(self, sentence: str, conditional_type: str) -> Tuple[str, str]:
        """汎用的な条件文分離"""
        
        # コンマで分割を試す
        parts = sentence.split(',')
        
        if len(parts) >= 2:
            condition_clause = parts[0].strip()
            main_clause = ','.join(parts[1:]).strip()
        else:
            # コンマがない場合、疑問文パターンを考慮
            if '?' in sentence:
                # "Suppose you had money, what would you do?" パターン
                question_match = re.search(r'^(.+?),?\s*(what|how|when|where|why.+\?)$', sentence, re.IGNORECASE)
                if question_match:
                    condition_clause = question_match.group(1).strip()
                    main_clause = question_match.group(2).strip()
                else:
                    condition_clause = sentence
                    main_clause = ""
            else:
                condition_clause = sentence
                main_clause = ""
        
        return condition_clause, main_clause
    
    def _analyze_generic_condition(self, condition_clause: str, conditional_type: str) -> Dict[str, str]:
        """汎用的な条件節解析"""
        
        sub_slots = {}
        
        # spaCy解析
        doc = self.nlp(condition_clause)
        
        # 条件詞 + 主語の抽出
        condition_words = {
            'unless': 'Unless',
            'suppose': 'Suppose',
            'imagine': 'Imagine if',
            'provided': 'Provided that',
            'as_long_as': 'As long as'
        }
        
        condition_word = condition_words.get(conditional_type, conditional_type.title())
        
        # 主語の検出
        subject = ""
        for token in doc:
            if token.dep_ == 'nsubj':
                subject = token.text
                break
        
        # 条件詞 + 主語
        if subject:
            sub_slots['sub-s'] = f"{condition_word} {subject}".strip()
        else:
            sub_slots['sub-s'] = condition_word
        
        # 動詞・助動詞・目的語等の解析
        verb = ""
        auxiliary = ""
        obj = ""
        modifier = ""
        
        for token in doc:
            if token.pos_ == 'AUX' and not auxiliary:
                auxiliary = token.text
            elif token.pos_ == 'VERB' and not verb:
                verb = token.text
            elif token.dep_ in ['dobj', 'pobj']:
                obj += token.text + " "
            elif token.dep_ in ['advmod', 'npadvmod']:
                modifier += token.text + " "
        
        if auxiliary:
            sub_slots['sub-aux'] = auxiliary
        if verb:
            sub_slots['sub-v'] = verb
        if obj.strip():
            sub_slots['sub-o1'] = obj.strip()
        if modifier.strip():
            sub_slots['sub-m2'] = modifier.strip()
        
        return sub_slots


# テスト用のメイン関数
if __name__ == "__main__":
    handler = ConditionalHandler()
    
    # テストケース
    test_sentences = [
        "If it rains tomorrow, I will stay home.",
        "If I were rich, I would travel the world.",
        "Had she known the truth, she would have acted differently.",
        "I wish I were taller.",
        "He talks as if he were the boss.",
        "Without your help, I would have failed."
    ]
    
    for sentence in test_sentences:
        print(f"\n🧪 テスト: {sentence}")
        result = handler.process(sentence)
        print(f"結果: {result}")
