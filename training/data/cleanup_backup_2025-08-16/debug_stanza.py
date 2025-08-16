#!/usr/bin/env python3

import stanza

# Stanza pipeline初期化
nlp = stanza.Pipeline('en', verbose=False, use_gpu=False)

# テスト文
sentence = "The woman is my neighbor."
doc = nlp(sentence)

print(f"文: {sentence}")
print("Stanza解析結果:")
print("-" * 50)

for sent in doc.sentences:
    for word in sent.words:
        print(f"ID:{word.id:2} | {word.text:12} | {word.deprel:12} | HEAD:{word.head}")
        
print("\n" + "="*50)

# neighborの修飾語を探す
sent = doc.sentences[0]
neighbor_word = None
for word in sent.words:
    if word.text == "neighbor":
        neighbor_word = word
        break

if neighbor_word:
    print(f"neighbor (ID:{neighbor_word.id}) の修飾語:")
    for word in sent.words:
        if word.head == neighbor_word.id:
            print(f"  - {word.text} ({word.deprel})")
else:
    print("neighborが見つかりません")
