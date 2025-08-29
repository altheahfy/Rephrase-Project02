"""
AbsoluteOrderManager - 絶対順序管理システム

グループベースの固定列マッピングシステム
- 各グループごとに固定列構成を定義
- 語順に依存しない一意の配置
- tellグループ、基本副詞グループ等に対応
"""

from typing import Dict, List, Any, Tuple


class AbsoluteOrderManager:
    """
    絶対順序管理システム - グループごとの固定列マッピング
    
    責任:
    - グループの特定と固定列構成の提供
    - スロットの絶対位置への変換
    - 文法項目の一意配置保証
    """
    
    def __init__(self):
        """初期化: グループ別固定列マッピングの定義"""
        
        # tellグループ: 8列固定構成
        self.tell_group_mapping = {
            "M2_wh": 1,      # wh疑問詞（時間・場所）
            "O2_wh": 2,      # wh疑問詞（第二目的語）
            "Aux": 3,        # 助動詞
            "S": 4,          # 主語
            "V": 5,          # 動詞
            "O1": 6,         # 第一目的語
            "O2_normal": 7,  # 通常の第二目的語
            "M2_normal": 8   # 通常の修飾語
        }
        
        # 基本副詞グループ: 7列固定構成
        self.basic_adverbs_mapping = {
            "S": 1,          # 主語
            "Aux": 2,        # 助動詞
            "V": 3,          # 動詞
            "O1": 4,         # 第一目的語
            "M1": 5,         # 副詞・方法
            "M2": 6,         # 副詞・時間場所
            "M3": 7          # 副詞・追加修飾
        }
        
        # gaveグループ: 4列固定構成
        self.gave_group_mapping = {
            "S": 1,          # 主語
            "V": 2,          # 動詞
            "O1": 3,         # 第一目的語
            "O2": 4          # 第二目的語
        }
        
        # グループ判定パターン
        self.group_patterns = {
            'tell_group': {
                'required_verbs': ['tell'],
                'required_slots': ['S', 'V'],
                'wh_support': True
            },
            'basic_adverbs': {
                'required_slots': ['S', 'V'],
                'modifier_required': True,
                'wh_support': False
            },
            'gave_group': {
                'required_verbs': ['give', 'gave'],
                'required_slots': ['S', 'V', 'O1', 'O2'],
                'wh_support': False
            }
        }
    
    def identify_group(self, slots: Dict[str, str], text: str = "") -> str:
        """
        スロット構成とテキストからグループを特定
        
        Args:
            slots: 分析されたスロット辞書
            text: 元の文章（動詞特定用）
        
        Returns:
            str: 特定されたグループ名
        """
        
        # tellグループ判定
        if 'V' in slots and 'tell' in slots['V'].lower():
            # tellが含まれている場合
            if any(key.endswith('_wh') for key in slots.keys()) or 'what' in text.lower() or 'where' in text.lower():
                return 'tell_group'
            if 'O1' in slots and 'O2' in slots:
                return 'tell_group'
        
        # gaveグループ判定
        if 'V' in slots and any(verb in slots['V'].lower() for verb in ['give', 'gave']):
            if 'O1' in slots and 'O2' in slots:
                return 'gave_group'
        
        # 基本副詞グループ判定（デフォルト）
        if 'S' in slots and 'V' in slots:
            modifier_count = sum(1 for key in slots.keys() if key.startswith('M'))
            if modifier_count > 0:
                return 'basic_adverbs'
        
        return 'basic_adverbs'  # デフォルト
    
    def apply_absolute_order(self, slots: Dict[str, str], text: str = "") -> Dict[str, Any]:
        """
        スロットに絶対順序を適用
        
        Args:
            slots: 分析されたスロット辞書
            text: 元の文章
        
        Returns:
            Dict: 絶対順序が適用された結果
        """
        
        # グループ特定
        group_name = self.identify_group(slots, text)
        
        # グループ別マッピング取得
        if group_name == 'tell_group':
            mapping = self.tell_group_mapping
            columns = 8
        elif group_name == 'basic_adverbs':
            mapping = self.basic_adverbs_mapping
            columns = 7
        elif group_name == 'gave_group':
            mapping = self.gave_group_mapping
            columns = 4
        else:
            # デフォルト（基本副詞グループ）
            mapping = self.basic_adverbs_mapping
            columns = 7
            group_name = 'basic_adverbs'
        
        # 位置ベースの要素分類（tellグループ専用）
        if group_name == 'tell_group':
            classified_slots = self._classify_tell_group_elements(slots, text)
        else:
            classified_slots = slots
        
        # 絶対順序配置
        absolute_order = {}
        for slot_key, slot_value in classified_slots.items():
            if slot_key in mapping:
                position = mapping[slot_key]
                absolute_order[position] = {
                    'slot': slot_key,
                    'value': slot_value
                }
        
        return {
            'group': group_name,
            'columns': columns,
            'absolute_order': absolute_order,
            'mapping': mapping,
            'original_slots': slots
        }
    
    def _classify_tell_group_elements(self, slots: Dict[str, str], text: str) -> Dict[str, str]:
        """
        tellグループの要素を位置ベースで分類（wh位置 vs 通常位置）
        
        Args:
            slots: 原始スロット辞書
            text: 元の文章
        
        Returns:
            Dict: 分類されたスロット辞書
        """
        classified = {}
        wh_words = ['what', 'where', 'when', 'why', 'how', 'who', 'which']
        
        for slot_key, slot_value in slots.items():
            # WH語の判定
            is_wh_word = any(wh in slot_value.lower() for wh in wh_words)
            
            if slot_key == 'O2' and is_wh_word:
                classified['O2_wh'] = slot_value
            elif slot_key == 'O2' and not is_wh_word:
                classified['O2_normal'] = slot_value
            elif slot_key == 'M2' and is_wh_word:
                classified['M2_wh'] = slot_value
            elif slot_key == 'M2' and not is_wh_word:
                classified['M2_normal'] = slot_value
            else:
                classified[slot_key] = slot_value
        
        return classified
    
    def generate_table_display(self, result: Dict[str, Any]) -> str:
        """
        絶対順序結果をtellグループ形式の表で表示
        
        Args:
            result: apply_absolute_orderの結果
        
        Returns:
            str: 表形式の文字列
        """
        group = result['group']
        columns = result['columns']
        absolute_order = result['absolute_order']
        
        # ヘッダー生成
        header1 = "        "
        header2 = "group   "
        
        circle_nums = "①②③④⑤⑥⑦⑧⑨⑩"
        
        for i in range(1, columns + 1):
            header1 += f"{circle_nums[i-1]}      "
            
            # 列名を生成
            column_name = ""
            for slot_key, position in result['mapping'].items():
                if position == i:
                    column_name = f"{slot_key}-{i}"
                    break
            header2 += f"{column_name:<7}"
        
        # データ行生成
        data_row = f"{group:<8}"
        for i in range(1, columns + 1):
            if i in absolute_order:
                value = absolute_order[i]['value']
                display_value = value[:6] if len(value) > 6 else value
                data_row += f"{display_value:<7}"
            else:
                data_row += f"{'':7}"
        
        return f"{header1}\n{header2}\n{'-' * (columns * 7 + 8)}\n{data_row}"
