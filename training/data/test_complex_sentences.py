#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版エンジンの複雑例文テスト
以前問題だった複雑な例文での性能を検証
"""

from ImprovedRephraseParsingEngine import ImprovedRephraseParsingEngine

def test_complex_sentences():
    """複雑な例文での改良版エンジンテスト"""
    print("🔍 改良版エンジン：複雑例文性能テスト\n")
    
    # エンジン初期化
    engine = ImprovedRephraseParsingEngine()
    
    # 以前に問題だった複雑な例文
    complex_test_cases = [
        {
            "sentence": "This morning when the request became urgent, the teacher who had just returned from a long absence might have given the student a summary.",
            "issues": "複雑な時間節・関係詞節・助動詞の組み合わせ",
            "expected_improvements": ["主語の正確な特定", "時間修飾語の正確な分離", "主動詞の正確な特定"]
        },
        {
            "sentence": "That afternoon at the crucial point in the presentation, the manager had to make the committee deliver the proposal.",
            "issues": "複数の前置詞句・使役動詞構造",
            "expected_improvements": ["時間表現の正確な認識", "複合前置詞句の適切な分類", "SVOC構造の認識"]
        },
        {
            "sentence": "He left New York a few days ago.",
            "issues": "時間修飾語の分離（以前は正しく処理できていたが確認）",
            "expected_improvements": ["時間修飾語の完全な形での抽出"]
        },
        {
            "sentence": "I can't afford it.",
            "issues": "助動詞縮約形の処理",
            "expected_improvements": ["縮約形の正確な認識"]
        }
    ]
    
    print(f"📊 {len(complex_test_cases)} 個の複雑例文をテスト\n")
    
    for i, test_case in enumerate(complex_test_cases, 1):
        sentence = test_case["sentence"]
        issues = test_case["issues"]
        improvements = test_case["expected_improvements"]
        
        print(f"=== テスト {i}: 複雑度レベル {i} ===")
        print(f"例文: {sentence}")
        print(f"従来の問題: {issues}")
        print(f"期待される改善: {', '.join(improvements)}")
        
        try:
            # 改良版エンジンでパーシング
            result = engine.analyze_sentence(sentence)
            print(f"改良版結果:")
            
            # 結果を整理して表示
            display_result_analysis(result)
            
            # 構造分析も表示
            print("📋 構造分析:")
            analyze_sentence_structure(sentence, result)
            
        except Exception as e:
            print(f"❌ パーシングエラー: {e}")
        
        print("\n" + "="*60 + "\n")

def display_result_analysis(result):
    """結果を分析して表示"""
    if not result or 'error' in result:
        print(f"  ❌ エラー: {result.get('error', 'Unknown error')}")
        return
        
    # スロット順序で表示
    slot_order = ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
    
    for slot in slot_order:
        if slot in result and result[slot]:
            items = result[slot]
            if isinstance(items, list):
                values = []
                for item in items:
                    if isinstance(item, dict) and 'value' in item:
                        rule_info = f"({item.get('rule_id', 'unknown')})" if 'rule_id' in item else ""
                        values.append(f"'{item['value']}' {rule_info}")
                    else:
                        values.append(f"'{str(item)}'")
                print(f"  {slot}: {', '.join(values)}")
            else:
                print(f"  {slot}: '{str(items)}'")

def analyze_sentence_structure(sentence, result):
    """文構造の分析結果を表示"""
    
    # 基本構造の確認
    has_subject = 'S' in result and result['S']
    has_verb = 'V' in result and result['V']
    has_object = any(slot in result and result[slot] for slot in ['O1', 'O2'])
    has_modifiers = any(slot in result and result[slot] for slot in ['M1', 'M2', 'M3'])
    has_aux = 'Aux' in result and result['Aux']
    
    print(f"  主語: {'✅' if has_subject else '❌'}")
    print(f"  動詞: {'✅' if has_verb else '❌'}")
    print(f"  目的語: {'✅' if has_object else '❌'}")
    print(f"  助動詞: {'✅' if has_aux else '❌'}")
    print(f"  修飾語: {'✅' if has_modifiers else '❌'}")
    
    # 文型の推定
    if has_subject and has_verb:
        if 'O1' in result and result['O1'] and 'O2' in result and result['O2']:
            print("  推定文型: 第4文型 (SVOO)")
        elif 'O1' in result and result['O1']:
            if 'C1' in result and result['C1']:
                print("  推定文型: 第5文型 (SVOC)")
            else:
                print("  推定文型: 第3文型 (SVO)")
        elif 'C1' in result and result['C1']:
            print("  推定文型: 第2文型 (SVC)")
        else:
            print("  推定文型: 第1文型 (SV)")
    else:
        print("  推定文型: 不完全または特殊構造")
    
    # 修飾語の分類
    modifier_types = []
    if 'M1' in result and result['M1']:
        modifier_types.append("M1(場所・状況)")
    if 'M2' in result and result['M2']:
        modifier_types.append("M2(方法・手段)")
    if 'M3' in result and result['M3']:
        modifier_types.append("M3(時間・頻度)")
    
    if modifier_types:
        print(f"  修飾語分類: {', '.join(modifier_types)}")

if __name__ == "__main__":
    test_complex_sentences()
