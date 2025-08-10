#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全スロット共通課題デバッグツール
spaCy依存構造解析の詳細分析

課題:
1. "home" 未配置問題: "to go home" の "home" が認識されない
2. 疑問詞節未処理問題: "what you said" が処理されない
"""

import spacy
from typing import List, Dict, Any

class CommonIssueDebugger:
    """全スロット共通課題のデバッグクラス"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def analyze_phrase(self, text: str) -> None:
        """フレーズの詳細分析"""
        doc = self.nlp(text)
        
        print(f"=== '{text}' の詳細分析 ===")
        print(f"トークン数: {len(doc)}")
        print()
        
        # 各トークンの詳細情報
        print("【トークン詳細】")
        for i, token in enumerate(doc):
            print(f"[{i}] '{token.text}':")
            print(f"    POS: {token.pos_}")
            print(f"    TAG: {token.tag_}")
            print(f"    DEP: {token.dep_}")
            print(f"    HEAD: '{token.head.text}' (index: {token.head.i})")
            print(f"    CHILDREN: {[child.text for child in token.children]}")
            print()
        
        # 依存関係の視覚化
        print("【依存関係ツリー】")
        for token in doc:
            indent = "  " * self._get_depth(token, doc)
            print(f"{indent}{token.text} ({token.dep_}) -> {token.head.text}")
        
        print()
        print("=" * 50)
        print()
    
    def _get_depth(self, token, doc) -> int:
        """トークンの階層深度を計算"""
        depth = 0
        current = token
        while current.head != current and current.i != current.head.i:
            depth += 1
            current = current.head
            if depth > 10:  # 無限ループ防止
                break
        return depth
    
    def find_objects_and_modifiers(self, text: str) -> Dict[str, List[str]]:
        """目的語と修飾語の検出"""
        doc = self.nlp(text)
        
        result = {
            'direct_objects': [],
            'indirect_objects': [],
            'prepositional_objects': [],
            'adverbial_modifiers': [],
            'nominal_modifiers': [],
            'unassigned_tokens': []
        }
        
        for token in doc:
            if token.dep_ == "dobj":
                result['direct_objects'].append(token.text)
            elif token.dep_ == "iobj":
                result['indirect_objects'].append(token.text)
            elif token.dep_ == "pobj":
                result['prepositional_objects'].append(token.text)
            elif token.dep_ in ["advmod", "amod"]:
                result['adverbial_modifiers'].append(token.text)
            elif token.dep_ in ["nmod", "compound"]:
                result['nominal_modifiers'].append(token.text)
            elif token.dep_ in ["ROOT", "aux", "mark", "cc", "det"]:
                # 構造的な語は除外
                continue
            else:
                result['unassigned_tokens'].append(f"{token.text}({token.dep_})")
        
        print(f"=== '{text}' の語彙分類 ===")
        for category, tokens in result.items():
            if tokens:
                print(f"{category}: {tokens}")
        print()
        
        return result

def debug_common_issues():
    """共通課題のデバッグ実行"""
    debugger = CommonIssueDebugger()
    
    # 問題ケースの分析
    problem_cases = [
        "to go home",           # home未配置問題
        "To learn English",     # 正常ケース（比較用）
        "eager to go home",     # C2での同様問題
        "what you said",        # 疑問詞節未処理
        "where he went",        # 疑問詞節未処理
        "reading books"         # 正常ケース（比較用）
    ]
    
    print("🔍 全スロット共通課題デバッグ開始\n")
    
    for case in problem_cases:
        debugger.analyze_phrase(case)
        debugger.find_objects_and_modifiers(case)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    debug_common_issues()
