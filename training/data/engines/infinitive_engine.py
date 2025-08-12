#!/usr/bin/env python3
"""
Infinitive Engine - 不定詞構文処理
Stanzaの構造を活用した不定詞構文の分解

核心原則:
1. Stanza依存関係による不定詞パターン検出 (csubj, xcomp, acl)
2. "to" マーカーの保持
3. Rephraseルール準拠の上位・サブスロット分解
4. 不定詞の機能別処理（主語・目的語・副詞・形容詞修飾）
"""

import stanza
from typing import Dict, List, Optional, Any

class InfinitiveEngine:
    """不定詞構文エンジン"""
    
    def __init__(self):
        print("🚀 不定詞構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 不定詞の依存関係パターン
        self.infinitive_patterns = {
            'csubj': 'subject',      # 主語不定詞: "To swim is fun"
            'xcomp': 'complement',   # 補語不定詞: "He wants to go", "I want him to come"
            'acl': 'adjectival',     # 形容詞修飾: "nothing to do", "work to finish"
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """メイン処理"""
        print(f"🔍 不定詞構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 不定詞構文の構造解析
        infinitive_info = self._analyze_infinitive_structure(sent)
        
        if infinitive_info:
            return self._process_infinitive_construction(sent, infinitive_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_infinitive_structure(self, sent) -> Optional[Dict]:
        """不定詞構文の構造分析"""
        # 不定詞動詞を探す（csubj, xcomp, acl関係）
        for word in sent.words:
            if word.deprel in self.infinitive_patterns:
                # "to" マーカーを確認
                to_marker = self._find_to_marker(sent, word)
                if to_marker:
                    structure_info = {
                        'infinitive_verb': word,
                        'to_marker': to_marker,
                        'pattern_type': self.infinitive_patterns[word.deprel],
                        'head_word': sent.words[word.head - 1] if word.head > 0 else None
                    }
                    
                    print(f"  📋 不定詞構文検出:")
                    print(f"    不定詞動詞: {word.text} ({word.deprel})")
                    print(f"    パターン: {structure_info['pattern_type']}")
                    print(f"    依存先: {structure_info['head_word'].text if structure_info['head_word'] else '?'}")
                    return structure_info
        
        return None
    
    def _find_to_marker(self, sent, infinitive_verb) -> Optional[Any]:
        """不定詞の "to" マーカーを探す"""
        for word in sent.words:
            if word.head == infinitive_verb.id and word.deprel == 'mark' and word.text.lower() == 'to':
                return word
        return None
    
    def _process_infinitive_construction(self, sent, infinitive_info) -> Dict[str, str]:
        """不定詞構文の処理 - Rephraseルール準拠"""
        infinitive_verb = infinitive_info['infinitive_verb']
        pattern_type = infinitive_info['pattern_type']
        head_word = infinitive_info['head_word']
        
        result = {}
        
        if pattern_type == 'subject':
            # 主語不定詞: "To swim is fun"
            result.update(self._process_subject_infinitive(sent, infinitive_verb, head_word))
            
        elif pattern_type == 'complement':
            # 補語不定詞の種類を判定
            if self._is_adverbial_complement(sent, infinitive_verb, head_word):
                # 副詞的: "He came to help"
                result.update(self._process_adverbial_infinitive(sent, infinitive_verb, head_word))
            else:
                # 目的語的: "He wants to go", "I want him to come"
                result.update(self._process_object_infinitive(sent, infinitive_verb, head_word))
                
        elif pattern_type == 'adjectival':
            # 形容詞修飾: "nothing to do", "work to finish"
            result.update(self._process_adjectival_infinitive(sent, infinitive_verb, head_word))
        
        print(f"  ✅ Rephraseルール準拠分解: {result}")
        return result
    
    def _process_subject_infinitive(self, sent, infinitive_verb, head_word) -> Dict[str, str]:
        """主語不定詞の処理: To swim is fun"""
        result = {}
        
        # 不定詞句をサブスロットに
        infinitive_phrase = self._build_infinitive_phrase(sent, infinitive_verb)
        result['sub-v'] = infinitive_phrase
        
        # 主節の処理
        if head_word:
            main_elements = self._extract_main_clause_elements(sent, head_word, [infinitive_verb])
            result.update(main_elements)
        
        return result
    
    def _process_object_infinitive(self, sent, infinitive_verb, head_word) -> Dict[str, str]:
        """目的語不定詞の処理"""
        result = {}
        
        # 主節の主語・動詞
        main_elements = self._extract_main_clause_elements(sent, head_word, [infinitive_verb])
        result.update(main_elements)
        
        # 不定詞句の処理
        infinitive_phrase = self._build_infinitive_phrase(sent, infinitive_verb)
        
        # 目的語不定詞かチェック: "I want him to come"
        obj_before_infinitive = self._find_object_before_infinitive(sent, head_word, infinitive_verb)
        if obj_before_infinitive:
            # C2位置: "I want him to come"
            result['O1'] = obj_before_infinitive.text
            result['sub-v'] = infinitive_phrase
        else:
            # O1位置: "He wants to go"
            result['sub-v'] = infinitive_phrase
        
        return result
    
    def _process_adverbial_infinitive(self, sent, infinitive_verb, head_word) -> Dict[str, str]:
        """副詞的不定詞の処理: He came to help"""
        result = {}
        
        # 主節の処理
        main_elements = self._extract_main_clause_elements(sent, head_word, [infinitive_verb])
        result.update(main_elements)
        
        # M2位置に不定詞句
        infinitive_phrase = self._build_infinitive_phrase(sent, infinitive_verb)
        result['sub-v'] = infinitive_phrase
        
        return result
    
    def _process_adjectival_infinitive(self, sent, infinitive_verb, head_word) -> Dict[str, str]:
        """形容詞修飾不定詞の処理: nothing to do, work to finish"""
        result = {}
        
        # 主節の動詞を探す
        main_verb = self._find_main_verb(sent)
        if main_verb:
            main_elements = self._extract_main_clause_elements(sent, main_verb, [infinitive_verb, head_word])
            result.update(main_elements)
        
        # O1位置に名詞+不定詞、サブスロットに不定詞
        infinitive_phrase = self._build_infinitive_phrase(sent, infinitive_verb)
        noun_phrase = self._build_noun_infinitive_phrase(sent, head_word, infinitive_verb)
        
        result['O1'] = noun_phrase
        result['sub-v'] = infinitive_phrase
        
        return result
    
    def _build_infinitive_phrase(self, sent, infinitive_verb) -> str:
        """不定詞句を構築（"to"含む）"""
        phrase_parts = ['to']  # "to" を必ず含める
        phrase_parts.append(infinitive_verb.text)
        
        # 不定詞動詞の目的語・修飾語を追加
        for word in sent.words:
            if word.head == infinitive_verb.id:
                if word.deprel in ['obj', 'iobj']:
                    phrase_parts.append(word.text)
                elif word.deprel in ['advmod', 'obl']:
                    phrase_parts.append(word.text)
        
        return ' '.join(phrase_parts).lower()
    
    def _build_noun_infinitive_phrase(self, sent, noun_word, infinitive_verb) -> str:
        """名詞+不定詞句を構築: nothing to do, work to finish"""
        phrase_parts = []
        
        # 修飾語を追加
        for word in sent.words:
            if word.head == noun_word.id and word.deprel in ['det', 'amod']:
                phrase_parts.append(word.text)
        
        # 名詞を追加
        phrase_parts.append(noun_word.text)
        
        # 不定詞句を追加
        phrase_parts.extend(['to', infinitive_verb.text])
        
        return ' '.join(phrase_parts).lower()
    
    def _is_adverbial_complement(self, sent, infinitive_verb, head_word) -> bool:
        """副詞的補語かどうか判定"""
        # 動詞 + to不定詞で目的を表す場合
        if head_word and head_word.upos == 'VERB':
            # came to help, went to see など
            verb_lemma = head_word.lemma.lower()
            motion_verbs = ['come', 'go', 'run', 'walk', 'drive', 'fly', 'move']
            return verb_lemma in motion_verbs
        return False
    
    def _find_object_before_infinitive(self, sent, main_verb, infinitive_verb):
        """不定詞前の目的語を探す: I want him to come"""
        for word in sent.words:
            if word.head == main_verb.id and word.deprel == 'obj':
                # この目的語が不定詞より前にあるかチェック
                if word.id < infinitive_verb.id:
                    return word
        return None
    
    def _find_main_verb(self, sent):
        """主動詞を探す"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _extract_main_clause_elements(self, sent, main_verb, exclude_words) -> Dict[str, str]:
        """主節の要素を抽出"""
        elements = {}
        exclude_ids = {w.id for w in exclude_words}
        
        # 動詞の処理
        if main_verb.upos == 'VERB':
            elements['V'] = main_verb.text
        elif main_verb.upos == 'AUX':
            elements['Aux'] = main_verb.text
        elif main_verb.upos == 'ADJ':
            # 形容詞が root の場合
            elements['C1'] = main_verb.text
            # be動詞を探す
            for word in sent.words:
                if word.head == main_verb.id and word.deprel == 'cop':
                    if word.upos == 'AUX':
                        elements['Aux'] = word.text
                    else:
                        elements['V'] = word.text
        
        # 依存要素の処理
        for word in sent.words:
            if word.id in exclude_ids:
                continue
                
            if word.head == main_verb.id:
                if word.deprel == 'nsubj':
                    elements['S'] = word.text
                elif word.deprel == 'obj' and 'O1' not in elements:
                    elements['O1'] = word.text
                elif word.deprel == 'iobj':
                    elements['O2'] = word.text
                elif word.deprel in ['advmod', 'obl']:
                    if 'M1' not in elements:
                        elements['M1'] = word.text
                    else:
                        elements['M2'] = word.text
        
        return elements
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理（不定詞構文なし）"""
        print("  📝 単純文処理")
        
        main_verb = self._find_main_verb(sent)
        if main_verb:
            return self._extract_main_clause_elements(sent, main_verb, [])
        
        return {"error": "動詞未検出"}

def test_infinitive_engine():
    """テスト実行"""
    engine = InfinitiveEngine()
    
    test_cases = [
        "To swim is fun",
        "He wants to go",
        "I want him to come",
        "He came to help",
        "I am happy to see you",
        "She has nothing to do",
        "I have work to finish",
        "They decided to leave"  # 追加テスト
    ]
    
    print("\n" + "="*50)
    print("🧪 不定詞構文エンジン テスト")
    print("="*50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n【Test {i}】 '{test}'")
        result = engine.process(test)
        
        print("📊 結果:")
        for key, value in result.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    test_infinitive_engine()
