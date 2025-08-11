try:
    import stanza
    print('✅ Stanza available')
except ImportError:
    print('❌ Stanza not available')

try:
    import allennlp
    print('✅ AllenNLP available')  
except ImportError:
    print('❌ AllenNLP not available')

print('\n=== 現在利用可能な選択肢 ===')
print('1. spaCy + 文法ルールエンジン（自作）')
print('2. Stanza/CoreNLP（要インストール）') 
print('3. AllenNLP SRL（要インストール）')
print('4. spaCy + 文型パターンマッチング（推奨）')

print('\n=== 推奨アプローチ ===')
print('spaCyの詳細な依存関係情報 + 5文型パターンルール')
print('→ 軽量かつ効果的な解決策')
