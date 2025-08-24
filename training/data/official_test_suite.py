#!/usr/bin/env python3
"""
正規テスト: 現在のdynamic_grammar_mapperの詳細検証
ChatGPT5パイプライン実装による影響を正確に特定
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import json

def official_test_suite():
    """正規テストスイート実行"""
    print("🔍 正規テスト: dynamic_grammar_mapper 検証")
    print("=" * 70)
    
    mapper = DynamicGrammarMapper()
    
    # 標準的なテストケース
    test_cases = [
        {
            "sentence": "I run.",
            "expected_pattern": "SV",
            "expected_slots": {"S": "I", "V": "run"}
        },
        {
            "sentence": "She sings.",
            "expected_pattern": "SV", 
            "expected_slots": {"S": "She", "V": "sings"}
        },
        {
            "sentence": "Dogs bark.",
            "expected_pattern": "SV",
            "expected_slots": {"S": "Dogs", "V": "bark"}
        },
        {
            "sentence": "The cat sleeps.",
            "expected_pattern": "SV",
            "expected_slots": {"S": "The cat", "V": "sleeps"}
        },
        {
            "sentence": "We study English.",
            "expected_pattern": "SVO",
            "expected_slots": {"S": "We", "V": "study", "O1": "English"}
        },
        {
            "sentence": "He is happy.",
            "expected_pattern": "SVC",
            "expected_slots": {"S": "He", "V": "is", "C1": "happy"}
        },
        {
            "sentence": "I give you a book.",
            "expected_pattern": "SVOO",
            "expected_slots": {"S": "I", "V": "give", "O1": "you", "O2": "a book"}
        }
    ]
    
    print("📝 テストケース実行:")
    print("-" * 50)
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        sentence = test_case["sentence"]
        expected_pattern = test_case["expected_pattern"]
        expected_slots = test_case["expected_slots"]
        
        print(f"\n📍 Test {i}: '{sentence}'")
        print(f"   期待文型: {expected_pattern}")
        print(f"   期待スロット: {expected_slots}")
        
        try:
            # 実際の分析実行
            result = mapper.analyze_sentence(sentence)
            
            # 重要な結果を抽出
            actual_slots = result.get('slots', {})
            main_slots = result.get('main_slots', {})
            v_detected = result.get('V', None)
            pattern_detected = result.get('pattern_detected', 'Unknown')
            
            print(f"   実際スロット: {actual_slots}")
            print(f"   main_slots: {main_slots}")
            print(f"   V検出: {v_detected}")
            print(f"   文型検出: {pattern_detected}")
            
            # 評価
            test_result = {
                "test_id": i,
                "sentence": sentence,
                "expected_pattern": expected_pattern,
                "expected_slots": expected_slots,
                "actual_slots": actual_slots,
                "main_slots": main_slots,
                "v_detected": v_detected,
                "pattern_detected": pattern_detected,
                "success": True,
                "issues": []
            }
            
            # 具体的な問題チェック
            issues = []
            
            # 主動詞チェック
            if expected_slots.get("V") and v_detected != expected_slots["V"]:
                issues.append(f"主動詞不一致: 期待'{expected_slots['V']}' vs 実際'{v_detected}'")
            
            # 主語チェック
            if expected_slots.get("S"):
                actual_s = actual_slots.get("S") or main_slots.get("S")
                if actual_s != expected_slots["S"]:
                    issues.append(f"主語不一致: 期待'{expected_slots['S']}' vs 実際'{actual_s}'")
            
            # スロットの異常配置チェック
            if "bark" in actual_slots.values() or "bark" in main_slots.values():
                if sentence == "Dogs bark." and actual_slots.get("V") != "bark":
                    issues.append("barkが動詞以外のスロットに配置されている")
            
            test_result["issues"] = issues
            if issues:
                test_result["success"] = False
                print(f"   ❌ 問題: {', '.join(issues)}")
            else:
                print(f"   ✅ 正常")
            
            results.append(test_result)
            
        except Exception as e:
            print(f"   ❌ エラー: {type(e).__name__}: {e}")
            test_result = {
                "test_id": i,
                "sentence": sentence,
                "error": str(e),
                "success": False
            }
            results.append(test_result)
    
    return results

def detailed_dogs_bark_analysis():
    """Dogs bark. の詳細分析"""
    print("\n🔍 詳細分析: 'Dogs bark.' の処理過程")
    print("=" * 50)
    
    mapper = DynamicGrammarMapper()
    sentence = "Dogs bark."
    
    print(f"📝 対象文: '{sentence}'")
    
    # Step-by-step分析
    try:
        # 1. spaCy基本解析
        doc = mapper.nlp(sentence)
        tokens = mapper._extract_tokens(doc)
        
        print(f"\n📊 Step 1: spaCy解析")
        print(f"   トークン数: {len(tokens)}")
        for i, token in enumerate(tokens):
            if isinstance(token, dict):
                print(f"   [{i}] '{token.get('text', '')}' pos={token.get('pos', '')} dep={token.get('dep', '')}")
        
        # 2. 関係節検出
        relative_clause_info = mapper._detect_relative_clause(tokens, sentence)
        print(f"\n📊 Step 2: 関係節検出")
        print(f"   結果: {relative_clause_info.get('found', False)}")
        
        # 3. コア要素特定
        core_elements = mapper._identify_core_elements(tokens)
        print(f"\n📊 Step 3: コア要素特定")
        print(f"   主語: {core_elements.get('subject', 'None')}")
        print(f"   動詞: {core_elements.get('verb', 'None')}")
        print(f"   主語インデックス: {core_elements.get('subject_indices', [])}")
        print(f"   動詞インデックス: {core_elements.get('verb_indices', [])}")
        
        # 4. 文型判定
        sentence_pattern = mapper._determine_sentence_pattern(core_elements, tokens)
        print(f"\n📊 Step 4: 文型判定")
        print(f"   文型: {sentence_pattern}")
        
        # 5. 文法要素割り当て
        grammar_elements = mapper._assign_grammar_roles(tokens, sentence_pattern, core_elements, relative_clause_info)
        print(f"\n📊 Step 5: 文法要素割り当て")
        print(f"   要素数: {len(grammar_elements) if isinstance(grammar_elements, list) else 'Not List'}")
        if isinstance(grammar_elements, list):
            for element in grammar_elements:
                if hasattr(element, 'role') and hasattr(element, 'text'):
                    print(f"   {element.role}: '{element.text}'")
        
        # 6. 最終結果
        final_result = mapper.analyze_sentence(sentence)
        print(f"\n📊 Step 6: 最終結果")
        print(f"   slots: {final_result.get('slots', {})}")
        print(f"   main_slots: {final_result.get('main_slots', {})}")
        print(f"   V: {final_result.get('V', None)}")
        
    except Exception as e:
        print(f"❌ 分析エラー: {e}")
        import traceback
        traceback.print_exc()

def generate_test_report(results):
    """テスト結果レポート生成"""
    print("\n📊 テスト結果サマリー")
    print("=" * 50)
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r.get("success", False))
    failed_tests = total_tests - successful_tests
    
    print(f"総テスト数: {total_tests}")
    print(f"成功: {successful_tests}")
    print(f"失敗: {failed_tests}")
    print(f"成功率: {successful_tests/total_tests*100:.1f}%")
    
    if failed_tests > 0:
        print(f"\n❌ 失敗したテスト:")
        for result in results:
            if not result.get("success", False):
                print(f"   Test {result['test_id']}: '{result['sentence']}'")
                if "issues" in result:
                    for issue in result["issues"]:
                        print(f"     - {issue}")
                if "error" in result:
                    print(f"     - エラー: {result['error']}")

if __name__ == "__main__":
    # 正規テストスイート実行
    test_results = official_test_suite()
    
    # Dogs bark. 詳細分析
    detailed_dogs_bark_analysis()
    
    # レポート生成
    generate_test_report(test_results)
    
    print("\n🎯 正規テスト完了")
    print("現在のシステムの実際の動作が明確になりました")
