# ===== 体系的文法パターンテスト v1.0 =====
# 優先度最高：様々な文法パターンでの系統的検証

import os
import sys
from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

class SystematicGrammarTest:
    """体系的文法パターンテストシステム"""
    
    def __init__(self):
        self.integrator = SimpleUnifiedRephraseSlotIntegrator()
        self.decomposer = SubSlotDecomposer()
        self.test_results = []
        self.failed_tests = []
        
        print("🚀 体系的文法パターンテストシステム初期化完了")
    
    def run_comprehensive_test(self):
        """包括的な文法パターンテスト実行"""
        print("\n" + "="*80)
        print("🎯 体系的文法パターンテスト開始")
        print("="*80)
        
        # テストカテゴリ別に実行
        test_categories = [
            ("基本文型テスト", self.test_basic_sentence_patterns),
            ("仮定法テスト", self.test_subjunctive_patterns),
            ("完了時制テスト", self.test_perfect_tense_patterns),
            ("受動態テスト", self.test_passive_voice_patterns),
            ("受動態混在テスト", self.test_mixed_passive_patterns),
            ("複合関係節テスト", self.test_complex_relative_clauses),
            ("複合副詞節テスト", self.test_complex_adverbial_clauses),
            ("使役動詞テスト", self.test_causative_verbs),
            ("Multi Cooperativeテスト", self.test_multi_cooperative)
        ]
        
        total_passed = 0
        total_tests = 0
        
        for category_name, test_function in test_categories:
            print(f"\n📋 {category_name}")
            print("-" * 50)
            
            passed, total = test_function()
            total_passed += passed
            total_tests += total
            
            success_rate = (passed / total * 100) if total > 0 else 0
            print(f"✅ {category_name}: {passed}/{total} ({success_rate:.1f}%)")
        
        # 総合結果
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print("\n" + "="*80)
        print(f"🎯 総合結果: {total_passed}/{total_tests} ({overall_success_rate:.1f}%)")
        
        if overall_success_rate >= 95:
            print("🎉 優秀！システムは高い完璧性を維持しています")
        elif overall_success_rate >= 90:
            print("✅ 良好！わずかな改善で完璧性に達します")
        elif overall_success_rate >= 80:
            print("⚠️ 改善必要！重要なエラーが存在します")
        else:
            print("❌ 重大問題！システムの見直しが必要です")
        
        # 失敗テストの詳細表示
        if self.failed_tests:
            print(f"\n❌ 失敗テスト詳細 ({len(self.failed_tests)}件):")
            for i, (sentence, expected, actual, error) in enumerate(self.failed_tests[:5], 1):
                print(f"\n{i}. 「{sentence}」")
                print(f"   期待: {expected}")
                print(f"   実際: {actual}")
                print(f"   理由: {error}")
        
        return overall_success_rate
    
    def test_single_sentence(self, sentence, expected_slots=None, description=""):
        """単一例文のテスト実行"""
        try:
            print(f"🔍 テスト: {sentence}")
            
            # Step 1: 統合分解
            main_result = self.integrator.process(sentence)
            
            if not main_result or 'slots' not in main_result:
                raise Exception("統合分解失敗")
            
            main_slots = main_result['slots']
            
            # Step 2: サブスロット分解
            sub_slot_results = self.decomposer.decompose_complex_slots(main_slots)
            
            print(f"✅ {description}: 分解成功")
            
            # メインスロット表示
            occupied_main_slots = {k: v for k, v in main_slots.items() if v}
            print(f"   メイン: {occupied_main_slots}")
            
            # サブスロット表示
            if sub_slot_results:
                for slot_name, sub_results in sub_slot_results.items():
                    for sub_result in sub_results:
                        print(f"   サブ({slot_name}): {sub_result.sub_slots}")
            
            self.test_results.append({
                'sentence': sentence,
                'description': description,
                'success': True,
                'main_slots': main_slots,
                'sub_slots': sub_slot_results
            })
            
            return True
            
        except Exception as e:
            print(f"❌ {description}: {str(e)}")
            self.failed_tests.append((sentence, expected_slots, "解析エラー", str(e)))
            
            self.test_results.append({
                'sentence': sentence,
                'description': description,
                'success': False,
                'error': str(e)
            })
            
            return False
    
    def test_basic_sentence_patterns(self):
        """基本文型パターンテスト"""
        test_cases = [
            ("I run fast.", "第1文型 + 副詞"),
            ("She is beautiful.", "第2文型"),
            ("He gave me a book.", "第4文型"),
            ("We made him happy.", "第5文型"),
            ("There are many students.", "存在文"),
            ("Give me the book!", "命令文"),
            ("Don't go home!", "否定命令文"),
            ("What did you buy?", "疑問文"),
            ("How beautiful she is!", "感嘆文")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_subjunctive_patterns(self):
        """仮定法パターンテスト"""
        test_cases = [
            ("If I had known that, I would have helped.", "仮定法過去完了"),
            ("If I were you, I would go.", "仮定法過去"),
            ("Were he to arrive early, we could start.", "倒置仮定法"),
            ("Should you need help, call me.", "Should倒置"),
            ("I wish I could fly.", "願望のwish"),
            ("It's time we went home.", "It's time仮定法"),
            ("If only he were here!", "If only仮定法"),
            ("I would rather you stayed.", "would rather仮定法")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_perfect_tense_patterns(self):
        """完了時制パターンテスト"""
        test_cases = [
            ("I have finished my work.", "現在完了"),
            ("She had left before I arrived.", "過去完了"),
            ("We will have completed by tomorrow.", "未来完了"),
            ("Having been completed, the project was approved.", "完了分詞構文"),
            ("By the time she arrives, I will have left.", "時制の一致"),
            ("I have been working here for five years.", "現在完了進行形"),
            ("She had been studying when I called.", "過去完了進行形"),
            ("They will have been traveling for hours.", "未来完了進行形")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_passive_voice_patterns(self):
        """受動態パターンテスト"""
        test_cases = [
            ("The book was written by him.", "基本受動態"),
            ("The project is being developed.", "進行形受動態"),
            ("The work has been completed.", "完了形受動態"),
            ("The letter will be sent tomorrow.", "未来受動態"),
            ("Being told the truth, she was shocked.", "受動分詞構文"),
            ("To be considered seriously, prepare well.", "不定詞受動態"),
            ("Having been informed, we took action.", "完了受動分詞構文"),
            ("The problem needs to be solved.", "need受動態")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_mixed_passive_patterns(self):
        """受動態混在パターンテスト"""
        test_cases = [
            ("The book that was written by him is popular.", "関係詞 + 受動態"),
            ("Having been told the truth, she decided to leave.", "受動分詞 + 不定詞"),
            ("The project being developed will be finished soon.", "受動進行形 + 未来受動"),
            ("Because the work had been completed, we celebrated.", "理由節 + 過去完了受動"),
            ("If the letter is sent tomorrow, we will receive it.", "条件節 + 受動態"),
            ("While being interviewed, she remained calm.", "時間節 + 受動進行形"),
            ("The problem to be solved needs careful attention.", "不定詞受動 + 能動態"),
            ("After having been informed, we were asked to respond.", "完了受動分詞 + 受動態")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_complex_relative_clauses(self):
        """複合関係節パターンテスト"""
        test_cases = [
            ("The person who knows someone who can help us is here.", "二重関係節"),
            ("The book which I bought yesterday is interesting.", "目的格関係代名詞"),
            ("The place where we met is special.", "関係副詞where"),
            ("The time when everything changed was difficult.", "関係副詞when"),
            ("The reason why he left is unknown.", "関係副詞why"),
            ("What he said was surprising.", "関係代名詞what"),
            ("Those who work hard will succeed.", "先行詞those"),
            ("All that glitters is not gold.", "先行詞all + that")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_complex_adverbial_clauses(self):
        """複合副詞節パターンテスト"""
        test_cases = [
            ("Because although when the meeting starts, I am busy, I cannot attend.", "三重副詞節"),
            ("While studying hard, she also worked part-time.", "時間節 + 並列"),
            ("If even though since you are tired, you want to continue, I will help.", "条件 + 譲歩 + 理由"),
            ("After before during the vacation, we planned our trip.", "時間副詞節の連続"),
            ("Since when where problems occur, solutions emerge.", "理由 + 時間 + 場所"),
            ("Unless until after you finish, don't leave.", "条件 + 時間の重複"),
            ("Whether because although it rains, we will go.", "選択 + 理由 + 譲歩"),
            ("As soon as while before the show ends, leave quietly.", "時間節の複合")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_causative_verbs(self):
        """使役動詞テスト"""
        test_cases = [
            ("I made him study hard.", "make使役"),
            ("She let me go home.", "let使役"),
            ("We had the car repaired.", "have使役"),
            ("He helped me carry the bag.", "help使役"),
            ("I got her to agree.", "get使役"),
            ("The teacher made us rewrite the essay.", "make + 複合目的語"),
            ("Don't let them know the truth.", "否定 + let使役"),
            ("I had my hair cut yesterday.", "have + 過去分詞"),
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def test_multi_cooperative(self):
        """Multi Cooperative システム動作テスト"""
        test_cases = [
            ("The students who were studying in the library have been working on the project that was assigned last week.", "Multi Cooperative Level 3"),
            ("Because she was tired after working all day, she went to bed early without eating dinner.", "Multi Cooperative Level 2"),
            ("If the weather had been better, we would have gone to the beach where we usually meet our friends.", "Multi Cooperative Level 3"),
            ("The book that I bought yesterday, which cost fifty dollars, was written by an author whom I met last year.", "Multi Cooperative Level 4"),
            ("Having been told that the meeting was cancelled, we decided to go home early, but we found that the office was still busy.", "Multi Cooperative Level 4"),
            ("When the project manager who had been working overtime finally finished the report that needed to be submitted, everyone was relieved.", "Multi Cooperative Level 5")
        ]
        
        passed = 0
        for sentence, description in test_cases:
            if self.test_single_sentence(sentence, description=description):
                passed += 1
        
        return passed, len(test_cases)
    
    def generate_test_report(self, filename="systematic_grammar_test_report.txt"):
        """テストレポート生成"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🎯 体系的文法パターンテスト レポート\n")
            f.write(f"実行日時: {sys.version}\n")
            f.write("=" * 80 + "\n\n")
            
            # 成功テスト
            successful_tests = [t for t in self.test_results if t['success']]
            f.write(f"✅ 成功テスト: {len(successful_tests)}件\n\n")
            
            for i, test in enumerate(successful_tests[:10], 1):  # 最初の10件を表示
                f.write(f"{i}. {test['sentence']}\n")
                f.write(f"   説明: {test['description']}\n")
                f.write(f"   メイン: {test.get('main_slots', {})}\n")
                f.write(f"   サブ: {test.get('sub_slots', {})}\n\n")
            
            # 失敗テスト
            failed_tests = [t for t in self.test_results if not t['success']]
            f.write(f"❌ 失敗テスト: {len(failed_tests)}件\n\n")
            
            for i, test in enumerate(failed_tests, 1):
                f.write(f"{i}. {test['sentence']}\n")
                f.write(f"   説明: {test['description']}\n")
                f.write(f"   エラー: {test.get('error', '不明')}\n\n")
        
        print(f"📄 テストレポート生成完了: {filename}")

def main():
    """メイン実行関数"""
    tester = SystematicGrammarTest()
    
    # 包括テスト実行
    success_rate = tester.run_comprehensive_test()
    
    # レポート生成
    tester.generate_test_report()
    
    print(f"\n🎯 最終成功率: {success_rate:.1f}%")
    
    return success_rate >= 95  # 95%以上で成功とみなす

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
