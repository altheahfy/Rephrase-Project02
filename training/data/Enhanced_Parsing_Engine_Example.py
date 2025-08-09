# Enhanced Parsing Engine with NLP Library Integration

import spacy
from spacy.lang.en import English

class EnhancedRephraseEngine:
    """外部NLPライブラリを活用した高精度パーサー"""
    
    def __init__(self):
        # 軽量モデルをロード（約50MB）
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            # フォールバック: 基本的なtokenizerのみ使用
            self.nlp = English()
            
        # 既存のルールベースロジックも保持（高速処理用）
        self.manual_rules = {
            'modal_verbs': ["will", "would", "can", "could", "may", "might", "must", "should"],
            'be_verbs': ["am", "is", "are", "was", "were", "be", "been", "being"],
            'have_verbs': ["have", "has", "had"]
        }
    
    def analyze_sentence_hybrid(self, sentence):
        """ハイブリッド解析: ルールベース + NLP"""
        
        # 1. spaCyで品詞解析（全語彙対応）
        doc = self.nlp(sentence)
        spacy_analysis = [(token.text, token.pos_, token.dep_, token.lemma_) 
                         for token in doc]
        
        # 2. 既存のルールベースロジックを適用
        rule_based_result = self.apply_grammar_rules(spacy_analysis)
        
        # 3. 結果をマージして最終判定
        return self.merge_results(rule_based_result, spacy_analysis)
    
    def get_word_info(self, word):
        """単語の詳細情報を取得"""
        doc = self.nlp(word)
        if doc:
            token = doc[0]
            return {
                'pos': token.pos_,          # 品詞
                'lemma': token.lemma_,      # 語幹
                'is_verb': token.pos_ == 'VERB',
                'is_noun': token.pos_ == 'NOUN',
                'is_adj': token.pos_ == 'ADJ'
            }
        return None

# 使用例
engine = EnhancedRephraseEngine()
result = engine.analyze_sentence_hybrid("I haven't seen you for a long time.")
