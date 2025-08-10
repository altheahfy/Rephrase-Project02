import spacy
from step13_o1_subslot_new import O1SubslotGenerator

nlp = spacy.load("en_core_web_sm")
generator = O1SubslotGenerator()

# テストケース
test_sentences = ["give him a book", "giving him a book", "send her the letter"]

for sentence in test_sentences:
    print(f"\n=== '{sentence}' のspaCy解析結果 ===")
    doc = nlp(sentence)
    
    for token in doc:
        print(f"'{token.text}': pos={token.pos_}, dep={token.dep_}, head='{token.head.text}', lemma={token.lemma_}")
    
    print(f"\n--- O1O2検出テスト ---")
    o1o2_result = generator._detect_o1o2_structure(doc)
    print(f"O1O2検出結果: {o1o2_result}")
    
    print(f"\n--- 完全検出テスト ---")
    full_result = generator._detect_all_subslots(doc)
    print(f"完全検出結果: {full_result}")
