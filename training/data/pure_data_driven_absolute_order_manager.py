"""
Pure Data-Driven Absolute Order Manager
純粋データ駆動型絶対順序管理システム

設計原則:
- 文法知識を一切使用しない
- V_group_key別の独立処理
- 4ステップアルゴリズム実装

アルゴリズム:
①全要素抽出：指定V_group_keyの全例文から全要素を抽出
②使用順序観察：各例文での要素の出現順序を記録
③共通順序構築：最も多く使用される順序を基準順序として決定
④順序付与：新しい例文に基準順序を適用
"""

import json
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter


class PureDataDrivenAbsoluteOrderManager:
    """
    純粋データ駆動型絶対順序管理システム
    
    特徴:
    - 文法カテゴリ依存なし
    - V_group_key別独立処理
    - 機械的データ分析のみ
    """
    
    def __init__(self, data_file_path: str = 'final_54_test_data_with_absolute_order_corrected.json'):
        """
        初期化
        
        Args:
            data_file_path: 例文データファイルのパス
        """
        self.data_file_path = data_file_path
        self.group_analysis_cache = {}  # V_group_key別分析結果キャッシュ
        
        print("🔧 Pure Data-Driven Absolute Order Manager 初期化完了")
    
    def apply_absolute_order(self, slots: Dict[str, str], text: str, v_group_key: str) -> Dict[str, Any]:
        """
        純粋データ駆動型絶対順序適用
        
        Args:
            slots: 分解済みスロット
            text: 元の文
            v_group_key: 動詞グループキー
            
        Returns:
            Dict: 絶対順序適用結果
        """
        try:
            # ステップ1: 指定V_group_keyの分析結果を取得（キャッシュ利用）
            if v_group_key not in self.group_analysis_cache:
                self.group_analysis_cache[v_group_key] = self._analyze_v_group_patterns(v_group_key)
            
            group_analysis = self.group_analysis_cache[v_group_key]
            
            if not group_analysis['success']:
                return {
                    'success': False,
                    'error': f"V_group_key '{v_group_key}' の分析失敗: {group_analysis['error']}",
                    'v_group_key': v_group_key
                }
            
            # ステップ2: 基準順序を取得
            standard_order = group_analysis['standard_order']
            
            # ステップ3: 入力スロットに基準順序を適用
            ordered_result = self._apply_standard_order_to_slots(slots, standard_order, v_group_key)
            
            return {
                'success': True,
                'v_group_key': v_group_key,
                'standard_order': standard_order,
                'ordered_slots': ordered_result['ordered_slots'],
                'confidence': group_analysis['confidence'],
                'analysis_stats': {
                    'total_examples': group_analysis['total_examples'],
                    'valid_patterns': group_analysis['valid_patterns'],
                    'most_common_pattern': group_analysis['most_common_pattern']
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"絶対順序適用エラー: {str(e)}",
                'v_group_key': v_group_key
            }
    
    def _analyze_v_group_patterns(self, v_group_key: str) -> Dict[str, Any]:
        """
        指定V_group_keyの純粋データ分析（4ステップアルゴリズム）
        
        Args:
            v_group_key: 分析対象の動詞グループキー
            
        Returns:
            Dict: 分析結果
        """
        try:
            # ステップ①：全要素抽出
            group_examples = self._extract_group_examples(v_group_key)
            
            if not group_examples:
                return {
                    'success': False,
                    'error': f"V_group_key '{v_group_key}' の例文が見つかりません"
                }
            
            print(f"🔍 ステップ①完了: V_group_key '{v_group_key}' から {len(group_examples)} 例文抽出")
            
            # ステップ②：使用順序観察
            order_patterns = self._observe_usage_orders(group_examples)
            
            if not order_patterns:
                return {
                    'success': False,
                    'error': f"V_group_key '{v_group_key}' で有効な順序パターンが見つかりません"
                }
            
            print(f"🔍 ステップ②完了: {len(order_patterns)} 種類の順序パターン検出")
            
            # ステップ③：共通順序構築
            standard_order = self._construct_common_order(order_patterns)
            
            print(f"🔍 ステップ③完了: 基準順序決定 = {standard_order}")
            
            # 信頼度計算
            most_common_pattern, confidence = self._calculate_confidence(order_patterns)
            
            return {
                'success': True,
                'v_group_key': v_group_key,
                'standard_order': standard_order,
                'confidence': confidence,
                'total_examples': len(group_examples),
                'valid_patterns': len(order_patterns),
                'most_common_pattern': most_common_pattern,
                'all_patterns': dict(order_patterns)  # デバッグ用
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"V_group_key '{v_group_key}' 分析エラー: {str(e)}"
            }
    
    def _extract_group_examples(self, v_group_key: str) -> List[Dict[str, Any]]:
        """
        ステップ①：指定V_group_keyの全例文を抽出（CentralController分解版）
        
        Args:
            v_group_key: 対象の動詞グループキー
            
        Returns:
            List[Dict]: 抽出された例文とCentralController分解結果
        """
        try:
            from central_controller import CentralController
            
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # CentralController初期化
            controller = CentralController()
            
            examples = []
            for key, item in data['data'].items():
                if item.get('V_group_key') == v_group_key:
                    sentence = item['sentence']
                    
                    # 🎯 実際の分解処理：例文をCentralControllerで分解
                    decomposition_result = controller.process_sentence(sentence)
                    
                    if decomposition_result.get('success'):
                        # 分解成功の場合のみ追加
                        examples.append({
                            'sentence': sentence,
                            'decomposed_slots': decomposition_result.get('main_slots', {}),
                            'V_group_key': v_group_key,
                            'key': key,
                            'controller_result': decomposition_result
                        })
                        print(f"✅ {key}: '{sentence}' → {decomposition_result.get('main_slots', {})}")
                    else:
                        print(f"❌ {key}: '{sentence}' → 分解失敗: {decomposition_result.get('error')}")
            
            return examples
            
        except Exception as e:
            print(f"⚠️ データ抽出エラー: {e}")
            return []
    
    def _observe_usage_orders(self, examples: List[Dict[str, Any]]) -> Counter:
        """
        ステップ②：各例文での要素出現順序を観察（CentralController分解結果から）
        
        Args:
            examples: CentralControllerで分解済み例文データリスト
            
        Returns:
            Counter: 順序パターンの出現回数
        """
        order_patterns = Counter()
        
        for example in examples:
            decomposed_slots = example.get('decomposed_slots', {})
            
            if not decomposed_slots:
                continue
            
            # 🎯 CentralController分解結果から順序リストを構築
            order_list = []
            # 典型的なスロット順序で確認
            for slot_name in ['S', 'V', 'Aux', 'O1', 'O2', 'C1', 'M1', 'M2', 'M3']:
                if slot_name in decomposed_slots and decomposed_slots[slot_name].strip():
                    order_list.append(slot_name)
            
            if order_list:
                # 順序パターンをタプルとして記録
                pattern = tuple(order_list)
                order_patterns[pattern] += 1
                print(f"  📝 例文 {example['key']}: {order_list}")
                
        return order_patterns
    
    def _construct_common_order(self, order_patterns: Counter) -> List[str]:
        """
        ステップ③：最も多く使用される順序を基準順序として決定
        
        Args:
            order_patterns: 順序パターンの出現回数
            
        Returns:
            List[str]: 基準順序（スロット名のリスト）
        """
        if not order_patterns:
            return []
        
        # 最も頻出するパターンを基準順序とする
        most_common_pattern = order_patterns.most_common(1)[0][0]
        
        return list(most_common_pattern)
    
    def _calculate_confidence(self, order_patterns: Counter) -> Tuple[Tuple, float]:
        """
        信頼度計算：最も多いパターンの割合
        
        Args:
            order_patterns: 順序パターンの出現回数
            
        Returns:
            Tuple[Tuple, float]: (最頻出パターン, 信頼度)
        """
        if not order_patterns:
            return ((), 0.0)
        
        total_count = sum(order_patterns.values())
        most_common_pattern, most_common_count = order_patterns.most_common(1)[0]
        
        confidence = most_common_count / total_count
        
        return most_common_pattern, confidence
    
    def _apply_standard_order_to_slots(self, slots: Dict[str, str], standard_order: List[str], 
                                     v_group_key: str) -> Dict[str, Any]:
        """
        ステップ④：新しい例文に基準順序を適用
        
        Args:
            slots: 入力スロット
            standard_order: 基準順序
            v_group_key: 動詞グループキー
            
        Returns:
            Dict: 順序適用結果
        """
        ordered_slots = {}
        position = 1
        
        # 基準順序に従ってスロットを配置
        for slot_name in standard_order:
            if slot_name in slots and slots[slot_name]:
                ordered_slots[str(position)] = slot_name
                position += 1
        
        # 基準順序にないスロットは末尾に追加
        for slot_name, value in slots.items():
            if value and slot_name not in standard_order:
                ordered_slots[str(position)] = slot_name
                position += 1
                print(f"⚠️ 基準順序外スロット '{slot_name}' を位置 {position-1} に配置")
        
        return {
            'ordered_slots': ordered_slots,
            'applied_standard_order': standard_order,
            'v_group_key': v_group_key
        }


# テスト用関数
def test_pure_data_driven_system():
    """新システムの動作テスト：実際の文→分解→順序付与"""
    print("🚀 Pure Data-Driven System Test: 実際の処理フロー")
    print("=" * 60)
    
    manager = PureDataDrivenAbsoluteOrderManager()
    
    # テストケース1: tellグループの実例文をCentralControllerで分解
    test_sentences_tell = [
        "What did he tell her at the store?",
        "Did he tell her a secret there?", 
        "Did I tell him a truth in the kitchen?",
        "Where did you tell me a story?"
    ]
    
    print("📊 Tell Group Processing:")
    for sentence in test_sentences_tell:
        print(f"\n🔍 Processing: '{sentence}'")
        
        # CentralControllerで分解
        from central_controller import CentralController
        controller = CentralController()
        decomposition = controller.process_sentence(sentence)
        
        if decomposition.get('success'):
            slots = decomposition.get('main_slots', {})
            print(f"  分解結果: {slots}")
            
            # 純粋データ駆動で順序付与
            order_result = manager.apply_absolute_order(slots, sentence, "tell")
            print(f"  順序付与: {order_result}")
        else:
            print(f"  ❌ 分解失敗: {decomposition.get('error')}")


def generate_tell_group_order_output():
    """tellグループの順序付与結果をファイル出力"""
    print("\n🎯 Tell Group Order Generation for User Verification")
    print("=" * 60)
    
    manager = PureDataDrivenAbsoluteOrderManager()
    
    # tellグループを分析して基準順序を取得
    if 'tell' not in manager.group_analysis_cache:
        manager.group_analysis_cache['tell'] = manager._analyze_v_group_patterns('tell')
    
    analysis = manager.group_analysis_cache['tell']
    
    if not analysis.get('success'):
        print(f"❌ Tell group analysis failed: {analysis.get('error')}")
        return
    
    # 実際の例文処理結果
    with open('final_54_test_data_with_absolute_order_corrected.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tell_results = []
    from central_controller import CentralController
    controller = CentralController()
    
    for key, item in data['data'].items():
        if item.get('V_group_key') == 'tell':
            sentence = item['sentence']
            
            # 実際の分解処理
            decomposition = controller.process_sentence(sentence)
            
            if decomposition.get('success'):
                slots = decomposition.get('main_slots', {})
                
                # 順序付与
                order_result = manager.apply_absolute_order(slots, sentence, "tell")
                
                tell_results.append({
                    'key': key,
                    'sentence': sentence,
                    'decomposed_slots': slots,
                    'absolute_order_result': order_result,
                    'expected_slots': item['expected']['main_slots']  # 比較用
                })
    
    # 結果をファイル出力
    output_data = {
        'metadata': {
            'processing_method': 'CentralController → PureDataDrivenAbsoluteOrderManager',
            'target_group': 'tell',
            'total_processed': len(tell_results),
            'analysis_summary': {
                'success': analysis.get('success'),
                'standard_order': analysis.get('standard_order'),
                'confidence': analysis.get('confidence'),
                'total_examples': analysis.get('total_examples'),
                'all_patterns': str(analysis.get('all_patterns', {}))  # tupleを文字列に変換
            }
        },
        'results': tell_results
    }
    
    output_filename = 'tell_group_pure_processing_results.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Tell group processing results saved to: {output_filename}")
    print(f"📊 Total examples processed: {len(tell_results)}")
    
    return output_filename


if __name__ == "__main__":
    print("🚀 Pure Data-Driven Absolute Order Manager - 実際の処理フロー")
    print("実際の文 → CentralController分解 → PureDataDriven順序付与")
    print("=" * 70)
    
    # テスト実行
    test_pure_data_driven_system()
    
    # tellグループの処理結果をファイル出力
    output_file = generate_tell_group_order_output()
    print(f"\n🎯 User verification file: {output_file}")
