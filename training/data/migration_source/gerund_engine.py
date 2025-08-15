#!/usr/bin/env python3
"""
Gerund Engine - 動名詞構文処理
Stanzaの構造を活用した動名詞構文の完全分解（上位スロット + サブスロット統合型）

核心原則:
1. Stanza依存関係による動名詞パターン検出 (csubj, xcomp, obl, advcl)
2. 動名詞句全体の上位スロット配置
3. 動名詞句内部のサブスロット分解
4. 主節要素との統合処理
"""

import stanza
from typing import Dict, List, Optional, Any

class GerundEngine:
    """動名詞構文エンジン（統合型）"""
    
    def __init__(self):
        print("🚀 動名詞構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 動名詞の依存関係パターンと機能分類
        self.gerund_patterns = {
            'csubj': 'subject',       # 主語動名詞: "Swimming is fun"
            'xcomp': 'object',        # 目的語動名詞: "I enjoy swimming"
            'obl': 'prepositional',   # 前置詞の目的語: "good at swimming"
            'advcl': 'adverbial'      # 副詞的動名詞: "interested in learning"
        }
        
        # 上位スロット配置マッピング
        self.slot_mapping = {
            'subject': 'S',
            'object': 'O1',
            'prepositional': 'M1',
            'adverbial': 'M2'
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """メイン処理 - 統合型完全分解"""
        print(f"🔍 動名詞構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 動名詞構文の構造解析
        gerund_info = self._analyze_gerund_structure(sent)
        
        if gerund_info:
            return self._process_complete_gerund_construction(sent, gerund_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_gerund_structure(self, sent) -> Optional[Dict]:
        """動名詞構文の構造分析"""
        # VBGタグを持つ動名詞を探す
        for word in sent.words:
            if word.xpos == 'VBG' and word.deprel in self.gerund_patterns:
                gerund_function = self.gerund_patterns[word.deprel]
                head_word = sent.words[word.head - 1] if word.head > 0 else None
                
                structure_info = {
                    'gerund_verb': word,
                    'function': gerund_function,
                    'head_word': head_word,
                    'phrase_words': self._extract_gerund_phrase(sent, word)
                }
                
                print(f"  📋 動名詞構文検出:")
                print(f"    動名詞動詞: {word.text} ({word.deprel})")
                print(f"    機能: {gerund_function}")
                print(f"    依存先: {head_word.text if head_word else '?'}")
                return structure_info
        
        # NOUN化された動名詞もチェック
        for word in sent.words:
            if (word.upos == 'NOUN' and 
                word.deprel in ['nsubj', 'obj'] and
                self._is_derived_from_verb(word.text)):
                
                gerund_function = 'subject' if word.deprel == 'nsubj' else 'object'
                head_word = sent.words[word.head - 1] if word.head > 0 else None
                
                structure_info = {
                    'gerund_verb': word,
                    'function': gerund_function,
                    'head_word': head_word,
                    'phrase_words': self._extract_gerund_phrase(sent, word)
                }
                
                print(f"  📋 NOUN化動名詞検出:")
                print(f"    動名詞: {word.text} ({word.deprel})")
                print(f"    機能: {gerund_function}")
                return structure_info
        
        return None
    
    def _extract_gerund_phrase(self, sent, gerund_verb) -> List:
        """動名詞句の範囲を抽出"""
        phrase_words = [gerund_verb]
        
        # 動名詞に依存する語を再帰的に収集
        def collect_dependents(head_id, exclude_case=True):
            dependents = []
            for word in sent.words:
                if word.head == head_id:
                    # 前置詞のcaseは除外（上位レベルで処理）
                    if exclude_case and word.deprel == 'case':
                        continue
                    dependents.append(word)
                    # 再帰的に孫も収集
                    dependents.extend(collect_dependents(word.id, exclude_case))
            return dependents
        
        dependents = collect_dependents(gerund_verb.id)
        phrase_words.extend(dependents)
        
        # 語順でソート
        phrase_words.sort(key=lambda w: w.id)
        return phrase_words
    
    def _process_complete_gerund_construction(self, sent, gerund_info) -> Dict[str, str]:
        """動名詞構文の完全処理 - 統合型"""
        gerund_verb = gerund_info['gerund_verb']
        gerund_function = gerund_info['function']
        head_word = gerund_info['head_word']
        phrase_words = gerund_info['phrase_words']
        
        result = {}
        
        print(f"  🎯 統合処理開始: {gerund_function}動名詞")
        
        # 1. 動名詞句全体を上位スロットに配置
        gerund_phrase = self._build_complete_gerund_phrase(sent, gerund_info)
        upper_slot = self._determine_upper_slot_position(gerund_info, sent)
        
        if upper_slot:
            result[upper_slot] = gerund_phrase
            print(f"    上位配置: {upper_slot} = '{gerund_phrase}'")
        
        # 2. 動名詞句をサブスロットに分解
        sub_elements = self._decompose_gerund_to_subslots(sent, gerund_info)
        result.update(sub_elements)
        
        # 3. 主節の他の要素を処理
        main_elements = self._extract_main_clause_elements(sent, head_word, phrase_words)
        result.update(main_elements)
        
        print(f"  ✅ 統合型完全分解: {result}")
        return result
    
    def _build_complete_gerund_phrase(self, sent, gerund_info) -> str:
        """動名詞句全体を構築"""
        phrase_parts = []
        phrase_words = gerund_info['phrase_words']
        gerund_function = gerund_info['function']
        
        # 前置詞付きの場合は前置詞から開始
        if gerund_function in ['prepositional', 'adverbial']:
            # 前置詞を探す
            prep_word = self._find_preposition(sent, gerund_info['gerund_verb'])
            if prep_word:
                phrase_parts.append(prep_word.text)
        
        # 動名詞句の語を順序通りに追加
        for word in phrase_words:
            phrase_parts.append(word.text)
        
        return ' '.join(phrase_parts).lower()
    
    def _determine_upper_slot_position(self, gerund_info, sent) -> str:
        """上位スロット位置の決定"""
        gerund_function = gerund_info['function']
        
        if gerund_function == 'subject':
            return 'S'
        elif gerund_function == 'object':
            return 'O1'
        elif gerund_function == 'prepositional':
            return 'M1'
        elif gerund_function == 'adverbial':
            return 'M2'
        
        return None
    
    def _decompose_gerund_to_subslots(self, sent, gerund_info) -> Dict[str, str]:
        """動名詞句のサブスロット分解"""
        sub_elements = {}
        gerund_verb = gerund_info['gerund_verb']
        phrase_words = gerund_info['phrase_words']
        phrase_ids = {w.id for w in phrase_words}
        
        # 1. 動名詞動詞本体
        sub_elements['sub-v'] = gerund_verb.text.lower()
        
        # 2. 前置詞の処理
        if gerund_info['function'] in ['prepositional', 'adverbial']:
            prep_word = self._find_preposition(sent, gerund_verb)
            if prep_word:
                sub_elements['sub-m1'] = prep_word.text.lower()
        
        # 3. 動名詞の目的語・修飾語を処理
        for word in sent.words:
            if word.id in phrase_ids and word.id != gerund_verb.id:
                if word.head == gerund_verb.id:
                    if word.deprel == 'obj':
                        sub_elements['sub-o1'] = word.text.lower()
                    elif word.deprel == 'iobj':
                        sub_elements['sub-o2'] = word.text.lower()
                    elif word.deprel == 'advmod':
                        if 'sub-m1' not in sub_elements:
                            sub_elements['sub-m1'] = word.text.lower()
                        elif 'sub-m2' not in sub_elements:
                            sub_elements['sub-m2'] = word.text.lower()
                        else:
                            sub_elements['sub-m3'] = word.text.lower()
                    elif word.deprel in ['obl', 'nmod']:
                        # 前置詞句の処理
                        prep_phrase = self._build_prepositional_phrase(sent, word)
                        if 'sub-m2' not in sub_elements:
                            sub_elements['sub-m2'] = prep_phrase
                        else:
                            sub_elements['sub-m3'] = prep_phrase
        
        return sub_elements
    
    def _find_preposition(self, sent, gerund_verb) -> Optional[Any]:
        """動名詞に関連する前置詞を探す"""
        for word in sent.words:
            if (word.deprel == 'case' and 
                any(w.head == gerund_verb.id for w in sent.words if w.id == word.head)):
                return word
        return None
    
    def _build_prepositional_phrase(self, sent, prep_obj) -> str:
        """前置詞句を構築"""
        phrase_parts = []
        
        # 前置詞を探す
        for word in sent.words:
            if word.head == prep_obj.id and word.deprel == 'case':
                phrase_parts.append(word.text)
                break
        
        # 前置詞の目的語
        phrase_parts.append(prep_obj.text)
        
        return ' '.join(phrase_parts).lower()
    
    def _extract_main_clause_elements(self, sent, head_word, exclude_words) -> Dict[str, str]:
        """主節の要素を抽出"""
        elements = {}
        exclude_ids = {w.id for w in exclude_words}
        
        # 主動詞を探す
        main_verb = head_word if head_word and head_word.upos in ['VERB', 'AUX'] else self._find_main_verb(sent)
        if not main_verb:
            return elements
        
        # 動詞の処理
        if main_verb.upos == 'VERB':
            elements['V'] = main_verb.text
        elif main_verb.upos == 'AUX':
            elements['Aux'] = main_verb.text
        elif main_verb.upos == 'ADJ':
            elements['C1'] = main_verb.text
            # be動詞を探す
            for word in sent.words:
                if word.head == main_verb.id and word.deprel == 'cop':
                    elements['Aux'] = word.text
        
        # 依存要素の処理
        for word in sent.words:
            if word.id in exclude_ids:
                continue
                
            if word.head == main_verb.id:
                if word.deprel == 'nsubj' and 'S' not in elements:
                    elements['S'] = word.text
                elif word.deprel == 'obj' and 'O1' not in elements:
                    elements['O1'] = word.text
                elif word.deprel == 'iobj':
                    elements['O2'] = word.text
                elif word.deprel in ['acomp', 'xcomp'] and 'C1' not in elements:
                    elements['C1'] = word.text
                elif word.deprel in ['advmod', 'obl']:
                    if 'M1' not in elements:
                        elements['M1'] = word.text
                    elif 'M2' not in elements:
                        elements['M2'] = word.text
                    else:
                        elements['M3'] = word.text
        
        return elements
    
    def _find_main_verb(self, sent):
        """主動詞を探す"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _is_derived_from_verb(self, word_text: str) -> bool:
        """動詞由来の名詞かどうか判定"""
        # 動名詞の典型的な語尾や語形
        gerund_indicators = ['ing', 'tion', 'sion', 'ment', 'ance', 'ence']
        # よく知られた動名詞
        common_gerunds = {'swimming', 'running', 'reading', 'writing', 'smoking', 'dancing'}
        
        word_lower = word_text.lower()
        return (any(word_lower.endswith(suffix) for suffix in gerund_indicators) or
                word_lower in common_gerunds)
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理（動名詞構文なし）"""
        print("  📝 単純文処理")
        
        main_verb = self._find_main_verb(sent)
        if main_verb:
            return self._extract_main_clause_elements(sent, main_verb, [])
        
        return {"error": "動詞未検出"}

def test_gerund_engine():
    """テスト実行"""
    engine = GerundEngine()
    
    test_cases = [
        "Swimming is fun",
        "I enjoy swimming", 
        "I enjoy playing tennis",
        "He is good at swimming fast",
        "They started working hard",
        "Running every day keeps me healthy",
        "I am interested in learning English",
        "She likes reading books"
    ]
    
    print("\n" + "="*60)
    print("🧪 動名詞構文エンジン テスト（統合型）")
    print("="*60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n【Test {i}】 '{test}'")
        result = engine.process(test)
        
        print("📊 完全分解結果:")
        # 上位スロットを先に表示
        upper_slots = {k: v for k, v in result.items() if not k.startswith('sub-') and k != 'error'}
        sub_slots = {k: v for k, v in result.items() if k.startswith('sub-')}
        
        if upper_slots:
            print("  【上位スロット】")
            for key, value in sorted(upper_slots.items()):
                print(f"    {key}: {value}")
        
        if sub_slots:
            print("  【サブスロット】")
            for key, value in sorted(sub_slots.items()):
                print(f"    {key}: {value}")
        
        if 'error' in result:
            print(f"  ❌ エラー: {result['error']}")

if __name__ == "__main__":
    test_gerund_engine()
