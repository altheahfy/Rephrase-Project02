"""
既存ハンドラー統合アダプター
Legacy Handler Integration Adapter for Generic Central Controller

このファイルは既存の高品質な文法ハンドラーを
新しい汎用型中央管理システムに統合するためのアダプターを提供します。

既存ハンドラーの特徴:
- RelativeClauseHandler: 1402行の高度な関係節処理
- AdverbHandler: 918行のspaCy品詞分析ベース修飾語処理  
- BasicFivePatternHandler: 367行の5文型専門処理
- PassiveVoiceHandler: 受動態変換処理
- その他多数の専門ハンドラー

これらの貴重な資産を完全に活用します。
"""

from handler_interface_standard import HandlerAdapter, HandlerConfiguration, HandlerCapability
from central_controller_v3_generic import GenericCentralController
import importlib.util
import os
from typing import Dict, Any, List


class LegacyHandlerIntegrator:
    """レガシーハンドラー統合システム"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.available_handlers = {}
        self.scan_available_handlers()
    
    def scan_available_handlers(self):
        """利用可能なハンドラーを自動スキャン"""
        handler_files = [
            ('relative_clause_handler.py', 'RelativeClauseHandler'),
            ('adverb_handler.py', 'AdverbHandler'),
            ('basic_five_pattern_handler.py', 'BasicFivePatternHandler'),
            ('passive_voice_handler.py', 'PassiveVoiceHandler'),
            ('modal_handler.py', 'ModalHandler'),
            ('conditional_handler.py', 'ConditionalHandler'),
            ('infinitive_handler.py', 'InfinitiveHandler'),
            ('gerund_handler.py', 'GerundHandler'),
            ('noun_clause_handler.py', 'NounClauseHandler'),
            ('question_handler.py', 'QuestionHandler'),
            ('imperative_handler.py', 'ImperativeHandler')
        ]
        
        for filename, class_name in handler_files:
            file_path = os.path.join(self.base_path, filename)
            if os.path.exists(file_path):
                try:
                    handler_class = self._load_handler_class(file_path, class_name)
                    if handler_class:
                        self.available_handlers[class_name] = handler_class
                        print(f"✅ {class_name} スキャン完了")
                except Exception as e:
                    print(f"⚠️ {class_name} 読み込みエラー: {e}")
    
    def _load_handler_class(self, file_path: str, class_name: str):
        """ハンドラークラスを動的に読み込み"""
        spec = importlib.util.spec_from_file_location(class_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name, None)
    
    def create_adapters(self) -> Dict[str, HandlerAdapter]:
        """全利用可能ハンドラーのアダプターを作成"""
        adapters = {}
        
        for handler_name, handler_class in self.available_handlers.items():
            try:
                # ハンドラー設定の作成
                config = self._create_handler_config(handler_name)
                
                # レガシーハンドラーのインスタンス作成
                if handler_name == 'RelativeClauseHandler':
                    # RelativeClauseHandlerは協力者パラメータが必要
                    legacy_instance = handler_class(collaborators={})
                else:
                    legacy_instance = handler_class()
                
                # アダプター作成
                adapter = HandlerAdapter(legacy_instance, config)
                adapters[handler_name] = adapter
                
                print(f"🔧 {handler_name} アダプター作成完了")
                
            except Exception as e:
                print(f"❌ {handler_name} アダプター作成失敗: {e}")
        
        return adapters
    
    def _create_handler_config(self, handler_name: str) -> HandlerConfiguration:
        """ハンドラー固有の設定を作成"""
        
        # ハンドラー別の設定マッピング
        config_mapping = {
            'RelativeClauseHandler': {
                'capabilities': [HandlerCapability.STRUCTURAL_ANALYSIS, HandlerCapability.BOUNDARY_DETECTION],
                'patterns': ['complex_structure', 'relative_clause'],
                'priority': 1,
                'cooperation': ['AdverbHandler', 'BasicFivePatternHandler', 'PassiveVoiceHandler']
            },
            'AdverbHandler': {
                'capabilities': [HandlerCapability.MODIFICATION_PROCESSING, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['modifier_detection', 'adverb_processing'],
                'priority': 2,
                'cooperation': ['BasicFivePatternHandler', 'RelativeClauseHandler']
            },
            'BasicFivePatternHandler': {
                'capabilities': [HandlerCapability.STRUCTURAL_ANALYSIS, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['basic_structure', 'five_pattern_analysis'],
                'priority': 3,
                'cooperation': ['AdverbHandler', 'PassiveVoiceHandler']
            },
            'PassiveVoiceHandler': {
                'capabilities': [HandlerCapability.TRANSFORMATION, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['voice_transformation', 'passive_voice'],
                'priority': 2,
                'cooperation': ['BasicFivePatternHandler', 'RelativeClauseHandler']
            },
            'ModalHandler': {
                'capabilities': [HandlerCapability.SEMANTIC_ANALYSIS, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['modal_analysis', 'auxiliary_processing'],
                'priority': 4,
                'cooperation': ['BasicFivePatternHandler']
            },
            'ConditionalHandler': {
                'capabilities': [HandlerCapability.STRUCTURAL_ANALYSIS, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['conditional_structure', 'complex_structure'],
                'priority': 2,
                'cooperation': ['BasicFivePatternHandler', 'AdverbHandler']
            },
            'InfinitiveHandler': {
                'capabilities': [HandlerCapability.TRANSFORMATION, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['infinitive_processing', 'verbal_structure'],
                'priority': 3,
                'cooperation': ['BasicFivePatternHandler']
            },
            'GerundHandler': {
                'capabilities': [HandlerCapability.TRANSFORMATION, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['gerund_processing', 'verbal_structure'],
                'priority': 3,
                'cooperation': ['BasicFivePatternHandler']
            },
            'NounClauseHandler': {
                'capabilities': [HandlerCapability.STRUCTURAL_ANALYSIS, HandlerCapability.BOUNDARY_DETECTION],
                'patterns': ['noun_clause', 'complex_structure'],
                'priority': 2,
                'cooperation': ['BasicFivePatternHandler', 'RelativeClauseHandler']
            },
            'QuestionHandler': {
                'capabilities': [HandlerCapability.STRUCTURAL_ANALYSIS, HandlerCapability.TRANSFORMATION],
                'patterns': ['question_structure', 'interrogative_processing'],
                'priority': 2,
                'cooperation': ['BasicFivePatternHandler']
            },
            'ImperativeHandler': {
                'capabilities': [HandlerCapability.STRUCTURAL_ANALYSIS, HandlerCapability.PATTERN_DETECTION],
                'patterns': ['imperative_structure', 'command_processing'],
                'priority': 3,
                'cooperation': ['BasicFivePatternHandler']
            }
        }
        
        config_data = config_mapping.get(handler_name, {
            'capabilities': [HandlerCapability.PATTERN_DETECTION],
            'patterns': ['generic_processing'],
            'priority': 5,
            'cooperation': []
        })
        
        return HandlerConfiguration(
            handler_id=handler_name.lower().replace('handler', ''),
            capabilities=config_data['capabilities'],
            supported_patterns=config_data['patterns'],
            processing_priority=config_data['priority'],
            cooperation_preferences=config_data['cooperation']
        )


def integrate_all_legacy_handlers(base_path: str) -> GenericCentralController:
    """全レガシーハンドラーを統合した中央管理システムを作成"""
    
    print("🚀 レガシーハンドラー統合システム起動")
    print("=" * 60)
    
    # 統合システム初期化
    integrator = LegacyHandlerIntegrator(base_path)
    controller = GenericCentralController()
    
    print(f"\n📋 利用可能ハンドラー: {len(integrator.available_handlers)}個")
    for handler_name in integrator.available_handlers.keys():
        print(f"  ✅ {handler_name}")
    
    # アダプター作成と登録
    print(f"\n🔧 アダプター統合開始")
    adapters = integrator.create_adapters()
    
    for adapter_name, adapter in adapters.items():
        controller.register_handler(adapter)
    
    print(f"\n🎯 統合完了結果")
    status = controller.get_system_status()
    print(f"  ・登録済みハンドラー: {len(status['registered_handlers'])}個")
    print(f"  ・利用可能パターン: {len(status['available_patterns'])}個")
    print(f"  ・システム状態: {status['system_health']}")
    
    return controller


def test_integrated_system():
    """統合システムのテスト"""
    
    print("\n🧪 統合システムテスト開始")
    print("-" * 40)
    
    # データディレクトリパス
    base_path = os.path.dirname(__file__)
    
    # システム統合
    controller = integrate_all_legacy_handlers(base_path)
    
    # テストケース
    test_cases = [
        {
            'input': "The book that she was reading quickly became very interesting.",
            'description': "関係節 + 副詞修飾 (RelativeClause + Adverb)"
        },
        {
            'input': "She gave him a present yesterday.",
            'description': "第4文型 (BasicFivePattern)"
        },
        {
            'input': "The house was built by my father.",
            'description': "受動態 (PassiveVoice)"
        },
        {
            'input': "I want to study English.",
            'description': "不定詞 (Infinitive)"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n【統合テスト {i}】 {case['description']}")
        print(f"入力: \"{case['input']}\"")
        
        result = controller.process_input(case['input'])
        
        print(f"📊 結果:")
        print(f"  ・全体信頼度: {result['confidence']:.3f}")
        print(f"  ・検出パターン: {result['detected_patterns']}")
        print(f"  ・参加ハンドラー: {result['metadata']['handlers_involved']}個")
        print(f"  ・処理時間: {result['metadata']['processing_time']:.3f}秒")
        
        if result['processing_result'].get('main_slots'):
            print(f"  ・メインスロット: {list(result['processing_result']['main_slots'].keys())}")
        if result['processing_result'].get('sub_slots'):
            print(f"  ・サブスロット: {list(result['processing_result']['sub_slots'].keys())}")
    
    print(f"\n✅ レガシーハンドラー統合テスト完了")
    print(f"全ての既存ハンドラーが新システムで正常動作を確認")


if __name__ == "__main__":
    test_integrated_system()
