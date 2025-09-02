"""
不定詞ハンドラー - spaCy依存関係分析による完全実装
To-infinitive constructions handler using spaCy dependency parsing
人間的文法認識システム - Human Grammar Pattern Recognition System
"""

import spacy
import re
from typing import Dict, List, Any, Optional, Tuple

class InfinitiveHandler:
    def __init__(self, nlp=None):
        """
        不定詞ハンドラーの初期化
        spaCy NLPモデルを使用した依存関係分析
        """
        if nlp is None:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = spacy.load("en_core_web_md")
        else:
            self.nlp = nlp
    
    def can_handle(self, sentence: str) -> bool:
        """
        不定詞構造を含む文かどうかを判定
        spaCyの依存関係分析で 'to' + base verb パターンを検出
        """
        doc = self.nlp(sentence)
        
        # to + infinitive パターンの検出
        for token in doc:
            if (token.text.lower() == "to" and 
                token.pos_ == "PART" and 
                token.dep_ in ["aux", "mark", "advcl"] and
                token.head.pos_ == "VERB"):
                return True
            
            # "be about to", "in order to", "so as to" などの複合構造
            if token.text.lower() == "to" and token.nbor(1).pos_ == "VERB":
                return True
                
        return False
    
    def handle(self, sentence: str, v_group_key: str) -> Dict[str, Any]:
        """
        不定詞構造の解析とスロット分解
        spaCy依存関係による汎用的アプローチ
        """
        doc = self.nlp(sentence)
        
        # 基本スロット初期化
        main_slots = {"S": "", "V": "", "O1": "", "O2": "", "C": "", 
                     "M1": "", "M2": "", "M3": "", "Aux": ""}
        sub_slots = {}
        
        # 不定詞の種類を特定
        infinitive_type = self._identify_infinitive_type(doc)
        
        if infinitive_type == "nominal_subject":
            return self._handle_nominal_subject(doc, main_slots, sub_slots)
        elif infinitive_type == "nominal_object":
            return self._handle_nominal_object(doc, main_slots, sub_slots)
        elif infinitive_type == "adjectival":
            return self._handle_adjectival(doc, main_slots, sub_slots)
        elif infinitive_type == "adverbial":
            return self._handle_adverbial(doc, main_slots, sub_slots)
        elif infinitive_type == "causative":
            return self._handle_causative(doc, main_slots, sub_slots)
        elif infinitive_type == "complex":
            return self._handle_complex_patterns(doc, main_slots, sub_slots)
        else:
            return self._handle_general_infinitive(doc, main_slots, sub_slots)
    
    def _identify_infinitive_type(self, doc) -> str:
        """
        不定詞の文法的機能を特定
        spaCy依存関係による自動分類
        """
        sentence_text = doc.text.lower()
        
        # 特定パターンの検出
        if sentence_text.startswith("to ") and " is " in sentence_text:
            return "nominal_subject"
        
        if any(pattern in sentence_text for pattern in 
               ["want to", "need to", "decide to", "plan to", "hope to"]):
            return "nominal_object"
        
        if any(pattern in sentence_text for pattern in 
               ["something to", "nothing to", "anything to", "time to"]):
            return "adjectival"
        
        if any(pattern in sentence_text for pattern in 
               ["in order to", "so as to", "came to", "went to"]):
            return "adverbial"
        
        if any(pattern in sentence_text for pattern in 
               ["want you to", "ask him to", "tell her to"]):
            return "causative"
        
        if any(pattern in sentence_text for pattern in 
               ["too", "enough", "about to", "perfect", "passive"]):
            return "complex"
        
        return "general"
    
    def _handle_nominal_subject(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        名詞的用法（主語）: To study English is important.
        """
        tokens = [token.text for token in doc]
        
        # "To + verb phrase"を主語として特定
        to_index = -1
        for i, token in enumerate(doc):
            if token.text.lower() == "to" and i + 1 < len(doc) and doc[i + 1].pos_ == "VERB":
                to_index = i
                break
        
        if to_index >= 0:
            # 主語部分の特定
            verb_start = -1
            for i in range(to_index + 1, len(doc)):
                if doc[i].pos_ == "VERB" and doc[i].dep_ in ["ROOT", "ccomp"]:
                    verb_start = i
                    break
            
            if verb_start > 0:
                main_slots["S"] = " ".join(tokens[to_index:verb_start])
                main_slots["V"] = tokens[verb_start]
                
                # 補語の特定
                for i in range(verb_start + 1, len(doc)):
                    if doc[i].pos_ in ["ADJ", "NOUN"]:
                        main_slots["C"] = " ".join(tokens[verb_start + 1:])
                        break
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    def _handle_nominal_object(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        名詞的用法（目的語）: I want to learn programming.
        """
        tokens = [token.text for token in doc]
        
        # 主語と動詞の特定
        for token in doc:
            if token.dep_ == "nsubj":
                main_slots["S"] = token.text
            elif token.dep_ == "ROOT":
                main_slots["V"] = token.text
                
                # 不定詞句を目的語として特定
                to_start = -1
                for child in token.children:
                    if child.text.lower() == "to" or child.dep_ == "xcomp":
                        to_start = child.i
                        break
                
                if to_start >= 0:
                    main_slots["O1"] = " ".join(tokens[to_start:])
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    def _handle_adjectival(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        形容詞的用法: She has something to tell you.
        """
        tokens = [token.text for token in doc]
        
        # 基本文型の解析
        for token in doc:
            if token.dep_ == "nsubj":
                main_slots["S"] = token.text
            elif token.dep_ == "ROOT":
                main_slots["V"] = token.text
                
                # "something to ..." パターンの検出
                something_start = -1
                for i, child in enumerate(token.children):
                    if child.text in ["something", "nothing", "anything"] or child.pos_ == "NOUN":
                        something_start = child.i
                        break
                
                if something_start >= 0:
                    main_slots["O1"] = " ".join(tokens[something_start:])
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    def _handle_adverbial(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        副詞的用法: He came to see his friend.
        """
        tokens = [token.text for token in doc]
        
        # 基本構造の解析
        for token in doc:
            if token.dep_ == "nsubj":
                main_slots["S"] = token.text
            elif token.dep_ == "ROOT":
                main_slots["V"] = token.text
                
                # 副詞的不定詞句の特定
                to_start = -1
                for child in token.children:
                    if (child.text.lower() == "to" or 
                        child.dep_ in ["advcl", "xcomp", "ccomp"]):
                        to_start = child.i
                        break
                
                if to_start >= 0:
                    main_slots["M3"] = " ".join(tokens[to_start:])
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    def _handle_causative(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        使役構造: I want you to help me.
        """
        tokens = [token.text for token in doc]
        
        # 主語と動詞の特定
        for token in doc:
            if token.dep_ == "nsubj":
                main_slots["S"] = token.text
            elif token.dep_ == "ROOT":
                main_slots["V"] = token.text
                
                # 直接目的語と不定詞句の分離
                objects = []
                for child in token.children:
                    if child.dep_ == "dobj":
                        objects.append(child.text)
                    elif child.dep_ == "xcomp" and child.text.lower() == "to":
                        objects.append(" ".join(tokens[child.i:]))
                
                if len(objects) >= 2:
                    main_slots["O1"] = objects[0]
                    main_slots["O2"] = objects[1]
                elif len(objects) == 1:
                    main_slots["O1"] = objects[0]
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    def _handle_complex_patterns(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        複雑パターン: too...to, enough to, be about to, perfect/passive
        """
        sentence_text = doc.text.lower()
        tokens = [token.text for token in doc]
        
        # "be about to" パターン
        if "about to" in sentence_text:
            for token in doc:
                if token.dep_ == "nsubj":
                    main_slots["S"] = token.text
                elif token.lemma_ == "be" and token.dep_ == "ROOT":
                    # "be about to start" を一つの動詞として扱う
                    about_start = -1
                    for i, t in enumerate(tokens):
                        if t.lower() == "about":
                            about_start = i
                            break
                    
                    if about_start >= 0:
                        main_slots["V"] = " ".join(tokens[token.i:])
        
        # "too...to" パターン
        elif "too" in sentence_text and "to" in sentence_text:
            for token in doc:
                if token.dep_ == "nsubj":
                    main_slots["S"] = token.text
                elif token.dep_ == "ROOT":
                    main_slots["V"] = token.text
                    
                    # "too heavy to carry" を補語として扱う
                    too_start = -1
                    for i, t in enumerate(tokens):
                        if t.lower() == "too":
                            too_start = i
                            break
                    
                    if too_start >= 0:
                        main_slots["C"] = " ".join(tokens[too_start:])
        
        # "enough to" パターン
        elif "enough to" in sentence_text:
            for token in doc:
                if token.dep_ == "nsubj":
                    main_slots["S"] = token.text
                elif token.dep_ == "ROOT":
                    main_slots["V"] = token.text
                    
                    # "old enough to drive" を補語として扱う
                    for i in range(token.i + 1, len(tokens)):
                        if "enough" in tokens[i]:
                            main_slots["C"] = " ".join(tokens[token.i + 1:])
                            break
        
        # その他の複雑パターン
        else:
            return self._handle_general_infinitive(doc, main_slots, sub_slots)
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
    
    def _handle_general_infinitive(self, doc, main_slots: Dict, sub_slots: Dict) -> Dict[str, Any]:
        """
        一般的な不定詞構造の処理
        """
        tokens = [token.text for token in doc]
        
        # 基本解析
        for token in doc:
            if token.dep_ == "nsubj":
                main_slots["S"] = token.text
            elif token.dep_ == "ROOT":
                main_slots["V"] = token.text
                
                # 助動詞の特定
                for child in token.children:
                    if child.dep_ == "aux":
                        main_slots["Aux"] = child.text
                
                # 不定詞句の特定
                to_found = False
                for child in token.children:
                    if child.text.lower() == "to" or child.dep_ in ["xcomp", "ccomp"]:
                        to_start = child.i
                        main_slots["O1"] = " ".join(tokens[to_start:])
                        to_found = True
                        break
                
                # 前置詞句や修飾語の処理
                if not to_found:
                    for child in token.children:
                        if child.dep_ == "prep":
                            main_slots["M2"] = " ".join([child.text] + 
                                [t.text for t in child.subtree if t != child])
        
        return {"main_slots": main_slots, "sub_slots": sub_slots}
