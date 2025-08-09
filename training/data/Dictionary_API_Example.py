# Dictionary API Integration Example

import requests
import json
from functools import lru_cache

class DictionaryAPIEngine:
    """オンライン辞書APIを活用したパーサー"""
    
    def __init__(self):
        # Free Dictionary API (制限なし)
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        
        # キャッシュで同じ単語の重複検索を避ける
        self.word_cache = {}
    
    @lru_cache(maxsize=5000)  # 最大5000語をメモリキャッシュ
    def get_word_info(self, word):
        """単語情報をAPIから取得（キャッシュ付き）"""
        
        if word.lower() in self.word_cache:
            return self.word_cache[word.lower()]
        
        try:
            response = requests.get(f"{self.api_url}{word.lower()}", timeout=2)
            if response.status_code == 200:
                data = response.json()[0]
                
                # 品詞情報を抽出
                parts_of_speech = []
                for meaning in data.get('meanings', []):
                    parts_of_speech.append(meaning['partOfSpeech'])
                
                word_info = {
                    'word': word,
                    'pos_list': parts_of_speech,
                    'is_verb': 'verb' in parts_of_speech,
                    'is_noun': 'noun' in parts_of_speech,
                    'is_adjective': 'adjective' in parts_of_speech
                }
                
                # キャッシュに保存
                self.word_cache[word.lower()] = word_info
                return word_info
                
        except (requests.RequestException, json.JSONDecodeError, IndexError):
            # API失敗時はフォールバック処理
            return self.fallback_word_analysis(word)
        
        return None
    
    def fallback_word_analysis(self, word):
        """API失敗時の形態素解析フォールバック"""
        word_lower = word.lower()
        
        # 基本的な形態素パターン
        if word_lower.endswith('ed'):
            return {'word': word, 'likely_pos': 'past_verb'}
        elif word_lower.endswith('ing'):
            return {'word': word, 'likely_pos': 'present_participle'}
        elif word_lower.endswith('ly'):
            return {'word': word, 'likely_pos': 'adverb'}
        
        return {'word': word, 'likely_pos': 'unknown'}

# 使用例
api_engine = DictionaryAPIEngine()

# 未知語でもAPIで解決
word_info = api_engine.get_word_info("ameliorate")  # 高難度語彙
print(f"ameliorate: {word_info}")
