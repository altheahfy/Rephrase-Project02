# Option 1: インターネット辞書API活用
# メリット・デメリット・実装方法の詳細

import requests
import json
import time

class OnlineDictionaryHelper:
    """オンライン辞書の実際のテスト"""
    
    def __init__(self):
        # 無料で使える辞書API
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    def test_word_lookup(self, word):
        """実際に辞書APIをテスト"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_url}{word}", timeout=3)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()[0]
                meanings = data.get('meanings', [])
                parts_of_speech = [m['partOfSpeech'] for m in meanings]
                
                return {
                    'word': word,
                    'found': True,
                    'pos_list': parts_of_speech,
                    'response_time': response_time,
                    'example': meanings[0].get('definitions', [{}])[0].get('definition', 'No definition')
                }
            else:
                return {'word': word, 'found': False, 'response_time': response_time, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'word': word, 'found': False, 'response_time': None, 'error': str(e)}

# 実際のテスト
if __name__ == "__main__":
    print("=== オンライン辞書APIテスト ===\n")
    
    dictionary = OnlineDictionaryHelper()
    
    # テスト語彙（様々な難易度）
    test_words = [
        'sophisticated',  # 高難度形容詞
        'efficiently',    # 副詞
        'investigation',  # 名詞
        'analyze',        # 動詞
        'comprehensive',  # 形容詞
        'nonexistentword' # 存在しない語（エラーテスト）
    ]
    
    results = []
    total_time = 0
    
    for word in test_words:
        print(f"検索中: {word}")
        result = dictionary.test_word_lookup(word)
        results.append(result)
        
        if result['found']:
            print(f"✅ 発見: {', '.join(result['pos_list'])}")
            print(f"   定義: {result['example'][:100]}...")
        else:
            print(f"❌ 未発見: {result.get('error', 'Unknown error')}")
        
        if result['response_time']:
            print(f"   応答時間: {result['response_time']:.2f}秒")
            total_time += result['response_time']
        
        print()
    
    # 統計
    successful_lookups = sum(1 for r in results if r['found'])
    print(f"=== 統計結果 ===")
    print(f"成功率: {successful_lookups}/{len(test_words)} ({successful_lookups/len(test_words)*100:.1f}%)")
    print(f"平均応答時間: {total_time/len(test_words):.2f}秒")
    
    # メリット・デメリット分析
    print(f"\n=== オンライン辞書のメリット・デメリット ===")
    print("✅ メリット:")
    print("  - 語彙制限なし（数十万語対応）")
    print("  - 最新語彙も含む") 
    print("  - 詳細な品詞情報取得可能")
    print("  - 実装が比較的簡単")
    
    print("\n❌ デメリット:")
    print("  - インターネット接続必須")
    print("  - API応答待機で処理速度低下")
    print("  - APIサーバー障害時の影響")
    print("  - 大量処理時のレート制限")
    
    # 16,000例文処理時の予測
    avg_response_time = total_time / len(test_words) if total_time > 0 else 0.5
    words_per_sentence = 8  # 平均語数
    total_api_calls = 16000 * words_per_sentence * 0.3  # 30%が未知語と仮定
    estimated_time = total_api_calls * avg_response_time
    
    print(f"\n=== 16,000例文処理時の予測 ===")
    print(f"予想API呼び出し数: {total_api_calls:,}回")
    print(f"予想処理時間: {estimated_time/60:.1f}分")
    
    if estimated_time < 300:  # 5分以内
        print("✅ 実用的な処理時間")
    elif estimated_time < 1800:  # 30分以内
        print("⚠️ やや時間がかかるが許容範囲")
    else:
        print("❌ 処理時間が長すぎる")
