# ===== Rephrase Parsing Engine with Hybrid Vocabulary =====
# 語彙制限を解決するハイブリッド版

import json
import re
import os

# ハイブリッド語彙エンジンのインポート
import sys
sys.path.append(os.path.dirname(__file__))
from Hybrid_Vocabulary_Engine import HybridVocabularyEngine

class EnhancedRephraseParsingEngine:
    """語彙制限を解決したRephrase品詞分解エンジン"""
    
    def __init__(self):
        self.engine_name = "Enhanced Rephrase Parsing Engine v2.0"
        
        # 既存のルールベースエンジン（高速処理用）
        self.rules_data = self.load_rules()
        
        # 新しいハイブリッド語彙エンジン（未知語対応）
        self.vocab_engine = HybridVocabularyEngine()
        
        # パフォーマンス統計
        self.stats = {
            'total_words_analyzed': 0,
            'core_dict_hits': 0,
            'morphology_hits': 0,
            'context_fallbacks': 0,
            'unknown_words': 0
        }
    
    def load_rules(self):
        """既存の文法ルールデータを読み込み"""
        rules_file = os.path.join(os.path.dirname(__file__), 'rephrase_rules_v1.0.json')
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_basic_rules()
    
    def get_basic_rules(self):
        """基本的な文法ルールセット"""
        return {
            "cognitive_verbs": ["think", "believe", "know", "realize", "understand", "feel", "guess", "suppose"],
            "modal_verbs": ["will", "would", "can", "could", "may", "might", "must", "should", "ought"],
            "be_verbs": ["am", "is", "are", "was", "were", "being", "been"],
            "have_verbs": ["have", "has", "had"],
            "copular_verbs": ["become", "seem", "appear", "look", "sound", "feel", "taste", "smell"],
            "ditransitive_verbs": ["give", "tell", "show", "send", "teach", "buy", "make", "get"],
            "wh_words": ["what", "where", "when", "who", "why", "how", "which", "whose"],
            "irregular_past_participles": {
                "seen": "see", "done": "do", "gone": "go", "taken": "take", "given": "give",
                "written": "write", "spoken": "speak", "broken": "break", "chosen": "choose",
                "driven": "drive", "eaten": "eat", "fallen": "fall", "forgotten": "forget"
            }
        }
    
    def analyze_word_enhanced(self, word, context=None, position=None):
        """ハイブリッド語彙解析を使用した語彙判定"""
        
        self.stats['total_words_analyzed'] += 1
        
        # まず既存のルールベース辞書をチェック
        word_lower = word.lower()
        
        # 高頻出語の高速処理
        if word_lower in self.rules_data.get('be_verbs', []):
            self.stats['core_dict_hits'] += 1
            return {'pos': 'be_verb', 'confidence': 0.98, 'method': 'rule_based'}
        
        if word_lower in self.rules_data.get('modal_verbs', []):
            self.stats['core_dict_hits'] += 1
            return {'pos': 'modal_verb', 'confidence': 0.98, 'method': 'rule_based'}
        
        if word_lower in self.rules_data.get('wh_words', []):
            self.stats['core_dict_hits'] += 1
            return {'pos': 'wh_word', 'confidence': 0.98, 'method': 'rule_based'}
        
        # ハイブリッド語彙エンジンによる解析
        vocab_result = self.vocab_engine.analyze_word(word, context)
        
        # 統計更新
        if vocab_result['analysis_method'] == 'core_dictionary':
            self.stats['core_dict_hits'] += 1
        elif vocab_result['analysis_method'] == 'morphology':
            self.stats['morphology_hits'] += 1
        elif vocab_result['analysis_method'] == 'context':
            self.stats['context_fallbacks'] += 1
        
        if vocab_result['pos'] == 'unknown':
            self.stats['unknown_words'] += 1
        
        return vocab_result
    
    def analyze_sentence_hybrid(self, sentence):
        """ハイブリッド解析による文分解"""
        
        sentence = sentence.strip()
        if not sentence:
            return {}
        
        # 1. 全語彙をハイブリッド解析
        words = sentence.split()
        word_analyses = []
        
        for i, word in enumerate(words):
            analysis = self.analyze_word_enhanced(word, sentence, i)
            analysis['word'] = word
            analysis['position'] = i
            word_analyses.append(analysis)
        
        # 2. 既存の文法パターン解析と組み合わせ
        if self.is_question(sentence):
            slots = self.analyze_question_hybrid(sentence, word_analyses)
        else:
            slots = self.analyze_statement_hybrid(sentence, word_analyses)
        
        # 3. メタデータを追加
        result = {
            'slots': slots,
            'word_analyses': word_analyses,
            'sentence_type': self.determine_sentence_type(sentence),
            'vocabulary_stats': self.stats.copy()
        }
        
        return result
    
    def analyze_question_hybrid(self, sentence, word_analyses):
        """疑問文のハイブリッド解析"""
        
        slots = {}
        sentence_clean = sentence.replace('?', '').strip()
        words = sentence_clean.split()
        
        # Wh疑問文パターン
        first_word = words[0].lower() if words else ""
        
        if first_word in ['what', 'where', 'when', 'who', 'why', 'how', 'which', 'whose']:
            # Wh疑問文の解析
            slots['M1'] = words[0]  # 疑問詞
            
            # 残りの語彙をハイブリッド解析で分類
            remaining_words = words[1:]
            remaining_analyses = word_analyses[1:]
            
            # 助動詞検出（didなど）
            for i, analysis in enumerate(remaining_analyses):
                word = remaining_words[i]
                if analysis['pos'] in ['modal_verb', 'aux_verb'] or word.lower() in ['do', 'did', 'does']:
                    if 'Aux' not in slots:
                        slots['Aux'] = word
                        continue
                
                # 主語検出（代名詞など）
                if analysis['pos'] in ['pronoun', 'probable_subject']:
                    if 'S' not in slots:
                        slots['S'] = word
                        continue
                
                # 動詞検出
                if analysis['pos'] in ['verb', 'probable_verb'] or word.endswith('ed'):
                    if 'V' not in slots:
                        slots['V'] = word
                        continue
                
                # 残りは目的語として処理
                if 'O1' not in slots:
                    slots['O1'] = word
                else:
                    # 複数目的語の場合は結合
                    slots['O1'] += f" {word}"
        
        # スロット表示順序を設定
        slots['Slot_display_order'] = ['M1', 'Aux', 'S', 'V', 'O1', 'O2', 'M3', 'M4', 'M5']
        
        return slots
    
    def analyze_statement_hybrid(self, sentence, word_analyses):
        """平叙文のハイブリッド解析"""
        
        slots = {}
        words = [analysis['word'] for analysis in word_analyses]
        
        # 基本的なS-V-O構造の解析
        subject_found = False
        verb_found = False
        
        for i, analysis in enumerate(word_analyses):
            word = analysis['word']
            pos = analysis['pos']
            
            # 主語検出
            if not subject_found and pos in ['pronoun', 'probable_subject']:
                slots['S'] = word
                subject_found = True
                continue
            
            # 動詞検出
            if not verb_found and pos in ['verb', 'probable_verb', 'be_verb', 'modal_verb']:
                if pos == 'modal_verb':
                    slots['Aux'] = word
                else:
                    slots['V'] = word
                    verb_found = True
                continue
            
            # 目的語検出
            if verb_found and pos in ['probable_object', 'noun']:
                if 'O1' not in slots:
                    slots['O1'] = word
                else:
                    slots['O2'] = word
                continue
        
        # スロット表示順序を設定
        slots['Slot_display_order'] = ['S', 'Aux', 'V', 'O1', 'O2', 'M3', 'M4', 'M5']
        
        return slots
    
    def is_question(self, sentence):
        """疑問文判定"""
        return sentence.strip().endswith('?') or sentence.split()[0].lower() in ['what', 'where', 'when', 'who', 'why', 'how', 'which', 'whose', 'do', 'does', 'did', 'is', 'are', 'was', 'were']
    
    def determine_sentence_type(self, sentence):
        """文型判定"""
        if self.is_question(sentence):
            return "interrogative"
        elif sentence.strip().endswith('!'):
            return "exclamatory"
        else:
            return "declarative"
    
    def get_vocabulary_coverage_report(self):
        """語彙カバレッジレポート"""
        total = self.stats['total_words_analyzed']
        if total == 0:
            return "まだ解析していません"
        
        report = f"""
=== 語彙解析統計 ===
総解析語数: {total}
コア辞書ヒット: {self.stats['core_dict_hits']} ({self.stats['core_dict_hits']/total*100:.1f}%)
形態素解析ヒット: {self.stats['morphology_hits']} ({self.stats['morphology_hits']/total*100:.1f}%)
文脈推定使用: {self.stats['context_fallbacks']} ({self.stats['context_fallbacks']/total*100:.1f}%)
未知語: {self.stats['unknown_words']} ({self.stats['unknown_words']/total*100:.1f}%)
"""
        return report

# テスト実行例
if __name__ == "__main__":
    engine = EnhancedRephraseParsingEngine()
    
    # テスト文章（様々な難易度）
    test_sentences = [
        "Where did you get it?",
        "I have not seen you for a long time.",
        "The perspicacious student comprehended the multifaceted implications effortlessly.",
        "What are you thinking about?",
        "She will be studying abroad next year."
    ]
    
    print("=== Enhanced Rephrase Parsing Engine Test ===\n")
    
    for sentence in test_sentences:
        print(f"文: {sentence}")
        result = engine.analyze_sentence_hybrid(sentence)
        
        print("スロット分解:")
        for slot, value in result['slots'].items():
            if slot != 'Slot_display_order':
                print(f"  {slot}: {value}")
        
        print("語彙解析詳細:")
        for word_analysis in result['word_analyses']:
            print(f"  {word_analysis['word']} -> {word_analysis['pos']} (method: {word_analysis['analysis_method']}, confidence: {word_analysis.get('confidence', 'N/A')})")
        
        print("-" * 50)
    
    # 語彙カバレッジレポート
    print(engine.get_vocabulary_coverage_report())
