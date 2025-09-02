"""
動名詞ハンドラー - spaCy依存関係分析による完全実装
Gerund constructions handler using spaCy dependency parsing
人間的文法認識システム - Human Grammar Pattern Recognition System

動名詞の3つの用法:
1. 主語として使用: "Swimming is fun."
2. 目的語として使用: "I enjoy reading."
3. 前置詞の目的語として使用: "I'm interested in learning."
"""

import spacy
import re
from typing import Dict, List, Any, Optional, Tuple

class GerundHandler:
    def __init__(self, nlp=None, collaborators=None):
        """
        動名詞ハンドラーの初期化
        spaCy NLPモデルを使用した依存関係分析
        """
        self.name = "GerundHandler"
        self.version = "v1.0"
        
        if nlp is None:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = spacy.load("en_core_web_md")
        else:
            self.nlp = nlp
            
        # 協力者ハンドラー設定
        self.collaborators = collaborators or {}
        
        # 動名詞を取る動詞パターン（Human Grammar Pattern）
        self.gerund_taking_verbs = {
            # 直後に動名詞を取る動詞
            'enjoy', 'finish', 'avoid', 'consider', 'suggest', 'recommend',
            'admit', 'deny', 'imagine', 'mind', 'practice', 'quit', 'risk',
            'appreciate', 'delay', 'involve', 'postpone', 'resist', 'miss',
            'keep', 'stop', 'give up', 'put off'
        }
        
        # 前置詞 + 動名詞パターン
        self.preposition_gerund_patterns = {
            'be interested in', 'be good at', 'be afraid of', 'be worried about',
            'thank you for', 'apologize for', 'responsible for', 'famous for',
            'instead of', 'in spite of', 'because of', 'after', 'before',
            'without', 'by', 'through', 'upon', 'about', 'of', 'for', 'in'
        }

    def can_handle(self, sentence: str) -> bool:
        """
        動名詞構造を含む文かどうかを判定
        spaCyの品詞分析で VBG (動名詞) パターンを検出
        """
        doc = self.nlp(sentence)
        
        # デバッグ用：全トークンの品詞を確認
        print(f"🔍 トークン分析: '{sentence}'")
        for token in doc:
            print(f"   '{token.text}' - POS: {token.pos_}, TAG: {token.tag_}, DEP: {token.dep_}")
        
        for token in doc:
            # VBG (動名詞/現在分詞) の検出
            if token.tag_ == "VBG":
                # 動名詞としての用法を判定
                if self._is_gerund_usage(token, doc):
                    print(f"✅ 動名詞検出: '{token.text}' ({token.dep_})")
                    return True
                else:
                    print(f"⚠️ VBGだが動名詞ではない: '{token.text}' ({token.dep_})")
            
            # 特殊ケース：NOUN として分類される動名詞も考慮
            elif token.pos_ == "NOUN" and token.text.endswith("ing"):
                # 語幹が動詞かチェック
                stem = token.text[:-3]  # "ing" を除去
                if self._is_verb_stem(stem, doc):
                    print(f"✅ NOUN分類の動名詞検出: '{token.text}'")
                    return True
                    
        print(f"❌ 動名詞構造なし: '{sentence}'")
        return False

    def _is_gerund_usage(self, token, doc) -> bool:
        """
        VBGトークンが動名詞として使用されているかを判定
        依存関係解析による文法的役割の特定
        """
        # 主語位置の動名詞: "Swimming is fun." / "Reading books is my hobby."
        if token.dep_ in ["nsubj", "nsubjpass", "csubj"]:
            return True
            
        # 目的語位置の動名詞: "I enjoy reading."
        if token.dep_ in ["dobj", "ccomp", "xcomp"]:
            # xcompの場合は親動詞が動名詞を取る動詞かチェック
            if token.dep_ == "xcomp" and token.head.lemma_ in self.gerund_taking_verbs:
                return True
            elif token.dep_ in ["dobj", "ccomp"]:
                return True
            
        # 前置詞の目的語: "interested in learning"
        if token.dep_ in ["pobj", "pcomp"]:
            return True
            
        # 補語位置: "My hobby is reading"
        if token.dep_ in ["attr", "acomp"]:
            return True
            
        # ROOTだが実際は補語として機能している場合（spaCy解析の例外）
        if token.dep_ == "ROOT" and token.head == token:
            # 前に主語がある場合は補語の可能性
            for prev_token in doc:
                if prev_token.i < token.i and prev_token.dep_ == "nsubj":
                    return True
            
        return False

    def _is_verb_stem(self, stem: str, doc) -> bool:
        """
        語幹が動詞かどうかを判定
        """
        # 基本的な動詞の語幹リスト
        common_verb_stems = {
            'swim', 'run', 'walk', 'read', 'write', 'learn', 'teach', 'play',
            'work', 'study', 'help', 'talk', 'speak', 'listen', 'watch', 'see',
            'cook', 'eat', 'drink', 'sleep', 'drive', 'travel', 'shop', 'buy'
        }
        
        return stem.lower() in common_verb_stems

    def handle(self, sentence: str, v_group_key: str) -> Dict[str, Any]:
        """
        動名詞構造の解析とスロット分解
        spaCy依存関係による汎用的アプローチ
        """
        if not self.can_handle(sentence):
            return self._create_failure_result("No gerund construction detected")
        
        doc = self.nlp(sentence)
        print(f"\n🔍 動名詞ハンドラー処理開始: '{sentence}'")
        
        # 動名詞パターンの特定
        gerund_pattern = self._identify_gerund_pattern(doc)
        
        if gerund_pattern["type"] == "subject_gerund":
            return self._handle_subject_gerund(doc, sentence, v_group_key, gerund_pattern)
        elif gerund_pattern["type"] == "object_gerund":
            return self._handle_object_gerund(doc, sentence, v_group_key, gerund_pattern)
        elif gerund_pattern["type"] == "prepositional_gerund":
            return self._handle_prepositional_gerund(doc, sentence, v_group_key, gerund_pattern)
        elif gerund_pattern["type"] == "complement_gerund":
            return self._handle_complement_gerund(doc, sentence, v_group_key, gerund_pattern)
        else:
            return self._create_failure_result(f"Unknown gerund pattern: {gerund_pattern['type']}")

    def _identify_gerund_pattern(self, doc) -> Dict[str, Any]:
        """
        動名詞パターンの特定
        Human Grammar Pattern Recognition
        """
        for token in doc:
            if token.tag_ == "VBG" and self._is_gerund_usage(token, doc):
                
                # 主語位置の動名詞
                if token.dep_ in ["nsubj", "nsubjpass", "csubj"]:
                    return {
                        "type": "subject_gerund",
                        "gerund_token": token,
                        "main_verb": token.head,
                        "pattern": "S[gerund] + V + ..."
                    }
                
                # 目的語位置の動名詞 (xcompも含む)
                elif token.dep_ in ["dobj", "ccomp", "xcomp"]:
                    return {
                        "type": "object_gerund", 
                        "gerund_token": token,
                        "main_verb": token.head,
                        "pattern": "S + V + O[gerund]"
                    }
                
                # 前置詞の目的語 (pcompも含む)
                elif token.dep_ in ["pobj", "pcomp"]:
                    return {
                        "type": "prepositional_gerund",
                        "gerund_token": token,
                        "preposition": token.head,
                        "pattern": "... + PREP + gerund"
                    }
                
                # 補語位置
                elif token.dep_ in ["attr", "acomp"]:
                    return {
                        "type": "complement_gerund",
                        "gerund_token": token,
                        "main_verb": token.head,
                        "pattern": "S + be + C[gerund]"
                    }
                
                # ROOTだが実際は補語として機能
                elif token.dep_ == "ROOT" and any(t.dep_ == "nsubj" and t.i < token.i for t in doc):
                    # be動詞を探す
                    be_verb = None
                    for t in doc:
                        if t.lemma_ == "be" and t.i < token.i:
                            be_verb = t
                            break
                    return {
                        "type": "complement_gerund",
                        "gerund_token": token,
                        "main_verb": be_verb or token,
                        "pattern": "S + be + C[gerund]"
                    }
        
        return {"type": "unknown", "gerund_token": None}

    def _handle_subject_gerund(self, doc, sentence: str, v_group_key: str, pattern: Dict) -> Dict[str, Any]:
        """
        主語位置の動名詞処理: "Swimming is fun." / "Reading books is my hobby."
        Rephraseルール: V要素があるものはサブスロット化
        """
        print(f"📋 主語動名詞パターン処理: {pattern['pattern']}")
        
        main_slots = {}
        sub_slots = {}
        
        gerund_token = pattern["gerund_token"]
        main_verb = pattern["main_verb"]
        
        # 動名詞が単体か句かを判定
        has_objects_or_modifiers = self._gerund_has_objects_or_modifiers(gerund_token)
        
        if has_objects_or_modifiers:
            # V要素（動詞的要素）があるのでサブスロット化
            print(f"   V要素を含む動名詞句 → サブスロット化")
            main_slots["S"] = ""  # 上位スロットは空
            
            # サブスロットに分解
            sub_slots["sub-v"] = gerund_token.text
            sub_slots["_parent_slot"] = "S"
            
            # 動名詞の目的語・修飾語をサブスロットに配置
            self._extract_gerund_elements_to_subslots(gerund_token, sub_slots)
            
        else:
            # 単体動名詞は上位スロットに直接配置
            print(f"   単体動名詞 → 上位スロット配置")
            main_slots["S"] = gerund_token.text
        
        # 主文の動詞・補語
        main_slots["V"] = main_verb.text
        self._process_main_clause_elements(main_verb, doc, main_slots)
        
        # 修飾語の処理（協力者ハンドラー使用）
        if 'adverb' in self.collaborators:
            adverb_result = self.collaborators['adverb'].handle(sentence, v_group_key)
            if adverb_result.get('success', False):
                self._merge_adverb_slots(main_slots, adverb_result.get('main_slots', {}))
        
        description = f"Subject gerund ({'complex' if has_objects_or_modifiers else 'simple'})"
        return self._create_success_result(main_slots, sub_slots, v_group_key, description)

    def _handle_object_gerund(self, doc, sentence: str, v_group_key: str, pattern: Dict) -> Dict[str, Any]:
        """
        目的語位置の動名詞処理: "I enjoy cooking." / "I enjoy reading books."
        Rephraseルール: V要素があるものはサブスロット化
        """
        print(f"📋 目的語動名詞パターン処理: {pattern['pattern']}")
        
        main_slots = {}
        sub_slots = {}
        
        gerund_token = pattern["gerund_token"]
        main_verb = pattern["main_verb"]
        
        # 主文の主語・動詞の特定
        subject = self._find_subject(main_verb, doc)
        if subject:
            main_slots["S"] = subject.text
            print(f"   主語: '{subject.text}'")
        
        main_slots["V"] = main_verb.text
        print(f"   動詞: '{main_verb.text}'")
        
        # 動名詞が単体か句かを判定
        has_objects_or_modifiers = self._gerund_has_objects_or_modifiers(gerund_token)
        
        if has_objects_or_modifiers:
            # V要素（動詞的要素）があるのでサブスロット化
            print(f"   V要素を含む動名詞句 → サブスロット化")
            main_slots["O1"] = ""  # 上位スロットは空
            
            # サブスロットに分解
            sub_slots["sub-v"] = gerund_token.text
            sub_slots["_parent_slot"] = "O1"
            
            # 動名詞の目的語・修飾語をサブスロットに配置
            self._extract_gerund_elements_to_subslots(gerund_token, sub_slots)
            
        else:
            # 単体動名詞は上位スロットに直接配置
            print(f"   単体動名詞 → 上位スロット配置")
            main_slots["O1"] = gerund_token.text
        
        # その他の補語・修飾語の処理
        self._process_main_clause_elements(main_verb, doc, main_slots, exclude_dobj=True)
        
        # 修飾語の処理
        if 'adverb' in self.collaborators:
            adverb_result = self.collaborators['adverb'].handle(sentence, v_group_key)
            if adverb_result.get('success', False):
                self._merge_adverb_slots(main_slots, adverb_result.get('main_slots', {}))
        
        description = f"Object gerund ({'complex' if has_objects_or_modifiers else 'simple'})"
        return self._create_success_result(main_slots, sub_slots, v_group_key, description)

    def _handle_prepositional_gerund(self, doc, sentence: str, v_group_key: str, pattern: Dict) -> Dict[str, Any]:
        """
        前置詞の目的語位置の動名詞処理: "I'm interested in learning English."
        Rephraseルール: V要素があるものはサブスロット化
        """
        print(f"📋 前置詞動名詞パターン処理: {pattern['pattern']}")
        
        main_slots = {}
        sub_slots = {}
        
        gerund_token = pattern["gerund_token"]
        preposition = pattern["preposition"]
        
        # 主文の主要要素を特定
        main_verb = self._find_main_verb(doc)
        if main_verb:
            main_slots["V"] = main_verb.text
            print(f"   主動詞: '{main_verb.text}'")
            
            # 主語の特定
            subject = self._find_subject(main_verb, doc)
            if subject:
                main_slots["S"] = subject.text
                print(f"   主語: '{subject.text}'")
        
        # 主動詞が見つからない場合、be動詞を探す
        if not main_verb:
            for token in doc:
                if token.lemma_ == "be" and token.pos_ in ["AUX", "VERB"]:
                    main_verb = token
                    main_slots["V"] = token.text
                    print(f"   補助動詞: '{token.text}'")
                    
                    # この場合の主語と形容詞補語も特定
                    for child in token.children:
                        if child.dep_ == "nsubj":
                            main_slots["S"] = child.text
                            print(f"   主語: '{child.text}'")
                        elif child.dep_ == "acomp":
                            main_slots["C1"] = child.text
                            print(f"   形容詞補語: '{child.text}'")
                    break
        
        # 動名詞が単体か句かを判定
        has_objects_or_modifiers = self._gerund_has_objects_or_modifiers(gerund_token)
        
        # 前置詞句の文法的役割を判定
        prep_role = self._determine_prep_phrase_role(preposition, doc)
        target_slot = "C2" if prep_role == "complement" else "M2"
        
        if has_objects_or_modifiers:
            # V要素（動詞的要素）があるのでサブスロット化
            print(f"   V要素を含む前置詞動名詞句 → サブスロット化")
            main_slots[target_slot] = ""  # 上位スロットは空
            
            # サブスロットに分解
            sub_slots["sub-m2"] = preposition.text  # 前置詞部分
            sub_slots["sub-v"] = gerund_token.text   # 動名詞部分
            sub_slots[f"_parent_slot"] = target_slot
            
            # 動名詞の目的語・修飾語をサブスロットに配置
            self._extract_gerund_elements_to_subslots(gerund_token, sub_slots)
            
        else:
            # 単体動名詞 + 前置詞は上位スロットに直接配置
            print(f"   単体前置詞動名詞 → 上位スロット配置")
            prep_phrase = f"{preposition.text} {gerund_token.text}"
            main_slots[target_slot] = prep_phrase
        
        # その他の要素の処理
        self._process_main_clause_elements(main_verb, doc, main_slots, exclude_prep=preposition)
        
        description = f"Prepositional gerund ({'complex' if has_objects_or_modifiers else 'simple'})"
        return self._create_success_result(main_slots, sub_slots, v_group_key, description)

    def _handle_complement_gerund(self, doc, sentence: str, v_group_key: str, pattern: Dict) -> Dict[str, Any]:
        """
        補語位置の動名詞処理: "My hobby is reading novels."
        Rephraseルール: V要素があるものはサブスロット化
        """
        print(f"📋 補語動名詞パターン処理: {pattern['pattern']}")
        
        main_slots = {}
        sub_slots = {}
        
        gerund_token = pattern["gerund_token"]
        main_verb = pattern["main_verb"]
        
        # 主語の特定
        subject = self._find_subject(main_verb, doc)
        if subject:
            main_slots["S"] = subject.text
            print(f"   主語: '{subject.text}'")
        else:
            # be動詞の場合、直接の主語を探す
            for token in doc:
                if token.dep_ == "nsubj":
                    # 所有詞がある場合は含める
                    subject_text = token.text
                    for child in token.children:
                        if child.dep_ == "poss":
                            subject_text = f"{child.text} {token.text}"
                            break
                    main_slots["S"] = subject_text
                    print(f"   主語: '{subject_text}'")
                    break
        
        main_slots["V"] = main_verb.text
        print(f"   動詞: '{main_verb.text}'")
        
        # 動名詞が単体か句かを判定
        has_objects_or_modifiers = self._gerund_has_objects_or_modifiers(gerund_token)
        
        if has_objects_or_modifiers:
            # V要素（動詞的要素）があるのでサブスロット化
            print(f"   V要素を含む補語動名詞句 → サブスロット化")
            main_slots["C1"] = ""  # 上位スロットは空
            
            # サブスロットに分解
            sub_slots["sub-v"] = gerund_token.text
            sub_slots["_parent_slot"] = "C1"
            
            # 動名詞の目的語・修飾語をサブスロットに配置
            self._extract_gerund_elements_to_subslots(gerund_token, sub_slots)
            
        else:
            # 単体動名詞は上位スロットに直接配置
            print(f"   単体補語動名詞 → 上位スロット配置")
            main_slots["C1"] = gerund_token.text
        
        # その他の要素の処理
        self._process_main_clause_elements(main_verb, doc, main_slots, exclude_attr=True)
        
        description = f"Complement gerund ({'complex' if has_objects_or_modifiers else 'simple'})"
        return self._create_success_result(main_slots, sub_slots, v_group_key, description)

    def _gerund_has_objects_or_modifiers(self, gerund_token) -> bool:
        """
        動名詞が目的語や修飾語を持つかどうかを判定
        V要素があるかどうかの判定（Rephraseルール）
        """
        for child in gerund_token.children:
            if child.dep_ in ["dobj", "pobj", "advmod", "amod", "compound", "prep"]:
                return True
        return False

    def _extract_gerund_elements_to_subslots(self, gerund_token, sub_slots):
        """
        動名詞の要素（目的語・修飾語）をサブスロットに抽出
        """
        for child in gerund_token.children:
            if child.dep_ == "dobj":
                # 直接目的語
                sub_slots["sub-o1"] = child.text
                print(f"   動名詞の目的語: '{child.text}'")
            elif child.dep_ == "prep":
                # 前置詞句
                prep_phrase = self._build_prep_phrase(child)
                sub_slots["sub-m2"] = prep_phrase
                print(f"   動名詞の前置詞句: '{prep_phrase}'")
            elif child.dep_ in ["advmod", "amod"]:
                # 修飾語
                if not sub_slots.get("sub-m2"):
                    sub_slots["sub-m2"] = child.text
                else:
                    sub_slots["sub-m3"] = child.text
                print(f"   動名詞の修飾語: '{child.text}'")

    def _build_gerund_phrase(self, gerund_token, doc) -> str:
        """
        動名詞句の構築（修飾語・目的語を含む）
        "reading books quickly" のような完全な句を構築
        """
        phrase_tokens = [gerund_token]
        
        # 動名詞の子要素（目的語・修飾語）を収集
        for child in gerund_token.children:
            if child.dep_ in ["dobj", "pobj", "advmod", "amod", "det", "poss", "compound"]:
                phrase_tokens.extend(self._collect_subtree(child))
        
        # トークンを文中の順序でソート
        phrase_tokens.sort(key=lambda x: x.i)
        
        # フレーズの構築
        return " ".join([token.text for token in phrase_tokens])

    def _collect_subtree(self, token) -> List:
        """
        トークンの下位ツリー全体を収集
        """
        subtree = [token]
        for child in token.children:
            subtree.extend(self._collect_subtree(child))
        return subtree

    def _find_main_verb(self, doc):
        """
        文の主動詞を特定
        """
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                return token
        return None

    def _find_subject(self, verb, doc):
        """
        動詞の主語を特定
        """
        for child in verb.children:
            if child.dep_ in ["nsubj", "nsubjpass"]:
                return child
        return None

    def _process_main_clause_elements(self, main_verb, doc, main_slots, exclude_dobj=False, exclude_attr=False, exclude_prep=None):
        """
        主文の要素（補語、目的語、修飾語）を処理
        """
        if not main_verb:
            return
            
        for child in main_verb.children:
            # 直接目的語（exclude_dobjが True の場合はスキップ）
            if child.dep_ == "dobj" and not exclude_dobj and not main_slots.get("O1"):
                main_slots["O1"] = child.text
                
            # 間接目的語
            elif child.dep_ == "iobj" and not main_slots.get("O2"):
                main_slots["O2"] = child.text
                
            # 属詞補語（exclude_attrが True の場合はスキップ）
            elif child.dep_ == "attr" and not exclude_attr and not main_slots.get("C1"):
                main_slots["C1"] = child.text
                
            # 前置詞句（exclude_prepで指定されたもの以外）
            elif child.dep_ == "prep" and child != exclude_prep:
                prep_phrase = self._build_prep_phrase(child)
                if not main_slots.get("C2"):
                    main_slots["C2"] = prep_phrase
                elif not main_slots.get("M3"):
                    main_slots["M3"] = prep_phrase

    def _build_prep_phrase(self, prep_token) -> str:
        """
        前置詞句の構築
        """
        phrase_parts = [prep_token.text]
        for child in prep_token.children:
            phrase_parts.extend([token.text for token in self._collect_subtree(child)])
        return " ".join(phrase_parts)

    def _determine_prep_phrase_role(self, prep_token, doc) -> str:
        """
        前置詞句の文法的役割を判定
        """
        # be動詞の補語として使われている場合
        if prep_token.head.lemma_ == "be":
            return "complement"
        
        # 形容詞の後の前置詞句（interested in, good at など）
        if prep_token.head.pos_ == "ADJ":
            return "complement"
        
        return "modifier"

    def _merge_adverb_slots(self, main_slots, adverb_slots):
        """
        副詞ハンドラーの結果をマージ
        """
        for slot in ["M1", "M2", "M3"]:
            if adverb_slots.get(slot) and not main_slots.get(slot):
                main_slots[slot] = adverb_slots[slot]

    def _create_success_result(self, main_slots: Dict[str, str], sub_slots: Dict[str, Any], 
                             v_group_key: str, description: str) -> Dict[str, Any]:
        """成功結果の生成"""
        return {
            'success': True,
            'handler': self.name,
            'main_slots': main_slots,
            'sub_slots': sub_slots,
            'v_group_key': v_group_key,
            'description': description,
            'confidence': 0.9
        }

    def _create_failure_result(self, reason: str) -> Dict[str, Any]:
        """失敗結果の生成"""
        return {
            'success': False,
            'handler': self.name,
            'reason': reason,
            'main_slots': {},
            'sub_slots': {},
            'confidence': 0.0
        }


# テスト用の実行部分
if __name__ == "__main__":
    handler = GerundHandler()
    
    # テストケース
    test_cases = [
        "Swimming is fun.",                           # 主語位置
        "I enjoy reading books.",                     # 目的語位置
        "I'm interested in learning English.",       # 前置詞の目的語
        "My hobby is reading mystery novels.",       # 補語位置
        "After finishing homework, I watch TV.",     # 前置詞句内
        "She keeps talking about the movie.",        # 複合動詞＋動名詞
    ]
    
    for sentence in test_cases:
        print(f"\n🧪 テスト: '{sentence}'")
        result = handler.handle(sentence, "test_gerund")
        if result['success']:
            print(f"✅ 成功: {result['description']}")
            print(f"   Main slots: {result['main_slots']}")
            if result['sub_slots']:
                print(f"   Sub slots: {result['sub_slots']}")
        else:
            print(f"❌ 失敗: {result['reason']}")
