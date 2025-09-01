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
    仮定法文の処理を専門とするハンドラー
    
    機能:
    - If仮定法の条件節・主節分離
    - 仮定法パターンの識別と分類
    - spaCy依存関係解析による構文解析
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
        
        print("ConditionalHandler初期化完了")
    
    def _initialize_conditional_patterns(self):
        """仮定法パターンの初期化"""
        
        # If仮定法パターン
        self.if_patterns = {
            'present': r'\bif\s+.*\s+(will|can|may|shall|must)\b',
            'past': r'\bif\s+.*\s+(would|could|might|should)\b',
            'past_perfect': r'\bif\s+.*\s+had\s+.*\s+(would|could|might|should)\s+have\b',
            'mixed': r'\bif\s+.*\s+had\s+.*\s+(would|could|might|should)\b'
        }
        
        # 倒置仮定法パターン
        self.inversion_patterns = {
            'were': r'^were\s+\w+\s+.*',
            'had': r'^had\s+\w+\s+.*',
            'should': r'^should\s+\w+\s+.*'
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
            'supposing': r'\bsupposing\s+.*'
        }
    
    def detect_conditional_patterns(self, text: str) -> List[str]:
        """仮定法パターンの検出"""
        detected_patterns = []
        
        # If仮定法の検出
        for pattern_name, pattern in self.if_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(f"if_{pattern_name}")
        
        # 倒置仮定法の検出
        for pattern_name, pattern in self.inversion_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(f"inversion_{pattern_name}")
        
        # As if/though仮定法の検出
        for pattern_name, pattern in self.as_if_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(pattern_name)
        
        # 仮定法相当語句の検出
        for pattern_name, pattern in self.equivalent_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_patterns.append(pattern_name)
        
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
            print(f"ConditionalHandler処理開始: '{sentence}'")
            
            # spaCy解析
            doc = self.nlp(sentence)
            
            # 前処理: 句読点除去と正規化
            clean_sentence = self._preprocess_sentence(sentence)
            
            # 仮定法パターン識別
            conditional_type = self._identify_conditional_type(clean_sentence)
            
            if not conditional_type:
                return {'success': False, 'error': 'No conditional pattern detected'}
            
            print(f"仮定法タイプ検出: {conditional_type}")
            
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
            print(f"ConditionalHandler処理エラー: {e}")
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
        
        # If仮定法の識別
        if re.search(r'\bif\b', sentence, re.IGNORECASE):
            # 現在仮定法
            if re.search(r'\bif\s+.*\s+(will|can|may|shall|must)\b', sentence, re.IGNORECASE):
                return 'if_present'
            # 過去仮定法
            elif re.search(r'\bif\s+.*\s+(would|could|might|should)\b', sentence, re.IGNORECASE):
                return 'if_past'
            # 過去完了仮定法
            elif re.search(r'\bif\s+.*\s+had\s+.*\s+(would|could|might|should)\s+have\b', sentence, re.IGNORECASE):
                return 'if_past_perfect'
            # 混合仮定法
            elif re.search(r'\bif\s+.*\s+had\s+.*\s+(would|could|might|should)\b', sentence, re.IGNORECASE):
                return 'if_mixed'
            else:
                return 'if_general'
        
        # 倒置仮定法の識別
        if re.search(r'^were\s+\w+', sentence, re.IGNORECASE):
            return 'inversion_were'
        elif re.search(r'^had\s+\w+', sentence, re.IGNORECASE):
            return 'inversion_had'
        elif re.search(r'^should\s+\w+', sentence, re.IGNORECASE):
            return 'inversion_should'
        
        # Wish仮定法の識別
        if re.search(r'\bwish\b', sentence, re.IGNORECASE):
            return 'wish'
        
        # As if/though仮定法の識別
        if re.search(r'\bas\s+if\b', sentence, re.IGNORECASE):
            return 'as_if'
        elif re.search(r'\bas\s+though\b', sentence, re.IGNORECASE):
            return 'as_though'
        
        # 仮定法相当語句の識別
        if re.search(r'\bwithout\b', sentence, re.IGNORECASE):
            return 'without'
        elif re.search(r'\bbut\s+for\b', sentence, re.IGNORECASE):
            return 'but_for'
        elif re.search(r'\bunless\b', sentence, re.IGNORECASE):
            return 'unless'
        elif re.search(r'\bsuppose\b', sentence, re.IGNORECASE):
            return 'suppose'
        elif re.search(r'\bprovided\b', sentence, re.IGNORECASE):
            return 'provided'
        
        return None
    
    def _process_if_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """If仮定法の処理"""
        try:
            print(f"If仮定法処理開始: {conditional_type}")
            
            # If節と主節の分離
            if_clause, main_clause = self._split_if_conditional(sentence)
            
            if not if_clause or not main_clause:
                return {'success': False, 'error': 'Failed to split conditional clauses'}
            
            print(f"If節: '{if_clause}'")
            print(f"主節: '{main_clause}'")
            
            # 主節の解析（期待値フォーマットに対応）
            main_slots = self._analyze_main_clause_for_conditional(main_clause)
            
            # If節の解析（期待値フォーマットに対応）
            sub_slots = self._analyze_if_clause_for_conditional(if_clause)
            
            # 親スロット決定
            parent_slot = self._determine_parent_slot_for_conditional(main_slots)
            sub_slots['_parent_slot'] = parent_slot
            
            # 親スロットを空にする
            main_slots[parent_slot] = ""
            
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
            print(f"If仮定法処理エラー: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_main_clause_for_conditional(self, main_clause: str) -> Dict[str, str]:
        """条件文の主節解析（期待値フォーマットに対応）"""
        main_slots = {"M1": "", "S": "", "Aux": "", "V": "", "O1": "", "C1": "", "M2": ""}
        
        doc = self.nlp(main_clause)
        
        # 基本構造抽出
        for token in doc:
            if token.dep_ in ['nsubj', 'nsubjpass'] and not main_slots["S"]:
                main_slots["S"] = token.text
            elif token.tag_ in ['MD', 'VBZ', 'VBP', 'VBD'] and token.dep_ == 'aux':
                main_slots["Aux"] = token.text
            elif token.dep_ == 'ROOT' or (token.pos_ == 'VERB' and token.dep_ != 'aux'):
                main_slots["V"] = token.text
            elif token.dep_ in ['dobj'] and not main_slots["O1"]:
                # 目的語の処理（複合語句対応）
                obj_phrase = self._extract_phrase(token, doc)
                main_slots["O1"] = obj_phrase
            elif token.dep_ in ['acomp', 'attr'] and not main_slots["C1"]:
                main_slots["C1"] = token.text
            elif token.dep_ in ['advmod', 'npadvmod', 'prep'] and not main_slots["M2"]:
                # 修飾語の処理
                mod_phrase = self._extract_phrase(token, doc)
                main_slots["M2"] = mod_phrase
        
        # 空のスロットを削除
        main_slots = {k: v for k, v in main_slots.items() if v}
        
        return main_slots
    
    def _analyze_if_clause_for_conditional(self, if_clause: str) -> Dict[str, str]:
        """If条件節の解析（期待値フォーマットに対応）"""
        sub_slots = {}
        
        # "If"を含む主語部分
        doc = self.nlp(if_clause)
        
        # If + 主語の抽出
        if_subject = ""
        verb = ""
        complement = ""
        modifier = ""
        
        for token in doc:
            if token.text.lower() == 'if':
                # Ifの次のトークンが主語
                next_tokens = []
                for i in range(token.i + 1, len(doc)):
                    next_token = doc[i]
                    if next_token.dep_ in ['nsubj', 'nsubjpass']:
                        next_tokens.append(next_token.text)
                        break
                    elif next_token.pos_ in ['NOUN', 'PRON', 'DET']:
                        next_tokens.append(next_token.text)
                    else:
                        break
                if next_tokens:
                    if_subject = f"If {' '.join(next_tokens)}"
                else:
                    if_subject = "If"
            elif token.dep_ == 'ROOT' or (token.pos_ == 'VERB' and token.dep_ != 'aux'):
                verb = token.text
            elif token.dep_ in ['acomp', 'attr']:
                complement = token.text
            elif token.dep_ in ['advmod', 'npadvmod', 'prep']:
                mod_phrase = self._extract_phrase(token, doc)
                if mod_phrase:
                    modifier = mod_phrase
        
        # sub_slotsの構築
        if if_subject:
            sub_slots['sub-s'] = if_subject
        if verb:
            sub_slots['sub-v'] = verb
        if complement:
            sub_slots['sub-c1'] = complement
        if modifier:
            sub_slots['sub-m2'] = modifier
        
        return sub_slots
    
    def _extract_phrase(self, token, doc) -> str:
        """トークンから完全なフレーズを抽出"""
        phrase_tokens = [token]
        
        # 子要素を追加
        for child in token.children:
            if child.dep_ in ['det', 'amod', 'compound', 'prep', 'pobj']:
                phrase_tokens.append(child)
                # 子の子も確認
                for grandchild in child.children:
                    if grandchild.dep_ in ['det', 'amod', 'pobj']:
                        phrase_tokens.append(grandchild)
        
        # トークンの位置でソート
        phrase_tokens.sort(key=lambda x: x.i)
        
        return ' '.join([t.text for t in phrase_tokens])
    
    def _determine_parent_slot_for_conditional(self, main_slots: Dict[str, str]) -> str:
        """条件節の配置先スロット（M1またはM2）を決定"""
        # 基本的にはM1を優先、M1が既に使用されている場合はM2
        if not main_slots.get("M1"):
            return "M1"
        elif not main_slots.get("M2"):
            return "M2"
        else:
            # 両方使用されている場合はM1を上書き
            return "M1"
    
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
    
    # 以下、他の仮定法タイプの処理メソッド（簡略版）
    def _process_inversion_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """倒置仮定法の処理"""
        return {'success': False, 'error': 'Inversion conditional not implemented yet'}
    
    def _process_wish_conditional(self, doc, sentence: str) -> Dict[str, Any]:
        """Wish仮定法の処理"""
        return {'success': False, 'error': 'Wish conditional not implemented yet'}
    
    def _process_as_if_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """As if/though仮定法の処理"""
        return {'success': False, 'error': 'As if conditional not implemented yet'}
    
    def _process_without_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """仮定法相当語句の処理"""
        return {'success': False, 'error': 'Without conditional not implemented yet'}
    
    def _process_other_conditional(self, doc, sentence: str, conditional_type: str) -> Dict[str, Any]:
        """その他の仮定法の処理"""
        return {'success': False, 'error': 'Other conditional not implemented yet'}
