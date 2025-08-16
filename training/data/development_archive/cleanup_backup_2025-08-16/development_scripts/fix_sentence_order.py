#!/usr/bin/env python3
"""
expected_results_progress.jsonの例文順序を元の54例文順序に修正するスクリプト
"""

import json
import re
from pathlib import Path

def extract_sentences_from_md(md_file_path):
    """Markdownファイルから例文リストを抽出"""
    sentences = []
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 例文の番号と文を抽出（例: "1. The car is red."）
    pattern = r'^\d+\.\s+(.+)$'
    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            sentence = match.group(1).strip()
            sentences.append(sentence)
    
    return sentences

def fix_expected_results_order(expected_results_path, original_sentences):
    """expected_results_progress.jsonの例文順序を修正"""
    
    with open(expected_results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 修正カウンター
    corrected_count = 0
    
    # correct_answers セクションを確認
    if "correct_answers" not in data:
        print("エラー: 'correct_answers' セクションが見つかりません")
        return 0
    
    correct_answers = data["correct_answers"]
    
    # 各エントリの例文を元の順序に修正
    for i, original_sentence in enumerate(original_sentences, 1):
        entry_key = str(i)
        
        if entry_key in correct_answers:
            current_sentence = correct_answers[entry_key].get("sentence", "")
            
            # 例文が違う場合のみ修正
            if current_sentence != original_sentence:
                print(f"修正 {i}: '{current_sentence}' → '{original_sentence}'")
                correct_answers[entry_key]["sentence"] = original_sentence
                corrected_count += 1
            else:
                print(f"確認 {i}: '{original_sentence}' (変更なし)")
        else:
            print(f"警告: エントリ {i} が見つかりません")
    
    # ファイルを保存
    with open(expected_results_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n修正完了: {corrected_count}個の例文を修正しました")
    return corrected_count

def main():
    # ファイルパス設定
    base_dir = Path(__file__).parent
    original_md_path = base_dir / "original_54_sentences.md"
    expected_results_path = base_dir / "expected_results_progress.json"
    
    print("=== Expected Results Progress.json 例文順序修正ツール ===\n")
    
    # 元の例文順序を読み込み
    if not original_md_path.exists():
        print(f"エラー: {original_md_path} が見つかりません")
        return
    
    if not expected_results_path.exists():
        print(f"エラー: {expected_results_path} が見つかりません")
        return
    
    print(f"元の例文ファイル: {original_md_path}")
    print(f"修正対象ファイル: {expected_results_path}")
    
    # 元の例文リストを抽出
    original_sentences = extract_sentences_from_md(original_md_path)
    print(f"\n元の例文数: {len(original_sentences)}例文")
    
    if len(original_sentences) == 0:
        print("エラー: 元の例文が見つかりませんでした")
        return
    
    # 最初の5例文を確認表示
    print("\n最初の5例文:")
    for i, sentence in enumerate(original_sentences[:5], 1):
        print(f"  {i}. {sentence}")
    
    # 修正実行の確認
    response = input(f"\n{len(original_sentences)}例文の順序修正を実行しますか？ (y/N): ")
    if response.lower() != 'y':
        print("修正をキャンセルしました")
        return
    
    # 修正実行
    corrected_count = fix_expected_results_order(expected_results_path, original_sentences)
    
    print(f"\n✅ 修正が完了しました。{corrected_count}個の例文を修正しました。")

if __name__ == "__main__":
    main()
