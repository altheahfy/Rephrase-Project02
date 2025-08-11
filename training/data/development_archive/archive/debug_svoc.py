import spacy
from step13_o1_subslot_new import O1SubslotGenerator

nlp = spacy.load("en_core_web_sm")

# 第5文型テストケース
fifth_pattern_cases = [
    "I saw her cry",
    "I found it interesting", 
    "They made him happy",
    "She kept the door open",
    "We consider it important"
]

print("=== 第5文型（SVOC）spaCy解析結果 ===\n")

for sentence in fifth_pattern_cases:
    print(f"'{sentence}':")
    doc = nlp(sentence)
    
    for token in doc:
        print(f"  '{token.text}': pos={token.pos_}, dep={token.dep_}, head='{token.head.text}'")
    
    print(f"  依存関係構造:")
    for token in doc:
        if token.dep_ in ["nsubj", "dobj", "xcomp", "ccomp", "acomp", "attr"]:
            print(f"    {token.dep_}: '{token.text}' -> '{token.head.text}'")
    print()
