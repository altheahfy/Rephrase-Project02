import spacy
import pandas as pd
import re
from collections import defaultdict

class UniversalDecomposeEngine:
    """
    Rephrase統一分解エンジン
    M1, S, M2, C1, O1, O2, C2, M3の8スロット共通
    フルセット解析で発見した全パターンに対応
    """
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # フルセット解析から抽出した全パターン
        self.patterns = {
            # Pattern A: sub-c1 + sub-m1 + sub-m2 + sub-s + sub-v (2例)
            'subordinate_clause_with_complement': {
                'triggers': ['although', 'even though', 'while'],
                'structure': 'CONJ + SUBJ + VERB + ADV + COMP'
            },
            
            # Pattern B: sub-aux + sub-m1 + sub-o1 + sub-s + sub-v (3例) 
            'subordinate_clause_with_object': {
                'triggers': ['because', 'while', 'even though'],
                'structure': 'CONJ + SUBJ + AUX + VERB + OBJ'
            },
            
            # Pattern C: sub-aux + sub-m2 + sub-o1 + sub-s + sub-v (4例)
            'relative_clause_with_object': {
                'triggers': ['who', 'that', 'which'],
                'structure': 'REL + SUBJ + AUX + ADV + VERB + OBJ'
            },
            
            # Pattern D: sub-c1 + sub-s + sub-v (2例)
            'simple_complement': {
                'triggers': ['seemed', 'appeared', 'looked'],
                'structure': 'SUBJ + VERB + COMP'
            },
            
            # Pattern E: sub-aux + sub-o2 + sub-s + sub-v (1例) - 最重要
            'that_clause_with_infinitive': {
                'triggers': ['that'],
                'structure': 'THAT + SUBJ + AUX + VERB + TO_INFINITIVE'
            },
            
            # Pattern F: sub-o1 + sub-s + sub-v (1例)
            'that_clause_simple': {
                'triggers': ['that'],
                'structure': 'THAT + SUBJ + VERB + TO_INFINITIVE'
            }
        }
    
    def decompose(self, phrase):
        """
        統一分解メソッド
        どのスロットからでも呼び出し可能
        """
        if not phrase or phrase.strip() == "":
            return self._empty_subslots()
            
        phrase = phrase.strip()
        doc = self.nlp(phrase)
        
        # 全パターンマッチング試行
        result = self._try_all_patterns(phrase, doc)
        
        # 100%単語保全チェック
        if not self._verify_word_coverage(phrase, result):
            print(f"⚠️  Word coverage incomplete for: '{phrase}'")
            result = self._fallback_decompose(phrase, doc)
        
        return result
    
    def _try_all_patterns(self, phrase, doc):
        """全パターンを順次試行"""
        
        # Pattern E: that節+不定詞（最重要）
        if phrase.startswith('that '):
            return self._decompose_that_clause_infinitive(phrase, doc)
        
        # Pattern A: 従属節+補語
        for trigger in ['although', 'even though', 'while']:
            if phrase.startswith(trigger):
                return self._decompose_subordinate_complement(phrase, doc, trigger)
        
        # Pattern B: 従属節+目的語
        for trigger in ['because', 'while', 'even though']:
            if phrase.startswith(trigger):
                return self._decompose_subordinate_object(phrase, doc, trigger)
        
        # Pattern C: 関係節+目的語
        if ' who ' in phrase or ' that ' in phrase or ' which ' in phrase:
            return self._decompose_relative_clause(phrase, doc)
        
        # Pattern D: 単純補語
        for verb in ['seemed', 'appeared', 'looked']:
            if f' {verb} ' in phrase:
                return self._decompose_simple_complement(phrase, doc, verb)
        
        # その他のパターン試行
        return self._decompose_general_structure(phrase, doc)
    
    def _decompose_that_clause_infinitive(self, phrase, doc):
        """Pattern E: that節+不定詞構造 - spaCy依存解析ベース"""
        result = self._empty_subslots()
        
        # spaCy解析による文法構造認識
        that_token = None
        subject_tokens = []
        aux_tokens = []
        verb_tokens = []
        infinitive_tokens = []
        
        for token in doc:
            # "that"の検出
            if token.text.lower() == "that" and token.dep_ in ["mark", "nsubj"]:
                that_token = token
            
            # 主語の検出（that以降の名詞句）
            elif token.dep_ in ["nsubj", "nsubjpass"] and token.pos_ in ["PRON", "NOUN"]:
                subject_tokens.append(token)
            
            # 助動詞の検出
            elif token.pos_ == "AUX" or (token.dep_ == "aux" and token.pos_ == "VERB"):
                aux_tokens.append(token)
            
            # メイン動詞の検出
            elif token.dep_ == "ROOT" or (token.pos_ == "VERB" and token.dep_ in ["xcomp", "ccomp"]):
                verb_tokens.append(token)
            
            # 不定詞句の検出（to + 動詞）
            elif token.text.lower() == "to" or (token.dep_ in ["xcomp", "dobj"] and "to" in phrase):
                # 不定詞句の開始位置から終わりまで取得
                infinitive_start = None
                for i, t in enumerate(doc):
                    if t.text.lower() == "to" and i < len(doc) - 1:
                        infinitive_start = i
                        break
                
                if infinitive_start:
                    infinitive_tokens = doc[infinitive_start:]
                break
        
        # Rephrase分解ルール適用
        if that_token and subject_tokens:
            # sub-s: "that" + 主語
            if subject_tokens:
                result['sub-s'] = f"that {subject_tokens[0].text}"
        
        if aux_tokens:
            # sub-aux: 助動詞
            result['sub-aux'] = aux_tokens[0].text
        
        if verb_tokens:
            # sub-v: メイン動詞（複合動詞含む）
            verb_phrase = []
            for v in verb_tokens:
                verb_phrase.append(v.text)
                # 付随する分詞等も含める
                for child in v.children:
                    if child.dep_ in ["aux", "auxpass", "neg"] or child.pos_ in ["VERB", "ADP"]:
                        verb_phrase.append(child.text)
            result['sub-v'] = " ".join(verb_phrase[:2])  # 最大2語まで
        
        if infinitive_tokens:
            # sub-o2: 不定詞句
            result['sub-o2'] = infinitive_tokens.text
        
        return result
    
    def _decompose_subordinate_complement(self, phrase, doc, trigger):
        """Pattern A: 従属節+補語構造 - spaCy依存解析ベース"""
        result = self._empty_subslots()
        
        # spaCy解析による構造認識
        conj_token = None
        subj_token = None
        verb_token = None
        adv_tokens = []
        comp_tokens = []
        
        for token in doc:
            # 従属接続詞
            if token.text.lower() == trigger.lower():
                conj_token = token
                result['sub-m1'] = token.text
            
            # 主語
            elif token.dep_ in ["nsubj", "nsubjpass"]:
                subj_token = token
                result['sub-s'] = token.text
            
            # 動詞（ROOT or cop）
            elif token.dep_ in ["ROOT", "cop"] and token.pos_ == "VERB":
                verb_token = token
                result['sub-v'] = token.text
            
            # 副詞（修飾語）
            elif token.pos_ == "ADV" and token.dep_ in ["advmod"]:
                adv_tokens.append(token)
            
            # 補語
            elif token.dep_ in ["attr", "acomp", "pcomp"] or (token.pos_ == "ADJ" and token.dep_ != "amod"):
                comp_tokens.append(token)
        
        # 副詞をsub-m2に配置
        if adv_tokens:
            result['sub-m2'] = adv_tokens[0].text
        
        # 補語をsub-c1に配置
        if comp_tokens:
            result['sub-c1'] = comp_tokens[0].text
        
        return result
    
    def _decompose_subordinate_object(self, phrase, doc, trigger):
        """Pattern B: 従属節+目的語構造 - spaCy依存解析ベース"""
        result = self._empty_subslots()
        
        # spaCy解析による構造認識
        for token in doc:
            # 従属接続詞
            if token.text.lower() == trigger.lower():
                result['sub-m1'] = token.text
            
            # 主語（句全体）
            elif token.dep_ in ["nsubj", "nsubjpass"]:
                subj_span = self._get_extended_span(token, doc)
                result['sub-s'] = subj_span
            
            # 助動詞
            elif token.pos_ == "AUX" or token.dep_ == "aux":
                result['sub-aux'] = token.text
            
            # メイン動詞
            elif token.dep_ == "ROOT" and token.pos_ == "VERB":
                result['sub-v'] = token.text
            
            # 目的語
            elif token.dep_ in ["dobj", "pobj"]:
                obj_span = self._get_extended_span(token, doc)
                result['sub-o1'] = obj_span
        
        return result
    
    def _decompose_relative_clause(self, phrase, doc):
        """Pattern C/D: 関係節構造 - spaCy依存解析ベース"""
        result = self._empty_subslots()
        
        # 関係代名詞の検出と処理
        rel_pronoun = None
        main_subj = None
        rel_clause_tokens = []
        
        for token in doc:
            # 関係代名詞の検出
            if token.text.lower() in ['who', 'that', 'which'] and token.dep_ in ['nsubj', 'dobj', 'nsubjpass']:
                rel_pronoun = token
                
                # メイン主語部分（関係代名詞より前）
                main_part = []
                for t in doc:
                    if t.i < token.i:
                        main_part.append(t.text)
                    elif t.i == token.i:
                        main_part.append(t.text)
                        break
                
                result['sub-s'] = " ".join(main_part)
                
                # 関係節部分の処理
                rel_clause_start = token.i + 1
                rel_clause_tokens = doc[rel_clause_start:]
                break
        
        # 関係節内の文法要素処理
        if rel_clause_tokens:
            for token in rel_clause_tokens:
                # 助動詞
                if token.pos_ == "AUX" or token.dep_ == "aux":
                    result['sub-aux'] = token.text
                
                # 副詞
                elif token.pos_ == "ADV" and token.dep_ == "advmod":
                    result['sub-m2'] = token.text
                
                # 動詞
                elif token.pos_ == "VERB" and token.dep_ in ["ROOT", "relcl"]:
                    result['sub-v'] = token.text
                
                # 補語
                elif token.dep_ in ["attr", "acomp"] or token.pos_ == "ADJ":
                    result['sub-c1'] = token.text
                
                # 目的語
                elif token.dep_ in ["dobj", "pobj"]:
                    obj_span = self._get_extended_span(token, doc)
                    result['sub-o1'] = obj_span
        
        return result
    
    def _decompose_complex_relative(self, phrase, doc):
        """複雑な関係節: the manager who had recently taken charge of the project"""
        result = self._empty_subslots()
        
        # パターン: SUBJ who AUX ADV VERB OBJ
        parts = phrase.split(' who ')
        if len(parts) == 2:
            result['sub-s'] = f"{parts[0]} who"
            
            remainder = parts[1].split()
            if len(remainder) >= 4:
                result['sub-aux'] = remainder[0]  # had
                result['sub-m2'] = remainder[1]   # recently  
                result['sub-v'] = remainder[2]    # taken
                result['sub-o1'] = " ".join(remainder[3:])  # charge of the project
        
        return result
    
    def _decompose_simple_complement(self, phrase, doc, verb):
        """Pattern D: simple complement structure"""
        result = self._empty_subslots()
        
        parts = phrase.split(f' {verb} ')
        if len(parts) == 2:
            result['sub-s'] = parts[0]
            result['sub-v'] = verb
            result['sub-c1'] = parts[1]
        
        return result
    
    def _decompose_general_structure(self, phrase, doc):
        """一般的な構造分析フォールバック"""
        result = self._empty_subslots()
        
        # spaCyによる文法解析
        for token in doc:
            if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
                # 主語の取得（修飾語含む）
                subj_span = self._get_extended_span(token, doc)
                result['sub-s'] = subj_span
            elif token.pos_ == "AUX":
                result['sub-aux'] = token.text
            elif token.dep_ == "ROOT" and token.pos_ == "VERB":
                result['sub-v'] = token.text
            elif token.dep_ == "dobj":
                obj_span = self._get_extended_span(token, doc)
                result['sub-o1'] = obj_span
            elif token.dep_ == "attr" or token.dep_ == "acomp":
                result['sub-c1'] = token.text
        
        # 単一要素の場合
        if not any(result.values()):
            result['sub-s'] = phrase  # フォールバック
        
        return result
    
    def _get_extended_span(self, token, doc):
        """トークンの修飾語を含む拡張スパンを取得"""
        left = token.i
        right = token.i + 1
        
        # 左側の修飾語
        for child in token.children:
            if child.i < token.i:
                left = min(left, child.i)
        
        # 右側の修飾語
        for child in token.children:
            if child.i > token.i:
                right = max(right, child.i + 1)
        
        return doc[left:right].text
    
    def _fallback_decompose(self, phrase, doc):
        """フォールバック：単純分解"""
        result = self._empty_subslots()
        result['sub-s'] = phrase  # 最低限の保全
        return result
    
    def _verify_word_coverage(self, original, subslots):
        """100%単語保全チェック"""
        original_words = set(original.lower().split())
        covered_words = set()
        
        for subslot_value in subslots.values():
            if subslot_value:
                covered_words.update(subslot_value.lower().split())
        
        missing_words = original_words - covered_words
        return len(missing_words) == 0
    
    def _empty_subslots(self):
        """空のサブスロット構造"""
        return {
            'sub-m1': '',
            'sub-s': '',  
            'sub-aux': '',
            'sub-m2': '',
            'sub-v': '',
            'sub-c1': '',
            'sub-o1': '',
            'sub-o2': '',
            'sub-c2': '',
            'sub-m3': ''
        }


# テスト実行
if __name__ == "__main__":
    engine = UniversalDecomposeEngine()
    
    print('🎯 統一分解エンジン：フルセットパターン対応テスト')
    print('=' * 80)
    
    # フルセットの重要例文でテスト
    test_cases = [
        "although it was emotionally hard",
        "that he had been trying to avoid Tom", 
        "the woman who seemed indecisive",
        "because he was afraid of hurting her feelings",
        "the manager who had recently taken charge of the project"
    ]
    
    for phrase in test_cases:
        print(f'\n📋 入力: "{phrase}"')
        result = engine.decompose(phrase)
        
        print('分解結果:')
        for key, value in result.items():
            if value:
                print(f'  {key}: "{value}"')
        
        # 単語保全チェック
        original_words = phrase.split()
        covered_words = []
        for value in result.values():
            if value:
                covered_words.extend(value.split())
        
        print(f'単語保全: {len(original_words)}語 -> {len(covered_words)}語')
        if len(original_words) == len(covered_words):
            print('✅ 100%保全達成')
        else:
            print('❌ 単語欠落あり')
