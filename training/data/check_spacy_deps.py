import spacy

# spaCyの全依存関係ラベルを確認
nlp = spacy.load("en_core_web_sm")

print('🔍 spaCy全依存関係ラベル一覧')
print('=' * 80)

# 依存関係ラベルの一覧を取得
dep_labels = list(nlp.get_pipe('parser').labels)
print(f'📊 総依存関係ラベル数: {len(dep_labels)}')
print()

print('📋 全依存関係ラベル:')
for i, label in enumerate(sorted(dep_labels)):
    print(f'{i+1:2d}. {label}')

print('\n🎯 Step15で使用されている依存関係を確認する必要があります')
print('Step15のコードを読み込んで、実際に使用されているdep_ラベルを抽出し、')
print('上記の全ラベルと比較して100%カバレッジを検証します。')
