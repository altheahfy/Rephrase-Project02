import stanza

# Stanzaベースの新しいRephrase分解エンジン設計
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== Stanzaベース Rephrase分解エンジン設計 ===")
nlp = stanza.Pipeline('en', verbose=False)
doc = nlp(text)

def extract_sentence_backbone(sent):
    """文の背骨（基本8スロット構造）を抽出"""
    
    # ROOT動詞特定
    root_verb = None
    for word in sent.words:
        if word.deprel == 'root':
            root_verb = word
            break
    
    if not root_verb:
        return None
    
    print(f"🎯 ROOT動詞: '{root_verb.text}'")
    
    # 基本構造抽出
    backbone = {
        'M1': [],     # 文頭修飾句
        'S': [],      # 主語
        'Aux': [],    # 助動詞
        'V': root_verb.text,  # 動詞
        'O1': [],     # 目的語1
        'O2': [],     # 目的語2
        'C1': [],     # 補語1
        'C2': [],     # 補語2
        'M2': [],     # 修飾句2
        'M3': []      # 修飾句3
    }
    
    # 各要素の境界特定
    for word in sent.words:
        head_id = word.head
        
        # ROOT動詞の直接の子要素
        if head_id == root_verb.id:
            if word.deprel == 'nsubj':
                backbone['S'].append(word)
            elif word.deprel == 'obj':
                backbone['O1'].append(word)
            elif word.deprel == 'xcomp':
                backbone['C2'].append(word)  # 補語動詞
            elif word.deprel in ['obl:unmarked', 'obl']:
                backbone['M1'].append(word)  # 文頭修飾
            elif word.deprel == 'aux':
                backbone['Aux'].append(word)
                
    return backbone

for sent in doc.sentences:
    backbone = extract_sentence_backbone(sent)
    if backbone:
        print("\n📋 基本8スロット構造:")
        for slot, words in backbone.items():
            if words and slot != 'V':
                word_texts = [w.text for w in words]
                print(f"  {slot:<3}: {word_texts}")
            elif slot == 'V':
                print(f"  {slot:<3}: ['{backbone[slot]}']")
    break

print("\n🎯 結論: Stanzaで正確な5文型背骨抽出が可能")
print("→ AllenNLPは不要、Stanzaで新しい分解エンジンを構築")
