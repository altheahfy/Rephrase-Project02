#!/usr/bin/env python3
"""
Question Handler - New System Architecture
新規システム設計仕様書準拠の疑問文処理ハンドラー

設計方針:
1. spaCyによる品詞分析・依存関係解析を活用
2. ハードコーディング最小化
3. Human Grammar Pattern認識
4. Central Controllerとのみ接続
5. 段階的100%精度達成目標

対応疑問文:
- Wh疑問文: What did he tell her?
- Yes/No疑問文: Did he tell her?
- 助動詞倒置: Can you help me?
- be動詞疑問文: Is she happy?
"""

import spacy
from typing import Dict, List, Optional, Any

class QuestionHandler:
    """
    新システム設計仕様書準拠の疑問文ハンドラー
    spaCy専門分担型ハイブリッド解析による疑問文処理
    """
    
    def __init__(self):
        """spaCy pipeline初期化"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError("spaCy英語モデル 'en_core_web_sm' が見つかりません")
    
    # 疑問詞の分類（Human Grammar Pattern）
    WH_WORDS = {
        'what': 'O2',      # 目的語として質問: What did he tell her?
        'who': 'S',        # 主語として質問: Who called you?
        'whom': 'O1',      # 目的語として質問: Whom did you see?
        'where': 'M2',     # 場所修飾語: Where did he go?
        'when': 'M2',      # 時間修飾語: When did he arrive?
        'why': 'M2',       # 理由修飾語: Why did he leave?
        'how': 'M2',       # 方法修飾語: How did he do it?
        'which': 'O2',     # 選択目的語: Which book did you read?
        'whose': 'O2'      # 所有目的語: Whose car is this?
    }
    
    def is_question(self, text: str) -> bool:
        """
        疑問文判定
        
        Args:
            text: 入力文
            
        Returns:
            bool: 疑問文の場合True
        """
        if not text or not text.strip():
            return False
            
        text = text.strip()
        
        # 疑問符チェック
        if text.endswith('?'):
            return True
            
        # spaCy解析による疑問文パターン検出
        doc = self.nlp(text)
        
        # 文頭のWH語検出
        if doc and doc[0].text.lower() in self.WH_WORDS:
            return True
        
        # 修飾語系WH語検出
        if doc and doc[0].text.lower() in self.MODIFIER_WH_WORDS:
            return True
            
        # 助動詞倒置パターン検出（依存関係専門分野）
        for token in doc:
            if (token.pos_ == 'AUX' and token.i == 0 and 
                token.dep_ in ['aux', 'cop'] and token.head.pos_ == 'VERB'):
                return True
                
        return False
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        疑問文処理メイン関数
        
        Args:
            text: 入力疑問文
            
        Returns:
            Dict: 処理結果（slots, question_type, success等）
        """
        if not self.is_question(text):
            return {
                'success': False,
                'slots': {},
                'question_type': None,
                'error': '疑問文ではありません'
            }
        
        doc = self.nlp(text)
        
        # 疑問文タイプ判定
        question_type = self._identify_question_type(doc)
        
        # スロット分解
        if question_type == 'wh_question':
            slots = self._process_wh_question(doc)
        elif question_type == 'yes_no_question':
            slots = self._process_yes_no_question(doc)
        else:
            slots = {}
        
        return {
            'success': bool(slots),
            'slots': slots,
            'question_type': question_type,
            'metadata': {
                'handler': 'question',
                'spacy_analysis': True,
                'confidence': self._calculate_confidence(slots)
            }
        }
    
    def _identify_question_type(self, doc) -> str:
        """
        疑問文タイプ識別（Human Grammar Pattern）
        
        Args:
            doc: spaCy Doc object
            
        Returns:
            str: 疑問文タイプ
        """
        if not doc:
            return 'unknown'
        
        # WH疑問文判定（品詞分析専門分野）
        first_token = doc[0].text.lower()
        if first_token in self.WH_WORDS or first_token in self.MODIFIER_WH_WORDS:
            return 'wh_question'
        
        # Yes/No疑問文判定（依存関係専門分野）
        # 助動詞・be動詞が文頭に来る倒置パターン
        if doc[0].pos_ == 'AUX' or (doc[0].lemma_ in ['be', 'do', 'have'] and doc[0].pos_ in ['AUX', 'VERB']):
            return 'yes_no_question'
        
        return 'unknown'
    
    def _process_wh_question(self, doc) -> Dict[str, str]:
        """
        WH疑問文処理: What did he tell her at the store?
        
        期待される分解:
        - O2: What (疑問詞)
        - Aux: did (助動詞)
        - S: he (主語)
        - V: tell (動詞)
        - O1: her (目的語1)
        - M2: at the store (修飾語)
        """
        slots = {}
        
        try:
            # WH語検出・配置（品詞分析専門分野）
            wh_word = doc[0].text.lower()
            if wh_word in self.WH_WORDS:
                target_slot = self.WH_WORDS[wh_word]
                slots[target_slot] = doc[0].text
            
            # 助動詞検出（品詞分析専門分野）
            for token in doc:
                if token.pos_ == 'AUX' and token.lemma_ in ['do', 'be', 'have', 'will', 'can', 'must', 'should']:
                    slots['Aux'] = token.text
                    break
            
            # 主語検出（依存関係専門分野）
            for token in doc:
                if token.dep_ == 'nsubj':
                    slots['S'] = token.text
                    break
            
            # 主動詞検出（依存関係専門分野）
            for token in doc:
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    slots['V'] = token.text
                    break
            
            # 目的語検出（依存関係専門分野）
            for token in doc:
                if token.dep_ == 'dobj' and 'O1' not in slots:
                    slots['O1'] = token.text
                    break
            
            # 注意: 修飾語（前置詞句等）の処理はAdverbHandlerの責任
            # 責任分担原則に従い、疑問文ハンドラーでは修飾語処理を行わない
                
        except Exception as e:
            print(f"WH疑問文処理エラー: {e}")
        
        return slots
    
    def _process_yes_no_question(self, doc) -> Dict[str, str]:
        """
        Yes/No疑問文処理: Did he tell her?
        
        期待される分解:
        - Aux: Did (助動詞)
        - S: he (主語)
        - V: tell (動詞)
        - O1: her (目的語)
        """
        slots = {}
        
        try:
            # 助動詞検出（文頭、品詞分析専門分野）
            if doc[0].pos_ == 'AUX' or doc[0].lemma_ in ['do', 'be', 'have']:
                slots['Aux'] = doc[0].text
            
            # 主語検出（依存関係専門分野）
            for token in doc:
                if token.dep_ == 'nsubj':
                    slots['S'] = token.text
                    break
            
            # 主動詞検出（依存関係専門分野）
            for token in doc:
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    slots['V'] = token.text
                    break
            
            # 目的語検出（依存関係専門分野）
            for token in doc:
                if token.dep_ == 'dobj':
                    slots['O1'] = token.text
                    break
                    
        except Exception as e:
            print(f"Yes/No疑問文処理エラー: {e}")
        
        return slots
    
    def _calculate_confidence(self, slots: Dict[str, str]) -> float:
        """
        処理信頼度計算
        
        Args:
            slots: 分解されたスロット
            
        Returns:
            float: 信頼度 (0.0-1.0)
        """
        if not slots:
            return 0.0
        
        # 基本要素の存在チェック
        essential_slots = ['S', 'V']  # 主語・動詞は必須
        found_essential = sum(1 for slot in essential_slots if slot in slots)
        
        # 助動詞またはWH語の存在チェック
        has_aux_or_wh = 'Aux' in slots or any(slot in ['O2', 'M2'] for slot in slots if slots[slot].lower() in self.WH_WORDS)
        
        confidence = (found_essential / len(essential_slots)) * 0.7
        if has_aux_or_wh:
            confidence += 0.3
            
        return min(confidence, 1.0)

# テスト用関数
def test_question_handler():
    """疑問文ハンドラーのテスト"""
    handler = QuestionHandler()
    
    test_cases = [
        "What did he tell her at the store?",
        "Did he tell her?",
        "Who called you?",
        "Where did he go?",
        "Is she happy?",
        "Can you help me?"
    ]
    
    print("=== Question Handler テスト ===")
    for i, sentence in enumerate(test_cases, 1):
        print(f"\nテストケース {i}: {sentence}")
        result = handler.process(sentence)
        print(f"成功: {result['success']}")
        print(f"タイプ: {result['question_type']}")
        print(f"スロット: {result['slots']}")
        print(f"信頼度: {result['metadata']['confidence']:.2f}")

if __name__ == "__main__":
    test_question_handler()
