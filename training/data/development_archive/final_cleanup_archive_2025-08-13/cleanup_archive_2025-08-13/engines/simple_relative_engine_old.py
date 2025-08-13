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
    
    def _process_relative_clause(self, sent) -> Dict[str, str]:
        """統合型処理への橋渡し（互換性維持）"""
        relative_info = self._analyze_relative_structure(sent)
        if relative_info:
            return self._process_complete_relative_construction(sent, relative_info)
        return {"error": "関係節検出失敗"}
    
    def _find_main_verb(self, sent, exclude_words=None):
                    possessive_rel_pronoun = word
                    # whoseが修飾している名詞を取得
                    possessed_noun = self._find_by_id(sent, word.head)
                    rel_pronoun = possessive_rel_pronoun
                    print(f"  🔍 所有格検出: {possessive_rel_pronoun.text} → {possessed_noun.text}")
                    break
        
        # 関係節内主語（目的語関係代名詞、関係副詞、前置詞+関係代名詞の場合）
        rel_subject = None
        if rel_pronoun and (rel_pronoun.deprel == 'obj' or rel_pronoun.deprel == 'advmod' or 
                           rel_pronoun.deprel in ['nmod', 'obl']):
            rel_subject = self._find_by_head_and_deprel(sent, rel_verb.id, 'nsubj')  # "he"
        
        print(f"  先行詞: {antecedent.text if antecedent else '?'}")
        print(f"  関係代名詞: {rel_pronoun.text if rel_pronoun else '?'}")
        print(f"  所有される名詞: {possessed_noun.text if possessed_noun else '?'}")
        print(f"  関係節主語: {rel_subject.text if rel_subject else '?'}")
        print(f"  関係動詞: {rel_verb.text}")
        
        # === 2. 先行詞句構築 ===
        noun_phrase = self._build_noun_phrase(sent, antecedent, rel_pronoun, possessed_noun, preposition)
        print(f"  構築句: '{noun_phrase}'")
        
        # === 3. Rephrase分解 ===
        result = {}
        
        # 関係代名詞の役割に応じて配置
        if preposition and rel_pronoun:
            # 前置詞+関係代名詞: "The book of which he spoke"
            if preposition.text.lower() in ['in', 'at', 'on']:  # 場所
                result["sub-m3"] = noun_phrase  # "The house in which"
            else:  # その他（of, to, for, about など）
                result["sub-m2"] = noun_phrase  # "The book of which"
            
            if rel_subject:
                result["sub-s"] = rel_subject.text  # "he"
            
            # 目的語があれば追加
            obj_word = self._find_by_head_and_deprel(sent, rel_verb.id, 'obj')
            if obj_word:
                result["sub-o2"] = obj_word.text  # "it"
                
        elif rel_pronoun and rel_pronoun.deprel == 'obj':
            # 目的語関係代名詞: "The book that he bought"
            result["O1"] = ""
            result["sub-o1"] = noun_phrase
            if rel_subject:
                result["sub-s"] = rel_subject.text
        elif rel_pronoun and rel_pronoun.deprel == 'nsubj':
            # 主語関係代名詞: "The man who runs"
            result["S"] = ""
            result["sub-s"] = noun_phrase
        elif rel_pronoun and rel_pronoun.deprel == 'nmod:poss':
            # 所有格関係代名詞: "The man whose car is red"
            result["S"] = ""
            result["sub-s"] = noun_phrase  # "The man whose car"
            
            # be動詞とその他の要素を処理
            cop_verb = self._find_by_head_and_deprel(sent, rel_verb.id, 'cop')  # "is"
            if cop_verb:
                if rel_verb.pos == 'ADJ':
                    # "is red" の場合
                    result["sub-aux"] = cop_verb.text  # "is" 
                    result["sub-c1"] = rel_verb.text   # "red"
                elif rel_verb.pos == 'VERB':
                    # "is torn" の場合  
                    result["sub-aux"] = cop_verb.text  # "is"
                    result["sub-v"] = rel_verb.text    # "torn"
            else:
                # be動詞がない場合
                result["sub-v"] = rel_verb.text
        elif rel_pronoun and rel_pronoun.deprel == 'advmod' and rel_pronoun.text.lower() in ['where', 'when', 'why', 'how']:
            # 関係副詞: "The place where he lives", "The reason why he is angry"
            if rel_pronoun.text.lower() in ['where', 'when']:
                result["sub-m3"] = noun_phrase  # 場所・時間: "The place where"
            elif rel_pronoun.text.lower() in ['why', 'how']:
                result["sub-m1"] = noun_phrase  # 理由・方法: "The reason why"
            
            if rel_subject:
                result["sub-s"] = rel_subject.text  # "he"
            
            # be動詞+形容詞の場合の処理
            cop_verb = self._find_by_head_and_deprel(sent, rel_verb.id, 'cop')
            if cop_verb and rel_verb.pos == 'ADJ':
                # "is angry" の場合
                result["sub-v"] = cop_verb.text    # "is"
                result["sub-c1"] = rel_verb.text   # "angry"
            else:
                result["sub-v"] = rel_verb.text  # "work"
        else:
            # デフォルト処理 - 省略された関係副詞の可能性もチェック
            if antecedent and antecedent.text.lower() in ['way', 'manner']:
                # "The way we work" (省略されたhow)
                result["sub-m1"] = noun_phrase + " (how)"
                # 省略されたhowの場合も主語を取得
                way_subject = self._find_by_head_and_deprel(sent, rel_verb.id, 'nsubj')
                if way_subject:
                    result["sub-s"] = way_subject.text
                result["sub-v"] = rel_verb.text
            else:
                # その他のデフォルト（目的語扱い）
                result["O1"] = ""
                result["sub-o1"] = noun_phrase
                if rel_subject:
                    result["sub-s"] = rel_subject.text
        
        # be動詞以外の場合の動詞設定
        if "sub-v" not in result and "sub-aux" not in result:
            result["sub-v"] = rel_verb.text
        
        return result
    
    def _build_noun_phrase(self, sent, antecedent, rel_pronoun, possessed_noun=None, preposition=None) -> str:
        """先行詞句を構築（修飾語含む、所有格・前置詞対応）"""
        if not antecedent:
            return rel_pronoun.text if rel_pronoun else ""
        
        # 先行詞の修飾語を収集
        modifiers = []
        for word in sent.words:
            if word.head == antecedent.id and word.deprel in ['det', 'amod', 'compound']:
                modifiers.append(word)
        
        # 語順でソート
        phrase_words = modifiers + [antecedent]
        
        # 前置詞+関係代名詞の場合
        if preposition and rel_pronoun:
            phrase_words.extend([preposition, rel_pronoun])
        # 所有格関係代名詞の場合
        elif possessed_noun and rel_pronoun:
            phrase_words.extend([rel_pronoun, possessed_noun])
        elif rel_pronoun:
            phrase_words.append(rel_pronoun)
        
        phrase_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理"""
        print("📝 単純文処理")
        
        root = self._find_root(sent)
        if not root:
            return {"error": "ROOT未検出"}
        
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
    
    # === ヘルパーメソッド ===
    def _find_by_deprel(self, sent, deprel: str):
        """依存関係で語を検索"""
        return next((w for w in sent.words if w.deprel == deprel), None)
    
    def _find_by_id(self, sent, word_id: int):
        """IDで語を検索"""
        return next((w for w in sent.words if w.id == word_id), None)
    
    def _find_by_head_and_deprel(self, sent, head_id: int, deprel: str):
        """頭IDと依存関係で語を検索"""
        return next((w for w in sent.words if w.head == head_id and w.deprel == deprel), None)
    
    def _find_root(self, sent):
        """ROOT語を検索"""
        return next((w for w in sent.words if w.head == 0), None)

# === テスト実行 ===
if __name__ == "__main__":
    print("="*60)
    print("🚀 シンプル関係節エンジン - 汎用性テスト")
    print("="*60)
    
    engine = SimpleRelativeEngine()
    
    # 複数の関係代名詞パターンをテスト
    test_cases = [
        # 目的語関係代名詞
        ("The book that he bought", "目的語関係代名詞"),
        ("The car which she drives", "目的語関係代名詞"),
        
        # 主語関係代名詞  
        ("The man who runs", "主語関係代名詞"),
        ("The dog which barks", "主語関係代名詞"),
        
        # 所有格関係代名詞
        ("The man whose car is red", "所有格関係代名詞"),
        ("The book whose cover is torn", "所有格関係代名詞"),
        
        # 関係副詞
        ("The place where he lives", "関係副詞 where"),
        ("The day when she arrived", "関係副詞 when"),
        
        # 前置詞+関係代名詞
        ("The book of which he spoke", "前置詞+関係代名詞 of"),
        ("The house in which he lives", "前置詞+関係代名詞 in"),
        ("The person to whom he gave it", "前置詞+関係代名詞 to"),
        
        # 関係副詞 why/how
        ("The reason why he is angry", "関係副詞 why"),
        ("The way we work", "関係副詞 how 省略"),
        ("The way how we work", "関係副詞 how 明示"),
    ]
    
    for i, (test_text, pattern_type) in enumerate(test_cases, 1):
        print(f"\n📖 テスト{i}: '{test_text}' ({pattern_type})")
        print("-" * 60)
        
        result = engine.process(test_text)
        
        print("📊 結果:")
        for key, value in result.items():
            print(f"  {key}: '{value}'")
    
    print("\n" + "="*60)
    print("🎯 汎用性確認: どのパターンも同じアルゴリズムで処理！")
    print("="*60)
