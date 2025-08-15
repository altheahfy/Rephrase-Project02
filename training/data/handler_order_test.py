from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

# 実行順序の詳細確認
mapper = UnifiedStanzaRephraseMapper()

print('=== ハンドラー実行順序テスト ===')
print('1. 5文型エンジンのみ')
mapper.add_handler('basic_five_pattern')
result1 = mapper.process('The book which lies there is mine.')
print(f'  結果: {len(result1.get("slots", {}))} slots - {list(result1.get("slots", {}).keys())}')

print('2. 関係節エンジン追加（順序重要）')
mapper.add_handler('relative_clause')
result2 = mapper.process('The book which lies there is mine.')
print(f'  結果: {len(result2.get("slots", {}))} slots - {list(result2.get("slots", {}).keys())}')

print()
print('アクティブハンドラー順序:', mapper.active_handlers)

# 詳細比較
print()
print('=== 詳細比較 ===')
print('5文型エンジンのみ:')
for k, v in result1.get('slots', {}).items():
    print(f'  {k}: {v}')

print('関係節+5文型:')
for k, v in result2.get('slots', {}).items():
    print(f'  {k}: {v}')
