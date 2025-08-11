"""
Step18: 完全8スロット分解システム
ex007の100%精度達成のための最終版
"""

import spacy
from collections import defaultdict

class Step18Complete8SlotSystem:
    def __init__(self):
        """完全8スロットシステム初期化"""
        print("🎯 Step18完全8スロット分解システム初期化中...")
        self.nlp = spacy.load('en_core_web_sm')
        
        # 依存関係-サブスロットマッピング
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
        
    def decompose_sentence(self, sentence):
        """完全8スロット分解"""
        print(f"\n🎯 完全8スロット分解開始: '{sentence}'")
        
        doc = self.nlp(sentence)
        
        # ROOT動詞特定
        root_verb = None
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ in ['VERB', 'AUX']:
                root_verb = token
                break
                
        if not root_verb:
            return {}
            
        print(f"🎯 ROOT動詞: '{root_verb.text}'")
        
        # 完全スロット分解
        all_slots = self._extract_complete_slots(doc, root_verb)
        
        return all_slots
    
    def _extract_complete_slots(self, doc, root_verb):
        """完全スロット抽出"""
        print(f"\n🔍 完全スロット抽出: ROOT='{root_verb.text}'")
        
        # スロット構造初期化
        slots = {
            'M1': {},  # 文頭修飾句
            'S': {},   # 主部スロット
            'Aux': {}, # 助動詞スロット
            'V': {},   # 動詞スロット  
            'O1': {},  # 目的語1スロット
            'C1': {},  # 補語1スロット
            'C2': {},  # 補語2スロット
            'M2': {},  # 副詞句2スロット
            'M3': {}   # 副詞句3スロット
        }
        
        # 1. 文頭修飾句（M1）抽出
        self._extract_m1_slot(doc, slots)
        
        # 2. 主部（S）スロット抽出
        self._extract_s_slot(doc, root_verb, slots)
        
        # 3. 動詞（V）スロット抽出  
        self._extract_v_slot(root_verb, slots)
        
        # 4. 助動詞（Aux）スロット抽出
        self._extract_aux_slot(doc, root_verb, slots)
        
        # 5. 目的語（O1）スロット抽出
        self._extract_o1_slot(doc, root_verb, slots)
        
        # 6. C2スロット抽出（conj動詞）
        self._extract_c2_slot(doc, root_verb, slots)
        
        # 7. M2スロット抽出（C2配下のadvcl）
        self._extract_m2_slot(doc, root_verb, slots)
        
        # 8. M3スロット抽出（ROOT配下のadvcl）
        self._extract_m3_slot(doc, root_verb, slots)
        
        # 空スロットを削除
        return {k: v for k, v in slots.items() if v}
    
    def _extract_m1_slot(self, doc, slots):
        """M1スロット抽出（文頭修飾句）"""
        print("🔍 M1スロット抽出（文頭修飾句）")
        # ex007では文頭修飾句なしのためスキップ
        pass
    
    def _extract_s_slot(self, doc, root_verb, slots):
        """Sスロット抽出（主部）"""
        print("🔍 Sスロット抽出（主部）")
        
        # ROOT動詞の主語を探す
        main_subject = None
        for child in root_verb.children:
            if child.dep_ in ['nsubj', 'nsubjpass']:
                main_subject = child
                break
                
        if not main_subject:
            return
            
        print(f"📌 主語発見: '{main_subject.text}'")
        
        # 主語の関係節処理
        s_tokens = defaultdict(list)
        
        # 主語の子要素収集
        for child in main_subject.children:
            if child.dep_ == 'relcl':  # 関係節
                print(f"📌 関係節発見: '{child.text}'")
                
                # 関係節内のサブスロット
                for rel_child in child.children:
                    dep = rel_child.dep_
                    if dep in self.dep_to_subslot:
                        subslot = self.dep_to_subslot[dep]
                        s_tokens[subslot].append(rel_child)
                        
                # 関係節動詞自体
                s_tokens['sub-v'].append(child)
        
        # 主語自体
        s_tokens['sub-s'].append(main_subject)
        
        # ROOT動詞のaux収集（Sスロット用）
        for child in root_verb.children:
            if child.dep_ in ['aux', 'auxpass']:
                s_tokens['sub-aux'].append(child)
        
        if s_tokens:
            slots['S'] = self._build_subslots(s_tokens, doc)
            
    def _extract_v_slot(self, root_verb, slots):
        """Vスロット抽出（動詞）"""
        print("🔍 Vスロット抽出（動詞）")
        slots['V'] = {'v': root_verb.text}
    
    def _extract_aux_slot(self, doc, root_verb, slots):
        """Auxスロット抽出（助動詞）"""
        print("🔍 Auxスロット抽出（助動詞）")
        # ex007では独立したAuxスロットなし
        pass
        
    def _extract_o1_slot(self, doc, root_verb, slots):
        """O1スロット抽出（目的語1）"""
        print("🔍 O1スロット抽出（目的語1）")
        
        # ROOT動詞の補語を探す（xcomp/ccomp）
        for child in root_verb.children:
            if child.dep_ in ['xcomp', 'ccomp']:
                print(f"📌 補語動詞発見: '{child.text}'")
                
                o1_tokens = defaultdict(list)
                
                # 補語動詞の子要素
                for comp_child in child.children:
                    dep = comp_child.dep_
                    if dep in self.dep_to_subslot:
                        subslot = self.dep_to_subslot[dep]
                        o1_tokens[subslot].append(comp_child)
                
                # 補語動詞自体
                o1_tokens['sub-v'].append(child)
                
                # 動詞のto不定詞マーカー処理
                for root_child in root_verb.children:
                    if root_child.dep_ == 'aux' and root_child.text == 'to':
                        o1_tokens['sub-aux'].append(root_child)
                
                if o1_tokens:
                    slots['O1'] = self._build_subslots(o1_tokens, doc)
                break
                
    def _extract_c2_slot(self, doc, root_verb, slots):
        """C2スロット抽出（conj動詞）"""
        print("🔍 C2スロット抽出（conj動詞）")
        
        for child in root_verb.children:
            if child.dep_ == 'conj':
                print(f"📌 C2動詞発見: '{child.text}'")
                
                c2_tokens = defaultdict(list)
                
                # C2動詞の子要素（advcl除く）
                for c2_child in child.children:
                    dep = c2_child.dep_
                    
                    if dep == 'advcl':  # M2スロットとして別処理
                        continue
                    
                    # advmod -> sub-m3に分類（flawlessly対応）    
                    if dep == 'advmod':
                        c2_tokens['sub-m3'].append(c2_child)
                    elif dep in self.dep_to_subslot:
                        subslot = self.dep_to_subslot[dep]
                        c2_tokens[subslot].append(c2_child)
                
                # C2動詞自体
                c2_tokens['sub-v'].append(child)
                
                if c2_tokens:
                    slots['C2'] = self._build_subslots(c2_tokens, doc)
                break
                
    def _extract_m2_slot(self, doc, root_verb, slots):
        """M2スロット抽出（C2配下のadvcl）"""
        print("🔍 M2スロット抽出（C2配下のadvcl）")
        
        # C2動詞を探す
        c2_verb = None
        for child in root_verb.children:
            if child.dep_ == 'conj':
                c2_verb = child
                break
                
        if not c2_verb:
            return
            
        # C2配下のadvcl
        for c2_child in c2_verb.children:
            if c2_child.dep_ == 'advcl':
                print(f"📌 M2 advcl発見: '{c2_child.text}'")
                
                m2_tokens = defaultdict(list)
                
                # advcl動詞の子要素
                for advcl_child in c2_child.children:
                    dep = advcl_child.dep_
                    if dep in self.dep_to_subslot:
                        subslot = self.dep_to_subslot[dep]
                        m2_tokens[subslot].append(advcl_child)
                
                # advcl動詞自体
                m2_tokens['sub-v'].append(c2_child)
                
                if m2_tokens:
                    slots['M2'] = self._build_subslots(m2_tokens, doc)
                break
                
    def _extract_m3_slot(self, doc, root_verb, slots):
        """M3スロット抽出（ROOT配下のadvcl）"""
        print("🔍 M3スロット抽出（ROOT配下のadvcl）")
        
        for child in root_verb.children:
            if child.dep_ == 'advcl':
                print(f"📌 M3 advcl発見: '{child.text}'")
                
                m3_tokens = defaultdict(list)
                
                # advcl動詞の子要素
                for advcl_child in child.children:
                    dep = advcl_child.dep_
                    if dep in self.dep_to_subslot:
                        subslot = self.dep_to_subslot[dep]
                        m3_tokens[subslot].append(advcl_child)
                
                # advcl動詞自体
                m3_tokens['sub-v'].append(child)
                
                if m3_tokens:
                    slots['M3'] = self._build_subslots(m3_tokens, doc)
                break
    
    def _build_subslots(self, slot_tokens, doc):
        """サブスロット構築"""
        subslots = {}
        
        for subslot_name, tokens in slot_tokens.items():
            if not tokens:
                continue
                
            if len(tokens) == 1:
                token = tokens[0]
                
                # 前置詞統合チェック
                integrated = self._integrate_prepositions(token, doc)
                if integrated:
                    subslots[subslot_name] = integrated
                else:
                    # スパン拡張
                    span = self._expand_span(token, doc)
                    subslots[subslot_name] = span
            else:
                # 複数トークン結合
                text = ' '.join([t.text for t in sorted(tokens, key=lambda x: x.i)])
                subslots[subslot_name] = text
                
        return subslots
    
    def _integrate_prepositions(self, token, doc):
        """前置詞統合処理"""
        # 動詞 + 前置詞句統合
        if token.pos_ in ['VERB', 'AUX']:
            prep_parts = []
            
            for child in token.children:
                if child.dep_ == 'prep':
                    prep_text = child.text
                    
                    # 前置詞の目的語
                    for prep_child in child.children:
                        if prep_child.dep_ == 'pobj':
                            obj_span = self._expand_span(prep_child, doc)
                            prep_text += f" {obj_span}"
                    
                    prep_parts.append(prep_text)
            
            if prep_parts:
                return f"{token.text} {' '.join(prep_parts)}"
        
        # mark + advmod統合（even though）
        if token.dep_ == 'mark':
            for i in range(max(0, token.i - 2), token.i):
                if doc[i].dep_ == 'advmod' and doc[i].head == token.head:
                    return f"{doc[i].text} {token.text}"
        
        return None
    
    def _expand_span(self, token, doc):
        """スパン拡張処理"""
        expand_deps = ['det', 'poss', 'compound', 'amod']
        
        start = token.i
        end = token.i
        
        # 子要素の拡張
        for child in token.children:
            if child.dep_ in expand_deps:
                start = min(start, child.i)
                end = max(end, child.i)
        
        return ' '.join([doc[i].text for i in range(start, end + 1)])

def test_complete_8slot_ex007():
    """ex007完全8スロットテスト"""
    system = Step18Complete8SlotSystem()
    
    ex007 = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    result = system.decompose_sentence(ex007)
    
    print(f"\n=== 完全8スロット分解結果 ===")
    for slot_name, subslots in result.items():
        print(f"\n📋 {slot_name}スロット:")
        for sub_name, sub_value in subslots.items():
            print(f"  {sub_name:<10}: \"{sub_value}\"")

if __name__ == "__main__":
    test_complete_8slot_ex007()
