#!/usr/bin/env python3
"""
Simple Relative Clause Engine - シンプル関係節処理（統合型）
Stanzaの構造をそのまま活用した直接的なRephrase分解

統合型アーキテクチャー:
1. 上位スロット配置 + サブスロット分解を単一エンジンで処理
2. 関係節：O1位置（先行詞+関係節全体） + sub-v（関係節動詞のみ）
3. Rephraseルール準拠：大文字上位スロット + 小文字サブスロット
4. 情報保持とデバッグ効率の両立
"""

import stanza
from typing import Dict, List, Optional, Any

class SimpleRelativeEngine:
    """シンプル関係節エンジン（統合型）"""
    
    def __init__(self):
        print("🚀 シンプル関係節エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 上位スロット配置マッピング
        self.slot_mapping = {
            'restrictive': 'O1',    # 限定用法: O1位置（先行詞+関係節全体）
            'non_restrictive': 'M1' # 非限定用法: M1位置（補足情報として）
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """統合型メイン処理"""
        print(f"🔍 関係節構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 関係節検出
        relative_info = self._analyze_relative_structure(sent)
        if relative_info:
            return self._process_complete_relative_construction(sent, relative_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_relative_structure(self, sent) -> Optional[Dict]:
        """関係節構造の統合分析"""
        # 関係節動詞を探す（acl:relcl, acl関係）
        for word in sent.words:
            if word.deprel in ['acl:relcl', 'acl']:
                antecedent = sent.words[word.head - 1] if word.head > 0 else None
                
                # 関係代名詞/副詞を探す
                rel_pronoun = self._find_relative_pronoun(sent, word)
                
                structure_info = {
                    'relative_verb': word,
                    'antecedent': antecedent,
                    'rel_pronoun': rel_pronoun,
                    'clause_type': 'restrictive'  # デフォルトは限定用法
                }
                
                print(f"  📋 関係節検出:")
                print(f"    関係動詞: {word.text} ({word.deprel})")
                print(f"    先行詞: {antecedent.text if antecedent else '?'}")
                print(f"    関係語: {rel_pronoun.text if rel_pronoun else '?'}")
                return structure_info
        
        return None
    
    def _process_complete_relative_construction(self, sent, relative_info) -> Dict[str, str]:
        """関係節構文の完全処理 - 統合型"""
        result = {}
        relative_verb = relative_info['relative_verb']
        antecedent = relative_info['antecedent']
        clause_type = relative_info['clause_type']
        
        print(f"  🎯 統合処理開始: {clause_type}関係節")
        
        # 主節の処理
        main_verb = self._find_main_verb(sent, [relative_verb])
        if main_verb:
            main_elements = self._extract_main_clause_elements(sent, main_verb, [relative_verb, antecedent])
            result.update(main_elements)
        
        # 上位スロット配置 + サブスロット分解
        upper_slot = self.slot_mapping[clause_type]
        
        # 先行詞+関係節全体を上位スロットに
        antecedent_phrase = self._build_antecedent_relative_phrase(sent, antecedent, relative_verb)
        result[upper_slot] = antecedent_phrase
        
        # 関係節動詞をサブスロットに
        relative_clause = self._build_relative_clause(sent, relative_verb)
        result['sub-v'] = relative_clause
        
        print(f"    上位配置: {upper_slot} = '{antecedent_phrase}'")
        print(f"    サブスロット配置: sub-v = '{relative_clause}'")
        print(f"  ✅ 統合型完全分解: {result}")
        return result
    
    def _find_relative_pronoun(self, sent, relative_verb):
        """関係代名詞/関係副詞を探す"""
        for word in sent.words:
            if (word.upos == 'PRON' and word.text.lower() in ['who', 'whom', 'whose', 'which', 'that'] or
                word.upos == 'ADV' and word.text.lower() in ['where', 'when', 'why', 'how']):
                if self._is_related_to_verb(sent, word, relative_verb):
                    return word
        return None
    
    def _is_related_to_verb(self, sent, pronoun, verb):
        """代名詞が動詞と関係があるかチェック"""
        # 簡易的な関係チェック：同一節内または直接的依存関係
        return abs(pronoun.id - verb.id) <= 5  # 位置的近さで判定
    
    def _build_antecedent_relative_phrase(self, sent, antecedent, relative_verb):
        """先行詞+関係節全体の構築"""
        if not antecedent:
            return self._build_relative_clause(sent, relative_verb)
        
        # 先行詞から関係節終了まで
        start_idx = antecedent.id - 1
        
        # 関係節の範囲を特定
        rel_words = self._get_relative_clause_words(sent, relative_verb)
        end_idx = max(w.id - 1 for w in rel_words) if rel_words else relative_verb.id - 1
        
        phrase_words = sent.words[start_idx:end_idx + 1]
        return ' '.join(w.text for w in phrase_words)
    
    def _build_relative_clause(self, sent, relative_verb):
        """関係節部分のみの構築"""
        rel_words = self._get_relative_clause_words(sent, relative_verb)
        if rel_words:
            return ' '.join(w.text for w in sorted(rel_words, key=lambda x: x.id))
        return relative_verb.text
    
    def _get_relative_clause_words(self, sent, relative_verb):
        """関係節に属する単語を収集"""
        rel_words = [relative_verb]
        
        # 関係節動詞の直接的な子要素を収集
        for word in sent.words:
            if word.head == relative_verb.id:
                rel_words.append(word)
                # さらにその子要素も収集
                rel_words.extend(self._get_children(sent, word))
        
        return rel_words
    
    def _get_children(self, sent, parent):
        """指定語の子要素を再帰的に収集"""
        children = []
        for word in sent.words:
            if word.head == parent.id:
                children.append(word)
                children.extend(self._get_children(sent, word))
        return children
    
    def _find_main_verb(self, sent, exclude_words=None):
        """主節動詞の特定"""
        exclude_ids = set()
        if exclude_words:
            exclude_ids = {w.id for w in exclude_words if w}
        
        for word in sent.words:
            if (word.upos == 'VERB' and 
                word.deprel == 'root' and 
                word.id not in exclude_ids):
                return word
        return None
    
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
        
        # 目的語（関係節以外）
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
