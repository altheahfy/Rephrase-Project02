import sys
sys.path.append('.')
from step18_unified_rephrase_system import Step18UnifiedRephraseSystem

# システム初期化
system = Step18UnifiedRephraseSystem()

# 前置詞統合テスト
phrase = 'the manager who had recently taken charge of the project'
print(f"=== 前置詞統合テスト ===")
print(f"テスト句: '{phrase}'")
print("=" * 50)

result = system._extract_slot_phrases(phrase)

print('\n=== 統合処理結果 ===')
for subslot, value in result.items():
    if value:
        print(f'{subslot:10}: "{value}"')

print("\n=== sub-m3の有無確認 ===")
if result.get('sub-m3'):
    print(f"❌ sub-m3が残存: '{result['sub-m3']}'")
else:
    print("✅ sub-m3が正常に除外されました")
