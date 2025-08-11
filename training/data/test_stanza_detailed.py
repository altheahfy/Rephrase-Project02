import stanza

# Stanzaの基本分解能力を詳細テスト
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== Stanza基本分解能力の詳細テスト ===")
nlp = stanza.Pipeline('en', verbose=False)
doc = nlp(text)

for sent in doc.sentences:
    print(f"文: {sent.text}\n")
    
    # 全ての依存関係を表示
    print("🔍 全依存関係:")
    for word in sent.words:
        head_text = sent.words[word.head-1].text if word.head > 0 else 'ROOT'
        print(f"  {word.id:2d}: {word.text:<15} --{word.deprel:>15}--> {head_text:<15} ({word.upos})")
    
    print("\n" + "="*80)
    
    # ROOT動詞とその直接の子要素
    root_verb = None
    for word in sent.words:
        if word.deprel == 'root':
            root_verb = word
            break
    
    if root_verb:
        print(f"🎯 ROOT動詞: '{root_verb.text}' (位置: {root_verb.id})")
        
        print("\n📋 ROOT動詞の直接の子要素:")
        for word in sent.words:
            if word.head == root_verb.id:
                print(f"  {word.deprel:<12}: '{word.text}'")
        
        print("\n🔍 各主要要素の詳細:")
        
        # 主語の展開
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'nsubj':
                print(f"\n主語 '{word.text}' の子要素:")
                for child_word in sent.words:
                    if child_word.head == word.id:
                        print(f"  {child_word.deprel:<12}: '{child_word.text}'")
                        
                        # 関係節の中身
                        if child_word.deprel == 'relcl':
                            print(f"    関係節 '{child_word.text}' の子要素:")
                            for rel_child in sent.words:
                                if rel_child.head == child_word.id:
                                    print(f"      {rel_child.deprel:<12}: '{rel_child.text}'")
        
        # xcomp（補語動詞）の展開
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                print(f"\n補語動詞 '{word.text}' の子要素:")
                for child_word in sent.words:
                    if child_word.head == word.id:
                        print(f"  {child_word.deprel:<12}: '{child_word.text}'")
                        
                        # ccomp（補語節）の中身
                        if child_word.deprel == 'ccomp':
                            print(f"    補語節 '{child_word.text}' の子要素:")
                            for ccomp_child in sent.words:
                                if ccomp_child.head == child_word.id:
                                    print(f"      {ccomp_child.deprel:<12}: '{ccomp_child.text}'")
        
        print("\n" + "="*80)
        print("🎯 Stanza分解能力評価:")
        print("1. ROOT動詞の特定: できる")
        print("2. 主語の特定: できる") 
        print("3. 関係節の検出: できる")
        print("4. 補語動詞の検出: できる")
        print("5. 文頭修飾句: obl:unmarkedで部分的")
        print("6. 助動詞: auxで検出")
        print("7. 複雑な入れ子構造: 詳細な解析が可能")
        
    break
