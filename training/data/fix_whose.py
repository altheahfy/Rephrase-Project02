import re

with open('unified_stanza_rephrase_mapper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 現在の主動詞チェックを特定
old_pattern = r'(\s*)(.*主動詞直接修飾チェック.*?\n)'

# whose構文判定 + 修正された主動詞チェック
new_code = r'''\1# 🔧 Whose構文位置ベース判定（Stanza誤解析対策）- 最優先
\1sentence_text = " ".join([w.text for w in sentence.words])
\1if "whose" in sentence_text:
\1    whose_pos = -1
\1    main_verb_pos = -1
\1    adverb_pos = adverb_word.id
\1    
\1    for word in sentence.words:
\1        if word.text.lower() == "whose":
\1            whose_pos = word.id
\1        elif word.id == main_verb_id:
\1            main_verb_pos = word.id
\1    
\1    # whose節内（whose〜主動詞前）の副詞は従属節
\1    if whose_pos > 0 and main_verb_pos > 0:
\1        if whose_pos < adverb_pos < main_verb_pos:
\1            print(f"   → WHOSE構文位置判定: SUBORDINATE (whose:{whose_pos} less_than adverb:{adverb_pos} less_than main:{main_verb_pos})")
\1            return 'subordinate'
\1        elif adverb_pos > main_verb_pos:
\1            print(f"   → WHOSE構文位置判定: MAIN (adverb:{adverb_pos} greater_than main:{main_verb_pos})")
\1            return 'main'
\1
\1# 🔧 主動詞直接修飾チェック（whose構文判定後）
'''

content = re.sub(old_pattern, new_code, content)

with open('unified_stanza_rephrase_mapper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("whose構文判定を最優先に移動しました")
