#!/usr/bin/env python3
"""
実際のanalyze_sentence内の処理を段階的に再現
エラー発生の正確なタイミングを特定
"""

import traceback
from dynamic_grammar_mapper import DynamicGrammarMapper

def replicate_analyze_sentence_steps():
    """analyze_sentence内の処理を段階的に再現"""
    print("🔍 analyze_sentence内処理の段階的再現")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    sentence = "I run."
    
    try:
        print(f"📝 テスト文: '{sentence}'")
        
        # Step 1: 基本解析
        print("\n📍 Step 1: spaCy基本解析")
        doc = mapper.nlp(sentence)
        tokens = mapper._extract_tokens(doc)
        print(f"   ✅ tokens: {len(tokens)}個")
        
        # Step 2: 関係節検出
        print("\n📍 Step 2: 関係節構造検出")
        relative_clause_info = mapper._detect_relative_clause(tokens, sentence)
        print(f"   ✅ 関係節情報: {relative_clause_info}")
        
        # Step 3: ChatGPT5パイプライン実行
        print("\n📍 Step 3: ChatGPT5パイプライン実行")
        aux_info = {}
        verb_head_info = {}
        
        try:
            aux_info = mapper._detect_multiword_aux(doc) or {}
            print(f"   ✅ AuxResolver: {aux_info}")
            
            verb_head_info = mapper._select_verb_head(doc, aux_info) or {}
            print(f"   ✅ VerbHeadSelector: {verb_head_info}")
        except Exception as chatgpt5_error:
            print(f"   ❌ ChatGPT5エラー: {chatgpt5_error}")
            aux_info = {}
            verb_head_info = {}
        
        # Step 4: 除外インデックス設定
        print("\n📍 Step 4: 除外インデックス設定")
        excluded_indices = set()
        print(f"   ✅ 除外インデックス: {excluded_indices}")
        
        # Step 5: サブスロット生成
        print("\n📍 Step 5: サブスロット生成")
        sub_slots = {}
        original_tokens = tokens.copy()
        if relative_clause_info['found']:
            print("   📊 関係節処理中...")
            temp_core_elements = mapper._identify_core_elements(tokens)
            processed_tokens, sub_slots = mapper._process_relative_clause(original_tokens, relative_clause_info, temp_core_elements)
        else:
            print("   📊 関係節なし")
        print(f"   ✅ サブスロット: {sub_slots}")
        
        # Step 6: ChatGPT5結果の取得
        print("\n📍 Step 6: ChatGPT5結果確認")
        print(f"   ✅ aux_info: {aux_info}")
        print(f"   ✅ verb_head_info: {verb_head_info}")
        
        # Step 7: レガシーシステム処理（ここでエラーが発生？）
        print("\n📍 Step 7: レガシーシステム処理")
        
        # 7-1: フィルター処理
        print("   📊 7-1: トークンフィルタリング")
        filtered_tokens = [token for i, token in enumerate(tokens) if i not in excluded_indices]
        print(f"   ✅ フィルター後: {len(filtered_tokens)}個")
        
        # 7-2: コア要素特定
        print("   📊 7-2: コア要素特定")
        core_elements = mapper._identify_core_elements(filtered_tokens)
        print(f"   ✅ コア要素: {list(core_elements.keys())}")
        
        # 7-3: 文型推定
        print("   📊 7-3: 文型推定")
        sentence_pattern = mapper._determine_sentence_pattern(core_elements, filtered_tokens)
        print(f"   ✅ 文型: {sentence_pattern}")
        
        # 7-4: 文法要素割り当て
        print("   📊 7-4: 文法要素割り当て")
        grammar_elements = mapper._assign_grammar_roles(filtered_tokens, sentence_pattern, core_elements, relative_clause_info)
        print(f"   ✅ 文法要素: {type(grammar_elements)}")
        
        # 7-5: ChatGPT5結果統合
        print("   📊 7-5: ChatGPT5結果統合")
        if aux_info and aux_info.get('phrase'):
            grammar_elements['aux_detected'] = aux_info
            print("   ✅ aux統合完了")
        if verb_head_info and verb_head_info.get('main_verb'):
            grammar_elements['main_verb_detected'] = verb_head_info
            print("   ✅ verb統合完了")
        
        # 7-6: Rephraseフォーマット変換 (ここが怪しい？)
        print("   📊 7-6: Rephraseフォーマット変換")
        rephrase_result = mapper._convert_to_rephrase_format(grammar_elements, sentence_pattern, sub_slots)
        print(f"   ✅ Rephrase結果: {type(rephrase_result)}")
        
        print("\n🎯 すべてのステップが成功しました！")
        
    except Exception as e:
        print(f"\n❌ エラー発生: {type(e).__name__}: {e}")
        print("📊 詳細スタックトレース:")
        
        tb_lines = traceback.format_exc().split('\n')
        for i, line in enumerate(tb_lines):
            if line.strip():
                if 'list indices must be integers' in line:
                    print(f"🎯 TARGET ERROR {i}: {line}")
                elif 'dynamic_grammar_mapper.py' in line and 'line' in line:
                    print(f"📍 FILE LOCATION {i}: {line}")
                elif 'File' in line and '.py' in line:
                    print(f"📁 FILE {i}: {line}")
                else:
                    print(f"   {i}: {line}")

def test_chatgpt5_results_integration():
    """ChatGPT5結果の統合テスト"""
    print("\n🔍 ChatGPT5結果統合テスト")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    doc = mapper.nlp("I run.")
    
    # ChatGPT5処理実行
    aux_info = mapper._detect_multiword_aux(doc) or {}
    verb_head_info = mapper._select_verb_head(doc, aux_info) or {}
    
    print("📊 ChatGPT5結果の詳細:")
    print(f"   aux_info: {type(aux_info)}")
    if isinstance(aux_info, dict):
        print(f"      Keys: {list(aux_info.keys())}")
        for k, v in aux_info.items():
            print(f"        {k}: {v} (type: {type(v)})")
    
    print(f"   verb_head_info: {type(verb_head_info)}")
    if isinstance(verb_head_info, dict):
        print(f"      Keys: {list(verb_head_info.keys())}")
        for k, v in verb_head_info.items():
            print(f"        {k}: {v} (type: {type(v)})")

if __name__ == "__main__":
    # analyze_sentence処理の段階的再現
    replicate_analyze_sentence_steps()
    
    # ChatGPT5結果統合テスト
    test_chatgpt5_results_integration()
    
    print("\n🎯 調査完了")
    print("エラーの正確な発生タイミングを特定しました")
