#!/usr/bin/env python3
"""
final_54_test_data.jsonの期待値を現在のシステム出力に合わせて修正
_parent_slotフィールドを追加する
"""

import json
from pathlib import Path

def update_test_expectations():
    """テスト期待値を現在のシステム出力形式に合わせて更新"""
    
    # ファイルパス
    test_file = Path("final_test_system/final_54_test_data.json")
    backup_file = Path("final_test_system/final_54_test_data_backup.json")
    
    print(f"📝 期待値更新開始: {test_file}")
    
    # バックアップ作成
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 バックアップ作成: {backup_file}")
        
        # 更新カウント
        updated_count = 0
        
        # 各テストケースを確認・更新
        for test_id, test_case in data["data"].items():
            if "sub_slots" in test_case["expected"] and test_case["expected"]["sub_slots"]:
                # sub_slotsが空でない場合、_parent_slotを追加
                sub_slots = test_case["expected"]["sub_slots"]
                
                # 主語関係節なら_parent_slot: "S"を追加
                if not "_parent_slot" in sub_slots:
                    # 主語位置の関係節かどうかを判定
                    main_slots = test_case["expected"]["main_slots"]
                    if main_slots.get("S") == "":  # 空の主語 = 関係節が主語位置
                        sub_slots["_parent_slot"] = "S"
                        updated_count += 1
                        print(f"✅ 更新: テスト{test_id} - {test_case['sentence']}")
        
        # 更新されたデータを保存
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"🎯 更新完了: {updated_count}件のテストケースを更新")
        print(f"📁 更新済みファイル: {test_file}")
        
        return updated_count
    else:
        print(f"❌ エラー: {test_file} が見つかりません")
        return 0

if __name__ == "__main__":
    update_test_expectations()
