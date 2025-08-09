# ===== 大規模データ処理検証テスト =====
# 16,000例文、4,000-6,000語彙対応テスト

import time
import random
from Enhanced_Rephrase_Parsing_Engine_v2 import EnhancedRephraseParsingEngine

def generate_test_sentences(count=100):
    """テスト用例文生成（実際の複雑さを模擬）"""
    
    # 様々な難易度の例文パターン
    patterns = [
        # 基本パターン
        "Where did you {} the {}?",
        "What are you {} about?", 
        "I have {} {} for a long time.",
        "She will be {} {} next year.",
        
        # 中級パターン  
        "The {} student {} the {} implications {}.",
        "I {} that you would {} this opportunity.",
        "Have you ever {} to {} before?",
        "When will you {} your {} project?",
        
        # 高難度パターン
        "The {} professor {} the {} methodology {} during the {}.",
        "I {} whether the {} approach would be {} for our {}.",
        "Having {} the preliminary results, we decided to {} the experiment.",
        "The {} committee unanimously {} to {} the new {}."
    ]
    
    # 語彙データベース（実際の4,000語彙を模擬）
    vocab_levels = {
        'basic': ['go', 'come', 'see', 'do', 'make', 'get', 'take', 'give', 'find', 'know'],
        'intermediate': ['realize', 'understand', 'accomplish', 'demonstrate', 'investigate', 
                        'analyze', 'evaluate', 'implement', 'coordinate', 'facilitate'],
        'advanced': ['comprehend', 'ascertain', 'perpetuate', 'ameliorate', 'substantiate',
                    'corroborate', 'exemplify', 'elucidate', 'consolidate', 'optimize']
    }
    
    nouns_levels = {
        'basic': ['book', 'car', 'house', 'person', 'time', 'place', 'thing', 'way', 'day', 'man'],
        'intermediate': ['opportunity', 'methodology', 'approach', 'project', 'solution', 
                        'strategy', 'analysis', 'framework', 'concept', 'principle'],
        'advanced': ['implications', 'paradigm', 'infrastructure', 'prerequisites', 'ramifications',
                    'methodology', 'epistemology', 'juxtaposition', 'dichotomy', 'synthesis']
    }
    
    adjectives_levels = {
        'basic': ['good', 'bad', 'big', 'small', 'new', 'old', 'long', 'short', 'high', 'low'],
        'intermediate': ['significant', 'comprehensive', 'effective', 'innovative', 'systematic',
                        'preliminary', 'substantial', 'crucial', 'fundamental', 'essential'],
        'advanced': ['perspicacious', 'multifaceted', 'ubiquitous', 'serendipitous', 'fortuitous',
                    'expeditious', 'meticulous', 'scrupulous', 'fastidious', 'punctilious']
    }
    
    adverbs_levels = {
        'basic': ['well', 'good', 'very', 'really', 'just', 'now', 'here', 'there', 'then', 'always'],
        'intermediate': ['effectively', 'significantly', 'systematically', 'comprehensively',
                        'successfully', 'efficiently', 'appropriately', 'consequently', 'furthermore'],
        'advanced': ['serendipitously', 'expeditiously', 'meticulously', 'scrupulously',
                    'perspicaciously', 'ubiquitously', 'fortuitously', 'fastidiously', 'punctiliously']
    }
    
    sentences = []
    
    for i in range(count):
        # 難易度をランダムに選択（実際の分布を模擬）
        if i < count * 0.4:  # 40%は基本レベル
            level = 'basic'
        elif i < count * 0.8:  # 40%は中級レベル  
            level = 'intermediate'
        else:  # 20%は高難度レベル
            level = 'advanced'
        
        # パターンとレベルに応じて例文生成
        pattern = random.choice(patterns)
        
        # パターンの{}を実際の語彙で置換
        words_needed = pattern.count('{}')
        replacement_words = []
        
        for _ in range(words_needed):
            word_type = random.choice(['verbs', 'nouns', 'adjectives', 'adverbs'])
            if word_type == 'verbs':
                word = random.choice(vocab_levels[level])
            elif word_type == 'nouns':
                word = random.choice(nouns_levels[level])
            elif word_type == 'adjectives':
                word = random.choice(adjectives_levels[level])
            else:
                word = random.choice(adverbs_levels[level])
            
            replacement_words.append(word)
        
        sentence = pattern.format(*replacement_words)
        sentences.append((sentence, level))
    
    return sentences

