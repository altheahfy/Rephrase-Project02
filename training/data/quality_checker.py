#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品質チェックスクリプト - スモールステップで各観点をチェック
"""

import pandas as pd
import re
from pathlib import Path

def load_excel_data():
    """最新のExcelファイルを読み込み"""
    excel_files = list(Path('.').glob('例文入力元_分解結果_v2_*.xlsx'))
    if not excel_files:
        print("❌ 分解結果Excelファイルが見つかりません")
        return None
    
    latest_file = max(excel_files, key=lambda x: x.stat().st_mtime)
    print(f"📊 読み込み中: {latest_file}")
    
    try:
        df = pd.read_excel(latest_file)
        print(f"✅ 読み込み完了: {len(df)}行")
        return df, latest_file
    except Exception as e:
        print(f"❌ 読み込みエラー: {e}")
        return None

def check_aux_order(df):
    """チェック1: 完了形のhave、can'tなどのAuxのorderは正しいか"""
    print("\n=== チェック1: Auxのorder検証 ===")
    
    # Auxスロットを持つ行を抽出（実際のカラム名を使用）
    aux_rows = df[df['Slot'] == 'Aux'].copy()
    print(f"🔍 Aux要素数: {len(aux_rows)}件")
    
    issues = []
    
    for idx, row in aux_rows.iterrows():
        sentence = row['原文']
        slot_content = row['SlotPhrase']
        order = row['Slot_display_order']
        
        # have/haven't の完了形チェック
        if slot_content in ['have', "haven't", 'has', "hasn't", 'had', "hadn't"]:
            # 完了形の場合、通常order=3が期待される
            if order != 3:
                issues.append({
                    'type': 'aux_order_issue',
                    'sentence': sentence,
                    'slot_content': slot_content,
                    'current_order': order,
                    'expected_order': 3,
                    'reason': '完了形auxは通常order=3'
                })
        
        # can/can't チェック
        elif slot_content in ['can', "can't", 'could', "couldn't"]:
            if order != 3:
                issues.append({
                    'type': 'aux_order_issue',
                    'sentence': sentence,
                    'slot_content': slot_content,
                    'current_order': order,
                    'expected_order': 3,
                    'reason': '助動詞can/couldは通常order=3'
                })
        
        # will/won't チェック
        elif slot_content in ['will', "won't", 'would', "wouldn't"]:
            if order != 3:
                issues.append({
                    'type': 'aux_order_issue',
                    'sentence': sentence,
                    'slot_content': slot_content,
                    'current_order': order,
                    'expected_order': 3,
                    'reason': '助動詞will/wouldは通常order=3'
                })
    
    if issues:
        print(f"⚠️ 発見された問題: {len(issues)}件")
        for issue in issues[:5]:  # 最初の5件を表示
            print(f"  - {issue['sentence']}")
            print(f"    {issue['slot_content']} (order={issue['current_order']}) → 期待order={issue['expected_order']}")
            print(f"    理由: {issue['reason']}")
    else:
        print("✅ Auxのorder問題なし")
    
    return issues

def check_cant_contraction(df):
    """チェック2: can'tを正しく「can't」でスロットに入れているか"""
    print("\n=== チェック2: can't短縮形の検証 ===")
    
    issues = []
    
    # can't, couldn't, won't, wouldn't, haven't, hasn't, hadn't をチェック
    contractions = ["can't", "couldn't", "won't", "wouldn't", "haven't", "hasn't", "hadn't", "isn't", "aren't", "wasn't", "weren't"]
    
    for idx, row in df.iterrows():
        sentence = row['原文']
        slot_content = row['SlotPhrase']
        
        # NaN値をスキップ
        if pd.isna(sentence) or pd.isna(slot_content):
            continue
            
        # 元の文に短縮形が含まれている場合
        for contraction in contractions:
            if contraction in sentence.lower():
                # スロット内容が勝手に展開されていないかチェック
                if slot_content == 'can not' and contraction == "can't":
                    issues.append({
                        'type': 'contraction_expanded',
                        'sentence': sentence,
                        'slot_content': slot_content,
                        'expected': "can't",
                        'reason': '短縮形を勝手に展開している'
                    })
                elif slot_content == 'could not' and contraction == "couldn't":
                    issues.append({
                        'type': 'contraction_expanded',
                        'sentence': sentence,
                        'slot_content': slot_content,
                        'expected': "couldn't",
                        'reason': '短縮形を勝手に展開している'
                    })
                elif slot_content == 'will not' and contraction == "won't":
                    issues.append({
                        'type': 'contraction_expanded',
                        'sentence': sentence,
                        'slot_content': slot_content,
                        'expected': "won't",
                        'reason': '短縮形を勝手に展開している'
                    })
    
    if issues:
        print(f"⚠️ 短縮形の問題: {len(issues)}件")
        for issue in issues:
            print(f"  - {issue['sentence']}")
            print(f"    '{issue['slot_content']}' → 期待: '{issue['expected']}'")
            print(f"    理由: {issue['reason']}")
    else:
        print("✅ 短縮形の処理問題なし")
    
    return issues

