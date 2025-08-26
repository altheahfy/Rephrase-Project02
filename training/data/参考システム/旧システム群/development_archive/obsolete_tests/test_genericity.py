#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stanza

class GenericityTester:
    def __init__(self):
        print("🧪 汎用性テスト開始")
        self.nlp = stanza.Pipeline('en', verbose=False)
    
    def test_c2_genericity(self):
        """C2スロット除外アルゴリズムの汎用性テスト"""
        
        test_sentences = [
            # テスト1: 短い文
            "John made Mary sing beautifully although she was nervous.",
            
            # テスト2: 複雑な目的語
            "The teacher forced all struggling students to complete their assignments carefully even though they lacked time.",
            
            # テスト3: 異なる副詞節タイプ
            "The manager encouraged the team to finish the project successfully because the deadline was approaching.",
            
            # テスト4: 多重副詞節
            "She convinced her colleagues to present their ideas confidently although they were inexperienced because success required courage."
        ]
        
        for i, sentence in enumerate(test_sentences, 1):
            print(f"\n{'='*60}")
            print(f"🧪 テスト{i}: {sentence[:50]}...")
            
            doc = self.nlp(sentence)
            for sent in doc.sentences:
                self._analyze_c2_pattern(sent)
    
    def _analyze_c2_pattern(self, sent):
        """C2パターンの構造解析"""
        
        # ROOT動詞を探す
        root_verb = None
        for word in sent.words:
            if word.deprel == 'root':
                root_verb = word
                break
        
        if not root_verb:
            print("❌ ROOT動詞が見つかりません")
            return
            
        print(f"📌 ROOT動詞: {root_verb.text}")
        
        # MAKE動詞（xcomp）を探す
        make_verb = None
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                make_verb = word
                break
                
        if not make_verb:
            print("❌ xcomp動詞が見つかりません")
            return
            
        print(f"📌 XCOMP動詞: {make_verb.text}")
        
        # C2動詞（advcl）を探す
        c2_verb = None
        for word in sent.words:
            if word.head == make_verb.id and word.deprel == 'advcl':
                c2_verb = word
                break
                
        if not c2_verb:
            print("❌ C2動詞が見つかりません")
            return
            
        print(f"📌 C2動詞: {c2_verb.text}")
        
        # C2動詞の子要素を分析
        print(f"\n📋 {c2_verb.text}動詞の子要素:")
        
        c2_words = {c2_verb.id}
        advcl_children = []
        
        for word in sent.words:
            if word.head == c2_verb.id:
                print(f"  {word.text:15} ({word.deprel:10}) -> {c2_verb.text}")
                
                if word.deprel == 'advcl':
                    advcl_children.append(word)
                    print(f"    ↑ 副詞節検出！除外対象")
                else:
                    c2_words.add(word.id)
                    # 非advcl子要素の子孫も追加
                    descendants = self._collect_non_advcl_descendants(sent, word)
                    c2_words.update(descendants)
        
        # C2範囲を計算
        if c2_words:
            min_start = min(sent.words[word_id-1].start_char for word_id in c2_words)
            max_end = max(sent.words[word_id-1].end_char for word_id in c2_words)
            c2_text = sent.text[min_start:max_end]
            print(f"\n✅ C2抽出結果: '{c2_text}'")
        
        # 除外された副詞節も表示
        for advcl_child in advcl_children:
            advcl_words = {advcl_child.id}
            descendants = self._collect_all_descendants(sent, advcl_child)
            advcl_words.update(descendants)
            
            min_start = min(sent.words[word_id-1].start_char for word_id in advcl_words)
            max_end = max(sent.words[word_id-1].end_char for word_id in advcl_words)
            advcl_text = sent.text[min_start:max_end]
            print(f"🚫 除外された副詞節: '{advcl_text}'")
    
    def _collect_non_advcl_descendants(self, sent, word):
        """advcl以外の子孫収集"""
        descendants = set()
        for child in sent.words:
            if child.head == word.id and child.deprel != 'advcl':
                descendants.add(child.id)
                child_descendants = self._collect_non_advcl_descendants(sent, child)
                descendants.update(child_descendants)
        return descendants
    
    def _collect_all_descendants(self, sent, word):
        """全子孫収集"""
        descendants = set()
        for child in sent.words:
            if child.head == word.id:
                descendants.add(child.id)
                child_descendants = self._collect_all_descendants(sent, child)
                descendants.update(child_descendants)
        return descendants

if __name__ == '__main__':
    tester = GenericityTester()
    tester.test_c2_genericity()
