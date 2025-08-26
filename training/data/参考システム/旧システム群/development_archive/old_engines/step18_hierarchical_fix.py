"""
Step18: 階層的依存関係処理の改良システム
ex007のC2/M2/M3スロット正確分離のための完全修正版
"""

import spacy
import pandas as pd
from collections import defaultdict

class Step18HierarchicalFixSystem:
    def __init__(self):
        """階層的処理システム初期化"""
        print("🎯 Step18階層的修正システム初期化中...")
        self.nlp = spacy.load('en_core_web_sm')
        
        # 依存関係-サブスロットマッピング（完全版）
        self.dependency_mapping = {
            # Core grammatical relationships
            'nsubj': 'sub-s',
            'nsubjpass': 'sub-s', 
            'aux': 'sub-aux',
            'auxpass': 'sub-aux',
            'dobj': 'sub-o1',
            'iobj': 'sub-o2',
            'attr': 'sub-c1',
            'ccomp': 'sub-c2',
            'xcomp': 'sub-c2',
            
            # Modifier relationships
            'advmod': 'sub-m2',
            'amod': 'sub-m3',
            'prep': 'sub-m3',
            'pobj': 'sub-o1',
            'pcomp': 'sub-c2',
            'mark': 'sub-m1',
            
            # Clausal relationships
            'advcl': 'M2',  # 要階層処理
            'relcl': 'sub-m3',
            'acl': 'sub-m3',
            'conj': 'C2',   # 要階層処理
            
            # Determiner relationships
            'det': 'EXTEND',
            'poss': 'EXTEND',
            'compound': 'EXTEND'
        }
        
    def decompose_sentence(self, sentence):
        """階層的文分解エンジン"""
        print(f"\n🎯 Step18階層的処理開始: '{sentence}'")
        
        # spaCy解析
        doc = self.nlp(sentence)
        
        # ROOT動詞特定
        root_verb = None
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ in ['VERB', 'AUX']:
                root_verb = token
                break
        
        if not root_verb:
            return {}
            
        print(f"🎯 ROOT動詞特定: '{root_verb.text}' (pos={root_verb.pos_})")
        
        # 階層的スロット抽出
        all_slots = self._extract_hierarchical_slots(doc, root_verb)
        
        return all_slots
    
    def _extract_hierarchical_slots(self, doc, root_verb):
        """階層的スロット抽出メソッド"""
        print(f"\n🔍 階層的スロット抽出開始: ROOT='{root_verb.text}'")
        
        all_slots = {}
        
        # 1. 基本スロット（S/V/O1/Aux/C1）抽出
        base_slots = self._extract_base_slots(doc, root_verb)
        if base_slots:
            all_slots.update(base_slots)
        
        # 2. C2スロット抽出（conj関係）
        c2_slots = self._extract_c2_slots(doc, root_verb)
        if c2_slots:
            all_slots.update(c2_slots)
            
        # 3. M2/M3スロット抽出（advcl階層処理）
        m_slots = self._extract_advcl_slots(doc, root_verb)
        if m_slots:
            all_slots.update(m_slots)
            
        return all_slots
    
    def _extract_base_slots(self, doc, root_verb):
        """基本スロット抽出"""
        print(f"🔍 基本スロット抽出: ROOT='{root_verb.text}'")
        
        # ROOT直結の子要素のみ処理
        base_children = [child for child in root_verb.children]
        
        base_tokens = defaultdict(list)
        
        for child in base_children:
            dep = child.dep_
            
            # conj/advclは基本スロットから除外（階層処理）
            if dep in ['conj', 'advcl']:
                continue
                
            # 依存関係マッピング
            if dep in self.dependency_mapping:
                subslot = self.dependency_mapping[dep]
                if subslot != 'EXTEND':
                    base_tokens[subslot].append(child)
        
        # サブスロット構築
        base_slots = {}
        if base_tokens:
            base_slots['S'] = self._build_subslots(base_tokens, doc)
            
        return base_slots
    
    def _extract_c2_slots(self, doc, root_verb):
        """C2スロット抽出（conj関係）"""
        print(f"🔍 C2スロット抽出: ROOT='{root_verb.text}'")
        
        c2_slots = {}
        
        # ROOT直結のconj検索
        for child in root_verb.children:
            if child.dep_ == 'conj':
                print(f"📌 C2発見: '{child.text}' (dep={child.dep_})")
                
                # C2動詞の子要素収集
                c2_tokens = defaultdict(list)
                
                for c2_child in child.children:
                    dep = c2_child.dep_
                    
                    # advcl は M2 として別処理
                    if dep == 'advcl':
                        continue
                        
                    if dep in self.dependency_mapping:
                        subslot = self.dependency_mapping[dep]
                        if subslot != 'EXTEND':
                            c2_tokens[subslot].append(c2_child)
                
                # C2動詞自体を追加
                c2_tokens['sub-v'].append(child)
                
                if c2_tokens:
                    c2_slots['C2'] = self._build_subslots(c2_tokens, doc)
                    
        return c2_slots
    
    def _extract_advcl_slots(self, doc, root_verb):
        """advcl階層処理（M2/M3分離）"""
        print(f"🔍 advcl階層処理: ROOT='{root_verb.text}'")
        
        m_slots = {}
        
        # ROOT直結のadvcl → M3
        for child in root_verb.children:
            if child.dep_ == 'advcl':
                print(f"📌 M3発見: '{child.text}' (advcl:ROOT)")
                
                m3_tokens = defaultdict(list)
                
                for m3_child in child.children:
                    dep = m3_child.dep_
                    if dep in self.dependency_mapping:
                        subslot = self.dependency_mapping[dep]
                        if subslot != 'EXTEND':
                            m3_tokens[subslot].append(m3_child)
                
                # M3動詞自体
                m3_tokens['sub-v'].append(child)
                
                if m3_tokens:
                    m_slots['M3'] = self._build_subslots(m3_tokens, doc)
        
        # C2配下のadvcl → M2
        for child in root_verb.children:
            if child.dep_ == 'conj':  # C2動詞
                for c2_child in child.children:
                    if c2_child.dep_ == 'advcl':
                        print(f"📌 M2発見: '{c2_child.text}' (advcl:C2)")
                        
                        m2_tokens = defaultdict(list)
                        
                        for m2_child in c2_child.children:
                            dep = m2_child.dep_
                            if dep in self.dependency_mapping:
                                subslot = self.dependency_mapping[dep]
                                if subslot != 'EXTEND':
                                    m2_tokens[subslot].append(m2_child)
                        
                        # M2動詞自体
                        m2_tokens['sub-v'].append(c2_child)
                        
                        if m2_tokens:
                            m_slots['M2'] = self._build_subslots(m2_tokens, doc)
        
        return m_slots
    
    def _build_subslots(self, slot_tokens, doc):
        """サブスロット構築（前置詞統合対応）"""
        subslots = {}
        
        for subslot_name, tokens in slot_tokens.items():
            if not tokens:
                continue
                
            if len(tokens) == 1:
                # 単一トークン処理
                token = tokens[0]
                
                # 前置詞統合チェック
                final_text = self._integrate_prepositions(token, doc)
                
                # スパン拡張適用
                if not final_text:
                    final_text = self._expand_span(token, doc)
                    
                subslots[subslot_name] = final_text
            else:
                # 複数トークン - 結合
                combined_text = ' '.join([t.text for t in sorted(tokens, key=lambda x: x.i)])
                subslots[subslot_name] = combined_text
        
        return subslots
        
    def _integrate_prepositions(self, token, doc):
        """前置詞統合処理"""
        # 動詞 + 前置詞の統合
        if token.pos_ in ['VERB', 'AUX']:
            prep_children = [child for child in token.children if child.dep_ == 'prep']
            if prep_children:
                prep_texts = []
                for prep in prep_children:
                    # 前置詞 + その目的語
                    pobj_children = [child for child in prep.children if child.dep_ == 'pobj']
                    if pobj_children:
                        pobj = pobj_children[0]
                        pobj_span = self._expand_span(pobj, doc)
                        prep_texts.append(f"{prep.text} {pobj_span}")
                    else:
                        prep_texts.append(prep.text)
                
                if prep_texts:
                    return f"{token.text} {' '.join(prep_texts)}"
        
        # mark + 従属接続詞の統合 (even though処理)
        if token.dep_ == 'mark':
            # 前方のadvmodをチェック
            for i in range(token.i - 1, -1, -1):
                prev_token = doc[i]
                if prev_token.dep_ == 'advmod' and prev_token.head == token.head:
                    return f"{prev_token.text} {token.text}"
                if prev_token.i < token.i - 2:  # 2語以内でチェック
                    break
        
        return None
    
    def _expand_span(self, token, doc):
        """スパン拡張処理"""
        # 拡張対象の依存関係
        expand_deps = ['det', 'poss', 'compound', 'amod', 'prep', 'pobj']
        
        # 左右拡張
        start_idx = token.i
        end_idx = token.i
        
        # 左拡張
        for i in range(token.i - 1, -1, -1):
            if doc[i].head.i == token.i and doc[i].dep_ in expand_deps:
                start_idx = i
            else:
                break
        
        # 右拡張
        for i in range(token.i + 1, len(doc)):
            if doc[i].head.i == token.i and doc[i].dep_ in expand_deps:
                end_idx = i
            else:
                break
        
        # スパンテキスト生成
        span_text = ' '.join([doc[i].text for i in range(start_idx, end_idx + 1)])
        
        return span_text

def test_ex007_hierarchical():
    """ex007階層的処理テスト"""
    system = Step18HierarchicalFixSystem()
    
    ex007 = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    result = system.decompose_sentence(ex007)
    
    print(f"\n=== 階層的処理結果 ===")
    for slot_name, subslots in result.items():
        print(f"\n📋 {slot_name}スロット:")
        for sub_name, sub_value in subslots.items():
            print(f"  {sub_name:<10}: \"{sub_value}\"")

if __name__ == "__main__":
    test_ex007_hierarchical()