def check_possessive_pronouns(df):
    """チェック3: his, her, their等の所有格代名詞が抜けていないか"""
    print("\n=== チェック3: 所有格代名詞の検証 ===")
    
    issues = []
    possessives = ["his", "her", "their", "our", "my", "your", "its"]
    
    for idx, row in df.iterrows():
        sentence = row['原文']
        
        if pd.isna(sentence):
            continue
            
        sentence_lower = sentence.lower()
        
        # 原文に所有格代名詞が含まれている場合
        for possessive in possessives:
            if f" {possessive} " in f" {sentence_lower} ":  # 単語境界を考慮
                # その文に対応するスロット内容をチェック
                sentence_slots = df[df['原文'] == sentence]['SlotPhrase'].tolist()
                slot_text_combined = ' '.join([str(slot) for slot in sentence_slots if not pd.isna(slot)])
                
                if possessive not in slot_text_combined.lower():
                    issues.append({
                        'type': 'missing_possessive',
                        'sentence': sentence,
                        'missing_word': possessive,
                        'slots_content': slot_text_combined,
                        'reason': f'所有格代名詞"{possessive}"が抜けている'
                    })
                    break  # 同じ文で複数回カウントしないように
    
    if issues:
        print(f"⚠️ 所有格代名詞の問題: {len(issues)}件")
        for issue in issues[:5]:  # 最初の5件を表示
            print(f"  - {issue['sentence']}")
            print(f"    欠落: '{issue['missing_word']}'")
            print(f"    スロット内容: {issue['slots_content']}")
            print(f"    理由: {issue['reason']}")
    else:
        print("✅ 所有格代名詞の問題なし")
    
    return issues

def check_articles(df):
    """チェック4: 冠詞(a, an, the)が抜けていないか"""
    print("\n=== チェック4: 冠詞の検証 ===")
    
    issues = []
    articles = ["a", "an", "the"]
    
    for idx, row in df.iterrows():
        sentence = row['原文']
        
        if pd.isna(sentence):
            continue
            
        sentence_lower = sentence.lower()
        
        # 原文に冠詞が含まれている場合
        for article in articles:
            if f" {article} " in f" {sentence_lower} ":  # 単語境界を考慮
                # その文に対応するスロット内容をチェック
                sentence_slots = df[df['原文'] == sentence]['SlotPhrase'].tolist()
                slot_text_combined = ' '.join([str(slot) for slot in sentence_slots if not pd.isna(slot)])
                
                if article not in slot_text_combined.lower():
                    issues.append({
                        'type': 'missing_article',
                        'sentence': sentence,
                        'missing_word': article,
                        'slots_content': slot_text_combined,
                        'reason': f'冠詞"{article}"が抜けている'
                    })
                    break  # 同じ文で複数回カウントしないように
    
    if issues:
        print(f"⚠️ 冠詞の問題: {len(issues)}件")
        for issue in issues[:5]:  # 最初の5件を表示
            print(f"  - {issue['sentence']}")
            print(f"    欠落: '{issue['missing_word']}'")
            print(f"    スロット内容: {issue['slots_content']}")
            print(f"    理由: {issue['reason']}")
    else:
        print("✅ 冠詞の問題なし")
    
    return issues

if __name__ == "__main__":
    data = load_excel_data()
    if data is None:
        exit(1)
    
    df, filename = data
    print(f"📋 カラム: {list(df.columns)}")
    
    # チェック1: Auxのorder
    aux_issues = check_aux_order(df)
    
    # チェック2: 短縮形
    contraction_issues = check_cant_contraction(df)
    
    # チェック3: 所有格代名詞
    possessive_issues = check_possessive_pronouns(df)
    
    # チェック4: 冠詞
    article_issues = check_articles(df)
    
    print(f"\n📊 チェック1完了: Aux order問題={len(aux_issues)}件")
    print(f"📊 チェック2完了: 短縮形問題={len(contraction_issues)}件")
    print(f"📊 チェック3完了: 所有格代名詞問題={len(possessive_issues)}件")
    print(f"📊 チェック4完了: 冠詞問題={len(article_issues)}件")
