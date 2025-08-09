import pandas as pd

# Excel読み込みテスト
df = pd.read_excel('例文入力元.xlsx')
print(f'Excel読み込み成功: {len(df)}行')
print(f'カラム: {list(df.columns)}')

print('\n=== 原文カラム内容確認 ===')
unique_sentences = df['原文'].dropna().unique()
print(f'ユニーク原文数: {len(unique_sentences)}')

print('\n最初の5つの原文:')
for i, sentence in enumerate(unique_sentences[:5]):
    print(f'{i+1}. "{sentence}"')

print('\n=== データ型確認 ===')
print(f'原文カラムのデータ型: {df["原文"].dtype}')
print(f'NaN値の数: {df["原文"].isna().sum()}')
print(f'空文字列の数: {(df["原文"] == "").sum()}')
