#!/usr/bin/env python3
"""
例文ID修正スクリプト
空の例文IDを直前の有効な例文IDで補完する
"""

import json
import sys

def fix_example_ids(filename):
    """例文IDの空欄を修正"""
    
    print(f"📂 {filename} を読み込み中...")
    
    # JSONファイル読み込み
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return False
    
    print(f"📊 総レコード数: {len(data)}")
    
    # 現在の例文IDを追跡
    current_example_id = ""
    fixed_count = 0
    
    # 各レコードを処理
    for i, record in enumerate(data):
        if record.get("例文ID"):
            # 例文IDが設定されている場合、現在のIDを更新
            current_example_id = record["例文ID"]
            print(f"🔄 例文ID更新: {current_example_id} (行 {i+1})")
        elif current_example_id and record.get("例文ID") == "":
            # 例文IDが空で、現在のIDがある場合は補完
            record["例文ID"] = current_example_id
            fixed_count += 1
            if fixed_count <= 10:  # 最初の10件だけログ出力
                print(f"✅ 修正: 行 {i+1}, スロット '{record.get('Slot', 'N/A')}' → {current_example_id}")
            elif fixed_count == 11:
                print("  ... (以降の修正は省略表示)")
    
    print(f"\n📈 修正統計:")
    print(f"  修正したレコード数: {fixed_count}")
    print(f"  総レコード数: {len(data)}")
    print(f"  修正率: {fixed_count/len(data)*100:.1f}%")
    
    # バックアップファイル作成
    backup_filename = filename.replace('.json', '_backup.json')
    try:
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 バックアップ作成: {backup_filename}")
    except Exception as e:
        print(f"⚠️ バックアップ作成失敗: {e}")
    
    # 修正済みファイルを保存
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 修正済みファイル保存完了: {filename}")
        return True
    except Exception as e:
        print(f"❌ ファイル保存エラー: {e}")
        return False

def verify_fix(filename):
    """修正結果の検証"""
    
    print(f"\n🔍 修正結果検証中...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 検証用ファイル読み込みエラー: {e}")
        return False
    
    empty_ids = 0
    example_ids = set()
    
    for record in data:
        example_id = record.get("例文ID", "")
        if example_id == "":
            empty_ids += 1
        else:
            example_ids.add(example_id)
    
    print(f"📊 検証結果:")
    print(f"  空の例文ID: {empty_ids}件")
    print(f"  ユニークな例文ID数: {len(example_ids)}")
    print(f"  例文ID一覧: {sorted(list(example_ids))}")
    
    if empty_ids == 0:
        print("🎉 すべての例文IDが正常に設定されました！")
        return True
    else:
        print(f"⚠️ まだ {empty_ids}件の空の例文IDがあります")
        return False

if __name__ == "__main__":
    filename = "slot_order_data_第4文型と極性.json"
    
    print("🔧 例文ID修正スクリプト開始")
    print("=" * 50)
    
    # 修正実行
    if fix_example_ids(filename):
        # 検証実行
        verify_fix(filename)
        print("\n🎯 修正完了！UIで動作確認してください。")
    else:
        print("\n❌ 修正に失敗しました")
    
    print("=" * 50)
