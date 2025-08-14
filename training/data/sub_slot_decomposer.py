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
        """メインスロットから複文箇所を検出してサブスロット分解"""
        sub_slot_results = {}
        
        print("\n🔍 複文箇所検出・サブスロット分解開始")
        
        # 1. 主語(S)内の関係詞節
        if 'S' in main_slots and ('who' in main_slots['S'] or 'which' in main_slots['S']):
            print(f"\n1️⃣ 主語(S)内関係詞節分析: {main_slots['S']}")
            relative_result = self._decompose_relative_clause(main_slots['S'])
            if relative_result:
                sub_slot_results['S'] = [relative_result]
        
        # 2. 修飾語(M2)内の副詞節
        if 'M2' in main_slots:
            print(f"\n2️⃣ 修飾語(M2)内副詞節分析: {main_slots['M2']}")
            adverbial_result = self._decompose_adverbial_clause(main_slots['M2'])
            if adverbial_result:
                sub_slot_results['M2'] = [adverbial_result]
        
        # 3. 修飾語(M3)内の副詞節
        if 'M3' in main_slots:
            print(f"\n3️⃣ 修飾語(M3)内副詞節分析: {main_slots['M3']}")
            adverbial_result = self._decompose_adverbial_clause(main_slots['M3'])
            if adverbial_result:
                sub_slot_results['M3'] = [adverbial_result]
        
        # 4. 補語(C2)内のサブスロット分解
        if 'C2' in main_slots:
            print(f"\n4️⃣ 補語(C2)内サブスロット分析: {main_slots['C2']}")
            complement_result = self._decompose_complement_phrase(main_slots['C2'])
            if complement_result:
                sub_slot_results['C2'] = [complement_result]
        
        print("\n✅ サブスロット分解完了")
        return sub_slot_results
    
    def _decompose_relative_clause(self, text: str) -> SubSlotResult:
        """関係詞節のサブスロット分解"""
        doc = self.nlp(text)
        
        # 関係詞節部分を抽出
        relative_clause = self._extract_relative_clause_text(text)
        if not relative_clause:
            return None
        
        print(f"   🎯 関係詞節抽出: {relative_clause}")
        
        # 関係詞節をサブスロット分解
        sub_slots = {}
        rel_doc = self.nlp(relative_clause)
        
        # サブS (関係代名詞 + 先行詞)
        # 完全な主語句を取得（先行詞 + 関係代名詞）
        main_text = text  # "the manager who had recently taken charge..."
        relative_clause = self._extract_relative_clause_text(text)  # "who had recently taken charge..."
        
        # 先行詞部分を抽出
        if relative_clause:
            antecedent_end_idx = text.find(relative_clause)
            antecedent = text[:antecedent_end_idx].strip()  # "the manager"
            relative_pronoun = relative_clause.split()[0]  # "who"
            sub_slots['sub_S'] = f"{antecedent} {relative_pronoun}"  # "the manager who"
        else:
            # フォールバック: 関係代名詞のみ
            for token in rel_doc:
                if token.dep_ == 'nsubj' and token.pos_ == 'PRON':
                    sub_slots['sub_S'] = token.text
                    break
        
        # サブAux (助動詞)
        aux_parts = []
        for token in rel_doc:
            if token.dep_ == 'aux':
                aux_parts.append(token.text)
        if aux_parts:
            sub_slots['sub_Aux'] = ' '.join(aux_parts)
        
        # サブV (動詞)
        for token in rel_doc:
            if token.dep_ == 'ROOT':
                sub_slots['sub_V'] = token.text
                break
        
        # サブM2 (副詞)
        for token in rel_doc:
            if token.dep_ == 'advmod':
                sub_slots['sub_M2'] = token.text
                break
        
        # サブO1 (目的語) - 前置詞句も含む完全な目的語
        for token in rel_doc:
            if token.dep_ == 'dobj':
                # 目的語の完全な句を抽出（前置詞句含む）
                obj_phrase = self._extract_complete_object_phrase(token, rel_doc)
                sub_slots['sub_O1'] = obj_phrase
                break
        
        return SubSlotResult(
            clause_type="relative_clause",
            original_text=relative_clause,
            sub_slots=sub_slots,
            confidence=0.95
        )
    
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
        """関係詞節部分のテキストを抽出"""
        if 'who' in text:
            who_index = text.find('who')
            return text[who_index:].strip()
        elif 'which' in text:
            which_index = text.find('which')
            return text[which_index:].strip()
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
