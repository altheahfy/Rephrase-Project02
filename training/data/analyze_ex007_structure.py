import spacy

# spaCy初期化
nlp = spacy.load('en_core_web_sm')

# ex007全文解析
sentence = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

doc = nlp(sentence)

print('=== ex007全文の依存関係解析 ===')
print(f'文: {sentence}')
print('=' * 100)

print(f'{"Token":<20} | {"POS":<6} | {"Dep":<12} | {"Head":<15} | {"Children"}')
print('-' * 100)

for token in doc:
    children = [child.text for child in token.children]
    children_str = ', '.join(children[:5])  # 最初の5個まで
    if len(children) > 5:
        children_str += '...'
    
    print(f'{token.text:<20} | {token.pos_:<6} | {token.dep_:<12} | {token.head.text:<15} | {children_str}')

print('\n=== ROOT動詞とその主要な依存関係 ===')
root_token = [token for token in doc if token.dep_ == 'ROOT'][0]
print(f'ROOT: {root_token.text} (pos={root_token.pos_})')

print('\n主要な依存関係:')
for child in root_token.children:
    print(f'  {child.dep_:<12}: {child.text}')
    if child.dep_ in ['advcl', 'ccomp', 'xcomp']:
        for grandchild in child.children:
            print(f'    └─ {grandchild.dep_:<10}: {grandchild.text}')
