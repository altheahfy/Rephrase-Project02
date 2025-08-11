#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step 14: 全上位スロット対応 10サブスロット生成システム

O1スロットで100%達成した10サブスロット構造を、
全上位スロット（S, O1, O2, C1, C2, M1, M2, M3）に適用

対象外スロット: Aux, V (元から単一機能のため除外)
"""

import spacy
import json
import traceback
from collections import OrderedDict

class UniversalSubslotGenerator:
    """全スロット対応 10サブスロット生成システム"""
    
    def __init__(self):
        """初期化"""
        print("🚀 Universal Subslot Generator 起動開始...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy 'en_core_web_sm' 読み込み完了")
        except IOError:
            print("❌ spaCy英語モデルが見つかりません。以下のコマンドでインストールしてください:")
            print("python -m spacy download en_core_web_sm")
            raise
        
        # 10サブスロット定義（O1で完成したもの）
        self.subslot_types = [
            'sub-s', 'sub-v', 'sub-o1', 'sub-o2', 
            'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux'
        ]
        
        # 対象上位スロット
        self.target_slots = ['S', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
        
        print(f"🎯 対象上位スロット: {', '.join(self.target_slots)}")
        print(f"🔧 サブスロット体系: {', '.join(self.subslot_types)}")
        
    def generate_subslots_for_slot(self, slot_name, sentence):
        """指定スロットの10サブスロット生成"""
        print(f"\n🎯 {slot_name}スロット サブスロット生成開始: '{sentence}'")
        
        if slot_name not in self.target_slots:
            print(f"❌ 非対象スロット: {slot_name}")
            return {}
        
        try:
            doc = self.nlp(sentence)
            print(f"📝 解析対象: {[(token.text, token.dep_, token.pos_) for token in doc]}")
            
            # スロット別専用処理
            if slot_name == 'O1':
                return self._generate_o1_subslots(doc, sentence)
            elif slot_name == 'S':
                return self._generate_s_subslots(doc, sentence)
            elif slot_name == 'O2':
                return self._generate_o2_subslots(doc, sentence)
            elif slot_name == 'C1':
                return self._generate_c1_subslots(doc, sentence)
            elif slot_name == 'C2':
                return self._generate_c2_subslots(doc, sentence)
            elif slot_name == 'M1':
                return self._generate_m1_subslots(doc, sentence)
            elif slot_name == 'M2':
                return self._generate_m2_subslots(doc, sentence)
            elif slot_name == 'M3':
                return self._generate_m3_subslots(doc, sentence)
            
        except Exception as e:
            print(f"❌ {slot_name}スロット処理エラー: {str(e)}")
            traceback.print_exc()
            return {}
    
    def _generate_o1_subslots(self, doc, sentence):
        """O1スロット用（すでに完成済みシステム）"""
        print("🔄 O1完成済みシステム使用")
        return self._detect_all_subslots(doc)
    
    def _generate_s_subslots(self, doc, sentence):
        """Sスロット用 10サブスロット生成"""
        print("🎯 S(Subject)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # S専用強化: 主語特有パターン
        self._enhance_subject_patterns(doc, subslots)
        
        return subslots
    
    def _generate_o2_subslots(self, doc, sentence):
        """O2スロット用 10サブスロット生成"""
        print("🎯 O2(Object2)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # O2専用強化: 間接目的語特有パターン
        self._enhance_indirect_object_patterns(doc, subslots)
        
        return subslots
    
    def _generate_c1_subslots(self, doc, sentence):
        """C1スロット用 10サブスロット生成"""
        print("🎯 C1(Complement1)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # C1専用強化: 第一補語特有パターン
        self._enhance_complement_patterns(doc, subslots, complement_type="C1")
        
        return subslots
    
    def _generate_c2_subslots(self, doc, sentence):
        """C2スロット用 10サブスロット生成"""
        print("🎯 C2(Complement2)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # C2専用強化: 第二補語特有パターン
        self._enhance_complement_patterns(doc, subslots, complement_type="C2")
        
        return subslots
    
    def _generate_m1_subslots(self, doc, sentence):
        """M1スロット用 10サブスロット生成"""
        print("🎯 M1(Modifier1)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # M1専用強化: 修飾語特有パターン
        self._enhance_modifier_patterns(doc, subslots, modifier_type="M1")
        
        return subslots
    
    def _generate_m2_subslots(self, doc, sentence):
        """M2スロット用 10サブスロット生成"""
        print("🎯 M2(Modifier2)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # M2専用強化: 修飾語特有パターン
        self._enhance_modifier_patterns(doc, subslots, modifier_type="M2")
        
        return subslots
    
    def _generate_m3_subslots(self, doc, sentence):
        """M3スロット用 10サブスロット生成"""
        print("🎯 M3(Modifier3)スロット専用処理")
        subslots = {}
        
        # 完全10サブスロット検出適用
        complete_subslots = self._detect_all_subslots(doc)
        subslots.update(complete_subslots)
        
        # M3専用強化: 修飾語特有パターン
        self._enhance_modifier_patterns(doc, subslots, modifier_type="M3")
        
        return subslots
    
    # ================================================================
    # 🚀 完全10サブスロット検出システム（O1完成版ベース）
    # ================================================================
    
    def _detect_all_subslots(self, doc):
        """完全10サブスロット検出（O1完成システムより移植）"""
        subslots = {}
        used_tokens = set()  # トークン重複防止
        
        # 1. O1O2構造検出（第4文型対応）
        o1o2_result = self._detect_o1o2_structure(doc, used_tokens)
        if o1o2_result:
            subslots.update(o1o2_result)
        
        # 2. SVOC構造検出（第5文型対応）
        svoc_result = self._detect_svoc_structure(doc, used_tokens)
        if svoc_result:
            subslots.update(svoc_result)
        
        # 3. 基本スロット検出
        basic_slots = self._detect_basic_slots(doc, used_tokens)
        subslots.update(basic_slots)
        
        # 4. 修飾語検出（位置ベース配置）
        modifier_slots = self._detect_modifier_slots(doc, used_tokens)
        subslots.update(modifier_slots)
        
        # 5. 助動詞検出
        aux_slots = self._detect_auxiliary_verbs(doc, used_tokens)
        subslots.update(aux_slots)
        
        return subslots
    
    def _detect_o1o2_structure(self, doc, used_tokens):
        """O1O2構造検出（give him a book パターン）"""
        subslots = {}
        
        # 二重目的語動詞検出
        ditransitive_verbs = {'give', 'send', 'show', 'tell', 'buy', 'make', 'teach', 'offer'}
        verb_token = None
        
        for token in doc:
            if token.lemma_.lower() in ditransitive_verbs:
                verb_token = token
                break
        
        if not verb_token:
            return subslots
        
        # 間接目的語（sub-o1）と直接目的語（sub-o2）の検出
        indirect_obj = None  # him
        direct_obj = None    # a book
        
        for child in verb_token.children:
            if child.dep_ == "dobj" and child.i not in used_tokens:
                direct_obj = child
            elif child.dep_ == "dative" and child.i not in used_tokens:
                indirect_obj = child
            elif child.dep_ == "pobj" and child.head.dep_ == "prep" and child.i not in used_tokens:
                if indirect_obj is None:
                    indirect_obj = child
        
        if indirect_obj and direct_obj:
            # sub-o1: 間接目的語
            subslots['sub-o1'] = {
                'text': indirect_obj.text,
                'tokens': [indirect_obj.text],
                'token_indices': [indirect_obj.i]
            }
            used_tokens.add(indirect_obj.i)
            
            # sub-o2: 直接目的語
            direct_obj_phrase = self._extract_phrase(direct_obj)
            subslots['sub-o2'] = {
                'text': direct_obj_phrase,
                'tokens': [token.text for token in doc if token.head == direct_obj or token == direct_obj],
                'token_indices': [token.i for token in doc if token.head == direct_obj or token == direct_obj]
            }
            for token in doc:
                if token.head == direct_obj or token == direct_obj:
                    used_tokens.add(token.i)
            
            print(f"✅ O1O2構造検出: him={indirect_obj.text}, book={direct_obj_phrase}")
        
        return subslots
    
    def _detect_svoc_structure(self, doc, used_tokens):
        """SVOC構造検出（I saw her cry パターン）"""
        subslots = {}
        
        # 知覚動詞・使役動詞
        perception_causative_verbs = {'see', 'watch', 'hear', 'feel', 'make', 'let', 'have'}
        verb_token = None
        
        for token in doc:
            if token.lemma_.lower() in perception_causative_verbs:
                verb_token = token
                break
        
        if not verb_token:
            return subslots
        
        # 目的語と補語の検出
        object_token = None
        complement_token = None
        
        for child in verb_token.children:
            if child.dep_ == "dobj" and child.i not in used_tokens:
                object_token = child
            elif child.dep_ in ["xcomp", "ccomp"] and child.i not in used_tokens:
                complement_token = child
        
        if object_token and complement_token:
            # sub-o1: 目的語
            subslots['sub-o1'] = {
                'text': object_token.text,
                'tokens': [object_token.text],
                'token_indices': [object_token.i]
            }
            used_tokens.add(object_token.i)
            
            # sub-c1: 補語
            complement_phrase = self._extract_phrase(complement_token)
            subslots['sub-c1'] = {
                'text': complement_phrase,
                'tokens': [token.text for token in doc if token.head == complement_token or token == complement_token],
                'token_indices': [token.i for token in doc if token.head == complement_token or token == complement_token]
            }
            for token in doc:
                if token.head == complement_token or token == complement_token:
                    used_tokens.add(token.i)
            
            print(f"✅ SVOC構造検出: obj={object_token.text}, comp={complement_phrase}")
        
        return subslots
    
    def _detect_basic_slots(self, doc, used_tokens):
        """基本スロット検出（S, V）"""
        subslots = {}
        
        # 主語検出
        for token in doc:
            if token.dep_ == "nsubj" and token.i not in used_tokens:
                subject_phrase = self._extract_phrase(token)
                subslots['sub-s'] = {
                    'text': subject_phrase,
                    'tokens': [t.text for t in doc if t.head == token or t == token],
                    'token_indices': [t.i for t in doc if t.head == token or t == token]
                }
                for t in doc:
                    if t.head == token or t == token:
                        used_tokens.add(t.i)
                break
        
        # 動詞検出
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ in ["ROOT", "conj"] and token.i not in used_tokens:
                subslots['sub-v'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                used_tokens.add(token.i)
                break
        
        return subslots
    
    def _detect_modifier_slots(self, doc, used_tokens):
        """修飾語スロット検出（位置ベース配置）"""
        subslots = {}
        modifier_count = 1
        
        for token in doc:
            if token.i in used_tokens:
                continue
            
            # 修飾語候補
            if token.dep_ in ["prep", "advmod", "amod", "npadvmod", "compound"] or token.pos_ in ["ADV", "ADJ"]:
                if modifier_count <= 3:  # M1, M2, M3
                    slot_key = f"sub-m{modifier_count}"
                    phrase = self._extract_phrase(token)
                    
                    subslots[slot_key] = {
                        'text': phrase,
                        'tokens': [t.text for t in doc if t.head == token or t == token],
                        'token_indices': [t.i for t in doc if t.head == token or t == token]
                    }
                    
                    for t in doc:
                        if t.head == token or t == token:
                            used_tokens.add(t.i)
                    
                    modifier_count += 1
        
        return subslots
    
    def _detect_auxiliary_verbs(self, doc, used_tokens):
        """助動詞検出"""
        subslots = {}
        
        aux_tokens = [token for token in doc if token.dep_ == "aux" and token.i not in used_tokens]
        if aux_tokens:
            aux_text = ' '.join([token.text for token in aux_tokens])
            subslots['sub-aux'] = {
                'text': aux_text,
                'tokens': [token.text for token in aux_tokens],
                'token_indices': [token.i for token in aux_tokens]
            }
            for token in aux_tokens:
                used_tokens.add(token.i)
        
        return subslots
    
    def _extract_phrase(self, token):
        """トークンから句を抽出"""
        # 依存関係ベースの句抽出
        phrase_tokens = [token]
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "prep", "pobj"]:
                phrase_tokens.append(child)
                # 前置詞句の場合、その目的語も含める
                if child.dep_ == "prep":
                    for grandchild in child.children:
                        if grandchild.dep_ == "pobj":
                            phrase_tokens.append(grandchild)
        
        # 語順でソート
        phrase_tokens.sort(key=lambda t: t.i)
        return ' '.join([t.text for t in phrase_tokens])
    
    # ================================================================
    # 🎯 スロット専用強化メソッド群
    # ================================================================
    
    def _enhance_subject_patterns(self, doc, subslots):
        """S専用: 主語特有パターン強化"""
        # 関係代名詞節の主語
        for token in doc:
            if token.dep_ == "relcl":
                subj_in_rel = None
                for child in token.children:
                    if child.dep_ == "nsubj":
                        subj_in_rel = child
                        break
                
                if subj_in_rel and 'sub-s' not in subslots:
                    subslots['sub-s'] = {
                        'text': subj_in_rel.text,
                        'tokens': [subj_in_rel.text],
                        'token_indices': [subj_in_rel.i]
                    }
                    print(f"✅ S専用強化: 関係節主語 '{subj_in_rel.text}'")
    
    def _enhance_indirect_object_patterns(self, doc, subslots):
        """O2専用: 間接目的語特有パターン強化"""
        # to/for句の目的語
        for token in doc:
            if token.text.lower() in ['to', 'for'] and token.dep_ == "prep":
                for child in token.children:
                    if child.dep_ == "pobj":
                        if 'sub-o2' not in subslots:
                            subslots['sub-o2'] = {
                                'text': child.text,
                                'tokens': [child.text],
                                'token_indices': [child.i]
                            }
                            print(f"✅ O2専用強化: to/for句 '{child.text}'")
    
    def _enhance_complement_patterns(self, doc, subslots, complement_type):
        """C1/C2専用: 補語特有パターン強化"""
        # be動詞の補語
        for token in doc:
            if token.lemma_ == "be":
                for child in token.children:
                    if child.dep_ in ["acomp", "attr"]:
                        slot_key = 'sub-c1' if complement_type == "C1" else 'sub-c2'
                        if slot_key not in subslots:
                            subslots[slot_key] = {
                                'text': child.text,
                                'tokens': [child.text],
                                'token_indices': [child.i]
                            }
                            print(f"✅ {complement_type}専用強化: be補語 '{child.text}'")
    
    def _enhance_modifier_patterns(self, doc, subslots, modifier_type):
        """M1/M2/M3専用: 修飾語特有パターン強化"""
        # 時間・場所・様態副詞の特別処理
        time_advs = {'today', 'yesterday', 'tomorrow', 'now', 'then', 'always', 'never'}
        place_advs = {'here', 'there', 'everywhere', 'nowhere', 'outside', 'inside'}
        manner_advs = {'quickly', 'slowly', 'carefully', 'suddenly', 'quietly'}
        
        for token in doc:
            if token.text.lower() in time_advs | place_advs | manner_advs:
                slot_key = f'sub-{modifier_type.lower()}'
                if slot_key not in subslots:
                    subslots[slot_key] = {
                        'text': token.text,
                        'tokens': [token.text],
                        'token_indices': [token.i]
                    }
                    print(f"✅ {modifier_type}専用強化: 副詞 '{token.text}'")

def test_universal_system():
    """全スロット対応システムのテスト"""
    print("🧪 Universal Subslot System テスト開始")
    print("=" * 60)
    
    generator = UniversalSubslotGenerator()
    
    # テストケース（各スロット用）
    test_cases = [
        # S (Subject) テスト
        ("S", "The intelligent student"),
        ("S", "My best friend who lives in Tokyo"),
        
        # O1 (完成済み) テスト
        ("O1", "the beautiful red car"),
        ("O1", "that he is studying hard"),
        
        # O2 (Object 2) テスト
        ("O2", "to his mother"),
        ("O2", "for the children"),
        
        # C1 (Complement 1) テスト
        ("C1", "very happy"),
        ("C1", "a good teacher"),
        
        # C2 (Complement 2) テスト
        ("C2", "extremely difficult"),
        ("C2", "the best solution"),
        
        # M1, M2, M3 (Modifier) テスト
        ("M1", "in the morning"),
        ("M2", "very carefully"),
        ("M3", "under the bridge")
    ]
    
    results = {}
    
    for slot_name, sentence in test_cases:
        print(f"\n{'='*50}")
        print(f"🎯 テスト: {slot_name}スロット")
        print(f"📝 入力: '{sentence}'")
        
        subslots = generator.generate_subslots_for_slot(slot_name, sentence)
        results[f"{slot_name}: {sentence}"] = subslots
        
        print(f"📊 検出サブスロット数: {len(subslots)}")
        for sub_type, sub_data in subslots.items():
            print(f"   {sub_type}: '{sub_data['text']}'")
    
    print(f"\n{'='*60}")
    print("🎉 Universal System テスト完了")
    print(f"📊 総テスト数: {len(test_cases)}")
    print(f"📊 全スロット対応: {', '.join(generator.target_slots)}")
    
    return results

if __name__ == "__main__":
    test_universal_system()
