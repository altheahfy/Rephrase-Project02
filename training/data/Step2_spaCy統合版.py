# Step 2: spaCy統合版のRephrase_Parsing_Engine

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

class SpacyEnhancedRephraseEngine(RephraseParsingEngine):
    """spaCy統合版Rephrase品詞分解エンジン"""
    
    def __init__(self):
        super().__init__()
        self.engine_name = "Rephrase Parsing Engine v2.0 (spaCy Enhanced)"
        
        # spaCy初期化
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self.spacy_available = True
            print("✅ spaCyエンジン初期化完了")
        except Exception as e:
            print(f"⚠️ spaCy初期化失敗: {e}")
            print("   形態素ルール拡張にフォールバック")
            self.spacy_available = False
    
    def analyze_word_spacy(self, word, context=""):
        """spaCyによる高精度語彙解析"""
        
        if not self.spacy_available:
            return self.analyze_word_morphology(word, context)
        
        try:
            # 文脈がある場合は文全体で解析
            if context and word in context:
                doc = self.nlp(context)
                for token in doc:
                    if token.text.lower() == word.lower():
                        return {
                            'word': word,
                            'pos': token.pos_,
                            'tag': token.tag_,
                            'lemma': token.lemma_,
                            'confidence': 0.95,
                            'method': 'spacy_context'
                        }
            
            # 単語単独で解析
            doc = self.nlp(word)
            if doc:
                token = doc[0]
                return {
                    'word': word,
                    'pos': token.pos_,
                    'tag': token.tag_, 
                    'lemma': token.lemma_,
                    'confidence': 0.90,
                    'method': 'spacy_single'
                }
        
        except Exception as e:
            print(f"spaCyエラー: {e}")
        
        # フォールバック: 形態素ルール使用
        return self.analyze_word_morphology(word, context)
    
    def batch_analyze_spacy(self, sentence):
        """文全体のspaCy解析"""
        
        if not self.spacy_available:
            # spaCy利用不可時は形態素ルールで解析
            words = sentence.split()
            return [self.analyze_word_morphology(word, sentence) for word in words]
        
        try:
            doc = self.nlp(sentence)
            results = []
            
            for token in doc:
                result = {
                    'word': token.text,
                    'pos': token.pos_,
                    'tag': token.tag_,
                    'lemma': token.lemma_,
                    'confidence': 0.95,
                    'method': 'spacy_batch',
                    'is_punct': token.is_punct,
                    'is_stop': token.is_stop
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"spaCyバッチ解析エラー: {e}")
            # フォールバック
            words = sentence.split()
            return [self.analyze_word_morphology(word, sentence) for word in words]
    
    def compare_methods(self, sentence):
        """形態素ルール vs spaCy の比較"""
        words = sentence.replace('.', '').replace(',', '').split()
        
        print(f"文: {sentence}")
        print(f"{'Word':15} {'形態素ルール':20} {'spaCy':20} {'一致':5}")
        print("-" * 65)
        
        morphology_correct = 0
        spacy_correct = 0
        total_words = len(words)
        agreement = 0
        
        for word in words:
            morph_result = self.analyze_word_morphology(word, sentence)
            spacy_result = self.analyze_word_spacy(word, sentence)
            
            # 品詞の簡略化（比較用）
            morph_pos = morph_result['pos']
            spacy_pos = spacy_result.get('pos', 'UNKNOWN')
            
            # 一致判定（大まかな品詞カテゴリで）
            match = self.pos_categories_match(morph_pos, spacy_pos)
            match_str = "✅" if match else "❌"
            
            if match:
                agreement += 1
            
            print(f"{word:15} {morph_pos:20} {spacy_pos:20} {match_str:5}")
        
        agreement_rate = (agreement / total_words) * 100
        print(f"\n📊 手法間一致率: {agreement}/{total_words} ({agreement_rate:.1f}%)")
        
        return {
            'total_words': total_words,
            'agreement': agreement,
            'agreement_rate': agreement_rate
        }
    
    def pos_categories_match(self, morph_pos, spacy_pos):
        """品詞カテゴリの一致判定"""
        # 大まかなカテゴリマッピング
        category_map = {
            'ADV': 'ADV', 'NOUN': 'NOUN', 'ADJ': 'ADJ', 
            'VERB_PAST': 'VERB', 'VERB_ING': 'VERB',
            'BE_VERB': 'VERB', 'AUX_VERB': 'AUX',
            'DET': 'DET', 'PRON': 'PRON', 'MODAL': 'AUX'
        }
        
        morph_category = category_map.get(morph_pos, morph_pos)
        spacy_category = spacy_pos
        
        return morph_category == spacy_category or morph_pos == spacy_pos

# テスト実行
if __name__ == "__main__":
    print("=== Step 2: spaCy統合版テスト ===\n")
    
    engine = SpacyEnhancedRephraseEngine()
    
    # 比較テスト
    test_sentences = [
        "The sophisticated analysis is comprehensive.",
        "She efficiently investigated the mysterious disappearance.",
        "Students frequently encounter challenging mathematical equations."
    ]
    
    total_agreement = 0
    total_words_all = 0
    
    for sentence in test_sentences:
        result = engine.compare_methods(sentence)
        total_agreement += result['agreement']
        total_words_all += result['total_words']
        print()
    
    overall_agreement = (total_agreement / total_words_all) * 100
    print(f"🎯 全体の手法間一致率: {total_agreement}/{total_words_all} ({overall_agreement:.1f}%)")
    
    print(f"\n💡 Step 2 完了:")
    print(f"  ✅ spaCy統合版実装完了")
    print(f"  🔄 両手法の比較検証完了")
    print(f"  📊 手法間一致率: {overall_agreement:.1f}%")
