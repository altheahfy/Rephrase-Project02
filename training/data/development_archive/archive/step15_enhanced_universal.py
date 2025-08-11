#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step 15: 強化版全スロット対応システム

包括テスト結果を基に、各スロットの専用強化を実装
目標: 全8スロットで80/80 (100%) サブスロット活用達成
"""

import spacy
import json
import traceback
from collections import OrderedDict

class EnhancedUniversalSubslotGenerator:
    """強化版全スロット対応 10サブスロット生成システム"""
    
    def __init__(self):
        """初期化"""
        print("🚀 Enhanced Universal Subslot Generator 起動開始...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy 'en_core_web_sm' 読み込み完了")
        except IOError:
            print("❌ spaCy英語モデルが見つかりません。以下のコマンドでインストールしてください:")
            print("python -m spacy download en_core_web_sm")
            raise
        
        # 10サブスロット定義
        self.subslot_types = [
            'sub-s', 'sub-v', 'sub-o1', 'sub-o2', 
            'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux'
        ]
        
        # 対象上位スロット
        self.target_slots = ['S', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
        
        print(f"🎯 対象上位スロット: {', '.join(self.target_slots)}")
        print(f"🔧 強化版サブスロット体系: {', '.join(self.subslot_types)}")
        
    def generate_subslots_for_slot(self, slot_name, sentence):
        """指定スロットの10サブスロット生成（強化版）"""
        print(f"\n🎯 {slot_name}スロット サブスロット生成開始: '{sentence}'")
        
        if slot_name not in self.target_slots:
            print(f"❌ 非対象スロット: {slot_name}")
            return {}
        
        try:
            doc = self.nlp(sentence)
            print(f"📝 解析対象: {[(token.text, token.dep_, token.pos_) for token in doc]}")
            
            # 包括的サブスロット検出（全スロット共通）
            complete_subslots = self._comprehensive_subslot_detection(doc)
            
            # スロット別専用強化
            if slot_name == 'S':
                enhanced = self._enhance_s_slot(doc, complete_subslots)
            elif slot_name == 'O1':
                enhanced = self._enhance_o1_slot(doc, complete_subslots)
            elif slot_name == 'O2':
                enhanced = self._enhance_o2_slot(doc, complete_subslots)
            elif slot_name == 'C1':
                enhanced = self._enhance_c1_slot(doc, complete_subslots)
            elif slot_name == 'C2':
                enhanced = self._enhance_c2_slot(doc, complete_subslots)
            elif slot_name == 'M1':
                enhanced = self._enhance_m1_slot(doc, complete_subslots)
            elif slot_name == 'M2':
                enhanced = self._enhance_m2_slot(doc, complete_subslots)
            elif slot_name == 'M3':
                enhanced = self._enhance_m3_slot(doc, complete_subslots)
            else:
                enhanced = complete_subslots
            
            print(f"🔧 強化後サブスロット数: {len(enhanced)}")
            return enhanced
            
        except Exception as e:
            print(f"❌ {slot_name}スロット処理エラー: {str(e)}")
            traceback.print_exc()
            return {}
    
    # ================================================================
    # 🚀 包括的サブスロット検出システム（強化版）
    # ================================================================
    
    def _comprehensive_subslot_detection(self, doc):
        """包括的サブスロット検出（全スロット対応強化版）"""
        subslots = {}
        used_tokens = set()
        
        # 1. 主語・動詞・目的語・補語の基本検出（強化）
        basic_slots = self._enhanced_basic_detection(doc, used_tokens)
        subslots.update(basic_slots)
        
        # 2. O1O2構造検出（第4文型）
        o1o2_result = self._enhanced_o1o2_detection(doc, used_tokens)
        if o1o2_result:
            subslots.update(o1o2_result)
        
        # 3. SVOC構造検出（第5文型）
        svoc_result = self._enhanced_svoc_detection(doc, used_tokens)
        if svoc_result:
            subslots.update(svoc_result)
        
        # 4. 補語構造の詳細検出（強化）
        complement_result = self._enhanced_complement_detection(doc, used_tokens)
        subslots.update(complement_result)
        
        # 5. 修飾語の包括検出（強化）
        modifier_result = self._enhanced_modifier_detection(doc, used_tokens)
        subslots.update(modifier_result)
        
        # 6. 助動詞の包括検出（強化）
        aux_result = self._enhanced_auxiliary_detection(doc, used_tokens)
        subslots.update(aux_result)
        
        return subslots
    
    def _enhanced_basic_detection(self, doc, used_tokens):
        """強化版基本要素検出"""
        subslots = {}
        
        # 主語検出（複数パターン対応）
        subjects_found = []
        for token in doc:
            if token.dep_ in ["nsubj", "nsubjpass", "csubj"] and token.i not in used_tokens:
                subjects_found.append(token)
        
        # 関係代名詞節内の主語も検出
        for token in doc:
            if token.dep_ == "relcl":  # 関係代名詞節
                for child in token.children:
                    if child.dep_ in ["nsubj", "nsubjpass"] and child.i not in used_tokens:
                        subjects_found.append(child)
        
        if subjects_found:
            # 最初の主語を採用
            subject = subjects_found[0]
            subject_phrase = self._extract_enhanced_phrase(subject, doc)
            subslots['sub-s'] = {
                'text': subject_phrase,
                'tokens': self._get_phrase_tokens(subject, doc),
                'token_indices': self._get_phrase_indices(subject, doc)
            }
            self._mark_tokens_used(subject, doc, used_tokens)
            print(f"✅ 強化版主語検出: '{subject_phrase}'")
        
        # 動詞検出（複数パターン対応）
        verbs_found = []
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ in ["ROOT", "conj", "relcl", "xcomp", "ccomp"] and token.i not in used_tokens:
                verbs_found.append(token)
        
        if verbs_found:
            # 最初の動詞を採用
            verb = verbs_found[0]
            subslots['sub-v'] = {
                'text': verb.text,
                'tokens': [verb.text],
                'token_indices': [verb.i]
            }
            used_tokens.add(verb.i)
            print(f"✅ 強化版動詞検出: '{verb.text}'")
        
        return subslots
    
    def _enhanced_o1o2_detection(self, doc, used_tokens):
        """強化版O1O2構造検出"""
        subslots = {}
        
        # 二重目的語動詞の拡張リスト
        ditransitive_verbs = {
            'give', 'send', 'show', 'tell', 'buy', 'make', 'teach', 'offer',
            'bring', 'get', 'find', 'leave', 'pay', 'sell', 'cook', 'build'
        }
        
        verb_token = None
        for token in doc:
            if token.lemma_.lower() in ditransitive_verbs or token.dep_ == "ROOT":
                verb_token = token
                break
        
        if not verb_token:
            return subslots
        
        # 間接目的語と直接目的語の検出（拡張版）
        indirect_obj = None
        direct_obj = None
        
        for child in verb_token.children:
            if child.dep_ == "dobj" and child.i not in used_tokens:
                direct_obj = child
            elif child.dep_ in ["dative", "iobj"] and child.i not in used_tokens:
                indirect_obj = child
            # 前置詞句からの間接目的語検出
            elif child.dep_ == "prep" and child.text.lower() in ['to', 'for']:
                for grandchild in child.children:
                    if grandchild.dep_ == "pobj" and indirect_obj is None:
                        indirect_obj = grandchild
        
        if indirect_obj and direct_obj:
            # sub-o1: 間接目的語
            subslots['sub-o1'] = {
                'text': indirect_obj.text,
                'tokens': [indirect_obj.text],
                'token_indices': [indirect_obj.i]
            }
            used_tokens.add(indirect_obj.i)
            
            # sub-o2: 直接目的語
            direct_phrase = self._extract_enhanced_phrase(direct_obj, doc)
            subslots['sub-o2'] = {
                'text': direct_phrase,
                'tokens': self._get_phrase_tokens(direct_obj, doc),
                'token_indices': self._get_phrase_indices(direct_obj, doc)
            }
            self._mark_tokens_used(direct_obj, doc, used_tokens)
            
            print(f"✅ 強化版O1O2検出: o1='{indirect_obj.text}', o2='{direct_phrase}'")
        
        return subslots
    
    def _enhanced_svoc_detection(self, doc, used_tokens):
        """強化版SVOC構造検出"""
        subslots = {}
        
        # 知覚動詞・使役動詞の拡張
        perception_causative_verbs = {
            'see', 'watch', 'hear', 'feel', 'make', 'let', 'have',
            'observe', 'notice', 'find', 'consider', 'think', 'believe'
        }
        
        verb_token = None
        for token in doc:
            if token.lemma_.lower() in perception_causative_verbs:
                verb_token = token
                break
        
        if not verb_token:
            return subslots
        
        object_token = None
        complement_token = None
        
        for child in verb_token.children:
            if child.dep_ == "dobj" and child.i not in used_tokens:
                object_token = child
            elif child.dep_ in ["xcomp", "ccomp", "acomp"] and child.i not in used_tokens:
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
            complement_phrase = self._extract_enhanced_phrase(complement_token, doc)
            subslots['sub-c1'] = {
                'text': complement_phrase,
                'tokens': self._get_phrase_tokens(complement_token, doc),
                'token_indices': self._get_phrase_indices(complement_token, doc)
            }
            self._mark_tokens_used(complement_token, doc, used_tokens)
            
            print(f"✅ 強化版SVOC検出: obj='{object_token.text}', comp='{complement_phrase}'")
        
        return subslots
    
    def _enhanced_complement_detection(self, doc, used_tokens):
        """強化版補語検出"""
        subslots = {}
        
        complement_count = 1  # C1, C2順序管理
        
        for token in doc:
            if token.i in used_tokens:
                continue
            
            # be動詞の補語
            if token.dep_ in ["acomp", "attr", "pcomp"]:
                if complement_count <= 2:
                    slot_key = f"sub-c{complement_count}"
                    phrase = self._extract_enhanced_phrase(token, doc)
                    
                    subslots[slot_key] = {
                        'text': phrase,
                        'tokens': self._get_phrase_tokens(token, doc),
                        'token_indices': self._get_phrase_indices(token, doc)
                    }
                    
                    self._mark_tokens_used(token, doc, used_tokens)
                    complement_count += 1
                    print(f"✅ 強化版補語検出: {slot_key}='{phrase}'")
        
        return subslots
    
    def _enhanced_modifier_detection(self, doc, used_tokens):
        """強化版修飾語検出"""
        subslots = {}
        modifier_count = 1
        
        # 修飾語の優先順位付け
        modifier_priorities = {
            'advmod': 1,    # 副詞修飾
            'amod': 2,      # 形容詞修飾  
            'prep': 3,      # 前置詞句
            'npadvmod': 4,  # 名詞句副詞的修飾
            'compound': 5   # 複合語
        }
        
        # 依存関係でソート
        potential_modifiers = []
        for token in doc:
            if token.i in used_tokens:
                continue
            if token.dep_ in modifier_priorities or token.pos_ in ["ADV", "ADJ"]:
                priority = modifier_priorities.get(token.dep_, 10)
                potential_modifiers.append((priority, token))
        
        potential_modifiers.sort(key=lambda x: x[0])  # 優先度順
        
        for priority, token in potential_modifiers:
            if modifier_count > 3:  # M1, M2, M3まで
                break
            
            slot_key = f"sub-m{modifier_count}"
            phrase = self._extract_enhanced_phrase(token, doc)
            
            subslots[slot_key] = {
                'text': phrase,
                'tokens': self._get_phrase_tokens(token, doc),
                'token_indices': self._get_phrase_indices(token, doc)
            }
            
            self._mark_tokens_used(token, doc, used_tokens)
            modifier_count += 1
            print(f"✅ 強化版修飾語検出: {slot_key}='{phrase}'")
        
        return subslots
    
    def _enhanced_auxiliary_detection(self, doc, used_tokens):
        """強化版助動詞検出"""
        subslots = {}
        
        # 助動詞の拡張検出
        aux_tokens = []
        for token in doc:
            if token.i in used_tokens:
                continue
            
            if token.dep_ in ["aux", "auxpass"] or token.pos_ == "AUX":
                aux_tokens.append(token)
            elif token.dep_ == "aux" and token.pos_ == "PART":  # to不定詞
                aux_tokens.append(token)
        
        if aux_tokens:
            aux_text = ' '.join([token.text for token in aux_tokens])
            subslots['sub-aux'] = {
                'text': aux_text,
                'tokens': [token.text for token in aux_tokens],
                'token_indices': [token.i for token in aux_tokens]
            }
            for token in aux_tokens:
                used_tokens.add(token.i)
            print(f"✅ 強化版助動詞検出: '{aux_text}'")
        
        return subslots
    
    # ================================================================
    # 🎯 スロット専用強化メソッド群
    # ================================================================
    
    def _enhance_s_slot(self, doc, subslots):
        """S専用強化: 主語特化"""
        enhanced = subslots.copy()
        
        # 関係代名詞節の主語検出強化
        for token in doc:
            if token.text.lower() in ['who', 'which', 'that'] and 'sub-s' not in enhanced:
                enhanced['sub-s'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"✅ S強化: 関係代名詞主語 '{token.text}'")
                break
        
        return enhanced
    
    def _enhance_o1_slot(self, doc, subslots):
        """O1専用強化: O1完成システム活用"""
        enhanced = subslots.copy()
        # O1は既に完成済みのため、現行システム維持
        print(f"🔄 O1完成システム活用: {len(enhanced)}サブスロット")
        return enhanced
    
    def _enhance_o2_slot(self, doc, subslots):
        """O2専用強化: 間接目的語特化"""
        enhanced = subslots.copy()
        
        # to/for句の強制的O2検出
        for token in doc:
            if token.text.lower() in ['to', 'for'] and token.dep_ == "prep":
                for child in token.children:
                    if child.dep_ == "pobj" and 'sub-o2' not in enhanced:
                        enhanced['sub-o2'] = {
                            'text': child.text,
                            'tokens': [child.text],
                            'token_indices': [child.i]
                        }
                        print(f"✅ O2強化: {token.text}句目的語 '{child.text}'")
                        break
        
        return enhanced
    
    def _enhance_c1_slot(self, doc, subslots):
        """C1専用強化: 第一補語特化"""
        enhanced = subslots.copy()
        
        # 形容詞補語の強制C1割り当て
        for token in doc:
            if token.pos_ == "ADJ" and token.dep_ in ["ROOT", "acomp"] and 'sub-c1' not in enhanced:
                enhanced['sub-c1'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"✅ C1強化: 形容詞補語 '{token.text}'")
                break
        
        return enhanced
    
    def _enhance_c2_slot(self, doc, subslots):
        """C2専用強化: 第二補語特化"""
        enhanced = subslots.copy()
        
        # 名詞補語の強制C2割り当て
        for token in doc:
            if token.pos_ == "NOUN" and token.dep_ in ["attr", "pcomp"] and 'sub-c2' not in enhanced:
                enhanced['sub-c2'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"✅ C2強化: 名詞補語 '{token.text}'")
                break
        
        return enhanced
    
    def _enhance_m1_slot(self, doc, subslots):
        """M1専用強化: 第一修飾語特化"""
        enhanced = subslots.copy()
        
        # 前置詞句の強制M1検出
        for token in doc:
            if token.dep_ == "prep" and 'sub-m1' not in enhanced:
                prep_phrase = self._extract_enhanced_phrase(token, doc)
                enhanced['sub-m1'] = {
                    'text': prep_phrase,
                    'tokens': self._get_phrase_tokens(token, doc),
                    'token_indices': self._get_phrase_indices(token, doc)
                }
                print(f"✅ M1強化: 前置詞句 '{prep_phrase}'")
                break
        
        return enhanced
    
    def _enhance_m2_slot(self, doc, subslots):
        """M2専用強化: 第二修飾語特化"""
        enhanced = subslots.copy()
        
        # 副詞の強制M2検出
        for token in doc:
            if token.pos_ == "ADV" and token.dep_ == "advmod" and 'sub-m2' not in enhanced:
                enhanced['sub-m2'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"✅ M2強化: 副詞 '{token.text}'")
                break
        
        return enhanced
    
    def _enhance_m3_slot(self, doc, subslots):
        """M3専用強化: 第三修飾語特化"""
        enhanced = subslots.copy()
        
        # 時間・場所副詞の強制M3検出
        time_place_advs = {'today', 'yesterday', 'tomorrow', 'here', 'there', 'now', 'then'}
        for token in doc:
            if token.text.lower() in time_place_advs and 'sub-m3' not in enhanced:
                enhanced['sub-m3'] = {
                    'text': token.text,
                    'tokens': [token.text],
                    'token_indices': [token.i]
                }
                print(f"✅ M3強化: 時間場所副詞 '{token.text}'")
                break
        
        return enhanced
    
    # ================================================================
    # 🛠️ ヘルパーメソッド
    # ================================================================
    
    def _extract_enhanced_phrase(self, token, doc):
        """強化版句抽出"""
        phrase_tokens = [token]
        
        # 子トークンを含める
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "pobj", "prep"]:
                phrase_tokens.append(child)
                # 前置詞句の場合、その目的語も
                if child.dep_ == "prep":
                    for grandchild in child.children:
                        if grandchild.dep_ == "pobj":
                            phrase_tokens.append(grandchild)
        
        # 語順でソート
        phrase_tokens.sort(key=lambda t: t.i)
        return ' '.join([t.text for t in phrase_tokens])
    
    def _get_phrase_tokens(self, token, doc):
        """句のトークンテキストリスト取得"""
        phrase_tokens = [token]
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "pobj", "prep"]:
                phrase_tokens.append(child)
        phrase_tokens.sort(key=lambda t: t.i)
        return [t.text for t in phrase_tokens]
    
    def _get_phrase_indices(self, token, doc):
        """句のトークンインデックスリスト取得"""
        phrase_tokens = [token]
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "pobj", "prep"]:
                phrase_tokens.append(child)
        phrase_tokens.sort(key=lambda t: t.i)
        return [t.i for t in phrase_tokens]
    
    def _mark_tokens_used(self, token, doc, used_tokens):
        """句全体のトークンを使用済みマーク"""
        used_tokens.add(token.i)
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "pobj", "prep"]:
                used_tokens.add(child.i)

def test_enhanced_system():
    """強化版システムのテスト"""
    print("🧪 Enhanced Universal System テスト開始")
    print("🎯 目標: 全スロット70%以上のサブスロット活用")
    print("=" * 80)
    
    generator = EnhancedUniversalSubslotGenerator()
    
    # 厳選テストケース
    critical_tests = {
        "S": ["The very intelligent student who was studying"],
        "O1": ["that he is definitely studying English very hard today"],
        "O2": ["to his very kind mother who lives in Tokyo"],
        "C1": ["extremely happy and excited about the news"],
        "C2": ["a very successful businessman who works here"],
        "M1": ["very carefully in the morning with great skill"],
        "M2": ["always working diligently until late"],
        "M3": ["under the bridge that was built yesterday"]
    }
    
    results = {}
    
    for slot_name, test_sentences in critical_tests.items():
        print(f"\n{'='*50}")
        print(f"🎯 {slot_name}スロット強化テスト")
        
        for sentence in test_sentences:
            print(f"📝 テスト: '{sentence}'")
            subslots = generator.generate_subslots_for_slot(slot_name, sentence)
            
            print(f"📊 検出サブスロット数: {len(subslots)}")
            for sub_type, sub_data in subslots.items():
                print(f"   ✅ {sub_type}: '{sub_data['text']}'")
            
            utilization_rate = (len(subslots) / 10) * 100
            print(f"🎯 活用率: {len(subslots)}/10 ({utilization_rate:.1f}%)")
            
            results[f"{slot_name}: {sentence}"] = {
                'subslots': subslots,
                'count': len(subslots),
                'rate': utilization_rate
            }
    
    # 全体統計
    print(f"\n{'='*80}")
    print("🎉 強化版テスト完了")
    
    total_slots = sum([r['count'] for r in results.values()])
    total_possible = len(results) * 10
    overall_rate = (total_slots / total_possible) * 100
    
    print(f"🎯 全体活用率: {total_slots}/{total_possible} ({overall_rate:.1f}%)")
    
    success_tests = [k for k, v in results.items() if v['rate'] >= 70]
    print(f"🎉 成功テスト (70%以上): {len(success_tests)}/{len(results)}")
    
    if len(success_tests) >= 6:  # 8中6以上で成功
        print("🎊 強化版システム成功！大部分のスロットで高活用率達成！")
    else:
        print("⚠️  更なる強化が必要")
    
    return results

if __name__ == "__main__":
    test_enhanced_system()
