#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2: 最小限のSubslot Generator - sub-s（主語）のみ
========================================================
構造解析ベースで1つのsubslotから始める
"""

import spacy

class MinimalSubslotGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract_subject_subslot(self, text):
        """sub-s: 主語subslotのみを抽出"""
        doc = self.nlp(text)
        
        # ROOTを見つける
        root = None
        for token in doc:
            if token.dep_ == "ROOT":
                root = token
                break
        
        if not root:
            return None
        
        # ROOTの子の中からnsubj（主語）を探す
        subjects = []
        for child in root.children:
            if child.dep_ in ["nsubj", "nsubjpass"]:  # 能動・受動両方対応
                # 主語とその修飾語を含める
                subject_tokens = self._collect_subtree(child)
                subjects.append({
                    'text': ' '.join([t.text for t in subject_tokens]),
                    'tokens': [t.text for t in subject_tokens],
                    'root_token': child.text,
                    'dependency': child.dep_
                })
        
        return {
            'sentence': text,
            'sub-s': subjects[0] if subjects else None
        }
    
    def _collect_subtree(self, token):
        """トークンとその全ての子（修飾語等）を収集"""
        subtree = []
        
        # 深さ優先で子を収集
        def collect_children(t):
            subtree.append(t)
            for child in sorted(t.children, key=lambda x: x.i):  # 語順を保持
                collect_children(child)
        
        collect_children(token)
        return sorted(subtree, key=lambda x: x.i)  # 元の語順でソート

def test_minimal_generator():
    """最小限のテスト"""
    generator = MinimalSubslotGenerator()
    
    test_sentences = [
        "The manager works.",
        "The experienced manager works efficiently.",
        "The manager who works here is experienced.",
        "A new project was completed."  # 受動文
    ]
    
    print("=== 最小限Subslot Generator テスト ===")
    for sentence in test_sentences:
        result = generator.extract_subject_subslot(sentence)
        print(f"\n文: {sentence}")
        if result and result['sub-s']:
            sub_s = result['sub-s']
            print(f"sub-s: '{sub_s['text']}'")
            print(f"  - root_token: '{sub_s['root_token']}'")
            print(f"  - dependency: {sub_s['dependency']}")
            print(f"  - tokens: {sub_s['tokens']}")
        else:
            print("sub-s: 見つかりませんでした")

if __name__ == "__main__":
    test_minimal_generator()
