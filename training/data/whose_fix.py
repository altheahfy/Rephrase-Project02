    def _is_whose_clause_adverb(self, adverb_word, sentence, main_verb_id):
        """whose構文での副詞が関係節内かを位置で判定"""
        sentence_text = " ".join([w.text for w in sentence.words])
        if "whose" not in sentence_text:
            return False
            
        whose_pos = -1
        main_verb_pos = -1
        adverb_pos = adverb_word.id
        
        for word in sentence.words:
            if word.text.lower() == "whose":
                whose_pos = word.id
            elif word.id == main_verb_id:
                main_verb_pos = word.id
        
        # whose節内（whose〜主動詞前）の副詞は従属節
        if whose_pos > 0 and main_verb_pos > 0:
            if whose_pos < adverb_pos < main_verb_pos:
                print(f"   → WHOSE句位置判定: SUBORDINATE (whose:{whose_pos} < adverb:{adverb_pos} < main:{main_verb_pos})")
                return True
        
        return False
