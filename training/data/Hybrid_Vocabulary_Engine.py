# Hybrid Vocabulary Solution
# ルールベース + API + 機械学習の組み合わせ

class HybridVocabularyEngine:
    """3段階語彙解析システム"""
    
    def __init__(self):
        # レベル1: 高頻出語の高速辞書（手動メンテナンス）
        self.core_vocabulary = {
            # 動詞
            'is': {'pos': 'verb', 'type': 'be_verb'},
            'are': {'pos': 'verb', 'type': 'be_verb'},
            'have': {'pos': 'verb', 'type': 'aux_verb'},
            'had': {'pos': 'verb', 'type': 'aux_verb'},
            'do': {'pos': 'verb', 'type': 'aux_verb'},
            'did': {'pos': 'verb', 'type': 'aux_verb'},
            'will': {'pos': 'verb', 'type': 'modal'},
            'can': {'pos': 'verb', 'type': 'modal'},
            'could': {'pos': 'verb', 'type': 'modal'},
            'should': {'pos': 'verb', 'type': 'modal'},
            'would': {'pos': 'verb', 'type': 'modal'},
            
            # 疑問詞
            'what': {'pos': 'wh_word', 'type': 'question'},
            'where': {'pos': 'wh_word', 'type': 'question'},
            'when': {'pos': 'wh_word', 'type': 'question'},
            'who': {'pos': 'wh_word', 'type': 'question'},
            'why': {'pos': 'wh_word', 'type': 'question'},
            'how': {'pos': 'wh_word', 'type': 'question'},
            
            # 代名詞
            'i': {'pos': 'pronoun', 'type': 'subject'},
            'you': {'pos': 'pronoun', 'type': 'object_subject'},
            'he': {'pos': 'pronoun', 'type': 'subject'},
            'she': {'pos': 'pronoun', 'type': 'subject'},
            'it': {'pos': 'pronoun', 'type': 'subject'},
            'we': {'pos': 'pronoun', 'type': 'subject'},
            'they': {'pos': 'pronoun', 'type': 'subject'},
            'me': {'pos': 'pronoun', 'type': 'object'},
            'him': {'pos': 'pronoun', 'type': 'object'},
            'her': {'pos': 'pronoun', 'type': 'object'},
            'them': {'pos': 'pronoun', 'type': 'object'},
            'us': {'pos': 'pronoun', 'type': 'object'}
        }
        
        # レベル2: 形態素パターン分析
        self.morphological_patterns = {
            'ed': 'past_verb',
            'ing': 'present_participle_gerund',
            'ly': 'adverb',
            'er': 'comparative_agent',
            'est': 'superlative',
            'tion': 'noun',
            'sion': 'noun',
            'ness': 'noun',
            'ment': 'noun'
        }
        
        # レベル3: API連携用設定
        self.api_available = False  # 環境に応じて設定
        self.api_cache = {}
    
    def analyze_word(self, word, context=None):
        """3段階語彙解析"""
        
        word_lower = word.lower()
        
        # レベル1: コア語彙辞書（最高速）
        if word_lower in self.core_vocabulary:
            result = self.core_vocabulary[word_lower].copy()
            result['analysis_method'] = 'core_dictionary'
            result['confidence'] = 0.95
            return result
        
        # レベル2: 形態素パターン分析
        morphology_result = self.analyze_morphology(word)
        if morphology_result:
            morphology_result['analysis_method'] = 'morphology'
            morphology_result['confidence'] = 0.75
            return morphology_result
        
        # レベル3: 文脈推定フォールバック
        context_result = self.analyze_by_context(word, context)
        context_result['analysis_method'] = 'context'
        context_result['confidence'] = 0.60
        return context_result
    
    def analyze_morphology(self, word):
        """形態素解析"""
        word_lower = word.lower()
        
        for suffix, pos_type in self.morphological_patterns.items():
            if word_lower.endswith(suffix):
                return {
                    'word': word,
                    'pos': pos_type,
                    'morphology': f'suffix_{suffix}'
                }
        
        return None
    
    def analyze_by_context(self, word, context):
        """文脈による品詞推定"""
        if not context:
            return {'word': word, 'pos': 'unknown', 'context': 'no_context'}
        
        # 簡単な位置分析
        words = context.split()
        try:
            word_index = words.index(word)
            
            # 文頭なら主語の可能性
            if word_index == 0:
                return {'word': word, 'pos': 'probable_subject'}
            
            # 前の語が助動詞なら動詞の可能性
            if word_index > 0 and words[word_index-1].lower() in ['do', 'did', 'will', 'can', 'could']:
                return {'word': word, 'pos': 'probable_verb'}
            
            # 前の語が動詞なら目的語の可能性
            prev_word = words[word_index-1].lower()
            if prev_word in self.core_vocabulary and self.core_vocabulary[prev_word].get('pos') == 'verb':
                return {'word': word, 'pos': 'probable_object'}
                
        except ValueError:
            pass
        
        return {'word': word, 'pos': 'unknown'}
    
    def batch_analyze(self, sentence):
        """文全体の語彙解析"""
        words = sentence.split()
        results = []
        
        for i, word in enumerate(words):
            context = sentence  # 全文を文脈として渡す
            analysis = self.analyze_word(word, context)
            analysis['position'] = i
            results.append(analysis)
        
        return results

# コア語彙拡張の実装例
def expand_core_vocabulary(engine, new_words_dict):
    """コア語彙の動的拡張"""
    engine.core_vocabulary.update(new_words_dict)
    print(f"コア語彙を{len(new_words_dict)}語追加しました")

# メイン実行部分（スクリプト単体実行時のみ）
if __name__ == "__main__":
    # 実使用例
    engine = HybridVocabularyEngine()

    # テスト文の解析
    test_sentence = "Where did you see the beautiful girl yesterday?"
    analysis_results = engine.batch_analyze(test_sentence)

    print("=== ハイブリッド語彙解析結果 ===")
    for result in analysis_results:
        word = result.get('word', 'Unknown')
        pos = result.get('pos', 'Unknown')
        method = result.get('analysis_method', 'Unknown')
        confidence = result.get('confidence', 'N/A')
        print(f"{word:12} -> {pos:20} (method: {method}, confidence: {confidence})")

    print("\n=== 未知語処理例 ===")
    unknown_word_result = engine.analyze_word("serendipitously", "I serendipitously met him")
    print(f"serendipitously -> {unknown_word_result}")

    # 追加語彙例
    additional_vocab = {
        'because': {'pos': 'conjunction', 'type': 'reason'},
        'although': {'pos': 'conjunction', 'type': 'contrast'},
        'however': {'pos': 'adverb', 'type': 'transition'}
    }

    expand_core_vocabulary(engine, additional_vocab)
