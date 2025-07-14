import json

# 複数のバックアップファイルでwhatグループのdidとwhereを確認
backup_files = [
    r"c:\Users\yurit\Downloads\Rephraseプロジェクト進捗ファイル20250529\完全トレーニングUI完成フェーズ３\project-root\backup\プロジェクトフォルダ全体\「後はイラスト表示機能の実装だけ」の状態を達成202507051003Rephrase-Project\slot_order_data.json",
    r"c:\Users\yurit\Downloads\Rephraseプロジェクト進捗ファイル20250529\完全トレーニングUI完成フェーズ３\project-root\old\GitHubで戻せなくなった202506231530Rephrase-Project\slot_order_data.json"
]

for file_path in backup_files:
    try:
        folder_name = file_path.split('\\')[-2]
        print(f"\n=== {folder_name} ===")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        found = []
        for entry in data:
            if entry.get('V_group_key') == 'what' and entry.get('SlotPhrase') in ['did', 'Where']:
                found.append(f"Phrase: {entry.get('SlotPhrase')}, Order: {entry.get('Slot_display_order')}")
        
        if found:
            for item in found[:2]:  # 最初の2つだけ表示
                print(item)
        else:
            print("whatグループのdidとwhereが見つからない")
    except Exception as e:
        print(f"エラー: {e}")
