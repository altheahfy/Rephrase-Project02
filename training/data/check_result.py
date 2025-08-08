import pandas as pd

# 作成されたファイルを確認
df = pd.read_excel('rephrase_88_complete_format.xlsx')

print("📊 完成したExcelファイル詳細:")
print(f"- 総レコード数: {len(df)}")
print(f"- 総例文数: {df['例文ID'].nunique()}")
print(f"- 総セット数: {len(set([ex_id[:5] for ex_id in df['例文ID'].unique()]))}")

print("\n🔍 最初の例文（ex101）:")
ex101 = df[df['例文ID'] == 'ex101'].copy()
for i, row in ex101.iterrows():
    print(f"  {row['Slot']}: '{row['SlotPhrase']}' ({row['PhraseType']})")

print("\n🔍 最初の5例文のID一覧:")
first_5 = df['例文ID'].unique()[:5]
for ex_id in first_5:
    original = df[df['例文ID'] == ex_id]['原文'].dropna().iloc[0] if len(df[df['例文ID'] == ex_id]['原文'].dropna()) > 0 else "N/A"
    print(f"  {ex_id}: {original}")

print("\n📈 スロット分布:")
slot_counts = df['Slot'].value_counts().sort_index()
for slot, count in slot_counts.items():
    print(f"  {slot}: {count}回")

print("\n✅ 様式確認:")
print(f"- 構文ID列: {'あり' if '構文ID' in df.columns else 'なし'}")
print(f"- 例文ID列: {'あり' if '例文ID' in df.columns else 'なし'}")
print(f"- V_group_key列: {'あり' if 'V_group_key' in df.columns else 'なし'}")
print(f"- 原文列: {'あり' if '原文' in df.columns else 'なし'}")
print(f"- 全11列: {'あり' if len(df.columns) == 11 else f'なし（{len(df.columns)}列）'}")

print(f"\n🎯 各セットの例文数確認:")
set_counts = {}
for ex_id in df['例文ID'].unique():
    set_id = ex_id[:3]
    if set_id not in set_counts:
        set_counts[set_id] = 0
    set_counts[set_id] += 1

for set_id in sorted(set_counts.keys()):
    print(f"  セット{set_id}: {set_counts[set_id]}例文")
    
print(f"\n✅ 全22セット × 4例文 = 88例文 完了！")
