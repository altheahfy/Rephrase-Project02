#!/usr/bin/env python3
"""
Stanza準拠従属接続詞エンジン（統合型）
ハードコーディングを最小化し、Stanzaの構造解析に依存

統合型アーキテクチャー:
1. 上位スロット配置 + サブスロット分解を単一エンジンで処理
2. 従属節：M1,M2,M3位置（意味分類別） + sub-v（従属節動詞のみ）
3. Rephraseルール準拠：大文字上位スロット + 小文字サブスロット
4. 情報保持とデバッグ効率の両立
"""

import stanza
from typing import Dict, List, Optional, Any

class StanzaBasedConjunctionEngine:
    """Stanza構造解析準拠の接続詞エンジン（統合型）"""
    
    def __init__(self):
        print("🚀 Stanza準拠接続詞エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 最小限の意味分類（語彙的知識として必要）+ 上位スロット配置
        self.semantic_mapping = {
            # 理由 -> M1位置
            'because': 'M1', 'since': 'M1', 'as': 'M1',
            # 条件 -> M1位置  
            'if': 'M1', 'unless': 'M1', 'provided': 'M1',
            # 譲歩 -> M2位置
            'although': 'M2', 'though': 'M2', 'whereas': 'M2',
            # 時間 -> M3位置
            'when': 'M3', 'while': 'M3', 'after': 'M3', 'before': 'M3', 'until': 'M3'
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """統合型メイン処理"""
        print(f"🔍 従属接続詞構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 従属節検出
        subordinate_info = self._analyze_subordinate_structure(sent)
        if subordinate_info:
            return self._process_complete_subordinate_construction(sent, subordinate_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_subordinate_structure(self, sent) -> Optional[Dict]:
        """従属節構造の統合分析"""
        # mark関係の接続詞を探す
        for word in sent.words:
            if word.deprel == 'mark' and word.text.lower() in self.semantic_mapping:
                # 接続詞が修飾する従属節動詞を探す
                subordinate_verb = sent.words[word.head - 1] if word.head > 0 else None
                
                # 主節動詞を探す
                main_verb = None
                if subordinate_verb and subordinate_verb.deprel == 'advcl':
                    main_verb = sent.words[subordinate_verb.head - 1] if subordinate_verb.head > 0 else None
                
                structure_info = {
                    'conjunction': word,
                    'subordinate_verb': subordinate_verb,
                    'main_verb': main_verb,
                    'conjunction_type': word.text.lower(),
                    'semantic_slot': self.semantic_mapping[word.text.lower()]
                }
                
                print(f"  📋 従属節検出:")
                print(f"    接続詞: {word.text} ({word.deprel})")
                print(f"    従属動詞: {subordinate_verb.text if subordinate_verb else '?'}")
                print(f"    主動詞: {main_verb.text if main_verb else '?'}")
                print(f"    意味分類: {structure_info['semantic_slot']}")
                return structure_info
        
        return None
    
    def _process_complete_subordinate_construction(self, sent, subordinate_info) -> Dict[str, str]:
        """従属接続詞構文の完全処理 - 統合型"""
        result = {}
        conjunction = subordinate_info['conjunction']
        subordinate_verb = subordinate_info['subordinate_verb']
        main_verb = subordinate_info['main_verb']
        semantic_slot = subordinate_info['semantic_slot']
        
        print(f"  🎯 統合処理開始: {semantic_slot}位置従属節")
        
        # 主節の処理
        if main_verb:
            main_elements = self._extract_main_clause_elements(sent, main_verb, [subordinate_verb, conjunction])
            result.update(main_elements)
        
        # 上位スロット配置 + サブスロット分解
        # 従属節全体を意味分類に応じた位置に配置
        subordinate_clause = self._build_subordinate_clause(sent, conjunction, subordinate_verb)
        result[semantic_slot] = subordinate_clause
        
        # 従属節動詞をサブスロットに
        subordinate_verb_phrase = self._build_subordinate_verb_phrase(sent, subordinate_verb)
        result['sub-v'] = subordinate_verb_phrase
        
        print(f"    上位配置: {semantic_slot} = '{subordinate_clause}'")
        print(f"    サブスロット配置: sub-v = '{subordinate_verb_phrase}'")
        print(f"  ✅ 統合型完全分解: {result}")
        return result
    
    def _build_subordinate_clause(self, sent, conjunction, subordinate_verb):
        """従属節全体の構築"""
        if not subordinate_verb:
            return conjunction.text
        
        # 接続詞から従属節終了まで
        start_idx = conjunction.id - 1
        
        # 従属節の範囲を特定
        sub_words = self._get_subordinate_clause_words(sent, subordinate_verb)
        if sub_words:
            end_idx = max(w.id - 1 for w in sub_words)
            # 接続詞も含める
            if conjunction not in sub_words:
                sub_words.append(conjunction)
            clause_words = sorted(sub_words, key=lambda x: x.id)
            return ' '.join(w.text for w in clause_words)
        
        return f"{conjunction.text} {subordinate_verb.text}"
    
    def _build_subordinate_verb_phrase(self, sent, subordinate_verb):
        """従属節動詞部分の構築"""
        if not subordinate_verb:
            return ""
        
        # 従属動詞とその直接的な修飾語
        verb_words = self._get_subordinate_clause_words(sent, subordinate_verb)
        if verb_words:
            return ' '.join(w.text for w in sorted(verb_words, key=lambda x: x.id))
        
        return subordinate_verb.text
    
    def _get_subordinate_clause_words(self, sent, subordinate_verb):
        """従属節に属する単語を収集"""
        if not subordinate_verb:
            return []
        
        sub_words = [subordinate_verb]
        
        # 従属動詞の子要素を再帰的に収集
        for word in sent.words:
            if word.head == subordinate_verb.id:
                sub_words.append(word)
                sub_words.extend(self._get_children(sent, word))
        
        return sub_words
    
    def _get_children(self, sent, parent):
        """指定語の子要素を再帰的に収集"""
        children = []
        for word in sent.words:
            if word.head == parent.id:
                children.append(word)
                children.extend(self._get_children(sent, word))
        return children
    
    def _extract_main_clause_elements(self, sent, main_verb, exclude_words=None):
        """主節要素の抽出"""
        result = {}
        exclude_ids = set()
        if exclude_words:
            exclude_ids = {w.id for w in exclude_words if w}
        
        result['V'] = main_verb.text
        
        # 主語
        for word in sent.words:
            if word.head == main_verb.id and word.deprel == 'nsubj' and word.id not in exclude_ids:
                result['S'] = word.text
                break
        
        # 目的語（従属節以外）
        for word in sent.words:
            if word.head == main_verb.id and word.deprel == 'obj' and word.id not in exclude_ids:
                result['O1'] = word.text
                break
        
        # 補語
        for word in sent.words:
            if word.head == main_verb.id and word.deprel in ['xcomp', 'ccomp'] and word.id not in exclude_ids:
                result['C1'] = word.text
                break
        
        return result
    
    def _process_simple_sentence(self, sent):
        """単純文の処理"""
        print("  📝 単純文処理")
        result = {}
        
        # ルート動詞を探す
        main_verb = None
        for word in sent.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                main_verb = word
                break
        
        if main_verb:
            result.update(self._extract_main_clause_elements(sent, main_verb))
        
        return result
