# Step 3: 最適化統合版 - ハイブリッドエンジン

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Rephrase_Parsing_Engine import RephraseParsingEngine

class HybridOptimizedEngine(RephraseParsingEngine):
    """ハイブリッド最適化エンジン - 形態素ルール + spaCy"""
    
    def __init__(self):
        super().__init__()
        self.engine_name = "Rephrase Hybrid Engine v3.0 (Optimized)"
        
        # spaCy初期化（警告抑制）
        try:
            import warnings
            warnings.filterwarnings("ignore")
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self.spacy_available = True
            print("✅ ハイブリッドエンジン初期化完了")
        except Exception as e:
            print(f"⚠️ spaCy初期化失敗: {e}")
            print("   形態素ルール専用モードで動作")
            self.spacy_available = False
        
        # 統計情報
        self.stats = {
            'morphology_success': 0,
            'spacy_success': 0,
            'fallback_used': 0,
            'total_analyzed': 0
        }
    
    def analyze_word_hybrid(self, word, context=""):
        """ハイブリッド解析: 形態素ルール優先 → spaCy補完"""
        self.stats['total_analyzed'] += 1
        
        # Step 1: 形態素ルール解析
        morph_result = self.analyze_word_morphology(word, context)
        
        # 形態素ルールで確実に判定できた場合
        if (morph_result['pos'] not in ['UNKNOWN', 'VERB_3SG_OR_NOUN_PLURAL', 'NOUN_OR_ADJ']
            and morph_result['confidence'] > 0.8):
            self.stats['morphology_success'] += 1
            morph_result['method'] = 'morphology_primary'
            return morph_result
        
        # Step 2: spaCy補完解析
        if self.spacy_available:
            try:
                # 文脈解析
                if context and word in context:
                    doc = self.nlp(context)
                    for token in doc:
                        if token.text.lower() == word.lower():
                            self.stats['spacy_success'] += 1
                            return {
                                'word': word,
                                'pos': token.pos_,
                                'tag': token.tag_,
                                'lemma': token.lemma_,
                                'confidence': 0.95,
                                'method': 'spacy_context'
                            }
                
                # 単独解析
                doc = self.nlp(word)
                if doc:
                    token = doc[0]
                    self.stats['spacy_success'] += 1
                    return {
                        'word': word,
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'lemma': token.lemma_,
                        'confidence': 0.90,
                        'method': 'spacy_single'
                    }
            except:
                pass
        
        # Step 3: フォールバック（形態素ルール結果）
        self.stats['fallback_used'] += 1
        morph_result['method'] = 'morphology_fallback'
        return morph_result
    
    def analyze_sentence_hybrid(self, sentence):
        """文全体のハイブリッド解析"""
        words = sentence.replace('.', '').replace(',', '').split()
        results = []
        
        for word in words:
            result = self.analyze_word_hybrid(word, sentence)
            results.append(result)
        
        return results
    
    def performance_test(self, test_sentences):
        """性能テストと統計表示"""
        print(f"=== ハイブリッドエンジン性能テスト ===\n")
        
        all_results = []
        
        for i, sentence in enumerate(test_sentences, 1):
            print(f"📝 テスト {i}: {sentence}")
            results = self.analyze_sentence_hybrid(sentence)
            all_results.extend(results)
            
            # 語彙別詳細表示
            print(f"{'Word':15} {'POS':12} {'Method':20} {'Confidence':12}")
            print("-" * 65)
            for result in results:
                conf_str = f"{result['confidence']:.2f}"
                print(f"{result['word']:15} {result['pos']:12} {result['method']:20} {conf_str:12}")
            print()
        
        # 統計サマリー
        total = self.stats['total_analyzed']
        morphology_rate = (self.stats['morphology_success'] / total) * 100
        spacy_rate = (self.stats['spacy_success'] / total) * 100  
        fallback_rate = (self.stats['fallback_used'] / total) * 100
        
        print(f"📊 処理統計:")
        print(f"  形態素ルール成功: {self.stats['morphology_success']}/{total} ({morphology_rate:.1f}%)")
        print(f"  spaCy補完成功:    {self.stats['spacy_success']}/{total} ({spacy_rate:.1f}%)")
        print(f"  フォールバック:   {self.stats['fallback_used']}/{total} ({fallback_rate:.1f}%)")
        print(f"  総合認識率:       {total - self.stats['fallback_used']}/{total} ({100 - fallback_rate:.1f}%)")
        
        # 解析品質評価
        recognized_words = [r for r in all_results if r['pos'] != 'UNKNOWN']
        recognition_rate = (len(recognized_words) / len(all_results)) * 100
        
        print(f"\n🎯 語彙認識品質:")
        print(f"  認識成功:         {len(recognized_words)}/{len(all_results)} ({recognition_rate:.1f}%)")
        print(f"  未認識語彙:       {len(all_results) - len(recognized_words)}")
        
        return {
            'total_words': len(all_results),
            'recognized_words': len(recognized_words),
            'recognition_rate': recognition_rate,
            'stats': self.stats
        }

# テスト実行
if __name__ == "__main__":
    print("=== Step 3: ハイブリッド最適化エンジンテスト ===\n")
    
    engine = HybridOptimizedEngine()
    
    # 包括的テストセット
    test_sentences = [
        "The sophisticated analysis is comprehensive.",
        "She efficiently investigated the mysterious disappearance.",
        "Students frequently encounter challenging mathematical equations.",
        "Innovative technologies revolutionize traditional methodologies.",
        "The remarkable achievement demonstrates exceptional capabilities."
    ]
    
    # 性能テスト実行
    results = engine.performance_test(test_sentences)
    
    print(f"\n🏆 Step 3 最終結果:")
    print(f"  ✅ ハイブリッドエンジン実装完了")
    print(f"  🎯 語彙認識率: {results['recognition_rate']:.1f}%")
    print(f"  ⚡ 処理語彙数: {results['total_words']} 語")
    print(f"  🔧 最適化手法併用: 形態素ルール + spaCy")
    
    # 16,000例文対応可能性の評価
    if results['recognition_rate'] >= 90:
        print(f"  🌟 16,000例文処理: 準備完了 (認識率{results['recognition_rate']:.1f}%)")
    else:
        print(f"  🔄 16,000例文処理: 追加調整推奨 (現在{results['recognition_rate']:.1f}%)")
