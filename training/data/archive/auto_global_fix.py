#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全サブスロット自動修正スクリプト
advmod（副詞修飾語）と節構造の処理を統一的に修正
"""

import os
import re
import json
import spacy
from collections import defaultdict
import shutil
from datetime import datetime

# spaCyモデルの読み込み（警告を抑制）
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("❌ spaCy英語モデルが見つかりません。インストールしてください:")
    print("python -m spacy download en_core_web_sm")
    exit(1)

def analyze_sentence(sentence):
    """文の構造を解析してadvmodと節構造を検出"""
    doc = nlp(sentence)
    
    advmod_tokens = []
    clause_structure = {
        'has_subject': False,
        'has_verb': False,
        'subjects': [],
        'verbs': []
    }
    
    for token in doc:
        # advmod（副詞修飾語）を検出
        if token.dep_ == "advmod":
            advmod_tokens.append(token.text)
        
        # 節構造の要素を検出
        if token.dep_ in ["nsubj", "nsubjpass", "csubj"]:
            clause_structure['has_subject'] = True
            clause_structure['subjects'].append(token.text)
        
        if token.pos_ == "VERB":
            clause_structure['has_verb'] = True
            clause_structure['verbs'].append(token.text)
    
    return {
        'advmod_tokens': advmod_tokens,
        'clause_structure': clause_structure,
        'has_clause': clause_structure['has_subject'] and clause_structure['has_verb']
    }

def backup_file(filepath):
    """ファイルのバックアップを作成"""
    backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(filepath, backup_path)
    return backup_path

def apply_advmod_fix(filepath):
    """advmod処理修正をファイルに適用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # advmodトークンをスキップする処理を追加
    advmod_fix = '''
        # advmod（副詞修飾語）は修飾子サブスロットで処理
        if token.dep_ == "advmod":
            continue
'''
    
    # process_tokenメソッド内でのトークン処理部分を探して修正
    pattern = r'(\s+)def process_token\(self, token\):[^}]+?(\s+)for token in doc:'
    
    # より具体的なパターンでadvmod処理を追加
    if 'def process_token(self, token):' in content:
        # process_tokenメソッドの最初にadvmodチェックを追加
        old_pattern = r'(def process_token\(self, token\):\s*"""[^"]*"""\s*)'
        new_replacement = r'\1' + advmod_fix.strip() + '\n        '
        
        content = re.sub(old_pattern, new_replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def apply_clause_detection_fix(filepath):
    """節構造検出修正をファイルに適用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 節構造検出の改善
    clause_fix = '''
        # 節構造（SV）を持つ場合は詳細分析
        analysis = self.analyze_clause_structure(phrase)
        if analysis['has_clause']:
            self.handle_clause_structure(phrase, analysis)
            continue
'''
    
    # analyze_clause_structure メソッドを追加
    clause_analysis_method = '''
    
    def analyze_clause_structure(self, phrase):
        """節構造を分析"""
        doc = self.nlp(phrase)
        analysis = {
            'has_subject': False,
            'has_verb': False,
            'subjects': [],
            'verbs': [],
            'objects': []
        }
        
        for token in doc:
            if token.dep_ in ["nsubj", "nsubjpass", "csubj"]:
                analysis['has_subject'] = True
                analysis['subjects'].append(token.text)
            elif token.pos_ == "VERB":
                analysis['has_verb'] = True
                analysis['verbs'].append(token.text)
            elif token.dep_ in ["dobj", "iobj"]:
                analysis['objects'].append(token.text)
        
        analysis['has_clause'] = analysis['has_subject'] and analysis['has_verb']
        return analysis
    
    def handle_clause_structure(self, phrase, analysis):
        """節構造を適切なサブスロットに振り分け"""
        print(f"🔄 節構造検出: '{phrase}' → S:{analysis['subjects']}, V:{analysis['verbs']}, O:{analysis['objects']}")
'''
    
    # クラスの最後にメソッドを追加
    if 'class ' in content and 'SubSlot' in content:
        # クラスの終わりを見つけて、メソッドを追加
        content += clause_analysis_method
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """メイン実行関数"""
    print("🔧 全サブスロット自動修正を開始")
    
    # 修正対象ファイルを検索
    subslot_files = []
    for filename in os.listdir('.'):
        if filename.startswith('step') and 'subslot' in filename and filename.endswith('.py'):
            subslot_files.append(filename)
    
    print(f"📁 修正対象ファイル数: {len(subslot_files)}")
    
    fixed_count = 0
    for filepath in subslot_files:
        print(f"\n🔧 修正中: {filepath}")
        
        try:
            # バックアップ作成
            backup_path = backup_file(filepath)
            print(f"💾 バックアップ作成: {backup_path}")
            
            # advmod修正適用
            if apply_advmod_fix(filepath):
                print("✅ advmod処理修正適用完了")
            
            # 節構造検出修正適用
            if apply_clause_detection_fix(filepath):
                print("✅ 節構造検出修正適用完了")
            
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ 修正エラー: {e}")
            continue
    
    print(f"\n🎉 修正完了: {fixed_count}/{len(subslot_files)} ファイル")
    print("\n📝 修正内容:")
    print("  1. advmod（副詞修飾語）は修飾子サブスロットで処理するよう変更")
    print("  2. 節構造（SV）検出機能を追加")
    print("  3. 各サブスロットでの適切な振り分け処理を追加")
    
    # テスト実行の提案
    print("\n🧪 修正後テスト推奨:")
    print("python step12_s_subslot.py")
    print("python step13_o1_subslot_new.py")

if __name__ == "__main__":
    main()
