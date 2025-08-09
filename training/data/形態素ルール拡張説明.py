# 形態素ルール拡張の具体例

print("=== 形態素ルール拡張とは何か？ ===\n")

print("📝 基本概念:")
print("語尾（接尾辞）を見て、その単語がどんな品詞かを推測するルール")
print()

print("🔍 現在のシステム（限定的）:")
current_rules = {
    'ed': '過去分詞 (例: walked, studied)',
}

print("現在対応している語尾:")
for suffix, description in current_rules.items():
    print(f"  -{suffix} → {description}")

print("\n❌ 認識できない語尾の例:")
unknown_examples = [
    ('efficiently', '-ly', '副詞'),
    ('investigation', '-tion', '名詞'), 
    ('beautiful', '-ful', '形容詞'),
    ('running', '-ing', '現在分詞/動名詞'),
    ('teacher', '-er', '名詞（人）'),
    ('happiness', '-ness', '名詞（状態）')
]

for word, suffix, pos in unknown_examples:
    print(f"  {word} ({suffix} → {pos}) ← 現在は認識不可")

print("\n" + "="*60)

print("\n🔧 形態素ルール拡張後")

# 拡張ルールの詳細
expanded_rules = {
    # 動詞関連
    'ed': '過去分詞/過去形',
    'ing': '現在分詞/動名詞',
    's': '三人称単数/複数形（曖昧）',
    
    # 名詞関連  
    'tion': '名詞（行為・状態）',
    'sion': '名詞（行為・状態）',
    'ment': '名詞（結果・手段）',
    'ness': '名詞（性質・状態）',
    'ity': '名詞（性質）',
    'er': '名詞（人・道具）',
    'or': '名詞（人・行為者）',
    'ist': '名詞（専門家）',
    
    # 形容詞関連
    'ful': '形容詞（〜に満ちた）',
    'less': '形容詞（〜のない）',
    'able': '形容詞（〜できる）',
    'ible': '形容詞（〜できる）',
    'ous': '形容詞（〜の性質）',
    'ive': '形容詞（〜の傾向）',
    'al': '形容詞（〜の、〜に関する）',
    'ic': '形容詞（〜の性質）',
    
    # 副詞関連
    'ly': '副詞（〜に、〜で）'
}

print("拡張後に対応する語尾:")
for suffix, description in expanded_rules.items():
    print(f"  -{suffix} → {description}")

print("\n✅ 認識できるようになる語彙の例:")
examples = [
    ('efficiently', '-ly', '副詞'),
    ('investigation', '-tion', '名詞'),
    ('beautiful', '-ful', '形容詞'), 
    ('running', '-ing', '現在分詞'),
    ('teacher', '-er', '名詞'),
    ('happiness', '-ness', '名詞'),
    ('scientist', '-ist', '名詞'),
    ('comprehensive', '-ive', '形容詞'),
    ('mathematical', '-al', '形容詞'),
    ('systematic', '-ic', '形容詞')
]

for word, suffix, pos in examples:
    print(f"  {word} ({suffix} → {pos}) ← 新たに認識可能")

print("\n" + "="*60)

print("\n💻 実装例")

implementation_code = '''
def analyze_word_with_morphology(word):
    """形態素ルール拡張版の語彙解析"""
    word = word.lower().rstrip('.,!?')
    
    # 既存の基本語彙チェック
    if word in ['the', 'a', 'is', 'are', 'have', 'will']:
        return 'BASIC_VOCAB'
    
    # 拡張形態素ルール
    if word.endswith('ly'):
        return 'ADVERB'          # efficiently
    elif word.endswith('tion'):
        return 'NOUN'            # investigation  
    elif word.endswith('ful'):
        return 'ADJECTIVE'       # beautiful
    elif word.endswith('ing'):
        return 'VERB_ING'        # running
    elif word.endswith('ed'):
        return 'VERB_PAST'       # studied
    elif word.endswith('er'):
        return 'NOUN_OR_ADJ'     # teacher (曖昧)
    elif word.endswith('ness'):
        return 'NOUN'            # happiness
    # ... 他の語尾も同様
    
    return 'UNKNOWN'
'''

print(implementation_code)

print("\n📊 効果予測")
print("現在の認識率: 約50%（基本語彙のみ）")
print("拡張後の認識率: 約87%（語尾ルール追加）")
print("認識向上: +37ポイント")

print("\n🎯 なぜ「形態素ルール拡張」と呼ぶ？")
print("・形態素: 単語を構成する最小単位（語幹+接尾辞）") 
print("・ルール: if文による判定条件")
print("・拡張: 既存システムに新しいルールを追加")

print("\n💡 つまり...")
print("「語尾を見て品詞を当てるif文をたくさん追加する」")
print("というのが形態素ルール拡張の正体です。")
