# Option 3: 形態素ルール拡張（シンプル版）
# 既存システムを最小限の変更で改善

print("=== 形態素ルール拡張による語彙制限緩和 ===\n")

class MorphologyRulesExpanded:
    """拡張形態素ルールエンジン"""
    
    def __init__(self):
        # 語尾パターンと品詞の対応
        self.suffix_rules = {
            # 動詞関連
            'ed': 'VERB_PAST',
            'ing': 'VERB_ING', 
            's': 'VERB_3SG_OR_NOUN_PLURAL',  # 曖昧
            
            # 名詞関連
            'tion': 'NOUN',
            'sion': 'NOUN', 
            'ness': 'NOUN',
            'ment': 'NOUN',
            'ity': 'NOUN',
            'er': 'NOUN_OR_ADJ',  # 曖昧
            'or': 'NOUN',
            'ist': 'NOUN',
            
            # 形容詞関連
            'able': 'ADJ',
            'ible': 'ADJ',
            'ful': 'ADJ',
            'less': 'ADJ',
            'ous': 'ADJ',
            'ive': 'ADJ',
            'al': 'ADJ',
            'ic': 'ADJ',
            
            # 副詞関連
            'ly': 'ADV',
        }
        
        # 基本語彙（現在のシステムにあるもの）
        self.basic_vocab = {
            'is': 'BE_VERB', 'are': 'BE_VERB', 'was': 'BE_VERB', 'were': 'BE_VERB',
            'have': 'AUX_VERB', 'has': 'AUX_VERB', 'had': 'AUX_VERB',
            'do': 'AUX_VERB', 'does': 'AUX_VERB', 'did': 'AUX_VERB',
            'will': 'MODAL', 'would': 'MODAL', 'can': 'MODAL', 'could': 'MODAL',
            'the': 'DET', 'a': 'DET', 'an': 'DET',
            'i': 'PRON', 'you': 'PRON', 'he': 'PRON', 'she': 'PRON', 'it': 'PRON'
        }
    
    def analyze_word(self, word, context=None):
        """単語の品詞を推定"""
        word_lower = word.lower().rstrip('.,!?')
        
        # 1. 基本語彙チェック
        if word_lower in self.basic_vocab:
            return {
                'word': word,
                'pos': self.basic_vocab[word_lower],
                'confidence': 0.95,
                'method': 'basic_vocab'
            }
        
        # 2. 形態素ルールチェック
        for suffix, pos in self.suffix_rules.items():
            if word_lower.endswith(suffix):
                return {
                    'word': word,
                    'pos': pos,
                    'confidence': 0.75,
                    'method': f'suffix_{suffix}'
                }
        
        # 3. 文脈推定（簡易版）
        context_pos = self.guess_from_context(word, context)
        return {
            'word': word,
            'pos': context_pos,
            'confidence': 0.50,
            'method': 'context_guess'
        }
    
    def guess_from_context(self, word, context):
        """文脈から品詞を推定"""
        if not context:
            return 'UNKNOWN'
        
        words = context.split()
        try:
            index = words.index(word)
            
            # 文頭なら主語の可能性
            if index == 0:
                return 'NOUN_OR_PRON'
            
            # 前の語が冠詞なら名詞の可能性
            if index > 0 and words[index-1].lower() in ['the', 'a', 'an']:
                return 'NOUN'
            
            # 前の語が助動詞なら動詞の可能性
            if index > 0 and words[index-1].lower() in ['do', 'does', 'did', 'will', 'can', 'could']:
                return 'VERB'
            
        except ValueError:
            pass
        
        return 'UNKNOWN'
    
    def batch_analyze(self, sentence):
        """文全体を解析"""
        words = sentence.split()
        results = []
        
        for word in words:
            analysis = self.analyze_word(word, sentence)
            results.append(analysis)
        
        return results

# テスト実行
if __name__ == "__main__":
    engine = MorphologyRulesExpanded()
    
    # テスト文章
    test_sentences = [
        "The sophisticated analysis is comprehensive.",
        "She efficiently investigated the mysterious disappearance.",
        "Students frequently encounter challenging mathematical equations.",
        "The environmental scientist conducted thorough research."
    ]
    
    print("=== 形態素ルール拡張テスト ===\n")
    
    total_words = 0
    recognized_words = 0
    
    for sentence in test_sentences:
        print(f"文: {sentence}")
        results = engine.batch_analyze(sentence)
        
        print("語彙解析:")
        for result in results:
            total_words += 1
            pos = result['pos']
            confidence = result['confidence']
            method = result['method']
            
            if pos != 'UNKNOWN':
                recognized_words += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"  {result['word']:15} -> {pos:20} ({confidence:.2f}) [{method}] {status}")
        
        print("-" * 60)
    
    # 統計
    recognition_rate = (recognized_words / total_words) * 100
    print(f"\n=== 統計結果 ===")
    print(f"総語数: {total_words}")
    print(f"認識語数: {recognized_words}")
    print(f"認識率: {recognition_rate:.1f}%")
    
    print(f"\n=== 形態素ルール拡張のメリット・デメリット ===")
    print("✅ メリット:")
    print("  - 既存システムへの統合が簡単")
    print("  - 外部依存なし（オフライン動作）")
    print("  - 軽量（メモリ使用量最小）")
    print("  - 即座に実装可能")
    
    print("\n❌ デメリット:")
    print("  - 認識精度に限界（70-80%程度）")
    print("  - 語尾の曖昧性（-s, -er等）")
    print("  - 不規則語への対応困難")
    print("  - 新語への対応不可")
    
    print(f"\n=== 実装の容易さ ===")
    print("既存のRephrase_Parsing_Engine.pyに追加するコード量:")
    print("  - 約30行の語尾ルール辞書")
    print("  - 約20行の判定関数")
    print("  - 合計50行程度の追加で実装可能")
    
    if recognition_rate >= 70:
        print(f"\n✅ 実用レベル: {recognition_rate:.1f}%の認識率を達成")
    else:
        print(f"\n⚠️ 改善必要: {recognition_rate:.1f}%では不十分")
