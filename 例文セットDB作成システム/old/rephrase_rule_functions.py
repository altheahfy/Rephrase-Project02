
def match_be_afraid_of(tokens, i):
    token = tokens[i]
    if token.text.lower() == "afraid" and token.head.lemma_ == "be":
        of_child = [c for c in token.children if c.text.lower() == "of"]
        if of_child:
            return f"{token.head.text} {token.text} {of_child[0].text}", i-1, i+1
    return None

def match_been_trying(tokens, i):
    token = tokens[i]
    if token.text.lower() == "trying" and i > 0 and tokens[i-1].lemma_ == "be":
        return f"{tokens[i-1].text} {token.text}", i-1, i
    return None

def match_relation_clause_subject(tokens, i):
    token = tokens[i]
    if token.dep_ == "nsubj" and token.head.dep_ == "relcl":
        head = token.head
        grand = head.head
        return f"{grand.text} {head.text}", i, i
    return None

def match_that_he_subject(tokens, i):
    token = tokens[i]
    if token.text.lower() == "he" and i > 0 and tokens[i-1].text.lower() == "that":
        return "that he", i-1, i
    return None

def match_to_avoid_tom(tokens, i):
    token = tokens[i]
    if token.text.lower() == "avoid" and i > 0 and tokens[i-1].text.lower() == "to":
        tom_child = [c for c in token.children if c.text.lower() == "tom"]
        if tom_child:
            return f"to {token.text} {tom_child[0].text}", i-1, i+1
        return f"to {token.text}", i-1, i
    return None

def match_hurting_her_feelings(tokens, i):
    token = tokens[i]
    if token.text.lower() == "hurting":
        children = [c.text for c in token.children if c.dep_ in ["dobj", "poss"]]
        if children:
            phrase = " ".join([token.text] + children)
            return phrase, i, i + len(children)
    return None
