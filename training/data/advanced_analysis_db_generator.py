# ===== 高度分析・DB生成統合テスト v1.0 =====
# 体系的テスト結果をExcel DB化する統合システム

import json
import pandas as pd
from systematic_grammar_test import SystematicGrammarTest
from simple_excel_generator_v3 import SimpleExcelGeneratorV3
from datetime import datetime

class AdvancedAnalysisDBGenerator:
    """高度分析・DB生成統合システム"""
    
    def __init__(self):
        self.grammar_tester = SystematicGrammarTest()
        self.excel_generator = SimpleExcelGeneratorV3()
        self.analysis_results = {}
        
        print("🚀 高度分析・DB生成統合システム初期化完了")
    
    def run_comprehensive_analysis(self):
        """包括的分析実行"""
        print("\n" + "="*80)
        print("🎯 高度分析・DB生成統合テスト開始")
        print("="*80)
        
        # Step 1: 体系的文法テスト実行
        print("\n📋 Step 1: 体系的文法パターンテスト")
        success_rate = self.grammar_tester.run_comprehensive_test()
        
        # Step 2: 成功例文のDB化
        print(f"\n📋 Step 2: 成功例文のDB生成 (成功率: {success_rate:.1f}%)")
        self.generate_successful_examples_db()
        
        # Step 3: 詳細品質分析
        print(f"\n📋 Step 3: 詳細品質分析")
        self.perform_detailed_quality_analysis()
        
        # Step 4: 改善提案生成
        print(f"\n📋 Step 4: 改善提案生成")
        self.generate_improvement_suggestions()
        
        return success_rate
    
    def generate_successful_examples_db(self):
        """成功例文をExcel DBに変換"""
        successful_tests = [t for t in self.grammar_tester.test_results if t['success']]
        
        print(f"📊 成功例文: {len(successful_tests)}件")
        
        # Excelジェネレータに例文を追加
        processed_count = 0
        
        for test_result in successful_tests:
            sentence = test_result['sentence']
            description = test_result['description']
            
            # V_group_key生成（動詞ベース）
            v_group_key = self.extract_verb_for_grouping(test_result)
            
            try:
                success = self.excel_generator.analyze_and_add_sentence(sentence, v_group_key)
                if success:
                    processed_count += 1
                    print(f"✅ DB追加: {sentence[:50]}... ({description})")
            except Exception as e:
                print(f"❌ DB追加エラー: {sentence[:50]}... - {e}")
        
        # Excel データ生成
        if processed_count > 0:
            self.excel_generator.generate_excel_data()
            
            # タイムスタンプ付きファイル名で保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"体系的テスト結果DB_{timestamp}.xlsx"
            self.excel_generator.save_to_excel(filename)
            
            print(f"🎉 Excel DB生成完了: {filename} ({processed_count}例文)")
        else:
            print("❌ DB生成対象例文がありません")
    
    def extract_verb_for_grouping(self, test_result):
        """テスト結果からV_group_key用の動詞を抽出"""
        main_slots = test_result.get('main_slots', {})
        
        # V スロットから動詞を抽出
        if 'V' in main_slots and main_slots['V']:
            return main_slots['V']
        
        # Aux スロットから助動詞を抽出
        if 'Aux' in main_slots and main_slots['Aux']:
            return main_slots['Aux']
        
        # 説明から動詞を推定
        description = test_result.get('description', '')
        if '使役' in description:
            return 'make_let_have'
        elif '仮定法' in description:
            return 'subjunctive'
        elif '完了' in description:
            return 'perfect'
        elif '受動態' in description:
            return 'passive'
        elif '関係節' in description:
            return 'relative'
        elif '副詞節' in description:
            return 'adverbial'
        
        return 'general'
    
    def perform_detailed_quality_analysis(self):
        """詳細品質分析"""
        print("🔍 詳細品質分析実行中...")
        
        successful_tests = [t for t in self.grammar_tester.test_results if t['success']]
        
        # カテゴリ別分析
        category_analysis = {}
        
        for test_result in successful_tests:
            description = test_result['description']
            category = self.categorize_test(description)
            
            if category not in category_analysis:
                category_analysis[category] = {
                    'count': 0,
                    'examples': [],
                    'slot_usage': {},
                    'complexity_scores': []
                }
            
            category_analysis[category]['count'] += 1
            category_analysis[category]['examples'].append(test_result['sentence'])
            
            # スロット使用状況分析
            main_slots = test_result.get('main_slots', {})
            for slot, value in main_slots.items():
                if value and value.strip():
                    if slot not in category_analysis[category]['slot_usage']:
                        category_analysis[category]['slot_usage'][slot] = 0
                    category_analysis[category]['slot_usage'][slot] += 1
            
            # 複雑度スコア計算
            complexity = self.calculate_complexity_score(test_result)
            category_analysis[category]['complexity_scores'].append(complexity)
        
        # 結果出力
        print("\n📊 カテゴリ別品質分析結果:")
        for category, analysis in category_analysis.items():
            avg_complexity = sum(analysis['complexity_scores']) / len(analysis['complexity_scores'])
            print(f"\n🎯 {category}:")
            print(f"  例文数: {analysis['count']}")
            print(f"  平均複雑度: {avg_complexity:.2f}")
            print(f"  主要スロット: {list(analysis['slot_usage'].keys())[:5]}")
            print(f"  例文例: {analysis['examples'][0] if analysis['examples'] else 'なし'}")
        
        self.analysis_results['category_analysis'] = category_analysis
    
    def categorize_test(self, description):
        """テスト説明からカテゴリを分類"""
        if '文型' in description or '存在' in description or '命令' in description or '疑問' in description or '感嘆' in description:
            return '基本文型'
        elif '仮定法' in description:
            return '仮定法'
        elif '完了' in description:
            return '完了時制'
        elif '受動態' in description:
            return '受動態'
        elif '関係' in description:
            return '関係節'
        elif '副詞節' in description or '時間' in description or '理由' in description:
            return '副詞節'
        elif '使役' in description:
            return '使役動詞'
        elif 'Cooperative' in description:
            return '複合構文'
        else:
            return 'その他'
    
    def calculate_complexity_score(self, test_result):
        """文の複雑度スコア計算"""
        sentence = test_result['sentence']
        main_slots = test_result.get('main_slots', {})
        sub_slots = test_result.get('sub_slots', {})
        
        score = 0
        
        # 文長ポイント
        score += len(sentence.split()) * 0.5
        
        # 使用スロット数ポイント
        occupied_main_slots = sum(1 for v in main_slots.values() if v and v.strip())
        score += occupied_main_slots * 2
        
        # サブスロットポイント
        if sub_slots:
            score += len(sub_slots) * 5
        
        # 特殊構文ポイント
        if 'who' in sentence or 'which' in sentence or 'that' in sentence:
            score += 10  # 関係詞
        if 'because' in sentence or 'although' in sentence or 'if' in sentence:
            score += 8   # 副詞節
        if 'make' in sentence or 'let' in sentence or 'have' in sentence:
            score += 6   # 使役動詞
        
        return min(score, 100)  # 最大100点
    
    def generate_improvement_suggestions(self):
        """改善提案生成"""
        print("💡 改善提案生成中...")
        
        suggestions = []
        
        # 失敗テスト分析（今回は0件だが、将来のため）
        failed_tests = [t for t in self.grammar_tester.test_results if not t['success']]
        
        if len(failed_tests) > 0:
            suggestions.append(f"❌ 失敗テスト {len(failed_tests)}件の詳細分析が必要")
        else:
            suggestions.append("✅ 全テストが成功！システムは高い完成度を維持")
        
        # カテゴリ別改善提案
        if 'category_analysis' in self.analysis_results:
            for category, analysis in self.analysis_results['category_analysis'].items():
                avg_complexity = sum(analysis['complexity_scores']) / len(analysis['complexity_scores'])
                
                if avg_complexity < 20:
                    suggestions.append(f"📈 {category}カテゴリ: より複雑な例文の追加を推奨")
                elif avg_complexity > 80:
                    suggestions.append(f"📉 {category}カテゴリ: 基本的な例文の追加でバランス改善")
                else:
                    suggestions.append(f"✅ {category}カテゴリ: 適切な複雑度バランス")
        
        # システム全体の提案
        successful_tests = [t for t in self.grammar_tester.test_results if t['success']]
        total_tests = len(successful_tests)
        
        suggestions.extend([
            f"📊 現在のテスト網羅性: {total_tests}パターン",
            "🎯 次期拡張候補: 慣用表現、倒置構文、省略構文",
            "🔧 性能最適化: 処理時間の更なる短縮",
            "📚 多様化: 実用的な日常会話例文の追加"
        ])
        
        print("\n💡 改善提案:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i:2d}. {suggestion}")
        
        # 提案をファイルに保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"改善提案_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🎯 Rephrase システム改善提案\n")
            f.write(f"生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            
            for i, suggestion in enumerate(suggestions, 1):
                f.write(f"{i:2d}. {suggestion}\n")
        
        print(f"📄 改善提案保存: {filename}")

def main():
    """メイン実行関数"""
    analyzer = AdvancedAnalysisDBGenerator()
    
    # 包括的分析実行
    success_rate = analyzer.run_comprehensive_analysis()
    
    print(f"\n🎯 最終評価:")
    print(f"成功率: {success_rate:.1f}%")
    
    if success_rate >= 95:
        print("🎉 優秀！システムは製品レベルの品質です")
    elif success_rate >= 90:
        print("✅ 良好！商用化に向けて準備が整っています")
    elif success_rate >= 80:
        print("⚠️ 改善余地あり！重要な問題の解決が必要")
    else:
        print("❌ 大幅改善必要！システムの根本的見直しが必要")
    
    return success_rate

if __name__ == "__main__":
    main()
