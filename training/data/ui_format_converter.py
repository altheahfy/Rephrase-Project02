#!/usr/bin/env python3
"""
UI Format Converter
現在のCentralController出力をUI最終形態に変換

【設計方針】
- CentralControllerの出力を破壊せず、変換レイヤーとして機能
- UI側が必要な時にいつでも変換可能
- 段階的に機能拡張（Subslot対応、V_group_key自動判定など）

【出力形式】
UI最終形態: slot_order_data.json形式の配列
[
  {
    "構文ID": "",
    "V_group_key": "action",
    "例文ID": "ex001",
    "Slot": "S",
    "SlotPhrase": "The car",
    "SlotText": "",
    "PhraseType": "word",
    "SubslotID": "",
    "SubslotElement": "",
    "SubslotText": "",
    "Slot_display_order": 2,
    "display_order": 0,
    "QuestionType": ""
  }
]
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class UIFormatConverter:
    """CentralController出力をUI形式に変換"""
    
    def __init__(self):
        """変換設定の初期化"""
        self.default_v_group_mapping = {
            "basic_five_pattern": "action",
            "passive_voice": "action", 
            "tell": "tell",
            "make": "make",
            "know": "know"
        }
        
        # スロット表示順序のデフォルト設定
        self.slot_order_mapping = {
            "M1": 1, "M2": 2, "M3": 3,
            "S": 4, "Aux": 5, "V": 6,
            "O1": 7, "O2": 8, "C1": 9, "C2": 10,
            "Adv": 11
        }
    
    def convert_to_ui_format(self, 
                           controller_result: Dict[str, Any], 
                           sentence_id: str = None,
                           syntax_id: str = "") -> List[Dict[str, Any]]:
        """
        CentralController出力をUI形式に変換
        
        Args:
            controller_result: CentralControllerの出力
            sentence_id: 例文ID (ex001など)
            syntax_id: 構文ID
            
        Returns:
            UI形式の配列
        """
        if not controller_result.get("success", False):
            return []
        
        ui_items = []
        
        # V_group_key推定
        v_group_key = self._estimate_v_group_key(controller_result)
        
        # 例文ID設定
        if sentence_id is None:
            sentence_id = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # main_slotsの処理
        main_slots = controller_result.get("main_slots", {})
        sub_slots = controller_result.get("sub_slots", {})
        ordered_slots = controller_result.get("ordered_slots", {})
        
        for slot, phrase in main_slots.items():
            if phrase:  # 空でない場合のみ処理
                # サブスロットの存在をチェック
                has_subslots = any(
                    sub_key.startswith(f"sub-{slot.lower()}") or 
                    sub_key.startswith(f"{slot.lower()}-")
                    for sub_key in sub_slots.keys()
                )
                
                ui_item = self._create_ui_item(
                    syntax_id=syntax_id,
                    v_group_key=v_group_key,
                    sentence_id=sentence_id,
                    slot=slot,
                    phrase=phrase,
                    ordered_slots=ordered_slots,
                    has_subslots=has_subslots
                )
                ui_items.append(ui_item)
        
        # display_orderでソート
        ui_items.sort(key=lambda x: x["Slot_display_order"])
        
        return ui_items
    
    def _estimate_v_group_key(self, controller_result: Dict[str, Any]) -> str:
        """文法パターンからV_group_keyを推定"""
        grammar_pattern = controller_result.get("grammar_pattern", "")
        
        # 動詞から推定（将来的に強化）
        verb = controller_result.get("main_slots", {}).get("V", "")
        if verb:
            verb_lower = verb.lower()
            if verb_lower in ["tell", "told"]:
                return "tell"
            elif verb_lower in ["make", "made"]:
                return "make"
            elif verb_lower in ["know", "knew", "known"]:
                return "know"
        
        # 文法パターンから推定
        for pattern, v_group in self.default_v_group_mapping.items():
            if pattern in grammar_pattern:
                return v_group
        
        return "action"  # デフォルト
    
    def _create_ui_item(self, 
                       syntax_id: str,
                       v_group_key: str,
                       sentence_id: str,
                       slot: str,
                       phrase: str,
                       ordered_slots: Dict[str, str],
                       has_subslots: bool = False) -> Dict[str, Any]:
        """UI形式のアイテムを作成"""
        
        # Slot_display_orderを決定（ordered_slotsを参考）
        slot_display_order = self._get_display_order(slot, phrase, ordered_slots)
        
        # PhraseTypeを推定（サブスロット情報を考慮）
        phrase_type = self._estimate_phrase_type(phrase, has_subslots)
        
        # SlotTextを推定（将来的に辞書ベースで強化）
        slot_text = self._estimate_slot_text(slot, phrase)
        
        return {
            "構文ID": syntax_id,
            "V_group_key": v_group_key,
            "例文ID": sentence_id,
            "Slot": slot,
            "SlotPhrase": phrase,
            "SlotText": slot_text,
            "PhraseType": phrase_type,
            "SubslotID": "",
            "SubslotElement": "",
            "SubslotText": "",
            "Slot_display_order": slot_display_order,
            "display_order": 0,
            "QuestionType": ""
        }
    
    def _get_display_order(self, slot: str, phrase: str, ordered_slots: Dict[str, str]) -> int:
        """表示順序を決定"""
        # ordered_slotsから順序を探す
        for order_num, order_phrase in ordered_slots.items():
            if order_phrase == phrase:
                return int(order_num)
        
        # フォールバック: デフォルト順序
        return self.slot_order_mapping.get(slot, 99)
    
    def _estimate_phrase_type(self, phrase: str, has_subslots: bool = False) -> str:
        """
        フレーズタイプを推定
        
        分類ルール:
        - word: サブスロットを持たない単純な要素（The car, is, red）
        - phrase: サブスロットを持つが、SがなくV以降のみ（to play tennis, talking of which）
        - clause: サブスロットを持ち、SVがある（関係節など）
        """
        if not phrase:
            return ""
        
        # サブスロットを持たない場合は word
        if not has_subslots:
            return "word"
        
        # サブスロットを持つ場合の詳細分析
        phrase_lower = phrase.lower()
        words = phrase_lower.split()
        
        # clause の特徴を検出
        # 関係代名詞・関係副詞でSV構造を持つもの
        relative_markers = ["who", "which", "that"]
        
        # clause判定: 関係代名詞/that + SV構造
        for marker in relative_markers:
            if marker in phrase_lower:
                # 関係代名詞の後にSV構造があるかチェック
                marker_index = phrase_lower.find(marker)
                after_marker = phrase_lower[marker_index + len(marker):].strip()
                if self._has_sv_structure(after_marker):
                    return "clause"
        
        # その他の接続詞でSV構造を持つもの
        conjunctions = ["because", "since", "although", "while", "if", "unless", "before", "after"]
        for conj in conjunctions:
            if conj in phrase_lower and self._has_sv_structure(phrase_lower):
                return "clause"
        
        # SVパターンが検出されない場合は phrase
        return "phrase"
    
    def _has_sv_structure(self, text: str) -> bool:
        """簡易的なSV構造検出"""
        if not text:
            return False
            
        words = text.split()
        if len(words) < 2:
            return False
        
        # 動詞リストを拡張
        verb_indicators = [
            "is", "are", "was", "were", "am", "be", "been", "being",  # be動詞
            "have", "has", "had", "having",  # have動詞
            "do", "does", "did", "doing",   # do動詞
            "will", "would", "can", "could", "should", "must", "may", "might",  # 助動詞
            "seem", "seemed", "look", "looked", "feel", "felt",  # 感覚動詞
            "tell", "told", "make", "made", "go", "went", "come", "came",  # 一般動詞
            "get", "got", "take", "took", "give", "gave", "see", "saw"
        ]
        
        # より柔軟な主語候補
        subject_indicators = [
            "i", "you", "he", "she", "it", "we", "they",  # 代名詞
            "this", "that", "these", "those",  # 指示代名詞
            "who", "which", "what"  # 疑問代名詞（関係代名詞後に来ることがある）
        ]
        
        # 主語候補＋動詞パターンの検出
        for i in range(len(words) - 1):
            current_word = words[i].lower()
            next_word = words[i + 1].lower()
            
            # 代名詞＋動詞
            if current_word in subject_indicators and next_word in verb_indicators:
                return True
            
            # 冠詞＋名詞の場合、その後の動詞をチェック
            if current_word in ["the", "a", "an"] and i + 2 < len(words):
                third_word = words[i + 2].lower()
                if third_word in verb_indicators:
                    return True
        
        # 動詞が存在するかの単純チェック
        for word in words:
            if word.lower() in verb_indicators:
                return True
        
        return False
    
    def _estimate_slot_text(self, slot: str, phrase: str) -> str:
        """SlotTextを推定（将来的に辞書で強化）"""
        # 基本的なマッピング
        basic_mapping = {
            "S": "",
            "V": "",
            "O1": "",
            "O2": "",
            "C1": "",
            "C2": "",
            "Aux": "",
            "M1": "",
            "M2": "",
            "M3": "",
            "Adv": ""
        }
        
        return basic_mapping.get(slot, "")
    
    def save_ui_format(self, ui_items: List[Dict[str, Any]], output_file: str):
        """UI形式をファイルに保存"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ui_items, f, ensure_ascii=False, indent=2)
        print(f"📁 UI形式を保存: {output_file}")
    
    def convert_and_save(self, 
                        controller_result: Dict[str, Any], 
                        output_file: str,
                        sentence_id: str = None,
                        syntax_id: str = "") -> List[Dict[str, Any]]:
        """変換して保存（ワンライナー）"""
        ui_items = self.convert_to_ui_format(controller_result, sentence_id, syntax_id)
        self.save_ui_format(ui_items, output_file)
        return ui_items


# 使用例・テスト用関数
def demo_conversion():
    """変換デモ"""
    from central_controller import CentralController
    
    # CentralControllerで処理
    controller = CentralController()
    result = controller.process_sentence("The car is red.")
    
    # UI形式に変換
    converter = UIFormatConverter()
    ui_items = converter.convert_to_ui_format(result, sentence_id="ex_demo")
    
    print("🔄 変換結果:")
    print(json.dumps(ui_items, ensure_ascii=False, indent=2))
    
    # ファイル保存
    converter.save_ui_format(ui_items, "demo_ui_format.json")
    
    return ui_items


if __name__ == "__main__":
    demo_conversion()
