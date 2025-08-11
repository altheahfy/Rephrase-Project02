import stanza
import spacy

# ex007で各ツールの能力をテスト
text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."

print("=== Stanza (Stanford CoreNLP) テスト ===")
try:
    # Stanzaダウンロードが必要かもしれない
    nlp_stanza = stanza.Pipeline('en', verbose=False)
    doc_stanza = nlp_stanza(text)
    
    print("🔍 Stanza構文解析結果:")
    for sent in doc_stanza.sentences:
        for word in sent.words:
            print(f"  {word.text:<15} | POS: {word.upos:<8} | Dep: {word.deprel:<12} | Head: {sent.words[word.head-1].text if word.head > 0 else 'ROOT'}")
            if len([w for w in sent.words if w.id <= 10]) <= word.id:  # 最初の10語のみ表示
                break
        break
        
except Exception as e:
    print(f"❌ Stanzaエラー: {e}")
    print("💡 初回使用時はモデルダウンロードが必要です")

print("\n" + "="*60)
print("=== spaCy比較結果 ===")
nlp_spacy = spacy.load('en_core_web_sm')
doc_spacy = nlp_spacy(text)

print("🔍 spaCy構文解析結果:")
for i, token in enumerate(doc_spacy):
    print(f"  {token.text:<15} | POS: {token.pos_:<8} | Dep: {token.dep_:<12} | Head: {token.head.text}")
    if i >= 9:  # 最初の10語のみ表示
        break

print("\n" + "="*60)        
print("=== 比較分析 ===")
print("Stanza: Stanford大学の学術的NLP - より深い構文解析")
print("spaCy: 実用的NLP - 高速で実装が容易")
print("AllenNLP: 後でSemantic Role Labelingをテスト")
