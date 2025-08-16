#!/usr/bin/env python3
"""
中央位置検出エンジン
===================

設計思想：
- 各ハンドラーが個別に位置情報を管理するのではなく
- 中央エンジンが原文とサブスロット内容を照合して位置を一括判定
- 一元管理により一貫性と保守性を向上

Author: GitHub Copilot
Date: 2025-08-16
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SubSlotMatch:
    """サブスロット照合結果"""
    sub_slot_type: str  # 'sub-s', 'sub-v', 'sub-o1', 'sub-c1' など
    position: str       # 'S', 'O1', 'M1' など（どのメインスロットの分解か）
    content: str        # サブスロットの内容
    start_pos: int      # 原文での開始位置
    end_pos: int        # 原文での終了位置
    confidence: float   # マッチング信頼度

class CentralPositionDetector:
    """
    中央位置検出エンジン
    
    機能：
    1. 原文解析により各語の位置情報を取得
    2. サブスロット内容と原文を照合して位置を特定
    3. 位置別サブスロット名を自動生成（S-sub-s, O1-sub-v等）
    """
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        
        # メインスロット優先順位（競合時の解決用）
        self.MAIN_SLOT_PRIORITY = ['S', 'V', 'O1', 'O2', 'C1', 'C2', 'Aux', 'M1', 'M2', 'M3']
        
    def detect_positions(self, 
                        sentence: str, 
                        main_slots: Dict[str, str], 
                        sub_slots: Dict[str, str]) -> Dict[str, str]:
        """
        メイン機能：サブスロットの位置を検出
        
        Args:
            sentence: 原文
            main_slots: メインスロット {'S': 'I', 'V': 'know', 'O1': 'the person'}
            sub_slots: サブスロット {'sub-s': 'the person whose dog', 'sub-v': 'barks'}
            
        Returns:
            位置別サブスロット {'S-sub-s': 'I', 'O1-sub-s': 'the person whose dog', 'O1-sub-v': 'barks'}
        """
        if not sub_slots:
            return {}
            
        if self.debug:
            print(f"🔍 中央位置検出開始:")
            print(f"  原文: '{sentence}'")
            print(f"  メインスロット: {main_slots}")
            print(f"  サブスロット: {sub_slots}")
        
        # 1. 各サブスロットの原文での位置を特定
        sub_slot_matches = self._find_sub_slot_positions(sentence, sub_slots)
        
        # 2. メインスロットとの照合で位置を決定
        positional_sub_slots = self._determine_positions(sentence, main_slots, sub_slot_matches)
        
        if self.debug:
            print(f"  ✅ 位置別サブスロット: {positional_sub_slots}")
            
        return positional_sub_slots
    
    def _find_sub_slot_positions(self, sentence: str, sub_slots: Dict[str, str]) -> List[SubSlotMatch]:
        """サブスロット内容の原文での位置を特定"""
        matches = []
        
        for sub_type, content in sub_slots.items():
            if not content.strip():
                continue
                
            # 原文でのマッチング検索
            match_info = self._find_content_in_sentence(sentence, content)
            
            if match_info:
                matches.append(SubSlotMatch(
                    sub_slot_type=sub_type,
                    position="",  # 後で決定
                    content=content,
                    start_pos=match_info['start'],
                    end_pos=match_info['end'],
                    confidence=match_info['confidence']
                ))
                
        return matches
    
    def _find_content_in_sentence(self, sentence: str, content: str) -> Optional[Dict]:
        """コンテンツの原文での位置を検索"""
        
        # 1. 完全一致検索
        start = sentence.lower().find(content.lower())
        if start != -1:
            return {
                'start': start,
                'end': start + len(content),
                'confidence': 1.0
            }
            
        # 2. 単語レベル部分一致
        content_words = content.lower().split()
        sentence_words = sentence.lower().split()
        
        # 最長共通部分列検索
        best_match = self._find_longest_common_subsequence(content_words, sentence_words)
        
        if best_match and best_match['confidence'] > 0.6:
            # 文字位置に変換
            word_start_pos = self._get_word_position_in_sentence(sentence, best_match['start_word_idx'])
            word_end_pos = self._get_word_position_in_sentence(sentence, best_match['end_word_idx'])
            
            return {
                'start': word_start_pos,
                'end': word_end_pos,
                'confidence': best_match['confidence']
            }
            
        return None
    
    def _find_longest_common_subsequence(self, words1: List[str], words2: List[str]) -> Optional[Dict]:
        """最長共通部分列を検索"""
        # 簡易実装：連続する共通単語の最長部分を検索
        best_match = None
        best_score = 0
        
        for i in range(len(words2)):
            for j in range(len(words1)):
                # words1[j:]とwords2[i:]の共通プレフィックス長を計算
                common_len = 0
                while (j + common_len < len(words1) and 
                       i + common_len < len(words2) and
                       words1[j + common_len] == words2[i + common_len]):
                    common_len += 1
                
                if common_len > 0:
                    confidence = common_len / max(len(words1), len(words2))
                    if confidence > best_score:
                        best_score = confidence
                        best_match = {
                            'start_word_idx': i,
                            'end_word_idx': i + common_len - 1,
                            'confidence': confidence
                        }
        
        return best_match
    
    def _get_word_position_in_sentence(self, sentence: str, word_idx: int) -> int:
        """単語インデックスから文字位置を取得"""
        words = sentence.split()
        if word_idx >= len(words):
            return len(sentence)
            
        # word_idx番目の単語の開始位置を検索
        current_pos = 0
        for i, word in enumerate(words):
            if i == word_idx:
                return current_pos
            current_pos += len(word) + 1  # +1 for space
            
        return len(sentence)
    
    def _determine_positions(self, 
                           sentence: str, 
                           main_slots: Dict[str, str], 
                           sub_slot_matches: List[SubSlotMatch]) -> Dict[str, str]:
        """メインスロットとの照合で位置を決定"""
        positional_sub_slots = {}
        
        for match in sub_slot_matches:
            # 各メインスロットとの重複度を計算
            best_position = self._find_best_position_match(sentence, main_slots, match)
            
            if best_position:
                # 位置別サブスロット名を生成
                positional_name = f"{best_position}-{match.sub_slot_type}"
                positional_sub_slots[positional_name] = match.content
                
                if self.debug:
                    print(f"    {match.sub_slot_type}='{match.content}' → {positional_name}")
        
        return positional_sub_slots
    
    def _find_best_position_match(self, 
                                sentence: str, 
                                main_slots: Dict[str, str], 
                                sub_match: SubSlotMatch) -> Optional[str]:
        """サブスロットに最適なメインスロット位置を特定"""
        
        best_position = None
        best_overlap = 0
        
        for slot_name, slot_content in main_slots.items():
            if not slot_content.strip():
                continue
                
            # 重複度計算
            overlap = self._calculate_content_overlap(sub_match.content, slot_content)
            
            if overlap > best_overlap:
                best_overlap = overlap
                best_position = slot_name
                
        # 閾値チェック
        if best_overlap < 0.3:  # 30%未満の重複は信頼性が低い
            # フォールバック：優先順位で決定
            return self._get_fallback_position(sub_match.sub_slot_type)
            
        return best_position
    
    def _calculate_content_overlap(self, sub_content: str, main_content: str) -> float:
        """コンテンツ重複度を計算"""
        
        # 1. 完全包含チェック
        if sub_content.lower() in main_content.lower() or main_content.lower() in sub_content.lower():
            return 1.0
            
        # 2. 単語レベル重複度
        sub_words = set(sub_content.lower().split())
        main_words = set(main_content.lower().split())
        
        if not sub_words or not main_words:
            return 0.0
            
        intersection = sub_words.intersection(main_words)
        union = sub_words.union(main_words)
        
        return len(intersection) / len(union)
    
    def _get_fallback_position(self, sub_slot_type: str) -> str:
        """フォールバック位置決定"""
        
        # サブスロットタイプから推定
        type_mapping = {
            'sub-s': 'S',
            'sub-v': 'V', 
            'sub-o1': 'O1',
            'sub-o2': 'O2',
            'sub-c1': 'C1',
            'sub-c2': 'C2',
            'sub-aux': 'Aux',
            'sub-m1': 'M1',
            'sub-m2': 'M2',
            'sub-m3': 'M3'
        }
        
        return type_mapping.get(sub_slot_type, 'S')  # デフォルトはS

# 使用例とテスト
if __name__ == "__main__":
    detector = CentralPositionDetector(debug=True)
    
    # テストケース1: 関係節
    sentence1 = "I know the person whose dog barks."
    main_slots1 = {'S': 'I', 'V': 'know', 'O1': 'the person'}
    sub_slots1 = {'sub-s': 'the person whose dog', 'sub-v': 'barks'}
    
    result1 = detector.detect_positions(sentence1, main_slots1, sub_slots1)
    print(f"\n✅ 期待結果: {{'O1-sub-s': 'the person whose dog', 'O1-sub-v': 'barks'}}")
    print(f"✅ 実際結果: {result1}")
    
    # テストケース2: 受動態
    sentence2 = "The car was stolen by someone."
    main_slots2 = {'S': 'The car', 'Aux': 'was', 'V': 'stolen', 'M1': 'by someone'}
    sub_slots2 = {'sub-s': 'someone', 'sub-v': 'stole', 'sub-o1': 'The car'}
    
    result2 = detector.detect_positions(sentence2, main_slots2, sub_slots2)
    print(f"\n✅ 期待結果: {{'M1-sub-s': 'someone', 'M1-sub-v': 'stole', 'M1-sub-o1': 'The car'}}")
    print(f"✅ 実際結果: {result2}")
