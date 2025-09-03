"""
Basic Five Pattern Handler - 5文型専門処理ハンドラー
Phase 1: 100%精度目標

Human Grammar Pattern:
- spaCy POS解析を情報源とした文法パターン認識
- 人間が文法体系を理解するように全体構造からパターン照合
- 依存関係解析は使用せず、POSタグベースの認識
"""

import spacy
from typing import Dict, List, Any, Optional


class BasicFivePatternHandler:
    """
    5文型専門ハンドラー
    
    責任:
    - 5文型の識別・分解処理
    - Rephraseスロット配置
    - 100%精度の実現
    
    禁止:
    - 依存関係解析の使用
    - 他ハンドラーとの直接通信
    - ハードコーディング
    """
    
    def __init__(self):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        
        # 5文型パターン定義
        self.patterns = {
            'SV': ['S', 'V'],                    # 第1文型
            'SVC': ['S', 'V', 'C1'],             # 第2文型  
            'SVO': ['S', 'V', 'O1'],             # 第3文型
            'SVOO': ['S', 'V', 'O1', 'O2'],      # 第4文型
            'SVOC': ['S', 'V', 'O1', 'C2']       # 第5文型
        }
        
        # 文型判定用動詞分類
        self.verb_types = {
            'linking': ['be', 'seem', 'become', 'appear', 'look', 'sound', 'feel', 'taste', 'smell', 'remain', 'stay', 'turn', 'grow'],
            'transitive': ['love', 'like', 'see', 'hear', 'make', 'take', 'give', 'send', 'show', 'read', 'play', 'study'],
            'ditransitive': ['give', 'send', 'show', 'tell', 'teach', 'buy', 'make', 'get', 'find', 'offer'],
            'causative': ['make', 'let', 'have', 'get', 'help', 'see', 'hear', 'watch', 'call', 'find', 'consider']
        }
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        5文型処理メイン
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果（success, slots, error）
        """
        try:
            doc = self.nlp(text)
            
            # 1. 基本要素抽出（POS解析ベース）
            elements = self._extract_basic_elements(doc)
            
            if not elements:
                return {'success': False, 'error': '基本要素が抽出できませんでした'}
            
            # 2. 文型判定
            pattern_type = self._identify_pattern(elements, doc)
            
            if not pattern_type:
                return {'success': False, 'error': '文型を判定できませんでした'}
            
            # 3. スロット配置
            slots = self._assign_slots(elements, pattern_type)
            
            return {
                'success': True,
                'slots': slots,
                'pattern_type': pattern_type
            }
            
        except Exception as e:
            return {'success': False, 'error': f'処理エラー: {str(e)}'}
    
    def _extract_basic_elements(self, doc) -> Dict[str, str]:
        """
        基本要素抽出: S, V, O, C の候補を抽出
        
        重要: 前置詞句の名詞は基本スロット（S, O1, O2, C1, C2）から完全除外
        
        Args:
            doc: spaCy Doc オブジェクト
            
        Returns:
            Dict: 抽出された要素
        """
        elements = {}
        
        # 主語候補（文頭の名詞句全体を抽出）
        subject_tokens = []
        for token in doc:
            if token.pos_ in ['DET', 'ADJ', 'NOUN', 'PRON', 'PROPN']:
                subject_tokens.append(token.text)
            elif token.pos_ in ['VERB', 'AUX']:
                break  # 動詞に到達したら主語終了
            elif subject_tokens:  # 主語候補があり、動詞以外に到達したら終了
                break
        
        if subject_tokens:
            elements['S'] = ' '.join(subject_tokens)
        
        # 動詞抽出と位置特定
        verb_idx = None
        for i, token in enumerate(doc):
            if token.pos_ == 'VERB' and not token.lemma_ in ['be']:
                elements['V'] = token.text
                verb_idx = i
                break
            elif token.pos_ == 'AUX' and token.lemma_ == 'be':
                elements['V'] = token.text
                verb_idx = i
                break
        
        if verb_idx is None:
            return elements
        
        # 🔥 重要: 前置詞句検出と除外
        # 動詞後の要素から前置詞句を完全に除外
        core_elements = []  # 基本スロット候補（前置詞句除外後）
        
        i = verb_idx + 1
        while i < len(doc):
            token = doc[i]
            
            if token.pos_ == 'PUNCT':
                i += 1
                continue
                
            elif token.pos_ == 'ADP':  # 前置詞発見
                # 前置詞句全体をスキップ（前置詞＋名詞句）
                print(f"🚫 前置詞句検出・除外: '{token.text}' から文末まで")
                while i < len(doc) and doc[i].pos_ != 'PUNCT':
                    i += 1
                break  # 前置詞句以降は全てスキップ
                
            elif token.pos_ in ['NOUN', 'PRON', 'PROPN', 'ADJ', 'DET']:
                core_elements.append(token)
                i += 1
                
            else:
                i += 1
        
        print(f"🔍 前置詞句除外後の核要素: {[token.text for token in core_elements]}")
        
        if not core_elements:
            return elements
        
        # 動詞の種類判定（連結動詞かどうか）
        verb_lemma = doc[verb_idx].lemma_
        is_linking_verb = verb_lemma in self.verb_types['linking']
        is_causative_verb = verb_lemma in self.verb_types['causative']
        is_ditransitive_verb = verb_lemma in self.verb_types['ditransitive']
        
        # 要素分類（動詞の種類に応じて処理）
        elements_found = []
        
        if is_causative_verb or is_ditransitive_verb:
            # 使役動詞・授与動詞の場合：特別な処理
            current_phrase = []
            
            for token in core_elements:
                if token.pos_ in ['DET', 'ADJ', 'NOUN', 'PRON', 'PROPN']:
                    if token.pos_ == 'PRON' and current_phrase:
                        # 代名詞が来た場合、前の句を終了して新しい句を開始
                        if current_phrase:
                            phrase_text = ' '.join([t.text for t in current_phrase])
                            elements_found.append(('NOUN', phrase_text))
                        current_phrase = [token]
                    elif token.pos_ == 'PRON':
                        # 単独の代名詞
                        elements_found.append(('NOUN', token.text))
                    elif token.pos_ == 'ADJ':
                        # 単独の形容詞
                        if current_phrase:
                            phrase_text = ' '.join([t.text for t in current_phrase])
                            elements_found.append(('NOUN', phrase_text))
                            current_phrase = []
                        elements_found.append(('ADJ', token.text))
                    else:
                        current_phrase.append(token)
            
            # 最後の句を処理
            if current_phrase:
                phrase_text = ' '.join([t.text for t in current_phrase])
                elements_found.append(('NOUN', phrase_text))
        else:
            # 通常の場合：句ベースで処理
            current_phrase = []
            
            for token in core_elements:
                if token.pos_ in ['DET', 'ADJ', 'NOUN', 'PRON', 'PROPN']:
                    current_phrase.append(token)
                elif current_phrase:  # 句の終了
                    phrase_text = ' '.join([t.text for t in current_phrase])
                    
                    # 最後のトークンのPOSで判定
                    last_token_pos = current_phrase[-1].pos_
                    
                    if last_token_pos == 'ADJ':
                        elements_found.append(('ADJ', phrase_text))
                    else:
                        elements_found.append(('NOUN', phrase_text))
                    current_phrase = []
            
            # 最後の句を処理
            if current_phrase:
                phrase_text = ' '.join([t.text for t in current_phrase])
                
                # 最後のトークンのPOSで判定
                last_token_pos = current_phrase[-1].pos_
                
                if last_token_pos == 'ADJ':
                    elements_found.append(('ADJ', phrase_text))
                else:
                    elements_found.append(('NOUN', phrase_text))
        
        # 文型判定とスロット配置
        noun_count = len([e for e in elements_found if e[0] == 'NOUN'])
        adj_count = len([e for e in elements_found if e[0] == 'ADJ'])
        
        if is_linking_verb and adj_count > 0:
            # 第2文型: 連結動詞 + 形容詞
            adj_elements = [e[1] for e in elements_found if e[0] == 'ADJ']
            elements['C1'] = adj_elements[0]
            
        elif is_linking_verb and noun_count > 0:
            # 第2文型: 連結動詞 + 名詞（補語）
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['C1'] = noun_elements[0]
            
        elif is_ditransitive_verb and noun_count == 2:
            # 第4文型: 授与動詞 + 間接目的語 + 直接目的語
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['O1'] = noun_elements[0]
            elements['O2'] = noun_elements[1]
            
        elif is_causative_verb and noun_count == 2:
            # 第5文型: 使役動詞 + 目的語 + 補語（名詞）
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['O1'] = noun_elements[0]
            elements['C2'] = noun_elements[1]
            
        elif is_causative_verb and noun_count == 1 and adj_count == 1:
            # 第5文型: 使役動詞 + 目的語 + 補語（形容詞）
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            adj_elements = [e[1] for e in elements_found if e[0] == 'ADJ']
            elements['O1'] = noun_elements[0]
            elements['C2'] = adj_elements[0]
            
        elif noun_count == 1 and adj_count == 0:
            # 第3文型: 他動詞 + 目的語
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['O1'] = noun_elements[0]
            
        elif noun_count == 2 and adj_count == 0:
            # 第4文型: 授与動詞 + 間接目的語 + 直接目的語
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['O1'] = noun_elements[0]
            elements['O2'] = noun_elements[1]
                
        return elements
    
    def _identify_pattern(self, elements: Dict[str, str], doc) -> Optional[str]:
        """
        文型判定: 抽出された要素から5文型を判定
        
        Args:
            elements: 抽出された基本要素
            doc: spaCy Doc オブジェクト
            
        Returns:
            Optional[str]: 判定された文型
        """
        if not elements.get('S') or not elements.get('V'):
            return None
        
        # 動詞の連結動詞判定
        verb_lemma = None
        for token in doc:
            if token.pos_ in ['VERB', 'AUX'] and token.text.lower() == elements['V'].lower():
                verb_lemma = token.lemma_
                break
        
        is_linking_verb = verb_lemma in self.verb_types['linking'] if verb_lemma else False
        
        # 第2文型: 連結動詞 + 補語
        if is_linking_verb and elements.get('C1'):
            return 'SVC'
        
        # 第5文型: 使役動詞 + O + C
        if elements.get('O1') and elements.get('C2'):
            return 'SVOC'
        
        # 第4文型: 授与動詞 + O1 + O2
        if elements.get('O1') and elements.get('O2'):
            return 'SVOO'
        
        # 第3文型: 他動詞 + O
        if elements.get('O1'):
            return 'SVO'
        
        # 第1文型: 自動詞のみ
        return 'SV'
    
    def _assign_slots(self, elements: Dict[str, str], pattern_type: str) -> Dict[str, str]:
        """
        スロット配置: 文型に応じたRephraseスロット配置
        
        Args:
            elements: 抽出された要素
            pattern_type: 判定された文型
            
        Returns:
            Dict: スロット配置結果
        """
        slots = {}
        pattern = self.patterns[pattern_type]
        
        for slot in pattern:
            if slot == 'S' and elements.get('S'):
                slots['S'] = elements['S']
            elif slot == 'V' and elements.get('V'):
                slots['V'] = elements['V']
            elif slot == 'O1' and elements.get('O1'):
                slots['O1'] = elements['O1']
            elif slot == 'O2' and elements.get('O2'):
                slots['O2'] = elements['O2']
            elif slot == 'C1' and elements.get('C1'):
                slots['C1'] = elements['C1']
            elif slot == 'C2' and elements.get('C2'):
                slots['C2'] = elements['C2']
        
        return slots


if __name__ == "__main__":
    # 基本テスト
    handler = BasicFivePatternHandler()
    
    test_cases = [
        ("She is happy.", "SVC"),
        ("I love you.", "SVO"),
        ("He gave me a book.", "SVOO"),
        ("We made him happy.", "SVOC"),
        ("Birds fly.", "SV")
    ]
    
    print("=== BasicFivePatternHandler テスト ===")
    for sentence, expected in test_cases:
        print(f"\n入力: {sentence}")
        print(f"期待: {expected}")
        result = handler.process(sentence)
        print(f"結果: {result}")
