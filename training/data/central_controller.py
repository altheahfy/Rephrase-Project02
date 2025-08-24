#!/usr/bin/env python3
"""
Central Controller - Phase 2: 精度向上型制御機構
副詞重複問題の解決とスロット統合の精密化

設計原則:
- 副詞の重複配置を防止
- サブスロットとメインスロットの一貫性確保
- 段階的制御によるエラー削減
"""

class CentralController:
    """
    中央制御機構 Phase 2
    副詞重複防止と精度向上を実現
    """
    
    def __init__(self, mapper_instance):
        """
        初期化 - 既存mapperを包装し制御機能を追加
        
        Args:
            mapper_instance: DynamicGrammarMapperのインスタンス
        """
        self.mapper = mapper_instance
        self.phase = "Phase 2: Precision Enhancement Controller"
        print(f"🎯 Central Controller初期化: {self.phase}")
    
    def analyze_sentence(self, sentence):
        """
        精度向上型文章解析 - 副詞重複問題を解決
        
        Args:
            sentence (str): 解析対象の文章
            
        Returns:
            dict: 解析結果（精度向上版）
        """
        # 既存システムの結果を取得
        result = self.mapper.analyze_sentence(sentence)
        
        # Phase 2: 副詞重複問題の解決
        result = self._resolve_adverb_duplication(result)
        
        return result
    
    def _resolve_adverb_duplication(self, result):
        """
        副詞重複問題を解決
        
        Args:
            result (dict): 解析結果
            
        Returns:
            dict: 副詞重複を解決した結果
        """
        main_slots = result.get('main_slots', {})
        sub_slots = result.get('sub_slots', {})
        
        # サブスロットに副詞が存在する場合、メインスロットから同じ副詞を削除
        adverb_slots = ['M1', 'M2', 'M3']
        sub_adverb_slots = ['sub-m1', 'sub-m2', 'sub-m3']
        
        for i, adverb_slot in enumerate(adverb_slots):
            sub_adverb_slot = sub_adverb_slots[i]
            
            # サブスロットに副詞が存在し、メインスロットにも同じ値がある場合
            if (sub_adverb_slot in sub_slots and 
                adverb_slot in main_slots and
                sub_slots[sub_adverb_slot] == main_slots[adverb_slot]):
                
                print(f"🔧 副詞重複解決: {adverb_slot}='{main_slots[adverb_slot]}' をメインスロットから削除 (sub-slot存在)")
                
                # メインスロットから削除
                main_slots.pop(adverb_slot, None)
                if 'slots' in result:
                    result['slots'].pop(adverb_slot, None)
        
        # 結果を更新
        result['main_slots'] = main_slots
        
        print(f"🎯 副詞重複解決完了: main_slots={main_slots}")
        return result
    
    def get_system_info(self):
        """
        システム情報取得
        
        Returns:
            dict: システム構成情報
        """
        return {
            "controller_phase": self.phase,
            "underlying_system": "DynamicGrammarMapper",
            "mode": "precision_enhancement",
            "features": ["adverb_duplication_resolution", "slot_consistency_check"]
        }
