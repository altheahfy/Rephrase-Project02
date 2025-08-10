#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rule Dictionary v2.0 - 全サブスロット共通修正パッチ
全サブスロットファイルに適用する統一修正システム

修正対象:
1. advmod(副詞修飾語)の誤分類防止 - "home"は修飾子として扱う
2. 節構造の適切な分解 - "what you said"のような完全SV構造
3. 未分類トークンの適切な処理
"""

import spacy
import os
import glob
from typing import Dict, List, Tuple, Any

class GlobalSubslotFixer:
    """全サブスロット共通修正クラス"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def apply_common_fixes_to_all_subslots(self):
        """全サブスロットファイルに共通修正を適用"""
        
        # 対象サブスロットファイルを検索
        subslot_files = glob.glob("step*_*subslot*.py")
        
        print("🔧 全サブスロット共通修正開始")
        print(f"対象ファイル数: {len(subslot_files)}")
        
        for file_path in subslot_files:
            print(f"\n📝 修正中: {file_path}")
            self._apply_fixes_to_file(file_path)
            
        print("\n✅ 全サブスロット共通修正完了")
    
    def _apply_fixes_to_file(self, file_path: str):
        """個別ファイルに修正を適用"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 修正1: advmod除外フィルターを追加
            fixed_content = self._add_advmod_filter(content)
            
            # 修正2: 節構造検出の改善
            fixed_content = self._improve_clause_detection(fixed_content)
            
            # 修正3: 未分類トークン処理の追加
            fixed_content = self._add_unassigned_token_handling(fixed_content)
            
            # バックアップ作成
            backup_path = file_path.replace('.py', '_backup.py')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # 修正版を保存
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
                
            print(f"  ✅ 修正完了: {file_path}")
            print(f"  📄 バックアップ: {backup_path}")
            
        except Exception as e:
            print(f"  ❌ 修正エラー: {file_path} - {e}")
    
    def _add_advmod_filter(self, content: str) -> str:
        """advmod除外フィルターを追加"""
        
        # 既存の分類ロジックにadvmod除外を追加
        advmod_filter_code = '''        
        # advmod(副詞修飾語)は修飾子として扱い、当サブスロットでは除外
        if token.dep_ == "advmod":
            continue  # homeなどの副詞修飾語は修飾子サブスロットで処理
        '''
        
        # 適切な位置にフィルターを挿入
        if "for token in doc:" in content and "advmod" not in content:
            content = content.replace(
                "for token in doc:",
                f"for token in doc:{advmod_filter_code}\n        "
            )
            
        return content
    
    def _improve_clause_detection(self, content: str) -> str:
        """節構造検出の改善"""
        
        clause_improvement = '''
        # 完全SV構造の節検出改善
        def _is_complete_clause(self, doc):
            """完全な節構造かどうかを判定"""
            has_subject = any(token.dep_ == "nsubj" for token in doc)
            has_verb = any(token.pos_ == "VERB" and token.dep_ == "ROOT" for token in doc)
            return has_subject and has_verb
        '''
        
        # クラス定義の後に新メソッドを追加
        if "class " in content and "_is_complete_clause" not in content:
            class_end = content.find("\n    def ")
            if class_end != -1:
                content = content[:class_end] + clause_improvement + content[class_end:]
                
        return content
    
    def _add_unassigned_token_handling(self, content: str) -> str:
        """未分類トークン処理の追加"""
        
        unassigned_handler = '''
        # 未分類トークン（nsubj等）の適切な処理
        unassigned_tokens = []
        for token in doc:
            if token.dep_ in ["nsubj", "nsubjpass"] and not self._is_processed_token(token):
                unassigned_tokens.append(token)
        
        if unassigned_tokens:
            # 主語トークンは別サブスロット（S）で処理するため記録のみ
            subslots["_unassigned_subjects"] = [token.text for token in unassigned_tokens]
        '''
        
        # サブスロット生成メソッドの最後に追加
        if "return subslots" in content and "_unassigned" not in content:
            return_pos = content.rfind("return subslots")
            if return_pos != -1:
                content = content[:return_pos] + unassigned_handler + "\n        " + content[return_pos:]
                
        return content
    
    def test_common_fixes(self):
        """共通修正の動作テスト"""
        
        test_cases = [
            ("to go home", "phrase"),           # homeはadvmod
            ("what you said", "clause"),        # 完全SV構造
            ("eager to go home", "phrase"),     # homeはadvmod
            ("To learn English", "phrase"),     # Englishはdobj
        ]
        
        print("🧪 共通修正テスト開始")
        
        for phrase, phrase_type in test_cases:
            print(f"\n📝 テスト: '{phrase}' ({phrase_type})")
            
            doc = self.nlp(phrase)
            
            # advmod検出
            advmod_tokens = [token.text for token in doc if token.dep_ == "advmod"]
            if advmod_tokens:
                print(f"  🎯 advmod検出: {advmod_tokens} → 修飾子サブスロットで処理")
            
            # 節構造検出
            has_subject = any(token.dep_ == "nsubj" for token in doc)
            has_verb = any(token.pos_ == "VERB" and token.dep_ == "ROOT" for token in doc)
            if has_subject and has_verb:
                print(f"  🎯 完全節構造検出: SV構造あり")
            
            # 未分類トークン検出
            unassigned = [token.text for token in doc if token.dep_ in ["nsubj", "nsubjpass"]]
            if unassigned:
                print(f"  🎯 未分類主語: {unassigned} → Sサブスロットで処理")

if __name__ == "__main__":
    fixer = GlobalSubslotFixer()
    
    # まずテスト実行
    fixer.test_common_fixes()
    
    print("\n" + "="*60)
    
    # 実際の修正適用
    user_input = input("\n全サブスロットファイルに修正を適用しますか？ (y/N): ")
    if user_input.lower() == 'y':
        fixer.apply_common_fixes_to_all_subslots()
    else:
        print("修正をキャンセルしました。")
