
def map_to_rephrase_slots(doc):
    result = []
    added = set()
    print(f"DEBUG: Mapping spaCy doc to Rephrase slots")
    tokens = list(doc)

    for i, token in enumerate(tokens):
        print(f"DEBUG: token='{token.text}', dep_='{token.dep_}', pos_='{token.pos_}', head='{token.head.text}'")

        # ① the woman who seemed indecisive
        if token.text.lower() in ["who", "that"] and token.head.pos_ == "NOUN":
            phrase = f"{token.head.text} {token.text}"
            if phrase not in added:
                result.append(("sub-s", phrase))
                added.add(phrase)

        # ② it as sub-s
        if token.text.lower() == "it" and token.dep_ == "nsubj":
            result.append(("sub-s", token.text))

        # ③ although + first adv
        if token.text.lower() == "although":
            result.append(("sub-m1", token.text))
        if token.pos_ == "ADV" and "sub-m1" in [r[0] for r in result]:
            result.append(("sub-m2", token.text))

        # ④ be動詞 + 補語
        if token.head.lemma_ == "be" and token.dep_ in ["acomp", "attr"]:
            result.append(("sub-c1", token.text))

        # ⑤ that he sub-s
        if token.text.lower() == "that":
            next_nsubj = [t for t in token.subtree if t.dep_ == "nsubj"]
            for nsubj in next_nsubj:
                phrase = f"{token.text} {nsubj.text}"
                if phrase not in added:
                    result.append(("sub-s", phrase))
                    added.add(phrase)

        # ⑥ had aux
        if token.text.lower() == "had" and token.dep_ == "aux":
            result.append(("sub-aux", token.text))

        # ⑦ been trying as sub-v
        if token.text.lower() == "trying" and token.head.text.lower() == "been":
            phrase = f"{token.head.text} {token.text}"
            result.append(("sub-v", phrase))

        # ⑧ to avoid Tom as sub-o1
        if token.dep_ == "xcomp" and token.head.lemma_ == "try":
            objs = [child.text for child in token.children if child.dep_ in ["dobj", "pobj"]]
            phrase = f"to {token.text} {' '.join(objs)}"
            result.append(("sub-o1", phrase.strip()))

        # ⑨ because he sub-s
        if token.dep_ == "nsubj" and any(p.text.lower() == "because" for p in token.ancestors):
            result.append(("sub-s", token.text))

        # ⑪ hurting her feelings as sub-o1
        if token.dep_ == "pcomp" and token.pos_ == "VERB":
            objs = [child.text for child in token.children if child.dep_ in ["dobj", "poss"]]
            phrase = f"{token.text} {' '.join(objs)}"
            if phrase not in added:
                result.append(("sub-o1", phrase.strip()))
                added.add(phrase)

    return result
