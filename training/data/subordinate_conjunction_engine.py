#!/usr/bin/env python3
"""
Subordinate Conjunction Engine - 従属接続詞処理
Stanzaの構造を活用した従属節の分解

核心原則:
1. 従属節の位置判定（M1/M2/M3）
2. 接続詞の意味分類
3. サブスロットへの単語分解
4. 主節との分離処理
"""

import stanza
from typing import Dict, List, Optional, Any

class SubordinateConjunctionEngine:
    """従属接続詞エンジン"""
    
    def __init__(self):
        print("🚀 従属接続詞エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 接続詞の分類
        self.conjunction_types = {
            # M1位置 - 理由・条件
            'M1': ['because', 'since', 'if', 'unless', 'provided', 'given'],
            # M2位置 - 方法・譲歩  
            'M2': ['as', 'while', 'though', 'although', 'whereas', 'even though'],
            # M3位置 - 時間・場所
            'M3': ['when', 'where', 'after', 'before', 'until', 'once']
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """メイン処理"""
        print(f"🔍 処理開始: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 従属節検出
        if self._has_subordinate_clause(sent):
            return self._process_subordinate_clause(sent)
        else:
            return self._process_simple_sentence(sent)
    
    def _has_subordinate_clause(self, sent) -> bool:
        """従属節を含むかチェック"""
        # 1. advcl等の従属関係をチェック
        subordinate_markers = ['advcl', 'csubj', 'ccomp']
        if any(w.deprel in subordinate_markers for w in sent.words):
            return True
        
        # 2. 文頭の接続詞をチェック（単独従属節の場合）
        if sent.words and sent.words[0].text.lower() in self._get_all_conjunctions():
            return True
            
        # 3. mark関係をチェック
        return any(w.deprel == 'mark' for w in sent.words)
    
    def _get_all_conjunctions(self):
        """全ての接続詞リストを取得"""
        all_conjunctions = []
        for conjunctions in self.conjunction_types.values():
            all_conjunctions.extend(conjunctions)
        return all_conjunctions
    
    def _process_subordinate_clause(self, sent) -> Dict[str, str]:
        """従属節の処理"""
        print("📖 従属節処理")
        
        # === 1. 従属節と主節の分離 ===
        subordinate_verb = self._find_subordinate_verb(sent)
        main_verb = self._find_main_verb(sent)
        
        # 単独従属節の場合
        if not subordinate_verb and sent.words and sent.words[0].text.lower() in self._get_all_conjunctions():
            return self._process_single_subordinate_clause(sent)
        
        if not subordinate_verb:
            return {"error": "従属動詞未検出"}
        
        if not main_verb:
            return {"error": "主動詞未検出"}
        
        # === 2. 接続詞検出 ===
        conjunction = self._find_conjunction(sent, subordinate_verb)
        conjunction_type = self._classify_conjunction(conjunction.text.lower() if conjunction else "")
        
        print(f"  従属動詞: {subordinate_verb.text}")
        print(f"  主動詞: {main_verb.text}")
        print(f"  接続詞: {conjunction.text if conjunction else '?'} ({conjunction_type})")
        
        # === 3. 従属節の要素抽出 ===
        sub_elements = self._extract_subordinate_elements(sent, subordinate_verb, conjunction)
        
        # === 4. 主節の要素抽出 ===
        main_elements = self._extract_main_elements(sent, main_verb)
        
        # === 5. Rephrase分解 ===
        result = {}
        
        # 従属節をサブスロットに配置
        if conjunction:
            result["sub-m1"] = conjunction.text.lower()
        if sub_elements.get('subject'):
            result["sub-s"] = sub_elements['subject'].text
        if sub_elements.get('aux'):
            result["sub-aux"] = sub_elements['aux'].text
        if sub_elements.get('verb'):
            result["sub-v"] = sub_elements['verb'].text
        if sub_elements.get('complement'):
            result["sub-c1"] = sub_elements['complement'].text
        
        # 主節を通常スロットに配置
        if main_elements.get('subject'):
            result["S"] = main_elements['subject'].text
        if main_elements.get('aux'):
            result["AUX"] = main_elements['aux'].text
        if main_elements.get('verb'):
            result["V"] = main_elements['verb'].text
        if main_elements.get('object'):
            result["O1"] = main_elements['object'].text
        if main_elements.get('modifier'):
            result["M3"] = main_elements['modifier'].text
        
        return result
    
    def _process_single_subordinate_clause(self, sent) -> Dict[str, str]:
        """単独従属節の処理"""
        print("📖 単独従属節処理")
        
        result = {}
        
        # 接続詞（文頭）
        conjunction = sent.words[0]
        result["sub-m1"] = conjunction.text.lower()
        print(f"  接続詞: {conjunction.text}")
        
        # 主語、動詞、その他要素を抽出
        root_verb = None
        for word in sent.words:
            if word.head == 0:  # root
                root_verb = word
                break
        
        if not root_verb:
            return result
            
        print(f"  動詞: {root_verb.text}")
        
        # 各要素を抽出
        for word in sent.words:
            if word.head == root_verb.id:
                if word.deprel == 'nsubj':
                    result["sub-s"] = word.text
                    print(f"  主語: {word.text}")
                elif word.deprel == 'cop':
                    result["sub-aux"] = word.text
                    print(f"  助動詞: {word.text}")
                elif word.deprel == 'obj':
                    result["sub-o1"] = word.text
                    print(f"  目的語: {word.text}")
        
        # 動詞の処理
        if root_verb.pos == 'ADJ':
            # be動詞+形容詞の場合、形容詞を補語として扱う
            result["sub-c1"] = root_verb.text
            print(f"  補語: {root_verb.text}")
        else:
            result["sub-v"] = root_verb.text
            print(f"  動詞: {root_verb.text}")
        
        return result
    
    def _find_subordinate_verb(self, sent):
        """従属動詞を検索"""
        for word in sent.words:
            if word.deprel in ['advcl', 'csubj', 'ccomp']:
                return word
        return None
    
    def _find_main_verb(self, sent):
        """主動詞を検索"""
        return next((w for w in sent.words if w.head == 0), None)
    
    def _find_conjunction(self, sent, subordinate_verb):
        """接続詞を検索"""
        # 1. 従属動詞を修飾するmarkを探す
        for word in sent.words:
            if word.head == subordinate_verb.id and word.deprel == 'mark':
                return word
        
        # 2. 文頭の接続詞を探す
        for word in sent.words:
            if word.text.lower() in self._get_all_conjunctions():
                return word
                
        return None
    
    def _classify_conjunction(self, conjunction_text: str) -> str:
        """接続詞を分類"""
        for pos_type, conjunctions in self.conjunction_types.items():
            if conjunction_text in conjunctions:
                return pos_type
        return "M1"  # デフォルト
    
    def _extract_subordinate_elements(self, sent, subordinate_verb, conjunction):
        """従属節の要素抽出"""
        elements = {}
        
        for word in sent.words:
            if word.head == subordinate_verb.id:
                if word.deprel == 'nsubj':
                    elements['subject'] = word
                elif word.deprel == 'cop':
                    elements['aux'] = word
                elif word.deprel == 'obj':
                    elements['object'] = word
                elif word.pos == 'ADJ' and subordinate_verb.pos == 'ADJ':
                    elements['complement'] = subordinate_verb
                    elements['verb'] = subordinate_verb
        
        # be動詞+形容詞の場合
        if subordinate_verb.pos == 'ADJ':
            elements['verb'] = elements.get('aux', subordinate_verb)
            elements['complement'] = subordinate_verb
        else:
            elements['verb'] = subordinate_verb
            
        return elements
    
    def _extract_main_elements(self, sent, main_verb):
        """主節の要素抽出"""
        elements = {}
        
        for word in sent.words:
            if word.head == main_verb.id:
                if word.deprel == 'nsubj':
                    elements['subject'] = word
                elif word.deprel == 'cop':
                    elements['aux'] = word
                elif word.deprel == 'obj':
                    elements['object'] = word
                elif word.deprel in ['advmod', 'obl']:
                    elements['modifier'] = word
        
        elements['verb'] = main_verb
        return elements
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理"""
        print("📝 単純文処理")
        
        result = {}
        
        # 基本要素抽出
        for word in sent.words:
            if word.deprel == 'nsubj':
                result["S"] = word.text
            elif word.deprel == 'obj':
                result["O1"] = word.text
            elif word.deprel == 'root':
                result["V"] = word.text
        
        return result

# === テスト実行 ===
if __name__ == "__main__":
    print("="*60)
    print("🚀 従属接続詞エンジン - 汎用性テスト")
    print("="*60)
    
    engine = SubordinateConjunctionEngine()
    
    # 複数の従属接続詞パターンをテスト
    test_cases = [
        # 単純な従属節
        ("Because he is tired", "理由接続詞"),
        ("If it rains", "条件接続詞"),
        ("When she arrives", "時間接続詞"),
        ("While we wait", "方法接続詞"),
        ("Although he was tired", "譲歩接続詞"),
        
        # 複文パターン
        ("If it rains, we stay home", "条件節+主節"),
        ("Because he is tired, he went to bed", "理由節+主節"),
        ("When she arrives, we will start", "時間節+主節"),
    ]
    
    for i, (test_text, pattern_type) in enumerate(test_cases, 1):
        print(f"\n📖 テスト{i}: '{test_text}' ({pattern_type})")
        print("-" * 60)
        
        result = engine.process(test_text)
        
        print("📊 結果:")
        for key, value in result.items():
            print(f"  {key}: '{value}'")
    
    print("\n" + "="*60)
    print("🎯 従属接続詞パターン検証完了！")
    print("="*60)
