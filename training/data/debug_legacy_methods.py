#!/usr/bin/env python3
"""
レガシーシステムエラー発生箇所の特定
各メソッドを個別テストしてエラー箇所を特定
"""

import traceback
from dynamic_grammar_mapper import DynamicGrammarMapper

def test_individual_legacy_methods():
    """レガシーメソッドを個別テスト"""
    print("🔍 レガシーシステムメソッド個別テスト")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    
    # テスト用のデータを準備
    test_sentence = "I run."
    doc = mapper.nlp(test_sentence)
    tokens = mapper._extract_tokens(doc)
    
    print(f"📝 テスト文: '{test_sentence}'")
    print(f"🎯 トークン数: {len(tokens)}")
    print(f"📊 トークン構造: {[type(token) for token in tokens[:3]]}")
    
    # 除外インデックスの準備
    excluded_indices = set()
    filtered_tokens = [token for i, token in enumerate(tokens) if i not in excluded_indices]
    
    print(f"🔧 フィルター後トークン数: {len(filtered_tokens)}")
    
    # 各メソッドを個別テスト
    methods_to_test = [
        ('_identify_core_elements', lambda: mapper._identify_core_elements(filtered_tokens)),
        ('_determine_sentence_pattern', None),  # core_elementsが必要
        ('_assign_grammar_roles', None),       # multiple paramsが必要
        ('_convert_to_rephrase_format', None)  # multiple paramsが必要
    ]
    
    core_elements = None
    sentence_pattern = None
    grammar_elements = None
    
    for method_name, method_func in methods_to_test:
        print(f"\n📍 テスト: {method_name}")
        print("-" * 40)
        
        try:
            if method_name == '_identify_core_elements':
                result = method_func()
                core_elements = result
                print(f"   ✅ 成功: {type(result)}")
                print(f"   📊 キー: {list(result.keys()) if isinstance(result, dict) else 'Not Dict'}")
                
            elif method_name == '_determine_sentence_pattern':
                if core_elements is not None:
                    result = mapper._determine_sentence_pattern(core_elements, filtered_tokens)
                    sentence_pattern = result
                    print(f"   ✅ 成功: {result}")
                else:
                    print("   ⏭️ スキップ: core_elementsがNone")
                    
            elif method_name == '_assign_grammar_roles':
                if core_elements is not None and sentence_pattern is not None:
                    relative_clause_info = {'found': False, 'type': None}
                    result = mapper._assign_grammar_roles(filtered_tokens, sentence_pattern, core_elements, relative_clause_info)
                    grammar_elements = result
                    print(f"   ✅ 成功: {type(result)}")
                    print(f"   📊 キー: {list(result.keys()) if isinstance(result, dict) else 'Not Dict'}")
                else:
                    print("   ⏭️ スキップ: 前提条件が不足")
                    
            elif method_name == '_convert_to_rephrase_format':
                if grammar_elements is not None and sentence_pattern is not None:
                    sub_slots = {}
                    result = mapper._convert_to_rephrase_format(grammar_elements, sentence_pattern, sub_slots)
                    print(f"   ✅ 成功: {type(result)}")
                    print(f"   📊 キー: {list(result.keys()) if isinstance(result, dict) else 'Not Dict'}")
                else:
                    print("   ⏭️ スキップ: 前提条件が不足")
                    
        except Exception as e:
            print(f"   ❌ エラー発生: {type(e).__name__}: {e}")
            print("   📊 詳細スタックトレース:")
            
            # スタックトレースの詳細表示
            tb_lines = traceback.format_exc().split('\n')
            for line in tb_lines:
                if line.strip():
                    if 'list indices must be integers' in line:
                        print(f"   🎯 TARGET ERROR: {line}")
                    elif 'dynamic_grammar_mapper.py' in line and 'line' in line:
                        print(f"   📍 FILE LOCATION: {line}")
                    else:
                        print(f"   {line}")
            
            # このメソッドでエラーが発生したので、以降はスキップ
            break

def test_data_structure_analysis():
    """データ構造の詳細分析"""
    print("\n🔍 データ構造詳細分析")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    doc = mapper.nlp("I run.")
    tokens = mapper._extract_tokens(doc)
    
    print("📊 tokens配列の詳細:")
    for i, token in enumerate(tokens):
        print(f"   [{i}] Type: {type(token)}")
        if hasattr(token, '__dict__'):
            print(f"       Attributes: {list(token.__dict__.keys())[:5]}...")  # 最初の5個のみ
        if isinstance(token, dict):
            print(f"       Dict Keys: {list(token.keys())}")
        if hasattr(token, 'text'):
            print(f"       Text: '{token.text}'")
        print()

def test_access_patterns():
    """問題のあるアクセスパターンのテスト"""
    print("\n🔍 アクセスパターンテスト")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    doc = mapper.nlp("I run.")
    tokens = mapper._extract_tokens(doc)
    
    # 危険なアクセスパターンをテスト
    test_patterns = [
        ("tokens[0]['text']", lambda: tokens[0]['text']),
        ("tokens[0].text", lambda: tokens[0].text),
        ("str(tokens[0])", lambda: str(tokens[0])),
        ("isinstance(tokens[0], dict)", lambda: isinstance(tokens[0], dict)),
    ]
    
    for pattern_name, pattern_func in test_patterns:
        print(f"📍 テスト: {pattern_name}")
        try:
            result = pattern_func()
            print(f"   ✅ 成功: {result}")
        except Exception as e:
            print(f"   ❌ エラー: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # レガシーメソッド個別テスト
    test_individual_legacy_methods()
    
    # データ構造分析
    test_data_structure_analysis()
    
    # アクセスパターンテスト
    test_access_patterns()
    
    print("\n🎯 調査完了")
    print("エラー発生箇所を特定しました")
