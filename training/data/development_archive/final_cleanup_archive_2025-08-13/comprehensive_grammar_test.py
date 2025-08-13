#!/usr/bin/env python3
"""
Grammar Engine Success Examples Comprehensive Test
=================================================
各文法エンジンが開発時に成功した典型的例文を包括テスト

登録エンジン (15個):
1. Basic Five Pattern (基本5文型)
2. Modal (法助動詞)  
3. Conjunction (接続詞)
4. Relative (関係節)
5. Passive (受動態)
6. Progressive (進行時制)
7. Prepositional (前置詞句)
8. Perfect Progressive (完了進行)
9. Subjunctive (仮定法)
10. Inversion (倒置)
11. Comparative (比較級)
12. Gerund (動名詞)
13. Participle (分詞)
14. Infinitive (不定詞)
15. Question (疑問文)
"""

from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType
import time

class ComprehensiveGrammarTest:
    def __init__(self):
        self.controller = GrammarMasterControllerV2()
        self.test_results = {
            'total_tests': 0,
            'successful_tests': 0,
            'failed_tests': [],
            'engine_specific_results': {},
            'processing_times': []
        }
        
        # 各エンジンの開発時成功例文
        self.success_examples = {
            EngineType.BASIC_FIVE: [
                "The cat sits.",                                    # SV
                "John reads books.",                                # SVO
                "She is beautiful.",                               # SVC
                "I gave him a gift.",                              # SVOO
                "They made him captain."                           # SVOC
            ],
            
            EngineType.MODAL: [
                "You can swim.",                                   # 可能
                "She should study harder.",                        # 義務・助言
                "We might go tomorrow.",                           # 推量
                "I must finish this work.",                        # 必要性
                "He would help if asked."                          # 仮定的意志
            ],
            
            EngineType.CONJUNCTION: [
                "I study because I want to learn.",               # 理由
                "Although it was raining, we went out.",          # 譲歩
                "She sings while she works.",                     # 同時
                "Since you are here, let's start.",              # 理由・時
                "If you come early, we can talk."                # 条件
            ],
            
            EngineType.RELATIVE: [
                "The book that I bought is interesting.",         # 制限的関係節
                "My friend who lives in Tokyo called me.",        # 主格関係代名詞
                "The house which we visited was old.",            # 目的格関係代名詞
                "The place where we met was crowded.",            # 関係副詞
                "The day when he arrived was sunny."              # 時の関係副詞
            ],
            
            EngineType.PASSIVE: [
                "The book was written by Shakespeare.",           # 基本受動態
                "The project has been completed.",                # 完了受動態
                "English is spoken worldwide.",                   # 現在受動態
                "The letter will be delivered tomorrow.",         # 未来受動態
                "Mistakes are being corrected."                   # 進行受動態
            ],
            
            EngineType.PROGRESSIVE: [
                "She is reading a book now.",                     # 現在進行
                "They were playing soccer yesterday.",            # 過去進行
                "We will be traveling next week.",               # 未来進行
                "I am studying English these days.",             # 継続的行動
                "He was working when I called."                  # 過去の継続動作
            ],
            
            EngineType.PREPOSITIONAL: [
                "The book is on the table.",                      # 場所
                "We arrived at the station.",                     # 到着地点
                "She studies in the library.",                    # 場所
                "They walked through the park.",                  # 通過
                "He works with great enthusiasm."                # 手段・方法
            ],
            
            EngineType.PERFECT_PROGRESSIVE: [
                "I have been studying for three hours.",          # 現在完了進行
                "She had been working before the meeting.",       # 過去完了進行
                "They will have been traveling for a week.",     # 未来完了進行
                "We have been waiting since morning.",           # 継続期間
                "He had been reading when she arrived."          # 過去の継続完了
            ],
            
            EngineType.SUBJUNCTIVE: [
                "If I were rich, I would travel the world.",      # 仮定法過去
                "I wish I were taller.",                          # 願望の仮定法
                "If he had studied, he would have passed.",      # 仮定法過去完了
                "She acts as if she were the boss.",             # as if の仮定法
                "I suggest that he be more careful."             # 提案の仮定法
            ],
            
            EngineType.INVERSION: [
                "Never have I seen such beauty.",                # 否定語の倒置
                "Rarely does she complain about work.",          # 頻度副詞の倒置
                "Not only did he win, but he also broke records.", # Not only の倒置
                "Hardly had we arrived when it started raining.", # Hardly の倒置
                "Seldom do we see such dedication."              # 頻度副詞の倒置
            ],
            
            EngineType.COMPARATIVE: [
                "This book is more interesting than that one.",   # 比較級
                "She is the most talented student in class.",     # 最上級
                "He runs faster than his brother.",              # 副詞比較級
                "This is the best movie I have ever seen.",      # 不規則最上級
                "The more you practice, the better you become."  # The more... the more
            ],
            
            EngineType.GERUND: [
                "Swimming is my favorite hobby.",                 # 主語の動名詞
                "I enjoy reading books.",                         # 目的語の動名詞
                "She is good at cooking.",                        # 前置詞の目的語
                "Thank you for helping me.",                      # 感謝表現の動名詞
                "I am looking forward to meeting you."           # look forward to
            ],
            
            EngineType.PARTICIPLE: [
                "The running water is clean.",                    # 現在分詞の形容詞用法
                "I found the book very interesting.",            # 現在分詞の補語
                "The broken window needs repair.",               # 過去分詞の形容詞用法
                "Walking in the park, I met an old friend.",     # 分詞構文
                "Having finished homework, she went to bed."     # 完了分詞構文
            ],
            
            EngineType.INFINITIVE: [
                "I want to learn English.",                       # 目的語不定詞
                "She decided to go abroad.",                      # 決定の不定詞
                "It is important to be honest.",                  # 主語の不定詞
                "I have something to tell you.",                  # 形容詞的用法
                "He came here to study."                         # 目的の不定詞
            ],
            
            EngineType.QUESTION: [
                "What time is it?",                               # 疑問詞疑問文
                "Where do you live?",                            # 場所の疑問
                "How are you feeling today?",                    # 様態の疑問
                "Did you finish your homework?",                 # Yes/No疑問文
                "Who called you last night?"                     # 主語の疑問
            ]
        }

    def run_comprehensive_test(self):
        """全エンジンの成功例文を包括テスト"""
        print("🎯 COMPREHENSIVE GRAMMAR ENGINE SUCCESS EXAMPLES TEST")
        print("=" * 70)
        
        for engine_type, examples in self.success_examples.items():
            print(f"\n📚 Testing {engine_type.value.upper()} Engine:")
            print("-" * 50)
            
            engine_results = {
                'total': len(examples),
                'successful': 0,
                'failed': 0,
                'examples': []
            }
            
            for i, sentence in enumerate(examples, 1):
                start_time = time.time()
                
                try:
                    result = self.controller.process_sentence(sentence)
                    processing_time = time.time() - start_time
                    
                    success = result.success and (result.slots if hasattr(result, 'slots') else True)
                    
                    if success:
                        engine_results['successful'] += 1
                        self.test_results['successful_tests'] += 1
                        status = "✅ PASS"
                    else:
                        engine_results['failed'] += 1
                        self.test_results['failed_tests'].append({
                            'engine': engine_type.value,
                            'sentence': sentence,
                            'error': getattr(result, 'error', 'No slots extracted')
                        })
                        status = "❌ FAIL"
                    
                    print(f"  {i}. {sentence}")
                    print(f"     {status} | Time: {processing_time:.3f}s | Slots: {len(result.slots) if hasattr(result, 'slots') and result.slots else 0}")
                    
                    engine_results['examples'].append({
                        'sentence': sentence,
                        'success': success,
                        'processing_time': processing_time,
                        'slots_count': len(result.slots) if hasattr(result, 'slots') and result.slots else 0
                    })
                    
                    self.test_results['processing_times'].append(processing_time)
                    
                except Exception as e:
                    engine_results['failed'] += 1
                    self.test_results['failed_tests'].append({
                        'engine': engine_type.value,
                        'sentence': sentence,
                        'error': str(e)
                    })
                    print(f"  {i}. {sentence}")
                    print(f"     ❌ ERROR | {str(e)}")
                
                self.test_results['total_tests'] += 1
            
            # エンジン別結果サマリー
            success_rate = (engine_results['successful'] / engine_results['total']) * 100
            print(f"\n  📊 {engine_type.value} Summary: {engine_results['successful']}/{engine_results['total']} ({success_rate:.1f}%)")
            
            self.test_results['engine_specific_results'][engine_type.value] = engine_results

    def print_final_summary(self):
        """最終テスト結果サマリー"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 70)
        
        total = self.test_results['total_tests']
        successful = self.test_results['successful_tests']
        failed = total - successful
        success_rate = (successful / total * 100) if total > 0 else 0
        
        print(f"🎯 Overall Results:")
        print(f"   Total Tests: {total}")
        print(f"   Successful: {successful} ({success_rate:.1f}%)")
        print(f"   Failed: {failed}")
        
        if self.test_results['processing_times']:
            avg_time = sum(self.test_results['processing_times']) / len(self.test_results['processing_times'])
            print(f"   Average Processing Time: {avg_time:.3f}s")
        
        print(f"\n📚 Engine-Specific Success Rates:")
        for engine_name, results in self.test_results['engine_specific_results'].items():
            rate = (results['successful'] / results['total']) * 100
            print(f"   {engine_name:20}: {results['successful']:2}/{results['total']:2} ({rate:5.1f}%)")
        
        if self.test_results['failed_tests']:
            print(f"\n⚠️  Failed Tests ({len(self.test_results['failed_tests'])}):")
            for failure in self.test_results['failed_tests']:
                print(f"   {failure['engine']:15}: {failure['sentence']}")
                print(f"   {'':17}  → {failure['error']}")
        
        print("\n🎉 COMPREHENSIVE GRAMMAR ENGINE TEST COMPLETED")
        print("=" * 70)

def main():
    """メイン実行関数"""
    tester = ComprehensiveGrammarTest()
    tester.run_comprehensive_test()
    tester.print_final_summary()

if __name__ == "__main__":
    main()
