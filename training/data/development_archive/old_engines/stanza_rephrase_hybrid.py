"""
StanzaRephraseEngine - ハイブリッド分解エンジン
Stanzaの正確な背骨構築 + Step18の高品質サブスロットシステム
"""

import stanza
import spacy
from collections import defaultdict

class StanzaRephraseEngine:
    def __init__(self):
        """初期化 - Stanza + spaCy + 既存モジュール統合"""
        print("🎯 StanzaRephraseEngine初期化中...")
        
        # Stanza: 背骨構築用
        self.stanza_nlp = stanza.Pipeline('en', verbose=False)
        
        # spaCy: 既存モジュール連携用（スパン拡張等）
        self.spacy_nlp = spacy.load('en_core_web_sm')
        
        # 既存Step18の優れたマッピング（流用）
        self.dep_to_subslot = {
            'nsubj': 'sub-s',
            'nsubjpass': 'sub-s',
            'aux': 'sub-aux', 
            'auxpass': 'sub-aux',
            'dobj': 'sub-o1',
            'iobj': 'sub-o2',
            'attr': 'sub-c1',
            'ccomp': 'sub-c2',
            'xcomp': 'sub-c2',
            'advmod': 'sub-m2',
            'amod': 'sub-m3', 
            'prep': 'sub-m3',
            'pobj': 'sub-o1',
            'pcomp': 'sub-c2',
            'mark': 'sub-m1',
            'relcl': 'sub-m3',
            'acl': 'sub-m3'
        }
        
        print("✅ ハイブリッドエンジン準備完了")
    
    def decompose_sentence(self, sentence):
        """完全分解: Stanza背骨 + Step18詳細化"""
        print(f"\n🎯 ハイブリッド分解開始: '{sentence[:50]}...'")
        
        # Step1: Stanzaで正確な背骨構築
        stanza_doc = self.stanza_nlp(sentence)
        backbone = self._extract_backbone_with_stanza(stanza_doc)
        
        # Step2: spaCyでStep18モジュール適用
        spacy_doc = self.spacy_nlp(sentence)
        detailed_slots = self._apply_step18_detailing(backbone, spacy_doc)
        
        return detailed_slots
    
    def _extract_backbone_with_stanza(self, stanza_doc):
        """Stanzaで背骨（基本8スロット構造）抽出"""
        print("🏗️ Stanza背骨構築中...")
        
        for sent in stanza_doc.sentences:
            # ROOT動詞特定
            root_verb = None
            for word in sent.words:
                if word.deprel == 'root':
                    root_verb = word
                    break
            
            if not root_verb:
                continue
                
            print(f"📌 ROOT動詞: '{root_verb.text}'")
            
            # 基本構造の境界特定
            backbone = {
                'M1': [],     # 文頭修飾句
                'S': [],      # 主語
                'Aux': [],    # 助動詞
                'V': root_verb.text,  # 主動詞
                'O1': [],     # 目的語1
                'O2': [],     # 目的語2  
                'C1': [],     # 補語1
                'C2': [],     # 補語2
                'M2': [],     # 修飾句2
                'M3': []      # 修飾句3
            }
            
            # Stanzaの依存関係で各スロットの核を特定
            for word in sent.words:
                if word.head == root_verb.id:  # ROOT動詞の直接の子
                    if word.deprel == 'nsubj':
                        backbone['S'].append(word)
                        print(f"📍 S核: '{word.text}'")
                    elif word.deprel == 'obj':
                        backbone['O1'].append(word) 
                        print(f"📍 O1核: '{word.text}'")
                    elif word.deprel == 'xcomp':
                        backbone['C2'].append(word)
                        # 実際の動作動詞はC2のxcomp
                        backbone['V'] = word.text  # ROOT動詞を上書き
                        print(f"📍 C2核: '{word.text}' → V動詞を更新")
                        
                        # xcompの目的語をO1として検出
                        for xcomp_child in sent.words:
                            if (xcomp_child.head == word.id and 
                                xcomp_child.deprel == 'obj'):
                                backbone['O1'].append(xcomp_child)
                                print(f"📍 O1核（xcomp配下）: '{xcomp_child.text}'")
                                
                    elif word.deprel in ['obl:unmarked', 'obl']:
                        backbone['M1'].append(word)
                        print(f"📍 M1核: '{word.text}'")
                    elif word.deprel == 'aux':
                        backbone['Aux'].append(word)
                        print(f"📍 Aux核: '{word.text}'")
                        
            return backbone, sent
            
        return None, None
    
    def _apply_step18_detailing(self, backbone_data, spacy_doc):
        """Step18の詳細化モジュール適用"""
        if not backbone_data:
            return {}
            
        backbone, stanza_sent = backbone_data
        print("🔧 Step18詳細化適用中...")
        
        detailed_slots = {}
        
        # 各スロットを詳細化
        for slot_name, stanza_words in backbone.items():
            if slot_name == 'V':  # 動詞は単純
                detailed_slots[slot_name] = {'v': backbone[slot_name]}
                continue
                
            if not stanza_words:  # 空のスロットはスキップ
                continue
                
            # M1スロット: 文頭修飾句の完全拡張
            if slot_name == 'M1':
                m1_phrase = self._expand_m1_phrase(stanza_words[0], stanza_sent)
                detailed_slots[slot_name] = {'main': m1_phrase}
                print(f"✅ {slot_name}スロット詳細化完了: '{m1_phrase}'")
                continue
                
            # Auxスロット: 助動詞 + to の組み合わせ
            if slot_name == 'Aux':
                aux_phrase = self._build_aux_phrase(stanza_words, stanza_sent)
                detailed_slots[slot_name] = {'main': aux_phrase}
                print(f"✅ {slot_name}スロット詳細化完了: '{aux_phrase}'")
                continue
                
            # StanzaからspaCyへの単語マッピング
            spacy_tokens = self._map_stanza_to_spacy(stanza_words, spacy_doc)
            
            if spacy_tokens:
                # Step18のサブスロット構築を適用
                subslots = self._build_subslots_step18_style(
                    spacy_tokens, spacy_doc, slot_name
                )
                if subslots:
                    detailed_slots[slot_name] = subslots
                    print(f"✅ {slot_name}スロット詳細化完了")
        
        # 正解データと比較表示
        self._compare_with_correct_data(detailed_slots)
        
        return detailed_slots
    
    def _compare_with_correct_data(self, results):
        """正解データとの比較"""
        print("\n🎯 正解データ比較:")
        
        # ex007正解データ（5文型フルセットより）
        correct_data = {
            'M1': "that afternoon at the crucial point in the presentation",
            'S': {
                'main': "the manager who had recently taken charge of the project",
                'sub-s': "the manager who",
                'sub-aux': "had", 
                'sub-m2': "recently",
                'sub-v': "taken",
                'sub-o1': "charge of the project"
            },
            'Aux': "had to",
            'V': "make",
            'O1': "the committee responsible for implementation"
        }
        
        for slot, correct in correct_data.items():
            if slot in results:
                if isinstance(correct, dict) and isinstance(results[slot], dict):
                    print(f"\n{slot}スロット比較:")
                    for sub, correct_val in correct.items():
                        actual = results[slot].get(sub, "❌ 未検出")
                        match = "✅" if actual == correct_val else "❌"
                        print(f"  {sub}: {match} 正解='{correct_val}' 実際='{actual}'")
                else:
                    actual = results[slot].get('v') if isinstance(results[slot], dict) else results[slot]
                    match = "✅" if actual == correct else "❌"  
                    print(f"{slot}: {match} 正解='{correct}' 実際='{actual}'")
            else:
                print(f"{slot}: ❌ スロット未検出 正解='{correct}'")
    
    def _map_stanza_to_spacy(self, stanza_words, spacy_doc):
        """Stanzaの単語をspaCyトークンにマッピング"""
        spacy_tokens = []
        
        for stanza_word in stanza_words:
            # テキスト位置で対応するspaCyトークンを探す
            for spacy_token in spacy_doc:
                if (spacy_token.text == stanza_word.text and 
                    abs(spacy_token.idx - (stanza_word.start_char or 0)) < 10):
                    spacy_tokens.append(spacy_token)
                    break
                    
        return spacy_tokens
    
    def _build_subslots_step18_style(self, main_tokens, doc, slot_type):
        """Step18スタイルのサブスロット構築（流用）"""
        slot_tokens = defaultdict(list)
        
        # メイントークンを解析してサブスロットに分類
        for token in main_tokens:
            # 関係詞句の処理
            if token.dep_ == 'nsubj' and slot_type == 'S':
                slot_tokens['sub-s'].append(token)
                
                # 関係節の処理
                for child in token.children:
                    if child.dep_ == 'relcl':
                        for rel_child in child.children:
                            dep = rel_child.dep_
                            if dep in self.dep_to_subslot:
                                subslot = self.dep_to_subslot[dep]
                                slot_tokens[subslot].append(rel_child)
                        slot_tokens['sub-v'].append(child)
        
        # Step18の_build_subslots相当の処理
        return self._finalize_subslots(slot_tokens, doc)
    
    def _finalize_subslots(self, slot_tokens, doc):
        """サブスロット最終化（Step18の_build_subslots流用）"""
        subslots = {}
        
        for subslot_name, tokens in slot_tokens.items():
            if not tokens:
                continue
                
            if len(tokens) == 1:
                token = tokens[0]
                # スパン拡張（Step18のロジック流用）
                span = self._expand_span_step18_style(token, doc)
                subslots[subslot_name] = span
            else:
                # 複数トークン結合
                text = ' '.join([t.text for t in sorted(tokens, key=lambda x: x.i)])
                subslots[subslot_name] = text
                
        return subslots
    
    def _expand_span_step18_style(self, token, doc):
        """Step18のスパン拡張ロジック（流用改良版）"""
        expand_deps = ['det', 'poss', 'compound', 'amod']
        
        start = token.i
        end = token.i
        
        # 基本的な子要素の拡張
        for child in token.children:
            if child.dep_ in expand_deps:
                start = min(start, child.i)
                end = max(end, child.i)
        
        # 関係代名詞の処理
        for child in token.children:
            if child.dep_ == 'relcl':
                for rel_child in child.children:
                    if rel_child.dep_ == 'nsubj' and rel_child.text in ['who', 'which', 'that']:
                        start = min(start, rel_child.i)
                        break
        
        return doc[start:end+1].text
    
    def _expand_m1_phrase(self, m1_word, stanza_sent):
        """M1スロット（文頭修飾句）の完全拡張"""
        # 文頭からS開始まで全てを取る
        s_start = None
        for word in stanza_sent.words:
            if word.deprel == 'nsubj':
                s_start = word.start_char
                break
        
        if s_start:
            sentence_text = stanza_sent.text
            m1_text = sentence_text[:s_start].strip().rstrip(',')
            return m1_text
        
        return m1_word.text
    
    def _build_aux_phrase(self, aux_words, stanza_sent):
        """Auxスロット構築（had to形式）"""
        aux_parts = []
        
        # ROOT動詞の助動詞を探す
        for word in stanza_sent.words:
            if word.deprel == 'root':
                root = word
                for child_word in stanza_sent.words:
                    if child_word.head == root.id and child_word.deprel == 'aux':
                        aux_parts.append(child_word.text)
                    elif child_word.head == root.id and child_word.deprel == 'mark' and child_word.text == 'to':
                        aux_parts.append(child_word.text)
                break
        
        return ' '.join(aux_parts) if aux_parts else aux_words[0].text if aux_words else ""
    
    def display_results(self, results):
        """結果表示（Step18スタイル）"""
        print("\n=== ハイブリッド分解結果 ===")
        
        for slot_name, slot_data in results.items():
            if isinstance(slot_data, dict) and len(slot_data) > 1:
                print(f"\n📋 {slot_name}スロット:")
                for subslot, content in slot_data.items():
                    print(f"  {subslot:<10}: \"{content}\"")
            else:
                content = slot_data.get('v', slot_data) if isinstance(slot_data, dict) else slot_data
                print(f"\n📋 {slot_name}スロット: \"{content}\"")

# テスト実行
if __name__ == "__main__":
    engine = StanzaRephraseEngine()
    
    text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    results = engine.decompose_sentence(text)
    engine.display_results(results)
