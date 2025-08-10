#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import json

# エンジンを初期化
engine = CompleteRephraseParsingEngine()

# 実際の例文入力元を読み込み
try:
    # 複数のExcelファイルを確認
    excel_files = [
        "例文入力元_分解結果_v2.xlsx",
        "（小文字化した最初の5文型フルセット）例文入力元.xlsx", 
        "例文入力元.xlsx"
    ]
    
    sentences_to_test = []
    
    for file_name in excel_files:
        try:
            df = pd.read_excel(file_name)
            print(f"✅ {file_name} 読み込み成功: {len(df)} 行")
            
            # '原文'列から例文を抽出
            if '原文' in df.columns:
                # 原文列からユニーク例文を取得
                sentences = df['原文'].dropna().astype(str).unique()
                sentences = [s.strip() for s in sentences if s.strip()]
                # 最初の10文を取得してテスト
                test_sentences = sentences[:10]
                sentences_to_test.extend([(file_name, s) for s in test_sentences])
                print(f"  → '原文'列から{len(test_sentences)}文を取得")
            else:
                print(f"  → '原文'列が見つかりませんでした: {list(df.columns)}")
                
        except Exception as e:
            print(f"❌ {file_name} 読み込み失敗: {e}")
    
    print(f"\n📊 総検証対象: {len(sentences_to_test)} 文")
    
    # 問題検出・分析
    issues = []
    
    for file_name, sentence in sentences_to_test[:5]:  # 最初の5文をテスト
        print(f"\n🔍 検証中: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # 問題検出
            sentence_issues = []
            
            # 1. Missing elements check
            main_slots = result.get('main_slots', {})
            for slot_name in ['S', 'V']:  # 必須要素
                if not main_slots.get(slot_name):
                    sentence_issues.append(f"Missing {slot_name}")
            
            # 2. Order value check  
            for slot_name, items in main_slots.items():
                for item in items:
                    if item and 'order' not in item:
                        sentence_issues.append(f"{slot_name} missing order")
                    elif item and item.get('order') == 99:
                        sentence_issues.append(f"{slot_name} has order=99")
            
            # 3. Value format check
            for slot_name, items in main_slots.items():
                for item in items:
                    if item and '_M3_' in str(item.get('value', '')):
                        sentence_issues.append(f"{slot_name} has formatted value instead of raw text")
            
            if sentence_issues:
                issues.append({
                    'file': file_name,
                    'sentence': sentence,
                    'issues': sentence_issues
                })
            else:
                print("  ✅ 問題なし")
                
        except Exception as e:
            issues.append({
                'file': file_name,
                'sentence': sentence,  
                'issues': [f"Processing error: {e}"]
            })
    
    # 問題要約
    if issues:
        print(f"\n🚨 検出された問題: {len(issues)} 文")
        for i, issue in enumerate(issues):
            print(f"  {i+1}. {issue['sentence'][:50]}...")
            for prob in issue['issues']:
                print(f"     - {prob}")
    else:
        print(f"\n✅ 全文で問題は検出されませんでした")
        
except Exception as e:
    print(f"❌ 初期化エラー: {e}")
