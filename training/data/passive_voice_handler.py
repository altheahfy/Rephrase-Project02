"""
PassiveVoiceHandler - 受動態専門ハンドラー

設計方針: 協力アプローチ採用
- 責任: 受動態（be動詞 + 過去分詞）の検出・分離のみ
- 協力: RelativeClauseHandlerからの要請で動作
- 報告: 結果はRelativeClauseHandler経由でCentralControllerに報告
"""

import spacy
from typing import Dict, Any, Optional

class PassiveVoiceHandler:
    """受動態構造の検出と分解を担当する専門ハンドラー"""
    
    def __init__(self):
        """PassiveVoiceHandlerの初期化"""
        self.nlp = spacy.load("en_core_web_sm")
        
        # be動詞リスト（受動態用）
        self.be_verbs = {
            'am', 'is', 'are', 'was', 'were', 
            'be', 'been', 'being'
        }
    
    def process(self, text: str) -> Optional[Dict[str, Any]]:
        """
        受動態構造を検出・分解する
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            受動態情報を含む辞書 or None（受動態でない場合）
        """
        if not text or not text.strip():
            return None
            
        doc = self.nlp(text.strip())
        
        # 受動態パターンを検出
        passive_info = self._detect_passive_pattern(doc)
        
        return passive_info
    
    def _detect_passive_pattern(self, doc) -> Optional[Dict[str, Any]]:
        """
        be動詞 + 過去分詞のパターンを検出
        
        Args:
            doc: spaCy Docオブジェクト
            
        Returns:
            受動態情報辞書 or None
        """
        tokens = [token.text for token in doc]
        
        for i, token in enumerate(doc):
            # be動詞をチェック
            if token.text.lower() in self.be_verbs:
                # 次のトークンが過去分詞かチェック（副詞があってもスキップ）
                next_idx = self._find_next_verb(doc, i + 1)
                
                if next_idx is not None:
                    past_participle = doc[next_idx]
                    
                    if self._is_past_participle(past_participle):
                        # 受動態パターン発見
                        return {
                            'is_passive': True,
                            'aux': token.text,
                            'verb': past_participle.text,
                            'pattern_type': 'passive_voice',
                            'be_index': i,
                            'participle_index': next_idx
                        }
        
        return None
    
    def _find_next_verb(self, doc, start_idx: int) -> Optional[int]:
        """
        次の動詞を探す（副詞をスキップ）- 専門分担型ハイブリッド解析
        
        Args:
            doc: spaCy Docオブジェクト
            start_idx: 検索開始インデックス
            
        Returns:
            動詞のインデックス or None
        """
        for i in range(start_idx, len(doc)):
            token = doc[i]
            # 副詞はスキップ
            if token.pos_ == 'ADV':
                continue
            # 動詞が見つかった（真の動詞のみ、形容詞は除外）
            if token.pos_ == 'VERB' or token.tag_ == 'VBN':
                return i
            # 形容詞（ADJ）は受動態の過去分詞ではないので除外
            if token.pos_ == 'ADJ':
                print(f"🔍 形容詞検出: {token.text} (POS=ADJ) - 受動態ではない")
                break
            # 他の品詞に達したら停止
            if token.pos_ in ['NOUN', 'PRON', 'PROPN']:
                break
                
        return None
    
    def _is_past_participle(self, token) -> bool:
        """
        トークンが過去分詞かどうかを判定
        
        Args:
            token: spaCyトークン
            
        Returns:
            過去分詞の場合True
        """
        # spaCy POS タグで過去分詞を確認
        if token.tag_ == 'VBN':  # Past participle
            return True
            
        # 規則変化（-ed）で確認
        word = token.text.lower()
        if word.endswith('ed') and len(word) > 3:
            return True
            
        return False
