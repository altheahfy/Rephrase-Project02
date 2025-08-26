#!/usr/bin/env python3
"""
custom_test.pyの例文順序を元の54例文順序に修正するスクリプト
"""

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

def fix_custom_test_sentences(test_file_path, original_sentences):
    """custom_test.pyの例文リストを修正"""
    
    with open(test_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # your_test_sentences配列の開始と終了を見つける
    start_pattern = r'your_test_sentences\s*=\s*\['
    end_pattern = r'\]'
    
    # 例文リスト作成（引用符とカンマ付き）
    sentence_lines = []
    for sentence in original_sentences:
        sentence_lines.append(f'        "{sentence}",')
    
    # 最後の要素からカンマを除去
    if sentence_lines:
        sentence_lines[-1] = sentence_lines[-1].rstrip(',')
    
    # 新しい例文リスト
    new_sentences_block = '\n'.join(sentence_lines)
    
    # 正規表現でyour_test_sentences配列全体を置換
    sentences_array_pattern = r'(your_test_sentences\s*=\s*\[)(.*?)(\s+\])'
    replacement = f'\\1\n{new_sentences_block}\n\\3'
    
    # 置換実行
    new_content = re.sub(sentences_array_pattern, replacement, content, flags=re.DOTALL)
    
    # ファイルに保存
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ custom_test.pyの例文を54例文の正しい順序に修正しました")
    print(f"   最初の5例文:")
    for i, sentence in enumerate(original_sentences[:5], 1):
        print(f"     {i}. {sentence}")

def main():
    # ファイルパス設定
    base_dir = Path(__file__).parent
    original_md_path = base_dir / "original_54_sentences.md"
    custom_test_path = base_dir / "custom_test.py"
    
    print("=== Custom Test.py 例文順序修正ツール ===\n")
    
    # 元の例文順序を読み込み
    if not original_md_path.exists():
        print(f"エラー: {original_md_path} が見つかりません")
        return
    
    if not custom_test_path.exists():
        print(f"エラー: {custom_test_path} が見つかりません")
        return
    
    print(f"元の例文ファイル: {original_md_path}")
    print(f"修正対象ファイル: {custom_test_path}")
    
    # 元の例文リストを抽出
    original_sentences = extract_sentences_from_md(original_md_path)
    print(f"\n元の例文数: {len(original_sentences)}例文")
    
    if len(original_sentences) == 0:
        print("エラー: 元の例文が見つかりませんでした")
        return
    
    # 修正実行の確認
    response = input(f"\ncustom_test.pyの例文を{len(original_sentences)}例文の正しい順序に修正しますか？ (y/N): ")
    if response.lower() != 'y':
        print("修正をキャンセルしました")
        return
    
    # 修正実行
    fix_custom_test_sentences(custom_test_path, original_sentences)
    
    print("\n✅ 修正が完了しました。")

if __name__ == "__main__":
    main()
