"""
DynamicAbsoluteOrderManager - 動的分析による絶対順序管理システム

グループの全例文を動的に分析し、語順に従って絶対順序を決定する
固定テンプレートではなく、実際の例文群から位置を導出
"""

from typing import Dict, List, Any, Tuple
import re


class DynamicAbsoluteOrderManager:
    """
    動的分析による絶対順序管理システム
    
    責任:
    - グループ内全例文の動的分析
    - 位置別要素の完全列挙
    - 語順に従った自動的な位置決定
    """
    
    def __init__(self):
        """初期化: 動的分析エンジンの準備"""
        self.group_mappings = {}  # キャッシュ用
        self.wh_words = ['what', 'where', 'when', 'why', 'how', 'who', 'which']
        
    def analyze_group_elements(self, v_group_key: str, example_sentences: List[str]) -> Dict[str, int]:
        """
        グループの全例文を分析して動的テンプレートを生成
        
        Args:
            v_group_key: 動詞グループキー (tell, gave等)
            example_sentences: グループに属する全例文
            
        Returns:
            Dict: 要素名→位置番号のマッピング
        """
        print(f"=== 動的分析開始: {v_group_key}グループ ===")
        
        # 各例文から要素順序を抽出
        sentence_orders = []
        for sentence in example_sentences:
            print(f"分析中: {sentence}")
            parsed_slots = self.parse_sentence_basic(sentence)
            positioned_elements = self.classify_by_position(parsed_slots, sentence)
            # 位置順にソートして要素順序を取得
            sorted_elements = sorted(positioned_elements, key=lambda x: x[1])
            element_order = [elem[0] for elem in sorted_elements]
            sentence_orders.append(element_order)
            print(f"  要素順序: {element_order}")
        
        # 例文間の相対位置関係を基に全体順序を決定
        global_order = self.merge_sentence_orders(sentence_orders)
        print(f"統合順序: {global_order}")
        
        # 絶対順序マッピングを作成（1始まり）
        absolute_order = {}
        for position, element_type in enumerate(global_order):
            absolute_order[element_type] = position + 1
        
        print(f"絶対順序マッピング: {absolute_order}")
        return absolute_order
    
    def parse_sentence_basic(self, sentence: str) -> Dict[str, str]:
        """
        基本的な文解析（簡易版）
        実際のCentralControllerの結果を使用することが望ましい
        """
        # この部分は実際にはCentralControllerの解析結果を使用すべき
        # ここでは簡易的な実装
        words = sentence.lower().split()
        slots = {}
        
        # 簡易パターンマッチング
        for i, word in enumerate(words):
            if word in self.wh_words:
                if word in ['where', 'when']:
                    slots['M2'] = word
                elif word in ['what', 'who']:
                    slots['O2'] = word
            elif word in ['did', 'do', 'does', 'will', 'can', 'should']:
                slots['Aux'] = word
            elif word in ['tell', 'told']:
                slots['V'] = 'tell'
            elif word in ['give', 'gave', 'given']:
                slots['V'] = 'gave'
            elif word in ['he', 'she', 'i', 'you', 'we', 'they'] or word.istitle():
                if 'S' not in slots:  # 最初の主語候補
                    slots['S'] = word
            elif word in ['me', 'him', 'her', 'us', 'them']:
                if 'O1' not in slots:
                    slots['O1'] = word
        
        # 時間副詞の検出
        time_words = ['yesterday', 'today', 'tomorrow', 'now', 'then']
        for word in words:
            if word.lower() in time_words:
                slots['M1'] = word
                break
                
        # 場所・その他の修飾語
        if 'at' in words or 'in' in words or 'there' in words:
            # 簡易的な修飾語抽出
            for i, word in enumerate(words):
                if word in ['at', 'in'] and i + 1 < len(words):
                    if 'M2' not in slots:  # wh語がない場合
                        slots['M2'] = ' '.join(words[i:i+3])  # at the store等
                    break
                elif word == 'there':
                    if 'M2' not in slots:
                        slots['M2'] = word
                    break
        
        # 目的語の検出（簡易版）
        articles = ['a', 'an', 'the']
        for i, word in enumerate(words):
            if word in articles and i + 1 < len(words):
                next_word = words[i + 1]
                if 'O2' not in slots and next_word not in ['store']:  # 場所ではない
                    slots['O2'] = ' '.join(words[i:i+2])  # a secret等
                    break
        
        return slots
    
    def classify_by_position(self, slots: Dict[str, str], sentence: str) -> List[Tuple[str, int]]:
        """
        要素を出現位置別に分類
        
        Args:
            slots: 解析されたスロット辞書
            sentence: 元の文章
            
        Returns:
            List: (要素タイプ, 文中位置)のリスト
        """
        elements = []
        words = sentence.split()
        
        for slot_key, slot_value in slots.items():
            # 文中での位置を特定
            position_in_sentence = self.find_word_position(slot_value, words)
            
            # 位置別分類
            if slot_key == "M2":
                if self.is_wh_word(slot_value):
                    element_type = "M2_wh"
                else:
                    element_type = "M2_normal"
            elif slot_key == "O2":
                if self.is_wh_word(slot_value):
                    element_type = "O2_wh"
                else:
                    element_type = "O2_normal"
            else:
                element_type = slot_key
                
            elements.append((element_type, position_in_sentence))
        
        return elements
    
    def find_word_position(self, slot_value: str, words: List[str]) -> int:
        """文中での単語の位置を特定"""
        slot_words = slot_value.lower().split()
        if not slot_words:
            return 999  # 見つからない場合は末尾扱い
            
        first_word = slot_words[0]
        for i, word in enumerate(words):
            if word.lower() == first_word:
                return i
        return 999
    
    def is_wh_word(self, value: str) -> bool:
        """wh語かどうかを判定"""
        return any(wh in value.lower() for wh in self.wh_words)
    
    def merge_sentence_orders(self, sentence_orders: List[List[str]]) -> List[str]:
        """
        複数例文の要素順序を統合して全体順序を決定
        
        例:
        文1: [a, b, c, d, e]
        文2: [b, c, e, f]  
        文3: [c, e, f, g]
        結果: [a, b, c, d, e, f, g]
        
        Args:
            sentence_orders: 各例文の要素順序リスト
            
        Returns:
            List: 統合された全体順序
        """
        from collections import defaultdict, deque
        
        print("=== 例文順序統合開始 ===")
        for i, order in enumerate(sentence_orders):
            print(f"文{i+1}: {order}")
        
        # 前後関係グラフを構築
        precedence = defaultdict(set)  # element -> {elements that come after}
        all_elements = set()
        
        for order in sentence_orders:
            all_elements.update(order)
            # 各文内での前後関係を記録
            for i in range(len(order)):
                for j in range(i + 1, len(order)):
                    precedence[order[i]].add(order[j])
        
        print(f"前後関係グラフ:")
        for element, followers in sorted(precedence.items()):
            if followers:
                print(f"  {element} → {sorted(list(followers))}")
        
        # トポロジカルソートで全体順序を決定
        in_degree = defaultdict(int)
        for element in all_elements:
            in_degree[element] = 0
        
        for element, followers in precedence.items():
            for follower in followers:
                in_degree[follower] += 1
        
        # 入次数0の要素から開始
        queue = deque(sorted([element for element in all_elements if in_degree[element] == 0]))
        result_order = []
        
        while queue:
            current = queue.popleft()
            result_order.append(current)
            
            # 後続要素の入次数を減少
            for follower in sorted(precedence[current]):  # 安定ソートのため
                in_degree[follower] -= 1
                if in_degree[follower] == 0:
                    queue.append(follower)
        
        print(f"統合結果: {result_order}")
        return result_order
    
    def merge_positional_elements(self, all_elements: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        位置別要素を統合し、全例文の相対位置関係を保持
        
        例:
        文1: a(0), b(1), c(2), d(3), e(4)
        文2: b(0), c(1), e(2), f(3)  
        文3: c(0), e(1), f(2), g(3)
        結果: a, b, c, d, e, f, g の順序
        
        Args:
            all_elements: 全例文から抽出された(要素タイプ, 位置)のリスト
            
        Returns:
            List: 相対位置関係を保持した要素リスト
        """
        from collections import defaultdict, deque
        
        print("=== 要素統合開始 ===")
        print(f"全要素: {all_elements}")
        
        # 実際のアプローチ：各要素タイプの最小位置を基準にソート
        # 複数例文の相対関係は、この段階では例文データが混在しているため
        # 単純に最小出現位置で並べる方式を採用
        element_positions = defaultdict(list)
        
        for element_type, position in all_elements:
            element_positions[element_type].append(position)
        
        # 各要素の最小位置で並べる
        unique_elements = []
        for element_type, positions in element_positions.items():
            min_position = min(positions)
            unique_elements.append((element_type, min_position))
            print(f"  {element_type}: 出現位置{positions} → 最小位置{min_position}")
        
        # 最小位置順でソート
        unique_elements.sort(key=lambda x: x[1])
        
        print(f"=== 統合された順序 ===")
        for i, (element_type, original_pos) in enumerate(unique_elements):
            print(f"  位置{i}: {element_type} (元位置{original_pos})")
        
        # 新しい連続位置を割り当てて返す
        return [(element_type, i) for i, (element_type, _) in enumerate(unique_elements)]
    
    def assign_absolute_positions(self, unique_elements: List[Tuple[str, int]]) -> Dict[str, int]:
        """
        語順による絶対位置の決定
        
        Args:
            unique_elements: 要素タイプと平均位置のリスト
            
        Returns:
            Dict: 要素タイプ→絶対位置のマッピング
        """
        # 文中位置でソート
        sorted_elements = sorted(unique_elements, key=lambda x: x[1])
        
        # 連続した位置番号を割り当て
        ordered_mapping = {}
        for i, (element_type, _) in enumerate(sorted_elements, 1):
            ordered_mapping[element_type] = i
        
        return ordered_mapping
    
    def apply_absolute_order(self, slots: Dict[str, str], text: str = "", v_group_key: str = "") -> Dict[str, Any]:
        """
        スロットに動的絶対順序を適用
        
        Args:
            slots: 分析されたスロット辞書
            text: 元の文章
            v_group_key: 動詞グループキー
            
        Returns:
            Dict: 絶対順序が適用された結果
        """
        # グループのマッピングが存在しない場合は、簡易的な固定マッピングを使用
        if v_group_key not in self.group_mappings:
            print(f"⚠️ {v_group_key}グループの動的マッピングが未定義。例文分析が必要です。")
            # 緊急時の簡易マッピング
            if 'tell' in v_group_key.lower() or any('tell' in str(v).lower() for v in slots.values()):
                mapping = self.get_emergency_tell_mapping()
            else:
                mapping = self.get_emergency_basic_mapping()
        else:
            mapping = self.group_mappings[v_group_key]
        
        # 要素分類
        classified_slots = self.classify_current_elements(slots, text)
        
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
            'group': v_group_key,
            'columns': len(mapping),
            'absolute_order': absolute_order,
            'mapping': mapping,
            'original_slots': slots
        }
    
    def classify_current_elements(self, slots: Dict[str, str], text: str) -> Dict[str, str]:
        """現在の要素を位置別に分類"""
        classified = {}
        
        for slot_key, slot_value in slots.items():
            if slot_key == 'O2' and self.is_wh_word(slot_value):
                classified['O2_wh'] = slot_value
            elif slot_key == 'O2' and not self.is_wh_word(slot_value):
                classified['O2_normal'] = slot_value
            elif slot_key == 'M2' and self.is_wh_word(slot_value):
                classified['M2_wh'] = slot_value
            elif slot_key == 'M2' and not self.is_wh_word(slot_value):
                classified['M2_normal'] = slot_value
            else:
                classified[slot_key] = slot_value
        
        return classified
    
    def get_emergency_tell_mapping(self) -> Dict[str, int]:
        """告示グループ用の緊急マッピング"""
        return {
            "M1": 1,           # Yesterday等
            "M2_wh": 2,        # Where等
            "O2_wh": 3,        # What等
            "Aux": 4,          # did等
            "S": 5,            # he/you等
            "V": 6,            # tell
            "O1": 7,           # her/me等
            "O2_normal": 8,    # a secret等
            "M2_normal": 9     # at the store等
        }
    
    def get_emergency_basic_mapping(self) -> Dict[str, int]:
        """基本グループ用の緊急マッピング"""
        return {
            "S": 1,      # 主語
            "V": 2,      # 動詞
            "O1": 3,     # 第一目的語
            "O2": 4      # 第二目的語
        }
    
    def register_group_mapping(self, v_group_key: str, mapping: Dict[str, int]):
        """グループマッピングを登録"""
        self.group_mappings[v_group_key] = mapping
        print(f"✅ {v_group_key}グループのマッピングを登録: {mapping}")


# 使用例とテスト
if __name__ == "__main__":
    manager = DynamicAbsoluteOrderManager()
    
    # tellグループの例文群
    tell_examples = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Where did you tell me a story?",
        "Yesterday what did he tell her?"
    ]
    
    # 動的分析実行
    tell_mapping = manager.analyze_group_elements("tell", tell_examples)
    manager.register_group_mapping("tell", tell_mapping)
    
    # テスト適用
    test_slots = {'M1': 'Yesterday', 'O2': 'what', 'Aux': 'did', 'S': 'he', 'V': 'tell', 'O1': 'her'}
    result = manager.apply_absolute_order(test_slots, "Yesterday what did he tell her?", "tell")
    
    print("\n=== テスト結果 ===")
    print(f"絶対順序: {result['absolute_order']}")
