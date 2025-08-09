#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包括的パーシングエンジン性能評価スクリプト
最も複雑で長い例文を使用してシステムの真の能力をテスト
"""

import pandas as pd
import sys
import os
from Rephrase_Parsing_Engine import RephraseParsingEngine
import json
import traceback

def load_complex_sentences():
    """最も複雑な例文セットを読み込み"""
    excel_file = "（小文字化した最初の5文型フルセット）例文入力元.xlsx"
    
    try:
        # Excelファイルを読み込み（シート名を指定しない場合は最初のシート）
        df = pd.read_excel(excel_file)
        print(f"✅ Excelファイル読み込み成功: {len(df)} 行")
        print(f"カラム名: {list(df.columns)}")
        
        # 例文を含む可能性のあるカラムを探す
        sentence_columns = []
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in ['例文', 'sentence', 'example', '英文']):
                sentence_columns.append(col)
        
        print(f"例文カラム候補: {sentence_columns}")
        
        # 最初の10行を表示して構造を確認
        print("\n=== ファイル構造確認（最初の10行） ===")
        for i in range(min(10, len(df))):
            print(f"行 {i+1}: {dict(df.iloc[i])}")
        
        return df, sentence_columns
        
    except Exception as e:
        print(f"❌ Excelファイル読み込みエラー: {e}")
        return None, None

def analyze_sentence_complexity(sentence):
    """例文の複雑度を分析"""
    if pd.isna(sentence) or not isinstance(sentence, str):
        return 0
    
    complexity_score = 0
    sentence = str(sentence).strip()
    
    # 文の長さ
    word_count = len(sentence.split())
    complexity_score += word_count
    
    # 複雑な構造のマーカー
    complex_markers = [
        'which', 'that', 'who', 'whom', 'whose', 'when', 'where', 'why',
        'although', 'because', 'since', 'while', 'if', 'unless', 'until',
        'before', 'after', 'as soon as', 'in order to', 'so that',
        'not only', 'either', 'neither', 'both', 'whether'
    ]
    
    for marker in complex_markers:
        if marker in sentence.lower():
            complexity_score += 10
    
    # 時間表現
    time_expressions = [
        'ago', 'yesterday', 'tomorrow', 'last', 'next', 'every', 'often',
        'always', 'never', 'sometimes', 'usually', 'frequently', 'rarely',
        'in the morning', 'at night', 'during', 'while', 'since', 'for'
    ]
    
    for time_expr in time_expressions:
        if time_expr in sentence.lower():
            complexity_score += 5
    
    return complexity_score

def test_parsing_engine_comprehensively():
    """パーシングエンジンの包括的テスト"""
    print("🔍 包括的パーシングエンジン性能評価を開始...")
    
    # Excelファイル読み込み
    df, sentence_columns = load_complex_sentences()
    if df is None:
        return
    
    # パーシングエンジン初期化
    try:
        engine = RephraseParsingEngine()
        print("✅ パーシングエンジン初期化成功")
    except Exception as e:
        print(f"❌ パーシングエンジン初期化失敗: {e}")
        return
    
    # 例文を収集・分析
    all_sentences = []
    
    for col in df.columns:
        for idx, value in enumerate(df[col]):
            if pd.notna(value) and isinstance(value, str) and len(str(value).strip()) > 5:
                sentence = str(value).strip()
                # 明らかに英文でないものを除外
                if any(char.isalpha() for char in sentence) and not sentence.startswith('#'):
                    complexity = analyze_sentence_complexity(sentence)
                    all_sentences.append({
                        'sentence': sentence,
                        'complexity': complexity,
                        'source_column': col,
                        'source_row': idx + 1
                    })
    
    print(f"\n📊 収集した例文数: {len(all_sentences)}")
    
    # 複雑度でソート（最も複雑なものから）
    all_sentences.sort(key=lambda x: x['complexity'], reverse=True)
    
    # 上位の複雑な例文をテスト
    test_count = min(20, len(all_sentences))  # 最大20文をテスト
    print(f"\n🧪 最も複雑な {test_count} 文をテスト開始...")
    
    results = []
    success_count = 0
    error_count = 0
    
    for i, sentence_data in enumerate(all_sentences[:test_count]):
        sentence = sentence_data['sentence']
        complexity = sentence_data['complexity']
        
        print(f"\n=== テスト {i+1}/{test_count} (複雑度: {complexity}) ===")
        print(f"例文: {sentence}")
        
        try:
            # パーシング実行
            parsed_result = engine.analyze_sentence(sentence)
            
            print(f"✅ パーシング成功")
            print(f"結果: {parsed_result}")
            
            # 結果の詳細分析
            analysis = analyze_parsing_result(sentence, parsed_result)
            
            results.append({
                'sentence': sentence,
                'complexity': complexity,
                'parsed_result': parsed_result,
                'analysis': analysis,
                'status': 'success'
            })
            success_count += 1
            
        except Exception as e:
            print(f"❌ パーシングエラー: {e}")
            print(f"エラー詳細: {traceback.format_exc()}")
            
            results.append({
                'sentence': sentence,
                'complexity': complexity,
                'error': str(e),
                'status': 'error'
            })
            error_count += 1
    
    # 結果サマリー
    print(f"\n📋 テスト結果サマリー")
    print(f"成功: {success_count}/{test_count} ({success_count/test_count*100:.1f}%)")
    print(f"エラー: {error_count}/{test_count} ({error_count/test_count*100:.1f}%)")
    
    # 詳細結果をJSONファイルに保存
    with open('comprehensive_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📄 詳細結果を comprehensive_test_results.json に保存しました")
    
    # 問題のある例文を特定
    print(f"\n🚨 問題のある例文の分析...")
    error_sentences = [r for r in results if r['status'] == 'error']
    
    if error_sentences:
        print(f"エラーが発生した例文:")
        for i, result in enumerate(error_sentences[:5]):  # 最大5個表示
            print(f"{i+1}. {result['sentence']}")
            print(f"   エラー: {result['error']}")
    
    return results

def analyze_parsing_result(sentence, parsed_result):
    """パーシング結果の詳細分析"""
    analysis = {
        'has_subject': False,
        'has_verb': False,
        'has_object': False,
        'has_modifiers': False,
        'slot_count': 0,
        'issues': []
    }
    
    if not parsed_result:
        analysis['issues'].append("パーシング結果が空")
        return analysis
    
    # スロットの存在確認
    for key, value in parsed_result.items():
        if key.startswith('S') and value:
            analysis['has_subject'] = True
        elif key.startswith('V') and value:
            analysis['has_verb'] = True
        elif key.startswith('O') and value:
            analysis['has_object'] = True
        elif key.startswith('M') and value:
            analysis['has_modifiers'] = True
        
        if value:
            analysis['slot_count'] += 1
    
    # 基本的な問題チェック
    if not analysis['has_subject']:
        analysis['issues'].append("主語が検出されていない")
    if not analysis['has_verb']:
        analysis['issues'].append("動詞が検出されていない")
    
    return analysis

if __name__ == "__main__":
    # 必要なライブラリの確認
    try:
        import pandas as pd
        print("✅ pandas ライブラリ確認完了")
    except ImportError:
        print("❌ pandas ライブラリがインストールされていません")
        print("インストールコマンド: pip install pandas openpyxl")
        sys.exit(1)
    
    # メインテスト実行
    test_parsing_engine_comprehensively()
