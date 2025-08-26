#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess

def get_git_data(commit_hash):
    """Gitコミットからデータを取得"""
    result = subprocess.run(['git', 'show', f'{commit_hash}:training/data/expected_results_progress.json'], 
                           capture_output=True, text=True, encoding='utf-8')
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def fix_data_alignment():
    """例文とチェック結果の対応を正しく修正"""
    
    # 元のデータ（4ハンドラー変更前、1-31まで）
    old_data = get_git_data('8633cbd2')
    
    # 新しいデータ（4ハンドラー変更後、35-54まで）
    new_data = get_git_data('3f0fe8d9')
    
    if not old_data or not new_data:
        print("エラー: コミットからデータを取得できませんでした")
        return
    
    # 統合データを作成
    fixed_data = {
        "meta": {
            "last_updated": "2025-08-16T18:00:00.000000",
            "current_sentence": 54,
            "total_sentences": 54,
            "completion_status": "completed",
            "session_notes": ["データ整合性修正: 例文とチェック結果の対応を復元"]
        }
    }
    
    # 1-31: 元のデータ（チェック済み）
    for i in range(1, 32):
        if str(i) in old_data:
            fixed_data[str(i)] = old_data[str(i)]
    
    # 32-34: 空のスロット
    for i in range(32, 35):
        fixed_data[str(i)] = {
            "sentence": f"[未設定 {i}]",
            "expected_result": {},
            "notes": "未実装ハンドラーのため空"
        }
    
    # 35-54: 新しいデータ（4ハンドラー対応、チェック済み）
    for i in range(35, 55):
        if str(i) in new_data:
            fixed_data[str(i)] = new_data[str(i)]
    
    # ファイルに保存
    with open('expected_results_progress.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print("データ整合性修正完了!")
    print("- 1-31: 元の例文 + チェック結果")
    print("- 32-34: 空のスロット")
    print("- 35-54: 新しい例文 + チェック結果")
    
    # 確認
    completed = sum(1 for k, v in fixed_data.items() if k.isdigit() and 'user_judgment' in v)
    print(f"チェック完了数: {completed}")

if __name__ == "__main__":
    fix_data_alignment()
