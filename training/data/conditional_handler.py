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
        
        # If仮定法パターン
        self.if_patterns = {
            'if_present': r'\bif\s+.*\b(will|can|may|shall|must)\b',
            'if_past': r'\bif\s+.*\b(would|could|might|should)\b',
            'if_past_perfect': r'\bif\s+.*\bhad\s+.*\b(would|could|might|should)\s+have\b',
            'if_mixed': r'\bif\s+.*\bhad\s+.*\b(would|could|might|should)\b'
        }
        
        # 倒置仮定法パターン
        self.inversion_patterns = {
            'were': r'^were\s+\w+',
            'had': r'^had\s+\w+',
            'should': r'^should\s+\w+'
        }
        
        # Wish仮定法パターン
        self.wish_patterns = {
            'simple': r'\bwish\s+.*',
            'that': r'\bwish\s+that\s+.*'
        }
        
        # As if/though仮定法パターン
        self.as_if_patterns = {
            'as_if': r'\bas\s+if\s+.*',
            'as_though': r'\bas\s+though\s+.*'
        }
        
        # 仮定法相当語句パターン
        self.equivalent_patterns = {
            'without': r'\bwithout\s+.*',
            'but_for': r'\bbut\s+for\s+.*',
            'unless': r'\bunless\s+.*',
            'suppose': r'\bsuppose\s+.*',
            'provided': r'\bprovided\s+.*',
            'supposing': r'\bsupposing\s+.*',
            'imagine': r'\bimagine\s+if\s+.*'
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
        for pattern_name, pattern in self.equivalent_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(f"equivalent_{pattern_name}")
        
        # As if/though仮定法の検出
        for pattern_name, pattern in self.as_if_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(pattern_name)
        
        # 🚫 Wish構文は除外 - 名詞節として処理される
        # Wish文は "I wish [that] I were rich" 構造で名詞節ハンドラーが適切
        
        return detected_patterns
    
    def _detect_inversion_pattern(self, text: str) -> bool:
        """
        倒置仮定法パターンの検出
        
        Args:
            text: 分析対象の英文
            
        Returns:
            bool: 倒置パターンが検出されたかどうか
        """
        for pattern_name, pattern in self.inversion_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
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
        # Case 151対策: Imagine構文の場合はコンマを保持
        if sentence.lower().startswith('imagine if'):
            # ピリオドのみ除去、コンマは保持
            clean = re.sub(r'[.]', ' ', sentence).strip()
        else:
            # 通常処理: 句読点処理
            clean = re.sub(r'[,.]', ' ', sentence).strip()
        
        # 余分な空白除去
        clean = re.sub(r'\s+', ' ', clean)
        return clean
    
    def _identify_conditional_type(self, sentence: str) -> Optional[str]:
        """仮定法タイプの識別"""
        
        # 仮定法相当語句チェック（優先度最高 - Case 151対策）
        for pattern_name, pattern in self.equivalent_patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                return pattern_name
        
        # If仮定法パターンチェック
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
        
        # As if/though構文チェック
        for pattern_name, pattern in self.as_if_patterns.items():
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
            # 倒置仮定法の場合はIfを付けない（Should you → you）
            is_inversion = self._detect_inversion_pattern(sentence)
            include_if_prefix = not is_inversion  # 倒置の場合はFalse
            sub_slots = self._analyze_if_clause_for_conditional(if_clause, include_if_prefix)
            
            # 主節の解析
            main_slots = self._analyze_main_clause_for_conditional(main_clause)
            
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
        """
        If仮定法の条件節と主節を分離（構造化解析使用）
        """
        print(f"🔍 if文節分離開始: '{sentence}'")
        
        # Case 151対策: Imagine構文の特殊処理
        if sentence.lower().startswith('imagine if'):
            # "Imagine if we could fly, how exciting it would be!" 
            # -> "if we could fly" + "how exciting it would be"
            comma_pos = sentence.find(',')
            if comma_pos != -1:
                if_part = sentence[:comma_pos].strip()  # "Imagine if we could fly"
                main_part = sentence[comma_pos + 1:].strip()  # "how exciting it would be!"
                
                # "Imagine if" から "if" 部分を抽出
                if_clause = if_part.replace('Imagine ', '').strip()  # "if we could fly"
                main_clause = main_part  # "how exciting it would be!"
                
                print(f"🎯 Imagine構文分離成功")
                print(f"   If節: '{if_clause}'")
                print(f"   主節: '{main_clause}'")
                return if_clause, main_clause
        
        doc = self.nlp(sentence)
        
        # spaCy依存関係による条件節検出
        conditional_info = self._detect_conditional_by_dependency(doc, sentence)
        if conditional_info:
            print(f"🎯 依存関係解析成功")
            return conditional_info["if_clause"], conditional_info["main_clause"]
        
        # パターン分析による補完検出
        print(f"🔍 パターン分析による補完検出")
        pattern_info = self._detect_conditional_by_pattern(doc, sentence)
        return pattern_info["if_clause"], pattern_info["main_clause"]
    
    def _detect_conditional_by_dependency(self, doc, sentence: str) -> Optional[Dict[str, Any]]:
        """
        spaCy依存関係による条件節検出
        """
        print(f"🔍 依存関係による条件節検出: '{sentence}'")
        
        for token in doc:
            print(f"   {token.text}: dep={token.dep_}, pos={token.pos_}, tag={token.tag_}")
            
            # advcl: 副詞節（if節・when節等）
            if token.dep_ == 'advcl':
                # if節かどうか確認
                if_marker = None
                for child in token.children:
                    if child.dep_ == 'mark' and child.text.lower() == 'if':
                        if_marker = child
                        break
                
                if if_marker:
                    print(f"🎯 advcl+mark(if)検出: '{token.text}' → 条件節境界解析")
                    return self._analyze_advcl_conditional(doc, token, if_marker, sentence)
        
        return None
    
    def _analyze_advcl_conditional(self, doc, advcl_token, if_marker, sentence: str) -> Dict[str, Any]:
        """
        advcl条件節の分析（最もシンプルで確実な分割）
        """
        print(f"📋 advcl条件節分析: '{advcl_token.text}'")
        
        # カンマで分割（最も一般的で確実）
        if ',' in sentence:
            parts = sentence.split(',', 1)
            # if句が最初に来る場合（標準的）
            if parts[0].strip().lower().startswith('if'):
                if_clause = parts[0].strip()
                main_clause = parts[1].strip()
            else:
                # if句が後に来る場合（稀）
                main_clause = parts[0].strip()
                if_clause = parts[1].strip()
        else:
            # カンマがない場合はif位置で判定
            if_pos = sentence.lower().find(' if ')
            if if_pos == -1:
                if_pos = 0 if sentence.lower().startswith('if ') else -1
            
            if if_pos == 0 or if_pos == -1:  # 文頭if
                # 主動詞（ROOT）の前後で分割
                root_token = None
                for token in doc:
                    if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                        root_token = token
                        break
                
                if root_token:
                    # if節の動詞位置とmain動詞位置で判定
                    if_verb_pos = -1
                    main_verb_pos = root_token.idx
                    
                    # if節内の動詞を探す
                    for token in doc:
                        if (token.dep_ == 'advcl' and 
                            any(child.dep_ == 'mark' and child.text.lower() == 'if' 
                                for child in token.children)):
                            if_verb_pos = token.idx
                            break
                    
                    if if_verb_pos != -1 and if_verb_pos < main_verb_pos:
                        # if節が先、main節が後
                        split_words = sentence.split()
                        if_end = -1
                        for i, word in enumerate(split_words):
                            if word.lower() in ['will', 'would', 'can', 'could', 'may', 'might', 'should', 'shall']:
                                if_end = i
                                break
                        
                        if if_end > 0:
                            if_clause = ' '.join(split_words[:if_end])
                            main_clause = ' '.join(split_words[if_end:])
                        else:
                            # フォールバック: 文の半分で分割
                            mid = len(split_words) // 2
                            if_clause = ' '.join(split_words[:mid])
                            main_clause = ' '.join(split_words[mid:])
                    else:
                        # フォールバック: 文の半分で分割
                        words = sentence.split()
                        mid = len(words) // 2
                        if_clause = ' '.join(words[:mid])
                        main_clause = ' '.join(words[mid:])
                else:
                    # フォールバック: 文の半分で分割
                    words = sentence.split()
                    mid = len(words) // 2
                    if_clause = ' '.join(words[:mid])
                    main_clause = ' '.join(words[mid:])
            else:
                # 文中if
                if_clause = sentence[if_pos:].strip()
                main_clause = sentence[:if_pos].strip()
        
        print(f"   条件節: '{if_clause}'")
        print(f"   主節: '{main_clause}'")
        
        print("🎯 依存関係解析成功")
        return {
            "if_clause": if_clause,
            "main_clause": main_clause,
            "structure_type": "dependency"
        }
    
    def _detect_conditional_by_pattern(self, doc, sentence: str) -> Dict[str, Any]:
        """
        パターン分析による条件節検出（シンプルで確実な方法）
        """
        print(f"🔍 パターン分析による条件節検出: '{sentence}'")
        
        # カンマで分割を試行（最も確実）
        if ',' in sentence:
            parts = sentence.split(',', 1)
            part1 = parts[0].strip()
            part2 = parts[1].strip()
            
            # ifがどこにあるか確認
            if part1.lower().startswith('if '):
                if_clause = part1
                main_clause = part2
            elif 'if ' in part2.lower():
                main_clause = part1
                if_clause = part2
            else:
                # デフォルト: 最初の部分をif節とする
                if_clause = part1
                main_clause = part2
        else:
            # カンマなしの場合: ifの位置で分割
            sentence_lower = sentence.lower()
            if_pos = sentence_lower.find('if ')
            
            if if_pos == 0:  # 文頭if
                # 助動詞を見つけて分割
                words = sentence.split()
                split_idx = len(words) // 2  # デフォルトは中間
                
                for i, word in enumerate(words):
                    if word.lower() in ['will', 'would', 'can', 'could', 'may', 'might', 'should', 'shall', 'must']:
                        # この助動詞が主節の一部か確認
                        if i > 2:  # "if it rains"より後にある
                            split_idx = i
                            break
                
                if_clause = ' '.join(words[:split_idx])
                main_clause = ' '.join(words[split_idx:])
                
            elif if_pos > 0:  # 文中if
                if_clause = sentence[if_pos:].strip()
                main_clause = sentence[:if_pos].strip()
            else:
                # ifが見つからない場合（エラー処理）
                if_clause = sentence
                main_clause = ""
        
        print(f"📝 If節: '{if_clause}'")
        print(f"📝 主節: '{main_clause}'")
        
        return {
            "if_clause": if_clause,
            "main_clause": main_clause,
            "structure_type": "pattern_based"
        }
    
    def _analyze_main_clause_for_conditional(self, main_clause: str) -> Dict[str, str]:
        """
        仮定法主節の解析（構造化アプローチ使用）- 感嘆文構造対応
        """
        print(f"📋 主節解析開始: '{main_clause}'")
        
        main_slots = {}
        doc = self.nlp(main_clause)
        
        # 感嘆文構造の特殊処理（Case 151対策: "how exciting it would be"）
        if main_clause.lower().startswith(('how ', 'what ', 'so ')):
            print(f"🎯 感嘆文構造検出: {main_clause}")
            
            tokens = main_clause.split()
            exclamation_word = tokens[0]  # "how"
            
            # "how exciting it would be" -> M2: "how", C1: "exciting", S: "it", Aux: "would", V: "be"
            main_slots["M2"] = exclamation_word
            
            # 残りの部分を解析 "exciting it would be"
            remaining = ' '.join(tokens[1:])
            doc_remaining = self.nlp(remaining)
            
            print(f"🔍 感嘆文残り部分解析: '{remaining}'")
            for token in doc_remaining:
                print(f"   {token.text}: dep={token.dep_}, pos={token.pos_}, tag={token.tag_}")
            
            # 詳細な要素抽出
            complement = ""    # exciting
            subject = ""       # it
            auxiliary = ""     # would
            verb = ""          # be
            
            # spaCy解析による詳細抽出
            for token in doc_remaining:
                if token.pos_ == 'ADJ' and token.dep_ in ['acomp', 'amod'] and not complement:
                    complement = token.text  # "exciting"
                elif token.dep_ in ['nsubj', 'nsubjpass', 'expl'] and not subject:
                    subject = token.text     # "it"
                elif token.pos_ in ['AUX'] and not auxiliary:
                    auxiliary = token.text   # "would"
                elif token.pos_ == 'VERB' and token.dep_ in ['ROOT', 'cop'] and not verb:
                    verb = token.text        # "be"
            
            # スロット設定
            if complement:
                main_slots["C1"] = complement
            if subject:
                main_slots["S"] = subject
            if auxiliary:
                main_slots["Aux"] = auxiliary
            if verb:
                main_slots["V"] = verb
            else:
                # 'be'動詞が抜けている場合の補完（Case 151対策）
                for token in doc_remaining:
                    if token.pos_ in ['AUX', 'VERB'] and token.dep_ == 'ROOT':
                        main_slots["V"] = token.text
                        break
                
            print(f"   感嘆文解析結果:")
            print(f"   M2: '{main_slots.get('M2', '')}'")
            print(f"   C1: '{main_slots.get('C1', '')}'")
            print(f"   S: '{main_slots.get('S', '')}'")
            print(f"   Aux: '{main_slots.get('Aux', '')}'")
            print(f"   V: '{main_slots.get('V', '')}'")
            
            return main_slots
        
        # 通常の主節解析
        # 各要素を解析
        main_slots["M1"] = ""  # 条件節情報は別途設定
        
        # 主語検出
        subject = self._extract_subject(doc)
        main_slots["S"] = subject if subject else ""
        
        # 助動詞検出
        auxiliary = self._extract_auxiliary(doc)
        main_slots["Aux"] = auxiliary if auxiliary else ""
        
        # 動詞検出
        verb = self._extract_main_verb(doc)
        main_slots["V"] = verb if verb else ""
        
        # その他の要素検出
        other_elements = self._extract_other_elements(doc, subject, auxiliary, verb)
        main_slots["M2"] = other_elements if other_elements else ""
        
        print(f"   主語: '{main_slots['S']}'")
        print(f"   助動詞: '{main_slots['Aux']}'")
        print(f"   動詞: '{main_slots['V']}'")
        print(f"   その他: '{main_slots['M2']}'")
        
        return main_slots
    
    def _extract_subject(self, doc) -> str:
        """主語を抽出"""
        for token in doc:
            if token.dep_ in ['nsubj', 'nsubjpass', 'csubj']:
                # 主語とその修飾語を含める
                subject_tokens = [token]
                for child in token.children:
                    if child.dep_ in ['det', 'amod', 'compound']:
                        subject_tokens.append(child)
                subject_tokens.sort(key=lambda t: t.i)
                return " ".join([t.text for t in subject_tokens])
        return ""
    
    def _extract_auxiliary(self, doc) -> str:
        """助動詞を抽出"""
        for token in doc:
            if token.dep_ == 'aux' or token.pos_ == 'AUX':
                return token.text
        return ""
    
    def _extract_main_verb(self, doc) -> str:
        """主動詞を抽出"""
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                return token.text
        return ""
    
    def _extract_other_elements(self, doc, subject: str, auxiliary: str, verb: str) -> str:
        """その他の要素を抽出"""
        used_words = set()
        if subject:
            used_words.update(subject.split())
        if auxiliary:
            used_words.add(auxiliary)
        if verb:
            used_words.add(verb)
        
        other_tokens = []
        for token in doc:
            if (token.text not in used_words and 
                token.pos_ not in ['PUNCT'] and
                token.dep_ not in ['aux', 'nsubj', 'ROOT']):
                other_tokens.append(token)
        
        other_tokens.sort(key=lambda t: t.i)
        return " ".join([t.text for t in other_tokens])
    
    def _analyze_if_clause_for_conditional(self, if_clause: str, include_if: bool = True) -> Dict[str, str]:
        """
        仮定法if節の解析（構造化アプローチ使用）
        
        Args:
            if_clause: if節の文字列
            include_if: Ifを含めるかどうか（倒置仮定法ではFalse）
        """
        print(f"📋 if節解析開始: '{if_clause}' (include_if={include_if})")
        
        sub_slots = {}
        
        # "if"を除去して解析
        clause_without_if = if_clause.lower().replace("if ", "").strip()
        doc = self.nlp(clause_without_if)
        
        # 主語検出
        subject = self._extract_subject(doc)
        
        # include_ifフラグに応じてIfを付けるかどうか決定
        if include_if:
            sub_slots["sub-s"] = f"If {subject}" if subject else "If it"
        else:
            sub_slots["sub-s"] = subject if subject else "it"
        
        # 動詞検出
        verb = self._extract_main_verb(doc)
        sub_slots["sub-v"] = verb if verb else ""
        
        # その他の要素検出
        other_elements = self._extract_other_elements(doc, subject, "", verb)
        sub_slots["sub-m2"] = other_elements if other_elements else ""
        
        # 親スロット情報
        sub_slots["_parent_slot"] = "M1"
        
        print(f"   if主語: '{sub_slots['sub-s']}'")
        print(f"   if動詞: '{sub_slots['sub-v']}'")
        print(f"   ifその他: '{sub_slots['sub-m2']}'")
        
        return sub_slots
    
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
            main_slots = self._analyze_main_clause_for_conditional(main_clause)
            
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
            main_clause = ' '.join(parts[1:]).strip()  # コンマを除去してスペース区切りに
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
            main_slots = self._analyze_main_clause_for_conditional(main_part)
            
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
            main_slots = self._analyze_main_clause_for_conditional(main_clause)
            
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
            main_slots = self._analyze_main_clause_for_conditional(main_clause)
            
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
        
        # Imagine構文の特殊処理（Case 151対策）
        if conditional_type == 'imagine':
            # "Imagine if we could fly" -> sub-s: "Imagine if we"
            if 'if' in condition_clause.lower():
                # "if" までの部分を sub-s に含める
                if_index = condition_clause.lower().find('if')
                before_if = condition_clause[:if_index + 2].strip()  # "if"
                after_if = condition_clause[if_index + 2:].strip()   # "we could fly"
                
                # 主語を抽出
                doc_after = self.nlp(after_if)
                subject = ""
                auxiliary = ""
                
                for token in doc_after:
                    if token.dep_ == 'nsubj':
                        subject = token.text
                    elif token.pos_ == 'AUX':
                        auxiliary = token.text
                
                # sub-s に "Imagine if + 主語" を設定（Case 151期待値対応）
                if subject:
                    sub_slots['sub-s'] = f"{before_if} {subject}"  # "Imagine"は既にbefore_ifに含まれている
                else:
                    sub_slots['sub-s'] = before_if
                
                # 助動詞の設定（Case 151期待値対応）
                if auxiliary:
                    sub_slots['sub-aux'] = auxiliary
                
                # 動詞と目的語の抽出
                for token in doc_after:
                    if token.pos_ == 'VERB' and 'sub-v' not in sub_slots:
                        sub_slots['sub-v'] = token.text
                    elif token.dep_ in ['dobj', 'pobj'] and 'sub-o1' not in sub_slots:
                        sub_slots['sub-o1'] = token.text
                
                return sub_slots
        
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
        
        # 条件詞 + 主語の設定（Case 150対策）
        if subject:
            sub_slots['sub-s'] = f"{condition_word} {subject}"
        else:
            sub_slots['sub-s'] = condition_word
        
        # 動詞・助動詞・目的語等の解析（条件詞以外の動詞を対象）
        verb = ""
        auxiliary = ""
        obj = ""
        modifier = ""
        
        for token in doc:
            # 条件詞（Suppose等）は動詞として除外
            if token.pos_ == 'VERB' and token.text.lower() != conditional_type.lower():
                if not verb:
                    verb = token.text
            elif token.pos_ == 'AUX' and not auxiliary:
                auxiliary = token.text
            elif token.dep_ in ['dobj', 'pobj'] and token.pos_ != 'PRON':  # 疑問詞を除外
                # 形容詞修飾語も含めて目的語を構築
                obj_parts = []
                
                # 目的語の修飾語を収集
                for child in token.children:
                    if child.dep_ == 'amod':  # 形容詞修飾語
                        obj_parts.append(child.text)
                
                # 形容詞 + 名詞の順序で構築
                obj_parts.append(token.text)
                obj += ' '.join(obj_parts) + " "
                
            elif token.dep_ in ['advmod', 'npadvmod']:
                modifier += token.text + " "
        
        # Unless/Suppose構文の場合は助動詞をサブスロットに含めない
        # 助動詞は主節に属するため
        if conditional_type.lower() not in ['suppose', 'unless'] and auxiliary:
            sub_slots['sub-aux'] = auxiliary
        if verb:
            sub_slots['sub-v'] = verb
        # Unless構文では条件節に目的語は含めない
        if conditional_type.lower() != 'unless' and obj.strip():
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
