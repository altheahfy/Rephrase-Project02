import stanza

# Stanzaで5文型レベルの文法解析
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== Stanza 5文型レベル解析 ===")
nlp = stanza.Pipeline('en', verbose=False)
doc = nlp(text)

for sent in doc.sentences:
    print(f"文: {sent.text[:100]}...")
    
    # ROOT動詞を見つける
    root_verb = None
    for word in sent.words:
        if word.deprel == 'root':
            root_verb = word
            break
    
    if root_verb:
        print(f"\n🎯 ROOT動詞: '{root_verb.text}'")
        
        # 主語（nsubj）
        subjects = [w for w in sent.words if w.deprel == 'nsubj' and w.head == root_verb.id]
        if subjects:
            print(f"📌 主語: '{subjects[0].text}'")
            
        # 直接目的語（obj）
        objects = [w for w in sent.words if w.deprel == 'obj' and w.head == root_verb.id]
        if objects:
            print(f"📌 目的語: '{objects[0].text}'")
            
        # 補語（xcomp, ccomp）
        complements = [w for w in sent.words if w.deprel in ['xcomp', 'ccomp'] and w.head == root_verb.id]
        if complements:
            print(f"📌 補語: '{complements[0].text}'")
            
        # 修飾語（obl, advmod）
        modifiers = [w for w in sent.words if w.deprel in ['obl:unmarked', 'obl', 'advmod'] and w.head == root_verb.id]
        for mod in modifiers:
            print(f"📌 修飾語: '{mod.text}' (type: {mod.deprel})")
    
    print("\n" + "="*50)
    print("📊 全依存関係:")
    for word in sent.words[:15]:  # 最初の15語
        head_text = sent.words[word.head-1].text if word.head > 0 else 'ROOT'
        print(f"  {word.text:<15} --{word.deprel:>12}--> {head_text}")
    
    break  # 最初の文のみ