def run_scalability_test():
    """スケーラビリティテスト実行"""
    
    print("=== 16,000例文対応スケーラビリティテスト ===\n")
    
    # エンジン初期化
    engine = EnhancedRephraseParsingEngine()
    
    # テストサイズを段階的に増加
    test_sizes = [100, 500, 1000, 2000, 5000]
    
    results = {}
    
    for test_size in test_sizes:
        print(f"--- {test_size}文処理テスト開始 ---")
        
        # テスト例文生成
        test_sentences = generate_test_sentences(test_size)
        
        # 処理時間測定開始
        start_time = time.time()
        successful_parses = 0
        errors = 0
        
        # 各例文を解析
        for i, (sentence, level) in enumerate(test_sentences):
            try:
                result = engine.analyze_sentence_hybrid(sentence)
                if result['slots']:
                    successful_parses += 1
                    
                # 進捗表示（100文ごと）
                if (i + 1) % 100 == 0:
                    print(f"  処理済み: {i + 1}/{test_size} 文")
                    
            except Exception as e:
                errors += 1
                if errors <= 5:  # 最初の5エラーのみ表示
                    print(f"  エラー: {sentence} -> {e}")
        
        # 処理時間測定終了
        end_time = time.time()
        processing_time = end_time - start_time
        
        # 語彙統計取得
        vocab_stats = engine.get_vocabulary_coverage_report()
        
        # 結果記録
        results[test_size] = {
            'processing_time': processing_time,
            'sentences_per_second': test_size / processing_time,
            'successful_parses': successful_parses,
            'errors': errors,
            'success_rate': successful_parses / test_size * 100,
            'vocab_stats': vocab_stats
        }
        
        print(f"  結果: {test_size}文を{processing_time:.2f}秒で処理")
        print(f"  処理速度: {test_size / processing_time:.1f}文/秒")
        print(f"  成功率: {successful_parses / test_size * 100:.1f}%")
        print(f"  エラー: {errors}件")
        print()
    
    return results

def generate_performance_report(results):
    """パフォーマンスレポート生成"""
    
    print("=== パフォーマンス総合レポート ===\n")
    
    print("| 文数 | 処理時間(秒) | 処理速度(文/秒) | 成功率(%) | エラー数 |")
    print("|------|-------------|----------------|-----------|----------|")
    
    for size, data in results.items():
        print(f"| {size:,} | {data['processing_time']:.2f} | {data['sentences_per_second']:.1f} | {data['success_rate']:.1f} | {data['errors']} |")
    
    print("\n=== スケーラビリティ評価 ===")
    
    # 16,000文の処理予測
    largest_size = max(results.keys())
    largest_data = results[largest_size]
    
    scaling_factor = 16000 / largest_size
    predicted_time = largest_data['processing_time'] * scaling_factor
    predicted_speed = largest_data['sentences_per_second']
    
    print(f"16,000文処理予測:")
    print(f"  予測処理時間: {predicted_time:.2f}秒 ({predicted_time/60:.1f}分)")
    print(f"  予測処理速度: {predicted_speed:.1f}文/秒")
    print(f"  予測成功率: {largest_data['success_rate']:.1f}%")
    
    # メモリ使用量予測
    predicted_memory = largest_size * 0.02 * scaling_factor  # 文あたり約0.02MB想定
    print(f"  予測メモリ使用量: {predicted_memory:.0f}MB")
    
    print("\n=== 語彙カバレッジ最終統計 ===")
    print(results[largest_size]['vocab_stats'])
    
    # 実用性評価
    print("\n=== 実用性評価 ===")
    if predicted_time < 300:  # 5分以内
        print("✅ 高速処理: 16,000文を5分以内で処理可能")
    elif predicted_time < 600:  # 10分以内
        print("⚠️ 中速処理: 16,000文を10分以内で処理可能")
    else:
        print("❌ 低速処理: 最適化が必要")
    
    if largest_data['success_rate'] > 85:
        print("✅ 高精度: 成功率85%以上達成")
    elif largest_data['success_rate'] > 70:
        print("⚠️ 中精度: 成功率70%以上達成")
    else:
        print("❌ 低精度: 精度改善が必要")
    
    if predicted_memory < 500:
        print("✅ 省メモリ: 500MB以内での動作")
    elif predicted_memory < 1000:
        print("⚠️ 中メモリ: 1GB以内での動作")
    else:
        print("❌ 大メモリ: メモリ最適化が必要")

# テスト実行
if __name__ == "__main__":
    results = run_scalability_test()
    generate_performance_report(results)
