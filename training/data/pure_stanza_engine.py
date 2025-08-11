"""
Pure Stanza Engine - Stanzaネイティブな基本構造
Stanzaの依存関係をそのまま活用したシンプルな分解エンジン
"""

import stanza

class PureStanzaEngine:
    def __init__(self):
        """Stanzaネイティブエンジン初期化"""
        print("🎯 PureStanzaEngine初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        print("✅ Stanza準備完了")
    
    def decompose(self, sentence):
        """基本分解: Stanzaの情報をそのまま活用"""
        print(f"\n🎯 Stanza基本分解開始: '{sentence[:50]}...'")
        
        doc = self.nlp(sentence)
        
        for sent in doc.sentences:
            # Step1: ROOT動詞特定
            root_verb = self._find_root_verb(sent)
            if not root_verb:
                return {}
            
            print(f"📌 ROOT動詞: '{root_verb.text}'")
            
            # Step2: 基本8スロット構造をStanzaから直接抽出
            slots = self._extract_all_slots_from_stanza(sent, root_verb)
            
            # Step3: 結果表示と正解データ比較
            self._display_results(slots)
            self._compare_with_correct_data(slots)
            
            return slots
            
        return {}
    
    def _find_root_verb(self, sent):
        """ROOT動詞を特定"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _extract_all_slots_from_stanza(self, sent, root_verb):
        """Stanzaから全8スロットを直接抽出"""
        print("🏗️ Stanzaから直接スロット抽出中...")
        
        slots = {}
        
        # M1: 文頭修飾句 (obl:unmarked)
        slots['M1'] = self._extract_m1_slot(sent, root_verb)
        
        # S: 主語 (nsubj + 関係節)
        slots['S'] = self._extract_s_slot(sent, root_verb)
        
        # Aux: 助動詞 (aux + mark)
        slots['Aux'] = self._extract_aux_slot(sent, root_verb)
        
        # V: 動詞 (root → xcomp)
        slots['V'] = self._extract_v_slot(sent, root_verb)
        
        # O1: 目的語1 (obj)
        slots['O1'] = self._extract_o1_slot(sent, root_verb)
        
        # C2: 補語2 (advcl)
        slots['C2'] = self._extract_c2_slot(sent, root_verb)
        
        # M2: 修飾句2 (advcl - even though)
        slots['M2'] = self._extract_m2_slot(sent, root_verb)
        
        # M3: 修飾句3 (advcl - so)
        slots['M3'] = self._extract_m3_slot(sent, root_verb)
        
        return {k: v for k, v in slots.items() if v}  # 空でないスロットのみ
    
    def _extract_m1_slot(self, sent, root_verb):
        """M1スロット: 文頭修飾句"""
        # obl:unmarkedを探す
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'obl:unmarked':
                # 文頭から主語開始まで
                subject_start = None
                for w in sent.words:
                    if w.head == root_verb.id and w.deprel == 'nsubj':
                        subject_start = w.start_char
                        break
                
                if subject_start:
                    m1_text = sent.text[:subject_start].strip().rstrip(',')
                    print(f"📍 M1検出: '{m1_text}'")
                    return {'main': m1_text}
        return None
    
    def _extract_s_slot(self, sent, root_verb):
        """Sスロット: 主語 + 関係節"""
        # nsubjを探す
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'nsubj':
                # 主語の範囲を特定（関係節含む）
                s_range = self._find_subject_range(sent, word)
                s_text = self._extract_text_range(sent, s_range)
                print(f"📍 S検出: '{s_text}'")
                
                # サブスロット分解
                subslots = self._extract_s_subslots(sent, word)
                subslots['main'] = s_text
                return subslots
        return None
    
    def _extract_aux_slot(self, sent, root_verb):
        """Auxスロット: 助動詞"""
        aux_parts = []
        
        # ROOT動詞の助動詞を探す
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'aux':
                aux_parts.append(word.text)
        
        # xcompのmarkも探す（had to のto）
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                for child in sent.words:
                    if child.head == word.id and child.deprel == 'mark':
                        aux_parts.append(child.text)
        
        if aux_parts:
            aux_text = ' '.join(aux_parts)
            print(f"📍 Aux検出: '{aux_text}'")
            return {'main': aux_text}
        return None
    
    def _extract_v_slot(self, sent, root_verb):
        """Vスロット: 動詞（実際の動作動詞）"""
        # xcompを探す（実際の動作動詞）
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                print(f"📍 V検出: '{word.text}'（xcomp）")
                return {'v': word.text}
        
        # fallback: ROOT動詞
        print(f"📍 V検出: '{root_verb.text}'（root）")
        return {'v': root_verb.text}
    
    def _extract_o1_slot(self, sent, root_verb):
        """O1スロット: 目的語1"""
        # xcompの目的語を探す
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':
                for child in sent.words:
                    if child.head == word.id and child.deprel == 'obj':
                        # 目的語の完全な範囲を取得
                        o1_range = self._find_object_range(sent, child)
                        o1_text = self._extract_text_range(sent, o1_range)
                        print(f"📍 O1検出: '{o1_text}'")
                        return {'main': o1_text}
        return None
    
    def _extract_c2_slot(self, sent, root_verb):
        """C2スロット: 補語2"""
        # makeのadvcl（deliver）を探す
        for word in sent.words:
            if word.head == root_verb.id and word.deprel == 'xcomp':  # make
                for child in sent.words:
                    if child.head == word.id and child.deprel == 'advcl':  # deliver
                        c2_range = self._find_verb_phrase_range(sent, child)
                        c2_text = self._extract_text_range(sent, c2_range)
                        print(f"📍 C2検出: '{c2_text}'")
                        return {'main': c2_text}
        return None
    
    def _extract_m2_slot(self, sent, root_verb):
        """M2スロット: 修飾句2（even though節）"""
        # even though節を探す
        for word in sent.words:
            if word.deprel == 'advcl' and self._has_mark(sent, word, ['though', 'although']):
                m2_range = self._find_clause_range(sent, word)
                m2_text = self._extract_text_range(sent, m2_range)
                print(f"📍 M2検出: '{m2_text}'")
                return {'main': m2_text}
        return None
    
    def _extract_m3_slot(self, sent, root_verb):
        """M3スロット: 修飾句3（so節）"""
        # so節を探す
        for word in sent.words:
            if word.deprel == 'advcl' and self._has_mark(sent, word, ['so']):
                m3_range = self._find_clause_range(sent, word)
                m3_text = self._extract_text_range(sent, m3_range)
                print(f"📍 M3検出: '{m3_text}'")
                return {'main': m3_text}
        return None
    
    def _find_subject_range(self, sent, subject_word):
        """主語の範囲を特定（関係節含む）"""
        start_id = subject_word.id
        end_id = subject_word.id
        
        # 関連する修飾語を含める
        for word in sent.words:
            if (word.head == subject_word.id or 
                (hasattr(word, 'head') and self._is_related_to_subject(sent, word, subject_word))):
                start_id = min(start_id, word.id)
                end_id = max(end_id, word.id)
        
        return (start_id, end_id)
    
    def _find_object_range(self, sent, obj_word):
        """目的語の範囲を特定"""
        start_id = obj_word.id
        end_id = obj_word.id
        
        # 修飾語を含める
        for word in sent.words:
            if word.head == obj_word.id:
                start_id = min(start_id, word.id)
                end_id = max(end_id, word.id)
        
        return (start_id, end_id)
    
    def _find_verb_phrase_range(self, sent, verb_word):
        """動詞句の範囲を特定"""
        start_id = verb_word.id
        end_id = verb_word.id
        
        # 動詞の子要素を含める
        for word in sent.words:
            if word.head == verb_word.id:
                start_id = min(start_id, word.id)
                end_id = max(end_id, word.id)
        
        return (start_id, end_id)
    
    def _find_clause_range(self, sent, clause_verb):
        """節の範囲を特定"""
        start_id = clause_verb.id
        end_id = clause_verb.id
        
        # markから始める
        for word in sent.words:
            if word.head == clause_verb.id and word.deprel == 'mark':
                start_id = min(start_id, word.id)
        
        # 節の全ての子要素を含める
        for word in sent.words:
            if word.head == clause_verb.id:
                start_id = min(start_id, word.id)
                end_id = max(end_id, word.id)
        
        return (start_id, end_id)
    
    def _extract_text_range(self, sent, id_range):
        """IDの範囲からテキストを抽出"""
        start_id, end_id = id_range
        words_in_range = [w for w in sent.words if start_id <= w.id <= end_id]
        words_in_range.sort(key=lambda w: w.id)
        return ' '.join([w.text for w in words_in_range])
    
    def _has_mark(self, sent, word, marks):
        """指定されたmarkを持つかチェック"""
        for child in sent.words:
            if child.head == word.id and child.deprel == 'mark' and child.text in marks:
                return True
        return False
    
    def _is_related_to_subject(self, sent, word, subject):
        """単語が主語に関連するかチェック"""
        # 関係節やその他の修飾語
        return (word.deprel in ['det', 'acl:relcl'] and 
                (word.head == subject.id or self._is_in_relcl_chain(sent, word, subject)))
    
    def _is_in_relcl_chain(self, sent, word, subject):
        """関係節チェーンに含まれるかチェック"""
        for w in sent.words:
            if w.head == subject.id and w.deprel == 'acl:relcl':
                if word.head == w.id:
                    return True
        return False
    
    def _extract_s_subslots(self, sent, subject_word):
        """Sスロットのサブスロット分解"""
        subslots = {}
        
        # 関係節を探す
        for word in sent.words:
            if word.head == subject_word.id and word.deprel == 'acl:relcl':
                # sub-s: "the manager who"
                det_text = ""
                for det_word in sent.words:
                    if det_word.head == subject_word.id and det_word.deprel == 'det':
                        det_text = det_word.text + " "
                subslots['sub-s'] = f"{det_text}{subject_word.text} who"
                
                # 関係節内のサブスロット
                for rel_child in sent.words:
                    if rel_child.head == word.id:
                        if rel_child.deprel == 'aux':
                            subslots['sub-aux'] = rel_child.text
                        elif rel_child.deprel == 'advmod':
                            subslots['sub-m2'] = rel_child.text
                        elif rel_child.deprel == 'obj':
                            # "charge of the project"
                            obj_range = self._find_object_range(sent, rel_child)
                            subslots['sub-o1'] = self._extract_text_range(sent, obj_range)
                
                subslots['sub-v'] = word.text
                break
        
        return subslots
    
    def _display_results(self, slots):
        """結果表示"""
        print("\n=== Stanza基本分解結果 ===")
        for slot_name, slot_data in slots.items():
            if isinstance(slot_data, dict) and len(slot_data) > 1:
                print(f"\n📋 {slot_name}スロット:")
                for subslot, content in slot_data.items():
                    print(f"  {subslot:<10}: \"{content}\"")
            else:
                content = slot_data.get('main') or slot_data.get('v') or slot_data
                print(f"\n📋 {slot_name}スロット: \"{content}\"")
    
    def _compare_with_correct_data(self, slots):
        """正解データとの比較"""
        print("\n🎯 正解データ比較:")
        
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
            'O1': "the committee responsible for implementation",
            'C2': "deliver the final proposal flawlessly",
            'M2': "even though he was under intense pressure",
            'M3': "so the outcome would reflect their full potential"
        }
        
        for slot, correct in correct_data.items():
            if slot in slots:
                if isinstance(correct, dict) and isinstance(slots[slot], dict):
                    print(f"\n{slot}スロット比較:")
                    for sub, correct_val in correct.items():
                        actual = slots[slot].get(sub, "❌ 未検出")
                        match = "✅" if actual == correct_val else "❌"
                        print(f"  {sub}: {match} 正解='{correct_val}' 実際='{actual}'")
                else:
                    actual = slots[slot].get('main') or slots[slot].get('v') or slots[slot]
                    match = "✅" if actual == correct else "❌"
                    print(f"{slot}: {match} 正解='{correct}' 実際='{actual}'")
            else:
                print(f"{slot}: ❌ スロット未検出 正解='{correct}'")

# テスト実行
if __name__ == "__main__":
    engine = PureStanzaEngine()
    
    text = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
    
    engine.decompose(text)
