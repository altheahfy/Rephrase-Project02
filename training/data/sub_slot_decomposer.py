"""
サブスロット分解エンジン
複文内部構造（関係詞節・副詞節）をサブスロットに分解
"""
import spacy
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class SubSlotResult:
    """サブスロット分解結果"""
    clause_type: str  # "relative_clause", "adverbial_clause"
    original_text: str
    sub_slots: Dict[str, str]
    confidence: float

class SubSlotDecomposer:
    """サブスロット分解エンジン"""
    
    def __init__(self):
        print("🔧 サブスロット分解エンジン初期化中...")
        self.nlp = spacy.load('en_core_web_sm')
        print("✅ サブスロット分解エンジン準備完了")
    
    def decompose_complex_slots(self, main_slots: Dict[str, str]) -> Dict[str, List[SubSlotResult]]:
        """メインスロットから複文箇所を検出してサブスロット分解（条件緩和版）"""
        sub_slot_results = {}
        
        print("\n🔍 複文箇所検出・サブスロット分解開始")
        
        # 1. 主語(S)内の関係詞節 - 条件を大幅緩和
        if 'S' in main_slots and main_slots['S'].strip():
            s_text = main_slots['S'].strip()
            print(f"\n1️⃣ 主語(S)内関係詞節分析: {s_text}")
            
            # 関係代名詞の検出を柔軟化
            if any(rel in s_text for rel in ['who', 'which', 'that', 'whose', 'whom']):
                relative_result = self._decompose_relative_clause(s_text)
                if relative_result and relative_result.sub_slots:
                    sub_slot_results['S'] = [relative_result]
                    print(f"   🎯 関係詞節抽出: {relative_result.original_text}")
            else:
                print("   ❌ 関係詞節なし")
        
        # 2. 修飾語(M2)内の副詞節 - 空でない場合は処理
        if 'M2' in main_slots and main_slots['M2'].strip():
            m2_text = main_slots['M2'].strip()
            print(f"\n2️⃣ 修飾語(M2)内副詞節分析: {m2_text}")
            adverbial_result = self._decompose_adverbial_clause(m2_text)
            if adverbial_result and (adverbial_result.sub_slots or len(m2_text) > 3):
                sub_slot_results['M2'] = [adverbial_result]
        else:
            print(f"\n2️⃣ 修飾語(M2)内副詞節分析: ")
            # 空の場合でもデフォルトサブスロット生成
            sub_slot_results['M2'] = [SubSlotResult(
                clause_type="adverbial_clause",
                original_text="",
                sub_slots={},
                confidence=0.90
            )]
        
        # 3. 修飾語(M3)内の副詞節 - 空でない場合は処理
        if 'M3' in main_slots and main_slots['M3'].strip():
            m3_text = main_slots['M3'].strip()
            print(f"\n3️⃣ 修飾語(M3)内副詞節分析: {m3_text}")
            adverbial_result = self._decompose_adverbial_clause(m3_text)
            if adverbial_result and (adverbial_result.sub_slots or len(m3_text) > 3):
                sub_slot_results['M3'] = [adverbial_result]
        else:
            print(f"\n3️⃣ 修飾語(M3)内副詞節分析: ")
            # 空の場合でもデフォルトサブスロット生成
            sub_slot_results['M3'] = [SubSlotResult(
                clause_type="adverbial_clause",
                original_text="",
                sub_slots={},
                confidence=0.90
            )]
        
        # 4. 補語(C2)内のサブスロット分解 - 空でない場合は処理
        if 'C2' in main_slots and main_slots['C2'].strip():
            c2_text = main_slots['C2'].strip()
            print(f"\n4️⃣ 補語(C2)内サブスロット分析: {c2_text}")
            complement_result = self._decompose_complement_phrase(c2_text)
            if complement_result and (complement_result.sub_slots or len(c2_text) > 3):
                sub_slot_results['C2'] = [complement_result]
        else:
            print(f"\n4️⃣ 補語(C2)内サブスロット分析: ")
            # 空の場合でもデフォルトサブスロット生成
            sub_slot_results['C2'] = [SubSlotResult(
                clause_type="complement_phrase",
                original_text="",
                sub_slots={},
                confidence=0.95
            )]
        
        print("\n✅ サブスロット分解完了")
        
        # 🔧 重要: サブスロットがある上位スロットを空にする
        self._clear_upper_slots_with_subs(main_slots, sub_slot_results)
        
        return sub_slot_results
    
    def _clear_upper_slots_with_subs(self, main_slots: Dict[str, str], sub_slot_results: Dict[str, List[SubSlotResult]]):
        """サブスロットがある上位スロットを空にする"""
        print("\n🔧 上位スロットクリア処理開始")
        
        for slot_name in sub_slot_results.keys():
            if slot_name in main_slots and main_slots[slot_name].strip():
                original_content = main_slots[slot_name]
                main_slots[slot_name] = ""  # 上位スロットを空にする
                print(f"  ✅ {slot_name}スロット: '{original_content}' → 空 (サブスロット有のため)")
        
        print("🔧 上位スロットクリア処理完了")
    
    def _decompose_relative_clause(self, text: str) -> SubSlotResult:
        """関係詞節のサブスロット分解（正しいRephraseルール準拠）"""
        doc = self.nlp(text)
        
        # 関係詞節部分を抽出
        relative_clause = self._extract_relative_clause_text(text)
        if not relative_clause:
            return None
        
        print(f"   🎯 関係詞節抽出: {relative_clause}")
        
        # 🎯 正しいRephraseルール：
        # "The book that I bought" →
        # sub_O1: "the book that" (関係詞節内の目的語=先行詞)
        # sub_S: "I" (関係詞節内の主語)
        # sub_V: "bought" (関係詞節内動詞)
        #
        # "The person who knows me" →
        # sub_S: "the person who" (関係詞節内の主語=先行詞+関係代名詞)
        # sub_V: "knows" (関係詞節内動詞)
        # sub_O1: "me" (関係詞節内目的語)
        
        sub_slots = {}
        
        # 先行詞を抽出
        antecedent = self._extract_antecedent_from_full_text(text, relative_clause)
        
        # 関係代名詞を特定
        relative_pronouns = ['who', 'which', 'that', 'whose', 'whom']
        rel_pronoun = ""
        for rel_pron in relative_pronouns:
            if relative_clause.strip().startswith(rel_pron):
                rel_pronoun = rel_pron
                break
        
        # 関係詞節の構文解析
        rel_doc = self.nlp(relative_clause)
        
        # 関係代名詞の機能を判定（主語か目的語か）
        is_subject_relative = False
        is_object_relative = False
        
        # 関係詞節内の実際の主語を検出
        actual_subject = ""
        for token in rel_doc:
            if token.dep_ == 'nsubj' and token.text.lower() not in relative_pronouns:
                actual_subject = token.text  # "I"
                is_object_relative = True  # 別の語が主語 = 関係代名詞は目的語
                break
        
        if not actual_subject and rel_pronoun in ['who', 'which', 'that']:
            is_subject_relative = True  # 関係代名詞が主語
        
        # サブスロット分解
        if is_object_relative:
            # 目的格関係代名詞の場合: "The book that I bought"
            sub_slots['sub_O1'] = f"{antecedent} {rel_pronoun}"  # "the book that"
            sub_slots['sub_S'] = actual_subject  # "I"
        elif is_subject_relative:
            # 主格関係代名詞の場合: "The person who knows me"
            sub_slots['sub_S'] = f"{antecedent} {rel_pronoun}"  # "the person who"
        
        # sub_V: 関係詞節内の動詞
        for token in rel_doc:
            if token.dep_ == 'ROOT' and token.pos_ in ['VERB', 'AUX']:
                sub_slots['sub_V'] = token.text  # "bought" or "knows"
                break
        
        # sub_Aux: 助動詞
        aux_parts = []
        for token in rel_doc:
            if token.dep_ == 'aux':
                aux_parts.append(token.text)
        if aux_parts:
            sub_slots['sub_Aux'] = ' '.join(aux_parts)
        
        # sub_M2: 副詞
        for token in rel_doc:
            if token.dep_ == 'advmod':
                sub_slots['sub_M2'] = token.text
                break
        
        # sub_O1: 関係詞節内の目的語（主格関係代名詞の場合のみ）
        if is_subject_relative:
            for token in rel_doc:
                if token.dep_ == 'dobj':
                    obj_phrase = self._extract_complete_object_phrase(token, rel_doc)
                    sub_slots['sub_O1'] = obj_phrase  # "me"
                    break
        
        return SubSlotResult(
            clause_type="relative_clause",
            original_text=relative_clause,
            sub_slots=sub_slots,
            confidence=0.95
        )
    
    def _extract_antecedent_from_full_text(self, full_text: str, relative_clause: str) -> str:
        """完全なテキストから先行詞を抽出"""
        # 関係詞節より前の部分を取得
        rel_start = full_text.find(relative_clause)
        if rel_start > 0:
            antecedent_part = full_text[:rel_start].strip()
            # 最後の名詞句を抽出
            words = antecedent_part.split()
            if words:
                # 冠詞+名詞の形で抽出
                if len(words) >= 2 and words[-2].lower() in ['the', 'a', 'an']:
                    return f"{words[-2]} {words[-1]}"
                else:
                    return words[-1]
        return ""
    
    def _decompose_adverbial_clause(self, text: str) -> SubSlotResult:
        """副詞節のサブスロット分解"""
        doc = self.nlp(text)
        sub_slots = {}
        
        # 接続詞を検出
        conjunction = self._extract_conjunction(text)
        if conjunction:
            sub_slots['sub_M1'] = conjunction
        
        # 主語を検出
        for token in doc:
            if token.dep_ == 'nsubj':
                # 完全な主語句を抽出
                subject_phrase = self._extract_noun_phrase(token, doc)
                sub_slots['sub_S'] = subject_phrase
                break
        
        # 助動詞を検出
        aux_parts = []
        for token in doc:
            if token.dep_ == 'aux':
                aux_parts.append(token.text)
        if aux_parts:
            sub_slots['sub_Aux'] = ' '.join(aux_parts)
        
        # 動詞を検出
        main_verb = None
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ != 'aux':
                main_verb = token.text
                break
        if not main_verb:
            for token in doc:
                if token.pos_ == 'AUX' and token.dep_ == 'ROOT':
                    main_verb = token.text
                    break
        if main_verb:
            sub_slots['sub_V'] = main_verb
        
        # 目的語を検出
        for token in doc:
            if token.dep_ == 'dobj':
                obj_phrase = self._extract_noun_phrase(token, doc)
                sub_slots['sub_O1'] = obj_phrase
                break
        
        # 前置詞句を検出
        prep_phrases = []
        for token in doc:
            if token.dep_ == 'prep':
                prep_phrase = self._extract_prep_phrase(token, doc)
                if prep_phrase and conjunction not in prep_phrase:
                    prep_phrases.append(prep_phrase)
        if prep_phrases:
            # M2スロットの場合は sub_M2 に設定 (M3ではなく)
            sub_slots['sub_M2'] = ' '.join(prep_phrases)
        
        return SubSlotResult(
            clause_type="adverbial_clause",
            original_text=text,
            sub_slots=sub_slots,
            confidence=0.90
        )
    
    def _decompose_complement_phrase(self, text: str) -> SubSlotResult:
        """補語句のサブスロット分解 (deliver the final proposal flawlessly)"""
        doc = self.nlp(text)
        sub_slots = {}
        
        # 動詞を検出 (sub_V)
        main_verb = None
        for token in doc:
            if token.pos_ == 'VERB':
                main_verb = token
                sub_slots['sub_V'] = token.text
                break
        
        # 目的語を検出 (sub_O1)
        if main_verb:
            for child in main_verb.children:
                if child.dep_ == 'dobj':
                    obj_phrase = self._extract_noun_phrase(child, doc)
                    sub_slots['sub_O1'] = obj_phrase
                    break
        
        # 修飾語を検出 (sub_M3)
        for token in doc:
            if token.dep_ == 'advmod':
                sub_slots['sub_M3'] = token.text
                break
        
        return SubSlotResult(
            clause_type="complement_phrase",
            original_text=text,
            sub_slots=sub_slots,
            confidence=0.95
        )
    
    def _extract_relative_clause_text(self, text: str) -> str:
        """関係詞節部分のテキストを抽出（改良版）"""
        relative_pronouns = ['who', 'which', 'that', 'whose', 'whom']
        
        for rel_pron in relative_pronouns:
            if f' {rel_pron} ' in text or text.startswith(rel_pron + ' '):
                rel_index = text.find(f' {rel_pron} ')
                if rel_index == -1:  # 文頭の場合
                    rel_index = text.find(rel_pron + ' ') - 1
                
                # 関係詞節の範囲を特定
                clause_start = rel_index + 1
                clause_text = text[clause_start:].strip()
                
                # 関係詞節の終了を検出（動詞を含む完全な節）
                words = clause_text.split()
                if len(words) >= 2:  # 最低限「who was」のような構造
                    # 動詞が含まれているか確認
                    doc = self.nlp(clause_text)
                    has_verb = any(token.pos_ in ['VERB', 'AUX'] for token in doc)
                    if has_verb:
                        return clause_text
                    else:
                        # 動詞がない場合は、最初の動詞まで延長を試行
                        remaining_text = text[clause_start:].strip()
                        return remaining_text
                
                return clause_text
        
        return ""
    
    def _extract_conjunction(self, text: str) -> str:
        """接続詞を抽出"""
        conjunctions = ['even though', 'though', 'although', 'so', 'because', 'since', 'while', 'when']
        
        for conj in conjunctions:
            if text.lower().startswith(conj):
                return conj
        
        # 単一語の接続詞
        words = text.split()
        if words and words[0].lower() in ['so', 'because', 'since', 'while', 'when']:
            return words[0]
        
        return ""
    
    def _extract_noun_phrase(self, head_token, doc) -> str:
        """名詞句を抽出"""
        phrase_tokens = []
        
        # 修飾語を収集
        for child in head_token.children:
            if child.dep_ in ['det', 'amod', 'poss']:
                phrase_tokens.append((child.i, child.text))
        
        # ヘッド語
        phrase_tokens.append((head_token.i, head_token.text))
        
        # 後置修飾語
        for child in head_token.children:
            if child.dep_ in ['nmod', 'amod'] and child.i > head_token.i:
                phrase_tokens.append((child.i, child.text))
        
        # 位置でソート
        phrase_tokens.sort()
        return ' '.join([text for _, text in phrase_tokens])
    
    def _extract_prep_phrase(self, prep_token, doc) -> str:
        """前置詞句を抽出"""
        phrase_parts = [prep_token.text]
        
        # 前置詞の目的語を取得
        for child in prep_token.children:
            if child.dep_ == 'pobj':
                obj_phrase = self._extract_noun_phrase(child, doc)
                phrase_parts.append(obj_phrase)
        
        return ' '.join(phrase_parts)
    
    def _extract_complete_object_phrase(self, obj_token, doc) -> str:
        """目的語の完全な句を抽出（前置詞句含む）"""
        phrase_parts = [obj_token.text]
        
        # 目的語に付随する前置詞句を収集
        for child in obj_token.children:
            if child.dep_ == 'prep':
                prep_phrase = self._extract_prep_phrase(child, doc)
                phrase_parts.append(prep_phrase)
        
        return ' '.join(phrase_parts)
    
    def print_sub_slot_analysis(self, main_slots: Dict[str, str], sub_slot_results: Dict[str, List[SubSlotResult]]):
        """サブスロット分析結果を表示"""
        print("\n" + "="*60)
        print("🔍 サブスロット分解結果詳細")
        print("="*60)
        
        for main_slot, sub_results in sub_slot_results.items():
            print(f"\n📌 【{main_slot}スロット】: {main_slots[main_slot]}")
            
            for i, sub_result in enumerate(sub_results, 1):
                print(f"\n   {i}. {sub_result.clause_type} (信頼度: {sub_result.confidence:.1%})")
                print(f"      原文: {sub_result.original_text}")
                print(f"      サブスロット分解:")
                
                for sub_slot, value in sub_result.sub_slots.items():
                    print(f"        {sub_slot}: {value}")
